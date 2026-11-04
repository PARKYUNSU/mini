"""answer_gap_1104: ans_hu(운영 설정 · 실제 답)의 답과 컨텍스트 문서 라벨을 나란히 뽑는다. 코드 변경 없음."""
import json, re, statistics, sys
sys.path.insert(0, "docs/experiments/topic_split2_1104")
import score as S

D = "docs/experiments/topic_filter_1104/"  # 풀 라벨
rows = S.rows("ans_hu")
gold = {g["id"]: g for g in map(json.loads, open(S.D + "heldout_gold.jsonl", encoding="utf-8"))}
lab = {}
for f in (S.D + "labels_hu.tsv", D + "labels_pool.tsv"):
    for l in open(f, encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            q, p, v = l.rstrip("\n").split("\t")[:3]
            lab.setdefault((q, p), v.strip())
qs = {l.split("\t")[0]: l.split("\t", 1)[1].rstrip("\n").replace("\\n", " / ") for l in open(S.D + "heldout.tsv", encoding="utf-8")}
el = []
for q in sorted(rows):
    r = rows[q]
    tr = {x.get("stage"): x for x in r.get("trace", [])}
    el.append(r.get("elapsed", 0))
    print(f"\n## {q} · 판정 {tr.get('judge', {}).get('pick')} · 게이트 {tr.get('judge', {}).get('gates')} · {r.get('elapsed')}s")
    print("질문:", qs[q][:170])
    print("주제:", " · ".join(f"{k}. {x}" for k, x in enumerate(gold[q]["topics"], 1)))
    print("문서:", " | ".join(f"{p}[{lab.get((q, p), '?')}] {t[:42]}" for p, (t, _) in S.docs(r).items()))
    print("답:\n" + (r.get("answer") or "")[:2600])
print("\n시간 중앙", statistics.median(el))
