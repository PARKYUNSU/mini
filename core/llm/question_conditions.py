"""질문의 기간 · 편수 조건을 규칙으로 뽑아 대조한다 (docs/experiments/qcond_rule_1025).

왜: qcond_1025 기준선에서 블록에 ``[발행일: …]`` 이 있는데도 2024 · 2025 논문을 "2026년 연구"로 소개했고
(기간 조건 3 중 2 문제), "6편"을 요청받아 5편을 내고도 밝히지 않았다(편수 5 중 2 문제). 둘 다 형태가 정해진
조건이라 LLM 없이 대조한다: 기간은 답 전에 블록을 발행일로 거르고, 편수는 본론 항목이 모자라면 고지를 붙인다.
"""

from __future__ import annotations

import re

from core.llm.answer_fix import _find
from core.llm.citation_fix import RAG_HIT_SEP

__all__ = ["year_condition", "filter_by_year", "requested_count", "count_notice"]

_YEAR = re.compile(r"(20\d\d)\s*년\s*(이후|부터|이전|전에|전|까지)?")
_DATE = re.compile(r"\[발행일:\s*(\d{4})-")
_COUNT = re.compile(r"(?<![\d.])(\d{1,2})\s*(?:개|편)")
_ITEM = re.compile(r"^\s*(?:<b>)?\d+\.\s", re.M)


def year_condition(question: str) -> tuple[str, int] | None:
    """``("eq"|"ge"|"lt"|"le", 연도)`` 또는 None. "2024년 이전"은 2023 까지(lt), "2024년까지"는 2024 까지(le)."""
    m = _YEAR.search(question)
    if not m:
        return None
    op = {"이후": "ge", "부터": "ge", "이전": "lt", "전에": "lt", "전": "lt", "까지": "le"}.get(m.group(2) or "", "eq")
    return op, int(m.group(1))


def _ok(year: int, cond: tuple[str, int]) -> bool:
    op, y = cond
    return {"eq": year == y, "ge": year >= y, "lt": year < y, "le": year <= y}[op]


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


def _period(cond: tuple[str, int]) -> str:
    op, y = cond
    return {"eq": f"{y}년", "ge": f"{y}년 이후", "lt": f"{y}년 이전", "le": f"{y}년까지"}[op]


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
