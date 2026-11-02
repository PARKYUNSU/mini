## H_C25

**질문** 법률 분야에 LLM을 적용한 연구 찾아줘

### 답 A

<b>서론</b>
법률 분야에서 대형 언어 모델(LLM)을 활용한 연구는 주로 판결 예측, 법률 조문 경쟁 탐지 및 신뢰성 향상 등을 목표로 합니다. 이러한 접근들은 효율성과 정확성을 동시에 개선하려는 시도로 진행되고 있습니다.

<b>본론</b>
1. <b>AgentsBench</b>: LLM 기반 다중 에이전트 프레임워크를 제안하여 사법 결정의 효율성과 품질을 동시 개선을 목적으로 실험 수행, 기존 방법보다 성능과 의사결정 질에서 우수함 [2412.18697v1]
2. <b>Legal Article Competition Detection (LACD)</b>: CAM-Re2라는 새로운 검색 방법을 통해 경쟁 조항 탐지 과제에서 오탐률 감소와 정밀도 향상 달성한 연구 제시됨 [2412.11787v1]
3. <b>NyayaAnumana &amp; INLegalLlama</b>: 인도 법률 판결 예측 데이터셋과 전용 언어 모델을 소개하고, 다양한 법원 데이터를 포함함으로써 모델 정확도가 약 90% F1‑score로 크게 개선된 실험 결과 보고함 [2412.08385v1]

<b>결론</b>
제공된 문서들에 따르면, 법률 분야에 LLM을 적용한 연구들은 모두 성능 향상을 보고하고 있다. 첫 번째 연구는 법적 판결 예측 과제에서 기존 LLM 기반 방법보다 성능과 결정 품질이 우수함을 보였다 [2412.18697v1]. 두 번째 연구는 한국 형사법 관련 법률 조문 경쟁 탐지 작업에서 기존 방법을 능가하며 위양성률을 20.8%, 위음성률을 8.3% 감소시켰다 [2412.11787v1]. 세 번째 연구는 인도 법원 데이터를 활용해 모델 정확도를 크게 향상시켜 예측 과제에서 약 90% F1 점수를 달성했다 [2412.08385v1]. 따라서 각 연구는 서로 다른 데이터와 과제를 대상으로 하였지만, 모두 LLM 기반 접근법이 기존 방법보다 우수한 결과를 얻었다는 점에서 결론은 일치한다.

_A 컨텍스트 10편_: 2412.18697 Agents on the Bench: Large Language Model Based Multi Agent  · 2412.11787 A Method for Detecting Legal Article Competition for Korean  · 2412.08385 NyayaAnumana & INLegalLlama: The Largest Indian Legal Judgme · 2502.20364 Bridging Legal Knowledge and AI: Retrieval-Augmented Generat · 2608.28593 Statutory AI: Aligning Large Language Models With Legal Norm · 2412.20468 A Comprehensive Framework for Reliable Legal AI: Combining S · 2605.17691 Validate Your Authority: Benchmarking LLMs on Multi-Label Pr · 2603.15094 Bridging National and International Legal Data: Two Projects · 2606.20929 Peeking Inside LLMs: Leveraging Internal Artifacts of LLMs f · 2602.23371 Domain-Partitioned Hybrid RAG for Legal Reasoning: Toward Mo

### 답 B

<b>서론</b>
법률 분야에서 <b>대형 언어 모델(LLM)</b> 을 적용하는 연구는 복잡한 법조문 해석과 판례 예측 등 전문적인 법적 지식을 LLM에 학습시켜야 하기 때문에 어려운 과제이다. 이러한 복잡성을 해결하기 위해 다양한 접근법이 제안되고 있다.

<b>본론</b>
1. <b>AgentsBench</b>: 다중 에이전트 프레임워크를 통해 재판소의 협상·결정 과정을 시뮬레이션하고, 효율성과 결정 품질을 동시에 향상시킨다[2412.18697v1].
2. <b>Legal Article Competition Detection (LACD)</b>: CAM‑Re2라는 새로운 검색 방법을 제안하여 법조항 간의 경쟁 관계를 탐지한다[2412.11787v1].

<b>결론</b>
제공된 문서들에 따르면, 법률 분야에 LLM을 적용한 연구는 모두 성능 향상을 보고하고 있다. [2412.18697v1]은 법적 판단 예측 과제에서 제안된 프레임워크가 기존 LLM 기반 방법보다 성능과 결정 품질 측면에서 우수함을 보여주었다. 또한 [2412.11787v1]에서는 LLM 생성 구성 요소를 도입함으로써 일부 법률 AI 작업의 성능을 향상시켰다고 언급한다. 따라서 두 연구 모두 LLM 적용이 법률 관련 과제의 성능 개선에 긍정적인 영향을 미친다는 점에서 결론은 일치한다.

_B 컨텍스트 5편_: 2412.18697 Agents on the Bench: Large Language Model Based Multi Agent  · 2412.11787 A Method for Detecting Legal Article Competition for Korean  · 2412.08385 NyayaAnumana & INLegalLlama: The Largest Indian Legal Judgme · 2502.20364 Bridging Legal Knowledge and AI: Retrieval-Augmented Generat · 2608.28593 Statutory AI: Aligning Large Language Models With Legal Norm

### 인용 블록

- **2412.18697** [인용 AB] Agents on the Bench: Large Language Model Based Multi Agent Framework for Trustworthy Digital Justice — [초록] To address these challenges, we propose a large language model based multi-agent framework named AgentsBench, which aims to simultaneously improve both efficiency and quality in judicial decision-making. We conducted experiments on legal judgment prediction task, and the results show that our framework outperforms existing LLM based methods in terms of performance and decision quality. ---

- **2412.11787** [인용 AB] A Method for Detecting Legal Article Competition for Korean Criminal Law Using a Case-augmented Mention Graph — [초록] In this paper, we propose a new legal AI task called Legal Article Competition Detection (LACD), which aims to identify competing articles within a given law. Our novel retrieval method, CAM-Re2, outperforms existing relevant methods, reducing false positives by 20.8% and false negatives by 8.3%, while achieving a 98.2% improvement in precision@5, for the LACD task. ---

- **2412.08385** [인용 A] NyayaAnumana & INLegalLlama: The Largest Indian Legal Judgment Prediction Dataset and Specialized Language Model for Enhanced Decision Analysis — [초록] This paper introduces NyayaAnumana, the largest and most diverse corpus of Indian legal cases compiled for LJP, encompassing a total of 7,02,945 preprocessed cases. Our experiments demonstrate that incorporating diverse court data significantly boosts model accuracy, achieving approximately 90% F1-score in prediction tasks. ---

---

## H_D16

**질문** 오픈소스 LLM이랑 상용 LLM은 RAG 답변 품질이 얼마나 차이 나? 비교한 연구 알려줘

### 답 A

<b>서론</b>
RAG 시스템에서 <b>오픈소스 LLM</b>과 <b>상용(프롭라이어터리) LLM</b> 간의 답변 품질 차이는 모델 자체 성능뿐만 아니라 검색 전략, 프롬프트 엔지니어링 등 전체 파이프라인에 따라 달라집니다. 이러한 차이점을 정량적으로 비교하기 위해서는 다양한 언어 모델을 동일한 평가 프레임워크에서 테스트한 연구가 필요합니다.

<b>본론</b>
1. <b>RAG Playground</b>: 오픈소스 LLM(Llama 3.1, Qwen 2.5)을 포함한 여러 모델과 검색 전략(나임 벡터 탐색, 리랭킹, 하이브리드 검색 등) 을 비교하는 평가 프레임워크를 제시하고, 프롬프트 엔지니어링이 RAG 성능에 중요한 영향을 미친다는 결과를 보여줍니다[2412.12322v1].
2. <b>CRAG 재현</b>: 오픈소스 파이프라인으로 CRAG 시스템을 복제하여 PopQA와 ARC‑Challenge에서 기존 시스템과 유사한 성과를 달성했으며, T5 기반 검색 평가자에 대한 SHAP 분석을 통해 주요 실패 모드를 식별했습니다[2603.16169v1].

<b>결론</b>
제공된 문서들은 오픈소스와 상용 LLM의 RAG 성능을 직접 비교한 연구가 아니며, 각각 다른 평가 대상과 결과를 제시하고 있습니다. [2603.16169v1]은 오픈소스 파이프라인이 PopQA와 ARC-Challenge 데이터셋에서 원래 시스템과 유사한 성능을 보였으며, 과학 질문 도메인 전이에 한계가 있음을 지적합니다. 반면 [2412.12322v1]는 하이브리드 검색 및 구조화된 자기평가 프롬프트를 적용했을 때 다중 지표 평가 프레임워크에서 최대 72.7%의 패스율을 달성하고, 커스텀 프롬프트 에이전트가 일관된 성능 향상을 보였음을 보고합니다. 따라서 두 연구는 모두 RAG 시스템 개선 가능성을 확인하지만, 비교 대상과 평가 데이터가 달라 직접적인 오픈소스와 상용 모델 간 성능 격차를 제시하지는 않습니다.

_A 컨텍스트 3편_: 2603.16169 Open-Source Reproduction and Explainability Analysis of Corr · 2412.12322 RAG Playground: A Framework for Systematic Evaluation of Ret · 2604.02259 Retrieval-Augmented Question Answering over Scientific Liter

### 답 B

<b>서론</b>
오픈소스 LLM과 상용(커머스) LLM 사이의 <b>RAG 답변 품질</b> 차이는 모델 크기·훈련 데이터와 외부 지식 검색 전략에 따라 달라지기 때문에, 동일한 RAG 파이프라인을 적용했을 때 성능 격차를 정량화하는 것이 중요합니다.

