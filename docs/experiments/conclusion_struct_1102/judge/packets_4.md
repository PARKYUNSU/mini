# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)

## H_C15 — 수학 문제 풀이 능력을 높이는 LLM 학습 방법 연구 트렌드 알려줘

### 인용 블록

[문서 1]
[Distance: 0.2449]
[발행일: 2024-06-26]
[2406.18321v1] MathOdyssey: Benchmarking Mathematical Problem-Solving Skills in Large Language Models Using Odyssey Math Data
[초록] By providing the MathOdyssey dataset as a resource to the AI community, we aim to contribute to the understanding and improvement of AI capabilities in complex mathematical problem-solving. Our analysis shows a narrowing performance gap between open-source and closed-source models, yet substantial challenges remain, particularly with the most demanding problems.
[문서 2]
[Distance: 0.2653]
[발행일: 2024-12-28]
[2501.00059v1] Large Language Models for Mathematical Analysis
[초록] We developed the DEMI-MathAnalysis dataset, comprising proof-based problems from mathematical analysis topics such as Sequences and Limits, Infinite Series, and Convex Functions. Through fine-tuning LLMs on this dataset and employing our framework, we observed significant improvements in their capability to generate logical, complete, and elegant proofs.
[문서 3]
[Distance: 0.3165]
[발행일: 2024-10-17]
[2410.13293v2] SBI-RAG: Enhancing Math Word Problem Solving for Students through Schema-Based Instruction and Retrieval-Augmented Generation
[초록] Building on this, we propose a Schema-Based Instruction Retrieval-Augmented Generation (SBI-RAG) framework that incorporates a large language model (LLM). Our findings suggest that SBI-RAG enhances reasoning clarity and facilitates a more structured problem-solving process potentially providing educational benefits for students.

### 문장

- s1: DEMIMathAnalysis 데이터셋을 개발하였으며, 이 데이터셋은 수열과 극한, 무한급수, 볼록함수와 같은 해석학 주제에 기반한 증명 문제를 포함하고 있습니다. [2501.00059v1]
- s2: 먼저, MathOdyssey 데이터셋을 활용한 연구에서는 오픈소스와 클로즈드 소스 모델 간의 성능 격차가 좁혀졌지만, 특히 어려운 문제에서는 여전히 큰 도전 과제가 남아있음을 보여줍니다[2406.18321v1].
- s3: 두 번째 연구는 DEMI-MathAnalysis 데이터셋으로 LLM을 미세 조정함으로써 논리적이며 완전하고 우아한 증명을 생성하는 능력에 상당한 개선을 관찰했습니다[2501.00059v1].
- s4: 이를 바탕으로 이 논문은 대규모 언어 모델(LLM)을 통합한 스키마 기반 지시 검색 증강 생성(SBI-RAG) 프레임워크를 제안한다. [2410.13293v2]
- s5: 세 번째 연구에서는 스키마 기반 지시와 검색 강화 생성(SBI-RAG) 프레임워크를 적용하여 추론 명확성을 향상시키고 구조화된 문제 해결 과정을 촉진한다는 점을 발견했습니다[2410.13293v2].
- s6: MathOdyssey 데이터셋을 AI 커뮤니티에 제공함으로써 복잡한 수학 문제 해결 능력을 이해하고 개선하는 데 기여하고자 합니다. [2406.18321v1]

## H_C17 — LLM 출력의 불확실성을 추정하는 연구들 조사해줘

### 인용 블록

[문서 1]
[Distance: 0.2398]
[발행일: 2024-06-28]
[2406.19712v1] Uncertainty Quantification in Large Language Models Through Convex Hull Analysis
[초록] This study proposes a novel geometric approach to uncertainty quantification using convex hull analysis.
[문서 2]
[Distance: 0.3457]
[발행일: 2024-10-28]
[2410.20783v1] Graph-based Uncertainty Metrics for Long-form Language Model Outputs
[초록] In this work, we propose Graph Uncertainty -- which represents the relationship between LLM generations and claims within them as a bipartite graph and estimates the claim-level uncertainty with a family of graph centrality metrics. Compared to existing methods, our graph-based uncertainty metrics lead to an average of 6.8% relative gains on AUPRC across various long-form generation settings, an…

### 문장

- s1: 본 연구는 볼록 껍질 분석을 활용한 새로운 기하학적 접근법을 제안하여 불확실성 정량화를 수행한다. [2406.19712v1]
- s2: 먼저, convex hull 분석을 통한 기하학적 접근이 제안되었으며 [2406.19712v1]에서 이를 통해 불확실성 정량화를 수행했습니다.
- s3: 또한, 그래프 기반 메트릭은 다양한 장형 생성 설정에서 AUPRC 평균 상대 향상률이 6.8%로 보고되었고 [2410.20783v1]에서 이러한 성능 향상이 확인되었습니다.
- s4: 기존 방법과 비교하여, 본 논문에서 제안한 그래프 기반 불확실성 지표는 다양한 긴 형식 생성 설정에서 AUPRC에 대해 평균 6.8%의 상대적 향상을 달성한다. [2410.20783v1]

## H_C18 — 음성 비서에 LLM을 붙인 연구 동향 정리해줘

### 인용 블록

