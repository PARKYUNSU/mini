# 답 단계 라벨 묶음 (README §6)

표본 10(근거 대조): C01 C02E HU27 MS2 MU1 N08 NM1 NM1E NM3E T01E

## NM1 · NM
- 질문: 
- 요소: ['Self-RAG 가 무엇인지', '핵심 방법(검색 여부 판단 · 반성 토큰)']
- 컨텍스트: 2310.11511 Self-RAG: Learning to Retrieve, Generate, and Critique throu
- 답:

서론
대규모 언어 모델(LLM)은 파라메트릭 지식에만 의존해 사실 오류가 발생하기 쉽습니다. 이러한 문제를 완화하려면 관련 지식을 검색하고 생성 과정을 스스로 평가하는 메커니즘이 필요합니다.

본론
1. Self-Reflective Retrieval-Augmented Generation (SELF-RAG): LLM의 품질과 사실을 향상시키기 위해 검색 및 자기반영을 결합한 새로운 프레임워크입니다[2310.11511v1]. 단일 임의 모델에 대해 필요 시에만 관련 문서를 적응적으로 가져옵니다[2310.11511v1].
결론
SELF-RAG은 LLM이 필요한 경우에만 관련 지식을 검색하고, 특수 토큰을 이용해 생성된 내용을 스스로 평가함으로써 기존 RAG 방식보다 사실 정확도와 응답 품질에서 큰 향상을 이룹니다.

- 인용 블록(근거 대조용):

  > [문서 1] [Distance: 0.3007] [발행일: 2023-10-17] [2310.11511v1] Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection [초록] Despite their remarkable capabilities, large language models (LLMs) often produce responses containing factual inaccuracies due to their sole reliance on the parametric knowledge they encapsulate. Retrieval-Augmented Generation (RAG), an ad hoc approach that augments LMs with retrieval of relevant knowledge, decreases such issues. However, indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility or can lead to unhelpful response generation. We introduce a new framework called Self-Reflective Retrieval-Augmented Generation (Self-RAG) that enhances an LM's quality and factuality through retrieval and self-reflection. Our framework trains a single arbitrary LM that adaptively retrieves passages on-demand, and generates and reflects on retrieved passages and its own generations using special tokens, called reflection tokens. Generating reflection tokens makes the LM controllable during the inference phase, enabling it to tailor its behavior to diverse task requirements. Experiments show that Self-RAG (7B and 13B parameters) significantly outperforms state-of-the-art LLMs and retrieval-augmented models on a diverse set of tasks. Specifically, Self-RAG outperforms ChatGPT and retrieval-augmented Llama2-chat on Open-domain QA, reasoning and fact verification tasks, and it shows significant gains in improving factuality and citation accuracy for long-form generations relative to these models. . However, indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility or can lead to unhelpful response generation. We introduce a new framework called **Self-Reflective Retrieval-Augmented Generation (SELF-RAG)** that enhances an LM’s quality and factuality through retrieval and self-reflection

## NM2 · NM
- 질문: 
- 요소: ['CRAG 가 무엇인지', '동작 방식(검색 평가 · 보정)']
- 컨텍스트: 2401.15884 Corrective Retrieval Augmented Generation · 2603.16169 Open-Source Reproduction and Explainability Analysis of Corr
- 답:

서론
검색 결과가 정확하지 않을 때 Retrieval Augmented Generation (RAG) 시스템은 잘못된 정보를 생성할 위험에 직면합니다. 이러한 오류를 자동으로 수정하는 메커니즘이 필요합니다.

본론
1. Corrective Retrieval Augmented Generation (CRAG) – 검색 품질 평가 및 교정: CRAG는 경량화된 retriever evaluator로 조회된 문서의 전반적인 질을 판단하고, 신뢰도 수준에 따라 다양한 지식 탐색 행동을 트리거합니다[2401.15884v3]. 또한 대규모 웹 검색 결과를 확장하여 정적·제한된 코퍼스만으로는 얻기 어려운 최적 문서를 보완하며, decompose‑then‑recompose 알고리즘으로 핵심 정보를 선택적으로 강조하고 관련 없는 내용을 필터링합니다. 이 방법은 플러그인 형태로 기존 RAG 파이프라인에 쉽게 결합됩니다[2401.15884v3].
2. CRAG – 오픈소스 재현 및 설명 가능성 분석: 원래 구현은 Google Search API와 폐쇄형 모델 가중치 등 비공개 구성 요소를 사용해 재현이 제한되었습니다. 본 연구는 Wikipedia API로 웹 검색을 대체하고 LLaMA‑2를 Phi‑3‑mini‑4k‑instruct으로 교체하여 완전한 오픈소스 파이프라인을 제공하며, PopQA와 ARC‑Challenge에서 기존 시스템과 유사한 성능을 보였습니다[2603.16169v1].

결론
CRAG는 검색 결과가 부정확할 때 웹 검색을 확장하여 결과를 보완하고, 자동 교정 능력을 향상시켜 RAG 기반 접근법의 성능을 크게 개선한다는 공통된 결론이 도출된다[2401.15884v3]. 또한 CRAG는 검색 문서의 품질을 평가하고 교정 행동을 유발함으로써 RAG 시스템의 견고성을 강화한다[2603.16169v1]. 다만 두 논문은 각각 다른 데이터셋과 실험 환경에서 결과를 제시하고 있어, 구체적인 성능 향상 정도와 적용 범위에 차이가 존재한다.

## NM3 · NM
- 질문: 
- 요소: ['중간 위치 정보 성능 저하 결과', 'U자 곡선']
- 컨텍스트: 2307.03172 Lost in the Middle: How Language Models Use Long Contexts · 2410.14641 Distance between Relevant Information Pieces Causes Bias in  · 2404.16811 Make Your LLM Fully Utilize the Context · 2406.16008 Found in the Middle: Calibrating Positional Attention Bias I · 2403.04797 Found in the Middle: How Language Models Use Long Contexts B
- 답:

서론
긴 입력 컨텍스트에서 중간에 위치한 관련 정보를 모델이 제대로 활용하지 못하는 현상은, 정보가 시작이나 끝보다 중간에 있을 때 성능이 크게 저하된다는 연구 결과로 확인되었습니다[2307.03172v3]. 이러한 문제는 현재 언어모델들이 긴 문맥을 처리할 수 있음에도 불구하고 해당 정보를 robust하게 사용하지 못한다는 한계를 보여줍니다.

본론
1. Lost in the Middle: 관련 정보가 입력 컨텍스트의 중간에 위치하면 모델 성능이 크게 저하되며, 이는 기존 모델을 포함한 모든 경우에 나타나는 현상입니다[2410.14641v3].
2. Positional Bias (U‑shaped): LLM은 시작과 끝 토큰을 더 높은 주의를 기울이는 U자형 주의 편향을 보이며, 중간에 있는 관련 정보를 놓치는 원인이 됩니다[2406.16008v2].

결론
제공된 문서들은 'Found in the Middle'와 관련된 연구 결과를 다루고 있으며, 이는 긴 컨텍스트 중간에 있는 정보를 모델이 놓치는 문제인 'Lost in the Middle' 현상을 해결하는 접근법으로 제시된다[2406.16008v2]. 또한, LongPiBench를 통해 다중 관련 정보가 존재할 때 두 가지 유형의 위치 편향이 존재한다는 실험 결과가 보고되어, 이러한 편향을 평가하고 완화하는 것이 LLM의 성능 향상에 중요함을 강조한다[2410.14641v3]. 따라서 'Found in the Middle'은 중간 정보 활용을 개선하여 RAG 성능을 향상시키는 구체적인 방법이며, LongPiBench는 해당 현상을 정량화하고 위치 편향 문제를 인식하는 벤치마크 역할을 한다.

## NM4 · NM
- 질문: 
- 요소: ['네 가지 능력(잡음 강건성 · 부정 거부 · 정보 통합 · 반사실 강건성)']
- 컨텍스트: 2309.01431 Benchmarking Large Language Models in Retrieval-Augmented Ge
- 답:

서론
RAG 평가 벤치마크 RGB는 대규모 언어 모델(LLM)에 적용된 검색 증강 생성(Retrieval‑Augmented Generation, RAG)의 성능을 체계적으로 측정하기 위해 설계되었습니다. 기존 연구에서는 다양한 LLM마다 RAG가 미치는 영향을 엄밀히 비교할 수 있는 기준이 부족해 잠재적 병목 현상을 파악하는 데 어려움이 있었습니다[2309.01431v2].

본론
1. Noise Robustness: 모델이 잡음에 견디는 능력을 평가합니다.[2309.01431v2] 부정적인 정보를 거부하거나 필터링할 수 있는지를 측정합니다.[2309.01431v2] 검색된 정보와 기존 지식을 통합하는 과정을 검증합니다[2309.01431v2].
결론
RGB 벤치마크는 LLM에 적용되는 RAG를 평가하기 위해 잡음 견고성, 부정적 거부 능력 및 정보 통합이라는 세 가지 핵심 능력을 정의하고 측정하도록 설계되었습니다.

## T07 · SV
- 질문: 
- 요소: ['대표 연구 3편 이상', '연구 방향 정리']
- 컨텍스트: 2507.19024 A Survey of Multimodal Hallucination Evaluation and Detectio · 2310.18344 Chainpoll: A high efficacy method for LLM hallucination dete · 2311.05232 A Survey on Hallucination in Large Language Models: Principl · 2404.18930 Hallucination of Multimodal Large Language Models: A Survey · 2606.06748 Evidence Graph Consistency in Retrieval-Augmented Generation · 2502.13490 What are Models Thinking about? Understanding Large Language · 2309.01219 Siren's Song in the AI Ocean: A Survey on Hallucination in L · 2508.01781 A comprehensive taxonomy of hallucinations in Large Language
- 답:

서론
LLM 환각 탐지는 모델이 사실과 다른 내용을 생성하는 현상을 식별하고 평가하기 위한 다양한 접근법이 연구되고 있습니다. 최근에는 환각 분류, 벤치마크 비교, 그리고 모델 내부 상태 분석 등 여러 방향으로 방법이 확장되었습니다.

본론
1. Hallucination Taxonomy: 환각을 충실성과 사실성 기준으로 분류한 체계를 제안하고, 실제 관측된 일반적인 유형들을 포함합니다[2507.19024v2]
2. ChainPoll: RealHall 벤치마크에서 전체 AUROC가 0.781로 가장 높은 성능을 보이며, 다음 이론적 방법보다 11% 높고 산업 표준보다 23% 초과했습니다[2310.18344v1]
3. Detection Methods &amp; Benchmarks Overview: 환각 탐지 방법과 벤치마크에 대한 포괄적인 개요를 제시하고, 현재 한계를 논의합니다[2311.05232v2]
4. Multimodal Hallucination Survey: 다중모달 LLM의 환각 문제를 다루며 기존 도전 과제와 제한점을 분석하고 미래 연구 방향을 제안합니다[2404.18930v2]
5. Evidence Graph Consistency (EGC): 응답마다 지역 증거 그래프를 구축해 다섯 가지 구조적 일관성 측정치를 계산하며, RAGTruth 데이터셋에서 모델 계열별 진단 효과를 확인했습니다[2606.06748v2]
6. Model Inner State Analysis: LLM 내부 상태를 활용해 환각 탐지를 수행하고 실험을 통해 장단점을 논의합니다[2502.13490v1]
7. LLM Hallucination Taxonomy &amp; Benchmarks Survey: LLM 환각 현상의 분류와 평가 벤치마크를 제시하며, 기존 완화 접근법을 분석하고 미래 연구 방향을 제안합니다[2309.01219v3]
8. Comprehensive Taxonomy of Halls in LLMs: 인지 및 인간 요인이 환각 인식에 미치는 영향을 조사하고, 탐지용벤치마크·메트릭과 구조적/시스템적 완화 전략을 제시합니다[2508.01781v1]

결론
제공된 문서들은 LLM 환각 탐지 방법의 성능과 한계를 다양한 측면에서 제시하고 있다. 먼저, ChainPoll은 모든 RealHall 벤치마크에서 AUROC 0.781을 달성하며 기존 이론적 방법을 11%나 앞섰고 산업 표준보다 23% 이상 우수함을 보이며 비용 효율성과 투명성도 높았다[2310.18344v1]. 반면, 다른 연구들은 환각 탐지 방법과 벤치마크에 대한 포괄적인 조사를 통해 현재 한계를 지적하고 향후 연구 방향을 제시한다[2507.19024v2][2311.05232v2][2309.01219v3][2508.01781v1]. 또한, EGC는 RAGTruth 데이터셋에서 그래프 일관성 특징이 모델 계열별로 일관된 진단 방향을 보임을 확인했다[2606.06748v2]. 이러한 결과들은 방법론과 평가 기준에 따라 성능 차이가 존재함을 보여주며, 특히 ChainPoll은 높은 정량적 성능을 입증한 반면, 다른 논문들은 전반적인 현황과 한계를 정리하는 데 초점을 맞추고 있다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• A Systematic Literature Review on Hallucination Detection Methods in LLMs (2026) https://openalex.org/W7164982801
• Large language models hallucination: A comprehensive survey (2026) [2510.06265]
• Hallucination Detection in Large Language Models with Metamorphic Relations (2025) [2502.15844]
• Cognitive Mirage: A Review of Hallucinations in Large Language Models (2023) [2309.06794]

