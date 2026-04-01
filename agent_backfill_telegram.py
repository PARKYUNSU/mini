"""텔레그램 /backfill_start·/backfill_stop 에서 쓰는 백필 프로세스 제어."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from typing import Optional

from agent_config import (
    BACKFILL_LOG_PATH,
    BACKFILL_PID_PATH,
    BACKFILL_QUARTERLY_SCRIPT_PATH,
    BACKFILL_SCRIPT_PATH,
    PROJECT_ROOT,
)

_BACKFILL_START_COUNT_PATH = PROJECT_ROOT / ".backfill.start_count"


def _quarterly_backfill_cmd() -> list[str]:
    """환경변수 기반 분기 백필 실행 커맨드 생성."""
    year = (os.getenv("BACKFILL_YEAR") or "2024").strip()
    category = (os.getenv("BACKFILL_CATEGORY") or "cs.AI").strip() or "cs.AI"
    batch_size = (os.getenv("BACKFILL_BATCH_SIZE") or "15").strip()
    time_limit = (os.getenv("BACKFILL_TIME_LIMIT_SEC") or "").strip()
    continue_on_error = (os.getenv("BACKFILL_CONTINUE_ON_ERROR") or "1").strip().lower() in (
        "1",
        "true",
        "yes",
        "y",
        "on",
    )

    cmd = [
        sys.executable,
        "-u",
        str(BACKFILL_QUARTERLY_SCRIPT_PATH),
        "--year",
        year,
        "--category",
        category,
        "--batch-size",
        batch_size,
    ]
    if time_limit.isdigit():
        cmd += ["--time-limit", time_limit]
    if continue_on_error:
        cmd.append("--continue-on-error")
    return cmd


def _read_backfill_pid() -> Optional[int]:
    try:
        if not BACKFILL_PID_PATH.exists():
            return None
        raw = BACKFILL_PID_PATH.read_text(encoding="utf-8").strip()
        return int(raw) if raw else None
    except Exception:
        return None


def _is_process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def get_running_backfill_pid() -> Optional[int]:
    pid = _read_backfill_pid()
    if pid and _is_process_alive(pid):
        return pid
    if BACKFILL_PID_PATH.exists():
        try:
            BACKFILL_PID_PATH.unlink()
        except Exception:
            pass
    return None


def _count_crawled_papers() -> int:
    raw_path = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"
    if not raw_path.exists():
        return 0
    try:
        return sum(1 for line in raw_path.read_text(encoding="utf-8").strip().split("\n") if line.strip())
    except Exception:
        return 0


def start_backfill_process() -> tuple[bool, str]:
    running_pid = get_running_backfill_pid()
    if running_pid:
        return False, f"이미 백필이 실행 중입니다. (pid={running_pid})"

    try:
        start_count = _count_crawled_papers()
        _BACKFILL_START_COUNT_PATH.write_text(str(start_count), encoding="utf-8")

        if not BACKFILL_QUARTERLY_SCRIPT_PATH.is_file() and not BACKFILL_SCRIPT_PATH.is_file():
            return False, f"백필 스크립트 없음: {BACKFILL_QUARTERLY_SCRIPT_PATH}"

        BACKFILL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        cmd = _quarterly_backfill_cmd() if BACKFILL_QUARTERLY_SCRIPT_PATH.is_file() else [
            sys.executable,
            "-u",
            str(BACKFILL_SCRIPT_PATH),
        ]
        with open(BACKFILL_LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write("\n" + "=" * 60 + "\n")
            log_file.write(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [telegram] "
                f"{' '.join(cmd[2:])} 시작\n"
            )
            log_file.write("=" * 60 + "\n")
            log_file.flush()
            proc = subprocess.Popen(
                cmd,
                cwd=str(PROJECT_ROOT),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"},
            )
        BACKFILL_PID_PATH.write_text(str(proc.pid), encoding="utf-8")
        mode = "분기 자동 백필" if BACKFILL_QUARTERLY_SCRIPT_PATH.is_file() else "단일 백필"
        return True, f"{mode}을 백그라운드에서 시작했습니다. (pid={proc.pid})"
    except Exception as e:
        return False, f"백필 시작 실패: {str(e)[:200]}"


def stop_backfill_process() -> tuple[bool, str]:
    pid = get_running_backfill_pid()
    if not pid:
        return False, "현재 실행 중인 백필이 없습니다."

    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    except Exception:
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception as e:
            return False, f"백필 중지 실패: {str(e)[:200]}"

    try:
        if BACKFILL_PID_PATH.exists():
            BACKFILL_PID_PATH.unlink()
    except Exception:
        pass

    current_count = _count_crawled_papers()
    try:
        start_count = (
            int(_BACKFILL_START_COUNT_PATH.read_text(encoding="utf-8").strip())
            if _BACKFILL_START_COUNT_PATH.exists()
            else current_count
        )
        _BACKFILL_START_COUNT_PATH.unlink(missing_ok=True)
    except Exception:
        start_count = current_count
    crawled_this_session = max(0, current_count - start_count)

    return (
        True,
        f"실행 중이던 백필을 중지했습니다. (pid={pid})\n\n📚 이번 백필에서 크롤링한 논문: **{crawled_this_session:,}**편",
    )
