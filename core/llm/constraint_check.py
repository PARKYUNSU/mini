"""평가 문항의 **기계 검증 가능한 제약**을 검사한다 (지시 따르기 측정).

왜 필요한가 — 잡담·계획·RAG 슬롯의 기존 판정기는 **붕괴 탐지기**다
(타임아웃·8자 미만·반복·영어 혼입·think 유출). 내용의 옳고 그름은 보지 않는다.
그래서 base 가 이 세 슬롯에서 0% 이고, 파인튜닝이 **더 나을 자리가 없다**
(docs/experiments/yunsur_v10/05_conclusion.md — 측정의 천장).

여기서 재는 것은 "지시대로 형식을 지켰는가" 다. 파인튜닝이 실제로 영향을 주는
능력이고, base 도 자주 틀린다 — 그래서 헤드룸이 생긴다.

규칙 하나: **사람 판단이 들어가면 안 된다.** 각 검사는 같은 입력에 항상 같은
답을 내야 하고, 문항 텍스트가 제약을 명시해야 한다 (숨은 제약은 함정이다).
"""

from __future__ import annotations

import json
import re

# 코드펜스로 감싼 출력도 내용으로 본다 (형식 지시를 지켰는지는 안쪽으로 판단).
_FENCE_RE = re.compile(r"^\s*```[a-zA-Z0-9_+-]*\s*\n(.*?)\n?\s*```\s*$", re.DOTALL)

KNOWN_KEYS = (
    "exact_lines",
    "max_lines",
    "max_chars_per_line",
    "max_chars",
    "json_only",
    "must_include",
    "must_exclude",
)


def strip_fence(text: str) -> str:
    """전체를 감싼 코드펜스 한 겹만 벗긴다. 펜스가 없으면 원문 그대로."""
    m = _FENCE_RE.match(text or "")
    return m.group(1) if m else (text or "")


def _lines(text: str) -> list[str]:
    """비어 있지 않은 줄만. 모델이 넣는 빈 줄로 줄 수 판정이 흔들리지 않게 한다."""
    return [ln.strip() for ln in (text or "").splitlines() if ln.strip()]


def check_constraints(text: str, constraints: dict | None) -> tuple[bool, str]:
    """(ok, kind). 위반하면 ``constraint:<키>`` 를 돌려준다.

    제약이 없으면 항상 통과다 — 기존 문항은 이 함수를 지나도 결과가 변하지 않는다.
    여러 개를 위반해도 **첫 번째만** 보고한다 (실패 종류를 하나로 세기 위해).
    """
    if not constraints:
        return True, ""
    body = strip_fence(text or "").strip()

    for key in constraints:
        if key not in KNOWN_KEYS:
            raise ValueError(f"모르는 제약 키: {key!r} (아는 키: {', '.join(KNOWN_KEYS)})")

    if "json_only" in constraints and constraints["json_only"]:
        try:
            json.loads(body)
        except Exception:
            return False, "constraint:json_only"

    if "exact_lines" in constraints:
        if len(_lines(body)) != int(constraints["exact_lines"]):
            return False, "constraint:exact_lines"

    if "max_lines" in constraints:
        if len(_lines(body)) > int(constraints["max_lines"]):
            return False, "constraint:max_lines"

    if "max_chars_per_line" in constraints:
        limit = int(constraints["max_chars_per_line"])
        if any(len(ln) > limit for ln in _lines(body)):
            return False, "constraint:max_chars_per_line"

    if "max_chars" in constraints:
        if len(body) > int(constraints["max_chars"]):
            return False, "constraint:max_chars"

    if "must_include" in constraints:
        for needle in constraints["must_include"]:
            if needle not in body:
                return False, "constraint:must_include"

    if "must_exclude" in constraints:
        low = body.lower()
        for needle in constraints["must_exclude"]:
            if needle.lower() in low:
                return False, "constraint:must_exclude"

    return True, ""
