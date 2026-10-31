"""conclusion_verify_1101 오프라인 (맥미니): 판정 라벨이 있는 결론 문장마다 그 문장이 인용한 블록만 보여 주고
9B 에게 같음 · 다름 · 없음을 묻는다. 질문은 보여 주지 않는다(질문 전제에 끌리지 않게).

    .venv/bin/python docs/experiments/conclusion_verify_1101/offline.py count   # 표본 수만
    .venv/bin/python docs/experiments/conclusion_verify_1101/offline.py v1      # results_v1.jsonl 에 이어 쓰기
    .venv/bin/python docs/experiments/conclusion_verify_1101/offline.py v2
"""
import collections, json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env")
from core.llm.answer_fix import _CITED, _find
from core.llm.citation_fix import RAG_HIT_SEP

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "conclusion_verify_1101"

SYSTEM = "너는 요약 문장이 참고 문서와 맞는지 확인하는 검사자다. 문서에 적힌 것만 근거로 삼고, 상식이나 추측으로 채우지 않는다."
CRITERIA = """문장 속 [arXiv 번호] 는 그 내용의 출처로 밝힌 문서다. 이 문장이 참고 문서와 맞는지 판단하라.
- 같음: 문장이 각 문서에 돌린 내용이 그 문서에 적혀 있다. 번역 · 요약 · 바꿔 말하기는 괜찮다.
- 다름: 문서와 어긋난다 — 방향이 반대 · 수치나 대상이 다름 · 다른 문서의 내용을 이 문서에 붙임 · 문서가 배경이나 기존 연구로 말한 것을 그 논문의 결과로 씀.
- 없음: 문서에 없는 내용이 들어 있다 — 문서가 말하지 않은 주장 · 해결책 · 비교 우열, "모두 · 공통" 같은 일반화."""
HEAD = "[참고 문서]\n{blocks}\n\n[확인할 문장]\n{sentence}\n\n" + CRITERIA + "\n"
PROMPT = {
    "v1": HEAD + "출력은 정확히 한 줄: `판정: 같음` 또는 `판정: 다름` 또는 `판정: 없음`",
    "v2": HEAD + "먼저 문장을 뒷받침하는 문서 원문 구절을 영어 그대로 옮기고(없으면 `없음`), 그다음 판정하라.\n"
                 "출력은 정확히 두 줄:\n근거: <원문 구절 또는 없음>\n판정: 같음 · 다름 · 없음 중 하나",
}
NUM_PREDICT = {"v1": 12, "v2": 200}
_VERDICT = re.compile(r"판정\s*[:：]\s*\**\s*(같음|다름|없음)")
# 눈가림 판정 파일과 같은 문장 나누기(conclusion_v3_1024 offline.py)
split = lambda t: [s.strip() for s in re.split(r"(?<=[.!?。])\s+|\n+", re.sub(r"<[^>]+>", "", t)) if len(s.strip()) > 10]
norm = lambda s: re.sub(r"\s+|<[^>]+>|v\d+(?=\])", "", s)
# answer_review_1030 §6 이 짚은 실사용 오류 문장(10-31 재질문) — 보고만
CASES = {"R_137": ("X", ["다른 모델군으로 교체"]), "R_138": ("E", ["회귀를 중요"]),
         "R_139": ("E", ["자신의 출력보다 다른 출력", "자신의 출력을 인식하는 메커니즘", "평균 40%"])}

_rows = {}


def row(lbl, qid):
    if lbl not in _rows:
        _rows[lbl] = {r["id"]: r for r in map(json.loads, open(R / f"{lbl}.jsonl"))}
    return _rows[lbl][qid]


def labels(p):
    return dict(l.split("\t")[:2] for l in open(p).read().splitlines()[1:] if "\t" in l)


def sents(md, pat):
    return {m.group(1): m.group(2).strip() for m in (re.match(pat, l) for l in open(md)) if m}


def items():
    """``[(출처, (세트, 질문 id), sid, 문장, 라벨)]`` — 같은 답의 같은 문장은 한 번만(첫 라벨)."""
    out = []
    lab = labels(EXP / "answer_judge_1024/judged_claims.tsv"); src = None
    for l in open(EXP / "answer_judge_1024/sample.md"):
        m = re.match(r"######## A\d\d \[\w\] (\S+) (\S+) \|", l)
        if m:
            src = (m.group(1), m.group(2))
        m = re.match(r"(C\d\d\.\d\d) \[결론\] (.*)", l)
        if m:
            out.append(("aj", src, m.group(1), m.group(2).strip(), lab[m.group(1)]))
    res = [json.loads(l) for l in open(EXP / "conclusion_v3_1024/results.jsonl")]
    s = sents(EXP / "conclusion_v3_1024/blind.md", r"(Q\d\d[AB]\.\d+) (.*)")
    for sid, v in labels(EXP / "conclusion_v3_1024/blind_judged.tsv").items():
        x = res[int(sid[1:3])]; out.append(("v3", (x["set"], x["id"]), sid, s[sid], v))
    for d, lbl in (("conclusion_drop2_1025", "cd2_new"), ("conclusion_overgen_1025", "cov_new")):
        key = json.load(open(EXP / d / "blind_key.json")); s = sents(EXP / d / "blind.md", r"(Q\d\d\.\d+) (.*)")
        for sid, v in labels(EXP / d / "blind_judged.tsv").items():
            out.append((d.split("_")[1], (lbl, key[sid.split(".")[0]]), sid, s[sid], v))
    for qid, (v, keys) in CASES.items():
        a = row("recheck_1031", qid)["answer"]
        for j, x in enumerate(split(a[_find("결론", a).end():])):
            if any(k in x for k in keys):
                out.append(("case", ("recheck_1031", qid), f"{qid}.{j}", x, v))
    grp = collections.defaultdict(list)  # 결론(답 · 조건) → 그 결론 문장들이 인용한 논문, 인용 없는 문장용
    for it in out:
        grp[(it[0], it[2].rsplit(".", 1)[0])] += _CITED.findall(it[3])
    seen, uniq, dup = {}, [], collections.Counter()
    for it in out:
        k = (it[1], norm(it[3]))
        if k in seen:
            dup["같은 라벨" if seen[k] == it[4] else "다른 라벨"] += 1
            continue
        seen[k] = it[4]; uniq.append(it)
    return uniq, dup, {k: list(dict.fromkeys(v)) for k, v in grp.items()}


