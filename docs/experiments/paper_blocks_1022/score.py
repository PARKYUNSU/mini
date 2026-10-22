"""paper_blocks_1022 §3 판정 (맥미니)."""
import json, re, statistics as st, sys
from math import comb
from pathlib import Path
sys.path.insert(0, ".")
from scripts.score_real_eval import score

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"
SETS = {"real40": "real_eval_1013", "real2": "real_eval2_1015"}
A = ("pb0", "pb1"); rows = {a: {} for a in A}; gold = {}
for t, d in SETS.items():
    for l in open(EXP / d / "gold.jsonl"):
        g = json.loads(l); gold[(t, g["id"])] = {re.sub(r"v\d+$", "", p) for p in g["relevant_papers"]}
    for a in A:
        for l in open(R / f"{a}_{t}.jsonl"):
            r = json.loads(l); rows[a][(t, r["id"])] = r
keys = [k for k in rows["pb0"] if k in rows["pb1"]]
cited = lambda a, k: set(re.findall(r"\[(\d{4}\.\d{4,5})", rows[a][k].get("answer") or ""))
gc = {a: {k: len(cited(a, k) & gold.get(k, set())) for k in keys} for a in A}
ng = {a: sum(len(cited(a, k) - gold.get(k, set())) for k in keys) for a in A}
b = sum(gc["pb1"][k] > gc["pb0"][k] for k in keys); c = sum(gc["pb1"][k] < gc["pb0"][k] for k in keys); n = b + c
p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)
for a in A:
    ids = [rows[a][k].get("doc_ids") or [] for k in keys]
    print(f"{a}: 같은 논문 두 칸 이상인 답 {sum(len(x) != len(set(x)) for x in ids)} · 서로 다른 논문 평균 {st.mean(len(set(x)) for x in ids):.2f} · "
          f"컨텍스트 안 gold {sum(len(set(rows[a][k].get('doc_ids') or []) & gold.get(k, set())) for k in keys)} · 1편만 남은 답 {sum(len(set(x)) == 1 for x in ids)} · "
          f"답 인용 gold {sum(gc[a].values())} · gold 아닌 인용 {ng[a]} · 응답 시간 중앙 {st.median(rows[a][k]['elapsed'] for k in keys):.1f}s")
print(f"주(효과): 답 인용 gold 처리가 많은 문항 {b} : 적은 문항 {c}, p={p:.4f}")
for t, d in SETS.items():
    s = {a: score(f"{a}_{t}", EXP / d) for a in A}
    f = lambda x: (sum(r["ok"] for r in x["N"]), sum(r["both_cited"] for r in x["C"]), sum(r["gold_cited"] >= 3 for r in x["T"]))
    ok = {a: sum(rows[a][k]["ok"] for k in keys if k[0] == t) for a in A}
    print(f"   보호 {t}: 검색 ok {ok['pb0']} → {ok['pb1']} · N 정답 · C 두 편 · T≥3 {f(s['pb0'])} → {f(s['pb1'])}")
