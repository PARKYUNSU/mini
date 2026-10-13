# launchd 에이전트 (맥미니, 사용자 yunsupark)

운영 중인 사본이다. 실제 파일 위치: `~/Library/LaunchAgents/*.plist`, `~/Library/Application Support/mini/*`.

| 에이전트 | 하는 일 | 방식 |
|---|---|---|
| `com.mini.runscheduler` | 통합 스케줄러(01:00 수집 등) | `mini_run_scheduler_launcher.sh` → venv Python 이 `apps.scheduler.run_scheduler` 를 exec. KeepAlive |
| `com.mini.telegrambot` (2026-10-13) | 재부팅 후 텔레그램 봇 자동 기동 | `mini_telegram_bot_launcher.sh` 가 T7·venv·Ollama 준비를 최대 10분 기다린 뒤 `start_telegram_bot.py`(venv Python)가 receiver·ai_worker 를 띄운다. 한 번 실행(KeepAlive 끔), `AbandonProcessGroup` |

**왜 bash 가 아니라 Python 으로 띄우나:** launchd 가 실행한 `/bin/bash` 는 macOS 권한(TCC) 때문에 외장 디스크(T7)의 파일을 읽지 못한다 (`bash: restart.sh: Operation not permitted`). venv Python(Homebrew Python.app)은 접근 권한이 있다.

다시 불러오기: `launchctl bootout gui/$(id -u)/com.mini.telegrambot; launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mini.telegrambot.plist`
수동 재시작은 여전히 `bash restart.sh` (대화형 셸에서는 T7 접근 가능).
