"""topic_split2_1104 dev: 하위 주제 뽑기 프롬프트 판별로 원출력 · 나뉨을 본다 (LLM 호출만, 검색 없음).

  .venv/bin/python docs/experiments/topic_split2_1104/extract_diag.py build      # dev.jsonl 만들기
  .venv/bin/python docs/experiments/topic_split2_1104/extract_diag.py run v2     # dev_v2.jsonl (이어 하기)
  .venv/bin/python docs/experiments/topic_split2_1104/extract_diag.py show v2    # 틀린 문항 · 요약
  .venv/bin/python docs/experiments/topic_split2_1104/extract_diag.py run code   # 코드 경로 그대로
  .venv/bin/python docs/experiments/topic_split2_1104/extract_diag.py tsv <질문 tsv>  # held-out 보호 2 · 2b: gate_<이름>.jsonl
  .venv/bin/python docs/experiments/topic_split2_1104/extract_diag.py sim        # 새 문항 ↔ 기존 문항 · 서로 유사도 (protocol < 0.72)
"""
import json, os, re, sys, time
sys.path.insert(0, ".")

D = "docs/experiments/topic_split2_1104/"
OLD = "docs/experiments/topic_split_1103/"
# 1103 §2 에서 내가 단 기준 (질문 앞부분 → 나눠야 함 · 주제 수)
EXPECT = [("다음 영어 키워드를 기반으로 논문 5개", "Y", 4), ("RAG retrieval accuracy enhancement, Reranking", "Y", 4),
          ("각 논문을 반드시 아래 4개 축", "Y", 4), ('"RAG 검색 정확도 향상', "Y", 4), ('"""RAG 검색 정확도 향상', "Y", 4),
          ("현재 RAG 기반 생성형 AI", "Y", 3), ("에이전트가 웹을 검색하며", "Y", 3), ("LLM-as-judge self-preference", "?", 0)]


def build():
    rows = []
    for r in map(json.loads, open(OLD + "gate_dev_v2.jsonl", encoding="utf-8")):
        hit = next((e for e in EXPECT if r["q"].startswith(e[0])), None)
        rows.append({"id": r["src"], "q": r["q"], "expect": hit[1] if hit else "N", "k": hit[2] if hit else 0})
    gold = {g["id"]: g for g in map(json.loads, open(OLD + "heldout_topics_gold.jsonl", encoding="utf-8"))}
    for l in open(OLD + "heldout_topics.tsv", encoding="utf-8"):
        qid, q = l.rstrip("\n").split("\t", 1)
        if qid != "HT30":  # 1단계 후보 아님
            rows.append({"id": qid, "q": q.replace("\\n", "\n"), "expect": "Y", "k": len(gold[qid]["topics"]), "topics": gold[qid]["topics"]})
    with open(D + "dev.jsonl", "w", encoding="utf-8") as w:
        for r in rows:
            w.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("dev", len(rows), "Y", sum(r["expect"] == "Y" for r in rows), "N", sum(r["expect"] == "N" for r in rows))


def prompt_v2(q):
    return f"""The user asks for research papers. Does the question list several separate research sub-topics to find papers for (for example a numbered list of topics, or "A, B, C" listed as separate techniques)?
- Instructions about the answer (number of papers, summary style, format, excluding surveys, research gaps) are not topics.
- A method that combines several parts, or a survey of one subject, is one topic.
Write one line per sub-topic with 3-6 English keywords (translate Korean into English). Keep a shared context such as RAG in every line.
If there is only one topic, write one line.
At most 4 lines, nothing else:
1: <English keywords>
2: <English keywords>

User question:
{q}
"""


def prompt_v3(q):
    return f"""The user asks for research papers. List the separate research sub-topics the question asks papers for.
- Numbered items, quoted keywords, or "A, B, C" that name different techniques or problems are separate sub-topics, one line each.
- Instructions about the answer (number of papers, summary style, format, excluding surveys, research gaps) are not sub-topics.
- One method that combines several parts, one comparison, or one survey of a subject is a single sub-topic: write one line.
Each line has 3-6 English keywords naming only that sub-topic (translate Korean). No sentences, no extra techniques.
If the sub-topics share a subject stated in the question, repeat it in each line.
At most 4 lines, nothing else:
1: <keywords>
2: <keywords>

User question:
{q}
"""


PROMPTS = {"v2": prompt_v2, "v3": prompt_v3}


