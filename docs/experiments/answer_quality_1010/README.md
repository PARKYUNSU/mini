# 답변 품질 — 정답 논문을 정확히 설명하는가 (기준선, 사전 등록)

- 시작일: 2026-10-10
- 선행: [`../topic_gate_llm_1010/README.md`](../topic_gate_llm_1010/README.md) — 끝단 컨텍스트 적중 0.852. 지금까지의 지표는 "정답 논문이 LLM 컨텍스트에 들어갔는가" 뿐이었다.
- **이 라운드는 기준선이다 — 판정 없음.**

## 1. 측정

1. 답변 생성: `eval_e2e_ko.py --answer --label ans_full` — 162문항, 현행 운영 코드(게이트 2단계·결정적 검색어·1편 규칙 끔), 답변 모델 `yunsur_v9`.
2. 판정: [`scripts/judge_answers.py`](../../../scripts/judge_answers.py) — Groq `openai/gpt-oss-120b`. 정답 논문의 제목·초록과 답변을 주고 JSON 으로:
   - `identifies_paper` — 답변이 그 논문을 결과로 제시하는가
   - `description` — correct / partial / wrong / absent
   - `fabrication` — 초록에 없는 구체 사실(숫자·방법·결과)을 그 논문에 붙였는가
   정답이 여럿(C1)이면 답변이 인용한 정답 중 첫 번째를 기준으로 판정한다.

## 2. 보고할 것

- 162 중 `description = correct` 비율 (주 수치), correct+partial, wrong, fabrication 비율.
- **컨텍스트에 정답이 있었던 문항만** 따로 — 검색 실패와 생성 실패를 가른다.
- 실패 유형 분류(수작업 표본 10개): 인용 ID 혼동 / 수치·내용 날조 / 정답을 무시 / 기타.

## 3. 파일럿 (판정기 확인용, 기준선 아님)

`single_hit_1009` 의 `ans_new` 57문항(1편 규칙 끈 상태)에 판정기를 돌렸다: correct 4 · partial 18 · wrong 15 · absent 20, fabrication 25. 수작업 확인 1건(`A007`): 답변이 CoPE 를 설명하면서 **다른 논문의 ID 를 인용**하고 초록에 없는 "256K → 384,000 토큰" 을 지어냈다 — 판정기 판단이 맞았다. 판정기는 쓸 만하다고 보고 본 측정에 쓴다.

## 4. 예상

- 컨텍스트 적중 문항 중 correct 는 20% 미만, wrong+fabrication 이 다수.
- 주된 실패는 **여러 논문을 받은 답변이 내용과 인용 ID 를 엇갈리게 붙이는 것**(교차 귀속)과 수치 날조.
