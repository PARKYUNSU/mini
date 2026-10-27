"""fusion_protect_1027 §3 채점 (판정 끝난 뒤 조건 열기)."""
import json
from math import comb
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "fusion_protect_1027/"
pool = {x["k"]: x for x in json.load(open(D + "pool.json"))}
J = json.load(open(D + "reused.json"))
for l in open(D + "judged.txt"):
    k, v = l.split(); J[f"{pool[int(k)]['q']}|{pool[int(k)]['p']}"] = int(v)
def sign(w, l):
    n = w + l
    return 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n)
load = lambda a, s: {json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}_{s}.jsonl")}
ctx = lambda r: r.get("doc_ids") or r["context_papers"]
print("보호 — 정답 세트 검색 ok")
for s in ("162", "real40", "real2"):
    a, b = load("fp0", s), load("fp1", s)
    print(f"  {s}: {sum(r['ok'] for r in a.values())} → {sum(r['ok'] for r in b.values())} / {len(a)} (처리만 {sum(b[q]['ok'] and not a[q]['ok'] for q in a)} · 대조만 {sum(a[q]['ok'] and not b[q]['ok'] for q in a)})")
w = l = 0; tot = {"fp0": 0, "fp1": 0}; inn = out = 0; nch = 0
for s in ("H", "D", "U"):
    a = {k: load(k, s) for k in ("fp0", "fp1")}
    sw = sl = 0
    for q in a["fp0"]:
        c0, c1 = ctx(a["fp0"][q]), ctx(a["fp1"][q])
        n = {k: sum(J[f"{q}|{p}"] == 2 for p in ctx(a[k][q])) for k in a}
        tot["fp0"] += n["fp0"]; tot["fp1"] += n["fp1"]
        sw += n["fp1"] > n["fp0"]; sl += n["fp1"] < n["fp0"]
        if set(c0) != set(c1):
            nch += 1
            i2 = [J[f"{q}|{p}"] for p in c1 if p not in c0]; o2 = [J[f"{q}|{p}"] for p in c0 if p not in c1]
            inn += i2.count(2); out += o2.count(2)
            print(f"   {q}: 들어옴 {i2} · 빠짐 {o2}")
    print(f"  [{s}] '2' 늘어남 {sw} : 줄어듦 {sl}")
    w += sw; l += sl
print(f"주: '2' 합 {tot['fp0']} → {tot['fp1']} | 늘어남 {w} : 줄어듦 {l} · p {sign(w, l):.4f}")
print(f"보호: 컨텍스트 바뀐 문항 {nch} · 들어온 '2' {inn} vs 빠진 '2' {out}")
u = {k: load(k, "U") for k in ("fp0", "fp1")}
g = ["2503.17229", "2508.14314"]
print("U1-4 정답:", {k: [p for p in g if p in ctx(u[k]["U1-4"])] for k in u}, "검색어", u["fp1"]["U1-4"]["rag_queries"][0])
