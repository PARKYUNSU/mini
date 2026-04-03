#!/usr/bin/env python3
"""
24시간 무중단 운영용 재시도(Retry) 유틸.
- ConnectionError, Timeout, HTTPError(5xx) 등 일시적 네트워크 에러만 재시도
- 지수 백오프: 1분 → 3분 → 5분, 최대 3회 재시도
- 최종 실패 시 텔레그램 알림
"""

import os
import subprocess
from functools import wraps

from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_incrementing,
)

# 일시적 네트워크 에러로 판단할 예외
try:
    import requests
    _TRANSIENT_EXCEPTIONS = (
        ConnectionError,
        BrokenPipeError,
        TimeoutError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
    )
except ImportError:
    _TRANSIENT_EXCEPTIONS = (ConnectionError, BrokenPipeError, TimeoutError)


def _is_transient_network_error(exc: BaseException) -> bool:
    """일시적 네트워크 에러인지 판별. 논리/문법 에러는 False."""
    if isinstance(exc, _TRANSIENT_EXCEPTIONS):
        return True
    # HTTPError 5xx
    try:
        import requests
        if isinstance(exc, requests.exceptions.HTTPError):
            if exc.response is None:
                return False
            # arXiv export은 burst 요청 시 429로 레이트리밋이 걸릴 수 있음.
            return exc.response.status_code == 429 or exc.response.status_code >= 500
    except ImportError:
        pass
    # OSError (Broken pipe, Connection reset 등)
    if isinstance(exc, OSError) and getattr(exc, "errno", None) in (32, 54, 61, 64, 111):
        return True
    return False


# 1분 → 3분 → 5분 (wait_incrementing: start=60, increment=120)
# 최대 4회 시도 (초기 1회 + 재시도 3회)
retry_on_network_error = retry(
    retry=retry_if_exception(_is_transient_network_error),
    stop=stop_after_attempt(4),
    wait=wait_incrementing(start=60, increment=120),
    reraise=True,
)


retry_on_subprocess_error = retry(
    retry=retry_if_exception(lambda e: isinstance(e, subprocess.CalledProcessError)),
    stop=stop_after_attempt(4),
    wait=wait_incrementing(start=60, increment=120),
    reraise=True,
)


def with_scheduler_retry(task_name: str):
    """스케줄러 subprocess 작업용. 재시도 후 최종 실패 시 텔레그램 알림."""

    def decorator(fn):
        wrapped = retry_on_subprocess_error(fn)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            from tenacity import RetryError
            try:
                return wrapped(*args, **kwargs)
            except RetryError as e:
                send_scheduler_failure_telegram(task_name, str(e.last_attempt.exception()))
                raise
        return wrapper
    return decorator


def send_scheduler_failure_telegram(task_name: str, error_detail: str = "") -> bool:
    """
    스케줄러 작업 최종 실패 시 마스터에게 텔레그램 알림.
    Returns: 전송 성공 여부
    """
    token = os.getenv("TELEGRAM_TOKEN") or ""
    chat_ids = [c.strip() for c in (os.getenv("ALLOWED_CHAT_ID") or "").split(",") if c.strip()]
    if not token or not chat_ids:
        print("⚠️ 텔레그램 알림 스킵: token/chat_id 미설정")
        return False

    msg = (
        "🚨 스케줄러 작업이 네트워크 에러로 최종 실패했습니다\n\n"
        f"작업: {task_name}\n"
        + (f"오류: {error_detail[:300]}" if error_detail else "")
    )

    try:
        import telebot
        bot = telebot.TeleBot(token)
        for cid in chat_ids:
            bot.send_message(cid, msg)
        print(f"✅ 실패 알림 전송: {task_name}")
        return True
    except Exception as e:
        print(f"⚠️ 실패 알림 전송 실패: {e}")
        return False
