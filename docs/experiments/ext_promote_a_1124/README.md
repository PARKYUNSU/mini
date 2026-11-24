# ext_promote_a_1124 — 판정 (a) 에도 외부 승격 · 📎 목록 판정 (5차 피드백 U4 / 4차 T6)

## 1. 왜
- 외부 승격(`RAG_EXT_PROMOTE`, ext_promote_1117)은 판정 집계가 (b)/(c) 일 때만 돈다. W07 은 판정 분리 뒤 (a) 가 되어 SAFE(2403.18802, golden)가 빠졌고, W05 2406.15264 도 (a) 라 외부 검색이 안 돈다.
- 📎 DB 밖 목록은 판정 없이 OpenAlex 상위를 그대로 싣는다(W07 5차: 단위 테스트 생성 논문 2302.06527).

## 2. dev 진단 (구현 전, dev10 sf1_d 의 (a) 6문항에 promote_external 만, `.cron/work_1117/probe_ext_a.py`)
| 문항 | 시간 | 승격 | golden |
|---|---|---|---|
| W02 | 9.0s | — | — |
| W05 | 15.2s | InFi-Check(D) | 2406.15264 안 들어옴 |
| W07 | 10.2s | Long-form factuality = SAFE(P) | **들어옴** |
| W08 | 3.8s | Analyzing Sustainability Reports Using NLP(D) | — |
| W09 | 3.5s | Complicated Table Structure Recognition(P) | — |
| W10 | 7.8s | LLM-as-a-Judge 평가 2편(D · P) | — |
27B 러너는 `-np 1` 이라 판정 호출끼리는 겹칠 수 없다 → OpenAlex 검색만 문서 판정과 동시에 미리 한다.

## 3. 무엇
- A `RAG_EXT_PROMOTE_A`(기본 0): 칸 틀 질문이면 문서 판정 시작 때 OpenAlex 검색을 스레드로 미리 시작하고, 집계가 (a) 여도 `promote_external`(후보 4 · 직접/부분 최대 2편)을 미리 찾은 결과로 돌린다. (b)/(c) 도 미리 찾은 결과를 쓴다.
- B `RAG_EXT_LIST_JUDGE`(기본 0): 📎 목록 후보 중 초록 있는 것을 27B 로 판정해 무관(N)은 뺀다. 답변 생성(v13)과 동시에 도는 스레드 안에서 한다(다른 러너라 겹침). 초록 없는 후보 · 판정 실패는 그대로.

## 4. 사전 등록 (측정 전, 11-24)
실행: dev10 · L30(agg_slots_1117/heldout30b) · N30(cond_keep_1118/heldout30) 을 두 플래그 0 / 1 로.
A
- 주 지표: dev10 golden 누락이 늘지 않고 W07 SAFE 가 답에 들어간다. held-out 에서 (a) 인데 승격이 일어난 문항의 블라인드 쌍에서 플래그 1 승 > 패, 패 ≤ 승의 절반.
- 보호 1: 승격된 논문이 질문과 관련 있음(Claude 판정, 제목 · 초록) ≥ 80%.
- 보호 2: 전체 문항 응답 시간 중앙값 증가 ≤ +8s.
B
- 주 지표: 📎 에서 뺀 후보 중 실제 무관(Claude 판정) ≥ 80%.
- 보호: 📎 답변 뒤 대기 시간 중앙값 증가 ≤ +2s.
