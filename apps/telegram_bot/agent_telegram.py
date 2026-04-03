"""텔레그램 전송·편집 유틸 (Broken pipe, ReadTimeout 방어 + tenacity 재시도)"""

import html
import re

from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from core.execution.retry_utils import retry_on_network_error

try:
    from telebot.apihelper import ApiTelegramException
except ImportError:

    class ApiTelegramException(Exception):
        """telebot 미설치/구버전 시 스텁"""


def _telegram_api_err_str(exc: BaseException) -> str:
    if isinstance(exc, ApiTelegramException):
        return f"{getattr(exc, 'error_code', '')} {getattr(exc, 'description', str(exc))}".strip()
    return str(exc)

CANCEL_RESTART_CMDS = ("/cancel", "취소", "취소해", "재시작", "/restart", "🔄 재시작", "❌ 취소")

# <think>, <thinking> 등 Chain-of-Thought 태그 제거 (출력 정제)
_REDACTED_THINKING_PATTERN = re.compile(
    r"<redacted_thinking\b[^>]*>.*?</redacted_thinking>",
    re.DOTALL | re.IGNORECASE,
)
_THINKING_PATTERN = re.compile(
    r"</?(?:think|thinking|scratchpad)[^>]*>.*?</(?:think|thinking|scratchpad)>",
    re.DOTALL | re.IGNORECASE,
)


def strip_thinking_tags(text: str) -> str:
    """<think>...</think>, <thinking>...</thinking> 등 사고 과정 블록 제거"""
    if not text or not isinstance(text, str):
        return text
    cleaned = _REDACTED_THINKING_PATTERN.sub("", text)
    cleaned = _THINKING_PATTERN.sub("", cleaned).strip()
    return cleaned if cleaned else "(답변을 생성하지 못했습니다)"


def main_keyboard() -> ReplyKeyboardMarkup:
    mk = ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add(KeyboardButton("🔄 재시작"), KeyboardButton("❌ 취소"))
    return mk


def strip_wake_word(text: str) -> str:
    """'윤수르, ~' → 순수 목적 텍스트만"""
    cleaned = re.sub(r"^윤수르[,\.\s]*", "", text.strip()).strip()
    return cleaned if cleaned else text.strip()


def escape_telegram_html(text: str) -> str:
    """Telegram HTML parse_mode용 이스케이프 (& < >)."""
    return html.escape(text or "", quote=False)


def rag_structured_lines_to_html(body: str) -> str:
    """
    RAG 후처리 본문(### 제목 또는 '1. 핵심 주제' 같은 번호 제목 + - bullet)을 Telegram HTML로 변환.
    Markdown 특수문자 파싱 오류를 피하고 줄바꿈은 그대로 유지한다.
    """
    out_lines: list[str] = []
    for raw in (body or "").splitlines():
        line = raw.rstrip()
        if not line.strip():
            out_lines.append("")
            continue
        if line.startswith("### "):
            title = escape_telegram_html(line[4:].strip())
            out_lines.append(f"<b>{title}</b>")
        elif re.match(r"^\d+\.\s+\S", line):
            # "1. 핵심 주제" 형식 (RAG 단순 섹션)
            title = escape_telegram_html(line.strip())
            out_lines.append(f"<b>{title}</b>")
        elif line.startswith("- "):
            out_lines.append("• " + escape_telegram_html(line[2:].strip()))
        else:
            out_lines.append(escape_telegram_html(line.strip()))
    return "\n".join(out_lines)


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
        print(f"[WARN] 텔레그램 전송 OSError: {e}")
        return False
    except ApiTelegramException as e:
        print(f"[WARN] 텔레그램 API 오류(send): {_telegram_api_err_str(e)}")
        return False
    except Exception as e:
        err_str = str(e).lower()
        if "readtimeout" in err_str or "broken pipe" in err_str:
            print(f"[DEBUG] 텔레그램 전송 타임아웃/파이프 (무시): {e}")
            return False
        print(f"[WARN] 텔레그램 전송 실패: {e}")
        return False


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
        print(f"[WARN] 텔레그램 send_and_get OSError: {e}")
        return None
    except ApiTelegramException as e:
        print(f"[WARN] 텔레그램 API 오류(send_and_get): {_telegram_api_err_str(e)}")
        return None
    except Exception as e:
        err_str = str(e).lower()
        if "readtimeout" in err_str or "broken pipe" in err_str:
            print(f"[DEBUG] 텔레그램 전송 타임아웃/파이프 (무시): {e}")
            return None
        print(f"[WARN] 텔레그램 send_and_get 실패: {e}")
        return None


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
        print(f"[WARN] 텔레그램 수정 OSError: {e}")
        return False
    except ApiTelegramException as e:
        print(f"[WARN] 텔레그램 API 오류(edit): {_telegram_api_err_str(e)}")
        return False
    except Exception as e:
        err_str = str(e).lower()
        if "readtimeout" in err_str or "broken pipe" in err_str:
            print(f"[DEBUG] 텔레그램 수정 타임아웃/파이프 (무시): {e}")
            return False
        print(f"[WARN] 텔레그램 수정 실패: {e}")
        return False


def cleanup_status_message(bot, chat_id: str, status_msg) -> None:
    """진행 메시지 삭제. 실패는 무시 (이미 삭제됐거나 권한 문제)."""
    if not bot or not status_msg:
        return
    try:
        bot.delete_message(chat_id, status_msg.message_id)
    except Exception:
        pass


def is_transient_network_error(e: BaseException) -> bool:
    """Broken pipe, Connection reset 등 일시적 네트워크/소켓 오류 여부"""
    err_str = str(e).lower()
    if "broken pipe" in err_str or "errno 32" in err_str:
        return True
    if "connection" in err_str and ("reset" in err_str or "refused" in err_str or "closed" in err_str):
        return True
    if isinstance(e, (ConnectionError, BrokenPipeError)):
        return True
    if isinstance(e, OSError) and getattr(e, "errno", None) == 32:
        return True
    return False


def notify_chat_error(
    bot,
    chat_id: str,
    *,
    headline: str = "🚨 처리 중 오류가 발생했습니다.",
    detail: str = "",
    status_message_id: int | None = None,
    max_len: int = 3600,
) -> bool:
    """
    사용자에게 오류를 반드시 보이게 함. parse_mode 없이 평문만 사용(400 방지).
    status_message_id가 있으면 먼저 해당 메시지를 편집하고, 실패 시 새 메시지 전송.
    내부 예외는 삼킴(로그만).
    """
    if not bot or not chat_id:
        return False
    d = (detail or "").strip().replace("<", "‹").replace(">", "›")
    if len(d) > max_len:
        d = d[: max_len - 30] + "\n…(이하 생략)"
    body = f"{headline}\n\n{d}" if d else headline
    body = strip_thinking_tags(body)
    try:
        if status_message_id is not None:
            if safe_telegram_edit(bot, body[:4096], chat_id, status_message_id):
                return True
        return safe_telegram_send(bot, chat_id, body[:4096])
    except Exception as e:
        print(f"[WARN] notify_chat_error 자체 실패: {e}")
        return False
