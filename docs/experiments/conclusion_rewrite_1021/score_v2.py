"""§8 판정: v1(2차) 대 v2 — 좋은 결론 = 근거 결과 있음 그리고 본론 재서술 아님(12-gram 겹침 < 25%)."""
import json, re, statistics as st
from collections import Counter
from math import comb
from pathlib import Path

D = Path("docs/experiments/conclusion_rewrite_1021"); E = Path("docs/experiments/e2e_ko_1008/results")
g = {}
exec((D / "offline.py").read_text().split("qs = {}")[0], g)


def norm(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>|\[\d{4}\.\d{4,5}(?:v\d+)?\]", "", t or "")).strip()
def sh(t, n=12): return {t[i:i + n] for i in range(max(0, len(t) - n + 1))}
def body(a):
    b, c = g["_find"]("본론", a), g["_find"]("결론", a)
    return a[b.end():c.start()] if b and c else ""


R = {}
for arm, suf in (("v1", "_concl_v1b"), ("v2", "_concl_v2")):
    for lbl in ("s18_real40", "s18_real2"):
        for l in open(E / f"{lbl}{suf}.jsonl"):
            r = json.loads(l); a = r.get("answer") or ""; ctx = r.get("numbered_context") or ""; ids = dict(enumerate(r.get("doc_ids") or [], 1))
            cc = norm(g["concl"](a)); ov = len(sh(cc) & sh(norm(body(a)))) / max(1, len(sh(cc)))
            gr = g["grounded"](a, ctx, ids)
            R.setdefault((lbl, r["id"]), {})[arm] = {"g": gr, "ov": ov, "good": gr and ov < 0.25, "o": g["outside"](a, ctx, ids), "c": g["concl"](a)}
meta = {(x["set"], x["id"]): x for x in map(json.loads, open(D / "results_v2.jsonl"))}
m1 = {(x["set"], x["id"]): x for x in map(json.loads, open(D / "results_v1b.jsonl"))}
tg = [k for k in R if meta[k]["why"] != "대상 아님"]
b = sum(R[k]["v2"]["good"] and not R[k]["v1"]["good"] for k in tg); c = sum(R[k]["v1"]["good"] and not R[k]["v2"]["good"] for k in tg); n = b + c
p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)
for arm in ("v1", "v2"):
    print(f"{arm}: 좋은 결론 {sum(R[k][arm]['good'] for k in tg)} · 근거 결과 {sum(R[k][arm]['g'] for k in tg)} · 재서술(겹침≥25%) {sum(R[k][arm]['ov'] >= 0.25 for k in tg)} · 겹침 중앙 {st.median(R[k][arm]['ov'] for k in tg):.2f} · 인용 밖 숫자 {sum(R[k][arm]['o'] for k in tg)} / 대상 {len(tg)}")
print(f"주: 좋은 결론 v2만 {b} : v1만 {c}, p={p:.4f}")
print(f"바꿈 v1 {sum(m1[k]['why'] == '바꿈' for k in tg)} · v2 {sum(meta[k]['why'] == '바꿈' for k in tg)} · 시간 중앙 v1 {st.median(m1[k]['sec'] for k in tg):.1f}s v2 {st.median(meta[k]['sec'] for k in tg):.1f}s")
print("v2 탈락:", Counter(re.sub(r" \S+$", "", meta[k]["why"]) for k in tg if meta[k]["why"] != "바꿈"))