<b>본론</b>
1. <b>MedRGB</b>: 의료 도메인에서 상용 및 오픈소스 LLM들을 다양한 Retrieval 조건 하에 평가하여 현재 모델이 검색된 문서의 노이즈와 허위 정보 처리 능력이 제한적임을 확인했습니다[2411.09213v1].
2. <b>RAG Playground</b>: RAG 시스템 평가를 위해 Naive Vector Search, Re‑ranking, Hybrid Vector‑Keyword Search 등 세 가지 Retrieve 전략을 구현·비교하고, Llama 3.1과 Qwen 2.5를 사용해 성능 차이를 측정했습니다[2412.12322v1].
3. <b>Chat3GPP</b>: 오픈소스 RAG 프레임워크로 제시되며, Chunking 및 Hybrid Retrieval 등을 활용해 도메인‑특화 데이터셋에서 기존 방법보다 우수한 결과를 보였습니다[2501.13954v1] (이 연구는 상용 LLM과의 직접 비교를 포함하지 않습니다).

<b>결론</b>
제공된 문서들은 오픈소스 LLM과 상용 LLM의 RAG 답변 품질 차이를 직접 비교한 연구가 없습니다. [2412.12322v1]는 하이브리드 검색 및 구조화된 자기평가 프롬프트를 적용했을 때 다중 지표 평가 프레임워크에서 최대 72.7%의 통과율을 달성했다고 보고합니다. 또한, [2501.13954v1]는 Chat3GPP라는 오픈소스 RAG 프레임워크가 기존 방법보다 우수한 성능을 보였으며, 이는 특정 도메인(통신) 데이터셋에서 평가된 결과임을 밝힙니다. 반면, [2411.09213v1]는 의료 질문 답변에 대한 RAG 시스템 평가를 통해 현재 모델이 검색 문서의 노이즈와 허위 정보를 처리하는 능력이 제한적이라고 지적합니다. 따라서 제공된 연구들은 오픈소스 LLM 기반 RAG가 특정 도메인이나 개선 전략 적용 시 기존 방법보다 성능을 향상시킬 수 있음을 보여주지만, 오픈소스와 상용 모델 간의 직접적인 품질 차이는 제시하지 않습니다.

_B 컨텍스트 5편_: 2503.24307 A Systematic Evaluation of LLM Strategies for Mental Health  · 2412.12322 RAG Playground: A Framework for Systematic Evaluation of Ret · 2604.02259 Retrieval-Augmented Question Answering over Scientific Liter · 2501.13954 Chat3GPP: An Open-Source Retrieval-Augmented Generation Fram · 2411.09213 Comprehensive and Practical Evaluation of Retrieval-Augmente

### 인용 블록

