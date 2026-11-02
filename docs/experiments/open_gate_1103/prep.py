"""open_gate_1103 §4.1: 1단계 질문 · 정답 파일 — 새 held-out 50 + 규칙에 걸리는 기존 held-out 단일 5 (쌍 H_I04 는 따로 --keep-session)."""
import json

D = "docs/experiments/open_gate_1103/"
F = "docs/experiments/foundation_1031/"
OLD = ["H_C07", "H_C16", "H_C24", "H_C31", "H_H03"]
q = [l.rstrip("\n").split("\t", 1) for l in open(D + "heldout_open.tsv", encoding="utf-8") if l.strip()]
hq = dict(l.rstrip("\n").split("\t", 1) for l in open(F + "heldout.tsv", encoding="utf-8") if l.strip())
hg = {j["id"]: j for j in map(json.loads, open(F + "heldout_gold.jsonl", encoding="utf-8"))}
ng = {j["id"]: j for j in map(json.loads, open(D + "heldout_open_gold.jsonl", encoding="utf-8"))}
with open(D + "stage1_questions.tsv", "w", encoding="utf-8") as f:
    for u, t in q + [(u, hq[u]) for u in OLD]:
        f.write(f"{u}\t{t}\n")
with open(D + "stage1_gold.jsonl", "w", encoding="utf-8") as f:
    for u, _ in q:
        f.write(json.dumps(ng[u], ensure_ascii=False) + "\n")
    for u in OLD:
        f.write(json.dumps(hg[u], ensure_ascii=False) + "\n")
print(len(q) + len(OLD))
