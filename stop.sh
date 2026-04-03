#!/bin/bash
# 봇·수신기·워커 프로세스 종료 (409 Conflict 방지, 재기동 전 사용)
echo "Stopping bot / telegram_receiver / ai_worker processes..."
pkill -9 -f "agent_bot.py" 2>/dev/null
pkill -9 -f "telegram_receiver.py" 2>/dev/null
pkill -9 -f "ai_worker.py" 2>/dev/null
pkill -9 -f "apps.telegram_bot.main" 2>/dev/null
pkill -9 -f "apps.telegram_bot.telegram_receiver" 2>/dev/null
pkill -9 -f "apps.telegram_bot.ai_worker" 2>/dev/null
count=0
while true; do
  if ! pgrep -f "agent_bot.py" >/dev/null 2>&1 \
    && ! pgrep -f "telegram_receiver.py" >/dev/null 2>&1 \
    && ! pgrep -f "ai_worker.py" >/dev/null 2>&1 \
    && ! pgrep -f "apps.telegram_bot.main" >/dev/null 2>&1 \
    && ! pgrep -f "apps.telegram_bot.telegram_receiver" >/dev/null 2>&1 \
    && ! pgrep -f "apps.telegram_bot.ai_worker" >/dev/null 2>&1; then
    break
  fi
  echo "  Waiting for processes to exit... ($count s)"
  sleep 1
  count=$((count + 1))
  [ "$count" -ge 30 ] && break
done
echo "Done. Wait 15 seconds before starting the bot again (restart.sh also waits 15s)."
