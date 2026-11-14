# 운영 설정 목록 (맥미니 `.env`)

> 기준일 2026-11-07. 표의 값은 이날 `.env` 와 글자까지 대조했고, 날짜는 모두 2026년이다. `.env` 는 git 에 없다. **`.env` 를 바꾸면 이 문서도 같은 커밋에서 고친다.** 저장소가 공개이므로 비밀 값 · 개인 값은 적지 않는다.

**`.env` 를 잃으면:** `RAG_*` 는 코드 기본값으로 돌아간다. 기본값은 대부분 꺼짐(`0`)이고 나머지는 옛 값(초록 800자, 결론 v1, 답 모델은 기본 모델)이라 오류 없이 품질만 떨어진다. 복원은 이 표의 값을 다시 넣고, §3 의 키는 각 서비스에서 다시 받는다. `.env` 백업은 내장 디스크 `~/backups/mini/` 에 있다: 바꾸기 전 복사본은 `env_history/`(11-11 에 `.cron/env.bak*` 24개를 옮김 — 암호화 안 된 T7 에 비밀 값 복사본이 644 로 쌓여 있었다), 전체 백업은 [`ops/backup.sh`](backup.sh) 가 만드는 `YYYY-MM-DD/env.backup`. **앞으로 `.env` 를 바꾸기 전 복사본은 `~/backups/mini/env_history/` 에 600 으로 둔다(T7 · `.cron` 에 두지 않는다).**

## 1. RAG 기능 (32개, 켠 순서)

켠 때는 라운드 문서와 `.env` 복사본(`env.bak*`, 지금은 `~/backups/mini/env_history/`) 시각으로 맞췄다. 날짜만 적은 앞쪽 4개(10-11 · 10-12)는 백업이 없던 때라 라운드 문서 기준이다. 측정 수치는 그 라운드의 dev · held-out 결과이고, 지금 다시 잰 값이 아니다.

