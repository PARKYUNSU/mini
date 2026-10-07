#!/usr/bin/env python3
"""BM25 주입의 배치 경로와 논문별 필터 검색 경로가 같은 청크·거리를 내는지 확인한다.

  .venv/bin/python scripts/diag_union_equivalence.py A035 A063 C1_01
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EVAL_SET = Path(__file__).resolve().parent.parent / "docs" / "experiments" / "retrieval_eval_1007" / "eval_set.jsonl"


def main() -> int:
    rows = {json.loads(l)["id"]: json.loads(l) for l in EVAL_SET.read_text().splitlines() if l.strip()}
    import chromadb
    from chromadb.config import Settings
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    import core.rag.agent_chroma_rag as R
    from core.config.agent_config import BM25_UNION_CHUNKS_PER_PAPER, BM25_UNION_TOP_M, CHROMA_DB_DIR, EMBEDDING_MODEL
    from core.rag.bm25_index import get_bm25_searcher
    from core.rag.query_expansion import expand_query_for_bm25

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR), settings=Settings(anonymized_telemetry=False))
    ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True)
    col = client.get_collection("arxiv_papers", embedding_function=ef)
    bm25 = get_bm25_searcher()
    worst = 0.0
    for qid in sys.argv[1:]:
        q = rows[qid]["query"]
        vq = col.query(query_texts=[q], n_results=200, include=["documents", "metadatas", "distances"])
        d0, m0, x0 = R._parse_chroma_query_result_row(vq)
        hits = bm25.search(expand_query_for_bm25(q), top_k=BM25_UNION_TOP_M)
        kw = dict(top_m=BM25_UNION_TOP_M, chunks_per_paper=BM25_UNION_CHUNKS_PER_PAPER, query_text=q)
        t = time.time()
        a = R._merge_bm25_union_chunks(col, hits, list(d0), list(m0), list(x0), **kw)
        ta = time.time() - t
        orig = R._nearest_chunks_per_paper_batched
        R._nearest_chunks_per_paper_batched = lambda *a_, **k_: None
        t = time.time()
        b = R._merge_bm25_union_chunks(col, hits, list(d0), list(m0), list(x0), **kw)
        tb = time.time() - t
        R._nearest_chunks_per_paper_batched = orig
        same_docs = a[0] == b[0]
        dd = max((abs(p - r) for p, r in zip(a[2], b[2]) if p is not None and r is not None), default=0.0)
        worst = max(worst, dd)
        print(f"{qid}: injected {a[3]} vs {b[3]} · same chunks={same_docs} · max|Δdist|={dd:.2e} · batched {ta:.1f}s vs per-paper {tb:.1f}s")
    print(f"WORST max|Δdist|={worst:.2e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
