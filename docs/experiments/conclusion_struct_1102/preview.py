"""conclusion_struct_1102 미리보기 — R5: 결론을 9B 종합 문장 대신 논문마다 초록 결과 한 줄로.

운영 코드는 안 바꾼다. 저장된 dev 답의 결론만 바꿔 전·후를 preview.md 에 적는다.
- 답: e2e_ko_1008/results/recheck_1031.jsonl(실사용 R_137~139 10-31 재질문) · weekly_20261101.jsonl(real40). held-out 은 안 쓴다.
- 대상: 지금 결론 다시 쓰기와 같게 본론이 2편 이상 인용한 답.
- 한 줄: 그 논문 초록에서 결과 문장 하나 — extract_findings 와 같은 점수(첫 문장 빼고 수치 2 + 결과 동사 1, 같으면 뒤쪽).
- 갈래 A: 본론 인용 논문마다 그 문장 영어 그대로.
- 갈래 B: 같은 줄을 RAG_ANSWER_MODEL 로 번역만(질문은 안 보여 줌) — 원문 밖 숫자 · 한자 · 여러 줄 · 영어 부정어가 번역에서
  빠지면 영어로 둔다.
- 갈래 C(혼합): 지금 결론에서 인용 붙은 문장만 그 논문 B 줄로 바꾸고(논문마다 한 번), 인용 없는 문장(직답 · 대비)은 그대로.
- 갈래 D(바꿔 끼우기): C 와 같되, 인용 붙은 문장마다 그 논문 블록(초록 + 본문 조각)에서 9B 문장과 숫자 · 영어 낱말이
  가장 많이 겹치는 원문 문장을 골라 번역해 넣는다 — C 의 줄은 질문과 상관없이 골라 N11 처럼 답이 되는 문장을 놓쳤다.

    .venv/bin/python docs/experiments/conclusion_struct_1102/preview.py R_137 R_139 N04 C08 N11 C09
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.config.agent_config import RAG_ANSWER_MODEL, ollama_kwargs  # noqa: E402
from core.llm.answer_fix import _CITED, _find  # noqa: E402
from core.llm.conclusion_rewrite import _RESULT_NUM, _RESULT_RE, _bare, _sentences, cited_blocks  # noqa: E402
from core.llm.lang_guard import hanzi_count  # noqa: E402

D = Path(__file__).resolve().parent
EXP = ROOT / "docs" / "experiments"
FILES = ("recheck_1031", "weekly_20261101")
QFILES = ("corpus_llmeval_1030/questions.tsv", "real_eval_1013/questions.tsv")
_TITLE = re.compile(r"^\[(\d{4}\.\d{4,5}(?:v\d+)?)\]\s*(.+)$", re.M)
_ABS = re.compile(r"\[초록\]\s*(.+?)(?:\n\s*\n|\Z)", re.S)
_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_LEAD = re.compile(r"^\s*((?:\[\s*\d{4}\.\d{4,5}(?:v\d+)?\s*\]\s*)+)(?![은는이가의와과에도를을])")  # conclusion_misattr_1025 dev.py
# "may not be a reliable gold standard" → "신뢰할 수 있는 금표준" 처럼 부정이 빠진 번역을 영어로 되돌린다('부재'는 inconsistency 번역이라 안 셈)
_NEG_EN = re.compile(r"\b(?:not|no|never|without|cannot|neither|nor|unable|fails?|failed|lacks?)\b|n't", re.I)
_NEG_KO = re.compile(r"않|없|못|아니|불가|실패|부족|결여")
# 겹침 셈: 모델 이름 속 숫자(GPT-4 · Llama-3)는 숫자로 안 센다
_NUMTOK = re.compile(r"(?<![A-Za-z])(?<![A-Za-z]-)\d+(?:[.,]\d+)?")
_LATIN = re.compile(r"[A-Za-z][A-Za-z0-9\-]{2,}")

SYSTEM = "너는 논문 문장 번역가다. 주어진 영어 문장 하나만 한국어로 옮긴다."
PROMPT = """다음 영어 문장을 한국어 한 문장으로 번역하라.
- 뜻을 더하거나 빼지 마라. 문장에 없는 대상·조건·평가를 붙이지 마라.
- 숫자·고유명사·모델 이름·지표 이름은 원문 그대로 쓴다.
- 번역문만 출력한다.

