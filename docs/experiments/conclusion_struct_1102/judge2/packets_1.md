# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)

## H_A26 — 긴 동영상에서 필요한 장면을 찾아서 질문에 답하는 연구 알려줘

### 인용 블록

[문서 2]
[Distance: 0.3386]
[발행일: 2026-03-19]
[2603.18558v1] HiMu: Hierarchical Multimodal Frame Selection for Long Video Question Answering
[초록] Long-form video question answering requires reasoning over extended temporal contexts, making frame selection critical for large vision-language models (LVLMs) bound by finite context windows. Existing methods face a sharp trade-off: similarity-based selectors are fast but collapse compositional queries into a single dense vector, losing sub-event ordering and cross-modal bindings; agent-based methods recover this structure through iterative LVLM inference, but at prohibitive cost. We introduce HiMu, a training-free framework that bridges this gap. A single text-only LLM call decomposes the query into a hierarchical logic tree whose leaves are atomic predicates, each routed to a lightweight expert spanning vision (CLIP, open-vocabulary detection, OCR) and audio (ASR, CLAP). The resulting signals are normalized, temporally smoothed to align different modalities, and composed bottom-up through fuzzy-logic operators that enforce temporal sequencing and adjacency, producing a continuous satisfaction curve. Evaluations on Video-MME, LongVideoBench and HERBench-Lite show that HiMu advances the efficiency-accuracy Pareto front: at 16 frames with Qwen3-VL 8B it outperforms all competing selectors, and with GPT-4o it surpasses agentic systems operating at 32-512 frames while requiring roughly 10x fewer FLOPs.

### **2 Related Work**  
Frame selection methods for long-video QA span a spectrum from fast but shallow similarity scoring to accurate but expensive multi-call reasoning. We organize prior work along this efficiency–
reasoning axis, and separately review token-compression methods that address a complementary
bottleneck.  
**Similarity-based frame selection.** The most efficient selectors score each frame against the
[문서 5]
[Distance: 0.3613]
[발행일: 2026-06-28]
[2606.29445v1] Bridging VideoQA and Video-Guided Agentic Tasks via Generalized Keyframe Extraction
[초록] Video understanding is a fundamental capability for multimodal intelligence, and recent Multimodal Large Language Models (MLLMs) have achieved remarkable performance on Video Question Answering (VideoQA) benchmarks. However, existing benchmarks primarily evaluate whether models can perceive shallow visual cues, while rarely examining whether MLLMs can learn deeper knowledge or procedural skills from video tutorials and generalize them to downstream long-horizon agentic tasks. To address this gap, we introduce VG-GUIBench (Video-Guided GUI Benchmark), a new benchmark designed to evaluate whether MLLM-based GUI agents can follow video tutorials to complete corresponding GUI interactive tasks. Furthermore, we observe that the performance of models on both VideoQA and video-guided agentic tasks critically depends on effective keyframe extraction. Based on this observation, we propose TASKER (Task-driven And Scene-aware Keyframe searchER), a keyframe extraction algorithm that jointly considers task relevance and scene dynamics to identify informative frames. Experimental results demonstrate that TASKER achieves significant performance improvements on both VideoQA and video-guided agentic task benchmarks, outperforming the best baseline by 2.0% on the EgoSchema fullset and 1.8% on the NExT-QA dataset, respectively. These results further highlight the potential of generalized keyframe extraction methods for video understanding tasks. Our code and data are available at https://github.com/VG-GUI-TASKER/VG-GUI-TASKER.

38. Park, J., Ranasinghe, K., Kahatapitiya, K., Ryu, W., Kim, D., Ryoo, M.S.: Too many frames, not all useful: Efficient strategies for long-form video QA. In: Demberg, V., Inui, K., Marquez, L. (eds.) Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics, EACL 2026 - Volume 1: Long Papers, Rabat, Morocco, March 24-29, 2026. pp. 3569–3588. Association for Computational Linguistics (2026)

### 문장

