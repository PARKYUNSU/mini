#!/usr/bin/env python3
"""RAG 검색 품질 정량 평가 스크립트.

Recall@K, Precision@1, MRR 세 가지 지표로 ChromaDB 벡터 검색 품질을 측정합니다.
평가 데이터는 DB에 실제 존재하는 논문 paper_id를 기반으로 자동 생성합니다.

청킹·노이즈 필터를 바꾼 뒤에는 반드시 재인덱싱 후 측정해야 수치가 의미 있다.
    .venv/bin/python rebuild_chroma_clean.py --wipe-db

사용법:
    cd /Volumes/T7\ Shield/mini
    .venv/bin/python3 scripts/eval_rag_quality.py
"""

import json
import os
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import CrossEncoder

# ============================================================
# 평가 데이터: query + 정답 paper_id 매핑
# DB에 실제 존재하는 논문 기준으로 작성.
# 2312.10997(RAG 서베이) 단일 논문 편향을 줄이기 위해 다수 쿼리는 다른 paper_id로 교체됨.
# ============================================================

EVAL_DATA = [
    # --- RAG 관련 ---
    {
        "query": "retrieval augmented generation survey",
        "relevant_papers": ["2312.10997"],  # RAG for LLMs: A Survey
    },
    {
        "query": "RAG retrieval accuracy improvement",
        "relevant_papers": ["2407.08223", "2408.02545"],  # Speculative RAG, RAG Foundry
    },
    {
        "query": "hallucination mitigation in RAG systems",
        "relevant_papers": ["2409.10102"],  # Trustworthiness in RAG
    },
    {
        "query": "RAG evaluation benchmark",
        "relevant_papers": ["2407.11005", "2405.07437"],  # RAGBench, Evaluation of RAG Survey
    },
    {
        "query": "retrieval augmented generation for question answering",
        "relevant_papers": ["2604.02259"],  # RAG QA for EIC (서베이 ID 편향 완화)
    },
    {
        "query": "discourse aware retrieval augmented generation",
        "relevant_papers": ["2601.04377"],  # Disco-RAG
    },
    {
        "query": "RAG playground evaluation framework",
        "relevant_papers": ["2412.12322"],  # RAG Playground
    },
    {
        "query": "enterprise RAG optimization content design",
        "relevant_papers": ["2410.12812"],  # Enterprise RAG
    },
    {
        "query": "medical RAG benchmarking",
        "relevant_papers": ["2402.13178"],  # Benchmarking RAG for Medicine
    },
    {
        "query": "knowledge oriented retrieval augmented generation",
        "relevant_papers": ["2503.10677"],  # Knowledge-Oriented RAG Survey
    },
    # --- Transformer / Attention ---
    {
        "query": "transformer self attention mechanism neural network",
        "relevant_papers": ["1706.03762"],  # Attention Is All You Need
    },
    {
        "query": "anomalous attention distribution in transformers",
        "relevant_papers": ["2407.01601"],  # Anomalous Attention Distribution
    },
    {
        "query": "vision transformer image classification",
        "relevant_papers": ["2412.16188"],  # Decade of Deep Learning
    },
    # --- LLM / Agent ---
    {
        "query": "large language model autonomous agents survey",
        "relevant_papers": ["2407.01603"],  # LLM Agents in Chemistry
    },
    {
        "query": "foundation agents brain inspired AI",
        "relevant_papers": ["2504.01990"],  # Foundation Agents
    },
    {
        "query": "fairness bias in large language models",
        "relevant_papers": ["2404.01349"],  # Fairness in LLMs Taxonomic Survey
    },
    # --- Hard Queries (의도적으로 어렵게) ---
    {
        "query": "CRAG corrective retrieval augmented generation",
        "relevant_papers": ["2407.08223", "2407.11005"],  # Speculative RAG, RAGBench
    },
    {
        "query": "chunking optimization for retrieval systems",
        "relevant_papers": ["2601.15457"],  # Chunking Retrieval Re-ranking
    },
    {
        "query": "reranking cross encoder in retrieval pipeline",
        "relevant_papers": ["2601.15457"],  # Chunking + retrieval re-ranking
    },
    {
        "query": "speculative decoding draft verification parallel language model inference",
        "relevant_papers": ["2407.08223"],  # Speculative RAG
    },
    {
        "query": "ontology and knowledge graph grounded retrieval question answering",
        "relevant_papers": ["2412.15235"],  # OG-RAG
    },
    {
        "query": "query decomposition hybrid retrieval BM25",
        "relevant_papers": ["2601.15457"],  # Chunking / hybrid 파이프라인
    },
    {
        "query": "ontology grounded RAG knowledge graph",
        "relevant_papers": ["2412.15235"],  # OG-RAG
    },
    {
        "query": "accelerating retrieval augmented generation inference",
        "relevant_papers": ["2412.15246"],  # Accelerating RAG
    },
    {
        "query": "seven failure points RAG engineering",
        "relevant_papers": ["2401.05856"],  # Seven Failure Points
    },
]


