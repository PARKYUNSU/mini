"""E2B 샌드박스에 넘기는 env 구성 (minimal / full)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.unit


def test_e2b_sandbox_envs_minimal(monkeypatch):
    import core.execution.agent_sandbox as m

    monkeypatch.setattr(m, "load_dotenv", lambda **kw: None)
    monkeypatch.setenv("E2B_SANDBOX_ENV_MODE", "minimal")
    monkeypatch.setenv("E2B_SANDBOX_EXTRA_KEYS", "MY_SECRET")
    monkeypatch.setenv("MY_SECRET", "x")

    d = m._e2b_sandbox_envs()
    assert d["PYTHONUTF8"] == "1"
    assert d["MY_SECRET"] == "x"
    assert "E2B_API_KEY" not in d


def test_e2b_sandbox_envs_full_passes_marker(monkeypatch):
    import core.execution.agent_sandbox as m

    monkeypatch.setattr(m, "load_dotenv", lambda **kw: None)
    monkeypatch.delenv("E2B_SANDBOX_ENV_MODE", raising=False)
    monkeypatch.setenv("ZZZ_UNIQUE_ROUTING_TEST_MARK", "1")

    d = m._e2b_sandbox_envs()
    assert d.get("ZZZ_UNIQUE_ROUTING_TEST_MARK") == "1"
    assert "E2B_API_KEY" not in d
