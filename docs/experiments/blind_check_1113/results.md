# 논문 봇 점검 25 문항 — 운영 설정 재생 결과 (채점 없음)

- 실행: `scripts/eval_e2e_ko.py --answer --save-context` (held-out 재생과 같은 경로, 대화 기록 없음), 운영 `.env` 그대로(`RAG_ANSWER_REPEAT_PENALTY=1.0` 포함). 코드 · `.env` · DB 변경 없음.
- 답 생성은 temperature 0.2 라 같은 질문도 텔레그램에서 물을 때마다 문장이 조금씩 다를 수 있다(검색 · 판정은 같은 입력이면 같다).
- 시간 옆 ⚠ = 그 문항이 도는 동안(시작 시각 + elapsed 누적으로 추정) 운영 모델(`yunsur_v13`) 밖 모델이 Ollama 에 올라와 있었음(`ollama_ps.log`).
- 프롬프트 지문 = 답 LLM 입력(system + user) sha1 앞 12자.

---

## B01. RAGChecker 논문은 RAG를 어떻게 평가해?

- 판정: 있음 — 문서 1
- 경로: `direct_answer/B`
- 시간: 24.8s (단계: query 0.47s · search 12.17s · select 2.78s · judge 2.59s · answer 6.83s)
- 답 길이: 509자
- 프롬프트 지문: `bf1ff8a45f93`
- 오류: 없음

**검색된 문서**

1. RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation [2408.08067]
2. LatentAudit: Real-Time White-Box Faithfulness Monitoring for Retrieval-Augmented Generation with Verifiable Deployment [2604.05358]
3. Towards Lighter and Robust Evaluation for Retrieval Augmented Generation [2503.16161]
4. Evaluation of Retrieval-Augmented Generation: A Survey [2405.07437]
5. Case-Aware LLM-as-a-Judge Evaluation for Enterprise-Scale RAG Systems [2602.20379]

**최종 답 (원문)**

````text
<b>서론</b>
RAG(검색‑증강 생성) 시스템은 외부 지식과 생성 모델을 결합하지만, <b>모듈화된 구조</b>와 <b>긴 응답 평가</b>, <b>측정 신뢰성</b> 문제로 인해 종합적인 성능 측정이 어렵습니다. 이러한 복잡성을 해결하기 위해 정교한 진단 메트릭이 필요합니다.

<b>본론</b>
1. <b>RAGChecker</b>: 검색 및 생성 모듈에 대한 일련의 진단 메트릭을 통합한 미세‑그레인 평가 프레임워크를 제안합니다. [2408.08067v2] 시스템 전체 성능을 포괄적으로 파악하고, 생성 응답의 전반적인 품질을 평가하는 지표입니다. [2408.08067v2] 검색기의 효과를 측정하여 지식베이스에서 관련 정보를 찾는 강점과 약점을 식별합니다. [2408.08067v2]
<b>결론</b>
RAGChecker는 검색과 생성 두 모듈에 대한 진단 메트릭을 제공함으로써 RAG 시스템의 전반적인 품질을 종합적으로 평가하고, 각 구성 요소의 성능 패턴과 트레이드오프를 파악할 수 있게 합니다.
````

---

## B02. RankZephyr가 GPT-4 없이 재순위를 잘하는 비결이 뭐야?

- 판정: 있음 — 문서 1
- 경로: `direct_answer/B`
- 시간: 14.0s (단계: router 2.44s · query 0.71s · search 0.76s · select 2.17s · judge 1.23s · answer 6.72s)
- 답 길이: 519자
- 프롬프트 지문: `f29c319821da`
- 오류: 없음

**검색된 문서**

1. RankZephyr: Effective and Robust Zero-Shot Listwise Reranking is a Breeze! [2312.02724]

**최종 답 (원문)**

````text
<b>서론</b>
정보 검색에서 <b>재순위(listwise reranking)</b>는 관련성 높은 결과를 정렬하는 핵심 단계이며, 특히 <b>제로샷(zero‑shot)</b> 상황에서 모델이 새로운 쿼리·문서에 대해 사전 학습 없이도 효과적으로 작동해야 합니다. 이러한 요구를 충족하려면 데이터 증강과 전략적인 훈련 선택이 필요합니다.

<b>본론</b>
1. <b>RankZephyr</b>: 데이터 증강을 통해 입력 교란에 대한 강인성을 확보하고, 초기 문서 순서와 재순위할 문서 수의 변화에도 견고합니다. [2312.02724v1] 전략적인 훈련 선택을 적용하여 GPT‑4와 효과성 격차를 해소했으며, 일부 경우 proprietary 모델을 능가합니다. [2312.02724v1]
<b>결론</b>
RankZephyr는 데이터 증강과 전략적 훈련으로 입력 교란에 대한 강인성을 확보하고, GPT‑4와 비교해도 효과성이 동등하거나 더 높은 수준을 달성함으로써 제로샷 재순위에서 GPT‑4 없이도 우수한 성능을 발휘합니다.
````

---

## B03. HyperGraphRAG는 기존 GraphRAG와 뭐가 달라?

- 판정: 건너뜀(게이트: cmp)
- 경로: `direct_answer/B`
- 시간: 22.8s (단계: router 4.81s · query 3.33s · search 2.46s · select 2.19s · answer 10.01s)
- 답 길이: 614자
- 프롬프트 지문: `60a6af31e9ca`
- 오류: 없음

**검색된 문서**

1. HyperGraphRAG: Retrieval-Augmented Generation via Hypergraph-Structured Knowledge Representation [2503.21322]
2. RAG vs. GraphRAG: A Systematic Evaluation and Key Insights [2502.11371]
3. Is GraphRAG Needed? From Basic RAG to Graph-/Agentic Solutions with Context Optimization [2606.25656]
4. XGraphRAG: Interactive Visual Analysis for Graph-based Retrieval-Augmented Generation [2506.13782]
5. UnWeaving the knots of GraphRAG -- turns out VectorRAG is almost enough [2603.29875]

**최종 답 (원문)**

````text
<b>서론</b>
기존 <b>GraphRAG</b>는 이진 관계만 표현할 수 있어 복잡한 n‑ary 관계를 다루기 어렵습니다. 이러한 한계를 극복하기 위해 <b>HyperGraphRAG</b>가 제안되었습니다.

<b>본론</b>
1. <b>HyperGraphRAG</b>: 하이퍼그래프를 이용해 n‑ary 관계를 하이퍼에지로 표현하고, 지식 하이퍼그래프 구축·검색·생성 파이프라인을 제공합니다. [2503.21322v3] 기존 GraphRAG와 LightRAG보다 모든 도메인에서 정답 정확도, 검색 효율성, 생성 품질이 우수하며, CS 영역에서는 26,902개의 하이퍼에지를 구축해 지식 포착 능력을 강화했습니다. [2503.21322v3] 기존 GraphRAG가 이진 관계만 연결하는 반면, HyperGraphRAG는 하이퍼에지를 통해 다중 엔티티 간 관계를 직접 모델링함으로써 복잡한 지식 구조를 보다 풍부하게 표현합니다. [2503.21322v3]
<b>결론</b>
HyperGraphRAG는 하이퍼그래프 기반의 n‑ary 관계 표현과 확장된 파이프라인을 도입해 기존 GraphRAG의 이진 관계 제한을 극복하고, 정답 정확도·검색 효율성·생성 품질에서 전반적으로 향상된 성능을 보입니다.
````

---

## B04. FinMCP-Bench에 샘플이 몇 개고 시나리오는 어떻게 나뉘어?

- 판정: 건너뜀(게이트: num)
- 경로: `direct_answer/B`
- 시간: 12.8s (단계: router 2.62s · query 0.39s · search 0.83s · select 2.18s · answer 6.74s)
- 답 길이: 467자
- 프롬프트 지문: `1501f791d92f`
- 오류: 없음

