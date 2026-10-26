"""라우터 1단계 하드룰 점검: 학술 질문인데 RAG 밖(A·도구·C)으로 가는 질문을 찾는다."""
import glob, sqlite3, sys, collections
sys.path.insert(0, ".")
from core.graph import agent_nodes as N
from core.graph import agent_router_rules as R

qs = {}
for i, t in sqlite3.connect(".bridge/agent_bridge.sqlite").execute("select id, user_text from bridge_jobs"):
    if t: qs.setdefault(t.strip(), f"job{i}")
for f in glob.glob("docs/experiments/**/questions*.tsv", recursive=True):
    for l in open(f):
        if "\t" in l:
            qs.setdefault(l.split("\t")[1].strip(), f.split("/")[2])
extra = [l.strip() for l in open(sys.argv[1])] if len(sys.argv) > 1 else []
for q in extra: qs.setdefault(q, "합성")
sub = {"잡담": R.is_smalltalk_or_memory_request, "단위변환": R.is_trivial_unit_conversion_query, "봇상태": R.is_meta_bot_availability_query}
cnt = collections.Counter(); bad = []
for q, src in qs.items():
    if not q: continue
    acad = R.is_academic_query_full(q)
    res = N.router_step1_hard_rules(q, q.lower(), "audit_router")
    route = (res or {}).get("router_choice", "-"), (res or {}).get("route_type", "-"), (res or {}).get("used_tool_name", "")
    cnt[(acad, route[0])] += 1
    if acad and res and not (route[0] == "B" and route[1] == "direct_answer"):
        why = [k for k, f in sub.items() if f(q, q.lower())]
        bad.append((src, route, why, q[:70]))
print("질문", len(qs), dict(cnt))
for b in bad: print(*b, sep=" | ")
print("학술인데 RAG 밖:", len(bad))
