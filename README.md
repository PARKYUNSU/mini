# AI 데이터 팩토리 (M2 맥 미니용)

arXiv 논문 수집·파싱, RAG, 파인튜닝 데이터 생성, 텔레그램 봇을 포함한 로컬 AI 파이프라인입니다.

---

## 1. 실행 순서

**Python 3.10+** 권장 (`agent_bot.py`·LangGraph·타입 힌트). macOS 기본 `/usr/bin/python3`(3.9)은 부족할 수 있습니다.

```bash
# 0) (최초 1회) 가상환경 + 의존성 — langchain-ollama 등 누락 시 테스트가 import 단계에서 실패합니다
cd /path/to/mini   # 저장소 클론 경로
python3.12 -m venv .venv   # 또는 python3.11
source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt
python scripts/check_agent_env.py   # 필수 패키지 확인 (통과해야 agent_bot·pytest 의미 있음)

# 1) 프로젝트 루트로 이동 후 가상환경 활성화
cd /path/to/mini
source .venv/bin/activate

# 2) arXiv 논문 수집 → RAG DB 적재 → raw_data_queue 저장 (최초 1회 필수)
python main.py

# 3) Ollama 실행 (Planner, RAG 봇, 토론 스케줄러에서 사용)
ollama serve
ollama pull qwen3.5:9b

# 4) 메인 봇 실행 (RAG + Agent 통합)
python agent_bot.py
```

**중요**: `main.py`를 먼저 실행해 `chroma_db/`와 `raw_data_queue/crawled_papers.jsonl`을 채워야 봇이 의미 있는 답변을 합니다.

### 과거 논문 대량 수집 (백필, 기간 기반)

`main.py`는 매일 소량만 수집합니다. **기간을 지정**해 과거 논문을 일괄 수집하려면:

```bash
python run_backfill.py                          # 기본: 2024-01-01 ~ 2024-12-31
python run_backfill.py -s 2023-01-01 -e 2023-12-31   # 2023년 전체
python run_backfill.py -s 2024-06-01 -e 2024-12-31 -b 20  # 20개씩 페이징
```

- `-s, --start-date`: 수집 시작일 (YYYY-MM-DD, 기본 2024-01-01)
- `-e, --end-date`: 수집 종료일 (YYYY-MM-DD, 기본 2024-12-31)
- `-b, --batch-size`: API 한 번에 가져올 개수 (기본 15, 10~20 권장)
- `-c, --category`: arXiv 카테고리 (기본 cs.AI)

백필은 **수집 + raw_data_queue 저장 + ChromaDB 적재**까지만 담당합니다.
학습용 Q&A 생성은 `llm_debate_scheduler.py`가 전담합니다.

**정보 오염 방지**: 오래된 논문은 구시대 지식이 될 수 있어, 최신 1~2년 치만 수집하는 것을 권장합니다.

### `/papers` 숫자가 줄었을 때 (큐 보충 정책)

텔레그램 `/papers`는 **`raw_data_queue/crawled_papers.jsonl`에 남아 있는 논문**만 셉니다. LLM 토론 배치가 끝나면 일부가 `raw_data_queue/processed/`로 옮겨져 숫자가 줄어드는 것이 정상입니다.

- **권장**: `processed/`를 통째로 되돌리기보다 **백필(또는 매일 `main.py` 스케줄)**로 **새 논문**을 큐에 쌓습니다.
- **빠른 보충**: 최근 N일 구간만 백필하려면 `bash scripts/refill_crawled_queue.sh` (기본 N=90, `REFILL_QUEUE_LOOKBACK_DAYS`로 변경 가능). `run_backfill.py` 인자만 쓰려면 `bash scripts/refill_crawled_queue.sh -- -s 2025-01-01 -e 2025-03-01`.

---

## 2. 환경 변수 (.env)

`agent_bot.py` 기동 시 **Groq + Gemini 키(최소 1개)**·텔레그램이 모두 필요합니다. (코드: `agent_bot.py` `main()` 초기 검사)

