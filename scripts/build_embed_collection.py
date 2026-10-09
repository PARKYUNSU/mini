#!/usr/bin/env python3
"""운영 Chroma 의 청크·메타데이터를 그대로 읽어 다른 임베더로 새 DB 에 다시 적재한다 (임베더 비교용).

설계·판정: docs/experiments/embedder_1009/README.md

  .venv/bin/python scripts/build_embed_collection.py \
      --model BAAI/bge-small-en-v1.5 --out "/Volumes/T7 Shield/mini-chroma-exp/bge_small"

- 운영 DB 는 읽기만 한다. 청크 텍스트·ID·메타데이터가 운영과 같으므로 바뀌는 것은 임베딩뿐이다.
- 이어서 하기: 새 DB 에 이미 있는 ID 는 건너뛴다 (중간에 끊겨도 다시 실행하면 된다).
"""
from __future__ import annotations

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True, help="새 PersistentClient 경로")
    ap.add_argument("--batch", type=int, default=2000, help="운영 DB 에서 한 번에 읽을 청크 수")
    ap.add_argument("--encode-batch", type=int, default=128)
    ap.add_argument("--limit", type=int, default=0, help="앞에서 N 청크만 (시험용)")
    args = ap.parse_args()

    import chromadb
    import torch
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer

    from core.config.agent_config import CHROMA_DB_DIR

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer(args.model, device=device)
    print(f"모델 {args.model} · dim {model.get_sentence_embedding_dimension()} · device {device}", flush=True)

    src = chromadb.PersistentClient(path=str(CHROMA_DB_DIR), settings=Settings(anonymized_telemetry=False))
    src_col = src.get_collection("arxiv_papers")
    total = src_col.count()
    os.makedirs(args.out, exist_ok=True)
    dst = chromadb.PersistentClient(path=args.out, settings=Settings(anonymized_telemetry=False))
    dst_col = dst.get_or_create_collection("arxiv_papers", metadata={"hnsw:space": "cosine"})
    print(f"원본 {total:,} 청크 → {args.out} (이미 {dst_col.count():,})", flush=True)

    target = min(total, args.limit) if args.limit else total
    t0 = time.time()
    done = 0
    offset = 0
    while offset < target:
        n = min(args.batch, target - offset)
        got = src_col.get(limit=n, offset=offset, include=["documents", "metadatas"])
        offset += n
        ids = got["ids"]
        have = set(dst_col.get(ids=ids, include=[])["ids"]) if ids else set()
        keep = [i for i, x in enumerate(ids) if x not in have]
        if keep:
            docs = [got["documents"][i] or "" for i in keep]
            embs = model.encode(docs, batch_size=args.encode_batch, normalize_embeddings=True,
                                show_progress_bar=False, convert_to_numpy=True)
            dst_col.add(
                ids=[ids[i] for i in keep],
                documents=docs,
                metadatas=[got["metadatas"][i] for i in keep],
                embeddings=embs.tolist(),
            )
        done = offset
        rate = done / max(time.time() - t0, 1e-6)
        print(f"{done:,}/{target:,} · {rate:.0f}/s · 남은 {((target - done) / max(rate, 1e-6)) / 60:.0f}분", flush=True)

    print(f"완료: 새 DB {dst_col.count():,} 청크 · {(time.time() - t0) / 60:.1f}분", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