[문서 1]
[Distance: 0.3844]
[발행일: 2024-03-29]
[2403.20262v3] ELITR-Bench: A Meeting Assistant Benchmark for Long-Context Language Models
[초록] In contrast, we propose a new benchmark for long-context LLMs focused on a practical meeting assistant scenario in which the long contexts consist of transcripts obtained by automatic speech recognition, presenting unique challenges for LLMs due to the inherent noisiness and oral nature of such data.
[문서 2]
[Distance: 0.4001]
[발행일: 2026-05-14]
[2605.15104v1] From Text to Voice: A Reproducible and Verifiable Framework for Evaluating Tool Calling LLM Agents
[초록] Based on extensive evaluation of 7 omni-modal models on audio-converted versions of Confetti and When2Call, our framework demonstrates that the performance is strongly model- and task-dependent: Gemini-3.1-Flash-Live obtains the highes… Notably, we find that open-source Qwen3 judges with at least 8B parameters exceed 80% agreement with proprietary judges, supporting privacy-preserving evaluation.

### 문장

- s1: 반면, 이 논문은 자동 음성 인식으로 얻은 전사들로 구성된 긴 컨텍스트를 갖는 실용적인 회의 보조 시나리오에 초점을 맞춘 새로운 벤치마크를 제안한다. 이러한 데이터는 본질적인 잡음과 구어적 특성 때문에 LLM에게 독특한 도전을 제시한다. [2403.20262v3]
- s2: 반면 [2605.15104v1]는 Confetti와 When2Call이라는 두 오디오 변환 버전에서 7개의 오모디얼 모델을 평가하여 성능이 모델과 작업에 크게 의존한다는 점을 강조하고, 특히 오픈소스 Qwen3(최소 8B 파라미터)가 독점적 판정자와 80% 이상의 일치율을 보인다고 언급합니다.
- s3: [2403.20262v3]은 자동 음성 인식(ASR)으로 생성된 긴 회의 전사 데이터를 대상으로 한 새로운 벤치마크를 제안하며, 이러한 데이터의 고유한 잡음과 구두적 특성이 LLM에 독특한 도전을 제시한다고 보고합니다.
- s4: Confetti 와 When2Call 의 오디오 변환 버전에서 7 개의 오모달 모델을 광범위하게 평가한 결과, 본 프레임워크는 성능이 모델과 작업에 크게 의존함을 보여주며, Gemini-3.1-Flash-Live 는 높은 …를 달성하고, 특히 오픈소스 Qwen3(최소 8B 파라미터) 가 독점적 판정자와 80% 이상의 일치도를 보임으로써 프라이버시 보호 평가를 지원한다는 점을 발견하였다. [2605.15104v1]

## H_D01 — BM25랑 밀집 검색은 어떤 질문에서 성능이 갈려? 비교한 연구 알려줘

### 인용 블록

[문서 1]
[Distance: 0.3353]
[발행일: 2026-07-29]
[2607.26497v3] BM25 Wins at Scale: A Scaling Study of Retrieval-Augmented Generation Paradigms
[초록] Retrieval-augmented generation (RAG) spans lexical and dense retrieval, graph-based indexing, and agentic search, but these paradigms are usually evaluated on different benchmarks at one corpus size, leaving their accuracy-cost scaling unclear. To bridge this gap, we present a controlled study that varies corpus size along 28 strictly nested tiers spanning roughly 450-fold, while holding questions and a fixed bedrock of relevant and adversarial documents unchanged. Under one reader model and one judging protocol, we measure official accuracy, construction and query tokens, and latency. The results reveal a scale-dependent crossover rather than an unconditional winner. File-System Agent leads at the smallest shared tiers, but its sequential exploration costs 39 times more query tokens at the bedrock and becomes less effective as the search space grows. Around 10 million corpus tokens, BM25 overtakes it and leads at every larger shared tier, with a margin approaching 20 points at full scale. BM25 also anchors the low-cost end of the Pareto frontier without LLM-based construction. Dense retrieval remains efficient but less accurate, whereas graph-based RAG encounters construction walls before deployment scale and its scalable variants remain below BM25 at shared tiers. Overall, corpus growth increasingly favors global candidate ranking: lexical retrieval is the strongest scalable default, while agentic reasoning works best after ranked discovery rather than in place of it.

These controls leave BM25 above dense and graph retrieval under comparable retrieval depth. In a 90question proposal-sensitivity audit, direct full-corpus DenseRAG top-10 retrieval overlaps the historical BM25prefiltered dense candidates by 1.2 documents on average, recovers 57 of 431 confirmed items, and identifies 115 traps plus 100 not-found lures
[문서 2]
[Distance: 0.3298]
[발행일: 2020-04-10]
[2004.04906v3] Dense Passage Retrieval for Open-Domain Question Answering
[초록] Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

. We find that DPR generalizes well, with 3-5 points loss from the best performing fine-tuned model in top-20 retrieval accuracy (69.9/86.3 vs. 75.0/89.1 for WebQuestions and TREC, respectively), while still greatly outperforming the BM25 baseline (55.0/70.9).
[문서 3]
[Distance: 0.4217]
[발행일: 2026-04-15]
[2604.13728v1] Hybrid Retrieval for COVID-19 Literature: Comparing Rank Fusion and Projection Fusion with Diversity Reranking
[초록] We present a hybrid retrieval system for COVID-19 scientific literature, evaluated on the TREC-COVID benchmark (171,332 papers, 50 expert queries). The system implements six retrieval configurations spanning sparse (SPLADE), dense (BGE), rank-level fusion (RRF), and a projection-based vector fusion (B5) approach. RRF fusion achieves the best relevance (nDCG@10 = 0.828), outperforming dense-only by 6.1% and sparse-only by 14.9%. Our projection fusion variant reaches nDCG@10 = 0.678 on expert queries while being 33% faster (847 ms vs. 1271 ms) and producing 2.2x higher ILD@10 than RRF. Evaluation across 400 queries -- including expert, machine-generated, and three paraphrase styles -- shows that B5 delivers the largest relative gain on keyword-heavy reformulations (+8.8%), although RRF remains best in absolute nDCG@10. On expert queries, MMR reranking increases intra-list diversity by 23.8-24.5% at a 20.4-25.4% nDCG@10 cost. Both fusion pipelines evaluated for latency remain below the sub-2 s target across all query sets. The system is deployed as a Streamlit web application backed by Pinecone serverless indices.

