#!/usr/bin/env python3
"""의도적 SyntaxError 요청·파이썬 라우터 하드룰 회귀 테스트

agent_bot( langchain/chromadb 등 ) 없이 agent_router_rules + agent_config 만 import.
"""
import re
import sys
from pathlib import Path
from typing import Optional

import pytest

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

pytestmark = pytest.mark.unit

from core.graph.agent_router_rules import (
    RouterStep1Deps,
    classify_python_pipeline_tier,
    is_explicit_python_coding_request,
    is_smalltalk_or_memory_request,
    router_step1_hard_rules,
    skip_planner_debate_for_fast_path,
    user_wants_intentional_exec_error,
)

_ROUTER_TEST_DEPS = RouterStep1Deps(
    agent_tools_dir=_ROOT / "tools" / "runtime" / "agent_tools" / "agent_tools",
    get_paper_mode=lambda _cid: False,
    resolve_recent_tool=lambda _a, _b: None,
)


def _step1(msg: str, low: str, cid: str = "x"):
    return router_step1_hard_rules(msg, low, cid, _ROUTER_TEST_DEPS)


def _strip_wake_word(text: str) -> str:
    """agent_telegram.strip_wake_word 와 동일 (의존성 분리)"""
    cleaned = re.sub(r"^윤수르[,\.\s]*", "", text.strip()).strip()
    return cleaned if cleaned else text.strip()


USER_MSG = (
    "윤수르, 파이썬으로 1부터 10까지 더하는 코드를 짜는데, "
    "일부러 오타(SyntaxError)를 하나 넣어서 실행해 봐"
)


def test_strip_and_intentional_flag():
    text = _strip_wake_word(USER_MSG)
    assert "파이썬" in text
    assert user_wants_intentional_exec_error(text) is True


def test_syntax_error_run_path_is_code_run_not_planner():
    """실행+SyntaxError 요청은 승인 없이 code_run (planner 생략)"""
    text = _strip_wake_word(USER_MSG)
    req_lower = text.lower()
    assert is_explicit_python_coding_request(text, req_lower) is True
    assert classify_python_pipeline_tier(text, req_lower) == "run"
    r = _step1(text, req_lower, "dummy_chat_id")
    assert r is not None
    assert r.get("route_type") == "code_run"
    assert r.get("approval_status") == "approved"
    assert r.get("skip_tool_save") is True


def test_simple_python_snippet_is_direct_example():
    r = _step1("간단한 파이썬 구문 만들어줘", "간단한 파이썬 구문 만들어줘".lower(), "x")
    assert r.get("route_type") == "direct_answer"
    assert r.get("python_example_direct") is True


def test_complex_python_stays_planner():
    msg = "파이썬으로 mysql 데이터베이스에 연결하는 코드 작성해줘"
    r = _step1(msg, msg.lower(), "x")
    assert r.get("route_type") == "planner"


def test_action_keywords_does_not_bypass_three_tier():
    """action_keywords에 걸려도 3단 분기 먼저 적용 (코드 짜줘 등이 planner로 선점되지 않음)"""
    r = _step1("파이썬 코드 짜줘", "파이썬 코드 짜줘".lower(), "x")
    assert r.get("route_type") == "direct_answer"
    assert r.get("python_example_direct") is True

    r2 = _step1("코드 작성해줘", "코드 작성해줘".lower(), "x")
    assert r2.get("route_type") == "direct_answer"
    assert r2.get("python_example_direct") is True

    r3 = _step1("코드 짜줘", "코드 짜줘".lower(), "x")
    assert r3.get("route_type") == "direct_answer"
    assert r3.get("python_example_direct") is True


def test_plain_python_intro_not_forced_planner():
    """설명-only 요청은 이 하드룰로 planner에 강제되지 않아야 함"""
    text = "파이썬이 뭐야?"
    assert is_explicit_python_coding_request(text, text.lower()) is False


def test_trivial_coding_skips_debate_heuristic():
    assert skip_planner_debate_for_fast_path("간단한 파이썬 구문 만들어줘") is True
    assert skip_planner_debate_for_fast_path("대규모 데이터 파이프라인 코드 짜줘") is False


def test_hello_inside_string_literal_not_greeting_smalltalk():
    """len('hello') 등 코드 문자열 안의 hello는 인사로 보지 않음."""
    msg = "파이썬으로 len('hello') 실행해줘"
    low = msg.lower()
    assert is_smalltalk_or_memory_request(msg, low) is False


def _assert_route(msg: str, *, route: str, example: Optional[bool] = None):
    low = msg.lower()
    r = _step1(msg, low, "x")
    assert r is not None, msg
    assert r.get("route_type") == route, (msg, r)
    if example is not None:
        assert bool(r.get("python_example_direct")) == example, (msg, r)


def test_three_tier_feedback_matrix():
    """피드백: 예제 / code_run / planner 대표 문장 회귀"""
    for s in (
        "파이썬 for문 예제 보여줘",
        "리스트 컴프리헨션 샘플 줘",
        "간단한 코드 작성해줘",
    ):
        _assert_route(s, route="direct_answer", example=True)

    for s in (
        "1부터 10까지 더하는 코드 실행해줘",
        "print hello world 돌려봐",
        "파이썬으로 len('hello') 결과를 print하는 코드 실행해줘",
        "오타 넣어서 실행해봐",
    ):
        low = s.lower()
        rr = _step1(s, low, "x")
        assert rr is not None and rr.get("route_type") == "code_run", (s, rr)
        assert rr.get("skip_tool_save") is True

    for s in (
        "파이썬으로 csv 파일 읽어서 정리해줘",
        "mysql 접속해서 테이블 목록 조회 스크립트 작성",
        "requests로 API 호출해서 저장해줘",
    ):
        _assert_route(s, route="planner", example=False)


if __name__ == "__main__":
    test_strip_and_intentional_flag()
    test_syntax_error_run_path_is_code_run_not_planner()
    test_simple_python_snippet_is_direct_example()
    test_complex_python_stays_planner()
    test_action_keywords_does_not_bypass_three_tier()
    test_plain_python_intro_not_forced_planner()
    test_trivial_coding_skips_debate_heuristic()
    test_hello_inside_string_literal_not_greeting_smalltalk()
    test_three_tier_feedback_matrix()
    print("OK: intentional_syntax_and_router")
