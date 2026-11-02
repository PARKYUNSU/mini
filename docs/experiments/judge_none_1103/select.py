"""judge_none_1103: 판정이 도는 dev 문항 80개를 고른다 — 실사용 전부 · 정규식이 놓친 수치 · 비교 전부 · 목록 16 · '-' 27."""
import json, os, random, sys
sys.path.insert(0, ".")
os.environ["RAG_QTYPE_CLF"] = "0"; os.environ["RAG_PRESENCE_GATE"] = "1"
from core.llm.presence_judge import should_judge

Q = "docs/experiments/qtype_1102/"
D = "docs/experiments/judge_none_1103/"
lab = dict(l.rstrip("\n").split("\t") for f in ("dev_labels.txt", "heldout_new_labels.txt") for l in open(Q + f) if l.strip())
rows = [l.rstrip("\n").split("\t") for l in open(Q + "all.tsv") if l.strip()][1:]
dev = [(r[0], r[2], r[3]) for r in rows if r[1] == "dev"]
dev += [(u, "qtype_1102:new", q) for u, q in (l.rstrip("\n").split("\t", 1) for l in open(Q + "heldout_new.tsv") if l.strip())]
pool = [(u, s, q, lab[u]) for u, s, q in dev
        if should_judge(q) and lab.get(u, "?") not in ("X", "?") and not lab.get(u, "").startswith("F")]
rng = random.Random(1103)
real = [x for x in pool if x[1].startswith("R_")]
rest = [x for x in pool if not x[1].startswith("R_")]
pick = real + [x for x in rest if x[3] in ("N", "C")]
for lb, n in (("L", 16), ("-", 27)):
    cand = [x for x in rest if x[3] == lb]
    pick += rng.sample(cand, n)
assert len(pick) == len({x[0] for x in pick}) == 80, len(pick)
os.makedirs(D, exist_ok=True)
with open(D + "questions.tsv", "w", encoding="utf-8") as f:
    for u, s, q, lb in pick:
        f.write(f"{u}\t{' '.join(q.split())}\n")
with open(D + "gold.jsonl", "w", encoding="utf-8") as f:
    for u, s, q, lb in pick:
        f.write(json.dumps({"id": u, "stratum": ("R" if s.startswith("R_") else "") + lb, "relevant_papers": []}, ensure_ascii=False) + "\n")
print(len(pick), "실사용", len(real))
