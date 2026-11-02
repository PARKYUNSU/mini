# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)

## H_F03 — 하이브리드 검색에서 RRF로 합칠 때 k 값을 바꾸면 결과가 얼마나 흔들리는지, 그리고 학습된 가중치 융합이 RRF보다 나은 조건을 다룬 논문이 있는가.

### 인용 블록

[문서 1]
[Distance: 0.3244]
[발행일: 2022-10-21]
[2210.11934v2] An Analysis of Fusion Functions for Hybrid Retrieval
[초록] We study hybrid search in text retrieval where lexical and semantic search are fused together with the intuition that the two are complementary in how they model relevance. In particular, we examine fusion by a convex combination (CC) of lexical and semantic scores, as well as the Reciprocal Rank Fusion (RRF) method, and identify their advantages and potential pitfalls. Contrary to existing studies, we find RRF to be sensitive to its parameters; that the learning of a CC fusion is generally agnostic to the choice of score normalization; that CC outperforms RRF in in-domain and out-of-domain settings; and finally, that CC is sample efficient, requiring only a small set of training examples to tune its only parameter to a target domain.

## **5 ANALYSIS OF RECIPROCAL RANK FUSION**  
Chen _et al._ [5] show that RRF performs better and more reliably than a convex combination of normalized scores. RRF is computed as follows:  
**==> picture [285 x 23] intentionally omitted <==**
[문서 2]
[Distance: 0.3725]
[발행일: 2026-04-15]
[2604.13728v1] Hybrid Retrieval for COVID-19 Literature: Comparing Rank Fusion and Projection Fusion with Diversity Reranking
[초록] We present a hybrid retrieval system for COVID-19 scientific literature, evaluated on the TREC-COVID benchmark (171,332 papers, 50 expert queries). The system implements six retrieval configurations spanning sparse (SPLADE), dense (BGE), rank-level fusion (RRF), and a projection-based vector fusion (B5) approach. RRF fusion achieves the best relevance (nDCG@10 = 0.828), outperforming dense-only by 6.1% and sparse-only by 14.9%. Our projection fusion variant reaches nDCG@10 = 0.678 on expert queries while being 33% faster (847 ms vs. 1271 ms) and producing 2.2x higher ILD@10 than RRF. Evaluation across 400 queries -- including expert, machine-generated, and three paraphrase styles -- shows that B5 delivers the largest relative gain on keyword-heavy reformulations (+8.8%), although RRF remains best in absolute nDCG@10. On expert queries, MMR reranking increases intra-list diversity by 23.8-24.5% at a 20.4-25.4% nDCG@10 cost. Both fusion pipelines evaluated for latency remain below the sub-2 s target across all query sets. The system is deployed as a Streamlit web application backed by Pinecone serverless indices.

## _B. Hybrid Fusion Strategies_  
Luan et al. [9] demonstrate that combining sparse and dense representations improves retrieval effectiveness. Reciprocal Rank Fusion (RRF) [7] provides a simple, effective method for merging ranked lists without requiring score normalisation, using the formula RRF( _d_ ) =[�] _r∈R k_ +rank _wrr_ ( _d_ )[where] _[k]_[= 60][.]

### 문장

- s1: Our projection fusion variant achieves nDCG@10 = 0.678 on expert queries, is 33% faster (847 ms vs. 1271 ms), and produces 2.2× higher ILD@10 than RRF. [2604.13728v1]
- s2: 특히, 이 논문은 어휘 점수와 의미 점수의 볼록 결합(CC)을 통한 융합과 상호 순위 융합(RRF) 방법을 검토하고, 각각의 장점과 잠재적인 함정을 파악한다. [2210.11934v2]
- s3: RRF는 파라미터에 매우 민감하여 k 값을 변경하면 결과가 크게 흔들리는 반면, 학습된 가중치 융합(CC)은 점수 정규화 선택과 무관하게 도메인 내·외에서 RRF보다 우수한 성능을 보이며 소량의 훈련 데이터로도 튜닝이 가능하다[2210.11934v2].
- s4: 또한 COVID-19 문헌 검색 시스템에서는 RRF가 절대적인 nDCG@10에서 가장 높은 점수를 기록하지만, 투영 융합은 RRF 대비 2.2배 높은 ILD@10와 33% 빠른 처리 속도를 달성한다[2604.13728v1].

## H_F05 — citation precision이 높아도 답 문장이 인용 문서 내용과 다를 수 있다. 인용 정확도와 근거성을 따로 재야 한다고 주장한 연구와 그 측정 방법을 알려줘.

### 인용 블록

[문서 1]
[Distance: 0.3679]
[발행일: 2024-12-23]
[2412.18004v1] Correctness is not Faithfulness in RAG Attributions
[초록] Retrieving relevant context is a common approach to reduce hallucinations and enhance answer reliability. Explicitly citing source documents allows users to verify generated responses and increases trust. Prior work largely evaluates citation correctness - whether cited documents support the corresponding statements. But citation correctness alone is insufficient. To establish trust in attributed answers, we must examine both citation correctness and citation faithfulness. In this work, we first disentangle the notions of citation correctness and faithfulness, which have been applied inconsistently in previous studies. Faithfulness ensures that the model's reliance on cited documents is genuine, reflecting actual reference use rather than superficial alignment with prior beliefs, which we call post-rationalization. We design an experiment that reveals the prevalent issue of post-rationalization, which undermines reliable attribution and may result in misplaced trust. Our findings suggest that current attributed answers often lack citation faithfulness (up to 57 percent of the citations), highlighting the need to evaluate correctness and faithfulness for trustworthy attribution in language models.

