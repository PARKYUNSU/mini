"""name_lookup_1101 채점: 상위 5 끔 → 켬 · 이름 논문 위치 · 잃은 정답 · 검색 단계 시간 (README §5)."""
import json, statistics as st
from pathlib import Path

D = Path(__file__).parent
R = D.parent / "e2e_ko_1008" / "results"
aff = json.load(open(D / "affected.json"))
rows = {a: {} for a in (0, 1)}
for a in (0, 1):
    for s in {x["set"] for x in aff}:
        for r in map(json.loads, open(R / f"nl{a}_{s}.jsonl")):
            rows[a][(s, r["id"])] = r


def stage(r, name):
    return next((t for n, t in r.get("stages", []) if n == name), None)


lost = {"heldout": [], "dev": []}; already = moved = 0; dsec = []
for x in aff:
    k = (x["set"], x["id"]); off, on = rows[0][k], rows[1][k]
    c0, c1 = off.get("context_papers", []), on.get("context_papers", [])
    named = list(dict.fromkeys(x["names"].values())); gold = set(x["gold"])
    pos = lambda c: [c.index(p) + 1 if p in c else None for p in named]
    already += all(p in c0 for p in named); moved += c0 != c1
    gone = sorted((gold & set(c0)) - set(c1))
    if gone:
        lost["heldout" if x["set"] == "heldout" else "dev"].append((x["id"], gone))
    if stage(off, "search") is not None and stage(on, "search") is not None:
        dsec.append(stage(on, "search") - stage(off, "search"))
    print(f"{x['set']:7} {x['id']:8} 이름 {named} 위치 {pos(c0)} → {pos(c1)} | 빠짐 {sorted(set(c0) - set(c1))}"
          f" | 정답 잃음 {gone}" + (" | 정답 없음" if not gold else ""))

r138 = "2305.14251" in rows[1][("llm", "R_138")].get("context_papers", [])
hb = [i for i in ("H_B01", "H_B02", "H_B05", "H_B10")
      if not {g for x in aff if x["id"] == i for g in x["gold"]} & set(rows[1][("heldout", i)].get("context_papers", []))]
dt = st.median(dsec) if dsec else 0.0
checks = {"1 R_138 FActScore 상위 5": r138, "2 held-out 정답 4 유지 · 잃음 0": not hb and not lost["heldout"],
          "3 dev 잃음 0": not lost["dev"], "4 검색 시간 중앙 +≤1s": dt <= 1.0}
print(f"\n이름 논문이 끔에서 이미 상위 5: {already}/{len(aff)} · 상위 5 가 바뀐 문항 {moved}")
print(f"held-out 정답 빠진 B: {hb} · 잃음 held-out {lost['heldout']} · dev {lost['dev']} · 검색 시간 중앙 차 {dt:+.2f}s")
for k, v in checks.items():
    print(("통과 " if v else "미달 ") + k)
print("→ 채택" if all(checks.values()) else "→ 기각")
