# 선행 연구 대조 — 우리가 본 현상은 알려진 것인가

2026-09-27 조사. 동기: v5~v8 네 라운드에서 코딩이 base 보다 유의하게 나빠졌고([`baseline_0926/`](baseline_0926/), McNemar p=0.004), 데이터 필터·디코딩 어느 쪽으로도 고쳐지지 않았다. **우리 구현의 버그인지, 방법 자체의 성질인지** 확인할 필요가 있었다.

결론부터: **방법의 성질이고 문헌에 잘 기록돼 있다.** 그리고 **우리가 시험하지 않은 처방이 둘 있다.**

> **출처 신뢰도 표시.** 아래에서 ✔︎ 는 원문을 직접 읽고 확인한 것, ○ 는 검색 요약에서 가져온 것이다. ○ 항목의 수치는 원문 확인 전에 크게 기대지 않는다.

## 1. 좁은 도메인 SFT 는 일반 능력을 깎는다 (catastrophic forgetting)

- ○ 도메인 SFT 가 코딩·수학·지시 따르기·다중 턴 대화를 떨어뜨리는 것은 catastrophic forgetting 으로 문서화돼 있다. Llama-3-70B 를 의료 데이터로 학습하면 MATH 가 30%p 이상 떨어진다는 보고.
- ○ **LoRA 는 완화하지만 제거하지 않는다.** 오히려 replay 없는 LoRA 가 full fine-tuning 보다 더 잊는다는 보고도 있다. LoRA 는 base 능력을 더 많이 남기지만 여전히 시작 모델보다 대부분 지표에서 낮다.
- ○ Qwen 계열 수치: 코드 학습 후 GSM8K 가 softmax_only 에서 −11.3%p, all_layers 에서 −21.9%p.

**우리 관찰과의 대조**: 우리는 코딩을 *학습시켰는데도* 코딩이 나빠졌다. 위 사례들은 A 를 학습해 B 를 잃는 구조인데, 우리는 A 를 학습해 A 를 잃었다 — 이것이 다음 절과 연결된다.

## 2. 자기 증류는 특히 알려진 함정이다 — 우리 상황과 정확히 겹친다

- ○ 자기 증류는 출력을 간결하게 만들면서 추론 능력을 떨어뜨린다. **모델이 작을수록 심하다**: 1.7B 45.9% 저하 vs Qwen3-8B(thinking on) 12.1%. OOD 평가 점수가 **base 아래로 내려간다**고 명시.
- ○ 교사를 바꾼 대조가 결정적이다. 같은 모델을 교사로 쓴 자기 증류는 테스트 정확도 **−0.4%**, 더 강한 교사(RL 모델)를 쓴 교차 증류는 **+11.6%**.

**우리 관찰과의 대조**: v4 결론에 "자기 증류의 상한 — base 출력으로 학습했으므로 base 를 넘을 수 없다" 고 적었다. 문헌은 한 걸음 더 나간다: **넘지 못하는 것이 아니라 내려간다.** 우리 코딩 슬롯이 정확히 그랬다 (base 15.6% vs v6 46.7%). 우리 데이터는 100% 자기 증류였고(RAG 만 v3_clean 재활용), 모델은 9B 로 위 실험들의 "작은 모델" 구간에 가깝다.

## 3. 성공 사례가 있다 — 처방은 둘

### (1) Replay: 일반 데이터를 섞는다
- ○ 권고 비율은 일반 사전학습 데이터 **5~10%** 혼합, 또는 예시 수 기준 **~23%** replay. 대규모 레시피에서는 도메인:일반 토큰 **2:1**.
- ○ **처음부터 섞어야 한다.** 도메인 학습 후에 추가하면 효과가 떨어진다. replay 는 혼합 비율에 민감하다.
- ○ 보존 효과: 과학 지식이 full FT 에서 7배, LoRA 에서 250배 잘 남았다는 보고.

