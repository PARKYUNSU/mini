#!/usr/bin/env python3
"""
서울 날씨 도구 출력을 텔레그램으로 전송 (수동 검증용).

  cd /path/to/mini
  TELEGRAM_TEST_CHAT_ID=123456789 .venv/bin/python scripts/send_seoul_weather_test_telegram.py

또는 .env 에 TELEGRAM_TEST_CHAT_ID 를 넣어 두면 생략 가능.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_weather_module():
    path = ROOT / "tools/runtime/agent_tools/agent_tools/서울_지금_현재_날씨_알려줘.py"
    spec = importlib.util.spec_from_file_location("seoul_weather_tool", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")

    mod = _load_weather_module()
    body = mod.build_seoul_weather_report()
    print(body)
    print("---")

    token = (os.getenv("TELEGRAM_TOKEN") or "").strip()
    chat = (os.getenv("TELEGRAM_TEST_CHAT_ID") or os.getenv("SCHEDULE_CHAT_ID") or "").strip()
    if not token:
        print("TELEGRAM_TOKEN 없음 — 위 출력만 확인하세요.")
        return 0
    if not chat:
        print("TELEGRAM_TEST_CHAT_ID(또는 SCHEDULE_CHAT_ID) 없음 — 텔레그램 전송 생략.")
        return 0

    import telebot

    from apps.telegram_bot.agent_telegram import safe_telegram_send

    bot = telebot.TeleBot(token)
    msg = "🧪 서울 날씨 도구 테스트\n\n" + body
    if len(msg) > 4000:
        msg = msg[:3990] + "…"
    if safe_telegram_send(bot, chat, msg):
        print(f"텔레그램 전송 완료 (chat_id={chat})")
        return 0
    print("텔레그램 전송 실패 (로그 확인)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
