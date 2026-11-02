# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)

## H_C01 — LLM이 외부 API를 호출하는 도구 사용 능력을 평가하는 벤치마크 연구들 정리해줘

### 인용 블록

[문서 1]
[Distance: 0.3271]
[발행일: 2024-06-27]
[2407.00121v1] Granite-Function Calling Model: Introducing Function Calling Abilities via Multi-task Learning of Granular Tasks
[초록] Therefore, in this work, we introduce the GRANITE-20B-FUNCTIONCALLING model under an Apache 2.0 license. As a result of the diverse tasks and datasets used for training our model, we show that GRANITE-20B-FUNCTIONCALLING has better generalizability on multiple tasks in seven different evaluation datasets.
[문서 4]
[Distance: 0.2974]
[발행일: 2026-03-16]
[2603.15372v1] SKILLS: Structured Knowledge Injection for LLM-Driven Telecommunications Operations
[초록] We introduce SKILLS (Structured Knowledge Injection for LLM-driven Service Lifecycle operations), a benchmark framework comprising 37 telecom operations scenarios spanning 8 TM Forum Open API domains (TMF620, TMF621, TMF622, TMF628, TMF629, TMF637, TMF639, TMF724). MiniMax M2.5 leads (81.1% with-skill, +13.5pp), followed by Nemotron 120B (78.4%, +18.9pp), GLM-5 Turbo (78.4%, +5.4pp), and Seed 2.…
[문서 7]
[Distance: 0.3227]
[발행일: 2026-01-31]
[2602.00933v1] MCP-Atlas: A Large-Scale Benchmark for Tool-Use Competency with Real MCP Servers
[초록] We introduce MCP-Atlas, a large-scale benchmark for evaluating tool-use competency, comprising 36 real MCP servers and 220 tools. Evaluation results on frontier models reveal that top models achieve pass rates exceeding 50%, with primary failures arising from inadequate tool usage and task understanding.

### 문장

- s1: SKILLS(Structured Knowledge Injection for LLM-driven Service Lifecycle operations)은 8개의 TM Forum Open API 도메인(TMF620, TMF621, TMF622, TMF628, TMF629, TMF637, TMF639, TMF724)에 걸친 총 37개의 통신 운영 시나리오를 포함하는 벤치마크 프레임워크를 소개한다. [2603.15372v1]
- s2: 따라서 본 연구에서는 Apache 2.0 라이선스를 적용한 GRANITE-20B-FUNCTIONCALLING 모델을 소개한다. [2407.00121v1]
- s3: 또한, MCP-Atlas는 36개의 실제 MCP 서버와 220개의 도구로 구성된 대규모 벤치마크를 통해 최상위 모델이 50% 이상의 통과율을 기록했으나, 도구 사용과 작업 이해 부족이 주요 실패 원인으로 나타났습니다 [2602.00933v1].
- s4: 먼저, GRANITE-20B-FUNCTIONCALLING은 7개의 평가 데이터셋에서 뛰어난 일반화 성능을 보였으며 [2407.00121v1], SKILLS는 8개 TM Forum Open API 도메인을 포함한 37개의 통신 운영 시나리오에서 MiniMax M2.5가 81.1%의 정확도를 달성했습니다 [2603.15372v1].
- s5: 이 논문은 도구 사용 능력을 평가하기 위한 대규모 벤치마크인 MCP-Atlas를 소개하며, 이는 실제 MCP 서버 36개와 도구 220개로 구성되어 있습니다. [2602.00933v1]

## H_C02 — 긴 컨텍스트 모델을 평가하는 벤치마크 연구들 알려줘

### 인용 블록

[문서 1]
[Distance: 0.3305]
[발행일: 2024-04-09]
[2404.06480v2] Ada-LEval: Evaluating long-context LLMs with length-adaptable benchmarks
[초록] These datasets include test samples of varying lengths (from 2k to 32k+) entangled together, making it challenging to assess model capabilities across different length ra… Moreover, they do not cover the ultralong settings (100k+ tokens) that the latest LLMs claim to achieve. In this paper, we introduce Ada-LEval, a length-adaptable benchmark for evaluating the long-context understanding of LLMs.
[문서 2]
[Distance: 0.3187]
[발행일: 2023-11-08]
[2311.04939v2] LooGLE: Can Long-Context Language Models Understand Long Contexts?
[초록] In this paper, we present LooGLE, a Long Context Generic Language Evaluation benchmark for LLMs' long context understanding. The evaluation of eight state-of-the-art LLMs on LooGLE revealed key findings: (i) commercial models outperformed open-sourced models; (ii) LLMs excelled in short dependency tasks like short question-answering and cloze tasks but struggled with more intricate long dependen…
[문서 3]
[Distance: 0.2608]
[발행일: 2026-01-06]
[2601.02872v1] LongBench Pro: A More Realistic and Comprehensive Bilingual Long-Context Evaluation Benchmark
[초록] We present LongBench Pro, a more realistic and comprehensive bilingual benchmark of 1,500 naturally occurring long-context samples in English and Chinese spanning 11 primary tasks and 25 secondary tasks, with input lengths from 8k to 256k tokens. Evaluating 46 widely used long-context LLMs on LongBench Pro yields three findings: (1) long-context optimization contributes more to long-context comp…
[문서 5]
[Distance: 0.3149]
[발행일: 2024-03-29]
[2403.20262v3] ELITR-Bench: A Meeting Assistant Benchmark for Long-Context Language Models
[초록] In contrast, we propose a new benchmark for long-context LLMs focused on a practical meeting assistant scenario in which the long contexts consist of transcripts obtained by automatic speech recognition, presenting unique challenges for LLMs due to the inherent noisiness and oral nature of such data.
[문서 6]
[Distance: 0.1980]
[발행일: 2025-10-20]
[2510.17725v1] AcademicEval: Live Long-Context LLM Benchmark
[초록] Therefore, we propose \textsc{AcademicEval}, a live benchmark for evaluating LLMs over long-context generation tasks. We conduct a holistic evaluation on \textsc{AcademicEval}, and the results illustrate that LLMs perform poorly on tasks with hierarchical abstraction levels and ten… Through experimental analysis, we also reveal some insights for enhancing LLMs' long-context modeling capabilities.