| 설정 | 값 | 켠 때 | 하는 일 | 근거 라운드와 측정 |
|---|---|---|---|---|
| `RAG_ANSWER_MODEL` | `"yunsur_v13"` | 10-11 | 답 · 거르기 · 판정 · 결론 다시 쓰기에 쓰는 모델 | [`yunsur_v13`](../docs/experiments/yunsur_v13/README.md): 거짓 부정 41→0 (p 9e-13) |
| `RAG_CONTEXT_ABSTRACT` | `1` | 10-12 | 문서 블록마다 논문 초록을 붙인다 | [`abstract_context_1011`](../docs/experiments/abstract_context_1011/README.md): ok 127:112 (p .006), 날조 22:40 (p .011) |
| `RAG_PRESENCE_JUDGE` | `1` | 10-12 | 답 전에 정답 유무를 판정하고, '없음'이면 힌트를 준다 | [`presence_integration_1012`](../docs/experiments/presence_integration_1012/README.md): 정답 없음 일관 고지 0→12/21 (p .0005) |
| `RAG_HANZI_RETRY` | `1` | 10-12 | 답에 한자가 섞이면 한 번 다시 생성한다 | [`hanzi_retry_1012`](../docs/experiments/hanzi_retry_1012/README.md): 생성당 22.2% (기준 ≤ 25%) |
| `RAG_PRESENCE_GATE` | `1` | 10-14 23:14 | 수치 · 비교 · 목록 질문은 판정을 건너뛴다 | [`presence_gate_1014`](../docs/experiments/presence_gate_1014/README.md): '있는데 없다' 8→0 (p .0078) |
| `RAG_COMPARE_SPLIT` | `1` | 10-15 08:16 | 비교 질문의 두 대상을 따로 검색한다 | [`compare_split_1015`](../docs/experiments/compare_split_1015/README.md): 두 편 모두 검색 5→19/22 (p .0001), 비교 질문 +37초 |
| `RAG_EMB_CACHE` | `1` | 10-15 22:05 | 임베딩 로컬 캐시. 매일 수집 뒤 다시 만든다 | [`emb_cache_1015`](../docs/experiments/emb_cache_1015/README.md): 162문항 중앙 46.3→37.0초, 결과 동일 |
| `RAG_ABSTRACT_CHARS` | `2000` | 10-16 15:28 | 초록 글자 상한 (코드 기본 800) | [`abstract_full_1016`](../docs/experiments/abstract_full_1016/README.md): 수치 정답 17→25/27 (p .0078) |
| `RAG_LIST_MODE` | `1` | 10-16 18:30 | 목록 질문 전용 답 형식 | [`list_mode_1016`](../docs/experiments/list_mode_1016/README.md): 정답 인용 24→31 (p .0156) |
| `RAG_LIST_SLOTS` | `1` | 10-16 19:31 | 목록 답에 번호 칸을 준다 | [`list_slots_1016`](../docs/experiments/list_slots_1016/README.md): 정답 인용 31→59 (p .0215), +18초 |
| `RAG_HELPER_MODEL` | `"yunsur_v13"` | 10-17 06:50 | 라우터 분류 · 검색어 재작성 모델. 답 모델과 같게 두어 모델 교체를 없앤다 | [`helper_model_1016`](../docs/experiments/helper_model_1016/README.md): 응답 중앙 70.0→56.1초 |
| `RAG_JUDGE_SHARED_PREFIX` | `1` | 10-17 10:14 | 판정이 답 프롬프트 앞부분의 캐시를 함께 쓴다 | [`judge_cache_1017`](../docs/experiments/judge_cache_1017/README.md): 응답 중앙 59.2→43.4초 |
| `RAG_HISTORY_GATE` | `1` | 10-20 02:03 | 이어지는 질문에만 대화 기록을 넣는다 | [`history_gate_1019`](../docs/experiments/history_gate_1019/README.md): 오염된 답 4→0 (p .125, 유의 아님). +7초를 알고 사용자가 결정 |
| `RAG_EXTERNAL_SEARCH` | `1` | 10-20 22:48 | 판정 '없음' · 목록 질문에 OpenAlex 외부 검색을 덧붙인다 | [`external_search_v3_1020`](../docs/experiments/external_search_v3_1020/README.md): '2' 1편 이상 12/15, 무관 13/50 |
| `RAG_MERGE_SAME_PAPER` | `1` | 10-21 12:27 | 같은 논문을 인용한 항목을 합친다 | [`merge_same_paper_1021`](../docs/experiments/merge_same_paper_1021/README.md): 같은 논문 두 항목 13→0 (real40) |
| `RAG_FOLLOWUP_REUSE` | `1` | 10-21 14:27 | 공백 뺀 25자 이하 이어지는 질문에 직전 컨텍스트를 다시 쓴다 | [`followup_reuse_1021`](../docs/experiments/followup_reuse_1021/README.md): 주 지표 6/7 (p .031). 25자 규칙은 오발동 때문에 사후 추가 |
| `RAG_CONCLUSION_REWRITE` | `1` | 10-21 17:43 | 결론을 따로 다시 쓴다 | [`conclusion_rewrite_1021`](../docs/experiments/conclusion_rewrite_1021/README.md): 주 · 보호 통과, 답마다 약 +18초 |
| `RAG_CONCLUSION_PROMPT` | `v2` | 10-21 22:53 | 결론 입력에서 본론을 빼고 초록의 결과 · 대상 문장을 규칙으로 뽑는다 (코드 기본 v1) | [`conclusion_rewrite_1021`](../docs/experiments/conclusion_rewrite_1021/README.md) §8: 사전 기준 통과 |
| `RAG_ABSTRACT_TAIL_CHECK` | `1` | 10-22 07:40 | 잘린 초록 청크에도 초록을 붙인다 (버그 수정) | [`abstract_tail_1021`](../docs/experiments/abstract_tail_1021/README.md): 효과 지표 변화 없음 (4:4) |
| `RAG_CITE_CLEANUP` | `1` | 10-22 10:57 | 인용 중복과 문서 번호 노출을 정리한다 | [`cite_cleanup_1022`](../docs/experiments/cite_cleanup_1022/README.md): 인용 중복 답 11→0 (real40) |
| `RAG_RELEVANCE_FILTER` | `1` | 10-22 14:32 | 관련 없는 문서를 답 전에 뺀다. 제목에 고유 이름이 든 문서는 지킨다 | [`relevance_filter_1022`](../docs/experiments/relevance_filter_1022/README.md): 정답 아닌 인용 98→77 (19:3, p .0009) |
| `RAG_PAPER_BLOCKS` | `1` | 10-22 22:38 | 논문당 한 블록, 라우터 5편 | [`paper_blocks_1022`](../docs/experiments/paper_blocks_1022/README.md): 효과 없음 (7:6), 중복 정리용 |
| `RAG_COND_CHECK` | `1` | 10-26 07:37 | 질문의 기간 조건으로 거르고 편수를 알린다. 기간에 맞는 문서가 없으면 기간 밖 문서로 답하되 서론 첫 문장을 코드가 고정하고 서론 · 결론의 요청 연도 단정 문장을 뺀다, DB 밖(OpenAlex) 목록도 요청 기간만(코드 변경 11-13, `.env` 그대로 — [`answer_issues_1113`](../docs/experiments/answer_issues_1113/README.md)) | [`qcond_rule_1025`](../docs/experiments/qcond_rule_1025/README.md): 조건 문제 있는 질문 18→2/38 (16:0, p < .0001) |
| `RAG_LIST_FINDINGS` | `1` | 10-26 10:55 | 목록 항목에 결과 문장을 넣는다 | [`list_findings_v2_1026`](../docs/experiments/list_findings_v2_1026/README.md): 배경만 쓴 항목 16→1 |
| `RAG_LIST_ABS_CHARS` | `400` | 10-26 10:55 | 목록 항목의 초록 상한 (코드 기본 500) | [`list_findings_v2_1026`](../docs/experiments/list_findings_v2_1026/README.md) |
| `RAG_BODY_NUM_CHECK` | `1` | 10-26 10:55 | 본문 숫자를 출처 블록과 대조한다 | [`list_findings_v2_1026`](../docs/experiments/list_findings_v2_1026/README.md) |
| `RAG_FILTER_BEFORE_CUT` | `1` | 10-28 20:10 | 15→5 자르기 전에 거른다 | [`filter_before_cut_1028`](../docs/experiments/filter_before_cut_1028/README.md): '2' 199→218 (13:2, p .0074) |
| `RAG_FILTER_NONE_KEEP` | `1` | 11-14 09:33 | 거르기가 '관련: 없음' 이면 다 남기지 않고 검색 1 위(+ 이름 보호 문서)만 | [`filter_none_1114`](../docs/experiments/filter_none_1114/README.md): held-out '없음' 10 문항, 빠지는 문서 29/32 무관 · 관련 다 잃음 1 · 정답 잃음 0 |
| `RAG_ROUTER_RESEARCH` | `1` | 10-29 07:00 | 라우터 경로도 15편을 다시 검색한다 | [`router_research_1028`](../docs/experiments/router_research_1028/README.md): '2' 219→247 (27:2, p 1.6e-6), +7.7초 |
| `RAG_NODOC_KEEP_CONCLUSION` | `1` | 10-29 08:22 | 판정 '없음'이면 결론 다시 쓰기를 건너뛴다 | [`nodoc_conclusion_1029`](../docs/experiments/nodoc_conclusion_1029/README.md): 모순 답 6→0 (p .031), −20초 |
| `RAG_NAME_LOOKUP` | `1` | 11-01 08:14 | 질문 속 고유 이름으로 논문을 찾아 앞에 둔다 | [`name_lookup_1101`](../docs/experiments/name_lookup_1101/README.md): held-out 이름 정답 상위 5 안 2/4→4/4 |
| `RAG_FIX_PDF_DECIMAL` | `1` | 11-07 09:18 | PDF 본문의 깨진 소수점 `87 _._ 5%` 를 컨텍스트에서 `87.5%` 로 고친다. 재색인 없음 | [`pdf_decimal_1107`](../docs/experiments/pdf_decimal_1107/README.md): 깨진 소수점 15곳→0곳, 보호 통과. 조각 오류는 양쪽 0 이라 효과는 재현 안 됨. 버그 수정 |
| `RAG_ANSWER_REPEAT_PENALTY` | `1.0` | 11-13 17:29 | 답 호출의 반복 억제(코드 기본 1.18). 다른 호출은 1.18 그대로. 되돌리기: 이 줄을 지우고 봇 재시작 | [`penalty_1113`](../docs/experiments/penalty_1113/README.md): 깨진 음차 용어 7/40→0/40 (p .016), 120 held-out 깨진 답 4→2 · 보호 P1–P6 통과(P7 시간은 35b 끼어듦으로 무효, 참고 +0.7초). 11-20 까지 운영 로그로 시간 · 깨짐 · 되풀이 확인 |

