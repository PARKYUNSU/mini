"""
노드 계약 테스트: LLM·E2B·Chroma를 mock 하여 state shape·분기만 검증.

외부 API 호출 없음 → integration 마커 (라우터 3단 경로는 Chroma 인스턴스 생성까지 mock).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

pytestmark = pytest.mark.integration

import agent_nodes  # noqa: E402


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
        def search(self, _q: str) -> str:
            return ""

    class DummyTRS:
        def format_topk_block(self, user_request: str, k: int = 3) -> str:
            return ""

        def format_router_tools_tag(self, user_request: str, k: int = 3) -> str:
            return "<tools></tools>"

    monkeypatch.setattr(agent_nodes, "ChromaRAGTool", DummyRAG)
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
