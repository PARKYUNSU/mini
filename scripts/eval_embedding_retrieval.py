#!/usr/bin/env python3
"""임베딩 모델별 실제 Retrieval 성능 비교 (Recall@K, Precision@1, MRR).

각 모델로 실제 80만 청크 DB에서 Top-K 검색을 수행하여 비교합니다.
ChromaDB 컬렉션을 모델별로 임시 생성하지 않고, 임베딩 모델로 직접 쿼리 벡터를 만들어
기존 DB 청크 샘플과 비교합니다.

전략: 전체 DB 재구축 없이 평가하기 위해
1. JSONL에서 평가 대상 논문의 실제 청크를 추출 (정답 + 오답 혼합)
2. 각 모델로 쿼리 + 모든 청크를 임베딩
3. 코사인 유사도 Top-K로 retrieval 시뮬레이션
4. Recall@K, Precision@1, MRR 측정

사용법:
    .venv/bin/python3 scripts/eval_embedding_retrieval.py
"""

import json
import time
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

# ============================================================
# 평가 쿼리 (eval_rag_quality.py와 동일)
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

MODELS = [
    {"name": "all-MiniLM-L6-v2 (현재)", "model_id": "sentence-transformers/all-MiniLM-L6-v2"},
    {"name": "bge-base-en-v1.5", "model_id": "BAAI/bge-base-en-v1.5"},
    {"name": "bge-small-en-v1.5", "model_id": "BAAI/bge-small-en-v1.5"},
    {"name": "all-mpnet-base-v2", "model_id": "sentence-transformers/all-mpnet-base-v2"},
]

