"""list_findings_v2_1026 채점 (맥미니) — 자동 지표 + 눈가림 표본(blind.md) · 공개 집계(judged.tsv 가 있으면)."""
import glob, json, random, re, statistics as st, sys
from math import comb
from pathlib import Path

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "list_findings_v2_1026"
A = ("lf0v", "lf2")
AB = {}
for f in ["raw_data_queue/crawled_papers.jsonl"] + glob.glob("raw_data_queue/processed/*.jsonl"):
    for l in open(f):
        try:
            d = json.loads(l)
        except ValueError:
            continue
        AB.setdefault(re.sub(r"v\d+$", "", d.get("paper_id", "")),
                      re.sub(r"\s+", " ", d.get("abstract") or "").replace("\\%", "%").replace("{,}", ","))
_CITE = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]")


def items(ans):
    body = (ans or "").split("본론", 1)[-1].split("결론", 1)[0]
    return [x.strip() for x in re.split(r"\n\s*(?:<b>)?\d+\.\s", "\n" + body)[1:] if x.strip()]


def nums(text):
    t = re.sub(r"\[[^\]]*\]|<[^>]+>|\b(19|20)\d{2}\b", " ", text)
    return {n for n in re.findall(r"\d+(?:[.,]\d+)?", t) if len(n) > 1}


def grade(it):
    src = " ".join(AB.get(p, "") for p in _CITE.findall(it))
    ns = nums(it); ok = {n for n in ns if re.search(rf"(?<![\d.,]){re.escape(n)}(?![\d])", src)}
    return bool(ok), bool(ns - ok)


def sign(w, l):
    n = w + l
    return min(1, 2 * sum(comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n) if n else 1


rows = {a: {r["id"]: r for r in map(json.loads, open(R / f"{a}.jsonl"))} for a in A}
keys = [k for k in rows["lf0v"] if rows["lf0v"][k].get("answer") and rows["lf2"].get(k, {}).get("answer")]
per = {a: {k: [grade(i) for i in items(rows[a][k]["answer"])] for k in keys} for a in A}
g = {a: {k: sum(x for x, _ in v) for k, v in per[a].items()} for a in A}
w = sum(g["lf2"][k] > g["lf0v"][k] for k in keys); l = sum(g["lf2"][k] < g["lf0v"][k] for k in keys)
for a in A:
    its = [x for v in per[a].values() for x in v]
    print(a, "항목", len(its), "근거 수치", sum(x for x, _ in its), "초록 밖 숫자", sum(y for _, y in its),
          "시간 중앙", st.median(rows[a][k]["elapsed"] for k in keys), "길이 중앙", st.median(len(rows[a][k]["answer"]) for k in keys))
print(f"문항 {len(keys)} · 근거 수치 lf2 많음 {w} : 적음 {l} · p {sign(w, l):.4f}")

rnd = random.Random(1026); pool = []
for a in A:
    cand = [(a, k, i, it) for k in keys for i, it in enumerate(items(rows[a][k]["answer"])) if _CITE.search(it)]
    pool += rnd.sample(cand, min(60, len(cand)))
rnd.shuffle(pool)
key = {f"S{n:03d}": [a, k, i] for n, (a, k, i, _) in enumerate(pool)}
with open(D / "blind.md", "w") as f:
    for n, (a, k, i, it) in enumerate(pool):
        p = _CITE.findall(it)[0]
        f.write(f"### S{n:03d} [{p}]\n초록: {AB.get(p, '(없음)')[:1500]}\n항목: {re.sub(r'<[^>]+>', '', it)}\n\n")
json.dump(key, open(D / "blind_key.json", "w"))

jt = D / "judged.tsv"
if jt.exists():
    lab = dict(l.split("\t")[:2] for l in open(jt).read().splitlines()[1:])
    c = {a: {"R": 0, "B": 0, "W": 0} for a in A}
    for s, v in lab.items():
        c[key[s][0]][v] += 1
    # Fisher 정확 검정(양측): 관측 표 이하 확률인 표들의 합
    b2, b0 = c["lf2"]["B"], c["lf0v"]["B"]; n2, n0 = sum(c["lf2"].values()), sum(c["lf0v"].values()); K = b2 + b0
    pr = lambda x: comb(n2, x) * comb(n0, K - x) / comb(n2 + n0, K)
    p = sum(pr(x) for x in range(max(0, K - n0), min(K, n2) + 1) if pr(x) <= pr(b2) * (1 + 1e-9))
    print("눈가림", c, f"B Fisher p {p:.4f}")
