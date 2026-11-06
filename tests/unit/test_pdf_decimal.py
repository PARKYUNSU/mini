"""PDF 깨진 소수점 고치기 (docs/experiments/pdf_decimal_1107)."""
from core.rag.agent_chroma_rag import _fix_pdf_decimal, _format_chroma_hits


def test_off_by_default(monkeypatch):
    monkeypatch.delenv("RAG_FIX_PDF_DECIMAL", raising=False)
    assert _fix_pdf_decimal("by 87 _._ 5%") == "by 87 _._ 5%"


def test_fixes_decimal_forms(monkeypatch):
    monkeypatch.setenv("RAG_FIX_PDF_DECIMAL", "1")
    assert _fix_pdf_decimal("by 87 _._ 5% and 2 _._ 35 _× fewer") == "by 87.5% and 2.35 _× fewer"
    assert _fix_pdf_decimal("|0_._594|8_._4<br>") == "|0.594|8.4<br>"
    assert _fix_pdf_decimal("Section 3 _._ 2 _._ 1") == "Section 3.2.1"


def test_leaves_other_text(monkeypatch):
    monkeypatch.setenv("RAG_FIX_PDF_DECIMAL", "1")
    for t in ("github _._ com", "0 _,_ 1", "a _._ 5", "5 _._ b", "12.5% 그대로"):
        assert _fix_pdf_decimal(t) == t


def test_format_hits_uses_fix(monkeypatch):
    monkeypatch.setenv("RAG_CONTEXT_ABSTRACT", "0")
    meta = [{"paper_id": "2401.00001", "title": "T"}]
    monkeypatch.delenv("RAG_FIX_PDF_DECIMAL", raising=False)
    assert "87 _._ 5%" in _format_chroma_hits(["reduce by 87 _._ 5%"], meta)
    monkeypatch.setenv("RAG_FIX_PDF_DECIMAL", "1")
    assert "87.5%" in _format_chroma_hits(["reduce by 87 _._ 5%"], meta)
