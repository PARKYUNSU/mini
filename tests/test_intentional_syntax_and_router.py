#!/usr/bin/env python3
"""의도적 SyntaxError 요청·파이썬 라우터 하드룰 회귀 테스트"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent_telegram import strip_wake_word
from agent_bot import (
    _is_explicit_python_coding_request,
    _router_step1_hard_rules,
    _user_wants_intentional_exec_error,
)


USER_MSG = (
    "윤수르, 파이썬으로 1부터 10까지 더하는 코드를 짜는데, "
    "일부러 오타(SyntaxError)를 하나 넣어서 실행해 봐"
)


def test_strip_and_intentional_flag():
    text = strip_wake_word(USER_MSG)
    assert "파이썬" in text
    assert _user_wants_intentional_exec_error(text) is True


def test_explicit_python_router():
    text = strip_wake_word(USER_MSG)
    req_lower = text.lower()
    assert _is_explicit_python_coding_request(text, req_lower) is True
    r = _router_step1_hard_rules(text, req_lower, "dummy_chat_id")
    assert r is not None
    assert r.get("route_type") == "planner"
    assert r.get("router_choice") == "C"


def test_plain_python_intro_not_forced_planner():
    """설명-only 요청은 이 하드룰로 planner에 강제되지 않아야 함"""
    text = "파이썬이 뭐야?"
    assert _is_explicit_python_coding_request(text, text.lower()) is False


if __name__ == "__main__":
    test_strip_and_intentional_flag()
    test_explicit_python_router()
    test_plain_python_intro_not_forced_planner()
    print("OK: intentional_syntax_and_router")
