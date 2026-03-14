# Agent Bot 코드 리뷰 보고서 (시니어 AI 아키텍트 관점)

## [핵심 설계 체크리스트 7가지] 점검 결과

---

### 1. Multi-Agent 역할 분담 ✅ 통과

| 항목 | 상태 | 근거 |
|------|------|------|
| Planner → Qwen 2.5 7B (ChatOllama) | ✅ | `get_planner_llm()` → `ChatOllama(model=OLLAMA_MODEL)` (OLLAMA_MODEL="qwen2.5:7b") |
| Executor → Gemini 2.5 Flash | ✅ | `get_executor_llm()` → `ChatGoogleGenerativeAI(model=GEMINI_MODEL)` |
| Monitor → Gemini 2.5 Flash | ✅ | `get_monitor_llm()` → `ChatGoogleGenerativeAI(model=GEMINI_MODEL)` |

---

### 2. LangGraph 워크플로우 & HITL ✅ 통과

| 항목 | 상태 | 근거 |
|------|------|------|
| Planner → Interrupt → Executor → Monitor 루프 | ✅ | `workflow.add_conditional_edges`로 approved 시 executor, monitor 후 route_after_monitor로 재시도/종료 분기 |
| 승인 시 State 재개 (Resume) | ✅ | `_pending_approvals`에 (thread_id, config) 저장, `Command(resume=user_text)`로 재개 |
| 거절 시 종료 | ✅ | `approval_status == "rejected"` 시 `__end__`로 분기 |

**⚠️ 보완 필요**: Resume 시 `add_turn`에 `user_text`("승인"/"거절") 대신 **원본 `user_request`**를 사용해야 대화 맥락이 올바르게 유지됨.

---

### 3. 샌드박스 실행 (E2B) ✅ 통과

| 항목 | 상태 | 근거 |
|------|------|------|
| E2B Sandbox 사용 | ✅ | `with Sandbox.create() as sandbox:` + `sandbox.run_code(code, timeout=30)` |
| 30초 타임아웃 | ✅ | `CODE_TIMEOUT_SEC = 30` |
| 에러 로그 1,000자 Truncate | ✅ | `ERROR_LOG_MAX_CHARS = 1000`, `err_msg[-ERROR_LOG_MAX_CHARS:]` |

---

### 4. 자가 진화 (Skill Library) ✅ 통과

| 항목 | 상태 | 근거 |
|------|------|------|
| 성공 시 agent_tools/ 저장 | ✅ | `run_or_resume` 내 `AgentSkillLibrary().save_tool(code, request)` |
| Planner가 기존 도구 참고 | ✅ | `skill_lib.get_tools_context()` → 프롬프트에 `[기존 도구 라이브러리]` 포함 |

---

### 5. 상태 영구 보존 (Checkpointer) ✅ 통과

| 항목 | 상태 | 근거 |
|------|------|------|
| SqliteSaver 적용 | ✅ | `build_graph(checkpointer=SqliteSaver(conn))` |
| CHAT_ID → thread_id | ✅ | `thread_id = f"tg_{chat_id}"` |
| 재시작 후 승인 대기 복구 | ✅ | `main()`에서 `allowed_ids` 순회하며 `graph.get_state`로 `_pending_approvals` 복구 |

---

### 6. 스마트 메모리 & RAG ⚠️ 보완 필요

| 항목 | 상태 | 근거 |
|------|------|------|
| ChromaDB RAG | ✅ | `ChromaRAGTool` → `rag.search()` |
| 최근 5턴 원본 + 과거 요약 | ⚠️ | **버그**: `deque(maxlen=MEMORY_K)`로 인해 `len`이 5를 초과할 수 없어 `maybe_compress`의 `popleft`가 절대 실행되지 않음. 과거 요약 로직이 동작하지 않음. |
| Qwen 요약 | ✅ | `_summarize_old()`에서 `ChatOllama` 사용 |

**수정 방향**: `recent_messages`의 `maxlen`을 15~20으로 확대하여, 5턴 초과 시 과거 메시지를 요약·제거하도록 수정.

---

### 7. 보안 ✅ 통과

| 항목 | 상태 | 근거 |
|------|------|------|
| ALLOWED_CHAT_ID 차단 | ✅ | `handle()` 최상단에서 `chat_id not in allowed_ids` 시 즉시 `return` |
| .env 로드 | ✅ | `load_dotenv()` 호출 |

**권장**: `main()`에서 `E2B_API_KEY` 미설정 시 경고 출력 추가 (Executor 실행 시점에만 에러가 나므로).

---

## 수정이 필요한 항목 요약 (적용 완료)

1. **SessionMemory.maybe_compress**: `maxlen`을 `MEMORY_BUFFER(15)`로 확대, `to_summarize`를 `[:to_remove]`로 수정 → ✅ 적용
2. **run_or_resume add_turn**: Resume 시 `values["user_request"]` 사용 → ✅ 적용
3. **main()**: E2B_API_KEY 미설정 시 경고 출력 → ✅ 적용
