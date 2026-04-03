#!/usr/bin/env bash
# 통합 스케줄러를 로그인 시 자동 실행 + 크래시 시 재시작 (LaunchAgent)
# 실행: python -m apps.scheduler.run_scheduler (PYTHONPATH=mini 루트)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MINI_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEST="$HOME/Library/LaunchAgents/com.mini.run-scheduler.plist"
VENV_PY="$MINI_ROOT/.venv/bin/python"
SCHEDULER_MODULE="apps.scheduler.run_scheduler"
SCHEDULER_FILE="$MINI_ROOT/apps/scheduler/run_scheduler.py"
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
if [[ ! -f "$SCHEDULER_FILE" ]]; then
	echo "⚠️  스케줄러 모듈 없음: $SCHEDULER_FILE" >&2
	exit 1
fi

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
		<string>-m</string>
		<string>$SCHEDULER_MODULE</string>
	</array>
	<key>WorkingDirectory</key>
	<string>$MINI_ROOT</string>
	<key>EnvironmentVariables</key>
	<dict>
		<key>PYTHONPATH</key>
		<string>$MINI_ROOT</string>
	</dict>
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
echo "  모듈: $SCHEDULER_MODULE"
echo "  로그: $STDOUT_LOG"
echo "  중지: launchctl bootout gui/$(id -u) $DEST"
