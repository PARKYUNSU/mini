"""canon_1110 사후 보고(등록 뒤 추가, 판정에 안 씀): 검토 답변(11-10) 요청 — 주제 밖 22건을 뺀 주 지표 + 문항별 내역.

    .venv/bin/python docs/experiments/canon_1110/extra.py
"""
import csv
import importlib.util
import json
from pathlib import Path

D = Path("docs/experiments/canon_1110")
spec = importlib.util.spec_from_file_location("canon_score", D / "score.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

P = {x["k"]: x for x in json.loads((D / "pool.json").read_text(encoding="utf-8"))}
J = {}
for l in (D / "judged.txt").read_text(encoding="utf-8").splitlines():
    if l.strip():
        k, v = l.split()
        J[(P[int(k)]["set"], P[int(k)]["q"], P[int(k)]["p"])] = int(v)
off = {r["id"] for r in csv.DictReader(open(D / "offtopic.tsv", encoding="utf-8"), delimiter="\t") if r["판정"] == "밖"}
new = {p["id"] for p in S.cand()["papers"]}
assert len(off) == 22 and off <= new
title = {p["id"]: p["title"] for p in S.cand()["papers"]}

b, a = S.rows("cn0_canon"), S.rows("cn1_canon")
win = lose = 0
print("문항 | 전 '2' | 후 '2' | 후 '2' (주제 밖 뺌) | 후에 새로 든 수집 논문(판정)")
for q in b:
    if S.ctx(b[q]) == S.ctx(a[q]):
        continue
    nb = sum(J[("canon", q, p)] == 2 for p in S.ctx(b[q]))
    na = sum(J[("canon", q, p)] == 2 for p in S.ctx(a[q]))
    na_off = sum(J[("canon", q, p)] == 2 for p in S.ctx(a[q]) - off)
    win += na_off > nb
    lose += na_off < nb
    got = [f"{p}({J[('canon', q, p)]}{', 밖' if p in off else ''})" for p in sorted(S.ctx(a[q]) & new)]
    print(f"{q} | {nb} | {na} | {na_off} | {' '.join(got) or '-'}")
print(f"주제 밖 22건 자리 빼고: '2' 늘어남 {win} : 줄어듦 {lose} · p {S.sign_p(win, lose):.4g}")
print("주제 밖 논문이 든 자리(대상 · held-out):",
      sum(len(S.ctx(a[q]) & off) for q in a), "·", sum(len(S.ctx(r) & off) for r in S.rows("cn1_heldout").values()))
