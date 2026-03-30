"""
llm_debate_scheduler.py --test 자식 프로세스 1개만 추적 (run_scheduler · 텔레그램 /debate_start 공통).

- PID 파일: .cron/llm_debate_child.pid (단일 소스)
- .llm_debate.telegram.pid 는 동일 PID 미러(/debate_stop·외부 스크립트 호환)
- 예전 .cron/llm_debate_batch_scheduler.pid 는 읽기만(잔존 시 중복 방지) 후 정리
"""

from __future__ import annotations
import contextlib
import fcntl
import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Iterator, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent
DEBATE_CHILD_PID_PATH = _PROJECT_ROOT / ".cron" / "llm_debate_child.pid"
TELEGRAM_PID_MIRROR_PATH = _PROJECT_ROOT / ".llm_debate.telegram.pid"
SCHEDULER_PID_LEGACY_PATH = _PROJECT_ROOT / ".cron" / "llm_debate_batch_scheduler.pid"

DEBATE_SPAWN_LOCK_PATH = _PROJECT_ROOT / ".cron" / "llm_debate_spawn.lock"
DEBATE_HEARTBEAT_PATH = _PROJECT_ROOT / ".cron" / "llm_debate_health.json"


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


def _read_json_file(path: Path) -> Optional[dict]:
    try:
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            return None
        return json.loads(raw)
    except Exception:
        return None


def _write_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


@contextlib.contextmanager
def debate_spawn_lock(timeout_sec: float = 20.0, poll_interval_sec: float = 0.1) -> Iterator[None]:
    """
    파일 락 기반 원자적 가드.

    두 경로(run_scheduler / agent_debate_telegram)가 거의 동시에
    get_running...() 확인 → Popen → register...() 순서를 밟는 레이스를 방지한다.
    """
    DEBATE_SPAWN_LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DEBATE_SPAWN_LOCK_PATH, "a+", encoding="utf-8") as f:
        start = time.time()
        while True:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if timeout_sec is not None and (time.time() - start) > timeout_sec:
                    raise TimeoutError(f"토론 배치 spawn 락 획득 실패(>{timeout_sec}s)")
                time.sleep(poll_interval_sec)
        try:
            yield
        finally:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except Exception:
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
        # alive check를 통과하지 못하면, heartbeat도 정리 (다음 get_running 호출 시에도 관측 혼선 방지)
        _unlink_quiet(DEBATE_HEARTBEAT_PATH)


def update_debate_heartbeat(*, pid: int, status: str = "running") -> None:
    """무제한/장시간 배치 운영 관측용 heartbeat(최근 업데이트 시각)."""
    payload = {
        "pid": pid,
        "status": status,
        "updated_at_epoch": time.time(),
        "updated_at_iso": datetime.now().isoformat(timespec="seconds"),
    }
    _write_json_atomic(DEBATE_HEARTBEAT_PATH, payload)


def _get_heartbeat_age_sec_for_pid(pid: int) -> Optional[float]:
    info = _read_json_file(DEBATE_HEARTBEAT_PATH)
    if not info:
        return None
    if info.get("pid") != pid:
        return None
    updated = info.get("updated_at_epoch")
    try:
        updated_f = float(updated)
    except (TypeError, ValueError):
        return None
    return time.time() - updated_f


def get_running_debate_scheduler_child_pid() -> Optional[int]:
    """
    추적 파일들을 보고, 실제로 살아 있고 cmdline에 llm_debate_scheduler 가 있는 PID 하나 반환.
    죽은 PID·잘못된 파일은 삭제.
    """
    paths = (DEBATE_CHILD_PID_PATH, SCHEDULER_PID_LEGACY_PATH, TELEGRAM_PID_MIRROR_PATH)
    tried: set[int] = set()
    max_stale_sec = int(os.getenv("LLM_DEBATE_HEARTBEAT_MAX_STALE_SEC", "900"))
    for path in paths:
        pid = _read_pid_file(path)
        if pid is None or pid in tried:
            continue
        tried.add(pid)
        if _is_live_llm_debate_scheduler(pid):
            # heartbeat가 너무 오래 갱신되지 않으면 "장애 상태"로 보고, 다음 spawn을 허용하기 위해 정리한다.
            age = _get_heartbeat_age_sec_for_pid(pid)
            if age is not None and age > max_stale_sec:
                clear_debate_child_pid_if_matches(pid)
                _unlink_quiet(DEBATE_HEARTBEAT_PATH)
                continue
            return pid
        _cleanup_stale_pid_file(path, pid)
    return None


def register_debate_child_pid(pid: int) -> None:
    """기동 직후: 공통 PID 파일 + 텔레그램 미러. 예전 스케줄 전용 파일은 제거."""
    DEBATE_CHILD_PID_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEBATE_CHILD_PID_PATH.write_text(str(pid), encoding="utf-8")
    TELEGRAM_PID_MIRROR_PATH.write_text(str(pid), encoding="utf-8")
    _unlink_quiet(SCHEDULER_PID_LEGACY_PATH)
    update_debate_heartbeat(pid=pid, status="starting")


def clear_debate_child_pid_if_matches(pid: int) -> None:
    """종료 시: 파일 내용이 pid 와 같을 때만 삭제."""
    for path in (DEBATE_CHILD_PID_PATH, TELEGRAM_PID_MIRROR_PATH, SCHEDULER_PID_LEGACY_PATH):
        try:
            cur = _read_pid_file(path)
            if cur == pid:
                _unlink_quiet(path)
        except Exception:
            pass
    # 종료 후 heartbeat는 관측 혼선을 줄이기 위해 제거
    _unlink_quiet(DEBATE_HEARTBEAT_PATH)


def clear_all_debate_child_pid_files() -> None:
    for path in (DEBATE_CHILD_PID_PATH, TELEGRAM_PID_MIRROR_PATH, SCHEDULER_PID_LEGACY_PATH):
        _unlink_quiet(path)
    _unlink_quiet(DEBATE_HEARTBEAT_PATH)