def normalize_pid(pid: str) -> str:
    """paper_id에서 버전 접미사 제거: 2312.10997v5 → 2312.10997"""
    s = (pid or "").strip()
    if "v" in s:
        base, suffix = s.rsplit("v", 1)
        if suffix.isdigit() and base.replace(".", "").isdigit():
            return base
    return s


def evaluate_rag(collection, eval_data: list[dict], top_k: int = 5):
    """Recall@K, Precision@1, MRR 평가."""
    recall_total = 0
    precision1_total = 0
    mrr_total = 0
    details = []

    for item in eval_data:
        query = item["query"]
        relevant = {normalize_pid(p) for p in item["relevant_papers"]}

        result = collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["metadatas", "distances"],
        )

        metas = (result.get("metadatas") or [[]])[0]
        dists = (result.get("distances") or [[]])[0]

        retrieved_ids = []
        for meta in metas:
            pid = normalize_pid((meta.get("paper_id") or "").strip())
            retrieved_ids.append(pid)

        # Recall@K: 정답 중 하나라도 Top-K에 있으면 hit
        hit = any(r in relevant for r in retrieved_ids)
        recall_total += 1 if hit else 0

        # Precision@1: 1위가 정답인지
        if retrieved_ids and retrieved_ids[0] in relevant:
            precision1_total += 1

        # MRR: 첫 번째 정답의 역순위
        reciprocal_rank = 0.0
        for idx, rid in enumerate(retrieved_ids):
            if rid in relevant:
                reciprocal_rank = 1.0 / (idx + 1)
                break
        mrr_total += reciprocal_rank

        # 로그 출력
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"Expected: {relevant}")
        print("Retrieved:")
        for i, (rid, dist) in enumerate(zip(retrieved_ids, dists)):
            marker = " ✅" if rid in relevant else ""
            print(f"  #{i+1} | {rid} | dist={dist:.4f}{marker}")
        print(f"Hit@{top_k}: {'✅ O' if hit else '❌ X'} | RR={reciprocal_rank:.4f}")

        details.append({
            "query": query,
            "hit": hit,
            "precision1": retrieved_ids[0] in relevant if retrieved_ids else False,
            "rr": reciprocal_rank,
            "top1_pid": retrieved_ids[0] if retrieved_ids else "",
            "top1_dist": dists[0] if dists else None,
        })

    # 최종 결과
    n = len(eval_data)
    recall = recall_total / n
    precision1 = precision1_total / n
    mrr = mrr_total / n

    print(f"\n{'='*60}")
    print(f"{'='*60}")
    print(f"📊 RAG 검색 품질 평가 결과 (Top-K={top_k}, 평가 쿼리 {n}개)")
    print(f"{'='*60}")
    print(f"  Recall@{top_k}:   {recall:.4f}  {'✅ 양호' if recall >= 0.8 else '⚠️ 개선 필요' if recall >= 0.6 else '🔴 심각'}")
    print(f"  Precision@1: {precision1:.4f}  {'✅ 양호' if precision1 >= 0.6 else '⚠️ 개선 필요' if precision1 >= 0.4 else '🔴 심각'}")
    print(f"  MRR:         {mrr:.4f}  {'✅ 양호' if mrr >= 0.7 else '⚠️ 개선 필요' if mrr >= 0.5 else '🔴 심각'}")
    print(f"{'='*60}")

    # 실패 쿼리 요약
    missed = [d for d in details if not d["hit"]]
    if missed:
        print(f"\n❌ 미스 쿼리 ({len(missed)}개):")
        for d in missed:
            print(f"  - {d['query']}")
            print(f"    Top-1: {d['top1_pid']} (dist={d['top1_dist']:.4f})" if d["top1_dist"] else "")

    # 진단
    print(f"\n🧠 자동 진단:")
    if recall < 0.6:
        print("  → Recall 낮음: embedding 모델 또는 query-chunk semantic mismatch 문제 가능성")
    if recall >= 0.8 and precision1 < 0.5:
        print("  → Recall 높지만 Precision 낮음: reranker(cross-encoder) 도입 권장")
    if mrr < 0.5:
        print("  → MRR 낮음: 관련 문서가 뒤쪽에 위치. reranker 또는 chunking 개선 필요")
    if recall >= 0.8 and precision1 >= 0.6 and mrr >= 0.7:
        print("  → 전반적으로 양호! retrieval 단계는 OK. 필요 시 reranking 고도화 검토")

    return {"recall": recall, "precision1": precision1, "mrr": mrr, "details": details}


