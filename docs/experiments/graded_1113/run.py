"""graded_1113 재생 (README §2). 맥미니에서:

  RAG_ANSWER_MODEL=<모델> .venv/bin/python docs/experiments/graded_1113/run.py filter   # 거르기 Q0 · v2
  RAG_ANSWER_MODEL=<모델> .venv/bin/python docs/experiments/graded_1113/run.py judge    # 판정 v2 (oj 167 + real40 N)
  .venv/bin/python docs/experiments/graded_1113/run.py score                            # 모든 모델 채점

결과는 filter.<모델>.jsonl · judge.<모델>.jsonl 에 이어 쓴다(끊겨도 다시 돌리면 이어 함).
"""
import json, os, re, sys, time

sys.path.insert(0, ".")
sys.path.insert(0, "docs/experiments/open_judge_1103")
D = "docs/experiments/graded_1113/"
TF = "docs/experiments/topic_filter_1104/"
TS = "docs/experiments/topic_split2_1104/"
MODELS = ["yunsur_v13", "qwen3.6:27b-q4_K_M", "qwen3.6:35b-a3b-q4_K_M"]


def sfx(m):
    return re.sub(r"[^A-Za-z0-9._-]", "_", m)


def head(block):
    return re.search(r"\[(\d{4}\.\d{4,5})", block).group(1)


def questions():
    return {l.split("\t")[0]: l.rstrip("\n").split("\t", 1)[1].replace("\\n", "\n") for l in open(TS + "heldout.tsv", encoding="utf-8") if "\t" in l}


