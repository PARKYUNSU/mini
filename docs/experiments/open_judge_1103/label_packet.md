## OB_005

**질문** 밀집 검색기를 학습시키는 방법 논문 세 편 추천해줘

- [문서 1] **Fine-Grained Guidance for Retrievers: Leveraging LLMs' Feedback in Retrieval-Augmented Generation** — [초록] Retrieval-Augmented Generation (RAG) has proven to be an effective method for mitigating hallucination issues inherent in large language models (LLMs). Previous approaches typically train retrievers based on semantic similarity, lacking optimization for RAG. More recent works have proposed aligning retrievers with the preference signals of LLMs. However, these preference signals are often difficult for dense ret
- [문서 2] **LLM2IR: simple unsupervised contrastive learning makes long-context LLM great retriever** — [초록] Modern dense information retrieval (IR) models usually rely on costly large-scale pretraining. In this paper, we introduce LLM2IR, an efficient unsupervised contrastive learning framework to convert any decoder-only large language model (LLM) to an information retrieval model. Despite its simplicity, the effectiveness is proven among different LLMs on multiple IR benchmarks including LoCo, LongEmbed and BEIR. We
- [문서 3] **Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence** — [초록] Dense retrieval models are commonly used in Information Retrieval (IR) applications, such as Retrieval-Augmented Generation (RAG). Since they often serve as the first step in these systems, their robustness is critical to avoid downstream failures. In this work, we repurpose a relation extraction dataset (e.g., Re-DocRED) to design controlled experiments that quantify the impact of heuristic biases, such as a pr
- [문서 4] **Dense Passage Retrieval for Open-Domain Question Answering** — [초록] Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When ev
- [문서 5] **Towards Competitive Search Relevance For Inference-Free Learned Sparse Retrievers** — [초록] Learned sparse retrieval, which can efficiently perform retrieval through mature inverted-index engines, has garnered growing attention in recent years. Particularly, the inference-free sparse retrievers are attractive as they eliminate online model inference in the retrieval phase thereby avoids huge computational cost, offering reasonable throughput and latency. However, even the state-of-the-art (SOTA) infere

---

## OB_009

**질문** 질의 확장 기법 논문 두 편만 골라줘

- [문서 1] **Generative Query Reformulation Using Ensemble Prompting, Document Fusion, and Relevance Feedback** — [초록] Query Reformulation (QR) is a set of techniques used to transform a user's original search query to a text that better aligns with the user's intent and improves their search experience. Recently, zero-shot QR has been a promising approach due to its ability to exploit knowledge inherent in large language models. Inspired by the success of ensemble prompting strategies which have benefited other tasks, we invest

---

## OB_010

**질문** 검색 질의를 늘려 쓰는 연구 중에 괜찮은 논문 하나 알려줘

- [문서 1] **Multi-Turn Agentic Scientific Literature Search via Workflow Induction** — [초록] Scientific literature search often requires more than retrieving papers from a single query: users' intents are underspecified, preference-dependent, and evolve through interaction. Existing search agents typically rely on fixed pipelines or implicit language-only reasoning, making their search strategies difficult to control, inspect, and refine. We introduce PaperPilot, a multi-turn literature search agent tha
- [문서 2] **InteractiveSurvey: An LLM-based Personalized and Interactive Survey Paper Generation System** — [초록] The exponential growth of academic literature creates urgent demands for comprehensive survey papers, yet manual writing remains time-consuming and labor-intensive. Recent advances in large language models (LLMs) and retrieval-augmented generation (RAG) facilitate studies in synthesizing survey papers from multiple references, but most existing works restrict users to title-only inputs and fixed outputs, neglect
- [문서 3] **From Interests to Insights: An LLM Approach to Course Recommendations Using Natural Language Queries** — [초록] Most universities in the United States encourage their students to explore academic areas before declaring a major and to acquire academic breadth by satisfying a variety of requirements. Each term, students must choose among many thousands of offerings, spanning dozens of subject areas, a handful of courses to take. The curricular environment is also dynamic, and poor communication and search functions on campu
- [문서 4] **A survey: Information search time optimization based on RAG (Retrieval Augmentation Generation) chatbot** — [초록] Retrieval-Augmented Generation (RAG) based chatbots are not only useful for information retrieval through questionanswering but also for making complex decisions based on injected private data.we present a survey on how much search time can be saved when retrieving complex information within an organization called "X Systems"(a stealth mode company) by using a RAG-based chatbot compared to traditional search met

---

## OB_014

**질문** 지식 그래프로 LLM 답을 보강하는 연구 아무거나 하나 골라줘

- [문서 1] **Large Language Models and Knowledge Graphs: Opportunities and Challenges** — [초록] Large Language Models (LLMs) have taken Knowledge Representation -- and the world -- by storm. This inflection point marks a shift from explicit knowledge representation to a renewed focus on the hybrid representation of both explicit knowledge and parametric knowledge. In this position paper, we will discuss some of the common debate points within the community on LLMs (parametric knowledge) and Knowledge Graph

---

## OB_019

**질문** 코드 검색 모델 논문 세 편만 뽑아줘

- [문서 1] **Issue Localization via LLM-Driven Iterative Code Graph Searching** — [초록] Issue solving aims to generate patches to fix reported issues in real-world code repositories according to issue descriptions. Issue localization forms the basis for accurate issue solving. Recently, LLM-based issue localization methods have demonstrated state-of-the-art performance. However, these methods either search from files mentioned in issue descriptions or in the whole repository and struggle to balance
- [문서 2] **Seed-CTS: Unleashing the Power of Tree Search for Superior Performance in Competitive Coding Tasks** — [초록] Competition-level code generation tasks pose significant challenges for current state-of-the-art large language models (LLMs). For example, on the LiveCodeBench-Hard dataset, models such as O1-Mini and O1-Preview achieve pass@1 rates of only 0.366 and 0.143, respectively. While tree search techniques have proven effective in domains like mathematics and general coding, their potential in competition-level code g

---

## OB_020

**질문** 자연어로 코드를 찾는 연구 추천 좀 해줘

- [문서 1] **SciReplicate-Bench: Benchmarking LLMs in Agent-driven Algorithmic Reproduction from Research Papers** — [초록] This study evaluates large language models (LLMs) in generating code from algorithm descriptions in recent NLP papers. The task requires two key competencies: (1) algorithm comprehension: synthesizing information from papers and academic literature to understand implementation logic, and (2) coding expertise: identifying dependencies and correctly implementing necessary APIs. To facilitate rigorous evaluation, w

---

## OB_022

**질문** 에이전트가 계획을 세우는 방법 최신 논문 두 편 알려줘

