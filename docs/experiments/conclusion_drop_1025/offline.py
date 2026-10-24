"""conclusion_drop_1025 오프라인 (맥미니): v2 가 못 바꾼 답에 drop_bundled 를 적용하고 눈가림 판정 파일을 만든다."""
import json, os, random, re, sys, time
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
os.environ["RAG_CONCLUSION_PROMPT"] = "v2"; os.environ["RAG_CONCLUSION_DROP_BUNDLED"] = "0"
from core.config.agent_config import RAG_ANSWER_MODEL
from core.llm.answer_fix import _CITED, _find
from core.llm.conclusion_rewrite import _OVERGEN, cited_blocks, drop_bundled, rewrite_conclusion

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "conclusion_drop_1025"
g = {}; exec((EXP / "conclusion_rewrite_1021/offline.py").read_text().split("qs = {}")[0], g)  # grounded · concl
QF = {"pb1_real40": EXP / "real_eval_1013/questions.tsv", "pb1_real2": EXP / "real_eval2_1015/questions.tsv",
      "as0_m12": EXP / "aspect_split_1022/questions.tsv", "lf0_new": EXP / "list_findings_1023/questions.tsv"}
old = {(x["set"], x["id"]): x["v2"]["why"] for x in map(json.loads, open(EXP / "conclusion_v3_1024/results.jsonl"))}
split = lambda t: [x.strip() for x in re.split(r"(?<=[.!?。])\s+|\n+", t) if x.strip()]
out = []; stat = {"대상": 0, "v2 못 바꿈": 0}
for lbl, qf in QF.items():
    qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(qf) if "\t" in l}
    for r in map(json.loads, open(R / f"{lbl}.jsonl")):
        a, ctx = r.get("answer") or "", r.get("numbered_context") or ""
        ids = dict(enumerate(r.get("doc_ids") or [], 1))
        if not a or not _find("결론", a) or len(cited_blocks(a, ctx, ids)) < 2:
            continue
        stat["대상"] += 1
        why = old.get((lbl, r["id"])) or rewrite_conclusion(a, qs.get(r["id"], ""), ctx, ids, RAG_ANSWER_MODEL)[1]
        if why == "바꿈":
            continue
        stat["v2 못 바꿈"] += 1
        new, n = drop_bundled(a)
        sents = split(g["concl"](a))
        rec = {"set": lbl, "id": r["id"], "question": qs.get(r["id"], ""), "why": why, "n": n, "sents": sents,
               "drop": [("묶음" if len(set(_CITED.findall(s))) >= 2 else "일반화" if _OVERGEN.search(s) else "") for s in sents],
               "grounded_before": g["grounded"](a, ctx, ids), "grounded_after": g["grounded"](new, ctx, ids),
               "after": g["concl"](new).strip(),
               "blocks": {str(k): b[:1000] for k, b in cited_blocks(a, ctx, ids).items()}, "doc_ids": {str(k): v for k, v in ids.items()}}
        out.append(rec); print(lbl, r["id"], why, n, flush=True)
with open(D / "results.jsonl", "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
tg = [x for x in out if x["n"]]; random.Random(1025).shuffle(tg); key = {}
with open(D / "blind.md", "w") as w:
    for n, x in enumerate(tg):
        key[f"Q{n:02d}"] = [x["set"], x["id"]]
        w.write(f"######## Q{n:02d} | {x['question']}\n")
        for k, b in x["blocks"].items():
            w.write(f"--- [{x['doc_ids'].get(k, '?')}] {re.sub(chr(10), ' ', b)}\n")
        for j, s in enumerate(x["sents"]):
            w.write(f"Q{n:02d}.{j} {s}\n")
        w.write("\n")
json.dump(key, open(D / "blind_key.json", "w"), ensure_ascii=False)
print(stat, "규칙 적용", len(tg), "지운 문장", sum(x["n"] for x in tg))
