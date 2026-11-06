"""unit_check_1106: 답의 숫자 단위 불일치 진단 (dev, 오프라인, README).

  .venv/bin/python docs/experiments/unit_check_1106/run.py scan    # 후보 · 표본 → flagged.md · scan.json
  .venv/bin/python docs/experiments/unit_check_1106/run.py score   # labels.tsv 집계
"""
import collections, json, os, random, re, sys

sys.path.insert(0, ".")
from core.llm.answer_fix import _CITED
from core.llm.body_numbers import _blocks, _norm

D = "docs/experiments/unit_check_1106/"
R = "docs/experiments/e2e_ko_1008/results/"
F = "docs/experiments/foundation_1031/"
FILES = ["weekly_20261101", "pl0_dev", "qt0_s2", "ogb0_s2", "ans_hu", "sg0_new", "sg0_old", "nk1", "us_1027"]

NUM = re.compile(r"(?<![A-Za-z0-9_.\-])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)")
# 앞에서부터 맞춘다. 긴 표기와 %p 를 먼저 둔다.
UNITS = [
    ("pp", r"%\s*p\b|퍼센트\s*포인트|percentage points?\b|pp\b"),
    ("percent", r"%|％|퍼센트|percent\b|pct\b"),
    ("times", r"배(?![경치열포])|x\b|×|-?fold\b|times\b"),
    ("ms", r"ms\b|밀리초|milliseconds?\b"),
    ("us", r"µs\b|μs\b|마이크로초|microseconds?\b"),
    ("s", r"초(?![기록과안반])|s\b|secs?\b|seconds?\b"),
    ("min", r"분(?![석야류할의산포])|mins?\b|minutes?\b"),
    ("hour", r"시간(?![대적])|hours?\b|hrs?\b|h\b"),
    ("day", r"일간|days?\b"),
    ("gb", r"GB\b|GiB\b|기가바이트"),
    ("mb", r"MB\b|MiB\b|메가바이트"),
    ("kb", r"KB\b|KiB\b|킬로바이트"),
    ("tb", r"TB\b|TiB\b|테라바이트"),
    ("token", r"tokens?\b|토큰"),
    ("word", r"words?\b|단어"),
    ("thousand", r"K\b|k\b|thousand\b|천(?![천문])"),
    ("million", r"M\b|million\b|백만"),
    ("billion", r"B\b|billion\b|십억"),
    ("man", r"만(?![큼약족])"),
    ("eok", r"억"),
    ("usd", r"달러|USD\b"),
    ("layer", r"layers?\b|층(?![위적])"),
    ("dim", r"dimensions?\b|dim\b|차원"),
    ("person", r"participants?\b|users?\b|명(?![시확령])"),
    ("sample", r"samples?\b|샘플|examples?\b|예제|문항|questions?\b|질문|quer(?:y|ies)\b|쿼리"),
    ("doc", r"documents?\b|문서|papers?\b|논문|편(?![향])"),
    ("fps", r"fps\b|FPS\b"),
    ("watt", r"kWh\b|Wh\b|kW\b|W\b|와트"),
    ("co2", r"k?t\s?CO|톤"),
]
UNIT_RE = [(n, re.compile(p)) for n, p in UNITS]


def to_num(tok):
    return float(tok.replace(",", ""))


def pairs(text):
    """``[(숫자값, 원문 숫자, 단위 또는 None, 위치)]``."""
    out = []
    for m in NUM.finditer(text):
        rest = text[m.end():m.end() + 24]
        if rest.startswith("  "):
            out.append((to_num(m.group(1)), m.group(1), None, m.start()))
            continue
        rest = rest.lstrip(" ")
        unit = next((n for n, p in UNIT_RE if p.match(rest)), None)
        if unit is None and text[max(0, m.start() - 1):m.start()] == "$" and not rest.startswith("$"):
            unit = "usd"
        out.append((to_num(m.group(1)), m.group(1), unit, m.start()))
    return out


def _selftest():
    t = lambda s: [(p[1], p[2]) for p in pairs(s)]
    assert t("지연이 12 ms 줄었다") == [("12", "ms")]
    assert t("3배의 속도와 20%의 정확도") == [("3", "times"), ("20", "percent")]
    assert t("46,080개") == [("46,080", None)]
    assert t("5%p 상승") == [("5", "pp")]
    assert t("GPT-4 와 BM25, F1") == []
    assert t("1.5초") == [("1.5", "s")]
    assert t("12 percent and 3-fold") == [("12", "percent"), ("3", "times")]
    assert t("$12 cost") == [("12", "usd")]
    assert t("$46,080$ 항목") == [("46,080", None)]


