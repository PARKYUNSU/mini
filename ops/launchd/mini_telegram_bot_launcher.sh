#!/bin/bash
# 재부팅 후 텔레그램 봇 자동 기동 (2026-10-13). T7·venv·Ollama 가 준비될 때까지 기다린 뒤 restart.sh 를 한 번 실행한다.
MINI_ROOT="/Volumes/T7 Shield/mini"
LOG="${HOME}/Library/Logs/mini-telegrambot-launcher.log"
log() { echo "[$(date "+%Y-%m-%d %H:%M:%S")] $*" >>"$LOG"; }
for _ in $(seq 1 120); do
  if [[ -x "$MINI_ROOT/.venv/bin/python" && -f "$MINI_ROOT/restart.sh" ]] && curl -sf -m 5 http://localhost:11434/api/tags >/dev/null && curl -sf -m 5 http://127.0.0.1:8001/api/v2/heartbeat >/dev/null; then
    log "준비됨 → start_telegram_bot.py"
    "$MINI_ROOT/.venv/bin/python" "$HOME/Library/Application Support/mini/start_telegram_bot.py" >>"$LOG" 2>&1
    log "기동기 끝 (rc=$?)"
    exit 0
  fi
  sleep 5
done
log "10분 대기 후에도 T7/Ollama 준비 실패"
exit 1
