"""제약 검사 계약 — 같은 입력에 항상 같은 답이 나와야 한다.

이 검사가 흔들리면 실패율이 모델이 아니라 판정기를 반영한다
(docs/experiments/protocol.md §2.4: 도구를 고칠 때는 고친 사실을 센다).

`core/llm/constraint_check.py` 는 의존성이 없어 이 테스트는 가볍다.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

from core.llm.constraint_check import check_constraints, strip_fence  # noqa: E402

pytestmark = pytest.mark.unit


def test_no_constraints_always_passes():
    """기존 54문항은 제약이 없다 — 이 함수를 지나도 결과가 달라지면 안 된다."""
    for text in ("", "아무 말", "```\n코드\n```", "a" * 5000):
        assert check_constraints(text, None) == (True, "")
        assert check_constraints(text, {}) == (True, "")


def test_unknown_key_raises_rather_than_silently_passing():
    """오타 난 제약이 '항상 통과'로 조용히 새면 문항이 무력해진다."""
    with pytest.raises(ValueError):
        check_constraints("아무 말", {"exact_line": 3})


@pytest.mark.parametrize(
    "text,expected",
    [("1\n2\n3", True), ("1\n\n2\n\n3", True), ("1\n2", False), ("1\n2\n3\n4", False)],
)
def test_exact_lines_ignores_blank_lines(text, expected):
    ok, kind = check_constraints(text, {"exact_lines": 3})
    assert ok is expected
    assert kind == ("" if expected else "constraint:exact_lines")


def test_max_lines_and_max_chars_per_line():
    assert check_constraints("가\n나", {"max_lines": 3})[0] is True
    assert check_constraints("가\n나\n다\n라", {"max_lines": 3}) == (False, "constraint:max_lines")
    assert check_constraints("짧은 줄", {"max_chars_per_line": 10})[0] is True
    assert check_constraints("아" * 11, {"max_chars_per_line": 10}) == (False, "constraint:max_chars_per_line")


def test_json_only_accepts_fenced_json():
    """모델이 ```json 으로 감싸는 것은 형식 위반으로 보지 않는다 — 안쪽을 본다."""
    assert check_constraints('{"a": 1}', {"json_only": True})[0] is True
    assert check_constraints('```json\n{"a": 1}\n```', {"json_only": True})[0] is True
    assert check_constraints("설명: {\"a\": 1}", {"json_only": True}) == (False, "constraint:json_only")


def test_must_include_and_exclude():
    assert check_constraints("결론: 지연", {"must_include": ["결론"]})[0] is True
    assert check_constraints("본문만", {"must_include": ["결론"]}) == (False, "constraint:must_include")
    assert check_constraints("한국어만 씁니다", {"must_exclude": ["TODO"]})[0] is True
    assert check_constraints("todo 남김", {"must_exclude": ["TODO"]}) == (False, "constraint:must_exclude")


def test_first_violation_only():
    """실패 종류를 하나로 세기 위해 첫 위반만 보고한다."""
    ok, kind = check_constraints("가\n나\n다\n라", {"exact_lines": 2, "max_chars_per_line": 1})
    assert ok is False
    assert kind == "constraint:exact_lines"


def test_strip_fence_only_removes_one_wrapping_layer():
    assert strip_fence("```python\nx = 1\n```") == "x = 1"
    assert strip_fence("펜스 없음") == "펜스 없음"
    assert "```" in strip_fence("```\n안에 ``` 가 또 있음\n```")
