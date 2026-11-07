"""topic_filter_1104 dev: 나뉜 질문의 거르기를 주제별로 — 검색 풀을 모아 라벨을 먼저 달고, 거르기는 오프라인으로 비교한다 (README).

  .venv/bin/python docs/experiments/topic_filter_1104/pool.py pool    # 문항 · 주제 줄마다 검색 상위 5 → pool_hu.jsonl (이어 하기)
  .venv/bin/python docs/experiments/topic_filter_1104/pool.py packet  # 라벨 없는 풀 문서 + 라벨 있는 대조 문서 섞어 → label_packet_pool.md
  .venv/bin/python docs/experiments/topic_filter_1104/pool.py filter  # 주제 줄마다 거르기 호출(5편 · 3편) → filter_hu.jsonl (이어 하기)
  .venv/bin/python docs/experiments/topic_filter_1104/pool.py score   # 판별 채점

다른 모델: RAG_ANSWER_MODEL=<모델> 을 앞에 붙이면 filter · score 가 filter_hu.<모델>.jsonl 을 쓴다.
"""
import json, math, os, random, re, statistics, sys, time
sys.path.insert(0, ".")
sys.path.insert(0, "docs/experiments/topic_split2_1104")

D = "docs/experiments/topic_filter_1104/"
S2 = "docs/experiments/topic_split2_1104/"
PID = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]*)")


def model_sfx():
    """저장된 filter_hu.jsonl 은 yunsur_v13 결과다. 다른 모델은 파일을 따로 써 이어 하기 · 채점이 섞이지 않게 한다 (newmac_1105 §6.2)."""
    import core.config.agent_config as cfg  # .env
    return "" if cfg.RAG_ANSWER_MODEL == "yunsur_v13" else "." + re.sub(r"[^A-Za-z0-9._-]+", "_", cfg.RAG_ANSWER_MODEL)


def split_lines():
    import score as S
    t = S.rows("ts1_hu")
    return [(q, next((x.get("topics") for x in t[q].get("trace", []) if x.get("stage") == "search"), None) or []) for q in sorted(t)]


def head(block):
    m = PID.search(block)
    if not m:
        return None, "", ""
    rest = re.sub(r"\s+", " ", block[m.end():]).strip()
    return m.group(1), m.group(2).strip(), rest


def pool():
    import core.config.agent_config as cfg  # .env
    from core.graph import agent_nodes as N
    from core.rag.agent_chroma_rag import get_chroma_rag_tool
    rag = get_chroma_rag_tool()
    out = D + "pool_hu.jsonl"
    done = {(json.loads(l)["id"], json.loads(l)["k"]) for l in open(out, encoding="utf-8")} if os.path.exists(out) else set()
    with open(out, "a", encoding="utf-8") as w:
        for q, lines in split_lines():
            for k, line in enumerate(lines):
                if (q, k) in done:
                    continue
                t0 = time.time()
                r = rag.search(line, top_k=15, session_context="", wants_depth=False, name_query=line)
                blocks = [b.strip() for b in r.split(N._RAG_HIT_SEP) if b.strip()][:5]
                w.write(json.dumps({"id": q, "k": k, "line": line, "s": round(time.time() - t0, 1), "blocks": [b[:1800] for b in blocks]}, ensure_ascii=False) + "\n")
                w.flush()
                print(q, k, len(blocks), f"{time.time() - t0:.1f}s", line[:70], flush=True)
    print("풀 끝")


def rows():
    return list(map(json.loads, open(D + "pool_hu.jsonl", encoding="utf-8")))


