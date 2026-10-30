"""query_example_1029 진단 4: 거르기 · 판정이 H3D 를 버리는 원인 — 질문 표현 · 순서만 바꿔 같은 15편에 돌린다 (읽기만).
질문 변형은 진단용이다. 'RAG 를 질문에서 빼기'를 해법으로 쓰지 않는다(§3)."""
import re, sys, os
sys.path.insert(0, os.getcwd())
import core.config.agent_config  # .env
from core.config.agent_config import RAG_ANSWER_MODEL
from core.rag.agent_chroma_rag import get_chroma_rag_tool
from core.llm.citation_fix import RAG_HIT_SEP, number_context_papers
from core.llm.relevance_filter import filter_relevant
from core.llm.presence_judge import judge_presence
from core.graph.agent_nodes import _rag_context_top_n_hits

QUERY = "cross-database retrieval similarity duplicate document detection large-scale database comparison research rag search"
QS = [
    ("Q0 운영 원문", "RAG검색을 했을시에, 두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘"),
    ("Q1 'RAG검색을 했을시에,' 뺌", "두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘"),
    ("Q2 RAG 는 두고 뒤로", "두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘. RAG 검색에 쓰려고 해"),
    ("Q3 RAG + 분야 용어", "RAG검색을 했을시에, 두개의 DB에서 서로 비슷하거나 같은 내용을 찾는(중복 탐지) 연구에 대해서 조사해줘"),
]
H3D = "2607.08382"
ctx15 = get_chroma_rag_tool().search(QUERY, top_k=15, session_context="", wants_depth=False, light_rerank=True)
blocks = [b for b in ctx15.split(RAG_HIT_SEP) if b.strip()]
pos = next(i for i, b in enumerate(blocks) if H3D in b)
h3d_first = RAG_HIT_SEP.join([blocks[pos]] + blocks[:pos] + blocks[pos + 1:])
ids = lambda c: [m for m in dict.fromkeys(re.findall(r"\[(\d{4}\.\d{4,5})", c))]

runs = [(n, q, ctx15) for n, q in QS] + [("Q0 + H3D 를 1번으로", QS[0][1], h3d_first)]
for name, q, ctx in runs:
    out, st = filter_relevant(q, ctx, RAG_ANSWER_MODEL)
    top5 = _rag_context_top_n_hits(out, n=5)
    numbered, doc_ids = number_context_papers(top5)
    pick = judge_presence(q, numbered, RAG_ANSWER_MODEL)
    kept = ids(out) if st not in ("없음", "못 읽음", "호출 실패") else []
    print(f"## {name}\n   거르기: {st} · 남김 {kept} · H3D 남음 {H3D in kept}\n   상위5 {ids(top5)}\n   판정: {pick}")