def run(ver):
    from core.graph import agent_nodes as N
    from core.llm.agent_llm import get_rag_query_rewrite_llm
    from langchain_core.messages import HumanMessage
    out = D + f"dev_{ver}.jsonl"
    done = {json.loads(l)["id"] + json.loads(l)["q"] for l in open(out, encoding="utf-8")} if os.path.exists(out) else set()
    rows = list(map(json.loads, open(D + "dev.jsonl", encoding="utf-8")))
    with open(out, "a", encoding="utf-8") as w:
        for k, r in enumerate(rows, 1):
            if r["id"] + r["q"] in done:
                continue
            t0 = time.time()
            if ver == "code":  # 코드 경로 그대로 (후보 · 직접 적은 항목 · LLM)
                row = {**r, "got": N._extract_subtopics(r["q"]) if N.topic_split_candidate(r["q"]) else []}
            else:
                raw = (N.normalize_ai_message_content(get_rag_query_rewrite_llm(num_predict=320).invoke([HumanMessage(content=PROMPTS[ver](r["q"]))])) or "").strip()
                row = {**r, "raw": raw, "got": N._parse_subtopics(raw, r["q"])}
            row["s"] = round(time.time() - t0, 1)
            w.write(json.dumps(row, ensure_ascii=False) + "\n")
            w.flush()
            print(f"[{k}/{len(rows)}] {r['id']} {r['expect']} {len(row['got'])}/{r['k']} {row['s']}s", flush=True)
    show(ver)


def show(ver):
    from core.graph import agent_nodes as N
    rows = list(map(json.loads, open(D + f"dev_{ver}.jsonl", encoding="utf-8")))
    for r in rows:  # 파서를 고쳐도 다시 부르지 않고 저장한 원출력으로 다시 읽는다
        if "raw" in r:
            r["got"] = N._parse_subtopics(r["raw"], r["q"]) if N.topic_split_candidate(r["q"]) else []
    y = [r for r in rows if r["expect"] == "Y"]
    n = [r for r in rows if r["expect"] == "N"]
    rag = N._RAG_WORD_RE
    pol = [r for r in rows if r["got"] and not rag.search(r["q"]) and any(rag.search(g) for g in r["got"])]
    for r in rows:
        print(f"--- {r['id']} {r['expect']} k={r['k']} 나뉨={len(r['got'])} {r.get('s')}s\nQ: {r['q'][:110]!r}\nRAW: {r.get('raw', '')[:400]!r}\nGOT: {r['got']}")
    print(f"\n{ver}: Y {len(y)} 중 나뉨 {sum(bool(r['got']) for r in y)} · 줄 수까지 맞음 {sum(len(r['got']) == r['k'] for r in y)}"
          f" · N {len(n)} 중 나뉨 {sum(bool(r['got']) for r in n)} · RAG 오염 {len(pol)}")


def tsv(path):
    from core.graph import agent_nodes as N
    out = D + "gate_" + os.path.basename(path).rsplit(".", 1)[0] + ".jsonl"
    rows = [l.rstrip("\n").split("\t", 1) for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]
    with open(out, "w", encoding="utf-8") as w:
        n_cand = n_split = 0
        for qid, q in rows:
            q = q.replace("\\n", "\n")
            cand = N.topic_split_candidate(q)
            got = N._extract_subtopics(q) if cand else []
            n_cand += cand
            n_split += bool(got)
            w.write(json.dumps({"id": qid, "q": q, "cand": cand, "got": got}, ensure_ascii=False) + "\n")
            if cand:
                print(qid, "후보", "나뉨" if got else "안 나뉨", got, flush=True)
    print(f"{os.path.basename(path)}: 문항 {len(rows)} · 1단계 후보 {n_cand} · 나뉨 {n_split}")


def sim():
    import difflib, glob, sqlite3
    old = {t.strip() for _, t in sqlite3.connect(".bridge/agent_bridge.sqlite").execute("select id, user_text from bridge_jobs") if t and t.strip()}
    for f in glob.glob("docs/experiments/**/*.tsv", recursive=True):
        if "topic_split2_1104" not in f:
            old |= {l.rstrip("\n").split("\t")[1].replace("\\n", "\n") for l in open(f, encoding="utf-8", errors="ignore") if l.count("\t") >= 1 and not l.startswith("#")}
    new = [l.rstrip("\n").split("\t", 1) for f in ("heldout.tsv", "heldout_single.tsv") for l in open(D + f, encoding="utf-8")]
    new = [(a, b.replace("\\n", "\n")) for a, b in new]
    ratio = lambda a, b: difflib.SequenceMatcher(None, a, b).ratio()
    top = max(((ratio(q, o), i, o[:50]) for i, q in new for o in old), key=lambda x: x[0])
    self_top = max((ratio(a[1], b[1]), a[0], b[0]) for k, a in enumerate(new) for b in new[k + 1:])
    print("기존 문항", len(old), "최대", round(top[0], 3), top[1], repr(top[2]), "· 서로 최대", round(self_top[0], 3), self_top[1:])
    assert top[0] < 0.72 and self_top[0] < 0.72


if __name__ == "__main__":
    {"build": lambda: build(), "run": lambda: run(sys.argv[2]), "show": lambda: show(sys.argv[2]), "tsv": lambda: tsv(sys.argv[2]), "sim": sim}[sys.argv[1]]()