- s1: 실험 결과는 TASKER가 VideoQA와 비디오 기반 에이전트 작업 벤치마크에서 모두 상당한 성능 향상을 보이며, 각각 EgoSchema 전체 데이터셋에서 최선의 베이스라인보다 2.0%, NExT-QA 데이터셋에서는 1.8% 더 높은 성능을 달성함을 보여준다. [2606.29445v1]
- s2: TASKER는 EgoSchema 전체 세트에서 베이스라인 대비 2.0%, NExT-QA 데이터셋에서 1.8%의 성능 향상을 보이며 VideoQA와 비디오 가이드 에이전트 작업 벤치마크 모두에서 기존 최고의 기준을 능가한다. [2606.29445v1]
- s3: HiMu는 Video-MME, LongVideoBench, HERBench-Lite에서 16 프레임으로 Qwen3-VL 8B를 사용해 모든 경쟁 선택기를 능가하고, GPT-4o와 함께 32~512 프레임을 사용하는 에이전트 시스템보다 약 10배 적은 FLOPs로 더 높은 효율·정확도 파레토 프론트를 달성한다. [2603.18558v1]
- s4: Video-MME, LongVideoBench 및 HERBench-Lite에서의 평가 결과에 따르면 HiMu는 효율성·정확성 파레토 프론트를 확장한다: Qwen3-VL 8B를 이용해 16 프레임에서 모든 경쟁 선택기를 능가하고, GPT-4o와 결합해 32~512 프레임의 에이전트 시스템을 제압하면서 약 10배 적은 FLOPs만 요구한다. [2603.18558v1]

## H_A27 — LLM이 만든 코드를 실행해 보고 오류 메시지를 보고 스스로 고치는 방법 다룬 논문 있어?

### 인용 블록

[문서 2]
[Distance: 0.2989]
[발행일: 2024-06-30]
[2407.01638v2] LASSI: An LLM-based Automated Self-Correcting Pipeline for Translating Parallel Scientific Codes
[초록] This paper addresses the problem of providing a novel approach to sourcing significant training data for LLMs focused on science and engineering. In particular, a crucial challenge is sourcing parallel scientific codes in the ranges of millions to billions of codes. To tackle this problem, we propose an automated pipeline framework called LASSI, designed to translate between parallel programming languages by bootstrapping existing closed- or open-source LLMs. LASSI incorporates autonomous enhancement through self-correcting loops where errors encountered during the compilation and execution of generated code are fed back to the LLM through guided prompting for debugging and refactoring. We highlight the bi-directional translation of existing GPU benchmarks between OpenMP target offload and CUDA to validate LASSI. The results of evaluating LASSI with different application codes across four LLMs demonstrate the effectiveness of LASSI for generating executable parallel codes, with 80% of OpenMP to CUDA translations and 85% of CUDA to OpenMP translations producing the expected output. We also observe approximately 78% of OpenMP to CUDA translations and 62% of CUDA to OpenMP translations execute within 10% of or at a faster runtime than the original benchmark code in the same language.

. Even if the LLM does not identify a fix, it might provide useful guidance to its human user toward a resolution.

LASSI incorporates a novel self-correction routine. The LLM attempts to rectify errors by re-prompting along with the context of specific compile or execute errors. This unique integration provides some autonomous control within the code generation pipeline. In the following subsection, we detail  
how errors encountered during compilation and execution are returned to the LLM through guided prompting for debugging and refactoring the generated code.

### 문장

- s1: 네 개의 대형 언어 모델(LLM)에서 다양한 애플리케이션 코드를 사용하여 LASSI를 평가한 결과는 LASSI가 실행 가능한 병렬 코드를 생성하는 데 효과적임을 보여주며, OpenMP에서 CUDA로의 변환의 80%와 CUDA에서 OpenMP로의 변환의 85%가 예상된 출력을 생성하였다. [2407.01638v2]
- s2: 또한 동일한 언어의 원래 벤치마크 코드보다 10% 이내이거나 더 빠른 실행 시간을 갖는 OpenMP에서 CUDA로의 번역은 약 78%, CUDA에서 OpenMP로의 번역은 약 62%를 차지한다는 것을 관찰한다. [2407.01638v2]
- s3: [2407.01638v2]는 LASSI 파이프라인을 통해 컴파일 및 실행 중 발생한 오류를 피드백으로 활용하여 코드 재작성을 수행했으며, OpenMP to CUDA 변환의 경우 80%가 예상 출력과 일치하고 78%가 벤치마크 대비 10% 이내 또는 더 빠른 런타임을 달성했습니다.

