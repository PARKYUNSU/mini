#!/usr/bin/env python3
"""의도적 SyntaxError 요청·파이썬 라우터 하드룰 회귀 테스트

agent_telegram은 import 시 pyTelegramBotAPI 등이 필요하므로,
라우터만 검증할 때는 wake word 제거를 테스트 내에서 처리합니다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent_bot import (
    _classify_python_pipeline_tier,
    _is_explicit_python_coding_request,
    _router_step1_hard_rules,
    _skip_planner_debate_for_fast_path,
    _user_wants_intentional_exec_error,
)


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
    assert _user_wants_intentional_exec_error(text) is True


def test_syntax_error_run_path_is_code_run_not_planner():
    """실행+SyntaxError 요청은 승인 없이 code_run (planner 생략)"""
    text = _strip_wake_word(USER_MSG)
    req_lower = text.lower()
    assert _is_explicit_python_coding_request(text, req_lower) is True
    assert _classify_python_pipeline_tier(text, req_lower) == "run"
    r = _router_step1_hard_rules(text, req_lower, "dummy_chat_id")
    assert r is not None
    assert r.get("route_type") == "code_run"
    assert r.get("approval_status") == "approved"
    assert r.get("skip_tool_save") is True


def test_simple_python_snippet_is_direct_example():
    r = _router_step1_hard_rules("간단한 파이썬 구문 만들어줘", "간단한 파이썬 구문 만들어줘".lower(), "x")
    assert r.get("route_type") == "direct_answer"
    assert r.get("python_example_direct") is True


def test_complex_python_stays_planner():
    msg = "파이썬으로 mysql 데이터베이스에 연결하는 코드 작성해줘"
    r = _router_step1_hard_rules(msg, msg.lower(), "x")
    assert r.get("route_type") == "planner"


def test_action_keywords_does_not_bypass_three_tier():
    """action_keywords에 걸려도 3단 분기 먼저 적용 (코드 짜줘 등이 planner로 선점되지 않음)"""
    r = _router_step1_hard_rules("파이썬 코드 짜줘", "파이썬 코드 짜줘".lower(), "x")
    assert r.get("route_type") == "direct_answer"
    assert r.get("python_example_direct") is True

    # "작성해"가 짧은 예제형 휴리스틱에 걸림 → planner 선점이 아니라 direct_answer
    r2 = _router_step1_hard_rules("코드 작성해줘", "코드 작성해줘".lower(), "x")
    assert r2.get("route_type") == "direct_answer"
    assert r2.get("python_example_direct") is True

    r3 = _router_step1_hard_rules("코드 짜줘", "코드 짜줘".lower(), "x")
    assert r3.get("route_type") == "direct_answer"
    assert r3.get("python_example_direct") is True


def test_plain_python_intro_not_forced_planner():
    """설명-only 요청은 이 하드룰로 planner에 강제되지 않아야 함"""
    text = "파이썬이 뭐야?"
    assert _is_explicit_python_coding_request(text, text.lower()) is False


def test_trivial_coding_skips_debate_heuristic():
    assert _skip_planner_debate_for_fast_path("간단한 파이썬 구문 만들어줘") is True
    assert _skip_planner_debate_for_fast_path("대규모 데이터 파이프라인 코드 짜줘") is False


def _assert_route(msg: str, *, route: str, example: bool | None = None):
    low = msg.lower()
    r = _router_step1_hard_rules(msg, low, "x")
    assert r is not None, msg
    assert r.get("route_type") == route, (msg, r)
    if example is not None:
        assert bool(r.get("python_example_direct")) == example, (msg, r)


def test_three_tier_feedback_matrix():
    """피드백: 예제 / code_run / planner 대표 문장 회귀"""
    # 예제형
    for s in (
        "파이썬 for문 예제 보여줘",
        "리스트 컴프리헨션 샘플 줘",
        "간단한 코드 작성해줘",
    ):
        _assert_route(s, route="direct_answer", example=True)

    # 실행형 (code_run)
    for s in (
        "1부터 10까지 더하는 코드 실행해줘",
        "print hello world 돌려봐",
        "오타 넣어서 실행해봐",
    ):
        low = s.lower()
        rr = _router_step1_hard_rules(s, low, "x")
        assert rr is not None and rr.get("route_type") == "code_run", (s, rr)
        assert rr.get("skip_tool_save") is True

    # 복잡형 → planner
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
    test_three_tier_feedback_matrix()
    print("OK: intentional_syntax_and_router")
