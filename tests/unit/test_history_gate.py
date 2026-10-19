"""RAG_HISTORY_GATE — 이어지는 질문에만 대화 기록 (docs/experiments/history_gate_1019)."""

import pytest

from core.graph import agent_nodes as N

FOLLOW = ["그 중 첫 번째 논문 자세히 설명해줘", "다른 논문도 추천해줘", "그 논문의 한계는 뭐야?", "방금 답한 거 더 쉽게 설명해줘",
          "두 번째 항목은 어떤 실험을 했어?", "위에서 말한 방법의 핵심 아이디어만 요약해줘", "이어서 그 분야 최신 동향도 알려줘",
          "그거 실제로 써먹으려면 뭐가 필요해?", "더 알려줘", "왜?", "3번 논문은?"]
NEW = ["RAG 답변이 검색된 문서에 근거하는지(faithfulness) 자동으로 검증하는 연구 있어?",
       "LLM 답변에 문장 단위 인용(citation)을 정확하게 붙이게 하는 방법 찾아줘",
       "KV 캐시를 양자화해서 긴 문맥 추론 메모리를 줄이는 연구 있어?",
       "EAGLE이랑 Medusa 차이가 뭐야?", "요즘 speculative decoding 연구 동향 정리해줘"]


@pytest.mark.parametrize("q", FOLLOW)
def test_followups_detected(q):
    assert N.is_followup(q)


@pytest.mark.parametrize("q", NEW)
def test_new_questions_not_followups(q):
    assert not N.is_followup(q)


def test_gate_off_always_allows(monkeypatch):
    monkeypatch.delenv("RAG_HISTORY_GATE", raising=False)
    assert N.rag_history_allowed(NEW[0])


def test_gate_on(monkeypatch):
    monkeypatch.setenv("RAG_HISTORY_GATE", "1")
    assert not N.rag_history_allowed(NEW[1]) and N.rag_history_allowed(FOLLOW[0])
