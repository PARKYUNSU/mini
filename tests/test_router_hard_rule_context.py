"""하드룰·문맥 충돌 회귀: URL·코드 조각·파일명 속 토큰."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

pytestmark = pytest.mark.unit

from agent_router_rules import (  # noqa: E402
    RouterStep1Deps,
    _ascii_greeting_in_smalltalk,
    _req_lower_for_ascii_greeting_scan,
    is_smalltalk_or_memory_request,
    router_step1_hard_rules,
)

_DEPS = RouterStep1Deps(
    agent_tools_dir=_ROOT / "agent_tools",
    get_paper_mode=lambda _cid: False,
    resolve_recent_tool=lambda _a, _b: None,
)


def test_url_path_hello_not_ascii_greeting():
    low = "이거 문서 봐줘 https://example.com/api/hello/world 뭐야".lower()
    assert _ascii_greeting_in_smalltalk(low) is False


def test_req_lower_url_stripped_for_greeting_scan():
    raw = "see https://site.com/hi/there and also https://x.y/hello".lower()
    stripped = _req_lower_for_ascii_greeting_scan(raw)
    assert "hello" not in stripped
    assert "hi" not in stripped or "/hi/" not in stripped


def test_standalone_hi_still_greeting():
    assert _ascii_greeting_in_smalltalk("hi there") is True


def test_sql_like_hi_table_not_hi_greeting():
    """hi_table 등 단어 경계로 인사 hi와 분리."""
    msg = "파이썬으로 select * from hi_table 실행해줘"
    low = msg.lower()
    assert is_smalltalk_or_memory_request(msg, low) is False


def test_filename_hello_world_pdf_not_greeting_alone():
    msg = "파이썬으로 report_hello_world.pdf 내용 한 줄만 읽는 코드 실행해줘"
    low = msg.lower()
    assert is_smalltalk_or_memory_request(msg, low) is False


def test_code_run_with_url_planner_not_smalltalk():
    """has_url 이면 planner 선점 — 인사 하드룰보다 뒤가 아니라 앞에서 걸러짐 확인용."""
    msg = "https://raw.githubusercontent.com/foo/bar/hello.py 내용 실행해줘"
    low = msg.lower()
    r = router_step1_hard_rules(msg, low, "x", _DEPS)
    assert r is not None
    assert r.get("route_type") == "planner"