The second condition, often referred to as the “correctness” of the citation, has been a focal point in previous studies evaluating RAG attribution. Correctness usually tests whether a statement is supported by the attributed document (measured by NLI models). However, while correctness is a necessary condition for faithfulness, it is insufficient. For a citation to be deemed faithful, the model must also rely causally on the cited document to generate the answer
[문서 3]
[Distance: 0.4233]
[발행일: 2026-06-24]
[2606.26449v1] ProvenAI: Provenance-Native Traces of Evidence in Generated Answers
[초록] Retrieval-augmented systems routinely present citations alongside generated answers, yet a citation does not confirm that the corresponding source meaningfully shaped the output. This paper introduces ProvenAI, a framework that decomposes transparency in multi-hop question answering into three independently measurable layers: answer correctness, citation fidelity against benchmark supporting evidence, and per-document influence under leave-one-resource-out intervention. Targeting the HotpotQA distractor benchmark through a seven-stage pipeline covering data normalisation, retrieval indexing, citation-aware answer generation, attribution auditing, ablation-based influence estimation, batch evaluation, and interactive inspection, ProvenAI evaluates 7,405 validation examples drawn from a canonical corpus of 509,300 passages. The system achieves 53.53% answer accuracy alongside a mean citation-fidelity score of 71.55%, and a worked example surfaces what we call the citation-influence gap: a clean citation audit co-occurring with a profile in which one cited source registers only weak influence while seven uncited sources demonstrably shift the output. We formalise the relationship between the implemented surface proxy and a token-level KL-divergence target through a stated faithfulness condition, ground the framework in causal-mediation analysis and database-provenance theory, and discuss how the three measurement layers compose with cryptographic provenance architectures emerging in autonomous scientific discovery. ProvenAI establishes that meaningful transparency in retrieval-grounded QA requires traceable links across retrieved, cited, and behaviourally influential evidence as three distinct, independently measured layers.

. The headline observation is that citation fidelity exceeds answer accuracy by a substantial margin (71.55% versus 53.53%): the model frequently identifies and cites the correct supporting titles even on examples where the final answer string is scored as incorrect. This divergence supports the core argument of the paper. Answer correctness and evidence alignment are not interchangeable, and collapsing them into a single score would obscure

### 문장

- s1: Our findings suggest that current attributed answers often lack citation faithfulness (up to 57 percent of the citations), highlighting the need to evaluate correctness and faithfulness for trustworthy attribution in language models. [2412.18004v1]
- s2: 시스템은 정답 정확도 53.53%와 평균 인용 충실도 점수 71.55%를 달성했으며, 작업된 예시는 이 논문이 '인용 영향력 격차'라고 부르는 현상을 드러낸다: 깨끗한 인용 감사와 함께 한 개의 인용된 출처는 약한 영향만을 기록하는 반면, 일곱 개의 인용되지 않은 출처가 출력에 명백하게 영향을 미친다. [2606.26449v1]
- s3: [2412.18004v1]은 현재 속성된 답변 중 최대 57%가 인용 신뢰성을 갖추지 못한다고 보고, 정확성과 신뢰성을 별도로 평가해야 한다고 주장한다[2412.18004v1].
- s4: [2606.26449v1]은 ProvenAI 프레임워크를 통해 정답 정확도(53.53%)와 인용 충실도(71.55%)를 독립적으로 측정하고, 인용 충실도가 정답 정확도를 크게 상회한다는 결과를 제시한다[2606.26449v1].
- s5: 따라서 두 연구 모두 인용 정확도와 근거성을 별도의 지표로 재평가해야 한다는 결론에 동의하지만, [2412.18004v1]은 높은 인용 정확도에도 불구하고 답변 내용이 문서 내용과 다를 수 있음을 강조하고 있다.

## H_F06 — 한국어 질문을 영어 검색어로 번역해 영어 코퍼스를 검색할 때 번역 오류가 검색 성능에 얼마나 영향을 주는지, 다국어 임베딩으로 바로 검색하는 것과 비교한 연구가 있는가.

### 인용 블록

[문서 2]
[Distance: 0.2621]
[발행일: 2026-06-13]
[2606.15345v2] Beyond Monolingual Deep Research: Evaluating Agents and Retrievers with Cross-Lingual BrowseComp-Plus
[초록] Deep research agents are increasingly evaluated on their ability to search for evidence, reason over retrieved sources, and produce grounded answers. Existing browsing benchmarks, however, largely assume that the user's query and the supporting evidence are written in the same language, leaving open whether agentic search systems can operate when relevant evidence appears in another language. We introduce XBCP (Cross-lingual BrowseComp-Plus), a controlled benchmark that preserves the English question-and-answer space of BrowseComp-Plus but varies the languages of the supporting documents. XBCP instantiates two complementary settings: in the cross-lingual setting, each query is paired with evidence in a single assigned language. In the multilingual setting, the full evidence corpus is distributed equally and randomly across 12 languages spanning high-resource and low-resource regimes. We evaluate four deep research agents using sparse and dense multilingual retrievers, measuring answer accuracy, evidence recall, search behavior, calibration, citation fidelity, and oracle retrieval. Results reveal substantial degradation when evidence is translated. Even strong, dense retrievers lose evidence recall, and agents become less calibrated and cite evidence less reliably. Notably, accuracy remains lower even when all gold evidence is supplied directly. These findings suggest that cross-lingual deep research exposes both retrieval failures and an independent, agent-side difficulty in integrating language-mismatched evidence.

