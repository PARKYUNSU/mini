"""work_topics_1111: 업무 주제별 인용 상위 10편(OpenAlex, arXiv 판) 중 DB 에 있는 수 — 읽기만, 수집은 하지 않는다.

    .venv/bin/python docs/experiments/work_topics_1111/gap.py

canon_1110/candidates.py 의 규칙 · 함수를 그대로 쓴다(주제 목록만 다르다).
"""
import importlib.util
import json
import time
import urllib.parse
from pathlib import Path

D = Path("docs/experiments/work_topics_1111")
spec = importlib.util.spec_from_file_location("canon_cand", "docs/experiments/canon_1110/candidates.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

db = C.db_ids()
out, missing = [], {}
for l in open(D / "topics.tsv", encoding="utf-8"):
    tid, name, q = l.rstrip("\n").split("\t")
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode({
        "filter": f"title_and_abstract.search:{q},locations.source.id:S4306400194",
        "sort": "cited_by_count:desc", "per-page": 25,
        "select": "title,publication_year,cited_by_count,locations,doi"})
    top = []
    for w in json.loads(C.get(url)).get("results", []):
        aid = C.arxiv_id(w)
        if aid and aid not in {t["id"] for t in top}:
            top.append({"id": aid, "year": w.get("publication_year"), "cited": w.get("cited_by_count"),
                        "title": w.get("title"), "in_db": aid in db})
        if len(top) == C.K:
            break
    out.append({"tid": tid, "name": name, "query": q, "top": top})
    for t in top:
        if not t["in_db"]:
            missing.setdefault(t["id"], []).append(tid)
    print(f"{tid} {name}: 상위 {len(top)} 중 DB 에 있음 {sum(x['in_db'] for x in top)}")
    for x in top:
        print(f"    {'DB' if x['in_db'] else '  '} {x['id']} {x['year']} {x['cited']:>5} {(x['title'] or '')[:78]}")
    time.sleep(1.5)
json.dump({"topics": out, "missing": missing}, open(D / "gap.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(len(t["top"]) for t in out)
print(f"합: 상위 {n}편 중 DB 에 있음 {sum(x['in_db'] for t in out for x in t['top'])} · 없는 논문(겹침 뺌) {len(missing)}")
