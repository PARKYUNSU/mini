"""topic_judge_1024 집계: 판정(judged.tsv)에 조건을 붙인다."""
import json, statistics as st
from math import comb
from pathlib import Path
D = Path("docs/experiments/topic_judge_1024")
key = json.load(open(D / "pool_key.json")); ctx = json.load(open(D / "contexts.json"))
g = {tuple(key[l.split("\t")[0]]): int(l.split("\t")[1]) for l in open(D / "judged.tsv").read().splitlines()[1:]}
def stats(cond, sets=None):
    rows = [(k, v) for k, v in ctx.items() if k.split("|")[0] == cond and (sets is None or k.split("|")[1] in sets)]
    two = {k.split("|", 1)[1]: sum(g[(k.split("|")[1], k.split("|")[2], p)] == 2 for p in v) for k, v in rows}
    zero = sum(g[(k.split("|")[1], k.split("|")[2], p)] == 0 for k, v in rows for p in v); n = sum(len(v) for _, v in rows)
    return two, zero, n
two, zero, n = stats("ops")
print(f"운영 기준선 {len(two)}문항: 문항당 '2' 평균 {st.mean(two.values()):.2f} · '2' 1편 이상 {sum(v > 0 for v in two.values())}/{len(two)} · 컨텍스트 '0' {zero}/{n} = {zero / n:.0%}")
for s in ("real40", "real2", "m12", "cs3"):
    t, z, m = stats("ops", {s})
    print(f"   {s}: 문항 {len(t)} · '2' 평균 {st.mean(t.values()):.2f} · 0건 문항 {[k for k, v in t.items() if v == 0]} · '0' {z}/{m}")
base, bz, bn = stats("ops", {"m12", "cs3"})
for cond in ("nofilter", "nolr"):
    t, z, m = stats(cond, {"m12", "cs3"})
    ks = [k for k in base if k in t]
    b = sum(t[k] > base[k] for k in ks); c = sum(t[k] < base[k] for k in ks)
    p = 1.0 if b + c == 0 else min(1, 2 * sum(comb(b + c, i) for i in range(min(b, c) + 1)) / 2 ** (b + c))
    print(f"{cond} 대 운영 (조건 세트 + R 3, {len(ks)}문항): '2' 합 {sum(base[k] for k in ks)} → {sum(t[k] for k in ks)} · 많음 {b} : 적음 {c}, p={p:.3f} · '0' {bz}/{bn} → {z}/{m}")
