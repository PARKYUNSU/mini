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

## 3. 사용자 맥락 (2026-10-29 사용자 확인)

사용자 직무는 **LLM · RAG** — 질문 속 "RAG" 는 대개 진짜 맥락이다(평가 세트에서도 RAG 언급 73/336). 그래서 고치는 방향은 **RAG 를 빼는 것이 아니라 RAG 와 분야 용어를 둘 다 살리는 것**: 손 검색어 C(`rag, near-duplicate detection across two large document databases`)는 RAG 를 남겨도 상위 5 중 4 가 수집 논문 — 쉼표 덕이 아니라 `near-duplicate detection` 이라는 분야 용어 덕(§5). 사용자가 원하는 답은 두 쪽 모두 — 대형 DB 간 중복 · 유사 탐지 연구 + RAG 에서의 쓰임(검색 문서 중복 제거 · 여러 출처 RAG).

## 4. 결론

라운드 만들지 않음. 병목은 9B 검색어가 "예시로 든 맥락"과 "묻는 주제"를 구분하지 못하는 것 — 이 모양 질문이 실사용에서 더 쌓이면(예: 3 고유 이상) 그때 질문 모아 사전 등록. 그 전까지 사용 팁: "RAG" 는 두고 "중복 탐지 · 개체 매칭" 같은 분야 용어를 함께 넣으면 찾힌다. ~~후보 방향: 한 덩어리 검색어를 쉼표 구로 나누기~~ → §5 에서 **반박됨**.

## 5. 진단 2 — 쉼표 · 순서는 원인 아님 (`diag2.py`, 2026-10-29)

검색은 쉼표 구를 따로 검색하지 않는다(한 문자열로 벡터 + BM25). 같은 단어로 쉼표 · 순서만 바꿨다.

| 검색어 | 상위 5 중 수집 논문 |
|---|---|
| 운영 그대로 `rag search across multiple databases duplicate content detection in large document collections` | 0 |
| 같은 단어 + 쉼표 4구 | 0 |
| 같은 단어, 순서 바꿈(rag search 를 뒤로) | 0 |
| `rag search` → `rag` 한 단어 + 쉼표 | 2 |
| `rag search` 뺌 | 3 |
| (진단 1) 예시 뺀 질문의 운영 검색어 — `similarity search · duplicate document detection` | 4 |
| (진단 1) 손 C — `rag, near-duplicate detection …` | 4 |

- 쉼표 · 순서는 효과 0. **단어가 결정한다**: `rag search` 두 단어가 강하게 끌고, 그걸 빼도 `duplicate content detection` 은 3. 분야 용어 `near-duplicate detection` · `deduplication` · `duplicate document detection` 이 들어가야 4~5.
- 그래서 '쉼표 구로 나누기' 안은 사전 등록하지 않는다. 남은 지렛대는 **검색어 단어 선택(일상어 → 분야 용어)** — external_term_1029(9B 는 직역)과 같은 벽.

## 6. 진단 3 — 10-30 08:32 실사용 실패 재현 (`diag3.py`, 2026-10-30)

같은 질문(예시 "예를들어" 뺀 꼴, job 136)을 10-30 08:30 에 보냈고 "찾을 수 없음". (job 134 10-28 · 135 10-29 도 같은 질문 · 같은 실패) 운영 로그 검색어는 `cross-database retrieval similarity duplicate document detection large-scale database comparison research rag search` — 이번엔 분야 용어 `duplicate document detection` 이 **들어 있었다**. 그 검색어 그대로 재현:

| 단계 | 결과 |
|---|---|
| 청크 300 원순위 | 중복 탐지 논문 6 · 10 · 23 · 35 · 48위 (Deduplicating Training Data · H3D · FOLD · Levenshtein 유사도 · ER 서베이) |
| 논문 단위 + light rerank 15편 (운영) | 수집 논문 1/15 — H3D 5위뿐. 나머지 일반 RAG 논문 (Multi-Meta-RAG 1위 · Progressive Searching 2위) |
| (참고) light rerank 끔 15편 | 수집 논문 2/15 — Billion-scale similarity search 1위 · 중복 이상사례 탐지 2위 · H3D 4위 |
| 관련 문서 거르기 (15편, 2번) | 둘 다 `없음` → 아무것도 안 빼고 상위 5 (H3D 5위 포함) |
| 정답 유무 판정 | 없음 → 답은 "찾을 수 없음" + Multi-Meta-RAG · Progressive Searching |