## 2. 그 밖 설정 (값 공개 가능)

| 묶음 | 설정 | 값 | 하는 일 |
|---|---|---|---|
| 모델 | `LOCAL_LLM_MODEL` | `"qwen3.5:9b"` | 잡담 · 계획 · 코딩 폴백 모델. 코딩 폴백과 묶여 있어 바꾸지 않는다 |
| 모델 | `GROQ_CODING_MODEL` | `"openai/gpt-oss-120b"` | 코딩 모델 |
| 모델 | `OLLAMA_KEEP_ALIVE` | `"30m"` | 모델을 메모리에 두는 시간 (10-18 01:54 설정) |
| 경로 | `CHROMA_DB_PATH` | `"/Volumes/T7 Shield/mini-chroma-rebuild2"` | 논문 DB 폴더 (T7) |
| 경로 | `CHECKPOINT_DB_PATH` | `"/Users/yunsupark/Library/Application Support/mini-agent/agent_checkpoints.db"` | 대화 체크포인트 DB (내장 디스크) |
| 수집 | `ARXIV_PIPELINE_SCHEDULE_AT` | `01:00` | arXiv 수집 시각 |
| 수집 | `ARXIV_INGEST_BATCH_SIZE` | `50` | 한 번에 읽는 메타 수 |
| 수집 | `ARXIV_INGEST_MAX_SCAN` | `400` | 최대 스캔 메타 수 |
| 수집 | `ARXIV_INGEST_TARGET_NEW` | `10` | 하루 신규 목표 편수 |
| 수집 | `ARXIV_HF_DAILY_TOP` | `20` | HF Daily 상위 편수 (`hf_coverage_1012`) |
| 스케줄 | `SCHEDULER_POLL_SEC` | `30` | 스케줄러 확인 주기(초) |
| 스케줄 | `MORNING_SCRAPER_SCHEDULE_AT` | `07:30` | 아침 캐시 시각 (`PHASE35_SCHEDULE_ENABLED` 에 묶여 있어 안 돎) |
| 스케줄 | `PHASE35_SCHEDULE_ENABLED` | `0` | YES 심사 끔 (마지막 실행 05-28) |
| 스케줄 | `PHASE35_CURATOR_SCHEDULE_AT` | `08:00` | YES 심사 시각 (꺼져 있어 안 돎) |
| 스케줄 | `LLM_DEBATE_SCHEDULE_ENABLED` | `0` | 논문 토론 배치 끔 |
| 스케줄 | `AGENT_BOT_CRON_WORKER` | `0` | 봇 프로세스 안 cron worker 끔 |
| 회의 배치 | `BOARDROOM_SCHEDULE_ENABLED` | `0` | 회의 배치 스케줄 끔 |
| 회의 배치 | `BOARDROOM_SCHEDULE_DAILY` | `1` | 주말 포함 매일 실행 (`0` 이면 월~금. 스케줄이 꺼져 있어 안 돎) |
| 회의 배치 | `BOARDROOM_MINUTES_OLLAMA_MAX_CHARS` | `8000` | 회의록 입력 상한 |
| 회의 배치 | `BOARDROOM_MINUTES_OLLAMA_PER_MSG_CHARS` | `3500` | 발언당 입력 상한 |
| 회의 배치 | `BOARDROOM_TURN_CONTEXT_CHARS` | `6000` | 차례당 맥락 상한 |
| 회의 배치 | `BOARDROOM_OLLAMA_TIMEOUT_SEC` | `1800` | 호출 제한 시간 |
| 회의 배치 | `BOARDROOM_CTO_NUM_PREDICT` | `1200` | CTO 발언 토큰 상한 |
| 회의 배치 | `BOARDROOM_MINUTES_REPEAT_LAST_N` | `2048` | 회의록 반복 억제 범위 |
| 회의 배치 | `BOARDROOM_MINUTES_REPEAT_PENALTY` | `1.25` | 회의록 반복 억제 강도 |
| 회의 배치 | `BOARDROOM_MINUTES_TEMPERATURE` | `0.5` | 회의록 온도 |

