P000 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2602.16974] Beyond Chunk-Then-Embed: A Comprehensive Taxonomy and Evaluation of Document Chunking Strategies for Information Retrieval
     This paper reproduces prior studies in document chunking and presents a systematic framework that unifies existing strategies along two key dimensions: (1) segmentation methods, including structure-based methods (fixed-size, sentence-based, and paragraph-based) as well as semantically-informed and LLM-guided methods; and (2) embedding paradigms, which determine the timing of chunking relative to embedding (pre-embedding chunking vs. contextualized chunking). Our comprehensive evaluation reveals that optimal chunking strategies are task-dependent: simple structure-based methods outperform LLM…

P001 | Q: 생성 모델 워터마크 연구들 정리해줘
     [2606.22875] FedOT: Ownership Verification and Leakage Tracing via Watermarks for Federated LDMs
     While an intuitive approach is to adopt existing VAE-based watermarking techniques for LDMs in FL, this strategy falls short in addressing such threats due to two fundamental challenges: (1) Existing methods support ownership verification but lack the ability to trace model leakage to a specific malicious client; (2) VAE-based watermarks are vulnerable, as they can be removed simply by replacing the decoder with a clean counterpart. In this paper, we propose FedOT, the first framework for ownership verification and leakage tracing in federated LDMs.

P002 | Q: LLM 환각을 탐지하는 연구나 완화하는 연구 알려줘
     [2310.18344] Chainpoll: A high efficacy method for LLM hallucination detection
     Our findings indicate that ChainPoll outperforms in all RealHall benchmarks, achieving an overall AUROC of 0.781. This surpasses the next best theoretical method by 11% and exceeds industry standards by over 23%. Additionally, ChainPoll is cost-effective and offers greater transparency than other metrics. We introduce two novel metrics to assess LLM hallucinations: Adherence and Correctness.

P003 | Q: 연합학습에서 통신 효율이나 차등 프라이버시를 다룬 연구 있어?
     [2503.21154] Federated Learning with Differential Privacy: An Utility-Enhanced Approach
     To improve the privacy-utility trade-off, we present a modification to these vanilla differentially private algorithms based on a Haar wavelet transformation step and a novel noise injection scheme that significantly lowers the asymptotic bound of the noise variance. We also present a holistic convergence analysis of our proposed algorithm, showing that our method yields better convergence performance than the vanilla DP algo… Numerical experiments on real-world datasets demonstrate that our method outperforms existing approaches in model utility while maintaining the same privacy guarantees.

P004 | Q: 시계열 예측 관련 논문 5개 찾아줘
     [2412.09328] Auto-Regressive Moving Diffusion Models for Time Series Forecasting
     To bridge this misalignment, and inspired by the classic Auto-Regressive Moving Average (ARMA) theory, which views time series as continuous sequential progressions evolving from previous data points, we propose a novel Auto-Regressive Moving Diffusion (ARMD) model to first achieve the continuous sequential diffusion-based TSF. Extensive experiments conducted on seven widely used datasets demonstrate that our model achieves state-of-the-art performance, significantly outperforming existing diffusion-based TSF models.

P005 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2506.17277] Chunk Twice, Embed Once: A Systematic Study of Segmentation and Representation Trade-offs in Chemistry-Aware Retrieval-Augmented Generation
     This study presents the first large-scale, systematic evaluation of chunking strategies and embedding models tailored to chemistry-focused RAG systems. Our results reveal that recursive token-based chunking (specifically R100-0) consistently outperforms other approaches, offering strong performance with minimal resource overhead. We also find that retrieval-optimized embeddings -- such as Nomic and Intfloat E5 variants -- substantially outperform domain-specialized models like SciBERT.

P006 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2412.15623] JailPO: A Novel Black-box Jailbreak Framework via Preference Optimization against Aligned LLMs
     To address these issues, we present JailPO, a novel black-box jailbreak framework to examine LLM alignment. Extensive experiments demonstrate that JailPO not only automates the attack process while maintaining effectiveness but also exhibits superior performance in efficiency, universality, and robustness against defenses compared to baselines. Additionally, our analysis of the three JailPO patterns reveals that attacks based on complex templates exhibit higher attack strength, whereas covert question transformations elicit riskier responses and are more likely to bypass defense mechanisms.

P007 | Q: LLM 환각 탐지 방법 논문들 비교해서 정리해줘
     [2404.18930] Hallucination of Multimodal Large Language Models: A Survey
     This problem has attracted increasing attention, prompting efforts to detect and mitigate such inaccuracies. We review recent advances in identifying, evaluating, and mitigating these hallucinations, offering a detailed overview of the underlying causes, evaluation benchmarks, metrics, and strategies developed to address this issue. Additionally, we analyze the current challenges and limitations, formulating open questions that delineate potential pathways for future research. Resources are available at: https://github.com/showlab/Awesome-MLLM-Hallucination.

P008 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2410.12837] A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions
     This paper presents a comprehensive study of Retrieval-Augmented Generation (RAG), tracing its evolution from foundational concepts to the current state of the art. Future research directions are proposed, focusing on improving the robustness of RAG models, expanding the scope of application of RAG models, and addressing societal implications. This survey aims to serve as a foundational resource for researchers and practitioners in understanding the potential of RAG and its trajectory in natural language processing.

P009 | Q: LLM 환각을 탐지하는 연구나 완화하는 연구 알려줘
     [2509.13702] DSCC-HS: A Dynamic Self-Reinforcing Framework for Hallucination Suppression in Large Language Models
     We introduce **Dynamic Self-reinforcing Calibration for Hallucination Suppression (DSCC-HS)**, a novel, proactive framework that intervenes during autoregressive decoding. Our experiments on TruthfulQA and BioGEN show DSCC-HS achieves state-of-the-art performance. On TruthfulQA, it reached a 99.2% Factual Consistency Rate (FCR).

P010 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2407.16667] RedAgent: Red Teaming Large Language Models with Context-aware Autonomous Language Agent
     Recently, advanced Large Language Models (LLMs) such as GPT-4 have been integrated into many real-world applications like Code Copilot. By self-reflecting on contextual feedback in an additional memory buffer, RedAgent continuously learns how to leverage these strategies to achieve effective jailbreaks in specific contexts. Extensive experiments demonstrate that our system can jailbreak most black-box LLMs in just five queries, improving the efficiency of existing red teaming methods by two times. We have reported all found issues and communicated with OpenAI and Meta for bug fixes.

P011 | Q: 요즘 speculative decoding 연구 동향 정리해줘
     [2606.18394] JetSpec: Breaking the Scaling Ceiling of Speculative Decoding with Parallel Tree Drafting
     We propose JetSpec, a head-based SD framework that combines one-forward drafting efficiency with branch-wise causal conditioning. Across math, coding, and chat benchmarks on dense and MoE Qwen3 models, JetSpec consistently outperforms bidirectional-head and tree-based SD baselines. On H100 GPUs, JetSpec achieves up to 9.64x speedup on MATH-500 and 4.58x on open-ended conversational workloads, with further latency gains demonstrated through vLLM integration under realistic serving loads.

P012 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2502.15723] Balancing Content Size in RAG-Text2SQL System
     While richer document content can improve schema relevance and retrieval accuracy, it also introduces noise, increasing the risk of hallucinations and reducing query fidelity as the prompt size of the Text2SQL model increases. Key thresholds are identified where performance degradation occurs, along with actionable strategies to mitigate these challenges. Our findings provide a roadmap for enhancing the robustness of RAG + Text2SQL systems, offering practical insights for real-world applications.

P013 | Q: 월드 모델 최근 연구 동향 정리해줘
     [2501.00195] Towards Unraveling and Improving Generalization in World Models
     Thus motivated, we develop a stochastic differential equation formulation by treating the world model learning as a stochastic dynamical system, and characterize the impact of latent representation errors on robustness and generalization, for both cases with zero-drift representation errors and with non-zero-drift representation errors. Our experimental studies corroborate that this regularization approach not only stabilizes training but also accelerates convergence and improves accuracy of long-horizon prediction.

P014 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2603.28817] GUARD-SLM: Token Activation-Based Defense Against Jailbreak Attacks for Small Language Models
     We analyze hidden-layer activations across different layers and model architectures, revealing that different input types form distinguishable patterns in the internal representation space. Based on this observation, we propose GUARD-SLM, a lightweight token activation-based method that operates in the representation space to filter malicious prompts during inference while preserving benign ones. Our findings highlight robustness limitations across layers of language models and provide a practical direction for secure small language model deployment.

P015 | Q: 생성 모델 워터마크에서 이미지·영상 워터마크나 텍스트·에이전트 워터마크 연구 있어?
     [2412.19834] RoboSignature: Robust Signature and Watermarking on Network Attacks
     In this paper, we present a novel adversarial fine-tuning attack that disrupts the model's ability to embed the intended watermark, exposing a significant vulnerability in existing watermarking methods. Our findings emphasize the importance of anticipating and defending against potential vulnerabilities in generative systems.

P016 | Q: 생성 모델 워터마크에서 이미지·영상 워터마크나 텍스트·에이전트 워터마크 연구 있어?
     [2610.08668] Semantic Behavioral Watermarking: Paraphrase-Robust and Forgery-Resistant Provenance for LLM Agents
     We present Semantic Behavioral Watermarking (SBW): watermarking over semantic action clusters under history conditioning, with the public-cluster bin replaced by keyed collision-resistant binning whose fresh-bucket assignment is provably unpredictable in the random-oracle model. Across five agent models (3B-14B, four vendors) and three encoders the ordering holds on both benchmarks: on ToolBench (600 trajectories per model) detection under rewriting is 0.49-0.66 for cluster-level versus 0.05-0.17 for exact-symbol at a permutation-calibrated 1% FPR, at 72-83% choice agreement against 22-27% f…

P017 | Q: LLM 환각 탐지 방법 논문들 비교해서 정리해줘
     [2310.18344] Chainpoll: A high efficacy method for LLM hallucination detection
     Our findings indicate that ChainPoll outperforms in all RealHall benchmarks, achieving an overall AUROC of 0.781. This surpasses the next best theoretical method by 11% and exceeds industry standards by over 23%. Additionally, ChainPoll is cost-effective and offers greater transparency than other metrics. We introduce two novel metrics to assess LLM hallucinations: Adherence and Correctness.

P018 | Q: 연합학습 연구들 정리해줘
     [2412.13589] SemiDFL: A Semi-Supervised Paradigm for Decentralized Federated Learning
     In this work, we propose SemiDFL, the first semi-supervised DFL method that enhances DFL performance in SSL scenarios by establishing a consensus in both data and model spaces. Specifically, we utilize neighborhood information to improve the quality of pseudo-labeling, which is crucial for effectively leveraging unlabeled data. Through extensive experimentation, we demonstrate the remarkable performance superiority of the proposed DFL-Semi method over existing CFL and DFL schemes in both IID and non-IID SSL scenarios.

P019 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2412.11120] Latent Reward: LLM-Empowered Credit Assignment in Episodic Reinforcement Learning
     To tackle these issues, we introduce LaRe, a novel LLM-empowered symbolic-based decision-making framework, to improve credit assignment. Theoretically, reward-irrelevant redundancy elimination in the latent reward benefits RL performance from more accurate reward estimation. Extensive experimental results witness that LaRe (i) achieves superior temporal credit assignment to SOTA methods, (ii) excels in allocating contributions among multiple agents, and (iii) outperforms policies trained with ground truth rewards for certain tasks.

P020 | Q: 요즘 LLM 양자화 연구들 정리해줘
     [2511.13023] SLMQuant:Benchmarking Small Language Model Quantization for Practical Deployment
     This paper introduces SLMQuant, the first systematic benchmark for evaluating LLM compression techniques when applied to SLMs. Our findings reveal fundamental disparities between SLMs and LLMs in quantization sensitivity, demonstrating that direct transfer of LLM-optimized techniques leads to suboptimal results due to SLMs' unique architectural characteristics a… SLMQuant establishes a foundational framework for advancing efficient SLM deployment on low-end devices in edge applications, and provides critical insights for deploying lightweight language models in resource-constrained scenarios.

P021 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2408.08067] RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation
     In this paper, we propose a fine-grained evaluation framework, RAGChecker, that incorporates a suite of diagnostic metrics for both the retrieval and generation modules. Meta evaluation verifies that RAGChecker has significantly better correlations with human judgments than other evaluation metrics. Using RAGChecker, we evaluate 8 RAG systems and conduct an in-depth analysis of their performance, revealing insightful patterns and trade-offs in the design choices of RAG architectures.

P022 | Q: VLA 모델 연구들 정리해줘
     [2412.18194] VLABench: A Large-Scale Benchmark for Language-Conditioned Robotics Manipulation with Long-Horizon Reasoning Tasks
     Recently, methods based on foundation models especially Vision-Language-Action models (VLAs) have shown a substantial potential to solve language-conditioned manipulation (LCM) tasks well. However, existing benchmarks do not adequately meet the needs of VLAs and relative algorithms. To better define such general-purpose tasks in the context of LLMs and advance the research in VLAs, we present VLABench, an open-source benchmark for evaluating universal LCM task learning.

P023 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2502.16886] ReFreeKV: Towards Threshold-Free KV Cache Compression
     As a result, the dependence of such input-sensitive threshold can be a fundamental limitation that causes large degradation on arbitrary inputs. In this work, we propose a new objective that lifts the threshold constraints for robust KV compression, advocating for "threshold-free" methods that adaptively adjust budget allocation while preserving full-cache performance. Extensive experiments across 13 datasets with diverse context lengths, task types, and model sizes demonstrate its efficacy and efficiency.

P024 | Q: 연합학습에서 통신 효율이나 차등 프라이버시를 다룬 연구 있어?
     [2412.11207] ProFe: Communication-Efficient Decentralized Federated Learning via Distillation and Prototypes
     Thus, this paper introduces ProFe, a novel communication optimization algorithm for DFL that combines knowledge distillation, prototype learning, and quantization techniques. ProFe utilizes knowledge from large local models to train smaller ones for aggregation, incorporates prototypes to better learn unseen classes, and applies quantization to reduce data transmit… Results showed that the proposed algorithm reduces communication costs by up to ~40-50% while maintaining or improving model performance. In addition, it adds ~20% training time due to increased complexity, generating a trade-off.

P025 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2610.14448] KV4-RL: Unlocking Faster Asynchronous Rollouts for RLVR with INT4 KV Cache Quantization
     We propose \emph{KV4-RL}, which combines calibration-free INT4 KV quantization with selective INT8 protection of attention sinks and recent context. Protecting a bounded number of positions reduces sampler mismatch while retaining most of the speedup from INT4. Across 400 iterations of Qwen3-8B-Base GRPO training, KV4-RL achieves $1.80\times$cumulative rollout speedup and$1.27\times$cumulative full-iteration speedup over BF16 rollout, reaching$1.97\times$ rollout speedup over the final 50 iterations.

P026 | Q: RAG에서 검색된 문서의 순서나 개수가 답변 품질에 주는 영향을 분석한 연구 찾아줘
     [2401.14887] The Power of Noise: Redefining Retrieval for RAG Systems
     We argue here that the retrieval component of RAG systems, be it dense or sparse, deserves increased attention from the research community, and accordingly, we conduct the first comprehensive and systematic examination of the retrieval strategy of RAG systems. One counter-intuitive finding of this work is that the retriever's highest-scoring documents that are not directly relevant to the query (e.g., do not contain the answer) negatively impact the effectiveness of the LLM. Even more surprising, we discovered that adding random documents in the prompt improves the LLM accuracy by up to 35%.

P027 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2404.00282] Survey on Large Language Model-Enhanced Reinforcement Learning: Concept, Taxonomy, and Methods
     Utilizing the classical agent-environment interaction paradigm, we propose a structured taxonomy to systematically categorize LLMs' functionalities in RL, including four roles: information processor, reward designer, decision-maker, and generator.

P028 | Q: 요즘 speculative decoding 연구 동향 정리해줘
     [2610.23787] DLite: History-free Speculative Decoding for Agentic AI
     Under such workloads, we observe that existing draft models suffer from up to an 80% degradation in acceptance length, while maintaining their historical KV cache introduces substantial system overhead. To effectively train this heterogeneous history-free architecture, we introduce a tailored two-stage training strategy. Experiments on general-purpose, long-context and agentic workloads show that DLite achieves 2-6 acceptance length and outperforms the state-of-the-art speculative decoding method, DSpark, up to 70%.

P029 | Q: LLM 코드 생성 연구들 어떤 방향으로 가고 있어?
     [2606.12191] Agentic Environment Engineering for Large Language Models: A Survey of Environment Modeling, Synthesis, Evaluation, and Application
     Specifically, the paper first introduces representative environments from the perspectives of eight attributes and eight domains, providing detailed analyses of their development paths and highlighting their core capabilities. This paper also shows different environment evaluation methods in each paradigm.

P030 | Q: RAG에서 노이즈 문서나 방해 문서에 대한 강건성을 다룬 연구 찾아줘
     [2401.14887] The Power of Noise: Redefining Retrieval for RAG Systems
     We argue here that the retrieval component of RAG systems, be it dense or sparse, deserves increased attention from the research community, and accordingly, we conduct the first comprehensive and systematic examination of the retrieval strategy of RAG systems. One counter-intuitive finding of this work is that the retriever's highest-scoring documents that are not directly relevant to the query (e.g., do not contain the answer) negatively impact the effectiveness of the LLM. Even more surprising, we discovered that adding random documents in the prompt improves the LLM accuracy by up to 35%.

