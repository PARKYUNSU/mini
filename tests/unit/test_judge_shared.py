"""판정이 답변과 같은 앞부분을 쓰는지 (docs/experiments/judge_cache_1017)."""

from core.llm.agent_prompts import DIRECT_ANSWER_RAG_SYSTEM_BASE, direct_answer_rag_user
from core.llm.presence_judge import shared_judge_messages, shared_prefix_active


def test_prefix_matches_answer():
    p = direct_answer_rag_user("맥락", "[문서 1]\nabc", "", "질문 X", doc_count=1)
    msgs = shared_judge_messages(DIRECT_ANSWER_RAG_SYSTEM_BASE, p, "질문 X")
    assert msgs[0].content == DIRECT_ANSWER_RAG_SYSTEM_BASE
    j = msgs[1].content
    cut = p.rfind("\n[사용자]\n")
    assert j.startswith(p[:cut]) and "[문서 1]\nabc" in j
    assert j.rstrip().endswith("질문 X") and "답: 없음" in j
    assert "출력 템플릿" not in j  # 답변 지시는 빠진다


def test_no_marker_returns_none():
    assert shared_judge_messages("s", "표지 없음", "q") is None


def test_flag_default_off(monkeypatch):
    monkeypatch.delenv("RAG_JUDGE_SHARED_PREFIX", raising=False)
    assert not shared_prefix_active()
    monkeypatch.setenv("RAG_JUDGE_SHARED_PREFIX", "1")
    assert shared_prefix_active()
