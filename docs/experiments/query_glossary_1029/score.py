"""query_glossary_1029 §3 채점 (판정 끝난 뒤 조건 열기)."""
import json
from collections import Counter
from math import comb
from statistics import median
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "query_glossary_1029/"
pool = {x["k"]: x for x in json.load(open(D + "pool.json"))}
J = {}
for l in open(D + "judged.txt"):
    k, v = l.split(); J[f"{pool[int(k)]['q']}|{pool[int(k)]['p']}"] = int(v)
changed = json.load(open(D + "changed.json"))
def sign(w, l):
    n = w + l
    return 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n)
load = lambda a, s: {json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}_{s}.jsonl")}
ctx = lambda r: r.get("doc_ids") or r["context_papers"]
def part(sets, title):
    w = l = 0; tot = [Counter(), Counter()]
    for s in sets:
        a, b = load("qg0", s), load("qg1", s)
        for q in changed[s]:
            n = []
            for i, r in enumerate((a[q], b[q])):
                js = [J[f"{s}|{q}|{p}"] for p in ctx(r)]; tot[i].update(js); n.append(js.count(2))
            w += n[1] > n[0]; l += n[1] < n[0]
            print(f"  {s}|{q}: '2' {n[0]} → {n[1]} · 편수 {len(ctx(a[q]))} → {len(ctx(b[q]))}")
    print(f"{title}: '2' 합 {tot[0][2]} → {tot[1][2]} | 늘어남 {w} : 줄어듦 {l} · p {sign(w, l):.4f} | '0' 합 {tot[0][0]} → {tot[1][0]} · '1' 합 {tot[0][1]} → {tot[1][1]}")
part(("g", "sub"), "주(G + sub)")
part(("er",), "보고(er, 표본 안)")
a, b = load("qg0", "sub"), load("qg1", "sub")
gq = [q for q in a if a[q].get("ok") is not None and q[0] in "AR"]
print("보호: sub 정답 문항 ok", sum(a[q]["ok"] for q in gq), "→", sum(b[q]["ok"] for q in gq), "/", len(gq), gq)
for s in ("g", "sub", "er"):
    a, b = load("qg0", s), load("qg1", s)
    same = [q for q in a if q not in changed[s]]
    print(f"보호: {s} 안 바뀐 {len(same)}문항 컨텍스트 같음 {sum(ctx(a[q]) == ctx(b[q]) for q in same)} · 시간 중앙 {median(r['elapsed'] for r in a.values()):.1f}s → {median(r['elapsed'] for r in b.values()):.1f}s")