## H_A28 — 에이전트가 작업 계획을 먼저 세운 뒤 단계별로 실행하는 방식을 다룬 연구 핵심 내용 알려줘

### 인용 블록

[문서 5]
[Distance: 0.2734]
[발행일: 2026-03-13]
[2603.12710v1] AI Planning Framework for LLM-Based Web Agents
[초록] Developing autonomous agents for web-based tasks is a core challenge in AI. While Large Language Model (LLM) agents can interpret complex user requests, they often operate as black boxes, making it difficult to diagnose why they fail or how they plan. This paper addresses this gap by formally treating web tasks as sequential decision-making processes. We introduce a taxonomy that maps modern agent architectures to traditional planning paradigms: Step-by-Step agents to Breadth-First Search (BFS), Tree Search agents to Best-First Tree Search, and Full-Plan-in-Advance agents to Depth-First Search (DFS). This framework allows for a principled diagnosis of system failures like context drift and incoherent task decomposition. To evaluate these behaviors, we propose five novel evaluation metrics that assess trajectory quality beyond simple success rates. We support this analysis with a new dataset of 794 human-labeled trajectories from the WebArena benchmark. Finally, we validate our evaluation framework by comparing a baseline Step-by-Step agent against a novel Full-Plan-in-Advance implementation. Our results reveal that while the Step-by-Step agent aligns more closely with human gold trajectories (38% overall success), the Full-Plan-in-Advance agent excels in technical measures such as element accuracy (89%), demonstrating the necessity of our proposed metrics for selecting appropriate agent architectures based on specific application constraints.

original intent even after many steps. Another reason for failure is that the agent fails to decompose a task into coherent  
multi-step actions [ 16 ]. Consequently, it may lose track of task goals or generate inconsistent plans. By exploring the  
reasons why agents fail, we conclude that many reasons are related to the planning approach the agent employs, and  
we suggest that choosing an agent based on the need would lead to better performance.

### 문장

- s1: 이 논문의 결과는 Step-by-Step 에이전트가 인간 골드 트래젝토리와 더 밀접하게 일치한다(전체 성공률 38%)는 점을 보여주지만, Full-Plan-in-Advance 에이전트는 요소 정확도(89%)와 같은 기술적 지표에서 뛰어난 성능을 발휘함으로써 특정 응용 제약에 따라 적절한 에이전트 아키텍처를 선택하기 위해 이 논문이 제안한 메트릭의 필요성을 입증한다. [2603.12710v1]
- s2: [2603.12710v1]는 Step-by-Step 에이전트와 Full-Plan-in-Advance 구현을 비교하여, 전자가 인간 금표 트래젝토리와 더 잘 일치하지만(38% 전체 성공률), 후자가 기술적 지표인 요소 정확도에서 우수한 성능(89%)을 보임을 보여줍니다.

## H_A32 — 전문가 혼합(MoE) 모델에서 토큰을 어느 전문가에게 보낼지 정하는 라우팅을 개선한 연구 알려줘

### 인용 블록

[문서 2]
[Distance: 0.3927]
[발행일: 2026-06-12]
[2607.08780v1] Sticky Routing: Training MoE Models for Memory-Efficient Inference
[초록] Mixture-of-Experts (MoE) models activate only a sparse subset of experts per token, yet consecutive tokens frequently activate different experts -- causing constant weight swapping between slow storage and fast memory on edge devices. Existing remedies are either system-level (caching heuristics) or post-hoc (router fine-tuning), leaving the root cause unchanged during pretraining. We propose StickyMoE, a differentiable routing consistency loss that penalises abrupt expert switches between adjacent tokens, encouraging the router to maintain the same expert assignment across semantically coherent spans. StickyMoE requires no architectural changes, adds a single hyperparameter lambda, and unlike post-hoc methods, allows expert representations and routing decisions to co-adapt from the first training step. Experiments on small-scale MoE language models show that StickyMoE reduces the expert switch rate by up to 60% with less than 4% perplexity degradation, Pareto-dominating post-hoc fine-tuning on the quality-locality frontier. Routing temporal locality is most efficiently instilled at training time.