## T01 · SV
- 질문: 
- 요소: ['대표 연구 3편 이상', '연구 방향 정리']
- 컨텍스트: 2412.19925 HADES: Hardware Accelerated Decoding for Efficient Speculati · 2412.12639 Falcon: Faster and Parallel Inference of Large Language Mode · 2504.00030 Token-Driven GammaTune: Adaptive Calibration for Enhanced Sp · 2412.18910 AdaEAGLE: Optimizing Speculative Decoding via Explicit Model · 2610.10411 Training Parallel Speculative Draft Models by Directly Minim · 2610.31819 Speculative Diffusion is a Tale of Two Tradeoffs · 2610.40541 On the Fundamental Limits of Prefill-Based Decoding Length P · 2610.23787 DLite: History-free Speculative Decoding for Agentic AI · 2611.06982 Decode Before You Hear: Speculative Listening for Chunk-Inte · 2605.02888 SpecKV: Adaptive Speculative Decoding with Compression-Aware
- 답:

서론
최근 대규모 언어 모델(LLM)에서 추상적 예측을 통해 생성 속도를 높이는 연구가 활발히 진행되고 있습니다. Speculative Decoding은 여러 논문이 다양한 하드웨어·소프트웨어 최적화, 적응형 구조 설계 및 학습 전략으로 성능과 효율성을 동시에 개선하고 있는 핵심 주제입니다.

본론
1. HADES: Hardware Accelerated Decoding (HADES)를 도입하여 LLM의 추상적 예측을 통해 연산 효율성과 에너지 소비량을 크게 향상시켰습니다. [2412.19925v2]
2. Falcon: Enhanced Semi-Autoregressive Drafting과 Custom-Designed Decoding Tree를 활용한 프레임워크로, Vicuna와 LLaMA‑Chat에서 손실 없는 속도 향상을 2.91배~3.51배 달성했습니다. [2412.12639v3]
3. GammaTune / GammaTune+: Token acceptance rate에 기반한 heuristic switching 메커니즘으로 speculation length를 동적으로 조정하며, SpecBench에서 고정 길이 방식보다 우수한 평균 속도 향상을 보였습니다. [2504.00030v3]
4. AdaEAGLE: Adaptive Draft Structures를 명시적으로 모델링하고 threshold‑based 전략을 결합해 vanilla AR 대비 1.62배의 속도를 얻으며 출력 품질은 유지했습니다. [2412.18910v1]
5. EDR (Markov Reward Process): Speculative Decoding을 Markov reward process로 표현한 이론적 프레임워크를 통해 DSpark와 DFly 두 draft 모델을 finetune하고, 평균 accepted length가 향상되었습니다. [2610.10411v1]
6. SpecDiffusion: Diffusion effort와 acceptance leniency라는 두 파라미터의 결합 변형을 탐색해 단일 단계 diffusion drafting보다 더 넓은 속도‑품질 Pareto frontier를 확장했습니다. [2610.31819v1]
7. Prefill-Based Decoding Length Prediction Limits: 응답 종료 확률이 step마다 증가하는 특성을 이용해 decode length가 중심극한정리를 따르며, per-prompt 정규성과 명시적 오차항을 포함한 affine variance law(σ=αμ+b)를 도출했습니다. [2610.40541v1]
8. DLite: History‑free 구조에 대한 맞춤형 두 단계 학습 전략으로 일반·장문의 작업에서 평균 accepted length가 2~6이며, DSpark 대비 최대 70% 성능 향상을 보였습니다. [2610.23787v1]
9. Speculative Listening: 입력 시간 자기 추상적 예측을 위한 lossless 프레임워크로 응답 시작 전 decoding delay를 평균 73% 감소시켜 인간 턴 간격(200 ms)에 근접했습니다. [2611.06982v1]
10. SpecKV: Draft 모델 자체 신호에서 γ 값을 선택하는 경량 적응형 컨트롤러이며, 고정‑γ=4 대비 토큰당 기대값을 크게 향상시키고 오버헤드는 0.34 ms 미만입니다. [2605.02888v1]

결론
제공된 문서들은 Speculative Decoding 연구가 하드웨어 가속(HADES), 적응형 드래프트 구조 설계(Falcon, AdaEAGLE, GammaTune 등)와 학습 전략(EDR, DLite)을 통해 속도 향상과 에너지 효율성을 동시에 추구한다는 공통 흐름을 보여줍니다. 또한 파라미터 결합 최적화(SpecDiffusion), 예측 기반 길이 제한 분석(Prefill‑Based Limits) 및 실시간 지연 감소 기술(Speculative Listening, SpecKV) 등 다양한 접근법이 적용되고 있어 연구가 하드웨어·알고리즘 전반에 걸쳐 확장되는 추세임을 확인할 수 있습니다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• Confidence-Modulated Speculative Decoding for Large Language Models (2025) [2508.15371]
• Self Speculative Decoding for Diffusion Large Language Models (2025) [2510.04147]
• Speculative Decoding for Multi-Sample Inference (2025) https://doi.org/10.18653/v1/2025.findings-emnlp.668
• Speculative Decoding Reimagined for Multimodal Large Language Models (2025) [2505.14260]

## T05 · SV
- 질문: 
- 요소: ['대표 연구 3편 이상', '연구 방향 정리']
- 컨텍스트: 2606.12737 PI-Hunter: Automated Red-Teaming for Exposing and Localizing · 2605.15030 WARD: Adversarially Robust Defense of Web Agents Against Pro · 2606.15441 Defending against Adaptive Prompt Injection Attacks via Reas · 2511.10720 PISanitizer: Preventing Prompt Injection to Long-Context LLM
- 답:

서론
프롬프트 인젝션 공격은 LLM 에이전트나 웹 에이전트가 의도하지 않은 명령을 따르게 만드는 보안 위협이며, 이를 탐지·방지하기 위한 다양한 연구가 진행되고 있다.

본론
1. PI-Hunter: 자동화된 에이전트 감사 프레임워크로 취약점 노출과 공격 표면 커버리지를 기존 강력한 레드팀 기반선에 비해 크게 향상시킨다[2606.12737v1]
2. WARD: 대규모 데이터셋(WARD-Base, 약 177K 샘플) 과 전용 인젝션数据集(WARD‑PIG) 을 기반으로 웹 에이전트의 프롬프트 인젝션을 견딜 수 있는 보호 모델을 제공한다[2605.15030v1]
3. RETA: 사용자 작업을 근거로 방어 결정을 내리는 훈련 기반 방법으로, 여섯 가지 블랙박스 적응형 공격에서 모든 ASR이 10% 미만이며 평균 ASR은 두 모델 각각 약 2.9~3.8% 수준이다[2606.15441v1]
4. PISanitizer: 컨텍스트에 잠재적 인젝션 토큰을 식별·정화한 뒤 백엔드 LLM이 응답하도록 하여, 프롬프트 정화를 통해 공격 지시어의 영향을 제거한다[2511.10720v1]

결론
PI-Hunter는 다양한 벤치마크와 에이전트 아키텍처에서 취약점 노출과 공격 표면 커버리지를 기존 자동 레드팀 기반선보다 크게 향상시킨다[2606.12737v1]. WARD는 대규모 데이터셋(약 177K 샘플)을 기반으로 웹 에이전트의 프롬프트 인젝션에 대한 적대적 견고성을 제공한다[2605.15030v1]. RETA는 여섯 가지 블랙박스 적응형 공격에서 모든 공격의 ASR을 10% 미만으로 유지하며 평균 2.92%와 3.75%를 달성한다[2606.15441v1]. PISanitizer는 프롬프트 정제 방식을 통해 토큰 주입을 방지한다[2511.10720v1]. 따라서 각 연구는 데이터 규모와 평가 조건에 따라 취약점 발견 능력과 방어 성능에서 차이가 있으며, 대규모 데이터 기반 접근법과 정밀한 정제 기법이 각각 다른 측면에서 효과적이다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• A Critical Evaluation of Defenses against Prompt Injection Attacks: [Dataset/Tool Paper] (2026) [2505.18333]
• Jatmo: Prompt Injection Defense by Task-Specific Finetuning (2024) [2312.17673]
• Prompt injection attacks and defenses in large language models: A systematic literature review (2026) https://doi.org/10.5281/zenodo.19856513
• Prompt Injection attack against LLM-integrated Applications (2023) [2306.05499]

## T04 · SV
- 질문: 
- 요소: ['대표 연구 3편 이상', '연구 방향 정리']
- 컨텍스트: 2502.15723 Balancing Content Size in RAG-Text2SQL System · 2503.23886 Text2Schema: Filling the Gap in Designing Database Table Str · 2403.20014 PURPLE: Making a Large Language Model a Better SQL Writer · 2410.01066 From Natural Language to SQL: Review of LLM-based Text-to-SQ · 2502.20657 Automatic database description generation for Text-to-SQL · 2501.12372 Is Long Context All You Need? Leveraging LLM's Extended Cont · 2412.10138 ROUTE: Robust Multitask Tuning and Collaboration for Text-to · 2412.17867 Evaluating and Enhancing LLMs for Multi-turn Text-to-SQL wit · 2604.28049 Agent-Agnostic Evaluation of SQL Accuracy in Production Text · 2503.21602 GenEdit: Compounding Operators and Continuous Improvement to
- 답:

서론
최근 Text‑to‑SQL 연구들은 모델이 더 큰 컨텍스트를 활용하고, 도메인 지식을 강화하며, 평가와 튜닝을 자동화하는 방향으로 발전하고 있다. 이러한 흐름은 LLM 기반 접근법과 다양한 보조 기법을 결합해 정확도와 견고성을 동시에 높이는 것을 목표로 한다.

본론
1. Balancing Content Size in RAG‑Text2SQL System: 문서 크기와 성능 저하 사이의 임계점을 식별하고, 이를 완화하기 위한 실용적인 전략을 제시한다[2502.15723v3]
2. SchemaAgent (LLM 기반 다중 에이전트 프레임워크): Text2Schema를 위해 전용 역할(반성·검토)과 오류 탐지‑수정 메커니즘을 도입해 설계 단계의 문제를 식별하고 수정한다[2503.23886v2]
3. PURPLE: 논리적 연산자 조합이 포함된 데모스트레이션을 검색하여 LLM에 SQL 변환 지침을 제공한다[2403.20014v1]
4. Graph RAGs 활용 평가 및 한계 분석: Graph‑based Retrieval Augmented Generation으로 컨텍스트 정확도와 스키마 연결성을 향상시키고, 계산 효율성·모델 견고성·데이터 프라이버시 등 주요 과제를 강조한다[2410.01066v2]
5. Automatic database description generation for Text-to-SQL: Bird 벤치마크에서 자동 생성된 데이터베이스 설명을 사용하면 SQL 생성 정확도가 기존 대비 0.93% 향상되고 인간 수준 성능의 약 37%를 달성한다[2502.20657v1]
6. Long Context NL2SQL Pipeline (gemini‑pro‑1.5): 긴 컨텍스트 LLM이 확장된 정보에서도 견고하게 작동하며, 파인튜닝 없이 다양한 벤치마크에서 강력한 성능을 보인다[2501.12372v6]
7. ROUTE: 오픈소스 LLM의 Text2SQL 전반적인 능력을 향상시키기 위해 다중 작업 튜닝·협업 메커니즘(Robust Multitask Tuning and Collaboration) 을 제안한다[2412.10138v3]
8. MMSQL (Multi‑turn Question Types Test Suite): 다양한 질문 유형과 멀티턴 Q&amp;A를 시뮬레이션해 LLM의 분류 및 SQL 생성 능력을 평가하고, 대화 역학을 탐색하는 모델을 크게 향상시킨다[2412.17867v4]
9. STEF: 스키마나 참조 쿼리 없이 사용자 질의와 재형식화된 문장만으로 생산 환경에서 SQL 정확도를 자동으로 평가한다[2604.28049v1]

