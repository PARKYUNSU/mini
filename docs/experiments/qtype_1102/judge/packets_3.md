## H_C27

**질문** 언어별로 LLM 성능이 얼마나 차이 나는지 다룬 다국어 연구들 조사해줘

### 답 A

<b>서론</b>
제공된 문서들은 다국어 언어 모델(LLM) 연구에서 각 국가·언어별로 성능 차이가 어떻게 발생하는지를 다양한 측면(데이터 양, 토큰 유사성 등) 에서 조사하고 있습니다. 이러한 차이를 이해하는 것이 보다 포용적인 AI 개발에 중요합니다.

<b>본론</b>
1. <b>Multilingual NLP</b>: 다국어 자연 언어 처리 분야에서 많은 모델과 벤치마크가 출시되고 있어 각 국가·언어별 성능 차이가 주목받고 있다 [2412.08392v1]
2. <b>Key Factors Driving Performance in MLLM</b>: 사전 학습 데이터 비율, 모델 크기뿐만 아니라 토큰 유사성과 국적 유사성이 LLM 성능에 중요한 영향을 미친다[2412.12500v1]
3. <b>MERaLiON-TextLLM</b>: 중국어·인도네시아어·말레이시아어·싱글리쉬를 대상으로 한 오픈소스 모델이 공식 라마‑3 모델을 능가하는 벤치마크 성능을 달성한다 [2501.08335v3]
4. <b>Low-Resource African Languages Enhancement Study</b>: 미세 조정으로 평균 단국어성 향상이 5.6%이며, 고품질 데이터 사용 시에는 5.4%, 교차언어적 이점은 2.9%이다[2412.12417v1]
5. <b>BenCzechMark (BCM)</b>: 체코어를 위한 첫 번째 종합 벤치마크로 다양한 작업과 평가 메트릭을 제공한다 [2412.17933v2]

<b>결론</b>
제공된 문서들은 다국어 LLM 성능에 영향을 미치는 요인과 특정 언어별 벤치마크를 다루고 있습니다. [2412.12500v1]는 토큰 유사성과 국가 유사성, 사전 학습 데이터 및 모델 크기가 성능 향상의 핵심 요소임을 밝히며, 이는 다양한 언어에 공통적으로 적용될 수 있는 일반적인 인과관계로 제시됩니다[2412.12500v1]. 반면, [2501.08335v3]은 중국어, 인도네시아어, 말레이어, 신글리시에서 벤치마크 점수가 공식 Llama-3 모델을 초과하는 성능 개선을 달성했다고 보고하고 있습니다[2501.08335v3]. 또한 [2412.12417v1]는 아프리카 언어에 대해 파인튜닝을 통해 평균 단국어 성능이 5.6% 향상되고, 고품질 데이터를 사용할 경우 5.4%의 개선 효과를 보였으며, 교차언어적 접근으로 2.9%의 추가 이득을 얻었다고 구체적인 수치와 함께 제시하고 있습니다[2412.12417v1]. 이러한 결과들은 언어별 자원 수준과 데이터 품질에 따라 성능 차이가 크게 달라진다는 점을 보여줍니다. 따라서 다국어 LLM 성능은 토큰·국가 유사성 등 공통 요인과 동시에 특정 언어의 데이터 양 및 품질에 크게 의존하여 큰 편차를 보인다고 결론지을 수 있습니다.

_A 컨텍스트 7편_: 2412.08392 The Roles of English in Evaluating Multilingual Language Mod · 2412.12500 Beyond Data Quantity: Key Factors Driving Performance in Mul · 2501.08335 MERaLiON-TextLLM: Cross-Lingual Understanding of Large Langu · 2412.12417 Bridging the Gap: Enhancing LLM Performance for Low-Resource · 2412.17933 BenCzechMark : A Czech-centric Multitask and Multimetric Ben · 2510.23070 Quality-Aware Translation Tagging in Multilingual RAG system · 2412.12499 LinguaLIFT: An Effective Two-stage Instruction Tuning Framew

### 답 B

<b>서론</b>
제공된 문서들은 다국어 언어 모델(LLM) 연구에서 각 언어별 성능 차이와 이를 개선하기 위한 접근법을 다루고 있습니다. 핵심 용어는 <b>다국어 LLM</b>, <b>언어별 성능 격차</b>입니다.

<b>본론</b>
1. <b>Multilingual Language Models</b>: 다양한 모델을 출시하고, 여러 언어나 벤치마크를 통해 다중언어 자연어 처리에 대한 관심이 증가하고 있다 [2412.08392v1]
2. <b>Token Similarity &amp; Country Similarity Factors</b>: 사전 학습 데이터 비율과 모델 크기가 성능에 미치는 영향은 잘 알려져 있으나, 토큰 유사성과 국가 유사성도 중요한 요인으로 확인되었다[2412.12500v1]
3. <b>MERaLiON-TextLLM</b>: 중국어·인도네시아어·말레이시아어·싱글리쉬를 대상으로 한 오픈소스 모델을 제시하고, 기존 Llama‑3 모델보다 벤치마크 성능을 향상시켰다 [2501.08335v3]
4. <b>Fine-tuning for Low-resource African Languages</b>: 파인튜닝으로 단일언어 평균 향상이 5.6%이며(고품질 데이터 대비 저품질 데이터를 사용할 때 5.4%), 교차 언어적 접근으로도 추가적인 이득이 관찰되었다[2412.12417v1]
5. <b>BenCzechMark (BCM)</b>: 체코어를 위한 첫 번째 종합 벤치마크로, 다양한 작업 형식과 평가 메트릭을 제공한다 [2412.17933v2]
6. <b>LinguaLIFT</b>: 두 단계 인스트럭션 튜닝 프레임워크를 제안하여 저자원 언어 추론 성능이 기존 경쟁 모델보다 우수함을 보였다[2412.12499v2]

<b>결론</b>
제공된 문서들은 다국어 LLM 성능에 영향을 미치는 요인과 특정 언어별 개선 효과를 다루고 있습니다. 먼저, 토큰 유사성과 국가 유사성, 사전 학습 데이터 양 및 모델 크기가 성능 향상의 핵심 요소임을 밝힌 연구가 존재합니다 [2412.12500v1]. 또한, 중국어, 인도네시아어, 말레이어, 신글리시에서 벤치마크 점수가 개선되어 공식 Llama-3 모델을 능가한다는 결과가 보고되었습니다 [2501.08335v3]. 마지막으로, 아프리카 저자원 언어에 대해 파인튜닝을 통해 평균 단국어 성능이 5.6% 향상되고, 고질량 데이터를 사용할 경우 5.4%의 향상이 관찰되었으며, 교차언어적 접근으로 추가적인 2.9%의 이득이 얻어진다는 구체적인 수치 결과가 제시됩니다 [2412.12417v1]. 이러한 결과들은 언어별 데이터 품질과 모델 조정 방법에 따라 성능 차이가 발생함을 보여줍니다.

_B 컨텍스트 9편_: 2412.08392 The Roles of English in Evaluating Multilingual Language Mod · 2412.12500 Beyond Data Quantity: Key Factors Driving Performance in Mul · 2501.08335 MERaLiON-TextLLM: Cross-Lingual Understanding of Large Langu · 2412.12417 Bridging the Gap: Enhancing LLM Performance for Low-Resource · 2412.17933 BenCzechMark : A Czech-centric Multitask and Multimetric Ben · 2412.12499 LinguaLIFT: An Effective Two-stage Instruction Tuning Framew · 2503.22973 XL-Suite: Cross-Lingual Synthetic Training and Evaluation Da · 2601.02872 LongBench Pro: A More Realistic and Comprehensive Bilingual  · 2504.03616 Multilingual Retrieval-Augmented Generation for Knowledge-In

### 인용 블록

- **2412.08392** [인용 AB] The Roles of English in Evaluating Multilingual Language Models — [초록] Multilingual natural language processing is getting increased attention, with numerous models, benchmarks, and methods being released for many languages. ---

- **2412.12500** [인용 AB] Beyond Data Quantity: Key Factors Driving Performance in Multilingual Language Models — [초록] While the impact of pre-train data percentage and model size on performance is well-known, our study reveals additional critical factors that significantly influence MLLM effectiveness. Our findings identify token similarity and country similarity as pivotal factors, alongside pre-train data and model size, in enhancing model performance. ---

- **2501.08335** [인용 AB] MERaLiON-TextLLM: Cross-Lingual Understanding of Large Language Models in Chinese, Indonesian, Malay, and Singlish — [초록] This report presents MERaLiON-TextLLM, a series of open-source language models specifically tailored to improve understanding and generation in Chinese, Indonesian, Malay, and Singlish. Our approach achieves performance improvements across benchmarks in these languages, exceeding the capabilities of the official Llama-3 models. ---

- **2412.12417** [인용 AB] Bridging the Gap: Enhancing LLM Performance for Low-Resource African Languages with New Benchmarks, Fine-Tuning, and Cultural Adjustments — [초록] Key findings include average mono-lingual improvements of 5.6% with fine-tuning (with 5.4% average mono-lingual improvements when using high-quality data over low-quality data), 2.9% average gains from cross-lingu… The publicly available benchmarks, translations, and code from this study support further research and development aimed at creating more inclusive and effective language technologies. ---

- **2412.17933** [인용 AB] BenCzechMark : A Czech-centric Multitask and Multimetric Benchmark for Large Language Models with Duel Scoring Mechanism — [초록] We present BenCzechMark (BCM), the first comprehensive Czech language benchmark designed for large language models, offering diverse tasks, multiple task formats, and multiple evaluation metrics. ---