- [문서 1] **Planning, Living and Judging: A Multi-agent LLM-based Framework for Cyclical Urban Planning** — [초록] Urban regeneration presents significant challenges within the context of urbanization, requiring adaptive approaches to tackle evolving needs. Leveraging advancements in large language models (LLMs), we propose Cyclical Urban Planning (CUP), a new paradigm that continuously generates, evaluates, and refines urban plans in a closed-loop. Specifically, our multi-agent LLM-based framework consists of three key comp
- [문서 2] **Systematic Analysis of LLM Contributions to Planning: Solver, Verifier, Heuristic** — [초록] In this work, we provide a systematic analysis of how large language models (LLMs) contribute to solving planning problems. In particular, we examine how LLMs perform when they are used as problem solver, solution verifier, and heuristic guidance to improve intermediate solutions. Our analysis reveals that although it is difficult for LLMs to generate correct plans out-of-the-box, LLMs are much better at providi
- [문서 3] **ToolTree: Efficient LLM Agent Tool Planning via Dual-Feedback Monte Carlo Tree Search and Bidirectional Pruning** — [초록] Large Language Model (LLM) agents are increasingly applied to complex, multi-step tasks that require interaction with diverse external tools across various domains. However, current LLM agent tool planning methods typically rely on greedy, reactive tool selection strategies that lack foresight and fail to account for inter-tool dependencies. In this paper, we present ToolTree, a novel Monte Carlo tree search-ins
- [문서 4] **InstructRAG: Leveraging Retrieval-Augmented Generation on Instruction Graphs for LLM-Based Task Planning** — [초록] Recent advancements in large language models (LLMs) have enabled their use as agents for planning complex tasks. Existing methods typically rely on a thought-action-observation (TAO) process to enhance LLM performance, but these approaches are often constrained by the LLMs' limited knowledge of complex tasks. Retrieval-augmented generation (RAG) offers new opportunities by leveraging external databases to ground
- [문서 5] **KGLAMP: Knowledge Graph-guided Language model for Adaptive Multi-robot Planning and Replanning** — [초록] Heterogeneous multi-robot systems are increasingly deployed in long-horizon missions that require coordination among robots with diverse capabilities. However, existing planning approaches struggle to construct accurate symbolic representations and maintain plan consistency in dynamic environments. Classical PDDL planners require manually crafted symbolic models, while LLM-based planners often ignore agent heter

---

## OB_027

**질문** 화면을 보고 조작하는 GUI 에이전트 논문 두 편 추천해줘

- [문서 1] **GUI Agents: A Survey** — [초록] Graphical User Interface (GUI) agents, powered by Large Foundation Models, have emerged as a transformative approach to automating human-computer interaction. These agents autonomously interact with digital systems or software applications via GUIs, emulating human actions such as clicking, typing, and navigating visual elements across diverse platforms. Motivated by the growing interest and fundamental importan
- [문서 2] **A Survey on (M)LLM-Based GUI Agents** — [초록] Graphical User Interface (GUI) Agents have emerged as a transformative paradigm in human-computer interaction, evolving from rule-based automation scripts to sophisticated AI-driven systems capable of understanding and executing complex interface operations. This survey provides a comprehensive examination of the rapidly advancing field of LLM-based GUI Agents, systematically analyzing their architectural founda
- [문서 3] **UI-MOPD: Multi-Platform On-Policy Distillation for Unified GUI Agents** — [초록] Recent advances in multimodal foundation models and agent systems have driven GUI agents from single-platform task execution toward cross-platform interaction. However, unified multi-platform GUI learning remains challenging: high-quality cross-platform trajectories remain scarce, while platforms share transferable capabilities but differ in action semantics and interaction conventions. Naively mixing supervisio
- [문서 4] **Work2Skill: Capturing Human GUI Experience for Reusable Agent Skill Induction** — [초록] Computer-use agents can perform increasingly complex GUI tasks, yet unfamiliar software and workflows requiring human domain knowledge remain challenging. Human demonstrations convey procedural knowledge through the same GUI interaction space, but reuse requires interpreting actions in context and separating workflow rules from task-specific details. We thus introduce Work2Skill, a framework that captures human 
- [문서 5] **Relevance Does Not Imply Applicability: Experience Activation for Personal GUI Agents** — [초록] Personal Graphical User Interface (GUI) agents rely on interaction history to infer what a user wants from ambiguous instructions and to anticipate recurring routines. Existing approaches retrieve task-relevant history and append it to the policy's context, implicitly assuming that experience relevant to a task remains useful for each decision within it. We find that this help is largely spent at the first decis

---

## OB_044

**질문** 여러 번 샘플링해서 답을 고르는 연구 좋은 논문 하나 골라줘

- [문서 1] **DK-PRACTICE: An Intelligent Educational Platform for Personalized Learning Content Recommendations Based on Students Knowledge State** — [초록] This study introduces DK-PRACTICE (Dynamic Knowledge Prediction and Educational Content Recommendation System), an intelligent online platform that leverages machine learning to provide personalized learning recommendations based on student knowledge state. Students participate in a short, adaptive assessment using the question-and-answer method regarding key concepts in a specific knowledge domain. The system d

---

## OB_050

**질문** 소스 코드 오류를 자동으로 수정하는 언어 모델 연구 세 편 추천해줘

- [문서 1] **Augmenting Large Language Models with Static Code Analysis for Automated Code Quality Improvements** — [초록] This study examined code issue detection and revision automation by integrating Large Language Models (LLMs) such as OpenAI's GPT-3.5 Turbo and GPT-4o into software development workflows. A static code analysis framework detects issues such as bugs, vulnerabilities, and code smells within a large-scale software project. Detailed information on each issue was extracted and organized to facilitate automated code r

---

## OB_059

**질문** 지시 튜닝 데이터 구축 논문 세 편 추천해줘

- [문서 1] **Pay More Attention to the Robustness of Prompt for Instruction Data Mining** — [초록] Instruction tuning has emerged as a paramount method for tailoring the behaviors of LLMs. Recent work has unveiled the potential for LLMs to achieve high performance through fine-tuning with a limited quantity of high-quality instruction data. Building upon this approach, we further explore the impact of prompt's robustness on the selection of high-quality instruction data. This paper proposes a pioneering frame
- [문서 2] **Small Language Model as Data Prospector for Large Language Model** — [초록] The quality of instruction data directly affects the performance of fine-tuned Large Language Models (LLMs). Previously, \cite{li2023one} proposed \texttt{NUGGETS}, which identifies and selects high-quality quality data from a large dataset by identifying those individual instruction examples that can significantly improve the performance of different tasks after being learnt as one-shot instances. In this work,
- [문서 3] **Boosting LLM via Learning from Data Iteratively and Selectively** — [초록] Datasets nowadays are generally constructed from multiple sources and using different synthetic techniques, making data de-noising and de-duplication crucial before being used for post-training. In this work, we propose to perform instruction tuning by iterative data selection (\ApproachName{}). We measure the quality of a sample from complexity and diversity simultaneously. Instead of calculating the complexity
- [문서 4] **Curriculum Learning with Quality-Driven Data Selection** — [초록] The impressive multimodal capabilities demonstrated by OpenAI's GPT-4 have generated significant interest in the development of Multimodal Large Language Models (MLLMs). Visual instruction tuning of MLLMs with machine-generated instruction-following data has shown to enhance zero-shot capabilities across various tasks. However, there has been limited exploration into controlling the quality of the instruction da
- [문서 5] **Can Generalist Agents Automate Data Curation?** — [초록] Curating training data is among the most consequential yet labor-intensive parts of modern AI development: practitioners iteratively propose, implement, evaluate, and revise data policies against noisy benchmark feedback. We ask whether generalist coding agents can automate this data-curation loop. We introduce *Curation-Bench*, an agent-centric benchmark that fixes the model, training recipe, and evaluation sui

---

## OB_069

**질문** 이미지 캡셔닝 연구 좋은 논문 두 편 추천해줘

