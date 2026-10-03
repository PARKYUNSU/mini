#!/usr/bin/env python3
"""BM25 진단: 미스 쿼리들에 대해 BM25가 정답 논문을 찾는지 확인."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rag.bm25_index import get_bm25_searcher

bm25 = get_bm25_searcher()

test_cases = [
    ("retrieval augmented generation survey", "2312.10997"),
    ("CRAG corrective retrieval augmented generation", "2407.08223"),
    ("speculative decoding draft verification parallel language model inference", "2407.08223"),
    ("ontology and knowledge graph grounded retrieval question answering", "2412.15235"),
    ("enterprise RAG optimization content design", "2410.12812"),
    ("transformer self attention mechanism neural network", "1706.03762"),
    ("accelerating retrieval augmented generation inference", "2412.15246"),
    ("chunking optimization for retrieval systems", "2601.15457"),
    ("seven failure points RAG engineering", "2401.05856"),
    ("RAG retrieval accuracy improvement", "2407.08223"),
    ("hallucination mitigation in RAG systems", "2409.10102"),
    ("retrieval augmented generation for question answering", "2604.02259"),
    ("vision transformer image classification", "2412.16188"),
    ("large language model autonomous agents survey", "2407.01603"),
    ("reranking cross encoder in retrieval pipeline", "2601.15457"),
    ("query decomposition hybrid retrieval BM25", "2601.15457"),
    ("ontology grounded RAG knowledge graph", "2412.15235"),
]

print(f"BM25 논문 수: {bm25.paper_count}")
print(f"{'Query':<55} {'Expected':<15} {'BM25 Hit':<10} {'Top-1 PID':<15} {'Score':<8}")
print("-" * 110)

hits = 0
for query, expected_pid in test_cases:
    results = bm25.search(query, top_k=10)
    found_pids = [r["paper_id"] for r in results]
    hit = expected_pid in found_pids
    if hit:
        hits += 1
    rank = found_pids.index(expected_pid) + 1 if hit else -1
    top1 = found_pids[0] if found_pids else "?"
    top1_score = results[0]["bm25_score"] if results else 0
    hit_str = f"✅ #{rank}" if hit else "❌"
    print(f"{query:<55} {expected_pid:<15} {hit_str:<10} {top1:<15} {top1_score:.2f}")

print(f"\nBM25 Hit Rate: {hits}/{len(test_cases)} = {hits/len(test_cases):.2%}")
