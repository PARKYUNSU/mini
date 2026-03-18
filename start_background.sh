#!/bin/bash
# nohup으로 봇 백그라운드 실행 (Cursor 종료해도 유지)
cd "$(dirname "$0")"
LOG="bot.log"
echo "봇을 백그라운드로 시작합니다. 로그: $LOG"
nohup bash restart.sh >> "$LOG" 2>&1 &
echo "PID: $!"
echo "종료하려면: pkill -f agent_bot.py"
