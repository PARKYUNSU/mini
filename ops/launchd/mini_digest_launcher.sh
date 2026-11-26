#!/bin/bash
# 주간 논문 다이제스트 (2026-11-26 등록, 7차 회신 승인). 월 08:30, 사용자 DM 전용 4주(11-30 · 12-07 · 12-14 · 12-21).
# 4주 뒤에는 보내지 않는다 — 팀 채널 게시 · 연장은 사용자가 따로 결정한다.
set -uo pipefail
MINI_ROOT=/Volumes/T7\ Shield/mini
LOG="${HOME}/Library/Logs/mini-digest.log"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >>"$LOG"; }
if [[ "$(date +%Y%m%d)" > "20261221" ]]; then
  log "DM 4주 끝(12-21) — 보내지 않음. 연장 · 팀 채널은 사용자 결정"
  exit 0
fi
for _ in $(seq 1 60); do
  if [[ -x "$MINI_ROOT/.venv/bin/python" ]] && curl -sf -m 5 http://localhost:11434/api/tags >/dev/null; then
    cd "$MINI_ROOT"
    export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$MINI_ROOT"
    log "다이제스트 시작"
    "$MINI_ROOT/.venv/bin/python" -u scripts/weekly_digest.py --send >>"$LOG" 2>&1
    log "다이제스트 끝 (rc=$?)"
    exit 0
  fi
  sleep 10
done
log "10분 대기 후에도 T7/Ollama 준비 실패"
exit 1
