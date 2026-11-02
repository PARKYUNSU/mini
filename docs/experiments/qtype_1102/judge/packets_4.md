## H_C31

**질문** 요즘 나온 LLM 에이전트 논문 중에 볼만한 거 추천해줘

### 답 A

<b>서론</b>
최근 <b>LLM 기반 에이전트</b>(Agent) 연구는 복잡한 데이터 처리, 과학적 발견 지원 및 다중 턴 대화 등 다양한 분야에서 빠르게 발전하고 있습니다. 이러한 시스템은 기존 LLM의 한계(환각·해석 어려움)를 보완하면서도 전문 도메인 지식과 도구 연동을 통해 실용성을 높이고 있어 주목받고 있습니다.

<b>본론</b>
1. <b>Agentic Large Language Models</b>: 에이전트형 LLM을 ‘이유’,‘행동’,‘상호작용’ 세 범주로 분류하고, 각 분야에서 연구 현황 및 향후 과제를 제시합니다[2503.23037v3].
2. <b>LLM‑based Data Agents (Data Science Agent)</b>: 데이터 분석 패러다임을 변화시키는 에이전트로, 계획·추론·반성·멀티에이전트 협업 등 핵심 기능을 갖추고 복잡한 데이터를 최소 인간 개입으로 처리하도록 설계되었습니다[2412.14222v2].
3. <b>PaperQA</b>: 과학 문헌 전체를 검색하고 관련성을 평가한 후 RAG 방식을 이용해 질문에 답하는 에이전트로, 기존 LLM 및 다른 agent보다 현재 QA 벤치마크에서 더 높은 성능을 보입니다[2312.07559v2].

<b>결론</b>
제공된 문서들은 LLM 에이전트의 성능과 적용 가능성을 각각 다른 측면에서 보고하고 있습니다. 먼저, Agentic LLM은 추론 시 행동 생성을 통해 학습 데이터 부족 문제를 해결한다는 점을 강조합니다 [2503.23037v3]. 두 번째로, 데이터 과학 분야에 특화된 LLM 기반 데이터 에이전트는 실제 사례 연구를 통해 복잡한 데이터 작업을 단순화하고 진입 장벽을 낮춘다는 실용적 잠재력을 보여줍니다 [2412.14222v2]. 마지막으로, PaperQA는 검색 증강 생성 방식을 적용하여 기존 LLM 및 에이전트보다 현재 과학 QA 벤치마크에서 더 높은 성능을 달성한다는 결과를 제시합니다 [2312.07559v2]. 따라서 각 논문은 서로 다른 도메인(일반 에이전트, 데이터 분석, 과학 질문 답변)과 평가 기준에 따라 각각의 고유한 성과를 보고 있으며, 이는 LLM 에이전트가 다양한 분야에서 실용화되고 있음을 시사합니다.

_A 컨텍스트 5편_: 2503.23037 Agentic Large Language Models, a survey · 2412.14222 A Survey on Large Language Model-based Agents for Statistics · 2503.24047 Towards Scientific Intelligence: A Survey of LLM-based Scien · 2503.22458 Evaluating LLM-based Agents for Multi-Turn Conversations: A  · 2312.07559 PaperQA: Retrieval-Augmented Generative Agent for Scientific

### 답 B

<b>서론</b>
최근 LLM 기반 에이전트 연구에서는 추론·행동·상호작용을 결합한 시스템과 데이터 중심 문제 해결에 특화된 프레임워크가 활발히 개발되고 있습니다. 이러한 흐름 속에서 다양한 접근법을 비교해 볼 수 있는 논문들을 소개합니다.

<b>본론</b>
1. <b>Agentic Large Language Models</b>: LLM이 (1) 추론, (2) 행동, (3) 상호작용을 수행하도록 설계되었으며, 검색은 도구 사용에 기여하고 반성은 다중 에이전트 협력 등을 향상시킨다는 점을 강조한다[2503.23037v3]
2. <b>LLM‑based Agents for Statistics and Data Science</b>: 계획·추론·반성·다중 에이전트 협업 등 핵심 기능을 갖춘 프레임워크를 제시하여 최소한의 인간 개입으로 데이터 중심 문제를 해결하도록 한다[2412.14222v2]

<b>결론</b>
제공된 문서들은 LLM 에이전트 연구의 공통적인 핵심 요소인 계획, 추론, 성찰 및 다중 에이전트 협업을 강조하지만, 각각 다른 초점을 가지고 있습니다. [2503.23037v3]은 이러한 요소들이 서로 상호보완적으로 작용하며 실제 세계에서의 안전성 문제를 지적하고, 반면 [2412.14222v2]는 통계와 데이터 과학 분야에서 최소한의 인간 개입으로 데이터 중심 문제를 해결하는 데 필요한 필수 기능들을 상세히 조사합니다. 따라서 두 논문 모두 LLM 기반 에이전트의 설계 트렌드를 다루지만, 하나는 일반적인 안전성과 사회적 이점을 강조하고 다른 하나는 특정 도메인(통계·데이터 과학)에 적용 가능한 구체적인 기능 목록을 제시한다는 점에서 차이가 있습니다.

_B 컨텍스트 6편_: 2503.23037 Agentic Large Language Models, a survey · 2412.14222 A Survey on Large Language Model-based Agents for Statistics · 2503.24047 Towards Scientific Intelligence: A Survey of LLM-based Scien · 2503.22458 Evaluating LLM-based Agents for Multi-Turn Conversations: A  · 2404.00282 Survey on Large Language Model-Enhanced Reinforcement Learni · 2312.07559 PaperQA: Retrieval-Augmented Generative Agent for Scientific

### 인용 블록

- **2503.23037** [인용 AB] Agentic Large Language Models, a survey — [초록] Background: There is great interest in agentic LLMs, large language models that act as agents. Objectives: We review the growing body of work in this area and provide a research agenda. Methods: Agentic LLMs are LLMs that (1) reason, (2) act, and (3) interact. We organize the literature according to these three categories. Results: The research in the first category focuses on reasoning, reflection, and retrieval, aiming to improve decision making; the second category focuses on action models, robots, and tools, aiming for agents that act as useful assistants; the third category focuses on multi-agent systems, aiming for collaborative task solving and simulating interaction to study emergent social behavior. We find that works mutually benefit from results in other categories: retrieval enables tool use, reflection improves multi-agent collaboration, and reasoning benefits all categ

- **2412.14222** [인용 AB] A Survey on Large Language Model-based Agents for Statistics and Data Science — [초록] In recent years, data science agents powered by Large Language Models (LLMs), known as "data agents," have shown significant potential to transform the traditional data analysis paradigm. This survey provides an overview of the evolution, capabilities, and applications of LLM-based data agents, highlighting their role in simplifying complex data tasks and lowering the entry barrier for users without related expertise. We explore current trends in the design of LLM-based frameworks, detailing essential features such as planning, reasoning, reflection, multi-agent collaboration, user interface, knowledge integration, and system design, which enable agents to address data-centric problems with minimal human intervention. Furthermore, we analyze several case studies to demonstrate the practical applications of various data agents in real-world scenarios. Finally, we identify key challen

- **2312.07559** [인용 A] PaperQA: Retrieval-Augmented Generative Agent for Scientific Research — [초록] Large Language Models (LLMs) generalize well across language tasks, but suffer from hallucinations and uninterpretability, making it difficult to assess their accuracy without ground-truth. Retrieval-Augmented Generation (RAG) models have been proposed to reduce hallucinations and provide provenance for how an answer was generated. Applying such models to the scientific literature may enable large-scale, systematic processing of scientific knowledge. We present PaperQA, a RAG agent for answering questions over the scientific literature. PaperQA is an agent that performs information retrieval across full-text scientific articles, assesses the relevance of sources and passages, and uses RAG to provide answers. Viewing this agent as a question answering model, we find it exceeds performance of existing LLMs and LLM agents on current science QA benchmarks. To push the field closer to ho

---

## H_F04

**질문** 9B급 로컬 모델로 RAG를 돌릴 때 컨텍스트 문서를 5편에서 10편으로 늘리면 오히려 답 품질이 떨어지는가. 모델 크기별로 이 현상을 비교한 연구가 있는가.

### 답 A

※ 요청한 5편 중 2편만 찾았습니다.

<b>서론</b>
제공된 연구들은 <b>컨텍스트 크기(문서 수)</b>가 RAG 성능에 미치는 영향을 조사하고 있습니다. 특히 컨텍스트를 늘리면 품질이 떨어질 수도 있다는 점을 확인했습니다. 이러한 현상은 모델 크기와 상관없이 일관되게 관찰됩니다[2502.14759v1][2601.14123v1].

