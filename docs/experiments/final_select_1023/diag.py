"""final_select_1023 최종 선택 진단 (맥미니, LLM 없음): 놓친 문항에서 정답 논문이 어느 단계에서 밀리는지.

질문마다 저장된 검색어(rag_queries[0])로 production_retrieval_debug_for_eval(운영과 같은 후보 풀 · 청크 점수 ·
논문 집계 · 제목 보정, light rerank 제외)를 돌려 정답 논문의 논문 순위와 점수 항목을 남긴다.
"""
import json, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from core.rag.agent_chroma_rag import _get_chroma_singleton, production_retrieval_debug_for_eval

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "final_select_1023"
bare = lambda p: re.sub(r"v\d+$", "", p or "")
SETS = [("s18_162", EXP / "retrieval_eval_1007/eval_set.jsonl"), ("as1_real40", EXP / "real_eval_1013/gold.jsonl"),
        ("as1_real2", EXP / "real_eval2_1015/gold.jsonl")]
col = _get_chroma_singleton()._collection
out = []
for lbl, gf in SETS:
    gold = {json.loads(l)["id"]: {bare(p) for p in json.loads(l)["relevant_papers"]} for l in open(gf)}
    for r in map(json.loads, open(R / f"{lbl}.jsonl")):
        g = gold.get(r["id"]); q = (r.get("rag_queries") or [""])[0]
        if not g or not q:
            continue
        dbg = production_retrieval_debug_for_eval(col, q, fetch_n=100)
        rows = dbg.get("ranked_papers") or []
        pos = {bare(x["paper_id"]): x for x in rows}
        hits = sorted((pos[p] for p in g if p in pos), key=lambda x: x["rank"])
        best = hits[0] if hits else None
        fifth = rows[4] if len(rows) >= 5 else None
        rec = {"set": lbl, "id": r["id"], "stratum": r["id"][:1], "query": q, "n_pool_papers": len(rows),
               "in_ops_context": bool(set(r.get("doc_ids") or []) & g),
               "gold_rank": best["rank"] if best else None,
               "gold": {k: best[k] for k in ("paper_id", "title", "paper_score_chunk_only", "multievidence_bonus", "title_sim",
                                             "paper_score_final", "n_chunks_in_paper", "chunk_scores_top5")} if best else None,
               "fifth": {k: fifth[k] for k in ("paper_id", "title", "paper_score_chunk_only", "title_sim", "paper_score_final",
                                               "n_chunks_in_paper")} if fifth else None}
        out.append(rec)
        print(lbl, r["id"], "정답 순위", rec["gold_rank"], "운영 컨텍스트", rec["in_ops_context"], flush=True)
with open(D / "diag.jsonl", "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)


def band(x):
    r = x["gold_rank"]
    return "풀에 없음" if r is None else "1~5" if r <= 5 else "6~10" if r <= 10 else "11~30" if r <= 30 else ">30"


for lbl, _ in SETS:
    xs = [x for x in out if x["set"] == lbl]
    print(f"{lbl}: {len(xs)}문항 · 운영 컨텍스트에 정답 {sum(x['in_ops_context'] for x in xs)} · 논문 점수 순위대 {dict(Counter(band(x) for x in xs))}")
    miss = [x for x in xs if not x["in_ops_context"]]
    print(f"   운영에서 놓친 {len(miss)}문항의 논문 점수 순위대 {dict(Counter(band(x) for x in miss))}")
