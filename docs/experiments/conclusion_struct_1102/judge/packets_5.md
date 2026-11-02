# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)

## H_D08 — GPT-4 판정이랑 사람 판정은 얼마나 일치해? 비교한 연구 알려줘

### 인용 블록

[문서 2]
[Distance: 0.2590]
[발행일: 2025-02-10]
[2502.10441v1] AI Alignment at Your Discretion
[초록] In AI alignment, extensive latitude must be granted to annotators, either human or algorithmic, to judge which model outputs are `better' or `safer.' We refer to this latitude as alignment discretion. Such discretion remains largely unexamined, posing two risks: (i) annotators may use their power of discretion arbitrarily, and (ii) models may fail to mimic this discretion. To study this phenomenon, we draw on legal concepts of discretion that structure how decision-making authority is conferred and exercised, particularly in cases where principles conflict or their application is unclear or irrelevant. Extended to AI alignment, discretion is required when alignment principles and rules are (inevitably) conflicting or indecisive. We present a set of metrics to systematically analyze when and how discretion in AI alignment is exercised, such that both risks (i) and (ii) can be observed. Moreover, we distinguish between human and algorithmic discretion and analyze the discrepancy between them. By measuring both human and algorithmic discretion over safety alignment datasets, we reveal layers of discretion in the alignment process that were previously unaccounted for. Furthermore, we demonstrate how algorithms trained on these datasets develop their own forms of discretion in interpreting and applying these principles, which challenges the purpose of having any principles at all. Our paper presents the first step towards formalizing this core gap in current alignment processes, and we call on the community to further scrutinize and control alignment discretion.

human values (pluralism) and defining precise rules for AI behavior (specification). Moreover, [1] points to the issue of transparency as a core element of legal decision-making that lends legitimacy to the legal system. These works suggest that a legally-inspired approach to AI alignment could be valuable. Moreover, they also highlight transparency in legal decision-making as a key factor of the exercise of discretion
[문서 4]
[Distance: 0.4024]
[발행일: 2026-05-17]
[2605.17691v1] Validate Your Authority: Benchmarking LLMs on Multi-Label Precedent Treatment Classification
[초록] Automating the classification of negative treatment in legal precedent is a critical yet nuanced NLP task where misclassification carries significant risk. To address the shortcomings of standard accuracy, this paper introduces a more robust evaluation framework. We benchmark modern Large Language Models on a new, expert-annotated dataset of 239 real-world legal citations and propose a novel Average Severity Error metric to better measure the practical impact of classification errors. Our experiments reveal a performance split. Google's Gemini 2.5 Flash achieved the highest accuracy on a high-level classification task (79.1%), while OpenAI's GPT-5-mini was the top performer on the more complex fine-grained schema (67.7%). This work establishes a crucial baseline, provides a new context-rich dataset, and introduces an evaluation metric tailored to the demands of this complex legal reasoning task.

Sarfaty, Gregory M. Dickinson, Haggai Porat, Jason Hegland, and 21 others. 2023. LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models. _arXiv_ .  
- Paul Hellyer. 2018. Evaluating Shepard’s, KeyCite, and BCite for Case Validation Accuracy. _Law Library Journal_ , 110(4):449–476.  
- In re Hatfield. 1990. (Bankr. C.D. Ill.).  
- In re Matthews. 1984. (United States Court of Appeals, Ninth Circuit.).

### 문장

- s1: 또한 [2605.17691v1]는 GPT‑5‑mini와 Gemini 2.5 Flash 등 최신 LLM을 법률 인용 분류 작업에서 평가하여, 고수준 분류에서는 79.1%의 정확도를 보였고, 복잡한 세부 스키마에서는 67.7%의 성능을 기록했다고 밝힙니다.
- s2: Google의 Gemini 2.5 Flash는 고수준 분류 작업에서 가장 높은 정확도(79.1%)를 달성했으며, OpenAI의 GPT-5-mini는 보다 복잡한 세분화된 스키마에서 최고 성능을 보였습니다. [2605.17691v1]
- s3: [2502.10441v1]는 안전 정렬 데이터셋에 대한 인간과 알고리즘의 판단 차이를 측정하여, 기존에 고려되지 않았던 다층적인 판단 층위를 드러냈으며, 이는 알고리즘이 원칙을 해석·적용하는 자체적인 판단 방식을 발전시킨다고 보고합니다.
- s4: 또한, 이 논문은 이러한 데이터셋으로 학습된 알고리즘이 원칙을 해석하고 적용하는 과정에서 자체적인 판단력을 발전시켜, 원칙 자체가 존재한다는 목적에 도전한다는 점을 보여준다. [2502.10441v1]

## H_E01 — speculative decoding을 쓰면 생성 속도가 보통 몇 배 빨라져?

### 인용 블록

[문서 1]
[Distance: 0.3657]
[발행일: 2024-12-27]
[2412.19925v2] HADES: Hardware Accelerated Decoding for Efficient Speculation in Large Language Models
[초록] Large Language Models (LLMs) have revolutionized natural language processing by understanding and generating human-like text. However, the increasing demand for more sophisticated LLMs presents significant computational challenges due to their scale and complexity. This paper introduces Hardware Accelerated Decoding (HADES), a novel approach to enhance the performance and energy efficiency of LLMs. We address the design of an LLM accelerator with hardware-level speculative decoding support, a concept not previously explored in existing literature. Our work demonstrates how speculative decoding can significantly improve the efficiency of LLM operations, paving the way for more advanced and practical applications of these models.