| 변수 | 용도 | 필수 |
|------|------|------|
| `GROQ_API_KEY` | Agent **Executor / Monitor** (코딩·검수) | ✅ (`agent_bot`) |
| `GEMINI_API_KEY` | 라우터 폴백·도구·Tavily 요약·**LLM 토론(Gemini 비평)** 등 | ✅ (`agent_bot`, 키 1개 이상) |
| `GEMINI_API_KEYS` | 쉼표 구분 다중 키 — 있으면 이 목록만 사용 (`GEMINI_API_KEY` 단독 설정 무시) | 위와 동일 |
| `GEMINI_API_KEY_2` … `_8` | `GEMINI_API_KEYS`가 비어 있을 때 순서대로 합쳐서 사용 (429 시 순환) | 선택 |
| `TELEGRAM_TOKEN` | 메인 봇 (`agent_bot.py`) | ✅ |
| `ALLOWED_CHAT_ID` | 접근 허용 Chat ID (쉼표 구분) | ✅ |
| `LOCAL_LLM_MODEL` | 로컬 LLM 모델명 (기본값: `qwen3.5:9b`) | |
| `E2B_API_KEY` | Agent 코드 실행 (E2B 샌드박스) | Agent 봇 사용 시 |
| `E2B_SANDBOX_ENV_MODE` | `full`(기본): 호스트 환경 전부를 샌드박스에 전달. `minimal`: LANG·UTF-8 등만 전달(`.env` 역슬래시·unicodeescape 이슈 완화) | |
| `E2B_SANDBOX_EXTRA_KEYS` | `minimal`일 때 추가로 넘길 키 목록(쉼표 구분), 예: `WEATHER_API_KEY,TAVILY_API_KEY` | |
| `TAVILY_API_KEY` | 웹/뉴스 검색 (Tavily) | 검색 기능 사용 시 |
| `TUYA_*` | Tuya 스마트 플러그 (`agent_tools/smart_plug.py`) — `TUYA_CONTROL_MODE=local`(기본) 또는 `cloud` | 플러그 제어·스케줄 실행 시 |

스마트 플러그 + cron 연동은 **`docs/SMART_PLUG_CRON.md`**, LAN이 막힌 기기는 **`docs/SMART_PLUG_CLOUD.md`** 참고.

---

## 3. 메인 봇 사용법 (`agent_bot.py`)

RAG(논문 질문 답변) + Agent(코딩 실행) 통합 봇입니다.

1. **요청** → Planner가 계획 수립 (RAG 검색 + 기존 도구 검색 포함)
2. **승인/거절** → 텔레그램에서 "승인" 또는 "거절" 입력
3. **승인 시** → Executor가 코드 생성 → E2B 샌드박스에서 실행 → 결과 전송
4. **실패 시** → Monitor가 에러 분석 → Executor 재시도 (최대 2회)

> `bot.py`는 단순 RAG 테스트용 Legacy. 24시간 구동 시 사용하지 않음.

### LLM 토론 스케줄러 (`llm_debate_scheduler.py`)

- **월~금 02:00** 배치는 `run_scheduler.py`가 `llm_debate_scheduler.py --test` 호출. **`LLM_DEBATE_BATCH_DURATION_SEC`** (기본 **0**): `0`이면 **시간 제한 없이 백그라운드 기동**만 하고 스케줄 메인 루프는 즉시 돌아옵니다(로그: `.cron/llm_debate_batch_stdout.log`). **실행 중인 토론 배치 PID는 `.cron/llm_debate_child.pid`에 기록되고, `.llm_debate.telegram.pid`에 동일 값이 미러됩니다**(`llm_debate_spawn_guard`). 스케줄·텔레그램 어느 쪽으로 띄웠든 **이미 `llm_debate_scheduler` 자식이 살아 있으면 중복 기동하지 않습니다.** 양수면 그만큼 초 동안 **동기** 실행(기간 동안 PID 파일 유지 후 종료 시 정리).
- 텔레그램 **`/debate_start`** 는 **`LLM_DEBATE_TELEGRAM_DURATION_SEC`** (기본 **0** = 무제한, 별도 프로세스, **위와 동일한 중복 가드**).
- `raw_data_queue/`의 JSONL → Qwen(초안) → Gemini(비평, 429 시 키 순환) → Qwen(최종) → `finetune_datasets/train_data.jsonl`
- 이미 토론 완료된 `paper_id`는 `finetune_datasets/debated_paper_ids.jsonl` 기준으로 자동 스킵
- 상한을 두려면: `--duration-sec 7200` 또는 `.env`에 초 단위로 양수 설정

```bash
python llm_debate_scheduler.py           # 스케줄 대기
python llm_debate_scheduler.py --test    # 즉시 1회 (기본 시간 한도는 EVENT_DURATION_SEC, `--duration-sec 0` 이면 무제한)
python llm_debate_scheduler.py --test --file sample.jsonl --max-records 3
```

### 텔레그램 운영 명령

- `/reboot`: 봇 프로세스 재부팅
- `/papers` (또는 `/paperlist`, `/논문목록`): `crawled_papers.jsonl` 큐에 있는 논문 목록
- `/debate_start` (또는 `/논문토론시작`): LLM 논문 토론 배치 백그라운드 시작 (`llm_debate_telegram.log`)
- `/debate_stop` (또는 `/논문토론중지`): 추적 중인 토론 배치 중지(스케줄로 띄운 배치 포함, 공통 PID 기준)
- `/backfill_start`: 백필 시작
- `/backfill_stop`: 실행 중인 백필 중지

---

