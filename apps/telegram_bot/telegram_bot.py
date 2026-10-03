#!/usr/bin/env python3
"""
Phase 3 — 텔레그램 단독 RAG 봇 (AsyncTeleBot).

핵심 RAG는 ``rag_engine`` 과 공유합니다. 운영 본진은 ``telegram_receiver.py`` + 동일 ``rag_engine`` 입니다.

실행:
  cd "/Volumes/T7 Shield/mini" && PYTHONPATH=. .venv/bin/python -m apps.telegram_bot.telegram_bot

백그라운드:
  ./scripts/run_phase3_telegram_bot.sh start|stop|status|logs

다른 터미널에서 동일 토큰으로 ``telegram_receiver`` 가 돌면 409 Conflict 가 납니다.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import traceback
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[misc, assignment]

if load_dotenv:
    load_dotenv(_PROJECT_ROOT / ".env")

from telebot.async_telebot import AsyncTeleBot

try:
    from telebot.asyncio_helper import ApiTelegramException as AsyncApiTelegramException
except ImportError:

    class AsyncApiTelegramException(Exception):
        """telebot 구버전 스텁"""


from apps.telegram_bot import rag_engine
from core.config.agent_config import ALLOWED_CHAT_ID, COLLECTION_NAME, TELEGRAM_TOKEN

logger = logging.getLogger(__name__)


def _allowed_chat_ids() -> set[str]:
    raw = (ALLOWED_CHAT_ID or "").strip()
    if not raw:
        return set()
    return {x.strip() for x in raw.split(",") if x.strip()}


async def _handle_rag_message_async(bot: AsyncTeleBot, chat_id: str, query: str) -> None:
    await bot.send_message(chat_id, rag_engine.RAG_LOADING_MESSAGE, parse_mode=None)
    try:
        answer = await rag_engine.process_rag_query(query)
        await rag_engine.send_rag_answer_async(bot, chat_id, answer)
    except Exception:
        logger.exception("Phase3 단독봇 RAG 실패 chat_id=%s", chat_id)
        traceback.print_exc()
        await bot.send_message(chat_id, rag_engine.RAG_ERROR_MESSAGE, parse_mode=None)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    if not TELEGRAM_TOKEN or not ALLOWED_CHAT_ID:
        print("❌ TELEGRAM_TOKEN, ALLOWED_CHAT_ID 가 mini/.env 에 필요합니다.")
        sys.exit(1)

    allowed = _allowed_chat_ids()
    bot = AsyncTeleBot(TELEGRAM_TOKEN)

    @bot.message_handler(commands=["start", "help"])
    async def cmd_start(message):
        cid = str(message.chat.id)
        if cid not in allowed:
            await bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return
        await bot.reply_to(
            message,
            "안녕하세요. 윤수르 V3 논문 RAG (단독 모드)입니다.\n"
            "질문을 내면 바로 검색합니다. 운영 본진은 telegram_receiver + /rag 입니다.\n"
            "/help — 이 도움말",
            parse_mode=None,
        )

    @bot.message_handler(content_types=["text"])
    async def on_text(message):
        cid = str(message.chat.id)
        if cid not in allowed:
            await bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return
        text = (message.text or "").strip()
        if not text or text.startswith("/"):
            return
        await _handle_rag_message_async(bot, cid, text)

    print(
        "🚀 Phase 3 텔레그램 RAG 봇 (단독) — 폴링 시작\n"
        f"   Chroma: {rag_engine.chroma_persist_path()}\n"
        f"   collection: {COLLECTION_NAME}\n"
        f"   Ollama: {os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434')} "
        f"model={os.environ.get('LOCAL_LLM_MODEL', 'yunsur_v3:latest')}\n"
        "✅ 설정 확인 완료. Telegram getUpdates 연결 중…\n"
        "   (연결되면 이 터미널이 대기 상태로 멈춥니다. 종료: Ctrl+C)\n"
    )
    try:
        await bot.infinity_polling(skip_pending=True, allowed_updates=["message"])
    except AsyncApiTelegramException as exc:
        if getattr(exc, "error_code", None) == 409:
            print(
                "\n❌ 실패: Telegram 409 Conflict — 같은 봇 토큰으로 이미 다른 곳에서 getUpdates 중입니다.\n"
                "   `telegram_receiver` 등을 끈 뒤 다시 실행하세요.\n"
            )
            sys.exit(1)
        raise
    finally:
        try:
            await bot.close_session()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
