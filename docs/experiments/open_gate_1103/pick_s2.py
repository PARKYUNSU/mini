"""open_gate_1103 §4.1 → §4.2: 1단계(대조 판정만) 행에서 바뀌는 문항(규칙에 걸리고 판정 '없음')을 골라 2단계 질문 · 정답 파일을 쓴다."""
import json, os, sys
from collections import Counter

sys.path.insert(0, ".")
os.environ["RAG_PRESENCE_GATE"] = "1"; os.environ["RAG_QTYPE_CLF"] = "0"
import core.llm.presence_judge as P

D = "docs/experiments/open_gate_1103/"
R = "docs/experiments/e2e_ko_1008/results/og_s1.jsonl"
Q = dict(l.rstrip("\n").split("\t", 1) for l in open(D + "stage1_questions.tsv", encoding="utf-8") if l.strip())
G = {j["id"]: j for j in map(json.loads, open(D + "stage1_gold.jsonl", encoding="utf-8"))}


def caught(q):
    os.environ["RAG_OPEN_GATE"] = "1"
    return not P.should_judge(q)


rows = {j["id"]: j for j in map(json.loads, open(R, encoding="utf-8"))}
pick = {}
for i, j in rows.items():
    s = [x for x in j.get("trace", []) if x["stage"] == "judge"]
    pick[i] = s[0].get("pick") if s else "단계 없음"
dist = Counter("없음" if v == "없음" else ("문서" if v not in (None, "단계 없음") else str(v)) for v in pick.values())
new = [i for i in Q if i.startswith("O_")]
print("1단계 행", len(rows), "/", len(Q), "· 판정", dict(dist))
print("규칙 재현율(새 50 중 걸림)", sum(caught(Q[i]) for i in new), "/", len(new))
ch = [i for i in Q if caught(Q[i]) and pick.get(i) == "없음"]
print("바뀌는 문항", len(ch), "(새", sum(i.startswith("O_") for i in ch), "· 기존", sum(i.startswith("H_") for i in ch), ")")
if not ch:
    sys.exit("바뀌는 문항 없음 — 2단계 중단")
with open(D + "stage2_questions.tsv", "w", encoding="utf-8") as f:
    f.writelines(f"{i}\t{Q[i]}\n" for i in ch)
with open(D + "stage2_gold.jsonl", "w", encoding="utf-8") as f:
    f.writelines(json.dumps(G[i], ensure_ascii=False) + "\n" for i in ch)
