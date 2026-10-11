"""정답 유무 판정 호출 (core.llm.presence_judge) — docs/experiments/presence_integration_1012."""

from __future__ import annotations

from core.llm.presence_judge import NO_DOC_HINT, PROMPT, parse_pick


def test_parse_number():
    assert parse_pick("답: 문서 3") == 3
    assert parse_pick("답: [문서 12]") == 12


def test_parse_none():
    assert parse_pick("생각해 보면…\n답: 없음") == "없음"


def test_parse_bad_format():
    assert parse_pick("문서 3 이 맞습니다") is None
    assert parse_pick("") is None


def test_hint_matches_v13_nogold_format():
    assert "제공된 문서에는 질문이 찾는 연구가 없습니다." in NO_DOC_HINT
    assert "따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다." in NO_DOC_HINT
    assert "(관련 연구)" in NO_DOC_HINT


def test_prompt_placeholders():
    assert "{question}" in PROMPT and "{context}" in PROMPT
