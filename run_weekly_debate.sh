#!/bin/bash
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
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [cron] llm_debate_scheduler.py 시작"
echo "============================================================"
exec "/Volumes/T7 Shield/mini/.venv/bin/python" "/Volumes/T7 Shield/mini/llm_debate_scheduler.py" --test
} >> "$LOG_FILE" 2>&1