. The limitation matters because multilingual and cross-lingual retrieval have long been central concerns in information retrieval, and recent multilingual embedding models have greatly expanded the ability to retrieve across languages (Yu et al., 2024; Zhang et al., 2024, 2025). Most evaluations of these models still treat retrieval as a standalone ranking problem: a query is matched against a fixed collection, and success is measured by documentlevel relevance
[문서 5]
[Distance: 0.3512]
[발행일: 2025-04-04]
[2504.03616v2] Multilingual Retrieval-Augmented Generation for Knowledge-Intensive Task
[초록] Retrieval-augmented generation (RAG) has become a cornerstone of contemporary NLP, enhancing large language models (LLMs) by allowing them to access richer factual contexts through in-context retrieval. While effective in monolingual settings, especially in English, its use in multilingual tasks remains unexplored. This paper investigates the effectiveness of RAG across multiple languages by proposing novel approaches for multilingual open-domain question-answering. We evaluate the performance of various multilingual RAG strategies, including question-translation (tRAG), which translates questions into English before retrieval, and Multilingual RAG (MultiRAG), where retrieval occurs directly across multiple languages. Our findings reveal that tRAG, while useful, suffers from limited coverage. In contrast, MultiRAG improves efficiency by enabling multilingual retrieval but introduces inconsistencies due to cross-lingual variations in the retrieved content. To address these issues, we propose Crosslingual RAG (CrossRAG), a method that translates retrieved documents into a common language (e.g., English) before generating the response. Our experiments show that CrossRAG significantly enhances performance on knowledge-intensive tasks, benefiting both high-resource and low-resource languages.

. The results show that multilingual retrieval brings significant benefits compared to monolingual retrieval or greedy approaches related to query translation. This research shows that a better understanding of RAG-based pipelines beyond English would enable reliable access to information in different languages and cultures

### 문장

- s1: 반면 [2504.03616v2]는 질문 번역(tRAG)과 직접 다국어 검색(MultiRAG)을 비교한 결과, CrossRAG가 지식 집약적 작업에서 기존 방법보다 성능 향상을 보였다고 결론지었습니다.
- s2: 다양한 다국어 RAG 전략의 성능을 평가한다: 질문 번역(tRAG)은 검색 전에 질문을 영어로 번역하고, 다국어 RAG(MultiRAG)는 여러 언어를 직접 대상으로 검색을 수행한다. [2504.03616v2]
- s3: [2606.15345v2]는 교차언어 심층 연구에서 언어 불일치 증거 통합의 어려움을 강조하며, 최근 다국어 임베딩 모델이 언어 간 검색 능력을 크게 확장했다고 보고합니다.
- s4: 이 연구 결과는 다국어 심층 검색이 검색 실패와 언어 불일치 증거를 통합하는 에이전트 측의 독립적인 어려움을 모두 드러낸다는 점을 시사한다. [2606.15345v2]

## H_F08 — LLM-as-a-judge로 0~5점 채점할 때 같은 답을 여러 번 채점하면 점수 분산이 얼마나 되고, 몇 번 평균내야 안정되는지 다룬 논문이 있는가.

### 인용 블록

[문서 2]
[Distance: 0.3119]
[발행일: 2026-06-17]
[2606.19544v1] Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias
[초록] LLM-as-a-Judge has become the dominant evaluation paradigm for language models, but judge validation in practice relies on exact-match agreement, a metric that does not correct for chance and systematically overstates discriminative ability. We present the largest systematic evaluation of LLM-as-a-Judge to date: 21 judges from nine providers across MT-Bench, JudgeBench, and RewardBench, evaluated under three protocols (agreement, consistency, bias audit) over 118 runs and approximately 541,000 individual judgments. Four findings emerge, consistent across the full cohort, including the April 2026 frontier: kappa deflation between exact match and Cohen's kappa is universal (33--41 pp on MT-Bench), judge rankings shift by up to 14 positions across benchmarks, high test--retest reliability (>0.95) coexists with severe position bias (>0.10) in two production-deployed judges (instantiating a consistency--bias paradox), and verbosity bias is small (<0.011) across our cohort under a single pairwise rubric. We distill these into a Minimum Viable Validation Protocol.

# **Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias**  
**Justin D. Norman and Michael U. Rivera and D. Alex Hughes** {justin.norman, michaelrivera, dhughes}@berkeley.edu UC Berkeley School of Information 102 South Hall Drive, Berkeley CA, 94708
[문서 4]
[Distance: 0.2859]
[발행일: 2026-01-06]
[2601.03444v1] Grading Scale Impact on LLM-as-a-Judge: Human-LLM Alignment Is Highest on 0-5 Grading Scale
[초록] Large language models (LLMs) are increasingly used as automated evaluators, yet prior works demonstrate that these LLM judges often lack consistency in scoring when the prompt is altered. However, the effect of the grading scale itself remains underexplored. We study the LLM-as-a-judge problem by comparing two kinds of raters: humans and LLMs. We collect ratings from both groups on three scales and across six benchmarks that include objective, open-ended subjective, and mixed tasks. Using intraclass correlation coefficients (ICC) to measure absolute agreement, we find that LLM judgments are not perfectly consistent across scales on subjective benchmarks, and that the choice of scale substantially shifts human-LLM agreement, even when within-group panel reliability is high. Aggregated over tasks, the grading scale of 0-5 yields the strongest human-LLM alignment. We further demonstrate that pooled reliability can mask benchmark heterogeneity and reveal systematic subgroup differences in alignment across gender groups, strengthening the importance of scale design and sub-level diagnostics as essential components of LLM-as-a-judge protocols.

**Grading consistency of LLM judges.** Beyond accuracy or bias, a growing body of work has analyzed judges’ self-consistency, whether an LLM’s evaluations remain stable when scoring is repeated or slightly perturbed, and found worrying patterns such as non-transitive preference cycles in pairwise comparisons (Lee et al., 2025; Xu et al., 2025)

### 문장

