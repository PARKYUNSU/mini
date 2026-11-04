"""filter_input_1104 dev: 거르기 입력을 앞 600자 → 요지 문장으로 (README §2).

  .venv/bin/python docs/experiments/filter_input_1104/run.py run     # 문항마다 검색 1회 + 거르기 2~3회 → results/fi_dev.jsonl (이어 하기)
  .venv/bin/python docs/experiments/filter_input_1104/run.py status  # 진행만 — 어느 문서가 갈렸는지는 보여 주지 않는다
  .venv/bin/python docs/experiments/filter_input_1104/run.py packet  # 갈린 문서를 조건 없이 섞어 → label_packet.md
  .venv/bin/python docs/experiments/filter_input_1104/run.py score   # labels.tsv (문항\t논문\t등급) 로 채점
"""
import json, math, os, random, re, statistics, sys, time
sys.path.insert(0, ".")

E = "docs/experiments/"
D = E + "filter_input_1104/"
OUT = E + "e2e_ko_1008/results/fi_dev.jsonl"
SETS = {
    "real40": ("real_eval_1013/questions.tsv", "real_eval_1013/gold.jsonl"),
    "real2": ("real_eval2_1015/questions.tsv", "real_eval2_1015/gold.jsonl"),
    "H": ("corpus_seed_1020/heldout_questions.tsv", "corpus_seed_1020/heldout_gold.jsonl"),
    "D": ("corpus_seed_1020/discovery_questions.tsv", "corpus_seed_1020/discovery_gold.jsonl"),
    "U": ("user_suite_1027/questions.tsv", "user_suite_1027/gold.jsonl"),
    "HU": ("topic_split2_1104/heldout.tsv", None),
    "HT": ("topic_split_1103/heldout_topics.tsv", None),
}
DEPTH = ("자세히", "더", "길게", "상세하게", "구체적으로")  # direct_answer 의 depth_keywords
PID = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]*)")


def plain_questions():
    """일반 경로(목록 · 단일 · 비교 아님) 문항 [(세트:문항, 질문)]."""
    from core.graph import agent_nodes as N
    from core.llm.presence_judge import gate_types

    out = []
    for name, (q, _) in SETS.items():
        for line in open(E + q, encoding="utf-8"):
            if not line.strip() or line.startswith("#"):
                continue
            cols = line.rstrip("\n").split("\t")
            text = cols[1]
            single = N._prefer_single_hit_rag_context(text, wants_depth=any(w in text for w in DEPTH))
            if single or N.list_mode_active(text, prefer_single_hit=single) or "cmp" in gate_types(text):
                continue
            out.append((f"{name}:{cols[0]}", text))
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


def run():
    import core.config.agent_config as cfg  # .env
    from core.graph import agent_nodes as N
    from core.llm import relevance_filter as RF
    from core.rag.agent_chroma_rag import get_chroma_rag_tool

    rag = get_chroma_rag_tool()
    done = {json.loads(l)["id"] for l in open(OUT, encoding="utf-8")} if os.path.exists(OUT) else set()
    qs = plain_questions()
    print("문항", len(qs), "· 이미", len(done), flush=True)

    def one(arm, q, ctx):
        os.environ["RAG_FILTER_FINDINGS"] = "1" if arm == "1" else "0"
        t0 = time.time()
        filtered, status = RF.filter_relevant(q, ctx, cfg.RAG_ANSWER_MODEL)
        s = round(time.time() - t0, 2)
        final = N._rag_context_top_n_hits(filtered, n=5)
        return {"status": status, "s": s, "kept": ids(filtered), "final": ids(final)}

    with open(OUT, "a", encoding="utf-8") as w:
        for i, (qid, q) in enumerate(qs):
            if qid in done:
                continue
            t0 = time.time()
            en = N._extract_english_rag_query(q, session_context="")
            ctx = rag.search(en, top_k=15, session_context="", wants_depth=any(x in q for x in DEPTH), name_query=q)
            search_s = round(time.time() - t0, 2)
            arms = {a: one(a, q, ctx) for a in (("0", "1") if i % 2 == 0 else ("1", "0"))}
            if i % 4 == 0:
                arms["rep"] = one("0", q, ctx)
            w.write(json.dumps({"id": qid, "question": q, "query": en, "search_s": search_s, "arms": arms, "pool": ids(ctx), "docs": docs_of(ctx), "ctx": ctx}, ensure_ascii=False) + "\n")
            w.flush()
            print(i + 1, "/", len(qs), qid, f"{time.time() - t0:.1f}s", flush=True)
    print("끝", flush=True)


def rows():
    return list(map(json.loads, open(OUT, encoding="utf-8")))


def status():
    r = rows()
    print("끝난 문항", len(r), "· 검색 중앙", statistics.median(x["search_s"] for x in r), "· 거르기 중앙", statistics.median(a["s"] for x in r for a in x["arms"].values()))


def diff_docs(x):
    return set(x["arms"]["0"]["final"]) ^ set(x["arms"]["1"]["final"])


