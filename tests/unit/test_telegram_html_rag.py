"""RAG → Telegram HTML 변환 (파싱 이스케이프·줄바꿈 유지)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

import apps.telegram_bot.agent_telegram as agent_telegram  # noqa: E402


def test_rag_structured_lines_to_html_escapes_special_chars():
    md = "### 핵심 주제\n- A & B <test>\n\n### 주요 방법론\n- C"
    h = agent_telegram.rag_structured_lines_to_html(md)
    assert "<b>핵심 주제</b>" in h
    assert "A &amp; B" in h
    assert "&lt;test&gt;" in h
    assert "\n" in h


def test_escape_telegram_html_basic():
    assert agent_telegram.escape_telegram_html("a<b>c") == "a&lt;b&gt;c"


def test_rag_structured_lines_to_html_markdown_bold_section():
    md = "**1. 핵심 주제**\n- 내용 A\n**2. 주요 방법론**\n- 내용 B"
    h = agent_telegram.rag_structured_lines_to_html(md)
    assert "<b>1. 핵심 주제</b>" in h
    assert "<b>2. 주요 방법론</b>" in h
    assert "내용 A" in h


def test_rag_structured_lines_to_html_preserves_html_bold():
    md = "<b>📄 논문 제목:</b> A & B <x>\n- 후속 <b>강조</b> 끝"
    h = agent_telegram.rag_structured_lines_to_html(md)
    assert "<b>📄 논문 제목:</b>" in h
    assert "A &amp; B" in h
    assert "&lt;x&gt;" in h
    assert "<b>강조</b>" in h
    assert "• 후속 " in h


def test_multi_doc_body_item_is_not_wholly_bolded():
    """다중 문서 템플릿의 본론 항목은 **줄째 굵게 하면 안 된다.**

    운영 실행에서 `1. **RAGStack** 프레임워크는 …` 전체가 <b> 로 감싸이고 내부
    `**…**` 가 리터럴 별표로 남았다 (docs/experiments/template_collapse_1006/).
    옛 단일 논문 템플릿의 짧은 섹션 제목(`1. 핵심 주제`)과 가려야 한다.
    """
    line = "1. **RAGStack**: 다섯 모듈을 통합해 실행 가능한 파이프라인을 만든다.[2408.08067v2]"
    out = agent_telegram.rag_structured_lines_to_html(line)
    assert not out.startswith("<b>1."), out          # 줄째 굵게 아님
    assert "<b>RAGStack</b>" in out                  # 인라인 굵게는 변환됨
    assert "**" not in out                           # 리터럴 별표 없음
    assert "[2408.08067v2]" in out                   # 인용 대괄호 보존


def test_short_numbered_title_still_bolded():
    """단일 논문 템플릿의 섹션 제목은 기존대로 줄째 굵게."""
    for t in ("1. 핵심 주제", "2. 주요 방법론", "3. 결론 및 의의"):
        out = agent_telegram.rag_structured_lines_to_html(t)
        assert out == f"<b>{t}</b>", out


def test_inline_bold_in_plain_and_bullet_lines():
    assert "<b>굵게</b>" in agent_telegram.rag_structured_lines_to_html("앞 **굵게** 뒤")
    assert "<b>굵게</b>" in agent_telegram.rag_structured_lines_to_html("- 불릿 **굵게** 끝")


def test_angle_brackets_still_escaped_with_inline_bold():
    """인라인 굵게 변환이 이스케이프를 깨뜨리지 않는다."""
    out = agent_telegram.rag_structured_lines_to_html("a < b 이고 **c > d** 이다")
    assert "&lt;" in out and "&gt;" in out
    assert "<b>c &gt; d</b>" in out
