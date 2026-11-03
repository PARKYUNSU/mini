"""dev 질문 전부 + 실사용(브리지) + 합성을 라우터 1단계에 통과시켜 DB 목록 · 날씨 · 웹검색 도구로 가는 질문을 모은다."""
import collections, glob, json, re, sqlite3, sys
sys.path.insert(0, ".")
from core.graph import agent_nodes as N
from core.graph import agent_router_rules as R

qs = {}
for i, t in sqlite3.connect(".bridge/agent_bridge.sqlite").execute("select id, user_text from bridge_jobs"):
    if t and t.strip():
        qs.setdefault(t.strip(), "실사용")
for f in sorted(glob.glob("docs/experiments/**/*.tsv", recursive=True)):
    name = f.split("/")[-1]
    if "heldout" in name and "heldout_open" not in name:
        continue  # held-out 은 판정 전용 (heldout_open* 은 R8 뒤 dev)
    for l in open(f, encoding="utf-8"):
        p = l.rstrip("\n").split("\t")
        if len(p) >= 2 and re.search(r"[가-힣]", p[1]) and len(p[1]) >= 6 and not l.startswith("#") and re.match(r"^[A-Za-z]{1,3}_?\d|^d\d{4}|^[A-Z]_[A-Z]\d", p[0]):
            qs.setdefault(p[1].strip(), f.split("/")[2])
for q in open("docs/experiments/router_audit_1027/router_risky.txt", encoding="utf-8"):
    if q.strip():
        qs.setdefault(q.strip(), "합성")
src = collections.Counter(qs.values())
print("질문", len(qs), "· 실사용", src["실사용"], "· 합성", src["합성"], "· 평가 세트", len(src) - 2)
out, cnt = [], collections.Counter()
for q, s in qs.items():
    res = N.router_step1_hard_rules(q, q.lower(), "router_diag_1103") or {}
    tool = res.get("used_tool_name", "")
    cnt[(res.get("route_type", "2단계"), tool if res.get("route_type") == "use_existing_tool" else "")] += 1
    if res.get("route_type") == "use_existing_tool" or (res and res.get("router_choice") != "B"):
        out.append({"q": q, "src": s, "route": res.get("route_type"), "choice": res.get("router_choice"), "tool": tool,
                    "acad": R.is_academic_query_full(q), "topic": R._names_paper_topic(q)})
json.dump(out, open("docs/experiments/router_open_1103/step1_nonrag.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
    print(v, k)
