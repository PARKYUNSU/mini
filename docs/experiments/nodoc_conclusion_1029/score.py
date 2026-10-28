"""nodoc_conclusion_1029 §3 채점 (규칙)."""
import json, re
from math import comb
from statistics import median
R = "docs/experiments/e2e_ko_1008/results/"
NO = re.compile(r"없습니다|찾을 수 없")
HINT = "따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다"
def sec(a, name):
    m = re.search(rf"<b>{name}</b>(.*?)(?=<b>(?:서론|본론|결론)</b>|📎|$)", a, re.S)
    return m.group(1).strip() if m else None
def contra(a):
    i, c = sec(a, "서론"), sec(a, "결론")
    return bool(i and NO.search(i)) and not (c and re.search(r"없", c))
load = lambda a: {json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}.jsonl")}
A = {k: load(k) for k in ("nk0", "nk1")}
picks = {k: [] for k in A}
for k in A:
    q = None
    for l in open(f".cron/{k}.log"):
        if "정답 유무 판정 = 없음" in l: q = True
        m = re.match(r"\[\d+/\d+\] (\S+) ok=", l)
        if m:
            if q: picks[k].append(m.group(1))
            q = None
w = l = 0
for q in A["nk0"]:
    a, b = contra(A["nk0"][q]["answer"]), contra(A["nk1"][q]["answer"])
    w += a and not b; l += b and not a
    print(f"  {q}: 모순 {int(a)} → {int(b)}")
n = w + l
p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n)
for k in A:
    ans = [r["answer"] for r in A[k].values()]
    print(f"{k}: 모순 {sum(map(contra, ans))} · 결론 빠짐 {sum(sec(x, '결론') is None for x in ans)} · 결론 첫 문장=지시 {sum(HINT in (sec(x, '결론') or '')[:80] for x in ans)} · (관련 연구) {sum('(관련 연구)' in x for x in ans)} · 시간 중앙 {median(r['elapsed'] for r in A[k].values()):.1f}s · 판정 없음 {len(picks[k])}")
print(f"주: 줄어듦 {w} : 늘어남(처리만 모순) {l} · p {p:.4f}")