P031 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2603.28817] GUARD-SLM: Token Activation-Based Defense Against Jailbreak Attacks for Small Language Models
     We analyze hidden-layer activations across different layers and model architectures, revealing that different input types form distinguishable patterns in the internal representation space. Based on this observation, we propose GUARD-SLM, a lightweight token activation-based method that operates in the representation space to filter malicious prompts during inference while preserving benign ones. Our findings highlight robustness limitations across layers of language models and provide a practical direction for secure small language model deployment.

P032 | Q: VLA 모델 연구들 정리해줘
     [2510.11660] ManiAgent: An Agentic Framework for General Robotic Manipulation
     To address this, we introduce ManiAgent, an agentic architecture for general manipulation tasks that achieves end-to-end output from task descriptions and environmental inputs to robotic manipulation actions. Evaluations show ManiAgent achieves an 86.8% success rate on the SimplerEnv benchmark and 95.8% on real-world pick-and-place tasks, enabling efficient data collection that yields VLA models with performance comparable to those trained on human-annotated datasets.

P033 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2603.25333] Adaptive Chunking: Optimizing Chunking-Method Selection for RAG
     To support this framework, we also introduce two new chunkers, an LLM-regex splitter and a split-then-merge recursive splitter, alongside targeted post-processing techniques. Without changing models or prompts, our framework increases RAG outcomes, raising answers correctness to 72% (from 62-64%) and increasing the number of successfully answered questions by over 30% (65 vs. 49). These results demonstrate that adaptive, document-aware chunking, guided by a complementary suite of intrinsic metrics, offers a practical and effective path to more robust RAG systems.

P034 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2606.03458] KVarN: Variance-Normalized KV-Cache Quantization Mitigates Error Accumulation in Reasoning Tasks
     KV-cache quantization can help improve this, but current methods are evaluated under prefill-like settings and errors behave differently under autoregres… We show that in the latter regime, quantization errors accumulate across timesteps, driven primarily by incorrect token scales. We introduce KVarN, a calibration-free KV-cache quantizer that applies a Hadamard rotation followed by a dual-scaling variance normalization across both axes of the K and V matrices. We find that this combination fixes outlying token-scale errors and substantially reduces error accumulation over existing baselines.

P035 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2603.23791] The Cognitive Firewall:Securing Browser Based AI Agents Against Indirect Prompt Injection Via Hybrid Edge Cloud Defense
     We present the Cognitive Firewall, a three-stage split-compute architecture that distributes security checks across the client and the cloud. In contrast, the full hybrid architecture reduces the overall attack success rate (ASR) to below 1% (0.88% under static evaluation and 0.67% under adaptive evaluation), while maintaining deterministic constraints on side-effecting actions. By filtering presentation-layer attacks locally, the system avoids unnecessary cloud inference and achieves an approximately 17,000x latency advantage over cloud-only baselines.

P036 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2410.12837] A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions
     This paper presents a comprehensive study of Retrieval-Augmented Generation (RAG), tracing its evolution from foundational concepts to the current state of the art. Future research directions are proposed, focusing on improving the robustness of RAG models, expanding the scope of application of RAG models, and addressing societal implications. This survey aims to serve as a foundational resource for researchers and practitioners in understanding the potential of RAG and its trajectory in natural language processing.

P037 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2605.15030] WARD: Adversarially Robust Defense of Web Agents Against Prompt Injections
     To address these limitations, we propose WARD (Web Agent Robust Defense against Prompt Injection), a practical guard model for secure and efficient web agents. WARD is built on WARD-Base, a large-scale dataset with around 177K samples collected from 719 high-traffic URLs and platforms, and WARD-PIG, a dedicated dataset designed for prompt injection attacks targeting the guard model. Extensive experiments show that WARD achieves nearly perfect recall on out-of-distribution benchmarks, maintains low false positive rates to preserve agent utility, remains robust against guard-targeted and adapt…

P038 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2503.24358] SQuat: Subspace-orthogonal KV Cache Quantization
     It reduces redundant computation at the cost of increased memory usage. To mitigate this overhead, existing approaches compress KV tensors into lower-bit representations; however, quantization errors can accumulate as more tokens are generated, potentially resulting in undesired outputs. In this paper, we introduce SQuat (Subspace-orthogonal KV cache quantization). Through numerical experiments, we show that our method reduces peak memory by 2.17 to 2.82, improves throughput by 2.45 to 3.60, and achieves more favorable benchmark scores than existing KV cache quantization algorithms.

P039 | Q: 요즘 speculative decoding 연구 동향 정리해줘
     [2412.19925] HADES: Hardware Accelerated Decoding for Efficient Speculation in Large Language Models
     However, the increasing demand for more sophisticated LLMs presents significant computational challenges due to their scale and complexity. This paper introduces Hardware Accelerated Decoding (HADES), a novel approach to enhance the performance and energy efficiency of LLMs. Our work demonstrates how speculative decoding can significantly improve the efficiency of LLM operations, paving the way for more advanced and practical applications of these models.

P040 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2503.04856] M2S: Multi-turn to Single-turn jailbreak in Red Teaming for LLMs
     We introduce a novel framework for consolidating multi-turn adversarial ``jailbreak'' prompts into single-turn queries, significantly reducing the manual overhead required for adversarial testing of large language models (LLMs). Despite removing iterative back-and-forth interactions, these prompts preserve and often enhance adversarial potency: in extensive evaluations on the Multi-turn Human Jailbreak (MHJ) dataset, M2S methods achieve attack success rates from 70.6 percent to 95.9 percent across several state-of-the-art LLMs.

P041 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2501.12372] Is Long Context All You Need? Leveraging LLM's Extended Context for NL2SQL
     In particular, improvements in reasoning abilities and the expansion of context windows have opened new avenues for leveraging these powerful models. We show that long context LLMs are robust and do not get lost in the extended contextual information. Additionally, our long-context NL2SQL pipeline based on Google's \textit{gemini-pro-1.5} achieve strong performances on various benchmark datasets without finetuning and expensive self-consistency based techniques.

P042 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2509.26205] Human-Centered Evaluation of RAG outputs: a framework and questionnaire for human-AI collaboration
     Building on Gienapp's utility-dimension framework, we designed a human-centred questionnaire that assesses RAG outputs across 12 dimensions. Ultimately, we incorporated feedback from both a human rater and a human-LLM pair.

P043 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2505.24179] SALE : Low-bit Estimation for Efficient Sparse Attention in Long-context LLM Prefilling
     In this paper, we propose SALE, a fine-grained sparse attention method that accelerates the long-context prefilling stage of LLM with negligible loss in model accuracy. We implement a custom CUDA kernel optimized for our approach for hardware efficiency, reducing the additional overhead to approximately 11% of the full attention latency. Experiments on long-context benchmarks demonstrate that our method outperforms existing approaches in accuracy-efficiency trade-offs, achieving at least 3.36x speedups on Llama-3.1-8B for sequences longer than 64K while maintaining model quality.

P044 | Q: RAG에서 리랭킹 개선하는 연구들 정리해줘
     [2603.02153] Scaling Retrieval Augmented Generation with RAG Fusion: Lessons from an Industry Deployment
     Moreover, fusion introduces additional latency overhead due to query rewriting and larger candidate sets, without corresponding improvements in downstream effectiveness. Our analysis suggests that recall-oriented fusion techniques exhibit diminishing returns once realistic re-ranking limits and context budgets are applied. We conclude that retrieval-level improvements do not reliably translate into end-to-end gains in production RAG systems, and argue for evaluation frameworks that jointly consider retrieval quality, system efficiency, and downstream impact.

P045 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2601.14123] A Systematic Analysis of Chunking Strategies for Reliable Question Answering
     We derive actionable lessons for cost-efficient deployment: (i) overlap provides no measurable benefit and increases indexing cost; (ii) sentence chunking is the most cost-effective method, matching semantic chunking up to ~5k tokens; (iii) a "context cliff" reduces quality beyond ~2.5k tokens; and (iv) optimal context depends on the goal (semantic quality peaks at small contexts; exact match at larger ones).

P046 | Q: 월드 모델 최근 연구 동향 정리해줘
     [2407.00118] From Efficient Multimodal Models to World Models: A Survey
     This review explores the latest developments and challenges in MLMs, emphasizing their potential in achieving artificial general intelligence and as a pathway to world models. We discuss the integration of 3D generation and embodied intelligence to enhance world simulation capabilities and propose incorporating external rule systems for improved reasoning and decision-making.

P047 | Q: 프롬프트 인젝션 공격이랑 방어 연구 정리해줘
     [2501.00517] A Method for Enhancing the Safety of Large Model Generation Based on Multi-dimensional Attack and Defense
     To address this issue, this paper proposes a method based on constructing data aligned with multi-dimensional attack defense to enhance the generative security of large models. The core of our method lies in improving the effectiveness of safe alignment learning for large models by innova-tively increasing the diversity of attack instruction dimensions and the a… The final ex-perimental results demonstrate that our method can significantly improve the generative security of large models under complex instructional attacks, while also maintaining and enhancing the models' general capabilities.

P048 | Q: VLA 모델 연구들 정리해줘
     [2406.20095] LLaRA: Supercharging Robot Learning Data for Vision-Language Policy
     In this work, we introduce LLaRA: Large Language and Robotics Assistant, a framework that formulates robot action policy as visuo-textual conversations and enables an efficient transfer of a pretrained VLM into a powerful VLA, motivated by the success of visual instruction tuning in Computer Vision. Through experiments across multiple simulated and real-world tasks, we demonstrate that LLaRA achieves state-of-the-art performance while preserving the generalization capabilities of large language models.

P049 | Q: VLA 모델 연구들 정리해줘
     [2412.10345] TraceVLA: Visual Trace Prompting Enhances Spatial-Temporal Awareness for Generalist Robotic Policies
     In this work, we introduce visual trace prompting, a simple yet effective approach to facilitate VLA models' spatial-temporal awareness for action prediction by encoding state-action trajectories visually. Evaluations of TraceVLA across 137 configurations in SimplerEnv and 4 tasks on a physical WidowX robot demonstrate state-of-the-art performance, outperforming OpenVLA by 10% on SimplerEnv and 3.5x on real-robot tasks and exhibiting robust generalization across diverse embodiments and scenarios.

P050 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2606.26080] Neglected Free Lunch from Post-training: Progress Advantage for LLM Agents
     In this work, we show that reinforcement learning (RL) post-training already provides the ingredients for effective step-level scoring, eliminating the need for dedicated reward model training altogether. We validate the effectiveness of the progress advantage across three different applications: test-time scaling, uncertainty quantification, and failure attribution on five benchmarks and four model families. Across all settings, it consistently outperforms confidence-based baselines and, despite requiring no task-specific training, surpasses dedicated trained reward models.

P051 | Q: RAG에서 리랭킹 개선하는 연구들 정리해줘
     [2602.03652] RAGTurk: Best Practices for Retrieval Augmented Generation in Turkish
     Our results show that complex methods like HyDE maximize accuracy (85%) that is considerably higher than the baseline (78.70%). Also a Pareto-optimal configuration using Cross-encoder Reranking and Context Augmentation achieves comparable performance (84.60%) with much lower cost. We further demonstrate that over-stacking generative modules can degrade performance by distorting morphological cues, whereas simple query clarification with robust reranking offers an effective solution.

P052 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2412.17867] Evaluating and Enhancing LLMs for Multi-turn Text-to-SQL with Multiple Question Types
     To bridge this gap, we propose MMSQL, a comprehensive test suite designed to evaluate the question classification and SQL generation capabilities of LLMs by simulating real-world scenarios with diverse question types and multi-turn Q&A interactions. Our experiments demonstrate that this approach significantly enhances the model's ability to navigate the complexities of conversational dynamics, effectively handling the diverse and complex nature of user queries. Our dataset and code are publicly available at https://mcxiaoxiao.github.io/MMSQL.

P053 | Q: speculative decoding에서 드래프트 모델 학습이나 검증 단계를 개선한 연구 알려줘
     [2605.29343] Draft-OPD: On-Policy Distillation for Speculative Draft Models
     Yet OPD remains difficult for draft models, as they cannot reliably roll out complete sequences independently, whereas target-assisted generation makes the collected sequences follow the target distribution and thus eliminates the on-policy signal. We therefore propose Draft-OPD, which uses target-assisted rollout for stable continuations and replays drafting from the verification-exposed error positions. Experiments show that Draft-OPD achieves over $5\times$ lossless acceleration for thinking models across diverse tasks, improving over EAGLE-3 and DFlash by 23% and 13%.

P054 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2602.02557] The Alignment Curse: Cross-Modality Jailbreak Transfer in Omni-Models
     We first analyze the connection between modality alignment and cross-modality jailbreak transfer, showing that strong alignment can inadvertently propagate textual vulnerabilities to the audio modality, which we term… Our results show that text-transferred audio jailbreaks perform comparably to, and often better than, audio-based jailbreaks, establishing them as simple yet powerful baselines for future audio red-teaming. We further demonstrate strong cross-model transferability and show that text-transferred audio attacks remain effective even under a stricter audio-only access threat model.

P055 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2408.08067] RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation
     In this paper, we propose a fine-grained evaluation framework, RAGChecker, that incorporates a suite of diagnostic metrics for both the retrieval and generation modules. Meta evaluation verifies that RAGChecker has significantly better correlations with human judgments than other evaluation metrics. Using RAGChecker, we evaluate 8 RAG systems and conduct an in-depth analysis of their performance, revealing insightful patterns and trade-offs in the design choices of RAG architectures.

P056 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2602.05723] Mitigating Hallucination in Financial Retrieval-Augmented Generation via Fine-Grained Knowledge Verification
     To mitigate this inconsistency, we propose a Reinforcement Learning framework enhanced with Fine-grained Knowledge Verification (RLFKV). This reward offers more precise optimization signals, thereby improving alignment with the retrieved documents. Experiments conducted on the public Financial Data Description (FDD) task and our newly proposed FDD-ANT dataset demonstrate consistent improvements, confirming the effectiveness of our approach.

P057 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2512.24044] Jailbreaking Attacks vs. Content Safety Filters: How Far Are We in the LLM Safety Arms Race?
     To address this gap, we present the first systematic evaluation of jailbreak attacks targeting LLM safety alignment, assessing their success across the full inference pipeline, including both input and output filtering stages. Our findings yield two key insights: first, nearly all evaluated jailbreak techniques can be detected by at least one safety filter, suggesting that prior assessments may have overestimated the practical success of these attacks; second, while safety filters are effective in detection, there remains room to better balance recall and precision to further optimize protec…

P058 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2412.08585] TurboAttention: Efficient Attention Approximation For High Throughputs LLMs
     Recent Key-value (KV) cache quantization reduces memory bandwidth but still needs floating-point dequantization for att… We present TurboAttention, a comprehensive approach to enable quantized execution of attention that simultaneously addresses both memory and computational efficiency. Experimental results demonstrate that TurboAttention achieves 1.2-1.8x speedup in attention, reduces the KV cache size by over 4.4x, and enables up to 2.37x maximum throughput over the FP16 baseline while outperforming state-of-the-art quantization and compression techniques across various datasets and models.

P059 | Q: 멀티에이전트 강화학습에서 비정상성이나 부분 관측 같은 문제를 게임 이론(내시 균형, 진화 동역학) 관점에서 정리한 논문 요약해줘
     [2412.20523] Game Theory and Multi-Agent Reinforcement Learning : From Nash Equilibria to Evolutionary Dynamics
     This paper explores advanced topics in complex multi-agent systems building upon our previous work. We investigate how Nash equilibria, evolutionary game theory, correlated equilibrium, and adversarial dynamics can be effectively incorporated into MARL algorithms to improve learning outcomes. Through this comprehensive analysis, we demonstrate how the synthesis of game theory and MARL can enhance the robustness and effectiveness of multi-agent systems in complex, dynamic environments.

P060 | Q: VLA 모델 연구들 정리해줘
     [2604.20012] EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training
     In this work, we propose EmbodiedMidtrain to bridge the gap between VLMs and VLAs. Experiments on three robot manipulation benchmarks show that mid-training consistently improves performance across different VLM backbones, achieving results competitive with expert VLAs and off-the-shelf VLMs trained with larger model scale and training budgets. Further analysis reveals that mid-training provides a stronger initialization for VLA fine-tuning, with gains emerging from the earliest steps and widening throughout training.

P061 | Q: 요즘 LLM 양자화 연구들 정리해줘
     [2607.07964] KronQ: LLM Quantization via Kronecker-Factored Hessian
     We propose KronQ, a PTQ framework that challenges this assumption by introducing the gradient covariance into the quantization pipeline. (1) KronQ introduces bidirectional incoherence processing, extending the existing input-side random rotation to the output dimension using the gradient covariance, reducing weight magnitude variance across both input and output dimensions. (2) KronQ derives a new sensitivity metric for inter-layer mixed-precision allocation, driven by the gradient and activation Hessian traces.