. Evaluation across 400 queries revealed that the optimal system depends on query characteristics: RRF for expert-crafted queries, SPLADE for keyword-like generated queries, and B5 shows the largest relative improvement on keyword-heavy reformulations (+8.8%) even though RRF remains best in absolute nDCG@10. On expert queries, MMR consistently increases diversity at a measurable relevance cost, positioning it as a deliberate design choice rather than a default improvement.

### 문장

- s1: Around 10 million corpus tokens, BM25 overtakes it and leads at every larger shared tier, with a margin approaching 20 points at full scale. [2607.26497v3]
- s2: 전문가 쿼리에 대해 MMR 재순위화는 nDCG@10이 20.4~25.4% 감소하는 비용으로 리스트 내 다양성을 23.8~24.5% 증가시킨다. [2604.13728v1]
- s3: 광범위한 오픈 도메인 질문 답변 데이터셋에서 평가했을 때, 이 논문의 밀집 검색기는 상위 20개 문서 검색 정확도 측면에서 Lucene-BM25 시스템을 절대적으로 9%~19% 정도 상회하며, 이는 여러 오픈 도메인 QA 벤치마크에서 엔드투엔드 QA 시스템이 새로운 최첨단 성능을 달성하도록 돕는다. [2004.04906v3]
- s4: 또한 두 방법을 결합한 하이브리드 접근법(랭크 퓨전) 이 관련성 측면에서 단일 방법보다 높은 정확도를 달성한다는 결과도 포함되어 있습니다[2607.26497v3][2004.04906v3][2604.13728v1].

## H_D02 — LoRA랑 전체 파인튜닝은 성능이랑 비용이 어떻게 달라?

### 인용 블록

[문서 1]
[Distance: 0.4557]
[발행일: 2021-06-17]
[2106.09685v2] LoRA: Low-Rank Adaptation of Large Language Models
[초록] An important paradigm of natural language processing consists of large-scale pre-training on general domain data and adaptation to particular tasks or domains. As we pre-train larger models, full fine-tuning, which retrains all model parameters, becomes less feasible. Using GPT-3 175B as an example -- deploying independent instances of fine-tuned models, each with 175B parameters, is prohibitively expensive. We propose Low-Rank Adaptation, or LoRA, which freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture, greatly reducing the number of trainable parameters for downstream tasks. Compared to GPT-3 175B fine-tuned with Adam, LoRA can reduce the number of trainable parameters by 10,000 times and the GPU memory requirement by 3 times. LoRA performs on-par or better than fine-tuning in model quality on RoBERTa, DeBERTa, GPT-2, and GPT-3, despite having fewer trainable parameters, a higher training throughput, and, unlike adapters, no additional inference latency. We also provide an empirical investigation into rank-deficiency in language model adaptation, which sheds light on the efficacy of LoRA. We release a package that facilitates the integration of LoRA with PyTorch models and provide our implementations and model checkpoints for RoBERTa, DeBERTa, and GPT-2 at https://github.com/microsoft/LoRA.

LoRA possesses several key advantages.  
- A pre-trained model can be shared and used to build many small LoRA modules for different tasks. We can freeze the shared model and efficiently switch tasks by replacing the matrices _A_ and _B_ in Figure 1, reducing the storage requirement and task-switching overhead significantly.
[문서 4]
[Distance: 0.3900]
[발행일: 2025-03-31]
[2504.00254v1] ElaLoRA: Elastic & Learnable Low-Rank Adaptation for Efficient Model Fine-Tuning
[초록] Low-Rank Adaptation (LoRA) has become a widely adopted technique for fine-tuning large-scale pre-trained models with minimal parameter updates. However, existing methods rely on fixed ranks or focus solely on either rank pruning or expansion, failing to adapt ranks dynamically to match the importance of different layers during training. In this work, we propose ElaLoRA, an adaptive low-rank adaptation framework that dynamically prunes and expands ranks based on gradient-derived importance scores. To the best of our knowledge, ElaLoRA is the first method that enables both rank pruning and expansion during fine-tuning. Experiments across multiple benchmarks demonstrate that ElaLoRA consistently outperforms existing PEFT methods across different parameter budgets. Furthermore, our studies validate that layers receiving higher rank allocations contribute more significantly to model performance, providing theoretical justification for our adaptive strategy. By introducing a principled and adaptive rank allocation mechanism, ElaLoRA offers a scalable and efficient fine-tuning solution, particularly suited for resource-constrained environments.

