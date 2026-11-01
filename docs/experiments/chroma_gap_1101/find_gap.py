"""BM25 색인(JSONL)에는 있는데 운영 Chroma 에 청크가 없는 논문 찾기.

1. Chroma SQLite 를 읽기 전용(``immutable=1``, 잠금 없음 — rebuild_chroma.py 와 같은 방식)으로 열어
   ``arxiv_papers`` 의 paper_id 목록을 색인으로 한 번에 읽는다. 서버를 거치지 않는다.
   (처음엔 논문마다 서버 get 을 했는데 대기열 논문은 한 번에 4~7초 · 서버 CPU 30~80% 라 2,000편에서 멈췄다.)
2. BM25 에만 있는 후보를 서버에 ``get(where={"paper_id": {"$in": 버전 후보}}, limit=1)`` 로 다시 확인한다.
3. 빠진 논문은 JSONL 어느 파일 몇째 줄에 있는지 · 본문/초록 길이를 같이 적는다(원인 나누기용).

    .venv/bin/python docs/experiments/chroma_gap_1101/find_gap.py --out docs/experiments/chroma_gap_1101/gap_before.jsonl
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction  # noqa: E402

from core.config.agent_config import CHROMA_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL  # noqa: E402
from core.config.chroma_client import make_chroma_client  # noqa: E402
from core.rag.agent_chroma_rag import _paper_id_version_candidates  # noqa: E402
from core.rag.bm25_index import BM25Searcher, _normalize_pid  # noqa: E402


def jsonl_files() -> list[Path]:
    """bm25_index._load 와 같은 순서."""
    files = sorted((ROOT / "raw_data_queue" / "processed").glob("crawled_papers*.jsonl"))
    main = ROOT / "raw_data_queue" / "crawled_papers.jsonl"
    return files + ([main] if main.exists() else [])


def chroma_paper_ids() -> tuple[set[str], int]:
    """(정규화 paper_id 집합, 청크 수) — 운영 컬렉션 메타데이터 세그먼트만."""
    con = sqlite3.connect(f"file:{Path(CHROMA_DB_DIR) / 'chroma.sqlite3'}?immutable=1", uri=True)
    seg, = con.execute(
        "SELECT s.id FROM segments s JOIN collections c ON s.collection = c.id WHERE c.name = ? AND s.scope = 'METADATA'",
        (COLLECTION_NAME,),
    ).fetchone()
    n, = con.execute("SELECT count(*) FROM embeddings WHERE segment_id = ?", (seg,)).fetchone()
    rows = con.execute(
        "SELECT DISTINCT m.string_value FROM embedding_metadata m JOIN embeddings e ON e.id = m.id "
        "WHERE m.key = 'paper_id' AND m.string_value IS NOT NULL AND e.segment_id = ?",
        (seg,),
    )
    ids = {_normalize_pid(v.strip()) for v, in rows if v and v.strip()}
    con.close()
    return ids, n


def describe(missing: set[str]) -> dict[str, dict]:
    """빠진 논문마다 JSONL 위치 · 길이 · 키."""
    out: dict[str, dict] = {}
    for f in jsonl_files():
        with f.open(encoding="utf-8", errors="replace") as fh:
            for ln, line in enumerate(fh, 1):
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pid = _normalize_pid((d.get("paper_id") or "").strip())
                if pid not in missing:
                    continue
                row = out.setdefault(pid, {"paper_id": pid, "where": []})
                row["where"].append(f"{f.relative_to(ROOT)}:{ln}")
                if "title" not in row:  # bm25_index 처럼 첫 줄 기준
                    row.update(
                        raw_id=d.get("paper_id"),
                        title=(d.get("title") or "").strip(),
                        published=d.get("published"),
                        abstract_chars=len((d.get("abstract") or d.get("summary") or "").strip()),
                        content_chars=len((d.get("content") or d.get("text") or "").strip()),
                        keys=sorted(d),
                    )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    t0 = time.time()
    s = BM25Searcher()
    s._load()
    pids = list(s._pid_to_idx)
    print(f"BM25 논문 {len(pids)}편 ({time.time() - t0:.0f}s)", flush=True)

    t1 = time.time()
    in_chroma, n_chunks = chroma_paper_ids()
    cands = [p for p in pids if p not in in_chroma]
    print(f"Chroma SQLite: 청크 {n_chunks:,} · 논문 {len(in_chroma):,} · Chroma 에만 {len(in_chroma - set(pids))} · "
          f"BM25 에만(후보) {len(cands)} · 처음 2,000편 중 후보 {sum(p not in in_chroma for p in pids[:2000])} "
          f"({time.time() - t1:.0f}s)", flush=True)

    ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True)
    col = make_chroma_client(CHROMA_DB_DIR).get_collection(name=COLLECTION_NAME, embedding_function=ef)
    missing: set[str] = set()
    errors: list[str] = []
    for pid in cands:
        where = {"paper_id": {"$in": _paper_id_version_candidates(pid)}}
        for attempt in range(3):
            try:
                if not col.get(where=where, limit=1, include=[])["ids"]:
                    missing.add(pid)
                break
            except Exception as e:  # 서버 일시 오류 — 두 번 더
                if attempt == 2:
                    errors.append(f"{pid}: {type(e).__name__}: {e}")
                time.sleep(2)
    print(f"서버 확인: 빠짐 {len(missing)} / 후보 {len(cands)} · 오류 {len(errors)}", flush=True)
    for e in errors:
        print("  오류", e)

    rows = describe(missing)
    with open(args.out, "w", encoding="utf-8") as f:
        for pid in sorted(rows):
            f.write(json.dumps(rows[pid], ensure_ascii=False) + "\n")
    print(f"저장 {args.out} ({len(rows)}편)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