- **2412.12322** [인용 AB] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems — [초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical results comparing different language models (Llama 3.1 and Qwen 2.5) across various retrieval configurations. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. The results also highlight the importance of prompt engineering in RAG systems, with our custom-prompted agents showing consistent improvements in retrieval ac

- **2603.16169** [인용 A] Open-Source Reproduction and Explainability Analysis of Corrective Retrieval Augmented Generation — [초록] Corrective Retrieval Augmented Generation (CRAG) improves the robustness of RAG systems by evaluating retrieved document quality and triggering corrective actions. However, the original implementation relies on proprietary components including the Google Search API and closed model weights, limiting reproducibility. In this work, we present a fully open-source reproduction of CRAG, replacing proprietary web search with the Wikipedia API and the original LLaMA-2 generator with Phi-3-mini-4k-instruct. We evaluate on PopQA and ARC-Challenge, demonstrating that our open-source pipeline achieves comparable performance to the original system. Furthermore, we contribute the first explainability analysis of CRAG's T5-based retrieval evaluator using SHAP, revealing that the evaluator primarily relies on named entity alignment rather than semantic similarity. Our analysis identifies key failu

- **2411.09213** [인용 B] Comprehensive and Practical Evaluation of Retrieval-Augmented Generation Systems for Medical Question Answering — [초록] Retrieval-augmented generation (RAG) has emerged as a promising approach to enhance the performance of large language models (LLMs) in knowledge-intensive tasks such as those from medical domain. However, the sensitive nature of the medical domain necessitates a completely accurate and trustworthy system. While existing RAG benchmarks primarily focus on the standard retrieve-answer setting, they overlook many practical scenarios that measure crucial aspects of a reliable medical system. This paper addresses this gap by providing a comprehensive evaluation framework for medical question-answering (QA) systems in a RAG setting for these situations, including sufficiency, integration, and robustness. We introduce Medical Retrieval-Augmented Generation Benchmark (MedRGB) that provides various supplementary elements to four medical QA datasets for testing LLMs' ability to handle these sp

- **2501.13954** [인용 B] Chat3GPP: An Open-Source Retrieval-Augmented Generation Framework for 3GPP Documents — [초록] The 3rd Generation Partnership Project (3GPP) documents is key standards in global telecommunications, while posing significant challenges for engineers and researchers in the telecommunications field due to the large volume and complexity of their contents as well as the frequent updates. Large language models (LLMs) have shown promise in natural language processing tasks, but their general-purpose nature limits their effectiveness in specific domains like telecommunications. To address this, we propose Chat3GPP, an open-source retrieval-augmented generation (RAG) framework tailored for 3GPP specifications. By combining chunking strategies, hybrid retrieval and efficient indexing methods, Chat3GPP can efficiently retrieve relevant information and generate accurate responses to user queries without requiring domain-specific fine-tuning, which is both flexible and scalable, offering 

---

## H_G09

**질문** 임베딩 모델 연구들을 비교해서 한국어 검색 서비스에 어떤 걸 쓰면 좋을지 추천해줘

### 답 A

<b>서론</b>
제공된 문서들은 텍스트 임베딩과 대형 언어 모델(LLM)을 결합한 연구들을 다루고 있으며, 이를 통해 검색 서비스 설계에 활용할 수 있는 다양한 접근법을 제시합니다. 핵심 용어는 <b>텍스트 임베딩</b>, <b>대형 언어 모델 (LLM)</b>, 그리고 <b>검색 성능 향상</b>입니다.

<b>본론</b>
1. <b>LLM‑augmented text embedding</b>: LLM을 활용해 기존 텍스트 임베딩 방법을 강화하는 연구가 소개됩니다[2412.09165v4].
2. <b>Embedding 기반 검색 벡터 변환</b>: 학생의 관심사를 자연어 쿼리로 표현한 뒤, 이를 임베딩으로 변환해 유사 콘텐츠를 가진 과목을 찾습니다[2412.19312v2].

<b>결론</b>
제공된 문서들은 임베딩 모델 연구 결과를 비교하여 한국어 검색 서비스에 적합한 모델을 선택하는 데 직접적인 근거를 제시하지 않습니다. [2412.09165v4]은 LLM과 텍스트 임베딩의 상호작용을 세 가지 주제로 분류하지만, 구체적인 성능 비교나 추천은 포함하고 있지 않으며, [2412.19312v2]는 자연어 쿼리를 임베딩 벡터로 변환하여 유사한 콘텐츠를 찾는 검색 시스템을 설명합니다. 따라서 현재 제공된 정보만으로는 특정 임베딩 모델을 한국어 검색 서비스에 적용할지 여부를 판단하기 어렵습니다.

_A 컨텍스트 4편_: 2412.09165 When Text Embedding Meets Large Language Model: A Comprehens · 2412.19312 From Interests to Insights: An LLM Approach to Course Recomm · 2507.21989 Benchmarking Filtered Approximate Nearest Neighbor Search Al · 2407.15831 NV-Retriever: Improving text embedding models with effective

### 답 B

<b>서론</b>
제공된 문서들은 모두 <b>임베딩 기반 검색·추천 시스템</b>, 지식 그래프, 그리고 대규모 언어 모델(LLM)을 활용한 접근법을 다루고 있습니다. 이러한 연구들을 비교하면 한국어 텍스트와 콘텐츠에 맞는 임베딩 모델을 선택하는 데 도움이 됩니다.

<b>본론</b>
1. <b>Embedding‑based Course Search</b>: 커리큘럼 설명을 임베딩 벡터로 변환하고, 유사한 콘텐츠를 가진 실제 과목을 찾기 위해 임베딩 간 Similarity를 비교합니다[2412.19312v2].
2. <b>KGSR-ADS (Knowledge Graph and Deep Learning-Based Semantic Recommendation Database System)</b>: 지식 그래프와 딥러닝 기반의 계층적 구조가 정확한 의미 매칭과 확장 가능한 검색을 가능하게 합니다[2601.00833v1].
3. <b>arxiv‑for‑fanns Dataset</b>: 트랜스포머 임베딩 벡터를 사용하여 arXiv 논문 초록에 대한 필터링된 근접 이웃(FANNS) 알고리즘 벤치마크를 제공합니다[2507.21989v3].

<b>결론</b>
제공된 문서들은 임베딩 기반 검색 시스템의 적용 사례와 성능 비교 결과를 제시하고 있습니다. [2412.19312v2]은 자연어 쿼리를 임베딩 벡터로 변환하여 유사한 콘텐츠를 찾는 방법을 소개하며, 이는 일반적인 콘텐츠 추천에 활용될 수 있음을 보여줍니다. [2601.00833v1]는 지식 그래프와 딥러닝을 결합한 계층적 아키텍처가 대규모 이질적인 워크로드에서도 정확한 의미 매칭과 확장 가능한 검색을 가능하게 한다고 강조합니다. 또한 [2507.21989v3]은 트랜스포머 기반 임베딩 벡터를 활용한 근접 이웃 검색 알고리즘들을 벤치마크하여, 구체적인 사용 사례에 따라 가장 적합한 FANNS 방법을 선택하도록 eight 가지 핵심 관찰 결과를 제시합니다. 따라서 한국어 검색 서비스에는 대규모 데이터와 다양한 속성을 다루는 경우 [2601.00833v1]의 확장성 있는 아키텍처를 고려하고, 특정 도메인이나 제한된 규모에서는 [2507.21989v3]에서 제시한 알고리즘 선택 가이드라인을 적용하는 것이 타당합니다.

_B 컨텍스트 10편_: 2412.19312 From Interests to Insights: An LLM Approach to Course Recomm · 2601.00833 A Knowledge Graph and Deep Learning-Based Semantic Recommend · 2507.21989 Benchmarking Filtered Approximate Nearest Neighbor Search Al · 2610.24481 DuoLM: Fast and Effective Personalized Recommendation with L · 2404.00579 A Review of Modern Recommender Systems Using Generative Mode · 2407.15831 NV-Retriever: Improving text embedding models with effective · 2412.13432 Large Language Model Enhanced Recommender Systems: A Survey · 2402.13750 Breaking the Barrier: Utilizing Large Language Models for In · 2410.04949 Leverage Knowledge Graph and Large Language Model for Law Ar · 2606.06779 Mind the Gap: Bridging Behavioral Silos with LLMs in Multi-V

### 인용 블록

- **2412.09165** [인용 A] When Text Embedding Meets Large Language Model: A Comprehensive Survey — [초록] In this survey, we categorize the interplay between LLMs and text embeddings into three overarching themes: (1) LLM-augmented text embedding, enhancing traditional embedding methods with LLMs; (2) LLMs as text embedders, adapting their innate capabilities for high-quality embedding; and (3) Text embedding understanding with LLMs, leveraging LLMs to analyze and interpret embeddings. ---

- **2412.19312** [인용 AB] From Interests to Insights: An LLM Approach to Course Recommendations Using Natural Language Queries — [초록] The curricular environment is also dynamic, and poor communication and search functions on campus can limit a student's ability to discover new courses of interest. This description is converted into a search vector using embeddings, which is then used to find actual courses with similar content by comparing embedding similarities. ---

- **2601.00833** [인용 B] A Knowledge Graph and Deep Learning-Based Semantic Recommendation Database System for Advertisement Retrieval and Personalization — [초록] To address this challenge, this paper proposes a Knowledge Graph and Deep Learning-Based Semantic Recommendation Database System (KGSR-ADS) for advertisement retrieval and personalization. This layered architecture enables both accurate semantic matching and scalable retrieval, allowing personalized ad recommendations under large-scale heterogeneous workloads. ---

- **2507.21989** [인용 B] Benchmarking Filtered Approximate Nearest Neighbor Search Algorithms on Transformer-based Embedding Vectors — [초록] To fill this gap, we introduce the arxiv-for-fanns dataset of transformer-based embedding vectors for the abstracts of over 2.7 million arXiv papers, enriched with 11 real-world attributes such as authors and categories. We distill our findings into eight key observations that guide users in selecting the most suitable FANNS method for their specific use cases. ---

---

## Q_A03

**질문** 생성 모델이 만든 답을 같은 모델이 다시 검증하면 오류의 30% 정도만 잡힌다고 들었다. 자기 검증의 한계를 실험으로 보인 논문을 알려줘.

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
<b>자기 검증(self‑verification)</b>은 생성 모델이 만든 답을 같은 모델로 다시 확인하는 과정인데, 실험 결과 오류의 약 30%만 포착한다는 결과가 보고되었습니다[2602.07594v1].

<b>본론</b>
1. <b>Learning to Self-Verify</b>: 동일한 작업에서 생성 성능 향상과 자기 검증 향상이 동시에 이루어지지 않는다는 비대칭성을 관찰하고, 학습을 통해 스스로 답을 다시 확인하도록 훈련함으로써 오류를 식별·수정하는 능력을 강화했습니다.[2602.07594v1]
2. <b>RISE (Reinforcing Reasoning with Self‑Verification)</b>: 온라인 RL 프레임워크로 문제 해결과 자기 검증을 동시에 개선하며, 검증 가능한 보상으로부터 실시간 피드백을 제공해 모델이 자신의 답을 비판하고 업데이트하도록 설계되었습니다[2505.13445v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 5편_: 2606.21724 Denoising Iterative Self-Correction: Structured Verification · 2511.10621 SSR: Socratic Self-Refine for Large Language Model Reasoning · 2505.13445 Trust, But Verify: A Self-Verification Approach to Reinforce · 2506.10406 PAG: Multi-Turn Reinforced LLM Self-Correction with Policy a · 2602.07594 Learning to Self-Verify Makes Language Models Better Reasone

### 답 B

<b>서론</b>
생성 모델이 만든 답을 같은 모델로 다시 검증하는 <b>자기‑검증(self‑verification)</b>은 오류를 감지하고 수정해야 하지만, 실제 실험에서 모든 오차를 포착하지 못하는 한계가 존재합니다. 이러한 제한된 검출률은 복잡한 추론 과정에서 특히 문제가 됩니다.

<b>본론</b>
1. <b>Learning to Self-Verify Makes Language Models Better Reasoners</b>: 동일한 작업에서도 생성 성능을 향상시켜도 자기‑검증 능력이同步히 개선되지 않는 현상을 관찰했습니다[2602.07594v1]. 학습 과정에서 모델이 잠재적 오류를 감지하고 즉시 수정하도록 유도함으로써, 토큰 사용량을 크게 감소시키고 불필요한 “가짜” 검증 행동을 방지합니다[2602.07594v1].
<b>결론</b>
제공된 문서에 따르면, 같은 모델을 이용해 생성 답을 다시 검증할 때 모든 오차를 잡지는 못하며 특히 오류의 상당 부분이 검출되지 않는 한계가 존재한다는 실험 결과가 제시됩니다. 이는 자기‑검증 능력과 생성 능력이 독립적으로 발전함을 보여줍니다[2602.07594v1].

_B 컨텍스트 5편_: 2606.21724 Denoising Iterative Self-Correction: Structured Verification · 2511.10621 SSR: Socratic Self-Refine for Large Language Model Reasoning · 2505.13445 Trust, But Verify: A Self-Verification Approach to Reinforce · 2506.10406 PAG: Multi-Turn Reinforced LLM Self-Correction with Policy a · 2602.07594 Learning to Self-Verify Makes Language Models Better Reasone

### 인용 블록

- **2602.07594** [인용 AB] Learning to Self-Verify Makes Language Models Better Reasoners — [초록] Recent large language models (LLMs) achieve strong performance in generating promising reasoning paths for complex tasks. However, despite powerful generation ability, LLMs remain weak at verifying their own answers, revealing a persistent capability asymmetry between generation and self-verification. In this work, we conduct an in-depth investigation of this asymmetry throughout training evolution and show that, even on the same task, improving generation does not lead to corresponding improvements in self-verification. Interestingly, we find that the reverse direction of this asymmetry behaves differently: learning to self-verify can effectively improve generation performance, achieving accuracy comparable to standard generation training while yielding more efficient and effective reasoning traces. Building on this observation, we further explore integrating self-verification into

- **2505.13445** [인용 A] Trust, But Verify: A Self-Verification Approach to Reinforcement Learning with Verifiable Rewards — [초록] Large Language Models (LLMs) show great promise in complex reasoning, with Reinforcement Learning with Verifiable Rewards (RLVR) being a key enhancement strategy. However, a prevalent issue is ``superficial self-reflection'', where models fail to robustly verify their own outputs. We introduce RISE (Reinforcing Reasoning with Self-Verification), a novel online RL framework designed to tackle this. RISE explicitly and simultaneously trains an LLM to improve both its problem-solving and self-verification abilities within a single, integrated RL process. The core mechanism involves leveraging verifiable rewards from an outcome verifier to provide on-the-fly feedback for both solution generation and self-verification tasks. In each iteration, the model generates solutions, then critiques its own on-policy generated solutions, with both trajectories contributing to the policy update. Ext

---

## Q_A09

**질문** 임베딩 모델을 바꿨더니 영어 질문 recall은 올랐지만 한국어 질문 recall은 10%p 떨어졌다. 언어별로 임베딩 성능이 갈리는 원인을 분석한 논문 있어?

### 답 A

<b>서론</b>
제공된 참고문서에는 질문에서 찾는 “언어별 임베딩 성능 차이 원인 분석”에 대한 논문을 찾을 수 없습니다. 따라서 해당 연구는 [2602.21553v1]과 2의 내용으로 요약할 수 없으며, 관련 정보를 제공하지 않습니다.

<b>본론</b>
[관련 논문 없음]

<b>결론</b>
따라서 질문에 해당하는 언어별로 임베딩이 갈리는 원인을 설명하는 문서는 참고문서에서 찾을 수 없습니다.

_A 컨텍스트 1편_: 2602.21553 Revisiting RAG Retrievers: An Information Theoretic Benchmar

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>MIGRASCOPE</b>: Mutual Information 기반 RAG Retriever 분석 범위로, 정보 이론과 통계 추정 이론에 근거한 원칙적인 메트릭을 도입해 검색 품질·중복성·시너지·변경 기여도를 정량화한다[2602.21553v1]. 다국어·다기능·다정밀도 텍스트 임베딩으로, 자기 지식 증류(self‑knowledge distillation)를 통해 언어별 성능을 개선한다는 점을 제시한다[2602.21553v1] (관련 연구).
<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 1편_: 2602.21553 Revisiting RAG Retrievers: An Information Theoretic Benchmar

### 인용 블록

- **2602.21553** [인용 AB] Revisiting RAG Retrievers: An Information Theoretic Benchmark — [초록] Retrieval-Augmented Generation (RAG) systems rely critically on the retriever module to surface relevant context for large language models. Although numerous retrievers have recently been proposed, each built on different ranking principles such as lexical matching, dense embeddings, or graph citations, there remains a lack of systematic understanding of how these mechanisms differ and overlap. Existing benchmarks primarily compare entire RAG pipelines or introduce new datasets, providing little guidance on selecting or combining retrievers themselves. Those that do compare retrievers directly use a limited set of evaluation tools which fail to capture complementary and overlapping strengths. This work presents MIGRASCOPE, a Mutual Information based RAG Retriever Analysis Scope. We revisit state-of-the-art retrievers and introduce principled metrics grounded in information and stati

---

## Q_C05

**질문** 멀티모달 모델의 환각 평가 벤치마크 쪽 연구 흐름 정리 부탁해

### 답 A

<b>서론</b>
멀티모달 대형 언어 모델(MLLM)은 시각·텍스트 정보를 통합해 다양한 작업을 수행하지만, 입력 내용이나 세계 지식과 모순되는 <b>환각</b> 현상이 빈번히 발생하여 신뢰성을 저하시킨다[2507.19024v2][2404.18930v2]. 이러한 환각을 정량적으로 측정하고 평가하기 위한 벤치마크와 방법론이 지속적으로 개발되고 있다.

<b>본론</b>
1. <b>MME</b>: 멀티모달 대형 언어 모델을 포괄적으로 평가하는 새로운 벤치마크를 제안하였다[2507.19024v2]
2. <b>Hallucinogen</b>: 대규모 시각‑언어 모델에서 객체 환각을 평가하기 위한 전용 벤치를 소개했다[2410.23114v4]
3. <b>Tri-HE (Unified Triplet-Level Evaluation)</b>: LVLM 응답으로부터 추출한 (객체, 관계, 객체) 삼중항으로 객체와 관계를 동시에 평가하는 벤치마크를 설계하였다[2510.08945v2]

<b>결론</b>
제공된 문서들은 멀티모달 환각 평가 벤치마크의 연구 흐름을 정리하고 있으며, 기존 벤치마크가 주로 객체 관련 환각에 제한되어 있다는 점을 지적한다[2410.23114v4]. 또한, 현재 벤치마크와 탐지 방법의 한계를 강조하고 향후 연구 방향을 제시한다[2507.19024v2]. 마지막으로, RAG 파이프라인 전체를 평가하는 새로운 벤치마크를 소개하고, 정성적 인간 평가에서 정확성과 환각 탐지에 대한 평균 동의도가 각각 4.62와 4.53으로 나타났다[2510.08945v2]. 이러한 결과들은 멀티모달 환각 평가가 객체 중심에서 벗어나 파이프라인 전체와 다양한 데이터 유형을 포괄하도록 진화하고 있음을 보여준다.

_A 컨텍스트 5편_: 2507.19024 A Survey of Multimodal Hallucination Evaluation and Detectio · 2404.18930 Hallucination of Multimodal Large Language Models: A Survey · 2410.23114 Unified Triplet-Level Hallucination Evaluation for Large Vis · 2510.08945 FATHOMS-RAG: A Framework for the Assessment of Thinking and  · 2407.00569 Investigating and Mitigating the Multimodal Hallucination Sn

### 답 B

<b>서론</b>
멀티모달 모델에서 발생하는 환각을 평가하고 탐지하기 위한 벤치마크 연구가 최근 활발히 진행되고 있습니다. 이 흐름은 <b>환각 분류</b>, <b>벤치마킹 한계 지적</b>, 그리고 <b>평가 프레임워크 확장</b>으로 이어집니다.

<b>본론</b>
1. <b>Multimodal Hallucination Taxonomy</b>: 환각을 충실성과 사실성 기준으로 분류하고, 실제 관측된 일반적인 유형을 포함하는 세분화된 정의를 제안합니다[2507.19024v2].
2. <b>HalluLens Benchmark</b>: 명확한 환각 분류를 기반으로 새로운 외재적 평가 작업을 도입하며, 데이터가 동적으로 재생산되어 정보 누출에 의한 포화 현상을 방지하도록 설계되었습니다[2504.17550v1].

<b>결론</b>
[2507.19024v2]은 환각 분류를 충실도와 사실성에 기반한 세분화된 태크소니미로 정의하고, 현재 벤치마크와 탐지 방법의 한계를 강조하며 향후 연구 방향을 제시한다[2507.19024v2]. [2504.17550v1]은 명확한 환각 태크소니미에 기반해 새로운 외재적 평가 작업을 도입하고, 데이터 누출 방지 위해 동적으로 재생성 가능한 데이터를 제공한다[2504.17550v1]. 두 논문 모두 환각 평가의 태크소니미를 정립한다는 점에서 목표가 일치하지만, [2507.19024v2]은 전반적인 한계와 미래 방향을 강조하는 반면, [2504.17550v1]은 구체적인 외재적 작업과 데이터 재생성 메커니즘에 초점을 맞추어 연구 흐름에서 서로 보완적인 역할을 한다.

_B 컨텍스트 6편_: 2507.19024 A Survey of Multimodal Hallucination Evaluation and Detectio · 2404.18930 Hallucination of Multimodal Large Language Models: A Survey · 2410.23114 Unified Triplet-Level Hallucination Evaluation for Large Vis · 2510.08945 FATHOMS-RAG: A Framework for the Assessment of Thinking and  · 2407.00569 Investigating and Mitigating the Multimodal Hallucination Sn · 2504.17550 HalluLens: LLM Hallucination Benchmark

### 인용 블록

- **2507.19024** [인용 AB] A Survey of Multimodal Hallucination Evaluation and Detection — [초록] Multi-modal Large Language Models (MLLMs) have emerged as a powerful paradigm for integrating visual and textual information, supporting a wide range of multi-modal tasks. However, these models often suffer from hallucination, producing content that appears plausible but contradicts the input content or established world knowledge. This survey offers an in-depth review of hallucination evaluation benchmarks and detection methods across Image-to-Text (I2T) and Text-to-image (T2I) generation tasks. Specifically, we first propose a taxonomy of hallucination based on faithfulness and factuality, incorporating the common types of hallucinations observed in practice. Then we provide an overview of existing hallucination evaluation benchmarks for both T2I and I2T tasks, highlighting their construction process, evaluation objectives, and employed metrics. Furthermore, we summarize recent ad

- **2404.18930** [인용 A] Hallucination of Multimodal Large Language Models: A Survey — [초록] This survey presents a comprehensive analysis of the phenomenon of hallucination in multimodal large language models (MLLMs), also known as Large Vision-Language Models (LVLMs), which have demonstrated significant advancements and remarkable abilities in multimodal tasks. Despite these promising developments, MLLMs often generate outputs that are inconsistent with the visual content, a challenge known as hallucination, which poses substantial obstacles to their practical deployment and raises concerns regarding their reliability in real-world applications. This problem has attracted increasing attention, prompting efforts to detect and mitigate such inaccuracies. We review recent advances in identifying, evaluating, and mitigating these hallucinations, offering a detailed overview of the underlying causes, evaluation benchmarks, metrics, and strategies developed to address this issu

- **2410.23114** [인용 A] Unified Triplet-Level Hallucination Evaluation for Large Vision-Language Models — [초록] Despite the outstanding performance in vision-language reasoning, Large Vision-Language Models (LVLMs) might generate hallucinated contents that do not exist in the given image. Most existing LVLM hallucination benchmarks are constrained to evaluate the object-related hallucinations. However, the potential hallucination on the relations between two objects, i.e., relation hallucination, still lacks investigation. To remedy that, we design a unified framework to measure the object and relation hallucination in LVLMs simultaneously. The core idea of our framework is to evaluate hallucinations via (object, relation, object) triplets extracted from LVLMs' responses, making it easily generalizable to different vision-language tasks. Based on our framework, we further introduce Tri-HE, a novel Triplet-level Hallucination Evaluation benchmark which can be used to study both object and rela

- **2510.08945** [인용 A] FATHOMS-RAG: A Framework for the Assessment of Thinking and Observation in Multimodal Systems that use Retrieval Augmented Generation — [초록] Retrieval-augmented generation (RAG) has emerged as a promising paradigm for improving factual accuracy in large language models (LLMs). We introduce a benchmark designed to evaluate RAG pipelines as a whole, evaluating a pipeline's ability to ingest, retrieve, and reason about several modalities of information, differentiating it from existing benchmarks that focus on particular aspects such as retrieval. We present (1) a small, human-created dataset of 93 questions designed to evaluate a pipeline's ability to ingest textual data, tables, images, and data spread across these modalities in one or more documents; (2) a phrase-level recall metric for correctness; (3) a nearest-neighbor embedding classifier to identify potential pipeline hallucinations; (4) a comparative evaluation of 2 pipelines built with open-source retrieval mechanisms and 4 closed-source foundation models; and (5)

- **2504.17550** [인용 B] HalluLens: LLM Hallucination Benchmark — [초록] This paper introduces a comprehensive hallucination benchmark, incorporating both new extrinsic and existing intrinsic evaluation tasks, built upon clear taxonomy of hallucination. The work aims to: (1) establish a clear taxonomy of hallucinations, (2) introduce new extrinsic hallucination tasks, with data that can be dynamically regenerated to prevent saturation by leakage, (3) provide a compre…

---

## Q_D02

**질문** 프롬프트 압축 방법 여러 개를 같은 조건에서 비교한 벤치마크 논문 알려줘

### 답 A

<b>서론</b>
프롬프트 압축은 긴 프롬프트를 짧게 만들어 LLM의 메모리 사용량과 추론 비용을 줄이는 기술이지만, 정보 손실이나 구조적 일관성 유지가 어려운 문제입니다. 이러한 어려움을 해결하기 위해 다양한 접근법이 제안되었습니다.

<b>본론</b>
1. <b>Prompt Compression Survey</b>: 하드 프롬프트와 소프트 프롬프트 방식으로 분류된 기존 압축 기법들을 정리하고, 주의력 최적화·PEFT·모달리티 통합 등 메커니즘을 비교하며 한계점과 향후 방향성을 제시합니다[2410.12388v2].
2. <b>SCOPE: A Generative Approach for LLM Prompt Compression</b>: 토큰 제거 방식의 정보 손실 문제를 극복하기 위해 프롬프트를 의미적으로 일관된 청크로 나누어 요약하고, 최적화된 시맨틱 채킹·아웃라이어 처리·동적 압축 비율 등을 적용해 높은 안정성과 품질을 달성합니다[2508.15813v1].
3. <b>Prompt-SAW</b>: 텍스트 정보를 이용해 그래프를 구축한 뒤 핵심 정보 요소를 추출하여 프롬프트를 압축하며, 가독성 향상과 함께 작업‑무관/작업‑인식 설정에서 각각 최대 10.1·77.1까지 성능을 개선하고 원본 대비 34.9~56.7%의 텍스트 감소율을 달성합니다[2404.00489v2].
4. <b>LLMLingua-2</b>: 데이터 디스틸레이션과 토큰 분류를 통해 프롬프트 압축 목표를 학습하며, 양방향 컨텍스트와 작은 모델(XLM‑RoBERTa·mBERT)을 활용해 기존 방법보다 낮은 지연시간(1.6~2.9배 감소)과 3×∼6×의 속도 향상을 보입니다[2403.12968v2].

<b>결론</b>
제공된 문서들은 프롬프트 압축 방법들을 동일한 조건에서 비교한 벤치마크 결과를 제시하고 있습니다. SCOPE는 질문‑답변 및 요약 과제와 다양한 도메인 데이터를 이용해 평가했으며, 높은 압축 비율에서도 기존 최첨단 방법보다 압축 품질과 안정성이 크게 향상됨을 보였습니다[2508.15813v1]. Prompt-SAW는 GSM8K‑aug 벤치마크를 사용해 작업‑무관 프롬프트에 대해 가독성뿐만 아니라 성능 측면에서 베이스라인 대비 최대 10.1 및 77.1의 향상을 달성하고, 원본 텍스트를 각각 34.9와 56.7만큼 압축함을 확인했습니다[2404.00489v2]. LLMLingua‑2는 데이터 증류 방식을 통해 작업‑무관 프롬프트 압축에 초점을 맞추어 기존 방법보다 3배~6배 빠른 속도와 1.6배~2.9배 감소된 전체 지연 시간을 보여주며, 성능과 압축 지연 측면에서 강력한 베이스라인을 능가함을 입증했습니다[2403.12968v2]. 따라서 각 논문은 서로 다른 평가 데이터와 벤치마크 설정에서 프롬프트 압축 방법의 효율성과 품질을 비교하고 있으며, 특정 도메인이나 비공개 데이터를 사용하지 않고 공개된 벤치마크를 활용해 결과를 제시하고 있습니다.

_A 컨텍스트 5편_: 2410.12388 Prompt Compression for Large Language Models: A Survey · 2508.15813 SCOPE: A Generative Approach for LLM Prompt Compression · 2404.00489 Prompt-SAW: Leveraging Relation-Aware Graphs for Textual Pro · 2403.12968 LLMLingua-2: Data Distillation for Efficient and Faithful Ta · 2511.08128 Sentence-Anchored Gist Compression for Long-Context LLMs

### 답 B

<b>서론</b>
프롬프트 압축은 긴 프롬프트를 짧게 만들어 메모리 사용량과 추론 비용을 줄이는 기술이지만, <b>압축률</b>·<b>가독성</b>·<b>정확도</b> 등 여러 성능 지표를 동시에 만족시키는 것이 어렵습니다. 이러한 다중 목표를 평가하기 위해 다양한 방법을 동일한 벤치마크에서 비교한 연구들이 필요합니다.

<b>본론</b>
1. <b>Prompt-SAW</b>: 관계‑인식 그래프를 이용해 프롬프트의 핵심 정보를 추출하고 압축함으로써 가독성을 향상시켰으며, 기존 베이스라인 대비 최대 77.1% 성능 향상을 보였습니다[2404.00489v2].
2. <b>LLMLingua-2</b>: 데이터 디스틸레이션과 토큰 분류를 통해 프롬프트의 핵심 정보를 보존하면서 압축률을 높이고, 작은 모델에서도 높은 효율성을 달성했습니다[2403.12968v2].

<b>결론</b>
Prompt-SAW는 벤치마크 데이터셋을 이용해 프롬프트 압축 성능을 평가했으며, task-agnostic 설정에서 기존 최상위 베이스라인보다 최대 10.1만큼, task-aware 설정에서는 77.1만큼 우수한 결과를 보였습니다[2404.00489v2]. LLMLingua-2는 데이터 증류 방식을 통해 프롬프트를 압축하고, 기존 방법 대비 3~6배 빠른 속도와 1.6~2.9배 감소된 전체 지연 시간을 달성하면서 성능과 압축 지연 측면에서 강력한 베이스라인을 능가했습니다[2403.12968v2]. 두 논문 모두 벤치마크 기반 정량 평가를 통해 각각의 프롬프트 압축 방법이 기존 방법보다 우수한 성능과 효율성을 보임을 입증하고 있습니다.

_B 컨텍스트 5편_: 2410.12388 Prompt Compression for Large Language Models: A Survey · 2404.00489 Prompt-SAW: Leveraging Relation-Aware Graphs for Textual Pro · 2403.12968 LLMLingua-2: Data Distillation for Efficient and Faithful Ta · 2511.08128 Sentence-Anchored Gist Compression for Long-Context LLMs · 2412.15298 A Comparative Study of DSPy Teleprompter Algorithms for Alig

### 인용 블록

- **2410.12388** [인용 A] Prompt Compression for Large Language Models: A Survey — [초록] Leveraging large language models (LLMs) for complex natural language tasks typically requires long-form prompts to convey detailed requirements and information, which results in increased memory usage and inference costs. To mitigate these challenges, multiple efficient methods have been proposed, with prompt compression gaining significant research interest. This survey provides an overview of prompt compression techniques, categorized into hard prompt methods and soft prompt methods. First, the technical approaches of these methods are compared, followed by an exploration of various ways to understand their mechanisms, including the perspectives of attention optimization, Parameter-Efficient Fine-Tuning (PEFT), modality integration, and new synthetic language. We also examine the downstream adaptations of various prompt compression techniques. Finally, the limitations of current p

- **2508.15813** [인용 A] SCOPE: A Generative Approach for LLM Prompt Compression — [초록] Prompt compression methods enhance the efficiency of Large Language Models (LLMs) and minimize the cost by reducing the length of input context. The goal of prompt compression is to shorten the LLM prompt while maintaining a high generation quality. However, existing solutions, mainly based on token removal, face challenges such as information loss and structural incoherence, like missing grammar elements in a sentence, or incomplete word phrases after token removal. Such challenges limit the final generation quality of LLM. To overcome these limitations, we present a novel generative prompt compression method. Unlike the existing token removal methods, our method centers at a chunking-and-summarization mechanism. Specifically, our method splits prompt into semantically coherent chunks and rewrites the chunks to be more concise. The chunks are reconstructed into meaningful prompt fi

- **2404.00489** [인용 AB] Prompt-SAW: Leveraging Relation-Aware Graphs for Textual Prompt Compression — [초록] Large Language Models (LLMs) have shown exceptional abilities for multiple different natural language processing tasks. While prompting is a crucial tool for LLM inference, we observe that there is a significant cost associated with exceedingly lengthy prompts. Existing attempts to compress lengthy prompts lead to substandard results in terms of readability/interpretability of the compressed prompt, with a detrimental impact on prompt utility. To address this, we propose PromptSAW: Prompt compresSion via Relation AWare graphs, an effective strategy for prompt compression over task-agnostic and task-aware prompts. Prompt-SAW uses the prompt's textual information to build a graph and later extracts key information elements in the graph to come up with the compressed prompt. We also propose GSM8K-aug, i.e., an extended version of the existing GSM8K benchmark for task-agnostic prompts i

- **2403.12968** [인용 AB] LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression — [초록] This paper focuses on task-agnostic prompt compression for better generalizability and efficiency. Considering the redundancy in natural language, existing approaches compress prompts by removing tokens or lexical units according to their information entropy obtained from a causal language model such as LLaMa-7B. The challenge is that information entropy may be a suboptimal compression metric: (i) it only leverages unidirectional context and may fail to capture all essential information needed for prompt compression; (ii) it is not aligned with the prompt compression objective. To address these issues, we propose a data distillation procedure to derive knowledge from an LLM to compress prompts without losing crucial information, and meantime, introduce an extractive text compression dataset. We formulate prompt compression as a token classification problem to guarantee the faithfuln

---

## Q_D06

**질문** 양자화 방식별로 추론 속도와 정확도를 비교 실험한 연구 알려줘

### 답 A

<b>서론</b>
양자화는 모델 파라미터를 낮은 비트로 압축해 <b>메모리 사용량</b>과 <b>추론 속도</b>를 크게 낮출 수 있지만, 정밀도 손실이라는 정확성 문제를 동시에 해결해야 합니다. 이러한 트레이드오프는 다양한 양자화 기법을 비교·평가하는 실험을 통해 파악할 필요가 있습니다.

<b>본론</b>
1. <b>Apollo‑Forecast</b>: Anti-Aliasing Quantization Module (AAQM)과 Race Decoding(RD) 기술을 도입해 신호 왜곡을 줄이고, 대규모 모델에서도 추론 속도를 1.9 ×~2.7 배 가속화했으며, WQL 지표에서 기존 SOTA 대비 성능이 35.41% 향상되었습니다[2412.12226v1].
2. <b>QMedSAM</b>: MedSAM 모델을 양자화‑인지 학습 파이프라인으로 최적화하고 OpenVINO 엔진을 이용해 배포함으로써 추론 속도를 크게 높였으며, 정확도는 여전히 수용 가능한 수준에 머물렀습니다[2412.11186v1].
3. <b>RaanA</b>: RaBitQ-H와 AllocateBits를 결합한 PTQ 프레임워크로 최소한의 교정 데이터만 필요하며 유연하게 비트 할당을 가능해 효율성과 정밀도의 균형을 달성했습니다[2504.03717v2].

<b>결론</b>
양자화 방식별 추론 속도와 정확도 비교 실험은 연구마다 대상과 조건이 달라 결과가 다르게 나타난다. Apollo-Forecast는 시간 시계열 예측 모델에서 WQL 기준으로 35.41% 성능 향상과 1.9X~2.7X 속도 가속을 달성했다[2412.12226v1]. Segment Anything Model에 대한 양자화 인식 훈련은 처리 속도를 크게 향상시키면서도 허용 가능한 정확도 수준을 유지하는 것으로 확인되었다[2412.11186v1]. RaanA는 경쟁력 있는 성능과 매우 빠른 속도를 보이며, 최소한의 교정 데이터와 유연한 비트 할당을 가능하게 하지만, 교정 데이터 분포와 먼 경우 일반화 성능이 저하될 수 있다는 한계가 있다[2504.03717v2]. 따라서 양자화 방법의 효과는 적용 대상 모델과 데이터 특성에 따라 크게 달라진다.

_A 컨텍스트 5편_: 2412.12226 Apollo-Forecast: Overcoming Aliasing and Inference Speed Cha · 2412.11186 Efficient Quantization-Aware Training on Segment Anything Mo · 2504.03717 RaanA: A Fast, Flexible, and Data-Efficient Post-Training Qu · 2412.19867 Data-Free Group-Wise Fully Quantized Winograd Convolution vi · 2607.01127 $\text{Log}_\text{b}$Quant: Quantizing Language Models in Lo

### 답 B

<b>서론</b>
양자화 방식별로 <b>추론 속도</b>와 <b>정확도</b>(또는 성능)를 비교하는 실험은 모델 압축과 효율성 사이의 균형을 파악하기 위해 중요합니다. 다양한 양자화 기법이 존재하지만, 각 방법의 실제 효과를 정량적으로 평가한 연구가 필요합니다.

<b>본론</b>
1. <b>RaanA</b>: RaanA 는 빠른 추론 속도와 높은 정확도를 동시에 달성하도록 설계된 통합 PTQ 프레임워크이며, 최소한의 보정 데이터와 유연한 비트 할당을 제공합니다[2504.03717v2].
2. <b>Log_bQuant</b>: Log$_\text{b}$Quant 은 로그 공간에서 모델 파라미터를 양자화하여 메모리 사용량을 크게 줄이고 추론 속도를 향상시키며, 특히 4‑비트 정밀도에서는 비대칭 선형 양자화에 비해 우수한 성능을 보입니다[2607.01127v1].
3. <b>FastText.zip</b>: FastText.zip 은 제품 기반의 압축 기법을 통해 텍스트 분류 모델에 필요한 메모리 용량을 크게 감소시키고 정확도를 유지합니다[1612.03651v1].

<b>결론</b>
제공된 문서들은 RaanA, Log$_\text{b}$Quant 및 FastText.zip을 각각 빠른 추론과 높은 성능을 목표로 한 양자화 방법으로 제시하고 있습니다. 따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 5편_: 2504.03717 RaanA: A Fast, Flexible, and Data-Efficient Post-Training Qu · 2607.01127 $\text{Log}_\text{b}$Quant: Quantizing Language Models in Lo · 1612.03651 FastText.zip: Compressing text classification models · 2606.22249 On the Expressive Power of Weight Quantization in Large Lang · 2511.13023 SLMQuant:Benchmarking Small Language Model Quantization for 

### 인용 블록

- **2412.12226** [인용 A] Apollo-Forecast: Overcoming Aliasing and Inference Speed Challenges in Language Models for Time Series Forecasting — [초록] Encoding time series into tokens and using language models for processing has been shown to substantially augment the models' ability to generalize to unseen tasks. However, existing language models for time series forecasting encounter several obstacles, including aliasing distortion and prolonged inference times, primarily due to the limitations of quantization processes and the computational demands of large models. This paper introduces Apollo-Forecast, a novel framework that tackles these challenges with two key innovations: the Anti-Aliasing Quantization Module (AAQM) and the Race Decoding (RD) technique. AAQM adeptly encodes sequences into tokens while mitigating high-frequency noise in the original signals, thus enhancing both signal fidelity and overall quantization efficiency. RD employs a draft model to enable parallel processing and results integration, which markedly ac

- **2412.11186** [인용 A] Efficient Quantization-Aware Training on Segment Anything Model in Medical Images and Its Deployment — [초록] Medical image segmentation is a critical component of clinical practice, and the state-of-the-art MedSAM model has significantly advanced this field. Nevertheless, critiques highlight that MedSAM demands substantial computational resources during inference. To address this issue, the CVPR 2024 MedSAM on Laptop Challenge was established to find an optimal balance between accuracy and processing speed. In this paper, we introduce a quantization-aware training pipeline designed to efficiently quantize the Segment Anything Model for medical images and deploy it using the OpenVINO inference engine. This pipeline optimizes both training time and disk storage. Our experimental results confirm that this approach considerably enhances processing speed over the baseline, while still achieving an acceptable accuracy level. The training script, inference script, and quantized model are publicly

- **2504.03717** [인용 AB] RaanA: A Fast, Flexible, and Data-Efficient Post-Training Quantization Algorithm — [초록] Post-training Quantization (PTQ) has become a widely used technique for improving inference efficiency of large language models (LLMs). However, existing PTQ methods generally suffer from crucial limitations such as heavy calibration data requirements and inflexible choice of target number of bits. In this paper, we propose RaanA, a unified PTQ framework that overcomes these challenges by introducing two novel components: 1) RaBitQ-H, a variant of a randomized vector quantization method RaBitQ, designed for fast, accurate, and highly efficient quantization; and 2) AllocateBits, an algorithm that optimally allocates bit-widths across layers based on their quantization sensitivity. RaanA achieves competitive performance with state-of-the-art quantization methods while being extremely fast, requiring minimal calibration data, and enabling flexible bit allocation. Extensive experiments 