P062 | Q: 시계열 예측 관련 논문 5개 찾아줘
     [2405.16312] Time-SSM: Simplifying and Unifying State Space Models for Time Series Forecasting
     To address this gap, this paper proposes a novel theoretical framework termed Dynamic Spectral Operator, offering more intuitive and general guidance on applying SSMs to time series data. Building upon our theory, we introduce Time-SSM, a novel SSM-based foundation model with only one-seventh of the parameters compared to Mamba.

P063 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2508.15437] Test-time Corpus Feedback: From Retrieval to RAG
     This static design often limits performance on complex tasks that require iterative evidence gathering or high-precision retrieval. Recent work in both the information retrieval (IR) and NLP communities has begun to close this gap by introducing adaptive retrieval and ranking methods that incorporate feedback. In this survey, we present a structured overview of advanced retrieval and ranking mechanisms that integrate such feedback. We categorize feedback signals based on their source and role in improving the query, retrieved context, or document pool.

P064 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2406.16008] Found in the Middle: Calibrating Positional Attention Bias Improves Long Context Utilization
     Second, we mitigate this positional bias through a calibration mechanism, found-in-the-middle, that allows the model to attend to contexts faithfully according to their relevance, even thoug… Third, we show found-in-the-middle not only achieves better performance in locating relevant information within a long context, but also eventually leads to improved retrieval-augmented generation (RAG) performance across various tasks, outperforming existing methods by up to 15 percentage points. These findings open up future directions in understanding LLM attention bias and its potential consequences.

P065 | Q: RAG의 검색 정확도를 높이는 논문들을 분석해 보고, 아직 사람들이 시도하지 않은 '연구의 빈틈(Research Gap)'을 3가지 제안해 봐
     [2408.08067] RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation
     In this paper, we propose a fine-grained evaluation framework, RAGChecker, that incorporates a suite of diagnostic metrics for both the retrieval and generation modules. Meta evaluation verifies that RAGChecker has significantly better correlations with human judgments than other evaluation metrics. Using RAGChecker, we evaluate 8 RAG systems and conduct an in-depth analysis of their performance, revealing insightful patterns and trade-offs in the design choices of RAG architectures.

P066 | Q: LLM 에이전트가 쓰는 도구가 오류를 내도 티가 안 나는 경우, 모델이 그걸 알아채는지 다룬 논문 있어? 핵심 내용 설명해줘
     [2606.05806] When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents
     We introduce ToolMaze, a benchmark for dynamic path discovery and error recovery in TIR agents. Driven by systemic over-trust in corrupted outputs, Perturbation Recovery Rate (PRR) plummets by around 37% in these scenarios, while complex topologies trap agents in futile trial-and-error loops. Crucially, agentic fault-tolerance improves with model scale$3.66\times$ slower than basic task execution, highlighting dynamic replanning as a distinct bottleneck unaddressed by model scaling or prompting.

P067 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2412.15623] JailPO: A Novel Black-box Jailbreak Framework via Preference Optimization against Aligned LLMs
     To address these issues, we present JailPO, a novel black-box jailbreak framework to examine LLM alignment. Extensive experiments demonstrate that JailPO not only automates the attack process while maintaining effectiveness but also exhibits superior performance in efficiency, universality, and robustness against defenses compared to baselines. Additionally, our analysis of the three JailPO patterns reveals that attacks based on complex templates exhibit higher attack strength, whereas covert question transformations elicit riskier responses and are more likely to bypass defense mechanisms.

P068 | Q: 생성 모델 워터마크 연구들 정리해줘
     [2412.15278] DreaMark: Rooting Watermark in Score Distillation Sampling Generated Neural Radiance Fields
     With the rapid advancement in NeRF generation quality, protecting the copyright of the generated NeRF has become increasingly important. To address both issues, we propose Dreamark to embed a secret message by backdooring the NeRF during NeRF generation. We evaluate the generation quality and watermark robustness against image- and model-level attacks. Extensive experiments show that the watermarking process will not degrade the generation quality, and the watermark achieves 90+% accuracy among both image-level attacks (e.g., Gaussian noise) and model-level attacks (e.g., pruning attack).

P069 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2503.24358] SQuat: Subspace-orthogonal KV Cache Quantization
     It reduces redundant computation at the cost of increased memory usage. To mitigate this overhead, existing approaches compress KV tensors into lower-bit representations; however, quantization errors can accumulate as more tokens are generated, potentially resulting in undesired outputs. In this paper, we introduce SQuat (Subspace-orthogonal KV cache quantization). Through numerical experiments, we show that our method reduces peak memory by 2.17 to 2.82, improves throughput by 2.45 to 3.60, and achieves more favorable benchmark scores than existing KV cache quantization algorithms.

P070 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2406.19644] Beyond Human Preferences: Exploring Reinforcement Learning Trajectory Evaluation and Improvement through LLMs
     To tackle this challenge, we propose a LLM-enabled automatic preference generation framework named LLM4PG , which harnesses the capabilities of large language models (LLMs) to abstract trajectories, rank preferences, and reconstruct reward functions to optimize conditioned policies. Experiments on tasks with complex language constraints demonstrated the effectiveness of our LLM-enabled reward functions, accelerating RL c… This approach mitigates the reliance on specialized human knowledge and demonstrates the potential of LLMs to enhance RL's effectiveness in complex environments in the wild.

P071 | Q: 프롬프트 인젝션 공격이랑 방어 연구 정리해줘
     [2606.15441] Defending against Adaptive Prompt Injection Attacks via Reasoning-enabled Task Alignment
     To address these gaps, we propose RETA, a training-based method that grounds defense decisions on the user tasks rather than attacker-controlled data. Together, these allow the defender to be optimized via multi-objective reinforcement learning and achieve better safety-utility trade-off. Across six black-box adaptive attacks, RETA keeps every per-attack ASR below 10%, with average ASR of 2.92% and 3.75% on the two target models, while preserving most utility under attack and on clean inputs.

P072 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2402.15727] LLMs Can Defend Themselves Against Jailbreaking in a Practical Manner: A Vision Paper
     This paper proposes a lightweight yet practical defense called SELFDEFEND, which can defend against all existing jailbreak attacks with minimal delay for jailbreak prompts and negligible delay for normal user prompts. Our key insight is that regardless of the kind of jailbreak strategies employed, they eventually need to include a harmful prompt (e.g., "how to make a bomb") in the prompt sent to LLMs, and we found that existing LLMs can effectively recognize such harmful prompts t… We demonstrate our idea of SELFDEFEND works in various jailbreak scenarios through manual analysis in GPT-3.5/4.

P073 | Q: LLM 환각을 탐지하는 연구나 완화하는 연구 알려줘
     [2309.01219] Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models
     We present taxonomies of the LLM hallucination phenomena and evaluation benchmarks, analyze existing approaches aiming at mitigating LLM hallucination, and discuss potential directions for future research.

P074 | Q: LLM 환각 탐지 방법 논문들 비교해서 정리해줘
     [2311.05232] A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions
     Subsequently, we present a thorough overview of hallucination detection methods and benchmarks. Additionally, we delve into the current limitations faced by retrieval-augmented LLMs in combating hallucinations, offering insights for developing more robust IR systems.

P075 | Q: VLA 모델 연구들 정리해줘
     [2607.07608] Dual Latent Memory in Vision-Language-Action Models for Robotic Manipulation
     To this end, we introduce LaMem-VLA, a latent-memory-native framework that reconstructs historical experience into latent memory tokens and directly interweaves them with VLA reasoning. Extensive experiments on SimplerEnv and LIBERO demonstrate the superiority of our LaMem-VLA.

P076 | Q: LLM 환각을 탐지하는 연구나 완화하는 연구 알려줘
     [2501.08292] HALoGEN: Fantastic LLM Hallucinations and Where to Find Them
     In this work, we release HALoGEN, a comprehensive hallucination benchmark consisting of: (1) 10,923 prompts for generative models spanning nine domains including programming, scientific attribution, and summarization, and (2) automatic high-precision verifiers for each use case that decompose LLM generations into atomic units, and verify each unit against a high-qua… We use this framework to evaluate ~150,000 generations from 14 language models, finding that even the best-performing models are riddled with hallucinations (sometimes up to 86% of generated atomic facts depending on the domain).

P077 | Q: LLM 코드 생성 연구들 어떤 방향으로 가고 있어?
     [2412.14222] A Survey on Large Language Model-based Agents for Statistics and Data Science
     This survey provides an overview of the evolution, capabilities, and applications of LLM-based data agents, highlighting their role in simplifying complex da… We explore current trends in the design of LLM-based frameworks, detailing essential features such as planning, reasoning, reflection, multi-agent collaboration, user interface, knowledge integration, and system design, which enable agents to address data-centric problems with minimal human intervention. Furthermore, we analyze several case studies to demonstrate the practical applications of various data agents in real-world scenarios.

P078 | Q: 지식 증류 관련 논문들 동향 알려줘
     [2412.09388] All You Need in Knowledge Distillation Is a Tailored Coordinate System
     Experiments show that TCS achieves significantly higher accuracy than state-of-the-art KD methods, while only requiring roughly half of their training time and GPU memory costs.

P079 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2402.05131] Financial Report Chunking for Effective Retrieval Augmented Generation
     This approach treats all texts as equal and neglects the information contained in the structure of documents. We propose an expanded approach to chunk documents by moving beyond mere paragraph-level chunking to chunk primary by structural element components of documents. We also demonstrate how this approach impacts RAG assisted Question & Answer task performance. Findings support that element type based chunking largely improve RAG results on financial reporting.

P080 | Q: RAG에서 노이즈 문서나 방해 문서에 대한 강건성을 다룬 연구 찾아줘
     [2601.01896] Tackling the Inherent Difficulty of Noise Filtering in RAG
     Therefore, LLMs must be robust against such noise, but we demonstrate that standard fine-tuning approaches are often ineffective in enabling the model to selectively utilize relevant information while ignoring irrelevant content due to the structural constraints of attention patte… To address this, we propose a novel fine-tuning method designed to enhance the model's ability to distinguish between relevant and irrelevant information within retrieved documents. Extensive experiments across multiple benchmarks show that our approach significantly improves the robustness and performance of LLMs.

P081 | Q: 생성 모델 워터마크에서 이미지·영상 워터마크나 텍스트·에이전트 워터마크 연구 있어?
     [2506.10030] Safeguarding Multimodal Knowledge Copyright in the RAG-as-a-Service Environment
     In this work, we propose AQUA, the first watermark framework for image knowledge protection in Multimodal RAG systems. Experiments across diverse models and datasets show that AQUA enables robust, stealthy, and reliable copyright tracing, filling a key gap in multimodal RAG protection.

P082 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2410.01066] From Natural Language to SQL: Review of LLM-based Text-to-SQL Systems
     We discuss benchmarks, evaluation methods, and evaluation metrics. Also, we uniquely study the use of Graph RAGs for better contextual accuracy and schema linking in these systems. Finally, we highlight key challenges such as computational efficiency, model robustness, and data privacy toward improvements of LLM-based text-to-SQL systems.

P083 | Q: RAG에서 노이즈 문서나 방해 문서에 대한 강건성을 다룬 연구 찾아줘
     [2512.01183] TempPerturb-Eval: On the Joint Effects of Internal Temperature and External Perturbations in RAG Robustness
     This work presents a systematic investigation of how text perturbations (simulating noisy retrieval) interact with temperature settings across multiple LLM runs. Through extensive experiments on HotpotQA with both open-source and proprietary LLMs, we demonstrate that performance degradation follows distinct patt… Our work yields three key contributions: (1) a diagnostic benchmark for assessing RAG robustness, (2) an analytical framework for quantifying perturbation-temperature interactions, and (3) practical guidelines for model selection and parameter tuning under noisy retrieval conditions.

P084 | Q: 비전-언어 모델 환각을 줄이는 방법이나 탐지하는 방법 연구 있어?
     [2410.15778] Reducing Hallucinations in Vision-Language Models via Latent Space Steering
     Inspired by this, we introduce Visual and Textual Intervention (VTI), a novel technique designed to reduce hallucinations by steering latent space representations during inference to enhance the stability of vision features. Extensive experiments demonstrate that it can effectively reduce hallucinations and outperform baseline methods across multiple metrics, highlighting the critical role of vision feature stability in LVLMs.

P085 | Q: 월드 모델 최근 연구 동향 정리해줘
     [2605.23993] Nano World Models: A Minimalist Implementation of Future Video Prediction
     We introduce Nano World Models, a minimalist codebase for future video prediction centered around diffusion forcing. Nano World Models provides a unified interface for generative objectives, model scales, action-conditioning mechanisms, latent observation spaces, datasets, evaluation protocols, and long-horizon rollout procedures.

P086 | Q: 연합학습에서 통신 효율이나 차등 프라이버시를 다룬 연구 있어?
     [2412.11674] UA-PDFL: A Personalized Approach for Decentralized Federated Learning
     Nonetheless, DFL still suffers from training degradation as FL does due to the non-independent and identically distributed (non-IID) nature of client data. Therefore, in this paper, we propose a novel unit representation aided personalized decentralized federated learning framework, named UA-PDFL, to deal with the non-IID challenge in DFL. Based on this scheme, client-wise dropout and layer-wise personalization are proposed to further enhance the learning performance of DFL.

P087 | Q: 월드 모델 최근 연구 동향 정리해줘
     [2604.27895] Graph World Models: Concepts, Taxonomy, and Future Directions
     To address these limitations, many recent studies use graph structure to decompose the environment into entity nodes and interactive edges, and model virtual environments in a structured space. Furthermore, we propose a taxonomy based on relational inductive biases (RIB), categorizing GWMs by the specific structural priors they inject: (1) spatial RIB for topological abstraction; (2) physical RIB for dynamic simulation; and (3) logical RIB for causal and semantic reasoning.

P088 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2610.13767] DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs
     In this work, we introduce DUALQUANT, a dual-scale, calibration-free post-training quantization framework that directly minimizes the weight-reconstruction Mean Squared Error (MSE) and, as an immediate by-product, yields per-channel activation rescalings prior to activation quantization. We validate these gains with a real packed W4A4 inference path for Llama-3.1-8B on an RTX 4090. The resulting implementation closely matches the accuracy of fake quantization while delivering up to 2.61x memory reduction and up to 2.46x throughput speedup over BF16.

P089 | Q: 월드 모델 최근 연구 동향 정리해줘
     [2606.18208] Looped World Models
     This yield up to 100x parameter efficiency over conventional approaches with adaptive computation that automatically scales depth to match the complexity of each prediction step.

P090 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2506.10408] Reasoning RAG via System 1 or System 2: A Survey on Reasoning Agentic Retrieval-Augmented Generation for Industry Challenges
     While early RAG systems based on static pipelines have shown effectiveness in well-structured tasks, they struggle in real-world scenarios requiring complex reasoning, dynamic retrieval, and multi-modal integration. In this paper, we present a comprehensive review of Reasoning Agentic RAG methods, categorizing them into two primary systems: predefined reasoning, which follows fixed modular pipelines to boost reasoning, and agentic reasoning, where the model autonomously orchestrates tool interaction during inference.

P091 | Q: 요즘 speculative decoding 연구 동향 정리해줘
     [2610.10411] Training Parallel Speculative Draft Models by Directly Minimizing Expected Decoding Rounds
     Parallel and semi-autoregressive (semi- AR) drafters improve drafting efficiency by proposing an entire block in a single forward pass, but training them raises a new difficulty: the draft distribution for a g… In this work, we develop a theoretical framework for training and evaluating these drafters by representing speculative decoding as a Markov reward process. Finetuning two state-of-the- art drafters, DSpark and DFly, with EDR consistently improves mean accepted length and outperforms existing training objectives across nine benchmarks spanning math reasoning, code generation, and chat.

P092 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2603.04406] CTRL-RAG: Contrastive Likelihood Reward Based Reinforcement Learning for Context-Faithful RAG Models
     To tackle these issues, we propose a novel "internal-external" hybrid reward framework centered on a Contrastive Likelihood Reward (CLR). This encourages the model to extract relevant evidence and increases its confidence when grounded in a specific context. Experiments show that our method (used alone or combined with external correctness rewards) achieves strong performance on singlehop, multi-hop, vertical-domain, and faithfulness benchmarks.

P093 | Q: 월드 모델 최근 연구 동향 정리해줘
     [2610.26844] AnyGoal: On World Model Generalization Beyond Expert Rollouts
     To answer this, we introduce AnyGoal, a benchmark of goal-shifted task variants built from widely used world-model environments, together with an open-source library. Across multiple environments and world model families, we find that current models consistently exhibit failures under these recombinations.

P094 | Q: RAG에서 검색된 문서의 순서나 개수가 답변 품질에 주는 영향을 분석한 연구 찾아줘
     [2604.07274] A Systematic Study of Retrieval Pipeline Design for Retrieval-Augmented Medical Question Answering
     This study presents a systematic evaluation of retrieval-augmented medical question answering using the MedQA USMLE benchmark and a structured textbook-based knowledge corpus. The best-performing configuration was dense retrieval with query reformulation and reranking achieved 60.49% accuracy. All experiments were conducted on a single consumer-grade GPU, demonstrating that systematic evaluation of retrieval-augmented medical QA systems can be performed under modest computational resources.

