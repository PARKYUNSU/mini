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


# RAG_FOLLOWUP_REUSE — 직전 답 컨텍스트 다시 쓰기 (docs/experiments/followup_reuse_1021)
from core.session.agent_session import SessionMemory

CTX = "[2401.00001v1] A\n초록 A\n\n---\n\n[2401.00002v2] B\n초록 B"
ANS = "<b>서론</b> 둘 다 [2401.00002v2]\n<b>본론</b>\n1. <b>B</b>: ... [2401.00002v2]\n2. <b>A</b>: ... [2401.00001v1]\n<b>결론</b> 끝"


def _sess(prev_q="RAG 논문 알려줘"):
    s = SessionMemory(chat_id="t")
    s.recent_messages.append((f"User: {prev_q}", "Assistant: ..."))
    s.last_rag = (prev_q, CTX, N.body_item_ids(ANS))
    return s


def test_body_item_ids():
    assert N.body_item_ids(ANS) == ["2401.00002", "2401.00001"]


def test_reuse(monkeypatch):
    monkeypatch.setenv("RAG_FOLLOWUP_REUSE", "1")
    s = _sess()
    assert N.followup_reuse_context(s, "그 논문의 한계는 뭐야?") == CTX
    assert N.followup_reuse_context(s, "그 중 첫 번째 논문 자세히 설명해줘").startswith("[2401.00002v2]")  # 본론 1번 = B
    assert N.followup_reuse_context(s, "두 번째 항목은 어떤 실험을 했어?").startswith("[2401.00001v1]")
    assert N.followup_reuse_context(s, "다른 논문도 추천해줘") == ""  # 새 논문을 원함 → 새로 검색
    assert N.followup_reuse_context(s, "KV 캐시 양자화 연구 있어?") == ""  # 새 질문
    assert N.followup_reuse_context(s, "요즘 날씨 어때?") == ""  # 짧은 잡담은 지시어가 없다 (job 128)
    assert N.followup_reuse_context(s, "고마워") == ""
    assert N.followup_reuse_context(s, "더 알려줘") == CTX
    # 긴 독립 질문 속 지시어는 재사용하지 않는다 (followup_reuse_1021 §5 오발동)
    assert N.followup_reuse_context(s, "LLM 탈옥에서 논리식으로 바꿔서 뚫는 방법이랑, 텍스트 탈옥을 오디오로 옮기는 연구는 뭐가 다른 거야?") == ""


def test_reuse_only_right_after_rag_turn(monkeypatch):
    monkeypatch.setenv("RAG_FOLLOWUP_REUSE", "1")
    s = _sess()
    s.recent_messages.append(("User: 배고파", "Assistant: ..."))
    assert N.followup_reuse_context(s, "그거 실제로 써먹으려면 뭐가 필요해?") == ""
    monkeypatch.delenv("RAG_FOLLOWUP_REUSE")
    assert N.followup_reuse_context(_sess(), "그 논문의 한계는 뭐야?") == ""