<b>본론</b>
1. <b>Context Size Evaluation</b>: 다양한 컨텍스트 크기(스니펫 수)와 BM25·semantic 검색기, 그리고 여덟 개의 베이스 LLM을 평가하여 최종 QA 성능이 최대 약 15개의 스니펫까지 꾸준히 향상되지만 그 이후에는 정체되거나 감소한다는 결과를 제시했습니다[2502.14759v1].
2. <b>Chunking Strategy Analysis</b>: 문서 조각화 전략(토큰·SENTENCE·SEMANTIC·CODE)과 컨텍스트 길이를 변화시켜 RAG 신뢰성을 평가한 연구에서, 과도한 컨텍스트가 존재할 때 성능이 평탄하거나 감소하는 현상이 일관되게 관찰된다고 보고했습니다[2601.14123v1].

<b>결론</b>
제공된 문서들에 따르면, <b>컨텍스트 문서를 늘리는 것만으로는 답 품질을 보장하지 않으며</b>, 오히려 일정 수준 이상으로 컨텍스트를 확대하면 성능이 정체되거나 감소할 수 있습니다. 이는 모델 크기보다는 과도한 맥락 길이가 주요 원인으로 작용한다는 점을 시사합니다[2502.14759v1][2601.14123v1].

_A 컨텍스트 3편_: 2407.19794 Introducing a new hyper-parameter for RAG: Context Window Ut · 2502.14759 On the Influence of Context Size and Model Choice in Retriev · 2601.14123 A Systematic Analysis of Chunking Strategies for Reliable Qu

### 답 B

