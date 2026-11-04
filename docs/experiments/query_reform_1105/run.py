"""query_reform_1105 dev: 거르기 뒤 빈 칸을 찾은 문서로 검색어를 다시 써 채운다 (README §2).

  .venv/bin/python docs/experiments/query_reform_1105/run.py tune    # 점검 전용 세트로 새 검색어만 본다 (측정에 안 씀)
  .venv/bin/python docs/experiments/query_reform_1105/run.py run     # 발동 70문항까지 → results/qr_dev.jsonl (이어 하기)
  .venv/bin/python docs/experiments/query_reform_1105/run.py status  # 진행 · 시간만 — 추가 문서는 보여 주지 않는다
  .venv/bin/python docs/experiments/query_reform_1105/run.py packet  # 바뀐 문항의 대조 문서 + 추가 문서를 섞어 → label_packet.md
  .venv/bin/python docs/experiments/query_reform_1105/run.py score   # labels.tsv (문항\t논문\t등급) 로 채점
"""
import json, math, os, random, re, statistics, sys, time
sys.path.insert(0, ".")

E = "docs/experiments/"
D = E + "query_reform_1105/"
OUT = E + "e2e_ko_1008/results/qr_dev.jsonl"
OLD_LABELS = E + "filter_input_1104/labels.tsv"  # 같은 등급 규칙 · 조건 가림
TARGET = 70
SETS = (
    ("real40", "real_eval_1013/questions.tsv"),
    ("real2", "real_eval2_1015/questions.tsv"),
    ("H", "corpus_seed_1020/heldout_questions.tsv"),
    ("D", "corpus_seed_1020/discovery_questions.tsv"),
    ("U", "user_suite_1027/questions.tsv"),
    ("HU", "topic_split2_1104/heldout.tsv"),
    ("HT", "topic_split_1103/heldout_topics.tsv"),
    ("JN", "judge_none_1103/questions.tsv"),
    ("SO", "survey_gate_1030/old_questions.tsv"),
    ("SN", "survey_gate_1030/new_questions.tsv"),
    ("ER", "corpus_er_1029/questions.tsv"),
    ("LE", "corpus_llmeval_1030/questions.tsv"),
    ("QG", "query_glossary_1029/g_questions.tsv"),
    ("OG", "open_gate_1103/stage1_questions.tsv"),
    ("HS", "topic_split2_1104/heldout_single.tsv"),
    ("QC", "qcond_1025/questions.tsv"),
)
TUNE = (("V3", "external_search_v3_1020/new_questions.tsv"), ("V2Q", "external_search_v2_1020/new_questions.tsv"))
GOLD = {"real40": "real_eval_1013/gold.jsonl", "real2": "real_eval2_1015/gold.jsonl"}  # 다른 세트의 정답 파일은 비어 있다
DEPTH = ("자세히", "더", "길게", "상세하게", "구체적으로")  # direct_answer 의 depth_keywords
PID = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]*)")


def tsv(path):
    for line in open(E + path, encoding="utf-8"):
        cols = line.rstrip("\n").split("\t")
        if line.strip() and not line.startswith("#") and len(cols) >= 2:
            yield cols[0], cols[1].strip()


def questions(sets, skip=()):
    """일반 경로(목록 · 단일 · 비교 · 수치 아님) · held-out 아님 · 같은 질문은 처음 나온 세트로 한 번만."""
    from core.graph import agent_nodes as N
    from core.llm.presence_judge import gate_types

    held = {t for f in ("foundation_1031/heldout.tsv", "foundation_1031/heldout_followup.tsv") for _, t in tsv(f)}
    out, seen = [], set(skip)
    for name, path in sets:
        for qid, text in tsv(path):
            if text in held or text in seen:
                continue
            single = N._prefer_single_hit_rag_context(text, wants_depth=any(w in text for w in DEPTH))
            if single or N.list_mode_active(text, prefer_single_hit=single) or {"cmp", "num"} & set(gate_types(text)):
                continue
            seen.add(text)
            out.append((f"{name}:{qid}", text))
    return out


def ids(ctx):
    from core.llm.citation_fix import RAG_HIT_SEP

    got = [PID.search(b) for b in (ctx or "").split(RAG_HIT_SEP) if b.strip()]
    return [m.group(1) for m in got if m]


def docs_of(ctx):
    from core.llm.citation_fix import RAG_HIT_SEP

    out = {}
    for b in (ctx or "").split(RAG_HIT_SEP):
        m = PID.search(b)
        if m:
            abstract = b.split("[초록] ", 1)[1].split("\n\n", 1)[0] if "[초록] " in b else b[m.end():]
            out.setdefault(m.group(1), {"title": m.group(2).strip(), "abstract": re.sub(r"\s+", " ", abstract).strip()[:1500]})
    return out


