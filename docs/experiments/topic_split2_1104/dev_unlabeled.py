"""dev: ts0_ht 대 ts1_htd — 1103 라벨에 없는 문서만 뽑는다 (dev 라벨은 labels_htd.tsv)."""
import json, re, sys
sys.path.insert(0, "docs/experiments/topic_split_1103")
import score as S

c, t = S.rows("ts0_ht"), S.rows("ts1_htd")
lab = {tuple(l.split("\t")[:2]) for l in open("docs/experiments/topic_split_1103/labels_ht.tsv", encoding="utf-8") if not l.startswith("#")}
gold = {g["id"]: g for g in map(json.loads, open("docs/experiments/topic_split_1103/heldout_topics_gold.jsonl", encoding="utf-8"))}
for q in sorted(c):
    a, b = S.docs(c[q]), S.docs(t[q])
    tr = {x.get("stage"): x for x in t[q].get("trace", [])}
    print(f"## {q} 편수 {len(a)}→{len(b)} 나뉨 {len((tr.get('search') or {}).get('topics') or [])} filter {(tr.get('filter') or {})}"[:170])
    print("**", " · ".join(f"{k}. {x}" for k, x in enumerate(gold[q]["topics"], 1)))
    for p, (title, rest) in b.items():
        if (q, p) not in lab:
            print(f"- `{p}` **{title}** — {rest[:260]}")