After applying speculative decoding to the target model with the help of a draft model, we were able to observe speedup compared to the baseline as expected. However, there were a few more notable observations. The speedup rate drops below the base line for certain cases, specifically ones with high gamma factors. Recalling that the idea of speculative decoding originated from hardware branch predictors, then a high gamma factor is analogous to a high latency until the branch is resolved
[문서 2]
[Distance: 0.4531]
[발행일: 2025-02-05]
[2502.10424v1] QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache
[초록] Large Language Models (LLMs) are increasingly being deployed on edge devices for long-context settings, creating a growing need for fast and efficient long-context inference. In these scenarios, the Key-Value (KV) cache is the primary bottleneck in terms of both GPU memory and latency, as the full KV cache must be loaded for each decoding step. While speculative decoding is a widely accepted technique to accelerate autoregressive decoding, existing methods often struggle to achieve significant speedups due to inefficient KV cache optimization strategies and result in low acceptance rates. To address these challenges, we propose a novel self-speculative decoding framework, QuantSpec, where the draft model shares the architecture of the target model but employs a hierarchical 4-bit quantized KV cache and 4-bit quantized weights for acceleration. QuantSpec maintains high acceptance rates ($>$90%) and reliably provides consistent end-to-end speedups upto $\sim2.5\times$, outperforming other self-speculative decoding methods that use sparse KV cache for long-context LLM inference. QuantSpec also reduces the memory requirements by $\sim 1.3\times$ compared to these alternatives.

struggle to achieve significant speedups due to
inefficient KV cache optimization strategies and
result in low acceptance rates. To address these
challenges, we propose a novel self-speculative
decoding framework, QuantSpec, where the draft
model shares the architecture of the target model
but employs a hierarchical 4-bit quantized KV
cache and 4-bit quantized weights for acceleration. QuantSpec maintains high acceptance rates
[문서 3]
[Distance: 0.3860]
[발행일: 2024-12-17]
[2412.12639v3] Falcon: Faster and Parallel Inference of Large Language Models through Enhanced Semi-Autoregressive Drafting and Custom-Designed Decoding Tree
[초록] Striking an optimal balance between minimal drafting latency and high speculation accuracy to enhance the inference speed of Large Language Models remains a significant challenge in speculative decoding. In this paper, we introduce Falcon, an innovative semi-autoregressive speculative decoding framework fashioned to augment both the drafter's parallelism and output quality. Falcon incorporates the Coupled Sequential Glancing Distillation technique, which fortifies inter-token dependencies within the same block, leading to increased speculation accuracy. We offer a comprehensive theoretical analysis to illuminate the underlying mechanisms. Additionally, we introduce a Custom-Designed Decoding Tree, which permits the drafter to generate multiple tokens in a single forward pass and accommodates multiple forward passes as needed, thereby boosting the number of drafted tokens and significantly improving the overall acceptance rate. Comprehensive evaluations on benchmark datasets such as MT-Bench, HumanEval, and GSM8K demonstrate Falcon's superior acceleration capabilities. The framework achieves a lossless speedup ratio ranging from 2.91x to 3.51x when tested on the Vicuna and LLaMA2-Chat model series. These results outstrip existing speculative decoding methods for LLMs, including Eagle, Medusa, Lookahead, SPS, and PLD, while maintaining a compact drafter architecture equivalent to merely two Transformer layers.

## **4.2 Metrics**  
Like other speculative decoding methods, Falcon primarily focuses on latency rather than throughput. We assess acceleration effects using the following metrics:  
- **Wall-time speedup ratio** : The actual test speedup ratio relative to vanilla AR decoding.  
- **Acceptance rate (** _α_ **)** : The ratio of tokens generated by the drafter to all tokens gauges draft accuracy.

### 문장

- s1: 추정 디코딩은 자동 회귀형 디코딩을 가속화하기 위해 널리 받아들여지는 기술이지만, 기존 방법들은 비효율적인 KV 캐시 최적화 전략으로 인해 상당한 속도 향상을 달성하기 어렵고 낮은 수용률을 초래한다. [2502.10424v1]
- s2: 본 연구는 추상적 디코딩이 대형 언어 모델(LLM) 연산의 효율성을 크게 향상시켜 이러한 모델의 보다 진보적이고 실용적인 응용을 가능하게 함을 보여줍니다. [2412.19925v2]
- s3: 이 프레임워크는 Vicuna와 LLaMA2-Chat 모델 시리즈에서 테스트했을 때 2.91배에서 3.51배까지 손실 없는 속도 향상을 달성한다. [2412.12639v3]
- s4: 그러나 속도 향상이 항상 보장되는 것은 아니며, 특정 조건에서는 기저라인보다 낮은 성능을 보일 수도 있습니다[2412.19925v2].
- s5: Speculative decoding은 일반적으로 2.5배에서 3.51배까지 생성 속도를 향상시킬 수 있습니다[2502.10424v1][2412.12639v3].

## H_E02 — RAG를 붙이면 환각이 몇 % 정도 줄어든다는 연구 있어?

### 인용 블록

[문서 1]
[Distance: 0.3538]
[발행일: 2025-03-30]
[2504.08758v1] Hyper-RAG: Combating LLM Hallucinations using Hypergraph-Driven Retrieval-Augmented Generation
1  
nine diverse datasets showed a 35.5% performance improvement over Light RAG using a selection-based assessment. The lightweight variant, Hyper-RAG-Lite, achieved twice the retrieval speed and a 3.3% performance boost compared with Light RAG. These results confirm Hyper-RAG’s effectiveness in enhancing LLM reliability and reducing hallucinations, making it a robust solution for high-stakes applications like medical diagnostics.
[문서 5]
[Distance: 0.3750]
[발행일: 2026-01-10]
[2601.06551v1] L-RAG: Balancing Context and Retrieval with Entropy-Based Lazy Loading
[초록] Retrieval-Augmented Generation (RAG) has emerged as the predominant paradigm for grounding Large Language Model outputs in factual knowledge, effectively mitigating hallucinations. However, conventional RAG systems operate under a "retrieve-always" assumption, querying vector databases for every input regardless of query complexity. This static approach incurs substantial computational overhead and inference latency, particularly problematic for high-throughput production deployments. We introduce L-RAG (Lazy Retrieval-Augmented Generation), an adaptive framework that implements hierarchical context management through entropy-based gating. L-RAG employs a two-tier architecture: queries are first processed with a compact document summary, and expensive chunk retrieval is triggered only when the model's predictive entropy exceeds a calibrated threshold, signaling genuine uncertainty. Through experiments on SQuAD 2.0 (N=500) using the Phi-2 model, we demonstrate that L-RAG provides a tunable accuracy-efficiency trade-off: at a conservative threshold (tau=0.5), L-RAG achieves 78.2% accuracy, matching Standard RAG (77.8%), with 8% retrieval reduction; at a balanced threshold (tau=1.0), retrieval reduction increases to 26% with modest accuracy trade-off (76.0%). Latency analysis shows that L-RAG saves 80-210ms per query when retrieval latency exceeds 500ms. Analysis of entropy distributions reveals statistically significant separation (p < 0.001) between correct predictions (H=1.72) and errors (H=2.20), validating entropy as a reliable uncertainty signal. L-RAG offers a practical, training-free approach toward more efficient RAG deployment, providing system architects with a configurable knob to balance accuracy and throughput requirements.

