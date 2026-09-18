#!/usr/bin/env python3
"""Hybrid Retrieval (Vector + BM25 + Cross-encoder Rerank) 평가 스크립트.

Recall@K, Precision@1, MRR 세 가지 지표로 평가.
Baseline(벡터만) vs 레거시 Hybrid(min-max) vs **Production Hybrid**(RRF+논문+제목유사도) vs Hybrid+Rerank.

Chroma 청크 파이프라인을 바꾼 경우 먼저 재인덱싱:
    .venv/bin/python rebuild_chroma_clean.py --wipe-db

사용법:
    cd "/Volumes/T7 Shield/mini"
    .venv/bin/python3 scripts/eval_rag_hybrid.py
    .venv/bin/python3 scripts/eval_rag_hybrid.py --top-k-list 5,8,10,15
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import CrossEncoder

from core.config.agent_config import (
    BM25_UNION_TOP_M,
    CHROMA_DB_DIR,
    CHROMA_FETCH_MIN,
    CHROMA_FETCH_MULTIPLIER,
    EMBEDDING_MODEL,
    HYBRID_MULTI_QUERY_RETRIEVAL,
)
from core.rag.agent_chroma_rag import hybrid_retrieve_paper_ids_for_eval
from core.rag.bm25_index import HYBRID_BM25_WEIGHT, HYBRID_VECTOR_WEIGHT, get_bm25_searcher

# ============================================================
# 평가 데이터
# ============================================================
EVAL_DATA = [
    {"query": "retrieval augmented generation survey", "relevant_papers": ["2312.10997"]},
    {"query": "RAG retrieval accuracy improvement", "relevant_papers": ["2407.08223", "2408.02545"]},
    {"query": "hallucination mitigation in RAG systems", "relevant_papers": ["2409.10102"]},
    {"query": "RAG evaluation benchmark", "relevant_papers": ["2407.11005", "2405.07437"]},
    {"query": "retrieval augmented generation for question answering", "relevant_papers": ["2604.02259"]},
    {"query": "discourse aware retrieval augmented generation", "relevant_papers": ["2601.04377"]},
    {"query": "RAG playground evaluation framework", "relevant_papers": ["2412.12322"]},
    {"query": "enterprise RAG optimization content design", "relevant_papers": ["2410.12812"]},
    {"query": "medical RAG benchmarking", "relevant_papers": ["2402.13178"]},
    {"query": "knowledge oriented retrieval augmented generation", "relevant_papers": ["2503.10677"]},
    {"query": "transformer self attention mechanism neural network", "relevant_papers": ["1706.03762"]},
    {"query": "anomalous attention distribution in transformers", "relevant_papers": ["2407.01601"]},
    {"query": "vision transformer image classification", "relevant_papers": ["2412.16188"]},
    {"query": "large language model autonomous agents survey", "relevant_papers": ["2407.01603"]},
    {"query": "foundation agents brain inspired AI", "relevant_papers": ["2504.01990"]},
    {"query": "fairness bias in large language models", "relevant_papers": ["2404.01349"]},
    {"query": "CRAG corrective retrieval augmented generation", "relevant_papers": ["2407.08223", "2407.11005"]},
    {"query": "chunking optimization for retrieval systems", "relevant_papers": ["2601.15457"]},
    {"query": "reranking cross encoder in retrieval pipeline", "relevant_papers": ["2601.15457"]},
    {"query": "speculative decoding draft verification parallel language model inference", "relevant_papers": ["2407.08223"]},
    {"query": "ontology and knowledge graph grounded retrieval question answering", "relevant_papers": ["2412.15235"]},
    {"query": "query decomposition hybrid retrieval BM25", "relevant_papers": ["2601.15457"]},
    {"query": "ontology grounded RAG knowledge graph", "relevant_papers": ["2412.15235"]},
    {"query": "accelerating retrieval augmented generation inference", "relevant_papers": ["2412.15246"]},
    {"query": "seven failure points RAG engineering", "relevant_papers": ["2401.05856"]},
]


def normalize_pid(pid: str) -> str:
    s = (pid or "").strip()
    if "v" in s:
        base, suffix = s.rsplit("v", 1)
        if suffix.isdigit() and base.replace(".", "").isdigit():
            return base
    return s


def calc_metrics(eval_data, retrieved_per_query, top_k=5):
    """Calculate Recall@K, Precision@1, MRR."""
    recall_total = precision1_total = mrr_total = 0
    details = []
    for i, item in enumerate(eval_data):
        relevant = {normalize_pid(p) for p in item["relevant_papers"]}
        retrieved = retrieved_per_query[i][:top_k]
        hit = any(r in relevant for r in retrieved)
        recall_total += 1 if hit else 0
        if retrieved and retrieved[0] in relevant:
            precision1_total += 1
        rr = 0.0
        for idx, rid in enumerate(retrieved):
            if rid in relevant:
                rr = 1.0 / (idx + 1)
                break
        mrr_total += rr
        details.append({"query": item["query"], "hit": hit, "rr": rr, "top1": retrieved[0] if retrieved else ""})
    n = len(eval_data)
    return {
        "recall": recall_total / n,
        "precision1": precision1_total / n,
        "mrr": mrr_total / n,
        "details": details,
    }


def print_metrics(label, metrics, top_k=5):
    n = len(metrics["details"])
    r, p, m = metrics["recall"], metrics["precision1"], metrics["mrr"]
    print(f"\n{'='*60}")
    print(f"📊 [{label}] 평가 결과 (Top-K={top_k}, 쿼리 {n}개)")
    print(f"{'='*60}")
    print(f"  Recall@{top_k}:   {r:.4f}  {'✅' if r >= 0.75 else '⚠️' if r >= 0.6 else '🔴'}")
    print(f"  Precision@1: {p:.4f}  {'✅' if p >= 0.6 else '⚠️' if p >= 0.4 else '🔴'}")
    print(f"  MRR:         {m:.4f}  {'✅' if m >= 0.7 else '⚠️' if m >= 0.5 else '🔴'}")
    print(f"{'='*60}")
    missed = [d for d in metrics["details"] if not d["hit"]]
    if missed:
        print(f"\n❌ 미스 쿼리 ({len(missed)}개):")
        for d in missed:
            print(f"  - {d['query']}  (Top-1: {d['top1']})")


def classify_query_difficulty(query: str) -> str:
    """generic: 광범위 주제 / specific: 약어·구체 기법·도메인 키워드."""
    ql = (query or "").lower()
    if re.search(
        r"\b(crag|dpr|colbert|ragas|self[\s-]?rag|hyde|specter|ontology|"
        r"knowledge graph|speculative decoding|discourse aware)\b",
        ql,
    ):
        return "specific"
    if re.search(
        r"\b(rag|retrieval augmented|transformer|attention|large language model|llm|"
        r"benchmark|survey|neural network|vision transformer)\b",
        ql,
    ):
        return "generic"
    return "generic"


def legacy_minmax_pids_for_query(
    collection,
    query: str,
    bm25,
    *,
    vw: float,
    bw: float,
    fetch_n: int,
    top_k: int,
    bm25_top: int,
) -> list[str]:
    """레거시 벡터+BM25 min-max 하이브리드 후 논문 단위 top-k."""
    result = collection.query(
        query_texts=[query],
        n_results=fetch_n,
        include=["metadatas", "distances", "documents"],
    )
    metas = (result.get("metadatas") or [[]])[0]
    dists = (result.get("distances") or [[]])[0]

    bm25_hits = bm25.search(query, top_k=bm25_top)
    bm25_pid_scores: dict[str, float] = {}
    if bm25_hits:
        raw_bm25 = [h["bm25_score"] for h in bm25_hits]
        min_b, max_b = min(raw_bm25), max(raw_bm25)
        rng_b = max_b - min_b if max_b > min_b else 1.0
        for h in bm25_hits:
            pid = h["paper_id"]
            norm = (h["bm25_score"] - min_b) / rng_b
            bm25_pid_scores[pid] = max(bm25_pid_scores.get(pid, 0), norm)

    if not dists:
        return [normalize_pid((m.get("paper_id") or "").strip()) for m in metas[:top_k]]

    valid_dists = [d for d in dists if d is not None]
    min_d = min(valid_dists) if valid_dists else 0.0
    max_d = max(valid_dists) if valid_dists else 1.0
    rng_d = max_d - min_d if max_d > min_d else 1.0

    scored = []
    for i in range(len(metas)):
        d_val = dists[i] if i < len(dists) and dists[i] is not None else max_d
        v_norm = 1.0 - (d_val - min_d) / rng_d
        pid = normalize_pid((metas[i].get("paper_id") or "").strip())
        b_norm = bm25_pid_scores.get(pid, 0.0)
        hybrid = vw * v_norm + bw * b_norm
        scored.append((hybrid, i, pid))
    scored.sort(key=lambda x: -x[0])

    seen: set[str] = set()
    deduped_pids: list[str] = []
    for _, _idx, pid in scored:
        if pid and pid not in seen:
            seen.add(pid)
            deduped_pids.append(pid)
        elif not pid:
            deduped_pids.append(pid)
    existing = set(deduped_pids)
    for h in bm25_hits[: min(15, len(bm25_hits))]:
        pid = h["paper_id"]
        if pid not in existing:
            deduped_pids.append(pid)
            existing.add(pid)
    return deduped_pids[:top_k]


def production_rank_of_pid(
    collection,
    query: str,
    fetch_n: int,
    target_pid: str,
    max_k: int,
) -> int | None:
    """Production과 동일 경로로 상위 max_k까지 펼쳐 1-based 순위. 없으면 None."""
    pids = hybrid_retrieve_paper_ids_for_eval(
        collection,
        query,
        fetch_n=fetch_n,
        top_k=max_k,
    )
    t = normalize_pid(target_pid)
    for i, p in enumerate(pids):
        if normalize_pid(p) == t:
            return i + 1
    return None


def main():
    parser = argparse.ArgumentParser(description="Hybrid RAG eval")
    parser.add_argument(
        "--top-k-list",
        type=str,
        default="5,8,10,15",
        help="쉼표로 구분한 Recall@K 목록 (예: 5,8,10,15)",
    )
    parser.add_argument(
        "--gap-k",
        type=int,
        default=5,
        help="Legacy vs Production 차이 분석 시 사용할 K (기본 5)",
    )
    args = parser.parse_args()
    top_k_list = sorted({int(x.strip()) for x in args.top_k_list.split(",") if x.strip()})
    primary_k = args.gap_k if args.gap_k in top_k_list else top_k_list[0]

    print("🔄 ChromaDB 연결 및 임베딩 모델 로드 중...")
    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR), settings=Settings(anonymized_telemetry=False))
    print(f"  임베딩 모델: {EMBEDDING_MODEL}")
    ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True)
    collection = client.get_collection("arxiv_papers", embedding_function=ef)
    print(f"  DB 청크 수: {collection.count():,}")

    print("\n🔄 BM25 인덱스 로드 중...")
    bm25 = get_bm25_searcher()
    print(f"  BM25 논문 수: {bm25.paper_count:,}  (레거시/분석용 BM25 top-M={BM25_UNION_TOP_M})")

    print("\n🔄 Cross-encoder 로드 중...")
    ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    max_k = max(top_k_list)
    fetch_n = int(max(float(max_k) * CHROMA_FETCH_MULTIPLIER, float(CHROMA_FETCH_MIN)))
    print(
        f"  후보 fetch: FETCH_N={fetch_n} (max K={max_k}, multiplier={CHROMA_FETCH_MULTIPLIER}, min={CHROMA_FETCH_MIN})"
    )
    print(f"  HYBRID_MULTI_QUERY_RETRIEVAL={HYBRID_MULTI_QUERY_RETRIEVAL} (멀티쿼리는 기본 끔 권장)")
    VW, BW = 0.5, 0.5

    baseline_by_k = {}
    production_by_k = {}
    legacy_by_k = {}

    for tk in top_k_list:
        print("\n" + "🔵" * 30)
        print(f"🔵 Baseline (Vector Only)  @K={tk}")
        print("🔵" * 30)
        baseline_retrieved = []
        for item in EVAL_DATA:
            result = collection.query(
                query_texts=[item["query"]],
                n_results=tk,
                include=["metadatas", "distances"],
            )
            metas = (result.get("metadatas") or [[]])[0]
            pids = [normalize_pid((m.get("paper_id") or "").strip()) for m in metas]
            baseline_retrieved.append(pids)
        baseline_by_k[tk] = calc_metrics(EVAL_DATA, baseline_retrieved, tk)
        print_metrics(f"Baseline @K={tk}", baseline_by_k[tk], tk)

        print("\n" + "🟣" * 30)
        print(f"🟣 Production Hybrid  @K={tk}")
        print("🟣" * 30)
        production_retrieved = []
        for item in EVAL_DATA:
            pids = hybrid_retrieve_paper_ids_for_eval(
                collection,
                item["query"],
                fetch_n=fetch_n,
                top_k=tk,
            )
            production_retrieved.append([normalize_pid(p) for p in pids])
        production_by_k[tk] = calc_metrics(EVAL_DATA, production_retrieved, tk)
        print_metrics(f"Production Hybrid @K={tk}", production_by_k[tk], tk)

    production_metrics = production_by_k.get(primary_k) or production_by_k[top_k_list[0]]

    # ── 3. 레거시 그리드 (primary_k에서 최적 가중치 선택) ──
    weight_configs = [
        (0.5, 0.5, "V0.5+B0.5"),
        (0.4, 0.6, "V0.4+B0.6"),
        (0.3, 0.7, "V0.3+B0.7"),
    ]
    best_recall = 0.0
    best_label = ""
    all_results: dict = {}
    for vw, bw, label in weight_configs:
        print(f"\n{'🟡' * 30}")
        print(f"🟡 Legacy Hybrid: {label}  @K={primary_k} (그리드)")
        print(f"{'🟡' * 30}")
        hybrid_retrieved = [
            legacy_minmax_pids_for_query(
                collection,
                item["query"],
                bm25,
                vw=vw,
                bw=bw,
                fetch_n=fetch_n,
                top_k=primary_k,
                bm25_top=BM25_UNION_TOP_M,
            )
            for item in EVAL_DATA
        ]
        metrics = calc_metrics(EVAL_DATA, hybrid_retrieved, primary_k)
        print_metrics(f"Hybrid ({label})", metrics, primary_k)
        all_results[label] = metrics
        if metrics["recall"] > best_recall:
            best_recall = metrics["recall"]
            best_label = label
            VW, BW = vw, bw

    print(f"\n🏆 Best Legacy Hybrid: {best_label} (Recall@{primary_k}={best_recall:.4f})")

    for tk in top_k_list:
        print(f"\n{'🟡' * 30}")
        print(f"🟡 Legacy Best ({best_label})  @K={tk}")
        print(f"{'🟡' * 30}")
        hybrid_retrieved = [
            legacy_minmax_pids_for_query(
                collection,
                item["query"],
                bm25,
                vw=VW,
                bw=BW,
                fetch_n=fetch_n,
                top_k=tk,
                bm25_top=BM25_UNION_TOP_M,
            )
            for item in EVAL_DATA
        ]
        legacy_by_k[tk] = calc_metrics(EVAL_DATA, hybrid_retrieved, tk)
        print_metrics(f"Legacy Best ({best_label}) @K={tk}", legacy_by_k[tk], tk)

    hybrid_metrics = all_results[best_label]
    baseline_metrics = baseline_by_k[primary_k]

    # ── Legacy vs Production gap (같은 K) ──
    print(f"\n{'='*72}")
    print(f"🔎 Legacy에만 있고 Production Top-{primary_k}에는 없는 paper_id")
    print("   (Production 상위 80위 안 순위로 탈락 원인 추정)")
    print(f"{'='*72}")
    gap_rows = []
    for i, item in enumerate(EVAL_DATA):
        query = item["query"]
        legacy_p = legacy_minmax_pids_for_query(
            collection,
            query,
            bm25,
            vw=VW,
            bw=BW,
            fetch_n=fetch_n,
            top_k=primary_k,
            bm25_top=BM25_UNION_TOP_M,
        )
        prod_p = [
            normalize_pid(x)
            for x in hybrid_retrieve_paper_ids_for_eval(
                collection,
                query,
                fetch_n=fetch_n,
                top_k=primary_k,
            )
        ]
        Ls = set(legacy_p[:primary_k])
        Ps = set(prod_p[:primary_k])
        only_leg = Ls - Ps
        for pid in sorted(only_leg):
            rel = normalize_pid(pid) in {normalize_pid(p) for p in item["relevant_papers"]}
            r80 = production_rank_of_pid(collection, query, fetch_n, pid, max_k=80)
            if r80 is None:
                reason = "not_in_production_top_80"
                detail = "후보 풀·BM25 union·논문집계 이전 단계에서 누락 가능"
            elif r80 > primary_k:
                reason = "ranking_drop"
                detail = f"Production 확장 순위 #{r80} (RRF·논문집계·제목보정으로 상위 밀림)"
            else:
                reason = "order/dedup"
                detail = "동일 상위권 내 순서/중복 처리 차이"
            row = {
                "query": query,
                "paper_id": pid,
                "relevant_label": rel,
                "reason": reason,
                "detail": detail,
                "prod_rank_in_80": r80,
            }
            gap_rows.append(row)
            tag = " ★정답" if rel else ""
            print(f"  [{i:02d}] {pid}{tag}")
            print(f"       → {reason}: {detail}")

    # ── 쿼리 난이도별 Production miss (primary_k) ──
    pm = production_by_k[primary_k]
    by_bucket = {"generic": {"hit": 0, "miss": 0}, "specific": {"hit": 0, "miss": 0}}
    for i, item in enumerate(EVAL_DATA):
        b = classify_query_difficulty(item["query"])
        if pm["details"][i]["hit"]:
            by_bucket[b]["hit"] += 1
        else:
            by_bucket[b]["miss"] += 1
    print(f"\n{'='*72}")
    print(f"📂 Query difficulty vs Production hit @K={primary_k}")
    print(f"{'='*72}")
    for b in ("generic", "specific"):
        h, m = by_bucket[b]["hit"], by_bucket[b]["miss"]
        tot = h + m
        print(f"  {b:10s}: hit {h}/{tot}  miss {m}/{tot}")

    # ── Recall@K 스윕 요약 ──
    print(f"\n{'='*72}")
    print("📈 Recall@K 스윕 (Legacy Best vs Production)")
    print(f"{'='*72}")
    print(f"  {'K':>4}  {'Legacy':>10}  {'Production':>12}")
    for tk in top_k_list:
        lr = legacy_by_k[tk]["recall"]
        pr = production_by_k[tk]["recall"]
        print(f"  {tk:>4}  {lr:>10.4f}  {pr:>12.4f}")

    # ── 4. Best Legacy + Cross-encoder Rerank (@primary_k) ──
    print(f"\n{'🟢' * 30}")
    print(f"🟢 Best Legacy ({best_label}) + CE  @K={primary_k}")
    print(f"{'🟢' * 30}")
    hybrid_rerank_retrieved = []
    for item in EVAL_DATA:
        query = item["query"]
        result = collection.query(
            query_texts=[query],
            n_results=fetch_n,
            include=["metadatas", "distances", "documents"],
        )
        metas = (result.get("metadatas") or [[]])[0]
        dists = (result.get("distances") or [[]])[0]
        docs = (result.get("documents") or [[]])[0]

        bm25_hits = bm25.search(query, top_k=BM25_UNION_TOP_M)
        bm25_pid_scores = {}
        if bm25_hits:
            raw_bm25 = [h["bm25_score"] for h in bm25_hits]
            min_b, max_b = min(raw_bm25), max(raw_bm25)
            rng_b = max_b - min_b if max_b > min_b else 1.0
            for h in bm25_hits:
                pid = h["paper_id"]
                norm = (h["bm25_score"] - min_b) / rng_b
                bm25_pid_scores[pid] = max(bm25_pid_scores.get(pid, 0), norm)

        if dists:
            valid_dists = [d for d in dists if d is not None]
            min_d = min(valid_dists) if valid_dists else 0.0
            max_d = max(valid_dists) if valid_dists else 1.0
            rng_d = max_d - min_d if max_d > min_d else 1.0
            scored = []
            for i in range(len(docs)):
                d_val = dists[i] if i < len(dists) and dists[i] is not None else max_d
                v_norm = 1.0 - (d_val - min_d) / rng_d
                pid = normalize_pid((metas[i].get("paper_id") or "").strip())
                b_norm = bm25_pid_scores.get(pid, 0.0)
                hybrid = VW * v_norm + BW * b_norm
                scored.append((hybrid, i))
            scored.sort(key=lambda x: -x[0])
            reorder = [idx for _, idx in scored[:fetch_n]]
            docs = [docs[i] for i in reorder]
            metas = [metas[i] for i in reorder]

        existing_pids_ce = {normalize_pid((m.get("paper_id") or "").strip()) for m in metas}
        for h in bm25_hits[:5]:
            bpid = h["paper_id"]
            if bpid not in existing_pids_ce:
                try:
                    extra_res = collection.get(where={"paper_id": bpid}, include=["documents", "metadatas"], limit=3)
                    e_docs = extra_res.get("documents") or []
                    e_metas = extra_res.get("metadatas") or []
                    for ed, em in zip(e_docs[:2], e_metas[:2]):
                        if ed and len(ed) >= 80:
                            docs.append(ed if isinstance(ed, str) else str(ed))
                            metas.append(
                                {str(k): ("" if v is None else str(v)) for k, v in (em or {}).items()}
                                if isinstance(em, dict)
                                else {}
                            )
                    existing_pids_ce.add(bpid)
                except Exception:
                    pass

        if docs:
            pairs = [(query, doc[:512]) for doc in docs]
            scores = ce.predict(pairs).tolist()
            indexed = sorted(enumerate(scores), key=lambda x: -x[1])
            first_per_paper = []
            extra = []
            seen_pids = set()
            for orig_idx, _ in indexed:
                pid = normalize_pid((metas[orig_idx].get("paper_id") or "").strip())
                if not pid or pid not in seen_pids:
                    if pid:
                        seen_pids.add(pid)
                    first_per_paper.append(orig_idx)
                else:
                    extra.append(orig_idx)
            final = (first_per_paper + extra)[:primary_k]
            pids = [normalize_pid((metas[i].get("paper_id") or "").strip()) for i in final]
        else:
            pids = []
        hybrid_rerank_retrieved.append(pids)

    hybrid_rerank_metrics = calc_metrics(EVAL_DATA, hybrid_rerank_retrieved, primary_k)
    print_metrics(f"Hybrid+Rerank ({best_label}+CE)", hybrid_rerank_metrics, primary_k)

    # ── 비교 요약 (@primary_k) ──
    print(f"\n{'='*60}")
    print(f"📊 요약 비교 @K={primary_k} (Production = 서비스 랭킹)")
    print(f"{'='*60}")
    print(f"  {'지표':<15} {'Baseline':>10} {'Legacy H':>10} {'Production':>12} {'H+Rerank':>10}")
    print(f"  {'-'*57}")
    for metric in ["recall", "precision1", "mrr"]:
        b = baseline_metrics[metric]
        h = hybrid_metrics[metric]
        p = production_metrics[metric]
        hr = hybrid_rerank_metrics[metric]
        print(f"  {metric:<15} {b:>10.4f} {h:>10.4f} {p:>12.4f} {hr:>10.4f}")
    print(f"{'='*60}")

    out_path = Path("scripts/eval_hybrid_results.json")
    out = {
        "primary_k": primary_k,
        "top_k_list": top_k_list,
        "baseline_by_k": {str(k): {x: v[x] for x in v if x != "details"} for k, v in baseline_by_k.items()},
        "legacy_by_k": {str(k): {x: v[x] for x in v if x != "details"} for k, v in legacy_by_k.items()},
        "production_by_k": {str(k): {x: v[x] for x in v if x != "details"} for k, v in production_by_k.items()},
        "baseline": {k: v for k, v in baseline_metrics.items() if k != "details"},
        "hybrid_legacy": {k: v for k, v in hybrid_metrics.items() if k != "details"},
        "production_hybrid": {k: v for k, v in production_metrics.items() if k != "details"},
        "hybrid_rerank": {k: v for k, v in hybrid_rerank_metrics.items() if k != "details"},
        "legacy_vs_production_gap": gap_rows,
        "query_difficulty_production": by_bucket,
        "config": {
            "legacy_grid_vector_weight": VW,
            "legacy_grid_bm25_weight": BW,
            "production_rrf_vector_weight": HYBRID_VECTOR_WEIGHT,
            "production_rrf_bm25_weight": HYBRID_BM25_WEIGHT,
            "bm25_union_top_m": BM25_UNION_TOP_M,
            "fetch_n": fetch_n,
            "model": EMBEDDING_MODEL,
            "note": "production_hybrid matches agent_chroma_rag (CE off); multi-query off recommended",
        },
    }
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n💾 결과 저장: {out_path}")


if __name__ == "__main__":
    main()
