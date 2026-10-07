#!/usr/bin/env python3
"""운영 검색 경로가 정답 논문을 어느 단계에서 잃는지 단계별 순위로 추적한다.

retrieval_eval_1007 에서 production 이 놓친 문항용. 단계마다 정답의 '논문 순위'를 찍는다.

  .venv/bin/python scripts/diag_production_drop.py A035 C2_03 C1_06

단계:
  bm25_raw      : BM25(질의 그대로) 논문 순위
  bm25_expanded : BM25(운영처럼 expand_query_for_bm25 꼬리 붙임) 논문 순위
  vector        : 벡터 fetch_n 청크를 논문 단위로 중복 제거한 순위
  pool          : 후보 풀(벡터 + BM25 union) 안에 정답 청크 수
  hybrid        : 청크 하이브리드 점수 → 논문 집계 + 제목 보정 후 순위 (light rerank 전)
  final         : light rerank 까지 끝난 운영 최종 순위
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROOT = Path(__file__).resolve().parent.parent
EVAL_SET = ROOT / "docs" / "experiments" / "retrieval_eval_1007" / "eval_set.jsonl"


def npid(p: str) -> str:
    return re.sub(r"v\d+$", "", (p or "").strip())


def rank_of(pids: list[str], gold: set[str]) -> int | None:
    return next((i + 1 for i, p in enumerate(pids) if npid(p) in gold), None)


def main() -> int:
    ids = sys.argv[1:]
    rows = {json.loads(l)["id"]: json.loads(l) for l in EVAL_SET.read_text().splitlines() if l.strip()}

    import chromadb
    from chromadb.config import Settings
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    import core.rag.agent_chroma_rag as R
    from core.config.agent_config import CHROMA_DB_DIR, CHROMA_FETCH_MIN, CHROMA_FETCH_MULTIPLIER, EMBEDDING_MODEL
    from core.rag.bm25_index import get_bm25_searcher
    from core.rag.query_expansion import expand_query_for_bm25

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR), settings=Settings(anonymized_telemetry=False))
    ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True)
    col = client.get_collection("arxiv_papers", embedding_function=ef)
    bm25 = get_bm25_searcher()
    fetch_n = int(max(10 * CHROMA_FETCH_MULTIPLIER, CHROMA_FETCH_MIN))

    out = []
    for qid in ids:
        r = rows[qid]
        q = r["query"]
        gold = {npid(p) for p in r["relevant_papers"]}
        res: dict = {"id": qid, "query": q, "gold": sorted(gold)}

        res["bm25_raw"] = rank_of([h["paper_id"] for h in bm25.search(q, top_k=200)], gold)
        qx = expand_query_for_bm25(q)
        res["bm25_expanded"] = rank_of([h["paper_id"] for h in bm25.search(qx, top_k=200)], gold)

        vq = col.query(query_texts=[q], n_results=fetch_n, include=["metadatas"])
        seen: list[str] = []
        for m in vq["metadatas"][0]:
            p = npid(m.get("paper_id", ""))
            if p not in seen:
                seen.append(p)
        res["vector"] = rank_of(seen, gold)

        docs, metas, dists, bm25_pid, _raw, _pre = R._hybrid_retrieve_candidate_pool(col, q, fetch_n=fetch_n, lock=None)
        res["pool_gold_chunks"] = sum(npid(m.get("paper_id", "")) in gold for m in metas)
        res["pool_papers"] = len({npid(m.get("paper_id", "")) for m in metas})
        cs = R._compute_hybrid_chunk_scores(metas, dists, bm25_pid, title_boost_query=q)
        ranked = R._compute_paper_ranking_rows(docs, metas, dists, cs, title_query=q)
        res["hybrid"] = rank_of([x["paper_id"] for x in ranked], gold)
        g = next((x for x in ranked if x["paper_id"] in gold), None)
        if g:
            res["gold_bm25_score"] = round(bm25_pid.get(g["paper_id"], 0.0), 3)
            res["gold_title_sim"] = round(g["title_sim"], 3)
        res["top_bm25_score_in_pool"] = round(max(bm25_pid.values(), default=0.0), 3)

        final = R.hybrid_retrieve_paper_ids_for_eval(col, q, fetch_n=fetch_n, top_k=50)
        res["final"] = rank_of(final, gold)
        out.append(res)

    print("\n=== TRACE ===")
    for res in out:
        print(json.dumps(res, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
