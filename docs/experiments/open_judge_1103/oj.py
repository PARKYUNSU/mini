"""open_judge_1103: 열린 요청용 판정 꼬리 오프라인 측정 (dev 만, 답 생성 없음, README 참고).

  .venv/bin/python docs/experiments/open_judge_1103/oj.py packet   # 저장 '없음' 33 라벨 묶음
  .venv/bin/python docs/experiments/open_judge_1103/oj.py run      # 옛 · 새 꼬리 판정 → oj_dev.jsonl
  .venv/bin/python docs/experiments/open_judge_1103/oj.py extra    # 새로 '없음'이 된 문항 라벨 묶음(어느 꼬리인지 안 보임)
  .venv/bin/python docs/experiments/open_judge_1103/oj.py score

판정 입력은 저장 행에서 운영과 같은 글자로 다시 만들고 answer_input sha1 로 확인한다.
판정 호출은 운영 함수 judge_presence_shared 그대로이고 꼬리(SHARED_TAIL)만 바꾼다.
"""
import hashlib, json, os, re, sys, time

sys.path.insert(0, ".")
import core.config.agent_config as cfg  # .env
import core.llm.presence_judge as pj
from core.graph.agent_nodes import _prefer_single_hit_rag_context, list_mode_active
from core.llm.agent_prompts import DIRECT_ANSWER_RAG_SYSTEM_BASE, RAG_OUTPUT_TEMPLATE_MULTI_STRICT, direct_answer_rag_user, list_slots_template
from core.rag.agent_chroma_rag import context_abstract_chars

R = "docs/experiments/e2e_ko_1008/results/"
D = "docs/experiments/open_judge_1103/"
SETS = (("ogb_s1", "docs/experiments/open_gate2_1103/heldout_open2.tsv"),
        ("og_s1", "docs/experiments/open_gate_1103/heldout_open.tsv"),
        ("jn_dev", "docs/experiments/judge_none_1103/questions.tsv"))
# README §1 — 측정 전 고정. 바꾸면 v2 로 기록한다.
OPEN_TAIL = """
[판정 요청 — 답변을 쓰지 말고 판정 한 줄만]
위 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 특정한 연구 하나가 아니라 **질문의 주제를 다룬 논문**을 추천받으려 한다.

질문의 주제를 주된 내용으로 다루는 문서가 있으면 그 문서 번호를, 하나도 없으면 `없음`을 답하라.
- 방법·대상·결과가 질문의 표현과 똑같지 않아도 주제가 같으면 고른다.
- 낱말이나 분야만 겹치고 주된 내용이 다른 주제이면 `없음`이다.
- 여러 문서가 맞으면 가장 앞 번호 하나만 적는다.

출력은 정확히 한 줄: `답: 문서 N` 또는 `답: 없음`

[질문]
{question}"""


def tsv(p):
    return dict(l.rstrip("\n").split("\t", 1) for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#"))


def rebuild(q, ctx, n_docs):
    """agent_nodes 의 답변 프롬프트 조립을 그대로 따른다(평가 세션은 대화 기록 없음)."""
    wd = any(k in q for k in ("자세히", "더", "길게", "상세하게", "구체적으로"))
    psh = _prefer_single_hit_rag_context(q, wants_depth=wd)
    tpl = RAG_OUTPUT_TEMPLATE_MULTI_STRICT
    if os.getenv("RAG_LIST_SLOTS", "0").strip() == "1" and n_docs > 1 and list_mode_active(q, prefer_single_hit=psh):
        tpl = list_slots_template(n_docs)
    mx = (8000 if (psh and wd) else (5000 if psh else 8000)) + 5 * max(0, context_abstract_chars() - 800)
    return direct_answer_rag_user("[최근 대화]\n", ctx, "", q, output_template_strict=tpl, rag_max_chars=mx,
                                  doc_count=n_docs, list_mode=list_mode_active(q, prefer_single_hit=psh))


def pool():
    out = []
    for lb, qf in SETS:
        Q = tsv(qf)
        for r in map(json.loads, open(R + lb + ".jsonl", encoding="utf-8")):
            q = Q.get(r["id"])
            pick = next((x.get("pick") for x in r.get("trace", []) if x.get("stage") == "judge"), None)
            if r["id"].startswith("H_") or not q or not pj._GATE_OPEN.search(q) or pick is None or not r.get("doc_ids"):
                continue
            p = rebuild(q, r["numbered_context"], len(r["doc_ids"]))
            sysp = DIRECT_ANSWER_RAG_SYSTEM_BASE + (pj.NO_DOC_HINT if pick == "없음" else "")
            assert hashlib.sha1((sysp + "\n" + p).encode()).hexdigest()[:12] == r["answer_input"], r["id"]
            out.append({"id": r["id"], "src": lb, "q": q, "stored": pick, "prompt": p, "ctx": r["numbered_context"]})
    return out


BLK = re.compile(r"\[문서 (\d+)\]\n(.*?)(?=\n\[문서 \d+\]\n|\Z)", re.S)
HEAD = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]*)")