- s1: [2606.19544v1]는 LLM-as-a-Judge의 재현성(&gt;0.95)과 편향 문제를 다루지만, 점수 분산이나 평균 횟수에 대한 정량적 분석은 포함하지 않습니다.
- s2: Four findings emerge, consistent across the full cohort, including the April 2026 frontier: kappa deflation between exact match and Cohen's kappa is universal (33--41 pp on MT-Bench), judge rankings shift by up to 14 positions across benchmarks, high test--retest reliability (>0.95) coexists with severe position bias (>0.10) in two production-deployed judges (instantiating a consistency--bias paradox), and verbosity bias is small (<0.011) across our cohort under a single pairwise rubric. [2606.19544v1]
- s3: 또한 [2601.03444v1]는 0-5점 척도에서 인간·LLM 일치도가 높고, ICC를 이용해 절대 일치를 측정하여 LLM 판단이 완전히 일관되지 않음을 보여줍니다.
- s4: 작업에 대해 집계할 때, 0~5 점의 평가 척도가 인간과 LLM 간의 정렬을 가장 강하게 제공한다. [2601.03444v1]

## H_G01 — RAG 리랭킹 관련 논문들을 바탕으로 아직 덜 연구된 빈틈 3가지 제안해줘

### 인용 블록

[문서 1]
[Distance: 0.2681]
[발행일: 2024-05-28]
[2405.18414v1] Don't Forget to Connect! Improving RAG with Graph-based Reranking
[초록] We introduce G-RAG, a reranker based on graph neural networks (GNNs) between the retriever and reader in RAG. G-RAG outperforms state-of-the-art approaches while having smaller computational footprint. Additionally, we assess the performance of PaLM 2 as a reranker and find it to significantly underperform G-RAG.
[문서 2]
[Distance: 0.3304]
[발행일: 2025-08-12]
[2508.08742v2] SciRerankBench: Benchmarking Rerankers Towards Scientific Retrieval-Augmented Generated LLMs
[초록] In this work, we present a Scientific Rerank-oriented RAG Benchmark (SciRerankBench), for evaluating rerankers within RAG-LLMs systems, spanning five scientific subjects. Through systematic evaluation of 13 widely used rerankers on five families of LLMs, we provide detailed insights into their relative strengths and limitations.
[문서 3]
[Distance: 0.2630]
[발행일: 2025-08-13]
[2508.09497v1] From Ranking to Selection: A Simple but Efficient Dynamic Passage Selector for Retrieval Augmented Generation
[초록] To address this, we introduce the Dynamic Passage Selector (DPS), a novel reranking framework that treats passage selection as a supervised learning problem. Notably, on the challenging MuSiQue dataset, DPS improves the F1-score by 30.06% and 15.4% over strong baselines like Qwen3-reranker and RankingGPT, respectively.

### 문장

- s1: [2508.09497v1]은 DPS가 MuSiQue 데이터셋에서 Qwen3-reranker와 RankingGPT보다 각각 30.06%와 15.4% 높은 F1-score를 달성했다고 보고합니다.
- s2: [2405.18414v1]은 G-RAG가 최신 접근법을 능가하면서도 계산 부피가 작으며, PaLM 2를 리랭커로 사용할 경우 성능이 크게 떨어지는 것을 확인했습니다.
- s3: 13개의 널리 사용되는 재랭커를 다섯 가지 LLM 계열에 대해 체계적으로 평가함으로써 그 상대적인 강점과 한계에 대한 상세한 통찰을 제공합니다. [2508.08742v2]
- s4: 또한 이 논문은 PaLM 2를 리랭커로 사용할 때 성능을 평가하고, 그 결과가 G-RAG보다 현저히 낮음을 확인하였다. [2405.18414v1]
- s5: [2508.08742v2]는 과학 분야에 특화된 SciRerankBench를 통해 13개의 널리 사용되는 리랭커를 평가하고, 그 상대적 강점과 한계를 제시했습니다.
- s6: 특히 어려운 MuSiQue 데이터셋에서 DPS는 강력한 베이스라인인 Qwen3-reranker와 RankingGPT에 비해 각각 F1 점수를 30.06%와 15.4% 향상시켰다. [2508.09497v1]

## H_G02 — LLM 에이전트 메모리 연구들을 읽고 실제 서비스에 적용할 때 문제점을 정리해줘

### 인용 블록

[문서 1]
[Distance: 0.3032]
[발행일: 2026-06-23]
[2606.24775v1] Are We Ready For An Agent-Native Memory System?
[초록] In this paper, we present a systematic experimental study of agent memory from a data management perspective. Finally, we reveal cost-performance trade-offs under realistic workloads, showing localized maintenance is more cost-efficient than global reorganization. Based on these findings, we identify promising directions towards building truly agent-native memory systems.
[문서 2]
[Distance: 0.3350]
[발행일: 2026-06-17]
[2606.18829v1] GateMem: Benchmarking Memory Governance in Multi-Principal Shared-Memory Agents
[초록] We introduce GateMem, a benchmark for multi-principal shared-memory agents. Long-context prompting often yields the best governance score at high token cost, while retrieval-based and external-memory methods reduce cost yet still leak unauthorized or deleted information. These results show current memory agents remain far from reliable shared institutional deployment.
[문서 3]
[Distance: 0.3373]
[발행일: 2026-02-17]
[2603.02240v1] SuperLocalMemory: Privacy-Preserving Multi-Agent Memory with Bayesian Trust Defense Against Memory Poisoning
[초록] We present SuperLocalMemory, a local-first memory system for multi-agent AI that defends against OWASP ASI06 memory poisoning through architectural isolation and Bayesian trust scoring, while personalizing retrieval through adaptive learning-to-rank -- all without cloud dependencies or LLM inference calls.

### 문장

