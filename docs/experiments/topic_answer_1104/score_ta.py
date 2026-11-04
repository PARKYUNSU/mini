"""topic_answer_1104: classes_ta1.tsv 를 세어 dev 관문(README §4)과 맞춰 본다. 손 분류를 trace · 문서 라벨과 교차 검사한다."""
import collections, json, re, statistics, sys
sys.path.insert(0, "docs/experiments/topic_split2_1104")
import score as S

BLANKET = re.compile(r"찾는 연구가 없습니다|찾을 수 없습니다")
D = "docs/experiments/topic_filter_1104/"
gold = {g["id"]: g for g in map(json.loads, open(S.D + "heldout_gold.jsonl", encoding="utf-8"))}
lab = {}
for f in (S.D + "labels_hu.tsv", D + "labels_pool.tsv"):
    for l in open(f, encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            q, p, v = l.rstrip("\n").split("\t")[:3]
            lab.setdefault((q, p), v.strip())


def load(path):
    out = {}
    for l in open(path, encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            c = (l.rstrip("\n").split("\t") + [""] * 7)[:7]
            out[(c[0], int(c[1]))] = c
    return out


ta = load("docs/experiments/topic_answer_1104/classes_ta1.tsv")
ct = {k: [v[0], v[1], v[2], v[3], "", v[4], v[5]] for k, v in load("docs/experiments/answer_gap_1104/classes.tsv").items()}
rows = S.rows("ta1_hu")
assert set(ta) == set(ct) == {(q, k) for q in gold for k in range(1, len(gold[q]["topics"]) + 1)}

# 교차 검사: C/U 는 문서 라벨과, 안내 Y 는 trace 와, 전체 없음 Y 는 정규식과 맞아야 한다.
judge_u = judge_fn = 0
for q, r in rows.items():
    cov = {int(x) for p in S.docs(r) for x in lab[(q, p)].replace("-", "").split(",") if x.strip()}
    j = {x.get("stage"): x for x in r["trace"]}["judge"]
    assert len(j["items"]) == len(gold[q]["topics"]), q
    for k in range(1, len(gold[q]["topics"]) + 1):
        c = ta[(q, k)]
        assert c[2] == ("C" if k in cov else "U"), c
        assert ct[(q, k)][2] == c[2], c
        none = not j["item_docs"][str(k)]
        if none and j.get("pick") != "없음":
            assert c[4] == "Y", c
        judge_u += none and c[2] == "U"
        judge_fn += none and c[2] == "C"
    assert any(ta[(q, k)][5] for k in range(1, len(gold[q]["topics"]) + 1)) == bool(BLANKET.search(r["answer"])), q


def metrics(cls):
    u = [c for c in cls.values() if c[2] == "U"]
    c_ = [c for c in cls.values() if c[2] == "C"]
    blanket = {c[0] for c in cls.values() if c[5] == "Y"}
    return {
        "blanket_with_C": sum(any(c[0] == q and c[2] == "C" for c in cls.values()) for q in blanket),
        "disclosed": sum(c[3] == "H" or c[4] == "Y" for c in u),
        "disclosed_clean": sum(c[3] == "H" for c in u),
        "U_X": sum(c[3] == "X" for c in u),
        "U_X_with_notice": sum(c[3] == "X" and c[4] == "Y" for c in u),
        "U_X_edge": sum(c[3] == "X" and c[6].startswith("경계") for c in u),
        "C_S": sum(c[3] == "S" for c in c_),
        "C_said_none": sum(c[3] == "H" or c[4] == "Y" for c in c_),
        "U": dict(sorted(collections.Counter(c[3] for c in u).items())),
        "C": dict(sorted(collections.Counter(c[3] for c in c_).items())),
    }


t0 = statistics.median(r["elapsed"] for r in S.rows("ans_hu").values())
t1 = statistics.median(r["elapsed"] for r in rows.values())
A, B = metrics(ct), metrics(ta)
print("대조", A)
print("처리", B)
print(f"항목 판정(운영 경로): 문서 없는 주제 {judge_u}/42 없음 · 문서 있는 주제 {judge_fn}/79 잘못 없음")
print(f"시간 중앙 {t0:.1f}s → {t1:.1f}s ({t1 - t0:+.1f}s)")
gates = [
    ("전체 없음 문구 답(문서 있는 주제 있음) ≤ 2", B["blanket_with_C"] <= 2),
    ("문서 없는 주제 밝힘 ≥ 21", B["disclosed"] >= 21),
    ("문서 없는 주제 근거 없이 다룸 ≤ 7", B["U_X"] <= 7),
    ("문서 있는 주제 근거 있게 다룸 ≥ 60", B["C_S"] >= 60),
    ("문서 있는 주제 없다고 안내 ≤ 12", B["C_said_none"] <= 12),
    ("응답 시간 중앙 ≤ +20s", t1 - t0 <= 20),
]
for name, ok in gates:
    print("통과" if ok else "미달", name)
