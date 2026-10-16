"""RAG 컨텍스트 블록에 초록 붙이기 (RAG_CONTEXT_ABSTRACT) — docs/experiments/abstract_context_1011."""

from __future__ import annotations

from core.rag import agent_chroma_rag as R

ABS = "We introduce CoPE, a soft clipping of low-frequency RoPE components that removes OOD outliers and scales to 256k context."


def _fmt(doc: str, monkeypatch, on: bool) -> str:
    monkeypatch.setenv("RAG_CONTEXT_ABSTRACT", "1" if on else "0")
    meta = {"paper_id": "2602.05258v1", "title": "CoPE", "abstract": ABS}
    return R._format_chroma_hits([doc], [meta], [0.3])


def test_off_by_default(monkeypatch):
    monkeypatch.delenv("RAG_CONTEXT_ABSTRACT", raising=False)
    out = R._format_chroma_hits(["## Related work\nYaRN scales frequencies."],
                                [{"paper_id": "2602.05258v1", "title": "CoPE", "abstract": ABS}], [0.3])
    assert "[초록]" not in out


def test_adds_abstract_before_excerpt(monkeypatch):
    out = _fmt("## Related work\nYaRN scales frequencies.", monkeypatch, True)
    assert "[2602.05258v1] CoPE\n[초록] We introduce CoPE" in out
    assert out.index("[초록]") < out.index("Related work")


def test_skips_when_excerpt_already_has_abstract(monkeypatch):
    out = _fmt("Abstract\n" + ABS + "\nMore text.", monkeypatch, True)
    assert "[초록]" not in out


def test_truncates_abstract(monkeypatch):
    long_abs = "x " * 1000
    monkeypatch.setenv("RAG_CONTEXT_ABSTRACT", "1")
    monkeypatch.delenv("RAG_ABSTRACT_CHARS", raising=False)  # 운영 .env(2000) 와 무관하게 기본 800
    out = R._format_chroma_hits(["body"], [{"paper_id": "1", "title": "t", "abstract": long_abs}], [0.3])
    assert len(out.split("[초록] ", 1)[1].split("\n\n", 1)[0]) == R._ABSTRACT_CHARS
