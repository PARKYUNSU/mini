#!/usr/bin/env bash
# run_scheduler.py 를 로그인 시 자동 실행 + 크래시 시 재시작 (LaunchAgent)
set -euo pipefail
PLIST_SRC="$(cd "$(dirname "$0")" && pwd)/com.mini.run-scheduler.plist"
DEST="$HOME/Library/LaunchAgents/com.mini.run-scheduler.plist"
mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "/Volumes/T7 Shield/mini/.cron"
cp "$PLIST_SRC" "$DEST"
# 이미 로드돼 있으면 먼저 unload
launchctl bootout "gui/$(id -u)" "$DEST" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"
launchctl enable "gui/$(id -u)/com.mini.run-scheduler"
echo "✓ 설치됨: $DEST"
echo "  로그: /Volumes/T7 Shield/mini/.cron/launchd-scheduler.log"
echo "  중지: launchctl bootout gui/$(id -u) $DEST"
