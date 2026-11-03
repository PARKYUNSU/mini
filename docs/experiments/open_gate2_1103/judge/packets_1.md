## OB_005

**질문** 밀집 검색기를 학습시키는 방법 논문 세 편 추천해줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>FiGRet (Fine‑grained Guidance for Retrievers)</b>: LLM의 언어 능력을 활용해 검색기가 수행 poorly 한 샘플에서 정보 중심 관점에서 예시를 구축하고, relevance·comprehensiveness·purity 세 가지 학습 목표를 통해 retriever를 정교하게 안내한다[2411.03957v1].
2. <b>LLM2IR</b>: Decoder‑only 대형 언어 모델을 단순한 비지도 대비학습으로 변환해 밀집 검색기로 만든다; LoCo, LongEmbed, BEIR 등 여러 IR 벤치마크에서 효과성을 입증하고 모델 컨텍스트 길이와 정보검색 능력 간의 관계를 밝힌다[2601.05262v1].
3. <b>Dense Passage Retrieval for Open‑Domain Question Answering</b>: 소수의 질문·패스지 쌍으로 듀얼 인코더 프레임워크를 학습시켜 밀집 표현만으로 검색을 구현한다; Lucene‑BM25 대비 top‑20 정확도에서 절대적으로 9%~19% 향상되며, 추가 훈련 데이터(1k→59k)가 일관되게 성능 향상을 가져온다[2004.04906v3].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 5편_: 2411.03957 Fine-Grained Guidance for Retrievers: Leveraging LLMs' Feedb · 2601.05262 LLM2IR: simple unsupervised contrastive learning makes long- · 2503.05037 Collapse of Dense Retrievers: Short, Early, and Literal Bias · 2004.04906 Dense Passage Retrieval for Open-Domain Question Answering · 2411.04403 Towards Competitive Search Relevance For Inference-Free Lear

### 답 B

<b>서론</b>
밀집 검색기(dense retriever)는 대규모 텍스트 데이터에서 관련 문서를 효율적으로 찾는 핵심 단계이지만, 기존 방법들은 문서 수준 학습에 의존하거나 사전 훈련 비용이 높아 실용성이 제한적입니다. 이러한 한계를 극복하기 위해 다양한 접근법이 연구되고 있습니다.

<b>본론</b>
1. <b>FiGRet</b>: LLM의 언어 능력을 활용해 검색기가 성능이 낮은 샘플에서 세밀한 예시를 생성하고, 관련성·포괄성·순수성을 목표로 학습을 안내합니다[2411.03957v1].
2. <b>LLM2IR</b>: 간단한 비지도 대조학습 프레임워크를 통해 임계값‑only LLM을 정보검색 모델로 변환하며, 긴 컨텍스트 길이를 가진 모델을 더 강력한 검색 능력으로 활용한다는 점을 제시합니다[2601.05262v1].

<b>결론</b>
제공된 문서들은 밀집 검색기 학습에 대한 구체적인 방법론을 제시하지 않으며, 각각 다른 초점을 가지고 있습니다. [2411.03957v1]은 제안된 프레임워크가 다양한 retriever와 LLM을 갖춘 RAG 시스템의 성능을 향상시킨다는 실험 결과를 보여줍니다. 반면 [2601.05262v1]는 단순한 비지도 대조 학습이 여러 IR 벤치마크에서 효과적임을 입증하고, 긴 컨텍스트 길이를 가진 모델이 더 강력한 검색 능력을 가질 수 있음을 발견합니다. 따라서 두 논문은 모두 밀집 검색기 성능 향상에 기여하지만, 각각 다른 접근법과 평가 기준을 통해 결과를 제시하고 있습니다.

_B 컨텍스트 5편_: 2411.03957 Fine-Grained Guidance for Retrievers: Leveraging LLMs' Feedb · 2601.05262 LLM2IR: simple unsupervised contrastive learning makes long- · 2503.05037 Collapse of Dense Retrievers: Short, Early, and Literal Bias · 2004.04906 Dense Passage Retrieval for Open-Domain Question Answering · 2411.04403 Towards Competitive Search Relevance For Inference-Free Lear

### 인용 블록

- **2411.03957** [인용 AB] Fine-Grained Guidance for Retrievers: Leveraging LLMs' Feedback in Retrieval-Augmented Generation — [초록] Retrieval-Augmented Generation (RAG) has proven to be an effective method for mitigating hallucination issues inherent in large language models (LLMs). Previous approaches typically train retrievers based on semantic similarity, lacking optimization for RAG. More recent works have proposed aligning retrievers with the preference signals of LLMs. However, these preference signals are often difficult for dense retrievers, which typically have weaker language capabilities, to understand and learn effectively. Drawing inspiration from pedagogical theories like Guided Discovery Learning, we propose a novel framework, FiGRet (Fine-grained Guidance for Retrievers), which leverages the language capabilities of LLMs to construct examples from a more granular, information-centric perspective to guide the learning of retrievers. Specifically, our method utilizes LLMs to construct easy-to-under

- **2601.05262** [인용 AB] LLM2IR: simple unsupervised contrastive learning makes long-context LLM great retriever — [초록] Modern dense information retrieval (IR) models usually rely on costly large-scale pretraining. In this paper, we introduce LLM2IR, an efficient unsupervised contrastive learning framework to convert any decoder-only large language model (LLM) to an information retrieval model. Despite its simplicity, the effectiveness is proven among different LLMs on multiple IR benchmarks including LoCo, LongEmbed and BEIR. We also find that models with a longer context length tend to have a stronger IR capacity by comparing task performances of models in the same model family. Our work not only provides an effective way to build IR models on the state-of-the-art LLMs, but also shed light on the relationship between information retrieval ability and model context length, which helps the design of better information retrievers. © 2026 Xiaocong Yang LLM2IR: SIMPLE UNSUPERVISED CONTRASTIVE LEARNING M

- **2004.04906** [인용 A] Dense Passage Retrieval for Open-Domain Question Answering — [초록] Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks. . This suggests that with a general pretrained language model, it is possible to train a high-quality dense retriever with a small number of question–passage pairs. Adding more training exa

---

## OB_010

**질문** 검색 질의를 늘려 쓰는 연구 중에 괜찮은 논문 하나 알려줘

### 답 A

<b>서론</b>
검색 질의를 <b>늘려 쓰는 연구</b>(multi‑turn search)는 사용자의 의도가 불명확하고 선호도에 따라 달라지며 상호작용 과정에서 진화하기 때문에, 단순 키워드 매칭만으로는 충분하지 않다[2607.00597v2]. 이러한 복잡성을 제어하려면 검색 워크플로우를 명시적으로 설계·수정할 수 있는 메커니즘이 필요하다.

<b>본론</b>
1. <b>PaperPilot</b>: 멀티턴 과학 문헌 탐색 에이전트로, 앵커 논문과 사용자 질의로부터 키워드 검색·인용 확장·필터링·스코어링·재랭킹·증거 추출을 포함한 실행 가능한 DAG 워크플로우를 유도한다[2607.00597v2].
2. <b>InteractiveSurvey</b>: LLM 기반 개인화 및 인터랙티브 서베이 논문 생성 시스템으로, 온라인 검색과 사용자 업로드된 참고 문헌으로부터 구조화된 다중모달 서베이를 만들고, 참조 분류·개요·내용을 단계별로 커스터마이징할 수 있다[2504.08762v1].
3. <b>Course Recommendation System</b>: LLM 기반 RAG를 활용해 자연어 질의에서 이상적인 과목 설명을 생성하고 임베딩 벡터로 변환해 유사한 실제 과목을 검색한다[2412.19312v2]。