### (2) 더 낮은 학습률 ✔︎
- ✔︎ [`SFT Doesn't Always Hurt General Capabilities`](https://arxiv.org/html/2509.20758v3) — 제목이 우리 질문 그대로다. 중심 주장: **학습률을 낮추면** 도메인 성능과 일반 능력 보존을 동시에 얻는 유리한 절충점이 생긴다.
- ✔︎ 권고 lr **1e-6** (선행 연구의 5e-6·2e-5 대비). 그것으로 부족하면 **TALR**(Token-Adaptive Loss Reweighting, 어려운 토큰의 가중치를 낮춤, τ = 배치별 평균 토큰 손실의 중앙값).
- ✔︎ MedCalc, lr 1e-6: 표준 SFT 는 도메인 0.534 / 일반 0.692, TALR 은 도메인 0.501 / 일반 0.717.
- ✔︎ 검증 모델: Qwen2.5-3B-Instruct, Qwen3-4B, Gemma3-4B. **LoRA rank·epoch·혼합 비율은 논문에 없다.**

## 4. 우리 설계의 맹점

**lr 을 v3 부터 v9 까지 2e-4 로 의도적으로 고정했다.** "데이터만 바꾼 효과를 분리한다" 는 정당한 이유였고 라운드마다 노트에 명시했다. 그런데 그 결과 **문헌이 주 레버로 지목하는 하이퍼파라미터를 한 번도 시험하지 않았다.** 다섯 라운드를 데이터 축에서만 움직였다.

**과장하지 않기 위해 적어 둔다**: 위 논문의 1e-6 은 full fine-tuning 기준이고, LoRA 는 관례적으로 훨씬 높은 lr 을 쓴다 (2e-4 는 LoRA 표준 기본값에 해당). 따라서 "우리가 200배 높다" 는 서술은 성립하지 않는다. 직접 비교 가능한 LoRA 기준 권고치는 이번 조사에서 찾지 못했다. 그래도 **방향은 분명하고 우리가 건드리지 않은 축**이라는 점은 유효하다.

우리가 쓰지 않은 것을 정리하면:

| 처방 | 우리 상태 | 비용 |
|---|---|---|
| 일반 데이터 replay | **안 했다.** 데이터 100% 자기 증류 (RAG 만 v3_clean 재활용) | 데이터 확보 필요 |
| 낮은 학습률 | **안 했다.** lr 2e-4 로 v3~v9 고정 | **없음** — 학습 1회 $0.5 |
| 더 강한 교사로 교차 증류 | 안 했다 (Gemini·Groq 를 교사로 쓸 수 있었다) | 데이터 재생성 비용 |
| TALR | 안 했다 | 학습 코드 수정 |

## 5. 못 찾은 것

**Qwen3.5-9B 를 직접 파인튜닝한 커뮤니티 후기를 찾지 못했다.** 검색 결과가 논문 쪽으로 쏠렸고 LocalLLaMA 류 실사용 스레드는 걸리지 않았다. 모델이 최근이라 후기가 적을 수도 있고, 검색어가 학술 쪽으로 편향됐을 수도 있다. 필요하면 커뮤니티만 따로 조사한다.

또한 위 ○ 표시 항목은 검색 요약에서 온 것이므로, **v10 설계의 근거로 쓰기 전에 원문을 확인할 것.** 특히 replay 혼합 비율(5~10% vs 23% vs 2:1)은 출처마다 달라 그대로 채택하기 어렵다.

## 6. 교차 증류 — 교사를 재보니 결론이 바뀌었다 (권하지 않음)

문헌은 자기 증류의 상한을 깨는 유일한 방향으로 **더 강한 교사**를 지목한다 (같은 모델 교사 −0.4% vs 강한 교사 +11.6%, §2). 이 프로젝트에 **이미 붙어 있는** 후보가 셋이다 — 새로 계약할 것이 없다.

| 후보 | 현재 용도 | 교사로서의 성격 |
|---|---|---|
| **Groq `openai/gpt-oss-120b`** (`GROQ_CODING_MODEL`) | Executor 코드 작성 · Monitor 검수 | **코딩 교사로 가장 적합.** 120B 로 체급 차이가 분명하고, 이미 `EXECUTOR_SYSTEM_CODE_RUN` 프롬프트로 코드를 쓰고 있어 **교사 출력이 학습 형식과 바로 맞는다.** 운영이 실제로 쓰는 모델이므로 "운영이 내는 답을 로컬이 흉내낸다" 는 목표와 일치한다. 무료 티어면 429 레이트 제한이 병목 (`_CodingChatGroqWithRetry` 가 지수 백오프로 4회까지 재시도) |
| **Gemini `gemini-3-flash-preview`** (`GEMINI_MODEL`) | 라우터 · 도구 · Tavily 요약 폴백 | 처리량이 좋고 이미 폴백 경로에 있다. 코딩 전용은 아니나 계획·잡담 슬롯 교사로는 충분 |
| **Anthropic** (`ANTHROPIC_API_KEY`) | `apps/boardroom/swarm_meeting.py` 만 사용 | 셋 중 코드 품질이 가장 높은 편. 다만 코딩 경로에 안 붙어 있어 배선이 필요하다 |

### Groq 을 실제로 재봤다 (2026-09-27) — 결론이 바뀐다

교사 후보를 고르기 전에 **Groq 이 우리 문항을 실제로 푸는지** 재봤다. 지금까지 한 번도 재지 않았다. [`scripts/eval_groq_coding.py`](../../scripts/eval_groq_coding.py) 로 평가기와 **같은 프롬프트·같은 판정**(`_coding_ok`, `extract_python_code`)을 써서 30문항 × 3회. 원본 [`teacher_check_0927/groq_coding.jsonl`](teacher_check_0927/groq_coding.jsonl).

| 모델 | 시행 실패 | 과반 실패 문항 | 시간 중앙 | 어려움 12문항 |
|---|---|---|---|---|
| **Groq `openai/gpt-oss-120b`** | **0/90** | **0** | **2.8s** | **0/12** |
| base `qwen3.5:9b` | 14/90 | 5 | 5.9s | 4/12 |
| v9 | 19/90 | 5 | 7.0s | 4/12 |
| v6 | 42/90 | 14 | 17.1s | 10/12 |

v6 만 실패했던 9문항(`coding_07`·`19`·`21`·`22`·`25`·`26`·`27`·`28`·`30`)을 Groq 은 **전부 0/3** 으로, 문항당 2~5초에 풀었다.

**"어려움" 구간의 의미가 바뀐다.** 절대적으로 어려운 문제가 아니었다 — 120B 는 3초에 푼다. 격차는 문제 난도가 아니라 **모델 용량**이다. 9B 가 못 하는 것을 120B 는 시시하게 한다.

### 그래서 교사 라운드는 권하지 않는다

1. **운영에 문제가 없다.** Groq 0/90 · 2.8초. 교차 증류의 목표가 "운영 답안을 로컬이 흉내내기" 인데 흉내낼 대상이 이미 완벽하다.
2. **최선의 경우가 base 수준이다.** 로컬 천장은 우리 측정으로 15.6%(base)이고 v9 가 이미 거기 도달했다 (둘 다 과반 실패 5문항). 교차 증류가 base 를 넘어야 의미가 있는데, 여섯 라운드가 9B 에서 그것이 안 된다는 방향을 일관되게 보였다. 격차가 용량이라면 완벽한 교사를 줘도 천장은 남는다.
3. **원하던 것(Groq 끊김 대비)은 학습으로 얻는 것이 아니다.** 폴백이 필요하다면 이미 쓸 수 있는 최선의 로컬 모델이 **base** 다 — v9 도 v6 도 base 보다 낫지 않다. 필요한 것은 학습이 아니라 **코드 수정**이다 (아래).

### 대신 할 일 — `executor_node` 에 폴백이 없었다 ✔︎ 배선 완료 (2026-09-27)

**했다.** [`core/graph/agent_nodes.py`](../../core/graph/agent_nodes.py) 의 `executor_node` 는 이제 `_invoke_llm_with_fallback(getters=(get_coding_groq_llm, get_planner_llm))` 으로 **Groq → 로컬 base** 체인을 탄다. 다른 노드들과 같은 경로이고, 코딩만 단일 경로였던 것이 없어졌다.

전(前): `get_coding_groq_llm()` 을 **직접** 호출하고 `llm.invoke(...)` 로 썼다 → Groq 이 429 나 장애를 내면 `except` 로 떨어져 `Error: Executor: ...` 를 반환, **답변 자체가 실패**했다.

바뀐 점:

- **폴백 체인**: Groq 이 죽으면(getter 예외든 `invoke` 예외든) 로컬 base(`get_planner_llm`, `OLLAMA_MODEL` · `num_predict=OLLAMA_DIRECT_NUM_PREDICT`)가 받는다. base 는 15.6% 실패율이지만 위 표대로 **아무 답도 못 주는 것보다는 낫다.** 파인튜닝(v6·v9)은 base 보다 나쁘므로 폴백에 쓰지 않는다.
- **`fallback_msg=""`**: 전부 실패하면 사과문 대신 빈 문자열을 받아 `RuntimeError` 로 올린다 → 기존과 같은 `Error: Executor: ...` 를 돌려주고, **사과문이 코드로 실행되는 일이 없다.**
- **어느 LLM 이 답했는지 로그에 남는다**: `_invoke_llm_with_fallback` 이 `adopted` 트레이스(`getter=... label=... fallback_used=...`)를 `_llm_invoke_trace` 관례로 bot.log 에 찍고, `adopted_out` dict 로 호출자에게도 넘긴다. Executor 는 `[DEBUG] Executor: LLM=... getter=... fallback=...` 을 남긴다. 모든 노드가 같이 얻는 정보다.
- **테스트**: [`tests/unit/test_executor_groq_fallback.py`](../../tests/unit/test_executor_groq_fallback.py) — Groq getter 429, Groq `invoke` 503, 양쪽 전멸, 정상 Groq 시 로컬 미호출, 배선 회귀(폴백이 base 인지 · 파인튜닝이 아닌지) 5건. `core.graph.agent_nodes` 임포트가 SMB 마운트에서 10분 걸리므로, 모듈을 임포트하지 않고 **해당 함수 소스만 ast 로 떼어내** 스텁 전역에서 실행한다 (1.2초).

남은 한계 둘. **(1) 타임아웃은 걸지 않았다.** Groq 이 에러를 내지 않고 매달리면(hang) 폴백이 발동하지 않는다 — 전과 같다. **(2) Groq 이 빈 응답을 주면 폴백하지 않는다** — `_invoke_llm_with_fallback` 은 빈 출력을 "실패" 로 보지 않고 그대로 `fallback_msg` 를 돌려주므로(모든 노드 공통 동작) 다음 getter 를 타지 않는다. 이 경우 Executor 는 `Error: Executor: RuntimeError` 로 끝난다 (전에는 빈 코드를 실행했다). 429·장애와는 다른 결이라 이번 범위에 넣지 않았다. `_invoke_llm_with_fallback(timeout_sec=...)` 이 이미 있으니 필요해지면 코딩 슬롯 상한을 재고 붙이면 된다. 코드 생성은 길어질 수 있어 값을 재지 않고 넣으면 정상 생성을 자르는 쪽이 더 위험하다.

목표별로 정리하면:

| 목표 | 필요한 것 | 학습 필요? | 상태 |
|---|---|---|---|
| Groq 끊김 대비 | `executor_node` 에 base 폴백 배선 (`getters=(get_coding_groq_llm, get_planner_llm)` 형태) | **아니오** | **✔︎ 완료 (2026-09-27)** |
| 로컬 코딩을 base 보다 낫게 | 교차 증류 + 검증된 정답 + replay + lr 인하 | 예 — 다만 여섯 라운드가 회의적 | 미착수 (권하지 않음) |
| 운영 코딩 품질 개선 | **불필요** — 이미 0% | — | — |

### 그래도 교사 라운드를 연다면 — 착수 조건

**교차 증류가 통한다는 보장은 없다.** v6 는 어려움 12문항 중 9개를 실패했고 그것은 형식 문제가 아니라 **알고리즘을 못 짜는 것**이었다 ([`yunsur_v9/05_conclusion.md`](yunsur_v9/05_conclusion.md)). 더 좋은 교사 답안을 보여줘도 9B 의 용량 한계는 그대로일 수 있다.

**그리고 지금은 할 이유가 없다.** 운영 Executor 가 이미 Groq 이므로, 교차 증류로 로컬 코딩을 개선한다는 것은 **"Groq 답안으로 학습해 Groq 보다 못한 로컬을 만든다"** 가 된다. 실익은 Groq 이 끊길 때의 대비뿐이다.

**착수 조건**: Groq 비용·가용성이 실제 문제가 되고, **폴백 배선(base)으로도 부족할 때.** 위 측정 이후 조건이 한 단계 올라갔고, 그 폴백 배선은 2026-09-27 에 끝났다 (위) — 이제 남은 착수 근거는 "base 폴백이 실제 장애에서 부족했다" 는 **측정**뿐이다. 끊김 대비만이 목적이라면 더 할 것이 없다.

**주의**: Groq 은 우리 평가 문항 30개를 전부 맞힌다. 그 데이터로 학습하면 평가 오염이므로, 교사 증류는 **학습용 프롬프트**에만 쓰고 평가 문항과의 유사도 격리(< 0.72)를 반드시 유지한다. 또한 "교사가 맞힌다" 는 사실은 학생이 맞힌다는 근거가 되지 못한다 — 격차가 용량이기 때문이다.

### 그때의 순서

1. **검증된 정답으로 데이터를 만든다.** Groq 이 쓴 코드를 **실제로 실행해 통과한 것만** 채택한다 — 평가기의 `_coding_ok`(ast.parse + 임시 디렉터리 8초 실행)를 그대로 재사용하면 된다. **자기 증류 때는 이 검증이 없었다** (생성 필터는 주석 비율·줄 수만 봤다). 교사를 바꾸는 것보다 이 검증이 더 결정적일 수 있으므로, 가능하면 **교사 교체와 정답 검증을 분리해 두 라운드로** 돌린다.
2. **일반 데이터 replay 를 처음부터 섞는다** (§3-(1)). 비율은 출처가 갈리므로 원문 확인 후 정한다.
3. **학습률을 낮춰 함께 시험한다** (§3-(2), §4). 우리가 한 번도 건드리지 않은 축이다.
4. **측정은 [`../../scripts/eval_round.sh`](../../scripts/eval_round.sh) 그대로.** 목표는 "base 초과" 가 아니라 **코딩 짝지은 불일치 쌍을 base 대비 0 으로** 만드는 것이다 ([`protocol.md`](protocol.md) §3).

## 7. v9·v10 에 주는 것

- **v9 판단은 바뀌지 않는다.** 코딩은 운영(Groq)에 없으므로 빼는 것이 맞고, 문헌도 자기 증류로 능력 슬롯을 학습하는 것을 지지하지 않는다.
- **v10 후보가 데이터 축에서 하이퍼파라미터 축으로 옮겨간다.** 가장 싼 것은 **lr 인하** 단독 실험이다 (예: 2e-4 → 5e-5). 데이터 제작 비용 0, 학습 1회, 측정 1회. v9 데이터를 그대로 쓰면 단일 변수가 된다. → 노트 개설: [`yunsur_v10/`](yunsur_v10/) (2026-09-28, 판정 확정 — **비열등성**. v9 가 천장에 닿아 개선은 유의하게 보일 수 없고, 열화만 탐지한다)
- 그 다음이 **replay** 다. 일반 데이터를 어디서 가져올지 정해야 하므로 준비가 더 필요하다.
- **하이퍼파라미터 고정 원칙을 언제 풀 것인지**를 v10 노트에 명시한다. 다섯 라운드를 고정으로 돌려 데이터 축은 충분히 탐색했고, 그 축에서 더 나올 것이 없다는 것이 v8 결론이다.

## 출처

직접 읽음 (✔︎):
- [SFT Doesn't Always Hurt General Capabilities: Revisiting Domain-Specific Fine-Tuning in LLMs](https://arxiv.org/html/2509.20758v3)

검색 요약 (○ — 원문 확인 전):
- [Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?](https://arxiv.org/pdf/2603.24472)
- [Reinforcement Learning vs. Distillation: Understanding Accuracy and Capability in LLM Reasoning](https://arxiv.org/pdf/2505.14216)
- [Understanding Catastrophic Forgetting In LoRA via Mean-Field Attention Dynamics](https://arxiv.org/html/2402.15415v2)
- [Why Your Fine-Tuned LLM Forgets Everything — and How Self-Synthesized Replay Fixes It](https://medium.com/@vishal09vns/why-your-fine-tuned-llm-forgets-everything-and-how-self-synthesized-replay-fixes-it-8f65bd663999)
- [RAFT: Data Refinement and Adaptive Distillation for Domain Fine-Tuning with Alleviated Forgetting](https://arxiv.org/html/2606.00147v1)
- [Learn More, Forget Less: A Gradient-Aware Data Selection Approach for LLM](https://arxiv.org/pdf/2511.08620)
