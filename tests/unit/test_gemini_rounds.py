"""전 키 429 시 기본은 기다리지 않고 예외 (봇 응답이 900초 멈추지 않게)."""
import pytest

from core.llm import agent_gemini


class _RL(Exception):
    status_code = 429


def test_all_keys_rate_limited_raises_without_sleep(monkeypatch):
    calls, sleeps = [], []

    class Fake:
        def __init__(self, **kw):
            self.key = kw["api_key"]

        def invoke(self, *a, **k):
            calls.append(self.key)
            raise _RL("429")

    monkeypatch.setattr(agent_gemini, "ChatGoogleGenerativeAI", Fake)
    monkeypatch.setattr(agent_gemini.time, "sleep", lambda s: sleeps.append(s))
    monkeypatch.delenv("GEMINI_RATE_LIMIT_ROUNDS", raising=False)
    with pytest.raises(_RL):
        agent_gemini.RotatingGeminiChat(["a", "b", "c"], "m", 0.1).invoke("hi")
    assert calls == ["a", "b", "c"]
    assert max(sleeps) < 10