결론
제공된 문서들은 Text-to-SQL 연구가 모델의 견고성 강화, 스키마 연결 정확도 향상, 그리고 다양한 평가 프레임워크 구축이라는 방향으로 진행되고 있음을 보여줍니다. 특히 RAG 기반 시스템의 견고성을 높이는 로드맵을 제시하고 [2502.15723v3], 그래프 RAG를 활용한 스키마 링크 정확도 개선을 논의하며 [2410.01066v2], 그리고 STEF와 같은 스키마에 무관한 평가 프레임워크를 제안하여 실제 환경에서의 평가를 가능하게 합니다 [2604.28049v1]. 또한, 다양한 벤치마크에서 모델 성능을 개선하거나 인간 수준의 성능에 근접하도록 하는 실험 결과들이 보고되고 있습니다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• Datrics Text2SQL: A Framework for Natural Language to SQL Query Generation (2025) [2506.12234]
• Arctic-Text2SQL-R1: Simple Rewards, Strong Reasoning in Text-to-SQL (2026) [2505.20315]
• MultiSQL: A Schema-Integrated Context-Dependent Text2SQL Dataset with Diverse SQL Operations (2024) https://doi.org/10.18653/v1/2024.findings-acl.823
• GBV-SQL: Guided Generation and SQL2Text Back-Translation Validation for Multi-Agent Text2SQL (2026) [2509.12612]

## HU17 · MU
- 질문: 
- 요소: ['서브워드 분할', '다국어 토크나이저', '토큰 줄이는 문맥 압축']
- 컨텍스트: 2406.19223 T-FREE: Subword Tokenizer-Free Generative LLMs via Sparse Re · 2504.00178 Boundless Byte Pair Encoding: Breaking the Pre-tokenization  · 2511.08128 Sentence-Anchored Gist Compression for Long-Context LLMs · 2604.15153 Compressing Sequences in the Latent Embedding Space: $K$-Tok · 2510.20535 ARC-Encoder: learning compressed text representations for la
- 답:

서론
토크나이저는 대규모 언어 모델(LLM)에서 정보를 인코딩하는 핵심 단계이지만, 최근 연구가 정체되어 있고 서브워드 분할, 다국어 지원 부족 등의 한계가 존재합니다. 또한 긴 프롬프트를 처리함에 따라 토큰 수가 급증해 메모리·계산 비용이 커지는 문제가 발생합니다.

본론
1. T-FREE: 서브워드를 사용하지 않고 문자 삼중항의 희소 활성화 패턴을 통해 단어를 직접 임베딩하며, 참조 코퍼스 없이도 작동합니다[2406.19223v2].
2. BoundlessBPE: 사전 토큰화 경계를 완화해 두 개의 완전한 pretoken을 하나의 superword로 병합함으로써 token 분포를 균일하게 만들고 텍스트 압축 효율이 최대 15% 향상됩니다[2504.00178v2].

결론
제공된 문서들은 서브워드 토크나이저와 관련된 연구 결과를 제시하고 있습니다. 먼저, 서브워드 분할 방식에 대한 비교는 제공된 결과에서 직접적으로 다루어지지 않습니다. 두 번째로, 다국어 토크나이저 측면에서는 T-FREE가 참조 코퍼스에 편향되어 소수 언어의 성능이 감소한다는 한계를 지적하며, 동시에 교차언어 전이 학습에서 유의미한 개선을 보인다고 보고합니다 [2406.19223v2]. 마지막으로, 토큰 수를 줄이는 문맥 압축에 대해서는 Boundless BPE가 표준 BPE보다 토큰 분포를 균일하게 만들고 텍스트를 더 효과적으로 압축하여 토큰당 바이트를 최대 15% 증가시킨다고 결론지었습니다 [2504.00178v2]. 따라서 서브워드 분할 방식 비교는 다루어지지 않았으나, 다국어 성능과 문맥 압축 효율성에서는 각각 다른 접근법이 고유한 장점을 보인 것으로 판단됩니다.

## HU27 · MU
- 질문: 
- 요소: ['constitutional AI', '레드팀 데이터셋', 'over-refusal']
- 컨텍스트: 2608.28593 Statutory AI: Aligning Large Language Models With Legal Norm · 2501.18837 Constitutional Classifiers: Defending against Universal Jail · 2408.11851 SAGE-RT: Synthetic Alignment data Generation for Safety Eval · 2412.16974 Cannot or Should Not? Automatic Analysis of Refusal Composit · 2506.05376 A Red Teaming Roadmap Towards System-Level Safety
- 답:

서론
LLM 정렬 과정에서 헌법 AI, 레드팀 데이터셋 및 거부 응답 과잉(over‑refusal) 문제를 동시에 다루는 연구가 필요합니다. 이러한 문제는 모델의 안전성을 확보하면서도 실제 사용 환경에서 과도한 거부가 발생하지 않도록 균형을 맞추어야 하기 때문에 복잡합니다.

본론
1. Statutory AI: 5개의 처벌 주제에 대한 레드팀 프롬프트를 이용해 유해 콘텐츠를 기존 Constitutional AI보다 약 10%p 더 많이 감소시켰으며, 계산 시간을 절반 이상 단축했습니다. [2608.28593v1]
2. Constitutional Classifiers (Improved): 합성 데이터를 기반으로 훈련된 분류기를 통해 거부율을 낮추고 추론 오버헤드를 줄였으며, 생산 트래픽에서 약 0.38%의 절대적 증가와 가짜 양성률 ≈ 1.74%를 유지했습니다. [2501.18837v1]
3. SAGE‑RT: 상세 분류학을 이용해 다양한 해악 주제에 대한 레드팀 데이터를 합성했으며, GPT‑4o·GPT‑3.5에서 유해 하위 범주별 공격 성공률 100%를 달성했습니다. [2408.11851v1]
4. Refusal Classification Framework: IFT/RLHF 데이터셋을 활용해 거부 응답 과잉 현상을 분석하고, 16개의 거부 카테고리와 인간 주석 데이터를 기반으로 분류기를 훈련해 거부를 정밀하게 감시할 수 있게 했습니다. [2506.05376v2][2412.16974v1]

결론
헌법 AI는 유해 콘텐츠를 52~59%p 감소시켰으며, 이는 표준 헌법 AI보다 약 10%p 더 높은 효과와 함께 계산 시간을 50% 이상 단축했다[2608.28593v1]. 레드팀 데이터셋과 거부 응답 과잉에 대한 연구에서는 향상된 분류기가 특정 도메인 제이브레이크에 대해 견고한 방어를 보이며, 생산 트래픽에서의 거부율은 절대적으로 0.38% 증가하고 추론 오버헤드는 23.7%로 나타났다[2501.18837v1]. 또한, 기존 거부 평가 데이터가 'should-not' 범주에 치중되어 있고 블랙박스 LLM 출력의 거부 내용을 감사할 도구가 부족하다는 한계가 지적되었다[2412.16974v1]. 이러한 결과들은 각 연구가 서로 다른 방법론과 평가 조건을 적용했음을 보여주며, 헌법 AI와 레드팀 기반 접근법이 각각 유해 콘텐츠 감소와 거부율 제어 측면에서 유의미한 성과를 달성하고 있음을 시사한다.

- 인용 블록(근거 대조용):

  > [문서 1] [Distance: 0.4119] [발행일: 2026-06-13] [2608.28593v1] Statutory AI: Aligning Large Language Models With Legal Norms . To illustrate the potential of our approach, we conducted an experiment involving 1,000 red-teaming prompts and five penal themes: discrimination, disclosure of confidential information, violence, fraud, and abuse of vulnerable persons. Statutory AI reduced harmful content by 52 to 59 percentage points across tested models, approximately 10 percentage points higher than standard Constitutional AI, while cutting computation time by over 50%.

  > [문서 2] [Distance: 0.4032] [발행일: 2025-01-31] [2501.18837v1] Constitutional Classifiers: Defending against Universal Jailbreaks across Thousands of Hours of Red Teaming [초록] Large language models (LLMs) are vulnerable to universal jailbreaks-prompting strategies that systematically bypass model safeguards and enable users to carry out harmful processes that require many model interactions, like manufacturing illegal substances at scale. To defend against these attacks, we introduce Constitutional Classifiers: safeguards trained on synthetic data, generated by prompting LLMs with natural language rules (i.e., a constitution) specifying permitted and restricted content. In over 3,000 estimated hours of red teaming, no red teamer found a universal jailbreak that could extract information from an early classifier-guarded LLM at a similar level of detail to an unguarded model across most target queries. On automated evaluations, enhanced classifiers demonstrated robust defense against held-out domain-specific jailbreaks. These classifiers also maintain deployment viability, with an absolute 0.38% increase in production-traffic refusals and a 23.7% inference overhead. Our work demonstrates that defending against universal jailbreaks while maintaining practical deployment viability is tractable. **Improved constitutional classifiers.** In the following section, we present an improved constitutional classifier method that achieves lower refusal rates and inference overhead than the system that was red teamed. When applied to this constitution, this methodology yields lower attack success rates (Figure 5) compared to our red-teamed system while simultaneously maintaining an acceptable false-positive rate (approximately 1.74% on production Claude.ai traffic)

  > [문서 3] [Distance: 0.4744] [발행일: 2024-08-14] [2408.11851v1] SAGE-RT: Synthetic Alignment data Generation for Safety Evaluation and Red Teaming [초록] We introduce Synthetic Alignment data Generation for Safety Evaluation and Red Teaming (SAGE-RT or SAGE) a novel pipeline for generating synthetic alignment and red-teaming data. Existing methods fall short in creating nuanced and diverse datasets, providing necessary control over the data generation and validation processes, or require large amount of manually generated seed data. SAGE addresses these limitations by using a detailed taxonomy to produce safety-alignment and red-teaming data across a wide range of topics. We generated 51,000 diverse and in-depth prompt-response pairs, encompassing over 1,500 topics of harmfulness and covering variations of the most frequent types of jailbreaking prompts faced by large language models (LLMs). We show that the red-teaming data generated through SAGE jailbreaks state-of-the-art LLMs in more than 27 out of 32 sub-categories, and in more than 58 out of 279 leaf-categories (sub-sub categories). The attack success rate for GPT-4o, GPT-3.5-turbo is 100% over the sub-categories of harmfulness. Our approach avoids the pitfalls of synthetic safety-training data generation such as mode collapse and lack of nuance in the generation pipeline by ensuring a detailed coverage of harmful topics using iterative expansion of the topics and conditioning the outputs on the generated raw-text. This method can be used to generate red-teaming and alignment data for LLM Safety completely synthetically to make LLMs safer or for red-teaming the models over a diverse range of topics. ## **Algorithm-3: Alignment Data Generation** Algorithm (3) converts the red-teaming data into a direct preference optimisation (DPO) dataset (Rafailov et al. 2023). This requires access to an uncensored LLM and a safety aligned LLM which has been prompted to give the rejection response and the reason for rejection. The uncensored LLM in our case is SolarLM (10.7B) (Zuev 2023) and the aligned LLM is Llama-3-instruct (Dubey et al. 2024)

  > [문서 4] [Distance: 0.4596] [발행일: 2024-12-22] [2412.16974v1] Cannot or Should Not? Automatic Analysis of Refusal Composition in IFT/RLHF Datasets and Refusal Behavior of Black-Box LLMs [초록] Refusals - instances where large language models (LLMs) decline or fail to fully execute user instructions - are crucial for both AI safety and AI capabilities and the reduction of hallucinations in particular. These behaviors are learned during post-training, especially in instruction fine-tuning (IFT) and reinforcement learning from human feedback (RLHF). However, existing taxonomies and evaluation datasets for refusals are inadequate, often focusing solely on should-not-related (instead of cannot-related) categories, and lacking tools for auditing refusal content in black-box LLM outputs. We present a comprehensive framework for classifying LLM refusals: (a) a taxonomy of 16 refusal categories, (b) a human-annotated dataset of over 8,600 instances from publicly available IFT and RLHF datasets, (c) a synthetic dataset with 8,000 examples for each refusal category, and (d) classifiers trained for refusal classification. Our work enables precise auditing of refusal behaviors in black-box LLMs and automatic analyses of refusal patterns in large IFT and RLHF datasets. This facilitates the strategic adjustment of LLM refusals, contributing to the development of more safe and reliable LLMs. . Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom Brown, and Jared Kaplan. Constitutional ai: Harmlessness from ai feedback, 2022b. URL `https://arxiv.org/abs/2212.08073` .

  > [문서 5] [Distance: 0.4905] [발행일: 2025-05-30] [2506.05376v2] A Red Teaming Roadmap Towards System-Level Safety [초록] Large Language Model (LLM) safeguards, which implement request refusals, have become a widely adopted mitigation strategy against misuse. At the intersection of adversarial machine learning and AI safety, safeguard red teaming has effectively identified critical vulnerabilities in state-of-the-art refusal-trained LLMs. However, in our view the many conference submissions on LLM red teaming do not, in aggregate, prioritize the right research problems. First, testing against clear product safety specifications should take a higher priority than abstract social biases or ethical principles. Second, red teaming should prioritize realistic threat models that represent the expanding risk landscape and what real attackers might do. Finally, we contend that system-level safety is a necessary step to move red teaming research forward, as AI models present new threats as well as affordances for threat mitigation (e.g., detection and banning of malicious users) once placed in a deployment context. Adopting these priorities will be necessary in order for red teaming research to adequately address the slate of new threats that rapid AI advances present today and will present in the very near future. ## **Abstract** Large Language Model (LLM) safeguards, which implement request refusals, have become a widely adopted mitigation strategy against misuse. At the intersection of adversarial machine learning and AI safety, safeguard red teaming has effectively identified critical vulnerabilities in state-of-the-art refusaltrained LLMs. However, in our view the many conference submissions on LLM red teaming do not, in aggregate, prioritize the right research problems

