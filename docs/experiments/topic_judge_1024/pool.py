"""topic_judge_1024 판정 풀 (맥미니): 조건을 지우고 (질문, 논문) 쌍을 섞는다."""
import glob, json, random, re, sys
from pathlib import Path
sys.path.insert(0, ".")
from core.llm.conclusion_rewrite import brief_findings

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "topic_judge_1024"
bare = lambda p: re.sub(r"v\d+$", "", p or "")
AB, TI = {}, {}
for f in ["raw_data_queue/crawled_papers.jsonl"] + glob.glob("raw_data_queue/processed/*.jsonl"):
    for l in open(f):
        try:
            d = json.loads(l)
        except ValueError:
            continue
        p = bare(d.get("paper_id", "")); AB.setdefault(p, re.sub(r"\s+", " ", d.get("abstract") or "")); TI.setdefault(p, d.get("title") or "")
QF = {"real40": EXP / "real_eval_1013/questions.tsv", "real2": EXP / "real_eval2_1015/questions.tsv",
      "m12": EXP / "aspect_split_1022/questions.tsv", "cs3": EXP / "corpus_seed_1023/questions.tsv"}
Q = {(s, l.split("\t")[0]): l.split("\t")[1].strip() for s, f in QF.items() for l in open(f) if "\t" in l}
want = lambda s, i: (s in ("real40", "real2") and i[0] in "TR") or s == "m12" or (s == "cs3" and i in ("R01", "R03", "R04"))
ctx = {}  # (조건, 세트, id) -> 논문 목록
for cond, pre in (("ops", "lq_ko"), ("nofilter", "lq_ko_nofilter"), ("nolr", "lq_ko_nolr")):
    for s in QF:
        f = R / f"{pre}_{s}.jsonl"
        if not f.exists():
            continue
        for r in map(json.loads, open(f)):
            if want(s, r["id"]):
                ctx[(cond, s, r["id"])] = list(dict.fromkeys(bare(p) for p in (r.get("doc_ids") or [])))
pairs = sorted({(s, i, p) for (c, s, i), ps in ctx.items() for p in ps})
random.Random(1024).shuffle(pairs)
with open(D / "pool.md", "w") as w:
    for n, (s, i, p) in enumerate(pairs):
        w.write(f"P{n:03d} | Q: {Q[(s, i)]}\n     [{p}] {TI.get(p, '?')}\n     {brief_findings(AB.get(p, ''), 600)}\n\n")
json.dump({f"P{n:03d}": [s, i, p] for n, (s, i, p) in enumerate(pairs)}, open(D / "pool_key.json", "w"))
json.dump({"|".join(k): v for k, v in ctx.items()}, open(D / "contexts.json", "w"), ensure_ascii=False)
print("문항·조건", len(ctx), "고유 쌍", len(pairs))