Table 2: Performance comparison of LoRA, AdaLoRA, ElaLoRA, and other fine-tuning methods across different ranks and parameter budgets. Methods marked with * are results cited from the AdaLoRA (Zhang et al., 2023b), DoRA (Mao et al., 2024), and DyLoRA (Valipour et al., 2022) papers. For QQP, both accuracy and F1 scores are reported when available, though some methods lack F1 scores
[문서 5]
[Distance: 0.4090]
[발행일: 2024-12-28]
[2412.20004v1] Adaptive Parameter-Efficient Federated Fine-Tuning on Heterogeneous Devices
[초록] Federated fine-tuning (FedFT) has been proposed to fine-tune the pre-trained language models in a distributed manner. However, there are two critical challenges for efficient FedFT in practical applications, i.e., resource constraints and system heterogeneity. Existing works rely on parameter-efficient fine-tuning methods, e.g., low-rank adaptation (LoRA), but with major limitations. Herein, based on the inherent characteristics of FedFT, we observe that LoRA layers with higher ranks added close to the output help to save resource consumption while achieving comparable fine-tuning performance. Then we propose a novel LoRA-based FedFT framework, termed LEGEND, which faces the difficulty of determining the number of LoRA layers (called, LoRA depth) and the rank of each LoRA layer (called, rank distribution). We analyze the coupled relationship between LoRA depth and rank distribution, and design an efficient LoRA configuration algorithm for heterogeneous devices, thereby promoting fine-tuning efficiency. Extensive experiments are conducted on a physical platform with 80 commercial devices. The results show that LEGEND can achieve a speedup of 1.5-2.8$\times$ and save communication costs by about 42.3% when achieving the target accuracy, compared to the advanced solutions.

- [40] Haobo Song, Hao Zhao, Soumajit Majumder, and Tao Lin. Increasing model capacity for free: A simple strategy for parameter efficient fine-tuning. _arXiv preprint arXiv:2407.01320_ , 2024.  
14  
- [41] Reece Shuttleworth, Jacob Andreas, Antonio Torralba, and Pratyusha Sharma. Lora vs full fine-tuning: An illusion of equivalence. _arXiv preprint arXiv:2410.21228_ , 2024.

### 문장

- s1: ElaLoRA는 다양한 벤치마크에서 기존 PEFT 방법을 초월하며, 레이어별 중요도에 따라 랭크를 동적으로 할당함으로써 성능 향상을 이론적으로 뒷받침합니다[2504.00254v1].
- s2: LoRA는 전체 파인튜닝에 비해 학습 가능한 파라미터를 10,000배 감소시키고 GPU 메모리 요구량을 3배 줄이면서 모델 품질은 동등하거나 더 나은 수준을 유지합니다[2106.09685v2].
- s3: GPT-3 175B 모델을 Adam으로 미세조정한 경우와 비교할 때, LoRA는 학습 가능한 파라미터 수를 10,000배 감소시키고 GPU 메모리 요구량을 3배 줄일 수 있다. [2106.09685v2]
- s4: 기존 연구들은 저랭크 적응(LoRA)과 같은 파라미터 효율적 파인튜닝 방법을 활용하지만, 주요 한계가 존재한다. [2412.20004v1]
- s5: 또한 LoRA 레이어의 랭크와 위치를 조정하면 자원 소비를 절감하면서도 유사한 파인튜닝 성능을 달성할 수 있습니다[2412.20004v1].
- s6: 여러 벤치마크에 걸친 실험 결과, ElaLoRA는 다양한 파라미터 예산에서 기존 PEFT 방법을 일관되게 능가함을 보여줍니다. [2504.00254v1]

## H_D03 — RAG로 검색해서 넣는 방식이랑 긴 컨텍스트에 문서를 다 넣는 방식 중 뭐가 나은지 비교한 연구 있어?

### 인용 블록

[문서 1]
[Distance: 0.2045]
[발행일: 2026-01-06]
[2603.26667v1] M-RAG: Making RAG Faster, Stronger, and More Efficient
[초록] Retrieval-Augmented Generation (RAG) has become a widely adopted paradigm for enhancing the reliability of large language models (LLMs). However, RAG systems are sensitive to retrieval strategies that rely on text chunking to construct retrieval units, which often introduce information fragmentation, retrieval noise, and reduced efficiency. Recent work has even questioned the necessity of RAG, arguing that long-context LLMs may eliminate multi-stage retrieval pipelines by directly processing full documents. Nevertheless, expanded context capacity alone does not resolve the challenges of relevance filtering, evidence prioritization, and isolating answer-bearing information. To this end, we proposed M-RAG, a novel Chunk-free retrieval strategy. Instead of retrieving coarse-grained textual chunks, M-RAG extracts structured, k-v decomposition meta-markers, with a lightweight, intent-aligned retrieval key for retrieval and a context-rich information value for generation. Under this setting, M-RAG enables efficient and stable query-key similarity matching without sacrificing expressive ability. Experimental results on the LongBench subtasks demonstrate that M-RAG outperforms chunk-based RAG baselines across varying token budgets, particularly under low-resource settings. Extensive analysis further reveals that M-RAG retrieves more answer-friendly evidence with high efficiency, validating the effectiveness of decoupling retrieval representation from generation and highlighting the proposed strategy as a scalable and robust alternative to existing chunk-based methods.

Retrieval-Augmented Generation (RAG) has
become a widely adopted paradigm for enhancing the reliability of large language models
(LLMs). However, RAG systems are sensitive
to retrieval strategies that rely on text chunking
to construct retrieval units, which often introduce information fragmentation, retrieval noise,
and reduced efficiency. Recent work has even
questioned the necessity of RAG, arguing that
long-context LLMs may eliminate multi-stage
[문서 2]
[Distance: 0.3034]
[발행일: 2024-06-21]
[2406.15319v3] LongRAG: Enhancing Retrieval-Augmented Generation with Long-context LLMs
[초록] In traditional RAG framework, the basic retrieval units are normally short. The common retrievers like DPR normally work with 100-word Wikipedia paragraphs. Such a design forces the retriever to search over a large corpus to find the `needle' unit. In contrast, the readers only need to generate answers from the short retrieved units. The imbalanced `heavy' retriever and `light' reader design can lead to sub-optimal performance. The loss of contextual information in the short, chunked units may increase the likelihood of introducing hard negatives during the retrieval stage. Additionally, the reader might not fully leverage the capabilities of recent advancements in LLMs. In order to alleviate the imbalance, we propose a new framework LongRAG, consisting of a `long retriever' and a `long reader'. In the two Wikipedia-based datasets, NQ and HotpotQA, LongRAG processes the entire Wikipedia corpus into 4K-token units by grouping related documents. By increasing the unit size, we significantly reduce the total number of units. This greatly reduces the burden on the retriever, resulting in strong retrieval performance with only a few (less than 8) top units. Without requiring any training, LongRAG achieves an EM of 62.7% on NQ and 64.3% on HotpotQA, which are on par with the (fully-trained) SoTA model. Furthermore, we test on two non-Wikipedia-based datasets, Qasper and MultiFieldQA-en. LongRAG processes each individual document as a single (long) unit rather than chunking them into smaller units. By doing so, we achieve an F1 score of 25.9% on Qasper and 57.5% on MultiFieldQA-en. Our study offers insights into the future roadmap for combining RAG with long-context LLMs.

