# 통합 스케줄 · Cron 정리

맥에서 **시스템 crontab을 직접 건드리지 않아도** 되는 경우가 많습니다. 실제로는 **`apps.scheduler.run_scheduler`** 프로세스가 **60초마다** `schedule.run_pending()`을 호출해 작업을 넣습니다.

## 필수: 프로세스 하나는 상시

| 실행 주체 | 하는 일 |
|-----------|---------|
| **`python3 -m apps.scheduler.run_scheduler`** (또는 `./start_scheduler_daemon.sh`) | arXiv·morning_scraper·Phase35 심사·Boardroom 시각 트리거 + (선택) LLM 논문 토론 배치 + **cron_engine** 1분 폴링 |
| **`python3 -m apps.telegram_bot.main`** | 봇 폴링(별도). 봇 단독 시에도 cron 워커 스레드가 뜨는 경로 있음(락으로 `run_scheduler`와 중복 방지) |

**`run_scheduler`가 꺼져 있으면** 매일 arXiv·Phase35/morning·Boardroom 시각 작업·(켜 두었다면) LLM 토론 배치가 돌지 않습니다. 상시 기동을 권장합니다.

## 시각별 작업 표 (`run_scheduler.py`)

| 작업 | 시각 | 조건 | 실행 내용 | 로그·비고 |
|------|------|------|-----------|-----------|
| **arXiv 파이프라인** | **`ARXIV_PIPELINE_SCHEDULE_AT`** (기본 **01:00**) | `GEMINI_API_KEY`(등) 있음 | `python -m pipelines.ingest.main` | 표준출력은 스케줄러 로그에 합류 |
| **LLM 논문 토론 배치** | **월~금 02:00** | Gemini 키 있음 **그리고** `LLM_DEBATE_SCHEDULE_ENABLED=1` | `llm_debate_scheduler --test …` | 기본 **`ENABLED` 미설정 = 꺼짐**. 켠 경우: `.cron/llm_debate_batch_stdout.log` |
| **morning_scraper** | **`MORNING_SCRAPER_SCHEDULE_AT`** (기본 **07:30**) | `PHASE35_SCHEDULE_ENABLED`≠0 (기본 **켜짐**) | `python -m apps.backfill.morning_scraper` **동기** `subprocess.run` | 스케줄러 표준출력 합류 |
| **Phase35 YES 심사·브리핑** | **`PHASE35_CURATOR_SCHEDULE_AT`** (기본 **08:00**) | 동일 마스터 스위치 | `python -m apps.backfill.phase35_auto_curator` **자식 Popen** | `.cron/phase35_curator_stdout.log` |
| **Boardroom** | **`BOARDROOM_SCHEDULE_AT`** (기본 **10:00**) · **매일(월~일)** 기본 | `BOARDROOM_SCHEDULE_ENABLED`≠0 (기본 **켜짐**) | `python -m apps.boardroom.swarm_meeting` **자식 Popen** | `.cron/boardroom_stdout.log`, PID: `.cron/boardroom_child.pid` |
| **주일 찬양 제목 정리** | **수 08:35** | `NOTION_TOKEN` 있음, `CHURCH_LYRICS_SCHEDULE_ENABLED`≠0 | `python -m apps.church_lyrics rename` (스레드) | `.cron/church_lyrics_stdout.log`, `.cron/job_runs.jsonl` |
| **주일 찬양 가사 게시** | **토 09:00** (콘티 없으면 **11:00** 재시도) | 동일 | `python -m apps.church_lyrics lyrics` (스레드) | 동일. 종료 코드 2 = 콘티 없음 → `.cron/church_lyrics_pending_*.marker` |
| **주일 찬양 가사 DB 저장** | **매시 10분** | 동일 | `python -m apps.church_lyrics harvest` (스레드) | 동일. '확인 완료' 체크된 콜아웃의 가사를 찬양 가사 DB로 |

08:00 심사 전에 **07:30 morning_scraper**가 직전에 돌도록 두 작업 모두 같은 마스터 스위치로 묶였습니다. arXiv 일일 수집은 기본 **새벽 01:00**입니다. 시스템 **crontab에 동일 명령이 있으면 중복 실행**되므로 제거하세요.

### arXiv 파이프라인 (`.env`)

