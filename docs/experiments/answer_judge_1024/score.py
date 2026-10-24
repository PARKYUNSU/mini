"""answer_judge_1024 집계."""
import collections, re
from pathlib import Path
D = Path("docs/experiments/answer_judge_1024")
sec = {}; typ = {}
for l in open(D / "sample.md"):
    m = re.match(r"######## A(\d\d) \[(\w)\]", l)
    if m:
        cur = m.group(1); typ[cur] = m.group(2)
    m = re.match(r"(C\d\d\.\d\d) \[(\S+)\]", l)
    if m:
        sec[m.group(1)] = m.group(2)
C = [l.split("\t") for l in open(D / "judged_claims.tsv").read().splitlines()[1:]]
L = "OEXUF?"
def row(name, xs):
    c = collections.Counter(x[1] for x in xs); n = len(xs)
    print(f"{name:10s} 주장 {n:3d} | " + " · ".join(f"{k} {c[k]} ({100 * c[k] / n:.0f}%)" for k in L))
row("전체", C)
for s in ("서론", "본론", "결론"):
    row(s, [c for c in C if sec[c[0]] == s])
for t in "NCTR":
    row(f"유형 {t}", [c for c in C if typ[c[0][1:3]] == t])
bad = [c for c in C if c[1] in "EXU"]
print("오류 주장이 1개 이상인 답", len({c[0][:3] for c in bad}), "/ 20")
A = [l.split("\t") for l in open(D / "judged_answers.tsv").read().splitlines()[1:]]
for i, n in enumerate(("결과 누락", "질문 조건 미충족", "1편 미고지", "무관 논문 비중"), 1):
    print(f"답: {n} {sum(int(a[i]) for a in A)}/20 {[a[0] for a in A if a[i] == '1']}")
