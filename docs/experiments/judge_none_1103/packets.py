"""judge_none_1103: 판정이 '없음'인 문항만 질문 · 컨텍스트 블록(블록당 앞 1000자)으로 묶는다 → packets.md. 판정 결과는 행 trace 의 judge.pick."""
import json, re
from collections import Counter

R = "docs/experiments/e2e_ko_1008/results/jn_dev.jsonl"
D = "docs/experiments/judge_none_1103/"
Q = dict(l.rstrip("\n").split("\t", 1) for l in open(D + "questions.tsv") if l.strip())
rows = [json.loads(l) for l in open(R)]


def pick(r):
    j = [s for s in r.get("trace", []) if s["stage"] == "judge"]
    return j[0].get("pick") if j else "판정 단계 없음"


print("행", len(rows), "판정", Counter(str(pick(r)) if pick(r) in (None, "없음", "판정 단계 없음") else "문서" for r in rows))
out = []
for r in rows:
    if pick(r) != "없음":
        continue
    blocks = re.split(r"\n(?=\[문서 \d+\]\n)", r.get("numbered_context") or "")
    body = "\n\n".join(re.sub(r"\[Distance:[^\]]*\]\n?", "", b).strip()[:1000] for b in blocks if b.strip())
    out.append(f"## {r['id']} ({r['slot']})\n\n**질문** {Q[r['id']]}\n\n{body}")
open(D + "packets.md", "w", encoding="utf-8").write("\n\n---\n\n".join(out) + "\n")
print("'없음' 묶음", len(out))