### 문장

- s1: ELITR-Bench는 자동 음성 인식으로 생성된 회의 기록이라는 고유한 노이즈와 구두 특성을 가진 데이터를 대상으로 한다[2403.20262v3].
- s2: AcademicEval은 계층적 추상화 수준이 높은 긴 컨텍스트 생성 작업에서 LLM의 성능이 낮다는 점을 보여준다[2510.17725v1].
- s3: We present LongBench Pro, a more realistic and comprehensive bilingual benchmark consisting of 1,500 naturally occurring long-context samples in English and Chinese that cover 11 primary tasks and 25 secondary tasks, with input lengths ranging from 8k to 256k tokens. [2601.02872v1]
- s4: These datasets include test samples of varying lengths (from 2k to 32k+) entangled together, making it challenging to assess model capabilities across different length ra… Moreover, they do not cover the ultralong settings (100k+ tokens) that the latest LLMs claim to achieve. [2404.06480v2]
- s5: 따라서 이 논문은 긴 문맥 생성 과제에 대한 LLM 평가를 위한 라이브 벤치마크인 \textsc{AcademicEval}을 제안한다. [2510.17725v1]
- s6: Ada-LEval은 2k~32k 토큰 범위의 샘플을 포함하지만 초장문 설정(100k+ 토큰) 을 다루지 못한다[2404.06480v2].
- s7: 본 논문에서는 LLM의 긴 문맥 이해를 평가하기 위한 'LooGLE'라는 장기 컨텍스트 범용 언어 평가 벤치마크를 제시한다. [2311.04939v2]
- s8: 반면, 이 논문은 자동 음성 인식으로 얻은 전사들로 구성된 긴 컨텍스트를 갖는 실용적인 회의 보조 시나리오에 초점을 맞춘 새로운 벤치마크를 제안한다. 이러한 데이터는 본질적인 잡음과 구어적 특성 때문에 LLM에게 독특한 도전을 제시한다. [2403.20262v3]
- s9: LongBench Pro는 영어와 중국어 모두를 포함한 8k~256k 토큰 범위의 자연 발생 샘플을 활용해 평가한다[2601.02872v1].
- s10: LooGLE는 상업 모델이 오픈소스 모델을 능가한다는 결과를 보이며, 짧은 의존성 작업에서는 우수하지만 복잡한 긴 의존성 작업에서는 어려움을 겪는다[2311.04939v2].

## H_C03 — Text-to-SQL 최신 연구 5개 찾아줘

### 인용 블록

[문서 1]
[Distance: 0.2539]
[발행일: 2025-01-28]
[2502.15723v3] Balancing Content Size in RAG-Text2SQL System
[초록] While richer document content can improve schema relevance and retrieval accuracy, it also introduces noise, increasing the… Key thresholds are identified where performance degradation occurs, along with actionable strategies to mitigate these challenges. Our findings provide a roadmap for enhancing the robustness of RAG + Text2SQL systems, offering practical insights for real-world applications.
[문서 2]
[Distance: 0.2656]
[발행일: 2025-03-31]
[2503.23886v2] Text2Schema: Filling the Gap in Designing Database Table Structures based on Natural Language
[초록] We propose SchemaAgent, an LLM-based multi-agent framework for Text2Schema. We also incorporate dedicated roles for reflection and inspection, along with an innovative error detection and correction mechanism to identify and rectify issues across various phases. Experimental results demonstrate the superiority of our approach over comparative work.
[문서 3]
[Distance: 0.2562]
[발행일: 2024-12-13]
[2412.10138v3] ROUTE: Robust Multitask Tuning and Collaboration for Text-to-SQL
[초록] To address this challenge, we propose a novel RObust mUltitask Tuning and collaboration mEthod (ROUTE) to improve the comprehensive capabilities of open-source LLMs for Text2SQL, thereby providing a more practical solution. The results demonstrate that our proposal outperforms the latest Text2SQL methods and yields leading performance.

### 문장

- s1: 이 과제를 해결하기 위해 텍스트 2 SQL 작업에서 오픈소스 대형 언어 모델의 전반적인 능력을 향상시키기 위한 새로운 RObust mUltitask Tuning and collaboration mEthod (ROUTE)를 제안한다. [2412.10138v3]
- s2: 실험 결과는 본 접근법이 비교 연구보다 우수함을 보여줍니다. [2503.23886v2]
- s3: 본 연구의 결과는 RAG와 Text2SQL 시스템을 강화하는 로드맵을 제시하며, 실제 응용에 실용적인 통찰력을 제공합니다. [2502.15723v3]
- s4: 마지막으로, [2412.10138v3]은 제안된 방법이 최신 Text2SQL 방법들을 능가하고 선도적인 성능을 달성한다는 결과를 보여줍니다[2412.10138v3].
- s5: [2502.15723v3]은 RAG와 Text2SQL 시스템을 결합한 시스템의 견고성을 향상시키는 로드맵을 제공하여 실제 응용에 실용적인 통찰을 줍니다[2502.15723v3].
- s6: 또한, [2503.23886v2]는 실험 결과에서 제안된 접근법이 비교 작업보다 우수함을 입증했습니다[2503.23886v2].

