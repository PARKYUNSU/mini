#!/usr/bin/env bash
# 2026년 Q1·Q2만 재백필 (이미 crawled_papers.jsonl에 있는 ID는 run_backfill.py에서 건너뜀)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$ROOT"
LOG="$ROOT/backfill_2026_q1q2_retry.log"
echo "[$(date -Iseconds)] Q1+Q2 retry start" >>"$LOG"
nohup "$ROOT/.venv/bin/python" -u "$ROOT/apps/backfill/run_backfill_quarterly.py" \
  --year 2026 \
  --category cs.AI \
  --batch-size 15 \
  --continue-on-error \
  --quarters Q1,Q2 \
  >>"$LOG" 2>&1 &
echo $! >"$ROOT/.backfill_2026_q1q2_retry.pid"
echo "started pid=$(cat "$ROOT/.backfill_2026_q1q2_retry.pid") log=$LOG"