- [문서 1] **Figuring out Figures: Using Textual References to Caption Scientific Figures** — [초록] Figures are essential channels for densely communicating complex ideas in scientific papers. Previous work in automatically generating figure captions has been largely unsuccessful and has defaulted to using single-layer LSTMs, which no longer achieve state-of-the-art performance. In our work, we use the SciCap datasets curated by Hsu et al. and use a variant of a CLIP+GPT-2 encoder-decoder model with cross-atte
- [문서 2] **From Simple to Professional: A Combinatorial Controllable Image Captioning Agent** — [초록] The Controllable Image Captioning Agent (CapAgent) is an innovative system designed to bridge the gap between user simplicity and professional-level outputs in image captioning tasks. CapAgent automatically transforms user-provided simple instructions into detailed, professional instructions, enabling precise and context-aware caption generation. By leveraging multimodal large language models (MLLMs) and externa
- [문서 3] **ViPCap: Retrieval Text-Based Visual Prompts for Lightweight Image Captioning** — [초록] Recent lightweight image captioning models using retrieved data mainly focus on text prompts. However, previous works only utilize the retrieved text as text prompts, and the visual information relies only on the CLIP visual embedding. Because of this issue, there is a limitation that the image descriptions inherent in the prompt are not sufficiently reflected in the visual embedding space. To tackle this issue,
- [문서 4] **Captioning Visualizations with Large Language Models (CVLLM): A Tutorial** — [초록] Automatically captioning visualizations is not new, but recent advances in large language models(LLMs) open exciting new possibilities. In this tutorial, after providing a brief review of Information Visualization (InfoVis) principles and past work in captioning, we introduce neural models and the transformer architecture used in generic LLMs. We then discuss their recent applications in InfoVis, with a focus on
- [문서 5] **Automated Image Captioning with CNNs and Transformers** — [초록] This project aims to create an automated image captioning system that generates natural language descriptions for input images by integrating techniques from computer vision and natural language processing. We employ various different techniques, ranging from CNN-RNN to the more advanced transformer-based techniques. Training is carried out on image datasets paired with descriptive captions, and model performanc

---

## OB_074

**질문** 글자 인식 없이 문서를 읽는 모델 논문 추천 부탁해

- [문서 1] **Transcription and Recognition of Italian Parliamentary Speeches Using Vision-Language Models** — [초록] Parliamentary proceedings represent a rich yet challenging resource for computational analysis, particularly when preserved only as scanned historical documents. Existing efforts to transcribe Italian parliamentary speeches have relied on traditional Optical Character Recognition pipelines, resulting in transcription errors and limited semantic annotation. In this paper, we propose a pipeline based on Vision-Lan
- [문서 2] **OvisOCR2 Technical Report** — [초록] We introduce OvisOCR2, a 0.8B document parsing model. OvisOCR2 is designed as an end-to-end parser: given a document page image, it generates a Markdown representation in natural reading order, covering text, formulas, tables, and visual regions. We build a data engine that combines filtered real-document annotations with synthetic pages whose rendered images and Markdown targets are derived from the same HTML s
- [문서 3] **Target Prompting for Information Extraction with Vision Language Model** — [초록] The recent trend in the Large Vision and Language model has brought a new change in how information extraction systems are built. VLMs have set a new benchmark with their State-of-the-art techniques in understanding documents and building question-answering systems across various industries. They are significantly better at generating text from document images and providing accurate answers to questions. However
- [문서 4] **AgenticOCR: Parsing Only What You Need for Efficient Retrieval-Augmented Generation** — [초록] The expansion of retrieval-augmented generation (RAG) into multimodal domains has intensified the challenge for processing complex visual documents, such as financial reports. While page-level chunking and retrieval is a natural starting point, it creates a critical bottleneck: delivering entire pages to the generator introduces excessive extraneous context. This not only overloads the generator's attention mech

---

## OB_081

**질문** 시계열 파운데이션 모델 최신 연구 두 편 알려줘

- [문서 1] **Time-SSM: Simplifying and Unifying State Space Models for Time Series Forecasting** — [초록] State Space Models (SSMs) have emerged as a potent tool in sequence modeling tasks in recent years. These models approximate continuous systems using a set of basis functions and discretize them to handle input data, making them well-suited for modeling time series data collected at specific frequencies from continuous systems. Despite its potential, the application of SSMs in time series forecasting remains und
- [문서 2] **LeForecast: Enterprise Hybrid Forecast by Time Series Intelligence** — [초록] Demand is spiking in industrial fields for multidisciplinary forecasting, where a broad spectrum of sectors needs planning and forecasts to streamline intelligent business management, such as demand forecasting, product planning, inventory optimization, etc. Specifically, these tasks expecting intelligent approaches to learn from sequentially collected historical data and then foresee most possible trend, i.e. t
- [문서 3] **Timestral** — [초록] We introduce Timestral, a family of four time series foundation models for probabilistic forecasting, with 5M, 28M, 123M, and 209M parameters. Timestral sets a new state of the art on GIFT-Eval, TIME, and fev-bench, where Timestral-209M and Timestral-123M take the top two places on every metric. We achieve this with three ingredients: Decoupled Horizon Forecasting (DHF), which separates prediction tokens from th
- [문서 4] **Time Series Foundational Models: Their Role in Anomaly Detection and Prediction** — [초록] Time series foundational models (TSFM) have gained prominence in time series forecasting, promising state-of-the-art performance across various applications. However, their application in anomaly detection and prediction remains underexplored, with growing concerns regarding their black-box nature, lack of interpretability and applicability. This paper critically evaluates the efficacy of TSFM in anomaly detecti
- [문서 5] **TimeRAG: BOOSTING LLM Time Series Forecasting via Retrieval-Augmented Generation** — [초록] Although the rise of large language models (LLMs) has introduced new opportunities for time series forecasting, existing LLM-based solutions require excessive training and exhibit limited transferability. In view of these challenges, we propose TimeRAG, a framework that incorporates Retrieval-Augmented Generation (RAG) into time series forecasting LLMs, which constructs a time series knowledge base from historic

---

## OB_085

**질문** 강화학습 탐험 전략 논문 두 편만 골라줘

- [문서 1] **MaxInfoRL: Boosting exploration in reinforcement learning through information gain maximization** — [초록] Reinforcement learning (RL) algorithms aim to balance exploiting the current best strategy with exploring new options that could lead to higher rewards. Most common RL algorithms use undirected exploration, i.e., select random sequences of actions. Exploration can also be directed using intrinsic rewards, such as curiosity or model epistemic uncertainty. However, effectively balancing task and intrinsic rewards 
- [문서 2] **Learning Off-policy with Model-based Intrinsic Motivation For Active Online Exploration** — [초록] Recent advancements in deep reinforcement learning (RL) have demonstrated notable progress in sample efficiency, spanning both model-based and model-free paradigms. Despite the identification and mitigation of specific bottlenecks in prior works, the agent's exploration ability remains under-emphasized in the realm of sample-efficient RL. This paper investigates how to achieve sample-efficient exploration in con
- [문서 3] **AIR: Unifying Individual and Collective Exploration in Cooperative Multi-Agent Reinforcement Learning** — [초록] Exploration in cooperative multi-agent reinforcement learning (MARL) remains challenging for value-based agents due to the absence of an explicit policy. Existing approaches include individual exploration based on uncertainty towards the system and collective exploration through behavioral diversity among agents. However, the introduction of additional structures often leads to reduced training efficiency and in
- [문서 4] **Entropy-guided sequence weighting for efficient exploration in RL-based LLM fine-tuning** — [초록] We introduce Entropy-Guided Sequence Weighting (EGSW), a novel approach that enhances the exploration-exploitation tradeoff by dynamically assigning weights to generated outputs based on their advantage and entropy for Reinforcement Learning-based Large Language Model fine-tuning. EGSW integrates entropy regularization with advantage-based weighting to balance policy updates, enabling efficient exploration in hi
- [문서 5] **SHAPO: Sharpness-Aware Policy Optimization for Safe Exploration** — [초록] Safe exploration is a prerequisite for deploying reinforcement learning (RL) agents in safety-critical domains. In this paper, we approach safe exploration through the lens of epistemic uncertainty, where the actor's sensitivity to parameter perturbations serves as a practical proxy for regions of high uncertainty. We propose Sharpness-Aware Policy Optimization (SHAPO), a sharpness-aware policy update rule that 

