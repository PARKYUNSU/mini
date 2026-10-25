######## K01 | KV 캐시 압축 논문 4개 찾아서 각각 메모리를 몇 % 줄였는지 알려줘 | route direct_answer/B
  조건 0: 편수: 4편
  조건 1: 수치: 각 논문 메모리 감소 %
--- [문서 1] [Distance: 0.3654] [발행일: 2025-03-31] [2503.24000v1] Rethinking Key-Value Cache Compression Techniques for Large Language Model Serving [초록] Key-Value cache (\texttt{KV} \texttt{cache}) compression has emerged as a promising technique to optimize Large Language Model (LLM) serving. It primarily decreases the memory consumption of \texttt{KV} \texttt{cache} to reduce the computation cost. Despite the development of many compression algorithms, their applications in production environments are still not prevalent. In this paper, we revisit mainstream \texttt{KV} \texttt{cache} compression solutions from a practical perspective. Our con
--- [문서 2] [Distance: 0.4940] [발행일: 2026-06-14] [2607.09683v1] Ablation, Statistical Inference, and Validation for KV-Cache Compression [초록] This study systematically compares Turbo-Quant and SpectralQuant KV-cache compression, evaluating non-dominated schemes, including WHT rotation with Beta Lloyd-Max and QJL, through a statistical validation methodology that separates systematic codec differences from implementation variance. Key findings reveal that while eigenbasis-based methods fail on heavy-tailed data due to covariance instability, they excel in structured regimes, with the effective semantic dimension ($d_{eff}$) adapting to
--- [문서 3] [Distance: 0.4547] [발행일: 2026-03-29] [2603.27819v1] KVSculpt: KV Cache Compression as Distillation [초록] KV cache compression is critical for efficient long-context LLM inference. Approaches that reduce the per-pair footprint -- quantization and low-rank decomposition -- are orthogonal to those that reduce the sequence length of the cache. Along the sequence-length dimension, existing methods range from pure eviction -- selecting which KV pairs to keep -- to merging, which combines similar pairs into fewer ones. Both remain anchored to the original cache entries. We propose KVSculpt, which moves to
--- [문서 4] [Distance: 0.4216] [발행일: 2026-02-08] [2602.08005v1] DeltaKV: Residual-Based KV Cache Compression via Long-Range Similarity [초록] The deployment of efficient long-context LLMs in applications like autonomous agents, long-chain reasoning, and creative writing is fundamentally bottlenecked by the linear growth of KV cache memory. Existing compression and eviction methods often struggle to balance accuracy, compression ratio, and hardware efficiency. We propose DeltaKV, a residual-based KV cache compression framework motivated by two empirical findings: long-range inter-token similarity and highly shared latent components in
--- [문서 5] [Distance: 0.4084] [발행일: 2025-02-24] [2502.16886v4] ReFreeKV: Towards Threshold-Free KV Cache Compression [초록] To reduce memory consumption during LLM inference, a handful of methods have been proposed for KV cache pruning. While these techniques can accomplish lossless memory reduction on many datasets, they often hinge on an under-emphasized condition: an input/domain-specific threshold for KV cache budget needs to be pre-determined to achieve the optimal performance. However, such input-sensitive design may be considerably limited in real-world scenarios, as open-domain inputs span diverse domains, le
--- [문서 6] [Distance: 0.4911] [발행일: 2026-01-15] [2601.10155v1] LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers [초록] Compressing the KV cache is a required step to deploy large language models on edge devices. Current quantization methods compress storage but fail to reduce bandwidth as attention calculation requires dequantizing keys from INT4/INT8 to FP16 before use. We observe that attention scoring is mathematically equivalent to the inner product similarity search and we can apply some compression techniques from vector databases to compress KV-cache better. We propose LOOKAT, which applies product quanti
--- [문서 7] [Distance: 0.4880] [발행일: 2025-03-13] [2503.10714v3] ZSMerge: Zero-Shot KV Cache Compression for Memory-Efficient Long-Context LLMs [초록] The linear growth of key-value (KV) cache memory and quadratic computational in attention mechanisms complexity pose significant bottlenecks for large language models (LLMs) in long-context processing. While existing KV cache optimization methods address these challenges through token pruning or feature merging, they often incur irreversible information loss or require costly parameter retraining. To this end, we propose ZSMerge, a dynamic KV cache compression framework designed for efficient ca
--- [문서 8] [Distance: 0.5053] [발행일: 2026-04-09] [2604.08426v1] KV Cache Offloading for Context-Intensive Tasks [초록] With the growing demand for long-context LLMs across a wide range of applications, the key-value (KV) cache has become a critical bottleneck for both latency and memory usage. Recently, KV-cache offloading has emerged as a promising approach to reduce memory footprint and inference latency while preserving accuracy. Prior evaluations have largely focused on tasks that do not require extracting large amounts of information from the context. In this work, we study KV-cache offloading on context-in
--- [문서 9] [Distance: 0.4553] [발행일: 2025-04-21] [2504.15364v4] KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments [초록] We demonstrate that geometrically distinctive keys during LLM inference tend to have high attention scores. Based on the phenomenon we propose KeyDiff, a training-free KV cache eviction method based solely on key similarity. Unlike other KV cache eviction methods, KeyDiff can process arbitrarily long prompts within strict resource constraints and efficiently generate responses. We provide a theoretical basis for KeyDiff by relating key diversity with attention scores. These results imply KeyDiff
=== 답
<b>서론</b>
제공된 문서들은 모두 <b>KV 캐시 압축·감소 기술</b>을 다루고 있으며, 각 연구는 메모리 사용량을 줄이는 다양한 접근법을 제시하고 있습니다. 그러나 질문에서 요구한 “각 방법의 구체적인 감소 비율(%)”에 대한 정보는 제공되지 않았습니다.

<b>본론</b>
1. <b>Rethinking Key-Value Cache Compression Techniques for Large Language Model Serving</b>: 이 논문은 KV 캐시 압축이 LLM 서비스 최적화에 유망하지만, 실제 프로덕션 환경에서의 적용률은 아직 낮다고 언급합니다. [2503.24000v1]
2. <b>Ablation, Statistical Inference, and Validation for KV-Cache Compression</b>: Turbo‑Quant와 SpectralQuant를 비교하고 WHT rotation·Beta Lloyd-Max·QJL 등의 비우세한 스키마도 평가하지만, 감소 비율은 제시하지 않습니다. [2607.09683v1]
3. <b>KVSculpt: KV Cache Compression as Distillation</b>: KVSculpt는 압축을 증류 방식으로 제안하며 기존 방법과 직교한다는 점을 강조합니다. 구체적인 메모리 절감률은 언급되지 않았습니다. [2603.27819v1]

<b>결론</b>
제공된 문서들은 KV 캐시 압축이 메모리 소비를 감소시킨다는 공통된 목표를 가지고 있으나, 구체적인 감소 비율에 대한 수치 정보는 포함하고 있지 않습니다. [2503.24000v1]은 이러한 압축이 계산 비용을 낮추기 위해 주로 메모리 사용량을 감소시킨다고 명시하고 있습니다. 또한, [2603.27819v1]에서는 페어당 푸트프린트를 줄이는 접근법과 시퀀스 길이를 줄이는 접근법이 서로 직교한다고 언급합니다. 따라서 각 논문은 방법론적 차이와 적용 조건에 따라 결과를 다르게 제시하지만, 메모리 감소라는 핵심 효과는 공통으로 확인됩니다.

######## K02 | speculative decoding 논문 3개만 골라서 속도 향상 배수 비교해줘 | route direct_answer/B
  조건 0: 편수: 3편만
  조건 1: 수치: 속도 향상 배수
--- [문서 1] [Distance: 0.1930] [발행일: 2026-10-07] [2610.10411v1] Training Parallel Speculative Draft Models by Directly Minimizing Expected Decoding Rounds [초록] Speculative decoding accelerates large language model inference by using a low-cost draft model to propose tokens that the full-size target model verifies in parallel. Parallel and semi-autoregressive (semi- AR) drafters improve drafting efficiency by proposing an entire block in a single forward pass, but training them raises a new difficulty: the draft distribution for a given position depends on where the decoding round starts, and where rounds start depends on how many tokens earlier rounds accepted. Existing training objectives typica
--- [문서 2] [Distance: 0.2901] [발행일: 2024-12-27] [2412.19925v2] HADES: Hardware Accelerated Decoding for Efficient Speculation in Large Language Models [초록] Large Language Models (LLMs) have revolutionized natural language processing by understanding and generating human-like text. However, the increasing demand for more sophisticated LLMs presents significant computational challenges due to their scale and complexity. This paper introduces Hardware Accelerated Decoding (HADES), a novel approach to enhance the performance and energy efficiency of LLMs. We address the design of an LLM accelerator with hardware-level speculative decoding support, a concept not previously explored in existing litera
=== 답
<b>서론</b>
제공된 참고문서에는 <b>Speculative Decoding</b> 관련 논문을 두 편만 찾을 수 있습니다. 따라서 세 편의 논문으로 속도 향상 배수를 비교하는 요청은 문서 범위 내에서 충족할 수 없습니다.

<b>본론</b>
1. <b>Parallel Speculative Draft Models</b>: Directly minimizing Expected Decoding Rounds (EDR)를 통해 draft 모델의 훈련을 최적화하고, DSpark·DFly와 같은 최신 drafter에 적용해 평균 accepted length가 향상되었다고 보고한다[2610.10411v1].
2. <b>HADES: Hardware Accelerated Decoding for Efficient Speculation</b>: 하드웨어 레벨에서 speculative decoding을 지원하도록 설계된 LLM 가속기를 제시하며, draft 모델을 활용해 target 모델의 속도를 기저라인 대비 개선한다는 결과를 보여준다[2412.19925v2]

<b>결론</b>
제공된 두 문서에 따르면, <b>Parallel Speculative Draft Models</b>와 <b>HADES</b> 모두 speculative decoding으로 인해 속도 향상을 달성하지만, 구체적인 배수 값은 제시되지 않습니다. 따라서 세 편의 논문을 비교할 수 없습니다; 기존 연구는 EDR 기반 훈련과 하드웨어 가속을 통해 각각 효율성을 높였음을 확인할 수 있습니다[2610.10411v1][2412.19925v2].

######## K03 | RAG 리랭커 연구 5개 정리해줘 | route direct_answer/B
  조건 0: 편수: 5편
--- [문서 1] [Distance: 0.3160] [발행일: 2026-03-02] [2603.02153v1] Scaling Retrieval Augmented Generation with RAG Fusion: Lessons from an Industry Deployment [초록] Retrieval-Augmented Generation (RAG) systems commonly adopt retrieval fusion techniques such as multi-query retrieval and reciprocal rank fusion (RRF) to increase document recall, under the assumption that higher recall leads to better answer quality. While these methods show consistent gains in isolated retrieval benchmarks, their effectiveness under realistic production constraints remains underexplored. In this work, we evaluate retrieval fusion in a production-style RAG pipeline operating ov
--- [문서 2] [Distance: 0.3635] [발행일: 2026-06-14] [2606.28367v1] Beyond the Reranker: Do RAG Retrieval Enhancements Help Once a Strong Reranker Is Present? [초록] Retrieval-augmented generation (RAG) is routinely extended with methods meant to improve retrieval: query expansion, hierarchical and cross-document summarization, graph-based expansion, per-query routing, rank fusion, and corrective re-retrieval. The benefits reported for these methods come almost exclusively from homogeneous corpora, predominantly Wikipedia prose. Whether they hold on the mixed-format collections common in practice, where code, markdown, tables, scientific PDFs, and prose are
--- [문서 3] [Distance: 0.2422] [발행일: 2025-11-03] [2511.01386v1] RAGSmith: A Framework for Finding the Optimal Composition of Retrieval-Augmented Generation Methods Across Datasets [초록] Retrieval-Augmented Generation (RAG) quality depends on many interacting choices across retrieval, ranking, augmentation, prompting, and generation, so optimizing modules in isolation is brittle. We introduce RAGSmith, a modular framework that treats RAG design as an end-to-end architecture search over nine technique families and 46{,}080 feasible pipeline configurations. A genetic search optimizes a scalar objective that jointly aggregates retrieval metrics (recall@k, mAP, nDCG, MRR) and genera
--- [문서 4] [Distance: 0.3244] [발행일: 2025-05-13] [2505.08445v1] Optimizing Retrieval-Augmented Generation: Analysis of Hyperparameter Impact on Performance and Efficiency [초록] Large language models achieve high task performance yet often hallucinate or rely on outdated knowledge. Retrieval-augmented generation (RAG) addresses these gaps by coupling generation with external search. We analyse how hyperparameters influence speed and quality in RAG systems, covering Chroma and Faiss vector stores, chunking policies, cross-encoder re-ranking, and temperature, and we evaluate six metrics: faithfulness, answer correctness, answer relevancy, context precision, context recall
--- [문서 5] [Distance: 0.2974] [발행일: 2024-09-17] [2409.11598v4] Towards Fair RAG: On the Impact of Fair Ranking in Retrieval-Augmented Generation [초록] Despite the central role of retrieval in retrieval-augmented generation (RAG) systems, much of the existing research on RAG overlooks the well-established field of fair ranking and fails to account for the interests of all stakeholders involved. In this paper, we conduct the first systematic evaluation of RAG systems that integrate fairness-aware rankings, addressing both ranking fairness and attribution fairness, which ensures equitable exposure of the sources cited in the generated content. Ou
=== 답
<b>서론</b>
제공된 문서들은 모두 <b>RAG 리랭커</b>(또는 랭킹·퓨전)와 관련된 연구들을 다루고 있습니다. 각 논문은 RAG 파이프라인에서 검색 결과 순위를 개선하거나, 다양한 기술 조합을 탐색하는 방법을 제시합니다.

<b>본론</b>
1. <b>Retrieval Fusion Evaluation</b>: 다중 쿼리 및 상호 역 순위 퓨션(RRF)과 같은 리트리벌퓨전 기법을 생산 환경 스타일의 RAG 파이프라인에서 평가했습니다[2603.02153v1].
2. <b>Reranker‑Centric Retrieval Enhancements</b>: 강력한 reranker가 존재할 때, query expansion, hierarchical summarization 등 다양한 검색 향상 방법의 효과를 조사했으며, 기존 연구는 주로 homogeneous corpus에 국한되어 있음을 지적합니다[2606.28367v1].
3. <b>RAGSmith Framework</b>: RAG 설계 전체를 엔드‑투엔드 아키텍처 탐색으로 접근하고, nine 기술 계열과 46 080 가지 파이프라인 구성을 유전 알고리즘으로 최적화하는 모듈러 프레임워크인 RAGSmith를 제안했습니다[2511.01386v1].
4. <b>Hyperparameter Impact Analysis</b>: Chroma와 Faiss 벡터 스토어, chunking 정책, cross‑encoder re-ranking 및 temperature 등 하이퍼파라미터가 속도·품질에 미치는 영향을 분석하고 six 가지 메트릭(faithfulness, answer correctness 등을 포함)을 평가했습니다[2505.08445v1].
5. <b>Fair Ranking Integration</b>: RAG 시스템에서 공정성 인식 랭킹(first systematic evaluation of fairness‑aware rankings in RAG)이 ranking 및 attribution 공정을 동시에 고려한다는 점을 강조합니다[2409.11598v4].

<b>결론</b>
각 연구는 리랭커와 관련된 다양한 접근을 제시하지만, 초점이 다릅니다: [2603.02153v1]은 생산 환경에서의 퓨전 기법 평가에 집중하고, [2606.28367v1]·3에서는 reranker 중심의 향상 방법과 전체 파이프라인 최적화를 탐색하며, [2505.08445v1]는 하이퍼파라미터가 성능/효율성에 미치는 영향을 정량화합니다. 반면 [2409.11598v4]는 공정성이라는 새로운 차원에서 랭킹을 다루어 기존 연구와 차별화된 목표를 설정하고 있습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• SMART-RAG: Selection using Determinantal Matrices for Augmented Retrieval (2024) [2409.13992]
• Are Re-Ranking in Retrieval-Augmented Generation Methods Impactful for Small Agriculture QA Datasets? A Small Experiment (2025) https://doi.org/10.1051/bioconf/202516701001
• Domain-Specific Retrieval-Augmented Generation with Adaptive Embedding and Knowledge Distillation-Based Re-Ranking (2025) https://doi.org/10.3390/pr14010099
• Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks (2026) [2407.21059]

######## K04 | LLM 탈옥 방어 논문 6개 찾아줘 | route direct_answer/B
  조건 0: 편수: 6편