def old_labels():
    lab = {}
    for l in open(S2 + "labels_hu.tsv", encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            q, p, v = l.rstrip("\n").split("\t")[:3]
            lab[(q, p)] = v.strip()
    return lab


def packet():
    import score as S
    c = S.rows("ts0_hu")
    gold = {g["id"]: g for g in map(json.loads, open(S2 + "heldout_gold.jsonl", encoding="utf-8"))}
    lab = old_labels()
    pool_docs = {}
    for r in rows():
        for b in r["blocks"]:
            p, title, rest = head(b)
            if p:
                pool_docs.setdefault(r["id"], {})[p] = (title, rest)
    rnd = random.Random(1104)
    out, new_n, decoy_n = [], 0, 0
    for q in sorted(pool_docs):
        new = {p: v for p, v in pool_docs[q].items() if (q, p) not in lab}
        # 라벨 일치 확인용: 이미 단 대조 문서 2편까지 섞는다 (옛 라벨은 보지 않고 다시 단다)
        known = [p for p in S.docs(c[q]) if (q, p) in lab and p not in new]
        rnd.shuffle(known)
        decoys = {p: S.docs(c[q])[p] for p in known[:2]}
        all_docs = {**new, **decoys}
        pids = sorted(all_docs)
        rnd.shuffle(pids)
        new_n += len(new)
        decoy_n += len(decoys)
        out.append(f"## {q}\n\n**하위 주제** " + " · ".join(f"{k}. {x}" for k, x in enumerate(gold[q]["topics"], 1)) + "\n")
        out += [f"- `{p}` **{all_docs[p][0]}** — {all_docs[p][1][:320]}" for p in pids]
        out.append("")
    open(D + "label_packet_pool.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("문항", len(pool_docs), "· 새 문서", new_n, "· 섞은 대조 문서", decoy_n, "· 글자", sum(map(len, out)))


def filter_all():
    import core.config.agent_config as cfg  # .env
    from core.llm import relevance_filter as RF
    from core.llm.citation_fix import RAG_HIT_SEP
    out = D + f"filter_hu{model_sfx()}.jsonl"
    done = {(json.loads(l)["id"], json.loads(l)["k"], json.loads(l)["n"]) for l in open(out, encoding="utf-8")} if os.path.exists(out) else set()
    with open(out, "a", encoding="utf-8") as w:
        for r in rows():
            for n in (5, 3):
                if (r["id"], r["k"], n) in done:
                    continue
                t0 = time.time()
                ctx, st = RF.filter_relevant(r["line"], RAG_HIT_SEP.join(r["blocks"][:n]), cfg.RAG_ANSWER_MODEL)
                kept = [head(b)[0] for b in ctx.split(RAG_HIT_SEP) if b.strip()]
                w.write(json.dumps({"id": r["id"], "k": r["k"], "n": n, "status": st, "kept": kept, "s": round(time.time() - t0, 1)}, ensure_ascii=False) + "\n")
                w.flush()
    print("거르기 끝")


def sign_p(a, b):
    n, k = a + b, min(a, b)
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def score():
    import score as S
    c = S.rows("ts0_hu")
    t = S.rows("ts1_hu")
    gold = {g["id"]: g for g in map(json.loads, open(S2 + "heldout_gold.jsonl", encoding="utf-8"))}
    lab = {}
    for f in (S2 + "labels_hu.tsv", D + "labels_pool.tsv"):
        for l in open(f, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                q, p, v = l.rstrip("\n").split("\t")[:3]
                if f.endswith("labels_pool.tsv") and (q, p) in lab:
                    continue  # 섞은 대조 문서는 옛 라벨 유지(일치만 따로 잰다)
                lab[(q, p)] = set() if v.strip() == "-" else {int(x) for x in re.findall(r"\d+", v)}
    # 라벨 일치
    old = old_labels()
    pairs = []
    for l in open(D + "labels_pool.tsv", encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            q, p, v = l.rstrip("\n").split("\t")[:3]
            if (q, p) in old:
                pairs.append((q, p, old[(q, p)], v.strip()))
    same = sum(sorted(re.findall(r"\d+", a)) == sorted(re.findall(r"\d+", b)) for _, _, a, b in pairs)
    print(f"섞은 대조 문서 라벨 일치 {same}/{len(pairs)} · 다름: {[x for x in pairs if sorted(re.findall(chr(92) + 'd+', x[2])) != sorted(re.findall(chr(92) + 'd+', x[3]))][:12]}")

    pool_rows = rows()
    by_q = {}
    for r in pool_rows:
        by_q.setdefault(r["id"], []).append(r)
    fil = {}
    path = D + f"filter_hu{model_sfx()}.jsonl"
    print("거르기 결과 파일:", path, "· 있음" if os.path.exists(path) else "· 없음")
    if os.path.exists(path):
        fil = {(x["id"], x["k"], x["n"]): x for x in map(json.loads, open(path, encoding="utf-8"))}

    def topic_docs(r, v):
        ids = [head(b)[0] for b in r["blocks"]]
        if v == "V0":
            return ids[:3]
        if v == "O":  # 완벽한 거르기(라벨로 거름) — 거르기를 아무리 고쳐도 넘지 못하는 상한
            return [p for p in ids if lab[(r["id"], p)]][:3]
        n = 5 if v in ("V1", "V2") else 3
        f = fil[(r["id"], r["k"], n)]
        if v == "V2" and f["status"] == "없음":
            return []
        return f["kept"][:3]

    def final(q, v):
        if v == "A":
            return list(S.docs(c[q]))
        if v == "B":
            return list(S.docs(t[q]))
        if q not in by_q:
            return list(S.docs(c[q]))
        rows_ = [topic_docs(r, v) for r in sorted(by_q[q], key=lambda x: x["k"])]
        order = []
        for rank in range(3):
            for row in rows_:
                if rank < len(row) and row[rank] not in order:
                    order.append(row[rank])
        return order[:10] or list(S.docs(c[q]))

    def stats(v):
        cov, off, n = {}, 0, 0
        for q in sorted(c):
            d = final(q, v)
            ls = [lab[(q, p)] for p in d]
            cov[q] = len(set().union(*ls)) if ls else 0
            off += sum(not x for x in ls)
            n += len(d)
        return cov, off, n

    base, off0, n0 = stats("A")
    print(f"A 대조: 덮음 {sum(base.values())}/121 · 다 덮음 {sum(base[q] == len(gold[q]['topics']) for q in base)} · 주제 밖 {off0}/{n0} = {off0 / n0:.1%}")
    # 풀 전체를 다 남겼을 때의 상한
    ub = {q: len(set().union(*[lab[(q, head(b)[0])] for r in by_q[q] for b in r["blocks"]])) if q in by_q else base[q] for q in c}
    print(f"풀 상한(상위 5 전부): 덮음 {sum(ub.values())}/121")
    for v in ["B", "V0", "O"] + (["V1", "V2", "V3"] if fil else []):
        cov, off, n = stats(v)
        win = sum(cov[q] > base[q] for q in c)
        lose = sum(cov[q] < base[q] for q in c)
        shrink = sum(len(final(q, v)) < 3 <= len(final(q, "A")) for q in c)
        full = sum(cov[q] == len(gold[q]["topics"]) for q in c)
        print(f"{v}: 많음 {win} : 적음 {lose} (동점 {len(c) - win - lose}) · p {sign_p(win, lose):.4f} · 덮음 {sum(cov.values())}/121 · 다 덮음 {full}/40"
              f" · 주제 밖 {off}/{n} = {off / n:.1%} ({off / n - off0 / n0:+.1%}p) · 평균 편수 {n / len(c):.1f} · 3편 미만으로 준 문항 {shrink}")
    if fil:
        # 9B 주제별 거르기 자체의 성적: 상위 5 안에서 주제 안 문서를 얼마나 남기고 주제 밖 문서를 얼마나 빼나
        kept_on = kept_off = drop_on = drop_off = 0
        for r in pool_rows:
            kept = set(fil[(r["id"], r["k"], 5)]["kept"])
            for b in r["blocks"]:
                p = head(b)[0]
                on = bool(lab[(r["id"], p)])
                kept_on += on and p in kept
                kept_off += (not on) and p in kept
                drop_on += on and p not in kept
                drop_off += (not on) and p not in kept
        print(f"5편 거르기: 주제 안 남김 {kept_on} · 뺌 {drop_on} / 주제 밖 남김 {kept_off} · 뺌 {drop_off}"
              f" · 정밀도 {kept_on / max(1, kept_on + kept_off):.1%} · 재현율 {kept_on / max(1, kept_on + drop_on):.1%}"
              f" · 풀의 주제 안 비율 {(kept_on + drop_on) / max(1, kept_on + kept_off + drop_on + drop_off):.1%}")
        st = {}
        for x in fil.values():
            if x["n"] == 5:
                st[x["status"] if not re.match(r"\d", x["status"]) else "걸렀음"] = st.get(x["status"] if not re.match(r"\d", x["status"]) else "걸렀음", 0) + 1
        print("5편 거르기 상태:", st, "· 호출 시간 중앙", statistics.median(x["s"] for x in fil.values() if x["n"] == 5))


if __name__ == "__main__":
    {"pool": pool, "packet": packet, "filter": filter_all, "score": score}[sys.argv[1]]()