**검색된 문서**

1. FinMCP-Bench: Benchmarking LLM Agents for Real-World Financial Tool Use under the Model Context Protocol [2603.24943]

**최종 답 (원문)**

````text
<b>서론</b>
FinMCP‑Bench는 금융 도구를 호출하여 실제 금융 문제를 해결하는 대형 언어 모델(LLM) 에이전트를 평가하기 위해 설계된 벤치마크입니다. 다양한 시나리오와 사용자 쿼리를 포함하고 있어 모델의 도구 사용 정확도와 추론 능력을 종합적으로 측정할 수 있습니다.

<b>본론</b>
1. <b>FinMCP‑Bench</b>: 613개의 샘플을 보유하고 있으며, 10개의 주요 시나리오와 33개의 하위 시나리오로 구성되어 있습니다. 또한 실제 및 합성 사용자 쿼리를 포함해 다양성을 확보하고, 단일 도구·다중 도구·다중 턴 등 세 가지 유형의 샘플을 제공합니다. [2603.24943v1]

<b>결론</b>
FinMCP‑Bench는 총 613개의 샘플과 10개 주요 시나리오·33개 하위 시나리오로 구성되어 있어, 다양한 금융 도구를 활용한 LLM 에이전트의 성능을 평가할 수 있는 표준화된 테스트베드를 제공합니다.
````

---

## B05. RankGPT 논문에서 LLM으로 재순위하는 방법 설명해줘

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 14.8s (단계: query 1.56s · search 0.76s · select 2.42s · judge 2.28s · answer 7.79s)
- 답 길이: 887자
- 프롬프트 지문: `21f9bef5d848`
- 오류: 없음

**검색된 문서**

1. FIRST: Faster Improved Listwise Reranking with Single Token Decoding [2406.15657]
2. APEER: Automatic Prompt Engineering Enhances Large Language Model Reranking [2406.14449]
3. LLM-Confidence Reranker: A Training-Free Approach for Enhancing Retrieval-Augmented Generation Systems [2602.13571]
4. RankZephyr: Effective and Robust Zero-Shot Listwise Reranking is a Breeze! [2312.02724]

**최종 답 (원문)**