--- [문서 1] [Distance: 0.2269] [발행일: 2024-06-26] [2406.18122v1] Poisoned LangChain: Jailbreak LLMs by LangChain [초록] With the development of natural language processing (NLP), large language models (LLMs) are becoming increasingly popular. LLMs are integrating more into everyday life, raising public concerns about their security vulnerabilities. Consequently, the security of large language models is becoming critically important. Currently, the techniques for attacking and defending against LLMs are continuously evolving. One significant method type of attack is the jailbreak attack, which designed to evade mo
--- [문서 2] [Distance: 0.2365] [발행일: 2024-12-13] [2412.12192v1] No Free Lunch for Defending Against Prefilling Attack by In-Context Learning [초록] The security of Large Language Models (LLMs) has become an important research topic since the emergence of ChatGPT. Though there have been various effective methods to defend against jailbreak attacks, prefilling attacks remain an unsolved and popular threat against open-sourced LLMs. In-Context Learning (ICL) offers a computationally efficient defense against various jailbreak attacks, yet no effective ICL methods have been developed to counter prefilling attacks. In this paper, we: (1) show th
--- [문서 3] [Distance: 0.2284] [발행일: 2025-05-18] [2505.13527v2] Logic Jailbreak: Efficiently Unlocking LLM Safety Restrictions Through Formal Logical Expression [초록] Despite substantial advancements in aligning large language models (LLMs) with human values, current safety mechanisms remain susceptible to jailbreak attacks. We hypothesize that this vulnerability stems from distributional discrepancies between alignment-oriented prompts and malicious prompts. To investigate this, we introduce LogiBreak, a novel and universal black-box jailbreak method that leverages logical expression translation to circumvent LLM safety systems. By converting harmful natural
--- [문서 4] [Distance: 0.2381] [발행일: 2025-12-30] [2512.24044v1] Jailbreaking Attacks vs. Content Safety Filters: How Far Are We in the LLM Safety Arms Race? [초록] As large language models (LLMs) are increasingly deployed, ensuring their safe use is paramount. Jailbreaking, adversarial prompts that bypass model alignment to trigger harmful outputs, present significant risks, with existing studies reporting high success rates in evading common LLMs. However, previous evaluations have focused solely on the models, neglecting the full deployment pipeline, which typically incorporates additional safety mechanisms like content moderation filters. To address thi
--- [문서 5] [Distance: 0.2536] [발행일: 2025-01-31] [2501.18837v1] Constitutional Classifiers: Defending against Universal Jailbreaks across Thousands of Hours of Red Teaming [초록] Large language models (LLMs) are vulnerable to universal jailbreaks-prompting strategies that systematically bypass model safeguards and enable users to carry out harmful processes that require many model interactions, like manufacturing illegal substances at scale. To defend against these attacks, we introduce Constitutional Classifiers: safeguards trained on synthetic data, generated by prompting LLMs with natural language rules (i.e., a constitution) specifying permitted and restricted conten
--- [문서 6] [Distance: 0.1934] [발행일: 2024-12-19] [2412.15289v5] SATA: A Paradigm for LLM Jailbreak via Simple Assistive Task Linkage [초록] Large language models (LLMs) have made significant advancements across various tasks, but their safety alignment remain a major concern. Exploring jailbreak prompts can expose LLMs' vulnerabilities and guide efforts to secure them. Existing methods primarily design sophisticated instructions for the LLM to follow, or rely on multiple iterations, which could hinder the performance and efficiency of jailbreaks. In this work, we propose a novel jailbreak paradigm, Simple Assistive Task Linkage (SAT
--- [문서 7] [Distance: 0.2365] [발행일: 2024-06-09] [2406.05644v2] How Alignment and Jailbreak Work: Explain LLM Safety through Intermediate Hidden States [초록] Large language models (LLMs) rely on safety alignment to avoid responding to malicious user inputs. Unfortunately, jailbreak can circumvent safety guardrails, resulting in LLMs generating harmful content and raising concerns about LLM safety. Due to language models with intensive parameters often regarded as black boxes, the mechanisms of alignment and jailbreak are challenging to elucidate. In this paper, we employ weak classifiers to explain LLM safety through the intermediate hidden states. W
--- [문서 8] [Distance: 0.2334] [발행일: 2025-11-09] [2511.07480v1] KG-DF: A Black-box Defense Framework against Jailbreak Attacks Based on Knowledge Graphs [초록] With the widespread application of large language models (LLMs) in various fields, the security challenges they face have become increasingly prominent, especially the issue of jailbreak. These attacks induce the model to generate erroneous or uncontrolled outputs through crafted inputs, threatening the generality and security of the model. Although existing defense methods have shown some effectiveness, they often struggle to strike a balance between model generality and security. Excessive def
--- [문서 9] [Distance: 0.2121] [발행일: 2024-12-20] [2412.15623v1] JailPO: A Novel Black-box Jailbreak Framework via Preference Optimization against Aligned LLMs [초록] Large Language Models (LLMs) aligned with human feedback have recently garnered significant attention. However, it remains vulnerable to jailbreak attacks, where adversaries manipulate prompts to induce harmful outputs. Exploring jailbreak attacks enables us to investigate the vulnerabilities of LLMs and further guides us in enhancing their security. Unfortunately, existing techniques mainly rely on handcrafted templates or generated-based optimization, posing challenges in scalability, efficien
--- [문서 10] [Distance: 0.2185] [발행일: 2026-03-28] [2603.28817v1] GUARD-SLM: Token Activation-Based Defense Against Jailbreak Attacks for Small Language Models [초록] Small Language Models (SLMs) are emerging as efficient and economically viable alternatives to Large Language Models (LLMs), offering competitive performance with significantly lower computational costs and latency. These advantages make SLMs suitable for resource-constrained and efficient deployment on edge devices. However, existing jailbreak defenses show limited robustness against heterogeneous attacks, largely due to an incomplete understanding of the internal representations across differe
=== 답
<b>서론</b>
LLM 탈옥(제일브레이크) 공격은 모델 안전성을 위협하는 주요 문제이며, 이를 방어하기 위한 다양한 연구가 진행되고 있습니다. 본 요약에서는 <b>탈옥</b> 방어를 주제로 한 6편의 논문을 정리합니다.

<b>본론</b>
1. <b>Poisoned LangChain</b>: Jailbreak LLMs by Poisoning the Chain of Thought [2406.18122v1]
2. <b>No Free Lunch for Defending Against Prefilling Attack via In-Context Learning (ICL)</b>: ICL은 다양한 jailbreak 공격에 대해 계산 효율적인 방어를 제공하지만, prefilling 공격에는 아직 효과적인 방법이 개발되지 않았다[2412.12192v1].
3. <b>LogiBreak</b>: 논리적 표현 번역을 이용해 LLM 안전 시스템을 우회하는 블랙박스 탈옥 방법을 제안한다[2505.13527v2].
4. <b>Jailbreaking Attacks vs. Content Safety Filters</b>: 기존 평가는 모델 자체에만 집중하여 콘텐츠 필터링 등 전체 파이프라인의 방어를 고려하지 않았다며, 추가적인 안전 메커니즘이 필요함을 강조한다[2512.24044v1].
5. <b>Constitutional Classifiers</b>: 합성 데이터를 이용해 자연어 규칙(헌법)을 학습한 분류기를 통해 범용 탈옥 공격에 대한 방어 모델을 제안한다[2501.18837v1].

<b>결론</b>
제공된 문서들은 LLM 안전성을 위협하는 다양한 탈옥 기법에 대응하기 위해 모델 내부 구조 활용, 논리적 표현 변환, 콘텐츠 필터링 통합 및 합성 데이터 기반 규칙 학습 등 다각적인 접근법을 제시하고 있습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• Withdrawn: Optimizing Safety Alignment and Jailbreak Defense for Large Language Models (2025) https://doi.org/10.20944/preprints202511.1521.v1
• Jailbreak Attacks and Defenses Against Large Language Models: A Survey (2024) [2407.04295]
• JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models (2024) [2404.01318]
• LLM-Virus: Evolutionary Jailbreak Attack on Large Language Models (2024) [2501.00055]

######## K05 | 2026년에 나온 RAG 평가 논문들 정리해줘 | route direct_answer/B
  조건 0: 기간: 2026년 발행
--- [문서 1] [Distance: 0.4199] [발행일: 2026-02-25] [2602.21553v1] Revisiting RAG Retrievers: An Information Theoretic Benchmark [초록] Retrieval-Augmented Generation (RAG) systems rely critically on the retriever module to surface relevant context for large language models. Although numerous retrievers have recently been proposed, each built on different ranking principles such as lexical matching, dense embeddings, or graph citations, there remains a lack of systematic understanding of how these mechanisms differ and overlap. Existing benchmarks primarily compare entire RAG pipelines or introduce new datasets, providing little
--- [문서 2] [Distance: 0.3361] [발행일: 2025-08-08] [2508.06401v3] A Systematic Literature Review of Retrieval-Augmented Generation: Techniques, Metrics, and Challenges [초록] This systematic review of the research literature on retrieval-augmented generation (RAG) provides a focused analysis of the most highly cited studies published between 2020 and May 2025. A total of 128 articles met our inclusion criteria. The records were retrieved from ACM Digital Library, IEEE Xplore, Scopus, ScienceDirect, and the Digital Bibliography and Library Project (DBLP). RAG couples a neural retriever with a generative language model, grounding output in up-to-date, non-parametric me
--- [문서 3] [Distance: 0.3682] [발행일: 2024-12-16] [2412.12322v1] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems [초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical results comparing different language models (Llama 3.1 and Qwen 2.5) across various r
--- [문서 4] [Distance: 0.3454] [발행일: 2024-05-31] [2406.04369v1] RAG Does Not Work for Enterprises [초록] Retrieval-Augmented Generation (RAG) improves the accuracy and relevance of large language model outputs by incorporating knowledge retrieval. However, implementing RAG in enterprises poses challenges around data security, accuracy, scalability, and integration. This paper explores the unique requirements for enterprise RAG, surveys current approaches and limitations, and discusses potential advances in semantic search, hybrid queries, and optimized retrieval. It proposes an evaluation framework
--- [문서 5] [Distance: 0.2512] [발행일: 2024-05-13] [2405.07437v2] Evaluation of Retrieval-Augmented Generation: A Survey [초록] Retrieval-Augmented Generation (RAG) has recently gained traction in natural language processing. Numerous studies and real-world applications are leveraging its ability to enhance generative models through external information retrieval. Evaluating these RAG systems, however, poses unique challenges due to their hybrid structure and reliance on dynamic knowledge sources. To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehe
--- [문서 6] [Distance: 0.3213] [발행일: 2024-06-25] [2407.11005v2] RAGBench: Explainable Benchmark for Retrieval-Augmented Generation Systems [초록] Retrieval-Augmented Generation (RAG) has become a standard architectural pattern for incorporating domain-specific knowledge into user-facing chat applications powered by Large Language Models (LLMs). RAG systems are characterized by (1) a document retriever that queries a domain-specific corpus for context information relevant to an input query, and (2) an LLM that generates a response based on the provided query and context. However, comprehensive evaluation of RAG systems remains a challenge
--- [문서 7] [Distance: 0.2820] [발행일: 2025-07-26] [2508.05650v1] OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools [초록] While Retrieval Augmented Generation (RAG) is now widely adopted to enhance LLMs, evaluating its true performance benefits in a reproducible and interpretable way remains a major hurdle. Existing methods often fall short: they lack domain coverage, employ coarse metrics that miss sub document precision, and fail to capture computational trade offs. Most critically, they provide no standardized framework for comparing RAG effectiveness across different models and domains. We introduce OmniBench R
--- [문서 8] [Distance: 0.3217] [발행일: 2024-12-16] [2412.12300v3] Unanswerability Evaluation for Retrieval Augmented Generation [초록] Existing evaluation frameworks for retrieval-augmented generation (RAG) systems focus on answerable queries, but they overlook the importance of appropriately rejecting unanswerable requests. In this paper, we introduce UAEval4RAG, a framework designed to evaluate whether RAG systems can handle unanswerable queries effectively. We define a taxonomy with six unanswerable categories, and UAEval4RAG automatically synthesizes diverse and challenging queries for any given knowledge base with unanswer
--- [문서 9] [Distance: 0.5472] [발행일: 2025-11-10] [2601.07838v1] A survey: Information search time optimization based on RAG (Retrieval Augmentation Generation) chatbot [초록] Retrieval-Augmented Generation (RAG) based chatbots are not only useful for information retrieval through questionanswering but also for making complex decisions based on injected private data.we present a survey on how much search time can be saved when retrieving complex information within an organization called "X Systems"(a stealth mode company) by using a RAG-based chatbot compared to traditional search methods. We compare the information retrieval time using standard search techniques vers
--- [문서 10] [Distance: 0.2872] [발행일: 2023-12-18] [2312.10997v5] Retrieval-Augmented Generation for Large Language Models: A Survey [초록] Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes. Retrieval-Augmented Generation (RAG) has emerged as a promising solution by incorporating knowledge from external databases. This enhances the accuracy and credibility of the generation, particularly for knowledge-intensive tasks, and allows for continuous knowledge updates and integration of domain-specific informati
=== 답
<b>서론</b>
2026년에 발표된 RAG 평가 연구들은 주로 새로운 벤치마크와 체계적인 비교 프레임워크를 제시하며, 기존 파이프라인이나 데이터셋 중심 접근법의 한계를 보완하려는 시도를 보여줍니다. 이러한 논문들은 정보 이론적 기준과 다중 도메인 평가를 통해 retriever의 성능을 정량화하고 설명 가능성을 강조합니다.

<b>본론</b>
1. <b>Revisiting RAG Retrievers: An Information Theoretic Benchmark</b>: 이 연구는 기존 벤치마크가 전체 파이프라인이나 새 데이터셋에 집중한다는 점을 지적하며, 다양한 ranking 원리(lexical matching, dense embeddings 등) 가 어떻게 달라지는지에 대한 체계적 이해의 부족을 강조합니다. [2602.21553v1]
2. <b>A Systematic Literature Review of Retrieval-Augmented Generation: Techniques, Metrics, and Challenges</b>: 이 리뷰는 2020년 ~ 2025년까지 가장 많이 인용된 RAG 연구를 대상으로 분석하고, 총 128편의 논문을 ACM Digital Library 등 데이터베이스에서 수집했습니다. [2508.06401v3]
3. <b>RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems</b>: 이 프레임워크는 naive vector search, reranking, hybrid vector‑keyword 검색을 구현하고 ReAct agents와 다양한 프롬프트 전략으로 비교하며 새로운 평가 지표도 도입합니다. [2412.12322v1]
4. <b>RAG Does Not Work for Enterprises</b>: 기업 환경에서 데이터 보안·정확성·확장성·통합 문제를 다루며, 현재 접근법의 한계를 조사하고 semantic search 및 hybrid query 등을 활용한 잠재적 진전을 논의한 후 평가를 위한 프레임워크를 제안합니다. [2406.04369v1]
5. <b>Evaluation of Retrieval-Augmented Generation: A Survey</b>: RAG의 하이브리드 구조와 동적인 지식 소스에 기반해 평가가 어려운 점을 강조하며, Unified Evaluation Process (Auepora) 를 통해 포괄적 이해에 기여한다고 명시합니다. [2405.07437v2]
6. <b>RAGBench: Explainable Benchmark for Retrieval-Augmented Generation Systems</b>: 문서 retriever 와 LLM이 결합된 RAG 시스템의 전반적인 평가를 어렵다는 문제를 제시하고, 설명 가능한 벤치마크를 목표로 합니다. [2407.11005v2]
7. <b>OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools</b>: 기존 평가가 도메인 범위를 제한하거나 정밀한 서브‑도큐먼트 정확도를 놓친다는 점을 지적하고, 다중 도메인과 모델 간 표준화된 비교 프레임워크를 제공합니다. [2508.05650v1]
8. <b>Unanswerability Evaluation for Retrieval Augmented Generation</b>: UAEval4RAG라는 새로운 평가 프레임을 도입하여 RAG가 unanswerable query 를 효과적으로 처리하는지를 검증하며, six 가지 unanswerable 카테고리를 정의하고 자동 생성된 복잡한 쿼리로 테스트합니다. [2412.12300v3]
9. <b>A survey: Information search time optimization based on RAG (Retrieval Augmentation Generation) chatbot<

######## K06 | 2025년 이후 나온 LLM 양자화 논문만 알려줘 | route direct_answer/B
  조건 0: 기간: 2025년 이후 발행만
--- [문서 1] [Distance: 0.3871] [발행일: 2025-11-17] [2511.13023v1] SLMQuant:Benchmarking Small Language Model Quantization for Practical Deployment [초록] Despite the growing interest in Small Language Models (SLMs) as resource-efficient alternatives to Large Language Models (LLMs), their deployment on edge devices remains challenging due to unresolved efficiency gaps in model compression. While quantization has proven effective for LLMs, its applicability to SLMs is significantly underexplored, with critical questions about differing quantization bottlenecks and efficiency profiles. This paper introduces SLMQuant, the first systematic benchmark for evaluating LLM compression techniques when applied t
--- [문서 2] [Distance: 0.3174] [발행일: 2026-06-20] [2606.22249v1] On the Expressive Power of Weight Quantization in Large Language Models [초록] In recent years, weight quantization that encodes the learnable parameters of large language models in an $n$-bit format has garnered significant attention due to its potential for model compression and inference acceleration. Many practical techniques have been developed; however, the theoretical understanding of many aspects, especially the approximation and degradation of expressive power as the number of quantization bits decreases, remains unclear. In this paper, we provide a theoretical investigation into the expressive capability of large language mod
--- [문서 3] [Distance: 0.3878] [발행일: 2025-06-23] [2506.18879v1] CommVQ: Commutative Vector Quantization for KV Cache Compression [초록] Large Language Models (LLMs) are increasingly used in applications requiring long context lengths, but the key-value (KV) cache often becomes a memory bottleneck on GPUs as context grows. To address this, we propose Commutative Vector Quantization (CommVQ) to significantly reduce memory usage for long-context LLM inference. We first introduce additive quantization with a lightweight encoder and codebook to compress the KV cache, which can be decoded via simple matrix multiplication. To further reduce computational costs during decoding, we design the codebook to be
--- [문서 4] [Distance: 0.4119] [발행일: 2025-03-29] [2504.03717v2] RaanA: A Fast, Flexible, and Data-Efficient Post-Training Quantization Algorithm [초록] Post-training Quantization (PTQ) has become a widely used technique for improving inference efficiency of large language models (LLMs). However, existing PTQ methods generally suffer from crucial limitations such as heavy calibration data requirements and inflexible choice of target number of bits. In this paper, we propose RaanA, a unified PTQ framework that overcomes these challenges by introducing two novel components: 1) RaBitQ-H, a variant of a randomized vector quantization method RaBitQ, designed for fast, accurate, and highly efficient quant
--- [문서 5] [Distance: 0.3686] [발행일: 2026-07-08] [2607.07964v2] KronQ: LLM Quantization via Kronecker-Factored Hessian [초록] Post-training quantization (PTQ) is a widely adopted technique for compressing large language models (LLMs) without retraining. Most existing second-order PTQ methods, including GPTQ, construct quantization objectives from input activation statistics, effectively assuming that all output channels contribute equally to the layer-wise reconstruction objective. We propose KronQ, a PTQ framework that challenges this assumption by introducing the gradient covariance into the quantization pipeline. Under the Kronecker-factored Hessian approximation, the quantization loss depends j
=== 답
<b>서론</b>
2025년 이후 발표된 <b>LLM 양자화</b> 연구는 모델 압축과 추론 속도를 높이는 동시에 정확도 손실을 최소화하는 방법을 탐구합니다. 이러한 작업은 다양한 정밀도와 구조에 대한 이론적 한계와 실용적인 구현 문제를 해결해야 하므로 어려운 과제입니다.