- **2412.12499** [인용 B] LinguaLIFT: An Effective Two-stage Instruction Tuning Framework for Low-Resource Language Reasoning — [초록] To alleviate this issue, we propose LinguaLIFT, a two-stage instruction tuning framework for advancing low-resource language reasoning. Experimental results show that LinguaLIFT outperforms several competitive baselines across MMWP and four widely used benchmarks.

---

## H_E13

**질문** 합성 데이터로만 학습한 검색기는 사람 라벨로 학습한 것과 성능 차이가 몇 % 나?

### 답 A

<b>서론</b>
합성 데이터만으로 학습된 검색기와 인간 라벨링 데이터를 활용한 모델 간의 성능 차이는, 합성 데이터가 실제 작업에 얼마나 효과적으로 전이되는지를 평가하는 핵심 지표이다. 이러한 비교는 장기 컨텍스트에서 정보 탐색과 추론 능력을 향상시키는 데 중요한 의미를 가진다[2406.19292v2][2601.18202v1].

<b>본론</b>
1. <b>Synthetic Retrieval Dataset</b>: 합성 데이터셋을 이용한 파인튜닝으로 GPT‑3.5 Turbo와 Mistral 7B의 장기 컨텍스트에서 정보 검색 및 추론 능력이 크게 향상되었으며, MDQA 벤치마크에서는 위치 10에서의 성능이 약 10.5% 개선되었다[2406.19292v2].
2. <b>ORBIT</b>: 합성 데이터셋을 이용해 생성된 ORBIT는 Qwen3‑4B를 기반으로 GRPO로 학습시켜 검색 에이전트로서 강력한 성과를 보였으며, 최소 비용과 단일 노트북으로도 경쟁력 있는 성능이 입증되었다[2604.01195v1].

<b>결론</b>
제공된 문서들은 합성 데이터와 인간 라벨 데이터를 활용한 검색기 성능 비교에 대한 구체적인 수치 결과를 제시하지 않습니다. [2406.19292v2]은 합성 데이터 파인튜닝이 MDQA에서 위치 10의 정확도를 10.5% 향상시켰으며, 일반 벤치마크에서는 성능 변화가 거의 없음을 보고하고 있습니다. 또한 Mistral 7B를 합성 데이터로 파인튜닝했을 때 TriviaQA에서 성능 저하가 발생하지 않았지만, 다른 기준 데이터는 2.33%~6.19%의 성능 하락을 초래한다는 점을 언급합니다. [2604.01195v1]는 ORBIT-4B가 합성 데이터를 이용해 검색 에이전트로서 강력한 성능을 보였음을 강조하지만, 인간 라벨 데이터와의 직접적인 비교 수치는 포함하지 않습니다. 따라서 두 논문 모두 합성 데이터가 검색 성능 향상에 유효함을 지지하지만, 인간 라벨 대비 구체적인 성능 차이 비율은 제시되지 않습니다.

_A 컨텍스트 4편_: 2406.19292 From Artificial Needles to Real Haystacks: Improving Retriev · 2604.01195 ORBIT: Scalable and Verifiable Data Generation for Search Ag · 2601.18202 SAGE: Steerable Agentic Data Generation for Deep Search with · 2606.20724 When Web Agents Finish but Still Fail: Reproducible Triggers

### 답 B

<b>서론</b>
검색 모델에 <b>합성 데이터</b>(synthetic data)만을 이용해 학습시키는 경우와 인간 라벨링으로 만든 데이터를 사용한 모델을 비교할 때, 두 접근법의 성능 차이가 궁금해집니다. 합성 데이터는 비용이 낮고 대규모로 생성 가능하지만, 실제 사용자 질의와의 괴리 때문에 정확도가 떨어질 수 있어 그 차이를 정량화하는 것이 중요합니다.

<b>본론</b>
1. <b>Finetuning on Synthetic Data</b>: GPT‑3.5 Turbo와 Mistral 7B를 합성 데이터셋으로 미세조정하면 긴 컨텍스트에서 정보 검색 및 추론 능력이 크게 향상됩니다[2406.19292v2].
2. <b>ORBIT Dataset for Search Agents</b>: ORBIT는 20K개의 짧은 검증 가능 답변을 가진 다단계 추론 질의로 구성된 훈련 데이터를 제공하며, 이 데이터만으로 Qwen3‑4B를 학습시켜 검색 에이전트 성능이 크게 향상됩니다[2604.01195v1].
3. <b>SAGE Agentic Data Generation</b>: SAGE 파이프라인은 합성 QA 쌍과 실행 피드백을 통해 생성된 데이터를 사용해 깊은 탐색 벤치마크에서 최대 27%의 상대적 향상을 보이며, 이는 기존 인간 라벨링 데이터에 기반한 모델 대비 성능 차이가 있음을 시사합니다[2601.18202v1].

<b>결론</b>
제공된 문서들은 합성 데이터와 사람 라벨 데이터를 비교한 구체적인 성능 차이를 제시하지 않습니다. [2406.19292v2]은 합성 데이터로 미세조정된 모델이 실제 작업에서 $10.5\%$ 향상과 함께 일반 벤치마크에서는 거의 변하지 않는 결과를 보였으며, 다른 기준 데이터는 $2.33\% \sim 6.19\%$의 성능 저하를 초래했다고 보고합니다. [2601.18202v1]은 합성 데이터를 이용해 심층 검색 벤치마크에서 최대 $23\%$의 상대적 성능 향상을 달성했다고 언급하고 있습니다. 따라서 현재 문서에는 사람 라벨 데이터와의 직접적인 비교 수치가 없어 정확한 차이를 판단할 수 없습니다.

_B 컨텍스트 3편_: 2406.19292 From Artificial Needles to Real Haystacks: Improving Retriev · 2604.01195 ORBIT: Scalable and Verifiable Data Generation for Search Ag · 2601.18202 SAGE: Steerable Agentic Data Generation for Deep Search with

### 인용 블록

- **2406.19292** [인용 AB] From Artificial Needles to Real Haystacks: Improving Retrieval Capabilities in LLMs by Finetuning on Synthetic Data — [초록] Recent studies have shown that Large Language Models (LLMs) struggle to accurately retrieve information and maintain reasoning capabilities when processing long-context inputs. To address these limitations, we propose a finetuning approach utilizing a carefully designed synthetic dataset comprising numerical key-value retrieval tasks. Our experiments on models like GPT-3.5 Turbo and Mistral 7B demonstrate that finetuning LLMs on this dataset significantly improves LLMs' information retrieval and reasoning capabilities in longer-context settings. We present an analysis of the finetuned models, illustrating the transfer of skills from synthetic to real task evaluations (e.g., $10.5\%$ improvement on $20$ documents MDQA at position $10$ for GPT-3.5 Turbo). We also find that finetuned LLMs' performance on general benchmarks remains almost constant while LLMs finetuned on other baseline 

- **2601.18202** [인용 AB] SAGE: Steerable Agentic Data Generation for Deep Search with Execution Feedback — [초록] Deep search agents, which aim to answer complex questions requiring reasoning across multiple documents, can significantly speed up the information-seeking process. Collecting human annotations for this application is prohibitively expensive due to long and complex exploration trajectories. We propose an agentic pipeline that automatically generates high quality, difficulty-controlled deep search question-answer pairs for a given corpus and a target difficulty level. Our pipeline, SAGE, consists of a data generator which proposes QA pairs and a search agent which attempts to solve the generated question and provide execution feedback for the data generator. The two components interact over multiple rounds to iteratively refine the question-answer pairs until they satisfy the target difficulty level. Our intrinsic evaluation shows SAGE generates questions that require diverse reasoni

- **2604.01195** [인용 AB] ORBIT: Scalable and Verifiable Data Generation for Search Agents on a Tight Budget — [초록] Search agents, which integrate language models (LMs) with web search, are becoming crucial for answering complex user queries. Constructing training datasets for deep research tasks, involving multi-step retrieval and reasoning, remains challenging due to expensive human annotation, or cumbersome prerequisites. In this work, we introduce ORBIT, a training dataset with 20K reasoning-intensive queries with short verifiable answers, generated using a frugal framework without relying on paid API services. The modular framework relies on four stages: seed creation, question--answer pair generation, and two stages of verification: self and external. ORBIT spans 15 domains and each training pair requires 4--5 reasoning steps, with external search verification required from the complete web. We train Qwen3-4B as the base model on ORBIT using GRPO and evaluate it on Wikipedia question answer

---

## H_I02a

**질문** 긴 대화를 기억하는 LLM 메모리 연구 알려줘

### 답 A

<b>서론</b>
긴 대화를 기억하는 LLM 메모리 연구에서는 복잡한 에이전트형 메커니즘보다 단순한 검색 기반 접근이 효과적일 수 있다는 결과가 제시되고 있습니다. 또한, 다층 구조와 심리적 모델 등을 활용해 장기 컨텍스트를 보존하거나 선택적으로 잊는 방법도 탐구됩니다.