. We propose StickyMoE, a differentiable _routing consistency loss_ that penalises abrupt expert switches between adjacent tokens, encouraging the router to maintain the same expert assignment across semantically coherent spans. StickyMoE requires no architectural changes, adds a single hyperparameter _λ_ , and unlike post-hoc methods, allows expert representations and routing decisions to co-adapt from the first training step

### 문장

- s1: StickyMoE는 소규모 MoE 언어 모델에서 전문가 전환율을 최대 60%까지 감소시키며, 퍼플렉시티 저하가 4% 미만으로 제한된다는 결과를 보여준다 [2607.08780v1].
- s2: 소규모 MoE 언어 모델에 대한 실험 결과, StickyMoE는 전문가 전환률을 최대 60% 감소시키면서 퍼플렉시티 저하가 4% 미만으로 제한되며, 품질-위치 프론티어에서 Pareto-dominating post-hoc fine-tuning을 달성한다. [2607.08780v1]

## H_A34 — LLM 답변에 성별이나 인종 편향이 있는지 측정하는 벤치마크 연구 알려줘

### 인용 블록

[문서 2]
[Distance: 0.2803]
[발행일: 2025-03-31]
[2503.24310v1] BEATS: Bias Evaluation and Assessment Test Suite for Large Language Models
[초록] In this research, we introduce BEATS, a novel framework for evaluating Bias, Ethics, Fairness, and Factuality in Large Language Models (LLMs). Building upon the BEATS framework, we present a bias benchmark for LLMs that measure performance across 29 distinct metrics. These metrics span a broad range of characteristics, including demographic, cognitive, and social biases, as well as measures of ethical reasoning, group fairness, and factuality related misinformation risk. These metrics enable a quantitative assessment of the extent to which LLM generated responses may perpetuate societal prejudices that reinforce or expand systemic inequities. To achieve a high score on this benchmark a LLM must show very equitable behavior in their responses, making it a rigorous standard for responsible AI evaluation. Empirical results based on data from our experiment show that, 37.65\% of outputs generated by industry leading models contained some form of bias, highlighting a substantial risk of using these models in critical decision making systems. BEATS framework and benchmark offer a scalable and statistically rigorous methodology to benchmark LLMs, diagnose factors driving biases, and develop mitigation strategies. With the BEATS framework, our goal is to help the development of more socially responsible and ethically aligned AI models.

## **2.7.2 Computational Representation for Fairness Detection and Evaluation**

Fairness in machine learning systems, particularly in LLMs, is critical to ensuring equitable treatment across diverse demographic groups. To rigorously evaluate fairness in LLM-generated responses, we define a set of structured fairness metrics that capture parity, opportunity, and group-level equity. These metrics provide a quantifiable framework for assessing how fairly the model treats different population segments.

### 문장

- s1: BEATS 벤치마크는 29개의 메트릭을 통해 LLM의 편향을 측정하며, 실험 결과 산업 선도 모델의 37.65%가 어떤 형태의 편향을 포함하고 있음을 보여준다[2503.24310v1].
- s2: 본 실험 데이터를 기반으로 한 실증 결과는 산업계 선두 모델이 생성한 출력 중 약 37.65%가 어떤 형태의 편향을 포함하고 있음을 보여주어, 이러한 모델을 핵심 의사결정 시스템에 적용할 때 상당한 위험이 존재함을 강조한다. [2503.24310v1]

## H_A35 — 차트나 그래프 이미지를 보고 질문에 답하는 모델 연구 핵심 내용 설명해줘

### 인용 블록

