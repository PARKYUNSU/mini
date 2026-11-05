"""jeff_1105: System One API(jeff · Jev)로 거르기 · 판정 · 분기를 저장 입력에 다시 돌린다 (README).

  export SYS1_URL=http://127.0.0.1:8090 SYS1_KEY=devkey SYS1_LABEL=jeff
  .venv/bin/python docs/experiments/jeff_1105/run.py smoke
  .venv/bin/python docs/experiments/jeff_1105/run.py filter
  .venv/bin/python docs/experiments/jeff_1105/run.py judge K
  .venv/bin/python docs/experiments/jeff_1105/run.py judge E [labeled]
  .venv/bin/python docs/experiments/jeff_1105/run.py router
  .venv/bin/python docs/experiments/jeff_1105/run.py control   # 배관 점검(본 뒤 추가, 보고만) — README §7
  .venv/bin/python docs/experiments/jeff_1105/run.py score

결과는 results/<SYS1_LABEL>_<자리>.jsonl 에 이어 쓴다.
진짜 Jev 는 README §8: SYS1_URL=https://api.typesafe.ai SYS1_KEY_FILE=~/dev/jeff_1105/jev.key SYS1_LABEL=jev SYS1_MODEL=jev-1.14.0
로컬이 아닌 URL 에는 실사용 질문을 보내지 않는다.
"""
import ast, hashlib, json, os, re, sqlite3, statistics, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, ".")

D = "docs/experiments/jeff_1105/"
TF = "docs/experiments/topic_filter_1104/"
S2 = "docs/experiments/topic_split2_1104/"
OJ = "docs/experiments/open_judge_1103/"
R = "docs/experiments/e2e_ko_1008/results/"
SETS = {"ogb_s1": "docs/experiments/open_gate2_1103/heldout_open2.tsv",
        "og_s1": "docs/experiments/open_gate_1103/heldout_open.tsv",
        "jn_dev": "docs/experiments/judge_none_1103/questions.tsv"}
PID = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]*)")
BLK = re.compile(r"\[문서 (\d+)\]\n(.*?)(?=\n\[문서 \d+\]\n|\Z)", re.S)

# README §3 — 측정 전 고정.
INSTR = "Does this paper mainly address the topic of the request below? Request: {q}"
CRIT = {"true": "the paper's main subject is this topic, even if its methods or wording differ",
        "false": "it only shares some words or the broad field, and its main subject is a different problem"}
THR = 0.5
# 본 뒤 추가한 단순 문구(README §7, 힌트 전용 — 통과 판정에 쓰지 않는다). SYS1_TEMPLATE=v2 · SYS1_LABEL=jeff_v2
if os.environ.get("SYS1_TEMPLATE") == "v2":
    INSTR, CRIT = "Is this paper about: {q}?", None
ROUTE_INSTR = "What kind of request is this message to a research assistant bot?"
ROUTE_CRIT = {"paper_research": "asks about academic papers, research findings, or AI and machine learning concepts that should be answered from a paper database",
              "chat": "casual conversation or a general question that needs no papers",
              "tool": "asks for live data or a tool: weather, news, web search, stock prices, or listing what is stored in the database",
              "coding": "asks to write, run, or debug code"}

URL = os.environ.get("SYS1_URL", "http://127.0.0.1:8090").rstrip("/")
KEY = open(os.path.expanduser(os.environ["SYS1_KEY_FILE"])).read().strip() if os.environ.get("SYS1_KEY_FILE") else os.environ.get("SYS1_KEY", "devkey")
LABEL = os.environ.get("SYS1_LABEL", "jeff")
MODEL = os.environ.get("SYS1_MODEL", "jev-latest")
LOCAL = urllib.parse.urlparse(URL).hostname in ("127.0.0.1", "localhost")


def ask(state, questions):
    req = urllib.request.Request(URL + "/v1/systemone", headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
                                 data=json.dumps({"model": MODEL, "state": state, "questions": questions}, ensure_ascii=False).encode("utf-8"))
    t0 = time.time()
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                out = json.load(r)
            return out["answers"], round(time.time() - t0, 3), out["usage"]["input_tokens"]
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503, 529) or attempt == 7:
                sys.exit(f"HTTP {e.code}: {e.read()[:300]!r} — 멈춤(이어 하기 가능)")
            wait = float(e.headers.get("retry-after-ms") or 2000) / 1000
            print(f"HTTP {e.code} — {wait:.1f}초 대기", flush=True)
            time.sleep(wait)
            t0 = time.time()


