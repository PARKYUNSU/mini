"""검색어 후처리만 (RAG_QUERY_CLEAN, docs/experiments/query_clean_1021) — LLM 없이."""

from core.graph import agent_nodes as N


def test_drop_generic_keeps_phrases():
    q = "faithfulness verification rag research, automated evaluation, retrieved documents academic papers"
    assert N._drop_generic_words(q) == "faithfulness verification rag, automated evaluation, retrieved documents"


def test_drop_generic_fallbacks():
    assert N._drop_generic_words("academic research papers") == "academic research papers"  # 3단어 미만 → 원래
    assert N._drop_generic_words("검색 문서 연구") == "검색 문서 연구"  # 한국어 원문 폴백은 그대로


def test_flag_strips_list_number_and_cleans(monkeypatch):
    seen = []
    monkeypatch.setattr(N, "_extract_english_rag_query_base", lambda req, ctx="": seen.append(req) or "rag answer grounding research, academic search keywords")
    monkeypatch.setenv("RAG_QUERY_CLEAN", "1")
    assert N._extract_english_rag_query("1. RAG 답변이 근거하는지 검증하는 연구 있어?") == "rag answer grounding, search"
    assert seen == ["RAG 답변이 근거하는지 검증하는 연구 있어?"]


def test_flag_off_unchanged(monkeypatch):
    monkeypatch.delenv("RAG_QUERY_CLEAN", raising=False)
    monkeypatch.setattr(N, "_extract_english_rag_query_base", lambda req, ctx="": "x research, y")
    assert N._extract_english_rag_query("1. q") == "x research, y"
