#!/bin/bash
# 외부 cron에서 호출 시: 월~금 02:00 등으로 맞추면 apps.scheduler.run_scheduler 의 토론 주기와 일치
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8
LOG_DIR="${YUNSUR_SCHEDULER_LOG_DIR:-$HOME/.yunsur-logs}"
LOG_FILE="${YUNSUR_SCHEDULER_LOG_FILE:-$LOG_DIR/scheduler.log}"
mkdir -p "$LOG_DIR" || exit 1
cd "/Volumes/T7 Shield/mini" || exit 1
{
echo ""
echo "============================================================"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [cron] pipelines.debate.llm_debate_scheduler 시작"
echo "============================================================"
export PYTHONPATH="/Volumes/T7 Shield/mini${PYTHONPATH:+:$PYTHONPATH}"
exec "/Volumes/T7 Shield/mini/.venv/bin/python" -m pipelines.debate.llm_debate_scheduler --test
} >> "$LOG_FILE" 2>&1