<b>본론</b>
1. <b>Raw‑RAG</b>: LoCoMo·LongMemEval·MEME·MemoryAgentBench 등 7개 벤치마크 중 6곳에서 가장 높은 성능을 보이며, 기존 에이전트형 메모리보다 최대 5.53점까지 우수합니다. [2610.30755v1]
2. <b>Multi‑Layer Memory Framework</b>: 대화 이력을 작업/에피소드·의미적 층으로 분해하고 적응형 검색 게이트와 보존 정규화를 적용하여 LOCOMO, LOCCO에서 성공률 46.85%, 전체 F1 0.618을 달성했습니다. [2603.29194v1]
3. <b>MemMachine</b>: 단기·장기 에피소드 및 프로필 메모리를 통합한 구조로 대화 전역을 저장하고 손실 추출을 줄여 개인화된 에이전트에 효율적인 장기 기억을 제공합니다. [2604.04853v1]
4. <b>LUFY (Psychological Memory Model)</b>: 감정적으로 자극받는 회상을 우선시하며 전체 대화의 약 10%만 유지함으로써 사용자 경험을 크게 향상시켰습니다. [2409.12524v3]
5. <b>Learned Relevance Eviction (LRE)</b>: 킬로바이트 규모의 CPU‑only 스코어로 작업에 중요한 역사 단위를 그대로 추출해 보존하고, 다른 정책보다 호출 횟수를 37% 감소시키며 기존에서 해결되지 않던 작업을 수행했습니다. [2606.20954v2]
6. <b>Self-Recall Thinking (SRT)</b>: 다중 턴 대화의 장기 컨텍스트 의존성과 희소 정보를 처리하도록 설계되어 F1 점수 4.7%, 전체 지연 시간 14.7%를 감소시켰습니다. [2605.15102v1]
7. <b>LightMem‑Ego</b>: 스마트폰·AI 안경에 배포 가능한 경량 스트리밍 멀티모달 메모리로 객체 찾기, 대화 회상 등 일상 지원 기능을 제공합니다. [2607.11487v1]

<b>결론</b>
제공된 문서들은 긴 대화를 기억하는 LLM 메커니즘이 복잡하지 않은 검색 기반 접근(Raw‑RAG)으로도 충분히 높은 성능을 보일 수 있음을 보여줍니다. 또한 다층 구조와 심리적 모델, 경량 스트리밍 등 다양한 설계가 장기 컨텍스트 보존과 효율성을 동시에 달성할 가능성을 제시합니다.

_A 컨텍스트 8편_: 2610.30755 Is Complex Agentic Memory Always Needed? Naive RAG Is Strong · 2603.29194 Multi-Layered Memory Architectures for LLM Agents: An Experi · 2604.04853 MemMachine: A Ground-Truth-Preserving Memory System for Pers · 2409.12524 Enhancing Long-term RAG Chatbots with Psychological Models o · 2606.20954 Learning What Not to Forget: Long-Horizon Agent Memory from  · 2605.15102 Improving Multi-turn Dialogue Consistency with Self-Recall T · 2607.11487 LightMem-Ego: Your AI Memory for Everyday Life · 2402.17753 Evaluating Very Long-Term Conversational Memory of LLM Agent

### 답 B

<b>서론</b>
긴 대화에서 <b>LLM 메모리</b>는 이전 상호작용 내용을 유지하고 활용해야 하므로, 단순한 컨텍스트 윈도우만으로는 한계가 있다. 이러한 장기 기억 요구를 충족시키기 위해 다양한 메커니즘이 연구되고 있다.

<b>본론</b>
1. <b>Raw‑RAG</b>: 원본 대화 기록을 그대로 사용하여 밀집 검색과 재랭킹으로 증거를 제공하는 간단한 RAG 베이스라인이다. 복잡한 에이전트 메모리보다 성능이 뛰어나며, 필요한 증거의 높은 커버리지와 관계·종속 경로 보존 덕분에 정확도가 유지된다[2610.30755v1].
2. <b>Multi‑Layer Memory Framework</b>: 대화 역사를 작업층, 에피소드형 층, 의미적 층으로 분해하고 적응형 검색 게이트 및 기억 정규화를 적용한다. 이를 통해 세션 간 드리프트를 제어하면서도 컨텍스트 성장과 계산 효율성을 유지하며 장기 맥락 보존 성능을 향상시킨다[2603.29194v1].
3. <b>MemMachine</b>: 짧은·장기 에피소드와 프로필 메모리를 통합한 지면‑진실 보전 구조로 전체 대화 회화를 저장하고, 주변 문맥으로 핵 매칭을 확장해 관련 증거를 더 잘 호출한다. 검색 단계 최적화(깊이 튜닝 등) 와 함께 효율적인 장기 기억과 개인화된 에이전트 구현에 기여한다[2604.04853v1].
4. <b>Continuum Memory Architecture (CMA)</b>: 지속적인 저장, 선택적 유지, 연상 라우팅, 시간적 체인링 및 고차원 추상화 통합을 통해 상태를 상호작용 간 업데이트하고 보존하는 아키텍처를 정의한다. RAG가 가진 상태 변경·변형 능력을 보완하며 장기 에이전트에서 필수적인 구조로 제시된다[2601.09913v1].

<b>결론</b>
제공된 문서들에 따르면, 긴 대화를 기억하는 LLM 메모리 연구에서 복잡한 에이전트 메모리가 항상 필요한 것은 아니며, 단순한 RAG 기반 접근법도 강력한 성능을 보인다는 결과가 제시된다. [2610.30755v1]은 Raw-RAG가 LoCoMo, LongMemEval, MEME, MemoryAgentBench 등 여러 벤치마크에서 가장 높은 순위를 차지하며, 기존 에이전트 메모리보다 0.13~5.53 점 더 높은 성능을 달성했다고 보고한다. 또한 [2603.29194v1]와 [2604.04853v1]은 각각 다층 구조와 지능형 검색 메커니즘을 통해 장기 컨텍스트 유지 및 정확도 향상을 입증하고 있다. 이러한 결과들은 데이터셋과 평가 조건에 따라 메모리 시스템의 설계가 성능에 큰 영향을 미친다는 점을 보여준다. 따라서 긴 대화 처리를 위해서는 단순하면서도 효율적인 RAG 기반 메모리가 충분히 활용될 수 있으며, 필요에 따라 다층적·지능형 구조를 추가하는 것이 효과적이다.

_B 컨텍스트 5편_: 2610.30755 Is Complex Agentic Memory Always Needed? Naive RAG Is Strong · 2603.29194 Multi-Layered Memory Architectures for LLM Agents: An Experi · 2604.04853 MemMachine: A Ground-Truth-Preserving Memory System for Pers · 2409.12524 Enhancing Long-term RAG Chatbots with Psychological Models o · 2601.09913 Continuum Memory Architectures for Long-Horizon LLM Agents

### 인용 블록

- **2610.30755** [인용 AB] Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought — [초록] Across LoCoMo, LongMemEval, MEME, and MemoryAgentBench, Raw-RAG ranks first among the compared memory systems in six of seven benchmark-model settings, outperforming the strongest compared agentic memory system by 0.13-5.53 points. These findings challenge the necessity of complex agentic memory for the evaluated conversation tasks and establish naive RAG as an essential baseline. ---

- **2603.29194** [인용 AB] Multi-Layered Memory Architectures for LLM Agents: An Experimental Evaluation of Long-Term Context Retention — [초록] This paper presents a Multi-Layer Memory Framework that decomposes dialogue history into working, episodic, and semantic layers with adaptive retrieval gating and retention regularization. Experiments on LOCOMO, LOCCO, and LoCoMo show improved performance, achieving 46.85 Success Rate, 0.618 overall F1 with 0.594 multi-hop F1, and 56.90% six-period retention while reducing false memory rate to 5… ---

- **2604.04853** [인용 AB] MemMachine: A Ground-Truth-Preserving Memory System for Personalized AI Agents — [초록] We present MemMachine, an open-source memory system that integrates short-term, long-term episodic, and profile memory within a ground-truth-preserving architecture that stores entire conversational episodes and reduces lossy LLM-based extraction. These results show that preserving episodic ground truth while layering adaptive retrieval yields robust, efficient long-term memory for personalized… ---

- **2409.12524** [인용 A] Enhancing Long-term RAG Chatbots with Psychological Models of Memory Importance and Forgetting — [초록] Drawing on psychological insights, we propose LUFY, a simple yet effective method that focuses on emotionally arousing memories and retains less than 10% of the conversation. The results demonstrate that prioritizing arousing memories while forgetting the majority of the conversation significantly enhances user experience. ---

- **2606.20954** [인용 A] Learning What Not to Forget: Long-Horizon Agent Memory from a Few Kilobytes of Learning — [초록] We present LRE (Learned Relevance Eviction), a kilobyte-scale, CPU-only, language-model-free scorer that learns which units of history are task-critical and keeps them by verbatim extraction. A controlled study trace shows LRE completes tasks where the others loop, finishing one such task in 37% fewer calls than keeping everything and solving 14 tasks where no other run policy does. ---

- **2605.15102** [인용 A] Improving Multi-turn Dialogue Consistency with Self-Recall Thinking — [초록] In this paper, we propose Self-Recall Thinking (SRT), a framework designed to address long-range contextual dependency and sparse informative signals in multi-turn dialogue. Experiments on multiple datasets demonstrate that SRT improves F1 score by 4.7% and reduces end-to-end latency by 14.7% over prior methods, achieving a balance between reasoning latency and accuracy, and outperforming state-… ---

- **2607.11487** [인용 A] LightMem-Ego: Your AI Memory for Everyday Life — [초록] To address this challenge, we present LightMem-Ego, a lightweight streaming multimodal memory system for everyday-life assistance. The demonstration can be deployed on smartphones and AI glasses, supporting object finding, conversation recall, life summarization, routine discovery, and personalized assistance. ---

- **2601.09913** [인용 B] Continuum Memory Architectures for Long-Horizon LLM Agents — [초록] Retrieval-augmented generation (RAG) has become the default strategy for providing large language model (LLM) agents with contextual knowledge. Yet RAG treats memory as a stateless lookup table: information persists indefinitely, retrieval is read-only, and temporal continuity is absent. We define the \textit{Continuum Memory Architecture} (CMA), a class of systems that maintain and update internal state across interactions through persistent storage, selective retention, associative routing, temporal chaining, and consolidation into higher-order abstractions. Rather than disclosing implementation specifics, we specify the architectural requirements CMA imposes and show consistent behavioral advantages on tasks that expose RAG's structural inability to accumulate, mutate, or disambiguate memory. The empirical probes (knowledge updates, temporal association, associative recall, conte