[문서 2]
[Distance: 0.2922]
[발행일: 2024-12-26]
[2412.19146v1] AskChart: Universal Chart Understanding through Textual Enhancement
[초록] Chart understanding tasks such as ChartQA and Chart-to-Text involve automatically extracting and interpreting key information from charts, enabling users to query or convert visual data into structured formats. State-of-the-art approaches primarily focus on visual cues from chart images, failing to explicitly incorporate rich textual information (e.g., data labels and axis labels) embedded within the charts. This textual information is vital for intuitive human comprehension and interpretation of charts. Moreover, existing models are often large and computationally intensive, limiting their practical applicability. In this paper, we introduce AskChart, a universal model that explicitly integrates both textual and visual cues from charts using a Mixture of Experts (MoE) architecture. AskChart facilitates the learning of enhanced visual-textual representations of charts for effectively handling multiple chart understanding tasks, while maintaining a smaller model size. To capture the synergy between visual and textual modalities, we curate a large-scale dataset named ChartBank with about 7.5M data samples, which helps align textual and visual information and facilitates the extraction of visual entities and text. To effectively train AskChart, we design a three-stage training strategy to align visual and textual modalities for learning robust visual-textual representations and optimizing the learning of the MoE layer. Extensive experiments across five datasets demonstrate the significant performance gains of AskChart in four chart understanding tasks. Remarkably, AskChart with 4.6B parameters outperforms state-of-the-art models with 13B parameters by 68.3% in Open-ended ChartQA and 49.2% in Chart-to-Text tasks, while achieving comparable performance in ChartQA and Chart-to-Table tasks.

## 2 RELATED WORK

**Chart Understanding.** In chart understanding, key tasks have emerged, each focusing on interpreting and reasoning over chart data Luo et al. (2022b; 2021); Qin et al. (2020). ChartQA (Hoque et al., 2022; Xu et al., 2023) involves answering questions related to both the content and structure of charts, requiring models to extract insights from graphical elements
[문서 3]
[Distance: 0.2806]
[발행일: 2026-04-03]
[2604.03157v1] Chart-RL: Policy Optimization Reinforcement Learning for Enhanced Visual Reasoning in Chart Question Answering with Vision Language Models
[초록] The recent advancements in Vision Language Models (VLMs) have demonstrated progress toward true intelligence requiring robust reasoning capabilities. Beyond pattern recognition, linguistic reasoning must integrate with visual comprehension, particularly for Chart Question Answering (CQA) tasks involving complex data visualizations. Current VLMs face significant limitations in CQA, including imprecise numerical extraction, difficulty interpreting implicit visual relationships, and inadequate attention mechanisms for capturing spatial relationships in charts. In this work, we address these challenges by presenting Chart-RL, a novel reinforcement learning framework that enhances VLMs chart understanding through feedback-driven policy optimization of visual perception and logical inference. Our key innovation includes a comprehensive framework integrating Reinforcement Learning (RL) from Policy Optimization techniques along with adaptive reward functions, that demonstrates superior performance compared to baseline foundation models and competitive results against larger state-of-the-art architectures. We also integrated Parameter-Efficient Fine-Tuning through Low-Rank Adaptation (LoRA) in the RL framework that only requires single GPU configurations while preserving performance integrity. We conducted extensive benchmarking across open-source, proprietary, and state-of-the-art closed-source models utilizing the ChartQAPro dataset. The RL fine-tuned Qwen3-VL-4B-Instruct model achieved an answer accuracy of 0.634, surpassing the 0.580 accuracy of the Qwen3-VL-8B-Instruct foundation model despite utilizing half the parameter count, while simultaneously reducing inference latency from 31 seconds to 9 seconds.

combine chart reading (recognition) and chart understanding (comprehension) to decipher underlying data patterns.
Thereby, Chart Question Answering (CQA) has emerged as
the standard, rigorous task to probe the visual reasoning
capabilities of VLMs.  
There are challenges in VLMs when handling CQA tasks,
including less precise numerical extraction and computation
for complex visual elements such as overlapping lines or
stacked bars, implicit relationships between visual elements

### 문장

