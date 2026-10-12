"""논문 수집 누락 감시 — ai_worker 안에서 돈다.

왜 (2026-10-12): 스케줄러 데몬(``apps.scheduler.run_scheduler``)이 2026-05-29 ~ 10-06 동안 돌지 않아
4개월 치 논문이 비었는데 아무 알림도 없었다. 데몬 안에서 확인하면 데몬이 죽었을 때 못 알리므로
**봇 worker** 에서 본다. 둘 다 죽었다면 맥미니가 멈춘 것이라 봇 무응답으로 드러난다.

매일 ``INGEST_WATCHDOG_AT``(기본 03:30, 서울) 이후 한 번:
- 오늘자 ``.cron/arxiv_pipeline_ok_YYYY-MM-DD.marker`` 가 없으면 알림 (01:00 수집 실패/미실행)
- 스케줄러 데몬 프로세스가 없으면 알림
하루 한 번만 보낸다(``.cron/ingest_watchdog_alert_YYYY-MM-DD.marker``). ``INGEST_WATCHDOG=0`` 이면 끈다.
"""

from __future__ import annotations

import os
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

__all__ = ["check_ingest", "start_ingest_watchdog"]

_ROOT = Path(__file__).resolve().parents[2]
_CRON = _ROOT / ".cron"
_TZ = ZoneInfo("Asia/Seoul")


def check_ingest(now: datetime, cron_dir: Path, scheduler_alive: bool, at: str = "03:30") -> str | None:
    """알릴 내용이 있으면 메시지, 없으면 None. 순수 함수(파일 존재만 본다)."""
    hh, mm = (int(x) for x in at.split(":"))
    if (now.hour, now.minute) < (hh, mm):
        return None
    day = now.date().isoformat()
    if (cron_dir / f"ingest_watchdog_alert_{day}.marker").exists():
        return None
    problems = []
    if not (cron_dir / f"arxiv_pipeline_ok_{day}.marker").exists():
        problems.append(f"오늘({day}) arXiv 수집 성공 기록이 없습니다 (01:00 수집 실패 또는 미실행).")
    if not scheduler_alive:
        problems.append("스케줄러 데몬(apps.scheduler.run_scheduler)이 떠 있지 않습니다.")
    if not problems:
        return None
    return "🚨 논문 수집 점검\n" + "\n".join(f"- {p}" for p in problems) + \
        "\n확인: ~/Library/Logs/mini-runscheduler.log · launchctl list | grep runscheduler"


def _scheduler_alive() -> bool:
    try:
        r = subprocess.run(["pgrep", "-f", "apps.scheduler.run_scheduler"], capture_output=True, timeout=10)
        return r.returncode == 0
    except Exception:
        return True  # 확인 실패를 '죽음'으로 단정하지 않는다


def _loop(poll_sec: float) -> None:
    from pipelines.ingest.main import _send_telegram_notification

    at = os.getenv("INGEST_WATCHDOG_AT", "03:30")
    while True:
        try:
            now = datetime.now(_TZ)
            msg = check_ingest(now, _CRON, _scheduler_alive(), at=at)
            if msg:
                _send_telegram_notification(msg)
                (_CRON / f"ingest_watchdog_alert_{now.date().isoformat()}.marker").write_text(now.isoformat())
                print(f"[ingest_watchdog] 알림 전송: {msg.splitlines()[1:]}", flush=True)
        except Exception as e:  # 감시가 worker 를 죽이지 않게
            print(f"[ingest_watchdog] 점검 오류: {type(e).__name__}: {e}", flush=True)
        time.sleep(poll_sec)


def start_ingest_watchdog(poll_sec: float = 300.0) -> None:
    if os.getenv("INGEST_WATCHDOG", "1").strip() == "0":
        print("[ingest_watchdog] INGEST_WATCHDOG=0 — 끔", flush=True)
        return
    threading.Thread(target=_loop, args=(poll_sec,), daemon=True, name="ingest_watchdog").start()
    print(f"[ingest_watchdog] 시작 (매일 {os.getenv('INGEST_WATCHDOG_AT', '03:30')} 이후 점검)", flush=True)
