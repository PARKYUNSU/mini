#!/bin/bash
# 텔레그램 수신기 + AI 워커 분리 기동 (기본). 단일 프로세스: AGENT_MONOLITH=1 bash restart.sh
cd "$(dirname "$0")" || exit 1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] restart.sh 시작"
echo "Stopping existing processes..."
pkill -9 -f "telegram_receiver.py" 2>/dev/null
pkill -9 -f "ai_worker.py" 2>/dev/null
pkill -9 -f "agent_bot.py" 2>/dev/null
while pgrep -f "telegram_receiver.py" >/dev/null 2>&1; do sleep 1; done
while pgrep -f "ai_worker.py" >/dev/null 2>&1; do sleep 1; done
while pgrep -f "agent_bot.py" >/dev/null 2>&1; do sleep 1; done
echo "Waiting 15s for Telegram to release connection..."
sleep 15
# Reset webhook on Telegram side (helps clear 409)
.venv/bin/python -c "
import os
from dotenv import load_dotenv
load_dotenv()
import telebot
t = os.getenv('TELEGRAM_TOKEN')
if t:
    b = telebot.TeleBot(t)
    b.delete_webhook(drop_pending_updates=True)
    print('Webhook cleared.')
" 2>/dev/null || true
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 새 봇 시작"
export PYTHONFAULTHANDLER=1
export PYTHONUNBUFFERED=1
if [ "${AGENT_MONOLITH:-0}" = "1" ]; then
  echo "모드: 단일 프로세스 (agent_bot.py)"
  .venv/bin/python agent_bot.py
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 봇 종료 (exit=$?)"
else
  echo "모드: 분리 (telegram_receiver.py + ai_worker.py)"
  nohup .venv/bin/python telegram_receiver.py >> bot_receiver.log 2>&1 &
  echo $! > .telegram_receiver.pid
  nohup .venv/bin/python ai_worker.py >> bot_ai_worker.log 2>&1 &
  echo $! > .ai_worker.pid
  echo "receiver PID $(cat .telegram_receiver.pid), worker PID $(cat .ai_worker.pid)"
  echo "로그: bot_receiver.log, bot_ai_worker.log"
fi