---

## OB_089

**질문** 로봇 정책 학습 논문 세 편 추천해줘

- [문서 1] **Policy Decorator: Model-Agnostic Online Refinement for Large Policy Model** — [초록] Recent advancements in robot learning have used imitation learning with large models and extensive demonstrations to develop effective policies. However, these models are often limited by the quantity, quality, and diversity of demonstrations. This paper explores improving offline-trained imitation learning models through online interactions with the environment. We introduce Policy Decorator, which uses a model
- [문서 2] **ENPIRE: Agentic Robot Policy Self-Improvement in the Real World** — [초록] Achieving dexterous robotic manipulation in the real world heavily relies on human supervision and algorithm engineering, which becomes a central bottleneck in the pursuit of general physical intelligence. Although emerging coding agents can generate code to automate algorithm search, their successes remain largely confined in digital environments. We conjecture that the missing abstraction to automate robotics 
- [문서 3] **Learning from Fleet Experience: A Collective Learning Paradigm for Robots** — [초록] Experience generated during deployment offers an opportunity for robots to improve policy reliability through learning from their own executions. However, learning through human corrections requires teleoperators to monitor execution and intervene when policies fail, a demand that is difficult to meet as robot fleets grow. We introduce collective experience learning (CEL), a learning paradigm in which deployed r
- [문서 4] **RLDG: Robotic Generalist Policy Distillation via Reinforcement Learning** — [초록] Recent advances in robotic foundation models have enabled the development of generalist policies that can adapt to diverse tasks. While these models show impressive flexibility, their performance heavily depends on the quality of their training data. In this work, we propose Reinforcement Learning Distilled Generalists (RLDG), a method that leverages reinforcement learning to generate high-quality training data 
- [문서 5] **Robots Need More than VLA and World Models** — [초록] Generalist robot intelligence is often framed as a policy-scaling problem: collect more robot demonstrations, train larger Vision-Language-Action (VLA) models, and expect broader generalisation. In this position paper, we argue that this framing is incomplete. The central bottleneck is not only policy learning, but the absence of mechanisms that convert the world's abundant unstructured behavioural data into gro

---

## OB_093

**질문** 의료 영상 분석 AI 논문 두 편 추천해줘

- [문서 1] **Improving Sickle Cell Disease Classification: A Fusion of Conventional Classifiers, Segmented Images, and Convolutional Neural Networks** — [초록] Sickle cell anemia, which is characterized by abnormal erythrocyte morphology, can be detected using microscopic images. Computational techniques in medicine enhance the diagnosis and treatment efficiency. However, many computational techniques, particularly those based on Convolutional Neural Networks (CNNs), require high resources and time for training, highlighting the research opportunities in methods with l
- [문서 2] **A Hybrid Deep Learning and Model-Checking Framework for Accurate Brain Tumor Detection and Validation** — [초록] Model checking, a formal verification technique, ensures systems meet predefined requirements, playing a crucial role in minimizing errors and enhancing quality during development. This paper introduces a novel hybrid framework integrating model checking with deep learning for brain tumor detection and validation in medical imaging. By combining model-checking principles with CNN-based feature extraction and K-F
- [문서 3] **Unsupervised Denoising of Real Clinical Low Dose Liver CT with Perceptual Attention Networks** — [초록] With the development of deep learning, medical image processing has been widely used to assist clinical research. This paper focuses on the denoising problem of low-dose computed tomography using deep learning. Although low-dose computed tomography reduces radiation exposure to patients, it also introduces more noise, which may interfere with visual interpretation by physicians and affect diagnostic results. To 
- [문서 4] **Towards Autonomous and Auditable Medical Imaging Model Development** — [초록] Large language model (LLM) agents are beginning to automate machine learning engineering (MLE) by coupling planning, code execution, debugging, and empirical feedback. Translating this capability to medical imaging remains difficult because each task imposes modality-specific experimentation and strict requirements for validation protocols and prediction artifacts. Here we introduce AMID, an autonomous multi-age
- [문서 5] **A Review on the Integration of Artificial Intelligence and Medical Imaging in IVF Ovarian Stimulation** — [초록] Artificial intelligence (AI) has emerged as a powerful tool to enhance decision-making and optimize treatment protocols in in vitro fertilization (IVF). In particular, AI shows significant promise in supporting decision-making during the ovarian stimulation phase of the IVF process. This review evaluates studies focused on the applications of AI combined with medical imaging in ovarian stimulation, examining met

---

## OB_101

**질문** 판결문을 분석하는 언어 모델 최신 논문 추천해줘

- [문서 1] **A Prompt Engineering Approach and a Knowledge Graph based Framework for Tackling Legal Implications of Large Language Model Answers** — [초록] With the recent surge in popularity of Large Language Models (LLMs), there is the rising risk of users blindly trusting the information in the response, even in cases where the LLM recommends actions that have potential legal implications and this may put the user in danger. We provide an empirical analysis on multiple existing LLMs showing the urgency of the problem. Hence, we propose a short-term solution cons
- [문서 2] **LegalBench-RAG: A Benchmark for Retrieval-Augmented Generation in the Legal Domain** — [초록] Retrieval-Augmented Generation (RAG) systems are showing promising potential, and are becoming increasingly relevant in AI-powered legal applications. Existing benchmarks, such as LegalBench, assess the generative capabilities of Large Language Models (LLMs) in the legal domain, but there is a critical gap in evaluating the retrieval component of RAG systems. To address this, we introduce LegalBench-RAG, the fir
- [문서 3] **On the Suitability of pre-trained foundational LLMs for Analysis in German Legal Education** — [초록] We show that current open-source foundational LLMs possess instruction capability and German legal background knowledge that is sufficient for some legal analysis in an educational context. However, model capability breaks down in very specific tasks, such as the classification of "Gutachtenstil" appraisal style components, or with complex contexts, such as complete legal opinions. Even with extended context and
- [문서 4] **Bridging Legal Knowledge and AI: Retrieval-Augmented Generation with Vector Stores, Knowledge Graphs, and Hierarchical Non-negative Matrix Factorization** — [초록] Agentic Generative AI, powered by Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG), Knowledge Graphs (KGs), and Vector Stores (VSs), represents a transformative technology applicable to specialized domains such as legal systems, research, recommender systems, cybersecurity, and global security, including proliferation research. This technology excels at inferring relationships within vast u
- [문서 5] **A Comprehensive Framework for Reliable Legal AI: Combining Specialized Expert Systems and Adaptive Refinement** — [초록] This article discusses the evolving role of artificial intelligence (AI) in the legal profession, focusing on its potential to streamline tasks such as document review, research, and contract drafting. However, challenges persist, particularly the occurrence of "hallucinations" in AI models, where they generate inaccurate or misleading information, undermining their reliability in legal contexts. To address this

---

## OB_114

**질문** LLM이 지어내는 답을 줄이는 방법 세 편만 추천해줘

