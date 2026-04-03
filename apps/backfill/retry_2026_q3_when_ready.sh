#!/usr/bin/env bash
# 2026년 Q3(7~9월)만 백필. 상반기 중(예: 4월)에는 해당 기간 제출분이 거의 없어 생략해도 됨.
# 실제로 7월 이후에 실행하고, export.arxiv.org 429·타임아웃이 잦으면 몇 시간~며칠 뒤 다시 실행하세요.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$ROOT"
LOG="$ROOT/backfill_2026_q3_retry.log"
echo "[$(date -Iseconds)] Q3-only retry start" >>"$LOG"
nohup "$ROOT/.venv/bin/python" -u "$ROOT/apps/backfill/run_backfill_quarterly.py" \
  --year 2026 \
  --category cs.AI \
  --batch-size 15 \
  --continue-on-error \
  --quarters Q3 \
  >>"$LOG" 2>&1 &
echo $! >"$ROOT/.backfill_2026_q3_retry.pid"
echo "started pid=$(cat "$ROOT/.backfill_2026_q3_retry.pid") log=$LOG"
