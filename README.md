# AI 데이터 팩토리 (M2 맥 미니용)

arXiv 논문 수집·파싱, RAG, 파인튜닝 데이터 생성, 텔레그램 봇을 포함한 로컬 AI 파이프라인입니다.

---

## 1. 실행 순서

```bash
# 1) 가상환경 활성화
cd /Users/parkyunsu/project/mini
source .venv/bin/activate

# 2) arXiv 논문 수집 → RAG DB 적재 → Q&A 생성 (최초 1회 필수)
python main.py

# 3) Ollama 실행 (Planner, RAG 봇, 토론 스케줄러에서 사용)
ollama serve
ollama pull qwen2.5:7b

# 4) 봇 실행 (택 1 또는 둘 다)
python bot.py          # RAG 봇 (ChromaDB 기반 Q&A)
python agent_bot.py    # Agent 코딩 봇 (계획 → 승인 → 코드 실행)
```

**중요**: `main.py`를 먼저 실행해 `test_chroma_db`와 `test_science_data.jsonl`을 채워야 RAG 봇이 의미 있는 답변을 합니다.

---

## 2. 환경 변수 (.env)

| 변수 | 용도 | 필수 |
|------|------|------|
| `GEMINI_API_KEY` | Q&A 생성, Agent Executor/Monitor | ✅ |
| `RAG_BOT_TOKEN` | RAG 봇 (`bot.py`) | RAG 봇 사용 시 |
| `AGENT_BOT_TOKEN` | Agent 코딩 봇 (`agent_bot.py`) | Agent 봇 사용 시 |
| `TELEGRAM_TOKEN` | RAG/Agent 둘 다 없을 때 사용 | 토큰 1개만 쓸 때 |
| `ALLOWED_CHAT_ID` | 접근 허용 Chat ID (쉼표 구분) | ✅ |
| `E2B_API_KEY` | Agent 코드 실행 (E2B 샌드박스) | Agent 봇 사용 시 |

`RAG_BOT_TOKEN`과 `AGENT_BOT_TOKEN`을 각각 설정하면 두 봇을 동시에 실행할 수 있습니다. 하나만 쓰면 `TELEGRAM_TOKEN`으로 충분합니다.

---

## 3. 봇 사용법

### RAG 봇 (`bot.py`)

- ChromaDB에 저장된 논문 기반 질문 답변
- 질문을 보내면 관련 문서를 검색해 Ollama로 답변 생성

### Agent 코딩 봇 (`agent_bot.py`)

1. **요청** → Planner가 계획 수립
2. **승인/거절** → 텔레그램에서 "승인" 또는 "거절" 입력
3. **승인 시** → Executor가 코드 생성 → E2B 샌드박스에서 실행 → 결과 전송
4. **실패 시** → Monitor가 에러 분석 → Executor 재시도 (최대 2회)

### LLM 토론 스케줄러 (`llm_debate_scheduler.py`)

- 매주 토요일 02:00에 2시간 동안 배치 실행
- `raw_data_queue/`의 JSONL → Qwen(초안) → Gemini(비평) → Qwen(최종) → `finetune_datasets/train_data.jsonl`

```bash
python llm_debate_scheduler.py           # 스케줄 대기
python llm_debate_scheduler.py --test    # 즉시 1회 테스트
```

---

## 4. 프로젝트 구조

```
mini/
├── main.py                 # arXiv 파이프라인 (수집 → RAG → Q&A)
├── bot.py                  # RAG 봇
├── agent_bot.py            # Agent 코딩 봇
├── llm_debate_scheduler.py # LLM 토론 스케줄러
├── run_scheduler.py        # 통합 스케줄러 (main + 토론)
├── src/
│   ├── arxiv_fetcher.py
│   ├── pdf_parser.py
│   ├── data_storage.py
│   ├── rag_processor.py
│   └── qa_generator.py
├── agent_tools/            # Agent가 성공한 코드 저장
├── test_chroma_db/         # RAG 벡터 DB
├── raw_data_queue/         # 토론 스케줄러 입력
└── finetune_datasets/      # 파인튜닝 출력
```

---

## 5. 통합 스케줄러 (24시간 운영)

M2 맥 미니에서 24시간 백그라운드 운영 시:

```bash
python run_scheduler.py
```

- **arXiv 파이프라인**: 매일 06:00 실행
- **LLM 토론**: 매주 토요일 02:00 실행 (2시간)
- **RAG 봇 / Agent 봇**: 별도 터미널에서 `python bot.py`, `python agent_bot.py` 실행

---

## 6. 의존성

```bash
pip install -r requirements.txt
```

---

## 7. 라이선스

MIT
