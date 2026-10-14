# launchd 에이전트 (맥미니, 사용자 yunsupark)

운영 중인 사본이다. 실제 파일 위치: `~/Library/LaunchAgents/*.plist`, `~/Library/Application Support/mini/*`.

| 에이전트 | 하는 일 | 방식 |
|---|---|---|
| `com.mini.runscheduler` | 통합 스케줄러(01:00 수집 등) | `mini_run_scheduler_launcher.sh` → venv Python 이 `apps.scheduler.run_scheduler` 를 exec. KeepAlive |
| `com.mini.telegrambot` (2026-10-13) | 재부팅 후 텔레그램 봇 자동 기동 | `mini_telegram_bot_launcher.sh` 가 T7·venv·Ollama 준비를 최대 10분 기다린 뒤 `start_telegram_bot.py`(venv Python)가 receiver·ai_worker 를 띄운다. 한 번 실행(KeepAlive 끔), `AbandonProcessGroup` |

**왜 bash 가 아니라 Python 으로 띄우나:** launchd 가 실행한 `/bin/bash` 는 macOS 권한(TCC) 때문에 외장 디스크(T7)의 파일을 읽지 못한다 (`bash: restart.sh: Operation not permitted`). venv Python(Homebrew Python.app)은 접근 권한이 있다.

다시 불러오기: `launchctl bootout gui/$(id -u)/com.mini.telegrambot; launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mini.telegrambot.plist`
수동 재시작은 여전히 `bash restart.sh` (대화형 셸에서는 T7 접근 가능).

## Chroma 서버 (2026-10-14)

`com.mini.chroma.plist` — `chroma run --path /Volumes/T7 Shield/mini-chroma-rebuild2 --host 127.0.0.1 --port 8001`. 운영 벡터 DB 를 여는 **유일한** 프로세스다. 봇·스케줄러·평가는 `.env` `CHROMA_SERVER_URL="http://127.0.0.1:8001"` 로 `HttpClient` 접속(`core/config/chroma_client.py`). 배경: [`docs/incidents/2026-10-14_chroma_multiwriter.md`](../../docs/incidents/2026-10-14_chroma_multiwriter.md).

- 설치: `cp com.mini.chroma.plist ~/Library/LaunchAgents/ && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mini.chroma.plist`
- 재시작: `launchctl kickstart -k gui/$(id -u)/com.mini.chroma` · 확인: `curl -s http://127.0.0.1:8001/api/v2/heartbeat`
- DB 를 바꿀 때: plist `--path` 와 `.env` `CHROMA_DB_PATH` 를 같이 바꾼다. **서버가 떠 있는 동안 다른 프로세스가 그 폴더를 `PersistentClient` 로 열지 않는다** (재구축 스크립트는 새 폴더에만 쓴다).
- 봇 기동기(`mini_telegram_bot_launcher.sh`)는 Ollama 와 Chroma heartbeat 를 둘 다 기다린다.