**1** **Introduction**  
Retrieval-Augmented Generation (RAG) methods have long been employed to enhance large language models
(LLMs) (Mialon et al., 2023). Knowledge in the form of natural language can be entirely offloaded from
the parametric knowledge of LLMs by leveraging a standalone retrieval component from an external corpus.

### 문장

- s1: 어떤 학습도 필요하지 않은 LongRAG은 NQ에서 정확률(EM)이 62.7%, HotpotQA에서는 64.3%를 달성하여, 완전 학습된 최첨단(SoTA) 모델과 동등한 성능을 보였습니다. [2406.15319v3]
- s2: M-RAG은 다양한 토큰 예산과 특히 저자원 설정에서 chunk 기반 RAG를 능가하며, 검색 효율성과 증거 수집 능력을 향상시킨다고 보고한다[2603.26667v1].
- s3: LongBench 서브태스크에 대한 실험 결과는 다양한 토큰 예산 하에서 특히 저자원 환경에서 M-RAG가 청크 기반 RAG 베이스라인을 능가함을 보여준다. [2603.26667v1]
- s4: 반면 LongRAG는 긴 컨텍스트 LLM을 활용해 검색 부담을 크게 줄이고, NQ와 HotpotQA에서 각각 EM 62.7%와 64.3%의 성능을 달성해 기존 최상위 모델과 동등한 결과를 보인다고 제시한다[2406.15319v3].

## H_D04 — DPO랑 PPO 기반 RLHF는 결과가 어떻게 달라?

### 인용 블록

[문서 1]
[Distance: 0.3796]
[발행일: 2023-05-29]
[2305.18290v3] Direct Preference Optimization: Your Language Model is Secretly a Reward Model
[초록] While large-scale unsupervised language models (LMs) learn broad world knowledge and some reasoning skills, achieving precise control of their behavior is difficult due to the completely unsupervised nature of their training. Existing methods for gaining such steerability collect human labels of the relative quality of model generations and fine-tune the unsupervised LM to align with these preferences, often with reinforcement learning from human feedback (RLHF). However, RLHF is a complex and often unstable procedure, first fitting a reward model that reflects the human preferences, and then fine-tuning the large unsupervised LM using reinforcement learning to maximize this estimated reward without drifting too far from the original model. In this paper we introduce a new parameterization of the reward model in RLHF that enables extraction of the corresponding optimal policy in closed form, allowing us to solve the standard RLHF problem with only a simple classification loss. The resulting algorithm, which we call Direct Preference Optimization (DPO), is stable, performant, and computationally lightweight, eliminating the need for sampling from the LM during fine-tuning or performing significant hyperparameter tuning. Our experiments show that DPO can fine-tune LMs to align with human preferences as well as or better than existing methods. Notably, fine-tuning with DPO exceeds PPO-based RLHF in ability to control sentiment of generations, and matches or improves response quality in summarization and single-turn dialogue while being substantially simpler to implement and train.

. First, DPO and PPO optimize the same objective, but DPO is notably more efficient;

> 3That is, the sum of the per-timestep KL-divergences.  
8  
DPO’s reward/KL tradeoff strictly dominates PPO. Second, DPO achieves a better frontier than PPO, _even when PPO can access ground truth rewards_ (PPO-GT).
[문서 3]
[Distance: 0.3606]
[발행일: 2024-12-20]
[2412.16145v2] Offline Reinforcement Learning for LLM Multi-Step Reasoning
[초록] Improving the multi-step reasoning ability of large language models (LLMs) with offline reinforcement learning (RL) is essential for quickly adapting them to complex tasks. While Direct Preference Optimization (DPO) has shown promise in aligning LLMs with human preferences, it is less suitable for multi-step reasoning tasks because (1) DPO relies on paired preference data, which is not readily available for multi-step reasoning tasks, and (2) it treats all tokens uniformly, making it ineffective for credit assignment in multi-step reasoning tasks, which often come with sparse reward. In this work, we propose OREO (Offline Reasoning Optimization), an offline RL method for enhancing LLM multi-step reasoning. Building on insights from previous works of maximum entropy reinforcement learning, it jointly learns a policy model and value function by optimizing the soft Bellman Equation. We show in principle that it reduces the need to collect pairwise data and enables better credit assignment. Empirically, OREO surpasses existing offline learning methods on multi-step reasoning benchmarks, including mathematical reasoning tasks (GSM8K, MATH) and embodied agent control (ALFWorld). The approach can be extended to a multi-iteration framework when additional resources are available. Furthermore, the learned value function can be leveraged to guide the tree search for free, which can further boost performance during test time.

