"""eval30_1110 답 단계 채점 (README §6).

  .venv/bin/python docs/experiments/eval30_1110/score_answer.py ev30_ans auto     # 자동 지표
  .venv/bin/python docs/experiments/eval30_1110/score_answer.py ev30_ans packet   # 라벨 묶음 → label_packet_answer.md
  .venv/bin/python docs/experiments/eval30_1110/score_answer.py ev30_ans labels   # labels_answer.tsv 집계
"""
import collections, glob, json, random, re, statistics, sys

D = "docs/experiments/eval30_1110/"
R = "docs/experiments/e2e_ko_1008/results/"
CITE = re.compile(r"\[\s*(\d{4}\.\d{4,5})(?:v\d+)?\s*\]")


def norm(p):
    return re.sub(r"v\d+$", "", str(p))


def load(label):
    rows = {r["id"]: r for r in map(json.loads, open(R + label + ".jsonl", encoding="utf-8"))}
    gold = {g["id"]: g for g in map(json.loads, open(D + "gold.jsonl", encoding="utf-8"))}
    return rows, gold


def db_ids():
    out = set()
    for f in sorted(glob.glob("raw_data_queue/processed/crawled_papers*.jsonl")) + ["raw_data_queue/crawled_papers.jsonl"]:
        for l in open(f, encoding="utf-8", errors="replace"):
            m = re.search(r'"paper_id":\s*"(\d{4}\.\d{4,5})', l)
            if m:
                out.add(m.group(1))
    return out


def body(answer):
    return answer.split("📎")[0]