- **2607.01127** [인용 B] $\text{Log}_\text{b}$Quant: Quantizing Language Models in Logarithmic Space — [초록] Quantization has become an invaluable tool to reduce memory requirements and inference speed of modern language models, in particular to make them available for consumer setups and edge devices. While previous work has primarily focused on uniform quantization codebooks, such approaches are prone to suboptimal representations due to low-frequency high-magnitude weights. We introduce Log$_\text{b}$Quant, a novel logarithmic quantization approach with adjustable bases, to adapt to common parameter distributions. We show that our method exhibits superior performance at 4-bit precision on several performance benchmarks compared to asymmetric linear quantization at tensor-wise granularity, while achieving moderate speedup and high memory savings, making it suitable for private use on consumer-grade GPUs. For 8-bit quantization, the linear quantization approach consistently outperforms ou

- **1612.03651** [인용 B] FastText.zip: Compressing text classification models — [초록] We consider the problem of producing compact architectures for text classification, such that the full model fits in a limited amount of memory. After considering different solutions inspired by the hashing literature, we propose a method built upon product quantization to store word embeddings. While the original technique leads to a loss in accuracy, we adapt this method to circumvent quantization artefacts. Our experiments carried out on several benchmarks show that our approach typically requires two orders of magnitude less memory than fastText while being only slightly inferior with respect to accuracy. As a result, it outperforms the state of the art by a good margin in terms of the compromise between memory usage and accuracy. Beyond these binarization strategies, more general quantization techniques derived from Jegou et al. (2011) offer better trade-offs between memory and

