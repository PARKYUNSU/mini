# '없음' 판정이면 외부 검색어를 분야 용어로 (사전 등록, 2026-10-29)

> 측정 **전에** 쓴다. 출발점: no_doc_format_1029 · job 134/135 — "두 대형 DB 간 유사 · 중복 내용 찾기" 질문에서 DB 검색어가 질문 직역(`rag search across multiple databases duplicate content detection …`)이라 OpenAlex 외부 검색도 금융 RAG · 바이오 그래프 RAG 같은 무관 논문을 가져왔다. 이 분야 표준 용어(entity resolution · near-duplicate detection · similarity join)를 쓰면 찾을 수 있다. 전체 검색어 바꾸기는 이미 기각(DB 검색어 v2 · HyPE 0) — 이번엔 판정 `없음` 일 때 외부 검색에만.

## 1. 바꾸는 것 — `RAG_EXTERNAL_TERM_QUERY=1` (기본 0)

`core/rag/external_search.py` `term_query(question, model)`: LLM 한 번(temperature 0, 비-thinking, 32 토큰)으로 "질문이 찾는 연구 분야의 표준 영어 학술 용어 검색어 한 줄(예로 든 기술은 핵심이 아니면 뺌)". `agent_nodes.py` direct_answer: `_pick == "없음"` 이면 그 검색어로 `ExternalSearch` (실패 · 빈 줄이면 원래 `rag_query`). DB 검색 · 답변 · 목록 · 단일 논문 외부 검색은 그대로.

## 2. 방법 (맥미니 오프라인 — 외부 검색만, 답변 생성 없음)

질문: nodoc_conclusion_1029 의 16 개(판정 `없음` 이던 문항 + job 134). 두 조건의 검색어 · 컨텍스트 논문(제외 목록)은 nk1 결과(`e2e_ko_1008/results/nk1.jsonl`) 그대로. `measure.py`: 대조 = `search_openalex(rag_query)`, 처리 = `search_openalex(term_query(질문))` — 같은 시각에 번갈아 부른다(OpenAlex 색인 변화 통제). 결과 `results.jsonl`.

관련성 판정: 두 조건 외부 논문(제목 + 초록 600 자)을 질문별로 합쳐 섞고 조건을 모른 채 0 · 1 · 2(2 = 질문을 직접 다룸). `pool.json` · `judged.txt` · `score.py`.

## 3. 판정 (측정 전 고정)

| 지표 | 기준 |
|---|---|
| **주:** 질문별 외부 논문 중 '2' 수 | 처리 > 대조, 부호 검정(동점 제외) 양측 p < 0.05 |
| 보호: '0' 논문 수 합 | 처리가 대조의 1.5 배 이하 |
| 보호: `term_query` 호출 시간 중앙값 | ≤ 8 s (답변 앞에 더해지는 시간) |
| 보고: 질문별 외부 논문 수 · 0 편 문항 수 · 처리 검색어 목록 | |

보호 미달이면 주 지표 판정 없이 기각. 채택이면 사용자 승인 후 운영 `.env` 반영 + 봇 재시작. 표본 16 이라 6 : 0 이상이어야 유의.

## 4. 기록

| 날짜 | 내용 |
|---|---|
| 2026-10-29 | 사전 등록 · 구현(단위 709 통과). |
| 2026-10-29 | 측정 · 판정 · **기각**(주 지표 미달). 운영 반영 없음 — 플래그 기본 0 유지. |

## 5. 결과 (2026-10-29) — 기각

판정 풀 `pool.py`(90 쌍 눈가림 판정 `judged.txt` — 판정자 1 명(Claude)), 채점 `score.py`.

| 지표 | 대조 et0 | 처리 et1 | 판정 |
|---|---|---|---|
| **주:** 질문별 외부 '2' 수 | 합 20 | 합 24 | 늘어남 3 : 줄어듦 2, **p 1.0** — 미달 |
| 보호: '0' 합 | 19 | 7 | 통과 |
| 보호: `term_query` 시간 중앙 | | 1.5 s | 통과 |
| 보고: '1' 합 | 17 | 16 | |
| 보고: 외부 편수(4 편인 문항 · 0 편) | 13 · 1 | 10 · 2 | |

늘어난 문항 대부분이 U_U2-5 하나('2' 0 → 4: 대조가 의료 RAG 서베이를 끌어옴). 출발점 R_134 는 '0' 1 편 → '1' 2 편 — 처리 검색어가 `Cross-database similarity search with large document corpora` 로 **분야 용어(entity resolution · near-duplicate detection)를 만들지 못함**. 16 문항 중 대부분에서 처리 검색어가 질문 직역 수준(예 H_H12 `LLM sparse matrix selection for long tables`).

결론: 운영 모델(9B)이 일상 표현 → 분야 용어 변환을 못 한다 — 프롬프트만으로는 출발점 문제가 안 풀린다. 무관('0') 외부 논문은 19 → 7 로 줄었지만 '2' 가 늘지 않아 채택 기준 미달. 남은 길: 코퍼스 보강(DB 공백 분야), 또는 더 큰 모델로 검색어 생성(Groq 는 운영 코딩과 할당량 공유라 신중).