- s1: Chart-RL은 정책 최적화 강화학습을 적용해 수치 추출과 시각적 관계 해석의 한계를 극복했으며, Qwen3-VL-4B-Instruct 모델이 0.634의 정확도를 달성해 8B 버전보다 높은 성능과 빠른 추론 속도를 보였습니다. [2604.03157v1]
- s2: AskChart는 텍스트 정보를 강화하여 기존 시각적 단서만 활용하던 접근법보다 성능을 크게 향상시켰으며, 4.6B 파라미터 모델이 13B 파라미터 모델을 Open-ended ChartQA에서 68.3%, Chart-to-Text에서 49.2% 더 높은 정확도로 능가했습니다. [2412.19146v1]
- s3: RL로 미세 조정된 Qwen3-VL-4B-Instruct 모델은 파라미터 수가 절반임에도 불구하고 기반 모델인 Qwen3-VL-8B-Instruct의 정확도 0.580보다 높은 0.634의 답변 정확도를 달성했으며, 추론 지연 시간을 31초에서 9초로 동시에 감소시켰다. [2604.03157v1]
- s4: Remarkably, AskChart with 4.6B parameters outperforms state-of-the-art models with 13B parameters by 68.3% in Open-ended ChartQA and 49.2% in Chart-to-Text tasks, while achieving comparable performance in ChartQA and Chart-to-Table tasks. [2412.19146v1]

## H_A40 — 로봇 팔이 물건을 집는 동작을 강화학습으로 배우는 연구 핵심 내용 알려줘

### 인용 블록

[문서 1]
[Distance: 0.3181]
[발행일: 2025-03-26]
[2503.20208v2] Learning Adaptive Dexterous Grasping from Single Demonstrations
[초록] How can robots learn dexterous grasping skills efficiently and apply them adaptively based on user instructions? This work tackles two key challenges: efficient skill acquisition from limited human demonstrations and context-driven skill selection. We introduce AdaDexGrasp, a framework that learns a library of grasping skills from a single human demonstration per skill and selects the most suitable one using a vision-language model (VLM). To improve sample efficiency, we propose a trajectory following reward that guides reinforcement learning (RL) toward states close to a human demonstration while allowing flexibility in exploration. To learn beyond the single demonstration, we employ curriculum learning, progressively increasing object pose variations to enhance robustness. At deployment, a VLM retrieves the appropriate skill based on user instructions, bridging low-level learned skills with high-level intent. We evaluate AdaDexGrasp in both simulation and real-world settings, showing that our approach significantly improves RL efficiency and enables learning human-like grasp strategies across varied object configurations. Finally, we demonstrate zero-shot transfer of our learned policies to a real-world PSYONIC Ability Hand, with a 90% success rate across objects, significantly outperforming the baseline.

**Implementation.** We adopt Proximal Policy Optimization (PPO) [57] for policy learning. The robot observes the full simulation state, including all joint angles, and the poses of the hand, fingertips, and objects, represented in the robot arm base frame. The policy outputs joint angle deltas, indicating real-time changes for actuation. For each object and grasp pose, we train the policy for 80M steps with a fixed initial pose, followed by another 120M steps using the proposed curriculum
[문서 2]
[Distance: 0.3913]
[발행일: 2026-06-22]
[2607.00033v2] Learning Dexterous Manipulation Using Contact Wrench Guidance From Human Demonstration
[초록] Dexterous robot manipulation can benefit from the abundance of human demonstrations, but transferring such demonstrations to robot policies remains challenging. We present Contact Wrench Guidance from Human Demonstration in Robotic Dexterous Manipulation (CHORD), a framework for long-horizon manipulation of rigid and articulated objects with reinforcement learning. The key idea is object-centric contact wrench space guidance: we represent human and robot motions by the forces and torques they can induce on the object, enabling similarity to be measured by the induced instantaneous motions. This guidance makes reinforcement learning more scalable for contact-rich dexterous manipulation. We further introduce a large-scale simulation benchmark with 4,739 bimanual dexterous manipulation tasks, constructed from motion-capture datasets and reconstructed in-house videos. Evaluated on 1,831 benchmark tasks, CHORD achieves an average success rate of 82.12%, demonstrating strong scalability. CHORD also generalizes to whole-body manipulation from hand-only and third-person demonstrations, achieving a 90.77% success rate, and the learned policies transfer to the real world in both open-loop and closed-loop settings.

## **3.2. Efficient, Robust, and Generalizable Policy Learning**

