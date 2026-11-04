"""topic_answer_1104 dev: 항목별 판정 오프라인 — ans_hu 컨텍스트(답 앞 단계 그대로)에 항목마다 문서 번호를 묻고 라벨과 비교한다.

  .venv/bin/python docs/experiments/topic_answer_1104/item_judge.py items        # 질문 → 항목 확인 (LLM 없음)
  .venv/bin/python docs/experiments/topic_answer_1104/item_judge.py run v1       # 판정 호출 → item_judge_v1.jsonl (이어 하기)
  .venv/bin/python docs/experiments/topic_answer_1104/item_judge.py score v1     # 항목 단위 · 문서 단위 채점
"""
import json, os, re, sys, time
sys.path.insert(0, ".")
sys.path.insert(0, "docs/experiments/topic_split2_1104")
import score as S

D = "docs/experiments/topic_answer_1104/"
PROMPTS = {
    "v1": """아래 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 아래 [항목]마다 논문을 찾고 있다.

항목마다 그 항목을 **직접** 다루는 문서 번호를 적어라. 직접 다루는 문서가 없으면 `없음`이라고 적어라.
- 단어 몇 개만 겹치거나 다른 문제를 다루는 문서는 넣지 마라.
- 항목과 문서를 억지로 맞추지 마라. `없음`도 정상 답이다.

출력은 항목마다 한 줄, 다른 말 없이:
1: 문서 N, 문서 M
2: 없음

[참고 문서]
{context}

[항목]
{items}""",
    "v2": """아래 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 아래 [항목]마다 논문을 찾고 있다.

항목마다 그 항목의 주제를 다루는 문서 번호를 모두 적어라. 그 주제를 다루는 문서가 하나도 없을 때만 `없음`이라고 적어라.
- 단어만 겹치고 다른 문제를 다루는 문서는 넣지 마라.

출력은 항목마다 한 줄, 다른 말 없이:
1: 문서 N, 문서 M
2: 없음

[참고 문서]
{context}

[항목]
{items}""",
    "v3": """아래 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 아래 [항목]마다 논문을 찾고 있다.

문서마다 그 문서가 다루는 항목 번호를 적어라. 어느 항목도 다루지 않으면 `없음`이라고 적어라.
- 단어만 겹치고 다른 문제를 다루는 문서는 `없음`이다.

출력은 문서마다 한 줄, 다른 말 없이:
문서 1: 항목 2
문서 2: 없음

[참고 문서]
{context}

[항목]
{items}""",
}


def questions():
    return {l.split("\t")[0]: l.split("\t", 1)[1].rstrip("\n").replace("\\n", "\n") for l in open(S.D + "heldout.tsv", encoding="utf-8")}


def items_cmd():
    from core.graph import agent_nodes as N
    gold = {g["id"]: g for g in map(json.loads, open(S.D + "heldout_gold.jsonl", encoding="utf-8"))}
    bad = 0
    for q, text in questions().items():
        it = N.topic_answer_items(text)
        ok = len(it) == len(gold[q]["topics"])
        bad += not ok
        print(q, "OK" if ok else f"개수 {len(it)}≠{len(gold[q]['topics'])}", it)
    print("개수 다름", bad)
    for l in open(S.D + "heldout_single.tsv", encoding="utf-8"):
        q, text = l.rstrip("\n").split("\t", 1)
        print(q, N.topic_answer_items(text.replace("\\n", "\n")))


def run(ver):
    import core.config.agent_config as cfg  # .env
    from core.graph import agent_nodes as N
    from langchain_ollama import ChatOllama
    from core.config.agent_config import ollama_kwargs
    rows = S.rows("ans_hu")
    out = D + f"item_judge_{ver}.jsonl"
    done = {json.loads(l)["id"] for l in open(out, encoding="utf-8")} if os.path.exists(out) else set()
    llm = ChatOllama(**ollama_kwargs(model=cfg.RAG_ANSWER_MODEL, temperature=0.0, seed=0, reasoning=False, num_predict=120))
    with open(out, "a", encoding="utf-8") as w:
        for q, text in questions().items():
            if q in done:
                continue
            it = N.topic_answer_items(text)
            if not it:
                continue
            t0 = time.time()
            prompt = PROMPTS[ver].format(context=rows[q].get("numbered_context") or "", items="\n".join(f"{k}. {x}" for k, x in enumerate(it, 1)))
            raw = str(llm.invoke(prompt).content or "")
            w.write(json.dumps({"id": q, "items": it, "raw": raw, "s": round(time.time() - t0, 1)}, ensure_ascii=False) + "\n")
            w.flush()
            print(q, f"{time.time() - t0:.1f}s", repr(raw[:110]), flush=True)
    print("판정 끝")


def score(ver):
    rows = S.rows("ans_hu")
    lab = {}
    for f in (S.D + "labels_hu.tsv", "docs/experiments/topic_filter_1104/labels_pool.tsv"):
        for l in open(f, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                q, p, v = l.rstrip("\n").split("\t")[:3]
                lab.setdefault((q, p), set() if v.strip() == "-" else {int(x) for x in re.findall(r"\d+", v)})
    cu = fu = cc = fc = 0  # 문서 없는 주제: 없음 맞힘 · 있다고 함 / 문서 있는 주제: 있다고 함 · 없음이라 함
    tp = fp = fn = 0
    miss = []
    for r in map(json.loads, open(D + f"item_judge_{ver}.jsonl", encoding="utf-8")):
        q = r["id"]
        nums = {int(a): b for a, b in re.findall(r"^\s*(\d)\s*[:：.)]\s*(.*)$", r["raw"], re.M)}
        ctx = {int(n): S.HEAD.search(b).group(1) for n, b in S.BLK.findall(rows[q].get("numbered_context") or "") if S.HEAD.search(b)}
        by_doc = re.findall(r"문서\s*(\d{1,2})\s*[:：]\s*(.*)", r["raw"])  # v3: 문서 → 항목
        for k in range(1, len(r["items"]) + 1):
            line = nums.get(k, "")
            if by_doc:
                picked = {ctx.get(int(n)) for n, v in by_doc if "없음" not in v and k in {int(x) for x in re.findall(r"\d", v)}} - {None}
            else:
                picked = {ctx.get(int(x)) for x in re.findall(r"\d{1,2}", line)} - {None} if "없음" not in line else set()
            truth = {p for p in ctx.values() if k in lab.get((q, p), set())}
            tp += len(picked & truth)
            fp += len(picked - truth)
            fn += len(truth - picked)
            if truth:
                cc += bool(picked)
                fc += not picked
                if not picked:
                    miss.append((q, k, "있는데 없음", r["items"][k - 1][:24]))
            else:
                cu += not picked
                fu += bool(picked)
                if picked:
                    miss.append((q, k, "없는데 있음", r["items"][k - 1][:24]))
    print(f"{ver}: 문서 없는 주제 {cu + fu} 중 없음 {cu} ({cu / max(1, cu + fu):.0%}) · 문서 있는 주제 {cc + fc} 중 잘못 없음 {fc} ({fc / max(1, cc + fc):.0%})"
          f" · 문서 단위 정밀도 {tp / max(1, tp + fp):.0%} 재현율 {tp / max(1, tp + fn):.0%}")
    for m in miss:
        print(" ", m)


if __name__ == "__main__":
    {"items": items_cmd, "run": lambda: run(sys.argv[2]), "score": lambda: score(sys.argv[2])}[sys.argv[1]]()
