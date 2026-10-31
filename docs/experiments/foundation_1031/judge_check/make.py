"""foundation_1031 §5 판정자 점검: survey_gate_1030 판정 풀에서 20쌍을 뽑아 사람이 판정할 문서를 만든다.

Claude 판정(survey_gate_1030/judged.txt)이 '2' 로 쏠려 있어(164 중 다수) 무작위로 뽑으면 '0' · '1' 을 거의 못 본다.
그래서 Claude 라벨별로 8 · 7 · 5 쌍을 뽑아 섞는다(층화). 사람은 라벨을 모른 채 판정한다 — 정답지는 key.json.
"""
import json
import random
from pathlib import Path

D = Path(__file__).resolve().parent
SG = D.parents[1] / "survey_gate_1030"
pool = {x["k"]: x for x in json.load(open(SG / "pool.json", encoding="utf-8"))}
lab = {int(k): int(v) for k, v in (l.split() for l in open(SG / "judged.txt") if l.strip())}
rng = random.Random(1031)
pick = []
for label, n in ((2, 8), (1, 7), (0, 5)):
    pick += rng.sample(sorted(k for k, v in lab.items() if v == label), n)
rng.shuffle(pick)
json.dump({i + 1: {"k": k, "claude": lab[k]} for i, k in enumerate(pick)}, open(D / "key.json", "w"), indent=0)
out = ["# 판정자 점검 — 20쌍 (조건 · Claude 판정 모름)\n\n",
       "질문마다 논문(제목 + 초록 앞부분)이 질문을 얼마나 직접 다루는지 매겨 주세요.\n\n",
       "- **2** = 질문 주제를 직접 다룸\n- **1** = 관련은 있지만 비껴감\n- **0** = 관련 없음\n\n",
       "답은 `1:2 2:0 3:1 …` 처럼 번호:점수로 보내 주세요.\n"]
for i, k in enumerate(pick, 1):
    x = pool[k]
    out.append(f"\n---\n\n### {i}\n**질문**: {x['question']}\n\n**논문**: {x['title']}\n\n> {x['abstract'][:450] or '(초록 없음)'}\n")
(D / "pairs.md").write_text("".join(out), encoding="utf-8")
print("20쌍 →", D / "pairs.md")
