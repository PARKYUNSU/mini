"""한국어 질문 → 영어 검색어 추출이 쉼표 없는 LLM 출력에서 원문으로 떨어지지 않게 지킨다.

2026-10-08 운영 확인: 로컬 모델이 'tool failure detection LLM agent reliability ...' 처럼
쉼표 없이 내면(재현 6/6) 파서가 그 덩어리를 '5단어 초과'로 버리고 한국어 원문을 반환했다.
영어 전용 임베딩·BM25 로 한국어를 검색해 정답 논문이 결과에 아예 없었다.
"""

from __future__ import annotations

import pytest


class _Resp:
    def __init__(self, content: str):
        self.content = content


def _patch_llm(monkeypatch, output: str):
    import core.graph.agent_nodes as N

    class _LLM:
        def invoke(self, _msgs):
            return _Resp(output)

    monkeypatch.setattr(N, "get_rag_query_rewrite_llm", lambda: _LLM())
    monkeypatch.setattr(N, "get_executor_llm", lambda: _LLM())  # 빈 출력이면 이쪽으로 넘어간다
    return N


KO = "LLM 에이전트가 쓰는 도구가 오류를 내도 티가 안 나는 경우, 모델이 그걸 알아채는지 다룬 논문 있어?"


def test_space_separated_keywords_are_used_not_korean_original(monkeypatch):
    N = _patch_llm(monkeypatch, "tool failure detection LLM agent reliability error awareness academic papers")
    q = N._extract_english_rag_query(KO)
    assert q == "tool failure detection llm agent reliability error awareness academic papers"


def test_comma_separated_keywords_unchanged(monkeypatch):
    N = _patch_llm(monkeypatch, "tool failure detection, LLM agents, silent errors")
    assert N._extract_english_rag_query(KO) == "tool failure detection, llm agents, silent errors"


@pytest.mark.parametrize("out", ["", "에이전트 도구 오류", "ok"])
def test_falls_back_to_original_when_no_usable_english(monkeypatch, out):
    N = _patch_llm(monkeypatch, out)
    assert N._extract_english_rag_query(KO) == KO
