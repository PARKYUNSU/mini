# 상한선 비교 — 같은 파이프라인, 답변 모델만 gpt-oss-120b (사전 등록, 2026-10-13)

> 측정 **전에** 쓴다. 채택 판정이 아니라 **위치 측정**이다(운영 9B 시스템이 강한 모델 대비 어디쯤인가).

## 1. 질문

운영 RAG(검색 → 초록 컨텍스트 → 정답 유무 판정 → 답변 → 후처리)에서 답변 모델 `yunsur_v13`(9B)을 gpt-oss-120b 로 바꾸면 내용 품질이 얼마나 오르나. 그 차이가 "9B 답변 모델의 한계"이고, 남은 오류는 검색·컨텍스트 쪽 한계다.

## 2. 방법

- 생성: `eval_e2e_ko.py --answer` 162문항, 운영 설정(`RAG_ANSWER_MODEL=yunsur_v13 RAG_CONTEXT_ABSTRACT=1 RAG_PRESENCE_JUDGE=1 RAG_HANZI_RETRY=1`) 그대로이고 **RAG 답변 호출만** `EVAL_ANSWER_OPENAI_URL`(RunPod H100 vLLM gpt-oss-120b, temperature 0.2, reasoning medium)로 보낸다. 정답 유무 판정은 운영대로 `yunsur_v13` 이 한다. 후처리·인용 교정은 운영 코드 그대로. 라벨 `ans_ub_gptoss`.
- 검색 DB: 2026-10-13 재구축본(`/Volumes/T7 Shield/mini-chroma-rebuild`). 비교 대상 v13 답변은 `ans_v13abs_pj`(운영 설정) — **컨텍스트 논문이 같은 문항만** 짝으로 쓴다.
- **주 판정: Claude 눈가림 짝 판정**(answer_quality_1010 §6 과 같은 기준·형식, X/Y 순서는 문항 ID 시드 동전). 판정자 일치도는 §6.1 에서 검증됨(κ 0.756). gpt-oss 는 자기 답을 판정하게 되므로 주 판정자로 쓰지 않는다.
- 부 판정(참고): gpt-oss 단일 답변 판정(`judge_answers.py --base-url`) — 자기 선호 편향 가능성을 명시하고 서술만.

## 3. 보고할 것

- 정답 있음 짝에서 ok · correct · wrong · 날조, 각각 McNemar(양측).
- **상대 위치**: v13 ok / gpt-oss ok, v13 correct / gpt-oss correct.
- 정답 없음 문항: 일관 고지 수(`nogold_metrics.py`).
- 지연(문항당 경과 시간 중앙값) — 참고(H100 vs 맥미니라 공정 비교 아님).

예상: ok 는 비슷(둘 다 높음), correct 는 gpt-oss 가 뚜렷이 높고(부분 정답 → 정답), 날조는 gpt-oss 가 낮다.

## 4. 비용

H100 Secure $3.99/h(또는 Community $2.69/h) — 답변 생성 ≈ 1시간(검색·판정은 맥미니) + 부 판정 10분 ≈ $4~5.

## 5. 기록

| 날짜 | 내용 |
|---|---|
| 2026-10-13 | 사전 등록. |
