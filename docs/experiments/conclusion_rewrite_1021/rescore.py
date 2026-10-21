"""offline.py 채점기 수정(같은 논문 블록 합치기 · [2] 찌꺼기 빼기) 뒤 LLM 없이 저장된 전/후 답으로 다시 채점."""
import json
from collections import Counter
from math import comb
from pathlib import Path

D = Path("docs/experiments/conclusion_rewrite_1021"); E = Path("docs/experiments/e2e_ko_1008/results")
g = {}
exec((D / "offline.py").read_text().split("qs = {}")[0], g)
res = [json.loads(l) for l in open(D / "results.jsonl")]
key = {(x["set"], x["id"]): x for x in res}
for lbl in ("s18_real40", "s18_real2"):
    old = {json.loads(l)["id"]: json.loads(l) for l in open(E / f"{lbl}.jsonl")}
    for l in open(E / f"{lbl}_concl.jsonl"):
        r = json.loads(l); o = old[r["id"]]; x = key[(lbl, r["id"])]
        ids = dict(enumerate(r.get("doc_ids") or [], 1)); ctx = r.get("numbered_context") or ""
        x["g0"], x["g1"] = g["grounded"](o["answer"] or "", ctx, ids), g["grounded"](r["answer"] or "", ctx, ids)
        x["o0"], x["o1"] = g["outside"](o["answer"] or "", ctx, ids), g["outside"](r["answer"] or "", ctx, ids)
with open(D / "results.jsonl", "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in res)
tg = [x for x in res if x["why"] != "대상 아님"]
b = sum(x["g1"] and not x["g0"] for x in tg); c = sum(x["g0"] and not x["g1"] for x in tg); n = b + c
p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n)
print(f"주: 근거 결과 결론 전 {sum(x['g0'] for x in tg)} → 후 {sum(x['g1'] for x in tg)} (후만 {b} : 전만 {c}, p={p:.4f}) / 대상 {len(tg)}")
print(f"인용 밖 숫자: 전 {sum(x['o0'] for x in tg)} · 후 {sum(x['o1'] for x in tg)} {[x['id'] for x in tg if x['o1']]}")
print("전만:", [(x["set"], x["id"], x["why"]) for x in tg if x["g0"] and not x["g1"]])
print("바꿈 중 근거 결과:", sum(x["g1"] for x in tg if x["why"] == "바꿈"), "/", sum(x["why"] == "바꿈" for x in tg))