def blocks(r):
    """논문 ID(버전 없음) → 블록 원문(문서 번호 · 거리 · 발행일 줄 뺌, 2,500자 — 결론 다시 쓰기의 _BLOCK_MAX)."""
    ids = dict(enumerate(r.get("doc_ids") or [], 1)); out = {}
    for b in (r.get("numbered_context") or "").split(RAG_HIT_SEP):
        m = re.match(r"\s*\[\s*문서\s*(\d+)\s*\]", b)
        if m and int(m.group(1)) in ids:
            body = "\n".join(l for l in b.strip().split("\n")[1:] if not re.match(r"\[(Distance|발행일)", l))
            out.setdefault(re.sub(r"v\d+$", "", ids[int(m.group(1))]), body[:2500])
    return out


def prepare(it, grp):
    """인용 있는 문장은 그 인용 블록, 없는 문장은 같은 결론이 인용한 블록 전부와 대조(보고용 범위)."""
    src, key, sid, s, lab = it
    # shortcut: 문장 앞에 붙은 인용([id] 다음 문장)도 그 문장 것으로 본다 — 드묾, 운영에 넣을 때 misattr dev.py 의 sentences() 로
    refs = list(dict.fromkeys(_CITED.findall(s)))
    use = refs or grp[(src, sid.rsplit(".", 1)[0])]
    bl = blocks(row(*key))
    rec = {"src": src, "key": list(key), "sid": sid, "sent": s, "label": lab, "refs": refs, "scope": "인용" if refs else "결론 전체"}
    if not use:
        rec["skip"] = "결론에 인용 없음"
    elif any(p not in bl for p in use):
        rec["skip"] = "컨텍스트 밖"
    return rec, "\n\n".join(bl.get(p, "") for p in use)


if __name__ == "__main__":
    arm = sys.argv[1]; xs, dup, grp = items()
    if arm == "count":
        recs = [prepare(it, grp)[0] for it in xs]
        print("중복 뺌", dict(dup))
        for src in dict.fromkeys(r["src"] for r in recs):
            z = [r for r in recs if r["src"] == src]
            print(src, len(z), {sc: dict(collections.Counter(r["label"] for r in z if r["scope"] == sc)) for sc in ("인용", "결론 전체")},
                  "건너뜀", dict(collections.Counter((r["skip"], r["label"]) for r in z if "skip" in r)))
        for sc in ("인용", "결론 전체"):
            z = [r for r in recs if r["scope"] == sc and "skip" not in r]
            print(sc, "검사", len(z), dict(collections.Counter(r["label"] for r in z)))
        sys.exit()
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_ollama import ChatOllama

    from core.config.agent_config import RAG_ANSWER_MODEL, ollama_kwargs

    model = os.getenv("RAG_HELPER_MODEL", "").strip() or RAG_ANSWER_MODEL
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=NUM_PREDICT[arm]))
    path = D / f"results_{arm}.jsonl"
    done = {(x["src"], x["sid"]) for x in map(json.loads, open(path))} if path.exists() else set()
    with open(path, "a") as w:
        for it in xs:
            if (it[0], it[2]) in done:
                continue
            rec, bl = prepare(it, grp)
            if "skip" not in rec:
                t0 = time.time()
                try:
                    raw = str(llm.invoke([SystemMessage(content=SYSTEM),
                                          HumanMessage(content=PROMPT[arm].format(blocks=bl, sentence=rec["sent"]))]).content or "")
                except Exception as exc:  # 못 읽음과 같게 — 남김
                    raw = f"호출 실패: {type(exc).__name__}: {str(exc)[:120]}"
                m = _VERDICT.search(raw)
                rec.update(model=model, verdict=m.group(1) if m else "", raw=raw[:600], sec=round(time.time() - t0, 2))
            w.write(json.dumps(rec, ensure_ascii=False) + "\n"); w.flush()
            print(arm, rec["src"], rec["sid"], rec["label"], rec.get("verdict", rec.get("skip")), rec.get("sec", ""), flush=True)