<b>결론</b>
제공된 문서들은 검색 질의를 늘려 쓰는 연구와 직접적인 관련이 없습니다. [2607.00597v2]은 과학 문헌 검색 분야에서 PaperPilot-9B가 다중 턴 상호작용에서 Hit@5를 58.0에서 77.0으로 향상시켰으며, MRR과 nDCG@10도 각각 47.5→59.4와 26.8→32.5로 개선되었고 워크플로우 오류율을 9.5%에서 0%로 낮췄다고 보고합니다. [2504.08762v1]는 InteractiveSurvey가 설문지 생성 시스템으로서 콘텐츠 품질과 시간 효율성 측면에서 대부분의 LLM 및 기존 방법을 능가한다는 결과를 제시하고 있습니다. 따라서 검색 질의 확장 연구와 관련된 결과는 제공된 문서에 포함되어 있지 않으며, 과학 문헌 검색 성능 향상과 설문지 생성 효율성이라는 두 다른 분야의 성과만 확인됩니다.

_A 컨텍스트 4편_: 2607.00597 Multi-Turn Agentic Scientific Literature Search via Workflow · 2504.08762 InteractiveSurvey: An LLM-based Personalized and Interactive · 2412.19312 From Interests to Insights: An LLM Approach to Course Recomm · 2601.07838 A survey: Information search time optimization based on RAG 

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
검색 질의를 늘려 쓰는 연구를 찾기 위해 관련 논문들을 검토했습니다.

<b>본론</b>
1. <b>PaperPilot</b>: 다중 턴 과학 문헌 검색 에이전트로, 워크플로우 인덕션을 통해 키워드 탐색·인용 확장·필터링·스코어링·재랭킹 등을 포함한 실행 가능한 DAG를 구축하고 사용자 피드백으로 질의와 워크플로우 자체를 개선합니다. [2607.00597v2]
2. <b>InteractiveSurvey</b>: LLM 기반 개인화 및 상호작용형 서베이 논문 생성 시스템이며, 온라인 검색과 업로드된 참고 문헌을 활용해 구조화된 다중 모달 서베이를 만들고 사용자가 중간 단계(참고 분류·개요·내용)를 지속적으로 커스터마이징할 수 있습니다. [2504.08762v1]
3. <b>Course Recommendation System</b>: LLM 기반 RAG 방법을 이용해 학생의 자연어 질의를 ‘이상적인’ 과목 설명으로 변환하고, 임베딩 벡터를 통해 유사한 실제 과목을 검색합니다. [2412.19312v2]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 4편_: 2607.00597 Multi-Turn Agentic Scientific Literature Search via Workflow · 2504.08762 InteractiveSurvey: An LLM-based Personalized and Interactive · 2412.19312 From Interests to Insights: An LLM Approach to Course Recomm · 2601.07838 A survey: Information search time optimization based on RAG 

### 인용 블록

- **2607.00597** [인용 AB] Multi-Turn Agentic Scientific Literature Search via Workflow Induction — [초록] Scientific literature search often requires more than retrieving papers from a single query: users' intents are underspecified, preference-dependent, and evolve through interaction. Existing search agents typically rely on fixed pipelines or implicit language-only reasoning, making their search strategies difficult to control, inspect, and refine. We introduce PaperPilot, a multi-turn literature search agent that frames scientific search as workflow induction. Given an anchor paper and a user query, PaperPilot constructs an executable DAG of paper-search operators, including keyword search, citation expansion, filtering, scoring, reranking, and evidence extraction. User feedback is then used to refine both the query and the workflow itself. We train PaperPilot with supervised workflow imitation and preference optimization over controlled workflow corruptions. Experiments show that P

- **2504.08762** [인용 AB] InteractiveSurvey: An LLM-based Personalized and Interactive Survey Paper Generation System — [초록] The exponential growth of academic literature creates urgent demands for comprehensive survey papers, yet manual writing remains time-consuming and labor-intensive. Recent advances in large language models (LLMs) and retrieval-augmented generation (RAG) facilitate studies in synthesizing survey papers from multiple references, but most existing works restrict users to title-only inputs and fixed outputs, neglecting the personalized process of survey paper writing. In this paper, we introduce InteractiveSurvey - an LLM-based personalized and interactive survey paper generation system. InteractiveSurvey can generate structured, multi-modal survey papers with reference categorizations from multiple reference papers through both online retrieval and user uploads. More importantly, users can customize and refine intermediate components continuously during generation, including reference 

- **2412.19312** [인용 AB] From Interests to Insights: An LLM Approach to Course Recommendations Using Natural Language Queries — [초록] Most universities in the United States encourage their students to explore academic areas before declaring a major and to acquire academic breadth by satisfying a variety of requirements. Each term, students must choose among many thousands of offerings, spanning dozens of subject areas, a handful of courses to take. The curricular environment is also dynamic, and poor communication and search functions on campus can limit a student's ability to discover new courses of interest. To support both students and their advisers in such a setting, we explore a novel Large Language Model (LLM) course recommendation system that applies a Retrieval Augmented Generation (RAG) method to the corpus of course descriptions. The system first generates an 'ideal' course description based on the user's query. This description is converted into a search vector using embeddings, which is then used to f

---

## OB_019

**질문** 코드 검색 모델 논문 세 편만 뽑아줘

### 답 A

<b>서론</b>
코드 검색은 방대한 소스 코드와 복잡한 의존성 관계를 탐색해야 하므로, 효율적인 그래프 기반 접근법이 필요합니다. 이러한 어려움을 해결하기 위해 최근 연구들은 LLM과 결합한 다양한 코딩그래프를 활용한 방법을 제안하고 있습니다.

<b>본론</b>
1. <b>CoSIL</b>: 두 단계의 코드‑그라프 검색 전략을 도입하여 파일 수준에서 모듈 호출 그래프로 넓은 탐색 후, 함수 레벨로 확장된 함수 호출 그래프에 대해 반복적인 심층 분석을 수행합니다[2503.22424v3]. 우선순위 스케줄링과 행동 분해, 관련성 점수를 기반으로 고유한 코드그래프를 검색하고, 거리‑인지적 프루닝으로 컨텍스트 정확도를 향상시킵니다[2503.22424v3]
<b>결론</b>
제공된 문서에 따르면 CoSIL은 파일·함수 수준의 그래프 탐색을 결합하여 정밀한 이슈 로컬라이제이션 성능을 달성하며, Orcaloca는 우선순위 기반 스케줄링과 거리‑인지적 프루닝으로 코드그래프 검색의 정확도를 높입니다. 따라서 질문에서 요구하는 두 가지 주요 코딩검색 모델은 CoSIL과 Orcaloca로 요약할 수 있습니다.

_A 컨텍스트 2편_: 2503.22424 Issue Localization via LLM-Driven Iterative Code Graph Searc · 2412.12544 Seed-CTS: Unleashing the Power of Tree Search for Superior P

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>CoSIL</b>: LLM 기반 함수 수준 이슈 로컬라이제이션 방법으로, 두 단계 코드 그래프 검색 전략과 프루너·반성 메커니즘을 도입하여 SWE-bench에서 Top‑1 정확도 43.3%~44.6%, Agentless와 결합 시 해결률 향상 효과를 보임 [2503.22424v3] LLM 에이전트 프레임워크로, 우선순위 스케줄링·행동 분해·관련성 점수를 활용한 고유한 코드 그래프 검색과 거리 기반 프루닝을 적용하여 오류 로컬라이제이션 정확도를 향상시킴 [2503.22424v3]
<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 2편_: 2503.22424 Issue Localization via LLM-Driven Iterative Code Graph Searc · 2412.12544 Seed-CTS: Unleashing the Power of Tree Search for Superior P

