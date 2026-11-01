"""결론의 인용 문장을 그 논문 원문 문장(번역)으로 바꿔 끼운다 (RAG_CONCLUSION_SWAP, docs/experiments/conclusion_struct_1102).

왜 따로 쓰나: 결론 오류(질문 전제 섞임 · 결과 뒤집기 · 남의 수치 붙이기)는 9B 가 논문 결과를 제 말로 옮길 때 생겼다
(answer_review_1030 · conclusion_verify_1101). 무엇을 말할지는 9B 결론을 따르고, 말은 그 논문 블록에서 9B 문장과 가장
많이 겹치는 원문 문장으로 바꾼다. 인용 없는 문장(직답 · 대비)은 둔다 — 논문별 한 줄만 쓰면 직답과 대비를 잃었다(미리보기).
"""

from __future__ import annotations

import re
import time
from typing import Callable

from core.llm.answer_fix import _CITED, _find
from core.llm.conclusion_rewrite import _RESULT_NUM, _RESULT_RE, _bare, _sentences, cited_blocks
from core.llm.lang_guard import hanzi_count

__all__ = ["best_result", "check_translation", "first_person", "sentences", "snap", "swap_conclusion"]

SYSTEM = "너는 논문 문장 번역가다. 주어진 영어 문장 하나만 한국어로 옮긴다."

PROMPT = """다음 영어 문장을 한국어 한 문장으로 번역하라.
- 뜻을 더하거나 빼지 마라. 문장에 없는 대상·조건·평가를 붙이지 마라.
- 숫자·고유명사·모델 이름·지표 이름은 원문 그대로 쓴다.
- 1인칭(we · our)은 '이 논문은' · '이 논문의'로 옮긴다.
- 번역문만 출력한다.

{sentence}"""

_TITLE = re.compile(r"^\[(\d{4}\.\d{4,5}(?:v\d+)?)\]\s*(.+)$", re.M)
_ABS = re.compile(r"\[초록\]\s*(.+?)(?:\n\s*\n|\Z)", re.S)
_NUM = re.compile(r"\d+(?:[.,]\d+)?")
# 겹침 셈: 모델 이름 속 숫자(GPT-4 · Llama-3)는 숫자로 안 센다
_NUMTOK = re.compile(r"(?<![A-Za-z])(?<![A-Za-z]-)\d+(?:[.,]\d+)?")
_LATIN = re.compile(r"[A-Za-z][A-Za-z0-9\-]{2,}")
_LEAD = re.compile(r"^\s*((?:\[\s*\d{4}\.\d{4,5}(?:v\d+)?\s*\]\s*)+)(?![은는이가의와과에도를을])")  # conclusion_misattr_1025 dev.py
# "may not be a reliable gold standard" → "신뢰할 수 있는 금표준" 처럼 부정이 빠진 번역은 영어로 둔다('부재'는 inconsistency 번역이라 안 셈)
_NEG_EN = re.compile(r"\b(?:not|no|never|without|cannot|neither|nor|unable|fails?|failed|lacks?)\b|n't", re.I)
_NEG_KO = re.compile(r"않|없|못|아[니닌닐님]|불가|실패|부족|결여")  # '아닐' 은 '아니' 를 글자로 안 품는다
_END = re.compile(r"\n\s*(?:<b>|📎)")  # 결론 단락 끝: 다음 머리 · 외부 검색 줄
# 1인칭 지시를 9B 가 안 따랐다(dev 점검: "우리는 …") → 번역 뒤 글자로 바꾼다
_WE = re.compile(r"우리(는|의|가|를)")
_WE_TO = {"는": "은", "의": "의", "가": "이", "를": "을"}


def best_result(abstract: str) -> str:
    """초록의 결과 문장 하나 — extract_findings 와 같은 점수(첫 문장 빼고 수치 2 + 결과 동사 1, 같으면 뒤쪽). 없으면 마지막 문장."""
    sents = _sentences(abstract.replace("\\%", "%"))
    score = {i: 2 * bool(_RESULT_NUM.search(x)) + bool(_RESULT_RE.search(x)) for i, x in enumerate(sents) if i}
    top = sorted((i for i in score if score[i]), key=lambda i: (-score[i], -i))
    return sents[top[0]] if top else (sents[-1] if sents else "")


