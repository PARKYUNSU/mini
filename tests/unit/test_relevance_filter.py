"""관련 문서 거르기의 응답 해석 · 안전장치 (docs/experiments/relevance_filter_1022)."""

from core.llm.relevance_filter import _brief, filter_relevant, parse_relevant


def test_parse_relevant():
    assert parse_relevant("관련: 1, 3", 5) == {1, 3}
    assert parse_relevant("답: 관련: 없음", 5) == set()
    assert parse_relevant("관련: 7", 5) is None  # 범위 밖뿐 → 못 읽음
    assert parse_relevant("모르겠다", 5) is None


def test_single_block_not_called():
    assert filter_relevant("q", "[2401.00001v1] A\n초록", "x") == ("[2401.00001v1] A\n초록", "대상 아님")


def test_brief_skips_header():
    b = "[Distance: 0.3]\n[발행일: 2026-01-01]\n[2410.14641v3] LongPiBench\n[초록] Positional bias in long context."
    assert _brief(2, b) == "[2] LongPiBench\n[초록] Positional bias in long context."