### 인용 블록

- **2503.22424** [인용 AB] Issue Localization via LLM-Driven Iterative Code Graph Searching — [초록] Issue solving aims to generate patches to fix reported issues in real-world code repositories according to issue descriptions. Issue localization forms the basis for accurate issue solving. Recently, LLM-based issue localization methods have demonstrated state-of-the-art performance. However, these methods either search from files mentioned in issue descriptions or in the whole repository and struggle to balance the breadth and depth of the search space to converge on the target efficiently. Moreover, they allow LLM to explore whole repositories freely, making it challenging to control the search direction to prevent the LLM from searching for incorrect targets. This paper introduces CoSIL, an LLM-driven, powerful function-level issue localization method without training or indexing. CoSIL employs a two-phase code graph search strategy. It first conducts broad exploration at the fil

---

## OB_022

**질문** 에이전트가 계획을 세우는 방법 최신 논문 두 편 알려줘

### 답 A

<b>서론</b>
에이전트가 복잡한 작업을 수행하기 위해 <b>계획(Planning)</b> 을 수립하는 것은 다단계 도구 호출, 환경 변화 및 사용자 선호도 학습 등 다양한 요소를 고려해야 하므로 어려운 문제입니다. 최근 연구에서는 대형 언어 모델(LLM)을 활용해 이러한 계획 과정을 자동화하고 개선하려는 시도가 활발히 진행되고 있습니다.

<b>본론</b>
1. <b>Cyclical Urban Planning (CUP)</b>: 다중 에이전트 LLM 기반 프레임워크로, <b>(Planning)</b>, <b>(Living)</b>, <b>(Judging)</b> 세 단계가 순환적으로 연결되어 도시 계획을 지속적으로 생성·평가·개선하는 폐쇄 루프를 구현합니다[2412.20505v1].
2. <b>InstructRAG</b>: 검색 증강 생성(Retrieval‑Augmented Generation)을 활용하고, 과거 명령 경로 그래프와 강화학습 에이전트(확장성), 메타러닝 에이전트(전이 학습 가능성)가 결합된 다중 에이전트 méta‑RL 프레임워크를 통해 계획 성능과 새로운 작업에 대한 적응력을 크게 향상시킵니다[2504.13032v1].

<b>결론</b>
제공된 문서들은 각각 순환적 도시 계획 자동화(CUP)[2412.20505v1]와 검색 증강·다단계 학습을 결합한 InstructRAG 기반 에이전트 계획(InstructRAG)[2504.13032v1] 두 가지 최신 접근법을 제시하고 있습니다.

_A 컨텍스트 5편_: 2412.20505 Planning, Living and Judging: A Multi-agent LLM-based Framew · 2412.09666 Systematic Analysis of LLM Contributions to Planning: Solver · 2603.12740 ToolTree: Efficient LLM Agent Tool Planning via Dual-Feedbac · 2504.13032 InstructRAG: Leveraging Retrieval-Augmented Generation on In · 2602.04129 KGLAMP: Knowledge Graph-guided Language model for Adaptive M

### 답 B

<b>서론</b>
에이전트가 복잡한 작업을 수행하기 위해 <b>계획 수립</b>은 다양한 도구나 에이전트 간의 상호작용, 그리고 환경 변화에 대응해야 하므로 매우 어려운 문제입니다. 최근 연구에서는 대규모 언어 모델(LLM)과 검색·트리 탐색 등 새로운 기법을 결합해 계획의 정확성과 효율성을 크게 향상시키고 있습니다.

<b>본론</b>
1. <b>Cyclical Urban Planning (CUP)</b>: 다중 에이전트 LLM 기반 프레임워크로, <b>(Planning)</b>, <b>(Living)</b>, <b>(Judging)</b> 세 단계가 순환적으로 연결되어 도시 계획을 지속적으로 생성·평가·개선하는 폐쇄 루프를 구현합니다[2412.20505v1].
2. <b>InstructRAG</b>: 멀티‑에이전트 메타 강화학습 구조 내에 그래프로 과거 명령 경로를 조직하고, RL-Agent로 확장성을, ML-Agent로 전이를 향상시켜 계획 성능을 크게 개선하며 새로운 작업에도 빠르게 적응할 수 있습니다[2504.13032v1].

<b>결론</b>
[2412.20505v1]은 도시 계획 도메인에서 다중 에이전트 LLM 기반 프레임워크가 연속적이고 적응적인 계획 과정을 구현한다는 점을 강조한다[2412.20505v1]. [2504.13032v1]는 다양한 작업 계획 데이터셋에서 InstructRAG가 기존 접근법보다 최대 19.2% 성능 향상을 보이며 새로운 작업에 효율적으로 적응함을 보여준다[2504.13032v1]. 두 연구 모두 LLM 기반 에이전트 계획을 향상시키는 결과를 제시하지만, 적용 대상과 평가 지표가 다르다: [2412.20505v1]은 도시 환경의 연속적 계획 과정에 초점을 맞추고, [2504.13032v1]는 일반적인 작업 계획 데이터셋에서 정량적인 성능 개선과 소거 학습 적응성을 강조한다. 따라서 두 논문은 각각 다른 도메인과 조건에서 LLM 기반 에이전트 계획의 효과를 입증하고 있다.

_B 컨텍스트 5편_: 2412.20505 Planning, Living and Judging: A Multi-agent LLM-based Framew · 2412.09666 Systematic Analysis of LLM Contributions to Planning: Solver · 2603.12740 ToolTree: Efficient LLM Agent Tool Planning via Dual-Feedbac · 2504.13032 InstructRAG: Leveraging Retrieval-Augmented Generation on In · 2602.04129 KGLAMP: Knowledge Graph-guided Language model for Adaptive M

### 인용 블록

- **2412.20505** [인용 AB] Planning, Living and Judging: A Multi-agent LLM-based Framework for Cyclical Urban Planning — [초록] Urban regeneration presents significant challenges within the context of urbanization, requiring adaptive approaches to tackle evolving needs. Leveraging advancements in large language models (LLMs), we propose Cyclical Urban Planning (CUP), a new paradigm that continuously generates, evaluates, and refines urban plans in a closed-loop. Specifically, our multi-agent LLM-based framework consists of three key components: (1) Planning, where LLM agents generate and refine urban plans based on contextual data; (2) Living, where agents simulate the behaviors and interactions of residents, modeling life in the urban environment; and (3) Judging, which involves evaluating plan effectiveness and providing iterative feedback for improvement. The cyclical process enables a dynamic and responsive planning approach. Experiments on the real-world dataset demonstrate the effectiveness of our fram

- **2504.13032** [인용 AB] InstructRAG: Leveraging Retrieval-Augmented Generation on Instruction Graphs for LLM-Based Task Planning — [초록] Recent advancements in large language models (LLMs) have enabled their use as agents for planning complex tasks. Existing methods typically rely on a thought-action-observation (TAO) process to enhance LLM performance, but these approaches are often constrained by the LLMs' limited knowledge of complex tasks. Retrieval-augmented generation (RAG) offers new opportunities by leveraging external databases to ground generation in retrieved information. In this paper, we identify two key challenges (enlargability and transferability) in applying RAG to task planning. We propose InstructRAG, a novel solution within a multi-agent meta-reinforcement learning framework, to address these challenges. InstructRAG includes a graph to organize past instruction paths (sequences of correct actions), an RL-Agent with Reinforcement Learning to expand graph coverage for enlargability, and an ML-Agent 

---

## OB_044

