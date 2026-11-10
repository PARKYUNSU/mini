"""E2B 샌드박스에 넘기는 env 구성 (minimal 기본 / full 은 명시할 때만)."""

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


def test_e2b_sandbox_envs_default_is_minimal(monkeypatch):
    """설정이 없으면 `.env` 키를 넘기지 않는다. 날씨 키만 넘기고 WEATHER_API_KEY 별칭을 붙인다."""
    import core.execution.agent_sandbox as m

    monkeypatch.setattr(m, "load_dotenv", lambda **kw: None)
    monkeypatch.delenv("E2B_SANDBOX_ENV_MODE", raising=False)
    monkeypatch.delenv("E2B_SANDBOX_EXTRA_KEYS", raising=False)
    monkeypatch.setenv("TELEGRAM_TOKEN", "t")
    monkeypatch.setenv("ZZZ_UNIQUE_ROUTING_TEST_MARK", "1")
    monkeypatch.setenv("OPENWEATHERMAP_API_KEY", "w")

    d = m._e2b_sandbox_envs()
    assert "TELEGRAM_TOKEN" not in d and "ZZZ_UNIQUE_ROUTING_TEST_MARK" not in d
    assert d["OPENWEATHERMAP_API_KEY"] == "w" and d["WEATHER_API_KEY"] == "w"
    assert "E2B_API_KEY" not in d


def test_e2b_sandbox_envs_empty_extra_passes_nothing(monkeypatch):
    import core.execution.agent_sandbox as m

    monkeypatch.setattr(m, "load_dotenv", lambda **kw: None)
    monkeypatch.delenv("E2B_SANDBOX_ENV_MODE", raising=False)
    monkeypatch.setenv("E2B_SANDBOX_EXTRA_KEYS", "")
    monkeypatch.setenv("OPENWEATHERMAP_API_KEY", "w")

    assert set(m._e2b_sandbox_envs()) == {"LANG", "PYTHONUTF8", "PYTHONIOENCODING"}


def test_e2b_sandbox_envs_full_only_when_asked(monkeypatch):
    import core.execution.agent_sandbox as m

    monkeypatch.setattr(m, "load_dotenv", lambda **kw: None)
    monkeypatch.setenv("E2B_SANDBOX_ENV_MODE", "full")
    monkeypatch.setenv("ZZZ_UNIQUE_ROUTING_TEST_MARK", "1")

    d = m._e2b_sandbox_envs()
    assert d.get("ZZZ_UNIQUE_ROUTING_TEST_MARK") == "1"
    assert "E2B_API_KEY" not in d
