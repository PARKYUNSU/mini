"""qcond_1025 판정 파일: 문항마다 질문 · 조건 · 답 · 블록(제목 · 발행일 · 초록 앞부분)."""
import json, re
from pathlib import Path

D = Path(__file__).parent; R = D.parent / "e2e_ko_1008/results/qc_base.jsonl"
qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(D / "questions.tsv")}
cond = {}
for l in open(D / "conditions.tsv").read().splitlines()[1:]:
    q, t, c = l.split("\t"); cond.setdefault(q, []).append(f"{t}: {c}")
with open(D / "judge.md", "w") as w:
    for r in map(json.loads, open(R)):
        w.write(f"######## {r['id']} | {qs[r['id']]} | route {r.get('route')}\n")
        for i, c in enumerate(cond.get(r["id"], [])):
            w.write(f"  조건 {i}: {c}\n")
        for blk in (r.get("numbered_context") or "").split("\n\n---\n\n"):
            b = re.sub(r"\s+", " ", blk).strip()
            if b:
                w.write(f"--- {b[:700]}\n")
        w.write("=== 답\n" + (r.get("answer") or "(없음)").strip() + "\n\n")
print("ok")
