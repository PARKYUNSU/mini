"""query_example_1029 진단 2: 같은 단어에서 쉼표 · 순서만 바꿔 원인 분리 (읽기만)."""
import re, sys, os
sys.path.insert(0, os.getcwd())
import core.config.agent_config  # .env
from core.rag.agent_chroma_rag import get_chroma_rag_tool
new = set(re.findall(r'id: "([0-9.]+)"', open("docs/experiments/corpus_er_1029/candidates.yaml").read()))
qs = ["rag search across multiple databases duplicate content detection in large document collections",
      "rag search, across multiple databases, duplicate content detection, in large document collections",
      "duplicate content detection in large document collections rag search across multiple databases",
      "rag, duplicate content detection across multiple databases, large document collections",
      "duplicate content detection across multiple databases in large document collections"]
t = get_chroma_rag_tool()
for q in qs:
    ctx = t.search(q, top_k=15, session_context="", wants_depth=False, light_rerank=True)
    hits = list(dict.fromkeys(re.findall(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]", ctx)))[:15]
    print(f"## {q}\n   수집 논문 {sum(p in new for p in hits)}/15 · 상위5 {sum(p in new for p in hits[:5])}")
