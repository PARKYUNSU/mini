"""
노드 계약 테스트: LLM·E2B·Chroma를 mock 하여 state shape·분기만 검증.

외부 API 호출 없음 → integration 마커 (라우터 3단 경로는 Chroma 인스턴스 생성까지 mock).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

pytestmark = pytest.mark.integration

import core.graph.agent_nodes as agent_nodes  # noqa: E402


@pytest.fixture
def cfg():
    return {"configurable": {"chat_id": "node_contract_chat", "bot": None}}


def test_router_node_hard_rule_no_llm(cfg):
    out = agent_nodes.router_node({"user_request": "안녕"}, config=cfg)
    assert out.get("route_type") == "direct_answer"
    assert out.get("router_choice") == "A"


def test_router_node_llm_path_uses_mock_classify(monkeypatch, cfg):
    """1단계 None → Chroma·tool RAG·_router_step3_llm_classify mock."""
    msg = "q9f2k_node_contract_only_no_hard_rule_match_xyz"

    class DummyRAG:
        def search(self, _q: str, **_kw) -> str:
            return ""

    class DummyTRS:
        def format_topk_block(self, user_request: str, k: int = 3) -> str:
            return ""

        def format_router_tools_tag(self, user_request: str, k: int = 3) -> str:
            return "<tools></tools>"

    _dummy_rag = DummyRAG()
    monkeypatch.setattr(agent_nodes, "get_chroma_rag_tool", lambda: _dummy_rag)
    monkeypatch.setattr(agent_nodes, "get_tool_rag_store", lambda: DummyTRS())

    def _fake_classify(*_a, **_kw):
        return {"route_type": "planner", "router_choice": "C"}

    monkeypatch.setattr(agent_nodes, "_router_step3_llm_classify", _fake_classify)

    out = agent_nodes.router_node({"user_request": msg}, config=cfg)
    assert out.get("route_type") == "planner"
    assert out.get("router_choice") == "C"


def test_direct_answer_node_greeting_branch_no_llm(cfg):
    out = agent_nodes.direct_answer_node(
        {"user_request": "안녕", "router_choice": "A"},
        config=cfg,
    )
    assert "direct_response" in out
    assert "윤수르" in (out.get("direct_response") or "")


def test_direct_answer_node_fatal_error_empty_dict(cfg):
    out = agent_nodes.direct_answer_node(
        {
            "user_request": "anything",
            "router_choice": "A",
            "agent_fatal_error": "boom",
        },
        config=cfg,
    )
    assert out == {}


def test_route_after_router_code_run_to_executor():
    assert agent_nodes.route_after_router({"route_type": "code_run"}) == "executor"


def test_route_after_router_fatal_to_direct_answer():
    assert agent_nodes.route_after_router({"route_type": "planner", "agent_fatal_error": "x"}) == "direct_answer"


def test_executor_node_not_approved():
    out = agent_nodes.executor_node(
        {
            "approval_status": "pending",
            "route_type": "code_run",
            "plan": [],
            "user_request": "x",
        }
    )
    assert out.get("execution_result") == "승인되지 않음"
    assert not out.get("generated_code")


def test_executor_node_code_run_mock_llm_and_sandbox(monkeypatch):
    class Resp:
        content = "```python\nprint(42)\n```"

    class LLM:
        def invoke(self, _msgs):
            return Resp()

    monkeypatch.setattr(agent_nodes, "get_coding_groq_llm", lambda: LLM())
    monkeypatch.setattr(agent_nodes, "_run_code_sandbox", lambda _code: "42")

    out = agent_nodes.executor_node(
        {
            "approval_status": "approved",
            "route_type": "code_run",
            "plan": ["단계1"],
            "user_request": "print 42",
            "error_hint": "",
        }
    )
    assert "42" in (out.get("execution_result") or "")
    assert "print" in (out.get("generated_code") or "").lower()


def test_monitor_node_execution_error_sets_retry_hint(monkeypatch):
    class MResp:
        content = "세미콜론을 확인하세요."

    class MLLM:
        def invoke(self, _msgs):
            return MResp()

    monkeypatch.setattr(agent_nodes, "get_coding_groq_llm", lambda: MLLM())

    out = agent_nodes.monitor_node(
        {
            "user_request": "파이썬 코드 실행",
            "execution_result": "실행 오류: SyntaxError: invalid syntax",
            "retry_count": 0,
            "light_monitor": True,
            "generated_code": "x = 1",
        }
    )
    assert out.get("retry_count") == 1
    assert "세미콜론" in (out.get("error_hint") or "")


def test_monitor_node_intentional_syntax_no_retry():
    out = agent_nodes.monitor_node(
        {
            "user_request": "파이썬으로 일부러 오타 넣어서 실행해줘",
            "execution_result": "실행 오류: SyntaxError: bad",
            "retry_count": 0,
            "light_monitor": False,
            "generated_code": "bad code",
        }
    )
    assert out.get("content_irrelevant") is False
    assert "retry_count" not in out


def test_route_after_monitor_intentional_syntax_ends():
    assert (
        agent_nodes.route_after_monitor(
            {
                "user_request": "일부러 SyntaxError 실행해줘",
                "execution_result": "실행 오류: SyntaxError",
                "retry_count": 0,
            }
        )
        == "__end__"
    )


def test_invoke_llm_with_fallback_timeout_then_second_succeeds(monkeypatch):
    from concurrent.futures import TimeoutError as FuturesTimeout

    class R:
        content = "second_ok"

    state = {"submit": 0}

    class FakePool:
        def submit(self, fn, *args):
            state["submit"] += 1

            class F:
                def result(self2, timeout=None):
                    if state["submit"] == 1:
                        raise FuturesTimeout()
                    return R()

            return F()

        def shutdown(self, *a, **k):
            pass

    monkeypatch.setattr(agent_nodes, "ThreadPoolExecutor", lambda *a, **k: FakePool())
    monkeypatch.setattr(agent_nodes, "get_planner_llm", lambda: object())
    monkeypatch.setattr(agent_nodes, "get_executor_llm", lambda: object())
    out = agent_nodes._invoke_llm_with_fallback([], timeout_sec=1.0)
    assert out == "second_ok"


def test_invoke_llm_with_fallback_all_timeout_returns_fallback(monkeypatch):
    from concurrent.futures import TimeoutError as FuturesTimeout

    class FakePool:
        def submit(self, fn, *args):
            class F:
                def result(self2, timeout=None):
                    raise FuturesTimeout()

            return F()

        def shutdown(self, *a, **k):
            pass

    monkeypatch.setattr(agent_nodes, "ThreadPoolExecutor", lambda *a, **k: FakePool())
    monkeypatch.setattr(agent_nodes, "get_planner_llm", lambda: object())
    monkeypatch.setattr(agent_nodes, "get_executor_llm", lambda: object())
    out = agent_nodes._invoke_llm_with_fallback([], fallback_msg="fallback_xyz", timeout_sec=1.0)
    assert out == "fallback_xyz"


def test_direct_answer_a_path_passes_timeout_to_invoke(monkeypatch, cfg):
    captured = []

    def _cap(*_a, timeout_sec=None, **_k):
        captured.append(timeout_sec)
        return "ok"

    monkeypatch.setattr(agent_nodes, "_invoke_llm_with_fallback", _cap)
    monkeypatch.setattr(agent_nodes, "DIRECT_ANSWER_TIMEOUT_SEC", 33.0)
    unique = "q9f2k_node_contract_timeout_pass_only"
    agent_nodes.direct_answer_node({"user_request": unique, "router_choice": "A"}, config=cfg)
    assert captured == [33.0]


def test_paper_mode_biases_knowledge_from_a_to_rag(monkeypatch, cfg):
    monkeypatch.setattr(agent_nodes, "get_paper_mode", lambda _cid: True)
    monkeypatch.setattr(agent_nodes, "router_step1_hard_rules", lambda *a, **k: None)

    class DummyRAG:
        def search(self, *a, **k):
            return ""

    _dummy_rag = DummyRAG()
    monkeypatch.setattr(agent_nodes, "get_chroma_rag_tool", lambda: _dummy_rag)

    class DummyTRS:
        def format_topk_block(self, *a, **k):
            return ""

        def format_router_tools_tag(self, *a, **k):
            return "<tools></tools>"

    monkeypatch.setattr(agent_nodes, "get_tool_rag_store", lambda: DummyTRS())
    monkeypatch.setattr(
        agent_nodes,
        "_router_step3_llm_classify",
        lambda *a, **k: {"route_type": "direct_answer", "router_choice": "A"},
    )
    out = agent_nodes.router_node({"user_request": "양자 얽힘이 뭐야?"}, config=cfg)
    assert out.get("router_choice") == "B"


def test_paper_mode_allows_explicit_code_to_planner(monkeypatch, cfg):
    monkeypatch.setattr(agent_nodes, "get_paper_mode", lambda _cid: True)
    monkeypatch.setattr(agent_nodes, "router_step1_hard_rules", lambda *a, **k: None)

    class DummyRAG:
        def search(self, *a, **k):
            return ""

    _dummy_rag = DummyRAG()
    monkeypatch.setattr(agent_nodes, "get_chroma_rag_tool", lambda: _dummy_rag)

    class DummyTRS:
        def format_topk_block(self, *a, **k):
            return ""

        def format_router_tools_tag(self, *a, **k):
            return "<tools></tools>"

    monkeypatch.setattr(agent_nodes, "get_tool_rag_store", lambda: DummyTRS())
    monkeypatch.setattr(
        agent_nodes,
        "_router_step3_llm_classify",
        lambda *a, **k: {"route_type": "direct_answer", "router_choice": "A"},
    )
    out = agent_nodes.router_node(
        {"user_request": "파이썬으로 피보나치 수열 코드 실행해줘"},
        config=cfg,
    )
    assert out.get("router_choice") == "C"
    assert out.get("route_type") == "planner"


def test_enforce_rag_structure_markdown_has_three_sections():
    raw = "이 논문은 멀티모달 모델의 효율을 개선합니다. 제안 방법은 저랭크 어댑터를 활용합니다. 실험에서 기존 대비 성능이 향상됩니다."
    out = agent_nodes._enforce_rag_structure_markdown(raw)
    assert "1. 핵심 주제" in out
    assert "2. 주요 방법론" in out
    assert "3. 결론 및 의의" in out


def test_strip_thinking_tags_removes_redacted_block():
    from apps.telegram_bot.agent_telegram import strip_thinking_tags

    raw = (
        "<redacted_thinking>\nstep A\n</redacted_thinking>\n\n"
        "1. 핵심 주제\n- 본문입니다."
    )
    out = strip_thinking_tags(raw)
    assert "redacted_thinking" not in out.lower()
    assert "본문입니다" in out


def test_markdown_struct_to_plain_preserves_structure():
    md = "### 핵심 주제\n- A\n\n### 주요 방법론\n- B\n\n### 결론 및 의의\n- C"
    plain = agent_nodes._markdown_struct_to_plain(md)
    assert "핵심 주제" in plain
    assert "주요 방법론" in plain
    assert "결론 및 의의" in plain
    assert "• A" in plain
