"""canon_1110 §1 후보 규칙 (측정 전 고정). 이 파일을 커밋한 뒤 한 번 돌린다:

    .venv/bin/python docs/experiments/canon_1110/candidates.py

주제(topics.tsv)마다 OpenAlex title_and_abstract 검색 + arXiv 출처 필터, 인용 수 내림차순 — arXiv ID 있는 앞 10편 중 DB 에 없는 것.
여기에 고정 목록(fixed.tsv) 중 DB 에 없는 것. 제목 · 초록은 arXiv API. OpenAlex 는 키 없이 주제당 한 번.
"""
import glob
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

D = "docs/experiments/canon_1110/"
UA = {"User-Agent": "mini-canon/0.1"}
K = 10


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def db_ids():
    out = set()
    for f in sorted(glob.glob("raw_data_queue/processed/crawled_papers*.jsonl")) + ["raw_data_queue/crawled_papers.jsonl"]:
        for l in open(f, encoding="utf-8", errors="replace"):
            m = re.search(r'"paper_id":\s*"(\d{4}\.\d{4,5})', l)
            if m:
                out.add(m.group(1))
    return out


def arxiv_id(w):
    for loc in w.get("locations") or []:
        m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", f"{loc.get('landing_page_url') or ''} {loc.get('pdf_url') or ''}")
        if m:
            return m.group(1)
    m = re.search(r"arxiv\.(\d{4}\.\d{4,5})", (w.get("doi") or "").lower())
    return m.group(1) if m else None


def main():
    db = db_ids()
    topics, picks = [], {}
    for l in open(D + "topics.tsv", encoding="utf-8"):
        tid, name, q = l.rstrip("\n").split("\t")
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({
            "filter": f"title_and_abstract.search:{q},locations.source.id:S4306400194",
            "sort": "cited_by_count:desc", "per-page": 25,
            "select": "title,publication_year,cited_by_count,locations,doi"})
        top = []
        for w in json.loads(get(url)).get("results", []):
            aid = arxiv_id(w)
            if aid and aid not in {t["id"] for t in top}:
                top.append({"id": aid, "year": w.get("publication_year"), "cited": w.get("cited_by_count"),
                            "title": w.get("title"), "in_db": aid in db})
            if len(top) == K:
                break
        topics.append({"tid": tid, "name": name, "query": q, "top": top})
        for t in top:
            if not t["in_db"]:
                picks.setdefault(t["id"], {"source": [], "cited": t["cited"], "year": t["year"]})["source"].append(tid)
        time.sleep(1.5)
    for l in open(D + "fixed.tsv", encoding="utf-8"):
        aid = l.split("\t")[0]
        if aid not in db:
            picks.setdefault(aid, {"source": [], "cited": None, "year": None})["source"].append("fixed")
    ns = {"a": "http://www.w3.org/2005/Atom"}
    meta, ids = {}, sorted(picks)
    for i in range(0, len(ids), 50):
        x = get("http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ",".join(ids[i:i + 50]), "max_results": 50}))
        for e in ET.fromstring(x).findall("a:entry", ns):
            m = re.search(r"(\d{4}\.\d{4,5})", e.find("a:id", ns).text or "")
            t, s = e.find("a:title", ns), e.find("a:summary", ns)
            if m and t is not None and s is not None:
                meta[m.group(1)] = (re.sub(r"\s+", " ", t.text).strip(), re.sub(r"\s+", " ", s.text).strip())
        time.sleep(3)
    papers = [dict(id=p, title=meta[p][0], abstract=meta[p][1], **picks[p]) for p in ids if p in meta]
    missing = [p for p in ids if p not in meta]
    assert len(topics) == 10 and papers, "주제 10 · 후보 1편 이상이어야 한다"
    json.dump({"rule": __doc__, "topics": topics, "papers": papers, "not_on_arxiv": missing},
              open(D + "candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(D + "candidates.yaml", "w", encoding="utf-8") as w:
        w.write("classics:\n" + "".join(f'  - id: "{p["id"]}"\n    note: "canon_1110"\n' for p in papers))
    n_rule = sum(s != ["fixed"] for s in (p["source"] for p in papers))
    n_fix = sum("fixed" in p["source"] for p in papers)
    print(f"후보 {len(papers)}편 (규칙 {n_rule} · 고정 {n_fix} · 겹침 {n_rule + n_fix - len(papers)}) · arXiv 에 없음 {missing}")
    for t in topics:
        print(f"  {t['tid']} {t['name']}: 상위 {len(t['top'])} 중 DB 에 있음 {sum(x['in_db'] for x in t['top'])} · 상위 5 중 {sum(x['in_db'] for x in t['top'][:5])}")


if __name__ == "__main__":
    main()
