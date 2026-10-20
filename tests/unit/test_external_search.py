"""외부(OpenAlex) 검색 덧붙이기 (docs/experiments/external_search_1020) — 네트워크 없이."""

import time

from core.rag import external_search as X

WORKS = {"results": [
    {"id": "https://openalex.org/W1", "title": "Enabling LLMs to Generate Text with Citations", "publication_year": 2023,
     "ids": {"doi": "https://doi.org/10.48550/arxiv.2305.14627"}, "locations": [], "abstract_inverted_index": {"We": [0], "cite": [1]}},
    {"id": "https://openalex.org/W2", "title": "Old Paper", "publication_year": 2010, "ids": {}, "locations": []},
    {"id": "https://openalex.org/W3", "title": "In Context Already", "publication_year": 2024, "ids": {},
     "locations": [{"landing_page_url": "https://arxiv.org/abs/2401.00001"}]},
    {"id": "https://openalex.org/W4", "title": "Journal Only", "publication_year": 2025, "ids": {"doi": "https://doi.org/10.1/x"}, "locations": []},
]}


class _R:
    def __init__(self, data): self._d = data
    def raise_for_status(self): pass
    def json(self): return self._d


def test_filters_and_ids(monkeypatch):
    monkeypatch.setattr(X.requests, "get", lambda *a, **k: _R(WORKS))
    out = X.search_openalex("q", {"2401.00001v2"})
    assert [o["title"] for o in out] == ["Enabling LLMs to Generate Text with Citations", "Journal Only"]
    assert out[0]["arxiv"] == "2305.14627" and out[0]["abstract"] == "We cite"
    assert out[1]["url"] == "https://doi.org/10.1/x"


def test_failure_returns_empty(monkeypatch):
    def boom(*a, **k): raise X.requests.Timeout("t")
    monkeypatch.setattr(X.requests, "get", boom)
    assert X.search_openalex("q") == []


def test_format_uses_bracket_ids():
    s = X.format_section([{"title": "A", "year": 2023, "arxiv": "2305.14627", "url": ""}, {"title": "B", "year": 2025, "arxiv": None, "url": "https://doi.org/10.1/x"}])
    assert "📎" in s and "- A (2023) [2305.14627]" in s and "- B (2025) https://doi.org/10.1/x" in s
    assert X.format_section([]) == ""


def test_parallel_wait_bounded(monkeypatch):
    monkeypatch.setattr(X, "search_openalex", lambda q, ex, timeout=6: time.sleep(0.2) or [{"title": "t"}])
    e = X.ExternalSearch("q", set(), timeout=1.0)
    items, waited = e.result()
    assert items == [{"title": "t"}] and waited < 1.0


def test_flag(monkeypatch):
    monkeypatch.delenv("RAG_EXTERNAL_SEARCH", raising=False)
    assert not X.external_search_active()