## 3. 값을 적지 않는 키

이름만 적는다. 값은 `.env` 에만 있다.

- **API 키 · 토큰:** `GEMINI_API_KEY` · `GEMINI_API_KEY_2` ~ `GEMINI_API_KEY_20`, `TELEGRAM_TOKEN`, `E2B_API_KEY`, `WEATHER_API_KEY`, `TAVILY_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY`, `NOTION_TOKEN`, `OPENALEX_API_KEY`
- **개인 · 기기 값:** `ALLOWED_CHAT_ID`, `TUYA_LOCAL_KEY`, `TUYA_PLUG_IP`, `TUYA_DEVICE_ID`, `TUYA_PROTOCOL_VERSION`, `NOTION_SUNDAY_DB_ID`, `NOTION_LYRICS_DB_ID`, `CHURCH_LYRICS_SKIP`
- **주소:** `OLLAMA_HOST`, `CHROMA_SERVER_URL`

## 4. `.env` 밖 설정

- **launchd · 실행기:** [`ops/launchd/`](launchd/README.md). 지금 등록 상태와 내장 디스크 자료는 [`newmac_1105`](../docs/experiments/newmac_1105/README.md) §1 에 있다.
- **Ollama 모델:** [`ops/modelfiles/`](modelfiles/) 와 `newmac_1105` §1.
- **Ollama 컨텍스트:** 설정이 아니라 기본값 4096 이다(11-03 확인, `.env` · 코드 · launchctl 어디에도 없음). 새 맥미니에서는 기본값이 달라지므로 `OLLAMA_CONTEXT_LENGTH` 를 명시한다.
- **주석으로 남긴 옛 값:** `.env` 의 주석 줄에 옛 `RAG_ANSWER_MODEL` 이 있다.
- **접어 둔 플래그:** 코드에는 있고 `.env` 에 없어 꺼진 것들(`RAG_TOPIC_SPLIT` 등)은 `newmac_1105` §7 의 접은 라운드에서 본다.