P095 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2412.12192] No Free Lunch for Defending Against Prefilling Attack by In-Context Learning
     In this paper, we: (1) show that ICL can effectively defend against prefilling jailbreak attacks by employing adversative sentence structures within demonstrations; (2) characterize the effectiveness of this defense through the lens of model size, number of demonstrations, over-defense, integration with other jailbreak attacks, and the presence of safety alignment. On the other hand, LLMs exhibit similar over-defensiveness when utilizing ICL demonstrations with adversative structures, and this behavior appears to be independent of model size.

P096 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2309.10253] GPTFUZZER: Red Teaming Large Language Models with Auto-Generated Jailbreak Prompts
     In this paper, we introduce GPTFuzz, a novel black-box jailbreak fuzzing framework inspired by the AFL fuzzing framework. We evaluate GPTFuzz against various commercial and open-source LLMs, including ChatGPT, LLaMa-2, and Vicuna, under diverse attack scenarios. Our results indicate that GPTFuzz consistently produces jailbreak templates with a high success rate, surpassing human-crafted templates. Remarkably, GPTFuzz achieves over 90% attack success rates against ChatGPT and Llama-2 models, even with suboptimal initial seed templates.

P097 | Q: 프롬프트 인젝션 공격이랑 방어 연구 정리해줘
     [2606.12737] PI-Hunter: Automated Red-Teaming for Exposing and Localizing Prompt Injections
     We propose PI-Hunter, an automated agentic auditing framework for proactive vulnerability exposure in LLM agents. PI-Hunter constructs realistic source-aware test cases and iteratively evolves them through feedback-driven exploration to induce agents to retrieve and reveal latent malicious… Extensive experiments across multiple benchmarks, agent architectures, attacks, and defenses demonstrate that PI-Hunter substantially improves vulnerability exposure and attack-surface coverage over strong automated red-teaming baselines, while remaining effective under existing prompt injection defenses.

P098 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2503.20320] Iterative Prompting with Persuasion Skills in Jailbreaking Large Language Models
     Our results show that the attack success rates (ASR) increase as the attacking prompts become more refined with the highest ASR of 90% for GPT4 and ChatGLM and the lowest ASR of 68% for LLaMa2. Our technique outperforms baseline techniques (PAIR and PAP) in ASR and shows comparable performance with GCG and ArtPrompt.

P099 | Q: speculative decoding에서 드래프트 모델 학습이나 검증 단계를 개선한 연구 알려줘
     [2610.10411] Training Parallel Speculative Draft Models by Directly Minimizing Expected Decoding Rounds
     Parallel and semi-autoregressive (semi- AR) drafters improve drafting efficiency by proposing an entire block in a single forward pass, but training them raises a new difficulty: the draft distribution for a g… In this work, we develop a theoretical framework for training and evaluating these drafters by representing speculative decoding as a Markov reward process. Finetuning two state-of-the- art drafters, DSpark and DFly, with EDR consistently improves mean accepted length and outperforms existing training objectives across nine benchmarks spanning math reasoning, code generation, and chat.

P100 | Q: speculative decoding에서 드래프트 모델 학습이나 검증 단계를 개선한 연구 알려줘
     [2407.08223] Speculative RAG: Enhancing Retrieval Augmented Generation through Drafting
     In this work, we introduce Speculative RAG - a framework that leverages a larger generalist LM to efficiently verify multiple RAG drafts produced in parallel by a smaller, distilled specialist LM. Extensive experiments demonstrate that Speculative RAG achieves state-of-the-art performance with reduced latency on TriviaQA, MuSiQue, PopQA, PubHealth, and ARC-Challenge benchmarks. It notably enhances accuracy by up to 12.97% while reducing latency by 50.83% compared to conventional RAG systems on PubHealth.

P101 | Q: VLA 모델 연구들 정리해줘
     [2503.22020] CoT-VLA: Visual Chain-of-Thought Reasoning for Vision-Language-Action Models
     In this paper, we introduce a method that incorporates explicit visual chain-of-thought (CoT) reasoning into vision-language-action models (VLAs) by predicting future image frames autoregressively as visual goals before generating a short action sequence to achieve these goals. Our experimental results demonstrate that CoT-VLA achieves strong performance, outperforming the state-of-the-art VLA model by 17% in real-world manipulation tasks and 6% in simulation benchmarks.

P102 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2602.09552] Comprehensive Comparison of RAG Methods Across Multi-Domain Conversational QA
     This paper addresses the lack of a systematic comparison of RAG methods for multi-turn conversational QA, where dialogue history, coreference, and shifting user intent substantially complicate retrieval. We present a comprehensive empirical study of vanilla and advanced RAG methods across eight diverse conversational QA datasets spanning multiple domains. Overall, our findings indicate that effective conversational RAG depends less on method complexity than on alignment between the retrieval strategy and the dataset structure.

P103 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2412.21001] LEASE: Offline Preference-based Reinforcement Learning with High Sample Efficiency
     To solve this, this paper proposes a offLine prEference-bAsed RL with high Sample Efficiency (LEASE) algorithm, where a learned transition model is leveraged to generate unlabeled preference data. Moreover, we provide the generalization bound of reward model to analyze the factors influencing reward accuracy, and demonstrate that the policy learned by LEASE has theoretical improvement guarantee. The experimental results show that LEASE can achieve comparable performance to baseline under fewer preference data without online interaction.

P104 | Q: 비전-언어 모델 환각을 줄이는 방법이나 탐지하는 방법 연구 있어?
     [2604.00455] First Logit Boosting: Visual Grounding Method to Mitigate Object Hallucination in Large Vision-Language Models
     In this paper, we propose First Logit Boosting (FLB), a simple yet effective training-free technique designed to alleviate long-term decay in LVLMs. We observe that FLB (1) sustains the visual information embedded in the first token throughout generation, and (2) suppresses hallucinated words through the stabilizing effect of the ``The'' token. Experimental results show that FLB significantly reduces object hallucination across various tasks, benchmarks, and backbone models.

P105 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2412.12300] Unanswerability Evaluation for Retrieval Augmented Generation
     In this paper, we introduce UAEval4RAG, a framework designed to evaluate whether RAG systems can handle unanswerable queries effectively. We conduct experiments with various RAG components, including retrieval models, rewriting methods, rerankers, language models, and prompting strategies, and reveal hidden trade-offs in performance of RAG systems. Our findings highlight the critical role of component selection and prompt design in optimizing RAG systems to balance the accuracy of answerable queries with high rejection rates of unanswerable ones.

P106 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2408.01262] RAGEval: Scenario Specific RAG Evaluation Dataset Generation Framework
     This paper introduces RAGEval, a framework designed to assess RAG systems across diverse scenarios by generating high-quality documents, questions, answers, and references through a schema-based pipeline. Experimental results show that RAGEval outperforms zero-shot and one-shot methods in terms of clarity, safety, conformity, and richness of generated samples. Furthermore, the use of LLMs for scoring the proposed metrics demonstrates a high level of consistency with human evaluations.

P107 | Q: 지식 증류 관련 논문들 동향 알려줘
     [2209.07521] On-Device Domain Generalization
     We present a systematic study of domain generalization (DG) for tiny neural networks. Another interesting observation is that the teacher-student gap on out-of-distribution data is bigger than that on in-distribution data, which highlights the capacity mismatch issue as well as the shortcoming of KD. Without adding any extra parameter to the model -- hence keeping the deployment cost unchanged -- OKD significantly improves DG performance for tiny neural networks in a variety of on-device DG scenarios for image and speech applications.

P108 | Q: LLM 환각을 탐지하는 연구나 완화하는 연구 알려줘
     [2508.01781] A comprehensive taxonomy of hallucinations in Large Language Models
     Furthermore, the report examines cognitive and human factors influencing hallucination perception, surveys evaluation benchmarks and metrics for detection, and outlines architectural and systemic mitigation strategies.

P109 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2504.07803] A System for Comprehensive Assessment of RAG Frameworks
     To address this gap, we introduce SCARF (System for Comprehensive Assessment of RAG Frameworks), a modular and flexible evaluation framework designed to benchmark deployed RAG applications systematically. SCARF provides an end-to-end, black-box evaluation methodology, enabling a limited-effort comparison across diverse RAG frameworks. Using the REST APIs interface, we demonstrate how SCARF can be applied to real-world scenarios, showcasing its flexibility in assessing different RAG frameworks and configurations.

P110 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2601.07838] A survey: Information search time optimization based on RAG (Retrieval Augmentation Generation) chatbot
     Retrieval-Augmented Generation (RAG) based chatbots are not only useful for information retrieval through questionanswering but also for making complex decisions based on injected private data.we present a survey on how much search time can be saved when retrieving complex information within an organization called "X Systems"(a stealth mode company) by using a RAG-based chatbot compared to traditional search methods. Comparison shows us, there are average 80-95% improvement on search when use RAG based chatbot than using standard search.

P111 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2607.09683] Ablation, Statistical Inference, and Validation for KV-Cache Compression
     Key findings reveal that while eigenbasis-based methods fail on heavy-tailed data due to covariance instability, they excel in structured regimes, with the effective semantic dimension ($d_{eff}$) adapting to calibration budgets rather than true data rank.

P112 | Q: speculative decoding에서 드래프트 모델 학습이나 검증 단계를 개선한 연구 알려줘
     [2604.02047] Goose: Anisotropic Speculation Trees for Training-Free Speculative Decoding
     We observe that two common training-free token sources - n-gram matches copied from the input context, and statistical predictions from prior forward passes - differ dramatically in acceptance rate (~6x median gap, range 2-18x across five models and five benchmarks). We realize this structure in GOOSE, a training-free framework that builds an adaptive spine tree - a deep chain of high-acceptance context-matched tokens with wide branches o… On five LLMs (7B-33B) and five benchmarks, GOOSE achieves 1.9-4.3x lossless speedup, outperforming balanced-tree baselines by 12-33% under the same budget.

P113 | Q: 요즘 speculative decoding 연구 동향 정리해줘
     [2605.02888] SpecKV: Adaptive Speculative Decoding with Compression-Aware Gamma Selection
     In this paper, we present \textbf{SpecKV}, a lightweight adaptive controller that selects~$γ$ per speculation step using signals extracted from the draft model itself. We demonstrate that the optimal~$γ$ shifts across compression regimes and that draft model confidence and entropy are stron… SpecKV uses a small MLP trained on these signals to maximize expected tokens per speculation step, achieving a 56.0% improvement over the fixed-$γ$=4 baseline with only 0.34\,ms overhead per decision ($<$0.5% of step time). The improvement is statistically significant ($p < 0.001$, paired bootstrap test).

P114 | Q: LLM 환각 탐지 방법 논문들 비교해서 정리해줘
     [2508.01781] A comprehensive taxonomy of hallucinations in Large Language Models
     Furthermore, the report examines cognitive and human factors influencing hallucination perception, surveys evaluation benchmarks and metrics for detection, and outlines architectural and systemic mitigation strategies.

P115 | Q: LLM 환각 탐지 방법 논문들 비교해서 정리해줘
     [2507.19024] A Survey of Multimodal Hallucination Evaluation and Detection
     This survey offers an in-depth review of hallucination evaluation benchmarks and detection methods across Image-to-Text (I2T) and Text-to-image (T2I) generation tasks. Specifically, we first propose a taxonomy of hallucination based on faithfulness and factuality, incorporating the common types of hallucinations observed in practice. Finally, we highlight key limitations in current benchmarks and detection methods, and outline potential directions for future research.

P116 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2503.21602] GenEdit: Compounding Operators and Continuous Improvement to Tackle Text-to-SQL in the Enterprise
     To address these issues, we designed and implemented GenEdit: our Text-to-SQL generation system that improves with user feedback. GenEdit builds and maintains a company-specific knowledge set, employs a pipeline of operators decomposing SQL generation, and uses feedback to update its knowledge set to i… For generation, GenEdit leverages compounding operators to improve knowledge retrieval and to create a plan as chain-of-thought steps that guides generation. Once the feedback is submitted, it gets merged after passing regression testing and obtaining an approval, improving future generations.

P117 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2410.13846] LightTransfer: Your Long-Context LLM is Secretly a Hybrid Model with Effortless Adaptation
     In this work, we propose LightTransfer, a lightweight method that transforms models such as LLaMA into hybrid variants. Experiments across diverse benchmarks and models (e.g., LLaMA, Mistral, QwQ-STILL) demonstrate that, even when half of the layers are identified as lazy, LightTransfer achieves up to 2.17$\times$ throughput improvement with minimal performance loss ($<1.5%$ on LongBench) and achieves 53.3% on math benchmark AIME24 of advanced o1-like long reasoning model QwQ-STILL.

P118 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2407.19794] Introducing a new hyper-parameter for RAG: Context Window Utilization
     This paper introduces a new hyper-parameter for Retrieval-Augmented Generation (RAG) systems called Context Window Utilization. RAG systems enhance generative models by incorporating relevant information retrieved from external knowledge bases, improving the factua… Our findings reveal that an optimal chunk size balances the trade-off between providing sufficient context and minimizing irrelevant information. These insights are crucial for enhancing the design and implementation of RAG systems, underscoring the importance of selecting an appropriate chunk size to achieve superior performance.

P119 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2603.08819] Beyond Relevance: On the Relationship Between Retrieval and RAG Information Coverage
     Through experiments across two text RAG benchmarks (TREC NeuCLIR 2024 and TREC RAG 2024) and one multimodal benchmark (WikiVideo), we analyze 15 text retrieval stacks and 10 multimodal retrieval stacks across four RAG pipelines and multiple evaluation frameworks (Auto-ARGUE and MiRAGE). Our findings demonstrate strong correlations between coverage-based retrieval metrics and nugget coverage in generated responses at both topic and system levels. These findings provide empirical support for using retrieval metrics as proxies for RAG performance.

P120 | Q: 월드 모델 최근 연구 동향 정리해줘
     [2606.24597] Qwen-AgentWorld: Language World Models for General Agents
     (i) We first focus on building foundation models for agentic environment simulation. (ii) Beyond foundation models, we further investigate two complementary paradigms through which world modeling enhances ge… First, as a decoupled environment simulator, Qwen-AgentWorld supports scalable and controllable simulation of thousands of real-world environments for agentic RL, yielding gains that surpass real-environment training alone. Second, as a unified agent foundation model, world-model training acts as a highly effective warm-up that improves downstream performance across 7 agentic benchmarks.

P121 | Q: 연합학습 연구들 정리해줘
     [2412.15728] fluke: Federated Learning Utility frameworK for Experimentation and research
     In this paper, we present \fluke, a Python package designed to simplify the development of new FL algorithms.

P122 | Q: 연합학습에서 통신 효율이나 차등 프라이버시를 다룬 연구 있어?
     [2412.15728] fluke: Federated Learning Utility frameworK for Experimentation and research
     In this paper, we present \fluke, a Python package designed to simplify the development of new FL algorithms.

P123 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2412.12322] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems
     We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. The results also highlight the importance of prompt engineering in RAG systems, with our custom-prompted agents showing consistent improvements in retrieval accuracy and response quality.

P124 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2412.10321] AdvPrefix: An Objective for Nuanced LLM Jailbreaks
     We introduce AdvPrefix, a plug-and-play prefix-forcing objective that selects one or more model-dependent prefixes by combining two criteria: high prefilling attack success rates and low negative log-likelihood. AdvPrefix integrates seamlessly into existing jailbreak attacks to mitigate the previous limitations for free. For example, replacing GCG's default prefixes on Llama-3 improves nuanced attack success rates from 14% to 80%, revealing that current safety alignment fails to generalize to new prefixes.

P125 | Q: speculative decoding에서 드래프트 모델 학습이나 검증 단계를 개선한 연구 알려줘
     [2605.02888] SpecKV: Adaptive Speculative Decoding with Compression-Aware Gamma Selection
     In this paper, we present \textbf{SpecKV}, a lightweight adaptive controller that selects~$γ$ per speculation step using signals extracted from the draft model itself. We demonstrate that the optimal~$γ$ shifts across compression regimes and that draft model confidence and entropy are stron… SpecKV uses a small MLP trained on these signals to maximize expected tokens per speculation step, achieving a 56.0% improvement over the fixed-$γ$=4 baseline with only 0.34\,ms overhead per decision ($<$0.5% of step time). The improvement is statistically significant ($p < 0.001$, paired bootstrap test).

P126 | Q: 연합학습 연구들 정리해줘
     [2503.21154] Federated Learning with Differential Privacy: An Utility-Enhanced Approach
     To improve the privacy-utility trade-off, we present a modification to these vanilla differentially private algorithms based on a Haar wavelet transformation step and a novel noise injection scheme that significantly lowers the asymptotic bound of the noise variance. We also present a holistic convergence analysis of our proposed algorithm, showing that our method yields better convergence performance than the vanilla DP algo… Numerical experiments on real-world datasets demonstrate that our method outperforms existing approaches in model utility while maintaining the same privacy guarantees.

P127 | Q: RAG에서 검색된 문서의 순서나 개수가 답변 품질에 주는 영향을 분석한 연구 찾아줘
     [2402.05131] Financial Report Chunking for Effective Retrieval Augmented Generation
     This approach treats all texts as equal and neglects the information contained in the structure of documents. We propose an expanded approach to chunk documents by moving beyond mere paragraph-level chunking to chunk primary by structural element components of documents. We also demonstrate how this approach impacts RAG assisted Question & Answer task performance. Findings support that element type based chunking largely improve RAG results on financial reporting.

