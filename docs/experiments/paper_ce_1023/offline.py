"""paper_ce_1023 오프라인 (맥미니): 운영 논문 순위 상위 30편을 MiniLM-L6 cross-encoder 로 다시 매긴다."""
import glob, json, os, re, statistics as st, sys, time
from math import comb
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from sentence_transformers import CrossEncoder
from core.rag.agent_chroma_rag import _get_chroma_singleton, production_retrieval_debug_for_eval

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "paper_ce_1023"
bare = lambda p: re.sub(r"v\d+$", "", p or "")
AB = {}
for f in ["raw_data_queue/crawled_papers.jsonl"] + glob.glob("raw_data_queue/processed/*.jsonl"):
    for l in open(f):
        try:
            d = json.loads(l)
        except ValueError:
            continue
        AB.setdefault(bare(d.get("paper_id", "")), re.sub(r"\s+", " ", d.get("abstract") or ""))
ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
col = _get_chroma_singleton()._collection
TOP = int(os.getenv("PCE_TOP", "30"))  # 2차(§6): 100


def rerank(q):
    rows = (production_retrieval_debug_for_eval(col, q, fetch_n=100).get("ranked_papers") or [])[:TOP]
    pids = [bare(r["paper_id"]) for r in rows]
    t0 = time.time()
    sc = ce.predict([(q, f"{r['title']}. {AB.get(p, '')[:1500]}") for r, p in zip(rows, pids)]).tolist() if rows else []
    dt = time.time() - t0
    base = pids
    ce_order = [p for _, p in sorted(zip(sc, pids), key=lambda x: -x[0])]
    rank_ce = {p: i for i, p in enumerate(ce_order)}
    rrf = sorted(pids, key=lambda p: -(1 / (60 + base.index(p) + 1) + 1 / (60 + rank_ce[p] + 1)))
    return {"base": base, "ce": ce_order, "rrf": rrf, "sec": dt}


out = []
SETS = [("s18_162", EXP / "retrieval_eval_1007/eval_set.jsonl"), ("as1_real40", EXP / "real_eval_1013/gold.jsonl"),
        ("as1_real2", EXP / "real_eval2_1015/gold.jsonl"), ("cs3_1_rq", EXP / "corpus_seed_1023/gold.jsonl")]
for lbl, gf in SETS:
    gold = {json.loads(l)["id"]: {bare(p) for p in json.loads(l)["relevant_papers"]} for l in open(gf)}
    for r in map(json.loads, open(R / f"{lbl}.jsonl")):
        g = gold.get(r["id"]); q = (r.get("rag_queries") or [""])[0]
        if g and q:
            out.append({"set": lbl, "id": r["id"], "query": q, "gold": sorted(g), **rerank(q)})
            print(lbl, r["id"], flush=True)
ASP = json.load(open(EXP / "aspect_split_1022/aspects.json"))
for r in map(json.loads, open(R / "as1_m12.jsonl")):
    q = (r.get("rag_queries") or [""])[0]
    if q:
        out.append({"set": "m12", "id": r["id"], "query": q, "aspects": ASP[r["id"]], **rerank(q)})
with open(D / ("results.jsonl" if TOP == 30 else f"results_top{TOP}.jsonl"), "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)

hit = lambda x, arm, k: bool(set(x[arm][:k]) & set(x["gold"]))
spec = [x for x in out if x["set"] in ("s18_162", "as1_real40", "as1_real2")]
for arm in ("rrf", "ce"):
    for k in (5, 10):
        b = sum(hit(x, arm, k) and not hit(x, "base", k) for x in spec); c = sum(hit(x, "base", k) and not hit(x, arm, k) for x in spec); n = b + c
        p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)
        print(f"{arm} @{k}: base {sum(hit(x, 'base', k) for x in spec)} → {sum(hit(x, arm, k) for x in spec)} / {len(spec)} | 얻음 {b} : 잃음 {c}, p={p:.4f}")
print(f"CE 30편 점수 시간 중앙 {st.median(x['sec'] for x in out):.2f}s")
FS = {"A039", "A044", "A106", "C2_09", "C2_19"}; BD = {"A056", "A092", "C1_22", "C2_06"}
for name, ids in (("청크 하나짜리 5", FS), ("경계 4", BD)):
    xs = [x for x in spec if x["set"] == "s18_162" and x["id"] in ids]
    print(f"{name}: @5 base {sum(hit(x, 'base', 5) for x in xs)} · rrf {sum(hit(x, 'rrf', 5) for x in xs)} · ce {sum(hit(x, 'ce', 5) for x in xs)}")
for x in out:
    if x["set"] == "cs3_1_rq":
        print(x["id"], {arm: sorted(set(x[arm][:5]) & set(x["gold"])) for arm in ("base", "rrf", "ce")})
for k in (5, 10):
    m = [x for x in out if x["set"] == "m12"]
    cov = {arm: sum(bool(set(x[arm][:k]) & set(v)) for x in m for v in x["aspects"].values()) for arm in ("base", "rrf", "ce")}
    print(f"M12 조건 커버 @{k} (24): {cov}")