The comparison between L-RAG and Strong RAG reveals a genuine trade-off. L-RAG sacrifices approximately 1.6 percentage points of accuracy (78.2% vs 79.8%) in exchange for 8% retrieval reduction. At more aggressive thresholds ( _τ_ = 1 _._ 0), retrieval reduction increases to 26% with 3.8 percentage points accuracy trade-off

### 문장

- s1: 제공된 문서에 따르면, Hyper-RAG는 다양한 데이터셋에서 Light RAG 대비 35.5%의 성능 향상을 보이며 환각 감소 효과를 확인했습니다[2504.08758v1].
- s2: 반면 L-RAG는 SQuAD 2.0 데이터셋에서 표준 RAG와 유사한 정확도를 유지하면서 검색량을 최대 26%까지 줄이는 결과를 제시합니다[2601.06551v1].
- s3: SQuAD 2.0(N=500) 데이터셋에서 Phi-2 모델을 이용해 수행한 실험을 통해 L-RAG가 조정 가능한 정확도‑효율성 트레이드오프를 제공함을 보여준다: 보수적 임계값(τ=0.5)에서는 정확도가 78.2%로 표준 RAG(77.8%)와 동등하며 검색 감소율이 8%이고, 균형 잡힌 임계값(τ=1.0)에서는 검색 감소율이 26%로 증가하면서 정확도는 76.0%로 약간 하락한다. [2601.06551v1]
- s4: 선택 기반 평가 방법을 통해 nine 개의 다양한 데이터셋에서 Light RAG 대비 35.5%의 성능 향상을 보였다. [2504.08758v1]

## H_E03 — LLM을 4비트로 양자화하면 정확도가 얼마나 떨어져?

### 인용 블록

[문서 1]
[Distance: 0.2953]
[발행일: 2026-07-01]
[2607.01127v1] $\text{Log}_\text{b}$Quant: Quantizing Language Models in Logarithmic Space
[초록] Quantization has become an invaluable tool to reduce memory requirements and inference speed of modern language models, in particular to make them available for consumer setups and edge devices. While previous work has primarily focused on uniform quantization codebooks, such approaches are prone to suboptimal representations due to low-frequency high-magnitude weights. We introduce Log$_\text{b}$Quant, a novel logarithmic quantization approach with adjustable bases, to adapt to common parameter distributions. We show that our method exhibits superior performance at 4-bit precision on several performance benchmarks compared to asymmetric linear quantization at tensor-wise granularity, while achieving moderate speedup and high memory savings, making it suitable for private use on consumer-grade GPUs.

## **5 Discussion and Limitations**

Our novel quantization scheme, LogbQuant, shows superior benchmark performance against asymmetric linear quantization at 4-bit and comes with minor to moderate speedups and significant memory savings compared to the unquantized model
[문서 2]
[Distance: 0.2931]
[발행일: 2026-06-04]
[2606.11244v1] SPEAR: A System for Post-Quantization Error-Adaptive Recovery Enabling Efficient Low-Bit LLM Serving
[초록] Efficient large language model (LLM) serving is increasingly constrained by deployment cost. Quantization is a key technique for reducing serving cost, yet even state-of-the-art 4-bit quantizers exhibit a noticeable quality gap from FP16, particularly for smaller models where low-bit serving is most beneficial. We identify a fundamental cause of this gap: quantization error is highly input-dependent and varies substantially across tokens, while existing post-quantization compensation methods are static and apply identical corrections to all inputs. As a result, easy tokens are over-corrected while hard tokens remain under-corrected. We present SPEAR, a system for post-quantization error-adaptive recovery that improves low-bit LLM serving. SPEAR introduces lightweight Error Compensators (ECs) modulated by per-token gates and places them only at the most error-sensitive layers identified through a CKA-guided entropy-aware diagnostic. This focuses a small parameter budget where it is most effective. Efficient deployment of ECs presents several systems challenges, including additional computation, tensor-parallel synchronization caused by input-dependent gating, and latency instability across configurations. SPEAR addresses these issues through adaptive kernel-fusion dispatch, combining an epilogue-integrated peer-reduction kernel with P2P dual-write to fuse the post-EC computation into low-bit GEMMs, and an SLO-constrained EC-aware scheduler for predictable serving performance. Across challenging per-channel quantization settings, SPEAR recovers 56-75% of the perplexity gap between W4 and FP16 while adding less than 1% model memory overhead and maintaining latency comparable to a widely used 4-bit serving deployment.