---

## Q_A04

**질문** 프롬프트에 예시를 3개 넣을 때와 10개 넣을 때 성능 차이가 거의 없었다. 인컨텍스트 예시 개수의 효과가 포화되는 현상을 다룬 연구가 있어?

### 답 A

※ 요청한 3편 중 2편만 찾았습니다.

<b>서론</b>
인컨텍스트 학습에서 <b>예시 개수</b>(few‑shot, one‑shot 등)가 모델 성능에 미치는 영향을 규명하는 것은 예시를 어떻게 선택하느냐와 관련되어 복잡합니다. 특히 3개나 10개의 예시로 넣을 때에도 차이가 거의 나타나면 이는 포화 현상을 의미할 수 있습니다.

<b>본론</b>
1. <b>LMS3</b>: 이론적 분석에 기반해 시맨틱 유사도와 추론 안정성을 이용해 가장 적합한 샘플을 선택하고, 부적합한 few‑shot 학습용 예시를 자동으로 필터링하는 메커니즘을 제공합니다[2412.12157v1].
2. <b>Adaptive-Prompt</b>: 모델이 이전에 선택된 예시로부터 피드백을 받아 적응적으로 새로운 예시를 선정함으로써 중복성을 줄이고 정보량을 높이는 방법을 제안합니다[2412.17891v1].

<b>결론</b>
제공된 문서에는 인컨텍스트 학습에서 예시 개수가 증가해도 성능 차이가 거의 없어 포화 현상이 나타난다는 구체적인 연구가 없습니다. LMS3과 Adaptive‑Prompt는 각각 최적의 샘플 선택 및 적응적 프롬프트를 통해 모델 효율성을 높이는 방법을 제시하지만, 질문이 찾는 “예시 수에 따른 효과 포화”와 관련된 내용은 포함되어 있지 않습니다.

_A 컨텍스트 4편_: 2412.12157 What Makes In-context Learning Effective for Mathematical Re · 2502.09933 MIR-Bench: Can Your LLM Recognize Complicated Patterns via M · 2412.11923 PICLe: Pseudo-Annotations for In-Context Learning in Low-Res · 2412.17891 The Power of Adaptation: Boosting In-Context Learning throug

### 답 B

※ 요청한 3편 중 2편만 찾았습니다.

<b>서론</b>
인컨텍스트 학습에서 예시 개수가 증가해도 성능 향상이 포화되는 현상은 모델 내부 메커니즘과 데이터 다양성 부족으로 인해 설명하기 어려운 문제입니다. 이러한 <b>예시 수의 효과</b>를 정량적으로 분석한 연구가 필요합니다.

<b>본론</b>
1. <b>LMS3</b>: 이 방법은 LLM‑지향적 의미 유사도와 추론 안정성을 이용해 예시를 선택하고, 부적합 샘플을 자동으로 걸러내는 기제를 제공합니다[2412.12157v1].
2. <b>MIR-Bench</b>: 많은 수의 예시(수백~천 개)를 활용한 인컨텍스트 학습 벤치마크로, 패턴 인식과 복잡한 추론 능력을 평가합니다[2502.09933v5].

<b>결론</b>
제공된 문서들은 질문에서 찾는 연구가 없습니다. [2412.12157v1]은 LMS3 방법이 모든 데이터셋에서 기존 방법보다 우수한 성능을 보인다고 보고하지만, 예시 개수 변화에 따른 포화 현상을 다루지 않습니다. 또한 [2502.09933v5]는 MIR-Bench를 통해 많은 수의 예시를 활용한 인컨텍스트 추론에 대한 스케일링 효과와 견고성 등 다양한 통찰을 제시하고 있으나, 역시 예시 개수가 증가함에 따라 성능이 포화되는 구체적인 관찰은 포함하지 않습니다. 따라서 두 논문 모두 질문에서 찾는 '예시 개수 증가 시 성능 차이가 거의 없어 포화가 일어난다'는 현상을 다루지 않습니다.

_B 컨텍스트 2편_: 2412.12157 What Makes In-context Learning Effective for Mathematical Re · 2502.09933 MIR-Bench: Can Your LLM Recognize Complicated Patterns via M

### 인용 블록

- **2412.12157** [인용 AB] What Makes In-context Learning Effective for Mathematical Reasoning: A Theoretical Analysis — [초록] Owing to the capability of in-context learning, large language models (LLMs) have shown impressive performance across diverse mathematical reasoning benchmarks. However, we find that few-shot demonstrations can sometimes bring negative performance and their effectiveness on LLMs' reasoning abilities remains unreliable. To this end, in this paper, we aim to theoretically analyze the impact of in-context demonstrations on LLMs' reasoning performance. We prove that the reasoning efficacy (measured by empirical prediction loss) can be bounded by a LLM-oriented semantic similarity and an inference stability of demonstrations, which is general for both one-shot and few-shot scenarios. Based on this finding, we propose a straightforward, generalizable, and low-complexity demonstration selection method named LMS3. It can adaptively facilitate to select the most pertinent samples for differe

- **2412.17891** [인용 A] The Power of Adaptation: Boosting In-Context Learning through Adaptive Prompting — [초록] Large Language Models (LLMs) have demonstrated exceptional abilities across a broad range of language-related tasks, including generating solutions to complex reasoning problems. An effective technique to enhance LLM performance is in-context learning, which encourages a step-by-step reasoning process by including explanatory examples to guide the model's responses. However, selecting appropriate exemplars for the model poses a challenge, as each dataset demands a distinct set of exemplars to enable the LLM to learn effectively and perform well on the test set. Current studies often rely on uncertainty- or diversity-based selection strategies to select exemplars for annotation and to improve model learning. However, these studies typically employ a non-adaptive approach, selecting a set of exemplars all at once. We argue that this non-adaptive strategy may result in a set of exempla

- **2502.09933** [인용 B] MIR-Bench: Can Your LLM Recognize Complicated Patterns via Many-Shot In-Context Reasoning? — [초록] The ability to recognize patterns from examples and apply them to new ones is a primal ability for general intelligence, and is widely studied by psychology and AI researchers. Many benchmarks have been proposed to measure such ability for Large Language Models (LLMs); however, they focus on few-shot (usually <10) setting and lack evaluation for aggregating many pieces of information from long contexts. On the other hand, the ever-growing context length of LLMs have brought forth the novel paradigm of many-shot In-Context Learning (ICL), which addresses new tasks with hundreds to thousands of examples without expensive and inefficient fine-tuning. However, many-shot evaluations often focus on classification, and popular long-context LLM tasks such as Needle-In-A-Haystack (NIAH) seldom require complicated intelligence for integrating many pieces of information. To fix the issues from

---

## Q_A10

**질문** 에이전트가 같은 작업을 5번 돌리면 성공률이 40%에서 70%까지 흔들린다. 에이전트 평가의 실행 간 분산을 다룬 연구를 찾아줘.

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 에이전트가 동일한 작업을 반복할 때 성공률이 크게 변동하는 현상은 <b>실행 간 분산</b>과 관련된 평가 문제이며, 이를 측정하려면 다중 실행 환경에서 일관성을 보장해야 합니다. 이러한 변동을 정량화하고 안정성 향상을 위한 방법은 현재 문서에 포함되어 있지 않습니다.

<b>본론</b>
1. <b>RAMP</b>: 생산 기반 인프라로 에이전트 평가를 수행하며 15개 주요 모델을 대상으로 런타임 평가 결과를 제시한다[2605.27492v1] <b>Task completion rates collapse across serial workflows, dropping from 100% in the initial stage to only 20% in the final stage</b> (관련 연구): 문서에 언급된 실험 결과로 에이전트의 작업 완료율이 초기 단계에서 최종 단계까지 급격히 감소한다[2605.27492v1]
<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 1편_: 2605.27492 Benchmarks are Not Enough: RAMP for Runtime Assessing of Age

### 답 B

<b>서론</b>
에이전트가 동일한 작업을 반복할 때 <b>성공률</b>이나 <b>실행 간 분산</b>이 크게 변동하는 현상은, 기존 평가 방식에서 충분히 포착되지 않는 중요한 문제입니다. 이러한 변동을 정량화하고 분석하려면 실제 실행 환경에서의 다중 런 테스트와 표준화된 메트릭이 필요합니다.

<b>본론</b>
1. <b>RAMP</b>: YatCC 기반 통합 플랫폼 위에 구축된 RAMP는 표준 오케스트레이션과 실행 인터페이스를 통해 에이전트의 장기 작업 수행 능력을 평가합니다[2605.27492v1]. 결과 품질뿐만 아니라 프로세스 효율성을 동시에 측정하는 다차원 메트릭을 도입하여, 단일 벤치마크만으로는 놓칠 수 있는 실행 간 변동을 포착할 수 있습니다[2605.27492v1].
<b>결론</b>
제공된 문서에 따르면 RAMP와 그다중 차원의 유틸리티‑지향적 메트릭이 에이전트의 장기 작업 수행 능력을 평가하고, 결과 품질과 프로세스 효율성을 동시에 측정함으로써 실행 간 변동을 포착할 수 있습니다. 따라서 동일한 작업을 반복했을 때 성공률이 크게 흔들리는 현상을 분석하려면 RAMP를 활용한 다차원 평가를 적용해야 합니다.

_B 컨텍스트 1편_: 2605.27492 Benchmarks are Not Enough: RAMP for Runtime Assessing of Age

### 인용 블록

