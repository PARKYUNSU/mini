"""relevance_filter_1022 2단계 판정 (맥미니)."""
import json, re, statistics as st, sys
from math import comb
from pathlib import Path
sys.path.insert(0, ".")
from scripts.score_real_eval import score

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"
SETS = {"real40": "real_eval_1013", "real2": "real_eval2_1015"}
rows = {a: {} for a in ("rf0", "rf1")}; gold = {}
for t, d in SETS.items():
    for l in open(EXP / d / "gold.jsonl"):
        g = json.loads(l); gold[(t, g["id"])] = {re.sub(r"v\d+$", "", p) for p in g["relevant_papers"]}
    for a in rows:
        for l in open(R / f"{a}_{t}.jsonl"):
            r = json.loads(l); rows[a][(t, r["id"])] = r
keys = [k for k in rows["rf0"] if k in rows["rf1"]]
non = {a: {k: len(set(re.findall(r"\[(\d{4}\.\d{4,5})", rows[a][k].get("answer") or "")) - gold.get(k, set())) for k in keys} for a in rows}
b = sum(non["rf1"][k] < non["rf0"][k] for k in keys); c = sum(non["rf1"][k] > non["rf0"][k] for k in keys); n = b + c
p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)
print(f"주: 답이 인용한 gold 아닌 논문 합 대조 {sum(non['rf0'].values())} · 처리 {sum(non['rf1'].values())} | 처리가 적은 문항 {b} : 많은 문항 {c}, 부호 검정 p={p:.4f}")
for t, d in SETS.items():
    s = {a: score(f"{a}_{t}", EXP / d) for a in rows}
    f = lambda x: (sum(r["ok"] for r in x["N"]), sum(r["both_cited"] for r in x["C"]), sum(r["gold_cited"] >= 3 for r in x["T"]))
    ok = {a: sum(rows[a][k]["ok"] for k in keys if k[0] == t) for a in rows}
    print(f"   보호 {t}: 검색 ok {ok['rf0']} → {ok['rf1']} · N 정답 · C 두 편 · T≥3 {f(s['rf0'])} → {f(s['rf1'])}")
for a in rows:
    one = sum(len(set(rows[a][k].get("doc_ids") or [])) == 1 for k in keys)
    print(f"   {a}: 응답 시간 중앙 {st.median(rows[a][k]['elapsed'] for k in keys):.1f}s · 남은 문서 1편인 답 {one}")