P128 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2511.10720] PISanitizer: Preventing Prompt Injection to Long-Context LLMs via Prompt Sanitization
     When extended to long-context scenarios, they have limited effectiveness. In this work, we propose PISanitizer, which first pinpoints and sanitizes potential injected tokens (if any) in a context before letting a backend LLM generate a response, thereby eliminating the influence of the injected instruction. To sanitize injected tokens, PISanitizer builds on two observations: (1) prompt injection attacks essentially craft an instruction that compels an LLM to follow it, and (2) LLMs intrinsically leverage the attention mechanism to focus on crucial input tokens for output generation.

P129 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2412.10321] AdvPrefix: An Objective for Nuanced LLM Jailbreaks
     We introduce AdvPrefix, a plug-and-play prefix-forcing objective that selects one or more model-dependent prefixes by combining two criteria: high prefilling attack success rates and low negative log-likelihood. AdvPrefix integrates seamlessly into existing jailbreak attacks to mitigate the previous limitations for free. For example, replacing GCG's default prefixes on Llama-3 improves nuanced attack success rates from 14% to 80%, revealing that current safety alignment fails to generalize to new prefixes.

P130 | Q: LLM 환각을 탐지하는 연구나 완화하는 연구 알려줘
     [2502.13490] What are Models Thinking about? Understanding Large Language Model Hallucinations "Psychology" through Model Inner State Analysis
     Considering the interpretability of LLM internal states and the fact that they do not require external information sources, we introduce such states into LLM hallucination detection. In this paper, we systematically analyze different internal states' revealing features during inference forward and comprehensively evaluate their ability in hallucination detection. Then, we introduce these internal states into hallucination detection and conduct comprehensive experiments to discuss the advantages and limitations.

P131 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2407.16833] Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach
     We benchmark RAG and LC across various public datasets using three latest LLMs. However, RAG's significantly lower cost remains a distinct advantage. Based on this observation, we propose Self-Route, a simple yet effective method that routes queries to RAG or LC based on model self-reflection. Self-Route significantly reduces the computation cost while maintaining a comparable performance to LC. Our findings provide a guideline for long-context applications of LLMs using RAG and LC.

P132 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2504.15364] KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments
     Based on the phenomenon we propose KeyDiff, a training-free KV cache eviction method based solely on key similarity. Under a strict memory allowance, we demonstrate the effectiveness of KeyDiff for the Llama and Qwen model families by observing a performance gap of less than 0.04% with 8K cache budget ($\sim$23% KV cache reduction) from the non-evicting baseline on LongBench for Llama 3.1-8B and Llama 3.2-3B. We also observe near baseline performance for Deepseek-R1-Distill-Llama-8B on the Math500 reasoning benchmark and decrease end-to-end inference latency by up to 30% compared to the othe…

P133 | Q: 연합학습 연구들 정리해줘
     [2503.22971] Enhancing Federated Learning Through Secure Cluster-Weighted Client Aggregation
     In FL, a global model is trained iteratively on local datasets residing on individual devices, each contributing to the model's improvement. To address this issue, this paper introduces a novel FL framework, ClusterGuardFL, that employs dissimilarity scores, k-means clustering, and reconciliation confidence scores to dynamically assign weights to client updates. Experimental results demonstrate the efficacy of the proposed approach in achieving improved model performance in diverse datasets.

P134 | Q: 연합학습 연구들 정리해줘
     [2412.11207] ProFe: Communication-Efficient Decentralized Federated Learning via Distillation and Prototypes
     Thus, this paper introduces ProFe, a novel communication optimization algorithm for DFL that combines knowledge distillation, prototype learning, and quantization techniques. ProFe utilizes knowledge from large local models to train smaller ones for aggregation, incorporates prototypes to better learn unseen classes, and applies quantization to reduce data transmit… Results showed that the proposed algorithm reduces communication costs by up to ~40-50% while maintaining or improving model performance. In addition, it adds ~20% training time due to increased complexity, generating a trade-off.

P135 | Q: 비전-언어 모델 환각을 줄이는 방법이나 탐지하는 방법 연구 있어?
     [2410.23114] Unified Triplet-Level Hallucination Evaluation for Large Vision-Language Models
     Most existing LVLM hallucination benchmarks are constrained to evaluate the object-related hallucinations. To remedy that, we design a unified framework to measure the object and relation hallucination in LVLMs simultaneously. Moreover, based on our findings, we design a simple training-free approach that effectively mitigates hallucinations for LVLMs.

P136 | Q: 지식 증류 관련 논문들 동향 알려줘
     [2412.09579] A Theoretical Analysis of Soft-Label vs Hard-Label Training in Neural Networks
     To address this, we first present motivating experimental results using simple neural network models on a binary classification problem. Specifically, we show that soft-label training using gradient descent requires only $O\left(\frac{1}{γ^2 ε}\right)$ neurons to achieve a classification lo… This implies that when $γ\leq ε$, i.e., when the dataset is challenging to classify, the neuron requirement for soft-label training can be significantly lower than that for hard-label training. Finally, we present experimental results on deep neural networks, further validating these theoretical findings.

P137 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2504.19754] Reconstructing Context: Evaluating Advanced Chunking Strategies for Retrieval-Augmented Generation
     Traditional methods address this by chunking external documents into smaller, fixed-size segments. While this approach alleviates input limitations, it often fragments context, resulting in incomplete retrieval and diminished coherence in generation. Despite their potential, their comparative strengths and limitations remain unclear. This study presents a rigorous analysis of late chunking and contextual retrieval, evaluating their effectiveness and efficiency in optimizing RAG systems. In contrast, late chunking offers higher efficiency but tends to sacrifice relevance and completeness.

P138 | Q: 요즘 speculative decoding 연구 동향 정리해줘
     [2412.12639] Falcon: Faster and Parallel Inference of Large Language Models through Enhanced Semi-Autoregressive Drafting and Custom-Designed Decoding Tree
     In this paper, we introduce Falcon, an innovative semi-autoregressive speculative decoding framework fashioned to augment both the drafter's parallelism and output quality. Additionally, we introduce a Custom-Designed Decoding Tree, which permits the drafter to generate multiple tokens in a single forward pass and accomm… Comprehensive evaluations on benchmark datasets such as MT-Bench, HumanEval, and GSM8K demonstrate Falcon's superior acceleration capabilities. The framework achieves a lossless speedup ratio ranging from 2.91x to 3.51x when tested on the Vicuna and LLaMA2-Chat model series.

P139 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2403.20137] Accurate Block Quantization in LLMs with Outliers
     In this paper, we focus on the most critical problem of limited KV-cache storage. We propose a novel approach enabling usage of low precision BFP formats without compromising the resulting model accuracy. We exploit the common channel-wise patterns exhibited by the outliers to rearrange them in such a way, that their quantization quality is significantly improved. The methodology yields 2x savings in the memory footprint without significant degradation of the model's accuracy.

P140 | Q: 연합학습 연구들 정리해줘
     [2412.11674] UA-PDFL: A Personalized Approach for Decentralized Federated Learning
     Nonetheless, DFL still suffers from training degradation as FL does due to the non-independent and identically distributed (non-IID) nature of client data. Therefore, in this paper, we propose a novel unit representation aided personalized decentralized federated learning framework, named UA-PDFL, to deal with the non-IID challenge in DFL. Based on this scheme, client-wise dropout and layer-wise personalization are proposed to further enhance the learning performance of DFL.

P141 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2412.16682] The Task Shield: Enforcing Task Alignment to Defend Against Indirect Prompt Injection in LLM Agents
     While existing defenses based on rule constraints, source spotlighting, and authentication protocols show promise, they struggle to maintain robust security while preserving task functionality. We propose a novel and orthogonal perspective that reframes agent security from preventing harmful actions to ensuring task alignment, requiring every agent action to serve user objectives. Through experiments on the AgentDojo benchmark, we demonstrate that Task Shield reduces attack success rates (2.07%) while maintaining high task utility (69.79%) on GPT-4o.

P142 | Q: 요즘 LLM 양자화 연구들 정리해줘
     [2606.22249] On the Expressive Power of Weight Quantization in Large Language Models
     We argue that 1.58-bit is the limiting precision for weight quantization by establishing the universal approximation and expressive collapse properties of weight-quantized models wi… Additionally, we confirm that weight quantization leads to expressive degradation, in which the expressive capacity of weight-quantized models degrades polynomially as the number of quantization bits decreases. These theoretical findings provide a solid foundation for advancing weight quantization in the context of scaling laws and shed insights for future research in model compression and inference acceleration.

P143 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2602.07297] Progressive Searching for Retrieval in RAG
     We propose a cost-effective searching algorithm for retrieval process. Our progressive searching algorithm incrementally refines the candidate set through a hierarchy of searches, starting from low-dimensional embeddings and progressing into a higher, target-dimensionality. This multi-stage approach reduces retrieval time while preserving the desired accuracy. Our findings demonstrate that progressive search in RAG systems achieves a balance between dimensionality, speed, and accuracy, enabling scalable and high-performance retrieval even for large databases.

P144 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2606.25182] What Intermediate Layers Know: Detecting Jailbreaks from Entropy Dynamics
     Importantly, this signal is not uniform across model depth: it is concentrated in intermediate layers and degrades at the final layer, indicating that jailbreak-relevant structure is most pronounced in mid-network representations rather than at the output head. Together, our findings show that jailbreak behavior is reflected in structured intermediate uncertainty dynamics, clarifying both which entropy-derived features encode harmful intent and where in the network that signal is most pronounced.

P145 | Q: LLM 코드 생성 연구들 어떤 방향으로 가고 있어?
     [2503.24235] A Survey on Test-Time Scaling in Large Language Models: What, How, Where, and How Well?
     Recent studies demonstrate that TTS can further elicit the problem-solving capabilities of large language models (LLMs), enabling significant breakthroughs not only in specialized reasoning tasks, such as mathematics and coding, but also in general tasks like open-ended Q&A. To fill this gap, we propose a unified, multidimensional framework structured along four core dimensions of TTS research: what to scale, how to scale, where to scale, and how well to scale.

P146 | Q: 비전-언어 모델 환각을 줄이는 방법이나 탐지하는 방법 연구 있어?
     [2507.19024] A Survey of Multimodal Hallucination Evaluation and Detection
     This survey offers an in-depth review of hallucination evaluation benchmarks and detection methods across Image-to-Text (I2T) and Text-to-image (T2I) generation tasks. Specifically, we first propose a taxonomy of hallucination based on faithfulness and factuality, incorporating the common types of hallucinations observed in practice. Finally, we highlight key limitations in current benchmarks and detection methods, and outline potential directions for future research.

P147 | Q: RAG에서 리랭킹 개선하는 연구들 정리해줘
     [2503.22672] Exploring the Effectiveness of Multi-stage Fine-tuning for Cross-encoder Re-rankers
     Our experiments show that the effectiveness of point-wise cross-encoders fine-tuned using contrastive learning is indeed on par with that of models fine-tuned with multi-stage approaches.

P148 | Q: 요즘 LLM 양자화 연구들 정리해줘
     [2504.03717] RaanA: A Fast, Flexible, and Data-Efficient Post-Training Quantization Algorithm
     In this paper, we propose RaanA, a unified PTQ framework that overcomes these challenges by introducing two novel components: 1) RaBitQ-H, a variant of a randomized vector quantization method RaBitQ, designed for fast, accurate, and highly efficient quantization; and 2) AllocateBits, an algorithm that optimally allocates bit-widths across layers based on their quantization sensitivity. RaanA achieves competitive performance with state-of-the-art quantization methods while being extremely fast, requiring… Extensive experiments demonstrate RaanA's efficacy in balancing efficiency and accuracy.

P149 | Q: 연합학습 연구들 정리해줘
     [2412.10605] Client-Side Patching against Backdoor Attacks in Federated Learning
     In this paper, we propose a novel defense mechanism for federated learning systems designed to mitigate backdoor attacks on the clients-side. Through extensive experiments on the MNIST and Fashion-MNIST datasets, we demonstrate that our defense effectively reduces backdoor accuracy, outperforming existing state-of-the-art defenses, such as LFighter, FLAME, and RoseAgg, in i.i.d.

P150 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2508.05650] OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools
     We introduce OmniBench RAG, a novel automated platform for multi domain evaluation of RAG systems. We introduce two standardized metrics: Improvements (accuracy gains) and Transformation (efficiency differences between pre RAG and post RAG models), enabling reproducible comparisons across models and tasks. Our evaluation reveals striking variability in RAG effectiveness, from significant gains in culture to declines in mathematics, highlighting the critical importance of systematic, domain aware assessment. A demonstration video is available at: https://www.youtube.com/watch?v=BZx83QFcTCI.

P151 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2506.18879] CommVQ: Commutative Vector Quantization for KV Cache Compression
     To address this, we propose Commutative Vector Quantization (CommVQ) to significantly reduce memory usage for long-context LLM inference. To further reduce computational costs during decoding, we design the codebook to be commutative with Rotary Position Embedding (RoPE) and train it… Our approach achieves high accuracy with additive quantization and low overhead via the RoPE-commutative codebook. Experiments on long-context benchmarks and GSM8K show that our method reduces FP16 KV cache size by 87.5% with 2-bit quantization, while outperforming state-of-the-art KV cache quantization methods.

P152 | Q: VLA 모델 연구들 정리해줘
     [2606.19297] Does VLA Even Know the Basics? Measuring Commonsense and World Knowledge Retention in Vision-Language-Action Models
     We introduce Act2Answer, a lightweight protocol that adapts VLM knowledge benchmarks to VLA evaluation by requiring agents to answer through action. In a large-scale study of 7 VLA models and 9 VLM baselines, we systematically rank models across categories, finding that VLAs show solid performance on simple concepts while exhibiting larger gaps on richer semantic categories relative to their source VLMs, that VQA co-training is associated with better knowledge retention, and that answer-relevant signals peak in middle VLA layers but attenuate in upper layers.

P153 | Q: 생성 모델 워터마크 연구들 정리해줘
     [2412.19834] RoboSignature: Robust Signature and Watermarking on Network Attacks
     In this paper, we present a novel adversarial fine-tuning attack that disrupts the model's ability to embed the intended watermark, exposing a significant vulnerability in existing watermarking methods. Our findings emphasize the importance of anticipating and defending against potential vulnerabilities in generative systems.

P154 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2512.24044] Jailbreaking Attacks vs. Content Safety Filters: How Far Are We in the LLM Safety Arms Race?
     To address this gap, we present the first systematic evaluation of jailbreak attacks targeting LLM safety alignment, assessing their success across the full inference pipeline, including both input and output filtering stages. Our findings yield two key insights: first, nearly all evaluated jailbreak techniques can be detected by at least one safety filter, suggesting that prior assessments may have overestimated the practical success of these attacks; second, while safety filters are effective in detection, there remains room to better balance recall and precision to further optimize protec…

P155 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2509.11552] HiChunk: Evaluating and Enhancing Retrieval-Augmented Generation with Hierarchical Chunking
     Based on this conclusion, we propose HiCBench, which includes manually annotated multi-level document chunking points, synthesized evidence-dense quetion answer(QA) pairs, and their corresponding evidence sources. Experiments demonstrate that HiCBench effectively evaluates the impact of different chunking methods across the entire RAG pipeline. Moreover, HiChunk achieves better chunking quality within reasonable time consumption, thereby enhancing the overall performance of RAG systems.

P156 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2412.16145] Offline Reinforcement Learning for LLM Multi-Step Reasoning
     While Direct Preference Optimization (DPO) has shown promise in aligning LLMs with human preferences, it is less suitable for multi-step reasoning tasks because (1) DPO relies on paired preference data, which is not readily available for multi-step reasoning tasks, and (2) it treats all tokens uniformly, making it ineffective for credit assignment in multi-step reasoning tasks, which often come with sparse reward. In this work, we propose OREO (Offline Reasoning Optimization), an offline RL method for enhancing LLM multi-step reasoning.

P157 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2407.16667] RedAgent: Red Teaming Large Language Models with Context-aware Autonomous Language Agent
     Recently, advanced Large Language Models (LLMs) such as GPT-4 have been integrated into many real-world applications like Code Copilot. By self-reflecting on contextual feedback in an additional memory buffer, RedAgent continuously learns how to leverage these strategies to achieve effective jailbreaks in specific contexts. Extensive experiments demonstrate that our system can jailbreak most black-box LLMs in just five queries, improving the efficiency of existing red teaming methods by two times. We have reported all found issues and communicated with OpenAI and Meta for bug fixes.

P158 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2412.12192] No Free Lunch for Defending Against Prefilling Attack by In-Context Learning
     In this paper, we: (1) show that ICL can effectively defend against prefilling jailbreak attacks by employing adversative sentence structures within demonstrations; (2) characterize the effectiveness of this defense through the lens of model size, number of demonstrations, over-defense, integration with other jailbreak attacks, and the presence of safety alignment. On the other hand, LLMs exhibit similar over-defensiveness when utilizing ICL demonstrations with adversative structures, and this behavior appears to be independent of model size.

P159 | Q: 지식 증류 관련 논문들 동향 알려줘
     [2605.02860] Standing on the Shoulders of Giants: Stabilized Knowledge Distillation for Cross--Language Code Clone Detection
     To address these limitations, we propose a knowledge distillation framework that transfers reasoning capabilities from DeepSeek-R1 into compact open-source student models for X-CCD. In addition, classification-head variants substantially reduce inference time compared to generation-based inference. Overall, our results show that reasoning-oriented distillation combined with response stabilization makes compact open-source models more practical and reliable for X-CCD detection.

