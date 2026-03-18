# AI 데이터 팩토리 (M2 맥 미니용)

arXiv 논문 수집·파싱, RAG, 파인튜닝 데이터 생성, 텔레그램 봇을 포함한 로컬 AI 파이프라인입니다.

---

## 1. 실행 순서

```bash
# 1) 프로젝트 루트로 이동 후 가상환경 활성화
cd /path/to/mini   # 저장소 클론 경로
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
├── agent_bot.py            # 메인 봇 (RAG + Agent 통합)
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

---

## 6. 의존성

```bash
pip install -r requirements.txt
```

---

## 7. 라이선스

MIT
