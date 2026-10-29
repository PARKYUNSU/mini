"""external_term_1029 §3 채점 (판정 끝난 뒤 조건 열기)."""
import json
from collections import Counter
from math import comb
from statistics import median
D = "docs/experiments/external_term_1029/"
pool = {x["k"]: x for x in json.load(open(D + "pool.json"))}
J = {}
for l in open(D + "judged.txt"):
    k, v = l.split(); J[(pool[int(k)]["q"], pool[int(k)]["title"])] = int(v)
R = [json.loads(l) for l in open(D + "results.jsonl")]
w = l = 0; tot = {a: Counter() for a in ("et0", "et1")}; n = {a: Counter() for a in tot}
for r in R:
    c = {a: [J[(r["id"], it["title"])] for it in r[a]] for a in tot}
    for a in tot: tot[a].update(c[a]); n[a][len(c[a])] += 1
    w += c["et1"].count(2) > c["et0"].count(2); l += c["et1"].count(2) < c["et0"].count(2)
    print(f"  {r['id']}: '2' {c['et0'].count(2)} → {c['et1'].count(2)} | {c['et0']} → {c['et1']}")
m = w + l
p = 1.0 if m == 0 else min(1, 2 * sum(comb(m, i) for i in range(min(w, l) + 1)) / 2 ** m)
print(f"주: '2' 합 {tot['et0'][2]} → {tot['et1'][2]} | 늘어남 {w} : 줄어듦 {l} · p {p:.4f}")
print(f"보호: '0' 합 {tot['et0'][0]} → {tot['et1'][0]} · '1' 합 {tot['et0'][1]} → {tot['et1'][1]}")
print(f"보호: term_query 시간 중앙 {median(r['term_sec'] for r in R):.1f}s")
print("보고: 편수 분포", {a: dict(sorted(n[a].items())) for a in n})