P160 | Q: 디코더 전용 LLM을 비지도 대조학습만으로 긴 문서 검색기로 바꾸는 연구 알려줘
     [2601.05262] LLM2IR: simple unsupervised contrastive learning makes long-context LLM great retriever
     In this paper, we introduce LLM2IR, an efficient unsupervised contrastive learning framework to convert any decoder-only large language model (LLM) to an information retrieval model. We also find that models with a longer context length tend to have a stronger IR capacity by comparing task performances of models in the same model family. Our work not only provides an effective way to build IR models on the state-of-the-art LLMs, but also shed light on the relationship between information retrieval ability and model context length, which helps the design of better information retrievers.

P161 | Q: RAG의 검색 정확도를 높이는 논문들을 분석해 보고, 아직 사람들이 시도하지 않은 '연구의 빈틈(Research Gap)'을 3가지 제안해 봐
     [2602.21553] Revisiting RAG Retrievers: An Information Theoretic Benchmark
     Those that do compare retrievers directly use a limited set of evaluation tools which fail to capture complementary and overlapping strengths. This work presents MIGRASCOPE, a Mutual Information based RAG Retriever Analysis Scope. We further show that if chosen carefully, an ensemble of retrievers outperforms any single retriever. Our findings provide a fresh perspective on the structure of modern retrieval techniques and actionable guidance for designing robust and efficient RAG systems.

P162 | Q: LLM 환각 탐지 방법 논문들 비교해서 정리해줘
     [2606.06748] Evidence Graph Consistency in Retrieval-Augmented Generation: A Model-Dependent Analysis of Hallucination Detection
     We propose Evidence Graph Consistency (EGC), a framework that constructs a local evidence graph per response and computes five structural consistency measures as hallucination indicators. Evaluated on the full question answering split of RAGTruth across six LLMs (5,767 responses), EGC reveals a consistent model-family split: graph consistency features show the expected diagnostic direction for hallucinations in Llama-2 models but exhibit systematic reversal in GPT-4, GPT-3.5, and Mistral-7B.

P163 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2505.13527] Logic Jailbreak: Efficiently Unlocking LLM Safety Restrictions Through Formal Logical Expression
     To investigate this, we introduce LogiBreak, a novel and universal black-box jailbreak method that leverages logical expression translation to circumvent LLM safety systems. We evaluate LogiBreak on a multilingual jailbreak dataset spanning three languages, demonstrating its effectiveness across various evaluation settings and linguistic contexts.

P164 | Q: 시계열 예측 관련 논문 5개 찾아줘
     [2503.22747] LeForecast: Enterprise Hybrid Forecast by Time Series Intelligence
     With aspirations of pre-trained foundational models for such purpose, given their remarkable success of large foundation model across… It integrates advanced interpretations of time series data and multi-source information, and a three-pillar modelling engine combining a large foundation model (Le-TSFM), multimodal model and hybrid model to derive insights, predict or infer futures, and then drive optimisation across multiple sectors in enterprise operations. Our comprehensive experiments indicate that LeForecast is a profound and practical platform for efficient and competitive performance.

P165 | Q: VLA 모델 연구들 정리해줘
     [2604.05014] StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing
     We present StarVLA, an open-source codebase for VLA research. StarVLA also ships simple, fully reproducible single-benchmark training recipes that, despite minimal data engineering, already match or surpass prior methods on multiple benchmarks with both VLM and world-model backbones. To our best knowledge, StarVLA is one of the most comprehensive open-source VLA frameworks available, and we expect it to lower the barrier for reproducing existing methods and prototyping new ones.

P166 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2607.02980] Hierarchical Sparse Attention Done Right: Toward Infinite Context Modeling
     We propose Hierarchical Landmark Sparse (HiLS) Attention, a chunk-wise sparse attention mechanism that learns chunk selection end-to-end under the language-modeling (LM) loss. Experimental results show that HiLS-Attention achieves performance comparable to, and in some cases better than, full attention at in-domain context lengths. Meanwhile, HiLS-Attention extrapolates more than $64\times$ the training context length with 90% retrieval accuracy, far beyond full attention.

P167 | Q: LLM 환각을 탐지하는 연구나 완화하는 연구 알려줘
     [2311.05232] A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions
     Subsequently, we present a thorough overview of hallucination detection methods and benchmarks. Additionally, we delve into the current limitations faced by retrieval-augmented LLMs in combating hallucinations, offering insights for developing more robust IR systems.

P168 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2506.18879] CommVQ: Commutative Vector Quantization for KV Cache Compression
     To address this, we propose Commutative Vector Quantization (CommVQ) to significantly reduce memory usage for long-context LLM inference. To further reduce computational costs during decoding, we design the codebook to be commutative with Rotary Position Embedding (RoPE) and train it… Our approach achieves high accuracy with additive quantization and low overhead via the RoPE-commutative codebook. Experiments on long-context benchmarks and GSM8K show that our method reduces FP16 KV cache size by 87.5% with 2-bit quantization, while outperforming state-of-the-art KV cache quantization methods.

P169 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2503.10714] ZSMerge: Zero-Shot KV Cache Compression for Memory-Efficient Long-Context LLMs
     To this end, we propose ZSMerge, a dynamic KV cache compression framework designed for efficient cache management, featuring three key operations: (1) fine-grained memory allocation guided by multi-dimensional token importance metrics at head-level granularity, (2) a residual merging mechanism that preserves critical context through compensated attention scoring, and (3) a zero-shot adaptation mechanism compatible with diverse LLM architectures without requiring retraining. When applied to LLaMA2-7B, it demonstrates a 20:1 compression ratio for key-value cache retention (reducing memory foot…

P170 | Q: 시계열 예측 관련 논문 5개 찾아줘
     [2403.20150] TFB: Towards Comprehensive and Fair Benchmarking of Time Series Forecasting Methods
     To achieve this, we propose TFB, an automated benchmark for Time Series Forecasting (TSF) methods. To achieve better domain coverage, we include datasets from 10 different domains: traffic, electricity, energy, the environment, nature, economic, stock markets, banking, health, and the web. To remove biases against some methods, we include a diverse range of methods, including statistical learning, machine learning, and deep learning methods, and we also support a variety of evaluation strategies and metrics to ensure a more comprehensive evaluations of different methods.

P171 | Q: LLM 환각 탐지 방법 논문들 비교해서 정리해줘
     [2502.13490] What are Models Thinking about? Understanding Large Language Model Hallucinations "Psychology" through Model Inner State Analysis
     Considering the interpretability of LLM internal states and the fact that they do not require external information sources, we introduce such states into LLM hallucination detection. In this paper, we systematically analyze different internal states' revealing features during inference forward and comprehensively evaluate their ability in hallucination detection. Then, we introduce these internal states into hallucination detection and conduct comprehensive experiments to discuss the advantages and limitations.

P172 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2606.12737] PI-Hunter: Automated Red-Teaming for Exposing and Localizing Prompt Injections
     We propose PI-Hunter, an automated agentic auditing framework for proactive vulnerability exposure in LLM agents. PI-Hunter constructs realistic source-aware test cases and iteratively evolves them through feedback-driven exploration to induce agents to retrieve and reveal latent malicious… Extensive experiments across multiple benchmarks, agent architectures, attacks, and defenses demonstrate that PI-Hunter substantially improves vulnerability exposure and attack-surface coverage over strong automated red-teaming baselines, while remaining effective under existing prompt injection defenses.

P173 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2510.00001] Methodological Framework for Quantifying Semantic Test Coverage in RAG Systems
     To address this, we present a novel, applied methodology to quantify the semantic coverage of RAG test questions against their underlying documents. Experimental evidence from two distinct use cases demonstrates that our framework effectively quantifies test coverage, identifies specific content areas with inadequate representation, and provides concrete recommendations for generating new, high-va… This work provides RAG developers with essential tools to build more robust test suites, thereby improving system reliability and extending to applications such as identifying misaligned documents.

P174 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2508.06401] A Systematic Literature Review of Retrieval-Augmented Generation: Techniques, Metrics, and Challenges
     Guided by the PRISMA 2020 framework, we (i) specify explicit inclusion and exclusion criteria based on citation count and research questions, (ii) catalogue datasets, architectures, and evaluation practices, and (iii) synthesise empirical evidence on the effectiveness and limitations of RAG. To mitigate citation-lag bias, we applied a lower citation-count threshold to papers published in 2025 so that emerging breakthroughs with naturally fewer citations were still captured.

P175 | Q: 비전-언어 모델 환각을 줄이는 방법이나 탐지하는 방법 연구 있어?
     [2603.29405] Hallucination-aware intermediate representation edit in large vision-language models
     To address the above issue, we propose a framework for dynamically detecting hallucination representations and performing hallucination-eliminating edits on these representations. With minimal additional computational cost, we achieve state-of-the-art performance on existing benchmarks. Extensive experiments demonstrate the effectiveness of our approach, highlighting its efficient and robust hallucination elimination capability and its powerful controllability over hallucinations.

P176 | Q: 연합학습 연구들 정리해줘
     [2412.17692] FedTLU: Federated Learning with Targeted Layer Updates
     However, non-IID (identically and independently distributed) data across clients often limits FL's performance. This paper proposes a targeted layer update strategy for fine-tuning in FL. We show in extensive experiments that our method improves convergence and performance in non-IID settings, offering a more efficient approach to fine-tuning federated language models.

P177 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2406.03482] QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead
     We introduce QJL, a new quantization approach that consists of a Johnson-Lindenstrauss (JL) transform followed by sign-bit quantization. We propose an asymmetric estimator for the inner product of two vectors and demonstrate that applying QJL to one vector and a standard JL transform without quantization to the other provides an unbiased estimator with minimal distort… When applied across various LLMs and NLP tasks to quantize the KV cache to only 3 bits, QJL demonstrates a more than fivefold reduction in KV cache memory usage without compromising accuracy, all while achieving faster runtime.

P178 | Q: 시계열 예측 관련 논문 5개 찾아줘
     [2412.16643] TimeRAG: BOOSTING LLM Time Series Forecasting via Retrieval-Augmented Generation
     In view of these challenges, we propose TimeRAG, a framework that incorporates Retrieval-Augmented Generation (RAG) into time series forecasting LLMs, which constructs a time series knowledge base from historical sequences, retrieves reference sequences from the knowledge base that exhibit similar patterns to the query sequence measured by Dynamic Time Warping (DTW), and combines these reference sequences and the prediction query as a textual prompt to the time series forecasting LLM.

P179 | Q: 생성 모델 워터마크에서 이미지·영상 워터마크나 텍스트·에이전트 워터마크 연구 있어?
     [2412.15278] DreaMark: Rooting Watermark in Score Distillation Sampling Generated Neural Radiance Fields
     With the rapid advancement in NeRF generation quality, protecting the copyright of the generated NeRF has become increasingly important. To address both issues, we propose Dreamark to embed a secret message by backdooring the NeRF during NeRF generation. We evaluate the generation quality and watermark robustness against image- and model-level attacks. Extensive experiments show that the watermarking process will not degrade the generation quality, and the watermark achieves 90+% accuracy among both image-level attacks (e.g., Gaussian noise) and model-level attacks (e.g., pruning attack).

P180 | Q: RAG에서 리랭킹 개선하는 연구들 정리해줘
     [2509.25085] jina-reranker-v3: Last but Not Late Interaction for Listwise Document Reranking
     Unlike late interaction models like ColBERT that encode documents separately before multi-vector matching, our approach applies causal attention between the query and all candidate documents in the same context window, enabling rich interactions before extracting contextual embeddings from each document's final token. The new model achieves state-of-the-art BEIR performance with 61.94 nDCG@10 while being significantly smaller than other models with comparable performance.

P181 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2402.15727] LLMs Can Defend Themselves Against Jailbreaking in a Practical Manner: A Vision Paper
     This paper proposes a lightweight yet practical defense called SELFDEFEND, which can defend against all existing jailbreak attacks with minimal delay for jailbreak prompts and negligible delay for normal user prompts. Our key insight is that regardless of the kind of jailbreak strategies employed, they eventually need to include a harmful prompt (e.g., "how to make a bomb") in the prompt sent to LLMs, and we found that existing LLMs can effectively recognize such harmful prompts t… We demonstrate our idea of SELFDEFEND works in various jailbreak scenarios through manual analysis in GPT-3.5/4.

P182 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2604.28049] Agent-Agnostic Evaluation of SQL Accuracy in Production Text-to-SQL Systems
     We present STEF (Schema-agnostic Text-to-SQL Evaluation Framework), a production-native evaluation system that operates exclusively on natural language inputs the user question, an enriched reformulation, and the generated SQL without requiring database schema or reference queries. Empirical results demonstrate that STEF enables continuous production monitoring and agent improvement feedback loops without schema dependency, making structured query evaluation viable at scale for the first time.

P183 | Q: RAG 청킹에서 청크 크기나 의미 단위 분할을 다룬 연구 있어?
     [2505.21700] Rethinking Chunk Size For Long-Document Retrieval: A Multi-Dataset Analysis
     Our experiments, conducted on both short-form and long-form datasets, reveal that chunk size plays a critical role in retrieval effectiveness -- smaller chunks (64-128 tokens) are optimal for datasets with concise, fact-based answers, whereas larger chunks (512-1024 tokens) improve retrieval in datasets requiring broader contextual understanding. Our results underscore the trade-offs between chunk size, embedding models, and dataset characteristics, emphasizing the need for improved chunk quality measures, and more comprehensive datasets to advance chunk-based retrieval in long-document Info…

P184 | Q: RAG의 검색 정확도를 높이는 논문들을 분석해 보고, 아직 사람들이 시도하지 않은 '연구의 빈틈(Research Gap)'을 3가지 제안해 봐
     [2508.06401] A Systematic Literature Review of Retrieval-Augmented Generation: Techniques, Metrics, and Challenges
     Guided by the PRISMA 2020 framework, we (i) specify explicit inclusion and exclusion criteria based on citation count and research questions, (ii) catalogue datasets, architectures, and evaluation practices, and (iii) synthesise empirical evidence on the effectiveness and limitations of RAG. To mitigate citation-lag bias, we applied a lower citation-count threshold to papers published in 2025 so that emerging breakthroughs with naturally fewer citations were still captured.

P185 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2503.09579] Cost-Optimal Grouped-Query Attention for Long-Context Modeling
     In this work, we analyze the relationship among context length, model size, GQA configuration, and model loss, and introduce two innovations: (1) we decouple the total head size from the hidden size, enabling more flexible control over attention FLOPs; and (2) we jointly optimize the model size and the GQA configuration to arrive at a better allo… More importantly, we propose a recipe for deriving cost-optimal GQA configurations. Configurations selected by our recipe can reduce both memory usage and FLOPs by more than 50% compared to Llama-3's GQA, with *no degradation in model capabilities*.

P186 | Q: 비전-언어 모델 환각을 줄이는 방법이나 탐지하는 방법 연구 있어?
     [2404.18930] Hallucination of Multimodal Large Language Models: A Survey
     This problem has attracted increasing attention, prompting efforts to detect and mitigate such inaccuracies. We review recent advances in identifying, evaluating, and mitigating these hallucinations, offering a detailed overview of the underlying causes, evaluation benchmarks, metrics, and strategies developed to address this issue. Additionally, we analyze the current challenges and limitations, formulating open questions that delineate potential pathways for future research. Resources are available at: https://github.com/showlab/Awesome-MLLM-Hallucination.

P187 | Q: 대기업처럼 사전학습부터 RL까지 다 하지 않고, 어렵고 정보량 많은 탐색 궤적 데이터만으로 검색 에이전트 성능을 끌어올린 연구 알려줘
     [2605.29307] GrepSeek: Training Search Agents for Direct Corpus Interaction
     We introduce GrepSeek, an optimized direct corpus interaction (DCI) agent that learns to find, filter, and compose evidence over large text corpora. To make DCI practical at scale, we introduce two semantics-preserving execution optimizations: Pruned Adaptive Command Execution, which re… Across eight open-domain QA benchmarks, GrepSeek achieves the strongest overall performance, with a statistically significant relative improvement of$5.7%$ over the best baseline. Our analysis shows how DCI-optimized agents conduct flexible and effective compositional search through direct corpus interaction.

P188 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2504.06214] From 128K to 4M: Efficient Training of Ultra-Long Context Large Language Models
     In this work, we introduce a efficient training recipe for building ultra-long context LLMs from aligned instruct model, pushing the boundaries of context lengths from 128K to 1M, 2M, and 4M tokens. Importantly, models trained with our approach maintain competitive performance on standard benchmarks, demonstrating balanced improvements for both long and short context tasks. Our findings establish a robust framework for efficiently scaling context lengths while preserving general model capabilities.

P189 | Q: 연합학습 연구들 정리해줘
     [2607.13045] Federated Explainable Artificial Intelligence: Roles, Architectures, Evaluation, and Open Challenges
     In parallel, Explainable Artificial Intelligence (XAI) has gained attention for improving transparency, trust, and accountability, particularly in high-stakes domains. We show how explainability supports aggregation, personalization, robustness, coordination, and system-level decision making. To organize the literature, we introduce a taxonomy that classifies FedXAI methods by the role of explainability, model and explainer types, explanation scope, integration level, FL settings, and data heterogeneity.

