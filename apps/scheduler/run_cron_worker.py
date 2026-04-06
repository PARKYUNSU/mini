#!/usr/bin/env python3
"""
cron_engine 전용 프로세스 — 등록된 스케줄만 1분마다 점검·실행.

agent_bot / run_scheduler 없이 백그라운드로만 돌릴 때:

  cd /path/to/mini
  nohup .venv/bin/python -u -m apps.scheduler.run_cron_worker >> .cron/cron_worker_stdout.log 2>&1 &

이미 agent_bot 이 worker 락을 잡고 있으면 이 프로세스는 즉시 exit(1) 합니다.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# mini/ 프로젝트 루트 (apps/scheduler/ 의 상위 2단계)
ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from apps.scheduler.agent_cron_worker import run_cron_worker_foreground

if __name__ == "__main__":
    run_cron_worker_foreground()
