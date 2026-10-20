# 외부 검색 v3 — 검색어 일반어 빼기, 새 질문으로 재측정 (사전 등록, 2026-10-20)

> 측정 **전에** 쓴다. 선행: [`external_search_v2_1020/`](../external_search_v2_1020/) — v2 직접 맞는 논문 62%(통과)지만 **무관 32%**(기준 30% 미달). 원인으로 본 것: 운영 검색어 추출이 일반어를 붙인다(N 질문 검색어 단어 빈도 research 49 · academic 42 · paper(s) 24 · keywords 10 …, 예 "… research paper academic search keywords query"). 사용자 요청(10-20): 일반어를 뺀 v3 를 **또 새 질문**으로 잰다.

## 1. 바꾸는 것 — v3 (v2 + 검색어 정리)

OpenAlex 에 보내기 **전에만** 검색어에서 아래 일반어를 뺀다(DB 검색어는 그대로):
`research researches academic paper papers study studies survey surveys keywords keyword summary trend trends overview literature article articles publication publications recent latest methods method approach approaches best practices guidelines`
- 끝에 홀로 남은 `large` 도 뺀다("large language" 가 잘려 생김).
- 빼고 3단어 미만이 되면 원래 검색어를 쓴다.
- 유사도 계산(문턱 0.47)도 정리된 검색어로 한다. 나머지(중복 제거 · 상위 4 · 트리거 · 형식)는 v2 그대로.
- 목록은 N 질문 검색어에서 뽑았다(측정할 M 질문은 보지 않음).

## 2. 측정 (맥미니, OpenAlex 키 사용)

- **새 질문 30개**(`new_questions.tsv` M01–M30, 이 문서와 함께 먼저 작성 — 앞선 H · D · N 과 겹치지 않는 같은 직무 분야).
- 운영 설정으로 검색만(판정 끔) → 운영 판정 함수 · 목록 모드로 트리거 → **v2 · v3** 외부 결과.
- 관련성 판정: v2 · v3 결과를 합쳐 섞은 풀을 Claude 가 어느 쪽인지 모른 채 0 · 1 · 2.
- 추가 지연: 트리거되는 질문 5개를 v3 를 켜고 답변까지 돌려 "답변 뒤 대기" 확인.

## 3. 판정 (측정 전 고정) — v3 에 대해

| 지표 | 기준 |
|---|---|
| **주 1:** 트리거 질문 중 외부 결과에 '2' 1편 이상 | ≥ 50% |
| **주 2:** 덧붙인 논문 중 '0'(무관) | ≤ 30% |
| 보호: OpenAlex 실패(≥ 6s · 오류) | ≤ 10% |
| 보호: 답변 뒤 추가 대기 중앙(5문항) | ≤ 2s |
| 보고: v2 같은 지표(같은 M 질문), 트리거 수, 정리 전·후 검색어 예 | |

두 주 지표를 **모두** 만족하면 채택 후보 → 사용자 승인 후 운영 `.env` `RAG_EXTERNAL_SEARCH=1` + 봇 재시작.

예상: 주 1 55~65% · 주 2 20~28%.

## 4. 기록

| 날짜 | 내용 |
|---|---|
| 2026-10-20 | 새 질문 30 · 일반어 목록 고정 · 사전 등록. |
| 2026-10-20 22:08 | v3 구현(테스트 660 통과) · M 검색(`xs_M`) 30/30 끝 · v2/v3 외부 결과 23/30 에서 **사용자 요청으로 중단**(`measure_v3.jsonl` 23행, 사본 `measure_v3_part1.jsonl`). 재개는 남은 7문항만 이어서 잰다(스크립트가 파일을 새로 쓰므로 사본과 합칠 것). |