---

## Q_E02

**질문** 재무 문서의 수치를 검증하는 RAG 연구 찾아줘

### 답 A

<b>서론</b>
재무 분야에서 <b>수치 검증</b>은 복잡한 계산과 다양한 출처를 다루기 때문에 오류가 발생하기 쉽습니다. 이러한 문제를 해결하려면 신뢰할 수 있는 문서 기반 검색(RAG) 시스템에 추가적인 검증 메커니즘이 필요합니다.

<b>본론</b>
1. <b>VERAFI</b>: 신경‑상징적 정책 생성을 통해 재무 도메인 전문 지식을 추론 과정에 직접 통합하고, GAAP·SEC 요구사항 및 수학 검증을 포함한 자동화된 정책을 적용합니다[2512.14744v1].
2. <b>FinVet</b>: 두 개의 RAG 파이프라인과 외부 사실 확인 에이전트를 결합한 다중‑에이전트 프레임워크로, 신뢰도 가중치 투표 메커니즘을 사용해 증거 기반의 판단 결과를 제공합니다[2510.11654v2].

<b>결론</b>
VERAFI는 FinanceBench에서 기존 밀집 검색 재랭킹의 사실 정확도 52.4%를 94.7%로 크게 향상시켰으며, 이는 상대적 개선율 81%에 해당한다[2512.14744v1]. FinVet은 FinFact 데이터셋에서 F1 점수 0.85를 달성해 개별 파이프라인 대비 10.4%, 독립형 RAG 접근법 대비 37%의 향상을 보였다[2510.11654v2]. 두 연구는 각각 서로 다른 재무 문서 검증 과제와 평가 데이터셋을 대상으로 하였으며, VERAFI는 사실 정확도 향상과 FinVet은 F1 점수 기반의 종합 성능 향상에 초점을 맞추고 있다. 따라서 재무 문서 수치 검증 분야에서 RAG 기반 접근법이 기존 방법보다 유의미한 성능 개선을 보인다는 공통된 결론이 도출된다.

