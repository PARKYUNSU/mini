## OB_009

**질문** 질의 확장 기법 논문 두 편만 골라줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>Generative Query Reformulation Using Ensemble Prompting, Document Fusion, and Relevance Feedback</b>: 이 논문은 제로샷 질의 개선을 위해 앙상블 프롬팅과 문서 퓨전 기법을 도입하고, 관련성 피드백을 통합하여 검색 성능을 향상시킨다[2405.17658v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 1편_: 2405.17658 Generative Query Reformulation Using Ensemble Prompting, Doc

### 답 B

<b>서론</b>
질의 확장(query expansion)은 사용자의 원래 검색어를 더 나은 의도와 일치하도록 변환하여 검색 경험을 향상시키는 과정으로, 대규모 언어 모델(LLM) 기반 제로샷 접근법이 최근 주목받고 있습니다[2405.17658v1]. 그러나 단일 프롬프트만으로는 다양한 상황에서의 성능 한계가 존재합니다.

<b>본론</b>
1. <b>GenQREnsemble</b>: 영사프롬팅(ensemble prompting) 전략을 활용해 제로스HOT 지시문의 패러파라임을 이용해 여러 키워드 세트를 생성하고, 이를 통해 검색 효과를 최대화하는 기법입니다[2405.17658v1]. GenQREnsemble과 유사하게 영사프롬팅 기반의 프롬프트를 사용하지만, 다수의 관련 문서와 오라클·비판자 LLM으로부터 피드백을 통합하여 검색 성능을 추가로 향상시키는 방식입니다[2405.17658v1].
<b>결론</b>
제공된 두 논문은 모두 질의를 확장하기 위해 대규모 언어 모델을 활용한 영사프롬팅과 다양한 피드백 메커니즘을 결합한 접근법을 제시합니다. GenQREnsemble이 기본 키워드 생성에 초점을 맞추는 반면, GenQRFusion은 추가적인 관련성 피드백을 통합함으로써 검색 성능을 더욱 향상시킵니다.

_B 컨텍스트 1편_: 2405.17658 Generative Query Reformulation Using Ensemble Prompting, Doc

### 인용 블록

- **2405.17658** [인용 AB] Generative Query Reformulation Using Ensemble Prompting, Document Fusion, and Relevance Feedback — [초록] Query Reformulation (QR) is a set of techniques used to transform a user's original search query to a text that better aligns with the user's intent and improves their search experience. Recently, zero-shot QR has been a promising approach due to its ability to exploit knowledge inherent in large language models. Inspired by the success of ensemble prompting strategies which have benefited other tasks, we investigate if they can improve query reformulation. In this context, we propose two ensemble-based prompting techniques, GenQREnsemble and GenQRFusion which leverage paraphrases of a zero-shot instruction to generate multiple sets of keywords to improve retrieval performance ultimately. We further introduce their post-retrieval variants to incorporate relevance feedback from a variety of sources, including an oracle simulating a human user and a "critic" LLM. We demonstrate that a

---

## OB_014

**질문** 지식 그래프로 LLM 답을 보강하는 연구 아무거나 하나 골라줘

### 답 A

<b>서론</b>
LLM은 파라메트릭 지식에 의존하지만, 명시적인 <b>지식 그래프</b>를 활용해 사실 정확성을 높이는 것이 어려운 과제입니다. 이러한 하이브리드 접근법에서 LLM의 답변이 KG 정보를 통해 보강되는 구체적인 연구는 현재 문서에는 제시되어 있지 않습니다.

<b>본론</b>
1. <b>Large Language Models and Knowledge Graphs: Opportunities and Challenges</b>: 이 논문은 LLM과 지식 그래프를 결합한 하이브리드 표현에 대한 기회와 과제를 논의하며, 관련 연구 주제와 도전 과제들을 소개한다[2308.06374v1].
2. (관련 문서 없음): 제공된 [참고 문서]에는 구체적인 KG 기반 LLM 답변 보강 연구를 다루는 내용이 없습니다.

<b>결론</b>
제공된 문서는 하이브리드 표현의 기회·과제를 논의하지만, 실제로 지식 그래프로 LLM 답을 보강하는 구체적 연구 사례를 제시하지 않습니다. 따라서 질문에서 요구한 특정 연구에 대한 정보는 현재 문서에는 포함되어 있지 않으며, 추가적인 검색이 필요할 수 있습니다.

_A 컨텍스트 1편_: 2308.06374 Large Language Models and Knowledge Graphs: Opportunities an

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>Large Language Models and Knowledge Graphs: Opportunities and Challenges</b>: 이 논문은 LLM(파라메트릭 지식)과 KG(명시적 지식)의 하이브리드 표현 전환을 논의하고, 관련 기회와 과제를 제시한다[2308.06374v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 1편_: 2308.06374 Large Language Models and Knowledge Graphs: Opportunities an

### 인용 블록

- **2308.06374** [인용 AB] Large Language Models and Knowledge Graphs: Opportunities and Challenges — [초록] Large Language Models (LLMs) have taken Knowledge Representation -- and the world -- by storm. This inflection point marks a shift from explicit knowledge representation to a renewed focus on the hybrid representation of both explicit knowledge and parametric knowledge. In this position paper, we will discuss some of the common debate points within the community on LLMs (parametric knowledge) and Knowledge Graphs (explicit knowledge) and speculate on opportunities and visions that the renewed focus brings, as well as related research topics and challenges. # **Large Language Models and Knowledge Graphs: Opportunities and Challenges** ## **Jeff Z. Pan** � � � The University of Edinburgh, United Kingdom **Simon Razniewski** � Bosch Center for AI, Germany **Jan-Christoph Kalo** � Vrije Universiteit Amsterdam, The Netherlands

---

## OB_020

**질문** 자연어로 코드를 찾는 연구 추천 좀 해줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
자연어로 코드를 찾는 작업은 자연어 설명과 실제 구현 사이의 복잡한 매핑 관계를 이해해야 하므로 매우 어려운 과제입니다.

<b>본론</b>
1. <b>SciReplicate-Bench</b>: 2024년 발표된 NLP 논문에서 추출한 36개의 논문에 대한 총 100개 작업을 포함한 벤치마크로, 알고리즘 설명을 바탕으로 코드를 생성하는 LLM 평가에 사용됩니다[2504.00255v2].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 1편_: 2504.00255 SciReplicate-Bench: Benchmarking LLMs in Agent-driven Algori

### 답 B

<b>서론</b>
자연어로 코드를 찾는 작업은 <b>코드 검색(Code Search)</b> 과 관련된 연구 분야이며, 자연어 설명과 실제 구현 사이의 간극 때문에 어려운 문제입니다[2504.00255v2].

<b>본론</b>
1. <b>SciReplicate-Bench</b>: 최근 NLP 논문에서 제시된 알고리즘 기술에 대한 코드 생성을 평가하기 위해 설계된 벤치마크로, 2024년 발표된 36편의 논문을 기반으로 한 총 100개의 작업과 상세 주석 및 포괄적인 테스트 케이스를 제공합니다[2504.00255v2]. Paper Agent와 Code Agent가 결합된 이중 에이전트 프레임워크로, 논문에서 알고리즘 개념을 해석하고 저장소에서 의존성을 검색해 솔루션을 구현합니다[2504.00255v2].
<b>결론</b>
제공된 문서에 따르면 자연어로 코드를 찾는 연구는 SciReplicate-Bench라는 벤치마크를 통해 평가되며, 이를 기반으로 Paper Agent와 Code Agent가 포함된 이중 에이전트 시스템인 Sci-Reproducer로 접근할 수 있습니다.

_B 컨텍스트 1편_: 2504.00255 SciReplicate-Bench: Benchmarking LLMs in Agent-driven Algori

### 인용 블록

- **2504.00255** [인용 AB] SciReplicate-Bench: Benchmarking LLMs in Agent-driven Algorithmic Reproduction from Research Papers — [초록] This study evaluates large language models (LLMs) in generating code from algorithm descriptions in recent NLP papers. The task requires two key competencies: (1) algorithm comprehension: synthesizing information from papers and academic literature to understand implementation logic, and (2) coding expertise: identifying dependencies and correctly implementing necessary APIs. To facilitate rigorous evaluation, we introduce SciReplicate-Bench, a benchmark of 100 tasks from 36 NLP papers published in 2024, featuring detailed annotations and comprehensive test cases. Building on SciReplicate-Bench, we propose Sci-Reproducer, a dual-agent framework consisting of a Paper Agent that interprets algorithmic concepts from literature and a Code Agent that retrieves dependencies from repositories and implements solutions. To assess algorithm understanding, we introduce reasoning graph accuracy

---

## OB_027

**질문** 화면을 보고 조작하는 GUI 에이전트 논문 두 편 추천해줘

### 답 A

<b>서론</b>
화면을 보고 조작하는 <b>GUI 에이전트</b>는 시각적 인터페이스를 이해하고, 복잡한 작업을 자동으로 수행해야 하므로 기술적으로 매우 어려운 과제이다. 이러한 문제를 해결하기 위해 최근 연구들은 다양한 접근법을 제시하고 있다.

<b>본론</b>
1. <b>Unified Framework for GUI Agents</b>: 이 논문은 GUI 에이전트의 인식·추리·계획·행동 능력을 포괄하는 통합 프레임워크를 제안하며, 벤치마크와 평가 지표 등을 체계적으로 정리한다[2412.13501v3].
2. <b>(M)LLM‑Based GUI Agent Components Survey</b>: 대규모 언어 모델을 기반으로 한 현대 GUI 에이전트가 갖는 네 가지 핵심 구성 요소(인식·탐색·계획·상호작용)를 상세히 분석하고, 각 기술의 발전과 평가 방법론을 제시한다[2504.13865v2].
3. <b>UI‑MOPD: Multi‑Platform On‑Policy Distillation</b>: 단일 플랫폼에서 다중 플랫폼으로 확장되는 GUI 에이전트 학습에 어려움을 해결하기 위해 고해상도 교차플랫폼 데이터셋 Uni‑GUI와 멀티교사 온폴리시 디스틸레이션(MOPD) 프레임워크를 도입한다[2607.04425v2].
4. <b>Work2Skill: Human Experience Capture for Reusable Agent Skills</b>: 인간이 수행한 데스크톱 GUI 조작을 녹화·정렬하여 재사용 가능한 에이전트 기술을 유도하는 WorkRecorder와 동기화된 멀티모달 데이터셋 WorkDemo‑350을 제공한다[2610.12984v1].

<b>결론</b>
제공된 문서들은 GUI 에이전트 연구의 다양한 측면을 다루며, 결과에 있어서는 데이터와 평가 환경이 달라 성능 차이가 존재한다. [2412.13501v3]은 현재까지의 진행 상황과 기술들을 종합적으로 정리한 개요를 제공한다[2412.13501v3]. [2504.13865v2]는 다중 모달 학습과 대규모 언어 모델이 데스크톱·모바일·웹 플랫폼 전반에 걸쳐 GUI 자동화를 혁신했다고 강조한다[2504.13865v2]. [2607.04425v2]은 단일 데이터셋을 이용해 교차 플랫폼 에이전트를 구축하고, OSWorld와 MobileWorld에서 각각 38.2%와 12.0%의 작업 성공률을 달성했다[2607.04425v2]. [2610.12984v1]는 인간 GUI 시연 데이터를 활용해 에이전트 기술을 유도했으며, MyPCBench Bounded Action과 OSWorld-Verified에서 기존 무기술 기반보다 높은 점수와 성공률을 보였다[2610.12984v1]. 따라서 이러한 연구들은 데이터 유형(데이터셋 기반 vs. 다중 플랫폼 통합) 및 평가 조건에 따라 성능이 달라지며, 전반적으로 GUI 에이전트 기술이 지속적으로 발전하고 있음을 보여준다.

_A 컨텍스트 5편_: 2412.13501 GUI Agents: A Survey · 2504.13865 A Survey on (M)LLM-Based GUI Agents · 2607.04425 UI-MOPD: Multi-Platform On-Policy Distillation for Unified G · 2610.12984 Work2Skill: Capturing Human GUI Experience for Reusable Agen · 2609.33304 Relevance Does Not Imply Applicability: Experience Activatio

### 답 B

<b>서론</b>
화면을 보고 조작하는 <b>GUI 에이전트</b>는 시각적 인터페이스를 인식하고, 복잡한 작업을 계획·실행해야 하므로 기술적으로 매우 어려운 과제입니다. 이러한 어려움을 해결하기 위해 다양한 연구가 진행되고 있습니다.

<b>본론</b>
1. <b>Unified Framework for GUI Agents</b>: 이 논문은 GUI 에이전트의 인지(Perception), 추론(reasoning), 기획(planning) 및 행동(actuation) 능력을 포괄하는 통합 프레임워크를 제시하고, 벤치마크·평가 지표·구조·훈련 방법을 종합적으로 정리합니다[2412.13501v3].
2. <b>Four Core Components of Modern GUI Agents</b>: 현대 GUI 에이전트는 (1) 다중모달 이해가 가능한 인지 시스템과 같은 네 가지 핵심 구성 요소로 구성되어 있으며, 대규모 언어 모델 기반 기술이 데스크톱·모바일·웹 플랫폼 전반에 적용되고 있습니다[2504.13865v2].

<b>결론</b>
제공된 문서들은 화면을 보고 조작하는 GUI 에이전트를 다루는 두 연구입니다. 첫 번째 논문은 통합 프레임워크와 종합적인 벤치마크를 제공하고, 두 번째 논문은 인지‑탐색‑계획‑상호작용 네 가지 핵심 구성 요소를 중심으로 현대 기술의 구조를 정리합니다.

_B 컨텍스트 5편_: 2412.13501 GUI Agents: A Survey · 2504.13865 A Survey on (M)LLM-Based GUI Agents · 2607.04425 UI-MOPD: Multi-Platform On-Policy Distillation for Unified G · 2610.12984 Work2Skill: Capturing Human GUI Experience for Reusable Agen · 2609.33304 Relevance Does Not Imply Applicability: Experience Activatio

### 인용 블록

- **2412.13501** [인용 AB] GUI Agents: A Survey — [초록] Graphical User Interface (GUI) agents, powered by Large Foundation Models, have emerged as a transformative approach to automating human-computer interaction. These agents autonomously interact with digital systems or software applications via GUIs, emulating human actions such as clicking, typing, and navigating visual elements across diverse platforms. Motivated by the growing interest and fundamental importance of GUI agents, we provide a comprehensive survey that categorizes their benchmarks, evaluation metrics, architectures, and training methods. We propose a unified framework that delineates their perception, reasoning, planning, and acting capabilities. Furthermore, we identify important open challenges and discuss key future directions. Finally, this work serves as a basis for practitioners and researchers to gain an intuitive understanding of current progress, techniques, 

- **2504.13865** [인용 AB] A Survey on (M)LLM-Based GUI Agents — [초록] Graphical User Interface (GUI) Agents have emerged as a transformative paradigm in human-computer interaction, evolving from rule-based automation scripts to sophisticated AI-driven systems capable of understanding and executing complex interface operations. This survey provides a comprehensive examination of the rapidly advancing field of LLM-based GUI Agents, systematically analyzing their architectural foundations, technical components, and evaluation methodologies. We identify and analyze four fundamental components that constitute modern GUI Agents: (1) perception systems that integrate text-based parsing with multimodal understanding for comprehensive interface comprehension; (2) exploration mechanisms that construct and maintain knowledge bases through internal modeling, historical experience, and external information retrieval; (3) planning frameworks that leverage advanced 

- **2607.04425** [인용 A] UI-MOPD: Multi-Platform On-Policy Distillation for Unified GUI Agents — [초록] Recent advances in multimodal foundation models and agent systems have driven GUI agents from single-platform task execution toward cross-platform interaction. However, unified multi-platform GUI learning remains challenging: high-quality cross-platform trajectories remain scarce, while platforms share transferable capabilities but differ in action semantics and interaction conventions. Naively mixing supervision or merging specialized models can blur native behaviors and produce imbalanced performance. To address these challenges, we construct Uni-GUI, a high-quality dataset containing nearly 10K executable cross-platform interaction trajectories collected through a unified desktop-mobile harness. Building on Uni-GUI, we propose UI-MOPD, the first framework to introduce multi-teacher on-policy distillation (MOPD) into unified multi-platform GUI agent training. UI-MOPD trains a shar

- **2610.12984** [인용 A] Work2Skill: Capturing Human GUI Experience for Reusable Agent Skill Induction — [초록] Computer-use agents can perform increasingly complex GUI tasks, yet unfamiliar software and workflows requiring human domain knowledge remain challenging. Human demonstrations convey procedural knowledge through the same GUI interaction space, but reuse requires interpreting actions in context and separating workflow rules from task-specific details. We thus introduce Work2Skill, a framework that captures human GUI experience for reusable agent skill induction. WorkRecorder provides the framework's infrastructure for collecting this experience, aligning screen recordings, mouse and keyboard events, and available accessibility-tree information. Using WorkRecorder, we construct WorkDemo-350, the first synchronized multimodal dataset of human desktop GUI demonstrations for reusable agent skill induction and downstream evaluation. Its 350 demonstrations are screened for completeness and

---

## OB_050

**질문** 소스 코드 오류를 자동으로 수정하는 언어 모델 연구 세 편 추천해줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 소스 코드 오류를 자동으로 수정하는 언어 모델에 대한 구체적인 세 편의 연구를 찾을 수 없다.

<b>본론</b>
1. <b>Augmenting Large Language Models with Static Code Analysis for Automated Code Quality Improvements</b>: 이 연구는 LLM을 소프트웨어 개발 워크플로우와 통합해 정적 코드 분석 프레임워크로 버그·취약점 등을 탐지하고, 각 이슈 정보를 추출하여 자동 코드 수정에 활용한다[2506.10330v1].

<b>결론</b>
따라서 질문이 찾는 세 편의 소스 코드 오류를 자동으로 수정하는 언어 모델 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 1편_: 2506.10330 Augmenting Large Language Models with Static Code Analysis f

### 답 B

<b>서론</b>
소스 코드 오류를 자동으로 수정하는 것은 <b>정적 분석</b>과 대규모 언어 모델(LLM) 을 결합해야 하며, 특히 LLM 의 환각 현상을 제어하고 외부 지식을 활용하여 정확한 변경 사항을 생성하도록 설계되어야 합니다. 이러한 복합적인 요구 때문에 단일 접근법으로는 한계가 있습니다.

<b>본론</b>
1. <b>Static Code Analysis Framework</b>: 정적 코드 분석 프레임워크를 이용해 대규모 소프트웨어 프로젝트 내에서 버그, 취약점 및 코드 냄새와 같은 문제를 탐지하고 각 이슈에 대한 상세 정보를 추출·정리합니다[2506.10330v1]. OpenAI 의 LLM 을 소프트웨어 개발 워크플로우에 통합하여 정적 분석으로 파악된 문제들을 자동으로 수정하고, 반복적인 프롬프트 엔지니어링과 RAG 를 통해 정확성과 관련성을 높입니다[2506.10330v1]. LLM 이 생성한 변경 사항이 오류를 포함하지 않도록 검증하는 맞춤형 “코드 비교 앱”을 구축하여 환각 문제를 해결하고 잘못된 수정 전에 이를 교정합니다[2506.10330v1]
<b>결론</b>
제공된 문서에 따르면, 정적 코드 분석과 OpenAI 기반 대규모 언어 모델을 결합하면서 RAG 와 프롬프트 엔지니어링을 적용한 시스템이 소스 코드 오류를 자동으로 탐지·수정한 연구로 제시됩니다. 또한 “코드 비교 앱”이라는 검증 단계가 추가되어 LLM 의 환각 문제를 방지하고 실제 프로젝트에 안전한 수정 사항을 제공합니다.

_B 컨텍스트 1편_: 2506.10330 Augmenting Large Language Models with Static Code Analysis f

### 인용 블록

- **2506.10330** [인용 AB] Augmenting Large Language Models with Static Code Analysis for Automated Code Quality Improvements — [초록] This study examined code issue detection and revision automation by integrating Large Language Models (LLMs) such as OpenAI's GPT-3.5 Turbo and GPT-4o into software development workflows. A static code analysis framework detects issues such as bugs, vulnerabilities, and code smells within a large-scale software project. Detailed information on each issue was extracted and organized to facilitate automated code revision using LLMs. An iterative prompt engineering process is applied to ensure that prompts are structured to produce accurate and organized outputs aligned with the project requirements. Retrieval-augmented generation (RAG) is implemented to enhance the relevance and precision of the revisions, enabling LLM to access and integrate real-time external knowledge. The issue of LLM hallucinations - where the model generates plausible but incorrect outputs - is addressed by a cu

---

## OB_069

**질문** 이미지 캡셔닝 연구 좋은 논문 두 편 추천해줘

### 답 A

<b>서론</b>
이미지를 자연어로 설명하는 <b>이미지 캡셔닝</b>은 시각 정보를 텍스트로 변환해야 하므로 모델 설계와 데이터 활용 측면에서 어려운 과제이다. 최근 연구들은 다양한 접근법을 통해 성능과 효율성을 동시에 개선하고 있다.

<b>본론</b>
1. <b>SciCap</b>: SciBERT를 이용해 논문 제목·추록·인용 등 메타데이터를 인코딩한 후, CLIP+GPT‑2와 GPT‑2만 사용한 두 모델을 비교해 텍스트 기반 캡셔닝 성능을 평가한다[2407.11008v1].
2. <b>ViPCap</b>: 검색된 텍스트 프롬프트에 이미지 정보를 결합하여 시각적 특징을 강화하고, 이를 CLIP 공간으로 매핑·샘플링함으로써 기존 경량 모델보다 효율성과 정확성을 크게 향상시킨다[2412.19289v3].

<b>결론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 5편_: 2407.11008 Figuring out Figures: Using Textual References to Caption Sc · 2412.11025 From Simple to Professional: A Combinatorial Controllable Im · 2412.19289 ViPCap: Retrieval Text-Based Visual Prompts for Lightweight  · 2406.19512 Captioning Visualizations with Large Language Models (CVLLM) · 2412.10511 Automated Image Captioning with CNNs and Transformers

### 답 B

<b>서론</b>
이미지를 텍스트로 설명하는 <b>이미지 캡셔닝</b>은 시각 정보를 언어와 정확히 매핑해야 하므로 매우 어려운 과제이다. 최근 연구들은 다양한 모델 구조를 통해 성능과 효율성을 크게 향상시키고 있다.

<b>본론</b>
1. <b>SciCap</b>: SciBERT로 논문 제목·초록·인용 등 텍스트 메타데이터를 인코딩하고, CLIP+GPT‑2와 같은 이미지 캡셔닝 모델을 사용하여 해당 정보를 함께 활용한다[2407.11008v1].
2. <b>ViPCap</b>: 검색된 텍스트 프롬프트에 이미지의 시각적 정보를 결합해 가우시안 샘플링을 통해 새로운 시각 프롬프트를 생성하고, 이를 CLIP 공간으로 매핑함으로써 기존 모델보다 효율성과 성능이 크게 향상된다[2412.19289v3].

<b>결론</b>
제공한 두 논문은 각각 메타데이터 기반 텍스트 인코딩과 검색된 텍스트‑이미지 결합 프롬프트라는 서로 다른 접근법을 통해 이미지 캡셔닝의 정확도와 속도를 개선한다. 따라서 질문에서 요구하는 좋은 연구 사례로 이 두 논문을 추천할 수 있다.

_B 컨텍스트 5편_: 2407.11008 Figuring out Figures: Using Textual References to Caption Sc · 2412.11025 From Simple to Professional: A Combinatorial Controllable Im · 2412.19289 ViPCap: Retrieval Text-Based Visual Prompts for Lightweight  · 2406.19512 Captioning Visualizations with Large Language Models (CVLLM) · 2412.10511 Automated Image Captioning with CNNs and Transformers

### 인용 블록

- **2407.11008** [인용 AB] Figuring out Figures: Using Textual References to Caption Scientific Figures — [초록] Figures are essential channels for densely communicating complex ideas in scientific papers. Previous work in automatically generating figure captions has been largely unsuccessful and has defaulted to using single-layer LSTMs, which no longer achieve state-of-the-art performance. In our work, we use the SciCap datasets curated by Hsu et al. and use a variant of a CLIP+GPT-2 encoder-decoder model with cross-attention to generate captions conditioned on the image. Furthermore, we augment our training pipeline by creating a new dataset MetaSciCap that incorporates textual metadata from the original paper relevant to the figure, such as the title, abstract, and in-text references. We use SciBERT to encode the textual metadata and use this encoding alongside the figure embedding. In our experimentation with different models, we found that the CLIP+GPT-2 model performs better when it rec

- **2412.19289** [인용 AB] ViPCap: Retrieval Text-Based Visual Prompts for Lightweight Image Captioning — [초록] Recent lightweight image captioning models using retrieved data mainly focus on text prompts. However, previous works only utilize the retrieved text as text prompts, and the visual information relies only on the CLIP visual embedding. Because of this issue, there is a limitation that the image descriptions inherent in the prompt are not sufficiently reflected in the visual embedding space. To tackle this issue, we propose ViPCap, a novel retrieval text-based visual prompt for lightweight image captioning. ViPCap leverages the retrieved text with image information as visual prompts to enhance the ability of the model to capture relevant visual information. By mapping text prompts into the CLIP space and generating multiple randomized Gaussian distributions, our method leverages sampling to explore randomly augmented distributions and effectively retrieves the semantic features that 

---

## OB_081

**질문** 시계열 파운데이션 모델 최신 연구 두 편 알려줘

### 답 A

<b>서론</b>
시계열 파운데이션 모델은 방대한 데이터와 복잡한 패턴 학습 능력을 바탕으로 시계열 예측 성능을 크게 향상시킬 수 있지만, 기존 방법들에 비해 높은 계산 비용과 해석 어려움이라는 과제를 안고 있다[2405.16312v2][2412.19286v1]. 이러한 한계를 극복하기 위해 최근 연구에서는 파라미터 효율성을 높이고 이론적 기반을 강화하는 새로운 모델들이 제안되고 있다.

<b>본론</b>
1. <b>Time-SSM</b>: Dynamic Spectral Operator라는 새로운 이론 프레임워크를 도입하여 시계열 데이터에 SSM 적용의 직관적이고 일반적인 지침을 제공한다[2405.16312v2].
2. <b>LeForecast (Le-TSFM)</b>: Le‑TSFM이라는 대형 파운데이션 모델을 포함한 세 가지 모델 엔진(대형 기반, 다중모달, 하이브리드) 을 결합한 엔터프라이즈 플랫폼으로 시계열 작업을 위한 통합 해석과 예측을 제공한다[2503.22747v1].
3. <b>Timestral</b>: DHF (Decoupled Horizon Forecasting), covariate 프레임워크 및 두 단계 파이프라인(대규모 합성 데이터 사전학습 → 실제·합성 혼합 포스트트레이닝) 을 활용해 파라미터 규모가 다양하고 GIFT‑Eval, TIME 등에서 최상위 성능을 달성한다[2610.37585v1].

<b>결론</b>
제공된 문서들은 시계열 파운데이션 모델 분야에서 <b>Time-SSM</b>이 이론적 기반과 낮은 파라미터 수로 효율성을 높이고, <b>LeForecast (Le-TSFM)</b>가 다중 엔진 구조를 통해 엔터프라이즈 수준의 통합 예측을 제공하며, <b>Timestral</b>이 대규모 합성 데이터와 해부된 호리존 학습으로 최상위 성능을 달성한다는 점을 보여준다.

_A 컨텍스트 5편_: 2405.16312 Time-SSM: Simplifying and Unifying State Space Models for Ti · 2503.22747 LeForecast: Enterprise Hybrid Forecast by Time Series Intell · 2610.37585 Timestral · 2412.19286 Time Series Foundational Models: Their Role in Anomaly Detec · 2412.16643 TimeRAG: BOOSTING LLM Time Series Forecasting via Retrieval-

### 답 B

<b>서론</b>
시계열 파운데이션 모델은 방대한 데이터와 복잡한 구조를 학습해 예측 성능과 일반화 능력을 크게 향상시키지만, 여전히 해석 가능성 부족·검증된 벤치마크 부재 등의 과제가 남아 있다[2405.16312v2][2412.19286v1]. 이러한 한계를 극복하기 위해 최근 연구들은 이론적 프레임워크 개선 및 실용적인 플랫폼 구축에 집중하고 있다.

<b>본론</b>
1. <b>Time-SSM</b>: Dynamic Spectral Operator라는 새로운 이론을 제안해 SSM 적용 지침을 직관적으로 제공하며, 파라미터 수를 Mamba 대비 7분의 1로 줄인 Time‑SSM 기반 파운데이션 모델을 도입했다[2405.16312v2].
2. <b>LeForecast (enterprise hybrid forecast)</b>: Le-TSFM이라는 대형 기초 모델과 멀티모달·하이브리드 엔진을 결합한 세 기둥 구조를 통해 시계열 데이터 해석, 예측 및 최적화를 수행하는 기업용 플랫폼으로 구현되었다[2503.22747v1].

<b>결론</b>
제공된 문서들은 Time‑SSM이 이론적 프레임워크와 파라미터 효율성을 개선하고, LeForecast가 대형 기초 모델을 활용한 실용적인 하이브리드 구조를 통해 시계열 파운데이션 모델의 성능과 적용 범위를 확장한다는 점을 보여준다.

_B 컨텍스트 5편_: 2405.16312 Time-SSM: Simplifying and Unifying State Space Models for Ti · 2503.22747 LeForecast: Enterprise Hybrid Forecast by Time Series Intell · 2610.37585 Timestral · 2412.19286 Time Series Foundational Models: Their Role in Anomaly Detec · 2412.16643 TimeRAG: BOOSTING LLM Time Series Forecasting via Retrieval-

### 인용 블록

- **2405.16312** [인용 AB] Time-SSM: Simplifying and Unifying State Space Models for Time Series Forecasting — [초록] State Space Models (SSMs) have emerged as a potent tool in sequence modeling tasks in recent years. These models approximate continuous systems using a set of basis functions and discretize them to handle input data, making them well-suited for modeling time series data collected at specific frequencies from continuous systems. Despite its potential, the application of SSMs in time series forecasting remains underexplored, with most existing models treating SSMs as a black box for capturing temporal or channel dependencies. To address this gap, this paper proposes a novel theoretical framework termed Dynamic Spectral Operator, offering more intuitive and general guidance on applying SSMs to time series data. Building upon our theory, we introduce Time-SSM, a novel SSM-based foundation model with only one-seventh of the parameters compared to Mamba. Various experiments validate both 

- **2412.19286** [인용 AB] Time Series Foundational Models: Their Role in Anomaly Detection and Prediction — [초록] Time series foundational models (TSFM) have gained prominence in time series forecasting, promising state-of-the-art performance across various applications. However, their application in anomaly detection and prediction remains underexplored, with growing concerns regarding their black-box nature, lack of interpretability and applicability. This paper critically evaluates the efficacy of TSFM in anomaly detection and prediction tasks. We systematically analyze TSFM across multiple datasets, including those characterized by the absence of discernible patterns, trends and seasonality. Our analysis shows that while TSFMs can be extended for anomaly detection and prediction, traditional statistical and deep learning models often match or outperform TSFM in these tasks. Additionally, TSFMs require high computational resources but fail to capture sequential dependencies effectively or im

- **2503.22747** [인용 AB] LeForecast: Enterprise Hybrid Forecast by Time Series Intelligence — [초록] Demand is spiking in industrial fields for multidisciplinary forecasting, where a broad spectrum of sectors needs planning and forecasts to streamline intelligent business management, such as demand forecasting, product planning, inventory optimization, etc. Specifically, these tasks expecting intelligent approaches to learn from sequentially collected historical data and then foresee most possible trend, i.e. time series forecasting. Challenge of it lies in interpreting complex business contexts and the efficiency and generalisation of modelling. With aspirations of pre-trained foundational models for such purpose, given their remarkable success of large foundation model across legions of tasks, we disseminate \leforecast{}, an enterprise intelligence platform tailored for time series tasks. It integrates advanced interpretations of time series data and multi-source information, an

- **2610.37585** [인용 A] Timestral — [초록] We introduce Timestral, a family of four time series foundation models for probabilistic forecasting, with 5M, 28M, 123M, and 209M parameters. Timestral sets a new state of the art on GIFT-Eval, TIME, and fev-bench, where Timestral-209M and Timestral-123M take the top two places on every metric. We achieve this with three ingredients: Decoupled Horizon Forecasting (DHF), which separates prediction tokens from the causally encoded context, so that longer horizons are trained without masking context and each observed value is both a forecast target and context for later forecasts; a covariate framework that natively supports known-future covariates within a causal architecture; and a two-stage pipeline that pretrains exclusively on a diverse, large-scale synthetic corpus before post-training on a mix of real and synthetic data with extended context. This report describes the model des

---

## OB_089

**질문** 로봇 정책 학습 논문 세 편 추천해줘

### 답 A

<b>서론</b>
로봇 정책 학습은 다양한 환경과 작업에 대해 일반화할 수 있는 정책을 자동으로 획득해야 하는 어려운 과제이다. 특히, 인간 시연 데이터만으로는 제한된 성능으로 인해 실제 적용에서 한계가 발생하고 있다. 이러한 문제를 해결하기 위해 최근 연구들은 온라인 상호작용을 통한 정제와 로봇 군집 경험을 공유하는 방식을 제안한다.

<b>본론</b>
1. <b>Policy Decorator</b>: 모델‑agnostic 잔여 정책을 이용해 대규모 시뮬레이션 학습 모델을 실시간 환경과 상호작용하며 지속적으로 개선한다[2412.13630v1].
2. <b>ENPIRE</b>: 코딩 에이전트를 활용해 실제 로봇에서 정책 실행 → 검증 → 정제라는 반복 피드백 루프를 자동화하고, 이를 통해 다exterous 조작 작업의 성공률을 크게 향상시킨다[2606.19980v2].
3. <b>Collective Experience Learning (CEL)</b>: 배포된 여러 로봇이 자신의 실패 경험을 공유하여 공통 정책을 미세 조정하며, 추가 전문가 시연 없이도 정책 신뢰성을 높인다[2610.25736v1].

<b>결론</b>
제공된 세 논문은 모두 로봇 정책 학습 분야에서 높은 성공률을 달성하지만, 데이터 수집 방식과 적용 대상에 따라 결과가 달라진다. Policy Decorator는 오프라인으로 학습된 모델을 온라인 환경과 상호작용시켜 성능을 향상시키며, 8개의 과제에서 두 최첨단 시뮬레이션 벤치마크(ManiSkill, Adroit)에서 검증되었다[2412.13630v1]. ENPIRE는 실제 로봇을 이용해 반복적인 피드백 루프를 통해 정책을 스스로 개선하고, 프론티어 코딩 에이전트 팀을 활용하면 핀 박스 정리와 같은 정교한 조작 과제에서 99%의 성공률을 달성한다[2606.19980v2]. Learning from Fleet Experience는 로봇 플릿 전체의 경험을 공유하는 집단 학습 패러다임을 제시하며, 실제 조작 과제에서 93.3~99.2%의 성공률을 보이며, 특정 작업(예: 휴대폰 포장)에서는 로봇 수를 늘리면 성공률이 79.2%에서 98.3%로 크게 향상된다[2610.25736v1]. 따라서 각 방법은 데이터 소스(시뮬레이션 vs 실제), 학습 대상(오프라인 모델 개선 vs 자체 개선 vs 플릿 경험 공유), 그리고 평가 조건에 따라 성능 차이가 존재한다.

_A 컨텍스트 5편_: 2412.13630 Policy Decorator: Model-Agnostic Online Refinement for Large · 2606.19980 ENPIRE: Agentic Robot Policy Self-Improvement in the Real Wo · 2610.25736 Learning from Fleet Experience: A Collective Learning Paradi · 2412.09858 RLDG: Robotic Generalist Policy Distillation via Reinforceme · 2606.06556 Robots Need More than VLA and World Models

### 답 B

<b>서론</b>
로봇 정책 학습은 다양한 환경에서 안정적이고 효율적인 행동을 생성해야 하는 복잡한 문제이며, 특히 시연 데이터와 모델 규모에 한계가 있어 지속적인 개선이 필요합니다. 이러한 어려움을 해결하기 위해 최근 연구들은 온라인 상호작용과 집단 경험 활용 등 새로운 접근법을 제시하고 있습니다.

<b>본론</b>
1. <b>Policy Decorator</b>: 대형 imitation learning 모델을 온라인 환경과의 상호작용 동안 model‑agnostic residual policy로 정제하여 안정적이고 샘플 효율적인 학습을 가능하게 합니다[2412.13630v1]
2. <b>ENPIRE</b>: 코딩 에이전트를 활용해 실제 로봇에서 정책을 자동으로 개선하는 폐쇄 루프 시스템을 구축합니다 (Environment, Policy Improvement, Rollout, Evolution 모듈) [2606.19980v2]
3. <b>Collective Experience Learning (CEL)</b>: 배포된 다중 로봇이 실행 경험을 공유하고 FERT와 같은 메커니즘으로 공통 정책의 신뢰성을 향상시킵니다[2610.25736v1]

<b>결론</b>
제공된 문서들은 각각 온라인 정제, 자동화된 실제 환경에서의 자기 개선, 그리고 집단 경험 기반 학습이라는 세 가지 다른 접근법을 제시합니다. 따라서 로봇 정책 학습을 위한 연구로는 Policy Decorator, ENPIRE 및 Collective Experience Learning이 적합하며, 각 방법은 데이터 효율성·자동화·확장성을 강화하는 고유한 장점을 가집니다.

_B 컨텍스트 5편_: 2412.13630 Policy Decorator: Model-Agnostic Online Refinement for Large · 2606.19980 ENPIRE: Agentic Robot Policy Self-Improvement in the Real Wo · 2610.25736 Learning from Fleet Experience: A Collective Learning Paradi · 2412.09858 RLDG: Robotic Generalist Policy Distillation via Reinforceme · 2606.06556 Robots Need More than VLA and World Models

### 인용 블록

- **2412.13630** [인용 AB] Policy Decorator: Model-Agnostic Online Refinement for Large Policy Model — [초록] Recent advancements in robot learning have used imitation learning with large models and extensive demonstrations to develop effective policies. However, these models are often limited by the quantity, quality, and diversity of demonstrations. This paper explores improving offline-trained imitation learning models through online interactions with the environment. We introduce Policy Decorator, which uses a model-agnostic residual policy to refine large imitation learning models during online interactions. By implementing controlled exploration strategies, Policy Decorator enables stable, sample-efficient online learning. Our evaluation spans eight tasks across two benchmarks-ManiSkill and Adroit-and involves two state-of-the-art imitation learning models (Behavior Transformer and Diffusion Policy). The results show Policy Decorator effectively improves the offline-trained policies a

- **2606.19980** [인용 AB] ENPIRE: Agentic Robot Policy Self-Improvement in the Real World — [초록] Achieving dexterous robotic manipulation in the real world heavily relies on human supervision and algorithm engineering, which becomes a central bottleneck in the pursuit of general physical intelligence. Although emerging coding agents can generate code to automate algorithm search, their successes remain largely confined in digital environments. We conjecture that the missing abstraction to automate robotics research is a repeatable feedback loop for real-world policy improvement: reset the scene, execute a policy, verify the outcome, and refine the next iteration. To bridge this gap, we introduce ENPIRE, a harness framework for coding agents that instantiates this physical feedback routine with four core modules: an Environment module (EN) for automatic reset and verification, a Policy Improvement module (PI) that launches policy refinement, a Rollout module (R) to evaluate poli

- **2610.25736** [인용 AB] Learning from Fleet Experience: A Collective Learning Paradigm for Robots — [초록] Experience generated during deployment offers an opportunity for robots to improve policy reliability through learning from their own executions. However, learning through human corrections requires teleoperators to monitor execution and intervene when policies fail, a demand that is difficult to meet as robot fleets grow. We introduce collective experience learning (CEL), a learning paradigm in which deployed robots share their execution experience to improve a common policy. We realize CEL through failure-guided experience retrieval fine-tuning (FERT), which uses failure contexts from robot executions to retrieve relevant trajectory segments from the fleet's shared successful experience and uses their actions as supervision for policy updates, without collecting additional expert demonstrations or corrective actions. A fault-tolerant asynchronous training system (FATS) coordinates

---

## OB_101

**질문** 판결문을 분석하는 언어 모델 최신 논문 추천해줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 판결문 분석은 복잡한 법적 논리와 구조화된 정보를 정확히 이해해야 하므로 어려운 과제입니다.

<b>본론</b>
1. <b>Retrieval-Augmented Generation with Vector Stores, Knowledge Graphs, and Hierarchical Non-negative Matrix Factorization</b>: 이 시스템은 RAG와 벡터 스토어·지식 그래프를 결합해 법적 문서의 복잡한 관계를 파악하고 인용 오류나 추상적 논리를 줄입니다[2502.20364v2].
2. <b>Retrieval Augmented Generation based prompt example selection method for German legal education analysis</b>: 이 방법은 데이터가 풍부한 상황에서 예측 정확도를 크게 향상시키며, 사전 학습된 LLM을 활용합니다[2412.15902v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 5편_: 2410.15064 A Prompt Engineering Approach and a Knowledge Graph based Fr · 2408.10343 LegalBench-RAG: A Benchmark for Retrieval-Augmented Generati · 2412.15902 On the Suitability of pre-trained foundational LLMs for Anal · 2502.20364 Bridging Legal Knowledge and AI: Retrieval-Augmented Generat · 2412.20468 A Comprehensive Framework for Reliable Legal AI: Combining S

### 답 B

<b>서론</b>
판결문과 같은 복잡한 법률 텍스트를 분석하는 것은 <b>맥락 이해</b>, <b>관계 추론</b> 및 <b>정확한 인용 생성</b>이라는 어려운 과제를 포함합니다. 이러한 작업은 모델의 환각 현상을 최소화하면서도 법적 정확성을 유지해야 하므로, 단순 언어 모델을 넘어 추가적인 지식 구조와 검색 메커니즘이 필요합니다.

<b>본론</b>
1. <b>LegalBench-RAG</b>: Retrieval-Augmented Generation (RAG) 파이프라인에서 핵심인 '검색' 단계만을 평가하는 벤치마크를 제시합니다. 최소한의 관련 텍스트 조각을 추출하도록 설계되어, 문서 ID나 큰 불완전한 청크보다 정밀한 검색 결과를 제공합니다[2408.10343v1].
2. <b>Retrieval Augmented Generation based prompt example selection</b>: 고데이터 가용 시나리오에서 예측 성능을 크게 향상시키는 방법론으로 도입되었습니다. 이 접근법은 전이 학습된 LLM에 프롬프트 예시를 추가해 데이터가 부족한 상황에서도 기반선을 능회합니다[2412.15902v1].
3. <b>Generative AI system integrating RAG, VS, KG</b>: 벡터 스토어와 지식 그래프를 결합한 생성형 시스템을 통해 법적 문서의 복잡한 관계를 탐색하고 인용을 최소화하는 환각 현상을 줄입니다. 웹 크롤링으로 공개된 법률 텍스트(법령·헌장 판례) 를 수집해 의미적 표현과 계층 관계, 잠재 주제 발견을 활용합니다[2502.20364v2].

<b>결론</b>
제공된 문서들은 모두 법적 도메인에서 RAG 시스템을 평가하거나 활용하는 연구이지만, 각각의 초점이 다릅니다. [2408.10343v1]는 LegalBench-RAG 벤치마크를 통해 기존 LLM 기반 평가와 달리 검색 구성 요소 자체를 평가할 필요성을 강조하고, 관련성 높은 스니펫이 문서 ID나 부정확한 큰 조각보다 선호됨을 보여줍니다. [2412.15902v1]는 독일 법률 교육 맥락에서 전처리된 기초 LLM의 성능을 평가하며, 데이터가 풍부한 상황에서는 RAG 기반 프롬프트 선택 방법이 예측을 크게 향상시키고, 적은 라벨 데이터 상황에서도 체인 오브 사운드를 통해 베이스라인을 능가함을 제시합니다. [2502.20364v2]는 벡터 스토어와 지식 그래프를 활용한 RAG 기술이 방대한 비정형 법률 문서에서 복잡한 관계를 파악하고 법적 추세를 예측하는 데 효과적임을 강조하며, 추적 가능한 법적 추론을 모델 설계에 포함해야 함을 지적합니다. 따라서 이 세 논문은 모두 법적 도메인에서 RAG의 중요성을 인정하지만, 평가 대상(검색 구성 요소 vs 전체 시스템 성능), 데이터 조건(데이터 풍부 vs 적은 라벨), 그리고 기술적 접근법(스니펫 선호 vs 프롬프트 선택 vs 다중 저장소)에 따라 결과가 달라집니다.

_B 컨텍스트 5편_: 2410.15064 A Prompt Engineering Approach and a Knowledge Graph based Fr · 2408.10343 LegalBench-RAG: A Benchmark for Retrieval-Augmented Generati · 2412.15902 On the Suitability of pre-trained foundational LLMs for Anal · 2502.20364 Bridging Legal Knowledge and AI: Retrieval-Augmented Generat · 2412.20468 A Comprehensive Framework for Reliable Legal AI: Combining S

### 인용 블록

- **2502.20364** [인용 AB] Bridging Legal Knowledge and AI: Retrieval-Augmented Generation with Vector Stores, Knowledge Graphs, and Hierarchical Non-negative Matrix Factorization — [초록] Agentic Generative AI, powered by Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG), Knowledge Graphs (KGs), and Vector Stores (VSs), represents a transformative technology applicable to specialized domains such as legal systems, research, recommender systems, cybersecurity, and global security, including proliferation research. This technology excels at inferring relationships within vast unstructured or semi-structured datasets. The legal domain here comprises complex data characterized by extensive, interrelated, and semi-structured knowledge systems with complex relations. It comprises constitutions, statutes, regulations, and case law. Extracting insights and navigating the intricate networks of legal documents and their relations is crucial for effective legal research. Here, we introduce a generative AI system that integrates RAG, VS, and KG, constructed 

- **2412.15902** [인용 AB] On the Suitability of pre-trained foundational LLMs for Analysis in German Legal Education — [초록] We show that current open-source foundational LLMs possess instruction capability and German legal background knowledge that is sufficient for some legal analysis in an educational context. However, model capability breaks down in very specific tasks, such as the classification of "Gutachtenstil" appraisal style components, or with complex contexts, such as complete legal opinions. Even with extended context and effective prompting strategies, they cannot match the Bag-of-Words baseline. To combat this, we introduce a Retrieval Augmented Generation based prompt example selection method that substantially improves predictions in high data availability scenarios. We further evaluate the performance of pre-trained LLMs on two standard tasks for argument mining and automated essay scoring and find it to be more adequate. Throughout, pre-trained LLMs improve upon the baseline in scenario

- **2408.10343** [인용 B] LegalBench-RAG: A Benchmark for Retrieval-Augmented Generation in the Legal Domain — [초록] Retrieval-Augmented Generation (RAG) systems are showing promising potential, and are becoming increasingly relevant in AI-powered legal applications. Existing benchmarks, such as LegalBench, assess the generative capabilities of Large Language Models (LLMs) in the legal domain, but there is a critical gap in evaluating the retrieval component of RAG systems. To address this, we introduce LegalBench-RAG, the first benchmark specifically designed to evaluate the retrieval step of RAG pipelines within the legal space. LegalBench-RAG emphasizes precise retrieval by focusing on extracting minimal, highly relevant text segments from legal documents. These highly relevant snippets are preferred over retrieving document IDs, or large sequences of imprecise chunks, both of which can exceed context window limitations. Long context windows cost more to process, induce higher latency, and lead

---

## OB_118

**질문** 과학 논문을 자동 요약하는 연구 중 읽을 만한 것 알려줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>A Comparative Study of Quality Evaluation Methods for Text Summarization</b>: 이 논문은 텍스트 요약을 평가하기 위해 대형 언어 모델(LLM) 기반 방법을 제안하고, 기존 자동 메트릭(ROUGE‑2, BERTScore 등), 인간 평가를 포함한 8가지 방법과 비교 연구를 수행한다[2407.00747v1].
2. <b>Survey on Abstractive Text Summarization: Dataset, Models, and Metrics</b>: 이 조사는 트랜스포머 기반 모델이 주의 메커니즘을 활용해 원문을 패러프레이징하여 인간 표현에 가까운 요약 생성한다는 점을 강조하고, 다양한 데이터셋과 평가 지표(semantic overlap 등)를 검토한다[2412.17165v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_A 컨텍스트 4편_: 2407.00747 A Comparative Study of Quality Evaluation Methods for Text S · 2604.27924 Can AI Be a Good Peer Reviewer? A Survey of Peer Review Proc · 2606.28277 Towards Automating Scientific Review with Google's Paper Ass · 2412.17165 Survey on Abstractive Text Summarization: Dataset, Models, a

### 답 B

<b>서론</b>
과학 논문을 <b>자동 요약</b>하는 작업은 방대한 양의 텍스트를 압축하면서도 핵심 내용을 정확히 전달해야 하므로 어려운 과제이다. 특히 기존 자동 평가 지표는 참고 요약을 크게 의존하거나 인간 평가를 대체하기 어렵다.

<b>본론</b>
1. <b>LLM 기반 문서 요약</b>: 대형 언어 모델(LLMs)을 활용해 문서를 자동으로 요약하고, ROUGE‑2·BERTScore와 같은 전통적 자동 지표를 보완한다[2606.28277v1].
2. <b>Paper Assistant Tool (PAT)</b>: 전체 과학 논문을 입력받아 이론 결과 검증과 실험 확인 등을 수행하며, 수학적 오류 탐지에서 제로샷 재현율 대비 34% 향상된 성능을 보인다[2407.00747v1][2606.28277v1]

<b>결론</b>
제공된 문서들은 과학 논문 자동 요약과 관련된 연구가 아니라, 각각 텍스트 요약 품질 평가 방법 비교와 과학 리뷰 자동화 도구인 PAT에 대한 결과를 다루고 있습니다. 따라서 질문에서 찾는 '과학 논문을 자동 요약하는 연구'는 해당 문서들에 포함되어 있지 않습니다. [2407.00747v1]은 특허 문서 데이터셋을 대상으로 LLM 기반 평가가 인간 평가와 일치함을 보였으며, [2606.28277v1]은 PAT 도구가 수학 오류를 34% 향상시키고 STOC·ICML 컨퍼런스에서 사전 제출 도구로 활용됨을 보고합니다.

_B 컨텍스트 4편_: 2407.00747 A Comparative Study of Quality Evaluation Methods for Text S · 2604.27924 Can AI Be a Good Peer Reviewer? A Survey of Peer Review Proc · 2606.28277 Towards Automating Scientific Review with Google's Paper Ass · 2412.17165 Survey on Abstractive Text Summarization: Dataset, Models, a

### 인용 블록

- **2407.00747** [인용 AB] A Comparative Study of Quality Evaluation Methods for Text Summarization — [초록] Evaluating text summarization has been a challenging task in natural language processing (NLP). Automatic metrics which heavily rely on reference summaries are not suitable in many situations, while human evaluation is time-consuming and labor-intensive. To bridge this gap, this paper proposes a novel method based on large language models (LLMs) for evaluating text summarization. We also conducts a comparative study on eight automatic metrics, human evaluation, and our proposed LLM-based method. Seven different types of state-of-the-art (SOTA) summarization models were evaluated. We perform extensive experiments and analysis on datasets with patent documents. Our results show that LLMs evaluation aligns closely with human evaluation, while widely-used automatic metrics such as ROUGE-2, BERTScore, and SummaC do not and also lack consistency. Based on the empirical comparison, we prop

- **2412.17165** [인용 A] Survey on Abstractive Text Summarization: Dataset, Models, and Metrics — [초록] The advancements in deep learning, particularly the introduction of transformers, have been pivotal in enhancing various natural language processing (NLP) tasks. These include text-to-text applications such as machine translation, text classification, and text summarization, as well as data-to-text tasks like response generation and image-to-text tasks such as captioning. Transformer models are distinguished by their attention mechanisms, pretraining on general knowledge, and fine-tuning for downstream tasks. This has led to significant improvements, particularly in abstractive summarization, where sections of a source document are paraphrased to produce summaries that closely resemble human expression. The effectiveness of these models is assessed using diverse metrics, encompassing techniques like semantic overlap and factual correctness. This survey examines the state of the art 

- **2606.28277** [인용 B] Towards Automating Scientific Review with Google's Paper Assistant Tool — [초록] Artificial intelligence is driving a revolution in scientific discovery, accelerating everything from hypothesis generation to mathematical theorem proving. However, this rapid acceleration is creating a systemic challenge: traditional human peer review cannot scale to match the influx of AI-assisted science. Ultimately, to resolve this tension, we must also deploy AI to accelerate the verification and review process itself. To frame the discussion around this transition, we propose a taxonomy consisting of four progressive levels of AI-human collaboration in scientific evaluation, and discuss various trade-offs involved with each. As a step toward this future, we introduce the Paper Assistant Tool (PAT), an agentic AI framework built for deep scientific review and verification. PAT ingests full scientific manuscripts and produces a comprehensive evaluation, checking theoretical res
