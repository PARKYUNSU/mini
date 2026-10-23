"""answer_judge_1024 표본 (맥미니/로컬 읽기 전용): 답 20개를 주장으로 나누고 인용 블록을 붙인다."""
import json, random, re
from pathlib import Path
EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "answer_judge_1024"
QF = {"pb1_real40": EXP / "real_eval_1013/questions.tsv", "pb1_real2": EXP / "real_eval2_1015/questions.tsv",
      "lf0_new": EXP / "list_findings_1023/questions.tsv"}
pool = []
for lbl, qf in QF.items():
    qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(qf) if "\t" in l}
    for r in map(json.loads, open(R / f"{lbl}.jsonl")):
        if r.get("answer") and "본론" in r["answer"]:
            k = "T" if r["id"][0] in "TL" else r["id"][0]
            pool.append((k, lbl, r, qs[r["id"]]))
rnd = random.Random(1024); pick = []
for k in "NCTR":
    xs = [p for p in pool if p[0] == k]; pick += rnd.sample(xs, min(5, len(xs)))
SEP = "\n\n---\n\n"
def claims(a):
    a = re.sub(r"<[^>]+>", "", re.sub(r"\(https://arxiv\.org/abs/[^)]*\)", "", a.split("📎")[0]))
    out = []
    for sec in ("서론", "본론", "결론"):
        m = re.search(sec + r"\s*\n(.*?)(?=\n\s*(서론|본론|결론)\s*\n|\Z)", a, re.S)
        if not m:
            continue
        for s in re.split(r"(?<=[.!?。])\s+|\n+", m.group(1)):
            if len(s.strip()) > 15:
                out.append((sec, s.strip()))
    return out
with open(D / "sample.md", "w") as w:
    for n, (k, lbl, r, q) in enumerate(pick):
        w.write(f"######## A{n:02d} [{k}] {lbl} {r['id']} | Q: {q}\n")
        blocks = {}
        for b in (r.get("numbered_context") or "").split(SEP):
            m = re.search(r"\[(\d{4}\.\d{4,5})v\d+\]", b)
            if m:
                blocks.setdefault(m.group(1), re.sub(r"\s+", " ", re.sub(r"^\[문서 \d+\]\n|\[Distance[^\]]*\]|\[발행일[^\]]*\]", "", b))[:1400])
        cited = dict.fromkeys(re.findall(r"\[(\d{4}\.\d{4,5})", r["answer"]))
        for p in cited:
            w.write(f"--- 문서 [{p}]: {blocks.get(p, '(컨텍스트에 없음)')}\n")
        others = [p for p in blocks if p not in cited]
        if others:
            w.write(f"--- (인용 안 한 컨텍스트 논문: {', '.join(others)})\n")
        for j, (sec, s) in enumerate(claims(r["answer"])):
            w.write(f"C{n:02d}.{j:02d} [{sec}] {s}\n")
        w.write("\n")
print(len(pick), [(k, r["id"]) for k, _, r, _ in pick])