- **2605.27492** [인용 AB] Benchmarks are Not Enough: RAMP for Runtime Assessing of Agentic Models in Production Systems — [초록] LLM agents are rapidly evolving from coding assistants into autonomous software engineering systems. However, existing evaluation methodologies remain largely centered on static, isolated, and short-horizon benchmarks that fail to capture the dynamic complexity of real-world production workflows. As a result, benchmark performance may poorly reflect practical capability under realistic runtime environments involving long execution chains, tool interactions, dependency management, and iterative feedback loops. We thus present RAMP, a production-grounded infrastructure for assessing long-horizon software engineering agents. Built upon the YatCC integrated platform, RAMP provides a unified runtime assessment architecture through standardized orchestration and execution interfaces. RAMP introduces realistic compiler-construction workloads with serial dependencies and complex toolchain i

---

## Q_C07

**질문** 텍스트 임베딩 압축 쪽 논문 쭉 훑어줘

### 답 A

<b>서론</b>
텍스트 임베딩을 압축하는 연구들은 차원 축소, 토큰 병합 및 저비트 표현 등을 통해 저장 공간과 연산 비용을 크게 줄이려는 시도를 하고 있습니다. 이러한 접근법들의 핵심 아이디어와 결과를 정리합니다.

<b>본론</b>
<b>1. [2504.08386v1]</b>
2. <b>K‑Token Merging</b>: 연속된 K개의 토큰 임베딩을 경량 엔코더로 하나의 벡터로 병합하는 잠재 공간 압축 프레임워크를 제안하고, 구조적 추론·감정 분류·코드 편집 작업에서 성능과 압축률의 파레토 프롈리에 위치함을 보였습니다. [2604.15153v3]
3. <b>BITEMBED</b>: LLM 기반 텍스트 임베딩을 위한 극저비트(BIT) 프레임워크로, 인코더 효율성과 벡터 저장 비용을 동시에 최적화하며 다양한 정밀도의 임베딩과 성능‑저장 비용 트레이드오프를 제공합니다. [2606.25674v2]
4. <b>EmbedFilter</b>: LLM에서 직접 도출된 텍스트 임베딩을 선형 변환으로 단순하게 개선하는 필터링 기법을 소개하고, 이를 통해 표현 메커니즘에 대한 통찰과 보다 원칙적인 설계 방안을 제시했습니다. [2606.07502v1]

<b>결론</b>
제공된 문서들에 따르면, 텍스트 임베딩 압축 연구들은 각각 다른 접근법과 결과를 제시하고 있습니다. PCA-RAG는 차원 축소(3,072→110)를 통해 검색 속도를 최대 60배 가속화하고 인덱스 크기를 약 28.6배 감소시켰으며, 인간 주석 점수에 대한 상관관계는 크게 떨어지지 않았습니다[2504.08386v1]. K-Token Merging은 구조적 추론, 감정 분류, 코드 편집 등 다양한 작업에서 성능과 압축률의 파레토 프론티어에 위치한다는 결과를 보였습니다[2604.15153v3]. BitNet Text Embeddings(BITEMBED)는 다양한 정밀도의 텍스트 임베딩을 유연하게 제공하여 성능과 저장 비용 사이의 트레이드오프를 달성했습니다[2606.25674v2]. 이러한 결과들은 각 연구가 서로 다른 방법론과 평가 기준을 사용하여 압축 효율성과 성능 간의 균형을 탐색하고 있음을 보여줍니다.

_A 컨텍스트 5편_: 2504.08386 PCA-RAG: Principal Component Analysis for Efficient Retrieva · 2604.15153 Compressing Sequences in the Latent Embedding Space: $K$-Tok · 2606.25674 BitNet Text Embeddings · 2606.07502 Your UnEmbedding Matrix is Secretly a Feature Lens for Text  · 2602.15547 jina-embeddings-v5-text: Task-Targeted Embedding Distillatio

### 답 B

<b>서론</b>
텍스트 임베딩은 대규모 언어 모델(LLM) 기반 검색·클러스터링 등 다양한 NLP 작업에 필수적이지만, 고차원 벡터를 저장하고 인덱싱하는 과정에서 <b>저장 공간</b>과 <b>연산 지연</b>이 크게 증가한다. 이러한 비용 문제를 해결하기 위해 차원을 축소하거나 비트 정밀도를 낮추는 압축 기법이 연구되고 있다.

<b>본론</b>
1. <b>PCA‑RAG</b>: 주성분 분석(PCA)을 이용해 3,072차원 임베딩을 110차원으로 줄여 검색 속도가 최대 60배 향상되며 인덱스 크기가 약 28.6배 감소한다[2504.08386v1].
2. <b>K‑Token Merging</b>: 연속된 K개의 토큰 임베딩을 경량 엔코더로 하나의 벡터로 병합하는 방식으로, 입력 길이를 최대 75%까지 줄이면서도 성능 저하가 최소화된다[2604.15153v3].

<b>결론</b>
PCA-RAG는 3,072 차원 임베딩을 110 차원으로 축소함으로써 검색 속도를 최대 60배 가속화하고 인덱스 크기를 약 28.6배 감소시켰으며, 인간 주석과 유사한 상관관계가 유지되는 결과를 보였습니다[2504.08386v1]. K-Token Merging은 입력 길이를 최대 75%까지 줄이면서도 성능 저하가 최소화되어 성능 대비 압축 비율에서 파레토 프론트에 위치한다는 실험 결과를 제시했습니다[2604.15153v3]. 두 연구 모두 고차원 텍스트 임베딩을 압축하여 효율성을 크게 향상시켰지만, PCA-RAG는 차원 축소와 인덱스 크기 감소에 초점을 둔 반면, K-Token Merging은 토큰 수 자체를 줄이는 방식으로 입력 길이 감소와 성능 보존 사이의 균형을 달성했습니다.

_B 컨텍스트 5편_: 2504.08386 PCA-RAG: Principal Component Analysis for Efficient Retrieva · 2401.08281 The Faiss library · 2604.15153 Compressing Sequences in the Latent Embedding Space: $K$-Tok · 2406.04165 Repurposing Language Models into Embedding Models: Finding t · 2606.25674 BitNet Text Embeddings

### 인용 블록

- **2504.08386** [인용 AB] PCA-RAG: Principal Component Analysis for Efficient Retrieval-Augmented Generation — [초록] Our results show that reducing vectors from 3,072 to 110 dimensions provides a sizeable (up to $60\times$) speedup in retrieval operations and a $\sim 28.6\times$ reduction in index size, with only moderate declines in correlation metrics relative to human-annotated similarity scores. ---

- **2604.15153** [인용 AB] Compressing Sequences in the Latent Embedding Space: $K$-Token Merging for Large Language Models — [초록] In this paper, we propose K-Token Merging, a latent-space compression framework that merges each contiguous block of K token embeddings into a single embedding via a lightweight encoder. Experiments on structural reasoning (Textualized Tree), sentiment classification (Amazon Reviews), and code editing (CommitPackFT) show that K-Token Merging lies on the Pareto frontier of performance vs. compres… ---

- **2606.25674** [인용 A] BitNet Text Embeddings — [초록] In this paper, we present BITEMBED, an extreme low-bit framework for LLM-based text embedding that jointly targets encoding efficiency and vector storage. Moreover, BITEMBED flexibly obtains text embeddings of various precisions, achieving a trade-off between performance and storage cost. ---

- **2606.07502** [인용 A] Your UnEmbedding Matrix is Secretly a Feature Lens for Text Embeddings — [초록] To address this, we introduce EmbedFilter, a simple linear transformation designed to refine text embeddings derived from LLMs directly. We hope our findings provide deeper insights into the mechanisms of LLM-based representations and inspire more principled designs to improve text embeddings training. ---

---

## Q_D03

**질문** 오픈소스 임베딩 모델들의 한국어 검색 성능을 비교한 연구 찾아줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
<b>1. [2610.32933v1]</b>
2. <b>NV-Retriever</b>: 하드 음영(mining)을 활용해 텍스트 임베딩 모델을 개선하고, MTEB Retrieval(BEIR) 벤치마크에서 60.9점을 얻어 당시 최고 순위(1위) 를 차지한 모델입니다[2407.15831v2].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 5편_: 2610.32933 Yalda-Embedding: Open Development of a Competitive Persian R · 2411.08438 Towards Optimizing a Retrieval Augmented Generation using La · 2409.15763 IRSC: A Zero-shot Evaluation Benchmark for Information Retri · 2506.17277 Chunk Twice, Embed Once: A Systematic Study of Segmentation  · 2407.15831 NV-Retriever: Improving text embedding models with effective

### 답 B

<b>서론</b>
제공된 참고 문서에는 <b>오픈소스 임베딩 모델들의 한국어 검색 성능</b>에 대한 직접적인 비교 연구가 포함되어 있지 않습니다. 따라서 해당 질문은 현재 제공된 자료에서 답변할 수 없습니다.

<b>본론</b>
<b>1. (관련 문서는 없음)</b>
<b>2. (관련 문서는 없음)</b>
<b>3. (관련 문서는 없음)</b>

<b>결론</b>
제공된 문서들은 F2LLM‑v2의 다국어 지원, HRET을 통한 한국어 LLM 평가 프레임워크, K-BrowseComp를 이용한 웹 브라우징 벤치마크 및 Yalda Embedding에 대한 설명만을 포함하고 있어, 오픈소스 임베딩 모델들의 <b>한국어 검색 성능 비교</b> 연구는 찾을 수 없습니다.

_B 컨텍스트 5편_: 2603.19223 F2LLM-v2: Inclusive, Performant, and Efficient Embeddings fo · 2412.09165 When Text Embedding Meets Large Language Model: A Comprehens · 2503.22968 Redefining Evaluation Standards: A Unified Framework for Eva · 2606.02404 K-BrowseComp: A Web Browsing Agent Benchmark Grounded in Kor · 2610.32933 Yalda-Embedding: Open Development of a Competitive Persian R

