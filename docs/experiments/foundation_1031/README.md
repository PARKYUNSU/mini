# 0단계 — 측정 기반 정비 (2026-10-31)

> 방향 초안(10-31) 0단계. 출발점: 실사용 답이 틀려도 어느 단계에서 틀렸는지 못 봤고(answer_review_1030 §2-3), 어느 단계가 느린지 몰랐으며, 방향이 맞는 변경도 문항이 적어 유의가 안 나왔다(protocol.md §2.5). 전체 품질은 10-24 이후 재지 않았다.
> 운영 동작을 바꾸는 변경은 없다 — 기록 추가 · 꺼진 코드 삭제 · 평가 도구뿐. 기록은 봇 재시작 뒤부터 쌓인다(사용자 승인).

## 1. 단계별 기록 — `core/graph/rag_trace.py`

워커(`agent_worker_runner.execute_graph_turn`)가 요청마다 `start` → 라우터 · 답변 노드가 `mark` → 워커가 `finish` 로 `.bridge/rag_trace.jsonl`(git 밖)에 한 줄을 쓴다. `RAG_TRACE=0` 이면 끈다(기본 켬). 기록이 실패해도 답은 나간다.

| 단계 | 담는 것 |
|---|---|
| `router` | 1단계 하드룰 또는 3단계 LLM 분류 결과 · 라우터 검색어 · 라우터 컨텍스트 논문 |
| `query` | 답변 노드 영어 검색어 · 대화 기록 사용 여부 |
| `search` | 컨텍스트 출처(`search` · `router` · `list` · `followup_reuse` · `list_papers`) · 논문 ID |
| `select` | 자르기 앞 거르기 결과 · 상위 5(목록 10) 뒤 논문 |
| `filter` | 자른 뒤 거르기 · 기간 거르기 · 번호 붙은 논문 |
| `judge` | 질문 유형 게이트 · 정답 유무 판정 |
| `answer` | 답변 LLM 원문(4,000자) |
| `post` | 인용 교정 요약 |
| `rewrite` | 결론 다시 쓰기 결과 · **다시 쓰기 전 답**(4,000자) |
| `external` | 외부 검색 편수 · 답변 뒤 대기 |
| `final` | 보낸 답(4,000자) |

각 단계에 직전 단계 뒤 걸린 초(`s`)가 붙고 끝에 `total_s`. 평가(`eval_e2e_ko.py`)도 같은 기록을 켜서 행에 `stages`(단계 · 초)를 남긴다(파일엔 안 씀).

점검(`trace_check`, survey_gate new S01 · S10, 답까지): 두 문항 모두 11단계가 다 찍혔다. 라우터 31.6 · 8.0s(첫 문항은 모델 적재 포함) · 검색어 2.2 · 1.1 · 검색 2.8 · 2.9 · 거르기 14.1 · 15.1 · 판정 17.5 · 17.4 · 답 30.5 · 31.5 · 결론 다시 쓰기 18.0 · 17.9s.

## 2. held-out 세트 — `heldout.tsv` 90문항 + `heldout_followup.tsv` 5쌍

실사용 139 job 의 질문 꼴을 보고 꼴별로 나눠 새로 썼다(DB 는 보지 않음). 기존 2,241 질문과 SequenceMatcher 0.75 이상 겹치는 주제 5개는 바꿨다.

| 꼴 | 수 | 예 |
|---|---|---|
| A 특정 연구 찾기 · 설명 | 24 | "…다룬 논문 있어?" · "…연구 알려줘" (2문항은 DB 밖일 주제 — 단백질 · 자율주행) |
| B 이름으로 묻기 | 14 | "Self-RAG 논문 요약해줘" — **정답 ID 있음**(`heldout_gold.jsonl`) |
| C 목록 · 정리 · 조사 · 추천 | 18 | "…연구들 정리해줘" · "…5개 찾아줘" · "2025년에 나온…" |
| D 비교 | 8 | "A랑 B는 어떻게 달라?" |
| E 수치 | 8 | "몇 배 빨라져?" |
| F 전제 · 복합 전문가형 | 9 | job 137–139 꼴 — 전제 + 여러 물음 |
| G 분석 · 생성 | 5 | "빈틈 3가지 제안해줘" |
| H 오타 · 막연 | 4 | "retreival augmented generaton…" |
| I 이어지는 질문 5쌍 | 10 | `--keep-session` 으로 잰다 |

규칙(protocol.md §2.5): 라운드 **판정**만 여기서 한다. 실패 사례를 보고 고치지 않는다 — 그렇게 쓴 문항은 dev 로 옮기고 새로 채운다.

## 3 · 4. 사전 등록 규칙 · 지표 — protocol.md §2.5

필요 문항 수(부호 검정 2:1 효과면 동점 뺀 37) · 검색 변경은 검색만 측정 · held-out 판정 · 인용 편수가 바뀌면 '2' 비율 보호 · 크기 검정은 사전 등록 때만 · 판정자 점검 · 단계별 시간 · 측정 한 번에 하나(`eval_e2e_ko.py` 가 같은 label 이 돌면 종료 코드 2로 멈춤 — 점검함).

