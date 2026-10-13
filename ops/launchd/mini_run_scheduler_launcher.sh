#!/bin/bash
set -euo pipefail
MINI_ROOT=/Volumes/T7\ Shield/mini
LOG="${HOME}/Library/Logs/mini-runscheduler.log"
mkdir -p "$(dirname "$LOG")"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >>"$LOG"; }
for _ in $(seq 1 120); do
  if [[ -x "$MINI_ROOT/.venv/bin/python" && -f "$MINI_ROOT/apps/scheduler/run_scheduler.py" ]]; then
    log "run_scheduler 시작: $MINI_ROOT"
    cd "$MINI_ROOT"
    export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$MINI_ROOT"
    exec "$MINI_ROOT/.venv/bin/python" -u -m apps.scheduler.run_scheduler >>"$LOG" 2>&1
  fi
  sleep 5
done
log "10분 대기 후에도 MINI_ROOT 준비 실패: $MINI_ROOT"
exit 1