To better understand the remaining accuracy gap in 4-bit inference, we examine the structure of quantization error. We observe that, for a fixed quantized model, quantization error varies sharply across inputs: some tokens incur only minor error, while others exhibit substantially larger deviation, as shown in Figure 1. This suggests that different tokens require substantially different amounts of compensation. Existing quantization error compensation methods Li et al. [2023], Zhao et al
[문서 3]
[Distance: 0.4340]
[발행일: 2026-05-14]
[2605.15138v1] Forgetting That Sticks: Quantization-Permanent Unlearning via Circuit Attribution
[초록] Standard unlearning evaluations measure behavioral suppression in full precision, immediately after training, despite every deployed language model being quantized first. Recent work has shown that 4-bit post-training quantization can reverse machine unlearning; we show this is not a tuning artefact but a systematic dual failure: gradient-based methods that achieve meaningful forgetting lose it under compression, while methods that survive quantization barely change the model. Both failures trace to the same root cause: across all baselines, per-parameter updates lie 47-828x below the NF4 quantization bin width; updates diffused across billions of parameters cannot clear quantization bin boundaries, a consequence we formalize as a sparsity-permanence tradeoff. We present MANSU (Mechanistic-Aligned Null-Space Unlearning), which resolves both modes by combining causal circuit attribution to isolate the minimal forget-set subgraph, circuit-restricted null-space projection with a diagonal-Fisher retain bound, and a per-parameter magnitude floor guaranteeing quantization survival by construction. We additionally introduce Circuit Attribution Divergence (CAD), a mechanistic verification metric distinguishing structural erasure from behavioral suppression, a distinction existing metrics cannot make. Across multiple model families and hazard benchmarks, MANSU is the first method to jointly satisfy all four properties with margin on each (meaningful forgetting, retain preservation, non-positive PTQ gap, and structural erasure), while gradient-based baselines recover up to +0.05 accuracy under compression.

Machine unlearning has become a safety-critical capability for deployed language models: hazardous-knowledge memorisation (biosecurity, cyberweapons, chemical synthesis) makes it necessary [1], and right-to-erasure regulations (EU AI Act, GDPR) make it legally required [2]. Yet every deployed LLM today is quantized 4-bit formats (NF4, GPTQ, AWQ) reduce memory by 4 _×_ and inference cost by 2–3 _×_ , making quantization the standard final step before release

### 문장

- s1: LogbQuant라는 새로운 양자화 방식은 4비트에서 비대칭 선형 양자화에 비해 우수한 벤치마크 성능을 보이며, 비양자화 모델에 비해 소규모에서 중간 규모의 속도 향상과 상당한 메모리 절약을 제공합니다. [2607.01127v1]
- s2: 최근 연구는 4비트 사후 학습 양자화가 기계 학습을 되돌릴 수 있음을 보여주었으며, 이 논문은 이것이 튜닝에 의한 오류가 아니라 압축 시 의미 있는 망각을 상실하는 경사 기반 방법과 양자화에 견디지만 모델이 거의 변하지 않는 방법이 공존하는 체계적인 이중 실패임을 제시한다. [2605.15138v1]
- s3: LogbQuant는 기존 비대칭 선형 양자화에 비해 4비트 정밀도에서 우수한 성능을 보이며, 이는 벤치마크 결과에서 확인됩니다[2607.01127v1].
- s4: SPEAR는 채널별 양자화 설정에서 W4와 FP16 사이의 퍼플렉시티 격차의 56-75%를 회복한다는 점을 강조합니다[2606.11244v1].
- s5: 어려운 채널별 양자화 설정에서도 SPEAR는 W4와 FP16 사이의 퍼플렉시티 격차의 56~75%를 회복하면서 모델 메모리 오버헤드를 1% 미만으로 유지하고, 널리 사용되는 4비트 서빙 배포와 유사한 지연 시간을 확보합니다. [2606.11244v1]
- s6: 또한, 4비트 포스트-훈련 양자화는 모델 압축 시 의미 있는 망각을 잃거나 변화를 거의 보이지 않는 등 정확도 손실과 관련된 근본적인 한계를 드러냅니다[2605.15138v1].

## H_E04 — 리랭커를 붙이면 검색 정확도(Recall@10)가 얼마나 올라가?

### 인용 블록

[문서 1]
[Distance: 0.3067]
[발행일: 2026-03-02]
[2603.02153v1] Scaling Retrieval Augmented Generation with RAG Fusion: Lessons from an Industry Deployment
[초록] Retrieval-Augmented Generation (RAG) systems commonly adopt retrieval fusion techniques such as multi-query retrieval and reciprocal rank fusion (RRF) to increase document recall, under the assumption that higher recall leads to better answer quality. While these methods show consistent gains in isolated retrieval benchmarks, their effectiveness under realistic production constraints remains underexplored. In this work, we evaluate retrieval fusion in a production-style RAG pipeline operating over an enterprise knowledge base, with fixed retrieval depth, re-ranking budgets, and latency constraints. Across multiple fusion configurations, we find that retrieval fusion does increase raw recall, but these gains are largely neutralized after re-ranking and truncation. In our setting, fusion variants fail to outperform single-query baselines on KB-level Top-$k$ accuracy, with Hit@10 decreasing from $0.51$ to $0.48$ in several configurations. Moreover, fusion introduces additional latency overhead due to query rewriting and larger candidate sets, without corresponding improvements in downstream effectiveness. Our analysis suggests that recall-oriented fusion techniques exhibit diminishing returns once realistic re-ranking limits and context budgets are applied. We conclude that retrieval-level improvements do not reliably translate into end-to-end gains in production RAG systems, and argue for evaluation frameworks that jointly consider retrieval quality, system efficiency, and downstream impact.

## **1.1 Contributions**  
This paper makes the following contributions:  
- We present a production-oriented evaluation of retrieval fusion methods in a RAG pipeline operating under fixed retrieval depth, reranking budgets, and latency constraints.  
- We empirically analyze the relationship between retrieval-level recall gains and downstream KB-level accuracy, showing that fusion-induced recall improvements are frequently neutralized after re-ranking and truncation.
[문서 2]
[Distance: 0.3417]
[발행일: 2025-05-13]
[2505.08445v1] Optimizing Retrieval-Augmented Generation: Analysis of Hyperparameter Impact on Performance and Efficiency
[초록] Large language models achieve high task performance yet often hallucinate or rely on outdated knowledge. Retrieval-augmented generation (RAG) addresses these gaps by coupling generation with external search. We analyse how hyperparameters influence speed and quality in RAG systems, covering Chroma and Faiss vector stores, chunking policies, cross-encoder re-ranking, and temperature, and we evaluate six metrics: faithfulness, answer correctness, answer relevancy, context precision, context recall, and answer similarity. Chroma processes queries 13% faster, whereas Faiss yields higher retrieval precision, revealing a clear speed-accuracy trade-off. Naive fixed-length chunking with small windows and minimal overlap outperforms semantic segmentation while remaining the quickest option. Re-ranking provides modest gains in retrieval quality yet increases runtime by roughly a factor of 5, so its usefulness depends on latency constraints. These results help practitioners balance computational cost and accuracy when tuning RAG systems for transparent, up-to-date responses. Finally, we re-evaluate the top configurations with a corrective RAG workflow and show that their advantages persist when the model can iteratively request additional evidence. We obtain a near-perfect context precision (99%), which demonstrates that RAG systems can achieve extremely high retrieval accuracy with the right combination of hyperparameters, with significant implications for applications where retrieval quality directly impacts downstream task performance, such as clinical decision support in healthcare.

