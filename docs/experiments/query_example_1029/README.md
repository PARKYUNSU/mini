# R_134 검색어가 질문 속 예시("RAG검색을 했을시에")에 끌리는 문제 (진단만, 2026-10-29)

> 출발점: corpus_er_1029 — 빈 분야 47편 수집 뒤 일상어 질문 12개 중 10개에 직접 관련 논문이 들어왔지만, 실사용 R_134(job 134 · 135)만 0 → 0.

## 1. 본 것 — `diag.py` (읽기만, 운영 검색 경로 `rag.search(top_k=15)`)

| 검색어 | 만든 방법 | 상위 15 중 수집 논문 | 상위 5 중 |
|---|---|---|---|
| `rag search across multiple databases duplicate content detection in large document collections` | 운영 검색어(원문 질문, 3회 같음) | 1 | **0** (RAG Does Not Work for Enterprises · KG RAG · RAG 서베이 …) |
| `database similarity search, duplicate document detection across databases, large-scale text comparison research` | 운영 검색어 — 질문에서 "예를들어 RAG검색을 했을시에," 만 뺌(3회 같음) | 9 | **4** (FOLD · Noise-Robust De-Duplication · ER 서베이 · H3D …) |
| `duplicate content detection across multiple large databases` | 손 | 8 | 5 |
| `near-duplicate detection, entity resolution, similarity join across large document collections` | 손 | 13 | 5 |
| `rag, near-duplicate detection across two large document databases` | 손(RAG 남김) | 4 | 4 |

- 검색어 LLM 이 결정적(3회 같음) — 우연이 아니다.
- **원인: 검색어 맨 앞 `rag search` 한 구.** RAG 를 남겨도 쉼표로 떼고 분야 용어를 넣으면(손 C) 상위 5 중 4 가 수집 논문. 운영 검색어는 쉼표 없이 12단어 한 덩어리(5단어 초과 → 공백 이어 쓰기 폴백)라 'rag search' 가 주제처럼 앞에 붙었다.
- 질문의 RAG 는 "예를 들어 RAG 검색에서" — 쓰임새 예시. 프롬프트 대상이 "academic RAG retrieval" 이라 RAG 쪽으로 더 끌린다(query_norag_1027 에서 이 대상 문구를 바꾸는 안은 이미 기각, 27:23).

## 2. 얼마나 자주 — 이 모양이 드물다

- 평가 세트 336문항(162 · real40 · real2 · H · D · U): "예를 들어 · 가령 · 예컨대" 0.
- 실사용 135 job: 예시 표현 3(76 은 분류 지시, 103 "대기업처럼" 은 비교, **134 · 135 만 이 모양** — 같은 질문 두 번).
- 즉 고유 질문 1개. 이 하나를 위한 규칙(질문 앞 "예를 들어 … 했을 시에," 지우기 · 프롬프트 규칙 추가)은 다른 질문에 미칠 영향을 잴 표본이 없다.

## 3. 결론

라운드 만들지 않음. 병목은 9B 검색어가 "예시로 든 맥락"과 "묻는 주제"를 구분하지 못하는 것 — 이 모양 질문이 실사용에서 더 쌓이면(예: 3 고유 이상) 그때 질문 모아 사전 등록. 그 전까지는 사용자에게 "RAG" 를 빼고 묻거나 "중복 탐지 · 개체 매칭" 같은 용어를 넣으면 찾힌다는 것만 안다.