### 인용 블록

- **2610.32933** [인용 A] Yalda-Embedding: Open Development of a Competitive Persian Retrieval Model — [초록] Despite advances in multilingual text representations, effective dense retrieval for Persian remains constrained by the limited availability of language-specific training resources and compact embedding models. We present Yalda Embedding, a 595.8-million-parameter Persian retrieval model adapted from Qwen3-Embedding-0.6B using more than one million query-document pairs. On eight Persian retrieval tasks from FaMTEB, the model achieves the highest macro-average among the evaluated 0.6B models, scoring 0.5488 and outperforming Qwen3-Embedding-0.6B and F2LLM-v2-0.6B on every task. It also approaches Qwen3-Embedding-4B, winning on four tasks, tying on one, and trailing by 0.0075 in macro-average. An incremental ablation study examines contrastive batch size, optimization stabilization, and relational knowledge distillation from F2LLM-v2-8B. Under the one-epoch training setup, contrastive

- **2407.15831** [인용 A] NV-Retriever: Improving text embedding models with effective hard-negative mining — [초록] Text embedding models have been popular for information retrieval applications such as semantic search and Question-Answering systems based on Retrieval-Augmented Generation (RAG). Those models are typically Transformer models that are fine-tuned with contrastive learning objectives. One of the challenging aspects of fine-tuning embedding models is the selection of high quality hard-negative passages for contrastive learning. In this paper we introduce a family of positive-aware mining methods that use the positive relevance score as an anchor for effective false negative removal, leading to faster training and more accurate retrieval models. We provide an ablation study on hard-negative mining methods over their configurations, exploring different teacher and base models. We further demonstrate the efficacy of our proposed mining methods at scale with the NV-Retriever-v1 model, whi

---

## Q_D07

**질문** 에이전트 프레임워크들의 성능 차이를 같은 과제로 측정한 연구 찾아줘

### 답 A

<b>서론</b>
에이전트 프레임워크들의 성능 차이를 <b>같은 과제</b>로 측정하는 연구는, 각 에이전트가 동일한 작업 환경에서 어떻게 수행되는지를 비교하기 위해 일관된 평가 기준과 과제가 필요합니다. 이러한 접근은 벤치마크 설계와 실험 프로토콜의 엄격성을 요구합니다.

<b>본론</b>
1. <b>CORE‑Bench Hard</b>: 과학 코드 재현을 위한 벤치마크로, 정확도 포화 이후에도 효율성·신뢰성·모델 성능 등을 측정할 수 있음을 보여줍니다[2606.26158v1].
2. <b>GauntletBench</b>: 웹 기반의 도전적인 시나리오에서 에이전트의 일반화를 평가하기 위해 설계된 벤치마크이며, 다섯 가지 전문 애플리케이션에 걸쳐 총 135개의 비시각‑중심 과제를 제공합니다[2606.14397v5].

<b>결론</b>
제공된 문서들은 에이전트 프레임워크의 성능 차이를 측정하는 연구가 존재함을 보여준다. CORE-Bench v1.1은 정확도 포화에도 불구하고 효율성, 신뢰성 및 모델 성능을 평가하는 데 유용하지만, 정확도로 에이전트를 구분하는 데는 한계가 있다[2606.26158v1]. 반면 GauntletBench는 현대 에이전트에서조차 성공률이 28.2%에 그쳐 인간 비전문가(80% 이상)와 큰 격차가 있음을 드러낸다[2606.14397v5]. 따라서 두 벤치마크 모두 에이전트 성능 차이를 측정하지만, CORE-Bench는 정확도 기반 평가에 한계가 있고 GauntletBench는 더 어려운 과제에서 에이전트의 전반적인 한계를 강조한다.

_A 컨텍스트 5편_: 2606.26158 Life After Benchmark Saturation: A Case Study of CORE-Bench · 2606.14397 Running the Gauntlet: Hard Agentic Tasks · 2605.20530 AgentAtlas: Beyond Outcome Leaderboards for LLM Agents · 2605.20049 Does Code Cleanliness Affect Coding Agents? A Controlled Min · 2511.13998 LoCoBench-Agent: An Interactive Benchmark for LLM Agents in 

### 답 B

<b>서론</b>
에이전트 프레임워크들의 성능 차이를 <b>같은 과제</b>로 측정하는 연구는 평가 기준과 실험 설정을 일관되게 유지해야 하므로 설계가 어렵습니다. 특히 다양한 에이전트가 동일한 벤치마크에서 어떻게 수행되는지를 비교하려면 공통된 테스트 환경과 과제가 필요합니다.

<b>본론</b>
1. <b>Self-Distillation AgentRL Benchmark</b>: GRPO를 기준으로 ALFWorld, ScienceWorld, Search-QA, WebShop 등 네 가지 과제와 세 모델 크기를 사용해 10개의 대표적 방법을 평가했습니다[2610.19789v1].
2. <b>CORE‑Bench Hard / CORE‑Bench v1.1 &amp; OOD</b>: 정확도 포화 이후에도 효율성·신뢰성·모델 성능 등을 측정하기 위해 개선된 벤치마크와 오스트라이버드 과제를 도입하여 에이전트 비교를 수행했습니다[2606.26158v1].
3. <b>GauntletBench</b>: 시간 인식, 그래픽 이해, 3D 추론 등 세 가지 능력을 평가하는 웹 기반 벤치를 구축하고 Video Editor·Workflow Builder·3D Modeller·Flight Analyser·Circuit Designer와 같은 다섯个专业 애플리케이션에 총 135개의 과제를 제공하여 에이전트 일반화 성능을 측정했습니다[2606.14397v5].
4. <b>AgentCompass</b>: Benchmark, Harness, Environment라는 세 독립적인 구성 요소로 평가 파이프라인을 재설계하고, fault‑tolerant 비동기 런타임과 종합적 트래젝토리 분석 도구를 제공하여 20개 이상의 벤치마크를 지원하며 에이전트 연구의 복제 가능성을 높였습니다[2607.13705v3].

<b>결론</b>
제공된 문서들은 에이전트 프레임워크의 성능 차이를 측정하는 연구들이 동일한 과제를 사용하여 비교한다는 공통점을 가지고 있습니다. [2610.19789v1]은 200개의 작업을 대상으로 Measure, Test-Cond., Find, Chem-Mix, Lifespan 등 다양한 영역에서 에이전트의 점수를 보고하며, 추가적인 학습 비용이 항상 성능 향상을 보장하지 않는다는 결과를 제시합니다. 또한 [2606.14397v5]에서는 GauntletBench라는 새로운 벤치마크를 통해 현재 최첨단 에이전트가 28.2%의 성공률만 달성하고, 비전문가 인간 주석이 80% 이상의 성공률을 보인다고 보고하여 에이전트와 인간 사이의 큰 격차를 강조합니다. 이러한 결과들은 동일한 과제 설정하에서도 벤치마크 유형과 평가 기준에 따라 에이전트의 성능 차이가 크게 달라질 수 있음을 보여줍니다.

_B 컨텍스트 5편_: 2610.19789 More Methods, Better Agents? A Reality Check on Self-Distill · 2606.26158 Life After Benchmark Saturation: A Case Study of CORE-Bench · 2606.14397 Running the Gauntlet: Hard Agentic Tasks · 2607.13705 AgentCompass: A Unified Evaluation Infrastructure for Agent  · 2605.20530 AgentAtlas: Beyond Outcome Leaderboards for LLM Agents

### 인용 블록

- **2606.26158** [인용 AB] Life After Benchmark Saturation: A Case Study of CORE-Bench — [초록] When a benchmark's accuracy saturates, it is often retired and replaced with a more challenging version. We show that this approach privileges accuracy and misses the opportunity to study six other key dimensions of agent performance: construct validity issues such as shortcuts, out-of-distribution generalizability, efficiency, reliability, the relative importance of the model versus the scaffold, and uplift from human-agent collaboration. We use CORE-Bench Hard, a benchmark for computational reproducibility of scientific code, as a case study to demonstrate that measuring agents along these dimensions yields meaningful insights into agent performance even after accuracy saturates. First, we surface threats to construct validity in CORE-Bench Hard that are difficult to anticipate with less capable agents. We introduce an improved benchmark, CORE-Bench v1.1, and an out-of-distributio

- **2606.14397** [인용 AB] Running the Gauntlet: Hard Agentic Tasks — [초록] As agentic systems continue to evolve and are widely deployed in real-world scenarios, there is a growing demand to faithfully evaluate their capabilities. However, current benchmarks are typically built on popular applications with relatively simple tasks and focus on a narrow set of capabilities while overlooking broader dimensions, resulting in saturated performance on modern agents and failing to probe their limitations. To this end, we introduce GauntletBench, a web-based benchmark for evaluating agent generalisation in challenging scenarios, focusing on three underexplored capabilities (temporal perception, graphical understanding, and 3D reasoning), across five less-covered professional applications (Video Editor, Workflow Builder, 3D Modeller, Flight Analyser, and Circuit Designer), each with 27 vision-intensive tasks (135 in total). Our benchmark provides a modular pipeline

- **2610.19789** [인용 B] More Methods, Better Agents? A Reality Check on Self-Distillation in Agentic Reinforcement Learning — [초록] Self-distillation in agentic reinforcement learning has produced a growing number of methods. However, existing evaluations often reuse published baseline scores under differing experimental conditions, provide few direct comparisons among contemporaneous methods, and give limited attention to training stability and computational cost. These limitations obscure the source of reported gains and the practical strengths and weaknesses of competing methods. Costly agent training further motivates a common basis for comparison. To address these gaps, we compare ten representative methods against GRPO on ALFWorld, ScienceWorld, Search-QA, and WebShop across three model sizes. Our study comprises 132 training runs totaling 12,124.4 recorded H800 GPU-hours, with repeated evaluations over eight rollout seeds for the pretrained backbones and all eleven trained methods. Beyond final task perfo