## **2 Related Work**

## **2.1 Reinforcement Learning for LLM**

Reinforcement Learning (RL) has become a standard approach in the post-training stage of LLMs. A widely adopted method, known as reinforcement learning from human feedback (RLHF) (Ziegler et al., 2019; Ouyang et al., 2022), is designed to align LLM responses more closely with human preferences. Traditional RL methods, such as Proximal Policy Optimization (PPO) (Schulman et al., 2017), have been extensively used in LLM post-training (Achiam et al., 2023; Team et al., 2023; Dubey et al., 2024)

### 문장

- s1: 특히 DPO 기반 파인튜닝은 생성물의 감정을 제어하는 능력이 PPO 기반 RLHF를 능가하며, 요약과 단일 턴 대화와 같은 작업에서 응답 품질을 일치시키거나 향상시키는 동시에 구현 및 학습이 현저히 단순합니다. [2305.18290v3]
- s2: DPO는 PPO 기반 RLHF와 비교해 감정 제어 능력이 더 뛰어나며, 요약과 단일 턴 대화에서는 응답 품질을 일치하거나 개선하고 구현 및 학습이 훨씬 간단합니다[2305.18290v3].
- s3: 직접 선호 최적화(DPO)는 대형 언어 모델을 인간 선호와 정렬하는 데 유망한 결과를 보였으나, 다단계 추론 작업에는 적합하지 않다: (1) DPO는 쌍으로 된 선호 데이터를 필요로 하는데, 이러한 데이터가 다단계 추론 작업에서는 쉽게 구할 수 없으며, (2) 모든 토큰을 균일하게 취급하여 희소 보상과 함께 발생하는 다단계 추론 작업에서의 신용 할당에 효과적이지 못하기 때문이다. [2412.16145v2]
- s4: 그러나 다단계 추론 작업에서는 DPO가 쌍별 선호 데이터에 의존하고 모든 토큰을 균일하게 처리해 희소 보상 환경에서 크레딧 할당에 비효율적이므로 PPO보다 적합하지 않습니다[2412.16145v2].

## H_D05 — cross-encoder 리랭커랑 LLM 리랭커는 정확도랑 속도가 어떻게 달라?

### 인용 블록

[문서 1]
[Distance: 0.1795]
[발행일: 2025-03-28]
[2503.22672v1] Exploring the Effectiveness of Multi-stage Fine-tuning for Cross-encoder Re-rankers
[초록] State-of-the-art cross-encoders can be fine-tuned to be highly effective in passage re-ranking. The typical fine-tuning process of cross-encoders as re-rankers requires large amounts of manually labelled data, a contrastive learning objective, and a set of heuristically sampled negatives. An alternative recent approach for fine-tuning instead involves teaching the model to mimic the rankings of a highly effective large language model using a distillation objective. These fine-tuning strategies can be applied either individually, or in sequence. In this work, we systematically investigate the effectiveness of point-wise cross-encoders when fine-tuned independently in a single stage, or sequentially in two stages. Our experiments show that the effectiveness of point-wise cross-encoders fine-tuned using contrastive learning is indeed on par with that of models fine-tuned with multi-stage approaches. Code is available for reproduction at https://github.com/fpezzuti/multistage-finetuning.

While cross-encoders exhibit remarkable effectiveness when fine-tuned as rankers, they are computationally expensive. Consequently, they are often used as re-rankers in retrieve-then-rerank systems to refine the ranking of a small subset of documents initially induced by a more efficient model like BM25 [24], which serves as retriever.
[문서 2]
[Distance: 0.3578]
[발행일: 2025-09-29]
[2509.25085v4] jina-reranker-v3: Last but Not Late Interaction for Listwise Document Reranking
[초록] jina-reranker-v3 is a 0.6B-parameter multilingual listwise reranker that introduces a novel "last but not late" interaction. Unlike late interaction models like ColBERT that encode documents separately before multi-vector matching, our approach applies causal attention between the query and all candidate documents in the same context window, enabling rich interactions before extracting contextual embeddings from each document's final token. The new model achieves state-of-the-art BEIR performance with 61.94 nDCG@10 while being significantly smaller than other models with comparable performance.

. Cross-encoders like BERT-based rerankers [Nogueira and Cho, 2019] achieve strong performance through full query-document interaction but require separate forward passes for each pair, creating computational bottlenecks for large-scale retrieval. Recent comparative studies [Déjean et al., 2024] demonstrate that while LLM-based rerankers show impressive zero-shot capabilities, traditional cross-encoders remain highly competitive across diverse retrieval scenarios.
[문서 3]
[Distance: 0.3998]
[발행일: 2026-10-29]
[2610.40454v1] Glance: The Generator Is Its Own Reranker
[초록] Retrieval-augmented generation commonly serves separate models for reranking and answering, duplicating model residency and passage processing. We introduce Glance, which equips the generator with a lightweight decision adapter and pointer head to score candidate passages from a shared prefill. Short relevance probes branch from the cached context, producing one score per passage without separately prefilling each query-passage pair. A single resident 9B backbone supports generation, general decisions and reranking, with approximately 0.1 GiB of additional memory per decision skill. After 39 minutes of MS MARCO fine-tuning, Glance achieves nDCG@10 of 0.741 on SciFact and 0.345 on NFCorpus, compared with 0.721 and 0.326 for bge-reranker-v2-m3. On 300 HotpotQA questions, its selected context improves answer F1 by 0.045 over cross-encoder-selected context under the same base generator (paired bootstrap 95% CI [0.014, 0.076]). In a scaling study, reranking quality keeps rising up to 200 candidates (43k tokens) scored from one shared prefill, where it exceeds the cross-encoder by 0.058 nDCG@10, and a probe-only activated adapter lets generation continue from the original passage cache. These initial results demonstrate generator-based reranking with one resident backbone; evaluation currently covers two retrieval datasets, one QA dataset and one backbone family.