| 변수 | 의미 |
|------|------|
| `ARXIV_PIPELINE_SCHEDULE_AT` | `HH:MM` (서버 로컬 시각). 기본 `01:00`. Gemini 키 없으면 job 미등록. |
| `ARXIV_INGEST_BATCH_SIZE` | 한 번의 API 호출당 메타 편수 (기본 `50`, 최대 300). |
| `ARXIV_INGEST_MAX_SCAN` | 한 실행에서 페이징으로 스캔할 메타 최대 편수 (기본 `200`, 최대 2000). 큐에 중복이 많을수록 키우면 신규를 더 찾음. |
| `ARXIV_INGEST_TARGET_NEW` | 선택. 신규 JSONL 저장 N편에 도달하면 같은 실행에서 뒤 메타는 생략 (부하 제한, `0` = 끔). |

스케줄러가 기동하는 Boardroom 자식에는 **`BOARDROOM_SCHEDULE_SKIP_IF_NO_YES=1`가 코드상 항상 지정**됩니다(YES 안건 없으면 즉시 종료). 터미널에서 수동 실행 시에는 `.env` 값만 적용됩니다.

### LLM 논문 토론 배치 (파인튜닝 데이터 생성)

| 변수 | 의미 |
|------|------|
| `LLM_DEBATE_SCHEDULE_ENABLED` | **`1`** 일 때만 월~금 02:00 등록. **미설정·0 = 꺼짐** |
| `LLM_DEBATE_BATCH_DURATION_SEC` | `0`이면 백그라운드 무제한(기본). 양수면 동기 상한(초) |

수동 실행은 그대로: `python3 -m pipelines.debate.llm_debate_scheduler --test`

### Phase35 · morning_scraper (`.env`)

| 변수 | 의미 |
|------|------|
| `PHASE35_SCHEDULE_ENABLED` | `0` 이면 morning_scraper·Phase35 심사 **시각 등록 안 함**. **미설정 시 켜짐.** |
| `MORNING_SCRAPER_SCHEDULE_AT` | `HH:MM`. 기본 `07:30` |
| `PHASE35_CURATOR_SCHEDULE_AT` | `HH:MM`. 기본 `08:00` |

### Boardroom 전용 환경변수 (`.env`)

| 변수 | 의미 |
|------|------|
| `BOARDROOM_SCHEDULE_ENABLED` | `0` 이면 시각 등록 안 함 (수동 실행만). **미설정 시 켜짐.** |
| `BOARDROOM_SCHEDULE_AT` | `HH:MM` (서버 로컬 시각). 예: `10:00` |
| `BOARDROOM_SCHEDULE_DAILY` | **미설정 시 매일(월~일)**. `0`이면 **월~금만** |
| `BOARDROOM_SCHEDULE_SKIP_IF_NO_YES` | 스케줄 자식에만: **`1`**이면 idea_vault에 YES 없으면 즉시 종료 (`run_scheduler`가 자식에 넣음) |

현재 저장소 기본: 스케줄 트리거 시 **`SKIP_IF_NO_YES=1`** 로 넘어가므로, YES 안건이 없으면 Boardroom은 빠르게 빠집니다.

## cron_engine (텔레그램으로 등록한 알림)

- **통합 스케줄러** 또는 **메인 봇**이 띄우는 **백그라운드 스레드**가 `.cron/cron_worker.lock`으로 **한 프로세스만** due job을 1분마다 처리합니다.
- 실행 로그: 터미널 / `scheduler.log`; 실행 이력: `.cron/job_runs.jsonl` 등 (`README.md` 참고).

## 기동 방법 요약

```bash
cd "/path/to/mini"
./start_scheduler_daemon.sh
# 또는 (.venv 없으면 python3 로 교체)
# PYTHONPATH=. nohup python3 -u -m apps.scheduler.run_scheduler >> scheduler.log 2>&1 &
```

- 로그 기본: **`scheduler.log`** (환경변수 `MINI_SCHEDULER_LOG`로 변경 가능).
- 맥 **부팅 후 자동 기동**: `README.md`의 LaunchAgent (`scripts/install_runscheduler_launchagent.sh`) 참고.

## Gemini 키가 없을 때

`run_scheduler`는 **arXiv 파이프라인을 등록하지 않습니다.** LLM 논문 토론 배치도 등록하지 않습니다.  
**Boardroom 스케줄·cron_engine**은 그대로 등록·동작합니다.

## 참고: 진짜 시스템 cron을 쓰고 싶다면

`mini/run_weekly_debate.sh` 등 외부 cron에서 **동일 시각**에 모듈을 직접 호출할 수는 있지만, **`run_scheduler` 한 프로세스로 통합**하는 편이 중복 기동 가드·로그 관리에 유리합니다.
