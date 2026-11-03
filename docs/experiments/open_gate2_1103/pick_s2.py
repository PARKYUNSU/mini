"""open_gate2_1103 §3: 1단계(대조 판정만) 행에서 바뀌는 문항(규칙에 걸리고 판정 '없음')을 골라 2단계 질문 · 정답 파일을 쓴다."""
import json, os, sys
from collections import Counter

sys.path.insert(0, ".")
os.environ["RAG_PRESENCE_GATE"] = "1"; os.environ["RAG_QTYPE_CLF"] = "0"; os.environ["RAG_OPEN_GATE"] = "1"
import core.llm.presence_judge as P

D = "docs/experiments/open_gate2_1103/"
Q = dict(l.rstrip("\n").split("\t", 1) for l in open(D + "heldout_open2.tsv", encoding="utf-8") if l.strip())
G = {j["id"]: j for j in map(json.loads, open(D + "heldout_open2_gold.jsonl", encoding="utf-8"))}
rows = {j["id"]: j for j in map(json.loads, open("docs/experiments/e2e_ko_1008/results/ogb_s1.jsonl", encoding="utf-8"))}
pick = {}
for i, j in rows.items():
    s = [x for x in j.get("trace", []) if x["stage"] == "judge"]
    pick[i] = s[0].get("pick") if s else "단계 없음"
print("1단계 행", len(rows), "/", len(Q), "· 판정", dict(Counter("없음" if v == "없음" else ("문서" if v not in (None, "단계 없음") else str(v)) for v in pick.values())))
print("경로", dict(Counter(j["route"] for j in rows.values())))
ch = [i for i in Q if not P.should_judge(Q[i]) and pick.get(i) == "없음"]
print("바뀌는 문항", len(ch))
if not ch:
    sys.exit("바뀌는 문항 없음 — 2단계 중단")
with open(D + "stage2_questions.tsv", "w", encoding="utf-8") as f:
    f.writelines(f"{i}\t{Q[i]}\n" for i in ch)
with open(D + "stage2_gold.jsonl", "w", encoding="utf-8") as f:
    f.writelines(json.dumps(G[i], ensure_ascii=False) + "\n" for i in ch)