def sentences(text: str) -> list[str]:
    """문장으로 나누되, 문장 앞에 붙은 인용([id]…)은 앞 문장 것으로 돌린다."""
    out = []
    for x in re.split(r"(?<=[.!?。])\s+|\n+", text):
        m = _LEAD.match(x)
        if m and out:
            out[-1] += " " + m.group(1).strip()
            x = x[m.end():]
        if x.strip():
            out.append(x.strip())
    return out


def snap(claim: str, blk: str) -> str:
    """9B 인용 문장과 숫자(3점) · 영어 낱말(1점)이 가장 많이 겹치는 블록 원문 문장. 같으면 앞(초록) · 0점이면 초록 결과 문장."""
    claim = _CITED.sub("", claim)
    nums, words = set(_NUMTOK.findall(claim)), {w.lower() for w in _LATIN.findall(claim)}
    t = _TITLE.search(blk)
    text = blk[t.end():] if t else blk
    best, top = "", 0
    for s in _sentences(text.replace("\\%", "%")):
        k = 3 * len(nums & set(_NUMTOK.findall(s))) + len(words & {w.lower() for w in _LATIN.findall(s)})
        if k > top:
            best, top = s, k
    if best:
        return best
    a = _ABS.search(blk)
    return best_result(a.group(1) if a else text)


def first_person(text: str) -> str:
    """'우리는 · 우리의 · 우리가 · 우리를' → '이 논문은 · 이 논문의 · 이 논문이 · 이 논문을'."""
    return _WE.sub(lambda m: "이 논문" + _WE_TO[m.group(1)], text)


def check_translation(src: str, text: str) -> str:
    """통과면 "", 아니면 영어 원문을 쓸 사유."""
    extra = [n for n in _NUM.findall(text) if n not in set(_NUM.findall(src))]
    if extra:
        return f"원문 밖 숫자 {extra[0]}"
    if hanzi_count(text):
        return "한자"
    if not text or "\n" in text:
        return "꼴"
    if _NEG_EN.search(src) and not _NEG_KO.search(text):
        return "부정어 빠짐"
    return ""


def _translator(model: str) -> Callable[[str], str]:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=300))

    def tr(sentence: str) -> str:
        msg = [SystemMessage(content=SYSTEM), HumanMessage(content=PROMPT.format(sentence=sentence))]
        return str(llm.invoke(msg).content or "").strip()

    return tr


def swap_conclusion(
    answer: str, numbered_context: str, doc_ids: dict[int, str], model: str,
    translate: Callable[[str], str] | None = None,
) -> tuple[str, str, dict]:
    """``(답, 상태, 기록)``. 상태: "바꿈 N"(바꾼 인용 문장 수) · "대상 아님" · "인용 문장 없음". 기록은 측정용."""
    info: dict = {"pairs": [], "dropped": 0, "fallback": [], "tsec": 0.0}
    blocks = cited_blocks(answer, numbered_context, doc_ids)
    c = _find("결론", answer)
    if len(blocks) < 2 or not c:
        return answer, "대상 아님", info
    rest = answer[c.end():]
    m = _END.search(rest)
    par, tail = (rest[:m.start()], rest[m.start():]) if m else (rest, "")
    sents = sentences(par.strip())
    if not any(_CITED.search(s) for s in sents):
        return answer, "인용 문장 없음", info
    by_id: dict[str, tuple[str, str]] = {}
    for blk in blocks.values():
        t = _TITLE.search(blk)
        if t:
            by_id.setdefault(_bare(t.group(1)), (t.group(1), blk))
    tr = translate or _translator(model)
    out, seen = [], set()
    for s in sents:
        ids = _CITED.findall(s)
        if not ids:
            out.append(s)
            continue
        after = []
        for i in ids:
            if i not in by_id:  # 본론 밖 논문 인용 — 다시 쓰기 검사가 막으므로 드물다
                info["dropped"] += 1
                continue
            pid, blk = by_id[i]
            src = snap(s, blk)
            if (i, src) in seen:
                continue
            seen.add((i, src))
            t0 = time.monotonic()
            try:
                ko = first_person(tr(src))
                why = check_translation(src, ko)
            except Exception as exc:  # 번역을 못 해도 원문 문장은 넣는다
                ko, why = "", f"호출 실패 {type(exc).__name__}"
            info["tsec"] += time.monotonic() - t0
            if why:
                info["fallback"].append(why)
            after.append(f"{src if why else ko} [{pid}]")
        info["pairs"].append({"before": s, "after": after, "ids": ids})
        out += after
    return answer[:c.end()] + "\n" + " ".join(out) + (tail or "\n"), f"바꿈 {len(info['pairs'])}", info