- s1: 이러한 결과를 바탕으로 이 논문은 진정한 에이전트 네이티브 메모리 시스템을 구축하기 위한 유망한 방향성을 제시합니다. [2606.24775v1]
- s2: 또한 [2603.02240v1]은 클라우드 의존성 없이 지역 우선 메모리 시스템을 통해 OWASP ASI06 메모리 중독 공격에 방어하고 개인화된 검색을 가능하게 한다고 보고, 이는 프라이버시 보호 측면에서의 해결책을 제시한다[2603.02240v1].
- s3: 먼저 [2606.24775v1]은 현실적인 워크로드 하에서 지역적 유지보수가 전역 재구성보다 비용 효율성이 높음을 보여주며, 이는 에이전트 네이티브 메모리 시스템 구축 방향성을 제시한다[2606.24775v1].
- s4: SuperLocalMemory는 다중 에이전트 AI를 위한 로컬 퍼스트 메모리 시스템으로, 구조적 격리와 베이지안 신뢰 점수를 통해 OWASP ASI06 메모리 중독을 방어하고 적응형 랭킹 학습을 통해 검색을 개인화하면서도 클라우드 의존성이나 LLM 추론 호출 없이 구현됩니다. [2603.02240v1]
- s5: 그러나 [2606.18829v1]는 현재 메모리 에이전트가 아직 신뢰할 수 있는 공유 기관 배포에 이르렀다고 보기 어렵다고 결론지으며, 특히 리트리벌 기반 및 외부 메모리 방법은 비용은 줄이지만 무단 또는 삭제된 정보를 누출한다는 한계를 지적한다[2606.18829v1].
- s6: 이 결과는 현재 메모리 에이전트가 신뢰할 수 있는 공유 기관 배포에 아직 멀어 있음을 보여준다. [2606.18829v1]

## H_G03 — 환각 탐지 연구들을 방법별(내부 상태 · 샘플링 일관성 · 외부 검증)로 나눠서 정리해줘

### 인용 블록

[문서 1]
[Distance: 0.2759]
[발행일: 2023-10-22]
[2310.18344v1] Chainpoll: A high efficacy method for LLM hallucination detection
[초록] Our findings indicate that ChainPoll outperforms in all RealHall benchmarks, achieving an overall AUROC of 0.781. This surpasses the next best theoretical method by 11% and exceeds industry standards by over 23%. Additionally, ChainPoll is cost-effective and offers greater transparency than other metrics. We introduce two novel metrics to assess LLM hallucinations: Adherence and Correctness.
[문서 2]
[Distance: 0.2457]
[발행일: 2026-06-04]
[2606.06748v2] Evidence Graph Consistency in Retrieval-Augmented Generation: A Model-Dependent Analysis of Hallucination Detection
[초록] We propose Evidence Graph Consistency (EGC), a framework that constructs a local evidence graph per response and computes five structural consistency measures as hallucination indicators. Evaluated on the full question answering split of RAGTruth across six LLMs (5,767 responses), EGC reveals a consistent model-family split: graph consistency features show the expected diagnostic direction for h…
[문서 3]
[Distance: 0.2598]
[발행일: 2025-12-29]
[2512.23547v1] Lie to Me: Knowledge Graphs for Robust Hallucination Self-Detection in LLMs
[초록] Specifically, we propose a simple yet powerful approach that enriches hallucination self-detection by (i) converting LLM responses into knowledge graphs of entities and relations, and (ii) using these graphs to estimate the likelihood that a response contains hallucinations. Compared to standard self-detection methods and SelfCheckGPT, a state-of-the-art approach, our method achieves up to 16% r…
[문서 4]
[Distance: 0.2351]
[발행일: 2025-12-26]
[2512.22396v1] HalluMat: Detecting Hallucinations in LLM-Generated Materials Science Content Through Multi-Stage Verification
[초록] To address this, we introduce HalluMatData, a benchmark dataset for evaluating hallucination detection methods, factual consistency, and response robustness in AI-generated materials science content. By utilizing HalluMatDetector verification pipeline, we reduce hallucination rates by 30% compared to standard LLM outputs.
[문서 6]
[Distance: 0.2985]
[발행일: 2024-12-17]
[2412.15264v3] ReXTrust: A Model for Fine-Grained Hallucination Detection in AI-Generated Radiology Reports
[초록] We present ReXTrust, a novel framework for fine-grained hallucination detection in AI-generated radiology reports. Our results show that white-box approaches leveraging model hidden states can provide reliable hallucination detection for medical AI systems, potentially improving the safety and reliability of automated radiology reporting.
[문서 8]
[Distance: 0.3136]
[발행일: 2026-02-20]
[2602.18145v1] Detecting Contextual Hallucinations in LLMs with Frequency-Aware Attention
[초록] Inspired by signal processing, we introduce a frequency-aware perspective on attention by analyzing its variation during generation. Experiments on the RAGTruth and HalluRAG benchmarks show that our approach achieves performance gains over verification-based, internal-representation-based, and attention-based methods across models and tasks.
[문서 9]
[Distance: 0.3941]
[발행일: 2025-07-08]
[2507.06196v2] UQLM: A Python Package for Uncertainty Quantification in Large Language Models
[초록] We introduce UQLM, a Python package for LLM hallucination detection using state-of-the-art uncertainty quantification (UQ) techniques. This toolkit offers a suite of UQ-based scorers that compute response-level confidence scores ranging from 0 to 1.

### 문장

