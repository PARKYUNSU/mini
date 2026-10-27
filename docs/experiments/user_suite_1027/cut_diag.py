"""U1-4: 운영 경로(top_k=15 → 상위 5 → 관련 문서 거르기)에서 정답이 어느 단계에서 빠지는지."""
import re, sys
sys.path.insert(0, ".")
import core.config.agent_config  # .env
from core.config.agent_config import RAG_ANSWER_MODEL
from core.rag.agent_chroma_rag import get_chroma_rag_tool
from core.graph.agent_nodes import _rag_context_top_n_hits
from core.llm.relevance_filter import filter_relevant

Q = "외부 지식 없이 샘플링 일관성으로 환각을 탐지하는 방법 알려줘"
RQ = "sampling consistency hallucination detection external knowledge free method"  # us_1027 운영 검색어
GOLD = {"2503.17229", "2508.14314"}
pids = lambda ctx: list(dict.fromkeys(re.sub(r"v\d+$", "", p) for p in re.findall(r"\[(\d{4}\.\d{4,5}(?:v\d+)?)\]", ctx)))


def show(name, ctx):
    ps = pids(ctx)
    print(f"{name}: {len(ps)}편 · 정답 순위", {g: (ps.index(g) + 1 if g in ps else "-") for g in sorted(GOLD)})
    for i, p in enumerate(ps, 1):
        t = re.search(rf"\[{re.escape(p)}(?:v\d+)?\]\s*([^\n\[]+)", ctx)
        print(f"  {i:2d} {'★' if p in GOLD else ' '} {p} {t.group(1).strip()[:80] if t else ''}")


ctx15 = get_chroma_rag_tool().search(RQ, top_k=15, session_context="", wants_depth=False, light_rerank=True)
show("검색 15", ctx15)
ctx5 = _rag_context_top_n_hits(ctx15, n=5)
show("상위 5 (agent_nodes.py:1261)", ctx5)
f5, s5 = filter_relevant(Q, ctx5, RAG_ANSWER_MODEL)
show(f"거르기(상위 5) {s5}", f5)
f15, s15 = filter_relevant(Q, ctx15, RAG_ANSWER_MODEL)  # 비교: 15편 모두 거르기에 넘겼다면
show(f"거르기(15편 전부) {s15}", f15)
