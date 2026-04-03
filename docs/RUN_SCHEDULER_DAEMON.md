# `apps.scheduler.run_scheduler` 계속 켜 두기 (macOS)

텔레그램 **cron 작업**(매일 07:30 등)은 통합 스케줄러 프로세스(`python -m apps.scheduler.run_scheduler`)가 살아 있어야 `job_runs.jsonl`에 기록됩니다.

## 1) 권장: LaunchAgent (홈 디렉터리 런처)

외장 디스크에 `mini`가 있을 때는 **`scripts/install_runscheduler_launchagent.sh`** 가 안전합니다 (`~/Library/Application Support/mini/` 런처 + `PYTHONPATH`).

```bash
cd /path/to/mini
bash scripts/install_runscheduler_launchagent.sh
launchctl bootout gui/$(id -u)/com.mini.runscheduler 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/com.mini.runscheduler.plist"
```

- 로그: **`~/Library/Logs/mini-runscheduler.log`** (README §5 참고)

## 2) 저장소 루트에서 백그라운드 (nohup)

```bash
cd "/path/to/mini"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
mkdir -p .cron
nohup .venv/bin/python -u -m apps.scheduler.run_scheduler >> .cron/scheduler-stdout.log 2>&1 &
```

또는 `./start_scheduler_daemon.sh` (동일하게 `-m apps.scheduler.run_scheduler` 사용).

터미널을 닫아도 `nohup`은 보통 유지되지만, **맥 절전·로그아웃**에는 LaunchAgent가 더 낫습니다.

## 3) Python 경로

**`mini/.venv/bin/python`** 과 저장소 루트가 `PYTHONPATH`에 포함되어야 `apps.*`, `core.*`, `pipelines.*` import가 동작합니다. venv가 없으면 `python3 -m venv .venv` 후 `pip install -r requirements.txt`.

구식 **`scripts/install-run-scheduler-launchagent.sh`**(루트의 `run_scheduler.py` 직접 실행)는 레이아웃 변경 후 사용하지 마세요. 대신 위 **`install_runscheduler_launchagent.sh`** 또는 수동 `nohup -m apps.scheduler.run_scheduler` 를 쓰세요.
