from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

import apps.telegram_bot.main as agent_bot  # noqa: E402


def test_should_notify_auto_cancel_short_confused_text():
    assert agent_bot._should_notify_auto_cancel("왜?") is True


def test_should_notify_auto_cancel_normal_new_request_silent():
    req = "윤수르, 네 지식 베이스에서 최근 AI 논문 하나 요약해 줘."
    assert agent_bot._should_notify_auto_cancel(req) is False