- s1: EGC는 RAGTruth 데이터셋의 전체 질문‑답변 분할에서 일관된 모델‑가족별 그래프 일관성 특징을 보이며 진단 방향이 기대대로 나타난다[2606.06748v2].
- s2: 표준 자체 탐지 방법과 최첨단 접근법인 SelfCheckGPT와 비교했을 때, 본 연구의 방법은 최대 16%까지 성능을 향상시켰습니다. [2512.23547v1]
- s3: HalluMat은 HalluMatData 벤치마크와 검증 파이프라인을 이용해 환각률을 30% 감소시킨다[2512.22396v1].
- s4: 신호 처리에서 영감을 받아 생성 과정 중 주의 메커니즘의 변화를 분석함으로써 주파수 인식 관점을 도입한다. [2602.18145v1]
- s5: 환각 탐지 연구들은 방법별로 성능 차이가 뚜렷하게 나타난다: ChainPoll은 모든 RealHall 벤치마크에서 AUROC 0.781을 달성해 다음 이론적 방법을 11% 상회하고 산업 표준보다 23% 이상 우수하다[2310.18344v1].
- s6: Frequency-Aware Attention은 RAGTruth와 HalluRAG 벤치마크에서 검증 기반, 내부 표현 기반, 주의 기반 방법보다 전반적인 성능 향상을 보인다[2602.18145v1].
- s7: HalluMatDetector 검증 파이프라인을 활용함으로써 표준 LLM 출력에 비해 환각 발생률을 30% 감소시켰다. [2512.22396v1]
- s8: ReXTrust는 화이트박스 접근법으로 모델 숨겨진 상태를 활용해 의료 AI 시스템에서 신뢰할 수 있는 탐지를 제공한다[2412.15264v3].
- s9: UQLM은 응답 수준 신뢰도 점수(0~1)를 제공하는 불확실성 정량화 툴킷을 제공한다[2507.06196v2].
- s10: 본 연구에서는 AI가 생성한 방사선학 보고서에서 미세한 환각을 탐지하기 위한 새로운 프레임워크인 ReXTrust를 제시한다. [2412.15264v3]
- s11: 이 논문의 연구 결과는 ChainPoll이 모든 RealHall 벤치마크에서 우수한 성능을 보이며 전체 AUROC가 0.781에 달함을 보여줍니다. [2310.18344v1]
- s12: Lie to Me는 표준 자기탐지 및 SelfCheckGPT 대비 최대 16% 성능 향상을 기록한다[2512.23547v1].
- s13: Evaluated on the full question answering split of RAGTruth across six LLMs (5,767 responses), EGC reveals a consistent model-family split: graph consistency features show the expected diagnostic direction for h… [2606.06748v2]
- s14: 이 툴킷은 0에서 1까지의 범위를 갖는 응답 수준의 신뢰도 점수를 계산하는 일련의 불확실성 정량화(UQ) 기반 스코어를 제공합니다. [2507.06196v2]

## H_G04 — RAG 평가 방법들을 비교표처럼 정리하고 어떤 상황에 뭘 쓰면 좋은지 추천해줘

### 인용 블록

[문서 1]
[Distance: 0.2215]
[발행일: 2025-04-10]
[2504.07803v1] A System for Comprehensive Assessment of RAG Frameworks
[초록] Retrieval Augmented Generation (RAG) has emerged as a standard paradigm for enhancing the factual accuracy and contextual relevance of Large Language Models (LLMs) by integrating retrieval mechanisms. However, existing evaluation frameworks fail to provide a holistic black-box approach to assessing RAG systems, especially in real-world deployment scenarios. To address this gap, we introduce SCARF (System for Comprehensive Assessment of RAG Frameworks), a modular and flexible evaluation framework designed to benchmark deployed RAG applications systematically. SCARF provides an end-to-end, black-box evaluation methodology, enabling a limited-effort comparison across diverse RAG frameworks. Our framework supports multiple deployment configurations and facilitates automated testing across vector databases and LLM serving strategies, producing a detailed performance report. Moreover, SCARF integrates practical considerations such as response coherence, providing a scalable and adaptable solution for researchers and industry professionals evaluating RAG applications. Using the REST APIs interface, we demonstrate how SCARF can be applied to real-world scenarios, showcasing its flexibility in assessing different RAG frameworks and configurations. SCARF is available at GitHub repository.

## _B. Related Frameworks_  
In this section, we examine several promising tools for RAG evaluation, assessing each one based on the key features described in the preceding discussion. By systematically analyzing how each tool addresses these criteria, we highlight their respective strengths, limitations, and potential gaps—thereby providing a clear perspective on the current state of RAG evaluation practices.
[문서 4]
[Distance: 0.3612]
[발행일: 2025-08-13]
[2510.00001v1] Methodological Framework for Quantifying Semantic Test Coverage in RAG Systems
[초록] Reliably determining the performance of Retrieval-Augmented Generation (RAG) systems depends on comprehensive test questions. While a proliferation of evaluation frameworks for LLM-powered applications exists, current practices lack a systematic method to ensure these test sets adequately cover the underlying knowledge base, leaving developers with significant blind spots. To address this, we present a novel, applied methodology to quantify the semantic coverage of RAG test questions against their underlying documents. Our approach leverages existing technologies, including vector embeddings and clustering algorithms, to create a practical framework for validating test comprehensiveness. Our methodology embeds document chunks and test questions into a unified vector space, enabling the calculation of multiple coverage metrics: basic proximity, content-weighted coverage, and multi-topic question coverage. Furthermore, we incorporate outlier detection to filter irrelevant questions, allowing for the refinement of test sets. Experimental evidence from two distinct use cases demonstrates that our framework effectively quantifies test coverage, identifies specific content areas with inadequate representation, and provides concrete recommendations for generating new, high-value test questions. This work provides RAG developers with essential tools to build more robust test suites, thereby improving system reliability and extending to applications such as identifying misaligned documents.

## **RAG-Specific Evaluation**

For retrieval–augmented generation (RAG) evaluation, two recent frameworks are particularly influential: **RAGAS** (Sharma et al. 2024) and **ARES** (Zhang et al. 2023). RAGAS introduces an end-to-end pipeline for automatically assessing RAG systems through language-model–based judges that approximate human ratings on several axes, including _answer relevance_ , _faithfulness to the retrieved context_ , and _context precision/recall_
[문서 5]
[Distance: 0.3656]
[발행일: 2024-08-15]
[2408.08067v2] RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation
[초록] Despite Retrieval-Augmented Generation (RAG) showing promising capability in leveraging external knowledge, a comprehensive evaluation of RAG systems is still challenging due to the modular nature of RAG, evaluation of long-form responses and reliability of measurements. In this paper, we propose a fine-grained evaluation framework, RAGChecker, that incorporates a suite of diagnostic metrics for both the retrieval and generation modules. Meta evaluation verifies that RAGChecker has significantly better correlations with human judgments than other evaluation metrics. Using RAGChecker, we evaluate 8 RAG systems and conduct an in-depth analysis of their performance, revealing insightful patterns and trade-offs in the design choices of RAG architectures. The metrics of RAGChecker can guide researchers and practitioners in developing more effective RAG systems. This work has been open sourced at https://github.com/amazon-science/RAGChecker.

