"""
code_run 하드룰이 만드는 state 조각 검증 (LLM·E2B 없음).

executor 노드 진입 전 라우터 1단계가 채우는 필드만 단위 검증합니다.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

pytestmark = pytest.mark.unit

from agent_router_rules import (  # noqa: E402
    RouterStep1Deps,
    router_step1_hard_rules,
)

_DEPS = RouterStep1Deps(
    agent_tools_dir=_ROOT / "agent_tools",
    get_paper_mode=lambda _cid: False,
    resolve_recent_tool=lambda _a, _b: None,
)


def _step1(msg: str) -> dict:
    low = msg.lower()
    r = router_step1_hard_rules(msg, low, "test_chat", _DEPS)
    assert r is not None, msg
    return r


def test_code_run_has_approval_plan_skip_tool_save_light_monitor():
    msg = "파이썬으로 len('hello') 결과를 print하는 코드 실행해줘"
    r = _step1(msg)
    assert r.get("route_type") == "code_run"
    assert r.get("router_choice") == "C"
    assert r.get("approval_status") == "approved"
    assert r.get("skip_tool_save") is True
    assert r.get("light_monitor") is True
    plan = r.get("plan") or []
    assert isinstance(plan, list) and len(plan) >= 1
    assert "파이썬" in plan[0] or "print" in plan[0].lower() or "실행" in plan[0]


def test_print_hello_world_still_code_run():
    r = _step1("print hello world 돌려봐")
    assert r.get("route_type") == "code_run"
    assert r.get("approval_status") == "approved"


def test_intentional_syntax_code_run():
    # wake word "윤수르"가 identity_q에 들어가 있어 smalltalk로 먼저 잡히므로 제거한 문장과 동일하게 검증
    msg = (
        "파이썬으로 1부터 10까지 더하는 코드를 짜는데, "
        "일부러 오타(SyntaxError)를 하나 넣어서 실행해 봐"
    )
    r = _step1(msg)
    assert r.get("route_type") == "code_run"
    assert r.get("skip_tool_save") is True