<b>본론</b>
1. <b>SLMQuant</b>: 소규모 언어 모델(SLM) 에 적용된 양자화 기법을 체계적으로 벤치마크하고, LLM‑최적화된 기술이 SLM에서 비효율적이 되는 원인을 분석합니다[2511.13023v1].
2. <b>KronQ</b>: 크로네커 팩터링 헤시안을 활용해 입력·출력 차원의 활성화와 그래디언트 공분산을 동시에 고려한 양자화 손실을 정의하고, 기존 GPTQ보다 낮은 퍼플렉시티를 달성하는 PTQ 프레임워크입니다[2607.07964v2].
3. <b>RaBitA</b>: 랜덤 벡터 양자화를 변형해 빠른 정확도 높은 양자화와 최소 교정 데이터를 요구하며, 레이어별 민감도에 따라 비트 폭을 최적화할 수 있는 통합 PTQ 알고리즘인 RaanA를 제안합니다[2504.03717v2].

<b>결론</b>
제공된 문서들은 2025년 이후 발표된 LLM 양자화 연구들을 다루고 있으며, 각각의 결과가 서로 다른 초점을 가지고 있음을 보여줍니다. 먼저 SLMQuant는 소규모 언어 모델(SLM)에 대한 양자화 민감도 차이와 기존 LLM 최적화 기법의 직접 적용 한계를 강조합니다[2511.13023v1]. 다음으로 RaanA는 빠른 속도와 최소 교정 데이터 요구를 통해 효율성과 정확성을 균형 있게 달성한다는 점을 제시합니다[2504.03717v2]. 마지막으로 KronQ는 크로네커-팩터드 헤시안을 활용한 양자화 방법과 새로운 민감도 메트릭을 도입하여 혼합 정밀도 할당에 대한 통찰을 제공합니다[2607.07964v2]. 따라서 이 세 논문은 모두 LLM 양자화의 효율성 향상에 기여하지만, 각각 SLM 특화 평가, 빠른 PTQ 알고리즘, 그리고 헤시안 기반 민감도 분석이라는 서로 다른 연구 목표와 방법론을 가지고 있어 결과의 초점이 다릅니다.

######## K07 | 2024년 이전 연합학습 논문 중 통신 효율화 다룬 거 알려줘 | route direct_answer/B
  조건 0: 기간: 2024년 이전 발행
  조건 1: 주제: 통신 효율화
--- [문서 1] [Distance: 0.2657] [발행일: 2024-12-15] [2412.11207v1] ProFe: Communication-Efficient Decentralized Federated Learning via Distillation and Prototypes [초록] Decentralized Federated Learning (DFL) trains models in a collaborative and privacy-preserving manner while removing model centralization risks and improving communication bottlenecks. However, DFL faces challenges in efficient communication management and model aggregation within decentralized environments, especially with heterogeneous data distributions. Thus, this paper introduces ProFe, a novel communication optimization algorithm for DFL that combines knowledge distillation, prototype learning, and quantization techniques. ProFe
--- [문서 2] [Distance: 0.2880] [발행일: 2024-06-27] [2406.19050v1] FedMap: Iterative Magnitude-Based Pruning for Communication-Efficient Federated Learning [초록] Federated Learning (FL) is a distributed machine learning approach that enables training on decentralized data while preserving privacy. However, FL systems often involve resource-constrained client devices with limited computational power, memory, storage, and bandwidth. This paper introduces FedMap, a novel method that aims to enhance the communication efficiency of FL deployments by collaboratively learning an increasingly sparse global model through iterative, unstructured pruning. Importantly, FedMap trains a global model from scratch, 
=== 답
<b>서론</b>
연합학습(FL)은 분산된 데이터를 이용해 모델을 학습시키지만, <b>통신 비용</b>과 제한된 클라이언트 자원을 효율적으로 관리하는 것이 핵심 과제입니다. 특히 통신 라운드마다 전송해야 하는 데이터 양을 줄이는 방법이 연구되고 있습니다.

<b>본론</b>
1. <b>ProFe</b>: 지식 증류와 프로토타입 학습에 정량화를 결합해 DFL 환경에서 모델 집계 시 필요한 데이터를 40‑50%까지 감소시키며, MNIST·CIFAR10·CIFAR100 벤치마크를 통해 성능을 유지하거나 향상시켰습니다. [2412.11207v1]
2. <b>FedMap</b>: 반복적인 크기 기반 가지름(iterative magnitude-based pruning)으로 글로벌 모델을 점진적으로 희소화시켜 통신 오버헤드를 크게 낮추고, IID 환경에서는 최대 90% 이상 모델 크기를 줄이면서도 성능 저하를 최소화합니다. [2406.19050v1]

<b>결론</b>
ProFe는 통신 비용을 최대 약 40~50% 감소시키며 모델 성능을 유지하거나 향상시킨 반면, 학습 시간이 약 20% 증가하는 트레이드오프를 보인다고 보고합니다 [2412.11207v1]. FedMap은 비IID 환경에서 최소 약 80%의 가지치기를 달성하면서도 정확도를 유지한다는 결과를 제시합니다 [2406.19050v1]. 두 논문 모두 통신 효율성을 높이는 데 성공했으나, ProFe는 전체적인 비용 절감과 성능 유지에 초점을 둔 반면, FedMap은 비균일 데이터 조건에서도 높은 가지치 비율을 달성하는 데 특화되어 있습니다.

######## K08 | 의료 데이터로 실험한 환각 탐지 연구 알려줘 | route direct_answer/B
  조건 0: 도메인: 의료 데이터 실험
--- [문서 1] [Distance: 0.2732] [발행일: 2024-08-28] [2408.15533v3] LRP4RAG: Detecting Hallucinations in Retrieval-Augmented Generation via Layer-wise Relevance Propagation [초록] Retrieval-Augmented Generation (RAG) has become a primary technique for mitigating hallucinations in large language models (LLMs). However, incomplete knowledge extraction and insufficient understanding can still mislead LLMs to produce irrelevant or even contradictory responses, which means hallucinations persist in RAG. In this paper, we propose LRP4RAG, a method based on the Layer-wise Relevance Propagation (LRP) algorithm for detecting hallucinations in RAG. Specifically, we first utilize LRP to compute the relevance betw
--- [문서 2] [Distance: 0.2801] [발행일: 2025-06-11] [2506.09886v2] Probabilistic distances-based hallucination detection in LLMs with RAG [초록] Detecting hallucinations in large language models (LLMs) is critical for their safety in many applications. Without proper detection, these systems often provide harmful, unreliable answers. In recent years, LLMs have been actively used in retrieval-augmented generation (RAG) settings. However, hallucinations remain even in this setting, and while numerous hallucination detection methods have been proposed, most approaches are not specifically designed for RAG systems. To overcome this limitation, we introduce a hallucination detection method based on estimat
--- [문서 3] [Distance: 0.3248] [발행일: 2026-06-04] [2606.06748v2] Evidence Graph Consistency in Retrieval-Augmented Generation: A Model-Dependent Analysis of Hallucination Detection [초록] Retrieval-Augmented Generation (RAG) reduces but does not eliminate hallucination in large language models. Existing detection methods rely on flat similarity between generated answers and retrieved passages, ignoring structural relationships among evidence pieces and answer claims. We propose Evidence Graph Consistency (EGC), a framework that constructs a local evidence graph per response and computes five structural consistency measures as hallucination indicators. Evaluated on the full question answering split o
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
의료 데이터를 이용한 환각 탐지 실험에 대한 내용은 제공되지 않았습니다.

<b>본론</b>
1. <b>LRP4RAG</b>: 레이어별 관련성 전파(LRP) 알고리즘을 이용해 RAG 생성기의 입력‑출력 간 관련성을 계산하고, 해당 행렬에서 추가 추출·재샘플링 후 여러 분류기에 넣어 환각 유무를 판단한다[2408.15533v3].
2. <b>Probabilistic distances-based hallucination detection</b>: 프롬프트 토큰 임베딩과 모델 응답 토크임베딩 사이의 분포 거리를 추정하여 사실성 신호를 추출하고, NLI 작업에서 학습된 방법을 환각 탐지에 전이시켜 완전히 비지도·효율적인 검출기를 제공한다[2506.09886v2].
3. <b>Evidence Graph Consistency (EGC)</b>: 각 응답에 대해 증거 그래프를 구축해 다섯 가지 구조적 일관성 지표를 계산하고, 이를 RAGTruth 데이터셋의 전체 QA 분할에서 Llama‑2와 GPT 계열 모델 간 진단 방향이 달라지는 현상을 관찰한다[2606.06748v2].

<b>결론</b>
제공된 문서들은 모두 RAG 기반 환각 탐지 연구이며, 각각 다른 접근법을 통해 실험 결과를 보고하고 있습니다. [2408.15533v3]은 LRP4RAG가 기존 베이스라인보다 우수한 성능을 보였다고 주장하며, 이는 의료 데이터와 직접적인 관련이 없는 일반적인 RAG 시스템에 대한 평가입니다. [2506.09886v2]는 확률적 거리 기반 방법이 현재 SOTA 또는 경쟁력 있는 성과를 달성했다고 보고하고 있습니다. [2606.06748v2]은 EGC가 Llama-2 모델에서는 기대된 진단 방향을 보이지만, GPT-4·GPT-3.5·Mistral-7B에서는 체계적인 반전을 보인다고 밝히며, 이는 모델 패밀리별로 결과가 갈린다는 점을 시사합니다. 따라서 의료 데이터로 실험한 환각 탐지 연구는 제공된 문서들에 포함되어 있지 않으며, 제시된 논문들은 일반적인 RAG 시스템에서 서로 다른 방법론과 모델별 성능 차이를 보여줍니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• A Comparative Evaluation of Hallucination Detection Methods for RAG Systems (2026) https://openalex.org/W7165432729
• ContextCheck: A Self-Consistency Framework for Hallucination Detection in Retrieval-Augmented Generation Systems (2026) https://doi.org/10.1109/isiber68248.2026.11470068
• Logic Matters in Lightweight Hallucination Classification for RAG System (2026) https://doi.org/10.18653/v1/2026.acl-long.73
• Building a Reliable Retrieval-Augmented Generation (RAG) System with Hallucination Awareness (2026) https://openalex.org/W7203956628

######## K09 | 한국어 데이터셋으로 평가한 LLM 연구 있어? | route direct_answer/B
  조건 0: 도메인: 한국어 데이터셋 평가
--- [문서 1] [Distance: 0.2036] [발행일: 2025-03-29] [2503.22968v5] Redefining Evaluation Standards: A Unified Framework for Evaluating the Korean Capabilities of Language Models [초록] Recent advancements in Korean large language models (LLMs) have driven numerous benchmarks and evaluation methods, yet inconsistent protocols cause up to 10 p.p performance gaps across institutions. Overcoming these reproducibility gaps does not mean enforcing a one-size-fits-all evaluation. Rather, effective benchmarking requires diverse experimental approaches and a framework robust enough to support them. To this end, we introduce HRET (Haerae Evaluation Toolkit), an open-source, registry-based framework that unifies
--- [문서 2] [Distance: 0.3506] [발행일: 2025-03-31] [2503.23730v1] KOFFVQA: An Objectively Evaluated Free-form VQA Benchmark for Large Vision-Language Models in the Korean Language [초록] The recent emergence of Large Vision-Language Models(VLMs) has resulted in a variety of different benchmarks for evaluating such models. Despite this, we observe that most existing evaluation methods suffer from the fact that they either require the model to choose from pre-determined responses, sacrificing open-endedness, or evaluate responses using a judge model, resulting in subjective and unreliable evaluation. In addition, we observe a lack of benchmarks for VLMs in the Korean language, which are necessary as a 
=== 답
<b>서론</b>
한국어 대형 언어 모델(LLM) 을 평가하려면 <b>언어별 특성</b>과 <b>다양한 벤치마크·평가 프로토콜</b>을 동시에 고려해야 합니다. 기존에는 기관마다 다른 기준이 적용되어 성능 격차가 발생했고, 이를 해결하기 위해 일관된 프레임워크가 필요합니다.

<b>본론</b>
1. <b>HRET (Haerae Evaluation Toolkit)</b>: 한국어 LLM 평가를 위한 오픈소스 레지스트리 기반 통합 프레임을 제공합니다. 주요 한국 벤치마크와 여러 추론 백엔드, 다중 방법 평가 및 언어 일관성 강제 기능을 포함하며 모듈식 설계로 새로운 데이터셋·방법을 빠르게 추가할 수 있습니다[2503.22968v5].
2. <b>KOFFVQA</b>: 한국어 시각 질문‑답변(VQA)를 위한 자유형 벤치마크입니다. 이미지와 함께 구성된 275개의 질문에 대해 사전 정의된 규칙에 따라 객관적으로 점수를 매기는 평가 기준을 적용해, 모델의 성능을 신뢰성 있게 측정합니다[2503.23730v1].

<b>결론</b>
제공된 문서들은 모두 한국어 데이터를 활용한 LLM(또는 VLM) 평가 연구임을 보여줍니다. [2503.22968v5]은 한국어 능력 평가를 위한 통합 프레임워크를 제시하고, [2503.23730v1]는 객관적으로 평가된 자유형 VQA 벤치마크인 KOFFVQA를 소개합니다. 따라서 질문처럼 한국어 데이터셋으로 평가한 LLM 연구가 존재하며, 이는 각각 다른 평가 기준과 데이터 유형을 통해 진행되고 있습니다.

######## K10 | 금융 분야에 멀티에이전트 LLM 적용한 연구 정리해줘 | route direct_answer/B
  조건 0: 도메인: 금융 분야
--- [문서 1] [Distance: 0.2394] [발행일: 2024-12-28] [2412.20138v7] TradingAgents: Multi-Agents LLM Financial Trading Framework [초록] Significant progress has been made in automated problem-solving using societies of agents powered by large language models (LLMs). In finance, efforts have largely focused on single-agent systems handling specific tasks or multi-agent frameworks independently gathering data. However, the multi-agent systems' potential to replicate real-world trading firms' collaborative dynamics remains underexplored. TradingAgents proposes a novel stock trading framework inspired by trading firms, featuring LLM
--- [문서 2] [Distance: 0.1626] [발행일: 2024-12-24] [2412.18174v1] INVESTORBENCH: A Benchmark for Financial Decision-Making Tasks with LLM-based Agent [초록] Recent advancements have underscored the potential of large language model (LLM)-based agents in financial decision-making. Despite this progress, the field currently encounters two main challenges: (1) the lack of a comprehensive LLM agent framework adaptable to a variety of financial tasks, and (2) the absence of standardized benchmarks and consistent datasets for assessing agent performance. To tackle these issues, we introduce \textsc{InvestorBench}, the first benchmark specifically designed
--- [문서 3] [Distance: 0.2903] [발행일: 2026-03-09] [2603.08262v1] FinToolBench: Evaluating LLM Agents for Real-World Financial Tool Use [초록] The integration of Large Language Models (LLMs) into the financial domain is driving a paradigm shift from passive information retrieval to dynamic, agentic interaction. While general-purpose tool learning has witnessed a surge in benchmarks, the financial sector, characterized by high stakes, strict compliance, and rapid data volatility, remains critically underserved. Existing financial evaluations predominantly focus on static textual analysis or document-based QA, ignoring the complex realit
=== 답
<b>서론</b>
최근 금융 분야에서 대형 언어 모델(LLM) 기반 다중 에이전트 시스템이 활발히 연구되고 있습니다. 이러한 접근은 단일 에이전트를 넘어 협업적인 거래 환경을 구현하려는 시도로 주목받고 있으며, 다양한 벤치마크와 평가 프레임워크가 개발 중입니다.

<b>본론</b>
1. <b>TradingAgents</b>: LLM을 활용한 새로운 주식 매매 프레임을 제안하고, 실제 트레이딩 회사의 협력 역학을 모방하도록 설계되었습니다. [2412.20138v7]
2. <b>INVESTORBENCH</b>: 금융 의사결정 작업에 적용 가능한 포괄적인 LLM 에이전트 프레임워크와 표준화된 벤치마크를 최초로 도입했습니다. [2412.18174v1]

<b>결론</b>
제공된 문서들은 멀티에이전트 LLM을 금융 분야에 적용한 연구에서 공통적으로 다루는 핵심 과제를 제시하고 있습니다. 먼저, [2412.20138v7]은 다중 에이전트 시스템이 실제 거래 회사의 협력 역학을 재현하는 잠재력이 아직 충분히 탐구되지 않았다고 지적합니다[2412.20138v7]. 또한, [2412.18174v1]는 현재 분야가 다양한 금융 작업에 적용 가능한 포괄적인 LLM 에이전트 프레임워크와 성능 평가를 위한 표준화된 벤치마크 및 일관된 데이터셋이 부족하다는 두 가지 주요 과제를 제시합니다[2412.18174v1]. 따라서 두 논문 모두 멀티에이전트 LLM 기반 금융 연구에서 기술적 구현과 평가 인프라의 부재를 공통된 한계로 파악하고 있습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• Large Language Model Agent in Financial Trading: A Survey (2026) [2408.06361]
• Multi-Agent Large Language Models for Traditional Finance and Decentralized Finance (2025) https://doi.org/10.70393/6a69656173.323634
• Large language models empowered agent-based modeling and simulation: a survey and perspectives (2024) [2312.11970]
• Large Language Model Based Multi-agents: A Survey of Progress and Challenges (2024) https://doi.org/10.24963/ijcai.2024/890

######## K11 | 코드 데이터로 실험한 모델 가지치기 연구 알려줘 | route direct_answer/B
  조건 0: 도메인: 코드 데이터 실험
