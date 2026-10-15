"""초록 길이 설정 RAG_ABSTRACT_CHARS (docs/experiments/abstract_full_1016)."""

from core.rag import agent_chroma_rag as m

ABS = "A" * 500 + " result 25.5% " + "B" * 1000


def test_default_800(monkeypatch):
    monkeypatch.delenv("RAG_ABSTRACT_CHARS", raising=False)
    assert m.context_abstract_chars() == 800
    out = m._with_abstract("body text", ABS)
    assert "25.5" in out  # 앞 800자 안
    assert out.startswith("[초록] ") and len(out.split("\n\n")[0]) == len("[초록] ") + 800


def test_full_abstract(monkeypatch):
    monkeypatch.setenv("RAG_ABSTRACT_CHARS", "2000")
    out = m._with_abstract("body", ABS)
    assert out.split("\n\n")[0] == "[초록] " + ABS.strip()


def test_bad_value_falls_back(monkeypatch):
    monkeypatch.setenv("RAG_ABSTRACT_CHARS", "lots")
    assert m.context_abstract_chars() == 800