|Context Recall Score|False|Faiss|1024|0.8|4|naive|128|86%|
|Answer Similarity Score|False|Faiss|1024|1.0|4|naive|128|86%|  
combination of hyperparameters. This finding has significant implications for applications where retrieval quality directly impacts downstream task performance.

### 문장

- s1: [2603.02153v1]에 따르면, 리랭커 적용 후 재랭킹과 컨텍스트 예산이 현실적인 제약을 받으면 recall-oriented fusion 기법의 이득은 감소하며, 검색 수준의 recall 향상이 최종 시스템 성능으로 직접 전환되지 않는다[2603.02153v1].
- s2: 반면 [2505.08445v1]는 특정 하이퍼파라미터 조합을 통해 Faiss를 사용할 때 context recall이 86%에 달하는 높은 정확도를 달성할 수 있음을 보여준다[2505.08445v1].
- s3: |Context Recall Score|False|Faiss|1024|0.8|4|naive|128|86%| |Answer Similarity Score|False|Faiss|1024|1.0|4|naive|128|86%| combination of hyperparameters. [2505.08445v1]
- s4: 검색 증강 생성(RAG) 시스템은 높은 문서 재현율을 높이기 위해 다중 쿼리 검색과 상호 순위 융합(RRF)과 같은 검색 융합 기법을 일반적으로 채택하며, 이는 재현율이 높아질수록 답변 품질이 향상된다는 전제하에 수행된다. [2603.02153v1]

## H_E05 — LLM 판정자가 자기 모델 답을 얼마나 더 높게 평가하는지 수치로 보여준 연구 있어?

### 인용 블록

[문서 1]
[Distance: 0.3272]
[발행일: 2025-04-04]
[2504.03846v3] Do LLM Evaluators Prefer Themselves for a Reason?
[초록] Large language models (LLMs) are increasingly used as automatic evaluators in applications such as benchmarking, reward modeling, and self-refinement. Prior work highlights a potential self-preference bias where LLMs favor their own generated responses, a tendency often intensifying with model size and capability. This raises a critical question: Is self-preference harmful, or does it simply reflect the genuinely higher-quality outputs of stronger models? Answering this has been difficult as prior works mostly relied on subjective tasks that lack an objective ground truth, meaning that either preference can be reasonably justified. To address this ambiguity, we investigate self-preference using verifiable benchmarks (mathematical reasoning, factual knowledge, code generation) that allow objective ground-truth assessment. This enables us to distinguish harmful (favoring objectively worse responses) from legitimate (favoring genuinely superior ones) self-preference. Our large-scale experiments across 7 model families reveal three key findings: (1) While stronger models exhibit greater self-preference, much of this preference aligns with objectively superior performance, indicating stronger models prefer themselves mostly legitimately. (2) Harmful self-preference persists when evaluator models err as generators, and stronger models display more pronounced harmful self-preference bias when they do err. This suggests stronger models struggle more to recognize when they are wrong. (3) Inference-time scaling strategies, such as generating a long Chain-of-Thought before evaluation, effectively reduce the harmful self-preference. Additionally, we experiment with LMArena and show that our findings extend beyond verifiable benchmarks to real-world, subjective domains. These results provide a more nuanced understanding of LLM-based evaluation and practical insights for improving its reliability.

. In this work, we present an in-depth analysis of self-preference bias in LLMs and provide empirical insights for improving the reliability of LLM-based evaluations.
[문서 2]
[Distance: 0.3624]
[발행일: 2025-04-04]
[2504.03846v3] Do LLM Evaluators Prefer Themselves for a Reason?
[초록] Large language models (LLMs) are increasingly used as automatic evaluators in applications such as benchmarking, reward modeling, and self-refinement. Prior work highlights a potential self-preference bias where LLMs favor their own generated responses, a tendency often intensifying with model size and capability. This raises a critical question: Is self-preference harmful, or does it simply reflect the genuinely higher-quality outputs of stronger models? Answering this has been difficult as prior works mostly relied on subjective tasks that lack an objective ground truth, meaning that either preference can be reasonably justified. To address this ambiguity, we investigate self-preference using verifiable benchmarks (mathematical reasoning, factual knowledge, code generation) that allow objective ground-truth assessment. This enables us to distinguish harmful (favoring objectively worse responses) from legitimate (favoring genuinely superior ones) self-preference. Our large-scale experiments across 7 model families reveal three key findings: (1) While stronger models exhibit greater self-preference, much of this preference aligns with objectively superior performance, indicating stronger models prefer themselves mostly legitimately. (2) Harmful self-preference persists when evaluator models err as generators, and stronger models display more pronounced harmful self-preference bias when they do err. This suggests stronger models struggle more to recognize when they are wrong. (3) Inference-time scaling strategies, such as generating a long Chain-of-Thought before evaluation, effectively reduce the harmful self-preference. Additionally, we experiment with LMArena and show that our findings extend beyond verifiable benchmarks to real-world, subjective domains. These results provide a more nuanced understanding of LLM-based evaluation and practical insights for improving its reliability.

## 8 CONCLUSION

