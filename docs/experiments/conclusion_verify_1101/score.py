"""conclusion_verify_1101 채점: 라벨별 지움(다름 · 없음) 비율 · 판정 분포 · 시간."""
import collections, json, statistics as st
from pathlib import Path
D = Path(__file__).parent
ERR = ("E", "X", "U")
drop = lambda x: x.get("verdict") in ("다름", "없음")


def rate(xs, lbls):
    z = [x for x in xs if x["label"] in lbls]
    return sum(map(drop, z)), len(z)


for arm in ("v1", "v2", "v1_lead", "v2_lead"):
    p = D / f"results_{arm}.jsonl"
    if not p.exists():
        continue
    xs = [json.loads(l) for l in open(p)]
    run = [x for x in xs if "skip" not in x]
    main = [x for x in run if x["src"] != "case" and x["scope"] == "인용"]
    rest = [x for x in run if x["scope"] == "결론 전체"]
    (e, ne), (o, no) = rate(main, ERR), rate(main, "O")
    ok = e / ne >= 0.5 and o / no <= 0.1
    print(f"== {arm} 검사 {len(run)} · 못 읽음 {sum(not x['verdict'] for x in run)} · 건너뜀 {len(xs) - len(run)}")
    print(f"주 1 오류 지움 {e}/{ne} = {e / ne:.2f} (≥ 0.50) · 주 2 O 지움 {o}/{no} = {o / no:.2f} (≤ 0.10) → {'통과' if ok else '미달'}")
    for name, z in (("인용", main), ("결론 전체", rest)):
        tab = collections.defaultdict(collections.Counter)
        for x in z:
            tab[x["label"]][x["verdict"] or "못 읽음"] += 1
        print(f"  [{name}] " + " | ".join(f"{k} {dict(tab[k])}" for k in "OEXUF?" if k in tab))
    (e2, ne2), (o2, no2) = rate(rest, ERR), rate(rest, "O")
    print(f"  인용 없음: 오류 지움 {e2}/{ne2} · O 지움 {o2}/{no2}")
    for src in dict.fromkeys(x["src"] for x in main):
        z = [x for x in main if x["src"] == src]; (a, b), (c, d) = rate(z, ERR), rate(z, "O")
        print(f"  {src}: 오류 {a}/{b} · O {c}/{d}")
    print("  사례", [(x["sid"], x["verdict"]) for x in run if x["src"] == "case"])
    per, per_cited = collections.defaultdict(float), collections.defaultdict(float)
    for x in run:
        k = (x["src"], x["sid"].rsplit(".", 1)[0]); per[k] += x["sec"]
        if x["scope"] == "인용":
            per_cited[k] += x["sec"]
    print(f"  시간: 문장당 중앙 {st.median(x['sec'] for x in run):.1f}s · 결론당 합 중앙 인용만 {st.median(per_cited.values()):.1f}s"
          f" · 전체 {st.median(per.values()):.1f}s (결론 {len(per)})")
