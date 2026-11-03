"""open_gate_1103 §5 채점: judge/labels.tsv(문항 · 이긴 쪽 A/B/= · A0 · B0 · A거짓없음 · B거짓없음 · A거짓있음 · B거짓있음 · 이유) + key.json."""
import json, statistics
from collections import Counter
from math import comb

R = "docs/experiments/e2e_ko_1008/results/"
D = "docs/experiments/open_gate_1103/"
key = json.load(open(D + "judge/key.json"))
lab = [l.rstrip("\n").split("\t") for l in open(D + "judge/labels.tsv", encoding="utf-8") if l.strip() and not l.startswith("#")]


def load(*labels):
    out = {}
    for lb in labels:
        out.update({j["id"]: j for j in map(json.loads, open(R + lb + ".jsonl", encoding="utf-8"))})
    return out


c0, c1 = load("og0_s2", "og0_f2"), load("og1_s2", "og1_f2")
win, zero, fnone, fyes, by = Counter(), Counter(), Counter(), Counter(), {}
for i, w, a0, b0, an, bn, ay, by_, *why in lab:
    t = key[i]
    res = "=" if w == "=" else ("처리" if w == t else "대조")
    win[res] += 1
    pick = lambda a, b: (int(a), int(b)) if t == "A" else (int(b), int(a))  # (처리, 대조)
    for ctr, (x, y) in ((zero, pick(a0, b0)), (fnone, pick(an, bn)), (fyes, pick(ay, by_))):
        ctr["처리"] += x; ctr["대조"] += y
    by.setdefault(i[:2], Counter())[res] += 1
a, b = win["처리"], win["대조"]
n, k = a + b, min(a, b)
p = min(1.0, 2 * sum(comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0
print(f"주: 처리 승 {a} · 대조 승 {b} · 동점 {win['=']} (판정 {len(lab)}) → 부호 검정 p {p:.4g}")
print(f"보호 1 거짓 있음: 처리 {fyes['처리']} · 대조 {fyes['대조']} (한도 {fyes['대조'] + 2})")
lim = zero["대조"] * 1.5 if zero["대조"] else 2
print(f"보호 2 무관 인용 '0': 처리 {zero['처리']} · 대조 {zero['대조']} (한도 {lim:.1f})")
ids = [x[0] for x in lab]
t1 = statistics.median(c1[i]["elapsed"] for i in ids); t0 = statistics.median(c0[i]["elapsed"] for i in ids)
print(f"보호 3 응답 시간 중앙: 처리 {t1:.1f}s · 대조 {t0:.1f}s (한도 {t0 + 20:.1f}s)")
print(f"보고 거짓 없음: 처리 {fnone['처리']} · 대조 {fnone['대조']}")
for nm, c in (("대조", c0), ("처리", c1)):
    print(f"보고 {nm}: 인용 편수 {sum(len(c[i].get('answer_papers') or []) for i in ids)}")
for k_, v in sorted(by.items()):
    print(f"   {k_}: 처리 {v['처리']} · 대조 {v['대조']} · 동점 {v['=']}")