In this work, we investigate self-preference in LLMs using verifiable benchmarks with objective ground-truth reference. Our experiments suggest that self-preference often reflects genuine output quality in more capable models. Stronger models tend to be more accurate judges, with their preferences frequently aligned with objective correctness. However, harmful self-preference persists when models favor an objectively incorrect response by themselves

### 문장

- s1: [2504.03846v3]는 각각 "stronger models exhibit greater self-preference"라는 정성적 관찰을 통해 모델 강도에 따라 자기 선호도가 증가함을 보고합니다.
- s2: 7개의 모델 패밀리에 걸친 대규모 실험은 세 가지 주요 결과를 제시한다: (1) 더 강력한 모델일수록 자기 선호도가 높아지지만, 이러한 선호도는 객관적으로 우수한 성능과 크게 일치하므로, 강력한 모델이 자신을 선호하는 것은 대부분 정당하다. [2504.03846v3]

## H_E06 — 프롬프트 압축으로 토큰을 몇 배까지 줄여도 성능이 유지돼?

### 인용 블록

[문서 2]
[Distance: 0.4029]
[발행일: 2025-08-16]
[2508.15813v1] SCOPE: A Generative Approach for LLM Prompt Compression
[초록] Prompt compression methods enhance the efficiency of Large Language Models (LLMs) and minimize the cost by reducing the length of input context. The goal of prompt compression is to shorten the LLM prompt while maintaining a high generation quality. However, existing solutions, mainly based on token removal, face challenges such as information loss and structural incoherence, like missing grammar elements in a sentence, or incomplete word phrases after token removal. Such challenges limit the final generation quality of LLM. To overcome these limitations, we present a novel generative prompt compression method. Unlike the existing token removal methods, our method centers at a chunking-and-summarization mechanism. Specifically, our method splits prompt into semantically coherent chunks and rewrites the chunks to be more concise. The chunks are reconstructed into meaningful prompt finally. We design several optimization techniques for the mechanism, including optimized semantic chunking, outlier chunk handling, dynamic compression ratio, compression prioritization, and keyword maintaining. These techniques effectively improve the identifying and preserving of critical information and coherence among texts, as well as providing finer grind control of the compression ratio. We conduct extensive evaluation on question-answering and summarization tasks, with datasets covering multiple different domain. The evaluation shows our method achieves a significantly better compression quality, and higher stability than the state-of-the-art methods, especially under high compression ratio, which proves the effectiveness and practicality of our method.

developed to shorten prompts while retaining essential information.
The state of the art methods are based on selective compression,
which focus on identifying and retaining the most important tokens
of the original prompt, while literally removing less critical tokens.
Although such approaches reduce prompt length, they have notable
drawbacks:  
- **Breaking contextual integrity:** By removing tokens of the
[문서 3]
[Distance: 0.4387]
[발행일: 2024-03-19]
[2403.12968v2] LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression
[초록] This paper focuses on task-agnostic prompt compression for better generalizability and efficiency. Considering the redundancy in natural language, existing approaches compress prompts by removing tokens or lexical units according to their information entropy obtained from a causal language model such as LLaMa-7B. The challenge is that information entropy may be a suboptimal compression metric: (i) it only leverages unidirectional context and may fail to capture all essential information needed for prompt compression; (ii) it is not aligned with the prompt compression objective. To address these issues, we propose a data distillation procedure to derive knowledge from an LLM to compress prompts without losing crucial information, and meantime, introduce an extractive text compression dataset. We formulate prompt compression as a token classification problem to guarantee the faithfulness of the compressed prompt to the original one, and use a Transformer encoder as the base architecture to capture all essential information for prompt compression from the full bidirectional context. Our approach leads to lower latency by explicitly learning the compression objective with smaller models such as XLM-RoBERTa-large and mBERT. We evaluate our method on both in-domain and out-of-domain datasets, including MeetingBank, LongBench, ZeroScrolls, GSM8K, and BBH. Despite its small size, our model shows significant performance gains over strong baselines and demonstrates robust generalization ability across different LLMs. Additionally, our model is 3x-6x faster than existing prompt compression methods, while accelerating the end-to-end latency by 1.6x-2.9x with compression ratios of 2x-5x. Our code is available at https://aka.ms/LLMLingua-2.

- We approach prompt compression as a token classification task ( _i.e._ , preserve or discard), and take the predicted probability of each token being labeled as preserve as the compression metric. The benefits are three folds: (1) It can capture all essential information needed for prompt compression from the full bidirectional context by using a Transformer encoder for feature extraction

### 문장

- s1: 평가 결과, 본 방법은 최신 기술 대비 압축 품질과 안정성이 크게 향상되었으며, 특히 높은 압축 비율에서도 이러한 성능을 유지함으로써 본 방법의 효과성과 실용성을 입증한다. [2508.15813v1]
- s2: SCOPE는 고압축 비율에서도 성능을 유지하며, 기존 최첨단 방법보다 압축 품질과 안정성이 크게 향상된다고 보고한다[2508.15813v1].
- s3: 또한, 본 모델은 기존 프롬프트 압축 방법에 비해 3배에서 6배 빠르게 수행되며, 2배에서 5배의 압축 비율을 달성하면서 엔드투엔드 지연 시간을 1.6배에서 2.9배 가속화합니다. [2403.12968v2]
- s4: LLMLingua-2는 2배~5배의 압축 비율에서 모델 성능이 강기초선을 크게 앞지르고, 다양한 LLM에 걸쳐 견고한 일반화 능력을 보인다고 제시한다[2403.12968v2].

## H_E07 — 긴 컨텍스트에서 필요한 정보가 중간에 있으면 정확도가 얼마나 떨어져?

### 인용 블록

