"""num_absent_1107: 답에 있는데 근거 블록에 없는 숫자 (dev, 오프라인, README).

  .venv/bin/python docs/experiments/num_absent_1107/run.py scan    # 후보 → flagged.md · scan.json
  .venv/bin/python docs/experiments/num_absent_1107/run.py score   # labels.tsv 집계
"""
import collections, json, os, random, re, sys

sys.path.insert(0, ".")
sys.path.insert(0, "docs/experiments/unit_check_1106")
import run as U  # load_rows · doc_map 를 같이 쓴다
from core.llm.answer_fix import _CITED
from core.llm.body_numbers import _blocks, _norm

D = "docs/experiments/num_absent_1107/"
E = "docs/experiments/"
QFILES = {"weekly_20261101": ["real_eval_1013/questions.tsv"], "pl0_dev": ["premise_leak_1102/dev_questions.tsv"],
          "qt0_s2": ["qtype_1102/heldout_new.tsv", "qtype_1102/stage2_questions.tsv"], "ogb0_s2": ["open_gate2_1103/stage2_questions.tsv", "open_gate2_1103/heldout_open2.tsv"],
          "ans_hu": ["topic_split2_1104/heldout.tsv"], "sg0_new": ["survey_gate_1030/new_questions.tsv"], "sg0_old": ["survey_gate_1030/old_questions.tsv"],
          "nk1": ["nodoc_conclusion_1029/questions.tsv"], "us_1027": ["user_suite_1027/questions.tsv"]}
TOK = re.compile(r"(?<![A-Za-z0-9_.\-‐‑])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)")
SRC = re.compile(r"(?<![\d.,])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)")
BROKEN = re.compile(r"(?<=\d) *_\._ *(?=\d)")
YEAR = re.compile(r"^(19|20)\d{2}$")
ITEM = re.compile(r"^\s*\d{1,2}\.\s")
SECT = re.compile(r"<b>(서론|본론|결론)</b>")


def val(t):
    return float(t.replace(",", ""))


def src_vals(text):
    return {val(t) for t in SRC.findall(BROKEN.sub(".", _norm(text)))}


def questions():
    out = {}
    for f, names in QFILES.items():
        q = {}
        for n in names:
            for l in open(E + n, encoding="utf-8", errors="replace"):
                p = l.rstrip("\n").split("\t")
                if len(p) >= 2 and p[0] not in q:
                    q[p[0]] = p[1]
        out[f] = q
    return out


def sections(answer):
    a = answer.split("📎")[0]
    parts = SECT.split(a)
    yield "머리", parts[0]
    for k in range(1, len(parts) - 1, 2):
        yield parts[k], parts[k + 1]


def line_tokens(line):
    if "요청한" in line:
        return []
    text = _CITED.sub(" ", re.sub(r"<[^>]+>", " ", _norm(line)))
    text = ITEM.sub(" ", text)
    out = []
    for m in TOK.finditer(text):
        t = m.group(1)
        if ("." not in t and len(t.replace(",", "")) == 1) or YEAR.match(t):
            continue
        out.append(t)
    return out, text


def near(src, v):
    """라벨용: 값이 가까운 원문 숫자와 그 주변."""
    hits = []
    s = BROKEN.sub(".", _norm(src))
    for m in SRC.finditer(s):
        x = val(m.group(1))
        if v and abs(x - v) <= 0.05 * abs(v) or (v and 0 < x < 1 and abs(x * 100 - v) <= 0.5) or (v and x > 1 and abs(x - v * 100) <= 0.5 and v < 1):
            hits.append(s[max(0, m.start() - 70):m.end() + 40].replace("\n", " "))
    return hits[:2]


