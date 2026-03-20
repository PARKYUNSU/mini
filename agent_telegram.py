"""텔레그램 전송·편집 유틸 (Broken pipe, ReadTimeout 방어 + tenacity 재시도)"""

import re

from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from retry_utils import retry_on_network_error

CANCEL_RESTART_CMDS = ("/cancel", "취소", "취소해", "재시작", "/restart", "🔄 재시작", "❌ 취소")

# <think>, <thinking> 등 Chain-of-Thought 태그 제거 (출력 정제)
_THINKING_PATTERN = re.compile(
    r"</?(?:think|thinking|scratchpad)[^>]*>.*?</(?:think|thinking|scratchpad)>",
    re.DOTALL | re.IGNORECASE,
)


def strip_thinking_tags(text: str) -> str:
    """<think>...</think>, <thinking>...</thinking> 등 사고 과정 블록 제거"""
    if not text or not isinstance(text, str):
        return text
    cleaned = _THINKING_PATTERN.sub("", text).strip()
    return cleaned if cleaned else "(답변을 생성하지 못했습니다)"


def main_keyboard() -> ReplyKeyboardMarkup:
    mk = ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add(KeyboardButton("🔄 재시작"), KeyboardButton("❌ 취소"))
    return mk


def strip_wake_word(text: str) -> str:
    """'윤수르, ~' → 순수 목적 텍스트만"""
    cleaned = re.sub(r"^윤수르[,\.\s]*", "", text.strip()).strip()
    return cleaned if cleaned else text.strip()


@retry_on_network_error
def _telegram_send_impl(bot, chat_id: str, text: str, parse_mode=None, **kwargs) -> None:
    """네트워크 재시도 적용 전송 (일시적 에러만 1분→3분→5분 재시도)"""
    text = strip_thinking_tags(text)
    bot.send_message(chat_id, text, parse_mode=parse_mode, **kwargs)


def safe_telegram_send(bot, chat_id: str, text: str, parse_mode=None, **kwargs) -> bool:
    try:
        _telegram_send_impl(bot, chat_id, text, parse_mode=parse_mode, **kwargs)
        return True
    except (ConnectionError, BrokenPipeError) as e:
        print(f"[DEBUG] 텔레그램 전송 일시 오류 (무시): {e}")
        return False
    except OSError as e:
        if getattr(e, "errno", None) == 32:
            print(f"[DEBUG] 텔레그램 전송 Broken pipe (무시): {e}")
            return False
        raise
    except Exception as e:
        err_str = str(e).lower()
        if "readtimeout" in err_str or "broken pipe" in err_str:
            print(f"[DEBUG] 텔레그램 전송 타임아웃/파이프 (무시): {e}")
            return False
        raise


@retry_on_network_error
def _telegram_send_and_get_impl(bot, chat_id: str, text: str, **kwargs):
    text = strip_thinking_tags(text)
    return bot.send_message(chat_id, text, **kwargs)


def safe_telegram_send_and_get(bot, chat_id: str, text: str, **kwargs):
    try:
        return _telegram_send_and_get_impl(bot, chat_id, text, **kwargs)
    except (ConnectionError, BrokenPipeError) as e:
        print(f"[DEBUG] 텔레그램 전송 일시 오류 (무시): {e}")
        return None
    except OSError as e:
        if getattr(e, "errno", None) == 32:
            print(f"[DEBUG] 텔레그램 전송 Broken pipe (무시): {e}")
            return None
        raise
    except Exception as e:
        err_str = str(e).lower()
        if "readtimeout" in err_str or "broken pipe" in err_str:
            print(f"[DEBUG] 텔레그램 전송 타임아웃/파이프 (무시): {e}")
            return None
        raise


@retry_on_network_error
def _telegram_edit_impl(bot, text: str, chat_id: str, message_id: int) -> None:
    text = strip_thinking_tags(text)
    bot.edit_message_text(text, chat_id, message_id)


def safe_telegram_edit(bot, text: str, chat_id: str, message_id: int) -> bool:
    try:
        _telegram_edit_impl(bot, text, chat_id, message_id)
        return True
    except (ConnectionError, BrokenPipeError) as e:
        print(f"[DEBUG] 텔레그램 수정 일시 오류 (무시): {e}")
        return False
    except OSError as e:
        if getattr(e, "errno", None) == 32:
            print(f"[DEBUG] 텔레그램 수정 Broken pipe (무시): {e}")
            return False
        raise
    except Exception as e:
        err_str = str(e).lower()
        if "readtimeout" in err_str or "broken pipe" in err_str:
            print(f"[DEBUG] 텔레그램 수정 타임아웃/파이프 (무시): {e}")
            return False
        raise