def packet():
    rnd = random.Random(1104)
    r = rows()
    rnd.shuffle(r)
    lines, n = [], 0
    for x in r:
        pids = sorted(diff_docs(x))
        if not pids:
            continue
        rnd.shuffle(pids)
        lines.append(f"## {x['id']}\n\n**질문** {x['question']}\n")
        lines += [f"- `{p}` **{x['docs'][p]['title']}** — {x['docs'][p]['abstract']}" for p in pids]
        lines.append("")
        n += len(pids)
    open(D + "label_packet.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("갈린 문항", sum(bool(diff_docs(x)) for x in r), "/", len(r), "· 문서", n, "· 글자", sum(map(len, lines)))


def sign_p(a, b):
    n, k = a + b, min(a, b)
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def gold_map():
    out = {}
    for name, (_, g) in SETS.items():
        if g:
            for row in map(json.loads, open(E + g, encoding="utf-8")):
                if row.get("relevant_papers"):
                    out[f"{name}:{row['id']}"] = {re.sub(r"v\d+$", "", p) for p in row["relevant_papers"]}
    return out


def score():
    lab = {}
    for l in open(D + "labels.tsv", encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            q, p, v = l.rstrip("\n").split("\t")[:3]
            lab[(q, p)] = int(v)
    r = rows()
    miss = [(x["id"], p) for x in r for p in diff_docs(x) if (x["id"], p) not in lab]
    assert not miss, f"라벨 없음 {len(miss)}: {miss[:5]}"
    gold = gold_map()
    win = lose = 0
    zero = [0, 0]
    two_only = [0, 0]
    per_set = {}
    ok = [0, 0]
    ok_win = ok_lose = 0
    shrink = 0
    n_final = [0, 0]
    for x in r:
        f0, f1 = set(x["arms"]["0"]["final"]), set(x["arms"]["1"]["final"])
        d2 = sum(lab[(x["id"], p)] == 2 for p in f1 - f0) - sum(lab[(x["id"], p)] == 2 for p in f0 - f1)
        two_only[0] += sum(lab[(x["id"], p)] == 2 for p in f0 - f1)
        two_only[1] += sum(lab[(x["id"], p)] == 2 for p in f1 - f0)
        zero[0] += sum(lab[(x["id"], p)] == 0 for p in f0 - f1)
        zero[1] += sum(lab[(x["id"], p)] == 0 for p in f1 - f0)
        s = per_set.setdefault(x["id"].split(":")[0], [0, 0, 0])
        if d2 > 0:
            win += 1
            s[0] += 1
        elif d2 < 0:
            lose += 1
            s[1] += 1
        else:
            s[2] += 1
        if x["id"] in gold:
            a, b = bool(gold[x["id"]] & f0), bool(gold[x["id"]] & f1)
            ok[0] += a
            ok[1] += b
            ok_win += b and not a
            ok_lose += a and not b
        shrink += len(f0) >= 3 and len(f1) < 3
        n_final[0] += len(f0)
        n_final[1] += len(f1)
    st = [{}, {}]
    for x in r:
        for k, a in enumerate(("0", "1")):
            v = x["arms"][a]["status"]
            v = "걸렀음" if re.match(r"\d", v) else v
            st[k][v] = st[k].get(v, 0) + 1
    bad = [sum(s.get(k, 0) for k in ("못 읽음", "호출 실패")) for s in st]
    t = [statistics.median(x["arms"][a]["s"] for x in r) for a in ("0", "1")]
    keep = [statistics.median(len(x["arms"][a]["kept"]) for x in r) for a in ("0", "1")]
    reps = [x for x in r if "rep" in x["arms"]]
    rep_diff = sum(set(x["arms"]["rep"]["final"]) != set(x["arms"]["0"]["final"]) for x in reps)
    print(f"문항 {len(r)} · 갈린 문항 {sum(bool(diff_docs(x)) for x in r)} · 갈린 문서 {sum(len(diff_docs(x)) for x in r)}")
    print(f"주: 많음 {win} : 적음 {lose} (동점 {len(r) - win - lose}) · p {sign_p(win, lose):.4f} · 갈린 문서 중 '2' 대조만 {two_only[0]} · 처리만 {two_only[1]}")
    print(f"세트별 많음:적음:동점 {per_set}")
    print(f"보호 1: 갈린 문서 중 '0' 대조만 {zero[0]} · 처리만 {zero[1]} (처리 ≤ 대조 + 2)")
    print(f"보호 2: 정답 문항 {len(gold)} 중 대조 {ok[0]} · 처리 {ok[1]} · 얻음 {ok_win} · 잃음 {ok_lose}")
    print(f"보호 3: 3편 미만으로 준 문항 {shrink} · 평균 최종 편수 {n_final[0] / len(r):.2f} → {n_final[1] / len(r):.2f} · 거르기 뒤 남은 편수 중앙 {keep[0]} → {keep[1]}")
    print(f"보호 4: 못 읽음 · 호출 실패 {bad[0]} → {bad[1]} · 상태 대조 {st[0]} · 처리 {st[1]}")
    print(f"보호 5: 거르기 호출 중앙 {t[0]}s → {t[1]}s")
    print(f"신뢰: 대조 재실행 {rep_diff}/{len(reps)} 달라짐 ({rep_diff / max(1, len(reps)):.1%})")


if __name__ == "__main__":
    {"run": run, "status": status, "packet": packet, "score": score}[sys.argv[1]]()
