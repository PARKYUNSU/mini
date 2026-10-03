#!/bin/bash
# 통합 스케줄러(run_scheduler.py) 백그라운드 기동
# - 매일 01:00 arXiv 파이프라인 (기본, ARXIV_PIPELINE_SCHEDULE_AT · Gemini 키 있을 때)
# - 매일 morning_scraper → Phase35 심사: PHASE35_SCHEDULE_* (.env), 기본 07:30 / 08:00 (마스터 스위치 PHASE35_SCHEDULE_ENABLED)
# - 월~금 02:00 LLM 논문 토론 배치는 **`LLM_DEBATE_SCHEDULE_ENABLED=1`** 일 때만 등록 (기본 꺼짐)
# - Boardroom: BOARDROOM_SCHEDULE_* (.env) — 기본 매일(월~일) 10:00, BOARDROOM_SCHEDULE_DAILY=0 이면 월~금만
# - 1분마다 텔레그램 cron_engine due 작업 점검
# - 이미 떠 있으면 중복 기동하지 않음

set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT" || exit 1

LOG="${MINI_SCHEDULER_LOG:-$ROOT/scheduler.log}"
PY="$ROOT/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "❌ 가상환경 Python 없음: $PY"
  exit 1
fi

# 자기 자신·grep 제외하고 스케줄러 모듈 프로세스만 검사
if pgrep -qf "apps.scheduler.run_scheduler" || pgrep -qf "$ROOT/apps/scheduler/run_scheduler.py"; then
  echo "ℹ️ apps.scheduler.run_scheduler 가 이미 실행 중입니다."
  pgrep -fl -f "run_scheduler" 2>/dev/null || true
  exit 0
fi

export PYTHONUNBUFFERED="${PYTHONUNBUFFERED:-1}"
export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8}"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$ROOT"

nohup "$PY" -u -m apps.scheduler.run_scheduler >>"$LOG" 2>&1 &
echo "✅ apps.scheduler.run_scheduler 기동 (pid=$!, 로그: $LOG)"