## 4. 프로젝트 구조

```
mini/
├── main.py                 # arXiv 파이프라인 (수집 → RAG → raw_data_queue)
├── run_backfill.py         # 과거 논문 대량 수집 (백필: 수집/RAG 전용)
├── bot.py                  # [Legacy] 단순 RAG 테스트용
├── agent_bot.py            # 텔레그램 진입·run_or_resume (그래프는 agent_graph)
├── agent_backfill_telegram.py  # /backfill_* 용 run_backfill 프로세스 제어
├── pyproject.toml          # pytest 마커·(선택) ruff 설정
├── agent_graph.py          # LangGraph 조립 (build_graph)
├── agent_nodes.py          # 라우터·플래너·실행기·모니터 노드
├── agent_session.py        # 세션 메모리·오답 노트·논문 모드·플랜 캐시 등
├── agent_prompts.py        # LLM 시스템/유저 프롬프트 문자열
├── llm_debate_scheduler.py # LLM 토론 스케줄러 (학습용 Q&A 생성 전담)
├── run_scheduler.py        # 통합 스케줄러 (main + 토론)
├── src/
│   ├── arxiv_fetcher.py
│   ├── pdf_parser.py
│   ├── data_storage.py
│   ├── rag_processor.py
│   └── qa_generator.py
├── agent_tools/            # Agent가 성공한 코드 저장
├── agent_learnings/        # 오답 노트 (재시도 후 성공한 에러·해결 요약)
├── chroma_db/              # RAG 벡터 DB
├── raw_data_queue/         # 원본 크롤링 데이터 (JSONL)
└── finetune_datasets/      # 토론 기반 파인튜닝 데이터 + 토론 이력 인덱스
```

---

## 5. 통합 스케줄러 (24시간 운영)

**`run_scheduler.py`가 꺼져 있으면** 월~금 02:00 LLM 토론·매일 06:00 arXiv·텔레그램 cron_engine **전부 동작하지 않습니다.** 반드시 상시 프로세스로 띄워 두세요.

### 한 번에 백그라운드 기동 (권장)

저장소 루트에서:

```bash
cd /path/to/mini
./start_scheduler_daemon.sh
```

이미 떠 있으면 중복 실행하지 않고, 로그는 `scheduler.log`에 이어 붙습니다.

### 수동 nohup

```bash
cd /path/to/mini
source .venv/bin/activate
nohup python -u run_scheduler.py >> scheduler.log 2>&1 &
```

### 재부팅 후에도 자동 실행 (macOS launchd)

외장 디스크(`T7 Shield` 등)에 `mini`가 있으면, plist에서 **바로 그 경로의 Python을 실행**하게 두면 `launchctl load` 시 **`Input/output error`(5)** 가 자주 납니다.  
**런처를 `~/Library/Application Support/mini/`에 두고**, `bootstrap`으로 등록하세요.

```bash
cd /path/to/mini
bash scripts/install_runscheduler_launchagent.sh
launchctl bootout gui/$(id -u)/com.mini.runscheduler 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/com.mini.runscheduler.plist"
```

- **구식 `launchctl load`는 쓰지 마세요.** 최신 macOS는 **`launchctl bootstrap gui/$(id -u) …`** 가 맞습니다.
- 로그: **`~/Library/Logs/mini-runscheduler.log`**

해제:

```bash
launchctl bootout gui/$(id -u)/com.mini.runscheduler
rm ~/Library/LaunchAgents/com.mini.runscheduler.plist
```

### 메인 봇 (별도 프로세스)

```bash
nohup python -u agent_bot.py >> agent.log 2>&1 &
tail -f scheduler.log
tail -f agent.log
```

- **arXiv 파이프라인**: 매일 06:00 실행 (수집 → RAG → raw_data_queue)
- **LLM 토론**: 월~금 02:00 실행 (각 최대 2시간, raw_data_queue → finetune_datasets)
- **메인 봇**: 위 nohup으로 백그라운드 실행 시 SSH 종료 후에도 유지됨

### 텔레그램으로 등록한 스케줄 (cron_engine)

- **실행 주체**: `run_scheduler.py`가 떠 있어야 함. `agent_bot.py`만 켜 두면 **등록만 되고 실행 루프는 돌지 않음**.
- **시간 기준**: 작업에 저장된 `timezone`(기본 `Asia/Seoul`) 기준 **한국 시간**으로 `next_run_at`을 계산·비교함. 텔레그램 API와 무관.
- **실패·실행 여부 확인**:
  - `scheduler.log`에서 `[cron] 실행:` / `[cron] worker 예외:` 검색
  - `.cron/job_runs.jsonl` — 각 실행의 `status`: `succeeded` / `failed` / `skipped`

---

## 6. 의존성

```bash
pip install -r requirements.txt
python scripts/check_agent_env.py
```

