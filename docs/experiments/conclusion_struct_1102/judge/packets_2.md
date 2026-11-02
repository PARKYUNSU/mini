# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)

## H_A16 — 에이전트가 웹 브라우저를 직접 조작해서 과제를 푸는 벤치마크 연구 있어?

### 인용 블록

[문서 1]
[Distance: 0.2959]
[발행일: 2026-06-12]
[2606.14397v5] Running the Gauntlet: Hard Agentic Tasks
[초록] As agentic systems continue to evolve and are widely deployed in real-world scenarios, there is a growing demand to faithfully evaluate their capabilities. However, current benchmarks are typically built on popular applications with relatively simple tasks and focus on a narrow set of capabilities while overlooking broader dimensions, resulting in saturated performance on modern agents and failing to probe their limitations. To this end, we introduce GauntletBench, a web-based benchmark for evaluating agent generalisation in challenging scenarios, focusing on three underexplored capabilities (temporal perception, graphical understanding, and 3D reasoning), across five less-covered professional applications (Video Editor, Workflow Builder, 3D Modeller, Flight Analyser, and Circuit Designer), each with 27 vision-intensive tasks (135 in total). Our benchmark provides a modular pipeline that comprises an environment compatible with both open- and closed-source agent frameworks, a controlled web-based application, a well-structured task suite, and an automated evaluation engine with diverse metrics. Contrary to widespread expectations, our empirical results reveal that frontier agentic systems remain far from achieving human-level performance. Even the state-of-the-art agent achieves only a 28.2% success rate on our GauntletBench, highlighting the limitations in these overlooked capabilities and generalisation. By comparison, non-expert human annotators achieve over 80% success on our challenging yet feasible tasks, revealing the substantial gap between current agent capabilities and those required for complex real-world scenarios.

**Web Agent Benchmarks** A growing number of work has focused on evaluating autonomous agents in web-based environments. Early benchmarks such as MiniWoB [39] and MiniWoB++ [24] introduced simplified web interaction tasks where agents had to perform basic operations like clicking buttons, filling forms, and navigating menus. While these benchmarks were instrumental in establishing the field, they relied on synthetic, toy-like interfaces that did not capture the complexity of real websites
[문서 2]
[Distance: 0.2702]
[발행일: 2026-06-16]
[2606.20724v2] When Web Agents Finish but Still Fail: Reproducible Triggers and Trace Diagnostics for Parallel Web Exploration
[초록] Long-horizon web agents often fail in ways hidden by final-answer evaluation: they may visit useful pages, produce a well-formed answer, and terminate confidently while still missing fields, over-including unsupported items, or relying on stale evidence. We study these failures with Parallel WebBench, a parallel web-exploration benchmark containing 1,679 verified records: 350 manually curated parallel tasks and 1,329 reconstructed records with verified URL-based trajectories. We train WebExplorer-style agents with GRPO under human-only, balanced human-synthetic, and synthetic-heavy data mixtures. At 16k context and 16 interaction rounds, the best GRPO model improves completion over WebExplorer-8B from 50.7% to 96.0% and GPT-4.1-mini-judged element-wise F1 from 0.2489 to 0.4529, but binary accuracy remains far below completion. Trace-level analysis identifies three persistent failure modes: context-bound search loops, premature termination on partial answers, and synthesis collapse after relevant evidence has already been retrieved. These results show that synthetic-data GRPO reduces abstention and improves partial correctness, but leaves a completion-correctness gap that requires evidence-grounded coverage and synthesis diagnostics.

## **2. Related Work**

