"""corpus_er_1029 사전 조사: 분야 용어 영어 검색어로 DB 에 이미 있는 논문 (읽기만)."""
import re, sys, os
sys.path.insert(0, os.getcwd())
import core.config.agent_config  # .env
from core.rag.agent_chroma_rag import get_chroma_rag_tool
Q = ["entity resolution large language models", "record linkage across databases",
     "near-duplicate document detection at scale", "similarity join embeddings vector database",
     "deduplication of large text corpora", "cross-database record matching retrieval",
     "schema matching ontology alignment", "semantic deduplication MinHash LSH"]
t = get_chroma_rag_tool()
for q in Q:
    ctx = t.search(q, top_k=10, session_context="", wants_depth=False, light_rerank=True)
    print("##", q)
    for m in dict.fromkeys(re.findall(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n\[]{0,90})", ctx)):
        print("  ", *m)
