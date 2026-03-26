"""텔레그램 /debate_start·/debate_stop — llm_debate_scheduler.py --test 백그라운드 실행."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from typing import Optional

from agent_config import (
    LLM_DEBATE_SCHEDULER_PATH,
    LLM_DEBATE_TELEGRAM_DURATION_SEC,
    LLM_DEBATE_TELEGRAM_LOG_PATH,
    LLM_DEBATE_TELEGRAM_PID_PATH,
    PROJECT_ROOT,
)


def _read_debate_pid() -> Optional[int]:
    try:
        if not LLM_DEBATE_TELEGRAM_PID_PATH.exists():
            return None
        raw = LLM_DEBATE_TELEGRAM_PID_PATH.read_text(encoding="utf-8").strip()
        return int(raw) if raw else None
    except Exception:
        return None


def _is_process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def get_running_llm_debate_telegram_pid() -> Optional[int]:
    """텔레그램으로 시작한 논문 토론 배치 PID (수동 nohup 과 별도)."""
    pid = _read_debate_pid()
    if pid and _is_process_alive(pid):
        return pid
    if LLM_DEBATE_TELEGRAM_PID_PATH.exists():
        try:
            LLM_DEBATE_TELEGRAM_PID_PATH.unlink()
        except Exception:
            pass
    return None


def start_llm_debate_telegram_process() -> tuple[bool, str]:
    running = get_running_llm_debate_telegram_pid()
    if running:
        return False, f"이미 논문 토론 배치가 실행 중입니다. (pid={running})"

    if not LLM_DEBATE_SCHEDULER_PATH.is_file():
        return False, f"스크립트 없음: {LLM_DEBATE_SCHEDULER_PATH}"

    duration = LLM_DEBATE_TELEGRAM_DURATION_SEC
    try:
        LLM_DEBATE_TELEGRAM_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LLM_DEBATE_TELEGRAM_LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write("\n" + "=" * 60 + "\n")
            log_file.write(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [telegram] "
                f"llm_debate_scheduler.py --test --duration-sec {duration}\n"
            )
            log_file.write("=" * 60 + "\n")
            log_file.flush()
            proc = subprocess.Popen(
                [
                    sys.executable,
                    "-u",
                    str(LLM_DEBATE_SCHEDULER_PATH),
                    "--test",
                    "--duration-sec",
                    str(duration),
                ],
                cwd=str(PROJECT_ROOT),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"},
            )
        LLM_DEBATE_TELEGRAM_PID_PATH.write_text(str(proc.pid), encoding="utf-8")
        h = duration / 3600
        return (
            True,
            f"논문 토론 배치를 백그라운드에서 시작했습니다. (pid={proc.pid}, 최대 약 {h:.1f}시간)",
        )
    except Exception as e:
        return False, f"시작 실패: {str(e)[:200]}"


def stop_llm_debate_telegram_process() -> tuple[bool, str]:
    pid = get_running_llm_debate_telegram_pid()
    if not pid:
        return False, "텔레그램으로 시작한 논문 토론 배치가 없습니다. (수동 `nohup`이면 터미널에서 종료)"

    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    except Exception:
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception as e:
            return False, f"중지 실패: {str(e)[:200]}"

    try:
        if LLM_DEBATE_TELEGRAM_PID_PATH.exists():
            LLM_DEBATE_TELEGRAM_PID_PATH.unlink()
    except Exception:
        pass

    return True, f"논문 토론 배치를 중지했습니다. (pid={pid})"