## H_C04 — LLM 탈옥(jailbreak) 공격과 방어 연구 동향 정리해줘

### 인용 블록

[문서 1]
[Distance: 0.2109]
[발행일: 2026-03-28]
[2603.28817v1] GUARD-SLM: Token Activation-Based Defense Against Jailbreak Attacks for Small Language Models
[초록] Based on this observation, we propose GUARD-SLM, a lightweight token activation-based method that operates in the representation space to filter malicious prompts during inference while preserving benign ones. Our findings highlight robustness limitations across layers of language models and provide a practical direction for secure small language model deployment.
[문서 2]
[Distance: 0.1935]
[발행일: 2024-12-20]
[2412.15623v1] JailPO: A Novel Black-box Jailbreak Framework via Preference Optimization against Aligned LLMs
[초록] To address these issues, we present JailPO, a novel black-box jailbreak framework to examine LLM alignment. Additionally, our analysis of the three JailPO patterns reveals that attacks based on complex templates exhibit higher attack strength, whereas covert question transformations elicit riskier responses and are more likely to bypass defense mechanisms.
[문서 4]
[Distance: 0.2321]
[발행일: 2024-12-13]
[2412.12192v1] No Free Lunch for Defending Against Prefilling Attack by In-Context Learning
[초록] In this paper, we: (1) show that ICL can effectively defend against prefilling jailbreak attacks by employing adversative sentence structures within demonstrations; (2) characterize the effectiveness of this defense through the lens of model size, number of demonstrations, over-defense, integration with other jailbreak attacks, and the presence of safety alignment.
[문서 6]
[Distance: 0.2081]
[발행일: 2025-03-06]
[2503.04856v3] M2S: Multi-turn to Single-turn jailbreak in Red Teaming for LLMs
[초록] We introduce a novel framework for consolidating multi-turn adversarial ``jailbreak'' prompts into single-turn queries, significantly reducing the manual overhead required for adversarial testing of large language models (LLMs). Despite removing iterative back-and-forth interactions, these prompts preserve and often enhance adversarial potency: in extensive evaluations on the Multi-turn Human Ja…

### 문장

- s1: 반복적인 왕복 상호작용을 제거했음에도 불구하고 이러한 프롬프트는 적대적 잠재력을 유지하고 종종 강화하며, 다중 턴 인간 대화 데이터셋에 대한 광범위한 평가에서 이를 입증했습니다. [2503.04856v3]
- s2: 반면 대규모 모델(LLM)에서는 복잡한 템플릿 기반 공격이 높은 공격 강도를 보이며, 은밀한 질문 변환은 방어 메커니즘을 우회하기 쉽다는 분석이 이루어졌다[2412.15623v1].
- s3: 본 연구는 언어 모델의 여러 층에서 견고성 한계를 드러내며, 안전한 소형 언어 모델 배포를 위한 실용적인 방향을 제시한다. [2603.28817v1]
- s4: 또한, 다중 턴 상호작용을 제거한 단일 턴 프롬프트도 적대적 잠재력을 유지하거나 강화할 수 있어, 적대적 테스트의 수작업 부담을 크게 줄일 수 있다[2503.04856v3].
- s5: 먼저 소규모 언어모델(SLM)에서는 레이어 전반에 걸쳐 견고성 한계가 존재하며, 이는 안전한 SLM 배포를 위한 실용적인 방향을 제시한다[2603.28817v1].
- s6: 이러한 문제들을 해결하기 위해 이 논문은 LLM 정렬을 조사하기 위한 새로운 블랙박스 제일브레이크 프레임워크인 JailPO를 제시한다. [2412.15623v1]
- s7: 이 논문에서는 (1) 데모에 반발적 문장 구조를 적용함으로써 ICL이 프릴링 재일브레이크 공격을 효과적으로 방어할 수 있음을 보이고, (2) 모델 크기, 데모 수, 과도한 방어, 다른 재일브레이크 공격과의 통합 여부, 안전 정렬 존재 여부를 통해 이러한 방어의 효과를 특성화한다. [2412.12192v1]
- s8: 이러한 다양한 공격과 방어 기법들은 모델 크기, 데이터 조건 및 안전 정렬 여부에 따라 그 효과성이 달라지며, 일부 연구에서는 ICL 기반 방어와 같은 특정 메커니즘이 특정 공격 유형에 대해 효과적임을 보여주지만, 모든 경우에 적용 가능한 보편적인 해결책은 존재하지 않는 것으로 나타났다[2412.12192v1].

## H_C05 — 지식 그래프와 LLM을 결합한 질의응답 연구들 조사해줘

### 인용 블록

