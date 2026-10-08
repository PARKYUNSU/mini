# 한국어 끝단 평가 — 질문이 LLM 컨텍스트에 정답 논문을 싣는가 (사전 등록)

- 시작일: 2026-10-08
- 선행: [`../retrieval_eval_1007/05_conclusion.md`](../retrieval_eval_1007/05_conclusion.md) §11 — 검색 평가셋(영어 검색어 직접 투입)이 재지 않는 단계에서 운영 버그 둘(이전 턴 컨텍스트 재사용, 한국어 검색어 폴백)이 나왔다.
- **이 라운드는 기준선이다 — 판정 없음.** 앞단(라우팅·검색어 추출·상태 관리)을 고칠 때 쓸 자와 현재 값을 만든다.

## 1. 무엇을 재나

한국어 질문 → `router_node` → (`direct_answer` / B 이면) `direct_answer_node` 의 검색어 추출·검색·컨텍스트 조립까지 **운영 노드를 그대로** 실행하고, 답변 LLM 호출만 가로챈다. 지표는 **LLM 에 건네진 `[문서 N]` 번호표에 정답 논문이 있는가** (`number_context_papers` 의 doc_ids — 청크 본문에 인용된 ID 는 세지 않는다). 답변 품질은 재지 않는다.

## 2. 문항

[`ko_questions.tsv`](ko_questions.tsv) · 164문항 · sha256 `7fc27b9d5bc9` — `retrieval_eval_1007` 의 A·C1·C2 를 사용자 말투의 한국어 질문으로 옮겼다 (정답은 같은 `eval_set.jsonl`). 기술 용어(LLM, RAG, CLIP …)는 실제 사용자처럼 영어로 둔다. "검색"이라는 단어가 든 문항 9개 — 인위적으로 빼지 않았다. `A026`·`A057` 은 정답이 Chroma 에 없어 제외 → **162문항**.

파일럿 3문항(`A063`·`C1_07`·`C2_03`, 하네스 확인용)은 결과에 넣지 않는다. 파일럿 후 문항은 바꾸지 않았다.

## 3. 측정

```bash
.venv/bin/python scripts/eval_e2e_ko.py --label prod_r1
.venv/bin/python scripts/eval_e2e_ko.py --label prod_r2
```

- 문항마다 새 chat_id, 앞뒤로 `clear_session` — 세션 오염 없음.
- 실패 라벨: `route`(direct_answer/B 아님) · `query_korean`(검색어에 한글) · `retrieval`(컨텍스트에 정답 없음) · `no_context`.
- **검색어 추출(로컬 LLM, temperature 0.2)과 라우터 3단계 LLM 분류는 비결정적이다.** 파일럿에서 `C1_07` 이 실행마다 적중이 갈렸다. 그래서 2회 잰다: **주 수치는 `prod_r1`**, `prod_r2` 는 문항별 적중이 두 번 사이에 바뀌는 비율(흔들림)을 재는 데만 쓴다.

## 4. 보고할 것 (판정 없음)

1. 162문항 컨텍스트 적중률 (층별).
2. 실패 원인 분포 — 특히 `route` 몇 개가 어느 경로로 샜는지.
3. **같은 문항의 검색 단계 성능과의 차** — `retrieval_eval_1007/results/fix3_lr/production.jsonl`(영어 검색어, Recall@5)과 짝지어: 검색 단계에서는 맞혔는데 끝단에서 놓친 문항 수 = 앞단 손실.
4. r1–r2 흔들림 비율. 이후 앞단 수정의 효과를 판정할 때 이 크기보다 작은 차이는 해석하지 않는다.

## 5. 예상 (기록만)

- 끝단 적중률은 검색 단계(0.951)보다 낮다. 앞단 손실의 다수는 `route` 일 것이다.
- 컨텍스트가 1편으로 줄어드는 경로(`prefer_single_hit`)가 "논문 요약해줘"류에서 정답을 잃게 만든다.