def _tools():
    import core.config.agent_config as cfg  # .env
    from core.graph import agent_nodes as N
    from core.llm import relevance_filter as RF
    from core.llm.query_reform import fill_slots
    from core.rag.agent_chroma_rag import get_chroma_rag_tool

    return cfg, N, RF, fill_slots, get_chroma_rag_tool()


def first_pass(q, cfg, N, RF, rag):
    t0 = time.time()
    en = N._extract_english_rag_query(q, session_context="")
    wd = any(x in q for x in DEPTH)
    pool = rag.search(en, top_k=15, session_context="", wants_depth=wd, name_query=q)
    t1 = time.time()
    kept, status = RF.filter_relevant(q, pool, cfg.RAG_ANSWER_MODEL)
    return en, wd, pool, kept, status, round(t1 - t0, 2), round(time.time() - t1, 2)


def tune():
    cfg, N, RF, fill_slots, rag = _tools()
    for qid, q in questions(TUNE):
        en, wd, pool, kept, status, _, _ = first_pass(q, cfg, N, RF, rag)
        filled, info = fill_slots(q, en, pool, kept, model=cfg.RAG_ANSWER_MODEL,
                                  search=lambda s: rag.search(s, top_k=15, session_context="", wants_depth=wd))
        print(f"\n{qid} {q}\n  첫 검색어 {en}\n  거르기 {status}")
        if info.get("on"):
            docs = docs_of(filled)
            print(f"  새 검색어 {info['query']}\n  새 문서 {info['new']} · 거르기 {info['filter']} · 시간 {info['laps']}")
            print("  찾은 문서", [docs[p]["title"][:60] for p in ids(kept)])
            print("  더한 문서", [docs[p]["title"][:60] for p in info["added"]])


def run():
    cfg, N, RF, fill_slots, rag = _tools()
    rows_done = list(map(json.loads, open(OUT, encoding="utf-8"))) if os.path.exists(OUT) else []
    done = {x["id"] for x in rows_done}
    fired = sum(x["reform"].get("on", False) for x in rows_done)
    qs = questions(SETS, skip={t for _, p in TUNE for _, t in tsv(p)})  # 프롬프트를 고치며 본 질문은 뺀다
    print("문항", len(qs), "· 이미", len(done), "· 발동", fired, flush=True)
    with open(OUT, "a", encoding="utf-8") as w:
        for i, (qid, q) in enumerate(qs):
            if fired >= TARGET:
                break
            if qid in done:
                continue
            t0 = time.time()
            en, wd, pool, kept, status, search_s, filter_s = first_pass(q, cfg, N, RF, rag)

            def fill():
                return fill_slots(q, en, pool, kept, model=cfg.RAG_ANSWER_MODEL,
                                  search=lambda s: rag.search(s, top_k=15, session_context="", wants_depth=wd))

            filled, info = fill()
            row = {"id": qid, "question": q, "query": en, "status": status, "search_s": search_s, "filter_s": filter_s,
                   "pool": ids(pool), "kept": ids(kept), "final0": ids(N._rag_context_top_n_hits(kept, n=5)),
                   "final1": ids(N._rag_context_top_n_hits(filled, n=5)), "reform": info}
            if info.get("on"):
                fired += 1
                row["docs"] = docs_of(filled)
                if fired % 4 == 1:
                    row["rep"] = fill()[1]
            w.write(json.dumps(row, ensure_ascii=False) + "\n")
            w.flush()
            print(i + 1, "/", len(qs), qid, f"발동 {fired}", f"{time.time() - t0:.1f}s", flush=True)
    print("끝", flush=True)


def rows():
    return list(map(json.loads, open(OUT, encoding="utf-8")))


def status():
    r = rows()
    on = [x for x in r if x["reform"].get("on")]
    print("끝난 문항", len(r), "· 발동", len(on), "· 첫 검색 중앙", statistics.median(x["search_s"] for x in r), "· 거르기 중앙", statistics.median(x["filter_s"] for x in r))
    if on:
        print("추가 시간 중앙", statistics.median(sum(x["reform"]["laps"].values()) for x in on))


def changed(x):
    return [p for p in x["final1"] if p not in x["final0"]]


def labels():
    lab = {}
    for path in (OLD_LABELS, D + "labels.tsv"):
        if os.path.exists(path):
            for l in open(path, encoding="utf-8"):
                if l.strip() and not l.startswith("#"):
                    q, p, v = l.rstrip("\n").split("\t")[:3]
                    lab[(q, p)] = int(v)
    return lab


