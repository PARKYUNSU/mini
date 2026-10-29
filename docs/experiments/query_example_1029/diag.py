"""query_example_1029 진단: R_134 검색어 변형별 DB 검색 상위 15 (읽기만)."""
import re, sys, os
sys.path.insert(0, os.getcwd())
import core.config.agent_config  # .env
from core.graph.agent_nodes import _extract_english_rag_query
from core.rag.agent_chroma_rag import get_chroma_rag_tool
Q = "예를들어 RAG검색을 했을시에, 두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘"
Q_NOEX = "두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘"
new = set(re.findall(r'id: "([0-9.]+)"', open("docs/experiments/corpus_er_1029/candidates.yaml").read()))
qs = [("원문 검색어 #%d" % i, _extract_english_rag_query(Q)) for i in range(3)]
qs += [("예시 뺀 질문 검색어 #%d" % i, _extract_english_rag_query(Q_NOEX)) for i in range(3)]
qs += [("손 검색어 A", "duplicate content detection across multiple large databases"),
       ("손 검색어 B", "near-duplicate detection, entity resolution, similarity join across large document collections"),
       ("손 검색어 C", "rag, near-duplicate detection across two large document databases")]
t = get_chroma_rag_tool()
for name, q in qs:
    ctx = t.search(q, top_k=15, session_context="", wants_depth=False, light_rerank=True)
    hits = list(dict.fromkeys(re.findall(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n\[]{0,70})", ctx)))[:15]
    print(f"## {name}: {q}\n   수집 논문 {sum(p in new for p, _ in hits)}/15 · 상위5 중 {sum(p in new for p, _ in hits[:5])}")
    for p, ti in hits[:8]:
        print("   ", "*" if p in new else " ", p, ti)
