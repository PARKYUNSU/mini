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

---

## 2. 환경 변수 (.env)

| 변수 | 용도 | 필수 |
|------|------|------|
| `GEMINI_API_KEY` | LLM 토론(Q&A), Agent Executor/Monitor | ✅ |
| `TELEGRAM_TOKEN` | 메인 봇 (`agent_bot.py`) | ✅ |
| `ALLOWED_CHAT_ID` | 접근 허용 Chat ID (쉼표 구분) | ✅ |
| `LOCAL_LLM_MODEL` | 로컬 LLM 모델명 (기본값: `qwen3.5:9b`) | |
| `E2B_API_KEY` | Agent 코드 실행 (E2B 샌드박스) | Agent 봇 사용 시 |
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

- 매주 토요일 02:00에 2시간 동안 배치 실행
- `raw_data_queue/`의 JSONL → Qwen(초안) → Gemini(비평) → Qwen(최종) → `finetune_datasets/train_data.jsonl`
- 이미 토론 완료된 `paper_id`는 `finetune_datasets/debated_paper_ids.jsonl` 기준으로 자동 스킵

```bash
python llm_debate_scheduler.py           # 스케줄 대기
python llm_debate_scheduler.py --test    # 즉시 1회 테스트
python llm_debate_scheduler.py --test --file sample.jsonl --max-records 3
```

### 텔레그램 운영 명령

- `/reboot`: 봇 프로세스 재부팅
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

M2 맥 미니에서 24시간 백그라운드 운영 시, **SSH 접속이 끊겨도 무중단** 실행하려면 `nohup` 사용:

```bash
# 프로젝트 루트로 이동 후 가상환경 활성화
cd /path/to/mini   # 저장소 클론 경로
source .venv/bin/activate

# 스케줄러 백그라운드 실행 (매일 06:00 arXiv, 매주 토 02:00 LLM 토론)
nohup python run_scheduler.py > scheduler.log 2>&1 &

# 메인 봇 백그라운드 실행
nohup python agent_bot.py > agent.log 2>&1 &

# 로그 확인
tail -f scheduler.log
tail -f agent.log
```

- **arXiv 파이프라인**: 매일 06:00 실행 (수집 → RAG → raw_data_queue)
- **LLM 토론**: 매주 토요일 02:00 실행 (2시간, raw_data_queue → finetune_datasets)
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

**회귀 확인 (권장 순서):**

```bash
source .venv/bin/activate
python scripts/check_agent_env.py          # 또는 -q (성공 시 무출력)
python -c "import agent_bot; import agent_graph; print('import OK')"   # 모듈 스모크
pip install -r requirements-dev.txt        # 최초 1회: pytest
pytest tests/ -v --tb=short                # 라우터·골든 케이스 (가벼움, LLM 불필요)
```

- **`test_agent_flow.py`**: Ollama·Gemini·Chroma·E2B·LangGraph 점검. 4번 E2B는 `실행 오류`면 **FAIL**로 표시. 5a는 `print(1+1)`이 산수 하드룰로 **direct_answer** 가는 스모크, 5b는 **code_run→executor** 경로 확인. `ollama serve` 및 `.env` 필요. LLM·E2B 대기로 느릴 수 있음.
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
