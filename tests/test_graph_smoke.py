"""LangGraph 조립 스모크 (외부 호출 없음)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

pytestmark = pytest.mark.integration

from agent_graph import build_graph  # noqa: E402


def test_build_graph_exposes_expected_nodes():
    g = build_graph(checkpointer=None)
    nodes = list(g.get_graph().nodes)
    for name in ("router", "direct_answer", "executor", "monitor", "planner", "planner_debate", "use_existing_tool"):
        assert name in nodes, f"missing node {name!r}, got {nodes}"
