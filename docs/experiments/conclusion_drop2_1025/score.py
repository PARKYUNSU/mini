"""conclusion_drop2_1025 채점: 판정 라벨 + 규칙(results.jsonl 의 drop) → 전 · 후 (E+X)."""
import json, math, collections
from pathlib import Path
D = Path(__file__).parent
key = json.load(open(D / "blind_key.json")); res = {x["id"]: x for x in map(json.loads, open(D / "results.jsonl"))}
lab = dict(l.split("\t") for l in open(D / "blind_judged.tsv").read().splitlines()[1:])
win = lose = 0; rm = collections.Counter(); kind = collections.Counter(); conn = 0; lost_g = 0
for q, qid in key.items():
    x = res[qid]; s = [lab.get(f"{q}.{j}") for j in range(len(x["sents"]))]
    before = sum(v in ("E", "X") for v in s)
    after = sum(v in ("E", "X") for v, d in zip(s, x["drop"]) if not d)
    win += after < before; lose += after > before
    for v, d in zip(s, x["drop"]):
        if d: rm[v] += 1; kind[d] += 1
    conn += x["after"].lstrip().startswith(("반면", "또한", "따라서", "이러한"))
    lost_g += x["grounded_before"] and not x["grounded_after"]
n = win + lose
p = min(1, 2 * sum(math.comb(n, i) for i in range(min(win, lose) + 1)) / 2 ** n) if n else 1
o = rm["O"] / max(1, sum(rm.values()))
print(f"규칙 적용 {len(key)} · 뒤 적음 {win} : 많음 {lose} · p {p:.4f}")
print("지운 문장 라벨", dict(rm), f"O 비율 {o:.2f}", "· 종류", dict(kind))
print("근거 결과 잃음", lost_g, "· 첫 문장 접속어", conn)