def noul(state, q):
    question = {"type": "noul", "instructions": INSTR.format(q=q)}
    if CRIT:
        question["criteria"] = CRIT
    a, s, tok = ask(state, {"topic": question})
    return a["topic"]["noul"], s, tok


def mem_guard(k):
    """README §2 — 25건마다. 여유 12% 미만이면 기다리고, 스왑 6GB 초과면 멈춘다."""
    if k % 25 or not LOCAL:
        return
    for _ in range(20):
        free = int(re.search(r"free percentage: (\d+)%", subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout).group(1))
        swap = float(re.search(r"used = ([\d.]+)M", subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout).group(1))
        if swap > 6000:
            sys.exit(f"스왑 {swap:.0f}MB > 6GB — 멈춤(이어 하기 가능)")
        if free >= 12:
            return
        print(f"여유 메모리 {free}% — 60초 대기", flush=True)
        time.sleep(60)
    sys.exit("여유 메모리 부족이 20분 이어짐 — 멈춤(이어 하기 가능)")


def norm(t):
    return re.sub(r"\s+", "", t or "").lower()


_real = None


def is_real(q):
    """봇에 실제로 온 질문인가(브리지 DB 와 글자 비교)."""
    global _real
    if _real is None:
        c = sqlite3.connect("file:.bridge/agent_bridge.sqlite?mode=ro", uri=True)
        _real = {norm(t) for (t,) in c.execute("select user_text from bridge_jobs") if t and t.strip()}
    return norm(q) in _real


def blocked(it):
    """외부 전송 금지 — jn_dev 는 실사용 질문을 넣은 세트라 통째로 뺀다(judge_none_1103 README)."""
    return not LOCAL and (it["src"] == "jn_dev" or is_real(it["q"]))


def jsonl(p):
    return list(map(json.loads, open(p, encoding="utf-8"))) if os.path.exists(p) else []


def pid(block):
    m = PID.search(block)
    return m.group(1) if m else None


def out_path(name):
    return f"{D}results/{LABEL}_{name}.jsonl"


def smoke():
    print(noul("I was charged twice for my subscription. Please refund me.", "billing problems"))
    print(ask("The export button crashes in Safari.", {"severity": {"type": "score", "instructions": "How severe?", "criteria": ["cosmetic", "degraded", "blocking"]}}))


def run_filter():
    from core.llm.relevance_filter import _brief
    out = out_path("filter")
    done = {(x["id"], x["k"], x["p"]) for x in jsonl(out)}
    rows = jsonl(TF + "pool_hu.jsonl")
    n = 0
    with open(out, "a", encoding="utf-8") as w:
        for r in rows:
            for b in r["blocks"][:5]:
                p = pid(b)
                if (r["id"], r["k"], p) in done:
                    continue
                mem_guard(n)
                v, s, tok = noul(re.sub(r"^\[1\] ", "", _brief(1, b)), r["line"])
                w.write(json.dumps({"id": r["id"], "k": r["k"], "p": p, "noul": v, "s": s, "tok": tok}) + "\n")
                w.flush()
                n += 1
                if n % 50 == 0:
                    print(f"거르기 {n}", flush=True)
    print("거르기 끝", n)


def judge_items():
    labels = load_oj_labels()
    items = []
    q_by_set = {k: dict(l.rstrip("\n").split("\t")[:2] for l in open(v, encoding="utf-8") if l.strip() and not l.startswith("#")) for k, v in SETS.items()}
    rows = {k: {r["id"]: r for r in jsonl(R + k + ".jsonl")} for k in SETS}
    for x in jsonl(OJ + "oj_dev.jsonl"):
        r = rows[x["src"]][x["id"]]
        items.append({"id": x["id"], "src": x["src"], "stored": x["stored"], "q": q_by_set[x["src"]][x["id"]], "ctx": r["numbered_context"],
                      "en": " ".join(r.get("rag_queries") or []), "label": labels.get(x["id"])})
    return items


