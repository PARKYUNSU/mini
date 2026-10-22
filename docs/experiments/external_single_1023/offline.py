"""external_single_1023 오프라인 (맥미니): 1편만 남은 답의 검색어로 OpenAlex 를 불러 결과를 저장한다."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from core.llm.presence_judge import gate_types
from core.rag.external_search import search_openalex

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "external_single_1023"
QS = {"as1_real40": EXP / "real_eval_1013/questions.tsv", "as1_real2": EXP / "real_eval2_1015/questions.tsv",
      "as1_m12": EXP / "aspect_split_1022/questions.tsv"}
out = []
for lbl, qf in QS.items():
    qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(qf) if "\t" in l}
    for r in map(json.loads, open(R / f"{lbl}.jsonl")):
        ids = set(r.get("doc_ids") or []); q = qs[r["id"]]
        if len(ids) != 1 or "list" in gate_types(q) or not r.get("rag_queries"):
            continue
        t0 = time.time(); items = search_openalex(r["rag_queries"][0], ids); dt = time.time() - t0
        out.append({"set": lbl, "id": r["id"], "question": q, "query": r["rag_queries"][0], "sec": round(dt, 2),
                    "items": [{k: it[k] for k in ("title", "year", "arxiv", "abstract")} for it in items]})
        print(lbl, r["id"], len(items), f"{dt:.1f}s", flush=True)
with open(D / "items.jsonl", "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
print("대상", len(out), "결과 0편", sum(not x["items"] for x in out), "6s 초과", sum(x["sec"] > 6 for x in out))
