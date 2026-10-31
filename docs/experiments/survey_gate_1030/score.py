"""survey_gate_1030 §3 채점: judged.txt(조건 모른 판정) → 주 지표 · 보호 · 보고."""
import json, statistics
from math import comb
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "survey_gate_1030/"
pool = json.load(open(D + "pool.json"))
lab = {int(k): int(v) for k, v in (l.split() for l in open(D + "judged.txt") if l.strip())}
J = {(x["q"], x["p"]): lab[x["k"]] for x in pool}
arms = {a: {json.loads(l)["id"]: json.loads(l) for s in ("new", "old") for l in open(R + f"{a}_{s}.jsonl")} for a in ("sg0", "sg1")}
gold = {json.loads(l)["id"]: json.loads(l) for s in ("new", "old") for l in open(D + f"{s}_gold.jsonl")}
def body_cites(r):  # pool.py 와 같은 규칙(📎 외부 목록 앞 본문만)
    body = (r.get("answer") or "").split("📎")[0]
    return [p for p in (r.get("answer_papers") or []) if p in body]


NODOC = ("찾을 수 없", "질문이 찾는 연구가 없")
def stat(r):
    c = body_cites(r); ls = [J[(r["id"], p)] for p in c]
    ctx = set(r.get("doc_ids") or r.get("context_papers") or [])
    ans = r.get("answer") or ""
    return dict(n2=ls.count(2), n0=ls.count(0), n1=ls.count(1), n=len(c), out=sum(p not in ctx for p in c),
                nodoc=any(s in ans.split("📎")[0] for s in NODOC), ext=ans.count("\n• ") if "📎" in ans else 0, t=r.get("elapsed") or 0)
S = {a: {q: stat(r) for q, r in arms[a].items()} for a in arms}
qs = list(arms["sg0"]); up = sum(S["sg1"][q]["n2"] > S["sg0"][q]["n2"] for q in qs); dn = sum(S["sg1"][q]["n2"] < S["sg0"][q]["n2"] for q in qs)
n = up + dn; k = min(up, dn); p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n) if n else 1.0
tot = lambda a, f: sum(S[a][q][f] for q in qs)
print(f"주: '2' 합 {tot('sg0','n2')} → {tot('sg1','n2')} · 늘어남 {up} : 줄어듦 {dn} (동점 {len(qs)-n}) · p {p:.4g}")
for f in ("n0", "n1", "n", "out", "nodoc", "ext"):
    print(f, tot("sg0", f), "→", tot("sg1", f))
print("시간 중앙", statistics.median(S["sg0"][q]["t"] for q in qs), "→", statistics.median(S["sg1"][q]["t"] for q in qs))
g = [q for q in qs if gold.get(q, {}).get("relevant_papers")]
print("정답 있는 문항", g, "answer_ok", [arms["sg0"][q].get("answer_ok") for q in g], "→", [arms["sg1"][q].get("answer_ok") for q in g])
for q in qs:
    a, b = S["sg0"][q], S["sg1"][q]
    if (a["n2"], a["n0"], a["n"], a["nodoc"]) != (b["n2"], b["n0"], b["n"], b["nodoc"]) or q in ("S13", "er_R_134"):
        print(f"  {q}: 2 {a['n2']}→{b['n2']} · 0 {a['n0']}→{b['n0']} · 인용 {a['n']}→{b['n']} · 없음 {a['nodoc']}→{b['nodoc']} · 외부 {a['ext']}→{b['ext']}")