def cross_encoder_rerank_eval(
    ce: CrossEncoder,
    query: str,
    metas: list[dict],
    docs: list[str],
    dists: list[float],
    *,
    top_k: int = 5,
) -> tuple[list[str], list[dict], list[float]]:
    """Cross-encoder로 재정렬 + paper_id 다양성 보장."""
    if not docs:
        return [], [], []
    pairs = [(query, doc[:512]) for doc in docs]
    scores = ce.predict(pairs).tolist()
    indexed = sorted(enumerate(scores), key=lambda x: -x[1])

    first_per_paper: list[int] = []
    extra: list[int] = []
    seen: set[str] = set()
    for orig_idx, _ in indexed:
        pid = normalize_pid((metas[orig_idx].get("paper_id") or "").strip())
        if not pid or pid not in seen:
            if pid:
                seen.add(pid)
            first_per_paper.append(orig_idx)
        else:
            extra.append(orig_idx)
    final = (first_per_paper + extra)[:top_k]
    return (
        [metas[i].get("paper_id", "") for i in final],
        [metas[i] for i in final],
        [dists[i] if i < len(dists) else 0.0 for i in final],
    )


def evaluate_rag_with_rerank(collection, ce: CrossEncoder, eval_data: list[dict], top_k: int = 5, fetch_n: int = 30):
    """벡터 검색 → cross-encoder rerank → 평가."""
    recall_total = 0
    precision1_total = 0
    mrr_total = 0
    details = []

    for item in eval_data:
        query = item["query"]
        relevant = {normalize_pid(p) for p in item["relevant_papers"]}

        result = collection.query(
            query_texts=[query],
            n_results=fetch_n,
            include=["metadatas", "distances", "documents"],
        )
        metas = (result.get("metadatas") or [[]])[0]
        dists = (result.get("distances") or [[]])[0]
        docs = (result.get("documents") or [[]])[0]

        reranked_ids, reranked_metas, reranked_dists = cross_encoder_rerank_eval(
            ce, query, metas, docs, dists, top_k=top_k
        )
        retrieved_ids = [normalize_pid(pid) for pid in reranked_ids]

        hit = any(r in relevant for r in retrieved_ids)
        recall_total += 1 if hit else 0
        if retrieved_ids and retrieved_ids[0] in relevant:
            precision1_total += 1
        reciprocal_rank = 0.0
        for idx, rid in enumerate(retrieved_ids):
            if rid in relevant:
                reciprocal_rank = 1.0 / (idx + 1)
                break
        mrr_total += reciprocal_rank

        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"Expected: {relevant}")
        print("Retrieved (after cross-encoder rerank):")
        for i, rid in enumerate(retrieved_ids):
            marker = " ✅" if rid in relevant else ""
            print(f"  #{i+1} | {rid}{marker}")
        print(f"Hit@{top_k}: {'✅ O' if hit else '❌ X'} | RR={reciprocal_rank:.4f}")

        details.append({
            "query": query, "hit": hit,
            "precision1": retrieved_ids[0] in relevant if retrieved_ids else False,
            "rr": reciprocal_rank,
            "top1_pid": retrieved_ids[0] if retrieved_ids else "",
        })

    n = len(eval_data)
    recall = recall_total / n
    precision1 = precision1_total / n
    mrr = mrr_total / n

    print(f"\n{'='*60}")
    print(f"📊 [Cross-encoder Rerank] 평가 결과 (Top-K={top_k}, fetch_n={fetch_n}, 쿼리 {n}개)")
    print(f"{'='*60}")
    print(f"  Recall@{top_k}:   {recall:.4f}  {'✅ 양호' if recall >= 0.8 else '⚠️ 개선 필요' if recall >= 0.6 else '🔴 심각'}")
    print(f"  Precision@1: {precision1:.4f}  {'✅ 양호' if precision1 >= 0.6 else '⚠️ 개선 필요' if precision1 >= 0.4 else '🔴 심각'}")
    print(f"  MRR:         {mrr:.4f}  {'✅ 양호' if mrr >= 0.7 else '⚠️ 개선 필요' if mrr >= 0.5 else '🔴 심각'}")
    print(f"{'='*60}")

    missed = [d for d in details if not d["hit"]]
    if missed:
        print(f"\n❌ 미스 쿼리 ({len(missed)}개):")
        for d in missed:
            print(f"  - {d['query']}  (Top-1: {d['top1_pid']})")

    return {"recall": recall, "precision1": precision1, "mrr": mrr, "details": details}