## HU39 · MU
- 질문: 
- 요소: ['문장 임베딩 평가', '다국어 임베딩', '임베딩 압축']
- 컨텍스트: 2604.15153 Compressing Sequences in the Latent Embedding Space: $K$-Tok · 2403.20327 Gecko: Versatile Text Embeddings Distilled from Large Langua · 2406.19223 T-FREE: Subword Tokenizer-Free Generative LLMs via Sparse Re · 2605.15081 ML-Embed: Inclusive and Efficient Embeddings for a Multiling · 2409.15763 IRSC: A Zero-shot Evaluation Benchmark for Information Retri
- 답:

서론
문장 임베딩 평가는 다양한 언어와 작업에 걸쳐 일관된 성능 측정이 필요하지만, 기존 벤치마크가 특정 모델이나 데이터셋에만 치우쳐 있어 포괄적인 비교가 어렵습니다[2409.15763v2]. 다국어 지원은 현재 대부분의 텍스트 임베딩이 영어 중심이며 저자원 언어나 소수언어에서 성능 격차가 존재한다는 점에서 어려운 과제입니다. 또한, 대규모 언어 모델을 압축하는 과정에서 임베딩 레이어를 크게 줄이는 것이 모델 효율성을 높이지만 정확도 손실을 최소화해야 하는 복잡한 문제이기도 합니다[2604.15153v3][2406.19223v2].

본론
1. IRSC: 다국어 RAG 시나리오에서 텍스트 임베딩 모델을 평가하기 위해 다섯 가지 검색 작업(쿼리, 제목, 부분 문단, 키워드, 요약)을 포함하는 벤치마크와 SSCI·RCCI라는 새로운 지표를 제시합니다[2409.15763v2].
2. Gecko: LLM으로부터 지식 추출 과정을 통해 소형화된 텍스트 임베딩 모델을 개발하고, MTEB에서 기존보다 더 작은 차원(256 또는 768)에서도 높은 성능을 달성했습니다[2403.20327v1][2605.15081v1].
3. T-FREE: 서브워드 토크나이저 없이 문자 삼중항에 기반한 희소 활성화 패턴으로 단어를 직접 임베딩하여 파라미터를 최대 87.5% 감소시키고, 텍스트 평균 인코더 길이를 56% 줄이는 압축 효과를 얻었습니다[2406.19223v2].

결론
Gecko는 256 차원 임베딩으로 MTEB 벤치마크에서 기존 768 차원 모델보다 우수한 성능을 보이며, 768 차원에서도 7배 큰 모델과 5배 높은 차원에 경쟁한다[2403.20327v1]. T-FREE는 파라미터를 85% 이상 감소시키고 임베딩 레이어 크기를 87.5% 줄이는 동시에 표준 다운스트림 벤치마크에서 경쟁력을 유지한다[2406.19223v2]. ML-Embed은 다국어 데이터셋을 활용해 140M~8B 파라미터 범위의 모델을 훈련했으며, 430개 작업 평가에서 9개의 MTEB 벤치마크 기록을 새로 세우고 저자원 언어에서 특히 강한 결과를 보였다[2605.15081v1]. IRSC는 다국어 RAG 작업을 위한 임베딩 모델 평가를 위한 벤치마크를 소개하고, 교차언어 제한에 대한 통찰을 제공한다[2409.15763v2]. 따라서 질문의 세 가지 주제(문장 임베딩 평가, 다국어 임베딩, 임베딩 압축) 모두 관련 연구가 존재하지만, Gecko는 성능과 차원 효율성, T-FREE는 파라미터 및 인코딩 길이 감소, ML-Embed은 다국어·저자원 언어에서의 기록 수립에 각각 초점을 맞추고 있다.

## MU1 · MU
- 질문: 
- 요소: ['E1 방해 · 무관 문서를 사실로 쓰는 문제를 재고 줄인 연구', 'E2 방해 문서를 일부러 섞는 평가 방법', 'E3 다른 주체(회사) 문서 혼동']
- 컨텍스트: 2601.01896 Tackling the Inherent Difficulty of Noise Filtering in RAG · 2510.21440 Redefining Retrieval Evaluation in the Era of LLMs · 2512.22442 HiFi-RAG: Hierarchical Content Filtering and Two-Pass Genera · 2601.20276 Beyond the Needle's Illusion: Decoupled Evaluation of Eviden · 2409.10102 Trustworthiness in Retrieval-Augmented Generation Systems: A
- 답:

서론
제공된 문서에는 질문이 찾는 연구가 없습니다.

본론
1. HiFi-RAG: 다단계 파이프라인으로 검색 단계에서 관련 없는 정보를 필터링하고, 최종 답변 생성 시 Gemini 2.5 Pro의 추론 능력을 활용하여 ROUGE‑L과 DeBERTaScore를 향상시켰다[2512.22442v1].
2. EverMemBench-S (EMB‑S): 충돌 테스트된 근접 음수 예제와 금전 증거 집합을 이용해 검색 기반 평가에서 의미 간섭에 대한 모델의 성능 격차를 측정한다; 이는 방해 문서가 섞인 상황에서도 모델을 진단하는 데 사용된다[2601.20276v1].
3. Utility and Distraction‑aware Cumulative Gain (UDCG): 관련 문단의 긍정적 기여와 방해 문서의 부정적 영향을 정량화하고, LLM 중심 위치 할인 방식을 도입해 전통적인 IR 지표보다 최대 36%까지 상관관계를 개선한다[2510.21440v1].

결론
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• When More Documents Hurt RAG: Measuring and Reducing Vector Search Dilution with Domain-Scoped Retrieval (2026) [2606.11350]
• Semantic Distractor Robustness in LLMs: Exploring the Underlying Mechanisms (2026) https://doi.org/10.18653/2026.emnlp-main.1573
• U-NIAH: Unified RAG and LLM Evaluation for Long Context Needle-in-a-Haystack (2025) [2503.00353]
• Compressing Long Context for Enhancing RAG with AMR-based Concept Distillation (2024) [2405.03085]

- 인용 블록(근거 대조용):

  > [문서 2] [Distance: 0.3735] [발행일: 2025-10-24] [2510.21440v1] Redefining Retrieval Evaluation in the Era of LLMs [초록] Traditional Information Retrieval (IR) metrics, such as nDCG, MAP, and MRR, assume that human users sequentially examine documents with diminishing attention to lower ranks. This assumption breaks down in Retrieval Augmented Generation (RAG) systems, where search results are consumed by Large Language Models (LLMs), which, unlike humans, process all retrieved documents as a whole rather than sequentially. Additionally, traditional IR metrics do not account for related but irrelevant documents that actively degrade generation quality, rather than merely being ignored. Due to these two major misalignments, namely human vs. machine position discount and human relevance vs. machine utility, classical IR metrics do not accurately predict RAG performance. We introduce a utility-based annotation schema that quantifies both the positive contribution of relevant passages and the negative impact of distracting ones. Building on this foundation, we propose UDCG (Utility and Distraction-aware Cumulative Gain), a metric using an LLM-oriented positional discount to directly optimize the correlation with the end-to-end answer accuracy. Experiments on five datasets and six LLMs demonstrate that UDCG improves correlation by up to 36% compared to traditional metrics. Our work provides a critical step toward aligning IR evaluation with LLM consumers and enables more reliable assessment of RAG components ## **8 Conclusions** This paper addresses a fundamental misalignment between traditional information retrieval evaluation metrics and the requirements of modern RAG systems. We demonstrated that classical IR metrics like nDCG, MAP, and MRR fail to adequately predict RAG performance because they assume monotonically decreasing document utility with rank position and ignore the heterogeneous distracting effects of irrelevant documents on LLM generation quality

  > [문서 3] [Distance: 0.5168] [발행일: 2025-12-27] [2512.22442v1] HiFi-RAG: Hierarchical Content Filtering and Two-Pass Generation for Open-Domain RAG [초록] Retrieval-Augmented Generation (RAG) in open-domain settings faces significant challenges regarding irrelevant information in retrieved documents and the alignment of generated answers with user intent. We present HiFi-RAG (Hierarchical Filtering RAG), the winning closed-source system in the Text-to-Text static evaluation of the MMU-RAGent NeurIPS 2025 Competition. Our approach moves beyond standard embedding-based retrieval via a multi-stage pipeline. We leverage the speed and cost-efficiency of Gemini 2.5 Flash (4-6x cheaper than Pro) for query formulation, hierarchical content filtering, and citation attribution, while reserving the reasoning capabilities of Gemini 2.5 Pro for final answer generation. On the MMU-RAGent validation set, our system outperformed the baseline, improving ROUGE-L to 0.274 (+19.6%) and DeBERTaScore to 0.677 (+6.2%). On Test2025, our custom dataset evaluating questions that require post-cutoff knowledge (post January 2025), HiFi-RAG outperforms the parametric baseline by 57.4% in ROUGE-L and 14.9% in DeBERTaScore. - [6] Chin-Yew Lin. ROUGE: A Package for Automatic Evaluation of Summaries. In Text Summarization Branches Out, pages 74–81, Barcelona, Spain. Association for Computational Linguistics, 2004. - [7] Microsoft. Deberta-xlarge-mnli model card. `https://huggingface.co/microsoft/ deberta-xlarge-mnli` , 2021. - [8] Cattalyya Nuengsigkapian and Stephanie Renee Debats. Cascaded models for context awareness with wearable devices. U.S. Patent Application US 2025/0024131 A1, 2025.

  > [문서 4] [Distance: 0.3857] [발행일: 2026-01-28] [2601.20276v1] Beyond the Needle's Illusion: Decoupled Evaluation of Evidence Access and Use under Semantic Interference at 326M-Token Scale [초록] Long-context LLM agents must access the right evidence from large environments and use it faithfully. However, the popular Needle-in-a-Haystack (NIAH) evaluation mostly measures benign span localization. The needle is near-unique, and the haystack is largely irrelevant. We introduce EverMemBench-S (EMB-S), an adversarial NIAH-style benchmark built on a 326M-token MemoryBank. While the full MemoryBank spans 326M tokens for retrieval-based (RAG) evaluation, we evaluate native long-context models only at scales that fit within each model's context window (up to 1M tokens in this work) to ensure a fair comparison. EMB-S pairs queries with collision-tested near-miss hard negatives and gold evidence sets spanning one or more documents, validated via human screening and LLM verification. We also propose a decoupled diagnostic protocol that reports evidence access (document-ID localization) separately from end-to-end QA quality under full-context prompting. This enables consistent diagnosis for both native long-context prompting and retrieval pipelines. Across a reference-corpus ladder from domain-isolated 64K contexts to a globally shared 326M-token environment, we observe a clear reality gap. Systems that saturate benign NIAH degrade sharply in evidence access under semantic interference. These results indicate that semantic discrimination, not context length alone, is the dominant bottleneck for long-context memory at scale. the integration of multiple documents rather than the retrieval of a single isolated span. Crucially, this challenge is orthogonal to context length alone: increasing scale primarily amplifies semantic interference rather than introducing new forms of difficulty. To bridge this realism gap while preserving the tractability of NIAH-style evaluation, we introduce **EverMemBench-S (EMB-S)**, an _adversar-_ _ial NIAH-style_ benchmark. Conceptually, EMB-S

## C02 · CP
- 질문: 
- 요소: ['두 방법 각각', '차이']
- 컨텍스트: 2605.00789 Make Your LVLM KV Cache More Lightweight · 2506.18879 CommVQ: Commutative Vector Quantization for KV Cache Compres
- 답:

서론
KV 캐시는 대규모 언어 모델(LLM)과 대형 비전‑언어 모델(LVLM)에서 인페런스를 가속화하지만, 특히 LVLM에서는 시각 토큰 수가 많아 GPU 메모리 사용량이 크게 증가하는 문제가 발생합니다. 이러한 과도한 KV 캐시 크기를 줄이는 것이 성능 저하 없이 효율적인 추론을 위해 중요합니다.

