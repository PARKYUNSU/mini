"""
cron_engine due job 폴링 (1분 간격).
- agent_bot / run_scheduler 에서 데몬 스레드로 시작하거나,
- run_cron_worker.py 로 단독 프로세스(nohup)로 실행.
- .cron/cron_worker.lock 으로 중복 실행 방지.
"""

from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

_CRON_LOCK_FP = None


def acquire_cron_worker_lock_nonblocking() -> bool:
    """
    이 프로세스가 worker 락을 잡음. 성공 시 전역 _CRON_LOCK_FP 설정.
    Windows 에는 락 파일 없이 True (단일 사용자 개발용).
    """
    global _CRON_LOCK_FP
    lock_path = PROJECT_ROOT / ".cron" / "cron_worker.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    if sys.platform == "win32":
        return True

    import fcntl

    fp = open(lock_path, "a+", encoding="utf-8")
    try:
        fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        fp.close()
        return False

    _CRON_LOCK_FP = fp
    fp.seek(0)
    fp.truncate()
    fp.write(f"pid={os.getpid()}\n")
    fp.flush()
    return True


def _cron_worker_loop_impl() -> None:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from tools.cron_engine.cron_api import get_due_jobs, mark_job_run
    from tools.cron_engine.lib.storage import append_job_run
    from apps.scheduler.agent_scheduled_runner import run_scheduled_job

    while True:
        try:
            due = get_due_jobs()
            for job in due:
                job_id = job.get("id")
                prompt = job.get("prompt") or job.get("title", "")
                chat_id = job.get("chat_id", "")
                started_at = time.time()

                def _log_run(status: str, error: str | None = None, message_preview: str | None = None):
                    evt = {
                        "event": "cron_job_run",
                        "job_id": job_id,
                        "chat_id": chat_id,
                        "status": status,
                        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(started_at)),
                        "duration_ms": int((time.time() - started_at) * 1000),
                    }
                    if message_preview:
                        evt["prompt_preview"] = message_preview[:80]
                    if error:
                        evt["error"] = error[:200]
                    append_job_run(evt)

                if not prompt or not chat_id:
                    mark_job_run(job_id)
                    _log_run("skipped", message_preview="prompt/chat_id 없음")
                    continue
                print(f"[cron] 실행: {job_id} → {prompt[:40]}... (chat={chat_id})", flush=True)
                result = run_scheduled_job(prompt, chat_id)
                if result == "ok":
                    mark_job_run(job_id)
                    _log_run("succeeded", message_preview=prompt[:80])
                else:
                    _log_run("failed", error=str(result)[:200], message_preview=prompt[:80])
                    print(f"[cron] 실행 실패 (next_run 유지): {result}", flush=True)
        except Exception as e:
            print(f"[cron] worker 예외: {e}", flush=True)
        time.sleep(60)


def start_cron_worker_daemon(*, respect_agent_disable_env: bool = False) -> bool:
    """
    백그라운드 스레드로 cron worker 시작.
    Returns True if this process started the worker thread, False if skipped (lock or env).
    """
    if respect_agent_disable_env:
        v = (os.getenv("AGENT_BOT_CRON_WORKER") or "1").strip().lower()
        if v in ("0", "false", "no", "off"):
            print("[cron] AGENT_BOT_CRON_WORKER=0 — 이 프로세스에서는 cron worker를 시작하지 않습니다.", flush=True)
            return False

    if sys.platform == "win32":
        threading.Thread(target=_cron_worker_loop_impl, daemon=True, name="cron_engine").start()
        print("[cron] worker 스레드 시작 (Windows: 파일 락 없음)", flush=True)
        return True

    if not acquire_cron_worker_lock_nonblocking():
        print(
            "[cron] 다른 프로세스가 이미 cron worker 락을 잡았습니다. "
            "(run_cron_worker.py / run_scheduler / agent_bot 중 하나)",
            flush=True,
        )
        return False

    threading.Thread(target=_cron_worker_loop_impl, daemon=True, name="cron_engine").start()
    print(f"[cron] worker 데몬 스레드 시작 (pid={os.getpid()})", flush=True)
    return True


def run_cron_worker_foreground() -> None:
    """
    단독 프로세스에서 메인 스레드로 무한 루프 (nohup 용).
    락을 못 잡으면 stderr 후 exit(1).
    """
    if sys.platform != "win32":
        if not acquire_cron_worker_lock_nonblocking():
            print(
                "[cron] 락 실패: 이미 다른 cron worker가 실행 중입니다. "
                "중지: 해당 프로세스 종료 또는 .cron/cron_worker.lock 점유 PID 확인",
                flush=True,
            )
            sys.exit(1)
    print(f"[cron] 포그라운드 worker 시작 pid={os.getpid()} (Ctrl+C 또는 SIGTERM 종료)", flush=True)
    _cron_worker_loop_impl()
