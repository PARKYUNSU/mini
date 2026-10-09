# 게이트 2단계(LLM) + 라우터 LLM 오분류 되돌리기 (사전 등록)

- 시작일: 2026-10-10
- 선행: [`../query_determinism_1009/README.md`](../query_determinism_1009/README.md) — 끝단 기준선 `det_r1` 0.778. [`../route_fix_1009/README.md`](../route_fix_1009/README.md) §1 의 남은 손실: 게이트 미탐 → Tavily 7 · 라우터 3단계 LLM 이 학술 질문을 A/C 로 6.

## 1. 조치 두 개

- **(b) 게이트 2단계**: `is_academic_query_full = 어휘 규칙 or (아니면) LLM 판정` ([`core/rag/topic_gate.py`](../../../core/rag/topic_gate.py) `is_academic_query_llm`, 검색어 추출과 같은 결정적 LLM — temperature 0, seed 0). 어휘 단어 목록은 그대로다(topic_gate_1009 test 판정 고정). 게이트를 쓰는 두 자리(`is_rag_allowed`, 1단계 Tavily 하드룰)를 `_full` 로 바꾼다.
- **(a) 라우터 되돌리기**: 3단계 LLM 분류가 `direct_answer/A` 또는 `planner/C` 를 냈는데 게이트(어휘 규칙만 — 비용 0)가 학술이라고 하고 명시적 코딩 요청이 아니면 `direct_answer/B`.

## 2. 분류기 판정 (topic_gate_1009 의 같은 분할)

dev 결과(규칙 확정 전 참고): 어휘만 TPR 0.988 · 어휘+LLM **1.000**, 오탐 chat+planner 1/51 (둘 다 `chat_05` — '논문' 단어라 기존 규칙도 허용), coding 0/13.

**test 판정 (결과 전 고정)**: 어휘+LLM 의 TPR 이 어휘만(0.922, 83/90)보다 **3문항 이상** 높고, 오탐 chat+planner **≤ 3/61**. 프롬프트는 dev 를 본 뒤 바꾸지 않았다 — 처음 쓴 그대로다.

## 3. 끝단 판정 (분류기 통과 시, 결과 전 고정)

(a)+(b) 를 함께 켠 코드로 `eval_e2e_ko.py --label gl_r1` · `eval_route_contamination.py --label gl_off`.
- 끝단 `gl_r1` vs `det_r1` 짝지은 McNemar, 새 쪽 p<0.05 우세.
- 오염: chat·planner 의 RAG(B) 경로 각각 ≤ 2.
- 지연: 게이트 LLM 호출은 어휘 규칙이 아니라고 한 '사실 조회형' 요청에서만 생긴다. 끝단 측정 경과 시간 중앙값을 함께 보고한다.

## 4. 예상

분류기: test TPR 0.92 → 0.96 이상, 오탐 0~1. 끝단 0.778 → 0.82 안팎 (표적 13 중 8~10 회복), 오염 0~1.

## 5. 분류기 결과 — test (2026-10-10)

| | TPR | 오탐 chat+planner | coding |
|---|---|---|---|
| 어휘만 | 0.922 (83/90) | 0/61 | 0/17 |
| **어휘+LLM** | **1.000 (90/90)** | **1/61** (`planner_61` "흐릿한 사진을 골라내려 한다…") | 0/17 |

**판정: 통과** (+7문항 ≥ 3, 오탐 1 ≤ 3). 예상(TPR 0.96 이상, 오탐 0~1): 맞음.

연결: `is_rag_allowed` · 1단계 Tavily 하드룰 → `is_academic_query_full`. 라우터 3단계 뒤 `_revert_academic_misroute` (어휘 게이트만). 라우팅 회귀 테스트 65 통과. 끝단·오염 측정 시작.
