"""qtype_1102: dev 라벨(dev_labels.txt)로 분류기 학습 파일 core/llm/qtype_train.tsv 를 만든다.

질문 아님(X) · 애매(?) 는 뺀다. held-out(test) 은 넣지 않는다 — 들어가면 멈춘다.
"""
import csv

D = "docs/experiments/qtype_1102/"
qs = {r["uid"]: r for r in csv.DictReader(open(D + "all.tsv"), delimiter="\t")}
rows = []
for line in open(D + "dev_labels.txt"):
    uid, lab = line.rstrip("\n").split("\t")
    assert qs[uid]["split"] == "dev", uid
    if lab not in ("X", "?"):
        rows.append((lab, qs[uid]["question"]))
with open("core/llm/qtype_train.tsv", "w", encoding="utf-8") as f:
    f.write("".join(f"{lab}\t{q}\n" for lab, q in rows))
print(len(rows), "줄")
