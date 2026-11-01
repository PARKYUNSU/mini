"""ce_rerank_1101 채점 (README §3 · §4). `score.py gate` 는 dev 관문만 보고 미달이면 1 로 끝난다."""
import json, sys
from math import comb
from pathlib import Path
from statistics import median

D = Path(__file__).parent; E = D.parent; R = E / "e2e_ko_1008/results"
load = lambda a, s: {r["id"]: r for r in map(json.loads, open(R / f"pc{a}_{s}.jsonl"))}
sign = lambda w, l: 1.0 if w + l == 0 else min(1, 2 * sum(comb(w + l, i) for i in range(min(w, l) + 1)) / 2 ** (w + l))
ctx = lambda r: r["context_papers"]

print("dev 관문 (§4.1)")
G = L = 0
rows = {0: [], 1: []}
for s in ("162", "real40", "real2"):
    a, b = load(0, s), load(1, s)
    assert a.keys() == b.keys(), s
    rows[0] += a.values(); rows[1] += b.values()
    g = sum(b[q]["ok"] and not a[q]["ok"] for q in a); l = sum(a[q]["ok"] and not b[q]["ok"] for q in a)
    G += g; L += l
    print(f"  {s}: ok {sum(r['ok'] for r in a.values())} → {sum(r['ok'] for r in b.values())} / {len(a)} · 얻음 {g} : 잃음 {l}"
          f" · 경로 다름 {sum(a[q]['route'] != b[q]['route'] for q in a)}"
          f" · 컨텍스트 편수 평균 {sum(len(ctx(r)) for r in a.values()) / len(a):.2f} → {sum(len(ctx(r)) for r in b.values()) / len(b):.2f}")
gate = G - L >= 3 and G >= 2 * L
print(f"  합 얻음 {G} : 잃음 {L} (순 {G - L:+d}, p {sign(G, L):.3f}) → {'통과' if gate else '미달 — R1 접음'}")
if not gate or sys.argv[1:] == ["gate"]:
    sys.exit(0 if gate else 1)

a, b = load(0, "heldout"), load(1, "heldout")
assert a.keys() == b.keys()
rows[0] += a.values(); rows[1] += b.values()
pool = {x["k"]: x for x in json.load(open(D / "pool.json"))}
J = {}
for line in open(D / "judged.txt"):
    k, v = line.split()
    J[pool[int(k)]["q"], pool[int(k)]["p"]] = int(v)
assert len(J) == len(pool), f"판정 {len(J)} / 쌍 {len(pool)}"
w = l = 0; only = {0: [], 1: []}
for q in a:
    n = []
    for i, (x, y) in enumerate(((a[q], b[q]), (b[q], a[q]))):
        js = [J[q, p] for p in ctx(x) if p not in ctx(y)]
        only[i] += js  # i=0: 끔에만 · i=1: 켬에만
        n.append(js.count(2))
    w += n[1] > n[0]; l += n[1] < n[0]
p = sign(w, l)
r2 = {i: only[i].count(2) / max(len(only[i]), 1) for i in (0, 1)}
print(f"held-out 주 (§4.2): '2' 개수 늘어남 {w} : 줄어듦 {l} · 동점 {len(a) - w - l} · p {p:.4f} → {'통과' if w > l and p < 0.05 else '미달'}")
print(f"  한쪽에만 든 논문: 끔 {len(only[0])}편('2' {only[0].count(2)} · '1' {only[0].count(1)} · '0' {only[0].count(0)})"
      f" · 켬 {len(only[1])}편('2' {only[1].count(2)} · '1' {only[1].count(1)} · '0' {only[1].count(0)})")
B = [q for q in a if q.startswith("H_B")]
bg = sum(b[q]["ok"] and not a[q]["ok"] for q in B); bl = sum(a[q]["ok"] and not b[q]["ok"] for q in B)
el = {i: median(r["elapsed"] for r in rows[i]) for i in (0, 1)}
er = {i: sum(bool(r["error"]) for r in rows[i]) for i in (0, 1)}
prot = {
    f"'2' 비율 끔 {r2[0]:.1%} → 켬 {r2[1]:.1%} (하락 < 5%p)": r2[0] - r2[1] < 0.05,
    f"B 층 정답 얻음 {bg} : 잃음 {bl} (잃음 ≤ 1)": bl <= 1,
    f"오류 행 {er[0]} → {er[1]} (켬 ≤ 끔)": er[1] <= er[0],
    f"문항 시간 중앙 {el[0]:.1f}s → {el[1]:.1f}s (+≤ 3s)": el[1] - el[0] <= 3.0,
}
for k_, v in prot.items():
    print(("  통과 " if v else "  미달 ") + k_)
st = {i: {} for i in (0, 1)}
for i in (0, 1):
    for r in rows[i]:
        for name, sec in r.get("stages") or []:
            st[i].setdefault(name, []).append(sec)
print("  단계 시간 중앙(끔 → 켬): " + " · ".join(f"{k_} {median(st[0][k_]):.1f} → {median(st[1].get(k_, [0])):.1f}" for k_ in st[0]))
print("→ 채택 제안" if w > l and p < 0.05 and all(prot.values()) else "→ 기각")
