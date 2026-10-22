"""조건별 분리 검색 — 나열 표지 · 응답 해석 (docs/experiments/aspect_split_1022)."""

from langchain_core.messages import AIMessage

from core.graph import agent_nodes as N


def test_aspect_marker():
    assert N._ASPECT_RE.search("검색된 문서의 순서나 개수가 답변 품질에 주는 영향")
    assert N._ASPECT_RE.search("탈옥 공격이랑 방어 연구")
    assert not N._ASPECT_RE.search("KV 캐시를 양자화해서 메모리를 줄이는 연구 있어?")


def _fake(text):
    class L:
        def invoke(self, _):
            return AIMessage(content=text)
    return lambda: L()


def test_extract_aspects(monkeypatch):
    monkeypatch.setattr(N, "get_rag_query_rewrite_llm", _fake("1: lost in the middle RAG document position\n2: number of retrieved passages RAG"))
    assert N._extract_aspects("q") == ["lost in the middle RAG document position", "number of retrieved passages RAG"]
    monkeypatch.setattr(N, "get_rag_query_rewrite_llm", _fake("NONE"))
    assert N._extract_aspects("q") == []
    monkeypatch.setattr(N, "get_rag_query_rewrite_llm", _fake("1: only one"))
    assert N._extract_aspects("q") == []