[문서 3]
[Distance: 0.2911]
[발행일: 2023-11-16]
[2311.09841v1] Leveraging LLMs in Scholarly Knowledge Graph Question Answering
[초록] This paper presents a scholarly Knowledge Graph Question Answering (KGQA) that answers bibliographic natural language questions by leveraging a large language model (LLM) in a few-shot manner. Our system achieves an F1 score of 99.0%, on SciQA - one of the Scholarly-QALD-23 challenge benchmarks.
[문서 6]
[Distance: 0.2788]
[발행일: 2024-03-17]
[2404.04264v5] Logic Query of Thoughts: Guiding Large Language Models to Answer Complex Logic Queries with Knowledge Graphs
[초록] In this paper, we propose 'Logic-Query-of-Thoughts' (LGOT) which is the first of its kind to combine LLMs with knowledge graph based logic query reasoning. By aggregating these results and selecting the highest quality candidate answers for each step, LGOT achieves accurate result… Our experimental findings demonstrate substantial performance enhancements, with up to 20% improvement over ChatGPT.
[문서 8]
[Distance: 0.2613]
[발행일: 2024-02-09]
[2402.06764v3] GLaM: Fine-Tuning Large Language Models for Domain Knowledge Graph Alignment via Neighborhood Partitioning and Generative Subgraph Encoding
[초록] We introduce a fine-tuning framework for developing Graph-aligned LAnguage Models (GLaM) that transforms a knowledge graph into an alternate text representation with labeled question-answer pairs. We demonstrate that grounding the models in specific graph-based knowledge expands the models' capacity for structure-based reasoning.
[문서 9]
[Distance: 0.3496]
[발행일: 2025-04-09]
[2504.07087v1] KG-LLM-Bench: A Scalable Benchmark for Evaluating LLM Reasoning on Textualized Knowledge Graphs
[초록] This is typically achieved by converting the knowledge graph into text that the LLM can process in context. We introduce KG-LLM-Bench, a comprehensive and extensible benchmark spanning five knowledge graph understanding tasks, and evaluate how different encoding strategies affect performance across various base models.
[문서 10]
[Distance: 0.2513]
[발행일: 2025-05-18]
[2505.12476v1] Enhancing Large Language Models with Reward-guided Tree Search for Knowledge Graph Question and Answering
[초록] To address these issues, this paper proposes a novel and training-free framework for KGQA tasks called Reward-guided Tree Search on Graph (RTSoG). Extensive experiments on four datasets demonstrate the effectiveness of RTSoG. Notably, it achieves 8.7% and 7.0% performance improvement over the state-of-the-art method on the GrailQA and the WebQSP respectively.

### 문장

- s1: SciQA 벤치마크 중 하나인 Scholarly-QALD-23 챌린지에서 본 시스템은 F1 점수가 99.0%를 달성했습니다. [2311.09841v1]
- s2: 반면, 다른 연구들은 ChatGPT 대비 최대 20%의 성능 향상을 보였으며[2404.04264v5], GrailQA와 WebQSP 데이터셋에서는 각각 8.7%와 7.0%의 개선 효과를 기록했습니다[2505.12476v1].
- s3: 또한, 일부 연구는 지식 그래프를 텍스트로 변환하거나 그래프 기반 정합을 통해 모델의 구조적 추론 능력을 확장하는 접근법을 제시하고 있습니다[2504.07087v1][2402.06764v3].
- s4: 이러한 결과를 집계하고 각 단계에서 가장 높은 품질의 후보 답변을 선택함으로써 LGOT은 정확한 결과를 달성하며, 실험 결과는 최대 20% 향상된 성능을 보여 ChatGPT 대비 상당한 성능 개선을 입증한다. [2404.04264v5]
- s5: We introduce KG-LLM-Bench, a comprehensive and extensible benchmark spanning five knowledge graph understanding tasks, and evaluate how different encoding strategies affect performance across various base models. [2504.07087v1]
- s6: 특정 그래프 기반 지식에 모델을 정렬함으로써 모델의 구조 기반 추론 능력을 확장함을 보여준다. [2402.06764v3]
- s7: 먼저, SciQA라는 학술 도메인 벤치마크에서는 F1 점수가 99.0%에 달하는 높은 성능을 달성했습니다[2311.09841v1].
- s8: 특히, 이 방법은 GrailQA와 WebQSP 데이터셋에서 각각 최첨단 기법에 비해 성능을 8.7%와 7.0% 향상시켰습니다. [2505.12476v1]

## H_C08 — 한국어 LLM이나 한국어 벤치마크 관련 연구 찾아줘

### 인용 블록

[문서 1]
[Distance: 0.2165]
[발행일: 2025-03-29]
[2503.22968v5] Redefining Evaluation Standards: A Unified Framework for Evaluating the Korean Capabilities of Language Models
[초록] Recent advancements in Korean large language models (LLMs) have driven numerous benchmarks and evaluation methods, yet inconsistent protocols cause up to 10 p.p performance gaps across institutions. Overcoming these reproducibility gaps does not mean enforcing a one-size-fits-all evaluation. Rather, effective benchmarking requires diverse experimental approaches and a framework robust enough to support them. To this end, we introduce HRET (Haerae Evaluation Toolkit), an open-source, registry-based framework that unifies Korean LLM assessment. HRET integrates major Korean benchmarks, multiple inference backends, and multi-method evaluation, with language consistency enforcement to ensure genuine Korean outputs. Its modular registry design also enables rapid incorporation of new datasets, methods, and backends, ensuring the toolkit adapts to evolving research needs. Beyond standard accuracy metrics, HRET incorporates Korean-focused output analyses-morphology-aware Type-Token Ratio (TTR) for evaluating lexical diversity and systematic keyword-omission detection for identifying missing concepts-to provide diagnostic insights into language-specific behaviors. These targeted analyses help researchers pinpoint morphological and semantic shortcomings in model outputs, guiding focused improvements in Korean LLM development.