_A 컨텍스트 5편_: 2603.14170 Citation-Enforced RAG for Fiscal Document Intelligence: Cite · 2512.14744 VERAFI: Verified Agentic Financial Intelligence through Neur · 2510.11654 FinVet: A Collaborative Framework of RAG and External Fact-C · 2510.24402 Metadata-Driven Retrieval-Augmented Generation for Financial · 2602.05723 Mitigating Hallucination in Financial Retrieval-Augmented Ge

### 답 B

<b>서론</b>
재무 분야에서는 <b>수치 계산 오류</b>, <b>규정 위반</b> 및 <b>환각 현상</b> 등이 발생하기 쉬워, 신뢰할 수 있는 답변 생성에 큰 어려움이 존재합니다. 이러한 문제를 해결하려면 문서 기반 검색과 검증 메커니즘을 결합한 RAG 시스템이 필요합니다.

<b>본론</b>
1. <b>VERAFI</b>: 신경‑기호 정책 생성 방식을 도입해 계산 오류와 규제 위반 가능성을 사전 차단하고, GAAP·SEC 요구사항 및 수학적 검증을 포함한 자동 추론 정책을 적용합니다[2512.14744v1].
2. <b>RLFKV (Reinforcement Learning with Fine-Grained Knowledge Verification)</b>: 재무 응답을 원자적 지식 단위로 분해하여 각 단위별 정확도를 평가하고, 이를 기반으로 미세한 충실도 보상을 계산함으로써 환각 현상을 완화하며 정보량 보상까지 추가합니다[2602.05723v1].
3. <b>FinVet</b>: 두 개의 RAG 파이프라인과 외부 사실 확인 에이전트를 결합한 다중‑에이전트 프레임워크로, 신뢰 기반 투표 메커니즘을 통해 증거가 부족한 경우 불확실성 플래그를 표시하고 F1 점수에서 0.85의 성능을 달성합니다[2510.11654v2].