- **2607.13705** [인용 B] AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities — [초록] As Large Language Models (LLMs) evolve into autonomous agents, the need for unified evaluation infrastructure becomes critical. However, current evaluation pipelines remain highly fragmented and tightly coupled, hindering reproducibility and causing redundant engineering. To address this, we introduce AgentCompass, an open-source, lightweight, and extensible infrastructure for evaluating LLM-based agents. AgentCompass organizes the evaluation process around three independent components, namely Benchmark, Harness, and Environment, thereby enabling flexible configurations without requiring the reimplementation of complex execution logic. Furthermore, it features a fault-tolerant asynchronous runtime and comprehensive trajectory analysis tools to transparently diagnose nuanced failure modes like reward-hacking. Natively supporting over 20 benchmarks across five capability dimensions, A

---

## Q_E03

**질문** 정확도가 높은 작은 리랭커 모델 연구 알려줘

### 답 A

<b>서론</b>
정확도가 높은 <b>작은 리랭커 모델</b> 연구는 제한된 파라미터와 메모리 내에서 검색 품질과 효율성을 동시에 확보해야 하는 어려움이 있습니다. 이러한 제약 하에서도 성능 경쟁력을 유지하는 설계가 필요합니다.

<b>본론</b>
1. <b>Glance</b>: 경량 결정 어댑터와 포인터 헤드를 추가해 생성기와 리랭킹을 하나의 9B 백본으로 통합하고, 공유 프리필에서 후보 문서를 점수화합니다[2610.40454v1].
2. <b>jina‑reranker‑v3</b>: “last but not late” 상호작용 방식을 도입하여 쿼리와 모든 후보 문서 사이에 인과적 주의를 적용해 풍부한 교차 정보를 생성하며, 0.6B 파라미터로 BEIR에서 nDCG@10 = 61.94를 달성합니다[2509.25085v4].
3. <b>Lychee‑Reranker</b>: 오프라인으로 문서를 인코딩하고 Matryoshka 임베딩 풀링을 사용해 컴팩트한 구조(최소 0.27B 활성화 파라미터) 를 유지하면서, 크로스‑주의를 통해 정교한 관련성 모델링이 가능합니다[2606.22807v4].

<b>결론</b>
Glance 모델은 MS MARCO 데이터셋에서 bge-reranker-v2-m3보다 높은 nDCG@10 점수 (SciFact: 0.741 vs 0.721, NFCorpus: 0.345 vs 0.326) 를 달성했으며, HotpotQA 질문에서는 선택된 컨텍스트가 F1 점수를 0.045 향상시켰다[2610.40454v1]. jina-reranker-v3는 BEIR 벤치마크에서 61.94 nDCG@10을 기록하며 다른 모델보다 크기가 훨씬 작지만 성능은 유지한다[2509.25085v4]. Lychee-Reranker는 BEIR와 MIRACL 데이터셋에서 Qwen3/BGE-Reranker 시리즈와 경쟁하는 수준의 다중 도메인·다국어 재랭킹 성능을 보이며 효율성이 우수하다[2606.22807v4]. 따라서 각 모델은 서로 다른 평가 데이터와 조건에서 높은 정확도를 달성하지만, Glance는 MS MARCO 기반의 정량적 비교에서 가장 높은 점수를 기록하고, jina-reranker-v3와 Lychee-Reranker는 각각 BEIR 및 다중 도메인 환경에서 경쟁력 있는 성능을 보인다.

_A 컨텍스트 3편_: 2610.40454 Glance: The Generator Is Its Own Reranker · 2509.25085 jina-reranker-v3: Last but Not Late Interaction for Listwise · 2606.22807 Lychee-Reranker: Fast but Not Late Interaction for Compresse

### 답 B

<b>서론</b>
정확도가 높은 <b>작은 리랭커 모델</b> 연구는 파라미터 수를 최소화하면서도 검색 품질과 효율성을 동시에 달성해야 하는 어려운 과제이다. 기존 대형 모델을 대체할 만한 경량화된 구조와 설계가 필요하다.

<b>본론</b>
1. <b>Glance</b>: 9B backbone을 단일 resident로 사용하며, 가벼운 decision adapter와 pointer head를 추가해 공유 prefill에서 후보 문서를 점수화한다. MS MARCO 미세 조정 후 SciFact nDCG@10은 0.741이며 HotpotQA에서는 선택된 컨텍스트가 F1을 기존 cross‑encoder 대비 0.045 향상시킨다[2610.40454v1].
2. <b>jina-reranker-v3</b>: 6B 파라미터의 다국어 listwise rerank로, “last but not late” 상호작용 방식을 도입해 query와 모든 후보 문서를 동일한 컨텍스트 윈도우에서 causal attention으로 결합한다. BEIR 성능은 nDCG@10 = 61.94이며 다른 모델보다 훨씬 작다[2509.25085v4].
3. <b>Lychee-Reranker</b>: Encoder‑decoder 구조에 Matryoshka embedding pooling을 적용해 문서를 사전 인코딩하고, decoder가 시스템·사용자 지시와 query 의도를 함께 학습한다. Nano 버전은 활성화 파라미터 0.27B이며 BEIR/MIRACL에서 강력한 성능과 높은 효율성을 보인다[2606.22807v4].

<b>결론</b>
Glance 모델은 MS MARCO 데이터셋에서 bge-reranker-v2-m3보다 높은 nDCG@10 점수 (SciFact: 0.741 vs 0.721, NFCorpus: 0.345 vs 0.326) 를 달성했으며, HotpotQA 질문에서는 선택된 컨텍스트가 F1 점수를 0.045 향상시켰다[2610.40454v1]. jina-reranker-v3는 BEIR 벤치마크에서 61.94 nDCG@10을 기록하며 다른 모델보다 크기가 훨씬 작지만 성능은 유지한다[2509.25085v4]. Lychee-Reranker는 BEIR와 MIRACL 데이터셋에서 Qwen3/BGE-Reranker 시리즈와 경쟁하는 수준의 다중 도메인·다국어 재랭킹 성능을 보이며 효율성이 우수하다[2606.22807v4]. 따라서 각 모델은 서로 다른 평가 데이터와 조건에서 높은 정확도를 달성하지만, Glance는 MS MARCO 기반의 정량적 비교에서 가장 높은 점수를 기록하고, jina-reranker-v3와 Lychee-Reranker는 각각 BEIR 및 다중 도메인 환경에서 경쟁력 있는 성능을 보인다.

_B 컨텍스트 3편_: 2610.40454 Glance: The Generator Is Its Own Reranker · 2509.25085 jina-reranker-v3: Last but Not Late Interaction for Listwise · 2606.22807 Lychee-Reranker: Fast but Not Late Interaction for Compresse

### 인용 블록

- **2610.40454** [인용 AB] Glance: The Generator Is Its Own Reranker — [초록] Retrieval-augmented generation commonly serves separate models for reranking and answering, duplicating model residency and passage processing. We introduce Glance, which equips the generator with a lightweight decision adapter and pointer head to score candidate passages from a shared prefill. Short relevance probes branch from the cached context, producing one score per passage without separately prefilling each query-passage pair. A single resident 9B backbone supports generation, general decisions and reranking, with approximately 0.1 GiB of additional memory per decision skill. After 39 minutes of MS MARCO fine-tuning, Glance achieves nDCG@10 of 0.741 on SciFact and 0.345 on NFCorpus, compared with 0.721 and 0.326 for bge-reranker-v2-m3. On 300 HotpotQA questions, its selected context improves answer F1 by 0.045 over cross-encoder-selected context under the same base generator 

- **2509.25085** [인용 AB] jina-reranker-v3: Last but Not Late Interaction for Listwise Document Reranking — [초록] jina-reranker-v3 is a 0.6B-parameter multilingual listwise reranker that introduces a novel "last but not late" interaction. Unlike late interaction models like ColBERT that encode documents separately before multi-vector matching, our approach applies causal attention between the query and all candidate documents in the same context window, enabling rich interactions before extracting contextual embeddings from each document's final token. The new model achieves state-of-the-art BEIR performance with 61.94 nDCG@10 while being significantly smaller than other models with comparable performance. The first-stage dense retriever is `jina-embeddings-v3` , providing the foundation top-100 candidates that all rerankers process. Second-stage rerankers encompass our previous `jina-reranker-v2` , the multilingual `bge-reranker-v2-m3` , the mxbai-rerank variants at different scales, and `Qwen

- **2606.22807** [인용 AB] Lychee-Reranker: Fast but Not Late Interaction for Compressed Document Reranking — [초록] As retrieval systems scale, effective and efficient reranking becomes increasingly important. However, most existing encoder- and decoder-based rerankers jointly process every query--passage pair, tightly coupling their online computation and limiting deployment efficiency and flexibility. We present Lychee-Reranker, a fast but not late-interaction (FBNL) reranker that decouples query and passage computation while retaining expressive relevance modeling. Built on an encoder--decoder architecture, Lychee-Reranker pre-encodes passages using Matryoshka embedding pooling, while its decoder models system and user instructions together with query intent; cross-attention then captures fine-grained relevance between the resulting query context and passage representations. Together, these designs offer four key advantages: (i) efficiency from offline passage encoding, (ii) expressiveness fro

---

## Q_F02

