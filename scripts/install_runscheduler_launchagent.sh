#!/bin/bash
# 통합 스케줄러용 LaunchAgent 설치 (외장 볼륨 마운트 대기 + 로그는 홈 디렉터리)
# 사용: mini 저장소가 마운트된 상태에서 한 번 실행
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LAUNCHER_DIR="${HOME}/Library/Application Support/mini"
LAUNCHER="${LAUNCHER_DIR}/mini_run_scheduler_launcher.sh"
PLIST_DST="${HOME}/Library/LaunchAgents/com.mini.runscheduler.plist"
LOG_DST="${HOME}/Library/Logs/mini-runscheduler.log"

mkdir -p "$LAUNCHER_DIR" "${HOME}/Library/LaunchAgents" "${HOME}/Library/Logs"

# 런처: MINI_ROOT 준비될 때까지 대기 (로그는 ~/Library/Logs)
{
  printf '%s\n' '#!/bin/bash' 'set -euo pipefail'
  printf 'MINI_ROOT=%q\n' "$REPO_ROOT"
  printf '%s\n' \
    'LOG="${HOME}/Library/Logs/mini-runscheduler.log"' \
    'mkdir -p "$(dirname "$LOG")"' \
    'log() { echo "[$(date '\''+%Y-%m-%d %H:%M:%S'\'')] $*" >>"$LOG"; }' \
    'for _ in $(seq 1 120); do' \
    '  if [[ -x "$MINI_ROOT/.venv/bin/python" && -f "$MINI_ROOT/run_scheduler.py" ]]; then' \
    '    log "run_scheduler 시작: $MINI_ROOT"' \
    '    cd "$MINI_ROOT"' \
    '    exec "$MINI_ROOT/.venv/bin/python" -u "$MINI_ROOT/run_scheduler.py" >>"$LOG" 2>&1' \
    '  fi' \
    '  sleep 5' \
    'done' \
    'log "10분 대기 후에도 MINI_ROOT 준비 실패: $MINI_ROOT"' \
    'exit 1'
} >"$LAUNCHER"
chmod +x "$LAUNCHER"

# plist: 실행 파일은 항상 내부 디스크(런처)
cat >"$PLIST_DST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mini.runscheduler</string>
    <key>ProgramArguments</key>
    <array>
        <string>${LAUNCHER}</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>${HOME}</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

plutil -lint "$PLIST_DST"

UID_NUM="$(id -u)"
echo ""
echo "✅ 설치 완료"
echo "   런처: $LAUNCHER"
echo "   plist: $PLIST_DST"
echo "   로그: $LOG_DST"
echo ""
echo "이전에 load/bootstrap 한 적이 있으면 먼저 제거:"
echo "  launchctl bootout gui/${UID_NUM}/com.mini.runscheduler 2>/dev/null || true"
echo ""
echo "등록 (macOS 권장):"
echo "  launchctl bootstrap gui/${UID_NUM} \"$PLIST_DST\""
echo ""
echo "해제:"
echo "  launchctl bootout gui/${UID_NUM}/com.mini.runscheduler"
echo "  rm \"$PLIST_DST\""
echo ""