본론
1. LightKV: 비전‑토크인 임베딩 사이의 중복성을 활용해 텍스트 프롬프트에 의해 안내된 교차 모달리티 메시지 전달로 정보를 집계하고, 프리필 단계에서 점진적으로 압축합니다[2605.00789v1].
2. CommVQ: 가산 양자화와 경량 인코더·코드북을 도입해 KV 캐시를 압축한 뒤, RoPE와 교환 가능한 코드북 설계 및 EM 알고리즘 학습으로 디코딩 비용을 낮추고, FP16 대비 최대 87.5%의 메모리 절감을 달성합니다[2506.18879v1].

결론
LightKV는 시각 토큰을 55%로 줄여 KV 캐시 크기를 절반으로 감소시키고, 최대 40%의 계산량을 절감하며 기존 기반 모델보다 성능이 우수함을 보여준다[2605.00789v1]. 반면 CommVQ는 2-bit 양자화를 통해 FP16 KV 캐시 크기를 87.5%까지 축소하고, RoPE-commutative 코드북을 이용해 높은 정확도와 낮은 오버헤드를 달성한다[2506.18879v1]. 두 방법은 각각 시각 토큰 압축과 일반적인 양자화 기반 압축이라는 다른 접근법을 취해, 캐시 크기 감소 비율과 성능 보존 측면에서 뚜렷한 차이를 보인다.

## C01 · CP
- 질문: 
- 요소: ['두 방법 각각', '차이']
- 컨텍스트: 2606.18394 JetSpec: Breaking the Scaling Ceiling of Speculative Decodin · 2607.05147 DSpark: Confidence-Scheduled Speculative Decoding with Semi-
- 답:

서론
Speculative decoding은 드래프트 생성 방식(parallel vs autoregressive)에 따라 모델 속도와 수용률이 크게 달라집니다. 기존 방법들은 병렬 드래프팅의 효율성과 인과적 조건화를 동시에 만족하기 어려워 성능 한계에 직면해 있었습니다[2606.18394v5][2607.05147v1].

본론
1. JetSpec: 단일 전방 통과에서 동결된 타겟 모델로부터 융합된 숨겨진 특징을 추출하고, 병렬‑인과적 조건화를 적용한 드래프트 헤드를 학습시켜 고품질 후보 트리를 생성합니다[2606.18394v5].
2. DSpark: 높은 처리량을 갖는 평행 백본과 경량 순차 모듈이 결합된 반자동회귀 구조를 사용해 블록 내 의존성을 모델링하고, 신뢰도 기반 동적 검증 길이를 설정함으로써 드래프트 품질을 유지하면서 수용률을 높입니다[2607.05147v1].

결론
JetSpec은 병렬 트리 드래프팅을 통해 더 큰 드래프트 예산을 긴 수용 가능한 접두사로 변환하고, 전체 엔드투엔드 속도 향상을 달성한다[2606.18394v5]. DSpark는 오프라인 벤치마크에서 기존 자동회귀 및 병렬 드래퍼보다 수용 길이를 크게 향상시킨다[2607.05147v1]. 두 방법은 각각 다른 접근법으로 성능을 개선하지만, 구체적인 수치나 조건에 따라 결과가 달라진다.

- 인용 블록(근거 대조용):

  > [문서 1] [Distance: 0.4291] [발행일: 2026-06-16] [2606.18394v5] JetSpec: Breaking the Scaling Ceiling of Speculative Decoding with Parallel Tree Drafting [초록] Speculative decoding (SD) accelerates autoregressive Large Language Models (LLMs) by drafting multiple tokens and verifying them in parallel, but it faces a scaling limitation: increasing the draft budget improves speed only when acceptance remains high and drafting overhead stays low. This ceiling has been difficult to break because prior head-based SD methods face a causality-efficiency dilemma. Autoregressive drafters produce path-conditioned candidates that are effective for tree speculative decoding with higher acceptance length, but their drafting cost grows with tree depth. Bidirectional block-diffusion drafters generate all positions in one pass, but their branch-agnostic marginals can form individually plausible yet mutually inconsistent trees, wasting budget and reducing acceptance. We propose JetSpec, a head-based SD framework that combines one-forward drafting efficiency with branch-wise causal conditioning. JetSpec trains a causal parallel draft head over fused hidden states from the frozen target model, producing candidate trees whose scores align with the target model's autoregressive factorization. This enables JetSpec to convert larger draft budgets into longer accepted prefixes and higher end-to-end speedup. Across math, coding, and chat benchmarks on dense and MoE Qwen3 models, JetSpec consistently outperforms bidirectional-head and tree-based SD baselines. On H100 GPUs, JetSpec achieves up to 9.64x speedup on MATH-500 and 4.58x on open-ended conversational workloads, with further latency gains demonstrated through vLLM integration under realistic serving loads. Our code and models are available at https://github.com/hao-ai-lab/JetSpec. Figure 3: JetSpec design overview. JetSpec extracts fused hidden features from the frozen target model and conditions a causal-parallel draft head to generate high-quality candidate trees in one forward pass.

  > [문서 2] [Distance: 0.3916] [발행일: 2026-07-06] [2607.05147v1] DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation [초록] Speculative decoding accelerates Large Language Model (LLM) inference by decoupling draft generation from target verification. While recent parallel drafters efficiently propose long token sequences in a single forward pass, they suffer from rapid acceptance decay due to a lack of inter-token dependencies. Furthermore, indiscriminately verifying these extended blocks wastes critical batch capacity on tokens with high rejection risks, severely degrading throughput in high-concurrency serving systems. We introduce DSpark, a speculative decoding framework that unifies high-throughput parallel generation with adaptive, load-aware verification. To maintain draft quality, DSpark utilizes a semi-autoregressive architecture, coupling a parallel backbone with a lightweight sequential module, to introduce intra-block dependency modeling and mitigate suffix decay. To optimize system efficiency, DSpark employs confidence-scheduled verification, dynamically tailoring the verification length for each request based on estimated prefix survival probabilities and engine-specific throughput profiles. On offline benchmarks across diverse domains, DSpark substantially improves the accepted length over state-of-the-art autoregressive and parallel drafters. When deployed within the DeepSeek-V4 serving system under live user traffic, DSpark successfully mitigates verification waste. Compared to the established production baseline (MTP-1), DSpark accelerates per-user generation speeds by 60 to 85 percent at matched throughput levels. More importantly, by preventing severe throughput degradation under strict interactivity constraints, it enables performance tiers that were previously unattainable, shifting the Pareto frontier of our serving system. ## **5. Real-World Deployment of DSpark** While Section 4 establishes the algorithmic gains of DSpark on offline benchmarks, deploying it alongside large-scale models like DeepSeek-V4 (DeepSeek-AI, 2026) introduces additional 15

## C07 · CP
- 질문: 
- 요소: ['두 방법 각각', '차이']
- 컨텍스트: 2503.23157 Reasoning-SQL: Reinforcement Learning with SQL Tailored Part · 2410.01066 From Natural Language to SQL: Review of LLM-based Text-to-SQ · 2412.12522 Solid-SQL: Enhanced Schema-linking based In-context Learning · 2502.20657 Automatic database description generation for Text-to-SQL · 2503.21602 GenEdit: Compounding Operators and Continuous Improvement to
- 답:

서론
Text-to‑SQL은 자연어 이해, 스키마 해석 및 정확한 SQL 생성이라는 여러 추론 집약적 하위 작업을 포함해 매우 어려운 과제이다[2503.23157v2]. 이러한 복잡성 때문에 모델이 스스로 논리적 사고를 강화하고 일반화 능력을 높이는 방법이 필요하다.

본론
1. Reasoning‑SQL: 스키마 링크, AI 피드백, n‑그램 유사도 및 문법 검사 등 부분 보상(reward)을 설계해 보강된 RL 학습으로 LLM이 내재적 추론 기술을 개발하도록 유도한다[2503.23157v2].
2. Solid‑SQL: 사전 처리 단계에서 LLM 기반 데이터 증폭에 의해 강화된 스키마 링크 모델을 훈련하고, 구조 유사성 예시 검색을 이용한 두 라운드 인컨텍스트 학습 전략을 도입해 시스템 견고성을 높인다[2412.12522v1].

결론
Reasoning-SQL은 RL 기반 훈련으로 BIRD 벤치마크에서 o3-mini보다 4%, Gemini-1.5-Pro-002보다 3% 높은 성능을 보이며, 기존 접근법보다 일반화 능력이 뛰어나다 [2503.23157v2]. Solid-SQL은 스키마 연결 기반 인-컨텍스트 학습을 통해 Spider와 Bird 벤치마크에서 각각 82.1%와 58.9%의 SQL 실행 정확도를 달성하고, 적대적 교란이 가해진 데이터셋에서도 기존 기법보다 평균 11.6% 향상된 결과를 보인다 [2412.12522v1]. 두 방법은 모두 Text-to-SQL 성능 향상에 기여하지만, Reasoning-SQL은 RL 보상 설계에 초점을 맞추어 벤치마크에서 큰 점수 차이를 보이고, Solid-SQL은 스키마 연결과 인-컨텍스트 학습을 통해 일반 데이터와 교란된 데이터 모두에서 높은 정확도와 강인함을 제공한다.

## C05 · CP
- 질문: 
- 요소: ['두 방법 각각', '차이']
- 컨텍스트: 2406.15927 Semantic Entropy Probes: Robust and Cheap Hallucination Dete · 2310.18344 Chainpoll: A high efficacy method for LLM hallucination dete
- 답:

서론
LLM 기반 환각 탐지는 모델 생성된 내용이 사실과 다르더라도 그럴듯하게 들릴 수 있어, 신뢰성 있는 자동 검출 방법이 필요합니다. 기존 방법들은 계산 비용이나 데이터 수집의 어려움 때문에 실용화에 한계가 있었습니다.

본론
1. Semantic Entropy Probes (SEPs): 단일 세대(hidden state)에서 직접 semantic entropy를 근사하여 훈련이 간단하고 테스트 시 다중 샘플링 없이도 거의 제로 오버헤드로 불확실성을 정량화합니다[2406.15927v1].
2. ChainPoll: ChainPoll은 새로운 환각 탐지 메트릭을 도입해 모든 RealHall 벤치마크에서 AUROC 0.781의 성능을 보이며, 기존 이론적 방법보다 11% 높고 산업 표준보다 23% 초과하는 결과를 달성했습니다[2310.18344v1].

결론
ChainPoll은 RealHall 벤치마크에서 전체 AUROC가 0.781이며, 이는 다음으로 좋은 이론적 방법보다 11% 높고 산업 표준보다 23% 더 높은 성능을 보였습니다[2310.18344v1]. Semantic Entropy Probes(SEP)는 이전 탐지 방법보다 오스트라이버전 데이터에 대해 더 잘 일반화되며 높은 성능을 유지한다는 결과가 있습니다[2406.15927v1]. 따라서 두 방법은 모두 환각 탐지에서 높은 성능을 보이지만, ChainPoll은 구체적인 벤치마크 수치와 산업 표준 대비 우위를 제시하고, SEP은 일반화 능력과 비용 효율성을 강조하는 점에서 평가 기준이 다릅니다.

## N08 · NU
- 질문: 
- 요소: ['수치 25 · 50']
- 컨텍스트: 2604.00314 Prompt-Guided Prefiltering for VLM Image Compression · 2412.08771 LLaVA-Zip: Adaptive Visual Token Compression with Intrinsic  · 2604.00886 PixelPrune: Pixel-Level Adaptive Visual Token Reduction via  · 2607.12756 VisCo: Leveraging Large Language Models as Intrinsic Encoder
- 답:

서론
VLM에 이미지를 업로드할 때 프롬프트를 기반으로 이미지 내 중요한 영역은 유지하고 덜 관련된 부분을 압축하는 방법이 필요합니다. 이러한 프롬프트‑가이드된 사전 필터링이 비트레이트 감소와 작업 정확도 보존을 동시에 달성하려면 어떻게 구현되는지 파악해야 합니다.

본론
1. Prompt-Guided Prefiltering: 텍스트 프롬프트에 가장 관련 있는 이미지 영역을 식별하여 중요한 디테일을 유지하고 덜 관련된 부분을 부드럽게 압축함으로써 코덱‑무관(preprocessor)으로 적용됩니다[2604.00314v1]. 비트레이트 감소: 여러 VQA 벤치마크에서 평균 비트레이트를 25~50% 줄이면서 작업 정확도는 동일하게 유지했습니다[2604.00314v1].
결론
프롬프트를 이용해 이미지 내 중요 영역을 보존하고 나머지 부분을 압축하는 Prompt‑Guided Prefiltering 방법은 비트레이트를 최대 50 %까지 감소시키면서도 VLM의 downstream task 성능에 영향을 주지 않습니다.