<b>결론</b>
VERAFI는 FinanceBench에서 기존 밀집 검색 재랭킹의 사실 정확도 52.4%를 94.7%로 향상시켰으며, 이는 상대적 개선율 81%에 해당한다[2512.14744v1]. FinVet은 FinFact 데이터셋에서 F1 점수 0.85를 달성해 개별 파이프라인 대비 10.4%, 독립형 RAG 대비 37%의 향상을 보였다[2510.11654v2]. 두 연구 모두 재무 문서 검증 분야에서 RAG 기반 접근법의 성능을 크게 개선했으나, 평가 대상 데이터셋과 측정 지표가 다르다.

_B 컨텍스트 5편_: 2603.14170 Citation-Enforced RAG for Fiscal Document Intelligence: Cite · 2512.14744 VERAFI: Verified Agentic Financial Intelligence through Neur · 2510.11654 FinVet: A Collaborative Framework of RAG and External Fact-C · 2510.24402 Metadata-Driven Retrieval-Augmented Generation for Financial · 2602.05723 Mitigating Hallucination in Financial Retrieval-Augmented Ge

### 인용 블록

- **2512.14744** [인용 AB] VERAFI: Verified Agentic Financial Intelligence through Neurosymbolic Policy Generation — [초록] Financial AI systems suffer from a critical blind spot: while Retrieval-Augmented Generation (RAG) excels at finding relevant documents, language models still generate calculation errors and regulatory violations during reasoning, even with perfect retrieval. This paper introduces VERAFI (Verified Agentic Financial Intelligence), an agentic framework with neurosymbolic policy generation for verified financial intelligence. VERAFI combines state-of-the-art dense retrieval and cross-encoder reranking with financial tool-enabled agents and automated reasoning policies covering GAAP compliance, SEC requirements, and mathematical validation. Our comprehensive evaluation on FinanceBench demonstrates remarkable improvements: while traditional dense retrieval with reranking achieves only 52.4\% factual correctness, VERAFI's integrated approach reaches 94.7\%, an 81\% relative improvement. T

- **2510.11654** [인용 AB] FinVet: A Collaborative Framework of RAG and External Fact-Checking Agents for Financial Misinformation Detection — [초록] Financial markets face growing threats from misinformation that can trigger billions in losses in minutes. Most existing approaches lack transparency in their decision-making and provide limited attribution to credible sources. We introduce FinVet, a novel multi-agent framework that integrates two Retrieval-Augmented Generation (RAG) pipelines with external fact-checking through a confidence-weighted voting mechanism. FinVet employs adaptive three-tier processing that dynamically adjusts verification strategies based on retrieval confidence, from direct metadata extraction to hybrid reasoning to full model-based analysis. Unlike existing methods, FinVet provides evidence-backed verdicts, source attribution, confidence scores, and explicit uncertainty flags when evidence is insufficient. Experimental evaluation on the FinFact dataset shows that FinVet achieves an F1 score of 0.85, wh

- **2602.05723** [인용 B] Mitigating Hallucination in Financial Retrieval-Augmented Generation via Fine-Grained Knowledge Verification — [초록] In financial Retrieval-Augmented Generation (RAG) systems, models frequently rely on retrieved documents to generate accurate responses due to the time-sensitive nature of the financial domain. While retrieved documents help address knowledge gaps, model-generated responses still suffer from hallucinations that contradict the retrieved information. To mitigate this inconsistency, we propose a Reinforcement Learning framework enhanced with Fine-grained Knowledge Verification (RLFKV). Our method decomposes financial responses into atomic knowledge units and assesses the correctness of each unit to compute the fine-grained faithful reward. This reward offers more precise optimization signals, thereby improving alignment with the retrieved documents. Additionally, to prevent reward hacking (e.g., overly concise replies), we incorporate an informativeness reward that encourages the polic

---

## Q_E06

**질문** 얼마나 자주 검색할지 모델이 스스로 정하는 적응형 RAG 연구 알려줘

### 답 A

<b>서론</b>
제공된 연구들은 <b>적응형 RAG(Adaptive Retrieval-Augmented Generation)</b> 시스템에 대해 설명하고 있습니다. 이러한 접근법은 모델 스스로 검색 여부를 결정함으로써 효율성을 높이는 것이 핵심 목표입니다.

<b>본론</b>
1. <b>L-RAG</b>: 엔트로피 기반 게이팅을 통해 두 단계 구조를 구현합니다; 쿼리는 먼저 압축된 문서 요약으로 처리되고, 예측 엔트로리가 임계값보다 높아 불확실성이 감지될 때 비로소 비용이 큰 청크 검색이 수행됩니다[2601.06551v1].
2. <b>MBA-RAG</b>: 다중‑아ーム 밴딧 알고리즘을 활용해 각 쿼리의 복잡도에 따라 가장 적합한 검색 전략을 동적으로 선택합니다; 탐색과 활용의 균형을 맞추며, 정확도와 효율성을 동시에 고려하는 역동적 보상 함수를 도입했습니다[2412.01572v4].
3. <b>SELF-ROUTE</b>: 모델 자체 반성(self‑reflection)에 기반해 쿼리를 RAG 또는 LC(Long Context)로 라우팅하도록 설계된 간단한 방법입니다; 이는 계산 비용을 크게 낮추면서도 성능을 유지합니다[2407.16833v2].

<b>결론</b>
L-RAG은 엔트로피 기반의 적응형 검색을 통해 정확도와 효율성 사이의 가변적인 트레이드오프를 제공하며, tau=0.5일 때 78.2%의 정확도를 유지하면서 검색량을 8% 감소시키고, tau=1.0일 때는 검색량 감소가 26%로 증가한다[2601.06551v1]. MBA-RAG는 밴디트 접근법을 적용해 단일 홉 및 멀티 홉 데이터셋에서 새로운 상태-of-the-art 결과를 달성하며, 기존 Adaptive-RAG보다 분류 정확도가 유의미하게 높다[2412.01572v4]. 두 연구 모두 적응형 검색을 통해 검색 비용을 줄이려는 목표를 공유하지만, L-RAG은 엔트로피 신호를 활용한 가변적 임계값 설정에 초점을 맞추고, MBA-RAG는 밴디트 메커니즘을 이용해 데이터셋 전반에서 성능을 향상시킨다[2601.06551v1][2412.01572v4].