※ 요청한 5편 중 2편만 찾았습니다.

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>On the Influence of Context Size and Model Choice in Retrieval-Augmented Generation Systems</b>: 다양한 컨텍스트 크기, BM25 및 시맨틱 검색 등 리트리버 방식과 8개의 베이스 LLM을 평가했으며, 최종 QA 성능은 최대 15개 스니펫까지 꾸준히 향상되지만 그 이후에는 정체되거나 감소한다는 결과를 제시한다. [2502.14759v1]
2. <b>A Systematic Analysis of Chunking Strategies for Reliable Question Answering</b>: 문서 청킹 방법과 크기를 변화시켜 RAG 시스템의 신뢰성을 평가했으며, 과도한 컨텍스트가 성능에 대한 평탄화 또는 감소를 초래하는 현상이 일관되게 관찰된다고 보고한다. [2601.14123v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 2편_: 2502.14759 On the Influence of Context Size and Model Choice in Retriev · 2601.14123 A Systematic Analysis of Chunking Strategies for Reliable Qu

### 인용 블록

- **2502.14759** [인용 AB] On the Influence of Context Size and Model Choice in Retrieval-Augmented Generation Systems — [초록] Retrieval-augmented generation (RAG) has emerged as an approach to augment large language models (LLMs) by reducing their reliance on static knowledge and improving answer factuality. RAG retrieves relevant context snippets and generates an answer based on them. Despite its increasing industrial adoption, systematic exploration of RAG components is lacking, particularly regarding the ideal size of provided context, and the choice of base LLM and retrieval method. To help guide development of robust RAG systems, we evaluate various context sizes, BM25 and semantic search as retrievers, and eight base LLMs. Moving away from the usual RAG evaluation with short answers, we explore the more challenging long-form question answering in two domains, where a good answer has to utilize the entire context. Our findings indicate that final QA performance improves steadily with up to 15 snippets

- **2601.14123** [인용 AB] A Systematic Analysis of Chunking Strategies for Reliable Question Answering — [초록] We study how document chunking choices impact the reliability of Retrieval-Augmented Generation (RAG) systems in industry. While practice often relies on heuristics, our end-to-end evaluation on Natural Questions systematically varies chunking method (token, sentence, semantic, code), chunk size, overlap, and context length. We use a standard industrial setup: SPLADE retrieval and a Mistral-8B generator. We derive actionable lessons for cost-efficient deployment: (i) overlap provides no measurable benefit and increases indexing cost; (ii) sentence chunking is the most cost-effective method, matching semantic chunking up to ~5k tokens; (iii) a "context cliff" reduces quality beyond ~2.5k tokens; and (iv) optimal context depends on the goal (semantic quality peaks at small contexts; exact match at larger ones). . However, the existence of a performance plateau or decline with excessiv

---

## Q_A01

**질문** 사내 RAG 챗봇 답변을 GPT-4o와 Claude로 각각 채점했더니 정답률이 72%와 85%로 갈렸다. 판정 모델에 따라 점수가 달라지는 문제를 다룬 논문을 찾아줘.

### 답 A

<b>서론</b>
제공된 질문은 <b>RAG(검색 증강 생성) 챗봇</b>에 대해 두 개의 판정 모델(GPT‑4o와 Claude)로 채점했을 때 정답률이 72%와 85%로 차이가 난다는 상황을 다루고 있습니다. 이러한 차이는 RAG 파이프라인이 적용된 경우에도 <b>모델별 성능 차이</b>가 발생한다는 점을 보여줍니다[2508.17527v1].

<b>본론</b>
1. <b>RAG‑augmented LLM framework</b>: 기본 RAG, 균형 잡힌 검색, 크로스‑엔코더 재랭킹 등 네 가지 전략을 모듈화하여 적용하고 GPT‑4o·o4‑mini·o3 세 모델에 대해 평가했습니다[2508.17527v1].

<b>결론</b>
따라서 질문에서 언급한 “판정 모델에 따라 점수가 달라지는 문제”는 RAG를 활용한 LLM 기반 예측 프레임워크가 여러 판별 모델을 대상으로 테스트되었을 때 나타나는 현상으로, 문서에서는 GPT‑4o와 o3 등 다양한 모델 간 성능 차이가 보고되고 있습니다.

_A 컨텍스트 1편_: 2508.17527 Evaluating Retrieval-Augmented Generation Strategies for Lar

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>Hybrid RAG</b>: 벡터와 그래프 기반 데이터베이스를 결합한 하이브리드 검색‑생성 시스템을 제안하고, 단일 업로드 문서를 대상으로 한 평가에서 평균 코사인 유사도 0.687과 충실도(faithfulness) 0.845의 높은 점수를 달성했습니다[2602.17856v1]. 벡터 기반 RAG와 그래프 기반 RAG를 각각 평가하여, 코사인 유사도와 충실도 측면에서 VectorRAG가 약간 더 나은 성능을 보였습니다(0.670 vs 0.654) [2602.17856v1].
<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 1편_: 2602.17856 Enhancing Scientific Literature Chatbots with Retrieval-Augm

### 인용 블록

- **2508.17527** [인용 A] Evaluating Retrieval-Augmented Generation Strategies for Large Language Models in Travel Mode Choice Prediction — [초록] Accurately predicting travel mode choice is essential for effective transportation planning, yet traditional statistical and machine learning models are constrained by rigid assumptions, limited contextual reasoning, and reduced generalizability. This study explores the potential of Large Language Models (LLMs) as a more flexible and context-aware approach to travel mode choice prediction, enhanced by Retrieval-Augmented Generation (RAG) to ground predictions in empirical data. We develop a modular framework for integrating RAG into LLM-based travel mode choice prediction and evaluate four retrieval strategies: basic RAG, RAG with balanced retrieval, RAG with a cross-encoder for re-ranking, and RAG with balanced retrieval and cross-encoder for re-ranking. These strategies are tested across three LLM architectures (OpenAI GPT-4o, o4-mini, and o3) to examine the interaction between mo

- **2602.17856** [인용 B] Enhancing Scientific Literature Chatbots with Retrieval-Augmented Generation: A Performance Evaluation of Vector and Graph-Based Systems — [초록] This paper investigates the enhancement of scientific literature chatbots through retrieval-augmented generation (RAG), with a focus on evaluating vector- and graph-based retrieval systems. The proposed chatbot leverages both structured (graph) and unstructured (vector) databases to access scientific articles and gray literature, enabling efficient triage of sources according to research objectives. To systematically assess performance, we examine two use-case scenarios: retrieval from a single uploaded document and retrieval from a large-scale corpus. Benchmark test sets were generated using a GPT model, with selected outputs annotated for evaluation. The comparative analysis emphasizes retrieval accuracy and response relevance, providing insight into the strengths and limitations of each approach. The findings demonstrate the potential of hybrid RAG systems to improve accessibilit

---

## Q_A05

**질문** 벡터 검색 결과 상위 10개 중 절반이 같은 문서의 다른 청크였다. 검색 결과 중복을 줄여 다양성을 높이는 방법을 다룬 논문을 찾아라.

### 답 A

※ 요청한 10편 중 1편만 찾았습니다.

<b>서론</b>
벡터 검색에서 상위 10개 결과에 동일한 문서가 여러 청크로 중복되어 나타나는 현상은 <b>검색 다양성</b>과 정확성을 저해하는 주요 문제입니다. 이러한 중복은 특히 대규모 문서를 다룰 때 발생하며, 관련 정보를 효율적으로 필터링하고 정제할 방법이 필요합니다[2506.14084v1].

<b>본론</b>
1. <b>Lightweight Relevance Grader</b>: RAG 파이프라인에서 검색된 문서의 관련성을 검증하기 위해 작은 언어 모델(LLaMA‑3.2‑1b)을 재학습한 경량화 relevance grader를 도입했습니다. 이 접근법은 기존 벡터 기반 검색 후 추가적인 정밀도 향상(0.7750 → 0.1301 대비 크게 증가) 을 제공하며, 관련성 판단 단계에서 중복된 청크의 유효성을 평가함으로써 다양성이 확보됩니다[2506.14084v1].

<b>결론</b>
제공된 문서들은 벡터 검색 결과에 동일한 문서를 여러 번 포함시키는 문제를 경량 relevance grader를 통해 해결하는 방법을 제시하고 있습니다. 따라서 질문이 찾는 “검색 결과 중 중복을 줄이고 다양성 높이기” 방법은 <b>Lightweight Relevance Grader</b>가 해당 접근법입니다[2506.14084v1].

_A 컨텍스트 4편_: 2509.04820 Fishing for Answers: Exploring One-shot vs. Iterative Retrie · 2505.21700 Rethinking Chunk Size For Long-Document Retrieval: A Multi-D · 2607.01601 SemHash-LLM: A Multi-Granularity Semantic Hashing Framework  · 2506.14084 Lightweight Relevance Grader in RAG

### 답 B

※ 요청한 10편 중 4편만 찾았습니다.

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 벡터 검색 결과 상위 10개 중 절반이 같은 문서의 다른 청크인 경우, 중복 제거와 다양성 확보는 대규모 데이터셋에서 효율적인 필터링과 다중 신호 활용을 필요로 하는 어려운 과제입니다.

<b>본론</b>
1. <b>SemHash LLM</b>: 문자·토큰·문서 수준의 시그널을 게이트드 퓨전으로 결합한 멀티‑그레이놀러리티 프레임워크를 제시하고, 캐스케이드 필터링 파이프라인과 선택적 LLM 기반 심판 과정을 통해 중복 감지 품질은 높이며 신경 검증 비용 1% 미만으로 유지합니다. [2607.01601v1]
2. <b>TOBUGraph</b>: 비정형 데이터에서 동적으로 지식 그래프를 구축하고, 그래프 탐색을 통한 관계·구조 활용으로 RAG의 텍스트‑텍스트 유사성 한계를 극복하며 청킹 의존성을 없애고 환각 위험도 감소시킵니다. [2412.05447v3]
3. <b>RAG-Stack</b>: 품질과 성능을 동시에 최적화하기 위한 세 가지 기둥(RAG-IR, RAG-CM, RAG‑PE)로 구성된 설계도를 제시하고, 중간 표현으로 질·성능 측면을 분리하며 비용 모델을 통해 시스템 효율성을 추정합니다. [2510.20296v1]
4. <b>Progressive Searching</b>: 저차원 임베딩에서 시작해 목표 차원으로 점진적으로 후보 집합을 정제하는 다단계 검색 알고리즘을 제안하고, 이는 높은 정확도와 빠른 속도를 동시에 달성하여 대규모 데이터베이스에서도 확장 가능한 성능을 보입니다. [2602.07297v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 5편_: 2607.01601 SemHash-LLM: A Multi-Granularity Semantic Hashing Framework  · 2412.05447 TOBUGraph: Knowledge Graph-Based Retrieval for Enhanced LLM  · 2510.20296 RAG-Stack: Co-Optimizing RAG Quality and Performance From th · 2602.07297 Progressive Searching for Retrieval in RAG · 2506.14084 Lightweight Relevance Grader in RAG

### 인용 블록

- **2506.14084** [인용 A] Lightweight Relevance Grader in RAG — [초록] Retrieval-Augmented Generation (RAG) addresses limitations of large language models (LLMs) by leveraging a vector database to provide more accurate and up-to-date information. When a user submits a query, RAG executes a vector search to find relevant documents, which are then used to generate a response. However, ensuring the relevance of retrieved documents with a query would be a big challenge. To address this, a secondary model, known as a relevant grader, can be served to verify its relevance. To reduce computational requirements of a relevant grader, a lightweight small language model is preferred. In this work, we finetuned llama-3.2-1b as a relevant grader and achieved a significant increase in precision from 0.1301 to 0.7750. Its precision is comparable to that of llama-3.1-70b. Our code is available at https://github.com/taeheej/Lightweight-Relevance-Grader-in-RAG. The ever

- **2607.01601** [인용 B] SemHash-LLM: A Multi-Granularity Semantic Hashing Framework for Document Deduplication — [초록] Large scale document deduplication must preserve semantic equivalence while remaining efficient over massive corpora. We present SemHash LLM, a multi granularity framework that unifies semantic projection hashing, attention weighted MinHash, contrastive boundary learning, and selective LLM based adjudication. The method combines character, token, and document level signals through gated fusion, then applies a cascaded filtering pipeline for efficient candidate reduction. Semantic projection hashing learns compact binary codes in distilled LLM embedding space, while attention weighted Min- Hash suppresses boilerplate and emphasizes informative content. Adaptive decision boundaries and uncertainty estimation further improve robustness across template pollution, short text perturbation, containment, and viral fragments. Experiments show that SemHash LLM achieves strong duplicate detect

- **2412.05447** [인용 B] TOBUGraph: Knowledge Graph-Based Retrieval for Enhanced LLM Performance Beyond RAG — [초록] Retrieval-Augmented Generation (RAG) is one of the leading and most widely used techniques for enhancing LLM retrieval capabilities, but it still faces significant limitations in commercial use cases. RAG primarily relies on the query-chunk text-to-text similarity in the embedding space for retrieval and can fail to capture deeper semantic relationships across chunks, is highly sensitive to chunking strategies, and is prone to hallucinations. To address these challenges, we propose TOBUGraph, a graph-based retrieval framework that first constructs the knowledge graph from unstructured data dynamically and automatically. Using LLMs, TOBUGraph extracts structured knowledge and diverse relationships among data, going beyond RAG's text-to-text similarity. Retrieval is achieved through graph traversal, leveraging the extracted relationships and structures to enhance retrieval accuracy, e

- **2510.20296** [인용 B] RAG-Stack: Co-Optimizing RAG Quality and Performance From the Vector Database Perspective — [초록] Retrieval-augmented generation (RAG) has emerged as one of the most prominent applications of vector databases. By integrating documents retrieved from a database into the prompt of a large language model (LLM), RAG enables more reliable and informative content generation. While there has been extensive research on vector databases, many open research problems remain once they are considered in the wider context of end-to-end RAG pipelines. One practical yet challenging problem is how to jointly optimize both system performance and generation quality in RAG, which is significantly more complex than it appears due to the numerous knobs on both the algorithmic side (spanning models and databases) and the systems side (from software to hardware). In this paper, we present RAG-Stack, a three-pillar blueprint for quality-performance co-optimization in RAG systems. RAG-Stack comprises: (1

- **2602.07297** [인용 B] Progressive Searching for Retrieval in RAG — [초록] Retrieval Augmented Generation (RAG) is a promising technique for mitigating two key limitations of large language models (LLMs): outdated information and hallucinations. RAG system stores documents as embedding vectors in a database. Given a query, search is executed to find the most related documents. Then, the topmost matching documents are inserted into LLMs' prompt to generate a response. Efficient and accurate searching is critical for RAG to get relevant information. We propose a cost-effective searching algorithm for retrieval process. Our progressive searching algorithm incrementally refines the candidate set through a hierarchy of searches, starting from low-dimensional embeddings and progressing into a higher, target-dimensionality. This multi-stage approach reduces retrieval time while preserving the desired accuracy. Our findings demonstrate that progressive search in R

---

## Q_A11

**질문** RAG 답의 인용 정확도를 사람 둘이 따로 매겼더니 일치율이 65%에 그쳤다. 인용 평가에서 평가자 간 불일치를 다룬 논문 알려줘.

### 답 A

<b>서론</b>
제공된 목록에는 질문에서 찾는 연구가 없습니다. 인용 정확도 평가와 관련된 핵심 용어는 <b>RAG</b>, <b>인용</b>입니다. 이러한 작업을 수행하기 위해 인간 두 명이 독립적으로 매긴 경우에도 65% 정도의 일치율만 달성한다는 점은, 현재까지 제안된 방법들이 이 문제를 충분히 해결하지 못함을 시사합니다.

<b>본론</b>
1. <b>Citation Evaluation</b>: 인용 정확도를 평가하는 방법을 제시하고, 이를 위해 인간 두 명이 독립적으로 매긴 경우에도 높은 불일치가 발생한다고 보고한다.
2. <b>RAG Citation Accuracy Benchmarking</b>: RAG 시스템의 답변에서 제공된 출처가 실제 문서와 일치 여부를 판단하기 위한 벤치마크를 소개하며, 평가자 간 일관성 문제를 강조한다.

<b>결론</b>
따라서 질문이 찾는 연구는 인용 정확도 평가를 다루며 인간 두 명이 독립적으로 매긴 경우에도 높은 불일치가 발생한다는 점을 보고한 논문들입니다.

_A 컨텍스트 0편_: 

### 답 B

<b>서론</b>
제공된 목록에는 질문에서 찾는 연구가 없습니다. 인용 정확도 평가와 인간 간 불일치를 다루는 논문은 제공되지 않았습니다.

<b>본론</b>
1. <b>RAG 답변의 인용 정확도를 두 사람이 독립적으로 매겼을 때 일치율이 65%에 그쳤다</b>: 이 결과는 RAG 기반 시스템이 생성한 응답에서 사실적 근거를 검증하는 과정에서 평가자 간 큰 불일치가 존재함을 보여줍니다[문서 X].

<b>결론</b>
따라서 질문과 직접 관련된 문서는 제공된 목록에는 없습니다.

_B 컨텍스트 0편_: 

### 인용 블록

---

## Q_C08

**질문** 검색 결과 재순위에 LLM을 쓰는 연구를 폭넓게 조사해서 알려줘

### 답 A

<b>서론</b>
검색 결과에 대해 LLM을 활용한 재순위(re‑ranking) 연구는 최근 Retrieval-Augmented Generation(RAG) 시스템에서 핵심 과제로 부상하고 있습니다. 본 요약은 제공된 문서들을 바탕으로 관련 접근법과 결과를 정리합니다.

<b>본론</b>
1. <b>LitLLMs</b>: 논문 초록으로부터 의미 있는 키워드를 추출한 뒤 외부 지식베이스를 조회해 잠재적으로 관련된 논문을 검색하는 두 단계 전략을 제안한다[2412.15249v2].
2. <b>ACL-rlg</b>: 전통적인 학술 검색 엔진과 인덱싱 방법이 이 작업에서 성능이 낮음을 강조하고, GPT‑4o가 더 나은 결과를 보이지만 데이터 오염 징후를 보인다며 LLM 기반 재순위를 간접적으로 언급한다[2502.15692v1].
3. <b>RAGSmith</b>: RAG 설계에 대해 엔드투엔드 아키텍처 검색을 수행하는 모듈식 프레임워크로, 나비어한 RAG 베이스라인보다 평균 +3.8% 향상(최대 +12.5%)을 달성한다[2511.01386v1].
4. <b>ELERAG</b>: Entity Linking에서 파생된 사실 신호를 통합해 교육용 질문‑응답 시스템의 정확도를 높이는 강화형 RAG 아키텍처이다[2512.05967v2].
5. <b>RAG Playground</b>: 하이브리드 검색 방법과 구조화된 자기평가 프롬프트를 통해 다중 지표 평가 프레임워크에서 최대 72.7% 통과율을 달성한다[2412.12322v1].
6. <b>EncouRAGe</b>: reranking 효과를 조사한 결과, 성능 향상은 미미하고 응답 지연이 증가함을 관찰했다[2511.04696v1].

<b>결론</b>
제공된 문서들은 LLM을 활용한 재순위 연구가 다양한 조건에서 서로 다른 결과를 보임을 보여줍니다. 먼저, LitLLMs 프로젝트는 도구와 시연 시스템을 제공하여 접근성을 높였으며 [2412.15249v2], ACL-rlg 데이터셋은 GPT-4o가 기존 검색 엔진보다 성능이 좋지만 데이터 오염 징후를 보인다는 점을 강조했습니다 [2502.15692v1]. 또한 RAGSmith는 평균 +3.8%의 향상과 최대 +12.5%의 검색 개선 효과를 달성했으며 [2511.01386v1], RAG Playground는 하이브리드 검색과 구조화된 자기평가 프롬프팅을 통해 72.7%의 패스율을 기록했습니다 [2412.12322v1]. 반면 EncouRAGe는 리랭킹이 성능 향상은 미미하지만 응답 지연을 증가시킨다고 보고했습니다 [2511.04696v1]. 이러한 결과들은 LLM 기반 재순위 연구가 도메인, 데이터 규모, 평가 지표에 따라 성능과 한계가 크게 달라짐을 시사합니다.

_A 컨텍스트 8편_: 2412.15249 LitLLMs, LLMs for Literature Review: Are we there yet? · 2502.15692 ACL-rlg: A Dataset for Reading List Generation · 2511.01386 RAGSmith: A Framework for Finding the Optimal Composition of · 2512.05967 Enhancing Retrieval-Augmented Generation with Entity Linking · 2412.12322 RAG Playground: A Framework for Systematic Evaluation of Ret · 2511.04696 EncouRAGe: Evaluating RAG Local, Fast, and Reliable · 2603.22376 AI Co-Scientist for Ranking: Discovering Novel Search Rankin · 2603.02153 Scaling Retrieval Augmented Generation with RAG Fusion: Less

### 답 B

<b>서론</b>
검색 결과에 대한 <b>재순위(re‑ranking)</b>는 관련성 높은 논문을 상위 순서로 배치하여 검색 품질과 효율성을 높이는 핵심 단계이다. 최근 연구에서는 이를 위해 대형 언어 모델(LLM) 을 활용한 다양한 접근법이 제안되고 있다.

<b>본론</b>
1. <b>LitLLMs</b>: LLM을 이용해 논문 초록에서 의미 있는 키워드를 추출한 후 외부 지식베이스를 조회하고, 귀속 정보를 포함한 프롬프트 기반 재순위 메커니즘으로 검색 결과를 다시 순위를 매긴다[2412.15249v2].
2. <b>InteractiveSurvey</b>: 온라인 검색과 사용자 업로드된 자료를 통해 참고 문헌을 분류·정리하며, 생성 과정에서 사용자가 인터페이스로 중간 구성 요소(참고분류, 개요 등)를 지속적으로 수정할 수 있도록 한다[2504.08762v1].

<b>결론</b>
[2412.15249v2]은 LLM을 활용한 재순위가 기존 검색 방법 대비 정규화된 회상률을 두 배로 높인다고 보고한다[2412.15249v2]. 반면, [2504.08762v1]은 인터랙티브 설문 생성 시스템이 대부분의 기존 LLM과 기존 방법을 능가한다고 평가한다[2504.08762v1]. 따라서 두 연구는 각각 재순위와 설문 생성이라는 다른 작업에서 LLM의 성능 향상을 확인하고 있다.

_B 컨텍스트 5편_: 2412.15249 LitLLMs, LLMs for Literature Review: Are we there yet? · 2501.00560 Re-evaluating Automatic LLM System Ranking for Alignment wit · 2504.08762 InteractiveSurvey: An LLM-based Personalized and Interactive · 2502.15692 ACL-rlg: A Dataset for Reading List Generation · 2511.01386 RAGSmith: A Framework for Finding the Optimal Composition of

### 인용 블록

- **2412.15249** [인용 AB] LitLLMs, LLMs for Literature Review: Are we there yet? — [초록] For retrieval, we introduce a novel two-step search strategy that first uses an LLM to extract meaningful keywords from the abstract of a paper and then retrieves potentially relevant papers by querying an external knowledge base. Our project page including a demonstration system and toolkit can be accessed here: https://litllm.github.io. ---

- **2502.15692** [인용 A] ACL-rlg: A Dataset for Reading List Generation — [초록] In this work, we introduce ACL-rlg, the largest open expert-annotated reading list dataset. Our qualitative study highlights the fact that traditional scholarly search engines and indexing methods perform poorly on this task, and GPT-4o, despite showing better results, exhibits signs of potential data contamination. ---

- **2511.01386** [인용 A] RAGSmith: A Framework for Finding the Optimal Composition of Retrieval-Augmented Generation Methods Across Datasets — [초록] We introduce RAGSmith, a modular framework that treats RAG design as an end-to-end architecture search over nine technique families and 46{,}080 feasible pipeline configurations. RAGSmith finds configurations that consistently outperform naive RAG baseline by +3.8% on average (range +1.2% to +6.9% across domains), with gains up to +12.5% in retrieval and +7.5% in generation. ---

- **2512.05967** [인용 A] Enhancing Retrieval-Augmented Generation with Entity Linking for Educational Platforms — [초록] This study proposes ELERAG, an enhanced RAG architecture that integrates a factual signal derived from Entity Linking to improve the accuracy of educational question-answering systems in Italian. They also demonstrate the potential of entity-aware RAG systems in educational environments, fostering adaptive and reliable AI-based tutoring tools. ---

- **2412.12322** [인용 A] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems — [초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. ---

- **2511.04696** [인용 A] EncouRAGe: Evaluating RAG Local, Fast, and Reliable — [초록] We introduce EncouRAGe, a comprehensive Python framework designed to streamline the development and evaluation of Retrieval-Augmented Generation (RAG) systems using Large Language Models (LLMs) and Embedding Models. We further examine the effects of reranking, observing only marginal performance improvements accompanied by higher response latency. ---

- **2504.08762** [인용 B] InteractiveSurvey: An LLM-based Personalized and Interactive Survey Paper Generation System — [초록] The exponential growth of academic literature creates urgent demands for comprehensive survey papers, yet manual writing remains time-consuming and labor-intensive. Recent advances in large language models (LLMs) and retrieval-augmented generation (RAG) facilitate studies in synthesizing survey papers from multiple references, but most existing works restrict users to title-only inputs and fixed outputs, neglecting the personalized process of survey paper writing. In this paper, we introduce InteractiveSurvey - an LLM-based personalized and interactive survey paper generation system. InteractiveSurvey can generate structured, multi-modal survey papers with reference categorizations from multiple reference papers through both online retrieval and user uploads. More importantly, users can customize and refine intermediate components continuously during generation, including reference 

---

## Q_D04

**질문** LLM 판정과 사람 판정의 차이를 분석한 연구 있어?

### 답 A

<b>서론</b>
LLM‑based <b>판정자</b>(judge)와 인간 평가자의 판단 차이는, 자동화된 모델 평가를 신뢰할 수 있는지 여부를 결정하는 핵심 문제입니다. 이러한 차이가 존재하면 동일한 데이터에 대해 서로 다른 결론이 도출될 위험이 있습니다[2610.05094v1].

<b>본론</b>
1. <b>LLM‑as‑a‑Judge 설계 비교</b>: 프롬프트와 평점 척도, 모델 선택 등 다양한 설계를 평가하여 인간 기준과 큰 차이가 있음에도 실제 편차는 작음을 확인했습니다(평균 절대 오차 0.11 점) [2610.05094v1].
2. <b>자동 판정 시스템의 신뢰성 및 충실도</b>: GPT‑4o와 ≥32B 파라미터 오픈소스 모델, Qwen2.5 14B 등 다양한 크기의 LLM을 인간 평가자와 비교했을 때 높은 상관관계를 보였습니다[2603.22214v1].
3. <b>판정자 편향 벤치마크 및 완화</b>: JudgeBiasBench를 통해 판정의 다양하고 큰 편향을 정량화했으며, bias‑aware 훈련과 강화학습·대조 학습으로 이러한 편향을 감소시켰습니다[2603.08091v4]

<b>결론</b>
제공된 문서들은 LLM 판정과 사람 판정의 차이를 분석한 연구가 존재함을 보여준다. [2610.05094v1]은 LLM judge들이 인간 기준과 유의미한 불일치를 보이지만, 평균 절대 편차가 0.11 점으로 매우 작아 실용적으로 신뢰할 수 있다고 평가한다. 또한 [2603.22214v1]는 적절한 프롬프트와 함께 GPT-4o 등 특정 모델들을 사용할 때 인간 평가와 높은 상관관계를 보인다고 보고한다. 반면 [2603.08091v4]는 현재 judge들이 다양한 편향 패턴을 보이며 자동 평가의 신뢰성을 훼손한다는 점을 지적한다. 따라서 LLM 판정은 조건에 따라 인간 판정과 유사한 수준을 유지할 수 있으나, 설계 선택과 모델에 따라 편향이 크게 달라질 수 있음을 시사한다.

_A 컨텍스트 5편_: 2610.05094 How Much Do LLM-as-a-Judge Design Choices Matter? A Systemat · 2603.22214 Evaluating the Reliability and Fidelity of Automated Judgmen · 2610.18389 PRISM: Calibrating Black-Box Judges with Counterfactual Prob · 2409.11547 Small Language Models can Outperform Humans in Short Creativ · 2603.08091 Toward Robust LLM-Based Judges: Taxonomic Bias Evaluation an

### 답 B

<b>서론</b>
LLM‑as‑a‑judge와 인간 판정 사이의 차이는 <b>판단 기준</b>, <b>프롬프트 설계</b> 및 <b>모델 선택</b>에 따라 크게 달라질 수 있어, 동일한 사실이라도 연구마다 다른 결론이 나올 위험을 안고 있다. 이러한 변이를 정량화하고 신뢰성을 평가하는 것이 핵심 과제이다[2610.05094v1].

<b>본론</b>
1. <b>LLM‑as‑a‑judge 설계 비교</b>: 프롬프트와 평점 척도 등 다양한 설계를 적용해 LLM 판정 결과를 인간 기준과 대비했으며, 평균 절대 편차(MAD)가 0.11 점으로 매우 작아 대부분의 judge를 신뢰할 수 있음을 확인했다[2610.05094v1]. 평점 척도만 변경해도 측정된 편향이 최대 0.93 포인트까지 이동하고, 상세 프롬프트 사용 시 판정 완화율이 약 28.9%p 감소하는 등 설계 선택이 결과에 큰 영향을 미친다[2610.05094v1]. 두 작업 모두에서 모델의 종류가 가장 큰 변이를 일으키는 주요 원인으로 나타났다[2610.05094v1].
<b>결론</b>
제공된 연구들은 LLM‑as‑a‑judge와 인간 판정 사이에 설계 선택과 모델에 따라 유의미한 차이가 존재함을 보여준다. 따라서 신뢰할 수 있는 자동 평가 파이프라인을 구축하려면 프롬프트·척도 등 설계를 표준화하고, 모델을 일관되게 선정해야 한다[2610.05094v1].

_B 컨텍스트 4편_: 2610.05094 How Much Do LLM-as-a-Judge Design Choices Matter? A Systemat · 2409.11547 Small Language Models can Outperform Humans in Short Creativ · 2504.13871 Human aversion? Do AI Agents Judge Identity More Harshly Tha · 2606.12754 LLMs Can Better Capture Human Judgments--With the Right Prom

### 인용 블록

- **2610.05094** [인용 AB] How Much Do LLM-as-a-Judge Design Choices Matter? A Systematic Comparison of Prompt Designs, Rating Scales, and Models — [초록] Researchers increasingly use Large Language Models as judges (LLM-as-a-judge) to evaluate model outputs. Yet there are no standards for how to design these judges. Typically, researchers choose the prompt, rating scale, and model intuitively. If these choices change the judge's verdicts, two studies can reach different conclusions about the same facts. To address this risk and to provide an empirical basis for judge designs, we evaluate 10 reasoning models across multiple designs on two tasks: a scalar rating of sentence sentiment and toxicity (over 500 items per category), as well as a binary accuracy classification of question-answer pairs (n=600). For the rating tasks, despite judges showing significant disagreements with the human ground truth, the practical size of differences is small enough to consider most judges reliable (mean absolute deviation of 0.11 points on a 1 - 7 sc

- **2603.22214** [인용 A] Evaluating the Reliability and Fidelity of Automated Judgment Systems of Large Language Models — [초록] A Large Language Model (LLM) as judge evaluates the quality of victim Machine Learning (ML) models, specifically LLMs, by analyzing their outputs. An LLM as judge is the combination of one model and one specifically engineered judge prompt that contains the criteria for the analysis. The resulting automation of the analysis scales up the complex evaluation of the victim models' free-form text outputs by faster and more consistent judgments compared to human reviewers. Thus, quality and security assessments of LLMs can cover a wide range of the victim models' use cases. Being a comparably new technique, LLMs as judges lack a thorough investigation for their reliability and agreement to human judgment. Our work evaluates the applicability of LLMs as automated quality assessors of victim LLMs. We test the efficacy of 37 differently sized conversational LLMs in combination with 5 differ

- **2603.08091** [인용 A] Toward Robust LLM-Based Judges: Taxonomic Bias Evaluation and Debiasing Optimization — [초록] Large language model (LLM)-based judges are widely adopted for automated evaluation and reward modeling, yet their judgments are often affected by judgment biases. Accurately evaluating these biases is essential for ensuring the reliability of LLM-based judges. However, existing studies typically investigate limited biases under a single judge formulation, either generative or discriminative, lacking a comprehensive evaluation. To bridge this gap, we propose JudgeBiasBench, a benchmark for systematically quantifying biases in LLM-based judges. JudgeBiasBench defines a taxonomy of judgment biases across 4 dimensions, and constructs bias-augmented evaluation instances through a controlled bias injection pipeline, covering 12 representative bias types. We conduct extensive experiments across both generative and discriminative judges, revealing that current judges exhibit significant an

---

## Q_D08

**질문** 디코딩 전략(greedy, beam, sampling)에 따라 환각이 어떻게 달라지는지 본 연구 있어?

### 답 A

<b>서론</b>
대형 언어 모델(LLM)은 토큰 단위로 순차적으로 응답을 생성하는데, 이때 사용하는 <b>디코딩 전략</b>에 따라 환각 발생률이 크게 달라집니다. 이러한 현상은 신뢰성 있는 LLM 적용의 주요 장애물로 여겨지고 있습니다.

<b>본론</b>
1. <b>Greedy Decoding</b>: 샘플링 기반 디코딩보다 벤치마크에서 더 나은 성능을 보이며, 이는 환각 감소와 관련이 있다는 증거로 제시됩니다[2309.01219v3]. 다양성과 창의성을 향상시키지만 동시에 환각 발생률을 증가시키는 것으로 보고되었습니다[2309.01219v3].
<b>결론</b>
제공된 문서에 따르면, 디코딩 전략은 LLM의 환행 현상에 직접적인 영향을 미칩니다. Greedy decoding이 샘플링 기반 방법보다 낮은 환각 비율을 보이며, top‑p/top‑k와 같은 확률적 방법은 다양성을 높이지만 동시에 환각 위험도 증가시킵니다[2309.01219v3].

_A 컨텍스트 3편_: 2309.01219 Siren's Song in the AI Ocean: A Survey on Hallucination in L · 2509.13702 DSCC-HS: A Dynamic Self-Reinforcing Framework for Hallucinat · 2404.18930 Hallucination of Multimodal Large Language Models: A Survey

### 답 B

<b>서론</b>
대형 언어 모델(LLM)에서 <b>디코딩 전략</b>에 따라 생성된 텍스트가 실제 입력이나 사전 지식과 일치하지 않는 현상인 <b>환각(hallucination)</b>은 신뢰성 문제를 야기합니다. 이러한 환각 발생률은 디코딩 방식(예: greedy, beam search, sampling 기반 방법 등) 에 크게 의존한다는 점이 연구되고 있습니다.

<b>본론</b>
1. <b>Greedy Decoding</b>: 샘플링을 사용하지 않는 그리디 디코딩이 여러 벤치마크에서 더 나은 성능을 보이며 환각 발생률이 낮습니다[2309.01219v3]. 토큰 하나씩 순차적으로 선택하는 샘플링 기반 방법들은 다양성과 창의성을 높이지만 동시에 환각이 증가합니다; 그리디 디코딩보다 벤치마크 성능에서 뒤처집니다[2309.01219v3].
2. <b>Beam Search</b>: 빔 검색은 MBR(최소 베이즈‑리스크) 디코딩과 비교될 때, 빔 크기를 5로 설정한 실험 결과에서도 환각을 줄이는 데 효과적입니다; 이는 샘플링 기반 방법보다 성능이 우수합니다[2404.00752v1].

<b>결론</b>
샘플링 기반 디코딩은 다양성과 창의성을 향상시키지만 환각 발생률을 증가시킨다는 결과가 제시된다 [2309.01219v3]. 반면, 그리디 디코딩이 여러 벤치마크에서 샘플링 기반 디코딩보다 더 나은 성능을 보인다는 증거도 있다 [2309.01219v3]. 또한, MBR 디코딩이 빔 서치를 크게 능가한다는 결과는 [2404.00752v1]에 나타나 있으나, 이는 환각과 직접적인 연관성이 없는 성능 비교이다 [2404.00752v1]. 따라서 디코딩 전략에 따라 환각 발생 정도는 달라지며, 샘플링은 다양성 증가와 함께 환각을 유발하고, 그리디는 상대적으로 낮은 환각 위험을 보인다.

_B 컨텍스트 5편_: 2309.01219 Siren's Song in the AI Ocean: A Survey on Hallucination in L · 2404.00752 On the True Distribution Approximation of Minimum Bayes-Risk · 2509.13702 DSCC-HS: A Dynamic Self-Reinforcing Framework for Hallucinat · 2604.03556 Focus Matters: Phase-Aware Suppression for Hallucination in  · 2404.18930 Hallucination of Multimodal Large Language Models: A Survey

### 인용 블록

- **2309.01219** [인용 AB] Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models — [초록] While large language models (LLMs) have demonstrated remarkable capabilities across a range of downstream tasks, a significant concern revolves around their propensity to exhibit hallucinations: LLMs occasionally generate content that diverges from the user input, contradicts previously generated context, or misaligns with established world knowledge. This phenomenon poses a substantial challenge to the reliability of LLMs in real-world scenarios. In this paper, we survey recent efforts on the detection, explanation, and mitigation of hallucination, with an emphasis on the unique challenges posed by LLMs. We present taxonomies of the LLM hallucination phenomena and evaluation benchmarks, analyze existing approaches aiming at mitigating LLM hallucination, and discuss potential directions for future research. **may also lead to hallucination** Today’s most advanced LLMs generate respo

- **2404.00752** [인용 B] On the True Distribution Approximation of Minimum Bayes-Risk Decoding — [초록] Minimum Bayes-risk (MBR) decoding has recently gained renewed attention in text generation. MBR decoding considers texts sampled from a model as pseudo-references and selects the text with the highest similarity to the others. Therefore, sampling is one of the key elements of MBR decoding, and previous studies reported that the performance varies by sampling methods. From a theoretical standpoint, this performance variation is likely tied to how closely the samples approximate the true distribution of references. However, this approximation has not been the subject of in-depth study. In this study, we propose using anomaly detection to measure the degree of approximation. We first closely examine the performance variation and then show that previous hypotheses about samples do not correlate well with the variation, but our introduced anomaly scores do. The results are the first to e

---

## Q_E04

**질문** 성공률이 낮은 웹 에이전트 과제를 분석한 연구 있어?

### 답 A

<b>서론</b>
성공률이 낮은 웹 에이전트 과제를 분석하는 것은 <b>최종 답변 평가</b>만으로는 실패 원인을 파악하기 어렵기 때문에 어려운 문제입니다. 특히, 유용한 페이지를 방문하고 잘 구성된 답안을 생성하지만 여전히 필드를 누락하거나 오래된 증거에 의존하는 경우가 발생합니다.

<b>본론</b>
1. <b>Parallel WebBench</b>: 350개의 수동으로 큐레이션된 병렬 작업과 URL 기반 궤적을 검증한 총 1,679개 기록을 포함한 벤치마크로, 웹 에이전트의 실패를 재현 가능한 트리거와 추적 진단에 초점을 맞춥니다. [2606.20724v2]
2. <b>AgentAtlas</b>: 최종 과제 성공률만 보는 기존 평가 방식을 넘어 제어‑결정 품질과 궤적 품질을 분리하는 진단 어휘 및 감사 프로토콜을 제시하며, six-state control-decision 분류와 trajectory-failure 어휘를 통해 실패 원인을 구체화합니다. [2605.20530v2]

<b>결론</b>
제공된 문서들은 성공률이 낮은 웹 에이전트 과제를 분석한 연구가 존재함을 보여준다. [2606.20724v2]은 Parallel WebBench 벤치마크를 통해 GRPO 모델이 완료율을 50.7%에서 96.0%로 향상시켰지만, 이진 정확도는 여전히 낮아 완전한 정답과 부분적 정답 사이에 격차가 있음을 보고한다. 또한 [2605.20530v2]는 AgentAtlas를 통해 에이전트 실패 원인과 영향을 분류하는 벤치마크와 프로토콜 연구를 제시하며, 이는 공개되지 않은 합성 데이터에 기반하고 있다. 따라서 두 연구 모두 웹 에이전트의 낮은 성공률을 다양한 측면에서 분석하지만, 하나는 정량적 성능 격차를 강조하고 다른 하나는 실패 유형과 평가 프로토콜을 제시한다는 점에서 초점이 다르다.

_A 컨텍스트 2편_: 2606.20724 When Web Agents Finish but Still Fail: Reproducible Triggers · 2605.20530 AgentAtlas: Beyond Outcome Leaderboards for LLM Agents

### 답 B

<b>서론</b>
성공률이 낮은 웹 에이전트 과제를 분석하는 것은 <b>최종 답변 평가만으로는 실패 원인을 파악하기 어렵기 때문에</b> 어려운 문제입니다. 특히, 유용한 페이지를 방문하고 잘 구성된 답안을 생성하면서도 필드 누락이나 오래된 증거 의존과 같은 문제를 가질 수 있습니다[2606.20724v2].

<b>본론</b>
1. <b>Parallel WebBench</b>: 검증된 URL 기반 궤적을 포함한 병렬 웹 탐색 벤치마크로, 350개의 매뉴얼 큐레이션 과업과 1,329개 재구성 기록을 제공합니다.[2606.20724v2] 인간‑만 데이터와 균형 잡힌 혼합 데이터를 사용해 훈련된 모델이 완료율을 WebExplorer-8B 대비 50.7%에서 96.0%로 향상시켰으며, GPT‑4.1-mini의 요소별 F1도 개선되었습니다.[2606.20724v2]
<b>결론</b>
제공된 문서에 따르면, 성공률이 낮은 웹 에이전트 과제를 분석하기 위해 Parallel WebBench 벤치마크와 GRPO 기반 모델이 사용되었으며, 이러한 접근은 완료율과 부분적 정확도를 크게 향상시켰지만 여전히 완전한 정답률 격차가 존재한다는 점을 보여줍니다.

_B 컨텍스트 2편_: 2606.20724 When Web Agents Finish but Still Fail: Reproducible Triggers · 2605.20530 AgentAtlas: Beyond Outcome Leaderboards for LLM Agents

### 인용 블록

- **2606.20724** [인용 AB] When Web Agents Finish but Still Fail: Reproducible Triggers and Trace Diagnostics for Parallel Web Exploration — [초록] Long-horizon web agents often fail in ways hidden by final-answer evaluation: they may visit useful pages, produce a well-formed answer, and terminate confidently while still missing fields, over-including unsupported items, or relying on stale evidence. We study these failures with Parallel WebBench, a parallel web-exploration benchmark containing 1,679 verified records: 350 manually curated parallel tasks and 1,329 reconstructed records with verified URL-based trajectories. We train WebExplorer-style agents with GRPO under human-only, balanced human-synthetic, and synthetic-heavy data mixtures. At 16k context and 16 interaction rounds, the best GRPO model improves completion over WebExplorer-8B from 50.7% to 96.0% and GPT-4.1-mini-judged element-wise F1 from 0.2489 to 0.4529, but binary accuracy remains far below completion. Trace-level analysis identifies three persistent failure

- **2605.20530** [인용 A] AgentAtlas: Beyond Outcome Leaderboards for LLM Agents — [초록] Large language model agents now act on codebases, browsers, operating systems, calendars, files, and tool ecosystems, but their evaluations often collapse behavior into final task success. AgentAtlas reframes agent evaluation as a diagnostic vocabulary and audit protocol for separating outcome success from control-decision quality and trajectory quality. The paper contributes: (i) a six-state control-decision taxonomy (Act / Ask / Refuse / Stop / Confirm / Recover); (ii) a trajectory-failure vocabulary with primary error source and downstream impact; (iii) a 0/1/2 benchmark-coverage audit over fifteen agent benchmarks; and (iv) an illustrative protocol study on a synthetic 1,342-item set evaluated with eight models under taxonomy-aware and taxonomy-blind prompt formats. The synthetic demonstration is not a public benchmark release and should not be read as a definitive model compari

---

## Q_F05

**질문** 작년에 나온 멀티에이전트 논문 중 볼만한 거 몇 개 알려줘

### 답 A

<b>서론</b>
최근 연구들은 다중 에이전트 시스템에서 협업, 학습 효율성 향상 및 복잡한 작업 자동화를 목표로 다양한 프레임워크와 벤치마크를 제시하고 있습니다. 이러한 흐름은 <b>멀티에이전트</b> 기술의 실용성을 높이는 데 초점을 맞추고 있으며, 각 접근법은 계획·실행 유연성과 통신 메커니즘을 핵심으로 합니다.

<b>본론</b>
1. <b>BMW Agents</b>: 다중 에이전트를 활용한 작업 자동화를 위한 프레임워크를 설계하고, 복잡한 사용 사례에 대한 계획을 포함하도록 했습니다 [2406.20041v3]
2. <b>Curriculum Learning + Population-based Self-Play (Pommerman)</b>: 커리큘럼 학습과 집단 기반 자기 플레이 방식을 결합한 시스템을 도입하여 통신 없이도 상위 에이전트를 능가하는 성능을 달성했습니다 [2407.00662v2]
3. <b>alem Benchmark</b>: JAX 기반으로 구축된 오픈‑엔드 다중 에이전트 조정 벤치마크를 소개하고, 현재 LLM 에이전트가 평균 약 6%의 정규화된 반환만을 얻는 결과를 보고합니다 [2606.08340v1]

<b>결론</b>
제공된 문서들에 따르면, 멀티에이전트 연구들은 각각 다른 목표와 결과를 보여줍니다. BMW Agents는 다양한 도메인에서 복잡한 사용 사례를 처리할 수 있는 유연한 에이전트 엔지니어링 프레임워크를 설계하는 데 초점을 맞추고 있습니다[2406.20041v3]. Pommerman을 대상으로 한 연구에서는 통신 없이도 동맹 에이전트가 상위 학습 에이전트를 능가한다는 실험 결과를 제시합니다[2407.00662v2]. 반면, Alem 벤치마크에 대한 평가에서는 현재 LLM 에이전트가 평균 약 6%의 정규화된 반환값으로 벤치마크를 해결하지 못하며, 통신이 조정의 가장 큰 기여 요인임을 밝힙니다[2606.08340v1]. 따라서 이러한 연구들은 모두 멀티에이전트 시스템의 성능과 한계를 다루지만, 각각 다른 평가 기준과 도메인을 대상으로 하고 있어 결과를 직접 비교하기는 어렵습니다.

_A 컨텍스트 8편_: 2406.20041 BMW Agents -- A Framework For Task Automation Through Multi- · 2407.00662 Multi-Agent Training for Pommerman: Curriculum Learning and  · 2606.08340 Benchmarking Open-Ended Multi-Agent Coordination in Language · 2604.00319 Collaborative AI Agents and Critics for Fault Detection and  · 2605.15132 APWA: A Distributed Architecture for Parallelizable Agentic  · 2412.11761 Harnessing Language for Coordination: A Framework and Benchm · 2610.12176 Recursive Self-Improvement through Multi-Agent Self-Supervis · 2606.28187 GBC: Gradient-Based Connections for Optimizing Multi-Agent S

### 답 B

<b>서론</b>
멀티에이전트 시스템은 <b>비정적 환경</b>, <b>부분 관측성</b> 및 대규모 에이전트 규모와 같은 복잡한 문제를 해결해야 하므로 설계가 어렵습니다. 이러한 어려움을 극복하기 위해 게임 이론과 강화 학습을 결합한 연구들이 주목받고 있습니다.

<b>본론</b>
1. <b>Game Theory and Multi-Agent Reinforcement Learning</b>: Nash 균형, 진화적 게임 이론, 상관된 균형을 MARL 알고리즘에 통합하여 비정성·부분 관측 문제를 해결하고 시스템의 견고성을 향상시킵니다[2412.20523v1].
2. <b>BMW Agents Framework</b>: LLM 기반 자율 에이전트를 활용해 복잡한 작업을 협업적으로 수행하며 계획‑실행 구조를 제공해 산업 응용에서 확장 가능한 워크플로우를 구현합니다[2406.20041v3].

<b>결론</b>
[2412.20523v1]은 게임 이론과 다중 에이전트 강화학습을 결합하여 복잡한 동적 환경에서 시스템의 견고성과 효과를 향상시킨다고 보고한다[2412.20523v1]. [2406.20041v3]는 다중 에이전트 접근법이 산업 응용 분야에서 큰 잠재력을 가지고 있으며, 초기 증명으로는 독립적인 작업을 수행하는 세 개의 에이전트가 존재함을 제시한다[2406.20041v3]. 두 논문 모두 다중 에이전트 시스템의 성능 향상에 초점을 맞추지만, [2412.20523v1]은 이론적 결합을 통한 견고성 강조와 [2406.20041v3]는 실제 산업 적용 가능성과 초기 구현 사례를 다루어 연구 방향이 다르다.

_B 컨텍스트 5편_: 2412.20523 Game Theory and Multi-Agent Reinforcement Learning : From Na · 2406.20041 BMW Agents -- A Framework For Task Automation Through Multi- · 2503.23615 An Organizationally-Oriented Approach to Enhancing Explainab · 2407.00662 Multi-Agent Training for Pommerman: Curriculum Learning and  · 2605.03986 From Intent to Execution: Composing Agentic Workflows with A

### 인용 블록

- **2406.20041** [인용 AB] BMW Agents -- A Framework For Task Automation Through Multi-Agent Collaboration — [초록] Early proof of this technology can be found in various demonstrations of agents solving complex tasks, interacting with external systems to augment their knowledge, and triggering actions. In this work, we focus on designing a flexible agent engineering framework with careful attention to planning and execution, capable of handling complex use case applications across various domains. ---

- **2407.00662** [인용 A] Multi-Agent Training for Pommerman: Curriculum Learning and Population-based Self-Play Approach — [초록] This study introduces a system designed to train multi-agent systems to play Pommerman using a combination of curriculum learning and population-based self-play. Our experimental results demonstrate that our trained agent can outperform top learning agents without requiring communication among allied agents. ---

- **2606.08340** [인용 A] Benchmarking Open-Ended Multi-Agent Coordination in Language Agents — [초록] We introduce $alem$, a JAX-based benchmark for open-ended multi-agent coordination built on Craftax-like dynamics. Current LLM agents remain far from solving alem, averaging only ~6% normalised return, but their failures are not uniform. Ablations show that communication is the largest contributor to coordination, while memory and reasoning help when used to maintain multi-step plans. ---

- **2412.20523** [인용 B] Game Theory and Multi-Agent Reinforcement Learning : From Nash Equilibria to Evolutionary Dynamics — [초록] This paper explores advanced topics in complex multi-agent systems building upon our previous work. We examine four fundamental challenges in Multi-Agent Reinforcement Learning (MARL): non-stationarity, partial observability, scalability with large agent populations, and decentralized learning. The paper provides mathematical formulations and analysis of recent algorithmic advancements designed to address these challenges, with a particular focus on their integration with game-theoretic concepts. We investigate how Nash equilibria, evolutionary game theory, correlated equilibrium, and adversarial dynamics can be effectively incorporated into MARL algorithms to improve learning outcomes. Through this comprehensive analysis, we demonstrate how the synthesis of game theory and MARL can enhance the robustness and effectiveness of multi-agent systems in complex, dynamic environments. Oth

---

## Q_H02

**질문** DPO vs KTO 장단점 알려줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>Direct Preference Optimization (DPO)</b>: DPO는 RLHF에서 보상 모델을 먼저 학습하고 정책을 최적화하는 복잡한 과정을 없애고, 간단한 이진 교차 엔트로피 손실로 직접 선호 데이터를 이용해 정책의 최적해를 닫힌 형태로 유도합니다[2305.18290v3].
2. <b>Kahneman‑Tversky Optimization (KTO)</b>: KTO는 기존 DPO와 함께 최근 발전된 직관적인 정렬 방법 중 하나로 언급되며, instruction fine-tuning과 비교했을 때 가이드라인 준수를 향상시키는 것으로 평가됩니다[2406.18954v1]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 4편_: 2412.15244 MPPO: Multi Pair-wise Preference Optimization for LLMs with  · 2305.18290 Direct Preference Optimization: Your Language Model is Secre · 2412.16145 Offline Reinforcement Learning for LLM Multi-Step Reasoning · 2406.18954 Alignment For Performance Improvement in Conversation Bots

### 답 B

<b>서론</b>
DPO와 KTO는 모두 인간 피드백과 LLM 정렬을 목표로 하는 선호 최적화 방법이지만, 각각 다른 설계 원칙 때문에 장단점이 존재합니다. 특히 DPO는 보상 모델을 직접 매핑하고 간단한 분류 손실을 사용한다는 점에서 구현이 간단하지만, 데이터 요구사항에 제한이 있습니다[2305.18290v3]. KTO는 문서에서 언급되지 않아 본론 항목으로 포함하지 않습니다.

<b>본론</b>
1. <b>Direct Preference Optimization (DPO)</b>: RLHF 파이프라인을 선호 분류 문제로 변환하고 언어 모델과 참조 모델을 이용해 암묵적 보상 함수를 형성합니다. 간단한 이진 교차 엔트로피 손실로 최적 정책을 직접 유도하며, 샘플링이나 복잡한 하이퍼파라미터 튜닝 없이도 안정적이고 효율적으로 학습됩니다[2305.18290v3].
- 장점: 구현이 간단하고 계산량이 적으며, 기존 RLHF보다 감정 제어와 요약·대화 품질에서 동등하거나 더 나은 성능을 보입니다.
- 단점: 참조 모델을 필요로 하므로 추가 GPU 메모리와 비용이 발생하며, 데이터가 엄격한 양의/음성 선호 쌍으로 제한됩니다[2412.15244v1].

<b>결론</b>
제공된 문서들은 DPO와 MPPO의 성능을 비교하고 있습니다. [2412.15244v1]에 따르면, Arena-Hard 벤치마크에서 MPPO가 DPO를 크게 앞지르는 결과를 보였습니다. 이는 MPPO가 DPO보다 선호 최적화 작업에서 뛰어난 장점을 가짐을 시사합니다. 또한 [2305.18290v3]는 DPO가 기존 RLHF 기반 방법과 비교해 감정 제어와 응답 품질 측면에서 동등하거나 더 나은 성능을 발휘한다고 보고 있습니다. 따라서 DPO는 간단한 구현과 훈련으로 인간 선호에 잘 정렬되지만, MPPO는 특정 벤치마크에서는 DPO를 능가하는 성능을 보입니다.

_B 컨텍스트 5편_: 2412.15244 MPPO: Multi Pair-wise Preference Optimization for LLMs with  · 2305.18290 Direct Preference Optimization: Your Language Model is Secre · 2407.00693 BAPO: Base-Anchored Preference Optimization for Overcoming F · 2503.22137 Sharpe Ratio-Guided Active Learning for Preference Optimizat · 2412.16145 Offline Reinforcement Learning for LLM Multi-Step Reasoning

### 인용 블록

- **2305.18290** [인용 AB] Direct Preference Optimization: Your Language Model is Secretly a Reward Model — [초록] While large-scale unsupervised language models (LMs) learn broad world knowledge and some reasoning skills, achieving precise control of their behavior is difficult due to the completely unsupervised nature of their training. Existing methods for gaining such steerability collect human labels of the relative quality of model generations and fine-tune the unsupervised LM to align with these preferences, often with reinforcement learning from human feedback (RLHF). However, RLHF is a complex and often unstable procedure, first fitting a reward model that reflects the human preferences, and then fine-tuning the large unsupervised LM using reinforcement learning to maximize this estimated reward without drifting too far from the original model. In this paper we introduce a new parameterization of the reward model in RLHF that enables extraction of the corresponding optimal policy in clo

- **2406.18954** [인용 A] Alignment For Performance Improvement in Conversation Bots — [초록] This paper shows that alignment methods can achieve superior adherence to guardrails compared to instruction fine-tuning alone in conversational agents, also known as bots, within predefined guidelines or 'guardrails'. It examines traditional training approaches such as instruction fine-tuning and the recent advancements in direct alignment methods like Identity Preference Optimization (IPO), and Kahneman-Tversky Optimization (KTO). The effectiveness of alignment techniques both pre and post-instruction tuning is highlighted, illustrating their potential to optimize conversational bots in domains that require strict adherence to specified rules, such as customer care. ## _B. DPO_ A major disadvantage of directly optimising the RLHF objective was that it required training a Reward Model first and then optimize the policy based on it. This was an extremely expensive process as it requ

- **2412.15244** [인용 B] MPPO: Multi Pair-wise Preference Optimization for LLMs with Arbitrary Negative Samples — [초록] Aligning Large Language Models (LLMs) with human feedback is crucial for their development. Existing preference optimization methods such as DPO and KTO, while improved based on Reinforcement Learning from Human Feedback (RLHF), are inherently derived from PPO, requiring a reference model that adds GPU memory resources and relies heavily on abundant preference data. Meanwhile, current preference optimization research mainly targets single-question scenarios with two replies, neglecting optimization with multiple replies, which leads to a waste of data in the application. This study introduces the MPPO algorithm, which leverages the average likelihood of model responses to fit the reward function and maximizes the utilization of preference data. Through a comparison of Point-wise, Pair-wise, and List-wise implementations, we found that the Pair-wise approach achieves the best perform
