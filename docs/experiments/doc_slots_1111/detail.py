"""doc_slots_1111 문항별 내역(보고용): 칸 틀 적용 여부 · 본론 항목 · 라벨별 인용 수.

    .venv/bin/python docs/experiments/doc_slots_1111/detail.py
"""
import importlib.util
import json
from pathlib import Path

D = Path("docs/experiments/doc_slots_1111")
spec = importlib.util.spec_from_file_location("ds_score", D / "score.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
S = M.S
J = M.known()
P = {x["k"]: x for x in json.loads((D / "pool.json").read_text(encoding="utf-8"))}
for l in (D / "judged.txt").read_text(encoding="utf-8").splitlines():
    if l.strip():
        k, v = l.split()
        J[(P[int(k)]["q"], P[int(k)]["p"])] = int(v)
a, b = S.rows("ds0_canon"), S.rows("ds1_canon")
up = down = same_applied = 0
print("문항 | 칸 틀 | 문서 수 | 항목 대조→처리 | '2' | '1' | '0' | 컨텍스트 같음")
for q in a:
    x, y = a[q], b[q]
    ap = any(isinstance(t, dict) and t.get("doc_slots") for t in (y.get("trace") or []))
    lab = [[J[(q, p)] for p in M.cited(M.body(r.get("answer")))] for r in (x, y)]
    d = lab[1].count(2) - lab[0].count(2)
    up += d > 0
    down += d < 0
    same_applied += ap and d == 0
    if ap or d:
        print(f"{q} | {'O' if ap else '-'} | {len(x.get('doc_ids') or [])}→{len(y.get('doc_ids') or [])} | {M.items(x.get('answer'))}→{M.items(y.get('answer'))} | "
              f"{lab[0].count(2)}→{lab[1].count(2)} | {lab[0].count(1)}→{lab[1].count(1)} | {lab[0].count(0)}→{lab[1].count(0)} | {'O' if S.ctx(x) == S.ctx(y) else 'X'}")
print(f"늘어남 {up} · 줄어듦 {down} · 칸 틀 적용했는데 '2' 같음 {same_applied}")
ap_rows = [q for q in a if any(isinstance(t, dict) and t.get("doc_slots") for t in (b[q].get("trace") or []))]
print("칸 틀 적용 문항만: 항목", sum(M.items(a[q].get("answer")) for q in ap_rows), "→", sum(M.items(b[q].get("answer")) for q in ap_rows),
      "· 컨텍스트 다른 문항(전체)", sum(S.ctx(a[q]) != S.ctx(b[q]) for q in a))
