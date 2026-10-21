"""conclusion_rewrite_1021 §3 오프라인 측정 (맥미니): 저장된 답에 결론 다시 쓰기 보조 호출만 돌린다."""
import json, re, statistics as st, sys, time
from math import comb
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()
from core.config.agent_config import RAG_ANSWER_MODEL
from core.llm.answer_fix import _find
from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.conclusion_rewrite import rewrite_conclusion
from scripts.score_real_eval import score

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; OUT = EXP / "conclusion_rewrite_1021"
SETS = {"s18_real40": "real_eval_1013", "s18_real2": "real_eval2_1015"}
_ID = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]")
_NUM = re.compile(r"\d+(?:[.,]\d+)?")


def concl(a):
    c = _find("결론", a)
    return a[c.end():] if c else ""


def grounded(a, ctx, ids):
    """결론에 인용 단 문장이 있고, 그 문장의 숫자(1개 이상)가 전부 인용한 블록에 있는가."""
    blk = {re.sub(r"v\d+$", "", pid): b for b in ctx.split(RAG_HIT_SEP) for n, pid in ids.items() if b.strip().startswith(f"[문서 {n}]")}
    for s in re.split(r"(?<=[.다])\s+", concl(a)):
        refs = _ID.findall(s); nums = _NUM.findall(_ID.sub("", s))
        if refs and nums:
            src = "\n".join(blk.get(r, "") for r in refs)
            if all(re.search(rf"(?<![\d.,]){re.escape(t)}(?![\d])", src) for t in nums):
                return True
    return False


def outside(a, ctx, ids):
    """결론에 인용 블록 밖 숫자가 있는 문장이 있는가 (인용 단 문장만 본다)."""
    blk = {re.sub(r"v\d+$", "", pid): b for b in ctx.split(RAG_HIT_SEP) for n, pid in ids.items() if b.strip().startswith(f"[문서 {n}]")}
    for s in re.split(r"(?<=[.다])\s+", concl(a)):
        refs = _ID.findall(s)
        src = "\n".join(blk.get(r, "") for r in refs)
        if refs and any(not re.search(rf"(?<![\d.,]){re.escape(t)}(?![\d])", src) for t in _NUM.findall(_ID.sub("", s))):
            return True
    return False


qs = {}
for d in SETS.values():
    for l in open(EXP / d / "questions.tsv") if (EXP / d / "questions.tsv").exists() else []:
        if "\t" in l: qs[(d, l.split("\t")[0])] = l.split("\t")[1].strip()
res = []
for lbl, d in SETS.items():
    rows = [json.loads(l) for l in open(R / f"{lbl}.jsonl")]
    out = []
    for r in rows:
        a, ctx = r.get("answer") or "", r.get("numbered_context") or ""
        ids = {int(k): v for k, v in (r.get("doc_ids") or {}).items()}
        q = qs.get((d, r["id"]), "")
        t0 = time.time(); new, why = rewrite_conclusion(a, q, ctx, ids, RAG_ANSWER_MODEL) if a and q else (a, "대상 아님"); dt = time.time() - t0
        rec = {"set": lbl, "id": r["id"], "why": why, "sec": round(dt, 1), "before": concl(a), "after": concl(new),
               "g0": grounded(a, ctx, ids), "g1": grounded(new, ctx, ids), "o1": outside(new, ctx, ids)}
        res.append(rec); out.append({**r, "answer": new})
        print(r["id"], why, f"{dt:.1f}s", flush=True)
    with open(R / f"{lbl}_concl.jsonl", "w") as w:
        w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
    f = lambda s: (sum(x["ok"] for x in s["N"]), sum(x["both_cited"] for x in s["C"]), sum(x["gold_cited"] >= 3 for x in s["T"]))
    print(f"{lbl} N 정답 · C 두 편 · T≥3: 전 {f(score(lbl, EXP / d))} → 후 {f(score(f'{lbl}_concl', EXP / d))}")
with open(OUT / "results.jsonl", "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in res)
tg = [x for x in res if x["why"] != "대상 아님"]
b = sum(x["g1"] and not x["g0"] for x in tg); c = sum(x["g0"] and not x["g1"] for x in tg); n = b + c
p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n)
print(f"대상 {len(tg)} / 전체 {len(res)} · 바꿈 {sum(x['why'] == '바꿈' for x in tg)}")
print(f"주: 근거 결과 있는 결론 전 {sum(x['g0'] for x in tg)} → 후 {sum(x['g1'] for x in tg)} (후만 {b} : 전만 {c}, p={p:.4f})")
print(f"보호: 결론에 인용 밖 숫자 (후) {sum(x['o1'] for x in tg)} · 보조 호출 시간 중앙 {st.median(x['sec'] for x in tg):.1f}s")
from collections import Counter
print("탈락 사유:", Counter(re.sub(r"\s\S+$", "", x["why"]) if x["why"].startswith("문서 밖") else x["why"] for x in tg))
print("유형별 바꿈:", Counter(x["id"][0] for x in tg if x["why"] == "바꿈"), "대상:", Counter(x["id"][0] for x in tg))