- 인용 블록(근거 대조용):

  > [문서 1] [Distance: 0.4325] [발행일: 2026-03-31] [2604.00314v1] Prompt-Guided Prefiltering for VLM Image Compression [초록] The rapid progress of large Vision-Language Models (VLMs) has enabled a wide range of applications, such as image understanding and Visual Question Answering (VQA). Query images are often uploaded to the cloud, where VLMs are typically hosted, hence efficient image compression becomes crucial. However, traditional human-centric codecs are suboptimal in this setting because they preserve many task-irrelevant details. Existing Image Coding for Machines (ICM) methods also fall short, as they assume a fixed set of downstream tasks and cannot adapt to prompt-driven VLMs with an open-ended variety of objectives. We propose a lightweight, plug-and-play, prompt-guided prefiltering module to identify image regions most relevant to the text prompt, and consequently to the downstream task. The module preserves important details while smoothing out less relevant areas to improve compression efficiency. It is codec-agnostic and can be applied before conventional and learned encoders. Experiments on several VQA benchmarks show that our approach achieves a 25-50% average bitrate reduction while maintaining the same task accuracy. Our source code is available at https://github.com/bardia-az/pgp-vlm-compression. preserve task-relevant image regions. To the best of our knowledge, this is the first compression framework for VLMs that adapts to the specific language prompt. _•_ The proposed method is **lightweight and codec-agnostic**, designed for seamless edge deployment. It operates as a plug-and-play preprocessor compatible with conventional and learned codecs, requiring no modifications to the encoder or cloud-based decoder. _•_ Extensive evaluations on two VLM backbones and three

## N04 · NU
- 질문: 
- 요소: ['수치 7 · 8']
- 컨텍스트: 2605.20049 Does Code Cleanliness Affect Coding Agents? A Controlled Min
- 답:

서론
코드 깔끔함(cleanliness) 이 코딩 에이전트의 성능에 미치는 영향을 파악하는 것은, 코드 구조와 스타일 차이가 작업 완료율뿐만 아니라 자원 소모에도 차이를 만들 수 있기 때문에 어려운 문제입니다. 특히 토큰 사용량과 파일 재방문 횟수 같은 운영적 발자국을 정밀하게 측정해야 합니다.

본론
1. Minimal‑Pair Evaluation Protocol: 동일한 아키텍처와 의존성을 가지지만 정적 분석 규칙 위반 및 인지 복잡도가 다른 코드 저장소를 쌍으로 구성하고, 에이전트 파이프라인이 깨끗한 코드를 저하시키거나 더러운 코드를 정리하는 방식으로 33개의 작업을 설계했습니다. [2605.20049v1] Claude Sonnet 4.6 기반의 코드 청결도 실험에서, 에이전트가 깔끔한 코드를 다룰 때 토큰 사용량이 기존 대비 약 7~8% 감소하는 것으로 확인되었습니다. [2605.20049v1]
결론
제공된 연구에 따르면 깨끗하게 정리된 코드는Claude Code와 같은 코드­ing 에이전트의 토큰 소비량을 평균적으로 7에서 8퍼센트 정도 줄이는 효과를 보입니다. 이는 모델 선택이나 프롬프트 설계뿐만 아니라, 유지보수 원칙이 AI 기반 개발 환경에서도 여전히 중요한 요소임을 시사합니다.

## N11 · NU
- 질문: 
- 요소: ['수치 5 · 10']
- 컨텍스트: 2412.19754 Complement or substitute? How AI increases the demand for hu · 2412.19754 Complement or substitute? How AI increases the demand for hu
- 답:

서론
AI가 인간 노동에 대체·보완 역할을 하는지 파악하기 위해 채용공고를 분석한 연구에서, 회복탄력성(resilience)과 윤리(ethics) 같은 스킬이 있는 데이터 과학자의 연봉 프리미엄을 확인하는 것이 핵심 질문입니다. 이러한 스킬은 AI 도입 시 요구되는 인간 능력으로 평가됩니다.

본론
1. AI‑포커스 역할 분석: 연구는 2018~2023년 미국 온라인 채용공고 약 1,200만 개를 활용해 “내부 효과”와 “외부 효과” 두 가지 접근법으로 AI가 인간 노동에 대체인지 보완인지를 조사했습니다. [2412.19754v3]
- 회복탄력성·민첩성·분석적 사고 등 보충 스킬이 필요 없는 역할보다 AI‑포커스 역할을 요구하는 경우가 거의 두 배였습니다. 데이터 과학자가 회복탄력성을 갖추면 연봉에 약 5%의 추가가, 윤리 능력을 갖출 경우 8%까지 더 높은 급여를 받는 것으로 나타났습니다. [2412.19754v3]

결론
제공된 문서에 따르면, 회복탄력성(resilience)을 갖춘 데이터 과학자는 연봉이 5~10% 더 높은 것으로 보고된다[2412.19754v3]. 이는 AI 수요가 증가함에 따라 보완적 스킬을 가진 인재에게 임금 프리미엄이 발생한다는 연구 결과와 일치한다. 따라서 AI는 회복탄력성 같은 인간 스킬의 수요를 늘리고, 해당 스킬을 보유한 데이터 과학자에게 상당한 연봉 상승 효과를 제공한다.

## N10 · NU
- 질문: 
- 요소: ['수치 55 · 40']
- 컨텍스트: 2605.00789 Make Your LVLM KV Cache More Lightweight
- 답:

서론
Large Vision-Language Model (LVLM) 의 KV 캐시와 비전 토큰 사용량을 줄이는 것은 모델 효율성을 높이기 위해 중요한 과제이다. 특히, 기존 방식에 비해 적은 시각 정보를 유지하면서도 연산 비용을 크게 감소시키는 방법이 필요하다.

본론
1. LightKV: 55%의 원본 비전 토큰만을 사용하여 KV 캐시 크기를 절반으로 줄이고, 최대 40%까지 연산을 절감한다[2605.00789v1].

결론
따라서 LightKV는 전체 시각 정보를 약 55%만 활용하면서도 기존 모델 대비 연산량을 최고 40% 감소시킨다.

## MS1 · MS
- 질문: 
- 요소: ['원 논문이 DB 에 없다고 밝힘(지어내지 않음)']
- DB 에 없는 원 논문: 2302.00093
- 컨텍스트: 2502.05252 GSM-Infinite: How Do Your LLMs Behave over Infinitely Increa · 2502.13442 TreeCut: A Synthetic Unanswerable Math Word Problem Dataset 
- 답:

서론
제공된 문서에는 질문이 찾는 연구가 없습니다.

본론
1. GSM-Infinite: grade school math problem generator를 이용해 무한 난이도와 컨텍스트 길이를 갖는 산술 문제를 생성하고, 이를 통해 LLM의 추론 성능을 평가한다[2502.05252v1]
2. TreeCut: 트리 구조로 수학 문제와 그 조건 중 일부만 제거해 만들어 불응답 가능한 수학적 단어를 데이터셋으로 만들고, 이 데이터를 이용해 GPT‑4o·o3‑mini 등 대형 언어 모델이 환각 현상을 보이는 비율을 측정한다[2502.13442v2]

결론
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• GSM-Plus: A Comprehensive Benchmark for Evaluating the Robustness of LLMs as Mathematical Problem Solvers (2024) [2402.19255]

## MS2 · MS
- 질문: 
- 요소: ['원 논문이 DB 에 없다고 밝힘(지어내지 않음)']
- DB 에 없는 원 논문: 2212.10496
- 컨텍스트: 2603.08429 One Model Is Enough: Native Retrieval Embeddings from LLM Ag · 2602.07297 Progressive Searching for Retrieval in RAG · 2603.08819 Beyond Relevance: On the Relationship Between Retrieval and  · 2406.15187 UDA: A Benchmark Suite for Retrieval Augmented Generation in · 2511.01386 RAGSmith: A Framework for Finding the Optimal Composition of
- 답:

서론
HyDE(Hypothetical Document Embedding)는 가상 문서를 생성해 이를 임베딩한 뒤 검색하는 방식인데, 기존에 텍스트 기반 쿼리만 사용해 매칭하던 방법보다 정밀도가 높아집니다. 그러나 LLM이 직접 문서를 만들어야 하므로 추가적인 비용과 모델 설계가 필요합니다.

본론
1. HyDE: Gao et al.(2022)은 검색을 위해 가상의 답변 텍스트를 생성하고, 그 응답에 해당하는 임베딩 벡터를 사용해 문서와 매칭함으로써 쿼리‑문서 일치도를 향상시킵니다[2511.01386v1].
HyDE는 LLM의 생성 능력을 활용해 직접적인 질료·문서 매칭 대신 합성된 답변을 먼저 만들고 이를 임베딩해 검색합니다. 기존의 “검색 쿼리 텍스트 → 별도의 임베딩 모델로 벡터화”라는 두 단계 방식과 달리, HyDE는 더 많은 텍스트를 생성하지 않고도 LLM이 직접 가상의 답변을 만들어 이를 바로 사용하므로 추가적인 검색 비용 없이 정밀도를 높입니다[2511.01386v1].

결론
HyDE는 가상 문서를 먼저 만들고 그 임베딩으로 문서와 매칭하는 방식으로 작동하며, 기존 파이프라인보다 높은 정확도와 효율성을 제공합니다. 다만 LLM이 직접 가상의 답변을 생성해야 하므로 추가적인 비용과 설계가 필요하다는 점이 제한 사항입니다[2511.01386v1].

- 인용 블록(근거 대조용):

  > [문서 5] [Distance: 0.2406] [발행일: 2025-11-03] [2511.01386v1] RAGSmith: A Framework for Finding the Optimal Composition of Retrieval-Augmented Generation Methods Across Datasets [초록] Retrieval-Augmented Generation (RAG) quality depends on many interacting choices across retrieval, ranking, augmentation, prompting, and generation, so optimizing modules in isolation is brittle. We introduce RAGSmith, a modular framework that treats RAG design as an end-to-end architecture search over nine technique families and 46{,}080 feasible pipeline configurations. A genetic search optimizes a scalar objective that jointly aggregates retrieval metrics (recall@k, mAP, nDCG, MRR) and generation metrics (LLM-Judge and semantic similarity). We evaluate on six Wikipedia-derived domains (Mathematics, Law, Finance, Medicine, Defense Industry, Computer Science), each with 100 questions spanning factual, interpretation, and long-answer types. RAGSmith finds configurations that consistently outperform naive RAG baseline by +3.8\% on average (range +1.2\% to +6.9\% across domains), with gains up to +12.5\% in retrieval and +7.5\% in generation. The search typically explores $\approx 0.2\%$ of the space ($\sim 100$ candidates) and discovers a robust backbone -- vector retrieval plus post-generation reflection/revision -- augmented by domain-dependent choices in expansion, reranking, augmentation, and prompt reordering; passage compression is never selected. Improvement magnitude correlates with question type, with larger gains on factual/long-answer mixes than interpretation-heavy sets. These results provide practical, domain-aware guidance for assembling effective RAG systems and demonstrate the utility of evolutionary search for full-pipeline optimization. 5. **Hypothetical Document Embedding** : The HyDE method, introduced by Gao et al. (2022), advances retrieval performance by leveraging the generative capacity of large language models. Instead of relying exclusively on direct query–document matching, HyDE prompts the model to generate a hypothetical answer that represents a plausible response to the query. This synthesized answer is then embedded and used to retrieve documents semantically aligned with the generated text

## MS3 · MS
- 질문: 
- 요소: ['원 논문이 DB 에 없다고 밝힘(지어내지 않음)']
- DB 에 없는 원 논문: 2305.06983
- 컨텍스트: 2412.01572 MBA-RAG: a Bandit Approach for Adaptive Retrieval-Augmented  · 2412.07618 Adapting to Non-Stationary Environments: Multi-Armed Bandit  · 2602.20735 RMIT-ADM+S at the MMU-RAG NeurIPS 2025 Competition · 2505.07233 DynamicRAG: Leveraging Outputs of Large Language Model as Fe
- 답:

서론
제공된 문서에는 질문이 찾는 연구가 없습니다.

본론
1. MBA-RAG: 다중‑아ーム 밴딧 알고리즘과 동적 보상 함수를 이용해 쿼리 복잡도에 따라 가장 적합한 검색 전략을 선택하고, 탐색·활용 균형을 유지하며 효율성을 높입니다[2412.01572v4].
2. Multi-Armed Bandit enhanced RAG: 각 검색 방법을 별도의 “arm”으로 취급하여 실시간 사용자 피드백과 과거 다목적 성능에 기반해 동적 환경에서 적절한 전략을 선택합니다[2412.07618v2].

결론
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• Chain-of-Retrieval Augmented Generation (2025) [2501.14342]
• Retrieval-Augmented Generation for AI-Generated Content: A Survey (2026) [2402.19473]
• Retrieval-Augmented Generation for Large Language Models: A Survey (2023) [2312.10997]
• Retrieval-Augmented Generation (RAG): Advances and Challenges (2025) https://doi.org/10.7546/pecr.83.25.03