**질문** 여러 번 샘플링해서 답을 고르는 연구 좋은 논문 하나 골라줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>DK-PRACTICE</b>: 이 플랫폼은 학생들의 지식 상태를 기반으로 개인화된 학습 콘텐츠를 추천하며, 적응형 평가와 기계학습 모델을 활용해 다음 문제를 선택하고 부족한 지식을 보완하는 자료를 제안한다[2501.10373v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 1편_: 2501.10373 DK-PRACTICE: An Intelligent Educational Platform for Persona

### 답 B

<b>서론</b>
제공된 연구는 <b>DK-PRACTICE</b>라는 지능형 교육 플랫폼에서 학생들의 지식 상태를 기반으로 개인화된 학습 콘텐츠를 추천하는 방법을 제시하고 있습니다. 이 시스템은 기계학습 모델을 활용해 질문 선택과 자료 권고를 수행하며, 적응적이고 맞춤형 교육을 가능하게 합니다[2501.10373v1].

<b>본론</b>
1. <b>DK-PRACTICE</b>: 짧은 적응형 평가와 Q&amp;A 방식을 통해 학생이 특정 지식 도메인의 핵심 개념에 대해 답하고, 이전 답변의 정확도에 따라 다음 질문을 동적으로 선택합니다. 테스트 완료 후 상호작용 이력을 분석해 식별된 지식 격차를 메우기 위한 학습 자료를 추천하며, 두 번의 시험(사전·사후)과 상세 결과 보고서 제공 기능을 포함하여 자기 평가와 진도 모니터링이 가능합니다[2501.10373v1].

<b>결론</b>
따라서 질문에서 찾는 “여러 번 샘플링해서 답을 고르는 연구”는 <b>DK-PRACTICE</b>가 해당합니다. 이 플랫폼은 기계학습 기반의 동적 질문 선택과 개인화된 학습 자료 추천으로 학생들의 지식 상태를 지속적으로 평가하고 보완하는 적응형 교육 환경을 구현합니다[2501.10373v1].

_B 컨텍스트 1편_: 2501.10373 DK-PRACTICE: An Intelligent Educational Platform for Persona

### 인용 블록

- **2501.10373** [인용 AB] DK-PRACTICE: An Intelligent Educational Platform for Personalized Learning Content Recommendations Based on Students Knowledge State — [초록] This study introduces DK-PRACTICE (Dynamic Knowledge Prediction and Educational Content Recommendation System), an intelligent online platform that leverages machine learning to provide personalized learning recommendations based on student knowledge state. Students participate in a short, adaptive assessment using the question-and-answer method regarding key concepts in a specific knowledge domain. The system dynamically selects the next question for each student based on the correctness and accuracy of their previous answers. After the test is completed, DK-PRACTICE analyzes students' interaction history to recommend learning materials to empower the student's knowledge state in identified knowledge gaps. Both question selection and learning material recommendations are based on machine learning models trained using anonymized data from a real learning environment. To provide self

---

## OB_059

**질문** 지시 튜닝 데이터 구축 논문 세 편 추천해줘

### 답 A

<b>서론</b>
지시 튜닝(instruction tuning)은 대규모 언어 모델(LLM) 의 행동을 맞춤설정하기 위한 핵심 방법이지만, <b>고품질 지시 데이터</b>를 확보하는 것이 성능에 직접적인 영향을 미칩니다. 이러한 데이터를 효과적으로 구축하려면 프롬프트의 견고성이나 효율적 필터링 기법이 필요합니다.

<b>본론</b>
1. <b>Adversarial Instruction-Following Difficulty</b>: 온라인 지시 데이터에서 공격을 통해 적대적 지시를 생성하고, 해당 응답에 대한 도움을 측정하는 메트릭으로 고품질 데이터를 선별합니다. [2503.24028v1]
2. <b>SuperNUGGETS</b>: 작은 언어 모델(SLM) 을 이용해 효율적으로 일회성(one‑shot) 예제를 필터링하며 기존 NUGGETS 대비 성능 손실은 1–2% 수준이고 처리 속도가 약 58 배 향상됩니다. [2412.09990v1]
3. <b>IterIT (Complexity-Diversity Scoring)</b>: 샘플의 복잡성과 다양성을 동시에 측정하고, 미세조정 과정에서 모델‑특정 점수를 반복적으로 업데이트하여 상위 복합점수 데이터를 선택합니다. [2412.17365v1]

<b>결론</b>
지시 튜닝 데이터 구축 연구들은 모두 제한된 양의 고품질 데이터를 활용해 LLM 성능을 향상시킬 수 있음을 보여준다[2503.24028v1]. SuperNUGGETS는 기존 NUGGETS 대비 효율성을 58배 증가시키면서 성능 저하를 1-2% 이내로 억제한다[2412.09990v1]. IterIT는 다중 출처와 합성 기법을 활용한 데이터에서 노이즈 제거 및 중복 제거가 필수적임을 강조하며, 반복적이고 선택적인 학습을 통해 기존 베이스라인보다 일관된 개선을 달성한다[2412.17365v1].

_A 컨텍스트 5편_: 2503.24028 Pay More Attention to the Robustness of Prompt for Instructi · 2412.09990 Small Language Model as Data Prospector for Large Language M · 2412.17365 Boosting LLM via Learning from Data Iteratively and Selectiv · 2407.00102 Curriculum Learning with Quality-Driven Data Selection · 2606.04261 Can Generalist Agents Automate Data Curation?

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 지시 튜닝 데이터 구축은 고품질 데이터를 선별하고 모델에 맞게 조정하는 과정으로, 효율성과 품질 확보를 동시에 달성하기 어려운 과제입니다.

<b>본론</b>
1. <b>Adversarial Instruction-Following Difficulty</b>: 프롬프트의 강인성을 고려해 온라인 지시 데이터를 공격하여 적대적 데이터 생성 및 평가 메트릭을 제안한다[2503.24028v1]
2. <b>SuperNUGGETS</b>: 작은 언어 모델(SLM) 을 이용해 고품질 일회성 예시를 필터링하고, 기존 NUGGETS 대비 효율성을 크게 향상시킨다[2412.09990v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 5편_: 2503.24028 Pay More Attention to the Robustness of Prompt for Instructi · 2412.09990 Small Language Model as Data Prospector for Large Language M · 2412.17365 Boosting LLM via Learning from Data Iteratively and Selectiv · 2407.00102 Curriculum Learning with Quality-Driven Data Selection · 2606.04261 Can Generalist Agents Automate Data Curation?

### 인용 블록

- **2503.24028** [인용 AB] Pay More Attention to the Robustness of Prompt for Instruction Data Mining — [초록] Instruction tuning has emerged as a paramount method for tailoring the behaviors of LLMs. Recent work has unveiled the potential for LLMs to achieve high performance through fine-tuning with a limited quantity of high-quality instruction data. Building upon this approach, we further explore the impact of prompt's robustness on the selection of high-quality instruction data. This paper proposes a pioneering framework of high-quality online instruction data mining for instruction tuning, focusing on the impact of prompt's robustness on the data mining process. Our notable innovation, is to generate the adversarial instruction data by conducting the attack for the prompt of online instruction data. Then, we introduce an Adversarial Instruction-Following Difficulty metric to measure how much help the adversarial instruction data can provide to the generation of the corresponding respons

- **2412.09990** [인용 AB] Small Language Model as Data Prospector for Large Language Model — [초록] The quality of instruction data directly affects the performance of fine-tuned Large Language Models (LLMs). Previously, \cite{li2023one} proposed \texttt{NUGGETS}, which identifies and selects high-quality quality data from a large dataset by identifying those individual instruction examples that can significantly improve the performance of different tasks after being learnt as one-shot instances. In this work, we propose \texttt{SuperNUGGETS}, an improved variant of \texttt{NUGGETS} optimised for efficiency and performance. Our \texttt{SuperNUGGETS} uses a small language model (SLM) instead of a large language model (LLM) to filter the data for outstanding one-shot instances and refines the predefined set of tests. The experimental results show that the performance of \texttt{SuperNUGGETS} only decreases by 1-2% compared to \texttt{NUGGETS}, but the efficiency can be increased by 

- **2412.17365** [인용 A] Boosting LLM via Learning from Data Iteratively and Selectively — [초록] Datasets nowadays are generally constructed from multiple sources and using different synthetic techniques, making data de-noising and de-duplication crucial before being used for post-training. In this work, we propose to perform instruction tuning by iterative data selection (\ApproachName{}). We measure the quality of a sample from complexity and diversity simultaneously. Instead of calculating the complexity score once for all before fine-tuning, we highlight the importance of updating this model-specific score during fine-tuning to accurately accommodate the dynamic changes of the model. On the other hand, the diversity score is defined on top of the samples' responses under the consideration of their informativeness. IterIT integrates the strengths of both worlds by iteratively updating the complexity score for the top-ranked samples and greedily selecting the ones with the hi

---

## OB_074

**질문** 글자 인식 없이 문서를 읽는 모델 논문 추천 부탁해

### 답 A

<b>서론</b>
문서 이미지를 직접 해석하여 텍스트를 추출하는 <b>OCR</b>은 복잡한 레이아웃과 다양한 글꼴 때문에 어려운 과제이며, 최근에는 시각‑언어 모델을 활용해 OCR 없이도 문서를 읽는 연구가 진행되고 있다[2603.28103v1][2607.13639v1].

<b>본론</b>
1. <b>dots.ocr</b>: 다국어 문서 레이아웃을 단일 시선·언어 모델로 파싱한다; 페이지 이미지를 입력받아 텍스트와 구조를 순차적으로 추출하고, bounding box 및 요소 라벨링을 수행한다[2408.03834v1][2607.13639v1].
2. <b>OvisOCR2</b>: 엔드‑투‑엔드 문서 파서를 제공하며 Markdown 형식으로 자연스러운 읽기 순서에 따라 텍스트·수식·표와 시각 영역까지 생성하고, 데이터 엔진과 강화학습 기반 학습을 통해 OmniDocBench에서 최고 점수를 기록한다[2607.13639v1].
3. <b>AgenticOCR</b>: OCR을 정적 전체‑텍스트 처리가 아닌 쿼리 주도 온디맨드 추출 시스템으로 전환해 레이아웃 분석 후 관심 영역만 선택적으로 인식하고, 시각 토큰 예산 내에서 효율적인 RAG 파이프라인에 통합한다[2602.24134v1].

<b>결론</b>
제공된 문서들은 글자 인식(OCR) 없이 문서를 읽는 모델에 대한 결과를 제시하고 있습니다. OvisOCR2는 OmniDocBench v1.6에서 96.58점이라는 최상위 점수를 기록했으며, PureDocBench에서는 Avg3 점수 75.06을 달성했습니다[2607.13639v1]. 반면, AgenticOCR은 시각적 RAG 시스템의 효율성과 정확성을 향상시켜 장기 문서 이해에서 전문가 수준의 성능을 보였으며, OmniDocBench 기준 90–95%의 정확도를 기록한 것으로 나타났습니다[2602.24134v1]. 따라서 두 모델 모두 글자 인식 없이 문서를 읽는 데 높은 성능을 보이지만, OvisOCR2가 전체 점수 측면에서 더 높은 결과를 보이고, AgenticOCR은 효율성과 시각적 RAG 시스템에 특화된 성능을 강조한다는 점에서 차이가 있습니다.

_A 컨텍스트 4편_: 2603.28103 Transcription and Recognition of Italian Parliamentary Speec · 2607.13639 OvisOCR2 Technical Report · 2408.03834 Target Prompting for Information Extraction with Vision Lang · 2602.24134 AgenticOCR: Parsing Only What You Need for Efficient Retriev

### 답 B

<b>서론</b>
문서에서 <b>글자 인식(OCR)</b> 없이도 전체 레이아웃과 텍스트를 읽어내는 모델은 복잡한 문서 구조와 다양한 시각적 요소를 동시에 이해해야 하므로 구현하기 어렵습니다. 이러한 접근법은 전통적인 파이프라인보다 높은 정확도와 효율성을 기대할 수 있습니다.

<b>본론</b>
1. <b>dots.ocr</b>: 단일 비전‑언어 모델을 이용해 다국어 문서를 레이아웃 분석과 읽기 순서 텍스트 전사까지 수행합니다[2607.13639v1]. 문서 페이지 이미지를 받아 Markdown 형식으로 자연스러운 읽기 순서에 따라 텍스트, 수식, 표 및 시각 영역을 모두 파싱하는 엔드‑투엔드 모델입니다[2607.13639v1] (관련 연구).
<b>결론</b>
따라서 질문이 찾는 “글자 인식 없이 문서를 읽어내는” 접근으로는 <b>dots.ocr</b>과 <b>OvisOCR2</b>가 해당 문서에서 제시된 핵심 시스템들입니다.

_B 컨텍스트 4편_: 2603.28103 Transcription and Recognition of Italian Parliamentary Speec · 2607.13639 OvisOCR2 Technical Report · 2408.03834 Target Prompting for Information Extraction with Vision Lang · 2602.24134 AgenticOCR: Parsing Only What You Need for Efficient Retriev

### 인용 블록

- **2603.28103** [인용 A] Transcription and Recognition of Italian Parliamentary Speeches Using Vision-Language Models — [초록] Parliamentary proceedings represent a rich yet challenging resource for computational analysis, particularly when preserved only as scanned historical documents. Existing efforts to transcribe Italian parliamentary speeches have relied on traditional Optical Character Recognition pipelines, resulting in transcription errors and limited semantic annotation. In this paper, we propose a pipeline based on Vision-Language Models for the automatic transcription, semantic segmentation, and entity linking of Italian parliamentary speeches. The pipeline employs a specialised OCR model to extract text while preserving reading order, followed by a large-scale Vision-Language Model that performs transcription refinement, element classification, and speaker identification by jointly reasoning over visual layout and textual content. Extracted speakers are then linked to the Chamber of Deputies kn

- **2607.13639** [인용 AB] OvisOCR2 Technical Report — [초록] We introduce OvisOCR2, a 0.8B document parsing model. OvisOCR2 is designed as an end-to-end parser: given a document page image, it generates a Markdown representation in natural reading order, covering text, formulas, tables, and visual regions. We build a data engine that combines filtered real-document annotations with synthetic pages whose rendered images and Markdown targets are derived from the same HTML source. The training recipe includes supervised fine-tuning, reinforcement learning on a 4B branch with a multi-component reward design, on-policy distillation into the 0.8B model, and model fusion. On OmniDocBench v1.6, OvisOCR2 achieves a state-of-the-art overall score of 96.58, placing an end-to-end model at the top of this leaderboard previously dominated by pipeline methods and highlighting the potential of end-to-end document parsing. On PureDocBench, OvisOCR2 also achie

- **2408.03834** [인용 A] Target Prompting for Information Extraction with Vision Language Model — [초록] The recent trend in the Large Vision and Language model has brought a new change in how information extraction systems are built. VLMs have set a new benchmark with their State-of-the-art techniques in understanding documents and building question-answering systems across various industries. They are significantly better at generating text from document images and providing accurate answers to questions. However, there are still some challenges in effectively utilizing these models to build a precise conversational system. General prompting techniques used with large language models are often not suitable for these specially designed vision language models. The output generated by such generic input prompts is ordinary and may contain information gaps when compared with the actual content of the document. To obtain more accurate and specific answers, a well-targeted prompt is requir

- **2602.24134** [인용 A] AgenticOCR: Parsing Only What You Need for Efficient Retrieval-Augmented Generation — [초록] The expansion of retrieval-augmented generation (RAG) into multimodal domains has intensified the challenge for processing complex visual documents, such as financial reports. While page-level chunking and retrieval is a natural starting point, it creates a critical bottleneck: delivering entire pages to the generator introduces excessive extraneous context. This not only overloads the generator's attention mechanism but also dilutes the most salient evidence. Moreover, compressing these information-rich pages into a limited visual token budget further increases the risk of hallucinations. To address this, we introduce AgenticOCR, a dynamic parsing paradigm that transforms optical character recognition (OCR) from a static, full-text process into a query-driven, on-demand extraction system. By autonomously analyzing document layout in a "thinking with images" manner, AgenticOCR ident

---

## OB_085

**질문** 강화학습 탐험 전략 논문 두 편만 골라줘

### 답 A

<b>서론</b>
강화학습에서 <b>탐험(exploration)</b> 은 현재 최적 정책을 활용하면서도 새로운 행동을 시도하여 더 높은 보상을 얻을 수 있는 기회를 찾는 과정입니다. 이는 탐험과 이용 사이의 균형을 맞추기 때문에 어려운 문제로 인식됩니다.

<b>본론</b>
1. <b>MaxInfoRL</b>: 정보 획득을 최대화하는 내재적 보상(정보 이득) 을 통해 탐색 방향성을 부여하고, 볼츠만 탐색과 결합하여 가치 함수와 상태·보상·행동의 엔트로피를 자연스럽게 트레이드오프합니다. [2412.12098v2]
2. <b>Entropy-Guided Sequence Weighting (EGSW)</b>: 생성된 출력의 장점과 엔트로피에 따라 가중치를 동적으로 할당함으로써 정책 업데이트에서 탐험‑이용 균형을 개선하고, 온도 스케일링 소프트맥스 가중치로 고보상·고불확실 단계와 안정성을 동시에 유지합니다. [2503.22456v2]

<b>결론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 5편_: 2412.12098 MaxInfoRL: Boosting exploration in reinforcement learning th · 2404.00651 Learning Off-policy with Model-based Intrinsic Motivation Fo · 2412.15700 AIR: Unifying Individual and Collective Exploration in Coope · 2503.22456 Entropy-guided sequence weighting for efficient exploration  · 2606.10228 SHAPO: Sharpness-Aware Policy Optimization for Safe Explorat

### 답 B

<b>서론</b>
강화학습에서 <b>탐험(exploration)</b>은 현재 최선의 전략보다 더 높은 보상을 가져올 수 있는 새로운 행동을 시도하는 과정으로, 탐험과 활용 사이의 균형을 맞추는 것이 핵심 과제이다. 특히 연속 상태·행동 공간이나 다중 에이전트 환경에서는 탐색 효율을 높이는 방법이 복잡하고 어려운 문제다.

<b>본론</b>
1. <b>MaxInfoRL</b>: 정보 이득(maximizing information gain) 기반 내재적 보상을 통해 탐험 방향성을 조절하며, 볼츠만탐색과 결합하면 가치 함수 최대화와 상태·보상·행동 엔트로피 간 자연스러운 트레이드오프를 제공한다[2412.12098v2].
2. <b>Learning Off-policy with Model-based Intrinsic Motivation</b>: 예측 모델과 오피시폴리 학습을 통합하고, 신규성 인식 종단값함수를 이용해 샘플 효율적인 온라인 탐험 계획을 수행한다[2404.00651v1].

<b>결론</b>
두 논문 모두 강화학습의 탐험 문제를 다루지만, [2412.12098v2]은 다팔수기(Multi-armed bandits) 설정에서 서브선형 후회(sublinear regret)를 달성하고 연속 상태·행동 공간에서도 우수한 성능을 보인 반면, [2404.00651v1]는 연속 제어 과제에서 샘플 효율적인 탐험을 목표로 경쟁력이나 우월한 성능을 입증한다[2412.12098v2][2404.00651v1]. 따라서 두 연구는 각각 다른 데이터와 조건(다팔수기 vs 연속 제어) 에서 유사한 목표인 탐험 성능 향상을 달성했으나, 적용 대상과 평가 지표가 다르므로 결과를 직접 비교할 수는 없다.

_B 컨텍스트 5편_: 2412.12098 MaxInfoRL: Boosting exploration in reinforcement learning th · 2404.00651 Learning Off-policy with Model-based Intrinsic Motivation Fo · 2412.15700 AIR: Unifying Individual and Collective Exploration in Coope · 2503.22456 Entropy-guided sequence weighting for efficient exploration  · 2606.10228 SHAPO: Sharpness-Aware Policy Optimization for Safe Explorat

### 인용 블록

- **2412.12098** [인용 AB] MaxInfoRL: Boosting exploration in reinforcement learning through information gain maximization — [초록] Reinforcement learning (RL) algorithms aim to balance exploiting the current best strategy with exploring new options that could lead to higher rewards. Most common RL algorithms use undirected exploration, i.e., select random sequences of actions. Exploration can also be directed using intrinsic rewards, such as curiosity or model epistemic uncertainty. However, effectively balancing task and intrinsic rewards is challenging and often task-dependent. In this work, we introduce a framework, MaxInfoRL, for balancing intrinsic and extrinsic exploration. MaxInfoRL steers exploration towards informative transitions, by maximizing intrinsic rewards such as the information gain about the underlying task. When combined with Boltzmann exploration, this approach naturally trades off maximization of the value function with that of the entropy over states, rewards, and actions. We show that ou

- **2503.22456** [인용 A] Entropy-guided sequence weighting for efficient exploration in RL-based LLM fine-tuning — [초록] We introduce Entropy-Guided Sequence Weighting (EGSW), a novel approach that enhances the exploration-exploitation tradeoff by dynamically assigning weights to generated outputs based on their advantage and entropy for Reinforcement Learning-based Large Language Model fine-tuning. EGSW integrates entropy regularization with advantage-based weighting to balance policy updates, enabling efficient exploration in high-dimensional state spaces. By employing temperature-scaled softmax weighting over sequences, EGSW prioritizing high-reward, high-uncertainty steps while maintaining training stability. Although originally developed to improve Group Relative Policy Optimization (GRPO) during large language model (LLM) fine-tuning, EGSW is generalizable to other reinforcement learning (RL) algorithms and can be implemented in both step-wise and trajectory-wise settings. Empirical evaluations 

- **2404.00651** [인용 B] Learning Off-policy with Model-based Intrinsic Motivation For Active Online Exploration — [초록] Recent advancements in deep reinforcement learning (RL) have demonstrated notable progress in sample efficiency, spanning both model-based and model-free paradigms. Despite the identification and mitigation of specific bottlenecks in prior works, the agent's exploration ability remains under-emphasized in the realm of sample-efficient RL. This paper investigates how to achieve sample-efficient exploration in continuous control tasks. We introduce an RL algorithm that incorporates a predictive model and off-policy learning elements, where an online planner enhanced by a novelty-aware terminal value function is employed for sample collection. Leveraging the forward predictive error within a latent state space, we derive an intrinsic reward without incurring parameters overhead. This reward establishes a solid connection to model uncertainty, allowing the agent to effectively overcome 

---

## OB_093

**질문** 의료 영상 분석 AI 논문 두 편 추천해줘

### 답 A

<b>서론</b>
의료 영상 분석은 <b>딥러닝 기반 모델</b>과 같은 복잡한 알고리즘으로 구현되지만, 데이터 수집·정제와 검증 과정 때문에 개발 난도가 높습니다. 특히 정확한 진단에 필요한 고해상도 이미지 처리는 계산 자원 요구량이 커서 효율적인 접근법이 필요합니다.

<b>본론</b>
1. <b>Sickle Cell Disease Classification Fusion</b>: 기존 분류기, 세그먼트된 이미지를 결합하고 CNN 특징을 SVM과 함께 사용하여 정확도를 96.80%로 달성했습니다[2412.17975v1].
2. <b>Hybrid Deep Learning and Model‑Checking Framework for Brain Tumor Detection</b>: 모델 체킹 원칙에 기반한 검증 단계와 CNN 기반 특징 추출·K-FCM 클러스터링을 결합해 뇌종양 탐지 정확도 98%, 정밀도 96.15%를 달성했습니다[2501.01991v2].
3. <b>Unsupervised Denoising of Low‑Dose Liver CT with Perceptual Attention Networks</b>: 사이클 GAN 영감을 받은 엔드투엔드 비지도 학습 프레임워크로, U-Net 다중 스케일 특징 추출과 주의 메커니즘을 활용해 저선량 CT 노이즈를 제거하고 임상 평가 기준에 부합하는 성능을 보였습니다[2605.00793v1].
4. <b>AMID Autonomous Multi‑Agent Framework for Medical Imaging Model Development</b>: 데이터 조건부 방법 계획과 검증 가이드 두 단계 최적화를 통해 의료 영상 모델 개발 워크플로우를 자동화·검증 가능하게 만들었으며, 다양한 모달리티와 예측 유형에 걸쳐 기존 일반 목적 MLE 시스템을 능가했습니다[2607.10522v2].

<b>결론</b>
제공된 문서들은 의료 영상 분석 AI 분야에서 서로 다른 임상 적용 사례와 성능을 보여줍니다. 첫 번째 연구는 세그먼트 이미지와 CNN 특징을 SVM과 결합하여 96.80%의 정확도를 달성했으며, 이는 계산 효율적인 시나리오에 적합하다고 평가되었습니다 [2412.17975v1]. 두 번째 연구는 뇌 종양 검출을 위한 하이브리드 딥러닝 및 모델 검증 프레임워크를 제시하고, 실험 결과에서 98% 정확도, 96.15% 정밀도, 100% 재현율을 기록했습니다 [2501.01991v2]. 이러한 결과는 각각 다른 질병(혈액병 vs 뇌종양)과 데이터 유형에 맞춰 설계되었지만, 모두 높은 정확도를 달성한다는 점에서 공통된 우수성을 보입니다. 따라서 의료 영상 분석 AI는 특정 도메인에 따라 최적화된 모델이 존재하지만, 전반적으로 높은 성능을 유지하고 있습니다.

_A 컨텍스트 5편_: 2412.17975 Improving Sickle Cell Disease Classification: A Fusion of Co · 2501.01991 A Hybrid Deep Learning and Model-Checking Framework for Accu · 2605.00793 Unsupervised Denoising of Real Clinical Low Dose Liver CT wi · 2607.10522 Towards Autonomous and Auditable Medical Imaging Model Devel · 2412.19688 A Review on the Integration of Artificial Intelligence and M

### 답 B

<b>서론</b>
의료 영상 분석은 <b>딥러닝 기반 모델</b>과 같은 복잡한 알고리즘으로 구현되지만, 데이터 부족·노이즈 문제와 해석 가능성 요구 때문에 어려운 과제입니다. 이러한 한계를 극복하기 위해 최근 연구들은 다양한 접근법을 제시하고 있습니다.

<b>본론</b>
1. <b>Sickle Cell Disease Classification Fusion</b>: 기존 분류기, 세그멘테이션 이미지 및 CNN을 결합해 자동화된 질병 분류를 구현했으며, SVM과 함께 사용 시 정확도 96.80% 를 달성했습니다. [2412.17975v1]
2. <b>Hybrid Deep Learning and Model-Checking Framework for Brain Tumor Detection</b>: 모델 체킹 원리와 CNN 기반 특징 추출·K‑FCM 클러스터링을 결합해 뇌 종양 탐지 및 세그멘테이션의 신뢰성을 향상시켰으며, 정확도 98%, 정밀도 96.15%를 기록했습니다. [2501.01991v2]
3. <b>Unsupervised Denoising of Low‑Dose Liver CT with Perceptual Attention Networks</b>: 사이클 GAN을 영감으로 한 엔드투엔드 비지도 학습 프레임워크로, U‑Net 다중 스케일 특징 추출·주의 메커니즘·잔차 네트워크를 결합해 저선량 CT 노이즈 제거 성능을 개선했습니다. [2605.00793v1]
4. <b>AMID Autonomous Multi-Agent Framework for Medical Imaging Model Development</b>: 데이터 조건부 방법 계획과 검증 가이드 두 단계 최적화를 통해 의료 영상 모델 개발 자동화와 감사 가능성을 제공하며, 다양한 모달리티·예측 유형 과제에서 일반 목적 MLE 시스템을 능가했습니다. [2607.10522v2]

<b>결론</b>
제공된 문서들은 각각 질병 분류 정확도 향상, 뇌 종양 탐지 신뢰성 강화, 저선량 CT 노이즈 제거 성능 개선 및 의료 영상 모델 개발 자동화라는 구체적인 기여를 제시하고 있습니다. 따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 5편_: 2412.17975 Improving Sickle Cell Disease Classification: A Fusion of Co · 2501.01991 A Hybrid Deep Learning and Model-Checking Framework for Accu · 2605.00793 Unsupervised Denoising of Real Clinical Low Dose Liver CT wi · 2607.10522 Towards Autonomous and Auditable Medical Imaging Model Devel · 2412.19688 A Review on the Integration of Artificial Intelligence and M

### 인용 블록

- **2412.17975** [인용 AB] Improving Sickle Cell Disease Classification: A Fusion of Conventional Classifiers, Segmented Images, and Convolutional Neural Networks — [초록] Sickle cell anemia, which is characterized by abnormal erythrocyte morphology, can be detected using microscopic images. Computational techniques in medicine enhance the diagnosis and treatment efficiency. However, many computational techniques, particularly those based on Convolutional Neural Networks (CNNs), require high resources and time for training, highlighting the research opportunities in methods with low computational overhead. In this paper, we propose a novel approach combining conventional classifiers, segmented images, and CNNs for the automated classification of sickle cell disease. We evaluated the impact of segmented images on classification, providing insight into deep learning integration. Our results demonstrate that using segmented images and CNN features with an SVM achieves an accuracy of 96.80%. This finding is relevant for computationally efficient scenarios

- **2501.01991** [인용 AB] A Hybrid Deep Learning and Model-Checking Framework for Accurate Brain Tumor Detection and Validation — [초록] Model checking, a formal verification technique, ensures systems meet predefined requirements, playing a crucial role in minimizing errors and enhancing quality during development. This paper introduces a novel hybrid framework integrating model checking with deep learning for brain tumor detection and validation in medical imaging. By combining model-checking principles with CNN-based feature extraction and K-FCM clustering for segmentation, the proposed approach enhances the reliability of tumor detection and segmentation. Experimental results highlight the framework's effectiveness, achieving 98\% accuracy, 96.15\% precision, and 100\% recall, demonstrating its potential as a robust tool for advanced medical image analysis. Deep learning, particularly convolutional neural networks (CNNs), has revolutionized the field of medical image analysis by providing state-of-the-art perform

- **2605.00793** [인용 AB] Unsupervised Denoising of Real Clinical Low Dose Liver CT with Perceptual Attention Networks — [초록] With the development of deep learning, medical image processing has been widely used to assist clinical research. This paper focuses on the denoising problem of low-dose computed tomography using deep learning. Although low-dose computed tomography reduces radiation exposure to patients, it also introduces more noise, which may interfere with visual interpretation by physicians and affect diagnostic results. To address this problem, inspired by Cycle-GAN for unsupervised learning, this paper proposes an end-to-end unsupervised low-dose computed tomography denoising framework. The proposed framework combines a U-Net structure for multi-scale feature extraction, an attention mechanism for feature fusion, and a residual network for feature transformation. It also introduces perceptual loss to improve the network for the characteristics of medical images. In addition, we construct a rea

- **2607.10522** [인용 AB] Towards Autonomous and Auditable Medical Imaging Model Development — [초록] Large language model (LLM) agents are beginning to automate machine learning engineering (MLE) by coupling planning, code execution, debugging, and empirical feedback. Translating this capability to medical imaging remains difficult because each task imposes modality-specific experimentation and strict requirements for validation protocols and prediction artifacts. Here we introduce AMID, an autonomous multi-agent framework for medical imaging model development. AMID first proposes Data-Conditioned Method Planning, which refines coarse task-level search spaces into executable, parallelizable method lanes grounded in task-specific data analysis and runnable medical-imaging resources. It then develops Verification-Guided Two-Stage Optimization, moving from broad early exploration of diverse method lanes to selective exploitation of promising candidates while enforcing strict verificat

---

## OB_114

**질문** LLM이 지어내는 답을 줄이는 방법 세 편만 추천해줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
LLM 응답 길이를 줄이는 구체적인 방법은 제공되지 않았습니다.

<b>본론</b>
1. <b>Response Length Affects Long-Form Factuality</b>: 긴 답변은 사실 정밀도가 낮아지며, 이는 모델이 신뢰할 수 있는 지식을 점차 고갈시키기 때문임을 확인했습니다.[2505.23295v1]
2. <b>Multiple Abstraction Level Retrieve Augment Generation (MAL‑RAG)</b>: 다중 추상화 수준(다구절·단락·섹션·전체 문서) 의 청크를 검색해 답변을 생성함으로써, 기존 단일 수준의 RAG보다 정답 정확도를 크게 향상시켰습니다.[2501.16952v1]
3. <b>Structured-Semantic RAG (SSRAG)</b>: 쿼리 증강과 에이전트 라우팅을 결합하고 벡터·그래프 기반 구조화된 검색 및 컨텍스트 통합 메커니즘으로, 기존 단일‑레벨 RAG보다 정답 정확도와 정보량을 개선했습니다.[2601.12658v2]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 5편_: 2505.23295 How Does Response Length Affect Long-Form Factuality · 2501.16952 Multiple Abstraction Level Retrieve Augment Generation · 2502.14759 On the Influence of Context Size and Model Choice in Retriev · 2601.12658 Augmenting Question Answering with A Hybrid RAG Approach · 2406.09155 DefAn: Definitive Answer Dataset for LLMs Hallucination Eval

### 답 B

<b>서론</b>
제공된 참고 문서에는 <b>LLM 응답 길이 축소 방법</b>에 대한 구체적인 내용이 없습니다. 따라서 해당 주제와 직접 관련된 정보를 찾을 수 없어, 질문에서 요구한 세 가지 방법을 제시할 근거가 존재하지 않습니다.

<b>본론</b>
1. (관련 정보 없음) [2406.09155v1]는 LLM의 환각 현상을 평가하기 위한 데이터셋을 소개하고 있으며, 응답 길이 축소와는 무관합니다.

<b>결론</b>
따라서 제공된 문서에 따르면 <b>LLM이 지어내는 답을 줄이는 구체적인 방법은 제시되지 않았습니다</b>.

_B 컨텍스트 5편_: 2505.23295 How Does Response Length Affect Long-Form Factuality · 2501.16952 Multiple Abstraction Level Retrieve Augment Generation · 2502.14759 On the Influence of Context Size and Model Choice in Retriev · 2601.12658 Augmenting Question Answering with A Hybrid RAG Approach · 2406.09155 DefAn: Definitive Answer Dataset for LLMs Hallucination Eval

### 인용 블록

- **2505.23295** [인용 A] How Does Response Length Affect Long-Form Factuality — [초록] Large language models (LLMs) are widely used for long-form text generation. However, factual errors in the responses would undermine their reliability. Despite growing attention to LLM factuality, the effect of response length on factuality remains underexplored. In this work, we systematically investigate this relationship by first introducing an automatic and bi-level long-form factuality evaluation framework, which achieves high agreement with human annotations while being cost-effective. Using this framework, we conduct controlled experiments and find that longer responses exhibit lower factual precision, confirming the presence of length bias. To explain this phenomenon, we empirically examine three hypotheses: error propagation, long context, and facts exhaustion. Our results reveal that facts exhaustion, where the model gradually exhausts more reliable knowledge, is the prima

- **2501.16952** [인용 A] Multiple Abstraction Level Retrieve Augment Generation — [초록] A Retrieval-Augmented Generation (RAG) model powered by a large language model (LLM) provides a faster and more cost-effective solution for adapting to new data and knowledge. It also delivers more specialized responses compared to pre-trained LLMs. However, most existing approaches rely on retrieving prefix-sized chunks as references to support question-answering (Q/A). This approach is often deployed to address information needs at a single level of abstraction, as it struggles to generate answers across multiple levels of abstraction. In an RAG setting, while LLMs can summarize and answer questions effectively when provided with sufficient details, retrieving excessive information often leads to the 'lost in the middle' problem and exceeds token limitations. We propose a novel RAG approach that uses chunks of multiple abstraction levels (MAL), including multi-sentence-level, para

- **2601.12658** [인용 A] Augmenting Question Answering with A Hybrid RAG Approach — [초록] Retrieval-Augmented Generation (RAG) has emerged as a powerful technique for enhancing the quality of responses in Question-Answering (QA) tasks. However, existing approaches often struggle with retrieving contextually relevant information, leading to incomplete or suboptimal answers. In this paper, we introduce Structured-Semantic RAG (SSRAG), a hybrid architecture that enhances QA quality by integrating query augmentation, agentic routing, and a structured retrieval mechanism combining vector and graph based techniques with context unification. By refining retrieval processes and improving contextual grounding, our approach improves both answer accuracy and informativeness. We conduct extensive evaluations on three popular QA datasets, TruthfulQA, SQuAD and WikiQA, across five Large Language Models (LLMs), demonstrating that our proposed approach consistently improves response qua

- **2406.09155** [인용 B] DefAn: Definitive Answer Dataset for LLMs Hallucination Evaluation — [초록] Large Language Models (LLMs) have demonstrated remarkable capabilities, revolutionizing the integration of AI in daily life applications. However, they are prone to hallucinations, generating claims that contradict established facts, deviating from prompts, and producing inconsistent responses when the same prompt is presented multiple times. Addressing these issues is challenging due to the lack of comprehensive and easily assessable benchmark datasets. Most existing datasets are small and rely on multiple-choice questions, which are inadequate for evaluating the generative prowess of LLMs. To measure hallucination in LLMs, this paper introduces a comprehensive benchmark dataset comprising over 75,000 prompts across eight domains. These prompts are designed to elicit definitive, concise, and informative answers. The dataset is divided into two segments: one publicly available for t