- [문서 1] **How Does Response Length Affect Long-Form Factuality** — [초록] Large language models (LLMs) are widely used for long-form text generation. However, factual errors in the responses would undermine their reliability. Despite growing attention to LLM factuality, the effect of response length on factuality remains underexplored. In this work, we systematically investigate this relationship by first introducing an automatic and bi-level long-form factuality evaluation framework,
- [문서 2] **Multiple Abstraction Level Retrieve Augment Generation** — [초록] A Retrieval-Augmented Generation (RAG) model powered by a large language model (LLM) provides a faster and more cost-effective solution for adapting to new data and knowledge. It also delivers more specialized responses compared to pre-trained LLMs. However, most existing approaches rely on retrieving prefix-sized chunks as references to support question-answering (Q/A). This approach is often deployed to addres
- [문서 3] **On the Influence of Context Size and Model Choice in Retrieval-Augmented Generation Systems** — [초록] Retrieval-augmented generation (RAG) has emerged as an approach to augment large language models (LLMs) by reducing their reliance on static knowledge and improving answer factuality. RAG retrieves relevant context snippets and generates an answer based on them. Despite its increasing industrial adoption, systematic exploration of RAG components is lacking, particularly regarding the ideal size of provided conte
- [문서 4] **Augmenting Question Answering with A Hybrid RAG Approach** — [초록] Retrieval-Augmented Generation (RAG) has emerged as a powerful technique for enhancing the quality of responses in Question-Answering (QA) tasks. However, existing approaches often struggle with retrieving contextually relevant information, leading to incomplete or suboptimal answers. In this paper, we introduce Structured-Semantic RAG (SSRAG), a hybrid architecture that enhances QA quality by integrating query 
- [문서 5] **DefAn: Definitive Answer Dataset for LLMs Hallucination Evaluation** — [초록] Large Language Models (LLMs) have demonstrated remarkable capabilities, revolutionizing the integration of AI in daily life applications. However, they are prone to hallucinations, generating claims that contradict established facts, deviating from prompts, and producing inconsistent responses when the same prompt is presented multiple times. Addressing these issues is challenging due to the lack of comprehensiv

---

## OB_118

**질문** 과학 논문을 자동 요약하는 연구 중 읽을 만한 것 알려줘

- [문서 1] **A Comparative Study of Quality Evaluation Methods for Text Summarization** — [초록] Evaluating text summarization has been a challenging task in natural language processing (NLP). Automatic metrics which heavily rely on reference summaries are not suitable in many situations, while human evaluation is time-consuming and labor-intensive. To bridge this gap, this paper proposes a novel method based on large language models (LLMs) for evaluating text summarization. We also conducts a comparative s
- [문서 2] **Can AI Be a Good Peer Reviewer? A Survey of Peer Review Process, Evaluation, and the Future** — [초록] Peer review is a multi-stage process involving reviews, rebuttals, meta-reviews, final decisions, and subsequent manuscript revisions. Recent advances in large language models (LLMs) have motivated methods that assist or automate different stages of this pipeline. In this survey, we synthesize techniques for (i) peer review generation, including fine-tuning strategies, agent-based systems, RL-based methods, and 
- [문서 3] **Towards Automating Scientific Review with Google's Paper Assistant Tool** — [초록] Artificial intelligence is driving a revolution in scientific discovery, accelerating everything from hypothesis generation to mathematical theorem proving. However, this rapid acceleration is creating a systemic challenge: traditional human peer review cannot scale to match the influx of AI-assisted science. Ultimately, to resolve this tension, we must also deploy AI to accelerate the verification and review pr
- [문서 4] **Survey on Abstractive Text Summarization: Dataset, Models, and Metrics** — [초록] The advancements in deep learning, particularly the introduction of transformers, have been pivotal in enhancing various natural language processing (NLP) tasks. These include text-to-text applications such as machine translation, text classification, and text summarization, as well as data-to-text tasks like response generation and image-to-text tasks such as captioning. Transformer models are distinguished by 

---

## O_03

**질문** 문서 청킹 관련 논문 두 편만 골라줘

- [문서 1] **Adaptive Chunking: Optimizing Chunking-Method Selection for RAG** — [초록] The effectiveness of Retrieval-Augmented Generation (RAG) is highly dependent on how documents are chunked, that is, segmented into smaller units for indexing and retrieval. Yet, commonly used "one-size-fits-all" approaches often fail to capture the nuanced structure and semantics of diverse texts. Despite its central role, chunking lacks a dedicated evaluation framework, making it difficult to assess and compar
- [문서 2] **Financial Report Chunking for Effective Retrieval Augmented Generation** — [초록] Chunking information is a key step in Retrieval Augmented Generation (RAG). Current research primarily centers on paragraph-level chunking. This approach treats all texts as equal and neglects the information contained in the structure of documents. We propose an expanded approach to chunk documents by moving beyond mere paragraph-level chunking to chunk primary by structural element components of documents. Dis
- [문서 3] **Beyond Chunk-Then-Embed: A Comprehensive Taxonomy and Evaluation of Document Chunking Strategies for Information Retrieval** — [초록] Document chunking is a critical preprocessing step in dense retrieval systems, yet the design space of chunking strategies remains poorly understood. Recent research has proposed several concurrent approaches, including LLM-guided methods (e.g., DenseX and LumberChunker) and contextualized strategies(e.g., Late Chunking), which generate embeddings before segmentation to preserve contextual information. However, 
- [문서 4] **HiChunk: Evaluating and Enhancing Retrieval-Augmented Generation with Hierarchical Chunking** — [초록] Retrieval-Augmented Generation (RAG) enhances the response capabilities of language models by integrating external knowledge sources. However, document chunking as an important part of RAG system often lacks effective evaluation tools. This paper first analyzes why existing RAG evaluation benchmarks are inadequate for assessing document chunking quality, specifically due to evidence sparsity. Based on this concl
- [문서 5] **Cross-Document Topic-Aligned Chunking for Retrieval-Augmented Generation** — [초록] Chunking quality determines RAG system performance. Current methods partition documents individually, but complex queries need information scattered across multiple sources: the knowledge fragmentation problem. We introduce Cross-Document Topic-Aligned (CDTA) chunking, which reconstructs knowledge at the corpus level. It first identifies topics across documents, maps segments to each topic, and synthesizes them 

---

## O_09

**질문** LLM을 평가자로 쓰는 연구 중에 꼭 읽어야 할 논문 두 편만 알려줘

- [문서 1] **Towards Understanding the Robustness of LLM-based Evaluations under Perturbations** — [초록] Traditional evaluation metrics like BLEU and ROUGE fall short when capturing the nuanced qualities of generated text, particularly when there is no single ground truth. In this paper, we explore the potential of Large Language Models (LLMs), specifically Google Gemini 1, to serve as automatic evaluators for non-standardized metrics in summarization and dialog-based tasks. We conduct experiments across multiple p
- [문서 2] **An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability** — [초록] As large language models (LLMs) continue to advance, reliable evaluation methods are essential particularly for open-ended, instruction-following tasks. LLM-as-a-Judge enables automatic evaluation using LLMs as evaluators, but its reliability remains uncertain. In this work, we analyze key factors affecting its trustworthiness, focusing on alignment with human judgments and evaluation consistency. Using BIGGENBe
- [문서 3] **Benchmarking Cognitive Biases in Large Language Models as Evaluators** — [초록] Large Language Models are cognitively biased judges. Large Language Models (LLMs) have recently been shown to be effective as automatic evaluators with simple prompting and in-context learning. In this work, we assemble 15 LLMs of four different size ranges and evaluate their output responses by preference ranking from the other LLMs as evaluators, such as System Star is better than System Square. We then evalua
- [문서 4] **Likelihood-based Mitigation of Evaluation Bias in Large Language Models** — [초록] Large Language Models (LLMs) are widely used to evaluate natural language generation tasks as automated metrics. However, the likelihood, a measure of LLM's plausibility for a sentence, can vary due to superficial differences in sentences, such as word order and sentence structure. It is therefore possible that there might be a likelihood bias if LLMs are used for evaluation: they might overrate sentences with h
- [문서 5] **Large Language Models are Inconsistent and Biased Evaluators** — [초록] The zero-shot capability of Large Language Models (LLMs) has enabled highly flexible, reference-free metrics for various tasks, making LLM evaluators common tools in NLP. However, the robustness of these LLM evaluators remains relatively understudied; existing work mainly pursued optimal performance in terms of correlating LLM scores with human expert scores. In this paper, we conduct a series of analyses using 