def run_judge(arm, labeled_only=False):
    out = out_path("judge_" + arm)
    done = {(x["id"], x["n"]) for x in jsonl(out)}
    n = 0
    with open(out, "a", encoding="utf-8") as w:
        for it in judge_items():
            if (labeled_only and not it["label"]) or blocked(it):
                continue
            q = it["q"] if arm == "K" or not it["en"] else it["en"]
            for no, block in BLK.findall(it["ctx"]):
                if (it["id"], int(no)) in done:
                    continue
                mem_guard(n)
                v, s, tok = noul(block, q)
                w.write(json.dumps({"id": it["id"], "src": it["src"], "n": int(no), "noul": v, "s": s, "tok": tok}) + "\n")
                w.flush()
                n += 1
                if n % 50 == 0:
                    print(f"판정 {arm} {n}", flush=True)
    print("판정 끝", arm, n)


def proto_lists():
    tree = ast.parse(open("docs/experiments/router_open_1103/proto.py", encoding="utf-8").read())
    v = {t.targets[0].id: ast.literal_eval(t.value) for t in tree.body if isinstance(t, ast.Assign) and getattr(t.targets[0], "id", "") in ("NEG", "POS")}
    return v["NEG"], v["POS"]


def router_items():
    neg, pos = proto_lists()
    items = [("합성-지킴", q, "not_rag") for q in neg] + [("합성-RAG", q, "rag") for q in pos]
    ids = {r["id"] for r in jsonl(R + "pc1_real40.jsonl") if str(r.get("route", "")).endswith("/B")}
    for l in open("docs/experiments/real_eval_1013/questions.tsv", encoding="utf-8"):
        p = l.rstrip("\n").split("\t")
        if len(p) >= 2 and p[0] in ids and (LOCAL or not is_real(p[1])):
            items.append(("real40", p[1], "rag"))
    if LOCAL:
        from core.graph import agent_nodes as N
        c = sqlite3.connect("file:.bridge/agent_bridge.sqlite?mode=ro", uri=True)
        for q in sorted({t.strip() for (t,) in c.execute("select user_text from bridge_jobs") if t and t.strip()}):
            res = N.router_step1_hard_rules(q, q.lower(), "router_diag_jeff") or {}
            rt, ch = res.get("route_type"), res.get("router_choice")
            ref = None if not res else ("rag" if rt == "direct_answer" and ch == "B" else "not_rag")
            items.append(("실사용", q, ref))
    return items


def run_router():
    out = out_path("router")
    done = {x["h"] for x in jsonl(out)}
    n = 0
    with open(out, "a", encoding="utf-8") as w:
        for src, q, ref in router_items():
            h = hashlib.sha1((src + q).encode()).hexdigest()[:12]
            if h in done:
                continue
            mem_guard(n)
            a, s, tok = ask(q, {"route": {"type": "choice", "instructions": ROUTE_INSTR, "criteria": ROUTE_CRIT}})
            w.write(json.dumps({"h": h, "src": src, "q": None if src == "실사용" else q, "ref": ref, "choice": a["route"]["choice"], "p": a["route"]["probabilities"], "s": s}, ensure_ascii=False) + "\n")
            w.flush()
            n += 1
    print("분기 끝", n)


def run_control():
    """무관해야 할 짝 100건: 다른 문항의 주제 줄 50 · 분야가 전혀 다른 요청 50. 모델이 '아니오'를 낼 수 있는지 본다."""
    import random
    from core.llm.relevance_filter import _brief
    out = out_path("control")
    if os.path.exists(out):
        return
    rows = jsonl(TF + "pool_hu.jsonl")
    rng = random.Random(1105)
    far = ["medieval French poetry", "how to bake sourdough bread", "the history of the Roman Empire", "marine biology of coral reefs", "tax law for small businesses"]
    with open(out, "w", encoding="utf-8") as w:
        for i in range(100):
            a = rng.choice(rows)
            block = rng.choice(a["blocks"][:5])
            if i < 50:
                q = rng.choice([r for r in rows if r["id"] != a["id"]])["line"]
                kind = "other_question"
            else:
                q = far[i % len(far)]
                kind = "far_field"
            v, s, tok = noul(re.sub(r"^\[1\] ", "", _brief(1, block)), q)
            w.write(json.dumps({"kind": kind, "doc_of": a["id"], "p": pid(block), "noul": v, "s": s}, ensure_ascii=False) + "\n")
    print("점검 끝")