def packet():
    """바뀐 문항의 대조 문서와 추가 문서를 어느 쪽인지 적지 않고 섞는다. 이전 라운드에서 단 문서는 뺀다."""
    rnd = random.Random(1105)
    lab = labels()
    r = [x for x in rows() if changed(x)]
    rnd.shuffle(r)
    lines, n = [], 0
    for x in r:
        pids = sorted(p for p in set(x["final0"]) | set(x["final1"]) if (x["id"], p) not in lab)
        if not pids:
            continue
        rnd.shuffle(pids)
        lines.append(f"## {x['id']}\n\n**질문** {x['question']}\n")
        lines += [f"- `{p}` **{x['docs'][p]['title']}** — {x['docs'][p]['abstract']}" for p in pids]
        lines.append("")
        n += len(pids)
    open(D + "label_packet.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("바뀐 문항", len(r), "· 라벨할 문서", n, "· 글자", sum(map(len, lines)))


def sign_p(a, b):
    n, k = a + b, min(a, b)
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def score():
    lab = labels()
    r = rows()
    on = [x for x in r if x["reform"].get("on")]
    ch = [x for x in on if changed(x)]
    miss = [(x["id"], p) for x in ch for p in set(x["final0"]) | set(x["final1"]) if (x["id"], p) not in lab]
    assert not miss, f"라벨 없음 {len(miss)}: {miss[:5]}"
    win = lose = gained = 0
    per_set = {}
    added = {0: 0, 1: 0, 2: 0}
    base = {0: 0, 1: 0, 2: 0}
    for x in ch:
        got = [lab[(x["id"], p)] for p in changed(x)]
        for v in got:
            added[v] += 1
        for p in x["final0"]:
            base[lab[(x["id"], p)]] += 1
        g, b = got.count(2), got.count(0)
        s = per_set.setdefault(x["id"].split(":")[0], [0, 0, 0])
        win += g > b
        lose += g < b
        gained += g > 0
        s[0 if g > b else 1 if g < b else 2] += 1
    n0, n1 = sum(base.values()), sum(base.values()) + sum(added.values())
    r0, r1 = base[2] / max(1, n0), (base[2] + added[2]) / max(1, n1)
    bad = sum(x["reform"]["filter"] in ("호출 실패", "못 읽음") for x in on)
    noq = sum(x["reform"]["filter"] == "검색어 없음" for x in on)
    extra = [sum(x["reform"]["laps"].values()) for x in on]
    reps = [x for x in on if "rep" in x]
    rep_diff = sum(x["rep"]["added"] != x["reform"]["added"] for x in reps)
    print(f"문항 {len(r)} · 발동 {len(on)} · 바뀜 {len(ch)} · 추가 문서 {sum(added.values())} · 평균 최종 편수 {sum(len(x['final0']) for x in r) / len(r):.2f} → {sum(len(x['final1']) for x in r) / len(r):.2f}")
    print(f"주: 얻음 > 무관 {win} : 얻음 < 무관 {lose} (동점 {len(ch) - win - lose}) · p {sign_p(win, lose):.4f}")
    print(f"크기: '2' 를 1편 이상 얻은 문항 {gained} / 발동 {len(on)} ({gained / max(1, len(on)):.1%})")
    print(f"보호 1: 바뀐 문항 최종 '2' 비율 {r0:.1%} → {r1:.1%} (대조 등급 {base} · 추가 등급 {added})")
    print(f"보호 2: 추가 문서 중 '0' {added[0]}/{sum(added.values())} ({added[0] / max(1, sum(added.values())):.1%})")
    print(f"보호 3: 추가 시간 중앙 {statistics.median(extra) if extra else 0:.1f}s · 단계 중앙 " + str({k: statistics.median(x['reform']['laps'][k] for x in on if k in x['reform']['laps']) for k in ('rewrite', 'search', 'filter')}))
    print(f"보호 4: 검색어 못 씀 {noq} · 못 읽음/호출 실패 {bad} / 발동 {len(on)}")
    print(f"신뢰: 재실행 추가 문서 달라짐 {rep_diff}/{len(reps)}")
    print(f"세트별 이김:짐:동점 {per_set}")
    gold = {f"{n}:{row['id']}": {re.sub(r'v\d+$', '', p) for p in row['relevant_papers']}
            for n, g in GOLD.items() for row in map(json.loads, open(E + g, encoding="utf-8")) if row.get("relevant_papers")}
    gs = [x for x in r if x["id"] in gold]
    print(f"참고: 정답 있는 문항 {len(gs)} · 대조 {sum(bool(gold[x['id']] & set(x['final0'])) for x in gs)} · 처리 {sum(bool(gold[x['id']] & set(x['final1'])) for x in gs)}")


if __name__ == "__main__":
    {"tune": tune, "run": run, "status": status, "packet": packet, "score": score}[sys.argv[1]]()
