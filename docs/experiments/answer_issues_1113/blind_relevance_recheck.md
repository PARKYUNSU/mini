# 관련 없는 문서 다시 보기 — 18 답

질문마다 답 본론에 인용된 문서 전부(제목 · 초록 앞부분)입니다. 어느 그룹인지, 어느 문서가 애매로 표시됐는지는 넣지 않았습니다.

**문서마다 한 줄:** `V07 2412.08392: 관련` / `무관` / `애매` (관련 = 질문 주제에 맞아 소개할 만함, 무관 = 질문과 상관없음)

---

## V01

**질문:** 작은 언어 모델로 추론 능력을 끌어올린 연구 추천해줘

- **2506.10408** Reasoning RAG via System 1 or System 2: A Survey on Reasoning Agentic Retrieval-Augmented Generation for Industry Challenges  
  Retrieval-Augmented Generation (RAG) has emerged as a powerful framework to overcome the knowledge limitations of Large Language Models (LLMs) by integrating external retrieval with language generation. While early RAG systems based on static pipelines have shown effectiveness in well-structured tasks, they struggle in real-world scenarios requiring complex reasoning, dynamic retrieval, and multi-modal integration. To address these challenges, th…

- **2410.13293** SBI-RAG: Enhancing Math Word Problem Solving for Students through Schema-Based Instruction and Retrieval-Augmented Generation  
  Many students struggle with math word problems (MWPs), often finding it difficult to identify key information and select the appropriate mathematical operations. Schema-based instruction (SBI) is an evidence-based strategy that helps students categorize problems based on their structure, improving problem-solving accuracy. Building on this, we propose a Schema-Based Instruction Retrieval-Augmented Generation (SBI-RAG) framework that incorporates …

---

## V02

**질문:** LLM 에이전트 평가 연구들을 바탕으로 앞으로 필요한 벤치마크 3가지를 제안해줘

- **2607.13705** AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities  
  To address this, we introduce AgentCompass, an open-source, lightweight, and extensible infrastructure for evaluating LLM-based agents. AgentCompass organizes the evaluation process around three independent components, namely Benchmark, Harness, and Environment, thereby enabling flexible configurations without requiring the reimplementation of complex execution logic.…

- **2606.22678** RigorBench: Benchmarking Engineering Process Discipline in Autonomous AI Coding Agents  
  We introduce RigorBench, the first benchmark designed to measure process discipline in AI coding agents. Our results show that structured process discipline not only improves process quality scores by an average of 41% but also raises downstream outcome correctness by 17%, providing the first quantitative evidence that how agents code matters as much as what they produce.…

- **2411.15594** A Survey on LLM-as-a-Judge  
  We explore strategies to enhance reliability, including improving consistency, mitigating biases, and adapting to diverse assessme… Additionally, we propose methodologies for evaluating the reliability of LLM-as-a-Judge systems, supported by a novel benchmark designed for this purpose. This survey serves as a foundational reference for researchers and practitioners in this rapidly evolving field.…

- **2503.24047** Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents  
  This survey provides a focused review of the architectures, design, benchmarks, applications, and ethical considerations surrounding LLM-based scientific agents.…

- **2603.11337** RewardHackingAgents: Benchmarking Evaluation Integrity for LLM ML-Engineering Agents  
  We introduce RewardHackingAgents, a workspace-based benchmark that makes two compromise vectors explicit and measurable: evaluator tampering (modifying metric computation or reporting) and train/test leakage (accessing held-out data or labels during training). In natural-agent runs, evaluator-tampering attempts occur in about 50% of episodes and are eliminated by evaluator locking, with a 25-31%……

