"""답변 인용 arXiv ID 를 링크로 (전송 직전)."""

from apps.telegram_bot.agent_telegram import linkify_arxiv_html, no_link_preview, rag_structured_lines_to_html


def test_linkify_bracketed_ids():
    html = rag_structured_lines_to_html("1. **HADES**: 가속기 [2412.19925v2][2610.08678]")
    out = linkify_arxiv_html(html)
    assert '[<a href="https://arxiv.org/abs/2412.19925v2">2412.19925v2</a>]' in out
    assert '[<a href="https://arxiv.org/abs/2610.08678">2610.08678</a>]' in out
    assert "<b>HADES</b>" in out


def test_leaves_numbers_alone():
    s = "정확도 79.6% · 거리 0.3840 · 2024.12 발표 · (2412.19925)"
    assert linkify_arxiv_html(s) == s


def test_preview_disabled():
    assert no_link_preview()["link_preview_options"].is_disabled is True