def packet(items, path):
    out = []
    for it in items:
        lines = [f"## {it['id']}\n\n**질문** {it['q']}\n"]
        for n, body in BLK.findall(it["ctx"]):
            m = HEAD.search(body)
            t, rest = (m.group(2).strip(), body[m.end():]) if m else ("?", body)
            lines.append(f"- [문서 {n}] **{t}** — {re.sub(r'\\s+', ' ', rest).strip()[:420]}")
        out.append("\n".join(lines))
    open(path, "w", encoding="utf-8").write("\n\n---\n\n".join(out) + "\n")
    print(len(items), "문항 →", path)


def is_none(x):
    return x == "없음"


def main():
    cmd = sys.argv[1]
    items = pool()
    print("문항", len(items), "· 저장 '없음'", sum(is_none(i["stored"]) for i in items), flush=True)
    if cmd == "packet":
        packet([i for i in items if is_none(i["stored"])], D + "label_packet.md")
    elif cmd == "run":
        out = D + "oj_dev.jsonl"
        done = {json.loads(l)["id"] for l in open(out, encoding="utf-8")} if os.path.exists(out) else set()
        old_tail = pj.SHARED_TAIL
        with open(out, "a", encoding="utf-8") as w:
            for k, it in enumerate(items, 1):
                if it["id"] in done:
                    continue
                row = {"id": it["id"], "src": it["src"], "stored": it["stored"]}
                try:
                    for name, tail in (("old", old_tail), ("new", OPEN_TAIL)):
                        pj.SHARED_TAIL = tail
                        t0 = time.time()
                        row[name] = pj.judge_presence_shared(DIRECT_ANSWER_RAG_SYSTEM_BASE, it["prompt"], it["q"], cfg.RAG_ANSWER_MODEL)
                        row[name + "_s"] = round(time.time() - t0, 1)
                finally:
                    pj.SHARED_TAIL = old_tail
                w.write(json.dumps(row, ensure_ascii=False) + "\n")
                w.flush()
                print(f"[{k}/{len(items)}] {it['id']} 저장 {it['stored']} · 옛 {row['old']} · 새 {row['new']} ({row['old_s']}s+{row['new_s']}s)", flush=True)
    elif cmd == "extra":
        res = {r["id"]: r for r in map(json.loads, open(D + "oj_dev.jsonl", encoding="utf-8"))}
        ids = sorted(i for i, r in res.items() if not is_none(r["stored"]) and (is_none(r["old"]) or is_none(r["new"])))
        packet([i for i in items if i["id"] in ids], D + "label_packet_extra.md")
    elif cmd == "score":
        res = {r["id"]: r for r in map(json.loads, open(D + "oj_dev.jsonl", encoding="utf-8"))}
        lab = {}
        for f in ("labels.tsv", "labels_extra.tsv"):
            if os.path.exists(D + f):
                lab.update({l.split("\t")[0]: l.split("\t")[1] for l in open(D + f, encoding="utf-8") if l.strip() and not l.startswith("#")})
        rs = list(res.values())
        same = sum(is_none(r["old"]) == is_none(r["stored"]) for r in rs)
        print(f"G0 재현: 옛 꼬리 '없음' 여부 저장과 같음 {same}/{len(rs)} ({same / len(rs):.1%}, 기준 ≥ 95%)")
        sn = [r for r in rs if is_none(r["stored"])]
        F = [r for r in sn if lab.get(r["id"]) == "F"]
        TQ = [r for r in sn if lab.get(r["id"]) in ("T", "?")]
        rec = sum(not is_none(r["new"]) for r in F)
        lost = sum(not is_none(r["new"]) for r in TQ)
        print(f"라벨(저장 '없음' {len(sn)}): F {len(F)} · T {sum(lab.get(r['id']) == 'T' for r in sn)} · ? {sum(lab.get(r['id']) == '?' for r in sn)} · 없음 {sum(r['id'] not in lab for r in sn)}")
        print(f"G1 회복: F 중 새 꼬리 '없음' 아님 {rec}/{len(F)} ({rec / max(1, len(F)):.0%}, 기준 ≥ 70%)")
        print(f"G2 보존: T · ? 중 새 꼬리 '없음' 아님 {lost}/{len(TQ)} ({lost / max(1, len(TQ)):.0%}, 기준 ≤ 20%)")
        sd = [r for r in rs if not is_none(r["stored"])]
        nn = [r for r in sd if is_none(r["new"])]
        print(f"G3 새 '없음': 저장 문서 {len(sd)} 중 새 꼬리 '없음' {len(nn)} (기준 ≤ 3) — 라벨 {[(r['id'], lab.get(r['id'])) for r in nn]}")
        print("보고: 파싱 실패 옛", sum(r["old"] is None for r in rs), "· 새", sum(r["new"] is None for r in rs))
        for nm, xs in (("F", F), ("T·?", TQ)):
            print(f"   {nm}: " + " · ".join(f"{r['id']}({lab[r['id']]}) 새 {r['new']}" for r in xs))
        print("보고: 옛 꼬리 '없음'인데 저장은 문서", [(r["id"], lab.get(r["id"])) for r in sd if is_none(r["old"])])


if __name__ == "__main__":
    main()