In addition to the contact reward in Section 3.1, we incorporate several mechanisms to improve training efficiency and robustness. First, we reset the simulator to arbitrary states along the reference trajectory and keep the VOC fully active for a short stabilization window, allowing the robot to recover contact before assistance is annealed

### 문장

- s1: 1,831개의 벤치마크 작업에서 평가된 CHORD는 평균 성공률 82.12%를 달성하여 뛰어난 확장성을 보였습니다. [2607.00033v2]
- s2: 마지막으로, 학습된 정책을 실제 PSYONIC Ability 핸드에 적용하여 대상별로 90%의 성공률을 달성함으로써 베이스라인을 크게 능가하는 제로샷 전이를 증명한다. [2503.20208v2]
- s3: [2503.20208v2]은 시뮬레이션과 실제 환경 모두에서 AdaDexGrasp 접근법이 RL 효율성을 크게 향상시키고 다양한 객체 구성에 대해 인간과 유사한 집기 전략을 학습하며, PSYONIC Ability Hand에서 90%의 성공률을 보였습니다.
- s4: 또한 [2607.00033v2]는 대규모 시뮬레이션 벤치마크(4,739개 작업)와 실제 전이 실험을 통해 CHORD가 평균 82.12%의 성공률을 기록하고, 전체 신체 조작으로 확장되어 오픈-루프 및 클로즈-루프 설정에서 각각 90.77%와 높은 성능을 달성했습니다.
- s5: CHORD는 손만 사용하는 시연과 타자 시연을 기반으로 전신 조작으로 일반화되어 90.77%의 성공률을 달성했으며, 학습된 정책은 개방 루프와 폐쇄 루프 환경 모두에서 실제 세계로 이전됩니다. [2607.00033v2]

## H_B17 — Chain-of-Thought 프롬프팅 논문 자세히 설명해줘

### 인용 블록

[문서 1]
[Distance: 0.2399]
[발행일: 2022-01-28]
[2201.11903v6] Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
[초록] We explore how generating a chain of thought -- a series of intermediate reasoning steps -- significantly improves the ability of large language models to perform complex reasoning. In particular, we show how such reasoning abilities emerge naturally in sufficiently large language models via a simple method called chain of thought prompting, where a few chain of thought demonstrations are provided as exemplars in prompting. Experiments on three large language models show that chain of thought prompting improves performance on a range of arithmetic, commonsense, and symbolic reasoning tasks. The empirical gains can be striking. For instance, prompting a 540B-parameter language model with just eight chain of thought exemplars achieves state of the art accuracy on the GSM8K benchmark of math word problems, surpassing even finetuned GPT-3 with a verifier.

Chain-of-thought prompting has several attractive properties as an approach for facilitating reasoning in language models.  
1. First, chain of thought, in principle, allows models to decompose multi-step problems into intermediate steps, which means that additional computation can be allocated to problems that require more reasoning steps.
[문서 2]
[Distance: 0.2412]
[발행일: 2022-01-28]
[2201.11903v6] Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
[초록] We explore how generating a chain of thought -- a series of intermediate reasoning steps -- significantly improves the ability of large language models to perform complex reasoning. In particular, we show how such reasoning abilities emerge naturally in sufficiently large language models via a simple method called chain of thought prompting, where a few chain of thought demonstrations are provided as exemplars in prompting. Experiments on three large language models show that chain of thought prompting improves performance on a range of arithmetic, commonsense, and symbolic reasoning tasks. The empirical gains can be striking. For instance, prompting a 540B-parameter language model with just eight chain of thought exemplars achieves state of the art accuracy on the GSM8K benchmark of math word problems, surpassing even finetuned GPT-3 with a verifier.

Figure 4: Chain-of-thought prompting enables large language models to solve challenging math problems. Notably, chain-of-thought reasoning is an emergent ability of increasing model scale. Prior best numbers are from Cobbe et al. (2021) for GSM8K, Jie et al. (2022) for SVAMP, and Lan et al. (2021) for MAWPS.

### 문장