def scan():
    rows, dropped = U.load_rows()
    Q = questions()
    noq = 0
    cnt = collections.Counter()
    by_sect = collections.Counter()
    items = {}
    answers = collections.defaultdict(set)
    for r in rows:
        ctx = r["numbered_context"]
        by = _blocks(ctx, U.doc_map(r))
        whole = src_vals(ctx)
        q = Q.get(r["_file"], {}).get(r["id"])
        if q is None:
            noq += 1
        qv = src_vals(q or "")
        for sect, body in sections(r["answer"]):
            for line in body.split("\n"):
                got = line_tokens(line)
                if not got:
                    continue
                toks, text = got
                if not toks:
                    continue
                refs = _CITED.findall(line)
                src = "\n".join(by.get(x, "") for x in refs).strip()
                cited = src_vals(src) if src else whole
                for t in toks:
                    v = val(t)
                    cnt["숫자"] += 1
                    if v in qv:
                        cnt["질문에 있음"] += 1
                        continue
                    if v in cited:
                        cnt["있음"] += 1
                        continue
                    kind = "A" if v in whole else "B"
                    cnt[kind] += 1
                    by_sect[(sect, kind)] += 1
                    numbered = bool(ITEM.match(re.sub(r"<[^>]+>", "", line)))
                    key = f"{r['_file']}|{r['id']}|{t}"
                    answers[kind].add(r["id"])
                    if key not in items:
                        pos = text.find(t)
                        items[key] = {"key": key, "kind": kind, "sect": sect, "numbered": numbered, "refs": len(refs),
                                      "line": text[max(0, pos - 150):pos + 130].strip(), "near": near(src or ctx, v)}
    its = list(items.values())
    rng = random.Random(1107)
    read = its if len(its) <= 80 else rng.sample(sorted(its, key=lambda x: x["key"]), 80)
    with open(D + "flagged.md", "w", encoding="utf-8") as w:
        w.write(f"# 후보 {len(its)} · 읽을 것 {len(read)}\n\n")
        for i in sorted(read, key=lambda x: x["key"]):
            w.write(f"## {i['key']}\n- 칸 {i['kind']} · 구역 {i['sect']} · 번호 항목 {i['numbered']} · 인용 {i['refs']}\n- 답: {i['line']}\n")
            for s in i["near"]:
                w.write(f"- 가까운 원문: …{s}…\n")
            w.write("\n")
    json.dump({"rows": len(rows), "counts": cnt, "sect": {f"{k[0]}|{k[1]}": v for k, v in by_sect.items()}, "unique": len(its), "read": [i["key"] for i in read],
               "answers_A": len(answers["A"]), "answers_B": len(answers["B"]), "no_question": noq, "all": {i["key"]: {"kind": i["kind"], "sect": i["sect"], "numbered": i["numbered"]} for i in its}},
              open(D + "scan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("답", len(rows), "· 뺌", dict(dropped), "· 질문 못 찾음", noq)
    print("칸", dict(cnt), "· 후보 고유", len(its), "· A 답", len(answers["A"]), "· B 답", len(answers["B"]))
    print("구역", sorted(by_sect.items()))


def score():
    m = json.load(open(D + "scan.json", encoding="utf-8"))
    lab = {}
    for l in open(D + "labels.tsv", encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            p = l.rstrip("\n").split("\t")
            lab[p[0]] = (p[1], p[2] if len(p) > 2 else "")
    c = collections.Counter(v[0] for v in lab.values())
    scale = m["unique"] / max(1, len(m["read"]))
    x = c["X"]
    prec = x / max(1, x + c["O"])
    print(f"후보 {m['unique']} · 읽음 {len(m['read'])} · 라벨 {len(lab)} · X {x} · O {c['O']} · ? {c['?']} · 정밀도 {prec:.0%} · 환산 X {x * scale:.1f}")
    print(f"빈도 X ≥ 5: {'통과' if x * scale >= 5 else '미달'} · 정밀도 ≥ 60%: {'통과' if prec >= .6 else '미달'}")
    by = collections.Counter()
    for k, v in lab.items():
        i = m["all"][k]
        by[(i["sect"], "번호" if i["numbered"] else "문단", i["kind"], v[0])] += 1
    print("구역별", sorted(by.items()))
    print("X 답", len({k.split("|")[1] for k, v in lab.items() if v[0] == "X"}))
    print("O · X 까닭:", collections.Counter(v[1].split(" ")[0] for v in lab.values()).most_common(12))


def sent():
    """본 뒤 추가(README §7, 힌트 전용): 문장 단위로 인용 블록과 대조해 다른 논문의 숫자를 붙인 자리를 찾는다."""
    rows, _ = U.load_rows()
    Q = questions()
    total, hits = 0, []
    for r in rows:
        ctx = r["numbered_context"]
        by = _blocks(ctx, U.doc_map(r))
        whole = src_vals(ctx)
        qv = src_vals(Q.get(r["_file"], {}).get(r["id"]) or "")
        for sect, body in sections(r["answer"]):
            for line in body.split("\n"):
                if len(set(_CITED.findall(line))) < 2 or "요청한" in line:
                    continue
                for snt in re.split(r"(?<=[.!?。])\s+", line):
                    refs = _CITED.findall(snt)
                    src = "\n".join(by.get(x, "") for x in refs).strip()
                    if not src:
                        continue
                    got = line_tokens(snt)
                    if not got or not got[0]:
                        continue
                    cited = src_vals(src)
                    for t in got[0]:
                        v = val(t)
                        total += 1
                        if v in qv or v in cited or v not in whole:
                            continue
                        other = [k for k, b in by.items() if k not in refs and v in src_vals(b)]
                        hits.append((r["_file"], r["id"], t, sect, got[1].strip()[:230], other[:2], near(ctx, v)[:1]))
    print("여러 논문을 인용한 줄의 문장 숫자", total, "· 다른 논문에 있는 숫자", len(hits))
    for h in hits:
        print(" ", h)


if __name__ == "__main__":
    {"scan": scan, "score": score, "sent": sent}[sys.argv[1]]()
