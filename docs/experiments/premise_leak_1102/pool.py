"""premise_leak_1102 §1 (R4 dev 조사): 이미 판정한 결론 문장에 질문 · 인용 블록 겹침 특징을 붙인다(맥미니, 읽기만)."""
import collections, json, re, sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, "docs/experiments/conclusion_verify_1101")
import offline as OV  # noqa: E402

EXP = Path("docs/experiments")
CS = EXP / "conclusion_struct_1102"

# 질문 찾기 — 출처마다 따로(같은 id 가 세트마다 다름)
Q = {}
for l in open(EXP / "answer_judge_1024/sample.md", encoding="utf-8"):
    m = re.match(r"######## A\d\d \[\w\] (\S+) (\S+) \| Q: (.*)", l)
    if m:
        Q[(m.group(1), m.group(2))] = m.group(3).strip()
for x in map(json.loads, open(EXP / "conclusion_v3_1024/results.jsonl", encoding="utf-8")):
    Q[(x["set"], x["id"])] = x["question"]
for d, lbl in (("conclusion_drop2_1025", "cd2_new"), ("conclusion_overgen_1025", "cov_new")):
    for l in open(EXP / d / "questions.tsv", encoding="utf-8"):
        if "\t" in l:
            a, b = l.rstrip("\n").split("\t", 1)
            Q[(lbl, a)] = b.split("\t")[0]
for l in open(EXP / "corpus_llmeval_1030/questions.tsv", encoding="utf-8"):
    if l.startswith("R_"):
        a, b = l.rstrip("\n").split("\t", 1)
        Q[("recheck_1031", a)] = b.split("\t")[0]

xs, _, grp = OV.items()
pool = []
for it in xs:
    rec, ctx = OV.prepare(it, grp)
    rec["q"] = Q.get(tuple(it[1]))
    rec["ctx"] = ctx
    pool.append(rec)

# D1 판정의 전(9B) 문장 — 61문항은 11-02 에 dev 로 옮김
DQ = dict(l.rstrip("\n").split("\t", 1) for l in open(EXP / "foundation_1031/dev_from_heldout_1102.tsv", encoding="utf-8") if "\t" in l)
key = json.load(open(CS / "judge/key.json", encoding="utf-8"))["sentences"]
lab = {tuple(l.split("\t")[:2]): l.rstrip("\n").split("\t")[2] for l in open(CS / "judge/labels.tsv", encoding="utf-8") if l.strip()}
txt = {}
for p in sorted(CS.glob("judge/packets_*.md")):
    cur = None
    for l in open(p, encoding="utf-8"):
        m = re.match(r"## (H_\w+) — ", l)
        if m:
            cur = m.group(1)
        m = re.match(r"- (s\d+): (.*)", l)
        if m and cur:
            txt[(cur, m.group(1))] = m.group(2).strip()
rows = {r["id"]: r for r in map(json.loads, open(EXP / "e2e_ko_1008/results/cs0_heldout.jsonl", encoding="utf-8"))}
for qid, m in key.items():
    if qid not in DQ:
        continue
    bl = OV.blocks(rows[qid])
    for s, (side, _) in m.items():
        if side != "전":
            continue
        t = txt[(qid, s)]
        refs = [re.sub(r"v\d+$", "", i) for i in dict.fromkeys(OV._CITED.findall(t))]
        pool.append({"src": "d1", "key": ["cs0_heldout", qid], "sid": s, "sent": t, "label": lab[(qid, s)],
                     "refs": refs, "scope": "인용", "q": DQ[qid], "ctx": "\n\n".join(bl.get(p, "") for p in refs)})

_CIT = re.compile(r"\[\s*\d{4}\.\d{4,5}(?:v\d+)?\s*\]")
_PUN = re.compile(r"[^\w가-힣]+")
_NUM = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?")
_LAT = re.compile(r"[A-Za-z][A-Za-z0-9\-]{2,}")
STOP = {"the", "and", "for", "with", "this", "that", "are", "from", "our", "llm", "llms", "rag", "model", "models", "based"}


def norm(s):
    return _PUN.sub("", _CIT.sub("", s))


def toks(s):
    s = _CIT.sub("", s)
    return {n.replace(",", "") for n in _NUM.findall(s)} | {w.lower() for w in _LAT.findall(s) if w.lower() not in STOP}


def feats(r):
    s, q, c = norm(r["sent"]), norm(r["q"] or ""), r["ctx"]
    m = SequenceMatcher(None, s, q, autojunk=False).find_longest_match(0, len(s), 0, len(q))
    tri = {s[i:i + 3] for i in range(len(s) - 2)}
    qtri = {q[i:i + 3] for i in range(len(q) - 2)}
    st, ct, qt = toks(r["sent"]), toks(c), toks(r["q"] or "")
    return {"lcs": m.size, "q3": round(len(tri & qtri) / max(1, len(tri)), 2), "doc": len(st & ct),
            "qonly": sorted((st & qt) - ct), "tok": len(st)}


ERR = {"E", "X", "U"}
pool = [r for r in pool if r.get("q") and "skip" not in r]
for r in pool:
    r.update(feats(r))
print("표본", len(pool), dict(collections.Counter(r["src"] for r in pool)), dict(collections.Counter(r["label"] for r in pool)))
for name, f in (("lcs>=8", lambda r: r["lcs"] >= 8), ("lcs>=12", lambda r: r["lcs"] >= 12),
                ("q3>=0.4", lambda r: r["q3"] >= 0.4), ("doc=0", lambda r: r["doc"] == 0),
                ("lcs>=8 & doc=0", lambda r: r["lcs"] >= 8 and r["doc"] == 0),
                ("q3>=0.3 & doc=0", lambda r: r["q3"] >= 0.3 and r["doc"] == 0),
                ("qonly", lambda r: bool(r["qonly"]))):
    z = [r for r in pool if f(r)]
    c = collections.Counter(r["label"] for r in z)
    print(f"{name:16s} {len(z):4d}  오류 {sum(c[k] for k in ERR):3d}  O {c['O']:3d}  {dict(c)}")
print("\n## lcs 상위 25")
for r in sorted(pool, key=lambda r: -r["lcs"])[:25]:
    print(f"{r['label']} lcs{r['lcs']} q3 {r['q3']} doc{r['doc']} qonly{r['qonly']} | {r['src']} {r['key'][1]} | {r['sent'][:110]}")
print("\n## qonly 있는 문장")
for r in pool:
    if r["qonly"]:
        print(f"{r['label']} lcs{r['lcs']} doc{r['doc']} {r['qonly']} | {r['key'][1]} | {r['sent'][:110]}")
