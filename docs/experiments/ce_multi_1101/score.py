"""ce_multi_1101 채점: 갈래 10 대 base — 상위 5 얻음 : 잃음 · 고르는 규칙 (README §3 · §4)."""
import json, statistics as st, sys
from math import comb
from pathlib import Path

D = Path(__file__).parent
rows = [json.loads(l) for l in open(D / (sys.argv[1] if len(sys.argv) > 1 else "results.jsonl"))]
ARMS = [(m, l, c) for m, l in (("bge", "ko"), ("bge", "en"), ("mm", "ko"), ("mm", "en"), ("msm", "en")) for c in ("ce", "rrf")]


def order(x, key=None, comb_="ce", n=30):
    """15편 순서 — key 없으면 base(가로챈 운영 순서), 있으면 상위 n편을 CE(·RRF)로 다시 줄 세운 순서."""
    pool, front = x["pool"], x["front"]
    if not pool:
        return x["base"]
    head = pool
    if key:
        s = x["scores"][key][:n]
        ce = [pool[i] for i in sorted(range(len(s)), key=lambda i: -s[i])]
        if comb_ == "rrf":
            rc = {p: i for i, p in enumerate(ce)}
            ce = sorted(pool[:len(s)], key=lambda p: -(1 / (61 + pool.index(p)) + 1 / (61 + rc[p])))
        head = ce + pool[len(s):]
    rest = list(dict.fromkeys(p for p in head if p not in front))
    return front + rest[:15 - len(front)]


hit = lambda o, g, k: bool(set(o[:k]) & set(g))
rr = lambda o, g: next((1 / (i + 1) for i, p in enumerate(o[:15]) if p in g), 0.0)
sign_p = lambda b, c: 1.0 if b + c == 0 else min(1, 2 * sum(comb(b + c, i) for i in range(min(b, c) + 1)) / 2 ** (b + c))
S18 = {r["id"] for r in map(json.loads, open(D.parent / "e2e_ko_1008/results/s18_162.jsonl")) if (r.get("rag_queries") or [""])[0]}
EXTRA = [x for x in rows if x["set"] == "162" and x["id"] not in S18]  # paper_ce_1023 에 없던 문항 — 판정 밖, 보고만 (README §4.2)
main = [x for x in rows if x["set"] != "sv_old" and x not in EXTRA]
print(f"주 문항 {len(main)} · base≠운영 {sum(not x['same'] for x in main)} · 후보 없음 {sum(not x['pool'] for x in main)}")
B = {x["id"] + x["set"]: order(x) for x in rows}
print(f"base @1 {sum(hit(B[x['id'] + x['set']], x['gold'], 1) for x in main)} · @5 {sum(hit(B[x['id'] + x['set']], x['gold'], 5) for x in main)}"
      f" · @15 {sum(hit(B[x['id'] + x['set']], x['gold'], 15) for x in main)} · MRR@15 {st.mean(rr(B[x['id'] + x['set']], x['gold']) for x in main):.3f}")


def compare(xs, key, c, n=30, k=5):
    o = {x["id"] + x["set"]: order(x, key, c, n) for x in xs}
    g = sum(hit(o[i], x["gold"], k) and not hit(B[i], x["gold"], k) for x in xs for i in [x["id"] + x["set"]])
    l = sum(hit(B[i], x["gold"], k) and not hit(o[i], x["gold"], k) for x in xs for i in [x["id"] + x["set"]])
    return g, l, o


res = []
for m, lang, c in ARMS:
    key = f"{m}_{lang}"
    g, l, o = compare(main, key, c)
    g15, l15, _ = compare(main, key, c, k=15); g1, l1, _ = compare(main, key, c, k=1)
    sec = st.median(x["sec"][key] for x in main if x["pool"])
    res.append((g - l, -l, -sec, key, c, g, l))
    print(f"{key:7} {c:3} | @5 얻음 {g} : 잃음 {l} (순 {g - l:+d}, p {sign_p(g, l):.3f}) | @15 {g15}:{l15} | @1 {g1}:{l1}"
          f" | MRR@15 {st.mean(rr(o[x['id'] + x['set']], x['gold']) for x in main):.3f} | CE 30편 중앙 {sec:.2f}s")

best = max(r for r in res if -r[2] <= 3.0)  # 조건 3 은 고르기 전 자격 (README §4.1)
net, _, nsec, key, c, g, l = best
ok = {"1 순 ≥ +5": net >= 5, "2 얻음 ≥ 2×잃음": g >= 2 * l}
print(f"\n고른 갈래(30편 ≤ 3s 중): {key} {c} (얻음 {g} : 잃음 {l})")
for r in res:
    if -r[2] > 3.0 and r[0] >= net + 3:
        print(f"  bge 갈래 {r[3]} {r[4]} 순 {r[0]:+d} — 고른 갈래보다 +3 이상 · 시간 {-r[2]:.1f}s → 사용자 결정")
for k_, v in ok.items():
    print(("통과 " if v else "미달 ") + k_)
print("→ 다음 단계(따로 사전 등록)" if all(ok.values()) else "→ R1 접음")

print("\n보고 — 고른 갈래")
for n in (15, 50):
    g_, l_, _ = compare(main, key, c, n=n)
    print(f"  재순위 범위 {n}: @5 {g_}:{l_}")
for s in ("162", "real40", "real2"):
    g_, l_, _ = compare([x for x in main if x["set"] == s], key, c)
    print(f"  {s}: @5 {g_}:{l_}")
if EXTRA:
    g_, l_, _ = compare(EXTRA, key, c)
    print(f"  판정 밖 {' · '.join(x['id'] for x in EXTRA)}: @5 {g_}:{l_}")
sv = [x for x in rows if x["set"] == "sv_old"]
if sv:
    cov = lambda o, x: len(set(o[:5]) & set(x["gold"]))
    print(f"  sv_old {len(sv)} 상위 5 정답 편수: base {sum(cov(B[x['id'] + x['set']], x) for x in sv)} · "
          + " · ".join(f"{k2} {c2} {sum(cov(order(x, k2, c2), x) for x in sv)}"
                       for k2, c2 in [(key, c)] + [(f'{m}_{l2}', c3) for m, l2, c3 in ARMS if (f'{m}_{l2}', c3) != (key, c)]))
