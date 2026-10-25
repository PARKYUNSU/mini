"""질문 기간 · 편수 조건 규칙 (docs/experiments/qcond_rule_1025)."""

from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.question_conditions import count_notice, filter_by_year, requested_count, year_condition


def test_year_condition():
    assert year_condition("2026년에 나온 RAG 논문") == ("eq", 2026)
    assert year_condition("2025년 이후 나온 양자화") == ("ge", 2025)
    assert year_condition("2024년 이전 연합학습") == ("lt", 2024)
    assert year_condition("2024년까지 나온") == ("le", 2024)
    assert year_condition("요즘 RAG 연구") is None


def test_filter_by_year():
    ctx = RAG_HIT_SEP.join(["[Distance: 0.1] [발행일: 2026-02-25] [2602.1v1] A", "[발행일: 2024-12-16] [2412.1v1] B"])
    out, st = filter_by_year("2026년에 나온 논문", ctx)
    assert st == "2→1" and "2602.1" in out and "2412.1" not in out
    assert filter_by_year("2023년에 나온 논문", ctx) == (ctx, "맞는 문서 없음")


def test_count_notice():
    assert requested_count("논문 6개 찾아줘") == 6 and requested_count("7B 이하 모델") is None
    ans = "<b>서론</b>\n…\n<b>본론</b>\n1. <b>A</b>: …\n2. <b>B</b>: …\n<b>결론</b>\n…"
    out, note = count_notice("탈옥 방어 논문 6개 찾아줘", ans)
    assert note == "※ 요청한 6편 중 2편만 찾았습니다." and out.startswith(note)
    assert count_notice("논문 2개", ans) == (ans, "")
    _, note = count_notice("2023년에 나온 논문 정리", ans, "맞는 문서 없음")
    assert "2023년" in note
