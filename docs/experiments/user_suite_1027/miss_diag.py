"""검색 놓침 4문항: 정답 논문 순위를 단계별로 — 벡터 청크(300) · BM25(300) · 최종 논문 순위(top 50) · 검색어 변형."""
import re, sys
sys.path.insert(0, ".")
import core.config.agent_config  # .env
from core.rag.agent_chroma_rag import get_chroma_rag_tool, _get_chroma_singleton
from core.rag.bm25_index import get_bm25_searcher

CASES = {
    "U1-4": ("sampling consistency hallucination detection external knowledge free method", ["2503.17229", "2508.14314"]),
    "U2-3": ("prompt compression, context length reduction, performance preservation in rag retrieval", ["2403.12968", "2410.12388", "2508.15813"]),
    "U2-5": ("query rewriting for rag retrieval quality improvement virtual answer generation before search", ["2411.13154", "2305.14283"]),
    "U5-2": ("quantized embedding vectors memory reduction search performance maintenance academic research keywords vector", ["2606.25674"]),
}
ALT = {  # 사람이 쓸 법한 짧은 검색어
    "U1-4": "sampling-based zero-resource black-box hallucination detection self-consistency",
    "U2-3": "prompt compression for large language models",
    "U2-5": "query rewriting for retrieval-augmented generation",
    "U5-2": "low-bit quantized text embeddings for retrieval",
}
rag = get_chroma_rag_tool(); bm = get_bm25_searcher()
bare = lambda p: re.sub(r"v\d+$", "", str(p))


def ranks(q, gold):
    res = _get_chroma_singleton()._collection.query(query_texts=[q], n_results=300, include=["metadatas"])
    vec = []
    for m in res["metadatas"][0]:
        p = bare(m.get("paper_id", ""))
        if p not in vec: vec.append(p)
    b = [bare(h["paper_id"]) for h in bm.search(q, top_k=300)]
    out = rag.search(q, top_k=50, session_context="", wants_depth=False, light_rerank=True)
    fin = list(dict.fromkeys(bare(x) for x in re.findall(r"\[(\d{4}\.\d{4,5}(?:v\d+)?)\]", out)))
    r = lambda L, g: (L.index(g) + 1) if g in L else "-"
    return {g: (r(vec, g), r(b, g), r(fin, g)) for g in gold}, fin[:5]


for k, (q, gold) in CASES.items():
    for name, qq in (("운영 검색어", q), ("짧은 검색어", ALT[k])):
        rr, top = ranks(qq, gold)
        print(f"{k} [{name}] {qq!r}")
        for g, (v, b, f) in rr.items():
            print(f"   {g}: 벡터 논문순위 {v} · BM25 {b} · 최종 {f}")
        print("   최종 상위5:", top)
