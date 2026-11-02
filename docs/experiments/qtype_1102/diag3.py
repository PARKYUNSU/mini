"""qtype_1102 dev: 고른 설정(c14w C10 · L=정규식∨분류기 · C·N=분류기)으로 결정이 바뀌는 문항 수 · 꼴."""
import csv, sys
from collections import Counter

import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

sys.path.insert(0, ".")
from core.llm.presence_judge import gate_types

D = "docs/experiments/qtype_1102/"
qs = {r["uid"]: r for r in csv.DictReader(open(D + "all.tsv"), delimiter="\t")}
lab = dict(l.rstrip("\n").split("\t") for l in open(D + "dev_labels.txt"))
grp = lambda s: "real" if s.startswith("R_") else s.split(":")[0]
rows = [(u, qs[u]["question"], v, grp(qs[u]["srcs"].split()[0])) for u, v in lab.items() if v not in ("X", "?")]
texts = [q for _, q, _, _ in rows]; groups = [g for *_, g in rows]
P = {}
for t in "LCN":
    y = np.array([t in v for _, _, v, _ in rows]); pred = np.zeros(len(rows), bool)
    for tr, te in GroupKFold(n_splits=len(set(groups))).split(texts, y, groups):
        vs = [TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 4), sublinear_tf=True),
              TfidfVectorizer(analyzer="word", token_pattern=r"\S+", ngram_range=(1, 2), sublinear_tf=True)]
        X = hstack([v.fit_transform([texts[i] for i in tr]) for v in vs]).tocsr()
        m = LogisticRegression(C=10, class_weight="balanced", max_iter=3000).fit(X, y[tr])
        pred[te] = m.predict(hstack([v.transform([texts[i] for i in te]) for v in vs]).tocsr())
    P[t] = pred
dec = lambda L, C, N: (bool(L or C or N), bool(L), bool(C))  # (판정 건너뜀, 목록, 비교 분리)
chg = Counter(); n = 0; good = bad = 0
for i, (u, q, v, g) in enumerate(rows):
    gt = gate_types(q)
    r = dec("list" in gt, "cmp" in gt, "num" in gt)
    c = dec(("list" in gt) or P["L"][i], P["C"][i], P["N"][i])
    y = dec("L" in v, "C" in v, "N" in v)
    if r != c:
        n += 1
        kind = " ".join(f"{k}{'+' if c[j] else '-'}" for j, k in enumerate(("skip", "list", "split")) if r[j] != c[j])
        chg[kind] += 1
        good += (c == y) and (r != y); bad += (r == y) and (c != y)
print("결정 바뀐 문항", n, "/", len(rows), f"({n/len(rows):.0%})", "| 분류기 쪽만 라벨과 맞음", good, "· 정규식 쪽만", bad)
for k, v in chg.most_common():
    print("  ", k, v)
