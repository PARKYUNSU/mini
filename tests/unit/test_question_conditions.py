"""질문 기간 · 편수 조건 규칙 (docs/experiments/qcond_rule_1025)."""

from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.question_conditions import count_notice, filter_by_year, requested_count, year_condition


def test_year_condition():
    assert year_condition("2026년에 나온 RAG 논문") == (2026, 2026)
    assert year_condition("2025년 이후 나온 양자화") == (2025, None)
    assert year_condition("2024년 이전 연합학습") == (None, 2023)
    assert year_condition("2024년까지 나온") == (None, 2024)
    assert year_condition("요즘 RAG 연구") is None
    # qtype_1102 §6.2: 범위 · 상대 연도
    assert year_condition("최신 연구(2023~2026년)를 중점적으로") == (2023, 2026)
    assert year_condition("2023년부터 2026년까지 나온 논문") == (2023, 2026)
    assert year_condition("작년에 나온 멀티에이전트 논문", 2026) == (2025, 2025)
    assert year_condition("올해 발표된 RAG 평가 논문", 2026) == (2026, 2026)
    assert year_condition("작년 이후 나온 논문", 2026) == (2025, None)
    assert year_condition("2026-09-16 날짜로 실행해줘") is None


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
    _, note = count_notice("최신 연구(2023~2026년) 찾아줘", ans, "맞는 문서 없음")
    assert "(2023~2026년)" in note


def test_requested_count_needs_request():
    # qtype_1102 §6.2: 질문 속 다른 수를 편수로 읽던 꼴
    assert requested_count("프롬프트에 예시를 3개 넣을 때와 10개 넣을 때 성능 차이가 거의 없었다") is None
    assert requested_count("컨텍스트 문서를 5편에서 10편으로 늘리면 품질이 떨어지는가") is None
    assert requested_count("벡터 검색 결과 상위 10개 중 절반이 같은 문서였다") is None
    assert requested_count("토큰마다 8개 전문가 중 2개로 보내는 희소 MoE") is None
    for q, n in (("연구 3개만 알려줘", 3), ("논문 5개를 찾아주세요", 5), ("5개 논문 추천해줘", 5),
                 ("그래프 RAG 논문 4편 정리해줘", 4), ("3편의 논문을 골라줘", 3)):
        assert requested_count(q) == n, q
