#!/usr/bin/env bash
# run_scheduler.py 를 로그인 시 자동 실행 + 크래시 시 재시작 (LaunchAgent)
# mini 루트는 이 스크립트 위치(…/mini/scripts) 기준으로 자동 계산 — 경로 하드코딩 없음.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MINI_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEST="$HOME/Library/LaunchAgents/com.mini.run-scheduler.plist"
VENV_PY="$MINI_ROOT/.venv/bin/python"
SCHEDULER_PY="$MINI_ROOT/run_scheduler.py"
LOGDIR="$MINI_ROOT/.cron"
STDOUT_LOG="$LOGDIR/launchd-scheduler.log"
STDERR_LOG="$LOGDIR/launchd-scheduler.err.log"

mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "$LOGDIR"

if [[ ! -x "$VENV_PY" ]]; then
	echo "⚠️  venv Python 없음: $VENV_PY" >&2
	echo "    cd \"$MINI_ROOT\" && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
	exit 1
fi
if [[ ! -f "$SCHEDULER_PY" ]]; then
	echo "⚠️  run_scheduler.py 없음: $SCHEDULER_PY" >&2
	exit 1
fi

# plist는 절대경로로 생성 (다른 checkout/볼륨에서도 동작)
cat >"$DEST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.mini.run-scheduler</string>
	<key>ProgramArguments</key>
	<array>
		<string>$VENV_PY</string>
		<string>$SCHEDULER_PY</string>
	</array>
	<key>WorkingDirectory</key>
	<string>$MINI_ROOT</string>
	<key>RunAtLoad</key>
	<true/>
	<key>KeepAlive</key>
	<true/>
	<key>StandardOutPath</key>
	<string>$STDOUT_LOG</string>
	<key>StandardErrorPath</key>
	<string>$STDERR_LOG</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)" "$DEST" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"
launchctl enable "gui/$(id -u)/com.mini.run-scheduler"
echo "✓ 설치됨: $DEST"
echo "  MINI_ROOT=$MINI_ROOT"
echo "  로그: $STDOUT_LOG"
echo "  중지: launchctl bootout gui/$(id -u) $DEST"