- **2604.01532** PHMForge: A Scenario-Driven Agentic Benchmark for Industrial Asset Lifecycle Maintenance  
  To address this critical gap, we introduce PHMForge, the first comprehensive benchmark specifically designed to evaluate LLM agents on Prognostics and Health Management (PHM) tasks through realistic interactions with domain-specific MCP servers. Through extensive evaluation of leading frameworks (ReAct, Cursor Agent, Claude Code) paired with frontier LLMs (Claude Sonnet 4.0, GPT-4o, Granite-3.0-……

- **2412.13501** GUI Agents: A Survey  
  We propose a unified framework that delineates their perception, reasoning, planning, and acting capabilities. Finally, this work serves as a basis for practitioners and researchers to gain an intuitive understanding of current progress, techniques, benchmarks, and critical open problems that remain to be addressed.…

---

## V03

**질문:** LLM이 영어 초록을 한국어로 요약할 때 숫자나 부정 표현이 바뀌는 오류가 얼마나 생기는지, 번역·요약 충실도를 잰 연구가 있는가.

- **2604.27920** Beyond Semantics: Measuring Fine-Grained Emotion Preservation in Small Language Model-Based Machine Translation  
  Preserving affective nuance remains a challenge in Machine Translation (MT), where semantic equivalence often takes precedence over emotional fidelity. This paper evaluates the performance of three state-of-the-art Small Language Models (SLMs) -- EuroLLM, Aya Expanse, and Gemma -- in maintaining fine-grained emotions during backtranslation. Using the GoEmotions dataset, which comprises Reddit comments across 28 distinct categories, we assess emot…

- **2503.21393** An evaluation of LLMs and Google Translate for translation of selected Indian languages via sentiment and semantic analyses  
  Large Language models (LLMs) have been prominent for language translation, including low-resource languages. There has been limited study on the assessment of the quality of translations generated by LLMs, including Gemini, GPT, and Google Translate. This study addresses this limitation by using semantic and sentiment analysis of selected LLMs for Indian languages, including Sanskrit, Telugu and Hindi. We select prominent texts (Bhagavad Gita, Ta…

- **2402.13249** TofuEval: Evaluating Hallucinations of LLMs on Topic-Focused Dialogue Summarization  
  Single document news summarization has seen substantial progress on faithfulness in recent years, driven by research on the evaluation of factual consistency, or hallucinations. We ask whether these advances carry over to other text summarization domains. We propose a new evaluation benchmark on topic-focused dialogue summarization, generated by LLMs of varying sizes. We provide binary sentence-level human annotations of the factual consistency o…

---

## V04

**질문:** LLM이 긴 대화에서 앞에서 한 말과 모순되는 답을 하는지 검사하는 연구 있어?

- **2504.00180** Contradiction Detection in RAG Systems: Evaluating LLMs as Context Validators for Improved Information Consistency  
  Retrieval Augmented Generation (RAG) systems have emerged as a powerful method for enhancing large language models (LLMs) with up-to-date information. However, the retrieval step in RAG can sometimes surface documents containing contradictory information, particularly in rapidly evolving domains such as news. These contradictions can significantly impact the performance of LLMs, leading to inconsistent or erroneous outputs. This study addresses t…

- **2402.13249** TofuEval: Evaluating Hallucinations of LLMs on Topic-Focused Dialogue Summarization  
  Single document news summarization has seen substantial progress on faithfulness in recent years, driven by research on the evaluation of factual consistency, or hallucinations. We ask whether these advances carry over to other text summarization domains. We propose a new evaluation benchmark on topic-focused dialogue summarization, generated by LLMs of varying sizes. We provide binary sentence-level human annotations of the factual consistency o…

- **2606.06748** Evidence Graph Consistency in Retrieval-Augmented Generation: A Model-Dependent Analysis of Hallucination Detection  
  Retrieval-Augmented Generation (RAG) reduces but does not eliminate hallucination in large language models. Existing detection methods rely on flat similarity between generated answers and retrieved passages, ignoring structural relationships among evidence pieces and answer claims. We propose Evidence Graph Consistency (EGC), a framework that constructs a local evidence graph per response and computes five structural consistency measures as hall…

- **2601.06519** MedRAGChecker: Claim-Level Verification for Biomedical Retrieval-Augmented Generation  
  Biomedical retrieval-augmented generation (RAG) can ground LLM answers in medical literature, yet long-form outputs often contain isolated unsupported or contradictory claims with safety implications. We introduce MedRAGChecker, a claim-level verification and diagnostic framework for biomedical RAG. Given a question, retrieved evidence, and a generated answer, MedRAGChecker decomposes the answer into atomic claims and estimates claim support by c…

---

## V05

**질문:** 고대 문자 해독하는 AI 연구 읽을 만한 거

- **2407.12013** Dating ancient manuscripts using radiocarbon and AI-based writing style analysis  
  Determining the chronology of ancient handwritten manuscripts is essential for reconstructing the evolution of ideas. For the Dead Sea Scrolls, this is particularly important. However, there is an almost complete lack of date-bearing manuscripts evenly distributed across the timeline and written in similar scripts available for palaeographic comparison. Here, we present Enoch, a state-of-the-art AI-based date-prediction model, trained on the basi…

- **2607.06374** VaseMuseum: Digital Intelligent Museum for Ancient Greek Pottery  
  Vision-language models (VLMs) have made interactive digital museums increasingly feasible by connecting 3D digitization with natural-language artifact exploration. However, in cultural heritage domains such as ancient Greek pottery, reliable VLM assistance is limited by two challenges. First, open-ended interpretation requires grounding fine-grained 2D/3D visual evidence in specialized curatorial knowledge, yet the retrieval process may introduce…

- **2503.21074** Rerouting Connection: Hybrid Computer Vision Analysis Reveals Visual Similarity Between Indus and Tibetan-Yi Corridor Writing Systems  
  This thesis employs a hybrid CNN-Transformer architecture, alongside a detailed anthropological framework, to investigate potential historical connections between the visual morphology of the Indus Valley script and pictographic systems of the Tibetan-Yi Corridor. Through an ensemble methodology of three target scripts across 15 independently trained models, we demonstrate that Tibetan-Yi Corridor scripts exhibit approximately six-fold higher vis…

---

## V06

**질문:** 소형 언어 모델 성능 끌어올리는 연구 추천 좀

- **2412.09990** Small Language Model as Data Prospector for Large Language Model  
  The quality of instruction data directly affects the performance of fine-tuned Large Language Models (LLMs). Previously, \cite{li2023one} proposed \texttt{NUGGETS}, which identifies and selects high-quality quality data from a large dataset by identifying those individual instruction examples that can significantly improve the performance of different tasks after being learnt as one-shot instances. In this work, we propose \texttt{SuperNUGGETS}, …

- **2409.15790** Small Language Models: Survey, Measurements, and Insights  
  Small language models (SLMs), despite their widespread adoption in modern smart devices, have received significantly less academic attention compared to their large language model (LLM) counterparts, which are predominantly deployed in data centers and cloud environments. While researchers continue to improve the capabilities of LLMs in the pursuit of artificial general intelligence, SLM research aims to make machine intelligence more accessible,…

- **2203.15556** Training Compute-Optimal Large Language Models  
  We investigate the optimal model size and number of tokens for training a transformer language model under a given compute budget. We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models whilst keeping the amount of training data constant. By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find tha…

---

## V07

**질문:** LLM이 만든 코드를 실행해 보고 오류 메시지를 보고 스스로 고치는 방법 다룬 논문 있어?

- **2604.04324** RESCORE: LLM-Driven Simulation Recovery in Control Systems Research Papers  
  Reconstructing numerical simulations from control systems research papers is often hindered by underspecified parameters and ambiguous implementation details. We define the task of Paper to Simulation Recoverability, the ability of an automated system to generate executable code that faithfully reproduces a paper's results. We curate a benchmark of 500 papers from the IEEE Conference on Decision and Control (CDC) and propose RESCORE, a three comp…

- **2412.11014** CoopetitiveV: Leveraging LLM-powered Coopetitive Multi-Agent Prompting for High-quality Verilog Generation  
  Recent advances in agentic LLMs have demonstrated great capabilities in Verilog code generation. However, existing approaches either use LLM-assisted single-agent prompting or cooperation-only multi-agent learning, which will lead to: (i) Degeneration issue for single-agent learning: characterized by diminished error detection and correction capabilities; (ii) Error propagation in cooperation-only multi-agent learning: erroneous information from …

---

## V08

**질문:** 사내 문서 검색 챗봇 만들 때 참고할 만한 논문 세 편 추천해줘

- **2601.07838** A survey: Information search time optimization based on RAG (Retrieval Augmentation Generation) chatbot  
  Retrieval-Augmented Generation (RAG) based chatbots are not only useful for information retrieval through questionanswering but also for making complex decisions based on injected private data.we present a survey on how much search time can be saved when retrieving complex information within an organization called "X Systems"(a stealth mode company) by using a RAG-based chatbot compared to traditional search methods. We compare the information re…

- **2602.17856** Enhancing Scientific Literature Chatbots with Retrieval-Augmented Generation: A Performance Evaluation of Vector and Graph-Based Systems  
  This paper investigates the enhancement of scientific literature chatbots through retrieval-augmented generation (RAG), with a focus on evaluating vector- and graph-based retrieval systems. The proposed chatbot leverages both structured (graph) and unstructured (vector) databases to access scientific articles and gray literature, enabling efficient triage of sources according to research objectives. To systematically assess performance, we examin…

- **2408.08925** Retail-GPT: leveraging Retrieval Augmented Generation (RAG) for building E-commerce Chat Assistants  
  This work presents Retail-GPT, an open-source RAG-based chatbot designed to enhance user engagement in retail e-commerce by guiding users through product recommendations and assisting with cart operations. The system is cross-platform and adaptable to various e-commerce domains, avoiding reliance on specific chat applications or commercial activities. Retail-GPT engages in human-like conversations, interprets user demands, checks product availabi…

---

## V09

**질문:** LLM 답변에 성별이나 인종 편향이 있는지 측정하는 벤치마크 연구 알려줘

- **2503.24310** BEATS: Bias Evaluation and Assessment Test Suite for Large Language Models  
  In this research, we introduce BEATS, a novel framework for evaluating Bias, Ethics, Fairness, and Factuality in Large Language Models (LLMs). Building upon the BEATS framework, we present a bias benchmark for LLMs that measure performance across 29 distinct metrics. These metrics span a broad range of characteristics, including demographic, cognitive, and social biases, as well as measures of ethical reasoning, group fairness, and factuality rel…

- **2402.10669** Humans or LLMs as the Judge? A Study on Judgement Biases  
  Adopting human and large language models (LLM) as judges (a.k.a human- and LLM-as-a-judge) for evaluating the performance of LLMs has recently gained attention. Nonetheless, this approach concurrently introduces potential biases from human and LLMs, questioning the reliability of the evaluation results. In this paper, we propose a novel framework that is free from referencing groundtruth annotations for investigating Misinformation Oversight Bias…

---

## V10

**질문:** 2025년에 나온 딥 리서치(검색 에이전트) 연구들 정리해줘

- **2604.07720** Towards Knowledgeable Deep Research: Framework and Benchmark  
  Furthermore, we propose the Hybrid Knowledge Analysis framework (HKA), a multi-agent architecture that reasons over both kinds of knowledge and integrates the texts, figures, and tables into coherent multimodal reports. Finally, we hope this work can serve as a new foundation for structured knowledge analysis in DR agents and facilitate future multimodal DR studies.…

- **2603.22376** AI Co-Scientist for Ranking: Discovering Novel Search Ranking Models alongside LLM-based AI Agents with Cloud Computing Access  
  In this paper, we present an AI Co-Scientist framework that automates the full search ranking research pipeline: from idea generation to code implementation and GPU training job scheduling with expert in the loop. Our findings suggest that AI systems can discover ranking architectures comparable to those developed by human experts while significantly reducing routine research workloads.…

- **2605.26081** VeriTrace: Evolving Mental Models for Deep Research Agents  
  Using matched Qwen3.5-27B backbones, VeriTrace improves over the strongest matched baseline by 4.22 pp on DeepResearch Bench (DRB) Insight (1.49 pp Overall) and by 5.9 pp Overall win rate on DeepConsult. With Config-DeepSeek, it achieves the strongest reproducible open-source result on DRB.…

- **2607.22375** IDEAgent: Agentic Quality-Diversity Search for Research Idea Generation  
  In line with this perspective, we introduce IDEAgent, a multi-agent framework that manages the evolution of ideas through lineages. Finally, through evaluations across 32 topics spanning 8 domains of Computer Science, we show that IDEAgent outperforms the best baseline by 3.89x on Yield, while achieving non-zero Yield on 8x more topics.…

- **2610.30181** Deep Search in Real-World Web Environments  
  To address this gap, we introduce the OpenDS task, designed to evaluate agents' ability to perform multi-step deep search in the live, open Web. The best-performing model achieves 39.0% accuracy, while human evaluation across 1,000 independent attempts yields 21.1% accuracy. Further analyses of tool usage, search cost, termination behavior, and failure recovery reveal substantial differences in……

- **2605.04036** OpenSeeker-v2: Pushing the Limits of Search Agents with Informative and High-Difficulty Trajectories  
  Trained on merely 10.6k data points, our OpenSeeker-v2 achieves state-of-the-art performance across 4 benchmarks (30B-sized agents with ReAct paradigm): 46.0% on BrowseComp, 58.1% on BrowseComp-ZH, 34.6% on Humanity's Last Exam, and 78.0% on xbench, surpassing even Tongyi DeepResearch trained with heavy CPT+SFT+RL pipeline, which achieves 43.4%, 46.7%, 32.9%, and 75.0%, respectively.…

- **2606.02060** Where Do Deep-Research Agents Go Wrong? Span-Level Error Localization in Agent Trajectories  
  From these annotations, we build TELBench, a 1,000-instance benchmark for identifying error spans among normal exploration, failed searches, tentative hypotheses, and harmless noise. Experiments across model families and auditing frameworks show that DRIFT improves span-level error localization and first-error accuracy by up to 30 percentage points.…

- **2606.15345** Beyond Monolingual Deep Research: Evaluating Agents and Retrievers with Cross-Lingual BrowseComp-Plus  
  We introduce XBCP (Cross-lingual BrowseComp-Plus), a controlled benchmark that preserves the English question-and-answer space of BrowseComp-Plus but varies the languages of the supporting documents. These findings suggest that cross-lingual deep research exposes both retrieval failures and an independent, agent-side difficulty in integrating language-mismatched evidence.…

- **2607.13705** AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities  
  To address this, we introduce AgentCompass, an open-source, lightweight, and extensible infrastructure for evaluating LLM-based agents. AgentCompass organizes the evaluation process around three independent components, namely Benchmark, Harness, and Environment, thereby enabling flexible configurations without requiring the reimplementation of complex execution logic.…

- **2606.09730** SearchSwarm: Towards Delegation Intelligence in Agentic LLMs for Long-Horizon Deep Research  
  To bridge this gap, we present a preliminary exploration targeting deep research, a representative long-horizon agent task. Our resulting model, SearchSwarm-30B-A3B, achieves 68.1 on BrowseComp and 73.3 on BrowseComp-ZH, the best results among all models of comparable scale.…

---

## V11

**질문:** 교육 분야에서 LLM을 튜터로 쓴 연구들 정리해줘

- **2412.11995** Combining Large Language Models with Tutoring System Intelligence: A Case Study in Caregiver Homework Support  
  We developed a system that provides instructional support to caregivers through conversational recommendations generated by a Large Language Model (LLM). Addressing known instructional limitations of LLMs, we use instructional intelligence from tutoring systems while conducting prompt engineering experiments with the open-source Llama 3 LLM.…

- **2412.11255** Do Tutors Learn from Equity Training and Can Generative AI Assess It?  
  We find marginally significant learning gains with increases in tutors' self-reported confidence in their knowledge in responding to middle school students experiencing possible inequities from pretest to posttest. Both GPT-4o and GPT-4-turbo demonstrate proficiency in assessing tutors ability to predict and explain the best approach.…

- **2412.08430** Assessing Personalized AI Mentoring with Large Language Models in the Computing Field  
  The analysis of survey responses shows that GPT-4 outperformed the other two LLMs in delivering more accurate and useful mentoring while addressing specific challenges with encouragement languages. Our work establishes a foundation for developing personalized mentoring tools based on LLMs, incorporating human mentors in the process to deliver a more impactful and tailored mentoring experience.…

- **2410.13293** SBI-RAG: Enhancing Math Word Problem Solving for Students through Schema-Based Instruction and Retrieval-Augmented Generation  
  Building on this, we propose a Schema-Based Instruction Retrieval-Augmented Generation (SBI-RAG) framework that incorporates a large language model (LLM). Our findings suggest that SBI-RAG enhances reasoning clarity and facilitates a more structured problem-solving process potentially providing educational benefits for students.…

- **2610.40563** Comparing Human Role-Players and LLM-Simulated Clients in Online Counselling Training: An Analysis of Counselling Patterns  
  Initially, we recorded role-playing sessions, where novice counsellors interacted with human peers acting as clients, followed by role-plays between humans a… We investigated two key questions: (1) to what extent LLM-generated responses replicate authentic conversational dynamics and (2) whether counsellors' communication behaviour differs when interacting with human versus LLM-simulated clients.…

- **2405.06681** Leveraging Lecture Content for Improved Feedback: Explorations with GPT-4 and Retrieval Augmented Generation  
  This paper presents the use of Retrieval Augmented Generation (RAG) to improve the feedback generated by Large Language Models for programming tasks. First results based on a questionnaire and the collected usage data show that the use of RAG can improve feedback generation and is preferred by students in some… Due to the slower speed of feedback generation, the benefits are situation dependent.…

- **2406.07796** Battling Botpoop using GenAI for Higher Education: A Study of a Retrieval Augmented Generation Chatbots Impact on Learning  
  This study introduces Professor Leodar, a custom-built, Singlish-speaking Retrieval Augmented Generation (RAG) chatbot designed to enhance educational while reducing Botpoop. Through a mixed-methods approach, we examine the impact of Professor Leodar on learning, engagement, and exam preparedness, with 97.1% of participants reporting positive experiences.…

---

## V12

**질문:** LLM 에이전트가 위험한 행동을 하지 않게 막는 안전성 연구들 정리해줘

- **2412.17686** Large Language Model Safety: A Holistic Survey  
  Our findings underscore the necessity for a proactive, multifaceted approach to LLM safety, emphasizing the integration of technical solutions, ethical cons… This survey is intended to serve as a foundational resource for academy researchers, industry practitioners, and policymakers, offering insights into the challenges and opportunities associated with the safe integration of LLMs into society.…

- **2608.14590** Toward Safe LLM Agents: A Survey of Specification, Verification, and Enforcement  
  Second, runtime monitoring is the most mature enforcement strategy, reducing unsafe actions by 40% to 65% in controlled settings, but it does not provide complete safety guarantees. Third, the verifier tax shows that blocking 94% of unsafe actions can still result in less than 5% safe task completion because agents exploit alternative unsafe paths.…

- **2604.00249** A Safety-Aware Role-Orchestrated Multi-Agent LLM Framework for Behavioral Health Communication Simulation  
  We propose a safety-aware, role-orchestrated multi-agent LLM framework designed to simulate supportive behavioral health dialogue through coordinated, role-differentiated agents. Using semi-structured interview transcripts from the DAIC-WOZ corpus, we evaluate the framework with scalable proxy metrics capturing structural quality, functional diversity, and computational characteristics.…

- **2502.10486** VLM-Guard: Safeguarding Vision-Language Models via Fulfilling Safety Alignment Gap  
  To avoid safety decay and fulfill the safety alignment gap, we propose VLM-Guard, an inference-time intervention strategy that leverages the LLM component of a VLM as supervision for the safety alignment of the VLM. Experimental results on three malicious instruction settings show the effectiveness of VLM-Guard in safeguarding VLM and fulfilling the safety alignment gap between VLM and its LLM c……

- **2603.20320** The Causal Impact of Tool Affordance on Safety Alignment in LLM Agents  
  Both evaluated models maintain perfect compliance in text-only settings, yet exhibit sharp increases in violations after tool access is introduced, reaching rates up to 85% despite unchanged rules. These results demonstrate that tool affordance acts as a primary driver of safety misalignment and that text-based evaluation alone is insufficient for assessing agentic systems.…

- **2606.22673** Agent MechSuits: Mechanistic Subspace Safety Steering for Multi-Turn CLI Agents  
  We propose Agent MechSuits (Mechanistic Subspace Intervention and Steering), a white-box defense framework that performs runtime safety detection and representation-level mitigation for CLI agents. Extensive experiments show that Agent MechSuits achieves strong safety detection performance, provides preliminary evidence for lookahead risk anticipation, and substantially reduces harmful actions o……

- **2603.16734** Differential Harm Propensity in Personalized LLM Agents: The Curious Case of Mental Health Disclosure  
  Adding a bio-only context generally reduces harm scores and increases refusals. Importantly, the refusal increase also appears on benign tasks, indicating a safety--utility trade-off via over-refusal. Finally, jailbreak prompting sharply elevates harm relative to benign conditions and can weaken or override the protective shift induced by personalization.…

- **2610.40516** How I Aligned Your Model: Scaling Up Multilingual Safety Training with Templates  
  We propose a scalable template-based augmentation pipeline to produce massive multilingual refusal and benign corpora, extracting safe templates from harmful prompts, translating them and then filling in the slots with culturally authentic entities, both harmful and benign. We also confirm that augmenting safety training data through templates allows for higher diversity and quality of alignment……

- **2412.16339** Deliberative Alignment: Reasoning Enables Safer Language Models  
  We introduce Deliberative Alignment, a new paradigm that directly teaches the model safety specifications and trains it to explicitly recall and accurately reason over the specifications before answering. We demonstrate that reasoning over explicitly specified policies enables more scalable, trustworthy, and interpretable alignment.…

---

## V13

**질문:** LLM으로 수학 증명을 자동으로 하는 연구 5개 찾아줘

- **2412.14063** Rango: Adaptive Retrieval-Augmented Proving for Automated Software Verification  
  We present Rango, a fully automated proof synthesis tool for Coq that automatically identifies relevant premises and also similar proofs from the current project and uses them during synthesis. Our evaluation also shows that Rango adding relevant proofs to its context leads to a 47% increase in the number of theorems proven.…

- **2605.22763** Advancing Mathematics Research with AI-Driven Formal Proof Search  
  These findings demonstrate the power of AI-aided formal proof search and shed light on the agent designs that enable it.…

- **2607.11849** AdvancedMathBench: A Benchmark Suite for Advanced Mathematical Proof Generation and Verification  
  To bridge this gap, we introduce AdvancedMathBench, a benchmark suite designed to evaluate the reasoning capabilities of LLMs on advanced mathematical proofs. On proof generation, the best-performing model, GPT-5.5-xhigh, achieves only 64.5 and 48.9 on the UG and QE splits, respectiv… Further analysis reveals a notable mismatch between proof generation and verification capabilities across models.…

- **2501.00059** Large Language Models for Mathematical Analysis  
  We developed the DEMI-MathAnalysis dataset, comprising proof-based problems from mathematical analysis topics such as Sequences and Limits, Infinite Series, and Convex Functions. Through fine-tuning LLMs on this dataset and employing our framework, we observed significant improvements in their capability to generate logical, complete, and elegant proofs.…

- **2412.16075** Formal Mathematical Reasoning: A New Frontier in AI  
  Extensive efforts on AI4Math have mirrored techniques in NLP, in particular, training large language models on carefully curated math datasets in text form. However, significant challenges remain to be solved for AI to truly master mathematics and achieve broader impact.…

---

## V14

**질문:** 추론 모델을 강화학습으로 학습시키는 좋은 논문 추천해줘

- **2503.20139** Look Before Leap: Look-Ahead Planning with Uncertainty in Reinforcement Learning  
  Model-based reinforcement learning (MBRL) has demonstrated superior sample efficiency compared to model-free reinforcement learning (MFRL). However, the presence of inaccurate models can introduce biases during policy learning, resulting in misleading trajectories. The challenge lies in obtaining accurate models due to limited diverse training data, particularly in regions with limited visits (uncertain regions). Existing approaches passively qua…

- **2603.08706** Agentic Critical Training  
  Training large language models (LLMs) as autonomous agents often begins with imitation learning, but it only teaches agents what to do without understanding why: agents never contrast successful actions against suboptimal alternatives and thus lack awareness of action quality. Recent approaches attempt to address this by introducing self-reflection supervision derived from contrasts between expert and alternative actions. However, the training pa…

---

## V15

**질문:** LLM이 답을 생성하는 도중에 확신이 낮아지면 그때 검색을 다시 하는 연구 알려줘

- **2405.18727** CtrlA: Adaptive Retrieval-Augmented Generation via Inherent Control  
  Retrieval-augmented generation (RAG) has emerged as a promising solution for mitigating hallucinations of large language models (LLMs) with retrieved external knowledge. Adaptive RAG enhances this approach by enabling dynamic retrieval during generation, activating retrieval only when the query exceeds LLM's internal knowledge. Existing methods primarily focus on detecting LLM's confidence via statistical uncertainty. Instead, we present the firs…

- **2602.13571** LLM-Confidence Reranker: A Training-Free Approach for Enhancing Retrieval-Augmented Generation Systems  
  Large language models (LLMs) have revolutionized natural language processing, yet hallucinations in knowledge-intensive tasks remain a critical challenge. Retrieval-augmented generation (RAG) addresses this by integrating external knowledge, but its efficacy depends on accurate document retrieval and ranking. Although existing rerankers demonstrate effectiveness, they frequently necessitate specialized training, impose substantial computational e…

- **2511.10621** SSR: Socratic Self-Refine for Large Language Model Reasoning  
  Large Language Models (LLMs) have demonstrated remarkable reasoning abilities, yet existing test-time frameworks often rely on coarse self-verification and self-correction, limiting their effectiveness on complex tasks. In this paper, we propose Socratic Self-Refine (SSR), a novel framework for fine-grained evaluation and precise refinement of LLM reasoning. Our proposed SSR decomposes model responses into verifiable (sub-question, sub-answer) pa…

---

## V16

**질문:** 임베딩 벡터를 양자화하면 검색 성능이 얼마나 떨어져?

- **2503.19868** GENIUS: A Generative Framework for Universal Multimodal Search  
  Generative retrieval is an emerging approach in information retrieval that generates identifiers (IDs) of target data based on a query, providing an efficient alternative to traditional embedding-based retrieval methods. However, existing models are task-specific and fall short of embedding-based retrieval in performance. This paper proposes GENIUS, a universal generative retrieval framework supporting diverse tasks across multiple modalities and…

- **1612.03651** FastText.zip: Compressing text classification models  
  We consider the problem of producing compact architectures for text classification, such that the full model fits in a limited amount of memory. After considering different solutions inspired by the hashing literature, we propose a method built upon product quantization to store word embeddings. While the original technique leads to a loss in accuracy, we adapt this method to circumvent quantization artefacts. Our experiments carried out on sever…

- **2605.19972** Block-Sphere Vector Quantization  
  Vector quantization is a fundamental primitive for scalable machine learning systems, enabling memory-efficient storage, fast retrieval, and compressed inference. Recent rotation-based quantizers such as EDEN, RabitQ, and TurboQuant have introduced strong guarantees and empirical performance, but the surrounding comparisons have been difficult to interpret because they rely on different distortion criteria, probability regimes, and implementation…

---

## V17

**질문:** 지식 증류로 작은 모델 만드는 최신 논문 추천해줘

- **2412.09388** All You Need in Knowledge Distillation Is a Tailored Coordinate System  
  Knowledge Distillation (KD) is essential in transferring dark knowledge from a large teacher to a small student network, such that the student can be much more efficient than the teacher but with comparable accuracy. Existing KD methods, however, rely on a large teacher trained specifically for the target task, which is both very inflexible and inefficient. In this paper, we argue that a SSL-pretrained model can effectively act as the teacher and…

- **2209.07521** On-Device Domain Generalization  
  We present a systematic study of domain generalization (DG) for tiny neural networks. This problem is critical to on-device machine learning applications but has been overlooked in the literature where research has been merely focused on large models. Tiny neural networks have much fewer parameters and lower complexity and therefore should not be trained the same way as their large counterparts for DG applications. By conducting extensive experim…

- **2607.22629** Masked Self-Distillation: Internalizing the Chain-of-Thought in Language Models  
  Large Reasoning Models produce long, explicit chains of intermediate steps before generating a final answer at inference time. These intermediate traces dominate latency, memory usage, and serving cost, even though final answer correctness is not causally related to the trace correctness and the trace length is not a reliable indicator of the problem complexity. This raises an obvious question: can the computation expressed in these intermediate …

- **2412.13943** On Explaining Knowledge Distillation: Measuring and Visualising the Knowledge Transfer Process  
  Knowledge distillation (KD) remains challenging due to the opaque nature of the knowledge transfer process from a Teacher to a Student, making it difficult to address certain issues related to KD. To address this, we proposed UniCAM, a novel gradient-based visual explanation method, which effectively interprets the knowledge learned during KD. Our experimental results demonstrate that with the guidance of the Teacher's knowledge, the Student mode…

---

## V18

**질문:** LLM으로 소프트웨어 버그를 찾는 연구들 정리해줘

- **2606.29088** Diff-Based Code Corruption using LLMs for Large-Scale Bugfix Benchmarking  
  To address these issues, we introduce MegaBugFix, a large-scale bugfixing benchmark containing 12,629 buggy Python programs synthesized from correct ones by a Large Language Model. This reveals that our benchmark presents more challenging bugs and exposes model failures that may remain hidden when evaluating on existing benchmarks.…

- **2412.14137** Design choices made by LLM-based test generators prevent them from finding bugs  
  Using real human-written buggy code as input, we evaluate these tools, showing how LLM-generated tests can fail to detect bugs and, more alarmingly, how their design can worsen the situation by validating bugs in the gen… These findings raise important questions about the validity of the design behind LLM-based test generation tools and their impact on software quality and test suite reliability.…

- **2601.00254** An Empirical Evaluation of LLM-Based Approaches for Code Vulnerability Detection: RAG, SFT, and Dual-Agent Systems  
  This paper presents a comparative study on the effectiveness of LLM-based techniques for detecting software vulnerabilities. Our RAG approach, which integrated external domain knowledge from the internet and the MITRE CWE database, achieved the highest overall accuracy (0.86) and F1 score (0.85), highlighting the value of contextual augmentation.…

- **2412.18750** Order Matters! An Empirical Study on Large Language Models' Input Order Bias in Software Fault Localization  
  Breaking down inputs into smaller contexts helps reduce this bias, narrowing the performance gap in FL from 22% to 6% and then to just 1% on both benchmarks. Ordering using DepGraph's ranking achieves 48% Top-1 accuracy, which is better than more straightforward ordering approaches like CallGraphDFS.…

- **2508.02611** Meta-RAG on Large Codebases Using Code Summarization  
  In this paper, we propose a multi-agent system to localize bugs in large pre-existing codebases using information retrieval and LLMs. We demonstrate the usefulness of Meta-RAG through evaluation with the SWE-bench Lite dataset. Meta-RAG scores 84.67 % and 53.0 % for file-level and function-level correct localization rates, respectively, achieving state-of-the-art performance.…