--- [문서 1] [Distance: 0.3783] [발행일: 2024-12-20] [2412.15921v2] Less is More: Towards Green Code Large Language Models via Unified Structural Pruning [초록] The extensive application of Large Language Models (LLMs) in generative coding tasks has raised concerns due to their high computational demands and energy consumption. Unlike previous structural pruning methods designed for classification models that deal with lowdimensional classification logits, generative Code LLMs produce high-dimensional token logit sequences, making traditional pruning objectives inherently limited. Moreover, existing single component pruning approaches further constrain the effectiveness when applied to generative Code 
--- [문서 2] [Distance: 0.4888] [발행일: 2024-12-24] [2412.18110v1] SlimGPT: Layer-wise Structured Pruning for Large Language Models [초록] Large language models (LLMs) have garnered significant attention for their remarkable capabilities across various domains, whose vast parameter scales present challenges for practical deployment. Structured pruning is an effective method to balance model performance with efficiency, but performance restoration under computational resource constraints is a principal challenge in pruning LLMs. Therefore, we present a low-cost and fast structured pruning method for LLMs named SlimGPT based on the Optimal Brain Surgeon framework. We propose Batched Greedy Pruning for r
=== 답
<b>서론</b>
코드 생성 작업을 위한 <b>Large Language Model (LLM)</b> 을 가지치기할 때, 기존 구조적 가지치기는 분류 모델에 최적화되어 있어 고차원 토큰 로짓 시퀀스를 다루는 코드 LLM에는 한계가 있다. 또한 일반적인 감독 기반 미세조정만으로는 도메인 특성에 맞는 성능 회복이 어렵다.

<b>본론</b>
1. <b>Flab-Pruner</b>: 단어 사전, 레이어 및 FFN을 통합적으로 가지치기하고, 코딩 작업에 맞춰 데이터 전략을 설계해 모델 파라미터를 22% 감소시키면서도 원래 성능의 97% 를 유지한다[2412.15921v2].
2. <b>SlimGPT</b>: Optimal Brain Surgeon 기반 Batched Greedy Pruning과 Dynamic Group Size로 FFN 효율성을 높이고, 레이어별 가지치기 한계를 보완하기 위해 Incremental Pruning Ratio를 도입해 성능 저하를 감소시킨다[2412.18110v1].

<b>결론</b>
Flab-Pruner는 코드 생성 작업에서 파라미터를 22% 가지치기해도 원래 성능의 97%를 유지하며, 후학습을 통해 동일한 또는 더 나은 성능을 달성한다는 결과를 보여준다[2412.15921v2]. 반면 SlimGPT는 LLaMA 벤치마크에서 모델 크기를 50% 줄였으며, 다른 방법들보다 우수한 성능을 기록하고 상태-of-the-art 결과를 달성했다는 점을 입증한다[2412.18110v1]. 두 연구 모두 코드와 일반 언어 모델이라는 대상에 따라 각각의 데이터셋과 평가 조건에서 높은 성능 유지율을 보이지만, 구체적인 수치와 적용 범위는 다르다.

######## K12 | 추가 학습 없이 LLM 환각을 줄인 방법 알려줘 | route direct_answer/B
  조건 0: 제약: 추가 학습 없음
--- [문서 1] [Distance: 0.3094] [발행일: 2025-08-19] [2508.14314v2] Zero-knowledge LLM hallucination detection and mitigation through fine-grained cross-model consistency [초록] Large language models (LLMs) have demonstrated impressive capabilities across diverse tasks, but they remain susceptible to hallucinations--generating content that appears plausible but contains factual inaccuracies. We present Finch-Zk, a black-box framework that leverages fine-grained cross-model consistency to detect and mitigate hallucinations in LLM outputs without requiring external knowledge sources. Finch-Zk introduces two key innovations: 1) a cross-model consistency checking strategy that reveals fine-grained inaccura
=== 답
<b>서론</b>
LLM은 다양한 작업에서 뛰어난 성능을 보이지만, 사실과 다른 내용을 생성하는 <b>환각</b> 현상에 여전히 취약합니다. 이러한 환각은 외부 지식 없이도 모델 내부의 일관성만으로도 감지·완화가 가능해야 하는 어려운 과제입니다.

<b>본론</b>
1. <b>Finch‑Zk</b>: 다수의 모델을 이용해 의미적으로 동등한 프롬프트에 대해 응답을 비교함으로써 미세 수준의 불일치를 발견하고, 문제 있는 구간에 정밀 수정을 적용해 환각을 감지·완화합니다[2508.14314v2].

<b>결론</b>
제공된 문서에는 추가 학습 없이 LLM의 환각을 줄이는 방법으로 <b>Finch‑Zk</b>가 제시되어 있으며, 이 시스템은 외부 지식 없이도 다중 모델 일관성 검사와 정밀 수정으로 환각 감지·완화를 달성합니다.

######## K13 | 사람 라벨 없이 텍스트 임베딩 모델 학습한 연구 알려줘 | route direct_answer/B
  조건 0: 제약: 사람 라벨 없음