. We encourage the community to contribute diverse benchmarks and evaluation methods to ensure broad representation of Korean language capabilities. All integrated datasets respect original licensing and guidelines.
[문서 2]
[Distance: 0.2953]
[발행일: 2025-03-31]
[2503.23730v1] KOFFVQA: An Objectively Evaluated Free-form VQA Benchmark for Large Vision-Language Models in the Korean Language
[초록] The recent emergence of Large Vision-Language Models(VLMs) has resulted in a variety of different benchmarks for evaluating such models. Despite this, we observe that most existing evaluation methods suffer from the fact that they either require the model to choose from pre-determined responses, sacrificing open-endedness, or evaluate responses using a judge model, resulting in subjective and unreliable evaluation. In addition, we observe a lack of benchmarks for VLMs in the Korean language, which are necessary as a separate metric from more common English language benchmarks, as the performance of generative language models can differ significantly based on the language being used. Therefore, we present KOFFVQA, a general-purpose free-form visual question answering benchmark in the Korean language for the evaluation of VLMs. Our benchmark consists of 275 carefully crafted questions each paired with an image and grading criteria covering 10 different aspects of VLM performance. The grading criteria eliminate the problem of unreliability by allowing the judge model to grade each response based on a pre-determined set of rules. By defining the evaluation criteria in an objective manner, even a small open-source model can be used to evaluate models on our benchmark reliably. In addition to evaluating a large number of existing VLMs on our benchmark, we also experimentally verify that our method of using pre-existing grading criteria for evaluation is much more reliable than existing methods. Our evaluation code is available at https://github.com/maum-ai/KOFFVQA

- [27] Seungone Kim, Juyoung Suk, Ji Yong Cho, Shayne Longpre, Chaeeun Kim, Dongkeun Yoon, Guijin Son, Yejin Cho, Sheikh Shafayat, Jinheon Baek, et al. The biggen bench: A principled benchmark for fine-grained evaluation of language models with language models. _arXiv preprint arXiv:2406.05761_ , 2024. 3

### 문장

- s1: 먼저 [2503.22968v5]은 최근 한국어 대형 언어 모델(LLM)의 발전으로 인해 다양한 벤치마크와 평가 방법이 등장했지만, 일관되지 않은 프로토콜로 인해 기관 간 최대 10%p의 성능 격차가 발생한다는 점을 강조합니다.
- s2: 이 논문의 벤치마크는 시각·언어 모델(VLM) 성능의 10 가지 측면을 포괄하는 평가 기준과 함께 제공되는 이미지와 매칭된 275 개의 정교하게 설계된 질문으로 구성됩니다. [2503.23730v1]
- s3: 이를 위해 이 논문은 한국어 대규모 언어 모델(LLM) 평가를 통합하는 오픈소스 레지스트리 기반 프레임워크인 HRET(Haerae Evaluation Toolkit)을 소개한다. [2503.22968v5]
- s4: 최근 한국어 대형 언어 모델(LLM)의 발전은 다양한 벤치마크와 평가 방법을 촉진했지만, 일관되지 않은 프로토콜로 인해 기관 간 최대 10%p의 성능 격차를 초래하고 있다. [2503.22968v5]
- s5: 따라서 이 논문은 한국어에서 시각 언어 모델(VLM)을 평가하기 위한 일반적인 자유형 시각 질문 답변 벤치마크인 KOFFVQA를 제시한다. [2503.23730v1]
- s6: 다음으로 [2503.23730v1]는 대형 비전-언어 모델(VLM) 평가를 위한 다양한 벤치마크가 등장했으며, KOFFVQA라는 객관적으로 평가되는 자유형 VQA 벤치마크를 제시하고 해당 평가 코드를 공개했다고 보고합니다.
- s7: 따라서 두 논문은 모두 한국어 언어 모델 평가의 현황과 한계를 다루지만, [2503.22968v5]은 LLM에 초점을 맞춘 성능 격차와 개선 방향을 제시하고, [2503.23730v1]는 VLM 평가를 위한 벤치마크와 코드 공개라는 구체적인 결과를 제공합니다.

## H_C10 — 여러 LLM 에이전트가 협업해서 문제를 푸는 연구들 조사해줘

### 인용 블록

[문서 1]
[Distance: 0.2264]
[발행일: 2024-06-28]
[2406.20041v3] BMW Agents -- A Framework For Task Automation Through Multi-Agent Collaboration
[초록] Early proof of this technology can be found in various demonstrations of agents solving complex tasks, interacting with external systems to augment their knowledge, and triggering actions. In this work, we focus on designing a flexible agent engineering framework with careful attention to planning and execution, capable of handling complex use case applications across various domains.
[문서 2]
[Distance: 0.3265]
[발행일: 2026-04-09]
[2604.07821v1] More Capable, Less Cooperative? When LLMs Fail At Zero-Cost Collaboration
[초록] We build a multi-agent setup designed to study cooperative behavior in a frictionless environment, removing all strategic complexity from cooperation. We find that capability does not predict cooperation: OpenAI o3 achieves only 17% of optimal collective performance while OpenAI o3-mini reaches 50%, despite identical instructions to maximize group revenue.
[문서 3]
[Distance: 0.1503]
[발행일: 2024-03-30]
[2404.00246v1] Your Co-Workers Matter: Evaluating Collaborative Capabilities of Language Models in Blocks World
[초록] To test LLM's ability to collaborate, we design a blocks-world environment, where two agents, each having unique goals and skills, build a target structure together. Both human-machine and machine-machine experiments show that LLM agents have strong grounding capacities, and our approach significantly improves the evaluation metric.

### 문장