**질문** 에이전트 메모리 논문 중에 코드가 공개된 것만 알려줘

### 답 A

<b>서론</b>
에이전트 메모리 연구에서는 <b>메모리 시스템</b>과 이를 평가하는 벤치마크가 빠르게 발전하고 있으나, 실제 구현 코드가 공개된 사례는 제한적입니다. 코드 접근성은 재현성·확장성을 위해 필수적이지만, 현재 논문들 중에는 오픈소스 링크를 제공하는 경우가 드뭅니다.

<b>본론</b>
1. <b>MemoryData</b>: 2026년 발표된 연구에서 에이전트 메모리를 데이터 관리 관점에서 체계적으로 분석하고 실험을 수행했으며, 관련 코드는 공개 GitHub 저장소에 제공됩니다[2606.24775v1].
2. <b>MemSyco-Bench</b>: 기억에 의한 사기성(sycophancy) 문제를 평가하기 위한 종합 벤치마크를 제안했고, 모든 리소스를 커뮤니티가 사용할 수 있도록 오픈 소스로 배포했습니다[2607.01071v2].

<b>결론</b>
제공된 문서들은 에이전트 메모리 연구에서 코드 공개 여부를 직접 언급하지 않습니다. [2606.24775v1]은 에이전트 네이티브 메모리 시스템 구축을 위한 비용‑성능 트레이드오프를 제시하고, [2607.01071v2]은 장기 메모리가 현대 에이전트 시스템의 핵심 구성 요소임을 강조합니다. 따라서 두 논문 모두 코드 공개 여부를 다루지 않으며, 각각 다른 연구 초점을 가지고 있습니다.

_A 컨텍스트 5편_: 2606.24775 Are We Ready For An Agent-Native Memory System? · 2607.20709 NVIDIA-labs OO Agents: Native Python Object-Oriented Agents · 2607.01071 MemSyco-Bench: Benchmarking Sycophancy in Agent Memory · 2606.13681 EvoArena: Tracking Memory Evolution for Robust LLM Agents in · 2606.18829 GateMem: Benchmarking Memory Governance in Multi-Principal S

### 답 B

<b>서론</b>
제공된 문서들은 에이전트 메모리 연구에서 코드가 공개되거나 구현 세부사항이 포함된 사례를 다루고 있습니다. 각 시스템은 그래프 기반 재구성, 로컬‑퍼스트 아키텍처 및 베이즈 신뢰 점수 등 고유한 설계와 평가 방법을 제시합니다.

<b>본론</b>
1. <b>MRAgent</b>: associative memory graph 와 active reconstruction mechanism 을 결합하여 LoCoMo·LongMemEval 벤치마크에서 기존 베이스라인 대비 최대 23% 성능 향상을 보이며, 토큰 및 실행 비용을 크게 감소시켰습니다 [2606.06036v1]
2. <b>SuperLocalMemory</b>: OWASP ASI06 메모리 포이즌 공격에 대해 아키텍처 격리와 베이즈 신뢰 점수를 통해 방어하고, 클라우드 의존성 없이 개인화된 검색을 가능하게 합니다[2603.02240v1]

<b>결론</b>
제공된 문서에 따르면, 에이전트 메모리 관련 논문 중 코드 공개 여부는 명시되어 있지 않다. [2606.06036v1]은 LoCoMo 및 LongMemEval 벤치마크에서 기존 베이스라인 대비 최대 23%의 성능 향상을 보였으며, 토큰과 실행 시간 비용을 크게 감소시켰다고 보고한다. [2603.02240v1]는 SuperLocalMemory를 소개하며, OWASP ASI06 메모리 포이즌 공격에 대한 방어와 개인화된 검색을 제공한다고 언급하고 있다. 두 논문 모두 성능 향상이나 보안 강화라는 결과를 제시하지만, 코드 공개 여부에 대한 정보는 포함하지 않는다. 따라서 질문에서 요구한 '코드 공개된 에이전트 메모리 논문'은 현재 제공된 정보만으로는 확인할 수 없다.

_B 컨텍스트 4편_: 2606.06036 Memory is Reconstructed, Not Retrieved: Graph Memory for LLM · 2603.02240 SuperLocalMemory: Privacy-Preserving Multi-Agent Memory with · 2607.13104 Self-Improvements in Modern Agentic Systems: A Survey · 2603.07670 Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and

### 인용 블록

- **2606.24775** [인용 A] Are We Ready For An Agent-Native Memory System? — [초록] Memory for large language model (LLM) agents has rapidly evolved from simple retrieval-augmented mechanisms into a data management system that supports persistent information storage, retrieval, update, consolidation, and dynamic lifecycle governance throughout agent execution. Despite this evolution, existing evaluations still benchmark agent memory mainly through end-to-end task success metrics (e.g., F1, BLEU), while treating the underlying system as a monolithic black box. As a result, critical system-level concerns, including operational costs, architectural trade-offs across memory modules, and robustness under dynamic knowledge updates, remain insufficiently explored. In this paper, we present a systematic experimental study of agent memory from a data management perspective. We propose an analytical framework that decomposes agent memory into four core modules: memory repres

- **2607.01071** [인용 A] MemSyco-Bench: Benchmarking Sycophancy in Agent Memory — [초록] Memory has emerged as a cornerstone of modern LLM-based agents, supporting their evolution from single-turn assistants to long-term collaborators. However, memory is not always beneficial: retrieved memories often induce a critical issue of sycophancy, causing agents to over-align with the user at the cost of factual accuracy or objective reasoning. Despite this emerging risk, existing memory benchmarks primarily evaluate whether memories are correctly stored, retrieved, or updated, while overlooking how retrieved memories influence downstream reasoning and decision-making. To bridge this gap, we propose MemSyco-Bench, a comprehensive benchmark for evaluating memory-induced sycophancy in agent systems. MemSyco-Bench measures when memory should influence a decision and how valid memory should be used. Specifically, it covers five tasks that assess whether agents can reject memory as 

- **2606.06036** [인용 B] Memory is Reconstructed, Not Retrieved: Graph Memory for LLM Agents — [초록] To bridge this gap, we propose MRAgent, a framework that combines an associative memory graph with an active reconstruction mechanism. Experiments on the LoCoMo benchmark and LongMemEval benchmark demonstrate significant improvements over strong baselines (up to 23%), while substantially reducing token and runtime cost, highlighting the effectiveness of active and associative reconstruction for… ---

- **2603.02240** [인용 B] SuperLocalMemory: Privacy-Preserving Multi-Agent Memory with Bayesian Trust Defense Against Memory Poisoning — [초록] We present SuperLocalMemory, a local-first memory system for multi-agent AI that defends against OWASP ASI06 memory poisoning through architectural isolation and Bayesian trust scoring, while personalizing retrieval through adaptive learning-to-rank -- all without cloud dependencies or LLM inference calls. ---

---

## Q_G04

**질문** Self-RAG는 몇 B 모델로 실험했어?

### 답 A

<b>서론</b>
Self‑Reflective Retrieval-Augmented Generation (<b>Self-RAG</b>)은 대규모 언어 모델(LLM)에 검색과 자기반영 메커니즘을 결합해 사실 정확도와 응답 품질을 향상시키는 프레임워크입니다. 기존 RAG가 고정된 수의 문서를 무조건 포함하는 반면, Self-RAG는 필요 시에만 관련 지식을 선택적으로 가져와 모델을 제어할 수 있게 합니다.

<b>본론</b>
1. <b>Self‑RAG</b>: 단일 임의 LLM에 적응형 검색과 자기반영을 도입해 질감과 사실성을 개선하고, 추론 단계에서 특수 토큰인 reflection token으로 행동을 조절합니다[2310.11511v1]. Self-RAG는 총 파라미터가 약 7 억(7B)과 13  억(13B) 두 버전의 모델을 사용해 다양한 작업에서 최신 LLM 및 검색‑증강 모델을 크게 능가했습니다[2310.11511v1].
<b>결론</b>
Self‑RAG은 <b>7B</b>와 <b>13B</b> 파라미터 규모의 모델로 실험되었으며, 이 중 특히 7 억(7B) 버전이 문서에 명시된 주요 실험 대상입니다.

_A 컨텍스트 1편_: 2310.11511 Self-RAG: Learning to Retrieve, Generate, and Critique throu

### 답 B

<b>서론</b>
대규모 언어 모델(LLM)은 파라메트릭 지식에만 의존해 사실 오류가 발생하기 쉽습니다. 이러한 문제를 완화하려면 관련 지식을 검색하고 생성·평가하는 메커니즘이 필요합니다.

<b>본론</b>
1. <b>Self-RAG</b>: 7B와 13B 규모의 모델을 사용해 실험했습니다[2310.11511v1].

<b>결론</b>
제공된 문서에 따르면 Self‑RAG는 7B 및 13B 모델로 구현되어 다양한 과제에서 기존 LLM과 검색 강화 모델을 능가하는 성능을 보였습니다.

_B 컨텍스트 1편_: 2310.11511 Self-RAG: Learning to Retrieve, Generate, and Critique throu

### 인용 블록

- **2310.11511** [인용 AB] Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection — [초록] Despite their remarkable capabilities, large language models (LLMs) often produce responses containing factual inaccuracies due to their sole reliance on the parametric knowledge they encapsulate. Retrieval-Augmented Generation (RAG), an ad hoc approach that augments LMs with retrieval of relevant knowledge, decreases such issues. However, indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility or can lead to unhelpful response generation. We introduce a new framework called Self-Reflective Retrieval-Augmented Generation (Self-RAG) that enhances an LM's quality and factuality through retrieval and self-reflection. Our framework trains a single arbitrary LM that adaptively retrieves passages on-demand, and generates and reflects on retrieved passages and its o
