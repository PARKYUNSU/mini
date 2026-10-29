"""corpus_er_1029 §3 채점 (판정 끝난 뒤 조건 열기)."""
import json, re
from collections import Counter
from math import comb
from statistics import median
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "corpus_er_1029/"
pool = {x["k"]: x for x in json.load(open(D + "pool.json"))}
J = {}
for l in open(D + "judged.txt"):
    k, v = l.split(); J[f"{pool[int(k)]['q']}|{pool[int(k)]['p']}"] = int(v)
NEW = {re.sub(r"v\d+$", "", x) for x in re.findall(r'id: "([^"]+)"', open(D + "candidates.yaml").read())}
def sign(w, l):
    n = w + l
    return 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n)
load = lambda a, s: {json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}_{s}.jsonl")}
ctx = lambda r: r.get("doc_ids") or r["context_papers"]
print("보호 — 정답 세트 검색 ok")
for s in ("162", "real40", "real2"):
    a, b = load("ce0", s), load("ce1", s)
    print(f"  {s}: {sum(r['ok'] for r in a.values())} → {sum(r['ok'] for r in b.values())} / {len(a)} (후만 {sum(b[q]['ok'] and not a[q]['ok'] for q in a)} · 전만 {sum(a[q]['ok'] and not b[q]['ok'] for q in a)})")
a, b = load("ce0", "er"), load("ce1", "er")
w = l = 0; tot = {0: Counter(), 1: Counter()}; any2 = [0, 0]; newpos = new2 = 0
for q in a:
    n = []
    for i, r in enumerate((a[q], b[q])):
        js = [J[f"{q}|{p}"] for p in ctx(r)]
        tot[i].update(js); n.append(js.count(2)); any2[i] += 2 in js
    for p in ctx(b[q]):
        if p in NEW: newpos += 1; new2 += J[f"{q}|{p}"] == 2
    w += n[1] > n[0]; l += n[1] < n[0]
    print(f"  {q}: '2' {n[0]} → {n[1]} | 편수 {len(ctx(a[q]))} → {len(ctx(b[q]))} | 검색어 후 {b[q]['rag_queries'][:1]}")
print(f"주: '2' 합 {tot[0][2]} → {tot[1][2]} | 늘어남 {w} : 줄어듦 {l} · p {sign(w, l):.4f}")
print(f"부: '2' 있는 질문 {any2[0]} → {any2[1]} / {len(a)}")
print(f"보호: '0' 합 {tot[0][0]} → {tot[1][0]} · '1' 합 {tot[0][1]} → {tot[1][1]}")
print(f"보고: 수집 논문이 든 자리 {newpos}(그중 '2' {new2}) · 시간 중앙 {median(r['elapsed'] for r in a.values()):.1f}s → {median(r['elapsed'] for r in b.values()):.1f}s")
