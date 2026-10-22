"""relevance_filter_1022 1단계: 저장 컨텍스트에 관련성 호출만 (맥미니)."""
import json, re, statistics as st, sys, time
from collections import Counter
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from core.config.agent_config import RAG_ANSWER_MODEL
from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.relevance_filter import filter_relevant

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "relevance_filter_1022"
SETS = {"at1_real40": "real_eval_1013", "at1_real2": "real_eval2_1015"}
pid = lambda b: (re.search(r"\[(\d{4}\.\d{4,5})v\d+\]", b) or [None, None])[1]
out = []
for lbl, d in SETS.items():
    gold = {json.loads(l)["id"]: {re.sub(r"v\d+$", "", p) for p in json.loads(l)["relevant_papers"]} for l in open(EXP / d / "gold.jsonl")}
    qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(EXP / d / "questions.tsv") if "\t" in l}
    for r in map(json.loads, open(R / f"{lbl}.jsonl")):
        plain = RAG_HIT_SEP.join(re.sub(r"^\[문서 \d+\]\n", "", b.strip()) for b in (r.get("numbered_context") or "").split(RAG_HIT_SEP) if b.strip())
        before = [pid(b) for b in plain.split(RAG_HIT_SEP)]
        t0 = time.time(); ctx, why = filter_relevant(qs[r["id"]], plain, RAG_ANSWER_MODEL); dt = time.time() - t0
        after = [pid(b) for b in ctx.split(RAG_HIT_SEP)]
        g = gold.get(r["id"], set())
        out.append({"set": lbl, "id": r["id"], "why": why, "sec": round(dt, 1), "before": before, "after": after,
                    "gold_in": sorted(set(before) & g), "gold_kept": sorted(set(after) & g),
                    "dropped": sorted(set(before) - set(after)), "dropped_gold": sorted((set(before) - set(after)) & g)})
        print(r["id"], why, f"{dt:.1f}s", flush=True)
with open(D / "stage1.jsonl", "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
tg = [x for x in out if x["why"] != "대상 아님"]
gi = sum(len(x["gold_in"]) for x in tg); gk = sum(len(x["gold_kept"]) for x in tg)
ng = sum(len(set(x["before"]) - set(x["gold_in"])) for x in tg); nd = sum(len(set(x["dropped"]) - set(x["dropped_gold"])) for x in tg)
print(f"대상 {len(tg)} · gold 유지 {gk}/{gi} = {gk / max(1, gi):.1%} · gold 아닌 논문 뺀 비율 {nd}/{ng} = {nd / max(1, ng):.1%}")
print("상태:", Counter(re.sub(r"\d+→\d+", "거름", x["why"]) for x in tg), "· 시간 중앙", f"{st.median(x['sec'] for x in tg):.1f}s")
print("gold 를 뺀 문항:", [(x["set"], x["id"], x["dropped_gold"]) for x in tg if x["dropped_gold"]])