## MS4 · MS
- 질문: 
- 요소: ['원 논문이 DB 에 없다고 밝힘(지어내지 않음)']
- DB 에 없는 원 논문: 2305.14627
- 컨텍스트: 2509.21557 Generation-Time vs. Post-hoc Citation: A Holistic Evaluation
- 답:

서론
제공된 문서에는 질문이 찾는 연구가 없습니다.

본론
1. Generation-Time Citation (G-Cite): 답변과 인용을 한 번의 패스에서 동시에 생성하는 방식을 도입하고, 포괄적인 평가와 증거 기반 권장사항을 제시한다[2509.21557v2]. 초안 작성 후 적절한 출처를 추가하거나 검증하도록 하는 두 번째 패러다임을 정의하며, 높은 커버리지와 경쟁력 있는 정확도·적당한 지연 시간을 제공한다[2509.21557v2].
결론
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• Auto-Judge: A Cross-Task Benchmark for Comparing LLM Judges for Citation-Grounded RAG Systems (2026) https://doi.org/10.1145/3805712.3808601
• Abstention vs. Hallucination: Benchmarking LLM Source Attribution for Scientific Citations (2024) [2405.02228]
• RAGBench: Explainable Benchmark for Retrieval-Augmented Generation Systems (2024) [2407.11005]
• Citation-Enforced RAG Architecture for Decision Support (2026) https://doi.org/10.26507/paper.4966

## NM1E · NM · en
- 질문: 
- 요소: ['Self-RAG 가 무엇인지', '핵심 방법']
- 컨텍스트: 2310.11511 Self-RAG: Learning to Retrieve, Generate, and Critique throu
- 답:

서론
대형 언어 모델(LLM)은 파라메트릭 지식에만 의존해 사실 오류가 발생하기 쉽습니다. 이를 보완하려면 관련 지식을 검색하고 생성 과정을 스스로 평가할 수 있는 메커니즘이 필요합니다. 이러한 요구를 충족하는 것이 Self‑RAG입니다.

본론
1. Self-Reflective Retrieval-Augmented Generation (Self-RAG): 단일 임의 LLM을 학습시켜 필요 시 관련 문서를 검색하고, 특수 토큰인 ‘reflection token’으로 생성된 답변과 해당 문서에 대해 스스로 비판·반성하도록 합니다[2310.11511v1].

결론
따라서 Self‑RAG는 retrieval와 self-reflection을 결합한 프레임워크로, LLM의 사실 정확성과 응답 품질을 향상시키는 것이 핵심 목표입니다.

- 인용 블록(근거 대조용):

  > [문서 1] [Distance: 0.2000] [발행일: 2023-10-17] [2310.11511v1] Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection [초록] Despite their remarkable capabilities, large language models (LLMs) often produce responses containing factual inaccuracies due to their sole reliance on the parametric knowledge they encapsulate. Retrieval-Augmented Generation (RAG), an ad hoc approach that augments LMs with retrieval of relevant knowledge, decreases such issues. However, indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility or can lead to unhelpful response generation. We introduce a new framework called Self-Reflective Retrieval-Augmented Generation (Self-RAG) that enhances an LM's quality and factuality through retrieval and self-reflection. Our framework trains a single arbitrary LM that adaptively retrieves passages on-demand, and generates and reflects on retrieved passages and its own generations using special tokens, called reflection tokens. Generating reflection tokens makes the LM controllable during the inference phase, enabling it to tailor its behavior to diverse task requirements. Experiments show that Self-RAG (7B and 13B parameters) significantly outperforms state-of-the-art LLMs and retrieval-augmented models on a diverse set of tasks. Specifically, Self-RAG outperforms ChatGPT and retrieval-augmented Llama2-chat on Open-domain QA, reasoning and fact verification tasks, and it shows significant gains in improving factuality and citation accuracy for long-form generations relative to these models. ## ABSTRACT Despite their remarkable capabilities, large language models (LLMs) often produce responses containing factual inaccuracies due to their sole reliance on the parametric knowledge they encapsulate. Retrieval-Augmented Generation (RAG), an ad hoc approach that augments LMs with retrieval of relevant knowledge, decreases such issues

## NM3E · NM · en
- 질문: 
- 요소: ['중간 위치 정보 성능 저하 결과', 'U자 곡선']
- 컨텍스트: 2307.03172 Lost in the Middle: How Language Models Use Long Contexts · 2410.14641 Distance between Relevant Information Pieces Causes Bias in  · 2404.16811 Make Your LLM Fully Utilize the Context · 2403.04797 Found in the Middle: How Language Models Use Long Contexts B · 2406.16008 Found in the Middle: Calibrating Positional Attention Bias I
- 답:

서론
긴 입력 컨텍스트에서 중간에 위치한 관련 정보를 활용하지 못하는 현상은 lost‑in‑the‑middle 문제라고 불리며, 현재 언어 모델들이 이러한 정보의 위치 변화에도 불구하고 성능이 크게 저하되는 것으로 알려져 있습니다[2307.03172v3]. 이는 긴 문맥을 처리하는 데 있어 여전히 해결되지 않은 핵심 과제입니다.

본론
1. Lost in the Middle: 관련 정보가 입력 컨텍스트 중간에 있을 때 언어 모델의 수행 능력이 현저히 감소하며, 초기·최종 위치에서는 성능이 가장 높게 나타납니다[2307.03172v3].
2. LongPiBench Benchmark: 다중 관련 정보 조각을 포함한 벤치마크를 통해 현재 대부분의 모델은 “lost in the middle”에 비교적 견고하지만, 관련 정보가 서로 다른 위치에 있을 때 공간적 편향이 존재한다는 것을 확인했습니다[2410.14641v3].

결론
Lost in the Middle 논문은 관련 정보가 입력 컨텍스트의 중간에 위치할 때 모델 성능이 크게 저하된다는 결과를 제시한다[2307.03172v3]. 반면, Distance between Relevant Information Pieces Causes Bias in Long-Context LLMs는 대부분의 현재 모델이 "lost in the middle" 문제에 대해 견고함을 보여주지만, 관련 정보 조각 사이의 간격과 관련된 유의미한 편향이 존재한다고 보고한다[2410.14641v3]. 따라서 두 연구는 동일한 현상을 관찰하지만, Lost in the Middle은 성능 저하를 강조하고, Distance between Relevant Information Pieces는 모델의 전반적인 견고성과 함께 정보 간 거리로 인한 편향을 추가로 지적한다는 점에서 결론이 다르다.

- 인용 블록(근거 대조용):

  > [문서 1] [Distance: 0.3043] [발행일: 2023-07-06] [2307.03172v3] Lost in the Middle: How Language Models Use Long Contexts [초록] While recent language models have the ability to take long contexts as input, relatively little is known about how well they use longer context. We analyze the performance of language models on two tasks that require identifying relevant information in their input contexts: multi-document question answering and key-value retrieval. We find that performance can degrade significantly when changing the position of relevant information, indicating that current language models do not robustly make use of information in long input contexts. In particular, we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models. Our analysis provides a better understanding of how language models use their input context and provides new evaluation protocols for future long-context language models. . We find that performance can degrade significantly when changing the position of relevant information, indicating that current language models do not robustly make use of information in long input contexts. In particular, we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models

  > [문서 2] [Distance: 0.4091] [발행일: 2024-10-18] [2410.14641v3] Distance between Relevant Information Pieces Causes Bias in Long-Context LLMs [초록] Positional bias in large language models (LLMs) hinders their ability to effectively process long inputs. A prominent example is the "lost in the middle" phenomenon, where LLMs struggle to utilize relevant information situated in the middle of the input. While prior research primarily focuses on single pieces of relevant information, real-world applications often involve multiple relevant information pieces. To bridge this gap, we present LongPiBench, a benchmark designed to assess positional bias involving multiple pieces of relevant information. Thorough experiments are conducted with five commercial and six open-source models. These experiments reveal that while most current models are robust against the "lost in the middle" issue, there exist significant biases related to the spacing of relevant information pieces. These findings highlight the importance of evaluating and reducing positional biases to advance LLM's capabilities. of information. 1 The minimal context size is 64k, but some tokenizers expand our 64k inputs to nearly 80k, exceeding the limit. We observe that both open-source and commercial models exhibit noticable biases toward different rela tive positions. In the case of _Code Completion_, this bias is prominent. As the relative positions of relevant information pieces shift from being fully adjacent to uniformly distributed across the context, the model’s

## T01E · SV · en
- 질문: 
- 요소: ['대표 연구 3편 이상', '연구 방향 정리']
- 컨텍스트: 2412.19925 HADES: Hardware Accelerated Decoding for Efficient Speculati · 2504.00030 Token-Driven GammaTune: Adaptive Calibration for Enhanced Sp · 2412.12639 Falcon: Faster and Parallel Inference of Large Language Mode · 2412.18910 AdaEAGLE: Optimizing Speculative Decoding via Explicit Model · 2605.20104 Draft Less, Retrieve More: Hybrid Tree Construction for Spec
- 답:

서론
Speculative decoding은 작은 draft 모델으로 토큰을 제안하고 큰 target 모델에서 병렬로 검증함으로써 LLM 추론 속도를 높이는 기법이지만, 최적의 speculation 길이와 draft 구조를 선택하는 것이 성능과 에너지 효율에 결정적인 영향을 미쳐 구현이 어렵습니다.

본론
1. HADES: 하드웨어 레벨에서 speculative decoding을 지원하도록 설계된 전용 가속기를 도입하여 검증 속도(A100 대비 6.99배, A6000 대비 7.74배)와 에너지 효율(각 GPU 대비 약 118~160배 향상)을 크게 개선했습니다. [2412.19925v2]
2. GammaTune / GammaTune+: 토큰 수용률을 기반으로 speculation 길이를 동적으로 조정하는 훈련‑없는 적응 알고리즘으로, 고정 길이 방식보다 평균 속도 향상을 각각 약 15%와 16%, 성능 변동성을 줄였습니다. [2504.00030v3]
3. Falcon: Coupled Sequential Glancing Distillation과 Custom-Designed Decoding Tree를 결합한 반‑자동회귀 speculative decoding 프레임워크로, drafter의 병렬성과 출력 품질을 동시에 향상시켜 Vicuna·LLaMA2‑Chat에서 손실 없는 2.91~3.51배 속도 향상을 달성했습니다. [2412.12639v3]
4. AdaEAGLE: Lightweight Draft Length Predictor(LDLP)를 이용해 최적의 draft 토큰 수를 예측하고, 정적 구조에 비해 컨텍스트‑인지 적응형 드래프트 구조로 1.62배 속도 향상을 보이며 출력 품질을 유지합니다. [2412.18910v1]

결론
제공된 문서들은 하드웨어 가속(HADES), 동적인 speculation 길이 조정(GammaTune/GammaTune+), 반자동회귀 및 커스텀 디코딩 트리(Falcon)와 적응형 드래프트 구조 예측(AdaEAGLE) 등 다양한 접근법을 통해 speculative decoding의 속도·에너지 효율과 안정성을 크게 향상시키고 있습니다. 이러한 연구들은 LLM 추론을 보다 빠르고 에너지‑효율적으로 만드는 최신 트렌드를 보여줍니다.

📎 DB 밖에서 찾은 관련 논문 (OpenAlex 검색 · 내용은 요약하지 않음)
• Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding (2024) [2401.07851]
• Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads (2024) [2401.10774]
• Speculative Decoding with CTC-based Draft Model for LLM Inference Acceleration (2024) [2412.00061]
• Self Speculative Decoding for Diffusion Large Language Models (2025) [2510.04147]

