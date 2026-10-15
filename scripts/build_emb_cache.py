"""BM25 합집합 배치 get 용 로컬 임베딩 캐시 만들기 (docs/experiments/emb_cache_1015).

Chroma 컬렉션을 **읽기만** 해서(페이지 단위 get) 청크 임베딩을 논문별로 연속 배치한 memmap 으로 쓴다.
임시 폴더에 다 쓴 뒤 이름 바꾸기로 교체한다 — 쓰는 도중 검색이 반쯤 된 캐시를 읽지 않게.

    .venv/bin/python scripts/build_emb_cache.py            # 기본: <CHROMA_DB_DIR>_emb_cache
    .venv/bin/python scripts/build_emb_cache.py --out DIR --page 5000
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time

import numpy as np

sys.path.insert(0, os.getcwd())
from dotenv import load_dotenv  # noqa: E402

load_dotenv(".env")

from core.config.agent_config import CHROMA_DB_DIR, COLLECTION_NAME  # noqa: E402
from core.config.chroma_client import make_chroma_client  # noqa: E402
from core.rag.agent_chroma_rag import _normalize_pid, emb_cache_dir  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(emb_cache_dir()))
    ap.add_argument("--page", type=int, default=5000)
    args = ap.parse_args()

    col = make_chroma_client(str(CHROMA_DB_DIR)).get_collection(COLLECTION_NAME)
    total = col.count()
    print(f"컬렉션 {COLLECTION_NAME} 행 {total:,} → {args.out}", flush=True)

    tmp = args.out.rstrip("/") + ".tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    ids: list[str] = []
    pids: list[str] = []
    raw = None  # 받은 순서 그대로 디스크에 (float64 124만 행 = 3.8GB 를 메모리에 올리지 않는다)
    t0 = time.time()
    off = 0
    while off < total:
        g = col.get(include=["metadatas", "embeddings"], limit=args.page, offset=off)
        n = len(g["ids"])
        if n == 0:
            break
        # 클라이언트가 돌려주는 float64 그대로 (float32 로 줄이면 거리가 1e-9 단위로 달라진다 — emb_cache_1015 §5)
        e = np.asarray(g["embeddings"], dtype=np.float64)
        if raw is None:
            raw = np.lib.format.open_memmap(os.path.join(tmp, "raw.npy"), mode="w+", dtype=np.float64, shape=(total, e.shape[1]))
        raw[off : off + n] = e
        ids.extend(g["ids"])
        pids.extend(_normalize_pid(((m or {}).get("paper_id") or "").strip()) for m in g["metadatas"])
        off += n
        if (off // args.page) % 20 == 0 or off >= total:
            print(f"  {off:,}/{total:,} {time.time() - t0:.0f}s", flush=True)

    x = raw[:off] if raw is not None else np.zeros((0, 0), dtype=np.float64)
    keep = [i for i, p in enumerate(pids) if p]
    # 논문별로 연속 배치 (같은 논문 안에서는 Chroma 가 돌려준 순서 유지)
    order = sorted(keep, key=lambda i: (pids[i], i))
    index: dict[str, list[int]] = {}
    for row, i in enumerate(order):
        p = pids[i]
        if p in index:
            index[p][1] = row + 1
        else:
            index[p] = [row, row + 1]

    mm = np.lib.format.open_memmap(os.path.join(tmp, "emb.npy"), mode="w+", dtype=np.float64, shape=(len(order), x.shape[1]))
    for s in range(0, len(order), 100_000):
        mm[s : s + 100_000] = x[order[s : s + 100_000]]
    mm.flush()
    dim = int(x.shape[1])
    del mm, x, raw
    os.remove(os.path.join(tmp, "raw.npy"))
    np.save(os.path.join(tmp, "ids.npy"), np.array([ids[i] for i in order], dtype="S"))
    with open(os.path.join(tmp, "paper_index.json"), "w") as f:
        json.dump(index, f)
    with open(os.path.join(tmp, "meta.json"), "w") as f:
        json.dump({"rows": len(order), "dim": dim, "papers": len(index), "collection": COLLECTION_NAME,
                   "collection_rows": total, "skipped_no_pid": len(ids) - len(keep),
                   "built_at": time.strftime("%Y-%m-%d %H:%M:%S")}, f)

    old = args.out.rstrip("/") + ".old"
    shutil.rmtree(old, ignore_errors=True)
    if os.path.exists(args.out):
        os.rename(args.out, old)
    os.rename(tmp, args.out)
    shutil.rmtree(old, ignore_errors=True)
    print(f"완료: 행 {len(order):,} · 논문 {len(index):,} · {time.time() - t0:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