def auto(label):
    rows, gold = load(label)
    db = db_ids()
    tot = in_db = in_ctx = 0
    unused, lens, gold_hit, gold_n, nu_ok = [], [], 0, 0, []
    none = ext = 0
    for i, g in gold.items():
        r = rows.get(i)
        if not r:
            continue
        a = r.get("answer") or ""
        b = body(a)
        cites = [norm(x) for x in CITE.findall(b)]
        ctx = {norm(x) for x in r.get("doc_ids") or []}
        tot += len(cites)
        in_db += sum(c in db for c in cites)
        in_ctx += sum(c in ctx for c in cites)
        unused.append(len(ctx - set(cites)))
        lens.append(len(re.sub(r"<[^>]+>", "", b)))
        gp = {norm(p) for p in g["relevant_papers"]}
        if gp and g["stratum"] != "MU":
            gold_n += 1
            gold_hit += bool(gp & set(cites))
        if g["stratum"] == "NU":
            nu_ok.append((i, [n for n in g.get("numbers", []) if re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", b)]))
        none += any(x.get("stage") == "judge" and x.get("pick") == "없음" for x in r.get("trace") or [])
        ext += "📎" in a
    print(f"인용 {tot}개: DB 에 있음 {in_db} · 이번 컨텍스트에 있음 {in_ctx}")
    print(f"정답 인용(정답 있는 문항, MU 제외) {gold_hit}/{gold_n}")
    print(f"안 쓴 컨텍스트 문서: 합 {sum(unused)} · 문항 중앙 {statistics.median(unused)} · 분포 {collections.Counter(unused).most_common()}")
    print(f"답 길이(본문) 중앙 {statistics.median(lens)}자 · 최소 {min(lens)} · 최대 {max(lens)}")
    print("NU 수치:", nu_ok)
    print(f"판정 '없음' {none} · 외부 검색 덧붙임 {ext}")
    keys = ["router", "query", "search", "select", "judge", "answer", "rewrite"]
    st = [dict(r.get("stages") or []) for r in rows.values()]
    print("시간 중앙", {k: round(statistics.median(s.get(k, 0) for s in st), 1) for k in keys}, "· 전체", round(statistics.median(r["elapsed"] for r in rows.values()), 1), "· 오류", sum(bool(r.get("error")) for r in rows.values()))
    print("경로", collections.Counter(r.get("route") for r in rows.values()).most_common(4))
    base = {r["id"]: r for r in map(json.loads, open(R + "ev30_base.jsonl", encoding="utf-8"))}
    same = sum(sorted(map(norm, rows[i].get("doc_ids") or [])) == sorted(map(norm, base[i].get("doc_ids") or [])) for i in rows if i in base)
    print(f"검색만 돌린 ev30_base 와 컨텍스트 논문이 같은 문항 {same}/{len(rows)}")


def packet(label):
    rows, gold = load(label)
    rng = random.Random(1110)
    sample = set(rng.sample(sorted(gold), 10))
    titles = {}
    for f in sorted(glob.glob("raw_data_queue/processed/crawled_papers*.jsonl")) + ["raw_data_queue/crawled_papers.jsonl"]:
        for l in open(f, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(l)
            except Exception:
                continue
            m = re.match(r"(\d{4}\.\d{4,5})", str(d.get("paper_id") or ""))
            if m and m.group(1) not in titles:
                titles[m.group(1)] = (d.get("title") or "")[:90]
    with open(D + "label_packet_answer.md", "w", encoding="utf-8") as w:
        w.write("# 답 단계 라벨 묶음 (README §6)\n\n표본 10(근거 대조): " + " ".join(sorted(sample)) + "\n\n")
        for i, g in gold.items():
            r = rows.get(i)
            if not r:
                continue
            a = re.sub(r"<[^>]+>", "", r.get("answer") or "")
            w.write(f"## {i} · {g['stratum']}{' · en' if g['lang'] == 'en' else ''}\n- 질문: {r.get('question') or ''}\n- 요소: {g['elements']}\n")
            if g.get("absent_paper"):
                w.write(f"- DB 에 없는 원 논문: {g['absent_paper']}\n")
            w.write("- 컨텍스트: " + " · ".join(f"{norm(x)} {titles.get(norm(x), '')[:60]}" for x in r.get("doc_ids") or []) + "\n")
            w.write("- 답:\n\n" + a.strip() + "\n\n")
            if i in sample:
                blocks = (r.get("numbered_context") or "").split("\n\n---\n\n")
                w.write("- 인용 블록(근거 대조용):\n\n")
                for b in blocks:
                    m = re.search(r"\[(\d{4}\.\d{4,5})", b)
                    if m and m.group(1) in a:
                        w.write("  > " + re.sub(r"\s+", " ", b) + "\n\n")
    print("묶음 씀 · 표본", sorted(sample))


def labels(label):
    lab = [l.rstrip("\n").split("\t") for l in open(D + "labels_answer.tsv", encoding="utf-8") if l.strip() and not l.startswith("#")]
    el = collections.Counter()
    d = f = ms = 0
    unsup = []
    by_type = collections.defaultdict(collections.Counter)
    for row in lab:
        i, typ, elements, dflag, fflag, msflag, uns = row[:7]
        for x in elements.split(","):
            x = x.strip()
            if x:
                el[x] += 1
                by_type[typ][x] += 1
        d += dflag == "Y"
        f += fflag == "Y"
        ms += msflag == "O"
        if uns.strip() not in ("", "-"):
            unsup.append((i, uns))
    tot = sum(el.values())
    print(f"요소 {tot}개: O {el['O']} ({el['O'] / max(1, tot):.0%}) · △ {el['△']} · X {el['X']}")
    for t, c in sorted(by_type.items()):
        s = sum(c.values())
        print(f"  {t}: O {c['O']}/{s} · △ {c['△']} · X {c['X']}")
    sd = sum("strictD=Y" in " ".join(row[7:]) for row in lab)
    sn = sum("strictD=" in " ".join(row[7:]) for row in lab)
    print(f"결론 문제(D, README §6.1 좁힌 정의) {d}/{len(lab)} · 사전 등록 정의 strictD {sd}/{sn} · 빈약(F) {f}/{len(lab)} · MS '모름' 잘함 {ms}/4")
    print(f"근거 없는 주장(표본 {len(unsup)}): 합 {sum(int(u) for _, u in unsup)} · 0 인 답 {sum(u == '0' for _, u in unsup)}", unsup)


if __name__ == "__main__":
    {"auto": auto, "packet": packet, "labels": labels}[sys.argv[2]](sys.argv[1])