---

## O_14

**질문** LLM 워터마크 연구 중에 입문용으로 읽을 만한 논문 알려줘

- [문서 1] **RAG-WM: An Efficient Black-Box Watermarking Approach for Retrieval-Augmented Generation of Large Language Models** — [초록] In recent years, tremendous success has been witnessed in Retrieval-Augmented Generation (RAG), widely used to enhance Large Language Models (LLMs) in domain-specific, knowledge-intensive, and privacy-sensitive tasks. However, attackers may steal those valuable RAGs and deploy or commercialize them, making it essential to detect Intellectual Property (IP) infringement. Most existing ownership protection solution
- [문서 2] **Safeguarding Multimodal Knowledge Copyright in the RAG-as-a-Service Environment** — [초록] As Retrieval-Augmented Generation (RAG) evolves into service-oriented platforms (Rag-as-a-Service) with shared knowledge bases, protecting the copyright of contributed data becomes essential. Existing watermarking methods in RAG focus solely on textual knowledge, leaving image knowledge unprotected. In this work, we propose AQUA, the first watermark framework for image knowledge protection in Multimodal RAG syst
- [문서 3] **FedOT: Ownership Verification and Leakage Tracing via Watermarks for Federated LDMs** — [초록] Training Latent Diffusion Models (LDMs) within Federated Learning (FL) has attracted increasing attention due to its ability to combine the powerful generative capacity of LDMs with the privacy-preserving properties of FL. However, FL requires sharing the global model with multiple participants, which risks unauthorized model distribution or resale by malicious clients. While an intuitive approach is to adopt ex
- [문서 4] **Is Your Writing Being Mimicked by AI? Unveiling Imitation with Invisible Watermarks in Creative Writing** — [초록] Efficient knowledge injection methods for Large Language Models (LLMs), such as In-Context Learning, knowledge editing, and efficient parameter fine-tuning, significantly enhance model utility on downstream tasks. However, they also pose substantial risks of unauthorized imitation and compromised data provenance for high-value unstructured data assets like creative works. Current copyright protection methods for
- [문서 5] **RoboSignature: Robust Signature and Watermarking on Network Attacks** — [초록] Generative models have enabled easy creation and generation of images of all kinds given a single prompt. However, this has also raised ethical concerns about what is an actual piece of content created by humans or cameras compared to model-generated content like images or videos. Watermarking data generated by modern generative models is a popular method to provide information on the source of the content. The 

---

## O_16

**질문** KV 캐시 압축 논문 두 편 추천해줘

- [문서 1] **Ablation, Statistical Inference, and Validation for KV-Cache Compression** — [초록] This study systematically compares Turbo-Quant and SpectralQuant KV-cache compression, evaluating non-dominated schemes, including WHT rotation with Beta Lloyd-Max and QJL, through a statistical validation methodology that separates systematic codec differences from implementation variance. Key findings reveal that while eigenbasis-based methods fail on heavy-tailed data due to covariance instability, they excel
- [문서 2] **LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers** — [초록] Compressing the KV cache is a required step to deploy large language models on edge devices. Current quantization methods compress storage but fail to reduce bandwidth as attention calculation requires dequantizing keys from INT4/INT8 to FP16 before use. We observe that attention scoring is mathematically equivalent to the inner product similarity search and we can apply some compression techniques from vector d
- [문서 3] **Rethinking Key-Value Cache Compression Techniques for Large Language Model Serving** — [초록] Key-Value cache (\texttt{KV} \texttt{cache}) compression has emerged as a promising technique to optimize Large Language Model (LLM) serving. It primarily decreases the memory consumption of \texttt{KV} \texttt{cache} to reduce the computation cost. Despite the development of many compression algorithms, their applications in production environments are still not prevalent. In this paper, we revisit mainstream \
- [문서 4] **ReFreeKV: Towards Threshold-Free KV Cache Compression** — [초록] To reduce memory consumption during LLM inference, a handful of methods have been proposed for KV cache pruning. While these techniques can accomplish lossless memory reduction on many datasets, they often hinge on an under-emphasized condition: an input/domain-specific threshold for KV cache budget needs to be pre-determined to achieve the optimal performance. However, such input-sensitive design may be conside
- [문서 5] **DeltaKV: Residual-Based KV Cache Compression via Long-Range Similarity** — [초록] The deployment of efficient long-context LLMs in applications like autonomous agents, long-chain reasoning, and creative writing is fundamentally bottlenecked by the linear growth of KV cache memory. Existing compression and eviction methods often struggle to balance accuracy, compression ratio, and hardware efficiency. We propose DeltaKV, a residual-based KV cache compression framework motivated by two empirica

---

## O_30

**질문** 멀티모달 모델 논문 중 재밌는 거 세 편만 뽑아줘

- [문서 1] **From Efficient Multimodal Models to World Models: A Survey** — [초록] Multimodal Large Models (MLMs) are becoming a significant research focus, combining powerful large language models with multimodal learning to perform complex tasks across different data modalities. This review explores the latest developments and challenges in MLMs, emphasizing their potential in achieving artificial general intelligence and as a pathway to world models. We provide an overview of key techniques
- [문서 2] **Survey of Large Multimodal Model Datasets, Application Categories and Taxonomy** — [초록] Multimodal learning, a rapidly evolving field in artificial intelligence, seeks to construct more versatile and robust systems by integrating and analyzing diverse types of data, including text, images, audio, and video. Inspired by the human ability to assimilate information through many senses, this method enables applications such as text-to-video conversion, visual question answering, and image captioning. R
- [문서 3] **Next Token Prediction Towards Multimodal Intelligence: A Comprehensive Survey** — [초록] Building on the foundations of language modeling in natural language processing, Next Token Prediction (NTP) has evolved into a versatile training objective for machine learning tasks across various modalities, achieving considerable success. As Large Language Models (LLMs) have advanced to unify understanding and generation tasks within the textual modality, recent research has shown that tasks from different m
- [문서 4] **A Survey of Multimodal Retrieval-Augmented Generation** — [초록] Multimodal Retrieval-Augmented Generation (MRAG) enhances large language models (LLMs) by integrating multimodal data (text, images, videos) into retrieval and generation processes, overcoming the limitations of text-only Retrieval-Augmented Generation (RAG). While RAG improves response accuracy by incorporating external textual knowledge, MRAG extends this framework to include multimodal retrieval and generatio
- [문서 5] **Multi-Dimensional Insights: Benchmarking Real-World Personalization in Large Multimodal Models** — [초록] The rapidly developing field of large multimodal models (LMMs) has led to the emergence of diverse models with remarkable capabilities. However, existing benchmarks fail to comprehensively, objectively and accurately evaluate whether LMMs align with the diverse needs of humans in real-world scenarios. To bridge this gap, we propose the Multi-Dimensional Insights (MDI) benchmark, which includes over 500 images co

---

## O_38

**질문** 합성 데이터로 학습하는 연구 중 읽어야 할 논문 두 편