- s1: LLM의 협업 능력을 테스트하기 위해 두 개의 고유한 목표와 기술을 가진 에이전트가 공동으로 목표 구조를 구축하도록 설계된 블록 월드 환경을 제공한다. [2404.00246v1]
- s2: 이 논문은 능력이 협력을 예측하지 못한다는 것을 발견했으며, 그룹 수익을 극대화하도록 동일한 지시를 받았음에도 불구하고 OpenAI o3는 최적의 집단 성능의 17%만을 달성하고 OpenAI o3-mini는 50%에 도달한다. [2604.07821v1]
- s3: 반면, More Capable, Less Cooperative?에서는 동일한 최대 집단 수익을 목표로 하는 지시에도 불구하고 OpenAI o3가 최적 집단 성능의 17%만 달성하고, o3-mini는 50%에 도달한다는 점을 발견하여 능력과 협력이 반드시 일치하지 않음을 보여줍니다[2604.07821v1].
- s4: BMW Agents는 다양한 도메인에서 복잡한 작업을 해결하는 유연한 프레임워크를 제시하며, 초기 증명 사례로 외부 시스템과 상호작용하고 행동을 트리거하는 데 성공했습니다[2406.20041v3].
- s5: 이 기술의 초기 증거는 외부 시스템과 상호작용하여 지식을 보강하고 행동을 유발하는 에이전트가 복잡한 작업을 해결하는 다양한 시연에서 찾을 수 있다. [2406.20041v3]
- s6: 또한, Your Co-Workers Matter에서는 인간‑기계와 기계‑기계 실험 모두에서 LLM 에이전트가 강력한 기반 능력을 보이며 평가 지표를 크게 향상시켰다고 보고합니다[2404.00246v1].

## H_C11 — 텍스트 임베딩 모델 학습 방법 연구 3개만 알려줘

### 인용 블록

[문서 1]
[Distance: 0.2718]
[발행일: 2024-06-06]
[2406.04165v2] Repurposing Language Models into Embedding Models: Finding the Compute-Optimal Recipe
[초록] Text embeddings are essential for many tasks, such as document retrieval, clustering, and semantic similarity assessment. In this paper, we study how to contrastively train text embedding models in a compute-optimal fashion, given a suite of pre-trained decoder-only language models. Our innovation is an algorithm that produces optimal configurations of model sizes, data quantities, and fine-tuning methods for text-embedding models at different computational budget levels. The resulting recipe, which we obtain through extensive experiments, can be used by practitioners to make informed design choices for their embedding models. Specifically, our findings suggest that full fine-tuning and low-rank adaptation fine-tuning produce optimal models at lower and higher computational budgets respectively.

. This enables researchers who wish to adapt language models to embed their own data, especially those with limited computational resources, to obtain optimal text embedding models with greater efficiency in time and resources.
[문서 2]
[Distance: 0.2059]
[발행일: 2024-03-29]
[2403.20327v1] Gecko: Versatile Text Embeddings Distilled from Large Language Models
[초록] We present Gecko, a compact and versatile text embedding model. Gecko achieves strong retrieval performance by leveraging a key idea: distilling knowledge from large language models (LLMs) into a retriever. Our two-step distillation process begins with generating diverse, synthetic paired data using an LLM. Next, we further refine the data quality by retrieving a set of candidate passages for each query, and relabeling the positive and hard negative passages using the same LLM. The effectiveness of our approach is demonstrated by the compactness of the Gecko. On the Massive Text Embedding Benchmark (MTEB), Gecko with 256 embedding dimensions outperforms all existing entries with 768 embedding size. Gecko with 768 embedding dimensions achieves an average score of 66.31, competing with 7x larger models and 5x higher dimensional embeddings.

The recent development of general-purpose text embedding models presents a challenge: these models require large amounts of training data to comprehensively cover desired domains and skills. Recent embedding efforts have focused on using extensive collections of training examples (Li et al., 2023; Wang et al., 2022)
[문서 3]
[Distance: 0.3298]
[발행일: 2026-02-17]
[2602.15547v2] jina-embeddings-v5-text: Task-Targeted Embedding Distillation
[초록] Text embedding models are widely used for semantic similarity tasks, including information retrieval, clustering, and classification. General-purpose models are typically trained with single- or multi-stage processes using contrastive loss functions. We introduce a novel training regimen that combines model distillation techniques with task-specific contrastive loss to produce compact, high-performance embedding models. Our findings suggest that this approach is more effective for training small models than purely contrastive or distillation-based training paradigms alone. Benchmark scores for the resulting models, jina-embeddings-v5-text-small and jina-embeddings-v5-text-nano, exceed or match the state-of-the-art for models of similar size. jina-embeddings-v5-text models additionally support long texts (up to 32k tokens) in many languages, and generate embeddings that remain robust under truncation and binary quantization. Model weights are publicly available, hopefully inspiring further advances in embedding model development.

## **4 Training**  
For training our embedding models we use the pretrained language models EuroBERT-210m [Boizard et al., 2025] for jina-embeddings-v5-text-nano and Qwen3-0.6B-Base [Yang et al., 2025] for jina-embeddings-v5-text-small (see Table 1). Both models are multilingual.[2]  
Our training method consists of two main stages:

### 문장

- s1: 제공된 문서들은 각각 계산 효율성을 고려한 최적 설계 알고리즘([2406.04165v2]), LLM 기반 지식 추출을 통한 컴팩트 모델 생성 과정([2403.20327v1]) 그리고 디스틸레이션과 작업별 대비 손실을 결합한 소규모 임베딩 훈련 레짐([2602.15547v2])이라는 세 가지 텍스트 임베딩 학습 방법을 제시하고 있습니다.
- s2: 이 논문의 두 단계 지식 증류 과정은 LLM을 이용해 다양한 합성 쌍 데이터를 생성하는 것으로 시작합니다. [2403.20327v1]
- s3: 구체적으로, 이 논문의 연구 결과는 완전한 파인튜닝과 저랭크 적응 파인튜닝이 각각 낮은 및 높은 계산 예산에서 최적의 모델을 생성한다는 것을 시사한다. [2406.04165v2]
- s4: Benchmark scores for the resulting models, jina-embeddings-v5-text-small and jina-embeddings-v5-text-nano, exceed or match the state-of-the-art for models of similar size. [2602.15547v2]

