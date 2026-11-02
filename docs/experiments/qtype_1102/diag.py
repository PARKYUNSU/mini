"""qtype_1102 dev 진단: 정규식 게이트 대 라벨 · 글자 n-gram 분류기(세트별 교차 검증)."""
import csv, sys
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

sys.path.insert(0, ".")
from core.llm.presence_judge import gate_types
from core.graph.agent_nodes import is_followup

D = "docs/experiments/qtype_1102/"
qs = {r["uid"]: r for r in csv.DictReader(open(D + "all.tsv"), delimiter="\t")}
lab = dict(l.rstrip("\n").split("\t") for l in open(D + "dev_labels.txt"))
rows = [(u, qs[u]["question"], v, qs[u]["srcs"].split()[0].split(":")[0].split("_")[0] if not qs[u]["srcs"].startswith("R_") else "real")
        for u, v in lab.items() if v not in ("X", "?")]
print("dev 쓸 문항", len(rows), Counter(r[2] for r in rows))
GATES = {"skip": lambda v: any(c in v for c in "LCN"), "list": lambda v: "L" in v, "split": lambda v: "C" in v, "follow": lambda v: "F" in v}
REGEX = {"skip": lambda q: bool(gate_types(q)), "list": lambda q: "list" in gate_types(q),
         "split": lambda q: "cmp" in gate_types(q), "follow": is_followup}
gold = {g: np.array([f(v) for _, _, v, _ in rows]) for g, f in GATES.items()}
rx = {g: np.array([f(q) for _, q, _, _ in rows]) for g, f in REGEX.items()}
texts = [q for _, q, _, _ in rows]
groups = [s for *_, s in rows]
print("그룹", Counter(groups))
# 분류기: 유형 L·C·N·F 마다 이진. skip = L|C|N
clf_pred = {}
for t in "LCNF":
    y = np.array([t in v for _, _, v, _ in rows])
    pred = np.zeros(len(rows), bool)
    for tr, te in GroupKFold(n_splits=min(8, len(set(groups)))).split(texts, y, groups):
        if y[tr].sum() == 0:
            continue
        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 4), sublinear_tf=True)
        X = vec.fit_transform([texts[i] for i in tr])
        m = LogisticRegression(C=10, class_weight="balanced", max_iter=2000).fit(X, y[tr])
        pred[te] = m.predict(vec.transform([texts[i] for i in te]))
    clf_pred[t] = pred
clf = {"skip": clf_pred["L"] | clf_pred["C"] | clf_pred["N"], "list": clf_pred["L"], "split": clf_pred["C"], "follow": clf_pred["F"]}
for g in GATES:
    y, r, c = gold[g], rx[g], clf[g]
    def cm(p):
        return f"FP {int((p & ~y).sum())} FN {int((~p & y).sum())} 맞음 {int((p == y).sum())}"
    b = int(((r == y) & (c != y)).sum()); cc = int(((r != y) & (c == y)).sum())
    print(f"[{g}] 라벨 참 {int(y.sum())} | 정규식 {cm(r)} | 분류기(CV) {cm(c)} | 정규식만 맞음 {b} · 분류기만 맞음 {cc}")
# 전체 결정(skip·list·split·follow 모두 맞음)
allr = np.all([rx[g] == gold[g] for g in GATES], axis=0); allc = np.all([clf[g] == gold[g] for g in GATES], axis=0)
print("네 결정 모두 맞음: 정규식", int(allr.sum()), "분류기", int(allc.sum()), "/", len(rows),
      "| 정규식만", int((allr & ~allc).sum()), "분류기만", int((~allr & allc).sum()))
print("\n정규식 틀림 (결정별):")
for g in GATES:
    bad = [(rows[i][0], rows[i][2], "+" if rx[g][i] else "-", rows[i][1][:90]) for i in range(len(rows)) if rx[g][i] != gold[g][i]]
    print(f"--- {g} {len(bad)}")
    for b_ in bad:
        print("  ", *b_)
