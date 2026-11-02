"""qtype_1102 §4.1: held-out 유형 정확도(관문) · 새 54 보고 · 2단계 문항(결정 바뀜) 목록."""
import csv, os, sys
from math import comb

sys.path.insert(0, ".")
from core.llm.presence_judge import gate_types

D = "docs/experiments/qtype_1102/"


def decide(q, clf):
    os.environ["RAG_QTYPE_CLF"] = "1" if clf else "0"
    g = gate_types(q)
    return (bool(g), "list" in g, "cmp" in g)


def gold(v):
    return (any(c in v for c in "LCN"), "L" in v, "C" in v)


def p2(a, b):
    n, k = a + b, min(a, b)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n) if n else 1.0


def run(name, items):
    """items: (id, 질문, 라벨). 반환: 결정이 바뀐 id 목록."""
    use = [(i, q, v) for i, q, v in items if v != "?"]
    rr = cc = ronly = conly = 0
    err = {k: [0, 0, 0, 0] for k in ("skip", "list", "split")}  # 정규식 FP FN · 분류기 FP FN
    changed = []
    for i, q, v in use:
        r, c, y = decide(q, False), decide(q, True), gold(v)
        rr += r == y; cc += c == y
        ronly += (r == y) and (c != y); conly += (c == y) and (r != y)
        for j, k in enumerate(err):
            err[k][0] += r[j] and not y[j]; err[k][1] += y[j] and not r[j]
            err[k][2] += c[j] and not y[j]; err[k][3] += y[j] and not c[j]
        if r != c:
            changed.append((i, v, r, c, q))
    print(f"== {name}: {len(use)}문항 | 세 결정 모두 맞음 정규식 {rr} · 분류기 {cc} | 정규식만 {ronly} · 분류기만 {conly} "
          f"(부호 검정 p {p2(ronly, conly):.3g}) | 바뀜 {len(changed)}")
    for k, (a, b, c_, d) in err.items():
        print(f"   {k}: 정규식 FP {a} FN {b} · 분류기 FP {c_} FN {d}")
    fmt = lambda t: "".join(n for n, x in zip(("판정건너뜀 ", "목록 ", "분리 "), t) if x).strip() or "-"
    for i, v, r, c, q in changed:
        print(f"   {i} [{v}] 정규식 {fmt(r)} → 분류기 {fmt(c)} | {q[:80]}")
    return changed


qs = {r["uid"]: r for r in csv.DictReader(open(D + "all.tsv"), delimiter="\t")}
tl = dict(l.rstrip("\n").split("\t") for l in open(D + "test_labels.txt"))
held = [(qs[u]["srcs"].split()[-1].split(":")[-1] if "foundation_1031:" in qs[u]["srcs"] else u, qs[u]["question"], v) for u, v in tl.items()]
held = [((s.split(":")[-1] for s in qs[u]["srcs"].split() if "foundation_1031:" in s).__next__(), qs[u]["question"], v) for u, v in tl.items()]
new_l = dict(l.rstrip("\n").split("\t") for l in open(D + "heldout_new_labels.txt"))
new = [(r[0], r[1], new_l[r[0]]) for r in csv.reader(open(D + "heldout_new.tsv"), delimiter="\t")]
ch_h = run("held-out 100 (관문)", held)
ch_n = run("새 54 (보고)", new)
with open(D + "stage2_ids.txt", "w") as f:
    f.write("".join(f"{i}\n" for i, *_ in ch_h + ch_n))
