"""qtype_1102 dev: 유형별(L·C·N·F) 정규식 · 분류기 변형 · 합치기(세트별 교차 검증)."""
import csv, sys
from collections import Counter

import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

sys.path.insert(0, ".")
from core.llm.presence_judge import gate_types
from core.graph.agent_nodes import is_followup

D = "docs/experiments/qtype_1102/"
qs = {r["uid"]: r for r in csv.DictReader(open(D + "all.tsv"), delimiter="\t")}
lab = dict(l.rstrip("\n").split("\t") for l in open(D + "dev_labels.txt"))
grp = lambda s: "real" if s.startswith("R_") else s.split(":")[0]
rows = [(u, qs[u]["question"], v, grp(qs[u]["srcs"].split()[0])) for u, v in lab.items() if v not in ("X", "?")]
texts = [q for _, q, _, _ in rows]; groups = [g for *_, g in rows]
Y = {t: np.array([t in v for _, _, v, _ in rows]) for t in "LCNF"}
RX = {"L": np.array(["list" in gate_types(q) for q in texts]), "C": np.array(["cmp" in gate_types(q) for q in texts]),
      "N": np.array(["num" in gate_types(q) for q in texts]), "F": np.array([is_followup(q) for q in texts])}

def feats(kind):
    if kind == "c14":
        return [TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 4), sublinear_tf=True)]
    if kind == "c25":
        return [TfidfVectorizer(analyzer="char", ngram_range=(2, 5), sublinear_tf=True)]
    if kind == "c14w":
        return [TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 4), sublinear_tf=True),
                TfidfVectorizer(analyzer="word", token_pattern=r"\S+", ngram_range=(1, 2), sublinear_tf=True)]

def cv(t, kind, C):
    y = Y[t]; pred = np.zeros(len(rows), bool)
    for tr, te in GroupKFold(n_splits=len(set(groups))).split(texts, y, groups):  # 세트 하나씩 빼기
        if y[tr].sum() == 0:
            continue
        vs = feats(kind)
        X = hstack([v.fit_transform([texts[i] for i in tr]) for v in vs]).tocsr()
        m = LogisticRegression(C=C, class_weight="balanced", max_iter=3000).fit(X, y[tr])
        pred[te] = m.predict(hstack([v.transform([texts[i] for i in te]) for v in vs]).tocsr())
    return pred

def show(name, t, p):
    y = Y[t]
    return f"{name}: FP {int((p & ~y).sum()):3d} FN {int((~p & y).sum()):3d} 틀림 {int((p != y).sum()):3d}"

for t in "LCNF":
    print(f"== {t} (참 {int(Y[t].sum())})", show("정규식", t, RX[t]))
    for kind in ("c14", "c25", "c14w"):
        for C in (1, 10):
            p = cv(t, kind, C)
            print("   ", show(f"{kind} C{C}", t, p), "|", show("정규식∨분류기", t, p | RX[t]), "|", show("정규식∧분류기", t, p & RX[t]))