## **2.2 Evaluation of RAG**  
Existing evaluation practices for RAG systems can be categorized into two main approaches: evaluating essential capabilities of generators only and assessing end-to-end performance of RAG systems.

### 문장

- s1: SCARF는 다양한 RAG 프레임워크를 비교하기 위해 모듈화되고 유연한 평가 프레임워크를 제공하며, REST API 인터페이스를 통해 실제 시나리오에서 적용 가능성을 보여준다[2504.07803v1].
- s2: RAGChecker는 검색 및 생성 모듈에 대한 정밀한 진단 메트릭을 포함하고 있어 인간 판단과의 상관관계가 다른 지표보다 현저히 높음을 확인했다[2408.08067v2].
- s3: 검색 증강 생성(RAG) 시스템의 성능을 신뢰성 있게 결정하려면 포괄적인 테스트 질문이 필요합니다. [2510.00001v1]
- s4: REST API 인터페이스를 활용하여 이 논문은 SCARF가 실제 시나리오에 적용되는 방법을 보여주며, 다양한 RAG 프레임워크와 구성을 평가하는 데 있어 그 유연성을 입증한다. [2504.07803v1]
- s5: 본 논문에서는 검색 및 생성 모듈 모두에 대한 진단 지표를 통합한 정밀 평가 프레임워크인 RAGChecker를 제안한다. [2408.08067v2]
- s6: 또한, 새로운 방법론은 RAG 테스트 질문의 의미적 커버리지를 정량화하고, 부적절하게 표현된 콘텐츠 영역을 식별하여 새로운 고부가가치 테스트 질문 생성에 대한 구체적인 권장사항을 제공한다[2510.00001v1].

## H_H01 — retreival augmented generaton 최신 논문 요약해줘

### 인용 블록

[문서 1]
[Distance: 0.1361]
[발행일: 2024-10-03]
[2410.12837v1] A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions
[초록] This paper presents a comprehensive study of Retrieval-Augmented Generation (RAG), tracing its evolution from foundational concepts to the current state of the art. RAG combines retrieval mechanisms with generative language models to enhance the accuracy of outputs, addressing key limitations of LLMs. The study explores the basic architecture of RAG, focusing on how retrieval and generation are integrated to handle knowledge-intensive tasks. A detailed review of the significant technological advancements in RAG is provided, including key innovations in retrieval-augmented language models and applications across various domains such as question-answering, summarization, and knowledge-based tasks. Recent research breakthroughs are discussed, highlighting novel methods for improving retrieval efficiency. Furthermore, the paper examines ongoing challenges such as scalability, bias, and ethical concerns in deployment. Future research directions are proposed, focusing on improving the robustness of RAG models, expanding the scope of application of RAG models, and addressing societal implications. This survey aims to serve as a foundational resource for researchers and practitioners in understanding the potential of RAG and its trajectory in natural language processing.

## **A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions**  
_Shailja Gupta (Carnegie Mellon University, USA) Rajesh Ranjan (Carnegie Mellon University, USA) Surya Narayan Singh (BIT Sindri, India)_
[문서 2]
[Distance: 0.2554]
[발행일: 2023-12-18]
[2312.10997v5] Retrieval-Augmented Generation for Large Language Models: A Survey
[초록] Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes. Retrieval-Augmented Generation (RAG) has emerged as a promising solution by incorporating knowledge from external databases. This enhances the accuracy and credibility of the generation, particularly for knowledge-intensive tasks, and allows for continuous knowledge updates and integration of domain-specific information. RAG synergistically merges LLMs' intrinsic knowledge with the vast, dynamic repositories of external databases. This comprehensive review paper offers a detailed examination of the progression of RAG paradigms, encompassing the Naive RAG, the Advanced RAG, and the Modular RAG. It meticulously scrutinizes the tripartite foundation of RAG frameworks, which includes the retrieval, the generation and the augmentation techniques. The paper highlights the state-of-the-art technologies embedded in each of these critical components, providing a profound understanding of the advancements in RAG systems. Furthermore, this paper introduces up-to-date evaluation framework and benchmark. At the end, this article delineates the challenges currently faced and points out prospective avenues for research and development.

. This paper considers both technical paradigms and research methods, summarizing three main research paradigms from over 100 RAG studies, and analyzing key technologies in the core stages of “Retrieval,” “Generation,” and “Augmentation.” On the other hand, current research tends to focus more on methods, lacking analysis and summarization of how to evaluate RAG. This paper comprehensively reviews the downstream tasks, datasets, benchmarks, and evaluation methods applicable to RAG
[문서 3]
[Distance: 0.1998]
[발행일: 2024-05-13]
[2405.07437v2] Evaluation of Retrieval-Augmented Generation: A Survey
[초록] Retrieval-Augmented Generation (RAG) has recently gained traction in natural language processing. Numerous studies and real-world applications are leveraging its ability to enhance generative models through external information retrieval. Evaluating these RAG systems, however, poses unique challenges due to their hybrid structure and reliance on dynamic knowledge sources. To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehensive overview of the evaluation and benchmarks of RAG systems. Specifically, we examine and compare several quantifiable metrics of the Retrieval and Generation components, such as relevance, accuracy, and faithfulness, within the current RAG benchmarks, encompassing the possible output and ground truth pairs. We then analyze the various datasets and metrics, discuss the limitations of current benchmarks, and suggest potential directions to advance the field of RAG benchmarks.