P190 | Q: 생성 모델 워터마크 연구들 정리해줘
     [2605.16239] Dynamics-Level Watermarking of Flow Matching Models with Random Codes
     We introduce a dynamics-level approach to watermarking generative models. Rather than embedding signals into model weights or outputs, we embed the watermark directly into the learned continuous dynamics -- the velocity field of a flow matching model. Experiments on MNIST and CIFAR-10 across different architectures confirm reliable message recovery, preserved generation quality, and chance-level decoding accuracy without the secret key.

P191 | Q: 생성 모델 워터마크에서 이미지·영상 워터마크나 텍스트·에이전트 워터마크 연구 있어?
     [2412.09492] Video Seal: Open and Efficient Video Watermarking
     To reduce these gaps, this paper introduces Video Seal, a comprehensive framework for neural video watermarking and a competitive open-sourced model. We present experimental results demonstrating the effectiveness of the approach in terms of speed, imperceptibility, and robustness. Video Seal achieves higher robustness compared to strong baselines especially under challenging distortions combining geometric transformations and video compression.

P192 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2412.12322] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems
     We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. The results also highlight the importance of prompt engineering in RAG systems, with our custom-prompted agents showing consistent improvements in retrieval accuracy and response quality.

P193 | Q: 월드 모델 최근 연구 동향 정리해줘
     [2606.20781] World Action Models: A Survey
     Across these axes, a consistent design pattern emerges: WAMs are not simply video generators with action heads, but predictive-action methods whose design choices trade representational richness against compute, memory, latency, and action-label cost.

P194 | Q: LLM 환각을 탐지하는 연구나 완화하는 연구 알려줘
     [2508.14314] Zero-knowledge LLM hallucination detection and mitigation through fine-grained cross-model consistency
     We present Finch-Zk, a black-box framework that leverages fine-grained cross-model consistency to detect and mitigate hallucinations in LLM outputs without requiring external knowledge sources. Experiments on the FELM dataset show Finch-Zk improves hallucination detection F1 scores by 6-39% compared to existing approaches. Extensive evaluation on multiple datasets demonstrates that Finch-Zk provides a practical, deployment-ready safeguard for enhancing factual reliability in production LLM systems.

P195 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2603.03541] RAG-X: Systematic Diagnosis of Retrieval-Augmented Generation for Medical Question Answering
     These approaches fail to diagnose whether an error stems from faulty retrieval or flawed generation, limiting developers from performing targeted improvement. To address this gap, we propose RAG-X, a diagnostic framework that evaluates the retriever and generator independently across a triad of QA tasks: information extraction, short-answer generation, and multiple-choice question (MCQ) answering. Our experiments reveal an ``Accuracy Fallacy", where a 14% gap separates perceived system success from evidence-based grounding.

P196 | Q: RAG에서 검색된 문서의 순서나 개수가 답변 품질에 주는 영향을 분석한 연구 찾아줘
     [2510.21440] Redefining Retrieval Evaluation in the Era of LLMs
     We introduce a utility-based annotation schema that quantifies both the positive contribution of relevant passages and the negative impact of distracting ones. Building on this foundation, we propose UDCG (Utility and Distraction-aware Cumulative Gain), a metric using an LLM-oriented positional discount to directly optimize the correlation with the end-to-end answer accuracy. Experiments on five datasets and six LLMs demonstrate that UDCG improves correlation by up to 36% compared to traditional metrics.

P197 | Q: speculative decoding에서 드래프트 모델 학습이나 검증 단계를 개선한 연구 알려줘
     [2605.29707] Domino: Decoupling Causal Modeling from Autoregressive Drafting in Speculative Decoding
     However, its practical speedup is constrained by the trade-off between draft quality and drafting cost: autoregressive drafters model causal dependencies among draft tokens but incur sequential overhead, while parallel drafters reduce drafting cost but weake… In this paper, we propose Domino, a speculative decoding framework that decouples causal dependency modeling from expensive autoregressive draft execution. Experiments on Qwen3 models show that Domino achieves up to $5.49\times$end-to-end speedup under the Transformers backend and up to$5.8\times$ throughput speedup under SGLang serving.

P198 | Q: 프롬프트 인젝션 공격이랑 방어 연구 정리해줘
     [2605.15030] WARD: Adversarially Robust Defense of Web Agents Against Prompt Injections
     To address these limitations, we propose WARD (Web Agent Robust Defense against Prompt Injection), a practical guard model for secure and efficient web agents. WARD is built on WARD-Base, a large-scale dataset with around 177K samples collected from 719 high-traffic URLs and platforms, and WARD-PIG, a dedicated dataset designed for prompt injection attacks targeting the guard model. Extensive experiments show that WARD achieves nearly perfect recall on out-of-distribution benchmarks, maintains low false positive rates to preserve agent utility, remains robust against guard-targeted and adapt…

P199 | Q: RAG에서 검색된 문서의 순서나 개수가 답변 품질에 주는 영향을 분석한 연구 찾아줘
     [2505.15561] Do RAG Systems Really Suffer From Positional Bias?
     Through extensive experiments on three benchmarks, we show how state-of-the-art retrieval pipelines, while attempting to retrieve relevant passages, systematically bring highly distracting ones to the top ranks, with over 60% of queries containing at least one highly distracting passage among the top-10 retrieved passages. Indeed, our findings reveal that sophisticated strategies that attempt to rearrange the passages based on LLM positional preferences do not perform better than random shuffling.

P200 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2512.22629] DICE: Discrete Interpretable Comparative Evaluation with Probabilistic Scoring for Retrieval-Augmented Generation
     We introduce DICE (Discrete Interpretable Comparative Evaluation), a two-stage, evidence-coupled framework that advances explainability and robustness in RAG evaluation. To address efficiency challenges at scale, DICE employs a Swiss-system tournament that reduces computational complexity from $O(N^2)$ to $O(N \log N)$, achieving a 42.9% reduction in our eight-system evaluation while preserving ranking f… Validation on a curated Chinese financial QA dataset demonstrates that DICE achieves 85.7% agreement with human experts, substantially outperforming existing LLM-based metrics such as RAGAS.

P201 | Q: LLM 양자화에서 가중치 양자화랑 KV 캐시 양자화 연구 알려줘
     [2504.03717] RaanA: A Fast, Flexible, and Data-Efficient Post-Training Quantization Algorithm
     In this paper, we propose RaanA, a unified PTQ framework that overcomes these challenges by introducing two novel components: 1) RaBitQ-H, a variant of a randomized vector quantization method RaBitQ, designed for fast, accurate, and highly efficient quantization; and 2) AllocateBits, an algorithm that optimally allocates bit-widths across layers based on their quantization sensitivity. RaanA achieves competitive performance with state-of-the-art quantization methods while being extremely fast, requiring… Extensive experiments demonstrate RaanA's efficacy in balancing efficiency and accuracy.

P202 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2406.18122] Poisoned LangChain: Jailbreak LLMs by LangChain
     Given the increasing demand for real-time capabilities in large language models, real-time updates and iterations of new knowledge have become essential. Retrieval-Augmented Generation (RAG), an advanced technique to compensate for the model's lack of new knowledg… In this paper, we conduct the first work to propose the concept of indirect jailbreak and achieve Retrieval-Augmented Generation via LangChain. The experiments demonstrate that PLC successfully implemented indirect jailbreak attacks under three different scenarios, achieving success rates of 88.56%, 79.04%, and 82.69% respectively.

P203 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2601.07320] Segmental Advantage Estimation: Enhancing PPO for Long-Context LLM Training
     To address this, we introduce Segmental Advantage Estimation (SAE), which mitigates the bias that GAE can incur in RLVR. Our experiments demonstrate that SAE achieves superior performance, with marked improvements in final scores, training stability, and sample efficiency. These gains are shown to be consistent across multiple model sizes, and a correlation analysis confirms that our proposed advantage estimator achieves a higher correlation with an approximate ground-truth advantage, justifying its superior performance.

P204 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2307.03172] Lost in the Middle: How Language Models Use Long Contexts
     We analyze the performance of language models on two tasks that require identifying relevant information in their input contexts: multi-documen… In particular, we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models. Our analysis provides a better understanding of how language models use their input context and provides new evaluation protocols for future long-context language models.

P205 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2511.07480] KG-DF: A Black-box Defense Framework against Jailbreak Attacks Based on Knowledge Graphs
     In response to this problem, we propose a Knowledge Graph Defense Framework (KG-DF). To address this issue, we introduce an extensible semantic parsing module, whose core task is to transform the input query into a set of structured and secure concept representations, thereby enhancing the relevance of the matching process. Experimental results show that our framework enhances defense performance against various jailbreak attack methods, while also improving the response quality of the LLM in general QA scenarios by incorporating domain-general knowledge.

P206 | Q: LLM 에이전트가 쓰는 도구가 오류를 내도 티가 안 나는 경우, 모델이 그걸 알아채는지 다룬 논문 있어? 핵심 내용 설명해줘
     [2406.19228] Tools Fail: Detecting Silent Errors in Faulty Tools
     Instead, we introduce a framework for tools more broadly which guides us to explore a model's ability to detect "silent" tool errors, and reflect on how to plan. This more directly aligns with the increasingly popular use of models as tools.

P207 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2412.19037] CL-Attack: Textual Backdoor Attacks via Cross-Lingual Triggers
     In this paper, inspired by cross-lingual (CL) prompts of LLMs in real-world scenarios, we propose a higher-dimensional trigger method at the paragraph level, namely CL-attack. Extensive experiments on different tasks and model architectures demonstrate that CL-attack can achieve nearly 100% attack success rate with a low poisoning rate in both classification and generation tasks. We also empirically show that the CL-attack is more robust against current major defense methods compared to baseline backdoor attacks.

P208 | Q: 프롬프트 인젝션 공격이랑 방어 연구 정리해줘
     [2511.10720] PISanitizer: Preventing Prompt Injection to Long-Context LLMs via Prompt Sanitization
     When extended to long-context scenarios, they have limited effectiveness. In this work, we propose PISanitizer, which first pinpoints and sanitizes potential injected tokens (if any) in a context before letting a backend LLM generate a response, thereby eliminating the influence of the injected instruction. To sanitize injected tokens, PISanitizer builds on two observations: (1) prompt injection attacks essentially craft an instruction that compels an LLM to follow it, and (2) LLMs intrinsically leverage the attention mechanism to focus on crucial input tokens for output generation.

P209 | Q: RAG에서 리랭킹 개선하는 연구들 정리해줘
     [2412.12322] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems
     We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. The results also highlight the importance of prompt engineering in RAG systems, with our custom-prompted agents showing consistent improvements in retrieval accuracy and response quality.

P210 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2503.00392] Progressive Sparse Attention: Algorithm and System Co-design for Efficient Attention in LLM Serving
     To overcome this trade-off, this paper presents PSA, a $\underline{P}$rogressive $\underline{S}$parse $\underline{A}$ttention mechanism that integrates algorithmic innovations with system co-design to achieve both high inference accuracy and improved efficiency in LLM serving. Extensive experimental results demonstrate that PSA reduces KV cache usage for attention computation by up to 2.4$\times$ and 8.8$\times$, and increases end-to-end serving throughput by up to 1.4$\times$ and 2.0$\times$, compared to state-of-the-art DSAes and systems without sparse attention, respectively.

P211 | Q: LLM 코드 생성 연구들 어떤 방향으로 가고 있어?
     [2606.20517] Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages
     LiveCodeBench (LCB) has recently become a widely adopted benchmark for evaluating large language models (LLMs) on code-generation tasks. We introduce Multi-LCB, a benchmark for evaluating LLMs across twelve programming languages, including Python. Our results establish Multi-LCB as a rigorous new benchmark for multi-programming-language code evaluation, directly addressing LCB's primary limitation and exposing critical gaps in current LLM capabilities.

P212 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2602.20735] RMIT-ADM+S at the MMU-RAG NeurIPS 2025 Competition
     This paper presents the award-winning RMIT-ADM+S system for the Text-to-Text track of the NeurIPS~2025 MMU-RAG Competition. R2RAG won the Best Dynamic Evaluation award in the Open Source category, demonstrating high effectiveness with careful design and efficient use of resources.

P213 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2405.07437] Evaluation of Retrieval-Augmented Generation: A Survey
     To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehensive overview of the evaluation and benchmarks of RAG systems. We then analyze the various datasets and metrics, discuss the limitations of current benchmarks, and suggest potential directions to advance the field of RAG benchmarks.

P214 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2602.21553] Revisiting RAG Retrievers: An Information Theoretic Benchmark
     Those that do compare retrievers directly use a limited set of evaluation tools which fail to capture complementary and overlapping strengths. This work presents MIGRASCOPE, a Mutual Information based RAG Retriever Analysis Scope. We further show that if chosen carefully, an ensemble of retrievers outperforms any single retriever. Our findings provide a fresh perspective on the structure of modern retrieval techniques and actionable guidance for designing robust and efficient RAG systems.

P215 | Q: 시계열 예측 관련 논문 5개 찾아줘
     [2412.12219] Are Large Language Models Useful for Time Series Data Analysis?
     Recently, large language models (LLMs) have gained prominence for their ability to handle complex data and extract meaningful insights. Our findings indicate that while LLM-based methods excel in specific tasks like anomaly detection, their benefits are less pronounced in others, such as forecasting, where simpler models sometimes perform comparably or better. This research highlights the role of LLMs in time series analysis and lays the groundwork for future studies to systematically explore their applications and limitations in handling temporal data.

P216 | Q: 시계열 예측 관련 논문 5개 찾아줘
     [2412.19932] Hidformer: Transformer-Style Neural Network in Stock Price Forecasting
     Our findings offer additional insights into the practical application of Transformer architectures in financial time series forecasting, highlighting their potential to improve algorithmic trading strategies, including human decision making.

P217 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2603.20122] Evolving Jailbreaks: Automated Multi-Objective Long-Tail Attacks on Large Language Models
     While recent studies have shown that leveraging long-tail distributions can facilitate such jailbreaks, existing approaches largely rely on handcrafted rules, limiting the systematic evaluation of these security and privacy vulnerabil… In this work, we present EvoJail, an automated framework for discovering long-tail distribution attacks via multi-objective evolutionary search. Extensive experiments demonstrate that EvoJail consistently discovers diverse and effective long-tail jailbreak strategies, achieving competitive performance with existing methods in both individual and ensemble level.

P218 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2403.20014] PURPLE: Making a Large Language Model a Better SQL Writer
     In this paper, we propose PURPLE (Pre-trained models Utilized to Retrieve Prompts for Logical Enhancement), which improves accuracy by retrieving demonstrations containing the requisite logical operator composition for the NL2SQL task on hand, thereby guiding LLMs to produce better SQL translation. PURPLE achieves a new state-of-the-art performance of 80.5% exact-set match accuracy and 87.8% execution match accuracy on the validation set of the popular NL2SQL benchmark Spider.

P219 | Q: 연합학습 연구들 정리해줘
     [2406.19050] FedMap: Iterative Magnitude-Based Pruning for Communication-Efficient Federated Learning
     This paper introduces FedMap, a novel method that aims to enhance the communication efficiency of FL deployments by collaboratively learning an increasingly sparse global model through iterative, unstructured pruning. Comparative analysis against the baseline approach demonstrates FedMap's ability to achieve more stable client model performance. For IID scenarios, FedMap achieves over $90$% pruning without significant performance degradation. In non-IID settings, it achieves at least $~80$% pruning while maintaining accuracy.

P220 | Q: 요즘 speculative decoding 연구 동향 정리해줘
     [2412.18910] AdaEAGLE: Optimizing Speculative Decoding via Explicit Modeling of Adaptive Draft Structures
     However, current studies on adaptive draft structures are limited by their performance, modeling approaches, and applicability. In this paper, we introduce AdaEAGLE, the first SD framework that explicitly models adaptive draft structures. It achieves comparable speedup results without manual thresholds and allows for deeper, more specialized optimizations. Moreover, together with threshold-based strategies, AdaEAGLE achieves a $1.62\times$ speedup over the vanilla AR decoding and outperforms fixed-length SotA baseline while maintaining output quality.

P221 | Q: RAG에서 노이즈 문서나 방해 문서에 대한 강건성을 다룬 연구 찾아줘
     [2502.06872] Towards Trustworthy Retrieval Augmented Generation for Large Language Models: A Survey
     However, despite RAG's success and potential, recent studies have shown that the RAG paradigm also introduces new risks, including robustness issues, privacy concerns, adversarial attacks, and accoun… Although various methods have been developed to improve the trustworthiness of RAG methods, there is a lack of a unified perspective and framework for research in this topic. For each perspective, we present a general framework and taxonomy, offering a structured approach to understanding the current challenges, evaluating existing solutions, and identifying promising future research directions.

P222 | Q: 생성 모델 워터마크에서 이미지·영상 워터마크나 텍스트·에이전트 워터마크 연구 있어?
     [2605.23994] RAW: Robust Avatar Watermarking -- Benchmarking and Baseline
     We introduce \textbf{RAW} (Robust Avatar Watermarking), a benchmark comprising 50 synthetic avatar videos from 5 commercial providers and 6 attacks simulating real-world avatar workflows. Evaluating 7 existing methods reveals that avatar-specific attacks such as background removal significantly degrade watermark recovery. WALT achieves the highest robustness to zoom attacks (92.4%) while maintaining strong performance on background removal (95.6%).