def main():
    print("🔄 ChromaDB 연결 및 임베딩 모델 로드 중...")
    client = chromadb.PersistentClient(
        path="./chroma_db", settings=Settings(anonymized_telemetry=False)
    )
    from core.config.agent_config import EMBEDDING_MODEL
    print(f"  임베딩 모델: {EMBEDDING_MODEL}")
    ef = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL,
        device="cpu",
        normalize_embeddings=True,
    )
    collection = client.get_collection("arxiv_papers", embedding_function=ef)
    print(f"  DB 청크 수: {collection.count():,}")

    print(f"\n📋 평가 데이터: {len(EVAL_DATA)}개 쿼리")

    # ── 1단계: 벡터 검색만 (baseline) ──
    print("\n" + "🔵" * 30)
    print("🔵 [Baseline] 벡터 검색만 (cross-encoder 없음)")
    print("🔵" * 30)
    baseline = evaluate_rag(collection, EVAL_DATA, top_k=5)

    # ── 2단계: 벡터 검색 + cross-encoder rerank ──
    print("\n" + "🟢" * 30)
    print("🟢 [개선] 벡터 검색(30개) + Cross-encoder Rerank + 다양성 보장")
    print("🟢" * 30)
    print("  Cross-encoder 모델 로드 중...")
    ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    improved = evaluate_rag_with_rerank(collection, ce, EVAL_DATA, top_k=5, fetch_n=30)

    # ── 비교 요약 ──
    print("\n" + "=" * 60)
    print("📊 Before vs After 비교")
    print("=" * 60)
    print(f"  {'지표':<15} {'Baseline':>10} {'+ Rerank':>10} {'변화':>10}")
    print(f"  {'-'*45}")
    for metric in ["recall", "precision1", "mrr"]:
        b = baseline[metric]
        a = improved[metric]
        delta = a - b
        sign = "+" if delta > 0 else ""
        print(f"  {metric:<15} {b:>10.4f} {a:>10.4f} {sign}{delta:>9.4f}")
    print("=" * 60)

    # JSON 결과 저장
    out_path = Path("scripts/eval_rag_results.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({"baseline": baseline, "with_rerank": improved}, f, ensure_ascii=False, indent=2)
    print(f"\n💾 상세 결과 저장: {out_path}")


if __name__ == "__main__":
    main()