def score_control():
    res = jsonl(out_path("control"))
    for kind in ("other_question", "far_field"):
        xs = [x["noul"] for x in res if x["kind"] == kind]
        if xs:
            print(f"[배관 점검] {kind}: {len(xs)}건 · noul 중앙 {statistics.median(xs):.3f} · 0.5 이상 {sum(v >= THR for v in xs)}/{len(xs)}")


def load_oj_labels():
    lab = {}
    for f in ("labels.tsv", "labels_extra.tsv", "labels_extra_v2.tsv"):
        if os.path.exists(OJ + f):
            lab.update({l.split("\t")[0]: l.split("\t")[1] for l in open(OJ + f, encoding="utf-8") if l.strip() and not l.startswith("#")})
    return lab


def is_none(x):
    return x == "없음"


def auc(pos, neg):
    if not pos or not neg:
        return float("nan")
    return sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))


def score_filter():
    from core.llm.relevance_filter import protected
    lab = {}
    for f in (S2 + "labels_hu.tsv", TF + "labels_pool.tsv"):
        for l in open(f, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                q, p, v = l.rstrip("\n").split("\t")[:3]
                if f.endswith("labels_pool.tsv") and (q, p) in lab:
                    continue
                lab[(q, p)] = v.strip() != "-"
    rows = jsonl(TF + "pool_hu.jsonl")

    def pr(kept_of):
        ko = kf = dn = df = 0
        for r in rows:
            kept = kept_of(r)
            for b in r["blocks"][:5]:
                p = pid(b)
                on = lab[(r["id"], p)]
                ko += on and p in kept
                kf += (not on) and p in kept
                dn += on and p not in kept
                df += (not on) and p not in kept
        return ko / max(1, ko + kf), ko / max(1, ko + dn), (ko, kf, dn, df)

    fil = {(x["id"], x["k"]): set(x["kept"]) for x in jsonl(TF + "filter_hu.jsonl") if x["n"] == 5}
    p9, r9, c9 = pr(lambda r: fil[(r["id"], r["k"])])
    print(f"9B 다시 계산: P {p9:.1%} · R {r9:.1%} · 남김 안/밖 {c9[0]}/{c9[1]} · 뺌 안/밖 {c9[2]}/{c9[3]}")
    res = {(x["id"], x["k"], x["p"]): x for x in jsonl(out_path("filter"))}
    if not res:
        return

    def kept_at(thr):
        def f(r):
            blocks = r["blocks"][:5]
            ids = [pid(b) for b in blocks]
            keep = {i for i, p in enumerate(ids, 1) if res[(r["id"], r["k"], p)]["noul"] >= thr}
            if not keep:
                return set(ids)  # filter_relevant 의 '없음' = 그대로 둔다
            keep |= protected(r["line"], blocks)
            return {ids[i - 1] for i in keep}
        return f

    p, rc, c = pr(kept_at(THR))
    print(f"[거르기] {LABEL}: 건수 {len(res)} · P {p:.1%}(기준 ≥ 60%) · R {rc:.1%}(기준 ≥ 78%) · 남김 안/밖 {c[0]}/{c[1]} · 뺌 안/밖 {c[2]}/{c[3]} · {'통과' if p >= .6 and rc >= .78 else '미달'}")
    none = sum(all(res[(r["id"], r["k"], pid(b))]["noul"] < THR for b in r["blocks"][:5]) for r in rows)
    print(f"  전부 0.5 미만이라 5편 유지한 줄 {none}/{len(rows)}")
    pos = [x["noul"] for k, x in res.items() if lab[(k[0], k[2])]]
    neg = [x["noul"] for k, x in res.items() if not lab[(k[0], k[2])]]
    print(f"  AUC {auc(pos, neg):.3f} · 주제 안 {len(pos)} 중앙 {statistics.median(pos):.3f} · 주제 밖 {len(neg)} 중앙 {statistics.median(neg):.3f} · 시간 중앙 {statistics.median(x['s'] for x in res.values()):.2f}s · 입력 토큰 중앙 {statistics.median(x['tok'] for x in res.values())}")
    print("  문턱별(보고만):", " · ".join(f"{t}: P {pr(kept_at(t))[0]:.1%} R {pr(kept_at(t))[1]:.1%}" for t in (0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7)))


def score_judge(arm):
    res = jsonl(out_path("judge_" + arm))
    if not res:
        return
    by = {}
    for x in res:
        by.setdefault(x["id"], []).append(x)
    rows = []
    for it in judge_items():
        ds = by.get(it["id"])
        if ds is None:
            continue
        best = max(ds, key=lambda x: x["noul"])
        rows.append({"id": it["id"], "stored": it["stored"], "label": it["label"], "new": best["n"] if best["noul"] >= THR else "없음", "top": best["noul"]})
    judge_gates(f"판정 {arm} {LABEL}", rows, arm == "K")
    print(f"  문항 {len(rows)} · 건수 {len(res)} · 시간 중앙 {statistics.median(x['s'] for x in res):.2f}s · 입력 토큰 중앙 {statistics.median(x['tok'] for x in res)} · 최고 noul 중앙 {statistics.median(r['top'] for r in rows):.3f}")


def judge_gates(name, rows, gate):
    sn = [r for r in rows if is_none(r["stored"])]
    F = [r for r in sn if r["label"] == "F"]
    TQ = [r for r in sn if r["label"] in ("T", "?")]
    rec = sum(not is_none(r["new"]) for r in F)
    lost = sum(not is_none(r["new"]) for r in TQ)
    sd = [r for r in rows if not is_none(r["stored"])]
    nn = [r for r in sd if is_none(r["new"])]
    g1, g2, g3 = rec / max(1, len(F)), lost / max(1, len(TQ)), len(nn)
    v = ("통과" if g1 >= .7 and g2 <= .2 and g3 <= 3 else "미달") if gate else "보고"
    print(f"[{name}] G1 F 회복 {rec}/{len(F)} ({g1:.0%}, ≥ 70%) · G2 T·? 바뀜 {lost}/{len(TQ)} ({g2:.0%}, ≤ 20%) · G3 새 '없음' {g3}/{len(sd)} (≤ 3) · {v}")


def score_router():
    res = jsonl(out_path("router"))
    if not res:
        return
    for src in ("합성-지킴", "합성-RAG", "real40", "실사용"):
        xs = [x for x in res if x["src"] == src]
        ref = [x for x in xs if x["ref"]]
        ok = sum((x["choice"] == "paper_research") == (x["ref"] == "rag") for x in ref)
        dist = {}
        for x in xs:
            dist[x["choice"]] = dist.get(x["choice"], 0) + 1
        print(f"[분기 보고] {src}: 문항 {len(xs)} · 기준 있는 {len(ref)} 중 일치 {ok} · 분포 {dist}")
    print(f"  시간 중앙 {statistics.median(x['s'] for x in res):.2f}s")


def score():
    score_filter()
    lab = load_oj_labels()
    items = {i["id"]: i for i in judge_items()}
    base = [{"id": x["id"], "stored": x["stored"], "label": lab.get(x["id"]), "new": x["new"]} for x in jsonl(OJ + "oj_dev.jsonl")]
    judge_gates("판정 9B v1 꼬리", base, False)
    base2 = [{"id": x["id"], "stored": x["stored"], "label": lab.get(x["id"]), "new": x["new"]} for x in jsonl(OJ + "oj_dev_v2.jsonl")]
    judge_gates("판정 9B v2 꼬리", base2, False)
    assert len(items) == len(base)
    sent = {x["id"] for x in jsonl(out_path("judge_K"))}
    if sent and len(sent) < len(base):  # 실사용 질문을 뺀 경우 9B 도 같은 문항으로 비교
        judge_gates(f"판정 9B v1 꼬리 · 같은 {len(sent)}문항", [b for b in base if b["id"] in sent], False)
        judge_gates(f"판정 9B v2 꼬리 · 같은 {len(sent)}문항", [b for b in base2 if b["id"] in sent], False)
    score_judge("K")
    score_judge("E")
    score_router()
    score_control()


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        smoke()
    elif cmd == "filter":
        run_filter()
    elif cmd == "judge":
        run_judge(sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == "labeled")
    elif cmd == "router":
        run_router()
    elif cmd == "control":
        run_control()
    elif cmd == "score":
        score()
