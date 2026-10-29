"""external_term_1029 §2: 판정 '없음' 질문의 외부 검색 — 대조(원래 검색어) · 처리(분야 용어 검색어)."""
import json, re, sys, time
sys.path.insert(0, ".")
import core.config.agent_config  # .env
from core.config.agent_config import RAG_ANSWER_MODEL
from core.rag.external_search import search_openalex, term_query
R = "docs/experiments/e2e_ko_1008/results/nk1.jsonl"; D = "docs/experiments/external_term_1029/"
qs = dict(l.rstrip("\n").split("\t")[:2] for l in open("docs/experiments/nodoc_conclusion_1029/questions.tsv"))
out = open(D + "results.jsonl", "w")
for l in open(R):
    r = json.loads(l)
    ex = set(r.get("doc_ids") or r["context_papers"])
    titles = set(re.findall(r"\[\d{4}\.\d{4,5}(?:v\d+)?\]\s*([^\[\n]+)", r.get("numbered_context") or ""))
    t0 = time.time(); tq = term_query(qs[r["id"]], RAG_ANSWER_MODEL); tt = time.time() - t0
    a = search_openalex(r["rag_queries"][0], ex, exclude_titles=titles)
    b = search_openalex(tq or r["rag_queries"][0], ex, exclude_titles=titles)
    out.write(json.dumps({"id": r["id"], "rq": r["rag_queries"][0], "tq": tq, "term_sec": tt, "et0": a, "et1": b}, ensure_ascii=False) + "\n")
    print(r["id"], f"{tt:.1f}s", len(a), len(b), "|", tq)