def clean(text):
    text = _norm(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    return text


def doc_map(r):
    d = r.get("doc_ids") or {}
    if isinstance(d, list):
        return {i: v for i, v in enumerate(d, 1)}
    return {int(k): v for k, v in d.items()}


def excluded_ids():
    ids = set()
    for f in ("heldout.tsv", "heldout_followup.tsv"):
        for l in open(F + f, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                ids.add(l.split("\t")[0].strip())
    return ids


def load_rows():
    skip = excluded_ids()
    seen, rows, dropped = set(), [], collections.Counter()
    for f in FILES:
        for l in open(R + f + ".jsonl", encoding="utf-8"):
            r = json.loads(l)
            a = r.get("answer") or ""
            if r["id"] in skip:
                dropped["held-out"] += 1
                continue
            if r["id"] in seen:
                dropped["겹침"] += 1
                continue
            if len(a) < 200 or not r.get("numbered_context"):
                dropped["답 또는 컨텍스트 없음"] += 1
                continue
            seen.add(r["id"])
            r["_file"] = f
            rows.append(r)
    return rows, dropped


def scan():
    _selftest()
    rows, dropped = load_rows()
    cnt, items = collections.Counter(), []
    per_file = collections.Counter()
    with_pair = with_flag = 0
    for r in rows:
        per_file[r["_file"]] += 1
        by = _blocks(r["numbered_context"], doc_map(r))
        whole = _norm(r["numbered_context"])
        got = flagged = False
        for line in clean(r["answer"]).split("\n"):
            refs = _CITED.findall(line)
            src = "\n".join(by.get(x, "") for x in refs).strip() or whole
            text = _CITED.sub(" ", line)
            src_pairs = pairs(src)
            for val, tok, unit, pos in pairs(text):
                if unit is None:
                    cnt["단위 모름"] += 1
                    continue
                got = True
                same = [p for p in src_pairs if p[0] == val]
                if not same:
                    cnt["숫자 없음"] += 1
                    continue
                units = collections.Counter(p[2] for p in same)
                if unit in units:
                    cnt["일치"] += 1
                    continue
                kind = "후보" if any(u for u in units) else "단위 없음"
                cnt[kind] += 1
                flagged = flagged or kind == "후보"
                snip = [src[max(0, p[3] - 90):p[3] + 60].replace("\n", " ") for p in same[:3]]
                items.append({"key": f"{r['_file']}|{r['id']}|{tok}|{unit}", "kind": kind, "tok": tok, "unit": unit,
                              "src_units": {str(k): v for k, v in units.items()}, "line": text.strip()[:400], "snip": snip})
        with_pair += got
        with_flag += flagged
    uniq = {i["key"]: i for i in items}
    items = list(uniq.values())
    cand = [i for i in items if i["kind"] == "후보"]
    unk = [i for i in items if i["kind"] == "단위 없음"]
    rng = random.Random(1106)
    sample = rng.sample(sorted(unk, key=lambda x: x["key"]), min(30, len(unk)))
    with open(D + "flagged.md", "w", encoding="utf-8") as w:
        for title, xs in (("후보", cand), ("단위 없음 표본", sample)):
            w.write(f"# {title} {len(xs)}\n\n")
            for i in xs:
                w.write(f"## {i['key']}\n- 블록 단위: {i['src_units']}\n- 답: {i['line']}\n")
                for s in i["snip"]:
                    w.write(f"- 원문: …{s}…\n")
                w.write("\n")
    json.dump({"rows": len(rows), "per_file": per_file, "dropped": dropped, "counts": cnt, "with_pair": with_pair, "with_flag": with_flag,
               "cand": len(cand), "unknown_total": len(unk), "sample": [i["key"] for i in sample]},
              open(D + "scan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("답", len(rows), "· 파일별", dict(per_file), "· 뺌", dict(dropped))
    print("단위 있는 숫자가 든 답", with_pair, "· 후보가 든 답", with_flag)
    print("칸", dict(cnt), "· 후보 고유", len(cand), "· 단위 없음 고유", len(unk))


def score():
    meta = json.load(open(D + "scan.json", encoding="utf-8"))
    lab = {}
    for l in open(D + "labels.tsv", encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            p = l.rstrip("\n").split("\t")
            lab[p[0]] = p[1]
    sample = set(meta["sample"])
    c = collections.Counter(v for k, v in lab.items() if k not in sample)
    s = collections.Counter(v for k, v in lab.items() if k in sample)
    missing = meta["cand"] + len(sample) - len(lab)
    prec = c["T"] / max(1, c["T"] + c["F"])
    print(f"후보 {meta['cand']} · 라벨 빠짐 {missing}")
    print(f"T {c['T']} · F {c['F']} · ? {c['?']} · 정밀도 {prec:.0%}")
    print(f"빈도 T ≥ 5: {'통과' if c['T'] >= 5 else '미달'} · 정밀도 ≥ 60%: {'통과' if prec >= .6 else '미달'}")
    print(f"단위 없음 표본 {len(sample)}: T {s['T']} · F {s['F']} · ? {s['?']}")


if __name__ == "__main__":
    {"scan": scan, "score": score}[sys.argv[1]]()
