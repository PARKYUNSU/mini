# '없음' 판정 뒤 논문 나열 · 검색어 진단 (2026-10-29)

> 진단만 — 코드 변경 없음. 출발점: router_research_1028 운영 ON 확인 질문(두 대형 DB 간 유사·중복 내용 찾기)과 job 134(10-28)가 "제공된 문서에는 질문이 찾는 연구가 없습니다" 뒤에 논문을 나열하고 결론에서 찾은 것처럼 정리했다. 재현: `scripts/eval_e2e_ko.py --answer --save-context --label ask_1029`(`.cron/ask_1029.log`).

## 1. 형식 모순 — 원인: 결론 다시 쓰기가 '없음' 결론을 덮어씀

- 정답 유무 판정 `없음` → `NO_DOC_HINT`(`core/llm/presence_judge.py:76`)가 형식을 지시: 서론 "없습니다" · 본론 가까운 문서 최대 2 개 + `(관련 연구)` · 결론 "따라서 … 찾을 수 없습니다". **본론 2 편 나열은 설계대로.**
- 그 뒤 `rewrite_conclusion`(`agent_nodes.py:1410`)이 판정과 상관없이 돈다(인용 2 편 이상이면 대상). 확인 질문 로그: `정답 유무 판정 = 없음` → `결론 다시 쓰기 = 바꿈` — "찾을 수 없습니다" 결론이 두 논문 결과 요약("유사한 내용을 찾는 연구 결과를 제시")으로 바뀜.
- 본론 `(관련 연구)` 표시도 빠짐(모델이 지시를 안 따름 — 코드에서 지우는 곳 없음).
- 빈도(`.cron/*.log` + `bot_ai_worker.log`, 측정 로그 중복 포함 가능): 판정 `없음` 답 약 800 중 결론 `바꿈` 204(약 25%). 실사용 로그(로테이션 뒤 11.7 k 줄)는 `없음` 2 건 중 1 건 `바꿈`.

**후보 수정:** `_pick == "없음"` 이면 결론 다시 쓰기 건너뜀(한 줄). 필요하면 본론 항목에 `(관련 연구)` 를 코드로 붙임. 효과 지표: `없음` 답의 결론 첫 문장 형식 지킴 비율 · 과장 결론 수.

## 2. 검색어 — 분야 용어를 못 만듦, 다만 DB 공백이 더 큼

운영 검색어 `rag search across multiple databases duplicate content detection in large document collections` = 질문 직역. 같은 질문으로 15 편 검색 → 관련 문서 거르기:

| 검색어 | 거르기 | 남은 논문 |
|---|---|---|
| 운영(직역) | 없음 | — (RAG 일반 · 기업 RAG) |
| `entity resolution record linkage near-duplicate detection across large databases` | 15→3 | LLM-Align(2412.04690) · Complex Ontology Matching(2502.13619) · KG+LLM 지식 통합(2401.16960) |
| `cross-collection document similarity matching deduplication large corpora` | 없음 | — |

분야 용어를 쓰면 3 편이 남지만 모두 지식 그래프 · 온톨로지 정렬(가까운 주제)이고, 대규모 문서 집합 간 유사 · 중복 탐지(near-duplicate detection, similarity join, cross-corpus dedup) 직접 연구는 DB 에 거의 없다. 검색어 라운드는 이미 마무리(DB 검색어 v2 기각 · 후처리 유의 X)라, 이 질문은 **코퍼스 공백 + 외부 검색**(이번에도 OpenAlex 1 편)이 맞는 대응.
