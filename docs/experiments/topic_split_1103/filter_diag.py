"""topic_split_1103 dev 진단: 나뉜 질문에서 거르기가 무엇을 남기나 (D_140 처리 19→2 · 목록 모드 10→4).

  .venv/bin/python docs/experiments/topic_split_1103/filter_diag.py D_140 [list]
운영과 같은 순서로 검색 · 주제 검색 · 번갈아 합치기를 다시 하고, 거르기 LLM 원출력과 남긴 번호를 찍는다.
list 를 붙이면 목록 모드(원래 검색 10편 · 상위 10 · 압축 블록) 그대로.
"""
import sys
sys.path.insert(0, ".")
import core.config.agent_config as cfg  # .env
from core.graph import agent_nodes as N
from core.llm import relevance_filter as RF
from core.rag.agent_chroma_rag import get_chroma_rag_tool

qid = sys.argv[1]
q = next(l.split("\t", 1)[1].rstrip("\n").replace("\\n", "\n")
         for l in open("docs/experiments/topic_split_1103/dev.tsv", encoding="utf-8") if l.startswith(qid + "\t"))
rag = get_chroma_rag_tool()
LIST = len(sys.argv) > 2 and sys.argv[2] == "list"
main = rag.search(N._extract_english_rag_query(q), top_k=N.LIST_MODE_TOP_K if LIST else 15, session_context="",
                  wants_depth=False, name_query=q)
topics = N._extract_subtopics(q)
per = [rag.search(t, top_k=15, session_context="", wants_depth=False, name_query=t) for t in topics]
ctx = N._interleave_topic_blocks(main, per)
if LIST:
    ctx = N._compact_list_blocks(N._rag_context_top_n_hits(ctx, n=N.LIST_MODE_TOP_K))
blocks = [b for b in ctx.split(N._RAG_HIT_SEP) if b.strip()]
src = {}
for k, r in enumerate(per, 1):
    for b in [x for x in r.split(N._RAG_HIT_SEP) if x.strip()][:N.TOPIC_SPLIT_PER_TOPIC]:
        src.setdefault(RF._title(b)[:22], f"주제{k}")
print("주제:", topics)
for i, b in enumerate(blocks, 1):
    t = RF._title(b)
    print(f"[{i}] {src.get(t[:22], '원래')} · {t[:110]}")
from langchain_ollama import ChatOllama
from core.config.agent_config import ollama_kwargs
prompt = RF.PROMPT.format(question=q, docs="\n\n".join(RF._brief(i, b) for i, b in enumerate(blocks, 1)))
raw = str(ChatOllama(**ollama_kwargs(model=cfg.RAG_ANSWER_MODEL, temperature=0.0, seed=0, reasoning=False, num_predict=32)).invoke(prompt).content or "")
print("거르기 원출력:", repr(raw), "→", RF.parse_relevant(raw, len(blocks)))
print("프롬프트 글자", len(prompt))
