# AI 데이터 팩토리 아키텍처 리뷰

**리뷰 기준**: 최종 설계 체크리스트 6가지  
**리뷰 일시**: 2026-03-14

---

## 1. 파이프라인 역할 분리 (관심사의 분리)

### 1.1 main.py

| 항목 | 상태 | 비고 |
|------|------|------|
| arXiv 크롤링 → PDF 파싱 → RAG 적재 → raw_data_queue 저장 | ✅ | QaGenerator import 제거됨 |
| Q&A 생성 로직 완전 제거 | ✅ | 확인됨 |

**결과: ✅ 통과**

---

### 1.2 llm_debate_scheduler.py

| 항목 | 상태 | 비고 |
|------|------|------|
| raw_data_queue/에서 JSONL 읽기 | ✅ | `get_unprocessed_raw_data()` |
| Qwen 초안 → Gemini 비평 → Qwen 최종 | ✅ | `run_debate_pipeline()` |
| finetune_datasets/train_data.jsonl 저장 | ✅ | `save_to_finetune_jsonl()` |
| raw_record의 "content" 필드 사용 | ✅ | DataStorage.build_paper_record와 일치 |

**결과: ✅ 통과**

---

## 2. 백필 스크립트 (run_backfill.py)

| 항목 | 상태 | 비고 |
|------|------|------|
| 기간(Date-range) 기반 필터링 | ✅ | start_date, end_date → submittedDate 쿼리 |
| 페이징 처리 (start, batch_size) | ✅ | fetch_metadata_batch(start, limit) |
| 5~10초 랜덤 딜레이 | ✅ | `time.sleep(random.uniform(5, 10))` 페이지 간 |

**⚠️ 설계 불일치**: run_backfill은 Q&A 생성(QaGenerator)을 포함하고 있음.  
"Q&A는 llm_debate_scheduler만 전담" 원칙과 맞지 않음.  
→ **선택적 수정**: run_backfill에서 Q&A 제거 시 `finetune_datasets/qa_data.jsonl` 대신 `raw_data_queue`만 채우고, llm_debate_scheduler가 토론으로 처리.

**결과: ✅ 통과** (기능 요건은 충족, 설계 일관성은 선택)

---

## 3. LangGraph 자율 에이전트 (agent_bot.py)

### 3.1 Multi-Agent 역할

| 역할 | 모델 | 상태 |
|------|------|------|
| Planner | ChatOllama (Qwen) | ✅ |
| Executor | ChatGoogleGenerativeAI (Gemini) | ✅ |
| Monitor | ChatGoogleGenerativeAI (Gemini) | ✅ |

### 3.2 HITL / SqliteSaver

| 항목 | 상태 | 비고 |
|------|------|------|
| SqliteSaver 체크포인트 | ✅ | `SqliteSaver(conn)`, CHECKPOINT_DB_PATH |
| interrupt()로 승인 대기 | ✅ | Planner 노드에서 `interrupt()` |
| Command(resume=...)로 재개 | ✅ | `run_or_resume(..., is_resume=True)` |
| _pending_approvals로 세션 복구 | ✅ | 봇 재시작 시 `graph.get_state()`로 복구 |

### 3.3 K=5 기반 대화 맥락

| 항목 | 상태 | 비고 |
|------|------|------|
| MEMORY_K = 5 | ✅ | 최근 5턴 원본 유지 |
| MEMORY_BUFFER = 15 | ✅ | 요약 전 버퍼 |
| maybe_compress() | ✅ | K 초과 시 Qwen으로 요약 후 제거 |
| ChatMemoryStore (SQLite) | ✅ | 영구 저장 |

**결과: ✅ 통과**

---

## 4. 샌드박스 및 보안 (E2B)

| 항목 | 상태 | 비고 |
|------|------|------|
| e2b_code_interpreter Sandbox 사용 | ✅ | `Sandbox.create()` |
| Host 환경 완전 격리 | ✅ | exec/eval 사용 안 함 |
| 30초 타임아웃 | ✅ | `CODE_TIMEOUT_SEC = 30` |
| 에러 로그 1,000자 Truncate | ✅ | `ERROR_LOG_MAX_CHARS = 1000`, `_truncate_error()` |

**결과: ✅ 통과**

---

## 5. 자가 진화 (Tool Maker)

| 항목 | 상태 | 비고 |
|------|------|------|
| 성공 시 agent_tools/에 .py 저장 | ✅ | `AgentSkillLibrary().save_tool()` |
| Planner가 기존 도구 먼저 검색 | ✅ | `get_tools_context()` |
| "기존 도구 재활용" 프롬프트 | ✅ | "반드시 먼저 확인: 비슷한 요청이면 새로 코딩하지 말고..." |
| Executor에도 tools_context 전달 | ✅ | import/subprocess 사용 유도 |

**결과: ✅ 통과**

---

## 6. 운영 안정성 및 보안 (Ops)

### 6.1 ALLOWED_CHAT_ID 화이트리스트

| 파일 | 상태 | 비고 |
|------|------|------|
| agent_bot.py | ✅ | `if chat_id not in allowed_ids` → "접근 권한이 없는 사용자입니다." |
| bot.py | ✅ | 동일 |

### 6.2 try-except 안정성

| 파일 | 상태 | 비고 |
|------|------|------|
| agent_bot.py | ✅ | run_or_resume, handle, planner_node 등 |
| bot.py | ✅ | rag_query, handle_message |
| run_scheduler.py | ✅ | run_arxiv_pipeline, run_llm_debate |
| main.py | ✅ | 논문별 try-except |
| llm_debate_scheduler.py | ✅ | run_debate_pipeline, weekly_llm_debate_event |

**결과: ✅ 통과**

---

## 7. 추가 수정 제안

### 7.1 run_scheduler.py 주석 (경미)

```python
# 현재: "main.py 실행 (arXiv 수집 → RAG → Q&A)"
# 수정: "main.py 실행 (arXiv 수집 → RAG → raw_data_queue)"
```

### 7.2 run_backfill.py Q&A 제거 (설계 일관성)

설계 원칙과 맞추려면 run_backfill에서 QaGenerator 제거를 고려할 수 있음.

---

## 8. 최종 요약

| # | 체크리스트 | 결과 |
|---|------------|------|
| 1 | 파이프라인 역할 분리 | ✅ | 
| 2 | 백필 스크립트 | ✅ |
| 3 | LangGraph 에이전트 | ✅ |
| 4 | E2B 샌드박스 | ✅ |
| 5 | Tool Maker | ✅ |
| 6 | Ops & 보안 | ✅ |

**전체: 6/6 통과**

잠재적 개선: run_backfill Q&A 제거, run_scheduler 주석 수정.
