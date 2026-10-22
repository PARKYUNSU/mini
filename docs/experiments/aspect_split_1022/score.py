"""aspect_split_1022 §3 판정 (맥미니)."""
import json, re, statistics as st, sys
from math import comb
from pathlib import Path
sys.path.insert(0, ".")
from scripts.score_real_eval import score

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "aspect_split_1022"
A = ("as0", "as1")
ASP = json.load(open(D / "aspects.json"))
m = {a: {json.loads(l)["id"]: json.loads(l) for l in open(R / f"{a}_m12.jsonl")} for a in A}
cov, cit = {a: {} for a in A}, {a: {} for a in A}
for a in A:
    for q, asp in ASP.items():
        r = m[a].get(q, {}); ctx = set(r.get("doc_ids") or []); ans = set(re.findall(r"\[(\d{4}\.\d{4,5})", r.get("answer") or ""))
        for name, gold in asp.items():
            cov[a][(q, name)] = bool(ctx & set(gold)); cit[a][(q, name)] = bool(ans & set(gold))
keys = list(cov["as0"])
b = sum(cov["as1"][k] and not cov["as0"][k] for k in keys); c = sum(cov["as0"][k] and not cov["as1"][k] for k in keys); n = b + c
p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)
print(f"주: 컨텍스트 조건 커버 대조 {sum(cov['as0'].values())} · 처리 {sum(cov['as1'].values())} / {len(keys)} | 처리만 {b} : 대조만 {c}, p={p:.4f}")
print(f"보조: 답 인용 조건 커버 대조 {sum(cit['as0'].values())} · 처리 {sum(cit['as1'].values())} / {len(keys)}")
for k in keys:
    print(f"   {k[0]} {k[1]}: 컨텍스트 {int(cov['as0'][k])}→{int(cov['as1'][k])} · 인용 {int(cit['as0'][k])}→{int(cit['as1'][k])}")
SETS = {"real40": "real_eval_1013", "real2": "real_eval2_1015"}
rows = {a: {(t, json.loads(l)["id"]): json.loads(l) for t in SETS for l in open(R / f"{a}_{t}.jsonl")} for a in A}
ks = [k for k in rows["as0"] if k in rows["as1"]]
for t, d in SETS.items():
    s = {a: score(f"{a}_{t}", EXP / d) for a in A}
    f = lambda x: (sum(r["ok"] for r in x["N"]), sum(r["both_cited"] for r in x["C"]), sum(r["gold_cited"] >= 3 for r in x["T"]))
    ok = {a: sum(rows[a][k]["ok"] for k in ks if k[0] == t) for a in A}
    print(f"   보호 {t}: 검색 ok {ok['as0']} → {ok['as1']} · N 정답 · C 두 편 · T≥3 {f(s['as0'])} → {f(s['as1'])}")
for a in A:
    print(f"   {a}: 응답 시간 중앙 74문항 {st.median(rows[a][k]['elapsed'] for k in ks):.1f}s · 조건 세트 {st.median(r['elapsed'] for r in m[a].values()):.1f}s")
