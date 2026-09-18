#!/usr/bin/env python3
"""임베딩 모델 비교 평가 스크립트.

현재 모델(all-MiniLM-L6-v2)과 후보 모델들을 동일 평가 데이터로 비교합니다.
ChromaDB를 사용하지 않고, 임베딩 모델만 직접 로드하여 코사인 유사도로 평가합니다.

사용법:
    .venv/bin/python3 scripts/eval_embedding_models.py
"""

import json
import time
from pathlib import Path

import numpy as np

# ============================================================
# 평가 데이터: (query, 정답 논문 제목/키워드 텍스트) 쌍
# 실제 DB 청크 대신 논문 제목+초록 일부를 정답 텍스트로 사용
# ============================================================

EVAL_PAIRS = [
    {
        "query": "retrieval augmented generation survey",
        "positive": "A Survey on Retrieval-Augmented Generation for Large Language Models. This survey provides a comprehensive overview of RAG methods.",
        "hard_negative": "Deep Residual Learning for Image Recognition. We present a residual learning framework.",
    },
    {
        "query": "RAG retrieval accuracy improvement",
        "positive": "Speculative RAG: Enhancing Retrieval Augmented Generation through Drafting. We propose speculative retrieval augmented generation.",
        "hard_negative": "Batch Normalization: Accelerating Deep Network Training by reducing internal covariate shift.",
    },
    {
        "query": "hallucination mitigation in RAG systems",
        "positive": "Trustworthiness in Retrieval-Augmented Generation Systems: A Survey on hallucination detection and mitigation strategies.",
        "hard_negative": "Generative Adversarial Networks for image synthesis and style transfer.",
    },
    {
        "query": "transformer self attention mechanism neural network",
        "positive": "Attention Is All You Need. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.",
        "hard_negative": "RAG evaluation benchmark for retrieval augmented generation systems.",
    },
    {
        "query": "fairness bias in large language models",
        "positive": "Fairness in Large Language Models: A Taxonomic Survey examining bias, discrimination and fairness issues in LLMs.",
        "hard_negative": "Accelerating retrieval augmented generation inference with speculative decoding.",
    },
    {
        "query": "CRAG corrective retrieval augmented generation",
        "positive": "Corrective Retrieval Augmented Generation (CRAG) incorporates a self-reflective retrieval evaluator to assess query-document relevance.",
        "hard_negative": "Vision Transformer for image classification using patch embeddings.",
    },
    {
        "query": "chunking optimization for retrieval systems",
        "positive": "Chunking, Retrieval, and Re-ranking: An Empirical Evaluation of text chunking strategies for retrieval-augmented generation.",
        "hard_negative": "Foundation agents brain inspired AI for autonomous decision making.",
    },
    {
        "query": "self RAG reflection token generation",
        "positive": "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection using reflection tokens.",
        "hard_negative": "Enterprise RAG optimization content design for business applications.",
    },
    {
        "query": "dense passage retrieval bi-encoder training",
        "positive": "Dense Passage Retrieval for Open-Domain Question Answering using bi-encoder architecture with BERT.",
        "hard_negative": "Medical RAG benchmarking for clinical question answering systems.",
    },
    {
        "query": "ontology grounded RAG knowledge graph",
        "positive": "OG-RAG: Ontology-Grounded Retrieval-Augmented Generation for Large Language Models using knowledge graphs.",
        "hard_negative": "Anomalous attention distribution in transformer language models.",
    },
    {
        "query": "seven failure points RAG engineering",
        "positive": "Seven Failure Points When Engineering a Retrieval Augmented Generation System: indexing, retrieval, augmentation failures.",
        "hard_negative": "Discourse aware retrieval augmented generation for dialogue systems.",
    },
    {
        "query": "knowledge oriented retrieval augmented generation",
        "positive": "A Survey on Knowledge-Oriented Retrieval-Augmented Generation covering knowledge integration in RAG pipelines.",
        "hard_negative": "Adam: A Method for Stochastic Optimization for training deep neural networks.",
    },
    {
        "query": "reranking cross encoder in retrieval pipeline",
        "positive": "Cross-encoder reranking in retrieval pipelines improves precision by scoring query-document pairs jointly.",
        "hard_negative": "Dropout: A Simple Way to Prevent Neural Networks from Overfitting.",
    },
    {
        "query": "query decomposition hybrid retrieval BM25",
        "positive": "Query decomposition with hybrid retrieval combining BM25 sparse retrieval and dense vector search for improved recall.",
        "hard_negative": "Denoising Diffusion Probabilistic Models for high-quality image generation.",
    },
    {
        "query": "large language model autonomous agents survey",
        "positive": "A Review of Large Language Models and Autonomous Agents in Chemistry: survey of LLM-based agent architectures.",
        "hard_negative": "Learning Transferable Visual Models From Natural Language Supervision (CLIP).",
    },
]