JSONL_DIR = Path("./raw_data_queue/processed")
# 청크 풀 크기: 실제 DB와 유사한 규모의 노이즈를 만들기 위해 많은 논문에서 청크 수집
MAX_DISTRACTOR_PAPERS = 500  # 정답 외 노이즈 논문 수
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def normalize_pid(pid: str) -> str:
    s = (pid or "").strip()
    if "v" in s:
        base, suffix = s.rsplit("v", 1)
        if suffix.isdigit() and base.replace(".", "").isdigit():
            return base
    return s


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """간단한 고정 크기 청킹."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) >= 80:  # 노이즈 필터
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def load_corpus_from_jsonl() -> tuple[list[str], list[str]]:
    """JSONL에서 청크 풀 구축. Returns (chunks, paper_ids)."""
    # 정답 논문 ID 수집
    relevant_pids = set()
    for item in EVAL_DATA:
        for pid in item["relevant_papers"]:
            relevant_pids.add(normalize_pid(pid))

    print(f"  정답 논문 수: {len(relevant_pids)}")

    all_chunks: list[str] = []
    all_pids: list[str] = []
    papers_loaded = set()
    distractor_count = 0

    jsonl_files = sorted(JSONL_DIR.glob("crawled_papers*.jsonl"))
    print(f"  JSONL 파일 수: {len(jsonl_files)}")

    for fpath in jsonl_files:
        try:
            with fpath.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    pid = normalize_pid((d.get("paper_id") or "").strip())
                    if not pid or pid in papers_loaded:
                        continue

                    content = (d.get("content") or d.get("text") or "").strip()
                    if not content:
                        content = (d.get("abstract") or d.get("summary") or "").strip()
                    if not content or len(content) < 200:
                        continue

                    is_relevant = pid in relevant_pids
                    if not is_relevant and distractor_count >= MAX_DISTRACTOR_PAPERS:
                        continue

                    chunks = chunk_text(content)
                    if not chunks:
                        continue

                    papers_loaded.add(pid)
                    if not is_relevant:
                        distractor_count += 1

                    for chunk in chunks:
                        all_chunks.append(chunk)
                        all_pids.append(pid)

        except OSError:
            continue

    relevant_loaded = relevant_pids & papers_loaded
    print(f"  로드된 논문: {len(papers_loaded)} (정답 {len(relevant_loaded)}/{len(relevant_pids)}, 노이즈 {distractor_count})")
    print(f"  총 청크 수: {len(all_chunks):,}")
    missing = relevant_pids - papers_loaded
    if missing:
        print(f"  ⚠️ 정답 논문 미발견: {missing}")

    return all_chunks, all_pids


def evaluate_retrieval(
    model: SentenceTransformer,
    model_name: str,
    queries: list[str],
    eval_data: list[dict],
    corpus_embs: np.ndarray,
    corpus_pids: list[str],
    top_k: int = 5,
) -> dict:
    """실제 retrieval 시뮬레이션 평가."""
    print(f"\n  쿼리 임베딩 중...")
    t0 = time.time()
    q_embs = model.encode(queries, normalize_embeddings=True, show_progress_bar=False)
    encode_time = time.time() - t0
    print(f"  쿼리 인코딩: {encode_time:.2f}초")

    recall_total = 0
    precision1_total = 0
    mrr_total = 0
    details = []

    for i, item in enumerate(eval_data):
        relevant = {normalize_pid(p) for p in item["relevant_papers"]}

        # 코사인 유사도 계산 (정규화된 벡터이므로 dot product = cosine sim)
        sims = corpus_embs @ q_embs[i]
        top_indices = np.argsort(-sims)[:top_k]

        retrieved_pids = []
        seen = set()
        for idx in np.argsort(-sims):
            pid = corpus_pids[idx]
            if pid not in seen:
                seen.add(pid)
                retrieved_pids.append(pid)
                if len(retrieved_pids) >= top_k:
                    break

        hit = any(r in relevant for r in retrieved_pids)
        recall_total += 1 if hit else 0
        if retrieved_pids and retrieved_pids[0] in relevant:
            precision1_total += 1
        rr = 0.0
        for idx, rid in enumerate(retrieved_pids):
            if rid in relevant:
                rr = 1.0 / (idx + 1)
                break
        mrr_total += rr

        details.append({
            "query": item["query"],
            "hit": hit,
            "rr": rr,
            "top1": retrieved_pids[0] if retrieved_pids else "",
            "top5": retrieved_pids[:5],
        })

    n = len(eval_data)
    recall = recall_total / n
    precision1 = precision1_total / n
    mrr = mrr_total / n

    print(f"\n  📊 {model_name}")
    print(f"    Recall@{top_k}:   {recall:.4f}")
    print(f"    Precision@1: {precision1:.4f}")
    print(f"    MRR:         {mrr:.4f}")

    missed = [d for d in details if not d["hit"]]
    if missed:
        print(f"    ❌ Miss ({len(missed)}개): ", end="")
        print(", ".join(d["query"][:30] for d in missed[:5]))

    return {
        "model": model_name,
        "recall": recall,
        "precision1": precision1,
        "mrr": mrr,
        "encode_time": encode_time,
        "details": details,
    }


def main():
    print("=" * 60)
    print("🔬 임베딩 모델별 실제 Retrieval 성능 비교")
    print("=" * 60)

    # 1. 코퍼스 로드
    print("\n[1/3] 코퍼스 로드 (JSONL → 청크)...")
    corpus_chunks, corpus_pids = load_corpus_from_jsonl()
    if not corpus_chunks:
        print("❌ 코퍼스가 비어 있습니다.")
        return

    queries = [item["query"] for item in EVAL_DATA]

    # 2. 각 모델별 평가
    print(f"\n[2/3] 모델별 평가 ({len(MODELS)}개 모델, {len(corpus_chunks):,} 청크)...")
    results = []

    for m in MODELS:
        print(f"\n{'='*60}")
        print(f"🔄 {m['name']} ({m['model_id']})")
        try:
            model = SentenceTransformer(m["model_id"], trust_remote_code=True)

            print(f"  코퍼스 임베딩 중 ({len(corpus_chunks):,} 청크)...")
            t0 = time.time()
            corpus_embs = model.encode(
                corpus_chunks,
                normalize_embeddings=True,
                show_progress_bar=True,
                batch_size=256,
            )
            embed_time = time.time() - t0
            print(f"  코퍼스 인코딩: {embed_time:.1f}초")

            r = evaluate_retrieval(
                model, m["name"], queries, EVAL_DATA,
                corpus_embs, corpus_pids, top_k=5,
            )
            r["corpus_embed_time"] = embed_time
            results.append(r)

            # 메모리 해제
            del model, corpus_embs
            import gc; gc.collect()

        except Exception as e:
            print(f"  ❌ 실패: {e}")
            results.append({"model": m["name"], "error": str(e)})

    # 3. 최종 비교
    print(f"\n[3/3] 최종 비교")
    print("\n" + "=" * 70)
    print("📊 임베딩 모델별 Retrieval 성능 비교 (실제 코퍼스 기반)")
    print("=" * 70)
    print(f"  {'모델':<28} {'Recall@5':>10} {'P@1':>8} {'MRR':>8} {'코퍼스(s)':>10}")
    print(f"  {'-'*64}")

    valid = [r for r in results if "error" not in r]
    valid.sort(key=lambda x: -x["recall"])

    for r in valid:
        best = " 🏆" if r == valid[0] else ""
        print(
            f"  {r['model']:<28} {r['recall']:>10.4f} {r['precision1']:>8.4f} "
            f"{r['mrr']:>8.4f} {r.get('corpus_embed_time', 0):>10.1f}{best}"
        )

    for r in results:
        if "error" in r:
            print(f"  {r['model']:<28}  ❌ {r['error'][:40]}")

    if len(valid) >= 2:
        best = valid[0]
        current = next((r for r in valid if "현재" in r["model"]), None)
        if current and best["model"] != current["model"]:
            print(f"\n🏆 최고: {best['model']}")
            print(f"   Recall: {current['recall']:.4f} → {best['recall']:.4f} (+{best['recall']-current['recall']:.4f})")
            print(f"   MRR:    {current['mrr']:.4f} → {best['mrr']:.4f} (+{best['mrr']-current['mrr']:.4f})")
            print(f"\n💡 이 모델로 교체 시 ChromaDB 전체 재구축 필요 (~2시간)")
        elif current and best["model"] == current["model"]:
            print(f"\n✅ 현재 모델이 retrieval 기준으로도 최고 성능")

    out_path = Path("scripts/eval_embedding_retrieval_results.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n💾 결과 저장: {out_path}")


if __name__ == "__main__":
    main()