P223 | Q: RAG에서 노이즈 문서나 방해 문서에 대한 강건성을 다룬 연구 찾아줘
     [2309.01431] Benchmarking Large Language Models in Retrieval-Augmented Generation
     To this end, we establish Retrieval-Augmented Generation Benchmark (RGB), a new corpus for RAG evaluation in both English and Chinese. Evaluation reveals that while LLMs exhibit a certain degree of noise robustness, they still struggle significantly in terms of negative rejection, information integration, and dealing with false information.

P224 | Q: RAG에서 검색된 문서의 순서나 개수가 답변 품질에 주는 영향을 분석한 연구 찾아줘
     [2410.12837] A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions
     This paper presents a comprehensive study of Retrieval-Augmented Generation (RAG), tracing its evolution from foundational concepts to the current state of the art. Future research directions are proposed, focusing on improving the robustness of RAG models, expanding the scope of application of RAG models, and addressing societal implications. This survey aims to serve as a foundational resource for researchers and practitioners in understanding the potential of RAG and its trajectory in natural language processing.

P225 | Q: 연합학습에서 통신 효율이나 차등 프라이버시를 다룬 연구 있어?
     [2503.21159] Multi-Objective Optimization for Privacy-Utility Balance in Differentially Private Federated Learning
     In this work, we propose an adaptive clipping mechanism that dynamically adjusts the clipping norm using a multi-objective optimization framework. We theoretically analyze the convergence properties of our method and demonstrate its effectiveness through extensive experiments on MNIST, Fashion-MNIST, and CIFAR-10 datasets. Our results show that adaptive clipping consistently outperforms fixed-clipping baselines, achieving improved accuracy under the same privacy constraints.

P226 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2405.07437] Evaluation of Retrieval-Augmented Generation: A Survey
     To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehensive overview of the evaluation and benchmarks of RAG systems. We then analyze the various datasets and metrics, discuss the limitations of current benchmarks, and suggest potential directions to advance the field of RAG benchmarks.

P227 | Q: LLM 보상 모델(reward model) 관련 논문들 알려줘
     [2503.22723] Zero-Shot LLMs in Human-in-the-Loop RL: Replacing Human Feedback for Reward Shaping
     To address these challenges, we propose two key contributions. The LLM-HFBF framework creates a more balanced and reliable system by addressing both the limitations of LLMs (e.g., lack of domain-specific knowledge) and human supervision (e.g., inheren… By enabling human feedback bias flagging and correction, our approach improves reinforcement learning performance and reduces reliance on potentially biased human feedback. Empirical experiments show that biased human feedback significantly reduces performance, with Average Episodic Reward dropping by nearly 94% compared to unbiased approaches.

P228 | Q: RAG에서 리랭킹 개선하는 연구들 정리해줘
     [2606.28367] Beyond the Reranker: Do RAG Retrieval Enhancements Help Once a Strong Reranker Is Present?
     To study this directly, we build \textbf{HetDocQA}, a heterogeneous benchmark with \emph{chunker-agnostic} span-overlap relevance labels and collection-disjoint splits, and pair it with MuSiQue and QASPER as homogeneous controls. A strong cross-encoder reranker accounts for most of the pipeline's quality; beyond it, only two methods yield reliable gains: query expansion and SSCC. The remaining reranking and pool-expansion methods in common use, among them hierarchical summarization, graph expansion, routing, and rank fusion, give no reliable gain once that reranker is present.

P229 | Q: RAG 답변 품질을 사람 평가 없이 자동으로 채점하는 지표 연구들 정리해줘
     [2601.05264] Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems
     RAG offers a modular approach for integrating external knowledge without increasing the capacity of the model as LLM systems expand. Research and engineering practices have been fragmented as a result of the increasing diversity of RAG methodologies, which encompasses a variety of fusion mechanisms, retrieval strategies, and orchestration approaches.

P230 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2504.00048] Distill-C: Enhanced NL2SQL via Distilled Customization with LLMs
     To address this conundrum, we introduce Distill-C, a distilled customization framework tailored for NL2SQL tasks. Evaluated on multiple challenging benchmarks, Distill-C achieves an average improvement of 36% in execution accuracy compared to the base models from three distinct LLM families. Additionally, on three internal customer benchmarks, Distill-C demonstrates a 22.6% performance improvement over the base models. Our results demonstrate that Distill-C is an effective, high-performing and generalizable approach for deploying lightweight yet powerful NL2SQL models, delivering exceptional…

P231 | Q: 요즘 speculative decoding 연구 동향 정리해줘
     [2504.00030] Token-Driven GammaTune: Adaptive Calibration for Enhanced Speculative Decoding
     We introduce \textit{GammaTune} and \textit{GammaTune+}, training-free adaptive algorithms that dynamically adjust speculation length based on token acceptance rates using a heuristic-based switching mechanism. Evaluated on SpecBench across multiple tasks and model pairs, our method outperforms other heuristic-based approaches and fixed-length speculative decoding, achieving an average speedup of 15% ($\pm$5%) with \textit{GammaTune} and 16% ($\pm$3%) with \textit{GammaTune+}, while reducing performance variance.

P232 | Q: RAG의 검색 정확도를 높이는 논문들을 분석해 보고, 아직 사람들이 시도하지 않은 '연구의 빈틈(Research Gap)'을 3가지 제안해 봐
     [2412.12322] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems
     We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. The results also highlight the importance of prompt engineering in RAG systems, with our custom-prompted agents showing consistent improvements in retrieval accuracy and response quality.

P233 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2603.08819] Beyond Relevance: On the Relationship Between Retrieval and RAG Information Coverage
     Through experiments across two text RAG benchmarks (TREC NeuCLIR 2024 and TREC RAG 2024) and one multimodal benchmark (WikiVideo), we analyze 15 text retrieval stacks and 10 multimodal retrieval stacks across four RAG pipelines and multiple evaluation frameworks (Auto-ARGUE and MiRAGE). Our findings demonstrate strong correlations between coverage-based retrieval metrics and nugget coverage in generated responses at both topic and system levels. These findings provide empirical support for using retrieval metrics as proxies for RAG performance.

P234 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2603.27819] KVSculpt: KV Cache Compression as Distillation
     We propose KVSculpt, which moves to the other end of this spectrum: instead of selecting or combining original pairs, we optimize a smaller set of unconstrained KV pairs in continuous embedding space to preserve each layer's attention behavior. Adaptive allocation provides an additional 1.3x KL reduction at no extra inference cost. Analysis reveals that compression difficulty is highly non-uniform: per-layer pilot MSE varies by up to 100x across layers, and the two KV heads within a single layer can differ by up to 467x -- demonstrating that fine-grained budget allocation is essential.

P235 | Q: RAG에서 리랭킹 개선하는 연구들 정리해줘
     [2508.15437] Test-time Corpus Feedback: From Retrieval to RAG
     This static design often limits performance on complex tasks that require iterative evidence gathering or high-precision retrieval. Recent work in both the information retrieval (IR) and NLP communities has begun to close this gap by introducing adaptive retrieval and ranking methods that incorporate feedback. In this survey, we present a structured overview of advanced retrieval and ranking mechanisms that integrate such feedback. We categorize feedback signals based on their source and role in improving the query, retrieved context, or document pool.

P236 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2503.23250] Encrypted Prompt: Securing LLM Applications Against Unauthorized Actions
     Unlike previous approaches that aim to detect these attacks on a best-effort basis, this paper introduces a novel method that appends an Encrypted Prompt to each user prompt, embedding current permissions.

P237 | Q: RAG의 검색 정확도를 높이는 논문들을 분석해 보고, 아직 사람들이 시도하지 않은 '연구의 빈틈(Research Gap)'을 3가지 제안해 봐
     [2504.07803] A System for Comprehensive Assessment of RAG Frameworks
     To address this gap, we introduce SCARF (System for Comprehensive Assessment of RAG Frameworks), a modular and flexible evaluation framework designed to benchmark deployed RAG applications systematically. SCARF provides an end-to-end, black-box evaluation methodology, enabling a limited-effort comparison across diverse RAG frameworks. Using the REST APIs interface, we demonstrate how SCARF can be applied to real-world scenarios, showcasing its flexibility in assessing different RAG frameworks and configurations.

P238 | Q: LLM 환각 탐지 방법 논문들 비교해서 정리해줘
     [2309.01219] Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models
     We present taxonomies of the LLM hallucination phenomena and evaluation benchmarks, analyze existing approaches aiming at mitigating LLM hallucination, and discuss potential directions for future research.

P239 | Q: RAG의 검색 정확도를 높이는 논문들을 분석해 보고, 아직 사람들이 시도하지 않은 '연구의 빈틈(Research Gap)'을 3가지 제안해 봐
     [2508.05650] OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools
     We introduce OmniBench RAG, a novel automated platform for multi domain evaluation of RAG systems. We introduce two standardized metrics: Improvements (accuracy gains) and Transformation (efficiency differences between pre RAG and post RAG models), enabling reproducible comparisons across models and tasks. Our evaluation reveals striking variability in RAG effectiveness, from significant gains in culture to declines in mathematics, highlighting the critical importance of systematic, domain aware assessment. A demonstration video is available at: https://www.youtube.com/watch?v=BZx83QFcTCI.

P240 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2406.18122] Poisoned LangChain: Jailbreak LLMs by LangChain
     Given the increasing demand for real-time capabilities in large language models, real-time updates and iterations of new knowledge have become essential. Retrieval-Augmented Generation (RAG), an advanced technique to compensate for the model's lack of new knowledg… In this paper, we conduct the first work to propose the concept of indirect jailbreak and achieve Retrieval-Augmented Generation via LangChain. The experiments demonstrate that PLC successfully implemented indirect jailbreak attacks under three different scenarios, achieving success rates of 88.56%, 79.04%, and 82.69% respectively.

P241 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2503.20320] Iterative Prompting with Persuasion Skills in Jailbreaking Large Language Models
     Our results show that the attack success rates (ASR) increase as the attacking prompts become more refined with the highest ASR of 90% for GPT4 and ChatGLM and the lowest ASR of 68% for LLaMa2. Our technique outperforms baseline techniques (PAIR and PAP) in ASR and shows comparable performance with GCG and ArtPrompt.

P242 | Q: 지식 증류 관련 논문들 동향 알려줘
     [2412.13943] On Explaining Knowledge Distillation: Measuring and Visualising the Knowledge Transfer Process
     To address this, we proposed UniCAM, a novel gradient-based visual explanation method, which effectively interprets the knowledge learned during KD. Our experimental results demonstrate that with the guidance of the Teacher's knowledge, the Student model becomes more efficient, learning m… In contrast, residual features demonstrate more diffused attention, often targeting irrelevant areas, including the backgrounds of the target objects. Experiments on the CIFAR10, ASIRRA, and Plant Disease datasets demonstrate that UniCAM and the two metrics offer valuable insights to explain the KD process.

P243 | Q: RAG에서 노이즈 문서나 방해 문서에 대한 강건성을 다룬 연구 찾아줘
     [2405.07437] Evaluation of Retrieval-Augmented Generation: A Survey
     To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehensive overview of the evaluation and benchmarks of RAG systems. We then analyze the various datasets and metrics, discuss the limitations of current benchmarks, and suggest potential directions to advance the field of RAG benchmarks.

P244 | Q: 검색이 필요할 때만 검색하도록 판단하는 적응형 RAG 연구들 정리해줘
     [2603.21654] Towards Secure Retrieval-Augmented Generation: A Comprehensive Review of Threats, Defenses and Benchmarks
     Retrieval-Augmented Generation (RAG) significantly mitigates the hallucinations and domain knowledge deficiency in large language models by incorporating external knowledge bases. To the best of our knowledge, this paper presents the first end-to-end survey dedicated to the security of RAG systems.

P245 | Q: 지식 증류 관련 논문들 동향 알려줘
     [2607.15161] On-Policy Delta Distillation
     In this paper, we introduce a new distillation reward, termed the delta signal, instead of directly imitating the teacher's output distribution. Using extensive empirical evidence, we show that the delta signal substantially improves on-policy distillation and refer to the new distillation method as On-Policy Delta Distillation (OPD$^2$). Experiments across mathematics, science, and code-reasoning benchmarks demonstrate that OPD$^2$ consistently outperforms conventional on-policy distillation, enabling reasoning LLMs to achieve strong performance with only a short post-training period.

P246 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2503.23886] Text2Schema: Filling the Gap in Designing Database Table Structures based on Natural Language
     We propose SchemaAgent, an LLM-based multi-agent framework for Text2Schema. We also incorporate dedicated roles for reflection and inspection, along with an innovative error detection and correction mechanism to identify and rectify issues across various phases. Experimental results demonstrate the superiority of our approach over comparative work.

P247 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2601.10155] LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers
     We propose LOOKAT, which applies product quantization and asymmetric distance computation, to transformer architecture by decomposing key vectors into subspaces, learning codebooks and computing attention tables via lookup tables. LOOKAT achieves 64 $\times$compression at 95.7% output fidelity and 32$\times$compression at 95.0% fidelity when tested on GPT-2. Theoretical analysis confirms that rank correlation degrades as $O(d_k/mK)$, with guarantees validated across sequence lengths up to 1024 tokens.

P248 | Q: LLM 탈옥 공격 논문들 정리해줘
     [2503.20320] Iterative Prompting with Persuasion Skills in Jailbreaking Large Language Models
     Our results show that the attack success rates (ASR) increase as the attacking prompts become more refined with the highest ASR of 90% for GPT4 and ChatGLM and the lowest ASR of 68% for LLaMa2. Our technique outperforms baseline techniques (PAIR and PAP) in ASR and shows comparable performance with GCG and ArtPrompt.

P249 | Q: LLM 탈옥 공격이랑 방어 연구 정리해줘
     [2503.04856] M2S: Multi-turn to Single-turn jailbreak in Red Teaming for LLMs
     We introduce a novel framework for consolidating multi-turn adversarial ``jailbreak'' prompts into single-turn queries, significantly reducing the manual overhead required for adversarial testing of large language models (LLMs). Despite removing iterative back-and-forth interactions, these prompts preserve and often enhance adversarial potency: in extensive evaluations on the Multi-turn Human Jailbreak (MHJ) dataset, M2S methods achieve attack success rates from 70.6 percent to 95.9 percent across several state-of-the-art LLMs.

P250 | Q: 프롬프트 인젝션 공격 기법이나 방어 기법 연구 알려줘
     [2606.15441] Defending against Adaptive Prompt Injection Attacks via Reasoning-enabled Task Alignment
     To address these gaps, we propose RETA, a training-based method that grounds defense decisions on the user tasks rather than attacker-controlled data. Together, these allow the defender to be optimized via multi-objective reinforcement learning and achieve better safety-utility trade-off. Across six black-box adaptive attacks, RETA keeps every per-attack ASR below 10%, with average ASR of 2.92% and 3.75% on the two target models, while preserving most utility under attack and on clean inputs.

P251 | Q: Text-to-SQL 최근 연구들 어떤 방향으로 가고 있어?
     [2412.10138] ROUTE: Robust Multitask Tuning and Collaboration for Text-to-SQL
     To address this challenge, we propose a novel RObust mUltitask Tuning and collaboration mEthod (ROUTE) to improve the comprehensive capabilities of open-source LLMs for Text2SQL, thereby providing a more practical solution. This strategy leverages collaboration across several SQL-related tasks to reduce hallucinations during SQL generation, thereby maximizing the potential of enhancing Text2SQL performance through explicit multitask capabilities. The results demonstrate that our proposal outperforms the latest Text2SQL methods and yields leading performance.

P252 | Q: 요즘 LLM 양자화 연구들 정리해줘
     [2501.00032] Highly Optimized Kernels and Fine-Grained Codebooks for LLM Inference on Arm CPUs
     In this work, we propose a set of highly optimized kernels to accelerate LLM inference and unleash the full potential of CPUs, particularly Arm CPUs. Furthermore, we present a groupwise non-uniform codebook-based quantization method for ultra-low-precision quantization of LLMs to better match non-uniform patterns in their weight distributions, demonstrating better throughput during token generation wh… Applying these improvements to 4-bit LLMs results in a 3-3.2x improvement in prompt processing and a 2x improvement in autoregressive decoding on Arm CPUs, compared to LLaMA.cpp-based solution.

P253 | Q: 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어?
     [2410.14641] Distance between Relevant Information Pieces Causes Bias in Long-Context LLMs
     To bridge this gap, we present LongPiBench, a benchmark designed to assess positional bias involving multiple pieces of relevant information. These experiments reveal that while most current models are robust against the "lost in the middle" issue, there exist significant biases related to the spacing of relevant information pieces. These findings highlight the importance of evaluating and reducing positional biases to advance LLM's capabilities.

P254 | Q: KV 캐시 압축 관련 논문 5개 찾아서 설명해줘
     [2607.09683] Ablation, Statistical Inference, and Validation for KV-Cache Compression
     Key findings reveal that while eigenbasis-based methods fail on heavy-tailed data due to covariance instability, they excel in structured regimes, with the effective semantic dimension ($d_{eff}$) adapting to calibration budgets rather than true data rank.