[문서 1]
[Distance: 0.3204]
[발행일: 2024-10-08]
[2410.05983v1] Long-Context LLMs Meet RAG: Overcoming Challenges for Long Inputs in RAG
[초록] Retrieval-augmented generation (RAG) empowers large language models (LLMs) to utilize external knowledge sources. The increasing capacity of LLMs to process longer input sequences opens up avenues for providing more retrieved information, to potentially enhance the quality of generated outputs. It is plausible to assume that a larger retrieval set would contain more relevant information (higher recall), that might result in improved performance. However, our empirical findings demonstrate that for many long-context LLMs, the quality of generated output initially improves first, but then subsequently declines as the number of retrieved passages increases. This paper investigates this phenomenon, identifying the detrimental impact of retrieved "hard negatives" as a key contributor. To mitigate this and enhance the robustness of long-context LLM-based RAG, we propose both training-free and training-based approaches. We first showcase the effectiveness of retrieval reordering as a simple yet powerful training-free optimization. Furthermore, we explore training-based methods, specifically RAG-specific implicit LLM fine-tuning and RAG-oriented fine-tuning with intermediate reasoning, demonstrating their capacity for substantial performance gains. Finally, we conduct a systematic analysis of design choices for these training-based methods, including data distribution, retriever selection, and training context length.

_retrieved context?_  
**Experimental setting.** We analyze the relationship between RAG performance and retrieval quality,
specifically recall and precision, using the Gemma-2-9B-Chat LLM with both e5 and BM25 retrievers
(Figure 2). Recall@k measures the presence of relevant passages within the top-k retrieved passages,
while precision@k quantifies the proportion of relevant passages among them.  
|Col1|Col2|Col3|Col4|Col5|Col6|RAG ac|curac|y|
|---|---|---|---|---|---|---|---|---|
||||||||||
[문서 3]
[Distance: 0.3335]
[발행일: 2024-09-03]
[2409.01666v1] In Defense of RAG in the Era of Long-Context Language Models
[초록] Overcoming the limited context limitations in early-generation LLMs, retrieval-augmented generation (RAG) has been a reliable solution for context-based answer generation in the past. Recently, the emergence of long-context LLMs allows the models to incorporate much longer text sequences, making RAG less attractive. Recent studies show that long-context LLMs significantly outperform RAG in long-context applications. Unlike the existing works favoring the long-context LLM over RAG, we argue that the extremely long context in LLMs suffers from a diminished focus on relevant information and leads to potential degradation in answer quality. This paper revisits the RAG in long-context answer generation. We propose an order-preserve retrieval-augmented generation (OP-RAG) mechanism, which significantly improves the performance of RAG for long-context question-answer applications. With OP-RAG, as the number of retrieved chunks increases, the answer quality initially rises, and then declines, forming an inverted U-shaped curve. There exist sweet points where OP-RAG could achieve higher answer quality with much less tokens than long-context LLM taking the whole context as input. Extensive experiments on public benchmark demonstrate the superiority of our OP-RAG.

performance of RAG for long-context questionanswer applications. OP-RAG’s superior performance suggests that efficient retrieval and focused context utilization can outperform the brute-force approach of processing extremely long contexts.

### 문장

- s1: 공용 벤치마크에 대한 광범위한 실험은 본 연구에서 제안한 OP-RAG의 우수성을 입증한다. [2409.01666v1]
- s2: 긴 컨텍스트에서 필요한 정보가 중간에 있을 때, 생성된 출력의 품질은 초기에는 향상되지만 검색된 패시지 수가 증가함에 따라 이후 감소하는 경향을 보인다 [2410.05983v1].
- s3: 또한 이 논문은 훈련 기반 방법을 탐색하며, 구체적으로 RAG 특화 암시적 LLM 미세조정과 중간 추론을 활용한 RAG 지향적 미세조정을 제시하여 상당한 성능 향상의 가능성을 입증한다. [2410.05983v1]
- s4: 또한, 긴 컨텍스트를 전체로 입력받는 방식보다 효율적인 검색과 집중된 문맥 활용이 더 높은 답변 품질을 달성할 수 있다는 결과가 제시된다 [2409.01666v1].

## H_E08 — 웹 에이전트 벤치마크에서 제일 좋은 모델 성공률이 몇 %야?

### 인용 블록

[문서 1]
[Distance: 0.4609]
[발행일: 2026-06-01]
[2606.02404v1] K-BrowseComp: A Web Browsing Agent Benchmark Grounded in Korean Contexts
[초록] Frontier model evaluations are shifting from foundational capabilities (e.g., instruction following and reasoning) toward compositional, agentic ones, but Korean agentic benchmarks remain scarce. We introduce K-BrowseComp, a web-browsing agent benchmark grounded in Korean contexts, consisting of 400 problems. The 300-problem K-BrowseComp-Verified subset is manually constructed and validated by native Korean speakers. On this subset, frontier LLMs, including GPT-5.5, DeepSeek-V4-Pro, and GLM-5.1, reach only 30.00--45.67\%, a substantial drop from BrowseComp, while Korean LLMs released through Korea's Proprietary AI Foundation Model program obtain only 0.00--10.33\%. We further construct a 100-problem synthetic split using hard few-shot exemplars and failure-mode-targeted generation to exploit the asymmetry between solving and creating web browsing problems. On the adversarially filtered synthetic diagnostic split, the strongest model reaches only 26.00\%, and we report this split separately as a targeted stress test. We publicly release our data and code.

Based on this motivation, we take a first step toward building Korean agentic benchmarks by proposing K-BROWSECOMP, a browsing agent benchmark grounded in Korean contexts. We focus  
1
[문서 2]
[Distance: 0.3951]
[발행일: 2026-06-12]
[2606.14397v5] Running the Gauntlet: Hard Agentic Tasks
[초록] As agentic systems continue to evolve and are widely deployed in real-world scenarios, there is a growing demand to faithfully evaluate their capabilities. However, current benchmarks are typically built on popular applications with relatively simple tasks and focus on a narrow set of capabilities while overlooking broader dimensions, resulting in saturated performance on modern agents and failing to probe their limitations. To this end, we introduce GauntletBench, a web-based benchmark for evaluating agent generalisation in challenging scenarios, focusing on three underexplored capabilities (temporal perception, graphical understanding, and 3D reasoning), across five less-covered professional applications (Video Editor, Workflow Builder, 3D Modeller, Flight Analyser, and Circuit Designer), each with 27 vision-intensive tasks (135 in total). Our benchmark provides a modular pipeline that comprises an environment compatible with both open- and closed-source agent frameworks, a controlled web-based application, a well-structured task suite, and an automated evaluation engine with diverse metrics. Contrary to widespread expectations, our empirical results reveal that frontier agentic systems remain far from achieving human-level performance. Even the state-of-the-art agent achieves only a 28.2% success rate on our GauntletBench, highlighting the limitations in these overlooked capabilities and generalisation. By comparison, non-expert human annotators achieve over 80% success on our challenging yet feasible tasks, revealing the substantial gap between current agent capabilities and those required for complex real-world scenarios.

