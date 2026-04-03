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
