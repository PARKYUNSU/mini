#!/usr/bin/env bash
# run_scheduler.py 백그라운드 (arXiv 06:00, LLM 토론 월~금 02:00, cron_engine 루프)
# 이미 떠 있으면 새로 띄우지 않음.

set -euo pipefail
MINI_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$MINI_ROOT"
mkdir -p .cron

if pgrep -f "[p]ython.*apps\.scheduler\.run_scheduler" >/dev/null 2>&1 || pgrep -f "[p]ython.*apps/scheduler/run_scheduler\.py" >/dev/null 2>&1; then
  echo "이미 apps.scheduler.run_scheduler 가 실행 중입니다. PID: $(pgrep -f 'apps.scheduler.run_scheduler' | tr '\n' ' ')"
  exit 0
fi

PY="${MINI_ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "ERROR: $PY 없음. venv 생성 후 다시 실행하세요."
  exit 1
fi

LOG="${MINI_ROOT}/.cron/scheduler-stdout.log"
{
  echo ""
  echo "=== $(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S%z') run_scheduler.py nohup 시작 ==="
} >>"$LOG"

export PYTHONUNBUFFERED=1
export PYTHONIOENCODING=utf-8
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}${MINI_ROOT}"
nohup "$PY" -u -m apps.scheduler.run_scheduler >>"$LOG" 2>&1 &
echo $! >"${MINI_ROOT}/.cron/run_scheduler_bg.pid"
echo "apps.scheduler.run_scheduler 시작 PID=$! (로그: .cron/scheduler-stdout.log)"