**Web agent benchmarks.** Prior web-agent benchmarks evaluate agents in simulated web environments, shopping tasks, realistic browser environments, enterprise software, multimodal web tasks, live websites, and general instructionfollowing settings (Yao et al., 2022; Deng et al., 2023; Zhou et al., 2023; Koh et al., 2024; Drouin et al., 2024; Lu et al.` , 2024; Zheng et al., 2024a; He et al., 2024; Liu et al., 2024; Xie et al., 2024; Zheng et al., 2024b)
[문서 3]
[Distance: 0.3467]
[발행일: 2026-06-01]
[2606.02404v1] K-BrowseComp: A Web Browsing Agent Benchmark Grounded in Korean Contexts
[초록] Frontier model evaluations are shifting from foundational capabilities (e.g., instruction following and reasoning) toward compositional, agentic ones, but Korean agentic benchmarks remain scarce. We introduce K-BrowseComp, a web-browsing agent benchmark grounded in Korean contexts, consisting of 400 problems. The 300-problem K-BrowseComp-Verified subset is manually constructed and validated by native Korean speakers. On this subset, frontier LLMs, including GPT-5.5, DeepSeek-V4-Pro, and GLM-5.1, reach only 30.00--45.67\%, a substantial drop from BrowseComp, while Korean LLMs released through Korea's Proprietary AI Foundation Model program obtain only 0.00--10.33\%. We further construct a 100-problem synthetic split using hard few-shot exemplars and failure-mode-targeted generation to exploit the asymmetry between solving and creating web browsing problems. On the adversarially filtered synthetic diagnostic split, the strongest model reaches only 26.00\%, and we report this split separately as a targeted stress test. We publicly release our data and code.

. We position K-BROWSECOMP as a shared diagnostic target to encourage prioritization of browsing-agent capabilities alongside static-benchmark performance.

### 문장

- s1: [2606.14397v5]은 GauntletBench를 통해 현재 에이전트의 성능이 제한적임을, [2606.20724v2]는 Parallel WebBench에서 모델의 완성도와 정확성 간 격차를 확인하고, [2606.02404v1]은 K-BrowseComp를 통해 한국어 컨텍스트에서의 에이전트 성능을 평가했습니다.
- s2: 이를 위해 이 논문은 어려운 시나리오에서 에이전트의 일반화 능력을 평가하기 위한 웹 기반 벤치마크인 GauntletBench를 소개하며, 시간적 지각, 그래픽 이해, 3D 추론이라는 세 가지 덜 탐구된 능력과 비디오 편집기, 워크플로우 빌더, 3D 모델러, 비행 분석기, 회로 설계기라는 다섯 가지 덜 다루어진 전문 응용 분야를 대상으로 각각 27개의 시각 집중형 작업(총 135개)을 포함한다. [2606.14397v5]
- s3: Parallel WebBench라는 병렬 웹 탐색 벤치마크를 사용하여 이러한 실패 사례들을 연구한다. 이 벤치마크는 1,679개의 검증된 기록을 포함하고 있으며, 이는 수동으로 정리한 350개의 병렬 작업과 URL 기반 궤적이 검증된 1,329개의 재구성된 기록으로 구성된다. [2606.20724v2]
- s4: 이 논문은 한국어 맥락을 기반으로 구성된 400개의 문제로 이루어진 웹 탐색 에이전트 벤치마크인 K-BrowseComp를 소개한다. [2606.02404v1]

## H_A17 — 사용자와 나눈 예전 대화를 장기 기억으로 저장했다가 꺼내 쓰는 LLM 구조 연구 핵심 내용 알려줘

### 인용 블록

[문서 1]
[Distance: 0.2500]
[발행일: 2025-02-19]
[2502.13847v1] DH-RAG: A Dynamic Historical Context-Powered Retrieval-Augmented Generation Method for Multi-Turn Dialogue
[초록] Retrieval-Augmented Generation (RAG) systems have shown substantial benefits in applications such as question answering and multi-turn dialogue \citep{lewis2020retrieval}. However, traditional RAG methods, while leveraging static knowledge bases, often overlook the potential of dynamic historical information in ongoing conversations. To bridge this gap, we introduce DH-RAG, a Dynamic Historical Context-Powered Retrieval-Augmented Generation Method for Multi-Turn Dialogue. DH-RAG is inspired by human cognitive processes that utilize both long-term memory and immediate historical context in conversational responses \citep{stafford1987conversational}. DH-RAG is structured around two principal components: a History-Learning based Query Reconstruction Module, designed to generate effective queries by synthesizing current and prior interactions, and a Dynamic History Information Updating Module, which continually refreshes historical context throughout the dialogue. The center of DH-RAG is a Dynamic Historical Information database, which is further refined by three strategies within the Query Reconstruction Module: Historical Query Clustering, Hierarchical Matching, and Chain of Thought Tracking. Experimental evaluations show that DH-RAG significantly surpasses conventional models on several benchmarks, enhancing response relevance, coherence, and dialogue quality.

## **Abstract**

Retrieval-Augmented Generation (RAG) systems have shown substantial benefits in applications such as question answering and multi-turn dialogue [22]. However, traditional RAG methods, while leveraging static knowledge bases, often overlook the potential of dynamic historical information in ongoing conversations. To bridge this gap, we introduce DH-RAG, a Dynamic Historical Context-Powered Retrieval-Augmented Generation Method for Multi-Turn Dialogue
[문서 2]
[Distance: 0.2344]
[발행일: 2026-10-22]
[2610.30755v1] Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought
[초록] LLM memory is widely used in long-term conversation understanding. Agentic memory systems often use mutation, structural organization, learned retrieval strategies, or other complex operations. Is this complexity always necessary? We study Raw-RAG, a naive RAG baseline using dense retrieval and reranking over raw history to supply evidence to a reader LLM. Across LoCoMo, LongMemEval, MEME, and MemoryAgentBench, Raw-RAG ranks first among the compared memory systems in six of seven benchmark-model settings, outperforming the strongest compared agentic memory system by 0.13-5.53 points. We investigate why raw-history retrieval remains competitive. Evidence analysis shows that its higher coverage of necessary evidence can offset lower utilization. Useful evidence includes both answer values and the relations and dependency paths needed to derive them. Even complete access to transformed memory stores leaves an accuracy gap relative to raw evidence, highlighting the importance of preserving raw information. These findings challenge the necessity of complex agentic memory for the evaluated conversation tasks and establish naive RAG as an essential baseline.

LLM memory is widely used in long-term conversation understanding. Agentic memory systems often use mutation, structural organization, learned retrieval strategies, or other complex operations. Is this complexity always necessary? We study RAW-RAG, a naive RAG baseline using dense retrieval and reranking over raw history to supply evidence to a reader LLM

### 문장

- s1: 반면 Raw-RAG는 LoCoMo, LongMemEval, MEME, MemoryAgentBench 등 다양한 벤치마크에서 복잡한 에이전트 메모리보다 우수한 성능을 보이며, 필요한 증거의 높은 커버리지로 인해 단순한 RAG가 강력한 기준이 된다 [2610.30755v1].
- s2: Across LoCoMo, LongMemEval, MEME, and MemoryAgentBench, Raw-RAG ranks first among the compared memory systems in six of seven benchmark-model settings, outperforming the strongest compared agentic memory system by 0.13-5.53 points. [2610.30755v1]
- s3: DH-RAG는 동적 역사 정보 데이터베이스와 쿼리 재구성 모듈을 활용해 다중 턴 대화에서 응답 관련성, 일관성 및 대화 품질을 크게 향상시킨다 [2502.13847v1].
- s4: 이를 연결하기 위해 다중 턴 대화에 적용되는 동적 역사적 맥락 기반 검색 증강 생성 방법인 DH-RAG를 제안한다. [2502.13847v1]

## H_A18 — 보상 모델 없이 선호 데이터만으로 바로 정책을 학습하는 방법 다룬 논문 설명해줘

### 인용 블록

[문서 1]
[Distance: 0.2802]
[발행일: 2024-12-30]
[2412.21001v3] LEASE: Offline Preference-based Reinforcement Learning with High Sample Efficiency
[초록] Offline preference-based reinforcement learning (PbRL) provides an effective way to overcome the challenges of designing reward and the high costs of online interaction. However, since labeling preference needs real-time human feedback, acquiring sufficient preference labels is challenging. To solve this, this paper proposes a offLine prEference-bAsed RL with high Sample Efficiency (LEASE) algorithm, where a learned transition model is leveraged to generate unlabeled preference data. Considering the pretrained reward model may generate incorrect labels for unlabeled data, we design an uncertainty-aware mechanism to ensure the performance of reward model, where only high confidence and low variance data are selected. Moreover, we provide the generalization bound of reward model to analyze the factors influencing reward accuracy, and demonstrate that the policy learned by LEASE has theoretical improvement guarantee. The developed theory is based on state-action pair, which can be easily combined with other offline algorithms. The experimental results show that LEASE can achieve comparable performance to baseline under fewer preference data without online interaction.

performance of policy learning. Recently, preference-based direct policy learning has gained significant research attention [51]–[54], as it directly optimizes the policy based on user preferences. The most representative work in this area is the Direct Preference Optimization (DPO) algorithm [51], which formulates an initial preference optimization objective
[문서 2]
[Distance: 0.3484]
[발행일: 2023-05-29]
[2305.18290v3] Direct Preference Optimization: Your Language Model is Secretly a Reward Model
[초록] While large-scale unsupervised language models (LMs) learn broad world knowledge and some reasoning skills, achieving precise control of their behavior is difficult due to the completely unsupervised nature of their training. Existing methods for gaining such steerability collect human labels of the relative quality of model generations and fine-tune the unsupervised LM to align with these preferences, often with reinforcement learning from human feedback (RLHF). However, RLHF is a complex and often unstable procedure, first fitting a reward model that reflects the human preferences, and then fine-tuning the large unsupervised LM using reinforcement learning to maximize this estimated reward without drifting too far from the original model. In this paper we introduce a new parameterization of the reward model in RLHF that enables extraction of the corresponding optimal policy in closed form, allowing us to solve the standard RLHF problem with only a simple classification loss. The resulting algorithm, which we call Direct Preference Optimization (DPO), is stable, performant, and computationally lightweight, eliminating the need for sampling from the LM during fine-tuning or performing significant hyperparameter tuning. Our experiments show that DPO can fine-tune LMs to align with human preferences as well as or better than existing methods. Notably, fine-tuning with DPO exceeds PPO-based RLHF in ability to control sentiment of generations, and matches or improves response quality in summarization and single-turn dialogue while being substantially simpler to implement and train.

## **4 Direct Preference Optimization**

Motivated by the challenges of applying reinforcement learning algorithms on large-scale problems such as fine-tuning language models, our goal is to derive a simple approach for policy optimization using preferences directly. Unlike prior RLHF methods, which learn a reward and then optimize it via RL, our approach leverages a particular choice of reward model parameterization that enables extraction of its optimal policy in closed form, without an RL training loop

### 문장

- s1: 이를 해결하기 위해 본 논문은 학습된 전이 모델을 이용해 라벨이 없는 선호도 데이터를 생성하는 고 샘플 효율성 오프라인 선호 기반 강화학습(LEASE) 알고리즘을 제안한다. [2412.21001v3]
- s2: 특히 DPO 기반 파인튜닝은 생성물의 감정을 제어하는 능력이 PPO 기반 RLHF를 능가하며, 요약과 단일 턴 대화와 같은 작업에서 응답 품질을 일치시키거나 향상시키는 동시에 구현 및 학습이 현저히 단순합니다. [2305.18290v3]
- s3: LEASE는 선호 데이터만으로 정책을 학습하는 방법으로, 적은 선호 데이터에서도 기존 기법과 유사한 성능을 달성한다는 실험 결과를 보여줍니다[2412.21001v3].
- s4: DPO는 언어 모델을 인간 선호와 정렬하도록 미세 조정하여 RLHF보다 단순하면서도 선호에 대한 제어 능력을 향상시킨다고 보고합니다[2305.18290v3].

## H_A20 — 질문을 여러 개의 하위 질문으로 쪼개서 차례로 검색하며 답하는 멀티홉 RAG 연구 알려줘

### 인용 블록

[문서 1]
[Distance: 0.1470]
[발행일: 2024-08-08]
[2408.04259v2] EfficientRAG: Efficient Retriever for Multi-Hop Question Answering
[초록] Retrieval-augmented generation (RAG) methods encounter difficulties when addressing complex questions like multi-hop queries. While iterative retrieval methods improve performance by gathering additional information, current approaches often rely on multiple calls of large language models (LLMs). In this paper, we introduce EfficientRAG, an efficient retriever for multi-hop question answering. EfficientRAG iteratively generates new queries without the need for LLM calls at each iteration and filters out irrelevant information. Experimental results demonstrate that EfficientRAG surpasses existing RAG methods on three open-domain multi-hop question-answering datasets.

## **Abstract**

Retrieval-augmented generation (RAG) methods encounter difficulties when addressing complex questions like multi-hop queries. While iterative retrieval methods improve performance by gathering additional information, current approaches often rely on multiple calls of large language models (LLMs). In this paper, we introduce EfficientRAG, an efficient retriever for multi-hop question answering
[문서 2]
[Distance: 0.2056]
[발행일: 2025-09-08]
[2509.09713v1] HANRAG: Heuristic Accurate Noise-resistant Retrieval-Augmented Generation for Multi-hop Question Answering
[초록] The Retrieval-Augmented Generation (RAG) approach enhances question-answering systems and dialogue generation tasks by integrating information retrieval (IR) technologies with large language models (LLMs). This strategy, which retrieves information from external knowledge bases to bolster the response capabilities of generative models, has achieved certain successes. However, current RAG methods still face numerous challenges when dealing with multi-hop queries. For instance, some approaches overly rely on iterative retrieval, wasting too many retrieval steps on compound queries. Additionally, using the original complex query for retrieval may fail to capture content relevant to specific sub-queries, resulting in noisy retrieved content. If the noise is not managed, it can lead to the problem of noise accumulation. To address these issues, we introduce HANRAG, a novel heuristic-based framework designed to efficiently tackle problems of varying complexity. Driven by a powerful revelator, HANRAG routes queries, decomposes them into sub-queries, and filters noise from retrieved documents. This enhances the system's adaptability and noise resistance, making it highly capable of handling diverse queries. We compare the proposed framework against other leading industry methods across various benchmarks. The results demonstrate that our framework obtains superior performance in both single-hop and multi-hop question-answering tasks.

## **Abstract**

The Retrieval-Augmented Generation (RAG) approach enhances question-answering systems and dialogue generation tasks by integrating information retrieval (IR) technologies with large language models (LLMs). This strategy, which retrieves information from external knowledge bases to bolster the response capabilities of generative models, has achieved certain successes. However, current RAG methods still face numerous challenges when dealing with multi-hop queries

### 문장

- s1: 이러한 문제들을 해결하기 위해 이 논문은 다양한 복잡성을 가진 문제를 효율적으로 다루도록 설계된 새로운 휴리스틱 기반 프레임워크인 HANRAG을 제안한다. [2509.09713v1]
- s2: HANRAG는 다양한 벤치마크에서 다른 주요 산업용 방법과 비교했을 때 단일홉 및 멀티홉 질문 답변 작업 모두에서 우수한 성능을 달성했다는 결과를 제시한다. [2509.09713v1]
- s3: EfficientRAG은 세 개의 오픈 도메인 멀티홉 질문 답변 데이터셋에서 기존 RAG 방법보다 뛰어난 성능을 보였으며, 반복적 검색이 추가 정보를 수집해 성능을 향상시키지만 현재 접근법은 대규모 언어 모델(LLM)의 다중 호출에 의존한다는 점을 강조한다. [2408.04259v2]
- s4: EfficientRAG은 각 반복마다 LLM 호출 없이 새로운 쿼리를 생성하고 관련 없는 정보를 걸러냅니다. [2408.04259v2]

## H_A23 — 단백질 구조 예측에 언어 모델을 쓰는 연구 있어?

### 인용 블록

[문서 2]
[Distance: 0.2749]
[발행일: 2024-12-16]
[2412.11618v1] EvoLlama: Enhancing LLMs' Understanding of Proteins via Multimodal Structure and Sequence Representations
[초록] Current Large Language Models (LLMs) for understanding proteins primarily treats amino acid sequences as a text modality. Meanwhile, Protein Language Models (PLMs), such as ESM-2, have learned massive sequential evolutionary knowledge from the universe of natural protein sequences. Furthermore, structure-based encoders like ProteinMPNN learn the structural information of proteins through Graph Neural Networks. However, whether the incorporation of protein encoders can enhance the protein understanding of LLMs has not been explored. To bridge this gap, we propose EvoLlama, a multimodal framework that connects a structure-based encoder, a sequence-based protein encoder and an LLM for protein understanding. EvoLlama consists of a ProteinMPNN structure encoder, an ESM-2 protein sequence encoder, a multimodal projector to align protein and text representations and a Llama-3 text decoder. To train EvoLlama, we fine-tune it on protein-oriented instructions and protein property prediction datasets verbalized via natural language instruction templates. Our experiments show that EvoLlama's protein understanding capabilities have been significantly enhanced, outperforming other fine-tuned protein-oriented LLMs in zero-shot settings by an average of 1%-8% and surpassing the state-of-the-art baseline with supervised fine-tuning by an average of 6%. On protein property prediction datasets, our approach achieves promising results that are competitive with state-of-the-art task-specific baselines. We will release our code in a future version.

- Jin Su, Chenchen Han, Yuyang Zhou, Junjie Shan, Xibin Zhou, and Fajie Yuan. 2023. Saprot: Protein language modeling with structure-aware vocabulary. _bioRxiv_ , pages 2023–10.  
10  
- Ross Taylor, Marcin Kardas, Guillem Cucurull, Thomas Scialom, Anthony Hartshorn, Elvis Saravia, Andrew Poulton, Viktor Kerkez, and Robert Stojnic. 2022. Galactica: A large language model for science. _arXiv preprint arXiv:2211.09085_ .  
- Tloen. 2023. Alpaca-lora. https://github.com/ tloen/alpaca-lora.
[문서 4]
[Distance: 0.3492]
[발행일: 2024-12-28]
[2412.20014v1] ProtCLIP: Function-Informed Protein Multi-Modal Learning
[초록] Multi-modality pre-training paradigm that aligns protein sequences and biological descriptions has learned general protein representations and achieved promising performance in various downstream applications. However, these works were still unable to replicate the extraordinary success of language-supervised visual foundation models due to the ineffective usage of aligned protein-text paired data and the lack of an effective function-informed pre-training paradigm. To address these issues, this paper curates a large-scale protein-text paired dataset called ProtAnno with a property-driven sampling strategy, and introduces a novel function-informed protein pre-training paradigm. Specifically, the sampling strategy determines selecting probability based on the sample confidence and property coverage, balancing the data quality and data quantity in face of large-scale noisy data. Furthermore, motivated by significance of the protein specific functional mechanism, the proposed paradigm explicitly model protein static and dynamic functional segments by two segment-wise pre-training objectives, injecting fine-grained information in a function-informed manner. Leveraging all these innovations, we develop ProtCLIP, a multi-modality foundation model that comprehensively represents function-aware protein embeddings. On 22 different protein benchmarks within 5 types, including protein functionality classification, mutation effect prediction, cross-modal transformation, semantic similarity inference and protein-protein interaction prediction, our ProtCLIP consistently achieves SOTA performance, with remarkable improvements of 75% on average in five cross-modal transformation benchmarks, 59.9% in GO-CC and 39.7% in GO-BP protein function prediction. The experimental results verify the extraordinary potential of ProtCLIP serving as the protein multi-modality foundation model.

## **2.2 Model Architecture**

The overview of our framework is displayed in Figure 3, which contains a protein encoder and a biotext encoder. The protein encoder is a protein language model for learning biological features from protein sequences and we use pre-trained ESM-2-650M (Lin et al. 2023) here. The biotext encoder is a text language model for learning linguistic features from biotext descriptions and we use PubMedBERT (Gu et al. 2021) here

### 문장

- s1: 5 가지 유형에 속하는 22 개의 서로 다른 단백질 벤치마크(단백질 기능 분류, 돌연변이 효과 예측, 교차 모달 변환, 의미 유사성 추론, 단백질-단백질 상호작용 예측 포함) 에서 이 논문의 ProtCLIP은 일관되게 SOTA 성능을 달성하며, 특히 5 개 교차 모달 변환 벤치마크에서 평균 75%의 뛰어난 향상을 보였고, GO-CC에서는 59.9%, GO-BP 단백질 기능 예측에서는 39.7%의 향상을 기록했습니다. [2412.20014v1]
- s2: ProtCLIP은 대규모 단백질-텍스트 쌍 데이터셋과 기능 정보 기반 사전학습 패러다임을 도입한 다중모달 기초 모델로, 5 가지 유형에 속하는 22 개의 다양한 단백질 벤치마크에서 일관되게 최첨단(SOTA) 성능을 보이며, 특히 교차모달 변환 벤치마크에서는 평균 75%의 향상률을 기록하였다[2412.20014v1].
- s3: EvoLlama는 다중모달 구조와 시퀀스 표현을 결합하여 LLM의 단백질 이해 능력을 향상시켰으며, 제로샷 설정에서 기존 미세조정 모델을 평균 1%-8% 상회하고, 감독학습 기반 최첨단 베이스라인보다 평균 6% 더 높은 성능을 달성했다[2412.11618v1].
- s4: 이 논문의 실험은 EvoLlama의 단백질 이해 능력이 크게 향상되었음을 보여주며, 제로샷 설정에서 다른 미세조정된 단백질 전용 대형 언어 모델보다 평균 1%~8% 더 우수한 성능을 보이고, 감독 학습 기반 미세조정을 통해 상태-of-the-art 기준선을 평균 6% 상회한다. [2412.11618v1]

## H_A24 — 자율주행 차량의 경로 계획을 강화학습으로 푸는 연구 핵심 내용 알려줘

### 인용 블록

[문서 1]
[Distance: 0.3260]
[발행일: 2024-12-17]
[2412.16201v1] CLIP-RLDrive: Human-Aligned Autonomous Driving via CLIP-Based Reward Shaping in Reinforcement Learning
[초록] This paper presents CLIP-RLDrive, a new reinforcement learning (RL)-based framework for improving the decision-making of autonomous vehicles (AVs) in complex urban driving scenarios, particularly in unsignalized intersections. To achieve this goal, the decisions for AVs are aligned with human-like preferences through Contrastive Language-Image Pretraining (CLIP)-based reward shaping. One of the primary difficulties in RL scheme is designing a suitable reward model, which can often be challenging to achieve manually due to the complexity of the interactions and the driving scenarios. To deal with this issue, this paper leverages Vision-Language Models (VLMs), particularly CLIP, to build an additional reward model based on visual and textual cues.

- [13] B Ravi Kiran, Ibrahim Sobh, Victor Talpaert, Patrick Mannion, Ahmad A Al Sallab, Senthil Yogamani, and Patrick Pérez. Deep reinforcement learning for autonomous driving: A survey. _IEEE Transactions on Intelligent Transportation Systems_ , 23(6):4909–4926, 2021.  
- [14] Minae Kwon, Sang Michael Xie, Kalesha Bullard, and Dorsa Sadigh. Reward design with language models. _arXiv preprint arXiv:2303.00001_ , 2023.
[문서 2]
[Distance: 0.3498]
[발행일: 2025-10-25]
[2510.22370v1] BLIP-FusePPO: A Vision-Language Deep Reinforcement Learning Framework for Lane Keeping in Autonomous Vehicles
[초록] In this paper, we propose Bootstrapped Language-Image Pretraining-driven Fused State Representation in Proximal Policy Optimization (BLIP-FusePPO), a novel multimodal reinforcement learning (RL) framework for autonomous lane-keeping (LK), in which semantic embeddings generated by a vision-language model (VLM) are directly fused with geometric states, LiDAR observations, and Proportional-Integral-Derivative-based (PID) control feedback within the agent observation space. The proposed method lets the agent learn driving rules that are aware of their surroundings and easy to understand by combining high-level scene understanding from the VLM with low-level control and spatial signals. Our architecture brings together semantic, geometric, and control-aware representations to make policy learning more robust. A hybrid reward function that includes semantic alignment, LK accuracy, obstacle avoidance, and speed regulation helps learning to be more efficient and generalizable. Our method is different from the approaches that only use semantic models to shape rewards. Instead, it directly embeds semantic features into the state representation. This cuts down on expensive runtime inference and makes sure that semantic guidance is always available. The simulation results show that the proposed model is better at LK stability and adaptability than the best vision-based and multimodal RL baselines in a wide range of difficult driving situations. We make our code publicly available.

1

# BLIP-FusePPO: A Vision-Language Deep Reinforcement Learning Framework for Lane Keeping in Autonomous Vehicles  
Seyed Ahmad Hosseini Miangoleh 1, Amin Jalal Aghdasian 1, Farzaneh Abdollahi 1 1Department of Electrical Engineering, Amirkabir University of Technology (Tehran Polytechnic), Tehran, Iran
[문서 3]
[Distance: 0.2905]
[발행일: 2026-03-18]
[2603.18315v1] DriveVLM-RL: Neuroscience-Inspired Reinforcement Learning with Vision-Language Models for Safe and Deployable Autonomous Driving
[초록] Ensuring safe decision-making in autonomous vehicles remains a fundamental challenge despite rapid advances in end-to-end learning approaches. Traditional reinforcement learning (RL) methods rely on manually engineered rewards or sparse collision signals, which fail to capture the rich contextual understanding required for safe driving and make unsafe exploration unavoidable in real-world settings. Recent vision-language models (VLMs) offer promising semantic understanding capabilities; however, their high inference latency and susceptibility to hallucination hinder direct application to real-time vehicle control. To address these limitations, this paper proposes DriveVLM-RL, a neuroscience-inspired framework that integrates VLMs into RL through a dual-pathway architecture for safe and deployable autonomous driving. The framework decomposes semantic reward learning into a Static Pathway for continuous spatial safety assessment using CLIP-based contrasting language goals, and a Dynamic Pathway for attention-gated multi-frame semantic risk reasoning using a lightweight detector and a large VLM. A hierarchical reward synthesis mechanism fuses semantic signals with vehicle states, while an asynchronous training pipeline decouples expensive VLM inference from environment interaction. All VLM components are used only during offline training and are removed at deployment, ensuring real-time feasibility. Experiments in the CARLA simulator show significant improvements in collision avoidance, task success, and generalization across diverse traffic scenarios, including strong robustness under settings without explicit collision penalties. These results demonstrate that DriveVLM-RL provides a practical paradigm for integrating foundation models into autonomous driving without compromising real-time feasibility. Demo video and code are available at: https://zilin-huang.github.io/DriveVLM-RL-website/

Wasif, D., Moore, T.J., Reddy, C.K., Cho, J.H., 2025. Drivemind: A dual-vlm based reinforcement learning framework for autonomous driving.
arXiv preprint arXiv:2506.00819 .
Wu, J., Huang, C., Huang, H., Lv, C., Wang, Y., Wang, F.Y., 2024. Recent advances in reinforcement learning-based autonomous driving behavior
planning: A survey. Transportation Research Part C: Emerging Technologies 164, 104654.

### 문장

- s1: 이러한 한계를 해결하기 위해 본 논문은 안전하고 실용적인 자율주행을 목표로 하는 이중 경로 구조를 통해 VLM을 강화학습에 통합하는 신경과학 영감을 받은 프레임워크인 DriveVLM-RL을 제안한다. [2603.18315v1]
- s2: CLIP 기반 보상 형성은 인간과 유사한 선호도를 반영하여 의사결정을 정렬한다[2412.16201v1].
- s3: BLIP-FusePPO는 다양한 어려운 주행 상황에서 기존 비전 기반 및 다중모달 RL 베이스라인보다 차선 유지 안정성과 적응성이 뛰어나다[2510.22370v1].
- s4: 이 논문에서는 자율 차선 유지(LK)를 위한 새로운 다중모달 강화학습(RL) 프레임워크인 Bootstrapped Language-Image Pretraining-driven Fused State Representation in Proximal Policy Optimization(BLIP-FusePPO)을 제안한다. [2510.22370v1]
- s5: 이를 달성하기 위해 CLIP 기반 보상 형상을 통해 자율주행차의 결정이 인간과 유사한 선호도에 맞춰 조정됩니다. [2412.16201v1]
- s6: DriveVLM-RL은 충돌 회피와 작업 성공률에서 유의미한 개선을 보이며, 명시적인 충돌 페널티가 없는 상황에서도 강인함을 입증한다[2603.18315v1].

## H_B02 — ColBERT 논문 자세히 설명해줘

### 인용 블록

[문서 1]
[Distance: 0.3947]
[발행일: 2020-04-27]
[2004.12832v2] ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT
[초록] Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

**RQ** 3: What does each component of ColBERT (e.g., late interaction, query augmentation) contribute to its quality? (§4.4)  
**RQ** 4: What are ColBERT’s indexing-related costs in terms of offline computation and memory overhead? (§4.5)
[문서 2]
[Distance: 0.4413]
[발행일: 2020-04-27]
[2004.12832v2] ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT
[초록] Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

## **3.1 Architecture**

Figure 3 depicts the general architecture of ColBERT, which comprises: (a) a query encoder _fQ_ , (b) a document encoder _fD_ , and (c) the late interaction mechanism. Given a query _q_ and document _d_ , _fQ_ encodes _q_ into a bag of fixed-size embeddings _Eq_ while _fD_ encodes _d_ into another bag _Ed_ . Crucially, each embeddings in _Eq_ and _Ed_ is _contextualized_ based on the other terms in _q_ or _d_ , respectively. We describe our BERT-based encoders in §3.2.

### 문장

- s1: 최근 두 개의 패시지 검색 데이터셋을 활용해 ColBERT를 광범위하게 평가합니다. [2004.12832v2]
- s2: [2004.12832v2]는 각각 "We extensively evaluate ColBERT using two recent passage search datasets"라는 동일한 대상 문장을 통해 연구의 범위를 명시하고 있습니다.

## H_B03 — Lost in the Middle 논문 핵심 내용 알려줘

### 인용 블록

[문서 1]
[Distance: 0.7041]
[발행일: 2023-07-06]
[2307.03172v3] Lost in the Middle: How Language Models Use Long Contexts
[초록] While recent language models have the ability to take long contexts as input, relatively little is known about how well they use longer context. We analyze the performance of language models on two tasks that require identifying relevant information in their input contexts: multi-document question answering and key-value retrieval. We find that performance can degrade significantly when changing the position of relevant information, indicating that current language models do not robustly make use of information in long input contexts. In particular, we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models. Our analysis provides a better understanding of how language models use their input context and provides new evaluation protocols for future long-context language models.

1nelsonliu.me/papers/lost-in-the-middle  
to the question and _k −_ 1 “distractor” documents do not. This task requires the model to access the document that contains the answer within its input context and use it to answer the question. Figure 2 presents an example.
[문서 2]
[Distance: 0.5742]
[발행일: 2024-10-18]
[2410.14641v3] Distance between Relevant Information Pieces Causes Bias in Long-Context LLMs
[초록] Positional bias in large language models (LLMs) hinders their ability to effectively process long inputs. A prominent example is the "lost in the middle" phenomenon, where LLMs struggle to utilize relevant information situated in the middle of the input. While prior research primarily focuses on single pieces of relevant information, real-world applications often involve multiple relevant information pieces. To bridge this gap, we present LongPiBench, a benchmark designed to assess positional bias involving multiple pieces of relevant information. Thorough experiments are conducted with five commercial and six open-source models. These experiments reveal that while most current models are robust against the "lost in the middle" issue, there exist significant biases related to the spacing of relevant information pieces. These findings highlight the importance of evaluating and reducing positional biases to advance LLM's capabilities.

Hsieh et al., 2024). In "needle in a haystack" tasks, models struggle to utilize information located in the middle
of the input, which is known as the "lost in the middle"
effect (Liu et al., 2024). This evaluation method is commonly used to analyze positional bias (Hengle et al.,
2024; Nelson et al., 2024). These analyses (Liu et al.,
2024) focused on single relevant information pieces
and their positions in the input sequence (front, middle,

### 문장

- s1: 특히, 이 논문은 관련 정보가 입력 컨텍스트의 시작이나 끝에 나타날 때 성능이 가장 높으며, 명시적으로 긴 컨텍스트를 지원하는 모델이라 하더라도 긴 컨텍스트 중간에 관련 정보를 접근해야 할 경우 성능이 크게 저하된다는 점을 관찰한다. [2307.03172v3]
- s2: Lost in the Middle 논문은 다문서 질문 답변과 키‑값 검색 과제에서 관련 정보가 입력 컨텍스트의 중간에 위치할 때 모델 성능이 크게 저하된다는 결과를 제시한다[2307.03172v3].
- s3: 반면 Distance between Relevant Information Pieces Causes Bias in Long-Context LLMs는 대부분의 현재 모델이 "lost in the middle" 문제에 대해 견고하지만, 관련 정보 조각 사이의 간격과 같은 위치 편향이 존재한다는 점을 강조한다[2410.14641v3].
- s4: 대표적인 예는 입력 중간에 위치한 관련 정보를 활용하는 데 어려움을 겪는 '중간에 사라지는' 현상이다. [2410.14641v3]

## H_B05 — ReAct 논문 자세히 설명해줘

### 인용 블록

[문서 1]
[Distance: 0.3513]
[발행일: 2022-10-06]
[2210.03629v3] ReAct: Synergizing Reasoning and Acting in Language Models
[초록] While large language models (LLMs) have demonstrated impressive capabilities across tasks in language understanding and interactive decision making, their abilities for reasoning (e.g. chain-of-thought prompting) and acting (e.g. action plan generation) have primarily been studied as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two: reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with external sources, such as knowledge bases or environments, to gather additional information. We apply our approach, named ReAct, to a diverse set of language and decision making tasks and demonstrate its effectiveness over state-of-the-art baselines, as well as improved human interpretability and trustworthiness over methods without reasoning or acting components. Concretely, on question answering (HotpotQA) and fact verification (Fever), ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API, and generates human-like task-solving trajectories that are more interpretable than baselines without reasoning traces. On two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples. Project site with code: https://react-lm.github.io

. In contrast to these methods, ReAct performs more than just isolated, fixed reasoning, and integrates model actions and their corresponding observations into a coherent stream of inputs for the model to reason more accurately and tackle tasks beyond reasoning (e.g. interactive decision making).
[문서 2]
[Distance: 0.3968]
[발행일: 2022-10-06]
[2210.03629v3] ReAct: Synergizing Reasoning and Acting in Language Models
[초록] While large language models (LLMs) have demonstrated impressive capabilities across tasks in language understanding and interactive decision making, their abilities for reasoning (e.g. chain-of-thought prompting) and acting (e.g. action plan generation) have primarily been studied as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two: reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with external sources, such as knowledge bases or environments, to gather additional information. We apply our approach, named ReAct, to a diverse set of language and decision making tasks and demonstrate its effectiveness over state-of-the-art baselines, as well as improved human interpretability and trustworthiness over methods without reasoning or acting components. Concretely, on question answering (HotpotQA) and fact verification (Fever), ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API, and generates human-like task-solving trajectories that are more interpretable than baselines without reasoning traces. On two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples. Project site with code: https://react-lm.github.io

to understand the importance of acting in reasoning tasks, and reasoning in interactive tasks; (4) we analyze the limitations of ReAct under the prompting setup (i.e

### 문장

- s1: 또한 ALFWorld와 WebShop에서 기존 방법보다 높은 성공률을 달성함으로써 실제 응용에 유용함을 입증한다[2210.03629v3].
- s2: 두 개의 상호작용적 의사결정 벤치마크(ALFWorld와 WebShop)에서 ReAct는 컨텍스트에 하나 또는 두 개의 예시만 제공되더라도 모방 학습과 강화학습 방법에 비해 절대 성공률이 각각 34%와 10% 더 높은 성능을 보였습니다. [2210.03629v3]

## H_B14 — RAG 자동 평가 프레임워크 ARES 논문 요약해줘

### 인용 블록

[문서 1]
[Distance: 0.3687]
[발행일: 2023-11-16]
[2311.09476v2] ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems
[초록] Evaluating retrieval-augmented generation (RAG) systems traditionally relies on hand annotations for input queries, passages to retrieve, and responses to generate. We introduce ARES, an Automated RAG Evaluation System, for evaluating RAG systems along the dimensions of context relevance, answer faithfulness, and answer relevance. By creating its own synthetic training data, ARES finetunes lightweight LM judges to assess the quality of individual RAG components. To mitigate potential prediction errors, ARES utilizes a small set of human-annotated datapoints for prediction-powered inference (PPI). Across eight different knowledge-intensive tasks in KILT, SuperGLUE, and AIS, ARES accurately evaluates RAG systems while using only a few hundred human annotations during evaluation. Furthermore, ARES judges remain effective across domain shifts, proving accurate even after changing the type of queries and/or documents used in the evaluated RAG systems. We make our code and datasets publicly available on Github.

The two most-closely related projects to ARES are EXAM (Sander and Dietz, 2021) and RAGAS (James and Es, 2023). To evaluate RAG systems, the EXAM metric estimates how many exam questions a reader (simulated as a QA system) can answer correctly based on the generated response. This requires a set of queries with several associated sub-questions each, which adds a burden that ARES does not bring. RAGAS is based on a handful of heuristic hand-written prompts
[문서 2]
[Distance: 0.5172]
[발행일: 2025-04-10]
[2504.07803v1] A System for Comprehensive Assessment of RAG Frameworks
[초록] Retrieval Augmented Generation (RAG) has emerged as a standard paradigm for enhancing the factual accuracy and contextual relevance of Large Language Models (LLMs) by integrating retrieval mechanisms. However, existing evaluation frameworks fail to provide a holistic black-box approach to assessing RAG systems, especially in real-world deployment scenarios. To address this gap, we introduce SCARF (System for Comprehensive Assessment of RAG Frameworks), a modular and flexible evaluation framework designed to benchmark deployed RAG applications systematically. SCARF provides an end-to-end, black-box evaluation methodology, enabling a limited-effort comparison across diverse RAG frameworks. Our framework supports multiple deployment configurations and facilitates automated testing across vector databases and LLM serving strategies, producing a detailed performance report. Moreover, SCARF integrates practical considerations such as response coherence, providing a scalable and adaptable solution for researchers and industry professionals evaluating RAG applications. Using the REST APIs interface, we demonstrate how SCARF can be applied to real-world scenarios, showcasing its flexibility in assessing different RAG frameworks and configurations. SCARF is available at GitHub repository.

[1] have evolved rapidly, resulting in a wide variety of system variants [2]–[5] and benchmarking frameworks [6]. Many existing evaluation methods [7], [8] focus on assessing specific components, such as the relevance of retrieved documents or the quality of generated responses

### 문장

- s1: 반면 SCARF는 REST API 인터페이스를 통해 다양한 RAG 프레임워크와 구성을 평가할 수 있는 유연한 엔드투엔드 블랙박스 평가 방법을 제공한다[2504.07803v1].
- s2: ARES는 복잡한 서브 질문을 포함한 쿼리 집합이 필요하지만 추가적인 부하를 발생시키지 않으며, RAGAS는 소수의 수작업 프롬프트에 기반한다[2311.09476v2].
- s3: ARES와 가장 밀접하게 관련된 두 프로젝트는 Sander와 Dietz(2021)가 제안한 EXAM과 James와 Es(2023)가 제안한 RAGAS이다. [2311.09476v2]
- s4: REST API 인터페이스를 활용하여 이 논문은 SCARF가 실제 시나리오에 적용되는 방법을 보여주며, 다양한 RAG 프레임워크와 구성을 평가하는 데 있어 그 유연성을 입증한다. [2504.07803v1]