_A 컨텍스트 3편_: 2601.06551 L-RAG: Balancing Context and Retrieval with Entropy-Based La · 2412.01572 MBA-RAG: a Bandit Approach for Adaptive Retrieval-Augmented  · 2407.16833 Retrieval Augmented Generation or Long-Context LLMs? A Compr

### 답 B

<b>서론</b>
제공된 연구들은 <b>적응형 RAG</b>(Adaptive Retrieval-Augmented Generation)를 통해 모델 스스로 검색 빈도를 조절하는 방법을 제시하고 있다. 이러한 접근은 쿼리의 복잡성이나 불확실성에 따라 필요한 만큼만 벡터 데이터베이스에 조회하도록 설계되어, 고처리량 환경에서 효율성을 크게 향상시킨다[2601.06551v1][2412.01572v4].

<b>본론</b>
1. <b>L-RAG (Entropy-Based Lazy Loading)</b>: 엔트로피 기반 게이팅을 이용해 모델의 예측 불확실성이 임계값보다 높으면 비싼 chunk 검색만 수행한다; 이는 쿼리당 지연 시간을 최대 약 80‑210 ms 감소시킨다[2601.06551v1].
2. <b>MBA-RAG (Multi-armed Bandit Adaptive Retrieval)</b>: 다중 팔 밴딧 알고리즘을 적용해 각 조회 방법을 ‘팔’로 간주하고, 탐험과 활용의 균형을 통해 쿼리 복잡성에 맞춰 최적의 검색 전략을 동적으로 선택한다[2412.01572v4].
3. <b>SELF‑ROUTE (Self-Reflection Routing)</b>: 모델이 자체 반성을 이용해 해당 요청에 RAG 또는 LC(Long Context) 중 하나를 라우팅하도록 설계되어, 계산 비용을 크게 낮추면서 성능은 유지한다[2407.16833v2].

<b>결론</b>
L-RAG은 엔트로피 기반의 적응형 검색을 통해 정확도와 효율성 사이의 가변적인 트레이드오프를 제공하며, tau=0.5일 때 78.2%의 정확도를 유지하면서 검색량을 8% 감소시키고, tau=1.0일 때는 검색량 감소가 26%로 증가한다[2601.06551v1]. MBA-RAG는 밴디트 접근법을 적용해 단일 홉 및 멀티 홉 데이터셋에서 새로운 상태-of-the-art 결과를 달성하며, 기존 Adaptive-RAG보다 분류 정확도가 유의미하게 높다[2412.01572v4]. 두 연구 모두 적응형 검색을 통해 검색 비용을 줄이려는 목표를 공유하지만, L-RAG은 엔트로피 신호를 활용한 가변적 임계값 설정에 초점을 맞추고, MBA-RAG는 밴디트 메커니즘을 이용해 데이터셋 전반에서 성능을 향상시킨다[2601.06551v1][2412.01572v4].

_B 컨텍스트 3편_: 2601.06551 L-RAG: Balancing Context and Retrieval with Entropy-Based La · 2412.01572 MBA-RAG: a Bandit Approach for Adaptive Retrieval-Augmented  · 2407.16833 Retrieval Augmented Generation or Long-Context LLMs? A Compr

### 인용 블록

- **2601.06551** [인용 AB] L-RAG: Balancing Context and Retrieval with Entropy-Based Lazy Loading — [초록] Retrieval-Augmented Generation (RAG) has emerged as the predominant paradigm for grounding Large Language Model outputs in factual knowledge, effectively mitigating hallucinations. However, conventional RAG systems operate under a "retrieve-always" assumption, querying vector databases for every input regardless of query complexity. This static approach incurs substantial computational overhead and inference latency, particularly problematic for high-throughput production deployments. We introduce L-RAG (Lazy Retrieval-Augmented Generation), an adaptive framework that implements hierarchical context management through entropy-based gating. L-RAG employs a two-tier architecture: queries are first processed with a compact document summary, and expensive chunk retrieval is triggered only when the model's predictive entropy exceeds a calibrated threshold, signaling genuine uncertainty. 

- **2412.01572** [인용 AB] MBA-RAG: a Bandit Approach for Adaptive Retrieval-Augmented Generation through Question Complexity — [초록] Retrieval Augmented Generation (RAG) has proven to be highly effective in boosting the generative performance of language model in knowledge-intensive tasks. However, existing RAG framework either indiscriminately perform retrieval or rely on rigid single-class classifiers to select retrieval methods, leading to inefficiencies and suboptimal performance across queries of varying complexity. To address these challenges, we propose a reinforcement learning-based framework that dynamically selects the most suitable retrieval strategy based on query complexity. % our solution Our approach leverages a multi-armed bandit algorithm, which treats each retrieval method as a distinct ``arm'' and adapts the selection process by balancing exploration and exploitation. Additionally, we introduce a dynamic reward function that balances accuracy and efficiency, penalizing methods that require more

- **2407.16833** [인용 AB] Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach — However, RAG’s significantly lower cost remains a distinct advantage. Based on this observation, we propose S ELF -R OUTE, a simple yet effective method that routes queries to RAG or LC based on model self-reflection. S ELF R OUTE significantly reduces the computation cost while maintaining a comparable performance to LC. Our findings provide a guideline for long-context applications of LLMs using RAG and LC. **1** **Introduction** _Retrieval augmented generation (RAG)_ has been

---

## Q_G03

**질문** Chinchilla 논문에서 권장한 토큰 대 파라미터 비율이 얼마야?

### 답 A

<b>서론</b>
Chinchilla 논문은 <b>compute‑optimal training</b> 하에서 모델 파라미터 수와 학습 토큰 수가 어떻게 비례해야 하는지를 제시하고 있습니다. 이는 고정된 컴퓨팅 예산 내에서 가장 효율적인 모델을 설계하기 위해 필요한 핵심 비율을 찾는 문제입니다.

<b>본론</b>
1. <b>Chinchilla</b>: “모델 크기와 훈련 데이터 양은 동등하게 스케일링되어야 한다”는 원칙에 따라, 파라미터 수가 두 배가 되면 학습 토큰 수도 두배로 증가시켜야 한다고 제안합니다[2203.15556v1]. 이 가설을 테스트하기 위해 Gopher와 동일한 컴퓨팅 예산으로 70B 파라미터·4× 더 많은 데이터를 사용한 Chinchilla 모델을 훈련했고, 이는 기존 모델들보다 일관되게 높은 성능과 효율성을 보였습니다[2203.15556v1].
<b>결론</b>
Chinchilla 논문은 <b>파라미터 수 : 학습 토큰 수가 약 1:2</b> (모델 크기가 두 배가 되면 데이터도 두배) 로 균등하게 스케일링하는 것을 권장합니다. 이는 고정된 컴퓨팅 예산에서 모델과 데이터를 동등히 증가시켜 최적의 성능을 달성하도록 설계되었습니다[2203.15556v1].

_A 컨텍스트 3편_: 2001.08361 Scaling Laws for Neural Language Models · 2406.18922 Time Matters: Scaling Laws for Any Budget · 2203.15556 Training Compute-Optimal Large Language Models

### 답 B

<b>서론</b>
토큰과 파라미터 비율에 대한 구체적인 수치는 Chinchilla 논문에서 제시되고 있습니다.

<b>본론</b>
1. <b>Chinchilla</b>: 모델 크기와 학습 데이터 양을 동등하게 스케일링해야 한다고 제안합니다 (모델 크기 두 배 → 훈련 토크도 두 배). [2203.15556v1]
2. <b>Optimal model scaling</b>: 컴퓨팅 예산이 증가함에 따라 파라미터 수와 학습 데이터를 약동적으로 같은 비율로 늘려야 함을 강조한다. [2001.08361v1][2203.15556v1]

<b>결론</b>
따라서 Chinchilla 논문에서 권장한 토큰 대 파라미터 비율은 <b>모델 크기와 데이터 양을 동등하게 증가시키는 것</b>이며, 이는 컴퓨팅 예산이 커질수록 두 요소를 같은 비례로 확대해야 한다는 원칙으로 요약됩니다.

_B 컨텍스트 3편_: 2001.08361 Scaling Laws for Neural Language Models · 2406.18922 Time Matters: Scaling Laws for Any Budget · 2203.15556 Training Compute-Optimal Large Language Models

### 인용 블록

- **2203.15556** [인용 AB] Training Compute-Optimal Large Language Models — [초록] We investigate the optimal model size and number of tokens for training a transformer language model under a given compute budget. We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models whilst keeping the amount of training data constant. By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and the number of training tokens should be scaled equally: for every doubling of model size the number of training tokens should also be doubled. We test this hypothesis by training a predicted compute-optimal model, Chinchilla, that uses the same compute budget as Gopher but with 70B parameters and 4$\times$ more more data. Chinchilla uniformly and significantly outperforms Gopher (280B), GPT-

- **2001.08361** [인용 B] Scaling Laws for Neural Language Models — [초록] We study empirical scaling laws for language model performance on the cross-entropy loss. The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude. Other architectural details such as network width or depth have minimal effects within a wide range. Simple equations govern the dependence of overfitting on model/dataset size and the dependence of training speed on model size. These relationships allow us to determine the optimal allocation of a fixed compute budget. Larger models are significantly more sample-efficient, such that optimally compute-efficient training involves training very large models on a relatively modest amount of data and stopping significantly before convergence. Throughout we will observe precise power-law scalings for performance as a function of trai
