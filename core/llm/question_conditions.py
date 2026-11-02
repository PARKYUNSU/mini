"""질문의 기간 · 편수 조건을 규칙으로 뽑아 대조한다 (docs/experiments/qcond_rule_1025).

왜: qcond_1025 기준선에서 블록에 ``[발행일: …]`` 이 있는데도 2024 · 2025 논문을 "2026년 연구"로 소개했고
(기간 조건 3 중 2 문제), "6편"을 요청받아 5편을 내고도 밝히지 않았다(편수 5 중 2 문제). 둘 다 형태가 정해진
조건이라 LLM 없이 대조한다: 기간은 답 전에 블록을 발행일로 거르고, 편수는 본론 항목이 모자라면 고지를 붙인다.
"""

from __future__ import annotations

import re
from datetime import date

from core.llm.answer_fix import _find
from core.llm.citation_fix import RAG_HIT_SEP

__all__ = ["year_condition", "filter_by_year", "requested_count", "count_notice"]

_RANGE = re.compile(r"(20\d\d)\s*년?\s*(?:~|-|–|부터)\s*(20\d\d)\s*년")
_YEAR = re.compile(r"(20\d\d)\s*년\s*(이후|부터|이전|전에|전|까지)?")
_REL = re.compile(r"(재작년|작년|지난해|올해|금년)\s*(이후|부터|이전|전에|전|까지)?")
_REL_YEARS = {"재작년": -2, "작년": -1, "지난해": -1, "올해": 0, "금년": 0}
_DATE = re.compile(r"\[발행일:\s*(\d{4})-")
# 요청 동사가 바로 따를 때만 편수다 — "예시를 3개 넣을 때" · "5편에서 10편으로" · "상위 10개 중"은 아니다(qtype_1102 §6.2)
_COUNT = re.compile(r"(?<![\d.])(\d{1,2})\s*(?:개|편)\s*(?:의\s*)?(?:논문|연구)?\s*(?:만|정도|쯤)?\s*(?:을|를)?\s*"
                    r"(?:찾|알려|골라|고르|뽑|추천|정리|보여|소개|요약|비교|설명|나열|줘|주세요)")
_ITEM = re.compile(r"^\s*(?:<b>)?\d+\.\s", re.M)


def year_condition(question: str, this_year: int | None = None) -> tuple[int | None, int | None] | None:
    """발행 연도 범위 ``(처음, 끝)``(포함, 열린 쪽은 None) 또는 None.

    "2024년 이전"은 (None, 2023), "2024년까지"는 (None, 2024), "2023~2026년"은 (2023, 2026), "작년"은 올해 − 1.
    """
    if m := _RANGE.search(question):
        lo, hi = sorted(int(g) for g in m.groups())
        return lo, hi
    if m := _YEAR.search(question):
        y = int(m.group(1))
    elif m := _REL.search(question):
        y = (this_year or date.today().year) + _REL_YEARS[m.group(1)]
    else:
        return None
    word = m.group(2) or ""
    if word in ("이후", "부터"):
        return y, None
    if word in ("이전", "전에", "전"):
        return None, y - 1
    return (None, y) if word == "까지" else (y, y)


def _ok(year: int, cond: tuple[int | None, int | None]) -> bool:
    lo, hi = cond
    return (lo is None or year >= lo) and (hi is None or year <= hi)


def filter_by_year(question: str, context: str) -> tuple[str, str]:
    """``(컨텍스트, 상태)``. 상태: "대상 아님" · "a→b" · "맞는 문서 없음"(그때는 그대로 둔다)."""
    cond = year_condition(question)
    if not cond:
        return context, "대상 아님"
    blocks = [b for b in context.split(RAG_HIT_SEP) if b.strip()]
    keep = [b for b in blocks if (m := _DATE.search(b)) and _ok(int(m.group(1)), cond)]
    if not keep:
        return context, "맞는 문서 없음"
    return RAG_HIT_SEP.join(keep), f"{len(blocks)}→{len(keep)}"


def requested_count(question: str) -> int | None:
    """질문이 요청한 편수(2–10) 또는 None."""
    m = _COUNT.search(question)
    return int(m.group(1)) if m and 2 <= int(m.group(1)) <= 10 else None


def _period(cond: tuple[int | None, int | None]) -> str:
    lo, hi = cond
    if lo == hi:
        return f"{lo}년"
    if hi is None:
        return f"{lo}년 이후"
    return f"{hi}년까지" if lo is None else f"{lo}~{hi}년"


def count_notice(question: str, answer: str, year_status: str = "") -> tuple[str, str]:
    """``(답, 붙인 고지)``. 본론 항목이 요청 편수보다 적거나, 기간에 맞는 문서가 없었으면 답 맨 앞에 한 줄 붙인다."""
    notes = []
    if year_status == "맞는 문서 없음" and (cond := year_condition(question)):
        notes.append(f"요청한 기간({_period(cond)})에 나온 논문은 찾지 못해, 기간 밖 논문으로 답했습니다.")
    n = requested_count(question)
    b, c = _find("본론", answer), _find("결론", answer)
    if n and b:
        m = len(_ITEM.findall(answer[b.end():c.start() if c and c.start() > b.end() else len(answer)]))
        if 0 < m < n:
            notes.append(f"요청한 {n}편 중 {m}편만 찾았습니다.")
    if not notes:
        return answer, ""
    note = "※ " + " ".join(notes)
    return note + "\n\n" + answer, note
