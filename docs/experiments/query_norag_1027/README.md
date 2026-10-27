# 검색어에서 질문에 없는 RAG 빼기 (사전 등록, 2026-10-27)

> 측정 **전에** 쓴다. 출발점: user_suite_1027 검색 놓침 진단 — 검색어 추출 프롬프트가 "keywords for academic **RAG** retrieval"이라 질문에 RAG 가 없어도 `in rag retrieval` · `for rag retrieval` 이 붙었다. U2-3(프롬프트 압축) · U2-5(질문 재작성) · U5-2(임베딩 양자화)에서 정답이 최종 50위 밖 · 10위였고, 질문 그대로의 짧은 검색어면 1–4위. 기존 `RAG_QUERY_CLEAN`(10-21, 유의 X)은 academic · research 만 빼고 rag 는 남긴다. 선행 `query_extract_1021`(프롬프트 예시가 새어 들어가 기각)과 달리 예시는 넣지 않는다.

## 1. 바꾸는 것 — `RAG_QUERY_NORAG=1` (기본 0)

`core/graph/agent_nodes.py` `_extract_english_rag_query`, 테스트 `tests/unit/test_query_norag.py`.

- 프롬프트 문구 "for academic RAG retrieval" → "for an academic paper search" (나머지 그대로).
- 질문에 RAG · retrieval-augmented · 검색 증강 · 리트리벌이 없으면 나온 검색어에서 `(in|for|of) rag (retrieval|system|pipeline)` · `retrieval-augmented generation` 을 지운다. 지우고 2 단어 미만이면 원래 검색어.
- `RAG_QUERY_CLEAN` 과는 따로(둘 다 운영 0).

## 2. 방법 (맥미니, 검색만 — `--answer` 없음, 운영 설정 그대로)

대조 `rn0_*` · 처리 `rn1_*`, 세트마다 번갈아: 정답 있는 세트 162 · real40 · real2 + held-out 30(H) · 직무 34(D) · 사용자 34(U, user_suite_1027).

- **관련성 판정(주 지표):** H · D · U 의 두 조건 컨텍스트 논문을 합쳐, 이미 판정한 쌍(corpus_seed `.cron/cs/judged_*`)은 그 판정을 쓰고 새 쌍만 섞어 조건을 모른 채 0 · 1 · 2 판정(2 = 질문을 직접 다룸).

## 3. 판정 (측정 전 고정)

| 지표 | 기준 |
|---|---|
| **주:** H + D + U (98) — 질문별 컨텍스트 '2' 논문 수 | 처리 > 대조, 부호 검정(동점 제외) 양측 p < 0.05 |
| 보호: 정답 있는 세트 검색 ok (162 + real40 + real2) | 처리가 대조보다 3 이상 낮지 않음 |
| 보호: 검색어에 한글이 남은 문항 | 처리 ≤ 대조 |
| 보고: 검색어에 rag 가 든 문항(질문에 RAG 없음) 수 · 검색어가 바뀐 문항 수 · 진단 4 문항(U1-4 · U2-3 · U2-5 · U5-2)의 정답 논문이 컨텍스트에 들었는지 | |

보호 미달이면 주 지표 판정 없이 기각. 채택이면 사용자 승인 후 운영 `.env` `RAG_QUERY_NORAG=1` + 봇 재시작.

예상: 질문에 RAG 가 없는 문항은 전체의 절반 안팎, 그중 검색어에 rag 가 붙은 문항이 20~40%. 프롬프트 문구만 바뀌는 RAG 질문은 검색어가 조금씩 흔들릴 수 있다(±).

## 4. 기록

| 날짜 | 내용 |
|---|---|
| 2026-10-27 | 사전 등록 · 구현(테스트 통과). |
