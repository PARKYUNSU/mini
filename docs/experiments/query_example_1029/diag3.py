"""query_example_1029 진단 3: 10-30 08:32 실사용 실패 재현 — 운영 검색어로 최종 15편 · 거르기 · 상위 5 (읽기만)."""
import re, sys, os
sys.path.insert(0, os.getcwd())
import core.config.agent_config  # .env
from core.config.agent_config import RAG_ANSWER_MODEL
from core.rag.agent_chroma_rag import get_chroma_rag_tool
from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.relevance_filter import filter_relevant
Q = "RAG검색을 했을시에, 두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘"
# 운영 로그(bot_ai_worker.log 10-30 08:32)의 검색어 그대로
QUERY = "cross-database retrieval similarity duplicate document detection large-scale database comparison research rag search"
new = set(re.findall(r'id: "([0-9.]+)"', open("docs/experiments/corpus_er_1029/candidates.yaml").read()))
t = get_chroma_rag_tool()


def papers(ctx):
    return [re.match(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]{0,80})", l.strip()).groups()
            for b in ctx.split(RAG_HIT_SEP) for l in b.split("\n")[:3]
            if re.match(r"\[\d{4}\.\d{4,5}", l.strip())]


for lr in (True, False):
    ctx = t.search(QUERY, top_k=15, session_context="", wants_depth=False, light_rerank=lr)
    ps = list(dict.fromkeys(papers(ctx)))
    print(f"## light_rerank={lr}: 블록 {len(ctx.split(RAG_HIT_SEP))} · 수집 논문 {sum(p in new for p, _ in ps)}/{len(ps)}")
    for i, (p, ti) in enumerate(ps, 1):
        print(f"   {i:2d}", "*" if p in new else " ", p, ti)
    if lr:
        for k in range(2):
            out, st = filter_relevant(Q, ctx, RAG_ANSWER_MODEL)
            print(f"   거르기 #{k}: {st} → 남은 논문 {[p for p, _ in dict.fromkeys(papers(out))][:5]}")