- [문서 1] **Assessing Generative Models for Structured Data** — [초록] Synthetic tabular data generation has emerged as a promising method to address limited data availability and privacy concerns. With the sharp increase in the performance of large language models in recent years, researchers have been interested in applying these models to the generation of tabular data. However, little is known about the quality of the generated tabular data from large language models. The predo
- [문서 2] **Autodata: An agentic data scientist to create high quality synthetic data** — [초록] We introduce Autodata, a general method that enables AI agents to act as data scientists who build high quality training and evaluation data. We show how to train (meta-optimize) such a data scientist agent, so that it learns to create even stronger data. We describe the overall formulation, and a specific practical implementation, Agentic Self-Instruct. We conduct experiments on computer science research tasks,
- [문서 3] **How to Synthesize Text Data without Model Collapse?** — [초록] Model collapse in synthetic data indicates that iterative training on self-generated data leads to a gradual decline in performance. With the proliferation of AI models, synthetic data will fundamentally reshape the web data ecosystem. Future GPT-$\{n\}$ models will inevitably be trained on a blend of synthetic and human-produced data. In this paper, we focus on two questions: what is the impact of synthetic dat
- [문서 4] **Is Synthetic Image Useful for Transfer Learning? An Investigation into Data Generation, Volume, and Utilization** — [초록] Synthetic image data generation represents a promising avenue for training deep learning models, particularly in the realm of transfer learning, where obtaining real images within a specific domain can be prohibitively expensive due to privacy and intellectual property considerations. This work delves into the generation and utilization of synthetic images derived from text-to-image generative models in facilita
- [문서 5] **Data Generation Using Large Language Models for Text Classification: An Empirical Case Study** — [초록] Using Large Language Models (LLMs) to generate synthetic data for model training has become increasingly popular in recent years. While LLMs are capable of producing realistic training data, the effectiveness of data generation is influenced by various factors, including the choice of prompt, task complexity, and the quality, quantity, and diversity of the generated data. In this work, we focus exclusively on us

---

## d0001

**질문** 네 지식 베이스(ChromaDB)에서 최근 AI 논문 아무거나 하나 찾아서 요약해 봐

- [문서 1] **UDA: A Benchmark Suite for Retrieval Augmented Generation in Real-world Document Analysis** — [초록] The use of Retrieval-Augmented Generation (RAG) has improved Large Language Models (LLMs) in collaborating with external data, yet significant challenges exist in real-world scenarios. In areas such as academic literature and finance question answering, data are often found in raw text and tables in HTML or PDF formats, which can be lengthy and highly unstructured. In this paper, we introduce a benchmark suite, 

---

## d0032

**질문** """RAG 검색 정확도 향상(retrieval accuracy), Reranking, Chunking, Hallucination mitigation 관련 최신 논문 찾아줘."""

- [문서 1] **Adaptive Chunking: Optimizing Chunking-Method Selection for RAG** — [초록] The effectiveness of Retrieval-Augmented Generation (RAG) is highly dependent on how documents are chunked, that is, segmented into smaller units for indexing and retrieval. Yet, commonly used "one-size-fits-all" approaches often fail to capture the nuanced structure and semantics of diverse texts. Despite its central role, chunking lacks a dedicated evaluation framework, making it difficult to assess and compar
- [문서 2] **Cross-Document Topic-Aligned Chunking for Retrieval-Augmented Generation** — [초록] Chunking quality determines RAG system performance. Current methods partition documents individually, but complex queries need information scattered across multiple sources: the knowledge fragmentation problem. We introduce Cross-Document Topic-Aligned (CDTA) chunking, which reconstructs knowledge at the corpus level. It first identifies topics across documents, maps segments to each topic, and synthesizes them 
- [문서 3] **Beyond Chunk-Then-Embed: A Comprehensive Taxonomy and Evaluation of Document Chunking Strategies for Information Retrieval** — [초록] Document chunking is a critical preprocessing step in dense retrieval systems, yet the design space of chunking strategies remains poorly understood. Recent research has proposed several concurrent approaches, including LLM-guided methods (e.g., DenseX and LumberChunker) and contextualized strategies(e.g., Late Chunking), which generate embeddings before segmentation to preserve contextual information. However, 
- [문서 4] **A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions** — [초록] The emergence of large language models (LLMs) has marked a significant breakthrough in natural language processing (NLP), fueling a paradigm shift in information acquisition. Nevertheless, LLMs are prone to hallucination, generating plausible yet nonfactual content. This phenomenon raises significant concerns over the reliability of LLMs in real-world information retrieval (IR) systems and has attracted intensiv
- [문서 5] **A Comprehensive Survey of Hallucination Mitigation Techniques in Large Language Models** — [초록] As Large Language Models (LLMs) continue to advance in their ability to write human-like text, a key challenge remains around their tendency to hallucinate generating content that appears factual but is ungrounded. This issue of hallucination is arguably the biggest hindrance to safely deploying these powerful LLMs into real-world production systems that impact people's lives. The journey toward widespread adopt

---

## d0038

**질문** 논문 재밌는것좀 요약해줘

- [문서 1] **The Pitfalls of Publishing in the Age of LLMs: Strange and Surprising Adventures with a High-Impact NLP Journal** — [초록] We show the fraught side of the academic publishing realm and illustrate it through a recent case study with an NLP journal.

. Overall, the paper’s literature review appears to be thorough, covering a wide range of relevant sources. However, the assessment of whether any “significant” work is ignored can be subjective, as it depends on the specific criteria for significance and the scope of the paper. We may ha
- [문서 2] **Large Language Models for Automated Literature Review: An Evaluation of Reference Generation, Abstract Writing, and Review Composition** — [초록] Large language models (LLMs) have emerged as a potential solution to automate the complex processes involved in writing literature reviews, such as literature collection, organization, and summarization. However, it is yet unclear how good LLMs are at automating comprehensive and reliable literature reviews. This study introduces a framework to automatically evaluate the performance of LLMs in three key tasks of
- [문서 3] **Automated Review Generation Method Based on Large Language Models** — [초록] Literature research, vital for scientific work, faces the challenge of surging information volumes exceeding researchers' processing capabilities. We present an automated review generation method based on large language models (LLMs) to overcome efficiency bottlenecks and reduce cognitive load. Our statistically validated evaluation framework demonstrates that the generated reviews match or exceed manual quality
- [문서 4] **A Comparative Study of Quality Evaluation Methods for Text Summarization** — [초록] Evaluating text summarization has been a challenging task in natural language processing (NLP). Automatic metrics which heavily rely on reference summaries are not suitable in many situations, while human evaluation is time-consuming and labor-intensive. To bridge this gap, this paper proposes a novel method based on large language models (LLMs) for evaluating text summarization. We also conducts a comparative s
- [문서 5] **Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems** — [초록] This article provides a comprehensive systematic literature review of academic studies, industrial applications, and real-world deployments from 2018 to 2025, providing a practical guide and detailed overview of modern Retrieval-Augmented Generation (RAG) architectures. RAG offers a modular approach for integrating external knowledge without increasing the capacity of the model as LLM systems expand. Research an

---

## Q_B06

**질문** 논문 검색 봇의 답이 길고 장황하다는 피드백을 받았다. 답변 길이와 사용자 만족도의 관계를 다룬 연구, 그리고 RAG 답변을 간결하게 만드는 방법 연구를 몇 편 추천해줘.