# 후보 임베딩 모델 목록
MODELS = [
    {
        "name": "all-MiniLM-L6-v2 (현재)",
        "model_id": "sentence-transformers/all-MiniLM-L6-v2",
        "dim": 384,
    },
    {
        "name": "bge-base-en-v1.5",
        "model_id": "BAAI/bge-base-en-v1.5",
        "dim": 768,
    },
    {
        "name": "bge-small-en-v1.5",
        "model_id": "BAAI/bge-small-en-v1.5",
        "dim": 384,
    },
    {
        "name": "gte-base-en-v1.5",
        "model_id": "Alibaba-NLP/gte-base-en-v1.5",
        "dim": 768,
        "trust_remote_code": True,
    },
    {
        "name": "all-mpnet-base-v2",
        "model_id": "sentence-transformers/all-mpnet-base-v2",
        "dim": 768,
    },
    {
        "name": "e5-base-v2",
        "model_id": "intfloat/e5-base-v2",
        "dim": 768,
    },
]


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """코사인 유사도."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def evaluate_model(model_id: str, model_name: str, eval_pairs: list[dict]) -> dict:
    """단일 모델 평가: 정답 vs 오답 구분 능력 측정."""
    from sentence_transformers import SentenceTransformer

    print(f"\n{'='*60}")
    print(f"🔄 모델 로드: {model_name} ({model_id})")
    t0 = time.time()

    try:
        model = SentenceTransformer(model_id, trust_remote_code=True)
    except Exception as e:
        print(f"  ❌ 모델 로드 실패: {e}")
        return {"model": model_name, "error": str(e)}

    load_time = time.time() - t0
    print(f"  로드 시간: {load_time:.1f}초")

    # 모든 텍스트 한번에 인코딩
    queries = [p["query"] for p in eval_pairs]
    positives = [p["positive"] for p in eval_pairs]
    hard_negatives = [p["hard_negative"] for p in eval_pairs]

    t1 = time.time()
    q_embs = model.encode(queries, normalize_embeddings=True)
    p_embs = model.encode(positives, normalize_embeddings=True)
    n_embs = model.encode(hard_negatives, normalize_embeddings=True)
    encode_time = time.time() - t1

    # 평가 지표
    correct = 0  # positive가 negative보다 유사도 높은 경우
    pos_sims = []
    neg_sims = []
    margins = []

    for i in range(len(eval_pairs)):
        pos_sim = cosine_sim(q_embs[i], p_embs[i])
        neg_sim = cosine_sim(q_embs[i], n_embs[i])
        margin = pos_sim - neg_sim

        pos_sims.append(pos_sim)
        neg_sims.append(neg_sim)
        margins.append(margin)

        if pos_sim > neg_sim:
            correct += 1

    accuracy = correct / len(eval_pairs)
    avg_pos_sim = np.mean(pos_sims)
    avg_neg_sim = np.mean(neg_sims)
    avg_margin = np.mean(margins)
    min_margin = np.min(margins)

    print(f"  인코딩 시간: {encode_time:.2f}초 ({len(queries)*3}개 텍스트)")
    print(f"  차원: {q_embs.shape[1]}")
    print(f"  정확도 (pos > neg): {accuracy:.4f} ({correct}/{len(eval_pairs)})")
    print(f"  평균 positive 유사도: {avg_pos_sim:.4f}")
    print(f"  평균 negative 유사도: {avg_neg_sim:.4f}")
    print(f"  평균 마진 (pos-neg): {avg_margin:.4f}")
    print(f"  최소 마진: {min_margin:.4f}")

    # 실패 케이스 출력
    failures = []
    for i in range(len(eval_pairs)):
        if margins[i] <= 0:
            failures.append({
                "query": eval_pairs[i]["query"],
                "pos_sim": pos_sims[i],
                "neg_sim": neg_sims[i],
                "margin": margins[i],
            })
    if failures:
        print(f"\n  ❌ 실패 케이스 ({len(failures)}개):")
        for f in failures:
            print(f"    - {f['query'][:50]}  pos={f['pos_sim']:.4f} neg={f['neg_sim']:.4f} margin={f['margin']:.4f}")

    return {
        "model": model_name,
        "model_id": model_id,
        "dim": int(q_embs.shape[1]),
        "accuracy": accuracy,
        "avg_pos_sim": float(avg_pos_sim),
        "avg_neg_sim": float(avg_neg_sim),
        "avg_margin": float(avg_margin),
        "min_margin": float(min_margin),
        "load_time": load_time,
        "encode_time": encode_time,
        "failures": len(failures) if failures else 0,
    }


def main():
    print("=" * 60)
    print("🔬 임베딩 모델 비교 평가")
    print(f"   평가 쌍: {len(EVAL_PAIRS)}개 (query + positive + hard_negative)")
    print(f"   후보 모델: {len(MODELS)}개")
    print("=" * 60)

    results = []
    for m in MODELS:
        try:
            r = evaluate_model(m["model_id"], m["name"], EVAL_PAIRS)
            results.append(r)
        except Exception as e:
            print(f"  ❌ {m['name']} 평가 실패: {e}")
            results.append({"model": m["name"], "error": str(e)})

    # 최종 비교 테이블
    print("\n" + "=" * 80)
    print("📊 임베딩 모델 비교 결과")
    print("=" * 80)
    print(f"  {'모델':<30} {'차원':>4} {'정확도':>8} {'평균마진':>8} {'최소마진':>8} {'로드(s)':>8} {'인코딩(s)':>9}")
    print(f"  {'-'*75}")

    valid_results = [r for r in results if "error" not in r]
    valid_results.sort(key=lambda x: -x["accuracy"])

    for r in valid_results:
        best_marker = " 🏆" if r == valid_results[0] else ""
        print(
            f"  {r['model']:<30} {r['dim']:>4} {r['accuracy']:>8.4f} "
            f"{r['avg_margin']:>8.4f} {r['min_margin']:>8.4f} "
            f"{r['load_time']:>8.1f} {r['encode_time']:>9.2f}{best_marker}"
        )

    for r in results:
        if "error" in r:
            print(f"  {r['model']:<30}  ❌ {r['error'][:40]}")

    # 추천
    if valid_results:
        best = valid_results[0]
        current = next((r for r in valid_results if "현재" in r["model"]), None)

        print(f"\n🏆 최고 성능: {best['model']} (정확도={best['accuracy']:.4f}, 마진={best['avg_margin']:.4f})")
        if current and best["model"] != current["model"]:
            improvement = best["accuracy"] - current["accuracy"]
            margin_improvement = best["avg_margin"] - current["avg_margin"]
            print(f"   현재 대비: 정확도 +{improvement:.4f}, 마진 +{margin_improvement:.4f}")
            if best["dim"] > current["dim"]:
                print(f"   ⚠️ 차원 증가: {current['dim']} → {best['dim']} (DB 재구축 + 저장 공간 증가)")
            print(f"\n💡 추천: {best['model']}로 업그레이드 시 검색 품질 대폭 개선 예상")
            print(f"   단, ChromaDB 전체 재구축 필요 (현재 799K 청크, 약 2시간 소요)")

    # JSON 저장
    out_path = Path("scripts/eval_embedding_results.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n💾 상세 결과 저장: {out_path}")


if __name__ == "__main__":
    main()