def labels():
    lab = {}
    for f in (TS + "labels_hu.tsv", TF + "labels_pool.tsv"):
        for l in open(f, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                q, p, v = l.rstrip("\n").split("\t")[:3]
                if f.endswith("labels_pool.tsv") and (q, p) in lab:
                    continue
                lab[(q, p)] = v.strip() != "-"
    return lab


def done(path):
    return {json.loads(l)["key"] for l in open(path, encoding="utf-8")} if os.path.exists(path) else set()


def run_filter(model):
    from core.llm import relevance_filter as RF
    from core.llm.citation_fix import RAG_HIT_SEP

    Q = questions()
    out = D + f"filter.{sfx(model)}.jsonl"
    seen = done(out)
    with open(out, "a", encoding="utf-8") as w:
        for r in map(json.loads, open(TF + "pool_hu.jsonl", encoding="utf-8")):
            key = f"{r['id']}#{r['k']}"
            if key in seen:
                continue
            blocks = r["blocks"][:5]
            ctx = RAG_HIT_SEP.join(blocks)
            t0 = time.time()
            c0, s0 = RF.filter_relevant(Q[r["id"]], ctx, model)
            t1 = time.time()
            _, s2, grades = RF.filter_graded(Q[r["id"]], ctx, model)
            t2 = time.time()
            w.write(json.dumps({"key": key, "id": r["id"], "docs": [head(b) for b in blocks], "q0_status": s0,
                                "q0_kept": [head(b) for b in c0.split(RAG_HIT_SEP) if b.strip()],
                                "v2_status": s2, "v2": grades, "s0": round(t1 - t0, 1), "s2": round(t2 - t1, 1)}, ensure_ascii=False) + "\n")
            w.flush()
            print(key, s0, s2, grades, flush=True)


def real40_items():
    import oj
    Q = {l.split("\t")[0]: l.rstrip("\n").split("\t")[1] for l in open("docs/experiments/real_eval_1013/questions.tsv", encoding="utf-8") if "\t" in l}
    out = []
    for r in map(json.loads, open("docs/experiments/e2e_ko_1008/results/weekly_20261112.jsonl", encoding="utf-8")):
        if r["id"].startswith("N") and r.get("doc_ids"):
            out.append({"id": "R40_" + r["id"], "src": "real40", "q": Q[r["id"]], "stored": None,
                        "prompt": oj.rebuild(Q[r["id"]], r["numbered_context"], len(r["doc_ids"]))})
    return out


def run_judge(model):
    import oj
    import core.llm.presence_judge as pj
    from core.llm.agent_prompts import DIRECT_ANSWER_RAG_SYSTEM_BASE

    items = oj.pool() + real40_items()
    out = D + f"judge.{sfx(model)}.jsonl"
    seen = done(out)
    with open(out, "a", encoding="utf-8") as w:
        for it in items:
            if it["id"] in seen:
                continue
            t0 = time.time()
            v2 = pj.judge_presence_shared_v2(DIRECT_ANSWER_RAG_SYSTEM_BASE, it["prompt"], it["q"], model)
            row = {"key": it["id"], "src": it["src"], "stored": it["stored"], "v2": v2, "s": round(time.time() - t0, 1)}
            if it["src"] == "real40":  # 운영 꼬리도 같이 — N 층 비교용
                row["old"] = pj.judge_presence_shared(DIRECT_ANSWER_RAG_SYSTEM_BASE, it["prompt"], it["q"], model)
            w.write(json.dumps(row, ensure_ascii=False) + "\n")
            w.flush()
            print(it["id"], row.get("old"), v2, flush=True)


def score():
    lab = labels()
    ojl = {l.split("\t")[0]: l.split("\t")[1] for l in open("docs/experiments/open_judge_1103/labels.tsv", encoding="utf-8") if l.strip() and not l.startswith("#")}
    fil = {m: [json.loads(l) for l in open(D + f"filter.{sfx(m)}.jsonl", encoding="utf-8")] for m in MODELS if os.path.exists(D + f"filter.{sfx(m)}.jsonl")}
    print("## 거르기 (문서-행, 라벨 = 하위 주제 어느 하나)")
    keepsets = {}
    for m, rows in fil.items():
        for var in ("Q0", "K", "KR"):
            tp = fp = fn = 0
            ks = {}
            for r in rows:
                if var == "Q0":
                    kept = set(r["q0_kept"]) if r["q0_status"] not in ("없음", "못 읽음", "호출 실패") else set(r["docs"])
                else:
                    g = r["v2"]
                    want = ("핵심",) if var == "K" else ("핵심", "관련")
                    kept = {r["docs"][int(i) - 1] for i, x in (g or {}).items() if x in want} if g else set(r["docs"])
                    kept = kept or set(r["docs"])  # 남는 게 없으면 그대로(운영과 같음)
                for p in r["docs"]:
                    on = lab[(r["id"], p)]
                    tp += on and p in kept
                    fp += (not on) and p in kept
                    fn += on and p not in kept
                    ks[(r["key"], p)] = p in kept
            keepsets[(m, var)] = ks
            unread = sum((r["q0_status"] if var == "Q0" else r["v2_status"]) in ("못 읽음", "호출 실패") for r in rows)
            P, R = tp / max(1, tp + fp), tp / max(1, tp + fn)
            ok = "통과" if var != "Q0" and P >= .60 and R >= .78 else ""
            print(f"{m:28s} {var:3s} 정밀도 {P:.1%} · 재현율 {R:.1%} · 못 읽음 {unread}/{len(rows)} {ok}")
    for var in ("Q0", "KR"):
        ms = [m for m in fil]
        for i in range(len(ms)):
            for j in range(i + 1, len(ms)):
                a, b = keepsets[(ms[i], var)], keepsets[(ms[j], var)]
                common = set(a) & set(b)
                print(f"  {var} 일치 {ms[i]}-{ms[j]}: {sum(a[k] == b[k] for k in common) / max(1, len(common)):.1%}")

    print("\n## 판정 v2")
    for m in MODELS:
        p = D + f"judge.{sfx(m)}.jsonl"
        if not os.path.exists(p):
            continue
        rows = {r["key"]: r for r in map(json.loads, open(p, encoding="utf-8"))}
        kind = lambda v: "없음" if v == "없음" else (v[0] if isinstance(v, list) else "실패")
        F = [k for k, v in ojl.items() if v == "F" and k in rows]
        T = [k for k, v in ojl.items() if v == "T" and k in rows]
        U = [k for k, v in ojl.items() if v == "?" and k in rows]
        j1 = sum(kind(rows[k]["v2"]) in ("있음", "부분") for k in F)
        j2 = sum(kind(rows[k]["v2"]) in ("없음", "부분") for k in T)
        stored_docs = [k for k, r in rows.items() if r["src"] != "real40" and r["stored"] != "없음"]
        j3 = [k for k in stored_docs if kind(rows[k]["v2"]) == "없음"]
        n40 = [k for k in rows if k.startswith("R40_")]
        j4a = sum(kind(rows[k]["v2"]) == "있음" for k in n40)
        j4n = sum(kind(rows[k]["v2"]) == "없음" for k in n40)
        old_n = sum(rows[k].get("old") == "없음" for k in n40)
        dist = {}
        for r in rows.values():
            dist[kind(r["v2"])] = dist.get(kind(r["v2"]), 0) + 1
        ok = all([j1 >= 20, j2 >= 2, len(j3) <= 5, j4a >= 13, j4n == 0])
        print(f"{m}: J1 F→있음/부분 {j1}/{len(F)} · J2 T→없음/부분 {j2}/{len(T)} · ? {[kind(rows[k]['v2']) for k in U]}"
              f" · J3 저장 문서 중 없음 {len(j3)}/{len(stored_docs)} · J4 N 있음 {j4a}/{len(n40)} 없음 {j4n} (운영 꼬리 없음 {old_n})"
              f" · 분포 {dist} · {'통과' if ok else '미달'}")
        if j3:
            print("   J3 없음:", j3)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "score":
        score()
    else:
        import core.config.agent_config as cfg  # .env
        {"filter": run_filter, "judge": run_judge}[cmd](cfg.RAG_ANSWER_MODEL)