- [문서 1] **From Questions to Insightful Answers: Building an Informed Chatbot for University Resources** — [초록] This paper presents BARKPLUG V.2, a Large Language Model (LLM)-based chatbot system built using Retrieval Augmented Generation (RAG) pipelines to enhance the user experience and access to information within academic settings.The objective of BARKPLUG V.2 is to provide information to users about various campus resources, including academic departments, programs, campus facilities, and student resources at a unive
- [문서 2] **Human-Centered Evaluation of RAG outputs: a framework and questionnaire for human-AI collaboration** — [초록] Retrieval-augmented generation (RAG) systems are increasingly deployed in user-facing applications, yet systematic, human-centered evaluation of their outputs remains underexplored. Building on Gienapp's utility-dimension framework, we designed a human-centred questionnaire that assesses RAG outputs across 12 dimensions. We iteratively refined the questionnaire through several rounds of ratings on a set of query
- [문서 3] **RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems** — [초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical 
- [문서 4] **Evaluation of Retrieval-Augmented Generation: A Survey** — [초록] Retrieval-Augmented Generation (RAG) has recently gained traction in natural language processing. Numerous studies and real-world applications are leveraging its ability to enhance generative models through external information retrieval. Evaluating these RAG systems, however, poses unique challenges due to their hybrid structure and reliance on dynamic knowledge sources. To better understand these challenges, w
- [문서 5] **Beyond Relevance: On the Relationship Between Retrieval and RAG Information Coverage** — [초록] Retrieval-augmented generation (RAG) systems combine document retrieval with a generative model to address complex information seeking tasks like report generation. While the relationship between retrieval quality and generation effectiveness seems intuitive, it has not been systematically studied. We investigate whether upstream retrieval metrics can serve as reliable early indicators of the final generated res

---

## Q_F03

**질문** LLM 안전성 쪽에서 꼭 읽어야 할 논문 세 편만 뽑아줘

- [문서 1] **A Method for Enhancing the Safety of Large Model Generation Based on Multi-dimensional Attack and Defense** — [초록] Currently, large models are prone to generating harmful content when faced with complex attack instructions, significantly reducing their defensive capabilities. To address this issue, this paper proposes a method based on constructing data aligned with multi-dimensional attack defense to enhance the generative security of large models. The core of our method lies in improving the effectiveness of safe alignment
- [문서 2] **Mitigating Adversarial Attacks in LLMs through Defensive Suffix Generation** — [초록] Large language models (LLMs) have exhibited outstanding performance in natural language processing tasks. However, these models remain susceptible to adversarial attacks in which slight input perturbations can lead to harmful or misleading outputs. A gradient-based defensive suffix generation algorithm is designed to bolster the robustness of LLMs. By appending carefully optimized defensive suffixes to input pro
- [문서 3] **Emerging Security Challenges of Large Language Models** — [초록] Large language models (LLMs) have achieved record adoption in a short period of time across many different sectors including high importance areas such as education [4] and healthcare [23]. LLMs are open-ended models trained on diverse data without being tailored for specific downstream tasks, enabling broad applicability across various domains. They are commonly used for text generation, but also widely used to
- [문서 4] **On Adversarial Robustness of Language Models in Transfer Learning** — [초록] We investigate the adversarial robustness of LLMs in transfer learning scenarios. Through comprehensive experiments on multiple datasets (MBIB Hate Speech, MBIB Political Bias, MBIB Gender Bias) and various model architectures (BERT, RoBERTa, GPT-2, Gemma, Phi), we reveal that transfer learning, while improving standard performance metrics, often leads to increased vulnerability to adversarial attacks. Our findi
- [문서 5] **On Adversarial Robustness and Out-of-Distribution Robustness of Large Language Models** — [초록] The increasing reliance on large language models (LLMs) for diverse applications necessitates a thorough understanding of their robustness to adversarial perturbations and out-of-distribution (OOD) inputs. In this study, we investigate the correlation between adversarial robustness and OOD robustness in LLMs, addressing a critical gap in robustness evaluation. By applying methods originally designed to improve o

---

## Q_F04

**질문** 요즘 많이 인용되는 검색 증강 생성 논문 추천해줘

- [문서 1] **A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions** — [초록] This paper presents a comprehensive study of Retrieval-Augmented Generation (RAG), tracing its evolution from foundational concepts to the current state of the art. RAG combines retrieval mechanisms with generative language models to enhance the accuracy of outputs, addressing key limitations of LLMs. The study explores the basic architecture of RAG, focusing on how retrieval and generation are integrated to han
- [문서 2] **Scholarly Question Answering using Large Language Models in the NFDI4DataScience Gateway** — [초록] This paper introduces a scholarly Question Answering (QA) system on top of the NFDI4DataScience Gateway, employing a Retrieval Augmented Generation-based (RAG) approach. The NFDI4DS Gateway, as a foundational framework, offers a unified and intuitive interface for querying various scientific databases using federated search. The RAG-based scholarly QA, powered by a Large Language Model (LLM), facilitates dynamic
- [문서 3] **RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems** — [초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical 
- [문서 4] **Harnessing Retrieval-Augmented Generation (RAG) for Uncovering Knowledge Gaps** — [초록] The paper presents a methodology for uncovering knowledge gaps on the internet using the Retrieval Augmented Generation (RAG) model. By simulating user search behaviour, the RAG system identifies and addresses gaps in information retrieval systems. The study demonstrates the effectiveness of the RAG system in generating relevant suggestions with a consistent accuracy of 93%. The methodology can be applied in var
- [문서 5] **An Analysis of Hyper-Parameter Optimization Methods for Retrieval Augmented Generation** — [초록] Optimizing Retrieval-Augmented Generation (RAG) configurations for specific tasks is a complex and resource-intensive challenge. Motivated by this challenge, frameworks for RAG hyper-parameter optimization (HPO) have recently emerged, yet their effectiveness has not been rigorously benchmarked. To fill this gap, we present a comprehensive study involving five HPO algorithms over five datasets from diverse domain

---

## d0802

**질문** LLM 추론 강화학습 논문 6편 알려줘

- [문서 1] **Survey on Large Language Model-Enhanced Reinforcement Learning: Concept, Taxonomy, and Methods** — [초록] With extensive pre-trained knowledge and high-level general capabilities, large language models (LLMs) emerge as a promising avenue to augment reinforcement learning (RL) in aspects such as multi-task learning, sample efficiency, and high-level task planning. In this survey, we provide a comprehensive review of the existing literature in LLM-enhanced RL and summarize its characteristics compared to conventional 
- [문서 2] **Rethinking Agentic Reinforcement Learning In Large Language Models** — [초록] Reinforcement Learning (RL) has traditionally focused on training specialized agents to optimize predefined reward functions within narrowly defined environments. However, the advent of powerful Large Language Models (LLMs) and increasingly complex, open-ended tasks has catalyzed a paradigm shift towards agentic paradigms within RL. This emerging framework extends beyond traditional RL by emphasizing the develop
- [문서 3] **Learning to Play Blackjack: A Curriculum Learning Perspective** — [초록] Reinforcement Learning (RL) agents often struggle with efficiency and performance in complex environments. We propose a novel framework that uses a Large Language Model (LLM) to dynamically generate a curriculum over available actions, enabling the agent to incorporate each action individually. We apply this framework to the game of Blackjack, where the LLM creates a multi-stage training path that progressively 
- [문서 4] **Online Preference-based Reinforcement Learning with Self-augmented Feedback from Large Language Model** — [초록] Preference-based reinforcement learning (PbRL) provides a powerful paradigm to avoid meticulous reward engineering by learning rewards based on human preferences. However, real-time human feedback is hard to obtain in online tasks. Most work suppose there is a "scripted teacher" that utilizes privileged predefined reward to provide preference feedback. In this paper, we propose a RL Self-augmented Large Language
- [문서 5] **LLM-Gomoku: A Large Language Model-Based System for Strategic Gomoku with Self-Play and Reinforcement Learning** — [초록] In recent years, large language models (LLMs) have shown significant advancements in natural language processing (NLP), with strong capa-bilities in generation, comprehension, and rea-soning. These models have found applications in education, intelligent decision-making, and gaming. However, effectively utilizing LLMs for strategic planning and decision-making in the game of Gomoku remains a challenge. This stud
