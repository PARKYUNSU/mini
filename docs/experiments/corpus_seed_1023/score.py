"""corpus_seed_1023 §3 판정 (맥미니)."""
import json, sys
from pathlib import Path
sys.path.insert(0, ".")
R = Path("docs/experiments/e2e_ko_1008/results"); D = Path("docs/experiments/corpus_seed_1023")
NEW = {"2401.14887", "2406.16008", "2403.04797", "2404.16811", "2404.13781", "2401.17043"}
gold = {json.loads(l)["id"]: set(json.loads(l)["relevant_papers"]) for l in open(D / "gold.jsonl")}
load = lambda f: {json.loads(l)["id"]: json.loads(l) for l in open(R / f"{f}.jsonl")}
pre, post = load("cs3_0_rq"), load("cs3_1_rq")
for q in gold:
    for tag, rows in (("전", pre), ("후", post)):
        ids = set(rows[q].get("doc_ids") or rows[q].get("context_papers") or [])
        print(f"{q} {tag}: 컨텍스트 {sorted(ids)} · 수집 논문 {sorted(ids & NEW)} · gold {len(ids & gold[q])}")
hit = sum(bool(set(post[q].get("doc_ids") or post[q].get("context_papers") or []) & NEW) for q in gold)
print(f"주: 수집 논문이 든 문항 {hit}/{len(gold)}")
for t in ("real40", "real2"):
    a, b = load(f"cs3_0_{t}"), load(f"cs3_1_{t}")
    ks = [k for k in a if k in b]
    print(f"보호 {t}: 검색 ok {sum(a[k]['ok'] for k in ks)} → {sum(b[k]['ok'] for k in ks)} (전만 {sum(a[k]['ok'] and not b[k]['ok'] for k in ks)} : 후만 {sum(b[k]['ok'] and not a[k]['ok'] for k in ks)})")
