#!/usr/bin/env bash
# Phase 3 텔레그램 RAG 봇 — 터미널 없이 백그라운드(nohup) 실행
# 사용: ./scripts/run_phase3_telegram_bot.sh start|stop|status|logs
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MINI_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PID_FILE="$MINI_ROOT/.phase3_telegram_bot.pid"
LOG_DIR="$MINI_ROOT/logs"
LOG_FILE="$LOG_DIR/phase3_telegram_bot.log"
VENV_PY="$MINI_ROOT/.venv/bin/python"

start() {
	if [[ ! -x "$VENV_PY" ]]; then
		echo "venv 없음: $VENV_PY" >&2
		exit 1
	fi
	if [[ -f "$PID_FILE" ]]; then
		old_pid="$(tr -d ' \n' <"$PID_FILE" || true)"
		if [[ -n "$old_pid" ]] && kill -0 "$old_pid" 2>/dev/null; then
			echo "이미 실행 중입니다 (PID $old_pid). 중지: $0 stop"
			exit 1
		fi
	fi
	mkdir -p "$LOG_DIR"
	cd "$MINI_ROOT"
	nohup env PYTHONPATH=. "$VENV_PY" -u -m apps.telegram_bot.telegram_bot >>"$LOG_FILE" 2>&1 &
	echo $! >"$PID_FILE"
	echo "✓ 백그라운드 시작 PID=$(cat "$PID_FILE")"
	echo "  로그: $LOG_FILE"
	echo "  팔로우: $0 logs   /   중지: $0 stop"
}

stop() {
	if [[ ! -f "$PID_FILE" ]]; then
		echo "PID 파일 없음 — 실행 중이 아닐 수 있습니다."
		exit 0
	fi
	pid="$(tr -d ' \n' <"$PID_FILE" || true)"
	if [[ -z "$pid" ]]; then
		rm -f "$PID_FILE"
		echo "빈 PID 파일 삭제함"
		exit 0
	fi
	if kill -0 "$pid" 2>/dev/null; then
		kill "$pid" 2>/dev/null || true
		echo "종료 신호 전송 PID=$pid (안 꺼지면: kill -9 $pid)"
	else
		echo "프로세스 없음 (PID $pid) — stale PID 파일 삭제"
	fi
	rm -f "$PID_FILE"
}

status() {
	if [[ -f "$PID_FILE" ]]; then
		pid="$(tr -d ' \n' <"$PID_FILE" || true)"
		if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
			echo "실행 중 PID=$pid"
			echo "로그: $LOG_FILE"
			return 0
		fi
	fi
	echo "실행 안 함 (또는 비정상 종료)"
	[[ -f "$PID_FILE" ]] && rm -f "$PID_FILE"
	return 1
}

logs() {
	mkdir -p "$LOG_DIR"
	touch "$LOG_FILE"
	exec tail -f "$LOG_FILE"
}

case "${1:-}" in
start) start ;;
stop) stop ;;
status) status ;;
logs) logs ;;
*)
	echo "사용법: $0 {start|stop|status|logs}" >&2
	echo "  start  — nohup 백그라운드 + $LOG_FILE" >&2
	echo "  stop   — PID 파일 기준 종료" >&2
	echo "  status — 실행 여부" >&2
	echo "  logs   — tail -f 로그" >&2
	exit 1
	;;
esac
