"""qcond_1025 집계."""
import collections
from pathlib import Path
D = Path(__file__).parent
rows = [l.split("\t") for l in open(D / "judged.tsv").read().splitlines()[1:]]
conds = [l.split("\t") for l in open(D / "conditions.tsv").read().splitlines()[1:]]
idx = collections.Counter(); ty = {}
for q, t, _ in conds:
    ty[(q, str(idx[q]))] = t; idx[q] += 1
rows = [r for r in rows if r[2] != "N/A"]
ans = collections.defaultdict(list)
for q, i, lab, ctx, *_ in rows:
    ans[q].append((lab, ctx))
bad = [q for q, v in ans.items() if any(l in "UF" for l, _ in v)]
print(f"판정 답 {len(ans)} · 조건 문제 답 {len(bad)} ({len(bad)/len(ans):.0%}) {bad}")
print("조건 라벨", dict(collections.Counter(r[2] for r in rows)), "· 조건", len(rows))
by = collections.defaultdict(collections.Counter)
for q, i, lab, ctx, *_ in rows:
    by[ty[(q, i)]][lab] += 1
for t, c in by.items():
    print(" ", t, dict(c))
print("U·F 컨텍스트", dict(collections.Counter(r[3] for r in rows if r[2] in "UF")))
print("D 컨텍스트", dict(collections.Counter(r[3] for r in rows if r[2] == "D")))
