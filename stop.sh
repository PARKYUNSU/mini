#!/bin/bash
# Kill all agent_bot processes - run this first if you get 409 Conflict
echo "Stopping all agent_bot processes..."
pkill -9 -f "agent_bot.py" 2>/dev/null
count=0
while pgrep -f "agent_bot.py" >/dev/null 2>&1; do
  echo "  Waiting for processes to exit... ($count s)"
  sleep 1
  count=$((count + 1))
  [ $count -ge 30 ] && break
done
echo "Done. Wait 15 seconds before starting the bot again."
