# `run_scheduler.py` 계속 켜 두기 (macOS)

텔레그램 **cron 작업**(매일 07:30 등)은 `run_scheduler.py` 프로세스가 살아 있어야 `job_runs.jsonl`에 기록됩니다.

## 1) 권장: LaunchAgent (로그인 시 자동 시작 · 죽으면 재시작)

1. **저장소(mini)가 보이는 경로**에서 터미널 실행 (외장 디스크면 마운트 후)
2. 아래 한 번만 실행 (`mini` 루트는 스크립트 위치로 **자동 계산**):

```bash
cd /path/to/mini
bash scripts/install-run-scheduler-launchagent.sh
```

- 표준 출력: `<mini>/.cron/launchd-scheduler.log`
- 에러: `<mini>/.cron/launchd-scheduler.err.log`

**중지**

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.mini.run-scheduler.plist
```

**주의:** 프로젝트가 외장 디스크(`T7 Shield`)에 있으면, 맥 부팅 직후 디스크가 늦게 붙으면 첫 기동이 실패할 수 있습니다. 그때는 디스크 연결 후 위 `install` 스크립트를 다시 실행하거나, `launchctl kickstart -k gui/$(id -u)/com.mini.run-scheduler` 로 재시작하세요.

## 2) 임시: 터미널에서 백그라운드

```bash
cd "/Volumes/T7 Shield/mini"
mkdir -p .cron
nohup .venv/bin/python run_scheduler.py >> .cron/scheduler-stdout.log 2>&1 &
```

터미널을 닫아도 `nohup`은 보통 유지되지만, **맥 절전·로그아웃**에는 LaunchAgent가 더 낫습니다.

## 3) Python 경로

설치 스크립트가 **`mini/.venv/bin/python`** 을 plist에 넣습니다. venv가 없으면 스크립트가 안내하고 종료합니다. venv를 다른 이름으로 쓰면 스크립트를 수정하거나 `.venv`에 맞추세요.

구조만 보려면 `scripts/com.mini.run-scheduler.plist.example` 참고 (실제 plist는 설치 시 생성).
