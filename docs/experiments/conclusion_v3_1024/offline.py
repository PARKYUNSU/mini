"""conclusion_v3_1024 오프라인 (맥미니): 저장된 답에 결론 v2 · v3 를 각각 적용하고 눈가림 판정 파일을 만든다."""
import json, os, random, re, statistics as st, sys, time
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from core.config.agent_config import RAG_ANSWER_MODEL
from core.llm.answer_fix import _find
from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.conclusion_rewrite import cited_blocks, rewrite_conclusion

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "conclusion_v3_1024"
g = {}; exec((EXP / "conclusion_rewrite_1021/offline.py").read_text().split("qs = {}")[0], g)  # grounded · concl
QF = {"pb1_real40": EXP / "real_eval_1013/questions.tsv", "pb1_real2": EXP / "real_eval2_1015/questions.tsv"}
out = []
for lbl, qf in QF.items():
    qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(qf) if "\t" in l}
    for r in map(json.loads, open(R / f"{lbl}.jsonl")):
        a, ctx = r.get("answer") or "", r.get("numbered_context") or ""
        ids = dict(enumerate(r.get("doc_ids") or [], 1))
        if not a or len(cited_blocks(a, ctx, ids)) < 2:
            continue
        rec = {"set": lbl, "id": r["id"], "question": qs[r["id"]]}
        for arm in ("v2", "v3"):
            os.environ["RAG_CONCLUSION_PROMPT"] = arm
            t0 = time.time(); new, why = rewrite_conclusion(a, qs[r["id"]], ctx, ids, RAG_ANSWER_MODEL)
            rec[arm] = {"why": why, "sec": round(time.time() - t0, 1), "concl": g["concl"](new).strip(), "grounded": g["grounded"](new, ctx, ids)}
        rec["blocks"] = {str(n): b[:1400] for n, b in cited_blocks(a, ctx, ids).items()}
        rec["doc_ids"] = {str(k): v for k, v in ids.items()}
        out.append(rec); print(lbl, r["id"], rec["v2"]["why"], rec["v3"]["why"], flush=True)
with open(D / "results.jsonl", "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
rnd = random.Random(1024); key = {}
split = lambda t: [s.strip() for s in re.split(r"(?<=[.!?。])\s+|\n+", re.sub(r"<[^>]+>", "", t)) if len(s.strip()) > 10]
with open(D / "blind.md", "w") as w:
    for n, x in enumerate(out):
        arms = ["v2", "v3"]; rnd.shuffle(arms); key[f"Q{n:02d}"] = arms
        w.write(f"######## Q{n:02d} | {x['question']}\n")
        for k, b in x["blocks"].items():
            w.write(f"--- [{x['doc_ids'].get(k, '?')}] {re.sub(chr(10), ' ', b)}\n")
        for tag, arm in zip("AB", arms):
            for j, s in enumerate(split(x[arm]["concl"])):
                w.write(f"Q{n:02d}{tag}.{j} {s}\n")
        w.write("\n")
json.dump(key, open(D / "blind_key.json", "w"))
print("대상", len(out), "· 시간 중앙 v2", st.median(x["v2"]["sec"] for x in out), "v3", st.median(x["v3"]["sec"] for x in out))
