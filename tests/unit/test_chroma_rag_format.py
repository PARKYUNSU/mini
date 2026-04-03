"""Chroma RAG 컨텍스트 포맷(발행일 주입)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

from core.rag.agent_chroma_rag import _format_chroma_hits, _published_line_from_record  # noqa: E402


def test_published_line_from_record_iso():
    assert _published_line_from_record({"published": "2024-03-15"}) == "[발행일: 2024-03-15]"
    assert _published_line_from_record({"date": "2024-03-15T12:00:00Z"}) == "[발행일: 2024-03-15]"
    assert _published_line_from_record({"published_date": "2020-01-02"}) == "[발행일: 2020-01-02]"
    assert _published_line_from_record({}) == ""


def test_format_chroma_hits_prefixes_date():
    text = _format_chroma_hits(
        ["Abstract body here."],
        [{"paper_id": "1234", "title": "My Paper", "published": "2023-06-01"}],
    )
    assert text.startswith("[발행일: 2023-06-01]")
    assert "[1234]" in text
    assert "My Paper" in text
    assert "Abstract body" in text
