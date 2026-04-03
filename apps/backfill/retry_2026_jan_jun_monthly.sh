#!/usr/bin/env bash
# 2026년 1~6월을 월 단위로 순차 백필 (이미 저장된 논문은 run_backfill.py에서 스킵)
# 하반기(7~12월)는 달력상 해당 월이 지나며 논문이 쌓인 뒤에만 돌리면 됨 (예: 7월 이후에 7월분부터).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$ROOT"
LOG="$ROOT/backfill_2026_monthly_h1.log"
echo "[$(date -Iseconds)] monthly H1 (Jan-Jun) start" >>"$LOG"
nohup "$ROOT/.venv/bin/python" -u "$ROOT/apps/backfill/run_backfill_monthly.py" \
  --year 2026 \
  --months 1-6 \
  --category cs.AI \
  --batch-size 15 \
  --continue-on-error \
  >>"$LOG" 2>&1 &
echo $! >"$ROOT/.backfill_2026_monthly_h1.pid"
echo "started pid=$(cat "$ROOT/.backfill_2026_monthly_h1.pid") log=$LOG"
