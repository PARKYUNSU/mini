"""eval30_1110 채점 (README §3).

  .venv/bin/python docs/experiments/eval30_1110/score.py ev30_base
"""
import collections, json, os, re, statistics, sys

D = "docs/experiments/eval30_1110/"
R = "docs/experiments/e2e_ko_1008/results/"
LABELS = ["docs/experiments/topic_split2_1104/labels_hu.tsv", "docs/experiments/topic_filter_1104/labels_pool.tsv", D + "labels_new.tsv"]


def norm(p):
    return re.sub(r"v\d+$", "", str(p))


def topic_labels():
    lab = {}
    for f in LABELS:
        if not os.path.exists(f):
            continue
        for l in open(f, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                q, p, v = l.rstrip("\n").split("\t")[:3]
                if (q, p) not in lab:
                    lab[(q, norm(p))] = set() if v.strip() == "-" else {int(x) for x in re.findall(r"\d+", v)}
    return lab


def main(label):
    rows = {r["id"]: r for r in map(json.loads, open(R + label + ".jsonl", encoding="utf-8"))}
    gold = {g["id"]: g for g in map(json.loads, open(D + "gold.jsonl", encoding="utf-8"))}
    lab = topic_labels()
    res, unl = {}, []
    for i, g in gold.items():
        r = rows.get(i)
        if r is None:
            continue
        s15 = next((x.get("ids") for x in r.get("trace") or [] if x.get("stage") == "search"), None) or []
        s15 = [norm(x) for x in s15]
        f5 = [norm(x) for x in r.get("doc_ids") or []]
        gp = [norm(p) for p in g["relevant_papers"]]
        o = {"type": g["stratum"], "lang": g["lang"], "pair": g.get("pair", ""), "n15": sum(p in s15 for p in gp), "n5": sum(p in f5 for p in gp), "ng": len(gp), "f5": f5}
        if g.get("element_papers"):
            o["el5"] = [k for k, ps in g["element_papers"].items() if any(norm(p) in f5 for p in ps)]
            o["el15"] = [k for k, ps in g["element_papers"].items() if any(norm(p) in s15 for p in ps)]
        if g.get("topics") and g.get("src") == "topic_split2_1104":
            cov = set()
            for p in f5:
                if (i, p) in lab:
                    cov |= lab[(i, p)]
                else:
                    unl.append((i, p))
            o["topics"] = f"{len(cov)}/{len(g['topics'])}"
        res[i] = o
    print(f"문항 {len(res)}/{len(gold)}")
    print("id | 유형 | 15편 정답 | 5편 정답 | 기타")
    for i, o in res.items():
        extra = o.get("topics") or (f"요소 5편 {o['el5']} · 15편 {o['el15']}" if "el5" in o else "")
        print(f"  {i:5s} {o['type']}{'·en' if o['lang'] == 'en' else '':3s} {o['n15']}/{o['ng']:<3d} {o['n5']}/{o['ng']:<3d} {extra}")
    qs = [o for o in res.values() if o["ng"] and "el5" not in o]
    hit15 = sum(o["n15"] > 0 for o in qs)
    hit5 = sum(o["n5"] > 0 for o in qs)
    print(f"\n정답 있는 문항 {len(qs)}(작업 141 쌍 제외): Recall@15 {hit15}/{len(qs)} · Recall@5 {hit5}/{len(qs)}")
    by = collections.defaultdict(list)
    for o in res.values():
        by[o["type"]].append(o)
    for t, os_ in sorted(by.items()):
        if t == "CP":
            print(f"  CP 두 편 모두 15편 {sum(o['n15'] == 2 for o in os_)}/{len(os_)} · 5편 {sum(o['n5'] == 2 for o in os_)}/{len(os_)} · 하나 이상 5편 {sum(o['n5'] > 0 for o in os_)}/{len(os_)}")
        elif t == "SV":
            print(f"  SV 5편 중 정답 3편 이상 {sum(o['n5'] >= 3 for o in os_)}/{len(os_)} · 5편 정답 수 {[o['n5'] for o in os_]} · 15편 {[o['n15'] for o in os_]}")
        elif t in ("NM", "NU"):
            print(f"  {t} 15편 {sum(o['n15'] > 0 for o in os_)}/{len(os_)} · 5편 {sum(o['n5'] > 0 for o in os_)}/{len(os_)}")
        elif t == "MU":
            print(f"  MU 주제 덮음 {[o.get('topics') for o in os_ if o.get('topics')]} · 작업 141 요소 {[(o['lang'], o.get('el5')) for o in os_ if 'el5' in o]}")
        elif t == "MS":
            print(f"  MS (DB 에 없음) 5편 {[o['f5'] for o in os_]}")
    print("\n한/영 쌍 (15편 · 5편 정답 수)")
    for i, o in res.items():
        if o["lang"] == "en" and o["pair"] in res:
            k = res[o["pair"]]
            ke = f" · 요소 {k.get('el5')} / {o.get('el5')}" if "el5" in o else ""
            print(f"  {o['pair']:5s} 한 {k['n15']}/{k['n5']} · 영 {o['n15']}/{o['n5']}{ke}")
    st = [dict(r.get("stages") or []) for r in rows.values()]
    keys = ["router", "query", "search", "select"]
    print("\n시간 중앙", {k: round(statistics.median(s.get(k, 0) for s in st), 1) for k in keys}, "· 전체", round(statistics.median(r["elapsed"] for r in rows.values()), 1), "· 오류", sum(bool(r.get("error")) for r in rows.values()))
    print("경로", collections.Counter(r.get("route") for r in rows.values()).most_common(4))
    if unl:
        print("\n라벨 없는 HU 문서", len(unl), unl)


if __name__ == "__main__":
    main(sys.argv[1])