## H_C12 — 과학 논문을 자동으로 읽고 요약하거나 리뷰하는 연구들 정리해줘

### 인용 블록

[문서 1]
[Distance: 0.6486]
[발행일: 2024-06-30]
[2407.00747v1] A Comparative Study of Quality Evaluation Methods for Text Summarization
[초록] To bridge this gap, this paper proposes a novel method based on large language models (LLMs) for evaluating text summarization. Based on the empirical comparison, we propose a LLM-powered framework for automatically evaluating and improving text summarization, which is beneficial and could attract wide attention among the community.
[문서 2]
[Distance: 0.4853]
[발행일: 2024-07-30]
[2407.20906v5] Automated Review Generation Method Based on Large Language Models
[초록] We present an automated review generation method based on large language models (LLMs) to overcome efficiency bottlenecks and reduce cognitive load. Through multi-layered quality control, we effectively mitigated LLMs' hallucinations, with expert verification confirming accuracy and citation integrity while demonstrating hallucination risks reduced to below 0.5% with 95% confidence.
[문서 3]
[Distance: 0.4508]
[발행일: 2026-04-30]
[2604.27924v1] Can AI Be a Good Peer Reviewer? A Survey of Peer Review Process, Evaluation, and the Future
[초록] We catalog datasets, compare modeling choices, and discuss limitations, ethical concerns, and future directions.
[문서 4]
[Distance: 0.4075]
[발행일: 2026-06-26]
[2606.28277v1] Towards Automating Scientific Review with Google's Paper Assistant Tool
[초록] To frame the discussion around this transition, we propose a taxonomy consisting of four progressive levels of AI-human collaboration in scientific evaluation, and discuss various trade-offs involved with each. By utilizing inference scaling techniques, PAT is able to identify deeper issues than a single model call alone, achieving a 34% improvement over zero-shot recall on mathematical errors i…
[문서 5]
[Distance: 0.3912]
[발행일: 2026-06-17]
[2608.28596v1] Paper Pilot: A Human-in-the-Loop Expert System for Evidence-Traceable Scientific Manuscript Generation in Applied Sciences
[초록] This paper proposes Paper Pilot, a human-in-the-loop expert system for evidence-traceable scientific manuscript generation in applied sciences. As a first empirical validation, we evaluate the citation-grounding layer with a controlled, mechanically scored benchmark (two commercial LLMs, real arXiv papers, no LLM judge): under coverage pressure ungated drafters fabricated up to 25% of their cita…

### 문장

- s1: 첫 번째 경험적 검증으로, 이 논문은 통제된 기계 점수 벤치마크(상용 LLM 두 개, 실제 arXiv 논문, LLM 판정자 없음)를 이용해 인용 기반 레이어를 평가했으며, 커버리지 압력 하에서 게이트가 없는 초안 작성자는 최대 25%까지 인용을 조작했습니다. [2608.28596v1]
- s2: 데이터셋을 카탈로그화하고 모델링 선택을 비교하며 한계점, 윤리적 문제 및 향후 방향에 대해 논의합니다. [2604.27924v1]
- s3: 반면, Paper Pilot 연구는 인용 기반 레이어를 평가한 결과, 커버리지 압력 하에서 무제한 초안 작성자가 최대 25%의 인용을 조작한다는 한계를 확인한다[2608.28596v1].
- s4: 다층 품질 관리 과정을 통해 이 논문은 LLM의 환각 현상을 효과적으로 완화했으며, 전문가 검증이 정확성과 인용 무결성을 확인하고 환각 위험을 95% 신뢰 수준에서 0.5% 미만으로 감소시켰음을 입증했습니다. [2407.20906v5]
- s5: 제공된 문서들은 과학 논문 자동 요약 및 리뷰 연구에서 LLM 기반 프레임워크가 텍스트 요약을 평가하고 개선하는 데 유용하며, 다중 레이어 품질 통제를 통해 환각 위험을 0.5% 미만으로 낮추는 결과를 보여준다[2407.00747v1][2407.20906v5].
- s6: 추론 스케일링 기법을 활용함으로써 단일 모델 호출보다 더 깊은 문제를 식별할 수 있으며, 수학 오류에 대한 제로샷 재현율 대비 34%의 향상을 달성한다. [2606.28277v1]
- s7: 또한, AI 기반 동료 검토에 대한 조사는 데이터셋과 모델 선택을 비교하고 윤리적 문제와 한계를 논의한다[2604.27924v1], 그리고 Paper Assistant Tool은 추론 스케일링 기법을 활용해 수학 오류 탐지에서 제로샷 재현율을 34% 향상시킨다[2606.28277v1].
- s8: 실증 비교를 바탕으로 텍스트 요약의 자동 평가 및 개선을 위한 LLM 기반 프레임워크를 제안하며, 이는 유익하고 학계 전체의 관심을 끌 수 있다. [2407.00747v1]

## H_C13 — 의료 분야에 RAG를 적용한 연구 찾아줘

### 인용 블록

[문서 1]
[Distance: 0.2710]
[발행일: 2026-01-23]
[2601.16503v2] MRAG: Benchmarking Retrieval-Augmented Generation for Bio-medicine
[초록] While Retrieval-Augmented Generation (RAG) has been swiftly adopted in scientific and clinical QA systems, a comprehensive evaluation benchmark in the medical domain is lacking. To address this gap, we introduce the Medical Retrieval-Augmented Generation (MRAG) benchmark, covering various tasks in English and Chinese languages, and building a corpus with Wikipedia and Pubmed. Additionally, we develop the MRAG-Toolkit, facilitating systematic exploration of different RAG components. Our experiments reveal that: (a) RAG enhances LLM reliability across MRAG tasks. (b) the performance of RAG systems is influenced by retrieval approaches, model sizes, and prompting strategies. (c) While RAG improves usefulness and reasoning quality, LLM responses may become slightly less readable for long-form questions. We will release the MRAG-Bench's dataset and toolkit with CCBY-4.0 license upon acceptance, to facilitate applications from both academia and industry.

