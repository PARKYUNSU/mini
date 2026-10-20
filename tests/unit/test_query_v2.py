"""검색어 추출 v2 (RAG_QUERY_V2, docs/experiments/query_extract_1021) — LLM 없이."""

from core.graph import agent_nodes as N


class _LLM:
    def __init__(self, out, seen):
        self.out, self.seen = out, seen

    def invoke(self, msgs):
        self.seen.append(msgs[0].content)
        return self.out


def _patch(monkeypatch, out):
    seen = []
    monkeypatch.setattr(N, "get_rag_query_rewrite_llm", lambda: _LLM(out, seen))
    monkeypatch.setattr(N, "normalize_ai_message_content", lambda r: r)
    monkeypatch.setenv("RAG_QUERY_V2", "1")
    return seen


def test_strips_list_number_and_generic_words(monkeypatch):
    seen = _patch(monkeypatch, "RAG answer faithfulness grounding automatic verification research papers\nextra")
    q = N._extract_english_rag_query("1. RAG 답변이 검색된 문서에 근거하는지 자동으로 검증하는 연구 있어?")
    assert q == "rag answer faithfulness grounding automatic verification"
    assert "User question:\nRAG 답변이" in seen[0]  # 앞 번호 "1." 은 지우고 넘긴다


def test_short_output_falls_back(monkeypatch):
    _patch(monkeypatch, "rag")
    assert N._extract_english_rag_query("① 짧은 질문") == "짧은 질문"


def test_flag_off_uses_v1(monkeypatch):
    monkeypatch.delenv("RAG_QUERY_V2", raising=False)
    called = []
    monkeypatch.setattr(N, "_extract_english_rag_query_v2", lambda *a, **k: called.append(1) or "x")
    monkeypatch.setattr(N, "get_rag_query_rewrite_llm", lambda: _LLM("a, b, c", []))
    monkeypatch.setattr(N, "normalize_ai_message_content", lambda r: r)
    N._extract_english_rag_query("질문")
    assert not called