## **2 Related Work**

**Rerankers.** Cross-encoders such as monoT5 [13] and BGE rerankers [6] score each query–passage pair independently. LLM rerankers score pointwise via yes/no logits [25], or listwise via permutation generation [19, 15]; FIRST [17] reads the ranking from the logits of the first generated token. Incontext reranking [7] uses attention patterns of a frozen LLM over all passages at once

### 문장

- s1: MS MARCO를 39분 동안 미세 조정하면 Glance는 SciFact에서 nDCG@10이 0.741, NFCorpus에서는 0.345로, 이는 bge-reranker-v2-m3의 각각 0.721과 0.326보다 높은 성능을 보인다. [2610.40454v1]
- s2: 또한, 생성기 기반 리랭커인 Glance는 HotpotQA 데이터셋에서 크로스엔코더 대비 F1 점수 향상과 nDCG@10 개선 효과를 보였습니다 [2610.40454v1].
- s3: Cross-encoder 기반 리랭커는 점별 학습과 다단계 학습 모두에서 유사한 성능을 보인다는 결과가 있습니다 [2503.22672v1].
- s4: 새로운 모델은 다른 모델보다 크기가 현저히 작으면서도, 비교 가능한 성능을 보이며 61.94 nDCG@10 의 BEIR 성능을 달성한다. [2509.25085v4]
- s5: 본 실험 결과, 대비 학습을 이용해 미세조정된 점별 교차 인코더의 효과는 다단계 접근법으로 미세조정된 모델과 동등함을 확인하였다. [2503.22672v1]
- s6: LLM 기반 리랭커는 제로샷 능력에서 인상적인 성능을 보여주지만, 전통적인 크로스엔코더가 다양한 검색 시나리오에서도 여전히 경쟁력이 있다는 비교 연구가 존재합니다 [2509.25085v4].

## H_D06 — Self-RAG랑 CRAG는 검색 결과를 다루는 방식이 뭐가 달라?

### 인용 블록

[문서 1]
[Distance: 0.3888]
[발행일: 2023-10-17]
[2310.11511v1] Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
[초록] Despite their remarkable capabilities, large language models (LLMs) often produce responses containing factual inaccuracies due to their sole reliance on the parametric knowledge they encapsulate. Retrieval-Augmented Generation (RAG), an ad hoc approach that augments LMs with retrieval of relevant knowledge, decreases such issues. However, indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility or can lead to unhelpful response generation. We introduce a new framework called Self-Reflective Retrieval-Augmented Generation (Self-RAG) that enhances an LM's quality and factuality through retrieval and self-reflection. Our framework trains a single arbitrary LM that adaptively retrieves passages on-demand, and generates and reflects on retrieved passages and its own generations using special tokens, called reflection tokens. Generating reflection tokens makes the LM controllable during the inference phase, enabling it to tailor its behavior to diverse task requirements. Experiments show that Self-RAG (7B and 13B parameters) significantly outperforms state-of-the-art LLMs and retrieval-augmented models on a diverse set of tasks. Specifically, Self-RAG outperforms ChatGPT and retrieval-augmented Llama2-chat on Open-domain QA, reasoning and fact verification tasks, and it shows significant gains in improving factuality and citation accuracy for long-form generations relative to these models.

. Using the top passages regardless of their relevance (Retrieve top 1) as in conventional RAG approaches causes a large drop in PopQA and ASQA, and removing **ISSUP** during the beam search results hurts performance on ASQA. This demonstrates the effectiveness of SELF-RAG’s capabilities of carefully selecting generations based fine-grained multiple criterion, instead of naively using all of the top passages from the retrieval model or solely depending on relevance scores.
[문서 3]
[Distance: 0.4020]
[발행일: 2024-01-29]
[2401.15884v3] Corrective Retrieval Augmented Generation
[초록] Large language models (LLMs) inevitably exhibit hallucinations since the accuracy of generated texts cannot be secured solely by the parametric knowledge they encapsulate. Although retrieval-augmented generation (RAG) is a practicable complement to LLMs, it relies heavily on the relevance of retrieved documents, raising concerns about how the model behaves if retrieval goes wrong. To this end, we propose the Corrective Retrieval Augmented Generation (CRAG) to improve the robustness of generation. Specifically, a lightweight retrieval evaluator is designed to assess the overall quality of retrieved documents for a query, returning a confidence degree based on which different knowledge retrieval actions can be triggered. Since retrieval from static and limited corpora can only return sub-optimal documents, large-scale web searches are utilized as an extension for augmenting the retrieval results. Besides, a decompose-then-recompose algorithm is designed for retrieved documents to selectively focus on key information and filter out irrelevant information in them. CRAG is plug-and-play and can be seamlessly coupled with various RAG-based approaches. Experiments on four datasets covering short- and long-form generation tasks show that CRAG can significantly improve the performance of RAG-based approaches.

four datasets of PopQA (Mallen et al., 2023), Biography (Min et al., 2023), Pub Health (Zhang et al., 2023a), and Arc-Challenge (Bhakthavatsalam et al., 2021) show that CRAG can significantly improve the performance of standard RAG and state-of-theart Self-RAG, demonstrating its generalizability across both short- and long-form generation tasks. To facilitate others to reproduce our results, we will publish all source code later.

### 문장