**읽은 것 — 실패 지점 둘**
1. **논문 단위 재순위(light rerank, 제목 + 초록 + 청크 임베딩 코사인)** 가 `rag search` 쪽으로 끌어 중복 탐지 논문을 15편 밖으로 민다. 청크 원순위에선 6 · 10 · 23위였다. 끄면 관련 논문이 1 · 2 · 4위.
2. **거르기 · 판정 LLM 이 H3D(문서 중복 제거)를 관련으로 안 본다.** 상위 5 안에 있었는데도 거르기 `없음`, 판정 `없음`. 질문 앞 "RAG검색을 했을시에" 때문에 'RAG 논문이어야 한다'로 읽는 것으로 보인다(추정, 확인 안 함).
- §5 의 "분야 용어가 들어가면 4~5" 는 이번엔 맞지 않았다 — 검색어에 `duplicate document detection` 이 있어도 뒤 단계 둘에서 졌다. 검색어만의 문제가 아니다.
- 빈도: 실사용 고유 질문은 여전히 이 하나(job 134 · 135 · 136 = 같은 사용자 같은 질문, 사흘에 한 번씩). light rerank 는 운영 전체에 걸린 단계라 이 한 질문으로 바꾸면 안 된다.

## 7. 진단 4 — 거르기 · 판정이 H3D 를 버리는 원인 (`diag4.py`, 2026-10-30)

§6 의 같은 15편(운영 검색어 · light rerank 켬)에 질문 표현 · 순서만 바꿔 거르기와 판정을 돌렸다. 질문 변형은 원인을 보려는 것이고, RAG 를 질문에서 빼는 것을 해법으로 쓰지 않는다(§3). 판정은 `judge_presence`(운영의 공유 앞부분 호출과 프롬프트는 같고 호출 방식만 다름).

| 질문 | 거르기 | H3D 남음 | 판정 |
|---|---|---|---|
| Q0 운영 원문 ("RAG검색을 했을시에, …조사해줘") | 없음 (아무것도 안 뺌) | — | 없음 |
| Q1 앞의 "RAG검색을 했을시에," 뺌 | 15→1 | ✓ (H3D 만) | 없음 |
| Q2 RAG 를 문장 뒤로 ("…조사해줘. RAG 검색에 쓰려고 해") | 15→6 | ✓ (1번) | 없음 |
| Q3 RAG 앞 그대로 + "(중복 탐지)" 덧붙임 | 없음 | — | 없음 |
| Q0 + H3D 를 1번 자리로 | 없음 | — | 없음 |

**읽은 것 — 원인 둘, 서로 다르다**
1. **거르기: 질문 첫머리 "RAG검색을 했을시에," 가 거르기 LLM 을 'RAG 논문만 관련'으로 읽게 한다.** 같은 RAG 를 문장 뒤에 두면(Q2) H3D 를 1번으로 남긴다. 분야 용어를 덧붙여도(Q3) · H3D 를 1번에 놓아도 못 고친다 — 순서 · 용어가 아니라 첫머리 틀(frame)이 원인.
2. **판정: 5 경우 모두 '없음' — H3D 하나만 남은 Q1 에서도.** 원인은 질문 유형. 운영 판정 프롬프트(v1)는 "사용자는 **특정한 연구 하나**를 찾고 있다"고 가정하는데, 이 질문은 분야 조사("…연구에 대해서 조사해줘")다. 목록 게이트 정규식(`논문들|연구들|동향|정리해|트렌드|N개 찾|목록`)에 "조사해줘"가 없어 판정 대상이 되고, 목록 모드(10편 · 판정 없음)도 안 탄다.
- 실사용 136 job 중 "조사 · 연구 있어 · 찾아줘"류인데 게이트 밖 14, 그중 '없음' 답 4 (134 · 135 · 136 이 질문, 114 faithfulness 검증 — 115 재질문은 정상).
- 판정 쪽(2)은 질문 하나가 아니라 **질문 유형** 문제라 표본을 모을 수 있다. 다만 e2e 162 는 "방법 알려줘"(특정 연구 찾기)가 대부분이라 "조사해줘" 유형 평가 문항이 거의 없다 — 라운드를 하려면 새 질문이 필요하다.