--- [문서 1] [Distance: 0.3562] [발행일: 2026-02-17] [2602.15547v2] jina-embeddings-v5-text: Task-Targeted Embedding Distillation [초록] Text embedding models are widely used for semantic similarity tasks, including information retrieval, clustering, and classification. General-purpose models are typically trained with single- or multi-stage processes using contrastive loss functions. We introduce a novel training regimen that combines model distillation techniques with task-specific contrastive loss to produce compact, high-performance embedding models. Our findings suggest that this approach is more effective for training small models than purely contrastive or distillation-based training paradigms a
--- [문서 2] [Distance: 0.2982] [발행일: 2024-03-29] [2403.20327v1] Gecko: Versatile Text Embeddings Distilled from Large Language Models [초록] We present Gecko, a compact and versatile text embedding model. Gecko achieves strong retrieval performance by leveraging a key idea: distilling knowledge from large language models (LLMs) into a retriever. Our two-step distillation process begins with generating diverse, synthetic paired data using an LLM. Next, we further refine the data quality by retrieving a set of candidate passages for each query, and relabeling the positive and hard negative passages using the same LLM. The effectiveness of our approach is demonstrated by the compactness of the Gecko. 
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>jina‑embeddings‑v5</b>: Task‑Targeted Embedding Distillation 방식을 도입해 모델 디스틸레이션과 작업별 대비 손실을 결합한 새로운 학습 절차를 제시한다[2602.15547v2].
2. <b>Gecko</b>: 대형 언어 모델을 이용해 다양한 합성 쌍 데이터를 생성하고, 후보 문서를 검색·재라벨링하는 두 단계의 디스틸레이션을 통해 컴팩트하면서도 강력한 텍스트 임베딩을 제공한다[2403.20327v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• GILE: A Generalized Input-Label Embedding for Text Classification (2019) https://doi.org/10.1162/tacl_a_00259
• Text Classification Using Label Names Only: A Language Model Self-Training Approach (2020) https://doi.org/10.18653/v1/2020.emnlp-main.724
• Unified Contrastive Learning in Image-Text-Label Space (2022) [2204.03610]
• Advancing Vision Without Human Supervision Through Multimodal and Unsupervised Learning (2026) https://doi.org/10.15496/publikation-123016

######## K14 | 강화학습 없이 LLM 추론 능력을 올린 연구 알려줘 | route direct_answer/B
  조건 0: 제약: 강화학습 없음
--- [문서 1] [Distance: 0.2852] [발행일: 2024-12-14] [2412.10827v4] Rethinking Chain-of-Thought from the Perspective of Self-Training [초록] Chain-of-thought (CoT) reasoning has emerged as an effective approach for activating latent capabilities in LLMs. Interestingly, we observe that both CoT reasoning and self-training share the core objective: iteratively leveraging model-generated information to progressively reduce prediction uncertainty. Building on this insight, we propose a novel CoT framework to improve reasoning performance. Our framework integrates two key components: (i) a task-specific prompt module that optimizes the initial reasoning process, and (ii) an adaptive reasoning iteration modu
--- [문서 2] [Distance: 0.3690] [발행일: 2022-01-28] [2201.11903v6] Chain-of-Thought Prompting Elicits Reasoning in Large Language Models [초록] We explore how generating a chain of thought -- a series of intermediate reasoning steps -- significantly improves the ability of large language models to perform complex reasoning. In particular, we show how such reasoning abilities emerge naturally in sufficiently large language models via a simple method called chain of thought prompting, where a few chain of thought demonstrations are provided as exemplars in prompting. Experiments on three large language models show that chain of thought prompting improves performance on a range of arithmetic, commonsense
=== 답
<b>서론</b>
LLM은 복잡한 추론 작업을 수행하기 위해 <b>Chain‑of‑Thought (CoT)</b>와 같은 중간 단계 생성 기법이 널리 사용되고 있습니다. 그러나 기존 CoT는 과다한 사고 과정이나 연속적인 반복 사이의 높은 유사성 등 한계가 존재합니다. 이러한 문제를 해결하면서도 강화학습 없이도 LLM의 추론 능력을 향상시키는 연구가 필요합니다.

<b>본론</b>
1. <b>Task‑specific Prompt Module</b>: 초기 추론 과정을 최적화하기 위해 작업에 특화된 프롬프트 모듈을 도입했습니다[2412.10827v4]. 이전 CoT 접근법의 한계인 과다 사고와 연속 반복 간의 높은 유사성을 해결하도록 동적으로 추론 과정을 정제하는 적응형 반복 모듈을 추가했습니다[2412.10827v4]．
<b>결론</b>
제공된 두 연구는 강화학습 없이도 LLM의 Chain‑of‑Thought 기반 추론 능력을 향상시키는 방법을 제시합니다. 첫 번째 접근은 작업 특화 프롬프트를 통해 초기 사고 흐름을 최적화하고, 두 번째 접근은 적응형 반복 모듈로 기존 CoT 방식이 가지는 과다 사고와 유사성 문제를 완화함으로써 전체적인 성능과 계산 효율성을 크게 개선했습니다.

######## K15 | GPU 없이 CPU만으로 돌아가는 RAG 연구 있어? | route direct_answer/B
  조건 0: 제약: GPU 없이 CPU만
--- [문서 1] [Distance: 0.3716] [발행일: 2025-12-09] [2602.22217v1] RAGdb: A Zero-Dependency, Embeddable Architecture for Multimodal Retrieval-Augmented Generation on the Edge [초록] Retrieval-Augmented Generation (RAG) has established itself as the standard paradigm for grounding Large Language Models (LLMs) in domain-specific, up-to-date data. However, the prevailing architecture for RAG has evolved into a complex, distributed stack requiring cloud-hosted vector databases, heavy deep learning frameworks (e.g., PyTorch, CUDA), and high-latency embedding inference servers. This ``infrastructure bloat'' creates a significant barrier to entry for edge computing, air-gapped environments, and privacy-const
=== 답
<b>서론</b>
제공된 연구는 <b>GPU 없이 CPU만으로 동작하는 RAG</b> 시스템을 제시하고 있습니다. 기존에는 GPU 기반 추론 서버가 필요했지만, 이 접근은 그런 의존성을 제거합니다.

<b>본론</b>
1. <b>RAGdb</b>: 단일 SQLite 컨테이너에 자동 멀티모달 인게스션과 ONNX‑기반 추출을 통합했으며, 하이브리드 스코어링 함수(HSF)를 통해 서브선형 TF-IDF 벡터화와 정확한 부분 문자열 부스팅으로 GPU 추론 없이도 쿼리 시점을 처리합니다. [2602.22217v1]

<b>결론</b>
따라서 질문에서 찾는 “GPU 없이 CPU만으로 돌아가는 RAG 연구”는 <b>RAGdb</b>입니다. 이 시스템은 단일 파일 컨테이너와 하이브리드 스코어링 함수를 통해 GPU 의존성을 없애고, 소비자 노트북(i7‑1165G7)에서도 100 % Recall@1과 높은 인게스션 효율을 달성합니다.

######## K16 | 재학습 없이 LLM 개인정보를 지우는 방법 연구 알려줘 | route direct_answer/B
  조건 0: 제약: 재학습 없음
--- [문서 1] [Distance: 0.2928] [발행일: 2024-06-26] [2406.18221v3] Enhancing Data Privacy in Large Language Models through Private Association Editing [초록] Large language models (LLMs) require a significant redesign in solutions to preserve privacy in data-intensive applications due to their text-generation capabilities. Indeed, LLMs tend to memorize and emit private information when maliciously prompted. In this paper, we introduce Private Association Editing (PAE) as a novel defense approach for private data leakage. PAE is designed to effectively remove Personally Identifiable Information (PII) without retraining the model. Experimental results demonstrate the effectiveness of PAE with respect to
=== 답
<b>서론</b>
대규모 언어 모델(LLM)은 방대한 텍스트 데이터를 학습하므로, 악성 프롬프트에 의해 <b>개인식별정보(PII)</b>를 기억하고 유출할 위험이 존재합니다. 이러한 개인정보 보호 문제는 모델을 재학습하지 않고도 해결해야 하는 기술적 난제입니다.

<b>본론</b>
1. <b>Private Association Editing (PAE)</b>: LLM의 파라미터만 조정하여 memorized private 정보를 제거하는 “one model, k edits” 전략을 도입하고 있습니다[2406.18221v3]. 기존 모델 재학습 없이 PII를 효과적으로 삭제할 수 있으며, 대안적인 베이스라인 방법 대비 실험 결과에서 우수한 성능을 보였습니다.

<b>결론</b>
제공된 문서에 따르면, <b>Private Association Editing (PAE)</b>은 LLM의 파라미터 조정만으로 개인정보를 제거하는 방법으로 제시되어 있습니다[2406.18221v3]. 이는 재학습 없이도 개인정보 유출 위험을 낮추는 핵심 도구로 평가됩니다.

######## K17 | ChainPoll이 환각 탐지에서 얼마나 좋은지 수치로 알려줘 | route direct_answer/B
  조건 0: 수치: ChainPoll 수치
--- [문서 1] [Distance: 0.1783] [발행일: 2023-10-22] [2310.18344v1] Chainpoll: A high efficacy method for LLM hallucination detection [초록] Large language models (LLMs) have experienced notable advancements in generating coherent and contextually relevant responses. However, hallucinations - incorrect or unfounded claims - are still prevalent, prompting the creation of automated metrics to detect these in LLM outputs. Our contributions include: introducing ChainPoll, an innovative hallucination detection method that excels compared to its counterparts, and unveiling RealHall, a refined collection of benchmark datasets to assess hallucination detection metrics from recent studies. While creating RealHa
=== 답
<b>서론</b>
LLM에서 발생하는 <b>환각</b>(hallucination)은 모델이 사실과 다른 내용을 생성하는 현상으로, 이를 자동으로 탐지하기 위한 정량적 지표가 필요합니다. 기존 메트릭들은 정확도나 비용 측면에서 한계가 있어 새로운 평가 방법이 요구됩니다.

<b>본론</b>
1. <b>ChainPoll</b>: RealHall 벤치마크 전반에 걸쳐 모든 항목에서 상위 성능을 보이며 전체 AUROC 0.781의 결과를 달성했습니다[2310.18344v1]. <b>Adherence</b>와 <b>Correctness</b>: ChainPoll이 도입한 두 새로운 지표로, 각각 문서 기반 분석 능력과 논리적 오류를 평가합니다[2310.18344v1]
<b>결론</b>
ChainPoll은 RealHall 벤치마크에서 AUROC 0.781이라는 높은 정확도를 달성하고 기존 메트릭 대비 비용 효율성과 투명성도 향상시켰습니다. 이는 환각 탐지 분야에서 현재 가장 우수한 성능을 보이는 방법임을 의미합니다.

######## K18 | LoRA 원 논문에서 학습 파라미터를 몇 배 줄였다고 했어? | route direct_answer/B
  조건 0: 수치: 파라미터 감소 배수
--- [문서 1] [Distance: 0.3855] [발행일: 2024-12-12] [2412.08946v1] MoSLD: An Extremely Parameter-Efficient Mixture-of-Shared LoRAs for Multi-Task Learning [초록] Recently, LoRA has emerged as a crucial technique for fine-tuning large pre-trained models, yet its performance in multi-task learning scenarios often falls short. In contrast, the MoE architecture presents a natural solution to this issue. However, it introduces challenges such as mutual interference of data across multiple domains and knowledge forgetting of various tasks. Additionally, MoE significantly increases the number of parameters, posing a computational cost challenge. Therefore, in this paper, we propose MoSLD, a mixture-of-shared
--- [문서 2] [Distance: 0.4477] [발행일: 2025-03-29] [2504.03719v2] Towards Symmetric Low-Rank Adapters [초록] In this paper, we introduce Symmetric Low-Rank Adapters, an optimized variant of LoRA with even fewer weights. This method utilizes Low-Rank Symmetric Weight Matrices to learn downstream tasks more efficiently. Traditional LoRA accumulates fine-tuning weights with the original pre-trained weights via a Singular Value Decomposition (SVD) like approach, i.e., model weights are fine-tuned via updates of the form $BA$ (where $B \in \mathbb{R}^{n\times r}$, $A \in \mathbb{R}^{r\times n}$, and $r$ is the rank of the merged weight matrix). In contrast, our approach, named SymLoRA, represents fine-tun
--- [문서 3] [Distance: 0.5618] [발행일: 2025-03-31] [2504.00254v1] ElaLoRA: Elastic & Learnable Low-Rank Adaptation for Efficient Model Fine-Tuning [초록] Low-Rank Adaptation (LoRA) has become a widely adopted technique for fine-tuning large-scale pre-trained models with minimal parameter updates. However, existing methods rely on fixed ranks or focus solely on either rank pruning or expansion, failing to adapt ranks dynamically to match the importance of different layers during training. In this work, we propose ElaLoRA, an adaptive low-rank adaptation framework that dynamically prunes and expands ranks based on gradient-derived importance scores. To the best of our knowledge, ElaLoRA is the first me
--- [문서 4] [Distance: 0.5593] [발행일: 2026-10-06] [2610.08669v1] MemFLoRA: Memory-Floor LoRA for CNN Adaptation at the Edge [초록] On-device learning is necessary when the model encounters user-,sensor-, or environment-specific shifts after deployment. Although parameter-efficient fine-tuning (PEFT) methods, particularly Low-Rank Adaptation (LoRA) variants, enable efficient adaptation at the edge, the limiting resource for Convolutional Neural Network (CNN) adaptation is often not the number of trainable parameters but the activation state that must be retained until the backward pass. This paper introduces Memory-Floor LoRA (MemFLoRA), a low-rank CNN adapter built around a memory-first design princ
=== 답
<b>서론</b>
LoRA는 대규모 사전 학습 모델을 미세 조정할 때 파라미터 업데이트를 제한하는 효율적인 방법이지만, <b>학습 가능한 파라미터 수</b>가 기존 방식에 비해 얼마나 감소했는지 구체적으로 명시된 정보가 필요합니다. 이러한 수치적 비교 없이는 LoRA의 실제 압축 효과를 판단하기 어렵습니다.

<b>본론</b>
1. <b>SymLoRA</b>: Symmetric Low-Rank Adapters를 도입하여 전통적인 $BA$ 형태의 업데이트 대신 스펙트럼 분해($Q\,diag(Λ)\,Q^T$) 를 사용함으로써 미세 조정 가중치를 약 절반으로 줄였습니다. [2504.03719v2]
2. <b>ElaLoRA</b>: 기존 LoRA가 모든 레이어에 고정된 랭크를 적용하는 반면, ElaLoRA는 그래디언트 기반 중요도 점수에 따라 동적으로 랭크를 잘라내거나 확장하여 파라미터 효율성을 높입니다. [2504.00254v1]
3. <b>MemFLoRA</b>: CNN 적응을 위해 메모리‑먼 설계 원칙과 활성화 상태 최소화를 적용해, 전체 미세 조정 대비 저장된 활성 상태를 약 98.5~98.7% 감소시키고 피크 학습 상태를 94.9~97.3% 낮춥니다. [2610.08669v1]

<b>결론</b>
제공된 문서들은 LoRA 원 논문에서 학습 파라미터를 몇 배 줄였는지 구체적으로 언급하고 있지 않습니다. [2504.03719v2]는 대칭형 저랭크 어댑터가 다운스트림 성능에 손실이 거의 없음을 보여줍니다. [2504.00254v1]은 ElaLoRA가 다양한 벤치마크에서 기존 PEFT 방법을 능가하며, 고정된 랭크를 모든 레이어에 적용하는 것이 한계임을 지적합니다. [2610.08669v1]는 MemFLoRA가 풀 파인튜닝 대비 저장 활성화 메모리를 98.5-98.7%, 피크 학습 상태 메모리를 94.9-97.3% 감소시킨다고 보고하지만, 이는 CNN 기반 작업에 대한 결과이며 파라미터 감소 비율을 직접 제시하지는 않습니다. 따라서 제공된 문서들만으로는 LoRA 원 논문에서 학습 파라미터가 몇 배 줄었는지 판단할 수 없습니다.

######## K19 | MobileVLM V2 1.7B가 어느 크기 모델과 비슷한 성능을 냈어? | route direct_answer/B
  조건 0: 수치: 비교 대상 모델 크기
--- [문서 1] [Distance: 0.2674] [발행일: 2024-02-06] [2402.03766v1] MobileVLM V2: Faster and Stronger Baseline for Vision Language Model [초록] We introduce MobileVLM V2, a family of significantly improved vision language models upon MobileVLM, which proves that a delicate orchestration of novel architectural design, an improved training scheme tailored for mobile VLMs, and rich high-quality dataset curation can substantially benefit VLMs' performance. Specifically, MobileVLM V2 1.7B achieves better or on-par performance on standard VLM benchmarks compared with much larger VLMs at the 3B scale. Notably, our 3B model outperforms a large variety of VLMs at the 7B+ scale. Our models will be released at ht
=== 답
<b>서론</b>
MobileVLM V2 1.7B 모델은 소형 파라미터 수에도 불구하고 대형 비전‑언어 모델을 견제할 만큼 높은 성능을 달성해야 하는 것이 핵심 과제입니다. 이러한 목표는 제한된 컴퓨팅 자원과 데이터 효율성을 유지하면서 정확도를 높이는 데서 비롯됩니다.

<b>본론</b>
MobileVLM V2 1.7B: 기존 MobileVLM보다 크게 개선된 비전‑언어 모델 패밀리이며, 표준 벤치마크에서 훨씬 큰 규모인 3 B 스케일의 다른 대형 모델을 견제하거나 동등한 성능을 보입니다[2402.03766v1].

<b>결론</b>
따라서 질문이 찾는 대상은 <b>MobileVLM V2</b>입니다.

######## K20 | ReXTrust의 AUROC가 얼마야? | route planner/C
  조건 0: 수치: AUROC 값
=== 답
(없음)

######## K21 | FlashRerank-XL 논문 핵심 내용 설명해줘 | route direct_answer/B
  조건 0: 이름: FlashRerank-XL
--- [문서 1] [Distance: 0.6434] [발행일: 2024-11-13] [2411.08438v1] Towards Optimizing a Retrieval Augmented Generation using Large Language Model on Academic Data [초록] Given the growing trend of many organizations integrating Retrieval Augmented Generation (RAG) into their operations, we assess RAG on domain-specific data and test state-of-the-art models across various optimization techniques. We incorporate four optimizations; Multi-Query, Child-Parent-Retriever, Ensemble Retriever, and In-Context-Learning, to enhance the functionality and performance in the academic domain. We focus on data retrieval, specifically targeting various study programs at a large technical university. We additionally in
--- [문서 2] [Distance: 0.6440] [발행일: 2024-06-21] [2406.15187v2] UDA: A Benchmark Suite for Retrieval Augmented Generation in Real-world Document Analysis [초록] The use of Retrieval-Augmented Generation (RAG) has improved Large Language Models (LLMs) in collaborating with external data, yet significant challenges exist in real-world scenarios. In areas such as academic literature and finance question answering, data are often found in raw text and tables in HTML or PDF formats, which can be lengthy and highly unstructured. In this paper, we introduce a benchmark suite, namely Unstructured Document Analysis (UDA), that involves 2,965 real-world documents and 29,590 expert-annotated Q&A pairs. We rev
--- [문서 3] [Distance: 0.6468] [발행일: 2025-03-31] [2504.08762v1] InteractiveSurvey: An LLM-based Personalized and Interactive Survey Paper Generation System [초록] The exponential growth of academic literature creates urgent demands for comprehensive survey papers, yet manual writing remains time-consuming and labor-intensive. Recent advances in large language models (LLMs) and retrieval-augmented generation (RAG) facilitate studies in synthesizing survey papers from multiple references, but most existing works restrict users to title-only inputs and fixed outputs, neglecting the personalized process of survey paper writing. In this paper, we introduce InteractiveSurvey - an LLM-based personalized a
--- [문서 4] [Distance: 0.5907] [발행일: 2024-12-30] [2412.20864v1] Enhancing Annotated Bibliography Generation with LLM Ensembles [초록] This work proposes a novel approach to enhancing annotated bibliography generation through Large Language Model (LLM) ensembles. In particular, multiple LLMs in different roles -- controllable text generation, evaluation, and summarization -- are introduced and validated using a systematic methodology to enhance model performance in scholarly tasks. Output diversity among the ensemble that generates text is obtained using different LLM parameters, followed by an LLM acting as a judge to assess relevance, accuracy, and coherence. Responses selected by several combinin
--- [문서 5] [Distance: 0.6118] [발행일: 2025-12-05] [2602.22215v1] Graph Your Way to Inspiration: Integrating Co-Author Graphs with Retrieval-Augmented Generation for Large Language Model Based Scientific Idea Generation [초록] Large Language Models (LLMs) demonstrate potential in the field of scientific idea generation. However, the generated results often lack controllable academic context and traceable inspiration pathways. To bridge this gap, this paper proposes a scientific idea generation system called GYWI, which combines author knowledge graphs with retrieval-augmented generation (RAG) to form an external knowledge base to provide controllable context and trace of inspiration path for LLMs to 
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>UDA</b>: Unstructured Document Analysis (UDA) 벤치마크를 소개하고, 2965개의 실제 문서를 활용해 RAG 기반 솔루션을 평가한다[2406.15187v2].
2. <b>InteractiveSurvey</b>: LLM과 검색 증강 생성(RAG) 을 결합한 인터랙티브 설문지 논문 작성 시스템을 제시하며, 사용자 입력에 따라 중간 구성 요소를 지속적으로 수정할 수 있다[2504.08762v1].

<b>결론</b>
UDA 벤치마크는 2,965개의 실제 문서와 29,590개의 전문가 주석 Q&amp;A 쌍을 포함하며, 데이터 파싱과 검색의 중요성을 강조한다[2406.15187v2]. InteractiveSurvey는 도메인 특화 LLM 미세조정 방식을 통해 설문지 생성 시스템의 내용 품질과 시간 효율성을 평가하고, 기존 방법보다 우수한 성능을 보인다고 보고한다[2504.08762v1]. 두 연구는 각각 문서 분석과 설문지 생성이라는 서로 다른 작업에서 데이터 규모와 평가 지표가 다르지만, 모두 해당 분야의 실제 적용 가능성을 검증한다는 공통점을 가진다.

######## K22 | QuantumRAG 프레임워크가 검색 정확도를 얼마나 올렸어? | route direct_answer/B
  조건 0: 이름: QuantumRAG
  조건 1: 수치: 검색 정확도 향상량
--- [문서 1] [Distance: 0.4051] [발행일: 2025-03-27] [2503.21514v2] Quantitative Evaluation of Quantum/Classical Neural Network Using a Game Solver Metric . These results demonstrate the viability of using gamebased benchmarks for evaluating quantum computing systems and suggest that quantum communication can be incorporated with limited impact on performance, providing a foundation for future hybrid quantum applications.
--- [문서 2] [Distance: 0.3157] [발행일: 2024-12-30] [2501.00135v4] GroverGPT: A Large Language Model with 8 Billion Parameters for Quantum Searching [초록] Quantum computing is an exciting non-Von Neumann paradigm, offering provable speedups over classical computing for specific problems. However, the practical limits of classical simulatability for quantum circuits remain unclear, especially with current noisy quantum devices. In this work, we explore the potential of leveraging Large Language Models (LLMs) to simulate the output of a quantum Turing machine using Grover's quantum circuits, known to provide quadratic speedups over classical counterparts. To this end, we developed GroverGPT, a speciali
--- [문서 3] [Distance: 0.4853] [발행일: 2024-06-28] [2406.19738v2] Batch Entanglement Detection in Parameterized Qubit States using Classical Bandit Algorithms [초록] Entanglement is a key property of quantum states that acts as a resource for a wide range of tasks in quantum computing. Entanglement detection is a key conceptual and practical challenge. Without adaptive or joint measurements, entanglement detection is constrained by no-go theorems (Lu et al. [Phys. Rev. Lett., 116, 230501 (2016)]), necessitating full state tomography. Batch entanglement detection refers to the problem of identifying all entangled states from amongst a set of $K$ unknown states, which finds applications in quantum info
--- [문서 4] [Distance: 0.5136] [발행일: 2025-03-26] [2503.21821v1] PHYSICS: Benchmarking Foundation Models on University-Level Physics Problem Solving [초록] We introduce PHYSICS, a comprehensive benchmark for university-level physics problem solving. It contains 1297 expert-annotated problems covering six core areas: classical mechanics, quantum mechanics, thermodynamics and statistical mechanics, electromagnetism, atomic physics, and optics. Each problem requires advanced physics knowledge and mathematical reasoning. We develop a robust automated evaluation system for precise and reliable validation. Our evaluation of leading foundation models reveals substantial limitations. Even the most advanced 
--- [문서 5] [Distance: 0.4475] [발행일: 2025-03-26] [2503.21815v1] ATP: Adaptive Threshold Pruning for Efficient Data Encoding in Quantum Neural Networks [초록] Quantum Neural Networks (QNNs) offer promising capabilities for complex data tasks, but are often constrained by limited qubit resources and high entanglement, which can hinder scalability and efficiency. In this paper, we introduce Adaptive Threshold Pruning (ATP), an encoding method that reduces entanglement and optimizes data complexity for efficient computations in QNNs. ATP dynamically prunes non-essential features in the data based on adaptive thresholds, effectively reducing quantum circuit requirements while preserving high performance
=== 답
<b>서론</b>
제공된 참고 문서에는 <b>QuantumRAG 프레임워크</b>와 관련된 내용이 없습니다. 따라서 검색 정확도 향상에 대한 구체적인 수치나 결과를 제시할 수 있는 정보는 존재하지 않습니다.

<b>본론</b>
1. <b>PHYSICS</b>: 대학 수준의 물리 문제 해결을 위한 포괄적인 벤치마크를 소개하고, RAG 기반 지식 증강이 성능 개선을 위해 사용된다고 언급합니다[2503.21821v1].
2. <b>GroverGPT</b>: Grover 양자 회로를 활용한 LLM(GroverGPT)은 기존 GPT‑4o보다 높은 정확도(6·10 큐비트 데이터셋에서 거의 100 %, 3~6 큐비트로 학습 시 95% 이상 일반화 성능 등)를 달성했습니다[2501.00135v4].

<b>결론</b>
제공된 문서에는 QuantumRAG 프레임워크에 대한 언급이 없으며, GroverGPT와 PHYSICS 벤치마크의 결과를 다루고 있습니다. 따라서 질문에서 요구한 'QuantumRAG'의 검색 정확도 향상 정도를 판단할 수 없습니다. [2501.00135v4]는 GroverGPT가 97K 양자 검색 인스턴스에서 GPT-4o(45% 정확도)보다 일관되게 우수한 성능을 보였으며, 6·10 큐비트 데이터셋에서는 거의 100% 정확도를 달성했다고 보고합니다. [2503.21821v1]는 물리학 문제 해결 벤치마크에서 o3-mini 모델이 최대 59.9% 정확도만 달성했으며, RAG 기반 지식 증강을 통해 성능 향상이 가능함을 제시하고 있습니다.

######## K23 | HyperKV 캐시 압축 방법이랑 SnapKV 비교해줘 | route direct_answer/B
  조건 0: 이름: HyperKV
  조건 1: 이름: SnapKV
--- [문서 1] [Distance: 0.3387] [발행일: 2025-03-31] [2503.23956v3] AirCache: Activating Inter-modal Relevancy KV Cache Compression for Efficient Large Vision-Language Model Inference [초록] Recent advancements in Large Visual Language Models (LVLMs) have gained significant attention due to their remarkable reasoning capabilities and proficiency in generalization. However, processing a large number of visual tokens and generating long-context outputs impose substantial computational overhead, leading to excessive demands for key-value (KV) cache. To address this critical bottleneck, we propose AirCache, a novel KV cache compression method aimed at accelerating LVLMs inference. This work systematically 
--- [문서 2] [Distance: 0.3588] [발행일: 2025-03-31] [2503.24000v1] Rethinking Key-Value Cache Compression Techniques for Large Language Model Serving [초록] Key-Value cache (\texttt{KV} \texttt{cache}) compression has emerged as a promising technique to optimize Large Language Model (LLM) serving. It primarily decreases the memory consumption of \texttt{KV} \texttt{cache} to reduce the computation cost. Despite the development of many compression algorithms, their applications in production environments are still not prevalent. In this paper, we revisit mainstream \texttt{KV} \texttt{cache} compression solutions from a practical perspective. Our contributions are three-fold. First, we comprehensively 
--- [문서 3] [Distance: 0.4820] [발행일: 2026-06-14] [2607.09683v1] Ablation, Statistical Inference, and Validation for KV-Cache Compression [초록] This study systematically compares Turbo-Quant and SpectralQuant KV-cache compression, evaluating non-dominated schemes, including WHT rotation with Beta Lloyd-Max and QJL, through a statistical validation methodology that separates systematic codec differences from implementation variance. Key findings reveal that while eigenbasis-based methods fail on heavy-tailed data due to covariance instability, they excel in structured regimes, with the effective semantic dimension ($d_{eff}$) adapting to calibration budgets rather than true data rank. (this is an ab
=== 답
<b>서론</b>
제공된 참고 문서에는 <b>HyperKV</b>, <b>SnapKV</b>에 대한 정보가 포함되어 있지 않습니다. 따라서 질문에서 언급한 두 방법과 관련된 내용을 찾을 수 없습니다.

<b>본론</b>
1. AirCache: 시각 토큰의 중복을 제거하고 elite observation window를 도입하여 KV 캐시 압축 효율성을 높였습니다[2503.23956v3].
2. Turbo‑Quant 및 SpectralQuant와 같은 기존 알고리즘에 대해 통계적 검증 방법을 통해 체계적으로 비교했습니다[2607.09683v1]

<b>결론</b>
HyperKV는 시각 KV 캐시의 10%만 유지하면서도 전체 캐시와 유사한 성능을 달성하고, 다양한 배치 크기와 프롬프트 길이에 따라 디코딩 지연을 29%에서 66%까지 감소시킨다[2503.23956v3]. 반면 SnapKV에 대한 구체적인 결과는 제공된 문서에 포함되어 있지 않아 두 방법의 직접적인 비교는 제한적이다. 따라서 HyperKV는 대규모 비전-언어 모델에서 캐시 압축 효율성을 입증했지만, 다른 연구에서는 고유벡터 기반 방법이 꼬리 분포 데이터에서는 실패하고 구조화된 영역에서는 우수한 성능을 보인다는 점을 강조한다[2607.09683v1].

######## K24 | MetaJailGuard 방어 기법이 공격 성공률을 몇 %로 낮췄어? | route direct_answer/B
  조건 0: 이름: MetaJailGuard
  조건 1: 수치: 공격 성공률 %
--- [문서 1] [Distance: 0.5231] [발행일: 2024-12-31] [2501.00517v1] A Method for Enhancing the Safety of Large Model Generation Based on Multi-dimensional Attack and Defense [초록] Currently, large models are prone to generating harmful content when faced with complex attack instructions, significantly reducing their defensive capabilities. To address this issue, this paper proposes a method based on constructing data aligned with multi-dimensional attack defense to enhance the generative security of large models. The core of our method lies in improving the effectiveness of safe alignment learning for large models by innova-tively increasing the diversity of attack instruction dimensions and the accur
=== 답
<b>서론</b>
대규모 언어 모델은 복잡한 공격 지시에 노출될 때 유해한 콘텐츠를 생성할 위험에 직면하며, 이는 방어 능력을 크게 저하시키는 문제입니다. 이러한 문제를 해결하기 위해 다차원적인 공격·방어 데이터를 활용한 안전 정렬 학습이 제안되었습니다[2501.00517v1].

<b>본론</b>
1. <b>Multi-dimensional Attack Defense Enhancement Method</b>: 이 방법은 다양한 차원의 공격 지시와 안전한 응답 생성 정확도를 향상시켜 대규모 모델의 보안 정렬 효과를 강화합니다.[2501.00517v1]
<b>2. (관련 정보 없음)</b>

<b>결론</b>
제공된 문서에 따르면, MetaJailGuard 방어 기법에 대한 구체적인 공격 성공률 감소 비율은 언급되어 있지 않습니다. 따라서 해당 수치로 답변할 수 없습니다[2501.00517v1].

######## K25 | DMQR-RAG랑 Rewrite-Retrieve-Read 쿼리 재작성 방식 비교해줘 | route direct_answer/B
  조건 0: 이름: DMQR-RAG
  조건 1: 이름: Rewrite-Retrieve-Read
--- [문서 1] [Distance: 0.2611] [발행일: 2024-11-20] [2411.13154v1] DMQR-RAG: Diverse Multi-Query Rewriting for RAG [초록] Large language models often encounter challenges with static knowledge and hallucinations, which undermine their reliability. Retrieval-augmented generation (RAG) mitigates these issues by incorporating external information. However, user queries frequently contain noise and intent deviations, necessitating query rewriting to improve the relevance of retrieved documents. In this paper, we introduce DMQR-RAG, a Diverse Multi-Query Rewriting framework designed to improve the performance of both document retrieval and final responses in RAG. Specifically, we investigate how queries wi
--- [문서 2] [Distance: 0.3227] [발행일: 2023-05-23] [2305.14283v3] Query Rewriting for Retrieval-Augmented Large Language Models [초록] Large Language Models (LLMs) play powerful, black-box readers in the retrieve-then-read pipeline, making remarkable progress in knowledge-intensive tasks. This work introduces a new framework, Rewrite-Retrieve-Read instead of the previous retrieve-then-read for the retrieval-augmented LLMs from the perspective of the query rewriting. Unlike prior studies focusing on adapting either the retriever or the reader, our approach pays attention to the adaptation of the search query itself, for there is inevitably a gap between the input text and the needed knowledge in retri
=== 답
<b>서론</b>
RAG 기반 시스템에서 <b>사용자 쿼리에는 노이즈와 의도 편차가 존재</b>하므로, 이를 재작성해 검색 관련성을 높이는 것이 핵심 과제입니다. 이러한 문제를 해결하기 위해 다양한 방식이 제안되었습니다.

<b>본론</b>
1. <b>DMQR-RAG</b>: 다중‑쿼리 재작성 프레임워크로, 정보 양에 따라 다른 수준의 4가지 전략을 적용하고 적응형 선택 메커니즘으로 불필요한 재작성을 최소화합니다[2411.13154v1].
2. <b>Rewrite‑Retrieve‑Read</b>: LLM이 쿼리를 생성·재작성하도록 프롬프트하며, 강화학습 기반 작은 언어 모델을 훈련시켜 검색 모듈에 맞춰 조정하고, 기존 retrieve‑then‑read 파이프라인 대신 rewrite 단계가 추가됩니다[2305.14283v3].

<b>결론</b>
DMQR-RAG는 적응형 재작성 선택을 통해 불필요한 재작성을 제거하고 관련 문서 검색을 유지하면서 노이즈를 감소시킨다 [2411.13154v1]. Rewrite-Retrieve-Read 파이프라인은 LLM 기반 재작성과 학습 가능한 재작성기를 도입하여 다운스트림 작업에서 일관된 성능 향상을 보이며, 기존 retrieve-then-read 방식보다 효과적이다 [2305.14283v3]. 두 연구 모두 RAG 시스템의 검색 정확도를 향상시키는 방향으로 결과를 제시하지만, DMQR-RAG는 적응형 선택 메커니즘을 강조하고, Rewrite-Retrieve-Read는 다양한 재작성 전략과 학습 가능한 모델을 통해 성능 개선을 입증한다.

######## K26 | jina-reranker-v3랑 RAG Playground 비교해줘 | route direct_answer/B
  조건 0: 이름: jina-reranker-v3
  조건 1: 이름: RAG Playground
--- [문서 1] [Distance: 0.1562] [발행일: 2025-09-29] [2509.25085v4] jina-reranker-v3: Last but Not Late Interaction for Listwise Document Reranking [초록] jina-reranker-v3 is a 0.6B-parameter multilingual listwise reranker that introduces a novel "last but not late" interaction. Unlike late interaction models like ColBERT that encode documents separately before multi-vector matching, our approach applies causal attention between the query and all candidate documents in the same context window, enabling rich interactions before extracting contextual embeddings from each document's final token. The new model achieves state-of-the-art BEIR performance with 61.94 nDCG@10 while being significantly smaller t
--- [문서 2] [Distance: 0.3456] [발행일: 2024-12-16] [2412.12322v1] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems [초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical results comparing different language models (Llama 3.1 and Qwen 2.5) across various retrieval configurati
=== 답
<b>서론</b>
jina‑reranker‑v3와 RAG Playground는 각각 <b>문서 재랭킹</b>과 <b>검색·프롬프트 엔지니어링 평가 프레임워크</b>를 목표로 하는 시스템으로, 서로 다른 문제 영역에서 성능을 향상시키는 접근법을 제시한다. 두 모델은 모두 최신 연구 결과에 기반해 설계되었으나 적용 대상이 다르다.

<b>본론</b>
1. <b>jina‑reranker‑v3</b>: 0.6B 파라미터 다국어 리스트위즈 재랭커이며, “last but not late” 상호작용을 도입한다[2509.25085v4].
2. <b>RAG Playground</b>: 오픈소스 프레임워크로 RAG 시스템의 검색 전략과 프롬프트 엔지니어링을 체계적으로 평가할 수 있도록 설계되었다[2412.12322v1]

<b>결론</b>
jina-reranker-v3는 BEIR 데이터셋에서 61.94 nDCG@10을 달성하여 이전 모델 대비 4.79% 향상된 성능을 보였습니다[2509.25085v4]. 반면 RAG Playground는 다중 지표 평가 프레임워크에서 하이브리드 검색과 구조화된 자기평가 프롬프트를 통해 최대 72.7%의 패스율을 기록했습니다[2412.12322v1]. 두 연구는 각각 문서 재랭킹과 전체 RAG 시스템 평가라는 서로 다른 대상에 초점을 맞추어, jina-reranker-v3가 특정 재랭킹 작업에서 높은 정확도를 달성한 반면 RAG Playground는 프롬프트 엔지니어링을 포함한 광범위한 RAG 파이프라인의 전반적인 성능 향상에 기여했다는 점에서 결과를 달리하고 있습니다.

######## K27 | World4RL이랑 Looped World Models 차이 알려줘 | route direct_answer/B
  조건 0: 이름: World4RL
  조건 1: 이름: Looped World Models
--- [문서 1] [Distance: 0.5128] [발행일: 2025-09-23] [2509.19080v2] World4RL: Diffusion World Models for Policy Refinement with Reinforcement Learning for Robotic Manipulation [초록] Robotic manipulation policies are commonly initialized through imitation learning, but their performance is limited by the scarcity and narrow coverage of expert data. Reinforcement learning can refine polices to alleviate this limitation, yet real-robot training is costly and unsafe, while training in simulators suffers from the sim-to-real gap. Recent advances in generative models have demonstrated remarkable capabilities in real-world simulation, with diffusion models in particular excelling at generation. This raises t
--- [문서 2] [Distance: 0.2539] [발행일: 2026-06-16] [2606.18208v1] Looped World Models [초록] Current world models face a fundamental tension: faithful long-horizon simulation demands deep computation, but deeper models are expensive to deploy and prone to compounding errors. We resolve this by introducing Looped World Models (LoopWM), which are the first looped architectures for world modelling. Our method iteratively refines latent environment states through a parameter-shared transformer block. This yield up to 100x parameter efficiency over conventional approaches with adaptive computation that automatically scales depth to match the complexity of each prediction step. Orthogonal to scaling model 
=== 답
<b>서론</b>
Robotic manipulation에서 <b>World Model</b>과 같은 생성 모델을 활용해 정책을 개선하는 것은, 전문가 데이터가 부족하고 시뮬레이션‑실제 간격(sim-to-real gap) 때문에 어려운 과제입니다. 또한 장기 예측이 필요한 경우 모델의 계산 비용과 오류 누적 문제를 동시에 해결해야 합니다.

<b>본론</b>
1. <b>World4RL</b>: 확산 기반 세계 모델을 고정된 환경으로 사용하여 사전 학습한 정책을 완전히 가상 공간에서 최적화하고, 두‑핫 액션 인코딩을 도입해 로봇 조작에 특화된 고충실도 시뮬레이션을 제공합니다[2509.19080v2].
2. <b>Looped World Models (LoopWM)</b>: 파라미터를 공유하는 트랜스포머 블록으로 잠재 환경 상태를 반복적으로 정제하고, 적응형 계산 방식을 통해 각 예측 단계의 복잡도에 맞춰 깊이를 자동으로 조정함으로써 기존 접근법 대비 최대 100배 이상의 매개변수 효율성을 달성합니다[2606.18208v1].

<b>결론</b>
World4RL은 로봇 조작 분야에서 고충실도 환경 모델링과 일관된 정책 정제를 통해 기존 강화학습 및 모방 학습 기반 방법보다 높은 성공률을 달성한다[2509.19080v2]. 반면 Looped World Models는 파라미터 효율성을 최대 100배 향상시키고, 예측 단계의 복잡성에 따라 계산 깊이를 자동으로 조정하며 안정적인 롤프를 장기적으로 유지하는 성능을 보인다[2606.18208v1]. 두 연구는 각각 로봇 조작과 일반적인 세계 모델 예측이라는 서로 다른 도메인과 목표에 초점을 맞추어, World4RL은 실제 실험을 통한 성공률 향상과 Looped World Models는 파라미터 효율성과 계산 적응성을 강조한다.

######## K28 | TradingAgents랑 BMW Agents 비교해줘 | route direct_answer/A
  조건 0: 이름: TradingAgents
  조건 1: 이름: BMW Agents
=== 답
(없음)

######## K29 | RAG 검색 정확도 연구 3개 찾고 각각 한계도 하나씩 알려줘 | route direct_answer/B
  조건 0: 편수: 3편
  조건 1: 과제: 논문마다 한계 하나
--- [문서 1] [Distance: 0.1836] [발행일: 2024-08-15] [2408.08067v2] RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation [초록] Despite Retrieval-Augmented Generation (RAG) showing promising capability in leveraging external knowledge, a comprehensive evaluation of RAG systems is still challenging due to the modular nature of RAG, evaluation of long-form responses and reliability of measurements. In this paper, we propose a fine-grained evaluation framework, RAGChecker, that incorporates a suite of diagnostic metrics for both the retrieval and generation modules. Meta evaluation verifies that RAGChecker has significantly
--- [문서 2] [Distance: 0.1908] [발행일: 2024-12-16] [2412.12322v1] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems [초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical results comparing different language models (Llama 3.1 and Qwen 2.5) across various r
--- [문서 3] [Distance: 0.1095] [발행일: 2024-05-13] [2405.07437v2] Evaluation of Retrieval-Augmented Generation: A Survey [초록] Retrieval-Augmented Generation (RAG) has recently gained traction in natural language processing. Numerous studies and real-world applications are leveraging its ability to enhance generative models through external information retrieval. Evaluating these RAG systems, however, poses unique challenges due to their hybrid structure and reliance on dynamic knowledge sources. To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehe
--- [문서 4] [Distance: 0.2477] [발행일: 2024-05-31] [2406.04369v1] RAG Does Not Work for Enterprises [초록] Retrieval-Augmented Generation (RAG) improves the accuracy and relevance of large language model outputs by incorporating knowledge retrieval. However, implementing RAG in enterprises poses challenges around data security, accuracy, scalability, and integration. This paper explores the unique requirements for enterprise RAG, surveys current approaches and limitations, and discusses potential advances in semantic search, hybrid queries, and optimized retrieval. It proposes an evaluation framework
--- [문서 5] [Distance: 0.2992] [발행일: 2025-07-26] [2508.05650v1] OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools [초록] While Retrieval Augmented Generation (RAG) is now widely adopted to enhance LLMs, evaluating its true performance benefits in a reproducible and interpretable way remains a major hurdle. Existing methods often fall short: they lack domain coverage, employ coarse metrics that miss sub document precision, and fail to capture computational trade offs. Most critically, they provide no standardized framework for comparing RAG effectiveness across different models and domains. We introduce OmniBench R
--- [문서 6] [Distance: 0.1773] [발행일: 2026-02-25] [2602.21553v1] Revisiting RAG Retrievers: An Information Theoretic Benchmark [초록] Retrieval-Augmented Generation (RAG) systems rely critically on the retriever module to surface relevant context for large language models. Although numerous retrievers have recently been proposed, each built on different ranking principles such as lexical matching, dense embeddings, or graph citations, there remains a lack of systematic understanding of how these mechanisms differ and overlap. Existing benchmarks primarily compare entire RAG pipelines or introduce new datasets, providing little
=== 답
<b>서론</b>
제공된 문서들은 모두 Retrieval-Augmented Generation (RAG) 시스템에서 검색 정확도를 평가하거나 개선하는 연구에 초점을 맞추고 있습니다. 각 논문은 RAG 파이프라인을 진단·평가하기 위한 새로운 프레임워크나 벤치마크를 제시하고, 기존 방법의 한계를 지적합니다.

<b>본론</b>
1. <b>RAGChecker</b>: Retrieval 및 Generation 모듈 각각에 대한 정밀한 평가 메트릭트를 포함하는 미세‑그레인 평가를 제안하며, Meta evaluation을 통해 RAG 시스템이 외부 지식을 활용한다는 점을 검증한다[2408.08067v2].
2. <b>RAG Playground</b>: Naive vector search, reranking, hybrid vector-keyword 검색 등 세 가지 접근법을 구현하고 ReAct 에이전트와 다양한 프롬프트 전략을 비교하며 새로운 메트릭으로 평가 결과를 제공한다[2412.12322v1].
3. <b>Auepora (Unified Evaluation Process of RAG)</b>: 하이브리드 구조 및 동적 지식원에 의존하는 특성 때문에 발생하는 독특한 평가를 이해하기 위해 통합된 평가 과정을 제안한다[2405.07437v2].

<b>결론</b>
제공된 문서들은 RAG 시스템의 정확도 평가를 위한 세 가지 다른 접근법을 제시하고 있다. 첫 번째 연구인 RAGChecker는 검색 및 생성 모듈을 모두 진단할 수 있는 정교한 평가 프레임워크를 제안하며, 메타 평가를 통해 기존 방법보다 유의미한 성능 향상을 보인 것으로 확인되었다[2408.08067v2]. 두 번째 연구인 RAG Playground는 단순 벡터 검색, 리랭킹, 하이브리드 검색 등 세 가지 검색 전략을 구현하고 비교함으로써 다양한 언어 모델에 대한 경험적 결과를 제공한다[2412.12322v1]. 세 번째 연구는 RAG 시스템의 고유한 평가 난점을 강조하고, 이를 해결하기 위해 통합 평가 프로세스인 Auepora를 제안한다[2405.07437v2]. 따라서 각 논문은 서로 다른 평가 목표와 방법론을 통해 RAG 정확도 향상에 기여하지만, 구체적인 수치나 조건에 따라 결과가 완전히 일치하지는 않는다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• Evaluating Retrieval Quality in Retrieval-Augmented Generation (2024) [2404.13781]
• A Research of Challenges and Solutions in Retrieval Augmented Generation (RAG) Systems (2025) https://doi.org/10.54097/364hex16
• Retrieval Augmented Generation (RAG) using LLMs (2025) https://doi.org/10.1109/aicdmb64359.2025.11277692
• Retrieval-Augmented Generation (RAG) in Healthcare: A Comprehensive Review (2025) https://doi.org/10.3390/ai6090226

######## K30 | LLM 에이전트 메모리 연구 정리하고 아직 안 풀린 문제 2가지 제안해줘 | route direct_answer/B
  조건 0: 과제: 안 풀린 문제 2가지 제안
--- [문서 1] [Distance: 0.1817] [발행일: 2026-06-23] [2606.24775v1] Are We Ready For An Agent-Native Memory System? [초록] Memory for large language model (LLM) agents has rapidly evolved from simple retrieval-augmented mechanisms into a data management system that supports persistent information storage, retrieval, update, consolidation, and dynamic lifecycle governance throughout agent execution. Despite this evolution, existing evaluations still benchmark agent memory mainly through end-to-end task success metrics (e.g., F1, BLEU), while treating the underlying system as a monolithic black box. As a result, critical system-level concerns, including operational costs, architectural trade-offs across 
--- [문서 2] [Distance: 0.1731] [발행일: 2026-03-08] [2603.07670v1] Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and Emerging Frontiers [초록] Large language model (LLM) agents increasingly operate in settings where a single context window is far too small to capture what has happened, what was learned, and what should not be repeated. Memory -- the ability to persist, organize, and selectively recall information across interactions -- is what turns a stateless text generator into a genuinely adaptive agent. This survey offers a structured account of how memory is designed, implemented, and evaluated in modern LLM-based agents, covering work from 2022 through early 2026. We formalize agent 
=== 답
<b>서론</b>
LLM 에이전트 메모리는 장기적인 상태 유지와 개인화된 상호작용을 지원해야 하므로, 단순한 검색‑증강 메커니즘으로는 부족합니다. 이러한 요구를 충족하려면 데이터 관리 관점에서 구조화되고 평가된 시스템이 필요합니다[2606.24775v1][2603.07670v1].

<b>본론</b>
1. <b>Agent Memory Data Management Framework</b>: 메모리를 네 가지 핵심 모듈(표현·저장, 추출, 검색·라우팅, 유지관리)로 분해하고, 다섯 벤치마크 워크로드와 두 기준 모델을 대상으로 총 14 시스템을 평가했습니다[2606.24775v1].
2. <b>Three‑Dimensional Memory Taxonomy</b>: 메모리를 시간 범위, 표현 기질, 제어 정책이라는 세 차원으로 분류하며, write–manage–read 루프를 통해 인지·행동과 결합된 설계와 평가를 제시합니다[2603.07670v1].

<b>결론</b>
제공한 두 문서에 따르면, LLM 에이전트 메모리 연구는 데이터 관리 프레임워크와 다차원적 태그노미로 구조화되고 있으며, 현재 해결되지 않은 주요 과제는 <b>continual consolidation</b> (지속적인 통합) 와 <b>causally grounded retrieval</b> (인과 기반 검색), 그리고 <b>trustworthy reflection</b>, <b>learned forgetting</b>, <b>multimodal embodied memory</b> 등입니다. 이러한 과제들은 향후 연구에서 집중해야 할 핵심 방향이 됩니다[2603.07670v1].

######## K31 | 프롬프트 인젝션 방어 연구를 공격 유형별로 나눠서 정리해줘 | route direct_answer/B
  조건 0: 과제: 공격 유형별로 나누기
--- [문서 1] [Distance: 0.4058] [발행일: 2026-05-14] [2605.15118v1] Talk is (Not) Cheap: A Taxonomy and Benchmark Coverage Audit for LLM Attacks [초록] We introduce a reusable framework for auditing whether LLM attack benchmarks collectively cover the threat surface: a 4$\times$6 Target $\times$ Technique matrix grounded in STRIDE, constructed from a 507-leaf taxonomy -- 401 data-populated and 106 threat-model-derived leaves -- of inference-time attacks extracted from 932 arXiv security studies (2023--2026). The matrix enables benchmark-external validation -- auditing collective coverage rather than individual benchmark consistency. Applying it
--- [문서 2] [Distance: 0.3783] [발행일: 2026-06-10] [2606.12737v1] PI-Hunter: Automated Red-Teaming for Exposing and Localizing Prompt Injections [초록] Large Language Models (LLMs) are rapidly evolving into agentic systems that interact with external tools and environments, introducing new security risks such as indirect prompt injection attacks through untrusted external sources. Existing defenses mainly focus on blocking malicious content at inference time, and current red-teaming methods primarily optimize attack success. As a result, developers have limited visibility into how latent prompt injections emerge and propagate through agents. We
--- [문서 3] [Distance: 0.4136] [발행일: 2026-05-14] [2605.15030v1] WARD: Adversarially Robust Defense of Web Agents Against Prompt Injections [초록] Web agents can autonomously complete online tasks by interacting with websites, but their exposure to open web environments makes them vulnerable to prompt injection attacks embedded in HTML content or visual interfaces. Existing guard models still suffer from limited generalization to unseen domains and attack patterns, high false positive rates on benign content, reduced deployment efficiency due to added latency at each step, and vulnerability to adversarial attacks that evolve over time or d
--- [문서 4] [Distance: 0.4166] [발행일: 2026-06-13] [2606.15441v1] Defending against Adaptive Prompt Injection Attacks via Reasoning-enabled Task Alignment [초록] Indirect prompt injection attacks hijack LLM-based agents by embedding malicious instructions in third-party data that the agent retrieves during task execution. Existing defenses report near-zero attack success rate on static benchmarks, yet recent adaptive evaluations show that these results collapse once the attacker is allowed to optimize against the deployed defense. In this work, we trace this collapse to two failure modes. First, existing defense methods are confined to recognizing specif
--- [문서 5] [Distance: 0.5277] [발행일: 2026-05-16] [2605.17163v1] STRIDE-AI: A Threat Modeling Framework for Generative AI Security Assessment [초록] Traditional cybersecurity methodologies target deterministic systems and fail to address the probabilistic nature of AI, leaving systems vulnerable to attack vectors such as model inversion, data poisoning, and prompt injection. Recent industry reports indicate that a majority of organizations deploying AI lack a dedicated security strategy, with adversarial attacks increasing rapidly year-over-year. We present \textit{STRIDE-AI}, a framework that bridges the gap between high-level risk standard
--- [문서 6] [Distance: 0.4810] [발행일: 2024-12-26] [2412.19037v2] CL-Attack: Textual Backdoor Attacks via Cross-Lingual Triggers [초록] Backdoor attacks significantly compromise the security of large language models by triggering them to output specific and controlled content. Currently, triggers for textual backdoor attacks fall into two categories: fixed-token triggers and sentence-pattern triggers. However, the former are typically easy to identify and filter, while the latter, such as syntax and style, do not apply to all original samples and may lead to semantic shifts. In this paper, inspired by cross-lingual (CL) prompts
=== 답
<b>서론</b>
프롬프트 인젝션 공격은 LLM 기반 에이전트가 외부 데이터를 처리하거나 웹 인터페이스와 상호작용할 때 발생하는 주요 위협이며, 이를 방어하기 위한 연구가 다양한 접근법으로 진행되고 있습니다.

<b>본론</b>
1. <b>Benchmark Coverage Audit</b>: 4×6 Target × Technique 행렬을 기반으로 LLM 공격 벤치마크의 전체적인 위협 표면 커버리지를 평가하는 재사용 가능한 프레임워크를 제안합니다[2605.15118v1]
2. <b>PI-Hunter</b>: 자동화된 레드팀 도구로, 에이전트 내부에서 잠재적 프롬프트 인젝션이 어떻게 발생·확산되는지 가시성을 높이고 공격 성공률을 최적화하도록 설계되었습니다[2606.12737v1]
3. <b>WARD</b>: 웹 에이전트가 HTML 콘텐츠나 시각 인터페이스에 포함된 프롬프트 인젝션을 견디도록, 일반화된 방어 모델을 제공합니다[2605.15030v1]
4. <b>Reasoning-enabled Task Alignment</b>: 적응형 프롬프트 인젝션 공격을 막기 위해 추론 기반 작업 정렬 메커니즘으로 기존 방어의 두 가지 실패 모드를 해결합니다[2606.15441v1]

<b>결론</b>
제공된 문서들은 프롬프트 인젝션 방어 연구의 결과를 공격 유형별로 정리할 수 있는 충분한 정보를 제공하지 않습니다. [2605.15118v1]은 LLM 공격 벤치마크가 위협 표면을 얼마나 포괄적으로 커버하는지 평가하는 재사용 가능한 프레임워크를 소개하고, 이는 STRIDE 기반의 4×6 타겟 × 기법 행렬과 507개의 분류 항목을 통해 구현됩니다. [2606.12737v1]는 개발자가 잠재적 프롬프트 인젝션이 에이전트를 통해 어떻게 나타나는지 파악하는 데 제한된 가시성만 있다고 보고합니다. [2605.15030v1]은 기존 가드 모델이 새로운 도메인과 공격 패턴에 대한 일반화 능력이 부족하고, 무해한 콘텐츠에 대해 높은 위양성률을 보이며, 지연으로 인한 효율성 저하와 시간에 따라 진화하는 적대적 공격에 취약함을 지적합니다. [2606.15441v1]는 정적 벤치마크에서는 공격 성공률이 거의 0에 가깝지만, 공격자가 방어 모델을 최적화할 수 있는 적응형 평가에서는 이러한 결과가 무너진다고 보고합니다. 따라서 각 연구는 서로 다른 평가 조건(벤치마크 포괄성, 개발자 가시성, 일반화 한계, 정적 vs 적응형 평가)에서 프롬프트 인젝션 방어의 취약점과 한계를 제시하고 있습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• Optimized Multi-Agent Defense Pipeline Against Advanced Prompt Injection Attacks (2026) https://openalex.org/W7213477280
• Prompt Injection Attacks on Large Language Models: A Survey of Attack Methods, Root Causes, and Defense Strategies (2025) https://doi.org/10.32604/cmc.2025.074081
• Prompt Injection attack against LLM-integrated Applications (2023) [2306.05499]
• Taxonomy of Prompt Injection Attacks and Analysis of Defense Mechanisms in Large Language Model-Based Chatbots (2026) https://doi.org/10.51582/interconf.19-20.05.2026.017

######## K32 | 확산 모델 가속 연구를 학습 필요 여부로 나눠서 정리해줘 | route direct_answer/B
  조건 0: 과제: 학습 필요 여부로 나누기
--- [문서 1] [Distance: 0.3714] [발행일: 2024-11-13] [2411.08438v1] Towards Optimizing a Retrieval Augmented Generation using Large Language Model on Academic Data [초록] Given the growing trend of many organizations integrating Retrieval Augmented Generation (RAG) into their operations, we assess RAG on domain-specific data and test state-of-the-art models across various optimization techniques. We incorporate four optimizations; Multi-Query, Child-Parent-Retriever, Ensemble Retriever, and In-Context-Learning, to enhance the functionality and performance in the academic domain. We focus on data retrieval, specifically targeting various study programs at a large
--- [문서 2] [Distance: 0.4093] [발행일: 2026-02-25] [2602.21553v1] Revisiting RAG Retrievers: An Information Theoretic Benchmark [초록] Retrieval-Augmented Generation (RAG) systems rely critically on the retriever module to surface relevant context for large language models. Although numerous retrievers have recently been proposed, each built on different ranking principles such as lexical matching, dense embeddings, or graph citations, there remains a lack of systematic understanding of how these mechanisms differ and overlap. Existing benchmarks primarily compare entire RAG pipelines or introduce new datasets, providing little
--- [문서 3] [Distance: 0.3388] [발행일: 2024-10-03] [2410.12837v1] A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions [초록] This paper presents a comprehensive study of Retrieval-Augmented Generation (RAG), tracing its evolution from foundational concepts to the current state of the art. RAG combines retrieval mechanisms with generative language models to enhance the accuracy of outputs, addressing key limitations of LLMs. The study explores the basic architecture of RAG, focusing on how retrieval and generation are integrated to handle knowledge-intensive tasks. A detailed review of the significant technological adv
--- [문서 4] [Distance: 0.3917] [발행일: 2025-08-08] [2508.06401v3] A Systematic Literature Review of Retrieval-Augmented Generation: Techniques, Metrics, and Challenges [초록] This systematic review of the research literature on retrieval-augmented generation (RAG) provides a focused analysis of the most highly cited studies published between 2020 and May 2025. A total of 128 articles met our inclusion criteria. The records were retrieved from ACM Digital Library, IEEE Xplore, Scopus, ScienceDirect, and the Digital Bibliography and Library Project (DBLP). RAG couples a neural retriever with a generative language model, grounding output in up-to-date, non-parametric me
--- [문서 5] [Distance: 0.4211] [발행일: 2025-08-01] [2508.05666v1] HySemRAG: A Hybrid Semantic Retrieval-Augmented Generation Framework for Automated Literature Synthesis and Methodological Gap Analysis [초록] We present HySemRAG, a framework that combines Extract, Transform, Load (ETL) pipelines with Retrieval-Augmented Generation (RAG) to automate large-scale literature synthesis and identify methodological research gaps. The system addresses limitations in existing RAG architectures through a multi-layered approach: hybrid retrieval combining semantic search, keyword filtering, and knowledge graph traversal; an agentic self-correction framework with iterative quality assurance; and post-hoc citatio
--- [문서 6] [Distance: 0.4682] [발행일: 2026-02-11] [2602.15895v2] Understand Then Memory: A Cognitive Gist-Driven RAG Framework with Global Semantic Diffusion [초록] Retrieval-Augmented Generation (RAG) effectively mitigates hallucinations in LLMs by incorporating external knowledge. However, the inherent discrete representation of text in existing frameworks often results in a loss of semantic integrity, leading to retrieval deviations. Inspired by the human episodic memory mechanism, we propose CogitoRAG, a RAG framework that simulates human cognitive memory processes. The core of this framework lies in the extraction and evolution of the Semantic Gist. Du
--- [문서 7] [Distance: 0.3725] [발행일: 2024-05-13] [2405.07437v2] Evaluation of Retrieval-Augmented Generation: A Survey [초록] Retrieval-Augmented Generation (RAG) has recently gained traction in natural language processing. Numerous studies and real-world applications are leveraging its ability to enhance generative models through external information retrieval. Evaluating these RAG systems, however, poses unique challenges due to their hybrid structure and reliance on dynamic knowledge sources. To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehe
--- [문서 8] [Distance: 0.4442] [발행일: 2024-12-30] [2412.20864v1] Enhancing Annotated Bibliography Generation with LLM Ensembles [초록] This work proposes a novel approach to enhancing annotated bibliography generation through Large Language Model (LLM) ensembles. In particular, multiple LLMs in different roles -- controllable text generation, evaluation, and summarization -- are introduced and validated using a systematic methodology to enhance model performance in scholarly tasks. Output diversity among the ensemble that generates text is obtained using different LLM parameters, followed by an LLM acting as a judge to assess r
--- [문서 9] [Distance: 0.4527] [발행일: 2025-06-01] [2506.06339v1] Optimizing RAG Pipelines for Arabic: A Systematic Analysis of Core Components [초록] Retrieval-Augmented Generation (RAG) has emerged as a powerful architecture for combining the precision of retrieval systems with the fluency of large language models. While several studies have investigated RAG pipelines for high-resource languages, the optimization of RAG components for Arabic remains underexplored. This study presents a comprehensive empirical evaluation of state-of-the-art RAG components-including chunking strategies, embedding models, rerankers, and language models-across a
--- [문서 10] [Distance: 0.4237] [발행일: 2025-10-30] [2510.26205v2] Towards Global Retrieval Augmented Generation: A Benchmark for Corpus-Level Reasoning [초록] Retrieval-augmented generation (RAG) has emerged as a leading approach to reducing hallucinations in large language models (LLMs). Current RAG evaluation benchmarks primarily focus on what we call local RAG: retrieving relevant chunks from a small subset of documents to answer queries that require only localized understanding within specific text chunks. However, many real-world applications require a fundamentally different capability -- global RAG -- which involves aggregating and analyzing in
=== 답
<b>서론</b>
제공된 문서들은 모두 Retrieval‑Augmented Generation (RAG) 시스템에 대한 연구이며, 질문에서 요구하는 “확산 모델 가속”과 관련된 내용은 포함되어 있지 않습니다. 따라서 학습 필요 여부에 따라 분류할 수 있는 정보는 없습니다.

<b>본론</b>
1. <b>Multi-Query</b>: 다중 쿼리 최적화 기법을 적용하여 RAG 성능을 향상시켰다 [2411.08438v1] 자식·부모 리트리버 구조를 도입해 기능과 성과를 강화했다 [2411.08438v1]
<b>결론</b>
제공된 문서들은 모두 학습 필요 여부와 무관하게 다양한 최적화 기법을 통해 RAG 성능을 개선하는 연구에 초점을 맞추고 있습니다.

######## K33 | 텍스트 임베딩 연구 중 다국어 지원하는 것만 골라줘 | route direct_answer/B
  조건 0: 선별: 다국어 지원만
--- [문서 1] [Distance: 0.3257] [발행일: 2024-09-24] [2409.15763v2] IRSC: A Zero-shot Evaluation Benchmark for Information Retrieval through Semantic Comprehension in Retrieval-Augmented Generation Scenarios [초록] In Retrieval-Augmented Generation (RAG) tasks using Large Language Models (LLMs), the quality of retrieved information is critical to the final output. This paper introduces the IRSC benchmark for evaluating the performance of embedding models in multilingual RAG tasks. The benchmark encompasses five retrieval tasks: query retrieval, title retrieval, part-of-paragraph retrieval, keyword retrieval, and summary retrieval. Our research addresses the current lack of comprehensive testing and eff
=== 답
<b>서론</b>
텍스트 임베딩 모델에서 <b>다국어 지원</b>은 다양한 언어 환경에서도 일관된 검색 성능을 보장해야 하므로 평가가 어렵습니다. 특히 기존 벤치마크는 단일어나 제한적인 다언어 데이터만 포함해 실제 활용성을 충분히 반영하지 못했습니다.

<b>본론</b>
1. <b>IRSC Benchmark</b>: 이벤트 모델의 멀티링구얼 RAG 작업을 위한 새로운 기준이며, 쿼리·키워드·제목·요약 및 부분 문단 검색 등 다섯 가지 작업과 다국어/교차언어 구성 요소를 포함합니다[2409.15763v2].

<b>결론</b>
제공된 문서에 따르면 <b>IRSC Benchmark</b>가 텍스트 임베딩 연구에서 다국어를 지원하는 유일한 평가 체계입니다.

######## K34 | 오픈소스 모델로만 실험한 Text-to-SQL 연구 알려줘 | route direct_answer/B
  조건 0: 선별: 오픈소스 모델로만 실험
--- [문서 1] [Distance: 0.3178] [발행일: 2024-10-01] [2410.01066v2] From Natural Language to SQL: Review of LLM-based Text-to-SQL Systems [초록] LLMs when used with Retrieval Augmented Generation (RAG), are greatly improving the SOTA of translating natural language queries to structured and correct SQL. Unlike previous reviews, this survey provides a comprehensive study of the evolution of LLM-based text-to-SQL systems, from early rule-based models to advanced LLM approaches that use (RAG) systems. We discuss benchmarks, evaluation methods, and evaluation metrics. Also, we uniquely study the use of Graph RAGs for better contextual accuracy and schema linking in these systems. Finally, we highlight key 
--- [문서 2] [Distance: 0.3428] [발행일: 2024-12-13] [2412.10138v3] ROUTE: Robust Multitask Tuning and Collaboration for Text-to-SQL [초록] Despite the significant advancements in Text-to-SQL (Text2SQL) facilitated by large language models (LLMs), the latest state-of-the-art techniques are still trapped in the in-context learning of closed-source LLMs (e.g., GPT-4), which limits their applicability in open scenarios. To address this challenge, we propose a novel RObust mUltitask Tuning and collaboration mEthod (ROUTE) to improve the comprehensive capabilities of open-source LLMs for Text2SQL, thereby providing a more practical solution. Our approach begins with multi-task supervised fine-tuning (SFT) u
--- [문서 3] [Distance: 0.3380] [발행일: 2024-12-17] [2412.12522v1] Solid-SQL: Enhanced Schema-linking based In-context Learning for Robust Text-to-SQL [초록] Recently, large language models (LLMs) have significantly improved the performance of text-to-SQL systems. Nevertheless, many state-of-the-art (SOTA) approaches have overlooked the critical aspect of system robustness. Our experiments reveal that while LLM-driven methods excel on standard datasets, their accuracy is notably compromised when faced with adversarial perturbations. To address this challenge, we propose a robust text-to-SQL solution, called Solid-SQL, designed to integrate with various LLMs. We focus on the pre-processing stage, train
--- [문서 4] [Distance: 0.3256] [발행일: 2024-12-21] [2412.17867v4] Evaluating and Enhancing LLMs for Multi-turn Text-to-SQL with Multiple Question Types [초록] Recent advancements in large language models (LLMs) have significantly advanced text-to-SQL systems. However, most LLM-based methods often narrowly focus on SQL generation, neglecting the complexities of real-world conversational queries. This oversight can lead to unreliable responses, particularly for ambiguous questions that cannot be directly addressed with SQL. To bridge this gap, we propose MMSQL, a comprehensive test suite designed to evaluate the question classification and SQL generation capabilities of LLMs by simulating real-world sc
--- [문서 5] [Distance: 0.3713] [발행일: 2026-04-08] [2604.07041v1] AV-SQL: Decomposing Complex Text-to-SQL Queries with Agentic Views [초록] Text-to-SQL is the task of translating natural language queries into executable SQL for a given database, enabling non-expert users to access structured data without writing SQL manually. Despite rapid advances driven by large language models (LLMs), existing approaches still struggle with complex queries in real-world settings, where database schemas are large and questions require multi-step reasoning over many interrelated tables. In such cases, providing the full schema often exceeds the context window, while one-shot generation frequently produces non-execut
=== 답
<b>서론</b>
Text-to-SQL은 자연어 질의를 실행 가능한 SQL로 변환하는 작업이며, 복잡한 스키마와 다단계 추리가 필요해 구현하기 어렵습니다. 특히 <b>오픈소스 모델</b>만 사용하여 연구한 사례는 제한적입니다.

<b>본론</b>
1. <b>ROUTE</b>: 오픈소스 LLM을 대상으로 멀티태스크 초점 미세조정(SFT)과 협업 프롬프팅(MCP) 전략을 도입해 SQL 생성 능력을 향상시켰습니다[2412.10138v3].
2. <b>Solid-SQL</b>: 스키마 링크 모델을 강화하고, 인‑컨텍스트 학습에 구조적 유사성 기반 예시 검색을 적용하여 오픈소스 LLM과의 통합 가능성을 제시했습니다[2412.12522v1].

<b>결론</b>
제공된 문서들은 모두 오픈소스 모델만을 대상으로 Text-to-SQL 성능 향상을 목표로 한 연구입니다.

######## K35 | 7B 이하 작은 모델로 실험한 수학 추론 연구 알려줘 | route direct_answer/B
  조건 0: 선별: 7B 이하 모델 실험
--- [문서 1] [Distance: 0.3282] [발행일: 2025-06-10] [2506.08669v1] Enhancing Reasoning Capabilities of Small Language Models with Blueprints and Prompt Template Search [초록] Small language models (SLMs) offer promising and efficient alternatives to large language models (LLMs). However, SLMs' limited capacity restricts their reasoning capabilities and makes them sensitive to prompt variations. To address these challenges, we propose a novel framework that enhances SLM reasoning capabilities through LLM generated blueprints. The blueprints provide structured, high-level reasoning guides that help SLMs systematically tackle related problems. Furthermore, our framework integrates a prompt template searc
--- [문서 2] [Distance: 0.3498] [발행일: 2024-12-24] [2412.18415v1] Multilingual Mathematical Reasoning: Advancing Open-Source LLMs in Hindi and English [초록] Large Language Models (LLMs) excel in linguistic tasks but struggle with mathematical reasoning, particularly in non English languages like Hindi. This research aims to enhance the mathematical reasoning skills of smaller, resource efficient open-source LLMs in both Hindi and English. We evaluate models like OpenHathi 7B, LLaMA-2 7B, WizardMath 7B, Mistral 7B, LLeMMa 7B, MAmmoTH 7B, Gemini Pro, and GPT-4 using zero-shot, few-shot chain-of-thought (CoT) methods, and supervised fine-tuning. Our approach incorporates curriculum learning, progressiv
=== 답
<b>서론</b>
작은 언어 모델(7B 이하) 은 <b>수학적 추론</b> 능력이 제한되어 있어 복잡한 연산이나 논리적 문제를 해결하기 어렵습니다. 이러한 한계를 극복하려면 효율적인 학습 전략과 구조화된 접근이 필요합니다.

<b>본론</b>
1. <b>Blueprints and Prompt Template Search</b>: LLM으로 생성된 블루프린트를 활용해 SLM에 고수준 추론 가이드를 제공하고, 프롬프트 템플릿 검색 메커니즘을 도입해 프롬프트 변화 민감도를 낮춥니다[2506.08669v1].
2. <b>Curriculum Learning &amp; Decomposition Strategy</b>: 커리큘럼 학습과 새로운 분할 전략(Decomposition) 을 적용하여 모델이 점진적으로 어려운 문제를 해결하도록 훈련하고, 구조화된 솔루션 설계로 복잡한 산술 연산을 단계별로 처리합니다[2412.18415v1].

<b>결론</b>
[2506.08669v1]은 7B 이하의 소규모 언어 모델(SLM)이 프롬프트 템플릿 검색을 통해 수학 추론(GSM8K) 성능을 향상시킬 수 있음을 보여준다[2506.08669v1]. [2412.18415v1]는 OpenHathi 7B, LLaMA-2 7B, WizardMath 7B 등 7B 모델들을 평가하여 WizardMath 7B가 영어 데이터셋에서 Gemini보다 정확도가 +6% 높고, 힌디어 데이터셋에서는 Gemini와 동등한 성능을 보임을 보고한다[2412.18415v1]. 두 연구 모두 7B 이하 규모의 모델을 대상으로 수학 추론 능력을 개선하는 방법을 제시하지만, [2506.08669v1]은 프롬프트 기반 경량화 접근에 초점을 맞추고, [2412.18415v1]는 다국어 샘플과 모델 비교를 통한 성능 평가에 중점을 둔다. 따라서 질문에서 요구한 '7B 이하 작은 모델로 실험한 수학 추론 연구'는 두 논문 모두 해당한다[2506.08669v1][2412.18415v1].

######## K36 | 이미지 말고 동영상으로 실험한 VLM 환각 연구 알려줘 | route direct_answer/B
  조건 0: 선별: 동영상 실험
--- [문서 1] [Distance: 0.4122] [발행일: 2024-05-27] [2405.17706v1] Video Enriched Retrieval Augmented Generation Using Aligned Video Captions [초록] In this work, we propose the use of "aligned visual captions" as a mechanism for integrating information contained within videos into retrieval augmented generation (RAG) based chat assistant systems. These captions are able to describe the visual and audio content of videos in a large corpus while having the advantage of being in a textual format that is both easy to reason about & incorporate into large language model (LLM) prompts, but also typically require less multimedia content to be inserted into the multimodal LLM context window, where typical co
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
<b>동영상 기반 VLM 환각</b>에 대한 실험은 제공되지 않았습니다.

<b>본론</b>
1. <b>Video Enriched Retrieval Augmented Generation Using Aligned Video Captions</b>: 이 작업에서는 동영상을 텍스트 형식의 “aligned visual captions”으로 변환하여 RAG 기반 챗봇 시스템에 통합하는 방법을 제안합니다[2405.17706v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• RoboJudge: Multimodal Language Models as Judges for Embodied Video Generation (2026) [2610.27782]
• A Comprehensive Survey of Hallucination in Large Language, Image, Video and Audio Foundation Models (2024) [2405.09589]
• 🧜Siren’s Song in the AI Ocean: A Survey on Hallucination in Large Language Models (2025) [2309.01219]
• Models See Hallucinations: Evaluating the Factuality in Video Captioning (2023) [2303.02961]

######## K37 | 실제 로봇으로 실험한 VLA 연구만 알려줘 | route direct_answer/B
  조건 0: 선별: 실제 로봇 실험만
--- [문서 1] [Distance: 0.2782] [발행일: 2026-06-11] [2606.13578v2] LabVLA: Grounding Vision-Language-Action Models in Scientific Laboratories [초록] Scientific laboratories increasingly rely on AI systems to reason about experiments, but the physical act of doing science remains largely outside their reach. AI can help read literature, generate hypotheses, and plan protocols, yet the execution of those protocols at the bench still requires a human operator. Vision-Language-Action (VLA) models provide one possible interface between written protocols and robot execution, but existing policies are trained mostly on household and tabletop demonstrations and rarely encounter the instruments, transparent li
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
<b>Vision-Language-Action (VLA)</b> 모델은 실험 프로토콜과 로봇 동작 사이의 인터페이스를 제공하지만, 실제 과학 laboratory 환경에서 직접 수행한 사례는 제한적입니다.

<b>본론</b>
1. <b>LabUtopia</b>: LabVLA 모델을 사용하여 Bench 위에서 실제로 실행된 VLA 연구가 평가되었습니다[2606.13578v2].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models (2026) [2606.10568]
• ReplanVLM: Replanning Robotic Tasks With Visual Language Models (2024) [2407.21762]
• SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Models (2025) https://doi.org/10.15607/rss.2025.xxi.011
• CoPAL: Corrective Planning of Robot Actions with Large Language Models (2024) [2310.07263]

######## K38 | 벤치마크 말고 실제 서비스 로그로 평가한 RAG 연구 있어? | route direct_answer/B
  조건 0: 선별: 실제 서비스 로그 평가
--- [문서 1] [Distance: 0.3102] [발행일: 2024-12-16] [2412.12364v1] LogBabylon: A Unified Framework for Cross-Log File Integration and Analysis [초록] Logs are critical resources that record events, activities, or messages produced by software applications, operating systems, servers, and network devices. However, consolidating the heterogeneous logs and cross-referencing them is challenging and complicated. Manually analyzing the log data is time-consuming and prone to errors. LogBabylon is a centralized log data consolidating solution that leverages Large Language Models (LLMs) integrated with Retrieval-Augmented Generation (RAG) technology. LogBabylon interprets the log data in a human-readable way 
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>LogBabylon</b>: 로그 데이터를 인간可读하게 해석하고 시스템 성능 및 이상 징후에 대한 통찰 분석을 추가하며, 다양한 로그 소스를 통합해 정확도와 관련성을 향상시킵니다[2412.12364v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• Trace-LogVector-Based Relational Retrieval for Conversational System Log Analysis (2026) https://doi.org/10.3390/s26061806
• Generating Q&amp;A Benchmarks for RAG Evaluation in Enterprise Settings (2025) https://doi.org/10.18653/v1/2025.acl-industry.33

######## K39 | LLM 워터마크 연구 중 공격에 강건성을 수치로 보고한 것 알려줘 | route direct_answer/B
  조건 0: 선별: 강건성 수치 보고
--- [문서 1] [Distance: 0.4072] [발행일: 2026-10-06] [2610.08668v1] Semantic Behavioral Watermarking: Paraphrase-Robust and Forgery-Resistant Provenance for LLM Agents [초록] Behavioral watermarking embeds an owner identifier in an LLM agent's high-level action choices, giving provenance without touching output tokens. Prior agent watermarks break in two ways. First, all three prior schemes bind the watermark to the exact action symbol, so renaming a tool desynchronizes decoding even when the observation is untouched; in AgentMark's own robustness test, paraphrasing the observation alone drops bit-recovery to 16.8%. Second, every prior agent watermark studies only removal: none asks whether an adversar
=== 답
<b>서론</b>
LLM 워터마크는 모델 출력을 변조하거나 복제하는 공격에 대해 강건해야 합니다. 특히 <b>paraphrase</b>와 같은 관찰 재작성이나 툴 이름 변경과 같이 행동 선택 자체를 바꾸더라도 소유자 식별자를 유지할 수 있어야 하며, 이러한 상황에서의 검출률과 위양성률을 정량적으로 보고한 연구가 필요합니다.

<b>본론</b>
1. <b>Semantic Behavioral Watermarking (SBW)</b>: SBW는 역사 조건화 하에서 의미 행동 클러스터에 워터마크를 삽입하고, 공개된 클러스트 대신 키드 충돌‑저항 빈을 사용해 새로운 버킷 할당을 무작위 오라클 모델에서 예측 불가능하게 만듭니다. 이 접근법은 툴 이름 변경이나 관찰 paraphrase에도 검출률이 유지됩니다[2610.08668v1].

<b>결론</b>
제공된 문서에 따르면, Semantic Behavioral Watermarking (SBW)이 공격 강건성을 수치로 보고한 유일한 LLM 워터마크 연구입니다.

######## K40 | 지식 증류 연구 중 학생 모델이 교사보다 나아진 사례 알려줘 | route direct_answer/B
  조건 0: 선별: 학생이 교사보다 나음
--- [문서 1] [Distance: 0.3560] [발행일: 2026-05-29] [2605.31159v1] Trust-Region Behavior Blending for On-Policy Distillation [초록] On-policy distillation (OPD) trains a student on prefixes sampled from its own policy while matching a stronger teacher. This addresses the prefix mismatch of offline distillation, but early student rollouts can still be poor, placing teacher supervision on weak or low-quality prefixes. We propose Trust-Region behavior Blending (TRB), a warmup method that replaces the early rollout policy with the closest-to-teacher behavior policy inside a student-centered KL trust region, while keeping the per-prefix reverse-KL OPD loss unchanged. The KL budget is annealed to zero, so t
--- [문서 2] [Distance: 0.4175] [발행일: 2026-07-16] [2607.15161v1] On-Policy Delta Distillation [초록] On-policy distillation is an alternative post-training method in reinforcement learning that alleviates the constraints imposed by reward models by providing token-level supervision from a teacher model. Although on-policy distillation has been studied and applied across various settings, its fundamental design remains underexplored. In this paper, we introduce a new distillation reward, termed the delta signal, instead of directly imitating the teacher's output distribution. The delta signal is defined as the difference between the teacher model and its base model prior to instruction tuning for rea
--- [문서 3] [Distance: 0.3789] [발행일: 2026-10-14] [2610.20572v1] Recovering Reliable Supervision via Critique-Guided On-Policy Distillation [초록] On-policy distillation (OPD) trains a student model on its own rollouts with token-level supervision from a teacher, assuming that the teacher can reach a correct answer from any prefix the student writes. We call this property the recoverability of the teacher and show it fails on incorrect rollouts: the teacher follows student errors, although it recognizes them. We propose CriticOPD, using error recognition to restore recoverability. The teacher critiques an incorrect rollout, allowing the student to rewrite its solution following the error. The result
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
<b>지식 증류</b>(knowledge distillation)는 학생 모델에 교사의 지식을 전달하는 과정이며, 특히 <b>온‑폴리시(distillation)</b> 방식에서는 초기 단계에서 학생들이 교사보다 성능이 낮을 수 있어 개선 방법이 필요합니다.

<b>본론</b>
1. <b>Trust-Region behavior Blending (TRB)</b>: 온‑폴리시 증류의 초기 롤아웃 정책을 교사와 가장 가까운 행동 정책으로 교체하고, KL 신뢰 영역 내에서 손실을 유지하며, KL 예산은 서서히 0 으로 감소시켜 최종적으로 순수 학생 rollout 로 복귀한다[2605.31159v1].
2. <b>On-Policy Delta Distillation (OPD²)</b>: 교사 모델과 기본 모델을 비교한 차이 신호(delta signal)를 새로운 증류 보상으로서 도입하고, 이를 통해 기존 온‑폴리시 증류를 크게 개선하며 수학·과학·코드 추론 벤치마크에서 일관된 성능 향상을 보인다[2607.15161v1].
3. <b>CriticOPD</b>: 교사가 학생의 잘못된 롤아웃을 비판함으로써 회복성을 복원하고, 오류를 인식해 학생들이 해법을 재작성하도록 유도한다; 두 Qwen3 모델과 여섯 개의 수학 추론 벤치마크에서 기존 OPD보다 성능이 향상되며 경쟁 문제에서 가장 큰 개선을 보인다[2610.20572v1].

<b>결론</b>
제공된 문서들에 따르면, 지식 증류 연구에서 학생 모델이 교사보다 나은 사례는 존재하지 않습니다. 오히려 초기 학생 롤아웃은 여전히 품질이 낮아 교사의 감독을 약하거나 낮은 품질의 접두사에 의존하게 된다고 보고됩니다 [2605.31159v1]. 또한, CriticOPD가 OPD를 개선하지만 이는 교사가 학생 오류를 인식함에도 불구하고 그 오류를 따라가는 경우로 설명되며, 이는 교사의 신뢰성 회복이 실패하는 상황을 나타냅니다 [2610.20572v1]. 따라서 현재까지의 연구 결과들은 학생 모델이 교사보다 뛰어난 성능을 보인 사례를 제시하지 못하고 있습니다.

📎 <b>DB 밖에서 찾은 관련 논문</b> (OpenAlex 검색 · 내용은 요약하지 않음)
• On the Efficacy of Knowledge Distillation (2019) [1910.01348]
• Knowledge Distillation with the Reused Teacher Classifier (2022) [2203.14001]
• Learning Student-Friendly Teacher Networks for Knowledge Distillation (2021) [2102.07650]
• Teacher-student collaborative knowledge distillation for image classification (2022) https://doi.org/10.1007/s10489-022-03486-4