## 5. 판정자 점검 — `judge_check/`

survey_gate_1030 판정 풀 164쌍에서 Claude 라벨별 8('2') · 7('1') · 5('0')쌍을 뽑아 섞었다(`make.py`, 시드 1031 — 무작위면 '2' 가 대부분이라 '0' · '1' 을 못 본다). 사용자가 `pairs.md` 를 라벨 모른 채 판정 → 일치도(정확 일치 · '2' 여부 일치 · 가중 κ)를 여기 적는다. 정답지 `key.json`.

## 6. 주간 점검 — `scripts/weekly_check.sh` → `weekly.md`

real40 고정 40문항(정답 34)을 운영 `.env` 그대로 답까지 재고 `scripts/weekly_report.py` 가 사람 판정 없는 지표 한 줄을 붙인다: 검색 정답 · 답 **본문** 정답 인용(📎 외부 목록 제외) · '없음' 답 · 컨텍스트 밖 인용 · 시간 중앙 · 단계별 중앙 · 오류. 주장 단위 판정(answer_judge_1024 방식)은 월 1회 따로. cron 등록은 사용자 승인 뒤(일요일 04:00 제안 — 매일 01:00 수집 · 캐시 재생성, 06:00 일일 파이프라인과 안 겹침).

## 7. 플래그 정리 — 운영에서 꺼진(기각) 코드 경로 삭제

운영 `.env` 의 RAG_ 플래그 29개(모두 채택)는 그대로 둔다 — **끄는 스위치로 남겨야** 다음 R7(값 못 하는 단계 끄기)에서 하나씩 끄고 잴 수 있다(초안의 "기본값으로"는 철회). 코드가 읽는 RAG_ 플래그 52 → 38.

| 지운 플래그 | 라운드 · 판정 |
|---|---|
| `RAG_SINGLE_HIT_SHORT_QUERY` | single_hit_1009 — 비교용 되살리기 |
| `RAG_QUERY_V2` · `RAG_QUERY_CLEAN` · `RAG_QUERY_NORAG` · `RAG_QUERY_GLOSSARY`(+ `core/rag/query_glossary.py`) | query_extract_1021 · query_clean_1021 · query_norag_1027 · query_glossary_1029 — 기각 |
| `RAG_LIGHT_RERANK_GATED_OFF` | real_eval2_1015 — 채택 안 함(light rerank 는 늘 켬 그대로) |
| `RAG_COMPARE_SPLIT_PARALLEL` | compare_latency_1015 — 채택 안 함 |
| `RAG_ASPECT_SPLIT` | aspect_split_1022 — 기각 |
| `RAG_ANSWER_DETAIL` | answer_detail_1013 — 채택 안 함 |
| `RAG_EXTERNAL_ON_SINGLE` · `RAG_EXTERNAL_TERM_QUERY` | external_single_1023 · external_term_1029 — 기각 |
| `RAG_PRESENCE_PROMPT=v2` | presence_judge_v2_1014 — 채택 안 함 |
| `RAG_SURVEY_GATE` | survey_gate_1030 — 기각 |
| `RAG_CONCLUSION_PROMPT=v3` · `RAG_CONCLUSION_DROP_BUNDLED` | conclusion_v3_1024 · conclusion_drop*_1025 · conclusion_overgen_1025 — 기각 |

- 남긴 것: 검색 내부의 `RAG_HYPE` · `RAG_FUSION_PROTECT` · `CHROMA_CROSS_ENCODER_RERANK` — R1(재순위 교체)이 바로 그 자리를 고치므로 그때 정리한다. 설정값(`RAG_EMB_CACHE_DIR` · `RAG_EXTERNAL_MIN_SIM` · `RAG_OLLAMA_TIMEOUT_SEC` · `RAG_BOT_TOKEN`)은 기능 플래그가 아니다.
- 지운 코드에 기대던 옛 측정 스크립트(`scripts/presence_judge_v2_eval.py` · `external_term_1029/*.py` · `survey_gate_1030/build_set.py`)는 이제 돌지 않는다 — 다시 잴 땐 정리 전 커밋(`0975202`)에서.
- 점검: 단위 테스트 697 통과(지운 기능의 테스트 18개 빠짐). **동작 같음**: survey_gate_1030 37문항을 정리 뒤 검색만 다시 재(`fc_new` · `fc_old`) 같은 DB 의 대조 `sg0_*` 와 컨텍스트 논문(`doc_ids`, 순서 포함)을 비교 — **37 / 37 같음**, 오류 0 (`fc_compare.py`).

## 8. 기록

| 날짜 | 내용 |
|---|---|
| 2026-10-31 | 단계별 기록 · held-out 세트 · protocol §2.5 · 판정자 점검 20쌍 · 주간 점검 스크립트 · 플래그 정리. 정리 전후 검색 37/37 같음. 첫 주간 점검(기준선) 11:12 시작. 판정자 점검은 사용자 판정 대기. |
