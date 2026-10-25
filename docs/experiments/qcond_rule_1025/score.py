"""qcond_rule_1025 공개 · 집계: judged.tsv(A·B) + blind_key.json → cr0 · cr1."""
import json, math, collections
from pathlib import Path
D = Path(__file__).parent
key = json.load(open(D / "blind_key.json"))
bad = collections.defaultdict(lambda: {"cr0": 0, "cr1": 0}); lab = {"cr0": collections.Counter(), "cr1": collections.Counter()}
by = collections.defaultdict(collections.Counter)
for l in open(D / "judged.tsv").read().splitlines()[1:]:
    q, t, a, b = l.split("\t")
    for v, arm in zip((a, b), key[q]):
        if v == "N/A":
            continue
        lab[arm][v] += 1; by[(t, arm)][v] += 1; bad[q][arm] += v in "UF"
win = sum(v["cr1"] < v["cr0"] for v in bad.values()); lose = sum(v["cr1"] > v["cr0"] for v in bad.values())
n = win + lose; p = min(1, 2 * sum(math.comb(n, i) for i in range(min(win, lose) + 1)) / 2 ** n) if n else 1
print(f"질문 {len(bad)} · cr1 적음 {win} : 많음 {lose} · p {p:.4f}")
for arm in ("cr0", "cr1"):
    print(arm, dict(lab[arm]), "U+F 질문", sum(v[arm] > 0 for v in bad.values()))
for (t, arm), c in sorted(by.items()):
    print(" ", t, arm, dict(c))