{sentence}"""


def best_result(abstract: str) -> str:
    """초록의 결과 문장 하나. 고를 문장이 없으면 마지막 문장."""
    sents = _sentences(abstract.replace("\\%", "%"))
    score = {i: 2 * bool(_RESULT_NUM.search(x)) + bool(_RESULT_RE.search(x)) for i, x in enumerate(sents) if i}
    top = sorted((i for i in score if score[i]), key=lambda i: (-score[i], -i))
    return sents[top[0]] if top else (sents[-1] if sents else "")


def sentences(text: str) -> list[str]:
    """문장으로 나누되, 문장 앞에 붙은 인용([id]…)은 앞 문장 것으로 돌린다 (conclusion_misattr_1025 dev.py)."""
    out = []
    for x in re.split(r"(?<=[.!?。])\s+|\n+", text):
        m = _LEAD.match(x)
        if m and out:
            out[-1] += " " + m.group(1).strip()
            x = x[m.end():]
        if x.strip():
            out.append(x.strip())
    return out


def doc_map(r: dict) -> dict[int, str]:
    return {i + 1: p for i, p in enumerate(r["doc_ids"])}


def paper_lines(answer: str, ctx: str, doc_ids: dict[int, str]) -> list[tuple[str, str, str]]:
    """본론에 처음 인용된 순서로 ``(ID, 제목, 결과 문장)``."""
    b, c = _find("본론", answer), _find("결론", answer)
    body = answer[b.end():c.start()]
    out = []
    for blk in cited_blocks(answer, ctx, doc_ids).values():
        t = _TITLE.search(blk)
        if not t:
            continue
        a = _ABS.search(blk)
        out.append((body.find(_bare(t.group(1))), t.group(1), t.group(2).strip(), best_result(a.group(1) if a else blk[t.end():])))
    return [x[1:] for x in sorted(out)]


def translate(llm, sentence: str) -> tuple[str, str]:
    """``(번역, 탈락 사유)``. 탈락이면 번역 자리에 원문."""
    from langchain_core.messages import HumanMessage, SystemMessage

    try:
        msg = [SystemMessage(content=SYSTEM), HumanMessage(content=PROMPT.format(sentence=sentence))]
        text = str(llm.invoke(msg).content or "").strip()
    except Exception as exc:  # 미리보기라 멈추지 않고 영어로 둔다
        return sentence, f"호출 실패 {type(exc).__name__}"
    src = set(_NUM.findall(sentence))
    extra = [n for n in _NUM.findall(text) if n not in src]
    if extra:
        return sentence, f"원문 밖 숫자 {extra[0]}"
    if hanzi_count(text):
        return sentence, "한자"
    if not text or "\n" in text:
        return sentence, "꼴"
    if _NEG_EN.search(sentence) and not _NEG_KO.search(text):
        return sentence, f"부정어 빠짐 — 번역은 「{text}」"
    return text, ""


def conclusion(answer: str) -> str:
    c = _find("결론", answer)
    return re.split(r"\n\s*<b>", answer[c.end():].strip())[0].strip() if c else ""


def hybrid(concl: str, line: dict[str, str]) -> list[str]:
    """C: 인용 붙은 문장은 그 논문 줄로(논문마다 한 번), 인용 없는 문장은 그대로. 본론 밖 논문 인용 문장은 뺀다."""
    out, used = [], set()
    for s in sentences(concl):
        ids = _CITED.findall(s)
        if not ids:
            out.append(f"(그대로) {s}")
            continue
        for i in ids:
            if i in line and i not in used:
                used.add(i)
                out.append(f"(초록) {line[i]}")
            elif i not in line:
                out.append(f"(뺌 — 본론 밖 논문 {i}) {s}")
    return out


def snap(claim: str, blk: str) -> str:
    """D: 9B 인용 문장과 숫자(3점) · 영어 낱말(1점)이 가장 많이 겹치는 블록 원문 문장. 같으면 앞(초록) · 겹침 0 이면 초록 결과 문장."""
    claim = _CITED.sub("", claim)
    nums, words = set(_NUMTOK.findall(claim)), {w.lower() for w in _LATIN.findall(claim)}
    t = _TITLE.search(blk)
    best, top = "", 0
    for s in _sentences(blk[t.end():].replace("\\%", "%")) if t else []:
        k = 3 * len(nums & set(_NUMTOK.findall(s))) + len(words & {w.lower() for w in _LATIN.findall(s)})
        if k > top:
            best, top = s, k
    if best:
        return best
    a = _ABS.search(blk)
    return best_result(a.group(1) if a else blk[t.end():] if t else blk)


def swap(concl: str, blocks: dict[str, tuple[str, str, str]], tr) -> list[str]:
    """D: 인용 붙은 문장은 논문마다 ``snap`` 한 원문 문장(번역)으로, 인용 없는 문장은 그대로. ``blocks`` 는 ID 앞부분 → (ID, 제목, 블록)."""
    out, seen = [], set()
    for s in sentences(concl):
        ids = _CITED.findall(s)
        if not ids:
            out.append(f"(그대로) {s}")
        for i in ids:
            if i not in blocks:
                out.append(f"(뺌 — 본론 밖 논문 {i}) {s}")
                continue
            pid, title, blk = blocks[i]
            src = snap(s, blk)
            if (i, src) not in seen:
                seen.add((i, src))
                ko, why = tr(src)
                out.append(f"(원문) {title} — {ko} [{pid}]" + (f" (영어로 둠: {why})" if why else ""))
    return out


def main() -> None:
    assert snap("자기 선호 편향이 GPT-4 에서 40% 였다[2401.00001v1].",
                "[2401.00001v1] T\n[초록] Intro sentence is here. GPT-4 shows bias. Bias was 40% across models.") == \
        "Bias was 40% across models."
    assert best_result("Background here is long enough. We propose X for long docs. "
                       "X improves recall by 12% on BEIR. We release code for everyone.") == "X improves recall by 12% on BEIR."
    assert sentences("A 는 좋다. [2401.00001v1] 따라서 B 다. [2401.00002]는 C 다.") == \
        ["A 는 좋다. [2401.00001v1]", "따라서 B 다.", "[2401.00002]는 C 다."]
    q = {}
    for f in QFILES:
        for line in (EXP / f).open(encoding="utf-8"):
            if "\t" in line:
                k, v = line.rstrip("\n").split("\t", 1)
                q[k] = v
    rows = {}
    for f in FILES:
        for line in (EXP / "e2e_ko_1008" / "results" / f"{f}.jsonl").open(encoding="utf-8"):
            r = json.loads(line)
            rows[r["id"]] = r
    # 모양: 답마다 결론 줄 수 = 본론 인용 논문 수 · C 가 바꾸는 문장(인용 붙은 문장) 비율
    nlines, cited, uncited = Counter(), 0, 0
    for r in rows.values():
        if not (r.get("answer") and r.get("numbered_context")):
            continue
        n = len(cited_blocks(r["answer"], r["numbered_context"], doc_map(r)))
        nlines[n] += 1
        if n >= 2:
            ss = sentences(conclusion(r["answer"]))
            cited += sum(1 for s in ss if _CITED.search(s))
            uncited += sum(1 for s in ss if not _CITED.search(s))
    from langchain_ollama import ChatOllama

    llm = ChatOllama(**ollama_kwargs(model=RAG_ANSWER_MODEL, temperature=0.0, seed=0, reasoning=False, num_predict=300))
    md = ["# R5 미리보기 — 결론을 논문마다 초록 결과 한 줄로 (운영 변경 없음)", "",
          f"답 {sum(nlines.values())}개(recheck_1031 3 + weekly_20261101 real40)의 본론 인용 논문 수 = A · B 결론 줄 수: "
          + " · ".join(f"{k}편 {v}답" for k, v in sorted(nlines.items())) + ".",
          "지금 결론 다시 쓰기처럼 2편 이상만 바꾼다(1편 답은 그대로).",
          f"2편 이상 답의 지금 결론 문장: 인용 붙음 {cited} · 인용 없음 {uncited} — C 는 앞쪽만 바꾼다.", ""]
    cache, tsec = {}, [0.0]

    def tr(sent: str) -> tuple[str, str]:
        if sent not in cache:
            t0 = time.monotonic()
            cache[sent] = translate(llm, sent)
            tsec[0] += time.monotonic() - t0
        return cache[sent]

    for qid in sys.argv[1:]:
        r = rows[qid]
        rw = sum(s for name, s in r.get("stages") or [] if name == "rewrite")
        lines = paper_lines(r["answer"], r["numbered_context"], doc_map(r))
        ko = {pid: tr(sent) for pid, _, sent in lines}
        blocks = {}
        for blk in cited_blocks(r["answer"], r["numbered_context"], doc_map(r)).values():
            t = _TITLE.search(blk)
            if t:
                blocks.setdefault(_bare(t.group(1)), (t.group(1), t.group(2).strip(), blk))
        md += [f"## {qid} — {q.get(qid, '')}", "", f"**지금 결론** (운영 · 9B v2 다시 쓰기 {rw:.1f}s)", "", conclusion(r["answer"]), "",
               "**A 논문별 한 줄 · 영어 원문**", ""]
        md += [f"- {title} — {sent} [{pid}]" for pid, title, sent in lines]
        md += ["", "**B 논문별 한 줄 · 9B 번역만 (질문은 안 보여 줌)**", ""]
        md += [f"- {title} — {ko[pid][0]} [{pid}]" + (f" (영어로 둠: {ko[pid][1]})" if ko[pid][1] else "") for pid, title, sent in lines]
        md += ["", "**C 혼합 — 인용 붙은 문장만 B 줄로**", ""]
        md += [f"- {x}" for x in hybrid(conclusion(r["answer"]), {_bare(pid): f"{title} — {ko[pid][0]} [{pid}]" for pid, title, _ in lines})]
        md += ["", "**D 바꿔 끼우기 — 인용 붙은 문장을 9B 문장과 가장 겹치는 원문 문장으로**", ""]
        md += [f"- {x}" for x in swap(conclusion(r["answer"]), blocks, tr)]
        md.append("")
    md.append(f"번역 호출 {len(cache)}번 총 {tsec[0]:.1f}s (모델 {RAG_ANSWER_MODEL})")
    (D / "preview.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