- s1: 반면 CRAG는 정적·제한된 코퍼스로부터 얻은 서브옵티멀 문서를 보완하기 위해 대규모 웹 검색을 확장하여 활용한다[2401.15884v3].
- s2: 이를 위해 이 논문은 생성의 견고성을 향상시키기 위해 수정형 검색 증강 생성(CRAG)을 제안한다. [2401.15884v3]
- s3: Self-RAG은 검색된 상위 문서들을 무조건 포함하는 기존 RAG 방식과 달리, 다중 기준을 통해 생성을 신중하게 선택함으로써 성능이 크게 향상된다[2310.11511v1].
- s4: 검색 증강 생성(Retrieval-Augmented Generation, RAG)은 관련 지식을 검색하여 언어 모델을 보강하는 임시적 접근법으로, 이러한 문제를 감소시킨다. [2310.11511v1]

## H_D07 — 문장 단위로 임베딩하는 거랑 문서 단위로 임베딩하는 거는 검색 정확도가 어떻게 달라?

### 인용 블록

[문서 1]
[Distance: 0.3702]
[발행일: 2024-12-13]
[2412.15241v4] Quantifying Positional Biases in Text Embedding Models
[초록] Embedding models are crucial for tasks in Information Retrieval (IR) and semantic similarity measurement, yet their handling of longer texts and associated positional biases remains underexplored. In this study, we investigate the impact of content position and input size on text embeddings. Our experiments reveal that embedding models, irrespective of their positional encoding mechanisms, disproportionately prioritize the beginning of an input. Ablation studies demonstrate that insertion of irrelevant text or removal at the start of a document reduces cosine similarity between altered and original embeddings by up to 12.3% more than ablations at the end. Regression analysis further confirms this bias, with sentence importance declining as position moves further from the start, even with with content-agnosticity. We hypothesize that this effect arises from pre-processing strategies and chosen positional encoding techniques. These findings quantify the sensitivity of retrieval systems and suggest a new lens towards embedding model robustness.

## **3 Effect of sentence-level positioning in embedding output**  
We explore how the position and size of a sentence in a text influence a document’s final embedding vector. Our methodology adapts the needle-in-a-haystack test [10], traditionally used for generative models in information retrieval [26], to evaluate embedding models.
[문서 3]
[Distance: 0.4193]
[발행일: 2026-02-19]
[2602.16974v1] Beyond Chunk-Then-Embed: A Comprehensive Taxonomy and Evaluation of Document Chunking Strategies for Information Retrieval
[초록] Document chunking is a critical preprocessing step in dense retrieval systems, yet the design space of chunking strategies remains poorly understood. Recent research has proposed several concurrent approaches, including LLM-guided methods (e.g., DenseX and LumberChunker) and contextualized strategies(e.g., Late Chunking), which generate embeddings before segmentation to preserve contextual information. However, these methods emerged independently and were evaluated on benchmarks with minimal overlap, making direct comparisons difficult. This paper reproduces prior studies in document chunking and presents a systematic framework that unifies existing strategies along two key dimensions: (1) segmentation methods, including structure-based methods (fixed-size, sentence-based, and paragraph-based) as well as semantically-informed and LLM-guided methods; and (2) embedding paradigms, which determine the timing of chunking relative to embedding (pre-embedding chunking vs. contextualized chunking). Our reproduction evaluates these approaches in two distinct retrieval settings established in previous work: in-document retrieval (needle-in-a-haystack) and in-corpus retrieval (the standard information retrieval task). Our comprehensive evaluation reveals that optimal chunking strategies are task-dependent: simple structure-based methods outperform LLM-guided alternatives for in-corpus retrieval, while LumberChunker performs best for in-document retrieval. Contextualized chunking improves in-corpus effectiveness but degrades in-document retrieval. We also find that chunk size correlates moderately with in-document but weakly with in-corpus effectiveness, suggesting segmentation method differences are not purely driven by chunk size. Our code and evaluation benchmarks are publicly available at (Anonymoused).

4  
- **In-corpus retrieval:** This task requires finding the most relevant documents within a large collection, such as the BEIR benchmarks [Thakur et al.(2021)]. It evaluates effectiveness when retrieval spans multiple documents across diverse domains.  
By evaluating each method across both tasks using a consistent set of embedding models, our study isolates the impact of the chunking strategy itself on retrieval effectiveness.

### 문장

- s1: 어떤 텍스트를 삽입하거나 문서 시작 부분에서 제거하는 아블레이션 연구는, 문서 끝부분에서의 아블레이션에 비해 변경된 임베딩과 원래 임베딩 사이의 코사인 유사도를 최대 12.3% 감소시킨다는 것을 보여준다. [2412.15241v4]
- s2: 문서 단위로 임베딩하는 경우, 입력의 시작 부분에 과도하게 집중되는 경향이 있어 문서 앞부분을 제거하거나 관련 없는 텍스트를 삽입하면 코사인 유사도가 최대 12.3% 감소한다는 결과가 보고되었습니다. [2412.15241v4]
- s3: 최근 연구에서는 DenseX와 LumberChunker와 같은 LLM 기반 방법과 Late Chunking과 같은 문맥을 고려한 전략을 포함하는 여러 동시 접근법을 제안했으며, 이러한 방법은 분할 전에 임베딩을 생성하여 문맥 정보를 보존한다. [2602.16974v1]
- s4: 또한, 문서 조각(chunking) 전략에 따라 검색 정확도가 달라지며, 단순 구조 기반 방법이 인-코퍼스 검색에서는 LLM 기반 방법보다 우수하지만, 인-문서 검색에서는 LumberChunker가 가장 잘 수행됩니다. [2602.16974v1]

