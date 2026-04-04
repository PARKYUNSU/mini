"""하드룰·문맥 충돌 회귀: URL·코드 조각·파일명 속 토큰."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

pytestmark = pytest.mark.unit

from core.graph.agent_router_rules import (  # noqa: E402
    RouterStep1Deps,
    _ascii_greeting_in_smalltalk,
    _is_followup_vague_query,
    _req_lower_for_ascii_greeting_scan,
    is_factual_lookup,
    is_smalltalk_or_memory_request,
    router_step1_hard_rules,
)

_DEPS = RouterStep1Deps(
    agent_tools_dir=_ROOT / "tools" / "runtime" / "agent_tools" / "agent_tools",
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


def test_paper_find_topic_list_goes_rag_not_chroma_inventory():
    """'찾아서 … 목록으로'는 주제 검색 → RAG(B). chromadb_db_inventory(전체 목록만)보다 앞선 규칙."""
    msg = "윤수르, 네 지식 베이스에서 환각(Hallucination) 현상을 다룬 논문 여러 개 찾아서 목록으로 알려줘."
    low = msg.lower()
    r = router_step1_hard_rules(msg, low, "x", _DEPS)
    assert r == {"route_type": "direct_answer", "router_choice": "B"}


def test_wake_word_yunsur_rag_query_not_smalltalk():
    """호칭 '윤수르,'만으로 일상(A) 하드룰에 걸리지 않음 (지식베이스·논문 질의)."""
    msg = (
        "윤수르, 네 지식 베이스에서 환각(Hallucination) 현상을 다룬 논문 여러 개 찾아서 목록으로 알려줘."
    )
    low = msg.lower()
    assert is_smalltalk_or_memory_request(msg, low) is False
    r = router_step1_hard_rules(msg, low, "x", _DEPS)
    assert r is not None
    # 논문+목록이면 chromadb_db_inventory 등으로 잡힐 수 있음. 금지: direct_answer (A)만.
    if r.get("route_type") == "direct_answer":
        assert r.get("router_choice") == "B"


def test_followup_vague_not_tavily():
    """'그거 더 자세히 알려줘' 같은 후속 질의는 Tavily로 빠지면 안 됨."""
    assert _is_followup_vague_query("그거 더 자세히 알려줘") is True
    assert _is_followup_vague_query("그게 뭐야") is True
    assert _is_followup_vague_query("이거 설명해줘") is True
    assert is_factual_lookup("그거 더 자세히 알려줘") is False
    assert is_factual_lookup("그게 뭐야") is False


def test_followup_routes_to_rag_not_tavily():
    """후속 질의 '그거 더 자세히 알려줘'는 RAG(B)로 라우팅."""
    msg = "그거 더 자세히 알려줘"
    low = msg.lower()
    r = router_step1_hard_rules(msg, low, "x", _DEPS)
    assert r is not None
    assert r.get("route_type") == "direct_answer"
    assert r.get("router_choice") == "B"


def test_normal_factual_lookup_still_works():
    """일반 사실 조회('비트코인 뭐야?')는 여전히 factual_lookup으로 분류."""
    assert is_factual_lookup("비트코인 뭐야?") is True
    assert _is_followup_vague_query("비트코인 뭐야?") is False
