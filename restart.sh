#!/bin/bash
# agent_bot restart script
cd "$(dirname "$0")" || exit 1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] restart.sh 시작"
echo "Stopping existing bot..."
pkill -9 -f "agent_bot.py" 2>/dev/null
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
PYTHONUNBUFFERED=1 .venv/bin/python agent_bot.py
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 봇 종료 (exit=$?)"