````text
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>RankGPT</b>: GPT4를 이용해 BEIR에서 상위 30개 문서를 재순위하는 작업을 수행합니다. [2406.14449v2]
2. <b>LLM-Confidence Reranker (LCR)</b>: 훈련 없이 블랙박스 LLM의 신뢰도 신호를 활용해 재순위를 개선하며, 두 단계 과정(신뢰도 평가·클러스터링 → 이진화 및 다단계 정렬)을 통해 관련 문서 우선순위와 원래 순위 보존을 동시에 달성합니다. [2602.13571v1]
3. <b>RankZephyr</b>: 오픈소스 LLM으로 리스트별 제로샷 재순위를 수행하며, GPT‑4와 유사한 성능을 보이며 일부 데이터셋에서는 이를 능가합니다. [2312.02724v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• REALM: Recursive Relevance Modeling for LLM-based Document Re-Ranking (2025) https://doi.org/10.18653/v1/2025.emnlp-main.1218
• ReAttn: Improving Attention-based Re-ranking via Attention Re-weighting (2026) [2602.19969]
• Evaluating Reranking Strategies for Portuguese Information Retrieval: Fine-Tuning, LLMs, and Sociocultural Aspects (2026) https://doi.org/10.5753/jbcs.2026.5659
````

---

## B06. AWQ처럼 중요한 가중치만 지켜서 양자화하는 연구 있어?

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 16.5s (단계: router 1.88s · query 0.4s · search 0.66s · select 2.82s · judge 3.02s · answer 7.67s)
- 답 길이: 829자
- 프롬프트 지문: `d4f7ca7faf17`
- 오류: 없음

**검색된 문서**

1. RaanA: A Fast, Flexible, and Data-Efficient Post-Training Quantization Algorithm [2504.03717]
2. On the Expressive Power of Weight Quantization in Large Language Models [2606.22249]
3. KronQ: LLM Quantization via Kronecker-Factored Hessian [2607.07964]
4. Panacea: Novel DNN Accelerator using Accuracy-Preserving Asymmetric Quantization and Energy-Saving Bit-Slice Sparsity [2412.10059]
5. DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs [2610.13767]

**최종 답 (원문)**

````text
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>RaanA</b>: PTQ 프레임워크로, RaBitQ‑H와 AllocateBits 두 구성 요소를 도입하여 빠른 양자화, 최소 교정 데이터 요구, 유연한 비트 할당을 제공한다. [2504.03717v2]
2. <b>KronQ</b>: Kronecker‑factored Hessian 근사를 이용해 활성화와 그래디언트 공분산을 동시에 고려하는 PTQ를 제안한다. [2607.07964v2]
3. <b>DualQuant</b>: 가중치 재구성을 최소화하고, 이를 통해 활성화 스케일링을 자동으로 도출하는 교정‑없는 양자화 프레임워크이다. [2610.13767v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• DAQ: Delta-Aware Quantization for Post-Training LLM Weight Compression (2026) [2603.22324]
• SQS: Bayesian DNN Compression through Sparse Quantized Sub-distributions (2025) [2510.08999]
• A Survey On Neural Network Quantization (2025) https://doi.org/10.1145/3746709.3746773
• BiLLM: Pushing the Limit of Post-Training Quantization for LLMs (2024) [2402.04291]
````

---

## B07. LLM이 학습 데이터의 개인정보를 그대로 외워서 내뱉는 걸 보여준 연구 있어?

- 판정: 있음 — 문서 1
- 경로: `direct_answer/B`
- 시간: 21.6s (단계: router 1.79s · query 0.36s · search 0.69s · select 2.7s · judge 2.79s · answer 8.87s · rewrite 4.44s)
- 답 길이: 870자
- 프롬프트 지문: `cfc7b3e5f3aa`
- 오류: 없음

**검색된 문서**

1. Be like a Goldfish, Don't Memorize! Mitigating Memorization in Generative LLMs [2406.10209]
2. Enhancing Data Privacy in Large Language Models through Private Association Editing [2406.18221]
3. Your LLM Agent Can Leak Your Data: Data Exfiltration via Backdoored Tool Use [2604.05432]
4. Pirates of the RAG: Adaptively Attacking LLMs to Leak Knowledge Bases [2412.18295]
5. You Told Me to Do It: Measuring Instructional Text-induced Private Data Leakage in LLM Agents [2603.11862]

**최종 답 (원문)**

````text
<b>서론</b>
대형 언어 모델(LLM)은 학습 데이터에 포함된 <b>개인정보</b>를 그대로 외우고, 악성 프롬프트가 주어지면 이를 그대로 출력하는 현상이 발생할 수 있다. 이러한 현상은 프라이버시 침해와 저작권 위험을 초래하므로, 모델을 재학습하지 않고도 개인정보를 제거하거나 감지하는 방법이 필요하다.

<b>본론</b>
1. <b>Goldfish Loss</b>: 다음 토큰 예측 목표에 미세한 수정을 가해 훈련 중 무작위로 선택된 토크 Subset 을 손실 계산에서 제외함으로써, 해당 토큰이 모델에 기억되지 않도록 한다. 이는 학습 데이터의 완전한 토큰 시퀀스를 그대로 재현하는 것을 방지한다. [2406.10209v2]
2. <b>Private Association Editing (PAE)</b>: 모델을 다시 훈련하지 않고도 개인정보 식별 정보(PII) 를 효과적으로 제거하도록 설계된 새로운 방어 기법이다. 실험 결과 기존 베이스라인 대비 PII 누출을 크게 감소시킨다. [2406.18221v3]

<b>결론</b>
제공된 문서들은 LLM이 학습 데이터를 그대로 외워 내뱉는 현상을 완화하는 연구들을 다루고 있습니다. [2406.10209v2]은 대규모 Llama-2 모델을 대상으로 광범위한 실험을 수행하여 추출 가능한 기억 효과를 크게 감소시켰으며, 이는 모델이 훈련 세트의 토큰 시퀀스를 그대로 재현하지 못하도록 합니다. 또한 [2406.18221v3]는 PAE라는 방법을 통해 데이터 프라이버시를 보호하는 것이 효과적임을 실험 결과로 입증했습니다. 따라서 두 연구 모두 LLM의 개인정보 외우기 문제를 해결하려는 접근을 제시하지만, 구체적인 방법과 평가 지표가 다르며, 이는 각각 다른 기술적 초점을 가지고 있음을 보여줍니다.
````

---

## B08. 첫 단계 후보 수를 늘리면 cross-encoder 재순위 성능이 포화되는지 다룬 논문 있어?

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 10.3s (단계: query 0.49s · search 0.75s · select 2.33s · judge 1.38s · answer 5.39s)
- 답 길이: 360자
- 프롬프트 지문: `89382ccc3fa0`
- 오류: 없음

**검색된 문서**

1. Efficient Document Ranking with Learnable Late Interactions [2406.17968]

**최종 답 (원문)**

````text
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>Efficient Document Ranking with Learnable Late Interactions</b>: Cross‑Encoder (CE)와 Dual‑Encoder (DE) 모델을 비교하고, DE 구조에 경량 스코어를 추가한 최신 지연 상호작용 모델을 제안한다. [2406.17968v1] LITE는 연속적인 점수 함수를 보편 근사기로 증명하며, 기존 ColBERT보다 일반화 성능이 좋고 지연 시간과 저장 공간을 각각 감소시킨다. [2406.17968v1]
<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.
````

---

## B09. 조선시대 농업 생산성을 다룬 연구 추천해줘

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 15.3s (단계: router 1.64s · query 0.21s · search 0.67s · select 2.28s · judge 2.98s · answer 7.48s)
- 답 길이: 484자
- 프롬프트 지문: `cc1d84184442`
- 오류: 없음

**검색된 문서**

1. Data-Driven Worker Activity Recognition and Efficiency Estimation in Manual Fruit Harvesting [2503.22809]
2. Towards AI Evaluation in Domain-Specific RAG Systems: The AgriHubi Case Study [2602.02208]
3. AgroXAI: Explainable AI-Driven Crop Recommendation System for Agriculture 4.0 [2412.16196]
4. ShizishanGPT: An Agricultural Large Language Model Integrating Tools and Resources [2409.13537]
5. Agri-GNN: A Novel Genotypic-Topological Graph Neural Network Framework Built on GraphSAGE for Optimized Yield Prediction [2310.13037]

**최종 답 (원문)**

````text
<b>서론</b>
제공된 문서에는 조선시대 농업 생산성을 다룬 연구가 없습니다. 질문은 역사적 시기의 농업 기술과 생산성 변화에 대한 정보를 찾고 있습니다.

<b>본론</b>
1. <b>Data-Driven Worker Activity Recognition and Efficiency Estimation in Manual Fruit Harvesting</b>: 이 연구는 수확 작업자의 비생산 활동을 감지하고 효율을 추정하는 시스템을 개발했습니다. [2503.22809v3]
2. <b>AgroXAI: Explainable AI-Driven Crop Recommendation System for Agriculture 4.0</b>: 이 시스템은 IoT, 머신러닝, 설명 가능한 인공지능(XAI)을 활용해 지역별 작물 추천과 생산성 향상을 목표로 합니다. [2412.16196v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.
````

---

## B10. 축구 전술 분석에 강화학습 쓴 논문 있어?

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 17.8s (단계: query 0.87s · search 0.82s · select 2.2s · judge 2.72s · answer 11.19s)
- 답 길이: 1402자
- 프롬프트 지문: `7ce48fa44272`
- 오류: 없음

**검색된 문서**

1. Optimizing Fantasy Sports Team Selection with Deep Reinforcement Learning [2412.19215]
2. Principled Analysis of Deep Reinforcement Learning Evaluation and Design Paradigms [2607.07769]
3. Agent-Temporal Credit Assignment for Optimal Policy Preservation in Sparse Multi-Agent Reinforcement Learning [2412.14779]
4. An Advantage-based Optimization Method for Reinforcement Learning in Large Action Space [2412.12605]
5. More Methods, Better Agents? A Reality Check on Self-Distillation in Agentic Reinforcement Learning [2610.19789]

**최종 답 (원문)**

````text
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
강화학습을 활용한 <b>축구 전술 분석</b>에 대한 구체적인 논문은 제공된 자료에서 찾을 수 없습니다.

<b>본론</b>
1. <b>Fantasy Cricket Team Selection with Deep Reinforcement Learning</b>: 이 연구는 강화학습(RL)을 이용해 팬타시 크리켓 팀 구성을 최적화하는 문제를 순차적 의사결정 문제로 모델링하고, 역사적 선수 데이터를 활용해 RL 알고리즘을 훈련시켜 미래 성능을 예측하고 팀 조합을 최적화합니다. [2412.19215v1]
2. <b>Temporal-Agent Reward Redistribution (TAR²)</b>: 다중 에이전트 환경에서 희소·지연된 보상을 시간 단계와 에이전트에 따라 재분배하는 TAR² 방법을 도입하여, 잠재 기반 보상 형성과 동등함을 이론적으로 증명하고 학습 안정성을 향상시킵니다. [2412.14779v1]
3. <b>Advantage Branching Dueling Q-network (ABQ)</b>: 큰 행동 공간에서 기존 가치 기반 RL의 한계를 극복하기 위해 각 차원의 독립적인 서브액션을 생성하고, 베이스라인 메커니즘을 이용해 액션 가치를 조정하는 ABQ 알고리즘을 제안합니다. [2412.12605v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다. 제공된 문서들은 각각 팬타시 크리켓 팀 최적화, 다중 에이전트 보상 재분배, 그리고 큰 행동 공간에서의 RL 알고리즘 개선에 초점을 맞추고 있습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• Boosting Studies of Multi-Agent Reinforcement Learning on Google Research Football Environment: The Past, Present, and Future (2024) https://doi.org/10.65109/dmin4153
• Expandable decision-making states for multi-agent deep reinforcement learning in soccer tactical analysis (2026) [2510.00480]
• Improving Sample Efficiency in Multi-Agent Reinforcement Learning for Simulated Football Games via Exploration (2026) [2503.13077]
• Maximising the Set-Piece Return: Optimising Football Corner Tactics with Graph Reinforcement Learning (2026) [2606.06353]
````

---

## B11. LLM 에이전트 도구 사용 관련 좋은 논문 세 편 추천해줘

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 17.8s (단계: query 0.55s · search 0.66s · select 2.88s · judge 3.0s · answer 10.67s)
- 답 길이: 1072자
- 프롬프트 지문: `c09669a26dbf`
- 오류: 없음

**검색된 문서**

1. A Survey on Large Language Model-based Agents for Statistics and Data Science [2412.14222]
2. Agentic Large Language Models, a survey [2503.23037]
3. FinMCP-Bench: Benchmarking LLM Agents for Real-World Financial Tool Use under the Model Context Protocol [2603.24943]
4. Evaluating LLM-based Agents for Multi-Turn Conversations: A Survey [2503.22458]
5. LoCoBench-Agent: An Interactive Benchmark for LLM Agents in Long-Context Software Engineering [2511.13998]

**최종 답 (원문)**

````text
<b>서론</b>
LLM 기반 에이전트가 실제 업무에서 <b>도구</b>를 호출·사용하는 능력은 복잡한 금융·소프트웨어 엔지니어링 등 다양한 도메인에서 핵심 과제이다. 도구 사용 정확도와 다중 도구 연동, 그리고 장기 컨텍스트에서의 안정성을 동시에 평가하려면 체계적인 벤치마크와 평가 지표가 필요하다.

<b>본론</b>
1. <b>FinMCP-Bench</b>: 65개의 실제 금융 MCP를 활용해 613개의 샘플을 포함한 새로운 벤치마크로, 단일·다중 도구 및 다중 턴 시나리오에서 모델의 도구 호출 정확도와 추론 능력을 측정한다. [2603.24943v1]
2. <b>LoCoBench-Agent</b>: 기존 LoCoBench의 8,000개 시나리오를 확장한 인터랙티브 평가 프레임워크로, 파일 조작·검색·코드 분석 등 8개의 전문 도구를 제공하고 10K~1M 토큰 범위의 장기 컨텍스트에서 에이전트의 도구 사용 효율성과 오류 복구 능력을 평가한다. [2511.13998v1]

<b>결론</b>
제공된 문서에서는 FinMCP-Bench와 LoCoBench-Agent가 각각 금융 및 소프트웨어 엔지니어링 분야에서 LLM 에이전트의 도구 사용 능력을 구체적으로 평가하는 벤치마크로 제시된다. 따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• AgentBench: Evaluating LLMs as Agents (2023) [2308.03688]
• From language to action: a review of large language models as autonomous agents and tool users (2026) [2508.17281]
• MetaTool Benchmark for Large Language Models: Deciding Whether to Use Tools and Which to Use (2023) [2310.03128]
• Agent-SafetyBench: Evaluating the Safety of LLM Agents (2024) [2412.14470]
````

---

## B12. 긴 문맥 처리 트랜스포머 개선 연구 두 편만

- 판정: 있음 — 문서 2
- 경로: `direct_answer/B`
- 시간: 25.2s (단계: router 1.7s · query 0.26s · search 0.82s · select 2.51s · judge 2.95s · answer 11.03s · rewrite 5.89s)
- 답 길이: 1057자
- 프롬프트 지문: `ef6cce823251`
- 오류: 없음

**검색된 문서**

1. Theoretical Constraints on the Expressive Power of $\mathsf{RoPE}$-based Tensor Attention Transformers [2412.18040]
2. Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers [2610.13735]
3. Morphing into Hybrid Attention Models [2606.30562]
4. LightTransfer: Your Long-Context LLM is Secretly a Hybrid Model with Effortless Adaptation [2410.13846]
5. How Well Can a Long Sequence Model Model Long Sequences? Comparing Architechtural Inductive Biases on Long-Context Abilities [2407.08112]

**최종 답 (원문)**

````text
<b>서론</b>
긴 문맥을 처리하는 트랜스포머는 <b>KV 캐시 비용</b>과 <b>정확도 유지</b>라는 두 가지 핵심 과제를 동시에 해결해야 합니다. 이러한 제약 때문에 기존 모델은 메모리 효율성과 성능 사이의 균형을 맞추기 어렵습니다.

<b>본론</b>
1. <b>Orthros</b>: Phase‑aware heterogeneous attention을 도입해 시퀀스 처리의 서로 다른 단계마다 계산 패턴을 동적으로 전환함으로써, 프리필링과 디코딩 모두에서 선형 복잡도를 달성하고 21.9배의 속도 향상을 이룹니다. [2610.13735v1]
2. <b>FlashMorph</b>: 각 풀‑어텐션 레이어에 변환된 선형‑어텐션 가지를 추가한 형태 가능한 모델을 구축한 뒤, 전체 가중치를 고정하고 합성 긴 문맥 검색 데이터에서 레이어별 게이트를 공동 최적화하여 예산 제약 하에 하이브리드 구조를 생성합니다. [2606.30562v1]
3. <b>LightTransfer</b>: 최근 또는 초기 토큰에 집중하는 “지연 레이어”를 식별해 이를 스트리밍 어텐션으로 교체함으로써, 별도의 학습 없이도 긴 문맥 이해와 o1‑형 추론 작업에서 2.17배의 처리량 향상을 달성합니다. [2410.13846v2]

<b>결론</b>
Orthros는 기존 트랜스포머 대비 21.9배의 프리필링 속도 향상을 달성하면서도 긴 컨텍스트 능력을 유지한 반면, LightTransfer는 하이브리드 모델 전환 시 최대 2.17배의 처리량 개선을 보이며 성능 손실을 최소화한다[2610.13735v1][2410.13846v2]. 두 연구 모두 트랜스포머 기반 모델을 효율적으로 개선하는 데 초점을 맞추고 있으나, Orthros는 엔드투엔드 추론에서의 속도 향상과 긴 컨텍스트 정확도 강조를, LightTransfer는 레이어 선택 비용 감소와 처리량 증가에 중점을 둔 결과를 제시한다[2610.13735v1][2410.13846v2]. 따라서 두 논문은 각각 다른 효율성 지표(속도 vs 처리량)와 조건에서 트랜스포머의 성능을 향상시킨다는 공통된 결론을 내리지만, 구체적인 개선 수치와 평가 기준이 다르다.
````

---

## B13. 코드 생성 LLM 논문 딱 하나만 골라줘

- 판정: 있음 — 문서 1
- 경로: `direct_answer/B`
- 시간: 13.3s (단계: query 1.78s · search 0.78s · judge 1.27s · answer 9.44s)
- 답 길이: 661자
- 프롬프트 지문: `bc8a6206f2bd`
- 오류: 없음

**검색된 문서**

1. Beyond Pass Rate: A Multilingual, Execution-Grounded Evaluation of Open Code LLMs [2606.08840]

**최종 답 (원문)**

````text
<b>서론</b>
코드 생성 LLM을 평가할 때 <b>단일 언어·단일 지표</b>에 의존하면 성능 차이가 숨겨질 수 있어, 다국어·실행 기반의 종합적 측정이 필요합니다.

<b>본론</b>
1. <b>Beyond Pass Rate</b>: 9개의 오픈 코드 전용 LLM을 2,707개의 LeetCode 문제와 12개 프로그래밍 언어에 대해 실행 기반 평가하고, 325,343개의 작업과 정적 분석 신호를 포함한 대규모 데이터셋을 구축했습니다. [2606.08840v1] Yi‑Coder‑9B‑Chat이 평균 정확도 23.64%로 인간 수용 기준(57.2%)에 크게 미치지 못하며, Qwen2.5‑Coder‑14B‑Instruct은 어려운 문제와 다양한 문제 커버리지에서 강점을 보였고, Gemma‑2‑27B‑IT는 모든 언어의 린트 통과율에서 최고를 기록했습니다. [2606.08840v1] 컴파일 오류가 비수용 제출의 63.25%를 차지해 많은 실패가 의미적 정확도 테스트 전에 발생하고, 정적 품질과 기능적 정확도는 크게 달라진다는 점을 확인했습니다. [2606.08840v1]
<b>결론</b>
제공된 문서에 따르면, <b>Beyond Pass Rate</b>는 다국어·실행 기반 평가와 정적 분석을 통해 기존 단일 지표 리더보드가 가려던 성능 차이와 실패 원인을 드러냅니다.
````

---

## B14. GraphRAG랑 벡터 RAG는 multi-hop 질문에서 성능이 어떻게 갈려?

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 16.9s (단계: router 2.38s · query 0.93s · search 0.73s · select 2.84s · judge 3.0s · answer 7.03s)
- 답 길이: 809자
- 프롬프트 지문: `aa0b4642ca45`
- 오류: 없음

**검색된 문서**

1. HyperGraphRAG: Retrieval-Augmented Generation via Hypergraph-Structured Knowledge Representation [2503.21322]
2. Is GraphRAG Needed? From Basic RAG to Graph-/Agentic Solutions with Context Optimization [2606.25656]
3. UnWeaving the knots of GraphRAG -- turns out VectorRAG is almost enough [2603.29875]
4. Think Parallax: Solving Multi-Hop Problems via Multi-View Knowledge-Graph-Based Retrieval-Augmented Generation [2510.15552]
5. RAG vs. GraphRAG: A Systematic Evaluation and Key Insights [2502.11371]

**최종 답 (원문)**

````text
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>HyperGraphRAG</b>: 초록에서 HyperGraphRAG는 n‑ary 관계를 나타내기 위해 하이퍼에지를 사용하고, 기존 그래프 기반 RAG가 이진 관계만 다루는 한계를 극복한다[2503.21322v3].
2. <b>UnWeaver</b>: UnWeaver는 문서 내용을 엔티티로 분해하고, 엔티티를 중간 단계로 활용해 원본 텍스트 청크를 복구함으로써 그래프 기반 RAG의 복잡성과 휴리스틱 의존성을 완화한다[2603.29875v2].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• Retrieval-Augmented Generation with Graphs (GraphRAG) (2024) [2501.00309]
• When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation (2025) [2506.05690]
• GFM-RAG: Graph Foundation Model for Retrieval Augmented Generation (2025) [2502.01113]
• GraphRAG-Bench: Challenging Domain-Specific Reasoning for Evaluating Graph Retrieval-Augmented Generation (2025) [2506.02404]
````

---

## B15. ESG 온톨로지 기반 지식 그래프 연구 설명해줘

- 판정: 있음 — 문서 2
- 경로: `direct_answer/B`
- 시간: 18.1s (단계: query 1.89s · search 0.82s · select 2.91s · judge 2.91s · answer 9.56s)
- 답 길이: 746자
- 프롬프트 지문: `abc4c0390f71`
- 오류: 없음

**검색된 문서**

1. Accelerating Knowledge Graph and Ontology Engineering with Large Language Models [2411.09601]
2. OntoMetric: An Ontology-Driven LLM-Assisted Framework for Automated ESG Metric Knowledge Graph Generation [2512.01289]
3. LLM-Driven Ontology Construction for Enterprise Knowledge Graphs [2602.01276]
4. Ontology-grounded Automatic Knowledge Graph Construction by LLM under Wikidata schema [2412.20942]
5. Knowledge Graphs Generation from Cultural Heritage Texts: Combining LLMs and Ontological Engineering for Scholarly Debates [2511.10354]

**최종 답 (원문)**

````text
<b>서론</b>
ESG(환경·사회·지배구조) 지표는 규제 문서에 명시된 구조화된 지식이지만, 이를 자동으로 추출하고 온톨로지로 정형화하는 과정은 복잡하고 비용이 많이 듭니다. 특히 규제 문서를 기반으로 한 대규모 데이터에서 의미적 정확도와 스키마 준수를 동시에 확보하는 것이 어려운 과제입니다.

<b>본론</b>
1. <b>OntoMetric</b>: ESG 메트릭 지식 그래프를 자동으로 생성·관리하기 위해 규제 문서에 내재된 구조를 온톨로지로 변환하고, 온톨로지‑가이드 LLM 추출과 두 단계 검증(semantic type verification + rule‑based schema checking)을 결합한 프레임워크를 제안합니다. [2512.01289v2] <b>OntoMetric</b> (성능 평가): 다섯 가지 ESG 규제 표준에 대해 적용한 결과, 온톨로지‑가이드 추출은 의미적 정확도 65‑90 %와 스키마 준수율 80 % 이상을 달성했으며, 비용 효율성은 0.01‑0.02 USD/개체로 안정적이고, 기존 기반 대비 48배의 효율성 향상을 보였습니다. [2512.01289v2]
<b>결론</b>
OntoMetric은 ESG 온톨로지를 핵심 제약으로 삼아 규제 문서에서 자동으로 지식 그래프를 구축하고 검증하는 프레임워크이며, 높은 의미적 정확도와 스키마 준수율을 유지하면서 비용과 효율성을 크게 개선합니다. 이는 ESG 메트릭의 구조화된 지식을 기계가 활용 가능한 형태로 전환하는 실용적인 해결책을 제공합니다.
````

---

## B16. 하이퍼그래프로 n-ary 관계 표현하는 RAG 연구 알려줘

- 판정: 있음 — 문서 1
- 경로: `direct_answer/B`
- 시간: 12.2s (단계: query 0.93s · search 0.94s · select 2.29s · judge 1.28s · answer 6.73s)
- 답 길이: 501자
- 프롬프트 지문: `cddffedccf90`
- 오류: 없음

**검색된 문서**

1. HyperGraphRAG: Retrieval-Augmented Generation via Hypergraph-Structured Knowledge Representation [2503.21322]

**최종 답 (원문)**

````text
<b>서론</b>
기존 <b>RAG</b>는 텍스트 조각 기반 검색에 의존하고, 그래프 기반 접근은 이진 관계만 표현할 수 있어 현실 지식에서 나타나는 <b>n-ary 관계</b>(n ≥ 2)를 제대로 모델링하기 어렵습니다. 이러한 한계를 극복하려면 다중 엔티티를 연결하는 고차원 구조가 필요합니다.

<b>본론</b>
1. <b>HyperGraphRAG</b>: 하이퍼그래프를 이용해 n‑ary 관계를 하이퍼에지로 표현하며, 지식 하이퍼그래프 구축·검색·생성 파이프라인을 제공합니다. 기존 그래프 기반 RAG와 표준 RAG보다 정답 정확도, 검색 효율성, 생성 품질에서 모두 우수합니다. [2503.21322v3]

<b>결론</b>
HyperGraphRAG는 하이퍼에지를 통한 n‑ary 관계 표현으로 기존 이진 관계만 다루던 그래프 기반 RAG의 한계를 극복하고, 다중 도메인 실험에서 정답 정확도·검색 효율성·생성 품질 모두에서 표준 RAG와 이전 그래프 기반 방법을 능가함을 보여줍니다.
````

---

## B17. 엔티티 추출과 세그먼트 분할을 같이 다룬 연구 있어?

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 15.1s (단계: router 1.8s · query 0.28s · search 0.72s · select 2.26s · judge 2.69s · answer 7.37s)
- 답 길이: 782자
- 프롬프트 지문: `79be69c40a71`
- 오류: 없음

**검색된 문서**

1. Retrieval-Augmented Generation-based Relation Extraction [2404.13397]
2. Semi-Supervised Learning from Small Annotated Data and Large Unlabeled Data for Fine-grained PICO Entity Recognition [2412.19346]
3. Can AI Extract Antecedent Factors of Human Trust in AI? An Application of Information Extraction for Scientific Literature in Behavioural and Computer Sciences [2412.11344]
4. A Comparative Analysis of Word Segmentation, Part-of-Speech Tagging, and Named Entity Recognition for Historical Chinese Sources, 1900-1950 [2503.19844]
5. Enhancing Retrieval Augmented Generation with Hierarchical Text Segmentation Chunking [2507.09935]

**최종 답 (원문)**

````text
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>Retrieval-Augmented Generation-based Relation Extraction</b>: 이 연구는 정보 추출(IE) 과정에서 엔티티와 관계 추출(RE)을 결합하고, LLM 기반 RAG4RE를 제안하여 레이블 데이터와 컴퓨팅 자원 의존도를 낮추고 성능을 향상시킨다. [2404.13397v2]
2. <b>Hierarchical Text Segmentation Chunking</b>: 이 연구는 RAG 시스템에 계층적 텍스트 분할과 클러스터링을 통합해 의미적으로 일관된 청크를 생성하고, 세그먼트·클러스터 수준의 벡터 표현을 활용해 더 정확한 정보를 검색한다. [2507.09935v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• Joint entity recognition and relation extraction as a multi-head selection problem (2018) [1804.07847]
• Joint Learning with Pre-trained Transformer on Named Entity Recognition and Relation Extraction Tasks for Clinical Analytics (2020) https://doi.org/10.18653/v1/2020.clinicalnlp-1.26
````

---

## B18. 시공간(spatiotemporal) 데이터에 LLM 쓴 연구 있어?

- 판정: 있음 — 문서 1
- 경로: `direct_answer/B`
- 시간: 24.2s (단계: router 3.13s · query 1.48s · search 0.78s · select 2.48s · judge 2.59s · answer 9.64s · rewrite 4.11s)
- 답 길이: 1007자
- 프롬프트 지문: `f6abf2d7757d`
- 오류: 없음

**검색된 문서**

1. Embracing Large Language Models in Traffic Flow Forecasting [2412.12201]
2. Understanding Data Temporality Impact on Large Language Models Pre-training [2605.22769]
3. Geode: A Zero-shot Geospatial Question-Answering Agent with Explicit Reasoning and Precise Spatio-Temporal Retrieval [2407.11014]
4. A Time Series Multitask Framework Integrating a Large Language Model, Pre-Trained Time Series Model, and Knowledge Graph [2503.07682]

**최종 답 (원문)**

````text
<b>서론</b>
시공간 데이터를 활용한 교통 흐름 예측은 역사적 교통 상황과 도로 네트워크 정보를 기반으로 미래 흐름을 추정해야 하므로, 공간·시간 의존성을 정확히 포착하고 환경 변화에 유연하게 대응하는 것이 핵심 과제이다. 이러한 복잡성을 해결하기 위해 최근 연구에서는 <b>대형 언어 모델(LLM)</b>을 도입하여 기존 방법의 한계를 보완하려는 시도가 이루어지고 있다.

<b>본론</b>
1. <b>Large Language Model Enhanced Traffic Flow Predictor (LEAF)</b>: 그래프와 하이퍼그래프 구조를 각각 사용하는 두 가지 브랜치를 설계하고, 각 브랜치를 사전 학습한 후 테스트 시간에 서로 다른 예측을 생성한다. 이후 LLM을 활용해 가장 그럴듯한 결과를 선택하며, 두 브랜치의 예측 능력을 향상시키기 위해 랭킹 손실을 학습 목표로 적용한다. [2412.12201v2] 시공간 대규모 언어 모델을 제안하여 교통 흐름 예측에 적용한다. [2412.12201v2]
2. <b>Geode</b>: 제로샷 지리 공간 질문‑응답 작업을 위해 명시적 추론과 정밀한 시공간 데이터 검색을 결합한 시스템을 소개한다. 기존 LLM이 지리 공간 데이터를 실시간으로 검색하지 못해 정확도가 낮았던 문제를 해결한다. [2407.11014v1]

<b>결론</b>
제공된 문서에 따르면, 시공간 데이터를 활용한 LLM 연구는 존재합니다. [2412.12201v2]은 교통 흐름 예측 분야에서 제안된 LEAF 모델이 여러 데이터셋에서 효과적임을 보여줍니다. 또한 [2407.11014v1]은 기존 사전 학습된 LLM이 정밀한 시공간 데이터 검색 능력이 부족해 지리 공간 질의에 정확도가 낮다고 지적하고, 이를 해결하기 위해 Geode 시스템을 도입하여 이러한 한계를 극복했다고 보고합니다. 따라서 두 연구 모두 시공간 데이터를 대상으로 LLM을 적용하거나 개선하는 작업을 수행했으나, 각각 교통 흐름 예측과 지리 공간 질의라는 서로 다른 도메인과 목적을 가지고 있습니다.
````

---

## B19. 파인튜닝 vs RAG 비교해줘

- 판정: 건너뜀(게이트: cmp)
- 경로: `direct_answer/B`
- 시간: 40.2s (단계: router 2.01s · query 0.47s · search 25.67s · select 3.1s · answer 8.95s)
- 답 길이: 549자
- 프롬프트 지문: `69602c736d50`
- 오류: 없음

**검색된 문서**

1. A Systematic Evaluation of LLM Strategies for Mental Health Text Analysis: Fine-tuning vs. Prompt Engineering vs. RAG [2503.24307]
2. A Comparison of Independent and Joint Fine-tuning Strategies for Retrieval-Augmented Generation [2510.01600]
3. RbFT: Robust Fine-tuning for Retrieval-Augmented Generation against Retrieval Defects [2501.18365]
4. RankRAG: Unifying Context Ranking with Retrieval-Augmented Generation in LLMs [2407.02485]
5. Establishing Performance Baselines in Fine-Tuning, Retrieval-Augmented Generation and Soft-Prompting for Non-Specialist LLM Users [2311.05903]

**최종 답 (원문)**

````text
<b>서론</b>
파인튜닝과 RAG는 각각 모델 자체를 학습시키고 외부 지식베이스를 활용해 답변을 생성하는 두 가지 접근법으로, 정확도와 자원 요구량 사이의 트레이드오프가 존재합니다. 이러한 차이가 정신 건강 텍스트 분석 같은 전문 분야에서 어떤 전략이 적합한지 판단하기 어렵습니다.

<b>본론</b>
1. <b>Fine-tuning</b>: 파인튜닝은 감정 분류와 정신 건강 상태 감지 작업에서 91%와 80%의 높은 정확도를 달성하지만, 대규모 학습 데이터와 상당한 컴퓨팅 자원이 필요합니다. [2503.24307v1] RAG는 외부 지식베이스를 활용해 답변을 생성하는 방식으로, 파인튜닝보다 낮은 정확도(40‑68%)를 보이지만 배포 유연성이 높습니다. [2503.24307v1]
<b>결론</b>
파인튜닝은 높은 정확도를 제공하지만 자원 요구량이 크고, RAG는 상대적으로 낮은 정확도에도 불구하고 유연한 배포가 가능합니다. 따라서 정신 건강 텍스트 분석과 같은 응용에서는 정확도와 비용·배포 요구사항을 고려해 두 방법을 상황에 맞게 선택하거나 결합하는 것이 바람직합니다.
````

---

## B20. 다국어 LLM 연구 조사해줘

- 판정: 있음 — 문서 1
- 경로: `direct_answer/B`
- 시간: 25.0s (단계: router 1.87s · query 0.56s · search 0.73s · select 2.94s · judge 2.45s · answer 10.1s · rewrite 6.36s)
- 답 길이: 1149자
- 프롬프트 지문: `469b3cc6d10f`
- 오류: 없음

**검색된 문서**

1. MERaLiON-TextLLM: Cross-Lingual Understanding of Large Language Models in Chinese, Indonesian, Malay, and Singlish [2501.08335]
2. The Roles of English in Evaluating Multilingual Language Models [2412.08392]
3. Beyond Data Quantity: Key Factors Driving Performance in Multilingual Language Models [2412.12500]
4. Overview of the First Workshop on Language Models for Low-Resource Languages (LoResLM 2025) [2412.16365]
5. On the Applicability of Zero-Shot Cross-Lingual Transfer Learning for Sentiment Classification in Distant Language Pairs [2412.18188]

**최종 답 (원문)**

````text
<b>서론</b>
다국어 대형 언어 모델(LLM)은 다양한 언어를 동시에 이해·생성해야 하므로, 언어별 자원 차이와 문화적 맥락 때문에 성능 격차가 발생하기 쉽습니다. 이러한 격차를 줄이기 위해 최근 연구들은 특정 언어에 특화된 모델을 개발하거나 평가 방식을 개선하고 있습니다.

<b>본론</b>
1. <b>MERaLiON-TextLLM</b>: 중국어, 인도네시아어, 말레이어, 신글리시를 대상으로 이해·생성 성능을 향상시키기 위해 Llama‑3‑8B‑Base를 기반으로 계속 사전학습과 가중치 병합을 적용한 오픈소스 모델을 제공합니다. [2501.08335v3]
2. <b>English as Interface in Multilingual Evaluation</b>: 다국어 모델 평가에서 영어를 인터페이스로 활용해 작업 수행 능력을 높이는 방식을 제시하고, 이는 언어 이해보다는 과제 성능에 초점을 맞춥니다. [2412.08392v1]
3. <b>Key Factors Beyond Data Quantity</b>: 토큰 유사성과 국가 유사성 등 데이터 양 외에도 언어·문화적 맥락이 모델 성능에 중요한 영향을 미친다는 점을 SIB‑200과 Flores‑200 데이터셋을 통해 규명했습니다. [2412.12500v1]

<b>결론</b>
제공된 문서들은 다국어 LLM 연구에서 모델 성능과 언어 간 이해 능력에 영향을 미치는 핵심 요인들을 각각 강조하고 있습니다. 먼저, MERaLiON-TextLLM은 중국어, 인도네시아어, 말레이어, 신글리시 등 특정 언어들에 대해 벤치마크에서 공식 Llama-3 모델을 능가하는 성능 향상을 달성했습니다[2501.08335v3]. 두 번째 연구는 영어를 사용하지 않으면 시스템이 제대로 작동하지 않을 수 있음을 지적하며, 다국어 모델 평가에서 영어의 역할을 강조합니다[2412.08392v1]. 세 번째 논문은 사전 학습 데이터 비율과 모델 크기 외에도 토큰 유사성과 국가 유사성이 성능에 중요한 영향을 미친다고 밝히며, 다양한 언어 특성과 자원 가용성을 고려한 공정한 성능 달성은 여전히 어려운 과제임을 언급합니다[2412.12500v1]. 이러한 결과들은 다국어 LLM의 성능 향상이 특정 언어 대상 최적화, 영어 의존성 평가, 그리고 데이터·모델 규모·유사성 등 복합적 요인에 의해 결정됨을 보여줍니다.
````

---

## B21. LLM-as-a-judge의 편향 종류를 연구별로 비교해줘

- 판정: 건너뜀(게이트: cmp)
- 경로: `direct_answer/B`
- 시간: 31.5s (단계: router 2.1s · query 0.73s · search 7.11s · select 3.09s · answer 14.41s · rewrite 4.06s)
- 답 길이: 1067자
- 프롬프트 지문: `f4793a2ce595`
- 오류: 없음

**검색된 문서**

1. Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge [2410.02736]
2. Evaluating Scoring Bias in LLM-as-a-Judge [2506.22316]
3. A Survey on LLM-as-a-Judge [2411.15594]
4. Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias [2606.19544]
5. How Much Do LLM-as-a-Judge Design Choices Matter? A Systematic Comparison of Prompt Designs, Rating Scales, and Models [2610.05094]

**최종 답 (원문)**

````text
<b>서론</b>
LLM-as-a-Judge는 대규모 언어 모델을 평가 도구로 활용하는 방법이지만, <b>편향</b>에 의해 판단이 왜곡될 위험이 존재합니다. 이러한 편향을 정확히 파악하고 분류하는 것은 신뢰성 있는 자동 평가를 구축하기 위해 필수적인 과제입니다.

<b>본론</b>
1. <b>CALM</b>: 12개의 핵심 잠재적 편향을 식별하고, 자동화된 원칙 기반 수정을 통해 각 유형의 편향을 체계적으로 정량화·분석합니다. [2410.02736v2]
2. <b>Scoring Bias Framework</b>: 기존 비교 평가 중심 연구와 달리 절대 점수 부여 방식의 편향에 초점을 맞추어 rubric order bias, score ID bias, reference answer score bias라는 세 가지 새로운 편향 유형을 정의하고 정량화 프레임워크를 제안합니다. [2506.22316v4]
3. <b>Bias Taxonomy</b>: LLM-as-a-Judge 시스템에서 발생하는 편향을 두 가지 큰 범주로 분류합니다: (1) task‑agnostic biases(모델 전반에 공통된 편향), (2) judgment‑specific biases(평가 시나리오에 고유한 편향). [2411.15594v6]
4. <b>Bias Types from Survey</b>: 위치 편향(position bias), 길이에 따른 편향(length bias), 자기 선호 편향(self‑preference bias) 등 기존 연구에서 보고된 여러 편향 유형을 나열합니다. [2610.05094v1]

<b>결론</b>
LLM-as-a-Judge의 편향은 모델 성능이 높아졌음에도 특정 작업에서 여전히 존재한다는 공통된 결과가 보고된다[2410.02736v2][2506.22316v4]. 또한, 평가 설계와 프롬프트 선택에 따라 측정되는 편향 크기가 크게 달라질 수 있으며, 이는 모델과 데이터 조건에 따라 편향이 변동함을 보여준다[2610.05094v1]. 따라서 LLM-as-a-Judge의 편향은 연구마다 동일한 현상을 확인하지만, 그 정도와 영향은 평가 방법과 설계 선택에 따라 다르게 나타난다.
````

---

## B22. DynaFlow랑 OmniNova 성능 수치 비교해줘

- 판정: 판정 단계 없음
- 경로: `planner/C` — 라우터가 계획(planner) 경로로 보냄. 이 재생 스크립트는 RAG 경로만 돌려 답이 비어 있다. 텔레그램에서는 계획 경로 답이 나간다(재생 안 됨)
- 시간: 2.5s (단계: router 2.51s)
- 답 길이: 0자
- 프롬프트 지문: `(답 LLM 호출 없음)`
- 오류: 없음

**검색된 문서**

(없음)

**최종 답 (원문)**

````text

````

---

## B23. RAG 평가 프레임워크 세 개를 장단점과 함께 비교해줘

- 판정: 건너뜀(게이트: cmp)
- 경로: `direct_answer/B`
- 시간: 213.1s (단계: router 1.7s · query 0.38s · search 188.2s · select 2.9s · answer 13.19s · rewrite 6.74s)
- 답 길이: 1243자
- 프롬프트 지문: `8538c5860b90`
- 오류: 없음

**검색된 문서**

1. A System for Comprehensive Assessment of RAG Frameworks [2504.07803]
2. Methodological Framework for Quantifying Semantic Test Coverage in RAG Systems [2510.00001]
3. RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation [2408.08067]
4. OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools [2508.05650]
5. RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems [2412.12322]

**최종 답 (원문)**

````text
<b>서론</b>
RAG(검색 증강 생성) 시스템은 외부 지식과 LLM을 결합해 사실 정확성과 맥락 관련성을 높이지만, <b>평가 프레임워크</b>가 부족해 실제 배포 환경에서 성능을 종합적으로 측정하기 어렵습니다. 특히 기존 도구들은 블랙박스 평가나 다중 도메인 지원이 제한적입니다.

<b>본론</b>
1. <b>SCARF</b>: 모듈화되고 유연한 평가 프레임워크로, 다양한 RAG 구성과 벡터 데이터베이스·LLM 서빙 전략에 대한 자동화된 테스트와 상세 성능 보고서를 제공합니다. REST API를 통해 실제 시나리오에서 적용 가능하며, 응답 일관성 등 실용적 고려사항을 통합합니다. [2504.07803v1]
2. <b>RAGChecker</b>: 검색 및 생성 모듈 모두에 대한 정밀 진단 메트릭을 포함하는 평가 프레임워크로, 인간 판단과 높은 상관관계를 보이며 8개의 RAG 시스템을 분석해 설계 선택의 패턴과 트레이드오프를 드러냅니다. [2408.08067v2]
3. <b>OmniBench‑RAG</b>: 다중 도메인 평가를 위한 자동화된 플랫폼으로, 정확도와 효율성 차원에서 성능 향상을 정량화하고 문화·지리·건강 등 9개 지식 분야를 포괄합니다. 표준화된 메트릭(Improvements, Transformation)과 동적 테스트 생성, 모듈 파이프라인을 제공해 재현 가능한 비교를 가능하게 합니다. [2508.05650v1]

<b>결론</b>
SCARF은 다양한 RAG 프레임워크를 비교하기 위해 모듈화되고 유연한 평가 방법론을 제공하며, REST API 인터페이스를 통해 실제 시나리오에서 적용 가능성을 보여준다[2504.07803v1]. RAGChecker는 검색 및 생성 모듈에 대한 정교한 진단 메트릭을 포함하고 있어 인간 판단과의 상관관계가 다른 지표보다 현저히 높음을 확인했으며, 8개의 RAG 시스템을 평가하여 설계 선택의 패턴과 트레이드오프를 분석했다[2408.08067v2]. OmniBench-RAG는 다중 도메인 평가를 지원하지만 현재 접근법에는 자동화된 다중 도메인 평가 기능이 부족하고 비결정성 구성 요소에 의존한다는 근본적인 한계가 있음을 드러냈다[2508.05650v1]. 따라서 세 프레임워크 모두 RAG 평가의 다양한 측면을 다루지만, SCARF은 유연성과 실용성에 강점이 있고, RAGChecker는 정밀한 진단과 인간 판단과의 높은 일관성을 제공하며, OmniBench-RAG는 도메인별 성능 변동성을 강조하지만 자동화된 다중 도메인 평가 능력에서 제한을 가진다.
````

---

## B24. 요즘 핫한 에이전트 논문 머있어

- 판정: 없음
- 경로: `direct_answer/B`
- 시간: 16.7s (단계: query 0.66s · search 0.71s · select 2.57s · judge 2.41s · answer 10.38s)
- 답 길이: 1119자
- 프롬프트 지문: `bd9cd31b3fbd`
- 오류: 없음

**검색된 문서**

1. Into the Unknown: Benchmarking AI agents on open scientific research problems [2610.19159]
2. NatureBench: Can Coding Agents Match the Published SOTA of Nature-Family Papers? [2606.24530]
3. CASCADE: Cumulative Agentic Skill Creation through Autonomous Development and Evolution [2512.23880]
4. The Age of AI Agents Demands A New Scientific Paradigm To Sustain Trustworthy Science [2607.26064]
5. Agentic Large Language Models, a survey [2503.23037]

**최종 답 (원문)**

````text
<b>서론</b>
최근 <b>AI 에이전트</b>가 과학 연구 문제를 직접 수행하고 논문을 작성하는 것이 주요 관심사로 부상하고 있다. 이러한 작업은 기존 모델이 단순 재현에 머무르는 한계를 넘어, 실제 과학적 발견을 요구하기 때문에 매우 어려운 과제이다.

<b>본론</b>
1. <b>Into the Unknown</b>: AI 에이전트가 과학 논문을 읽고 연구 방향을 따라 후속 논문을 작성하도록 하는 벤치마크이며, DOE 국립연구소의 전문가들이 제시한 조건에 기반한 평가 rubric을 제공한다. [2610.19159v1]
2. <b>NatureBench</b>: Nature 계열 논문에서 추출한 90개의 교차학문 과제를 포함하는 벤치마크로, AI 코딩 에이전트가 실제 과학 문제를 재현·발견할 수 있는지 평가한다. [2606.24530v2]
3. <b>CASCADE</b>: 자율 실험과 선택적 논문의 재발행, 인간‑에이전트 협업 및 기억 통합을 통해 실행 가능한 기술을 축적하고 공유함으로써 확장 가능한 AI 보조 과학 연구를 목표로 한다. [2512.23880v2]

<b>결론</b>
제공된 문서들은 Into the Unknown, NatureBench, CASCADE와 같은 최신 에이전트 연구들을 제시한다. 이러한 벤치마크와 시스템은 AI 에이전트가 과학 문제를 직접 수행하도록 설계되었으나, 현재까지도 전문가 수준의 완성도를 달성하지 못하고 있다. 따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• AI Agents That Matter (2024) [2407.01502]
• Agentic Search Spaces for Tabular Machine Learning (2026) [2609.16309]
• SELA: Tree-Search Enhanced LLM Agents for Automated Machine Learning (2024) [2410.17238]
• Multi-Agent AI Framework for Threat Mitigation and Resilience in Machine Learning Systems (2026) [2512.23132]
````

---

## B25. llm 할루시네이숀 줄이는 법 논문

- 판정: 있음 — 문서 4
- 경로: `direct_answer/B`
- 시간: 25.9s (단계: query 1.56s · search 0.6s · select 2.83s · judge 2.92s · answer 12.71s · rewrite 5.29s)
- 답 길이: 1270자
- 프롬프트 지문: `e93dead6e12a`
- 오류: 없음

**검색된 문서**

1. Chainpoll: A high efficacy method for LLM hallucination detection [2310.18344]
2. HalluMat: Detecting Hallucinations in LLM-Generated Materials Science Content Through Multi-Stage Verification [2512.22396]
3. RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models [2401.00396]
4. GraphEval: A Knowledge-Graph Based LLM Hallucination Evaluation Framework [2407.10793]
5. FactSelfCheck: Fact-Level Black-Box Hallucination Detection for LLMs [2503.17229]

**최종 답 (원문)**

````text
<b>서론</b>
LLM이 생성한 응답에서 <b>할루시네이션</b>(거짓 또는 근거 없는 주장)은 연구와 실제 응용에 심각한 신뢰성 문제를 초래합니다. 이러한 오류를 자동으로 탐지하고 수정하는 방법은 모델의 내부 동작을 이해해야 하므로 매우 어려운 과제입니다.

<b>본론</b>
1. <b>ChainPoll</b>: 기존 평가 데이터가 도전성·현실성·작업 다양성 측면에서 부족함을 지적하고, 이를 보완한 RealHall 벤치마크를 구축하여 ChainPoll이 모든 벤치마크에서 AUROC 0.781로 최고의 성능을 보임을 제시합니다. 또한 Adherence와 Correctness라는 두 가지 새로운 메트릭을 도입해 분석 능력과 논리적 오류를 평가합니다. [2310.18344v1]
2. <b>HalluMatDetector</b>: 다단계 검증 파이프라인(인트린식 평가, 멀티소스 검색, 모순 그래프 분석, 메트릭 기반 평가)으로 구성되며, 이를 통해 재료과학 분야 LLM 응답의 할루시네이션률을 기존 대비 30% 감소시켰습니다. [2512.22396v1]
3. <b>GraphEval</b>: 지식 그래프(KG) 구조를 활용해 응답 내 특정 삼중항을 식별하고, NLI 모델과 결합해 다양한 벤치마크에서 균형 정확도를 향상시키며, GraphCorrect라는 KG 기반 수정 메커니즘으로 대부분의 할루시네이션을 교정합니다. [2407.10793v1]
4. <b>FactSelfCheck</b>: 외부 자원이나 학습 데이터 없이 텍스트를 사실 삼중항으로 표현한 해석 가능한 지식 그래프를 이용해 정교한 사실 수준 할루시네이션 점수를 계산하며, 기존 문장 수준의 SelfCheckGPT 대비 35.5%의 사실 내용 증가를 달성했습니다. [2503.17229v3]

<b>결론</b>
ChainPoll은 기존 방법 대비 11% 향상되고 산업 표준을 23% 초과하며 비용 효율성과 투명성을 제공한다[2310.18344v1]. HalluMat은 재료 과학 도메인에서 엔트로피가 높은 쿼리에 대해 사실 일관성이 크게 달라지며, 검증 파이프라인을 통해 할루시네이션 발생률을 30% 감소시킨다[2512.22396v1]. FactSelfCheck는 사실 수준의 검출 접근법으로 기존 샘플링 기반 방법과 경쟁하며, 사실 내용을 35.5% 증가시키는 효과를 보인 반면 문장 수준의 SelfCheckGPT는 10.6%만 개선한다[2503.17229v3]. 따라서 할루시네이션 감소를 위한 방법은 도메인과 데이터 유형에 따라 효과가 크게 달라지며, 특히 사실 수준 검출이 높은 성능을 보인다.
````
