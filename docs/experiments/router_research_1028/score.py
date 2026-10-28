"""router_research_1028 §3 채점 (판정 끝난 뒤 조건 열기)."""
import json, re
from collections import Counter
from math import comb
from statistics import median
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "router_research_1028/"
pool = {x["k"]: x for x in json.load(open(D + "pool.json"))}
J = json.load(open(D + "reused.json"))
for l in open(D + "judged.txt"):
    k, v = l.split(); J[f"{pool[int(k)]['q']}|{pool[int(k)]['p']}"] = int(v)
def sign(w, l):
    n = w + l
    return 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n)
load = lambda a, s: {json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}_{s}.jsonl")}
ctx = lambda r: r.get("doc_ids") or r["context_papers"]
A = ("rr0", "rr1")
print("보호 — 정답 세트 검색 ok")
for s in ("162", "real40", "real2"):
    a, b = load("rr0", s), load("rr1", s)
    print(f"  {s}: {sum(r['ok'] for r in a.values())} → {sum(r['ok'] for r in b.values())} / {len(a)} (처리만 {sum(b[q]['ok'] and not a[q]['ok'] for q in a)} · 대조만 {sum(a[q]['ok'] and not b[q]['ok'] for q in a)})")
w = l = 0; tot = {k: Counter() for k in A}; el = {k: [] for k in A}; nd = {k: Counter() for k in A}
for s in ("H", "D", "U"):
    a = {k: load(k, s) for k in A}
    sw = sl = 0
    for q in a["rr0"]:
        n = {}
        for k in A:
            js = [J[f"{q}|{p}"] for p in ctx(a[k][q])]
            tot[k].update(js); n[k] = js.count(2); el[k].append(a[k][q]["elapsed"]); nd[k][len(js)] += 1
        sw += n["rr1"] > n["rr0"]; sl += n["rr1"] < n["rr0"]
    print(f"  [{s}] '2' 늘어남 {sw} : 줄어듦 {sl}")
    w += sw; l += sl
print(f"주: '2' 합 {tot['rr0'][2]} → {tot['rr1'][2]} | 늘어남 {w} : 줄어듦 {l} · p {sign(w, l):.4f}")
print(f"보호: '0' 합 {tot['rr0'][0]} → {tot['rr1'][0]} · '1' 합 {tot['rr0'][1]} → {tot['rr1'][1]}")
print(f"보호: 시간 중앙 {median(el['rr0']):.1f}s → {median(el['rr1']):.1f}s")
print("보고: 편수 분포", {k: dict(sorted(nd[k].items())) for k in A})
st = Counter()
for s in ("H", "D", "U"):
    for m in re.findall(r"거르기\(자르기 앞\) = (\S+)", open(f".cron/rr1_{s}.log").read()):
        st[m if not re.match(r"\d+→\d+", m) else "n→m"] += 1
print("보고: 처리 거르기 상태", dict(st))
u = {k: load(k, "U") for k in A}
g = ["2503.17229", "2508.14314"]
print("U1-4 정답:", {k: [p for p in g if p in ctx(u[k]["U1-4"])] for k in A}, "검색어", u["rr1"]["U1-4"]["rag_queries"][0])
# 대조에서 라우터 재사용이던 문항만 (로그 블록 순서 = 문항 순서)
rw = rl = rn = 0
for s in ("H", "D", "U"):
    a = {k: load(k, s) for k in A}
    route = ["reused from router" in b for b in open(f".cron/rr0_{s}.log").read().split("DirectAnswer TRACE | entry")[1:]]
    assert len(route) == len(a["rr0"]), (s, len(route))
    for q, r in zip(a["rr0"], route):
        if r:
            n0, n1 = (sum(J[f"{q}|{p}"] == 2 for p in ctx(a[k][q])) for k in A)
            rn += 1; rw += n1 > n0; rl += n1 < n0
print(f"보고: 라우터 재사용 문항 {rn} — 늘어남 {rw} : 줄어듦 {rl}")