Evaluation of Retrieval-Augmented Generation: A Survey  
9  
In summary, the creation and selection of datasets are crucial for evaluating RAG systems. Datasets tailored for specific metrics or tasks improve evaluation accuracy and guide the development of adaptable RAG systems for real-world information needs.

### 문장

- s1: [2410.12837v1]은 검색 효율성 향상 및 모델 견고성 강화와 같은 최근 연구 돌파구와 미래 방향성을 제시한다[2410.12837v1].
- s2: 그 후 다양한 데이터셋과 지표를 분석하고 현재 벤치마크의 한계를 논의하며 RAG 벤치마크 분야의 발전을 위한 잠재적 방향성을 제안한다. [2405.07437v2]
- s3: 본 조사는 연구자와 실무자가 자연어 처리 분야에서 RAG의 잠재력과 그 발전 경로를 이해하는 데 기초 자원으로 활용되도록 목표로 한다. [2410.12837v1]
- s4: [2312.10997v5]는 RAG 프레임워크의 핵심 구성 요소인 검색·생성·증강 기술에 대한 최신 기술을 강조한다[2312.10997v5].
- s5: [2405.07437v2]은 평가 프로세스와 벤치마크를 종합적으로 검토하고, 특정 메트릭이나 작업에 맞춘 데이터셋이 평가 정확도를 높이는 역할을 한다고 주장한다[2405.07437v2].
- s6: 외부 데이터베이스의 지식을 통합함으로써 유망한 해결책으로 부상한 Retrieval-Augmented Generation(RAG)이 등장했습니다. [2312.10997v5]

## H_H02 — 랭체인 말고 다른 rag 프레임워크 논문 있어?

### 인용 블록

[문서 2]
[Distance: 0.4045]
[발행일: 2024-07-26]
[2407.21059v1] Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks
[초록] Retrieval-augmented Generation (RAG) has markedly enhanced the capabilities of Large Language Models (LLMs) in tackling knowledge-intensive tasks. The increasing demands of application scenarios have driven the evolution of RAG, leading to the integration of advanced retrievers, LLMs and other complementary technologies, which in turn has amplified the intricacy of RAG systems. However, the rapid advancements are outpacing the foundational RAG paradigm, with many methods struggling to be unified under the process of "retrieve-then-generate". In this context, this paper examines the limitations of the existing RAG paradigm and introduces the modular RAG framework. By decomposing complex RAG systems into independent modules and specialized operators, it facilitates a highly reconfigurable framework. Modular RAG transcends the traditional linear architecture, embracing a more advanced design that integrates routing, scheduling, and fusion mechanisms. Drawing on extensive research, this paper further identifies prevalent RAG patterns-linear, conditional, branching, and looping-and offers a comprehensive analysis of their respective implementation nuances. Modular RAG presents innovative opportunities for the conceptualization and deployment of RAG systems. Finally, the paper explores the potential emergence of new operators and paradigms, establishing a solid theoretical foundation and a practical roadmap for the continued evolution and practical deployment of RAG technologies.

- The Modular RAG framework offers exceptional flexibility and extensibility. This paper delves into the new opportunities brought by Modular RAG and provides a thorough discussion on the adaptation and expansion of new methods in different application scenarios, offering guidance for future research directions and practical exploration.
[문서 3]
[Distance: 0.4162]
[발행일: 2025-04-10]
[2504.07803v1] A System for Comprehensive Assessment of RAG Frameworks
[초록] Retrieval Augmented Generation (RAG) has emerged as a standard paradigm for enhancing the factual accuracy and contextual relevance of Large Language Models (LLMs) by integrating retrieval mechanisms. However, existing evaluation frameworks fail to provide a holistic black-box approach to assessing RAG systems, especially in real-world deployment scenarios. To address this gap, we introduce SCARF (System for Comprehensive Assessment of RAG Frameworks), a modular and flexible evaluation framework designed to benchmark deployed RAG applications systematically. SCARF provides an end-to-end, black-box evaluation methodology, enabling a limited-effort comparison across diverse RAG frameworks. Our framework supports multiple deployment configurations and facilitates automated testing across vector databases and LLM serving strategies, producing a detailed performance report. Moreover, SCARF integrates practical considerations such as response coherence, providing a scalable and adaptable solution for researchers and industry professionals evaluating RAG applications. Using the REST APIs interface, we demonstrate how SCARF can be applied to real-world scenarios, showcasing its flexibility in assessing different RAG frameworks and configurations. SCARF is available at GitHub repository.

## _A. Key Feature of RAG Evaluators_  
In this section, we systematically review and analyze the essential characteristics that any framework designed to evaluate framework RAG systems should possess. Our objective is to dissect the key features of these tools and elucidate how they overcome the challenges of assessing RAG’s retrieval and generation components. The main features are presented in Table I. Below, we provide a brief explanation of each column:

### 문장

- s1: 그러나 급속한 발전은 기본 RAG 패러다임을 따라가지 못해 많은 방법들이 "검색 후 생성"이라는 과정 아래 통합되는 데 어려움을 겪고 있다. [2407.21059v1]
- s2: [2407.21059v1]는 기존 "retrieve-then-generate" 패러다임의 한계를 지적하며 모듈형 RAG 프레임워크를 도입하여 새로운 연산자와 패러다임을 탐색합니다.
- s3: 이를 해소하기 위해 이 논문은 모듈형이고 유연한 평가 프레임워크인 SCARF(System for Comprehensive Assessment of RAG Frameworks)를 도입하여, 배포된 RAG 애플리케이션을 체계적으로 벤치마크하도록 설계했습니다. [2504.07803v1]
- s4: 또한, [2504.07803v1]에서는 SCARF라는 평가 시스템을 통해 다양한 RAG 프레임워크와 구성을 비교·평가할 수 있는 방법을 제시합니다.