- **`langchain-ollama`**: 라우터·플래너 등 로컬 Qwen (`ChatOllama`) — `requirements.txt`에 포함. 미설치 시 `ModuleNotFoundError: langchain_ollama`.
- 점검 스크립트: `python scripts/check_agent_env.py` (`-q` 성공 시 무출력)
- 선택 플래그: `--keys` (Gemini/E2B/텔레그램/Tavily 키 요약), `--services` (Ollama HTTP), `--models` (HF 캐시·임베딩 흔적)

**회귀 확인 (권장 순서):**

```bash
source .venv/bin/activate
python scripts/check_agent_env.py          # 또는 -q (성공 시 무출력)
python scripts/check_agent_env.py --keys --services --models   # 통합 테스트 전 선택
python -c "import agent_bot; import agent_graph; print('import OK')"   # 모듈 스모크
pip install -r requirements-dev.txt        # 최초 1회: pytest, pytest-timeout(external 120초 제한)
pytest tests/ -v --tb=short                # 단위(라우터·code_run state·골든 등, LLM 불필요)
pytest tests/ -m unit -q                   # 마커만 (pyproject.toml)
pytest tests/ -m "not external" -q         # CI와 동일: Ollama/Gemini/E2B 실호출 테스트 제외
pytest tests/ -m external -q               # 키·서비스 준비된 환경에서만 (실패 시 skip 가능)
pytest tests/ -m integration -q           # 노드 mock·그래프 스모크만
```

**일상 치트시트 (복붙용):**

| 목적 | 명령 |
|------|------|
| CI와 동일 | `pytest tests/ -m "not external" -q` |
| unit만 | `pytest tests/ -m unit -q` |
| integration만 | `pytest tests/ -m integration -q` |
| 실연동(Ollama/Gemini/E2B) | `pytest tests/ -m external -q` |
| 수동 통합 점검 | `python test_agent_flow.py` |
| 그래프만·로그 줄이기 | `python test_agent_flow.py --only graph --quiet-graph` |

**Git 원격 (HTTPS 인증이 번거로우면 SSH 예시):**

```bash
git remote -v
# git remote set-url origin git@github.com:USER/REPO.git
git pull
git push
```

- **봇이 새로 저장하는 도구**는 `agent_tools/saved/` 아래에만 쓰며, 이 디렉터리는 `.gitignore` 처리됩니다. 레포에 포함할 **코어 도구**는 기존처럼 `agent_tools/*.py` 루트에 두면 됩니다.

- **`test_agent_flow.py`** (스크립트, pytest 아님): 외부 서비스 점검. **환경이 없으면 FAIL 대신 SKIP**으로 표시. 시작 시 환경 요약 출력. 옵션: `--only all|ollama|groq|gemini|chroma|e2b|graph` (기본 `all`), `--verbose` (traceback 전체), `--quiet-graph` (5a/5b DEBUG print 억제). 종료 코드는 **FAIL이 하나라도 있을 때만 1**. E2B `실행 오류` 문자열은 FAIL. 5b에서 executor까지 갔으나 샌드박스만 실패하면 **SKIP/WARN** 처리(라우팅은 `tests/test_code_run_state.py`로 검증).
- **`pyproject.toml`**: `pytest` 마커 `unit` / `integration` / `external` 정의.
- **테스트 계층 (요약)**  
  - **A · unit**: `agent_router_rules`, 골든 라우팅, `test_code_run_state`, E2B env 구성 등.  
  - **B · integration**: `tests/test_node_contracts.py`(router/direct_answer/executor/monitor mock), `tests/test_graph_smoke.py`.  
  - **C · external**: `tests/test_external_integration.py` — 로컬에서 키·Ollama 있을 때만 의미 있음.  
  - **D · 수동**: `test_agent_flow.py` 스크립트(SKIP/FAIL 구분).
- **GitHub Actions**: 이 저장소 루트의 `.github/workflows/ci.yml` — `check_agent_env.py -q` 후 `pytest tests/ -m "not external" -q` (Ollama/Gemini/E2B 실호출 제외).
- **`batch_test_runner.py`**: LangGraph + 라우터/직접응답을 **실제 LLM**으로 돌리는 배치. API·로컬 모델 준비된 환경에서만 실행 권장.

**라우터 단위 테스트 (pytest 없이):** `agent_router_rules.py`는 langchain/chromadb 없이 import 가능합니다.

```bash
python tests/test_intentional_syntax_and_router.py
python tests/test_routing_golden.py
```

### 검색 도구 (`tavily_search_tool`) 의존성

- **tavily-python**, **langchain-community**: Tavily Search API (웹 검색 유일 엔진)
- `.env`에 `TAVILY_API_KEY` 설정 (https://tavily.com 에서 발급)

---

## 7. 라이선스

MIT