- 인용 블록(근거 대조용):

  > [문서 1] [Distance: 0.2669] [발행일: 2024-12-27] [2412.19925v2] HADES: Hardware Accelerated Decoding for Efficient Speculation in Large Language Models [초록] Large Language Models (LLMs) have revolutionized natural language processing by understanding and generating human-like text. However, the increasing demand for more sophisticated LLMs presents significant computational challenges due to their scale and complexity. This paper introduces Hardware Accelerated Decoding (HADES), a novel approach to enhance the performance and energy efficiency of LLMs. We address the design of an LLM accelerator with hardware-level speculative decoding support, a concept not previously explored in existing literature. Our work demonstrates how speculative decoding can significantly improve the efficiency of LLM operations, paving the way for more advanced and practical applications of these models. ## VII. CONCLUSIONS In this paper, we introduced the first specialized hardware support for speculative decoding in Large language models (LLMs). Our novel approach significantly enhances the performance and energy efficiency of LLM operations. Specifically, our hardware-accelerated speculative decoding achieves verification speeds that are 6.99 times and 7.74 times faster than those of the A100 and A6000 GPUs, respectively. Moreover, our approach demonstrates remarkable improvements in energy efficiency, being 117.95 times and 159.66 times more energy-efficient than the A100 and A6000 GPUs during the verification phase. These substantial gains highlight the potential of hardware-accelerated speculative decoding to overcome the computational challenges posed by large-scale LLMs, paving the way for more advanced and efficient applications in natural language processing.

  > [문서 2] [Distance: 0.2188] [발행일: 2025-03-28] [2504.00030v3] Token-Driven GammaTune: Adaptive Calibration for Enhanced Speculative Decoding [초록] Speculative decoding accelerates large language model (LLM) inference by using a smaller draft model to propose tokens, which are then verified by a larger target model. However, selecting an optimal speculation length is critical for maximizing speedup while minimizing wasted computation. We introduce \textit{GammaTune} and \textit{GammaTune+}, training-free adaptive algorithms that dynamically adjust speculation length based on token acceptance rates using a heuristic-based switching mechanism. Evaluated on SpecBench across multiple tasks and model pairs, our method outperforms other heuristic-based approaches and fixed-length speculative decoding, achieving an average speedup of 15\% ($\pm$5\%) with \textit{GammaTune} and 16\% ($\pm$3\%) with \textit{GammaTune+}, while reducing performance variance. This makes \textit{GammaTune} a robust and efficient solution for real-world deployment. ## **3 Background: Speculative Decoding** Leviathan et al. and Chen et al. proposed **speculative sampling** to accelerate inference in large language models by utilizing a smaller **draft model** to autoregressively sample tokens, while the larger **target model** verifies these tokens in parallel. This approach has been shown to produce sequences with the same distribution as those sampled directly

  > [문서 3] [Distance: 0.2445] [발행일: 2024-12-17] [2412.12639v3] Falcon: Faster and Parallel Inference of Large Language Models through Enhanced Semi-Autoregressive Drafting and Custom-Designed Decoding Tree [초록] Striking an optimal balance between minimal drafting latency and high speculation accuracy to enhance the inference speed of Large Language Models remains a significant challenge in speculative decoding. In this paper, we introduce Falcon, an innovative semi-autoregressive speculative decoding framework fashioned to augment both the drafter's parallelism and output quality. Falcon incorporates the Coupled Sequential Glancing Distillation technique, which fortifies inter-token dependencies within the same block, leading to increased speculation accuracy. We offer a comprehensive theoretical analysis to illuminate the underlying mechanisms. Additionally, we introduce a Custom-Designed Decoding Tree, which permits the drafter to generate multiple tokens in a single forward pass and accommodates multiple forward passes as needed, thereby boosting the number of drafted tokens and significantly improving the overall acceptance rate. Comprehensive evaluations on benchmark datasets such as MT-Bench, HumanEval, and GSM8K demonstrate Falcon's superior acceleration capabilities. The framework achieves a lossless speedup ratio ranging from 2.91x to 3.51x when tested on the Vicuna and LLaMA2-Chat model series. These results outstrip existing speculative decoding methods for LLMs, including Eagle, Medusa, Lookahead, SPS, and PLD, while maintaining a compact drafter architecture equivalent to merely two Transformer layers. Cai, T.; Li, Y.; Geng, Z.; Peng, H.; Lee, J. D.; Chen, D.; and Dao, T. 2024. Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads. arXiv:2401.10774. Chen, C.; Borgeaud, S.; Irving, G.; Lespiau, J.-B.; Sifre, L.; and Jumper, J. 2023. Accelerating Large Language Model Decoding with Speculative Sampling. arXiv:2302.01318.

  > [문서 4] [Distance: 0.2213] [발행일: 2024-12-25] [2412.18910v1] AdaEAGLE: Optimizing Speculative Decoding via Explicit Modeling of Adaptive Draft Structures [초록] Speculative Decoding (SD) is a popular lossless technique for accelerating the inference of Large Language Models (LLMs). We show that the decoding speed of SD frameworks with static draft structures can be significantly improved by incorporating context-aware adaptive draft structures. However, current studies on adaptive draft structures are limited by their performance, modeling approaches, and applicability. In this paper, we introduce AdaEAGLE, the first SD framework that explicitly models adaptive draft structures. AdaEAGLE leverages the Lightweight Draft Length Predictor (LDLP) module to explicitly predict the optimal number of draft tokens during inference to guide the draft model. It achieves comparable speedup results without manual thresholds and allows for deeper, more specialized optimizations. Moreover, together with threshold-based strategies, AdaEAGLE achieves a $1.62\times$ speedup over the vanilla AR decoding and outperforms fixed-length SotA baseline while maintaining output quality. - Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre, and John Jumper. 2023. Accelerating large language model decoding with speculative sampling. _Preprint_ , arXiv:2302.01318.

## C02E · CP · en
- 질문: 
- 요소: ['두 방법 각각', '차이']
- 컨텍스트: 2506.18879 CommVQ: Commutative Vector Quantization for KV Cache Compres · 2605.00789 Make Your LVLM KV Cache More Lightweight
- 답:

서론
KV 캐시 압축은 긴 컨텍스트를 처리하는 대형 언어 모델(LLM)과 대규모 비전‑언어 모델(LVLM)에서 GPU 메모리 사용량을 크게 줄이기 위해 필요한 핵심 과제이다. 그러나 각 방법마다 적용 대상, 구현 방식 및 성능에 차이가 있다.

본론
1. CommVQ: 가법 양자화와 경량 인코더·코드북을 도입해 KV 캐시를 압축하고, RoPE와 교환 가능한 코드북 설계로 디코딩 비용을 낮추며 EM 알고리즘으로 학습한다[2506.18879v1].
2. LightKV: 비전 토큰 임베디드 간의 중복성을 활용해 텍스트 프롬프트에 의해 교차‑모달 메시지 전달을 통해 정보를 집계하고, 프리필 단계에서 점진적으로 압축함으로써 KV 캐시 크기를 절반으로 줄이고 연산량을 최대 40% 감소시킨다[2605.00789v1].

결론
LightKV는 시각 토큰 임베딩 간의 중복성을 활용해 KV 캐시 크기를 절반으로 줄이고, 기존 기법보다 성능을 크게 향상시킨다[2605.00789v1]. 반면 CommVQ는 2비트 양자화를 통해 FP16 KV 캐시 크기를 87.5% 감소시키며, 기존 양자화 방법들을 능가한다[2506.18879v1]. 두 방법은 각각 시각 토큰과 일반 토큰에 초점을 맞추어 서로 다른 압축 비율과 성능을 달성한다.

- 인용 블록(근거 대조용):

  > [문서 1] [Distance: 0.3273] [발행일: 2025-06-23] [2506.18879v1] CommVQ: Commutative Vector Quantization for KV Cache Compression [초록] Large Language Models (LLMs) are increasingly used in applications requiring long context lengths, but the key-value (KV) cache often becomes a memory bottleneck on GPUs as context grows. To address this, we propose Commutative Vector Quantization (CommVQ) to significantly reduce memory usage for long-context LLM inference. We first introduce additive quantization with a lightweight encoder and codebook to compress the KV cache, which can be decoded via simple matrix multiplication. To further reduce computational costs during decoding, we design the codebook to be commutative with Rotary Position Embedding (RoPE) and train it using an Expectation-Maximization (EM) algorithm. This enables efficient integration of decoding into the self-attention mechanism. Our approach achieves high accuracy with additive quantization and low overhead via the RoPE-commutative codebook. Experiments on long-context benchmarks and GSM8K show that our method reduces FP16 KV cache size by 87.5% with 2-bit quantization, while outperforming state-of-the-art KV cache quantization methods. Notably, it enables 1-bit KV cache quantization with minimal accuracy loss, allowing a LLaMA-3.1 8B model to run with a 128K context length on a single RTX 4090 GPU. The source code is available at: https://github.com/UMass-Embodied-AGI/CommVQ. compressing the KV cache. However, their achieved compression rate is relatively modest, and their basic decodethen-self-attention process introduces significant computational overhead, limiting its practicality for serving longcontext LLMs. There remains a lack of in-depth research on how to optimize vector quantization and better integrate it with self-attention for both more efficient and effective KV cache compression. **3. Preliminaries** **3.1. Self-Attention and KV Cache**

  > [문서 2] [Distance: 0.3227] [발행일: 2026-05-01] [2605.00789v1] Make Your LVLM KV Cache More Lightweight [초록] Key-Value (KV) cache has become a de facto component of modern Large Vision-Language Models (LVLMs) for inference. While it enhances decoding efficiency in Large Language Models (LLMs), its direct adoption in LVLMs introduces substantial GPU memory overhead due to the large number of vision tokens processed during the prefill stage. To tackle this problem, we propose LightKV, a novel approach that reduces KV cache size by exploiting the redundancy among vision-token embeddings. Guided by text prompts, LightKV employs cross-modality message passing to aggregate informative messages across vision tokens and progressively compress them during prefill. This prompt-aware guidance distinguishes our method from prior vision-only compression strategies. We evaluate LightKV on eight open-source LVLMs across eight public benchmark datasets, e.g., MME and SeedBench. Experimental results demonstrate that with only 55% of the original vision tokens, LightKV (a) halves the vision-token KV cache size, (b) reduces computation by up to 40%, and (c) preserves general-purpose performance while significantly outperforming existing baselines. . In contrast, methods from (b) improve KV cache size by pruning or merging tokens based either on minimal importance (Zhang et al., 2023b; Li et al., 2024d; Cai et al., 2024) or attention consistency across layers (Liu et al., 2023b; 2024d; Yang et al., 2024). Beyond LLMs, some initial efforts have been devoted to optimizing the KV cache for LVLMs

## N10E · NU · en
- 질문: 
- 요소: ['수치 55 · 40']
- 컨텍스트: 
- 답:



## MU1E · MU · en
- 질문: 
- 요소: ['E1', 'E2', 'E3']
- 컨텍스트: 2507.18857 PrismRAG: Boosting RAG Factuality with Distractor Resilience · 2601.07226 Lost in the Noise: How Reasoning Models Fail with Contextual · 2601.01896 Tackling the Inherent Difficulty of Noise Filtering in RAG · 2506.05154 Resisting Contextual Interference in RAG via Parametric-Know · 2510.09710 SeCon-RAG: A Two-Stage Semantic Filtering and Conflict-Free 
- 답:

서론
검색된 문서에 관련 없는 내용(예: 다른 회사의 정보) 이 포함되면, 생성 모델은 이를 사실로 잘못 인용할 위험이 커집니다. 이러한 현상은 검색 결과의 품질과 신뢰성을 크게 떨어뜨리는 주요 원인입니다.

본론
1. PrismRAG: 금전 증거와 미묘한 방해 문서를 혼합한 QA 쌍으로 모델을 학습시켜, 혼란스러운 반‑관련 정보를 포함한 상황에서도 모델이 사실에 기반해 답변하도록 합니다[2507.18857v1].
2. NoisyBench: 랜덤 문서·무관 채팅 기록 등 다양한 소음 유형을 포함하는 벤치마크를 구축하여 RAG 및 추론 작업에서 모델의 견고성을 평가하고, 방해 문서를 의도적으로 섞어 성능 저하 정도(최대 80% 하락) 를 측정합니다[2601.07226v1].
3. Knowledgeable‑R1: 파라메트릭 지식(PK) 을 활용해 잘못된·관련 없는 검색 텍스트에 대한 간섭을 견디도록 강화학습 프레임워크를 제안하고, 관련/비관련 정보를 구분하는 능력을 향상시킵니다[2506.05154v4].

결론
제공된 문서들은 모두 RAG 시스템이 관련 없는 문서나 다른 엔티티에 대한 정보를 포함할 때 생성 모델이 이를 사실로 오인하는 현상을 평가하고 완화하려는 연구임을 보여준다. PrismRAG는 12개의 오픈북 RAG QA 벤치마크에서 평균 사실성을 5.4% 향상시켰으며, 반관련 또는 혼란스러운 정보를 학습 데이터에 포함시켜 모델의 방해 요소에 대한 회복력을 강화한다[2507.18857v1]. Lost in the Noise는 현재 정제된 벤치마크가 포착하지 못하는 노이즈 입력을 도입함으로써 최신 모델이 최대 80%까지 성능이 급격히 떨어질 수 있음을 평가했다[2601.07226v1]. Knowledgeable-R1은 지식 충돌 시나리오와 일반적인 RAG 상황에서 기존 대비 +22.89%의 정확도 향상을 보이며, 검색된 컨텍스트가 완전히 정확한 경우에도 성능 저하 없이 견고함을 유지한다[2506.05154v4]. 따라서 이러한 연구들은 모두 유사한 목표(관련 없는 컨텍스트에 대한 저항성 강화)를 공유하지만, 평가 대상 벤치마크와 실험 조건이 다르며, 각각 다른 정도의 성능 향상을 보고하고 있다.