## **Abstract**

While Retrieval-Augmented Generation (RAG) has been swiftly adopted in scientific and clinical QA systems, a comprehensive evaluation benchmark in the medical domain is lacking. To address this gap, we introduce the Medical Retrieval-Augmented Generation (MRAG) benchmark, covering various tasks in English and Chinese languages, and building a corpus with Wikipedia and Pubmed. Additionally, we develop the MRAG-Toolkit, facilitating systematic exploration of different RAG components
[문서 2]
[Distance: 0.3804]
[발행일: 2025-02-23]
[2503.01859v1] Optimizing Retrieval-Augmented Generation of Medical Content for Spaced Repetition Learning
[초록] Advances in Large Language Models revolutionized medical education by enabling scalable and efficient learning solutions. This paper presents a pipeline employing Retrieval-Augmented Generation (RAG) system to prepare comments generation for Poland's State Specialization Examination (PES) based on verified resources. The system integrates these generated comments and source documents with a spaced repetition learning algorithm to enhance knowledge retention while minimizing cognitive overload. By employing a refined retrieval system, query rephraser, and an advanced reranker, our modified RAG solution promotes accuracy more than efficiency. Rigorous evaluation by medical annotators demonstrates improvements in key metrics such as document relevance, credibility, and logical coherence of generated content, proven by a series of experiments presented in the paper. This study highlights the potential of RAG systems to provide scalable, high-quality, and individualized educational resources, addressing non-English speaking users.

Augmented Generation (RAG) systems in medical education, focusing on optimizing learning for Polish medical specialists by integrating spaced repetition methodologies. The proposed solution merges advanced machine learning algorithms with medical knowledge grounded in Evidence-Based Medicine (EBM), ensuring accuracy and credibility.
[문서 3]
[Distance: 0.2584]
[발행일: 2025-12-08]
[2602.22216v1] Retrieval-Augmented Generation Assistant for Anatomical Pathology Laboratories
[초록] Accurate and efficient access to laboratory protocols is essential in Anatomical Pathology (AP), where up to 70% of medical decisions depend on laboratory diagnoses. However, static documentation such as printed manuals or PDFs is often outdated, fragmented, and difficult to search, creating risks of workflow errors and diagnostic delays. This study proposes and evaluates a Retrieval-Augmented Generation (RAG) assistant tailored to AP laboratories, designed to provide technicians with context-grounded answers to protocol-related queries. We curated a novel corpus of 99 AP protocols from a Portuguese healthcare institution and constructed 323 question-answer pairs for systematic evaluation. Ten experiments were conducted, varying chunking strategies, retrieval methods, and embedding models. Performance was assessed using the RAGAS framework (faithfulness, answer relevance, context recall) alongside top-k retrieval metrics. Results show that recursive chunking and hybrid retrieval delivered the strongest baseline performance. Incorporating a biomedical-specific embedding model (MedEmbed) further improved answer relevance (0.74), faithfulness (0.70), and context recall (0.77), showing the importance of domain-specialised embeddings. Top-k analysis revealed that retrieving a single top-ranked chunk (k=1) maximized efficiency and accuracy, reflecting the modular structure of AP protocols. These findings highlight critical design considerations for deploying RAG systems in healthcare and demonstrate their potential to transform static documentation into dynamic, reliable knowledge assistants, thus improving laboratory workflow efficiency and supporting patient safety.

## **2.3 Retrieval-Augmented Generation**

Retrieval-Augmented Generation (RAG) integrates information retrieval with generative modelling to produce answers that are both contextually grounded and dynamically updated. In a typical RAG pipeline (Figure 1), domain-specific documents are divided into smaller chunks, embedded into a vector space, and stored in a vector database

### 문장

- s1: 생물학적 특화 임베딩 모델(MedEmbed)을 통합함으로써 답변 관련성(0.74), 충실도(0.70), 그리고 문맥 회상률(0.77)이 추가로 향상되어 도메인 특화 임베딩의 중요성이 입증되었다. [2602.22216v1]
- s2: 의료 주석가들에 의한 엄격한 평가는 문서 관련성, 신뢰성, 생성 콘텐츠의 논리적 일관성 등 주요 지표에서 개선이 있음을 보여준다. 이러한 결과는 논문에서 제시된 일련의 실험을 통해 입증되었다. [2503.01859v1]
- s3: [2601.16503v2]은 MRAG 벤치마크에서 RAG가 LLM 신뢰성을 향상시키지만, 긴 질문에서는 가독성이 약간 감소한다고 보고한다[2601.16503v2].
- s4: 이 논문의 실험 결과는 (a) RAG가 MRAG 작업 전반에 걸쳐 LLM의 신뢰성을 향상시킨다는 것을 보여줍니다. [2601.16503v2]
- s5: [2602.22216v1]은 MedEmbed를 활용한 RAG가 정밀도·충실도·맥락 회상을 각각 0.74, 0.70, 0.77으로 높였으며, 단일 톱 랭킹 조각(k=1)이 효율성과 정확도를 최대화한다고 밝혔다[2602.22216v1].
- s6: [2503.01859v1]는 간격 반복 학습과 결합한 시스템이 문서 관련성·신뢰도·논리적 일관성을 개선했다고 평가한다[2503.01859v1].

