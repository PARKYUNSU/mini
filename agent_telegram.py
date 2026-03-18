"""텔레그램 전송·편집 유틸 (Broken pipe, ReadTimeout 방어)"""

import re

from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

CANCEL_RESTART_CMDS = ("/cancel", "취소", "취소해", "재시작", "/restart", "🔄 재시작", "❌ 취소")


def main_keyboard() -> ReplyKeyboardMarkup:
    mk = ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add(KeyboardButton("🔄 재시작"), KeyboardButton("❌ 취소"))
    return mk


def strip_wake_word(text: str) -> str:
    """'윤수르, ~' → 순수 목적 텍스트만"""
    cleaned = re.sub(r"^윤수르[,\.\s]*", "", text.strip()).strip()
    return cleaned if cleaned else text.strip()


def safe_telegram_send(bot, chat_id: str, text: str, parse_mode=None, **kwargs) -> bool:
    try:
        bot.send_message(chat_id, text, parse_mode=parse_mode, **kwargs)
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


def safe_telegram_send_and_get(bot, chat_id: str, text: str, **kwargs):
    try:
        return bot.send_message(chat_id, text, **kwargs)
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


def safe_telegram_edit(bot, text: str, chat_id: str, message_id: int) -> bool:
    try:
        bot.edit_message_text(text, chat_id, message_id)
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