- s1: 예를 들어, 사슬 사고 (chain of thought) 예시 8개만을 사용하여 파라미터가 540B인 언어 모델을 프롬프트하면 수학 단어 문제 벤치마크인 GSM8K에서 최첨단 정확도를 달성하여, 검증기를 갖춘 파인튜닝된 GPT-3보다도 뛰어난 성능을 보였습니다. [2201.11903v6]
- s2: 특히 540B 파라미터 규모의 언어 모델을 8개의 예시만으로 프롬핑했을 때 GSM8K 벤치마크에서 최첨단 정확도를 달성하고, 검증기가 포함된 파인튜닝된 GPT-3를 능가한다는 구체적인 성과가 두 문서 모두에 명시되어 있습니다 [2201.11903v6].

## H_C19 — LLM 에이전트가 위험한 행동을 하지 않게 막는 안전성 연구들 정리해줘

### 인용 블록

[문서 2]
[Distance: 0.3359]
[발행일: 2026-06-22]
[2608.14590v1] Toward Safe LLM Agents: A Survey of Specification, Verification, and Enforcement
[초록] Second, runtime monitoring is the most mature enforcement strategy, reducing unsafe actions by 40% to 65% in controlled settings, but it does not provide complete safety guarantees. Third, the verifier tax shows that blocking 94% of unsafe actions can still result in less than 5% safe task completion because agents exploit alternative unsafe paths.

### 문장

- s1: 셋째, 검증자 세금은 위험 행동을 94% 차단해도 대체적인 위험 경로를 이용해 에이전트가 안전 작업 완료율을 5% 미만으로 낮출 수 있음을 보여준다. [2608.14590v1]
- s2: 그러나 구체적인 실험 결과에서는 검증기 사용 시 위험 행동을 94% 차단해도 안전한 작업 완료율이 5% 미만으로 떨어지는 현상이 관찰되어, 에이전트가 대체 경로를 통해 위험을 우회한다는 한계가 드러납니다[2608.14590v1].

## H_C22 — 멀티모달 LLM이 이미지 속 글자를 읽는 능력을 평가한 연구들 조사해줘

### 인용 블록

[문서 2]
[Distance: 0.2249]
[발행일: 2024-10-17]
[2410.13611v1] H2OVL-Mississippi Vision Language Models Technical Report
[초록] To address this need, we present H2OVL-Mississippi, a pair of small VLMs trained on 37 million image-text pairs using 240 hours of compute on 8 x H100 GPUs. H2OVL-Mississippi-0.8B is a tiny model with 0.8 billion parameters that specializes in text recognition, achieving state of the art performance on the Text Recognition portion of OCRBench and surpassing much larger models in this area.
[문서 3]
[Distance: 0.2861]
[발행일: 2026-03-30]
[2603.27942v2] JaWildText: A Benchmark for Vision-Language Models on Japanese Scene Text Understanding
[초록] To fill this gap, we introduce JaWildText, a diagnostic benchmark for evaluating vision-language models (VLMs) on Japanese scene text understanding. JaWildText contains 3,241 instances from 2,961 images newly captured in Japan, with 1.12 million annotated characters spanning 3,643 unique character types. Error analyses show recognition remains the dominant bottleneck, especially for kanji.

### 문장

- s1: H2OVL-Mississippi-0.8B is a tiny model with 0.8 billion parameters that specializes in text recognition, achieving state of the art performance on the Text Recognition portion of OCRBench and surpassing much larger models in this area. [2410.13611v1]
- s2: H2OVL-Mississippi-0.8B는 0.8억 파라미터 규모의 소형 모델이며, OCRBench의 텍스트 인식 부분에서 최첨단 성능을 달성하고 더 큰 모델을 능가한다[2410.13611v1].
- s3: JaWildText는 일본 현장 텍스트 이해를 평가하기 위한 벤치마크로, 3,241개의 인스턴트와 1.12백만 개의 주석된 문자를 포함하며, 특히 한자 인식에서 오류가 주요 병목 현상으로 나타난다[2603.27942v2].
- s4: JaWildText contains 3,241 instances from 2,961 images newly captured in Japan, with 1.12 million annotated characters spanning 3,643 unique character types. [2603.27942v2]