- [50] Ori Yoran, Samuel Joseph Amouyal, Chaitanya Malaviya, Ben Bogin, Ofir Press, and Jonathan Berant. Assistantbench: Can web agents solve realistic and time-consuming tasks?, 2024.

### 문장

- s1: [2606.14397v5]는 이 낮은 성적이 모델이 아직 충분히 탐구되지 않은 능력과 일반화 한계 때문에 발생함을 강조합니다.
- s2: 이 하위 집합에서 GPT-5.5, DeepSeek-V4-Pro, GLM-5.1을 포함한 최첨단 대형 언어 모델(LLMs)은 BrowseComp 대비 크게 감소한 30.00~45.67%의 성능만을 달성하고 있으며, 한국 정부 산하 고유 AI 기반 모델 프로그램으로 출시된 한국어 LLM들은 0.00~10.33%에 그치고 있다. [2606.02404v1]
- s3: [2606.02404v1]에 의하면 이 결과는 BrowseComp 대비 큰 하락을 보였으며, 한국어 컨텍스트에 특화된 벤치마크에서는 해당 수치가 관찰됩니다.
- s4: 비전문가 인간 주석가는 어려운 그러나 실현 가능한 작업에서 80% 이상의 성공률을 달성함으로써 현재 에이전트의 능력과 복잡한 실제 시나리오에 필요한 능력 사이의 큰 격차를 드러냈다. [2606.14397v5]

## H_F02 — RAG 평가에서 같은 LLM이 답 생성과 근거성 판정을 둘 다 하면 점수가 부풀려지는가. 판정 모델을 분리했을 때 차이를 측정한 연구를 찾아라.

### 인용 블록

[문서 1]
[Distance: 0.3850]
[발행일: 2024-08-15]
[2408.08067v2] RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation
[초록] Despite Retrieval-Augmented Generation (RAG) showing promising capability in leveraging external knowledge, a comprehensive evaluation of RAG systems is still challenging due to the modular nature of RAG, evaluation of long-form responses and reliability of measurements. In this paper, we propose a fine-grained evaluation framework, RAGChecker, that incorporates a suite of diagnostic metrics for both the retrieval and generation modules. Meta evaluation verifies that RAGChecker has significantly better correlations with human judgments than other evaluation metrics. Using RAGChecker, we evaluate 8 RAG systems and conduct an in-depth analysis of their performance, revealing insightful patterns and trade-offs in the design choices of RAG architectures. The metrics of RAGChecker can guide researchers and practitioners in developing more effective RAG systems. This work has been open sourced at https://github.com/amazon-science/RAGChecker.

## **3.2 Fine-grained Evaluation with Claim Entailment**

As illustrated in Fig. 1, a response generated by a RAG system might be a mixture of correct ( le) ) and incorrect claims ( x ), while also missing some in-ground-truth claims ( A ). In this sense, evaluating responses at a finer granularity is crucial to comprehensively assess the quality of an answer
[문서 2]
[Distance: 0.4294]
[발행일: 2024-04-15]
[2404.13076v1] LLM Evaluators Recognize and Favor Their Own Generations
[초록] Self-evaluation using large language models (LLMs) has proven valuable not only in benchmarking but also methods like reward modeling, constitutional AI, and self-refinement. But new biases are introduced due to the same LLM acting as both the evaluator and the evaluatee. One such bias is self-preference, where an LLM evaluator scores its own outputs higher than others' while human annotators consider them of equal quality. But do LLMs actually recognize their own outputs when they give those texts higher scores, or is it just a coincidence? In this paper, we investigate if self-recognition capability contributes to self-preference. We discover that, out of the box, LLMs such as GPT-4 and Llama 2 have non-trivial accuracy at distinguishing themselves from other LLMs and humans. By fine-tuning LLMs, we discover a linear correlation between self-recognition capability and the strength of self-preference bias; using controlled experiments, we show that the causal explanation resists straightforward confounders. We discuss how self-recognition can interfere with unbiased evaluations and AI safety more generally.

In self-evaluation, as the name suggests, the same underlying LLM acts as both the evaluator and the evaluatee. As a result, the neutrality of the evaluator is in question, and the evaluation can suffer from biases where the LLM evaluators diverge from humans in systematic ways (Zheng et al., 2024; Bai et al., 2024). One such bias is self-preference, where an LLM rates its own outputs higher than texts written by other LLMs or humans, while human annotators judge them as equal quality

### 문장

- s1: 하지만 동일한 대형 언어 모델(LLM) 이 평가자와 피평가자 역할을 동시에 수행함으로써 새로운 편향이 도입된다. [2404.13076v1]
- s2: 반면 [2408.08067v2]은 RAGChecker라는 평가 프레임워크를 제안하며, 이 도구가 인간 판단과 높은 상관관계를 보인다는 결과를 제시하지만, 동일한 LLM이 생성과 판정을 동시에 수행했을 때 점수가 부풀려지는지에 대한 직접적인 비교는 다루지 않습니다.
- s3: 본 논문에서는 검색 및 생성 모듈 모두에 대한 진단 지표를 통합한 정밀 평가 프레임워크인 RAGChecker를 제안한다. [2408.08067v2]
- s4: [2404.13076v1]는 LLM이 자신의 생성물을 더 높은 점수로 평가하는 '자기 선호 편향'을 확인하고, 이를 정량화하여 인과 관계를 규명했습니다.

