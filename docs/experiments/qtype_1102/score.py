"""qtype_1102 §4.2 채점: judge/labels.tsv(문항 · 이긴 쪽 A/B/= · A0 · B0 · A거짓없음 · B거짓없음 · 이유) + key.json."""
import json, os, re, statistics, sys
from collections import Counter
from math import comb

sys.path.insert(0, ".")
from core.llm.presence_judge import gate_types

R = "docs/experiments/e2e_ko_1008/results/"
D = "docs/experiments/qtype_1102/"
key = json.load(open(D + "judge/key.json"))
lab = [l.rstrip("\n").split("\t") for l in open(D + "judge/labels.tsv") if l.strip() and not l.startswith("#")]
Q = dict(l.rstrip("\n").split("\t", 1) for f in ("stage2_questions.tsv", "stage2_followup.tsv") for l in open(D + f) if l.strip())


def load(*labels):
    out = {}
    for lb in labels:
        out.update({j["id"]: j for j in map(json.loads, open(R + lb + ".jsonl"))})
    return out


c0, c1 = load("qt0_s2", "qt0_f2"), load("qt1_s2", "qt1_f2")


def kind(q):
    def dec(clf):
        os.environ["RAG_QTYPE_CLF"] = "1" if clf else "0"
        g = gate_types(q)
        return (bool(g), "list" in g, "cmp" in g)
    r, c = dec(False), dec(True)
    return " ".join(f"{n}{'+' if c[j] else '-'}" for j, n in enumerate(("판정건너뜀", "목록", "분리")) if r[j] != c[j])


win = Counter(); zero = Counter(); fnone = Counter(); by = {}
for i, w, a0, b0, af, bf, *why in lab:
    t = key[i]  # 처리 쪽 글자
    res = "=" if w == "=" else ("처리" if w == t else "대조")
    win[res] += 1
    zero["처리"] += int(a0 if t == "A" else b0); zero["대조"] += int(b0 if t == "A" else a0)
    fnone["처리"] += int(af if t == "A" else bf); fnone["대조"] += int(bf if t == "A" else af)
    by.setdefault(kind(Q[i]), Counter())[res] += 1
a, b = win["처리"], win["대조"]
n, k = a + b, min(a, b)
p = min(1.0, 2 * sum(comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0
print(f"주: 처리 승 {a} · 대조 승 {b} · 동점 {win['=']} (판정 {len(lab)}) → 부호 검정 p {p:.4g}")
print(f"보호 1 무관 인용 '0': 처리 {zero['처리']} · 대조 {zero['대조']} (한도 {zero['대조'] * 1.5:.1f})")
print(f"보호 2 거짓 없음: 처리 {fnone['처리']} · 대조 {fnone['대조']} (한도 {fnone['대조'] + 1})")
ids = [x[0] for x in lab]
t1 = statistics.median(c1[i]["elapsed"] for i in ids); t0 = statistics.median(c0[i]["elapsed"] for i in ids)
print(f"보호 3 응답 시간 중앙: 처리 {t1:.1f}s · 대조 {t0:.1f}s (한도 {t0 + 20:.1f}s)")
NONE = re.compile(r"찾을 수 없|없습니다|찾지 못")
for nm, c in (("대조", c0), ("처리", c1)):
    print(f"보고 {nm}: 인용 편수 {sum(len(c[i].get('answer_papers') or []) for i in ids)} · "
          f"'없음' 꼴 답 {sum(bool(NONE.search(c[i]['answer'].split('📎')[0][:400])) for i in ids)}")
for k_, v in sorted(by.items(), key=lambda x: -sum(x[1].values())):
    print(f"   {k_}: 처리 {v['처리']} · 대조 {v['대조']} · 동점 {v['=']}")
