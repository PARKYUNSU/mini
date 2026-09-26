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

## 6. v9·v10 에 주는 것

- **v9 판단은 바뀌지 않는다.** 코딩은 운영(Groq)에 없으므로 빼는 것이 맞고, 문헌도 자기 증류로 능력 슬롯을 학습하는 것을 지지하지 않는다.
- **v10 후보가 데이터 축에서 하이퍼파라미터 축으로 옮겨간다.** 가장 싼 것은 **lr 인하** 단독 실험이다 (예: 2e-4 → 5e-5). 데이터 제작 비용 0, 학습 1회, 측정 1회. v9 데이터를 그대로 쓰면 단일 변수가 된다.
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
