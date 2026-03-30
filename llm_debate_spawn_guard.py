"""
llm_debate_scheduler.py --test 자식 프로세스 1개만 추적 (run_scheduler · 텔레그램 /debate_start 공통).

- PID 파일: .cron/llm_debate_child.pid (단일 소스)
- .llm_debate.telegram.pid 는 동일 PID 미러(/debate_stop·외부 스크립트 호환)
- 예전 .cron/llm_debate_batch_scheduler.pid 는 읽기만(잔존 시 중복 방지) 후 정리
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent
DEBATE_CHILD_PID_PATH = _PROJECT_ROOT / ".cron" / "llm_debate_child.pid"
TELEGRAM_PID_MIRROR_PATH = _PROJECT_ROOT / ".llm_debate.telegram.pid"
SCHEDULER_PID_LEGACY_PATH = _PROJECT_ROOT / ".cron" / "llm_debate_batch_scheduler.pid"


def _read_pid_file(path: Path) -> Optional[int]:
    try:
        raw = path.read_text(encoding="utf-8").strip()
        return int(raw) if raw else None
    except Exception:
        return None


def _unlink_quiet(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass


def _pid_cmdline(pid: int) -> str:
    try:
        return subprocess.check_output(
            ["ps", "-p", str(pid), "-o", "command="],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def _is_live_llm_debate_scheduler(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    cmd = _pid_cmdline(pid)
    return "llm_debate_scheduler" in cmd


def _cleanup_stale_pid_file(path: Path, pid: Optional[int]) -> None:
    if pid is None:
        return
    if not _is_live_llm_debate_scheduler(pid):
        _unlink_quiet(path)


def get_running_debate_scheduler_child_pid() -> Optional[int]:
    """
    추적 파일들을 보고, 실제로 살아 있고 cmdline에 llm_debate_scheduler 가 있는 PID 하나 반환.
    죽은 PID·잘못된 파일은 삭제.
    """
    paths = (DEBATE_CHILD_PID_PATH, SCHEDULER_PID_LEGACY_PATH, TELEGRAM_PID_MIRROR_PATH)
    tried: set[int] = set()
    for path in paths:
        pid = _read_pid_file(path)
        if pid is None or pid in tried:
            continue
        tried.add(pid)
        if _is_live_llm_debate_scheduler(pid):
            return pid
        _cleanup_stale_pid_file(path, pid)
    return None


def register_debate_child_pid(pid: int) -> None:
    """기동 직후: 공통 PID 파일 + 텔레그램 미러. 예전 스케줄 전용 파일은 제거."""
    DEBATE_CHILD_PID_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEBATE_CHILD_PID_PATH.write_text(str(pid), encoding="utf-8")
    TELEGRAM_PID_MIRROR_PATH.write_text(str(pid), encoding="utf-8")
    _unlink_quiet(SCHEDULER_PID_LEGACY_PATH)


def clear_debate_child_pid_if_matches(pid: int) -> None:
    """종료 시: 파일 내용이 pid 와 같을 때만 삭제."""
    for path in (DEBATE_CHILD_PID_PATH, TELEGRAM_PID_MIRROR_PATH, SCHEDULER_PID_LEGACY_PATH):
        try:
            cur = _read_pid_file(path)
            if cur == pid:
                _unlink_quiet(path)
        except Exception:
            pass


def clear_all_debate_child_pid_files() -> None:
    for path in (DEBATE_CHILD_PID_PATH, TELEGRAM_PID_MIRROR_PATH, SCHEDULER_PID_LEGACY_PATH):
        _unlink_quiet(path)
