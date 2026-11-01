"""ce_multi_1101 오프라인 (맥미니): 운영 검색의 가벼운 재순위 순서(상위 50편)를 가로채 cross-encoder 로 다시 매긴다 (README §1)."""
import os
os.environ.setdefault("HF_HUB_OFFLINE", "1")  # 받아 둔 스냅샷만 쓴다
import glob, json, re, resource, sys, time
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
import torch
from sentence_transformers import CrossEncoder
import core.rag.agent_chroma_rag as acr
from core.graph.rag_trace import paper_ids
from core.llm.relevance_filter import names
from scripts.eval_e2e_ko import load_items

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "ce_multi_1101"
bare = lambda p: re.sub(r"v\d+$", "", p or "")
AB = {}
for f in ["raw_data_queue/crawled_papers.jsonl"] + glob.glob("raw_data_queue/processed/*.jsonl"):
    for l in open(f):
        try:
            d = json.loads(l)
        except ValueError:
            continue
        AB.setdefault(bare(d.get("paper_id", "")), re.sub(r"\s+", " ", d.get("abstract") or ""))

CAP = {}
_light = acr._light_rerank_paper_pool_by_embedding


def _capture(query, paper_best, docs, metas, pool_k, **kw):  # 반환값은 그대로 — 순서만 적어 둔다
    out = _light(query, paper_best, docs, metas, pool_k, **kw)
    CAP.update(query=query, pool=[(bare(pk), (metas[bi].get("title") or "").strip(), (metas[bi].get("abstract") or "").strip())
                                  for _, bi, pk in out[:50]])
    return out


acr._light_rerank_paper_pool_by_embedding = _capture

MODELS = {}
for k, name, kw in (("bge", "BAAI/bge-reranker-v2-m3", {"dtype": torch.float16}),
                    ("mm", "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1", {}),
                    ("msm", "cross-encoder/ms-marco-MiniLM-L-6-v2", {})):
    m0 = torch.mps.current_allocated_memory()
    MODELS[k] = CrossEncoder(name, max_length=512, device="mps", model_kwargs=kw)
    MODELS[k].predict([("warm up", "warm up")])
    print(f"{k} MPS {(torch.mps.current_allocated_memory() - m0) / 2**20:.0f}MB", flush=True)
ARMS = [("bge", "ko"), ("bge", "en"), ("mm", "ko"), ("mm", "en"), ("msm", "en")]
SETS = [("162", EXP / "e2e_ko_1008/ko_questions.tsv", EXP / "retrieval_eval_1007/eval_set.jsonl", "lv1_162", "162"),
        ("real40", EXP / "real_eval_1013/questions.tsv", EXP / "real_eval_1013/gold.jsonl", "lv1_real40", "real40"),
        ("real2", EXP / "real_eval2_1015/questions.tsv", EXP / "real_eval2_1015/gold.jsonl", "lv1_real2", "real2"),
        ("sv_old", EXP / "survey_gate_1030/old_questions.tsv", EXP / "survey_gate_1030/old_gold.jsonl", "sg0_old", "old")]


def queries(first: str, suffix: str) -> dict:
    """문항별 영어 검색어 — ``first`` 실행 행 먼저, 없으면 같은 세트의 다른 실행(최신 먼저) (README §2)."""
    files = [R / f"{first}.jsonl"] + sorted(set(R.glob(f"*_{suffix}.jsonl")) - {R / f"{first}.jsonl"},
                                            key=lambda p: -p.stat().st_mtime)
    q = {}
    for p in files:
        for r in map(json.loads, open(p)):
            if (r.get("rag_queries") or [""])[0]:
                q.setdefault(r["id"], (r["rag_queries"][0], p.stem))
    return q


tool = acr._get_chroma_singleton(); bm = acr.get_bm25_searcher()
LIMIT = int(os.getenv("CEM_LIMIT", "0"))
out = []
for s, qf, gf, first, suffix in SETS:
    qs = queries(first, suffix)
    for x in [x for x in load_items(qf, gf) if x["gold"] and x["id"] in qs][:LIMIT or None]:
        if acr.is_chroma_write_locked() or acr._vector_search_effective_disabled():
            sys.exit("Chroma 쓰기 잠금 또는 벡터 검색 꺼짐 — 측정 중단")
        q, src = qs[x["id"]]
        CAP.clear()
        base = paper_ids(tool.search(q, top_k=15, name_query=x["question"]))[:15]
        pool = CAP.get("pool") or []
        named = [p for p in dict.fromkeys(bm.named_paper(n) for n in names(x["question"])) if p][:3]
        front = [p for p in named if p in base]
        texts = [f"{t}. {(AB.get(p) or a)[:1500]}" for p, t, a in pool]
        scores, sec = {}, {}
        for m, lang in ARMS:
            qq = x["question"] if lang == "ko" else q
            t0 = time.time()
            a = MODELS[m].predict([(qq, t) for t in texts[:30]]).tolist() if texts else []
            sec[f"{m}_{lang}"] = time.time() - t0
            scores[f"{m}_{lang}"] = a + (MODELS[m].predict([(qq, t) for t in texts[30:]]).tolist() if len(texts) > 30 else [])
        rest = list(dict.fromkeys(p for p, _, _ in pool if p not in front))
        out.append({"set": s, "id": x["id"], "question": x["question"], "query": q, "qsrc": src,
                    "gold": sorted({bare(g) for g in x["gold"]}), "base": base, "front": front,
                    "pool": [p for p, _, _ in pool], "scores": scores, "sec": sec,
                    "same": base == front + rest[:15 - len(front)], "light_q": CAP.get("query", "").strip() == q.strip()})
        print(s, x["id"], f"CE {sum(sec.values()):.1f}s", "" if out[-1]["same"] else "base≠pool", flush=True)
with open(D / ("results.jsonl" if not LIMIT else "smoke.jsonl"), "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
print(f"행 {len(out)} · base≠pool {sum(not x['same'] for x in out)} · 가로챈 검색어 다름 {sum(not x['light_q'] for x in out)}"
      f" · 최대 RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30:.1f}GB")
