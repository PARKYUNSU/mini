"""held-out 뒤 진단(이 문항들은 이제 dev): 진 문항 · 거르기 비율 · 라벨이 있는 문서만 본다. 코드 변경 없음."""
import json, re, statistics, sys
sys.path.insert(0, "docs/experiments/topic_split2_1104")
import score as S

c, t = S.rows("ts0_hu"), S.rows("ts1_hu")
gold = {g["id"]: g for g in map(json.loads, open(S.D + "heldout_gold.jsonl", encoding="utf-8"))}
lab = {}
for l in open(S.D + "labels_hu.tsv", encoding="utf-8"):
    if l.strip() and not l.startswith("#"):
        q, p, v = l.rstrip("\n").split("\t")[:3]
        lab[(q, p)] = set() if v.strip() == "-" else {int(x) for x in re.findall(r"\d+", v)}


def tr(r):
    return {x.get("stage"): x for x in r.get("trace", [])}


ratios = []
for q in sorted(c):
    a, b = S.docs(c[q]), S.docs(t[q])
    ca = set().union(*[lab[(q, p)] for p in a]) if a else set()
    cb = set().union(*[lab[(q, p)] for p in b]) if b else set()
    tt = tr(t[q])
    f = (tt.get("filter") or {}).get("filter", "")
    m = re.match(r"(\d+)→(\d+)", f)
    if m and (tt.get("search") or {}).get("topics"):
        ratios.append((int(m.group(1)), int(m.group(2))))
    if len(cb) < len(ca) or q in sys.argv[1:]:
        print(f"## {q} 덮음 {sorted(ca)} → {sorted(cb)} · 대조 편수 {len(a)} · 처리 거르기 {f} · 겹침 {len(set(a) & set(b))}")
        print("  주제:", " · ".join(f"{k}. {x}" for k, x in enumerate(gold[q]["topics"], 1)))
        print("  줄:", (tt.get("search") or {}).get("topics"))
        print("  대조만:", [f"{p}{sorted(lab[(q, p)])}" for p in a if p not in b])
        print("  처리만:", [f"{p}{sorted(lab[(q, p)])}" for p in b if p not in a])
print("\n나뉜 문항 거르기: 들어옴 중앙", statistics.median(x for x, _ in ratios), "· 남음 중앙", statistics.median(y for _, y in ratios),
      "· 3편 이하로 줄어든 문항", sum(y <= 3 for _, y in ratios), "/", len(ratios))
print("대조 거르기:", [(tr(c[q]).get("filter") or {}).get("filter", "") for q in sorted(c)][:40])
