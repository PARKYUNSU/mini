######## U1-1 | RAG 답변이 검색된 문서에 근거하는지 자동으로 검증하는 연구 있어? | direct_answer/B | 87.5s
컨텍스트: 2605.03534
=== 답
<b>서론</b>
검색된 <b>문서</b>(retrieved passages)에 근거한 RAG 답변은 관련성만으로는 충분하지 않아, 해당 문서가 질문에 대한 답을 충분히 뒷받침하는지 자동으로 판단해야 하는 어려움이 있습니다. 이러한 검증 문제는 단순 점수화보다 증거의 부족·충분 여부를 세밀하게 구분할 수 있어야 합니다[2605.03534v2].

<b>본론</b>
SURE-RAG: 질문과 후보 답변 및 검색된 증명을 입력받아, 해당 문서가 답을 지지하거나 반박하는지 판단하고 지원이 확인될 때만 응답하도록 설계되었습니다. 증거 충분성을 집합 수준 속성으로 취급하여 개별 문서를 점수화할 수 없는 결손·충돌 문제를 해결하며, 공유 주장‑증명 검증기로 (claim, passage) 쌍에 대한 지역 관계 분포를 생성한 뒤 이를 coverage, relation strength, uncertainty, retrieval 네 가지 해석 가능한 특성 블록으로 집계해 세방향 결정과 감사 가능한 선택 점수를 제공합니다[2605.03534v2].

<b>결론</b>
제공된 문서에는 RAG 답변이 검색된 문서를 기반으로 자동으로 검증하는 연구인 <b>SURE‑RAG</b>가 소개되어 있습니다.
--- [2605.03534] SURE-RAG: Sufficiency and Uncertainty-Aware Evidence Verification for Selective Retrieval- :: Retrieval-augmented generation (RAG) grounds answers in retrieved passages, yet relevance does not guarantee sufficiency: a topical passage may still fail to justify the answer. We study evidence sufficiency verification for selective RAG answering, in which a verifier receives a question, a candidate answer, and retrieved evidence and decides whether the evidence supports, refutes, or is insufficient for the answer, answering only when support is established. We present SURE-RAG, an aggregation protocol that treats evidence sufficiency as a set-level property: missing hops and unresolved conflicts cannot be detected by scoring passages indep

######## U1-2 | LLM 답변에 문장 단위 인용(citation)을 정확하게 붙이게 하는 방법 찾아줘 | direct_answer/B | 56.0s
컨텍스트: 2404.09763, 2510.17853, 2509.21557
=== 답
<b>서론</b>
LLM 답변에 <b>문장 단위 인용(citation)</b> 을 정확하게 붙이는 것은 모델이 생성한 텍스트와 실제 참고 문서 간의 관계를 정확히 파악해야 하므로 어려운 문제이다. 특히 신뢰성이 요구되는 분야에서 작은 오류도 심각한 결과를 초래할 수 있다.

<b>본론</b>
1. <b>KG-CTG</b>: 지식 그래프 관계 정보를 프롬프트에 포함시켜 LLM을 통해 인용 생성 성능을 향상시킨다[2404.09763v1]
2. <b>CiteGuard</b>: 검색 기반 검증 프레임워크를 도입해 모델이 만든 인용과 인간 작가가 넣어야 할 인용의 일치도를 평가하고, 기존 베이스라인보다 정확도가 최대 68.1%까지 개선한다[2510.17853v4]

<b>결론</b>
KG-CTG는 지식 그래프 관계를 프롬프트에 포함시켜 LLM의 인용 생성 성능을 향상시켰으며, Alpaca 모델이 Rouge-1 점수에서 36.98%, Meteor 점수에서 33.14% 개선된 결과를 보였습니다[2404.09763v1]. CiteGuard는 이전 베이스라인보다 정확도가 10%p 높아져 CiteME 벤치마크에서 최대 68.1%의 정확도를 달성하고 인간 성능(69.2%)에 근접했습니다[2510.17853v4]. 두 연구 모두 LLM 기반 인용 생성·평가 분야에서 성능 향상을 입증하지만, KG-CTG는 지식 그래프 활용을 통한 프롬프트 엔지니어링에 초점을 둔 반면, CiteGuard는 검색 증강 검증과 인용 귀속 정렬이라는 다른 접근법을 통해 정확도 개선을 달성했습니다.
--- [2404.09763] KG-CTG: Citation Generation through Knowledge Graph-guided Large Language Models :: Citation Text Generation (CTG) is a task in natural language processing (NLP) that aims to produce text that accurately cites or references a cited document within a source document. In CTG, the generated text draws upon contextual cues from both the source document and the cited paper, ensuring accurate and relevant citation information is provided. Previous work in the field of citation generation is mainly based on the text summarization of documents. Following this, this paper presents a framework, and a comparative study to demonstrate the use of Large Language Models (LLMs) for the task of citation generation. Also, we have shown the im
--- [2510.17853] CiteGuard: Faithful Citation Attribution for LLMs via Retrieval-Augmented Validation :: Large Language Models (LLMs) have emerged as powerful assistants for scientific writing. However, concerns remain about the quality and reliability of the generated text, including citation accuracy and faithfulness. While most recent work relies on methods such as LLM-as-a-Judge, the reliability of LLM-as-a-Judge alone is also in doubt. In this work, we reframe citation evaluation as a problem of citation attribution alignment, which assesses whether LLM-generated citations match those a human author would include for the same text. We propose CiteGuard, a retrieval-aware agent framework designed to provide more faithful grounding for citati

######## U1-3 | 검색 문서에 답이 없을 때 모른다고 답하게(abstention) 만드는 연구들 정리해줘 | direct_answer/B | 75.8s
컨텍스트: 2606.28733, 2604.03904, 2506.09038, 2602.04755
=== 답
<b>서론</b>
제공된 문서들은 LLM이 답변할 수 없는 상황에서 스스로를 멈추도록 (<b>abstention</b>) 유도하는 연구들을 다룹니다. 각 접근법은 모델 재학습 없이도 신뢰성 있는 ‘모른다’ 응답을 강화하거나, 벤치마크로 평가 가능성을 제시합니다.

<b>본론</b>
1. <b>CONVOLVE</b>: 컨텍스트 엔지니어링 방법으로 전체 상호작용 궤적을 활용 가능한 정지 규칙으로 추출하여 WebShop에서 Llama‑3.3‑70B의 적시 recall률을 26.7→57.4로 크게 향상시켰습니다[2606.28733v1].
2. <b>I-CALM</b>: GPT‑5 mini를 PopQA에 적용한 신뢰도 유발·abstention 보상 프롬프트(규범 포함)가 답변된 사례의 오답률을 낮추고, 재학습 없이 선택적 응답을 개선한다는 결과를 보였습니다[2604.03904v1].
3. <b>AbstentionBench</b>: 20개의 다양한 데이터셋에 걸친 대규모 벤치마크로 abstention 성능을 종합적으로 평가하고, 최근 추론 LLM이 복잡한 문제 해결에서는 성과가 좋으나 모호·오류 전제 등 질문에 대해서는 여전히 실패한다는 점을 확인했습니다[2506.09038v1].
4. <b>RL‑based Abstention</b>: 시간적 QA에서 RL 학습으로 abstention 능력을 배양한 모델은 순수 SFT 대비 불응 가능 질문의 True Positive율을 20% 향상시켰으며, 다양한 방법론에 대한 광범위한 실험을 통해 이를 검증했습니다[2602.04755v2].

<b>결론</b>
제공된 문서들은 abstention을 유도하는 연구들이 데이터셋과 모델에 따라 효과가 다르게 나타난다는 점을 보여줍니다. Agentic Abstention은 WebShop 환경에서 Llama-3.3-70B의 timely recall을 26.7에서 57.4로 크게 향상시켰으며, 이는 파라미터 업데이트 없이 달성된 결과입니다[2606.28733v1]. I-CALM은 PopQA 데이터셋에서 GPT-5 mini에 대해 신뢰 기반 프롬프트와 보상을 통해 오답률을 감소시키고 선택적 답변을 개선했지만, 효과 크기는 모델과 데이터셋마다 차이가 있었습니다[2604.03904v1]. AbstentionBench는 20개의 다양한 데이터셋을 포함한 대규모 벤치마크를 소개하여 abstention 성능을 종합적으로 평가하는 기준을 제시했습니다[2506.09038v1]. 또한, RL 기반 접근법은 추론 작업에서 순수 SFT 대비 unanswerable 질문의 True Positive율을 20% 향상시켰습니다[2602.04755v2]. 따라서 abstention 연구들은 도메인·모델·평가 방식에 따라 성능 향상이나 한계가 다르게 나타나는 것으로 확인됩니다.
--- [2606.28733] Agentic Abstention: Do Agents Know When to Stop Instead of Act? :: LLM agents are expected to act over multiple turns, using search, browsing interfaces, and terminal tools to complete user goals. Yet not every goal is well specified or achievable in the available environment. In such cases, a reliable agent should recognize that further interaction is unlikely to help and abstain from additional tool calls. We define Agentic Abstention, the problem of deciding when an agent should stop acting under uncertainty. Unlike standard LLM abstention, which is usually evaluated as a single-turn answer-or-abstain decision, agentic abstention is a sequential decision problem: an agent can answer, abstain, or gather mo
--- [2604.03904] I-CALM: Incentivizing Confidence-Aware Abstention for LLM Hallucination Mitigation :: Large language models (LLMs) frequently produce confident but incorrect answers, partly because common binary scoring conventions reward answering over honestly expressing uncertainty. We study whether prompt-only interventions -- explicitly announcing reward schemes for answer-versus-abstain decisions plus humility-oriented normative principles -- can reduce hallucination risk without modifying the model. Our focus is epistemic abstention on factual questions with a verifiable answer, where current LLMs often fail to abstain despite being uncertain about their answers. We first assess self-reported verbal confidence as a usable uncertainty s
--- [2506.09038] AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions :: For Large Language Models (LLMs) to be reliably deployed in both everyday and high-stakes domains, knowing when not to answer is equally critical as answering correctly. Real-world user queries, which can be underspecified, ill-posed, or fundamentally unanswerable, require LLMs to reason about uncertainty and selectively abstain -- i.e., refuse to answer definitively. However, abstention remains understudied, without a systematic evaluation framework for modern LLMs. In this work, we introduce AbstentionBench, a large-scale benchmark for holistically evaluating abstention across 20 diverse datasets, including questions with unknown answers, u
--- [2602.04755] When Silence Is Golden: Can LLMs Learn to Abstain in Temporal QA and Beyond? :: Large language models (LLMs) rarely admit uncertainty, often producing fluent but misleading answers, rather than abstaining (i.e., refusing to answer). This weakness is even evident in temporal question answering, where models frequently ignore time-sensitive evidence and conflate facts across different time-periods. In this paper, we present the first empirical study of training LLMs with an abstention ability while reasoning about temporal QA. Existing approaches such as calibration might be unreliable in capturing uncertainty in complex reasoning. We instead frame abstention as a teachable skill and introduce a pipeline that couples Chain

######## U1-4 | 외부 지식 없이 샘플링 일관성으로 환각을 탐지하는 방법 알려줘 | direct_answer/B | 31.4s
컨텍스트: 2606.06748
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.
<b>샘플링 일관성</b>(sampling consistency)은 환각 탐지에 사용되는 개념이지만, 현재 제공된 자료에서는 이에 대한 구체적인 방법이나 결과가 포함되어 있지 않습니다.

<b>본론</b>
1. <b>Evidence Graph Consistency (EGC)</b>: 응답마다 지역 증거 그래프를 구축하고 다섯 가지 구조적 일치 측정치를 계산해 이를 환각 지표로 활용한다[2606.06748v2].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.
--- [2606.06748] Evidence Graph Consistency in Retrieval-Augmented Generation: A Model-Dependent Analysis o :: Retrieval-Augmented Generation (RAG) reduces but does not eliminate hallucination in large language models. Existing detection methods rely on flat similarity between generated answers and retrieved passages, ignoring structural relationships among evidence pieces and answer claims. We propose Evidence Graph Consistency (EGC), a framework that constructs a local evidence graph per response and computes five structural consistency measures as hallucination indicators. Evaluated on the full question answering split of RAGTruth across six LLMs (5,767 responses), EGC reveals a consistent model-family split: graph consistency features show the exp

######## U1-5 | 모델이 답을 만든 뒤 검증 질문을 스스로 만들어 사실을 확인하는 연구 있어? | direct_answer/B | 52.9s
컨텍스트: 2609.15830, 2602.07594
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>CiteGuard-RAG</b>: 검증 중심 AI 시스템으로, 검색·생성·인용 확인·거부 및 재생성을 통합하고 런타임에 후보 답변을 수용/거부/재생산하도록 합니다[2609.15830v1].
2. <b>Self‑Verification Learning Framework</b>: 생성과 자체 검증을 독립적이지만 상호 보완적인 목표로 하는 다중 작업 강화 학습 프레임워크를 도입해, 검증 능력을 향상시키면서 동시에 생성 성능도 개선합니다[2602.07594v1]

<b>결론</b>
[2609.15830v1]은 CiteGuard-RAG 시스템이 검증 단계에서 환각을 전혀 탐지하지 못했으며, 신뢰성 있는 RAG 시스템에는 검색과 최종 답변 전달 사이에 명시적인 검증이 필요하다고 강조한다[2609.15830v1]. [2602.07594v1]는 언어 모델을 스스로 검증하도록 학습하면 생성 성능이 향상되고, 특히 수학 도메인에서 자체 검증 과정을 통해 더 효율적이고 효과적인 추론 흔적을 얻는다고 보고한다[2602.07594v1]. 따라서 두 연구 모두 모델이 답을 만든 뒤 스스로 검증 질문을 만들어 사실을 확인하는 접근이 효과적임을 지지하지만, [2609.15830v1]은 실제 데이터셋에서의 환각 탐지 결과를 제시하고, [2602.07594v1]는 학습 과정 중 자체 검증이 생성 성능에 미치는 영향을 강조한다는 점에서 초점이 다르다.
--- [2609.15830] CiteGuard-RAG: A Validation-Centered AI System for Evidence-Grounded Question Answering :: Retrieval-augmented generation (RAG) can improve access to complex information; however, retrieving evidence alone does not ensure that answers are grounded, citation-valid, or appropriately refused. This paper introduces CiteGuard-RAG, a validation-centered AI system for evidence-grounded question answering. The system integrates hybrid semantic-lexical retrieval, citation-constrained generation, sentence-level grounding validation, and single-pass regeneration. Validation is used at runtime to determine whether a candidate answer should be accepted, refused, or regenerated before final delivery. CiteGuard-RAG is evaluated on 400 questions a
--- [2602.07594] Learning to Self-Verify Makes Language Models Better Reasoners :: Recent large language models (LLMs) achieve strong performance in generating promising reasoning paths for complex tasks. However, despite powerful generation ability, LLMs remain weak at verifying their own answers, revealing a persistent capability asymmetry between generation and self-verification. In this work, we conduct an in-depth investigation of this asymmetry throughout training evolution and show that, even on the same task, improving generation does not lead to corresponding improvements in self-verification. Interestingly, we find that the reverse direction of this asymmetry behaves differently: learning to self-verify can effect

######## U1-6 | LLM 환각 탐지 연구 동향 정리해줘 | direct_answer/B | 62.4s
컨텍스트: 2310.18344, 2502.13490, 2311.05232, 2309.01219, 2507.06196, 2404.18930, 2508.14314, 2507.19024, 2606.06748, 2407.00488
=== 답
<b>서론</b>
최근 연구들은 LLM 환각 탐지를 위해 다양한 접근법을 제시하고 있으며, 그 흐름은 모델 내부 상태 분석에서부터 외부 지식 활용까지 확장되고 있다[2502.13490v1][2311.05232v2].

<b>본론</b>
1. <b>ChainPoll</b>: Chainpoll이 모든 RealHall 벤치마크를 초과하며 전체 AUROC가 0.781로 기록되었고, 이는 다음 최선의 이론적 방법보다 11% 높으며 산업 표준을 23% 이상 상회한다[2310.18344v1].
2. <b>Model Inner State Analysis</b>: 모델 내부 상태를 환각 탐지에 도입하고 종합적인 실험을 통해 그 장점과 한계를 논의하였다[2502.13490v1].
3. <b>Hallucination Detection Methods and Benchmarks Overview</b>: 환각 탐지 방법 및 벤치마크에 대한 포괄적 개요를 제시한다[2311.05232v2].

<b>결론</b>
ChainPoll은 모든 RealHall 벤치마크에서 AUROC 0.781을 달성하여 다음으로 좋은 이론적 방법보다 11% 더 높은 성능을 보이며, 산업 표준보다 23% 이상 초과한다[2310.18344v1]. 반면, 모델 내부 상태를 활용한 환각 탐지 연구는 이러한 내부 상태를 도입하고 포괄적인 실험을 통해 장단점을 논의한다[2502.13490v1]. 또한, 검색 증강 LLM이 환각을 억제하는 데 직면한 현재 한계를 제시하며 더 견고한 IR 시스템 개발에 통찰을 제공한다[2311.05232v2]. 따라서 ChainPoll은 벤치마크 기반 정량적 성능에서 우위를 점하고, 내부 상태 분석과 검색 증강 접근법은 각각 모델 해석 및 시스템 강인성 향상에 초점을 둔 연구로 구분된다.
--- [2502.13490] What are Models Thinking about? Understanding Large Language Model Hallucinations "Psychol :: Large language model (LLM) systems suffer from the models' unstable ability to generate valid and factual content, resulting in hallucination generation. Current hallucination detection methods heavily rely on out-of-model information sources, such as RAG to assist the detection, thus bringing heavy additional latency. Recently, internal states of LLMs' inference have been widely used in numerous research works, such as prompt injection detection, etc. Considering the interpretability of LLM internal states and the fact that they do not require external information sources, we introduce such states into LLM hallucination detection. In this pa
--- [2311.05232] A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and  :: The emergence of large language models (LLMs) has marked a significant breakthrough in natural language processing (NLP), fueling a paradigm shift in information acquisition. Nevertheless, LLMs are prone to hallucination, generating plausible yet nonfactual content. This phenomenon raises significant concerns over the reliability of LLMs in real-world information retrieval (IR) systems and has attracted intensive research to detect and mitigate such hallucinations. Given the open-ended general-purpose attributes inherent to LLMs, LLM hallucinations present distinct challenges that diverge from prior task-specific models. This divergence highl
--- [2310.18344] Chainpoll: A high efficacy method for LLM hallucination detection :: Large language models (LLMs) have experienced notable advancements in generating coherent and contextually relevant responses. However, hallucinations - incorrect or unfounded claims - are still prevalent, prompting the creation of automated metrics to detect these in LLM outputs. Our contributions include: introducing ChainPoll, an innovative hallucination detection method that excels compared to its counterparts, and unveiling RealHall, a refined collection of benchmark datasets to assess hallucination detection metrics from recent studies. While creating RealHall, we assessed tasks and datasets from previous hallucination detection studies

######## U2-1 | 긴 컨텍스트 중간에 있는 정보를 LLM이 놓치는 문제를 다룬 연구 있어? | direct_answer/B | 74.5s
컨텍스트: 2406.16008, 2410.14641, 2307.03172
=== 답
<b>서론</b>
긴 입력 컨텍스트에서 <b>중간에 위치한 관련 정보</b>를 활용하지 못하는 현상은 LLM 내부에 존재하는 위치 기반 주의 편향 때문에 발생하며, 이는 모델의 성능 저하와 신뢰성 감소로 이어집니다[2406.16008v2][2410.14641v3]. 이러한 문제는 특히 긴 문서를 다루는 작업이나 검색‑증강 생성(RAG)에서 중요한 한계점으로 인식되고 있습니다.

<b>본론</b>
1. <b>Found-in-the-Middle</b>: LLM의 U자형 위치 주의 편향을 보정하는 메커니즘으로, 입력 중간에 있는 토큰도 관련성만큼 공정하게 주의를 기울이도록 설계되었습니다[2406.16008v2].
2. <b>LongPiBench</b>: 여러 개의 관련 정보 조각을 동시에 고려하여 LLM의 위치 편향과 그 간격 효과를 평가하기 위한 벤치마크이며, 기존 모델들이 중간 정보를 활용하는 데 여전히 상당한 편향을 보인다는 결과를 제시했습니다[2410.14641v3].

<b>결론</b>
제공된 문서들은 긴 컨텍스트에서 <b>중간 정보</b>를 놓치는 문제를 LLM의 위치 주의 편향과 연결하고 있으며, 이를 완화하기 위한 ‘Found-in-the-Middle’ 메커니즘을 제안함과 동시에 이러한 현상을 측정할 수 있는 벤치마크인 LongPiBench도 제시합니다. 따라서 질문이 찾는 연구는 [2406.16008v2]에 명시된 Found‑in‑the‑Middle 접근법에서 찾을 수 있습니다[2406.16008v2].
--- [2406.16008] Found in the Middle: Calibrating Positional Attention Bias Improves Long Context Utilizati :: Large language models (LLMs), even when specifically trained to process long input contexts, struggle to capture relevant information located in the middle of their input. This phenomenon has been known as the lost-in-the-middle problem. In this work, we make three contributions. First, we set out to understand the factors that cause this phenomenon. In doing so, we establish a connection between lost-in-the-middle to LLMs' intrinsic attention bias: LLMs exhibit a U-shaped attention bias where the tokens at the beginning and at the end of its input receive higher attention, regardless of their relevance. Second, we mitigate this positional bi
--- [2410.14641] Distance between Relevant Information Pieces Causes Bias in Long-Context LLMs :: Positional bias in large language models (LLMs) hinders their ability to effectively process long inputs. A prominent example is the "lost in the middle" phenomenon, where LLMs struggle to utilize relevant information situated in the middle of the input. While prior research primarily focuses on single pieces of relevant information, real-world applications often involve multiple relevant information pieces. To bridge this gap, we present LongPiBench, a benchmark designed to assess positional bias involving multiple pieces of relevant information. Thorough experiments are conducted with five commercial and six open-source models. These experi

######## U2-2 | RAG에서 검색된 문서의 순서나 개수가 답변 품질에 주는 영향을 분석한 연구 찾아줘 | direct_answer/B | 39.1s
컨텍스트: 2505.15561
=== 답
<b>서론</b>
검색 증강 생성(RAG) 시스템에서 <b>위치 편향</b>과 검색된 패시지의 순서가 모델 성능에 미치는 영향을 파악하는 것은, 관련 문서와 방해가 되는 문서를 동시에 처리해야 하기 때문에 어려운 문제입니다.

<b>본론</b>
1. <b>Positional Bias Investigation</b>: 이 연구는 LLM이 프롬프트 내 위치에 따라 정보를 다르게 가중치는 현상이 어떻게 RAG 시스템의 정확도에 영향을 주는지 조사합니다[2505.15561v2]. 네 가지 검색 파이프라인을 HITS@ _k_ 지표로 평가하여 상위 _k개에 적어도 하나의 관련 패시지가 포함되는 비율을 측정했습니다[2505.15561v2].
<b>결론</b>
제공된 문서들은 RAG에서 위치 편향과 검색 순서가 모델 성능에 미치는 영향을 분석하고, 다양한 파이프라인의 HITS@ _k_ 결과를 제시함으로써 질문이 찾는 연구와 그 핵심 내용을 담고 있습니다.
--- [2505.15561] Do RAG Systems Really Suffer From Positional Bias? :: Retrieval Augmented Generation enhances LLM accuracy by adding passages retrieved from an external corpus to the LLM prompt. This paper investigates how positional bias - the tendency of LLMs to weight information differently based on its position in the prompt - affects not only the LLM's capability to capitalize on relevant passages, but also its susceptibility to distracting passages. Through extensive experiments on three benchmarks, we show how state-of-the-art retrieval pipelines, while attempting to retrieve relevant passages, systematically bring highly distracting ones to the top ranks, with over 60% of queries containing at least on

######## U2-3 | 프롬프트를 압축해서 컨텍스트 길이를 줄이면서 성능을 유지하는 방법 알려줘 | direct_answer/B | 64.7s
컨텍스트: 2401.14887, 2412.12322, 2504.07803, 2602.21553, 2407.11005
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 프롬프트를 압축해 컨텍스트 길이를 줄이는 방법은 현재 제공된 자료에서 찾을 수 없다.

<b>본론</b>
1. <b>RAG Playground</b>: RAG 시스템의 검색 전략과 프롬프트 엔지니어링을 체계적으로 평가하기 위한 오픈소스 프레임워크로, naive vector search와 reranking 및 hybrid vector-keyword search 등 세 가지 접근법을 구현하고 비교한다[2412.12322v1].
2. <b>SCARF (System for Comprehensive Assessment of RAG Frameworks)</b>: 모듈형·유연한 평가를 통해 배포된 RAG 애플리케이션을 블랙박스 방식으로 벤치마크하며, 응답 일관성 등을 고려해 성능 보고서를 생성한다[2504.07803v1].

<b>결론</b>
제공된 문서들은 프롬프트 압축을 통한 성능 유지 방법에 대한 구체적인 결과를 제시하지 않습니다. [2412.12322v1]는 하이브리드 검색과 구조화된 자기평가 프롬프팅을 통해 다중 지표 평가 프레임워크에서 최대 72.7%의 패스율을 달성했다고 보고합니다. 또한, 커스텀 프롬프트를 사용한 에이전트가 검색 정확도와 응답 품질에서 일관된 개선을 보였으며, 이는 프롬프트 엔지니어링이 RAG 시스템에서 중요함을 강조합니다. 따라서 현재 연구는 프롬프트 설계와 평가 방법의 개선에 초점을 맞추고 있습니다.
--- [2412.12322] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt E :: We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical results comparing different language models (Llama 3.1 and Qwen 2.5) across various retrieval configurations. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation
--- [2504.07803] A System for Comprehensive Assessment of RAG Frameworks :: Retrieval Augmented Generation (RAG) has emerged as a standard paradigm for enhancing the factual accuracy and contextual relevance of Large Language Models (LLMs) by integrating retrieval mechanisms. However, existing evaluation frameworks fail to provide a holistic black-box approach to assessing RAG systems, especially in real-world deployment scenarios. To address this gap, we introduce SCARF (System for Comprehensive Assessment of RAG Frameworks), a modular and flexible evaluation framework designed to benchmark deployed RAG applications systematically. SCARF provides an end-to-end, black-box evaluation methodology, enabling a limited-ef

######## U2-4 | 롱 컨텍스트 LLM이랑 RAG 중 어느 쪽이 나은지 비교한 연구 있어? | direct_answer/B | 273.1s
컨텍스트: 2407.16833
=== 답
<b>서론</b>
제공된 연구는 <b>Retrieval Augmented Generation (RAG)</b>과 <b>Long‑Context LLM</b> 간의 성능 차이를 비교하고, 두 접근법의 장점을 결합하는 방법을 제시합니다[2407.16833v2].

<b>본론</b>
1. <b>Self-Route</b>: 모델의 자체 반성을 이용해 쿼리를 RAG 또는 Long‑Context 방식으로 라우팅함으로써 계산 비용을 크게 줄이면서도 LC와 유사한 성능을 유지한다[2407.16833v2] 충분한 자원 확보 시 평균적으로 RAG보다 우수한 성과를 보이며, 최근 모델(Gemini-1.5, GPT‑4 등)은 긴 컨텍스트를 직접 이해하는 뛰어난 능력을 보인다[2407.16833v2].
<b>결론</b>
연구 결과에 따르면 Long‑context LLM이 성능 면에서 우위를 점하지만 비용 측면에서는 RAG가 훨씬 저렴합니다. 따라서 Self‑Route와 같은 하이브리드 라우팅 방식을 통해 두 방법의 강점을 동시에 활용할 수 있습니다.
--- [2407.16833] Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Appr :: Retrieval Augmented Generation (RAG) has been a powerful tool for Large Language Models (LLMs) to efficiently process overly lengthy contexts. However, recent LLMs like Gemini-1.5 and GPT-4 show exceptional capabilities to understand long contexts directly. We conduct a comprehensive comparison between RAG and long-context (LC) LLMs, aiming to leverage the strengths of both. We benchmark RAG and LC across various public datasets using three latest LLMs. Results reveal that when resourced sufficiently, LC consistently outperforms RAG in terms of average performance. However, RAG's significantly lower cost remains a distinct advantage. Based on

######## U2-5 | 검색 전에 질문을 재작성하거나 가상 답변을 만들어 검색 품질을 높이는 방법 찾아줘 | direct_answer/B | 75.3s
컨텍스트: 2503.04789, 2505.11626, 2511.01386, 2309.16035, 2503.01859
=== 답
<b>서론</b>
검색 전에 <b>질문 재작성</b>(query rephrasing)은 검색 품질 향상에 중요한 단계이지만, 질문 의도를 정확히 파악하고 적절한 키워드를 추출하는 것이 어렵습니다. 또한 가상 답변 생성 없이도 관련 문서를 효과적으로 찾는 메커니즘이 필요합니다.

<b>본론</b>
1. <b>Query Rephraser</b>: LLM 기반 모듈로 시험 문제를 최적화된 검색 쿼리로 변환하여 문서 검색 품질을 향상시킵니다[2503.01859v1].
2. <b>Ext2Gen (Extract‑then‑Generate)</b>: 질문 관련 콘텐츠를 동적으로 식별하고 소음을 억제하며, 사전 압축 없이 추출 후 생성 방식으로 답변 신뢰성을 높입니다[2503.04789v3].

<b>결론</b>
검색 품질 향상을 위한 질문 재작성이나 가상 답변 생성은 문서 유형과 데이터 조건에 따라 효과가 달라진다. Ext2Gen은 선호도 정렬을 통해 노이즈가 있거나 부정확한 검색 결과에서도 정확한 답변을 제공하며, 쿼리 재작성과 같은 개선된 검색 기술의 이점을 추가로 누린다[2503.04789v3]. 반면, 의료 콘텐츠 생성 시스템은 간격 반복 학습 알고리즘과 통합되어 문서 관련성, 신뢰성, 논리적 일관성을 향상시켰지만, 이는 정성 평가와 실험을 통해 검증된 결과이며 특정 도메인에 국한된다[2503.01859v1]. 따라서 검색 전 질문 재작성이나 가상 답변 생성은 일반적인 경우보다 특정 도메인이나 조건에서 더 큰 성능 향상을 보인다.
--- [2503.01859] Optimizing Retrieval-Augmented Generation of Medical Content for Spaced Repetition Learnin :: Advances in Large Language Models revolutionized medical education by enabling scalable and efficient learning solutions. This paper presents a pipeline employing Retrieval-Augmented Generation (RAG) system to prepare comments generation for Poland's State Specialization Examination (PES) based on verified resources. The system integrates these generated comments and source documents with a spaced repetition learning algorithm to enhance knowledge retention while minimizing cognitive overload. By employing a refined retrieval system, query rephraser, and an advanced reranker, our modified RAG solution promotes accuracy more than efficiency. R
--- [2503.04789] Aligning Extraction and Generation for Robust Retrieval-Augmented Generation :: Retrieval-augmented generation (RAG) enhances LLMs with external knowledge, yet generation remains vulnerable to retrieval-induced noise and uncertain placement of relevant chunks, often causing hallucinations. We present Ext2Gen, an extract-then-generate framework that strengthens LLMs via joint evidence selection and answer generation, dynamically identifying query-relevant content while suppressing noise, thereby removing the need for any independent pre-generation compression module. Optimized through preference alignment with well-curated pairwise feedback, Ext2Gen produces accurate and faithful answers even under noisy or imprecise retr

######## U2-6 | 관련 없는 문서가 섞였을 때 RAG가 흔들리지 않게 하는 연구들 정리해줘 | direct_answer/B | 86.1s
컨텍스트: 2601.01896, 2501.18365, 2406.01549, 2502.11770, 2509.12765, 2512.22442, 2409.10102
=== 답
<b>서론</b>
제공된 문서들은 모두 RAG 시스템이 관련 없는 노이즈나 검색 오류에 노출되었을 때 견고성을 높이는 방법을 제시합니다. 각 연구는 <b>fine‑tuning</b>, <b>정보 병목 이론 적용</b>, <b>문서 정보 이득 기반 재순위화</b> 등 다양한 접근법을 통해 신뢰성 있는 답변 생성을 목표로 합니다.

<b>본론</b>
1. <b>Novel Fine-tuning Method</b>: 모델이 검색된 문서 내에서 관련·비관련 정보를 구분하는 능력을 향상시키기 위해 새로운 fine‑tuning 방법을 제안하고, 여러 벤치마크에서 LLM의 견고성과 성능 향상을 확인했습니다 [2601.01896v2]
2. <b>Robust Fine-Tuning (RbFT)</b>: 두 가지 타겟ted fine-tuning 작업을 통해 검색 결함에 대한 RAG 시스템의 회복력을 강화했으며, 다양한检索 조건에서도 기존 방법보다 높은 견고성을 유지하면서 추론 효율을 높였습니다 [2501.18365v1]
3. <b>Information Bottleneck Approach</b>: 정보 병목 이론을 Retrieval‑Augmented Generation에 적용하여 정답 생성 정확도와 간결성(약 2.5% 압축) 을 동시에 개선했습니다[2406.01549v2].

<b>결론</b>
제공된 문서들은 모두 RAG 시스템이 노이즈나 검색 결함에 노출되었을 때 성능을 향상시킨다는 공통된 결론을 제시하고 있습니다. [2601.01896v2]은 다중 벤치마크에서 접근법이 LLM의 견고성과 성능을 크게 개선한다는 결과를 보여줍니다. 또한 [2501.18365v1]와 [2406.01549v2]도 각각 다양한 검색 조건과 질문 답변 데이터셋에서 시스템의 견고성을 향상시켰음을 실험 결과로 입증하고 있습니다. 따라서 이 연구들은 서로 다른 평가 환경에서도 RAG의 견고성 향상에 긍정적인 효과를 미친다는 점에서 일관된 결과를 보여줍니다.
--- [2601.01896] Tackling the Inherent Difficulty of Noise Filtering in RAG :: Retrieval-Augmented Generation (RAG) has become a widely adopted approach to enhance Large Language Models (LLMs) by incorporating external knowledge and reducing hallucinations. However, noisy or irrelevant documents are often introduced during RAG, potentially degrading performance and even causing hallucinated outputs. While various methods have been proposed to filter out such noise, we argue that identifying irrelevant information from retrieved content is inherently difficult and limited number of transformer layers can hardly solve this. Consequently, retrievers fail to filter out irrelevant documents entirely. Therefore, LLMs must be 
--- [2501.18365] RbFT: Robust Fine-tuning for Retrieval-Augmented Generation against Retrieval Defects :: Retrieval-augmented generation (RAG) enhances large language models (LLMs) by integrating external knowledge retrieved from a knowledge base. However, its effectiveness is fundamentally constrained by the reliability of both the retriever and the knowledge base. In real-world scenarios, imperfections in these components often lead to the retrieval of noisy, irrelevant, or misleading counterfactual information, ultimately undermining the trustworthiness of RAG systems. To address this challenge, we propose Robust Fine-Tuning (RbFT), a method designed to enhance the resilience of LLMs against retrieval defects through two targeted fine-tuning t
--- [2406.01549] An Information Bottleneck Perspective for Effective Noise Filtering on Retrieval-Augmented :: Retrieval-augmented generation integrates the capabilities of large language models with relevant information retrieved from an extensive corpus, yet encounters challenges when confronted with real-world noisy data. One recent solution is to train a filter module to find relevant content but only achieve suboptimal noise compression. In this paper, we propose to introduce the information bottleneck theory into retrieval-augmented generation. Our approach involves the filtration of noise by simultaneously maximizing the mutual information between compression and ground output, while minimizing the mutual information between compression and ret

######## U3-1 | 표가 포함된 문서에서 질의응답 성능을 높이는 RAG 연구 있어? | direct_answer/B | 42.7s
컨텍스트: 2605.18766
=== 답
<b>서론</b>
질문이 가리키는 문제는 <b>표(테이블)가 포함된 데이터베이스</b>에서 자연어 질의를 이용해 정확한 답변을 제공하는 것인데, 이는 방대한 테이블 집합 중 관련 표를 효율적으로 선택해야 하므로 어려운 과제이다.

<b>본론</b>
1. <b>Adaptive Table Retrieval</b>: 적응형 임계값 메커니즘과 슬라이딩 윈도우 재랭킹 알고리즘을 결합해 질의 요구에 따라 필요한 표 수를 동적으로 조절한다[2605.18766v1]. 최근 RAG 분야에서 질문 복잡도를 평가하고 텍스트 청크 크기를 조정하는 적응형 검색 방법이 제안되었다(이 접근은 구조화된 테이블 데이터에는 적용되지 않는다)[2605.18766v1].
<b>결론</b>
제공된 문서에 따르면, 표가 포함된 환경에서 질의응답 성능을 높이기 위해 <b>Adaptive Table Retrieval</b>이라는 연구가 존재한다. 이 방법은 기존 고정 개수의 top‑k 검색 전략과 달리 각 질문에 맞춰 필요한 테이블 수를 자동으로 결정함으로써 관련성 높은 정보를 더 정확히 추출하고 downstream 작업(예: text-to-SQL)에서 성능 향상을 달성한다는 점에서 질문의 요구에 부합한다.
--- [2605.18766] Retrieve Only Relevant Tables Whether Few or Many: Adaptive Table Retrieval Method :: Retrieving relevant tables from extensive databases for a given natural language query is essential for accurately answering questions in tasks such as text-to-SQL. Existing table retrieval approaches select a pre-determined set of k tables with the highest similarity to the query. However, the number of required tables varies across queries and cannot be known in advance. Enforcing a fixed number of retrieved tables regardless of the query may either retrieve an undersized set, failing to obtain all necessary evidence, or retrieve an oversized pool, including irrelevant tables. To address this issue, we propose an adaptive table retrieval me

######## U3-2 | 표를 LLM에 넣을 때 어떤 형식으로 직렬화하는 게 좋은지 비교한 연구 찾아줘 | direct_answer/B | 263.4s
컨텍스트: 2210.10723, 2505.14131
=== 답
<b>서론</b>
표를 <b>LLM</b>(Large Language Model)에 입력하기 위해 표를 자연어 문자열로 변환하는 과정은, 데이터 구조와 의미 정보를 어떻게 보존하느냐가 성능에 큰 영향을 미칩니다. 이러한 직렬화 방식의 선택이 모델 예측 정확도에 어떤 차이를 만드는지 파악하는 것이 핵심 과제입니다.

<b>본론</b>
1. <b>TabLLM</b>: 표를 자연어 문자열로 변환하고, 분류 문제 설명을 함께 프롬프트하여 LLM에 입력합니다[2210.10723v2].
2. <b>FRES</b>: 테이블 표현과 모델을 동적으로 선택해 질문 복잡도와 테이블 크기에 따라 최적의 조합이 달라짐을 확인했습니다[2505.14131v1].

<b>결론</b>
[2210.10723v2]에 따르면, 기존 연구들은 표를 단순 리스트나 문장으로 직렬화하거나 열 데이터 타입을 포함하는 방식을 사용했으며, Bertsimas et al. (2022)는 BERT 스타일 언어 모델에서 특징 임베딩을 유도하는 다른 맥락에서 직렬화 변형을 조사했다[2210.10723v2]. [2505.14131v1]에서는 표 표현과 모델의 최적 조합이 설정마다 달라지며, FRES 방법을 통해 무차별적으로 두 표현을 모두 사용할 때보다 평균 성능이 10% 향상된다고 보고한다[2505.14131v1]. 따라서 표를 LLM에 입력할 때 직렬화 형식은 데이터와 실험 설정에 따라 효과가 크게 달라지고, 동적 선택이 성능 향상에 도움이 된다는 결론을 내릴 수 있다.
--- [2210.10723] TabLLM: Few-shot Classification of Tabular Data with Large Language Models :: We study the application of large language models to zero-shot and few-shot classification of tabular data. We prompt the large language model with a serialization of the tabular data to a natural-language string, together with a short description of the classification problem. In the few-shot setting, we fine-tune the large language model using some labeled examples. We evaluate several serialization methods including templates, table-to-text models, and large language models. Despite its simplicity, we find that this technique outperforms prior deep-learning-based tabular classification methods on several benchmark datasets. In most cases, 
--- [2505.14131] Texts or Images? A Fine-grained Analysis on the Effectiveness of Input Representations and :: In table question answering (TQA), tables are encoded as either texts or images. Prior work suggests that passing images of tables to multi-modal large language models (MLLMs) performs comparably to or even better than using textual input with large language models (LLMs). However, the lack of controlled setups limits fine-grained distinctions between these approaches. In this paper, we conduct the first controlled study on the effectiveness of several combinations of table representations and models from two perspectives: question complexity and table size. We build a new benchmark based on existing TQA datasets. In a systematic analysis of 

######## U3-3 | PDF 문서에서 표와 레이아웃을 보존하며 파싱하는 방법 알려줘 | direct_answer/B | 54.8s
컨텍스트: 2410.21169, 2605.24973
=== 답
<b>서론</b>
PDF 문서에서 <b>표와 레이아웃</b>를 보존하며 파싱하는 것은 페이지 경계로 인해 표가 끊기거나, 복잡한 배치 구조 때문에 기존 OCR 모델만으로는 전체적인 논리적 관계를 복원하기 어렵습니다. 이러한 문제를 해결하려면 페이지 단위의 결과를 통합하고 교차‑페이지 연결성을 재구성할 수 있는 추가 처리 단계가 필요합니다.

<b>본론</b>
1. <b>MinerU-Popo</b>: VLM 기반 OCR 출력에 대해 텍스트·표 절단 복구, 제목 계층 구조 복원 및 이미지-텍스트 연관을 수행하는 경량 포스트프로세싱 프레임워크를 제안합니다[2605.24973v2].
2. <b>Document Parsing Unveiled survey</b>: 파이프라인 방식의 레이아웃 분석과 이질적 콘텐츠(테이블 포함) 인식 기술, 그리고 VLM 기반 문서 해석 모델들의 진화를 체계적으로 검토하고 평가 지표와 벤치마크를 정리했습니다[2410.21169v5]

<b>결론</b>
제공된 문서들은 PDF 파싱에 대한 구체적인 방법론보다는 평가 지표와 벤치마크를 정리하거나, 긴 문서 처리를 위한 동적 채킹 및 포스트프로세싱 모델을 소개하는 내용에 초점을 맞추고 있습니다[2410.21169v5][2605.24973v2]. 따라서 표와 레이아웃을 보존하며 파싱하는 직접적인 기술은 제시되지 않습니다.
--- [2605.24973] MinerU-Popo: Universal Post-Processing Model for Structured Document Parsing :: VLM-based OCR models have become the de facto choice for document parsing, as they can accurately extract page-level elements (e.g., paragraphs within individual pages) together with their bounding boxes and textual content. However, downstream applications such as RAG require coherent document-level information, whereas these models often break cross-page continuity and fail to recover disrupted structures, such as paragraphs and tables truncated by page boundaries. Such relationships are not confined to a single page; instead, they require joint analysis of titles, paragraphs, tables, and images spanning multiple pages. A natural solution i
--- [2410.21169] Document Parsing Unveiled: Techniques, Challenges, and Prospects for Structured Informatio :: Document parsing (DP) transforms unstructured or semi-structured documents into structured, machine-readable representations, enabling downstream applications such as knowledge base construction and retrieval-augmented generation (RAG). This survey provides a comprehensive and timely review of document parsing research. We propose a systematic taxonomy that organizes existing approaches into modular pipeline-based systems and unified models driven by Vision-Language Models (VLMs). We provide a detailed review of key components in pipeline systems, including layout analysis and the recognition of heterogeneous content such as text, tables, mat

######## U3-4 | 표와 텍스트를 함께 보고 수치 추론하는 QA 연구 동향 정리해줘 | direct_answer/B | 63.9s
컨텍스트: 2206.01347, 2412.11757, 2105.07624, 2407.05952, 2406.17961, 2503.12345, 2412.17189
=== 답
<b>서론</b>
최근 연구들은 <b>표와 텍스트를 동시에 활용하여 수치 추론을 수행하는 QA 모델·벤치마크</b>에 집중하고 있다. 이러한 접근은 복잡한 계산과 도메인 지식을 요구한다[2105.07624v2].

<b>본론</b>
1. <b>MT2Net</b>: 사실 검색으로 표 및 텍스트에서 관련 사실을 추출한 뒤, 이를 기반으로 기호적 추론을 수행하는 새로운 QA 모델을 제안하였다 [2206.01347v1]
2. <b>SciTaT (CaR)</b>: 과학적인 표와 텍스트를 포함한 다양한 유형에 대한 수치·논리적 추론이 필요한 벤치마크인 SciTaT 를 구축하고, CaR 모델은 기존 베이스라인 대비 평균 12.9% 향상된 성능을 보였다 [2412.11757v1]
3. <b>TAT-QA</b>: 금융 보고서에서 표와 텍스트 데이터를 결합한 대규모 QA 데이터셋으로 구성되었으며, 덧셈·뺄셈·곱셈·나눗셈 등 수치 연산이 필요한 질문들을 포함한다[2105.07624v2]

<b>결론</b>
SciTaT 벤치마크에서 CaR은 다른 베이스라인 대비 평균 12.9%의 성능 향상을 보이며, 복잡한 수치 계산과 도메인 지식이 주요 도전 과제로 확인되었다[2412.11757v1]. TAT-QA 데이터셋은 금융 보고서에서 추출한 대규모 표·텍스트 혼합 데이터를 기반으로 하며, 덧셈·뺄셈·곱셈·나눗셈·카운팅·비교·정렬·구성 등 다양한 수치 추론 작업이 필요함을 제시한다[2105.07624v2]. MultiHiertt는 다중 계층적 표와 텍스트 데이터에 대해 실험 결과에서 기존 베이스라인보다 인간 전문가 수준에 근접한 성능을 달성해 현재 모델들의 한계를 극복하고 있음을 보여준다[2206.01347v1].
--- [2105.07624] TAT-QA: A Question Answering Benchmark on a Hybrid of Tabular and Textual Content in Finan :: Hybrid data combining both tabular and textual content (e.g., financial reports) are quite pervasive in the real world. However, Question Answering (QA) over such hybrid data is largely neglected in existing research. In this work, we extract samples from real financial reports to build a new large-scale QA dataset containing both Tabular And Textual data, named TAT-QA, where numerical reasoning is usually required to infer the answer, such as addition, subtraction, multiplication, division, counting, comparison/sorting, and the compositions. We further propose a novel QA model termed TAGOP, which is capable of reasoning over both tables and 
--- [2206.01347] MultiHiertt: Numerical Reasoning over Multi Hierarchical Tabular and Textual Data :: Numerical reasoning over hybrid data containing both textual and tabular content (e.g., financial reports) has recently attracted much attention in the NLP community. However, existing question answering (QA) benchmarks over hybrid data only include a single flat table in each document and thus lack examples of multi-step numerical reasoning across multiple hierarchical tables. To facilitate data analytical progress, we construct a new large-scale benchmark, MultiHiertt, with QA pairs over Multi Hierarchical Tabular and Textual data. MultiHiertt is built from a wealth of financial reports and has the following unique characteristics: 1) each 
--- [2412.11757] SCITAT: A Question Answering Benchmark for Scientific Tables and Text Covering Diverse Rea :: Scientific question answering (SQA) is an important task aimed at answering questions based on papers. However, current SQA datasets have limited reasoning types and neglect the relevance between tables and text, creating a significant gap with real scenarios. To address these challenges, we propose a QA benchmark for scientific tables and text with diverse reasoning types (SciTaT). To cover more reasoning types, we summarize various reasoning types from real-world questions. To involve both tables and text, we require the questions to incorporate tables and text as much as possible. Based on SciTaT, we propose a strong baseline (CaR), which 

######## U3-5 | 차트나 도표가 있는 문서를 검색하는 멀티모달 RAG 논문 5개 찾아줘 | direct_answer/B | 72.6s
컨텍스트: 2510.15253, 2412.10704, 2504.08748, 2406.15187, 2509.20769
=== 답
※ 요청한 5편 중 3편만 찾았습니다.

<b>서론</b>
제공된 문서들은 멀티모달 검색‑증강 생성(Multimodal RAG)을 활용한 문서 이해 및 질문 응답 연구들을 다루고 있습니다. 특히 차트·도표와 같은 시각적 요소를 포함한 다중 문서를 처리하는 시스템에 초점을 맞추어 정리합니다.

<b>본론</b>
1. <b>Multimodal Retrieval-Augmented Generation for Document Understanding</b>: OCR 파이프라인과 네이티브 멀티모달 LLM의 한계를 지적하고, 문서 이해를 위한 체계적인 서베이와 Multimodal RAG 접근법을 제시한다 [2510.15253v3]
2. <b>VisDoMRAG (VisDoMBench)</b>: 표·차트·슬라이드 등 풍부한 시각적 요소를 포함한 다중 문서를 대상으로 멀티모달 QA 시스템을 평가하는 벤치마크를 소개하고, 기존 단일 모드 및 긴 컨텍스트 LLM 대비 성능 향상을 보고한다 [2412.10704v2]
3. <b>Multimodal Retrieval-Augmented Generation (MRAG) Survey</b>: MRAG가 전통적 RAG보다 시각·언어 이해 모두 필요한 시나리오에서 우수한 성과를 보이며, 핵심 구성 요소와 데이터셋을 검토한 서베이이다 [2504.08748v1]

<b>결론</b>
제공된 문서들은 멀티모달 RAG가 차트나 도표와 같은 시각적 요소를 포함한 문서 이해에 적용되는 다양한 접근법을 조사하고 있습니다. [2510.15253v3]은 현재 OCR 기반 파이프라인과 네이티브 멀티모달 LLM 모두 구조적 세부 사항 손실이나 컨텍스트 모델링 어려움이라는 한계를 지적하며, 이러한 문제를 해결하기 위해 체계적인 조사를 제시합니다. [2412.10704v2]는 VisDoMBench라는 벤치마크를 통해 테이블, 차트, 슬라이드 등 풍부한 멀티모달 콘텐츠를 포함한 다문서 설정에서 QA 시스템을 평가하고, 기존 단일모달 및 긴 컨텍스트 LLM 기반선을 12-20% 상회하는 성능을 보인다고 보고합니다. [2504.08748v1]은 MRAG의 핵심 구성 요소, 데이터셋, 평가 방법 및 한계를 검토하여 시스템 구축과 개선을 위한 통찰을 제공합니다. 따라서 이 논문들은 멀티모달 RAG가 시각적 요소를 포함한 문서 처리에 효과적이지만, 여전히 구조적 정보 손실과 컨텍스트 모델링이라는 근본적인 과제를 해결해야 함을 공통적으로 강조합니다.
--- [2510.15253] Scaling Beyond Context: A Survey of Multimodal Retrieval-Augmented Generation for Document :: Document understanding is critical for applications from financial analysis to scientific discovery. Current approaches, whether OCR-based pipelines feeding Large Language Models (LLMs) or native Multimodal LLMs (MLLMs), face key limitations: the former loses structural detail, while the latter struggles with context modeling. Retrieval-Augmented Generation (RAG) helps ground models in external data, but documents' multimodal nature, i.e., combining text, tables, charts, and layout, demands a more advanced paradigm: Multimodal RAG. This approach enables holistic retrieval and reasoning across all modalities, unlocking comprehensive document i
--- [2412.10704] VisDoM: Multi-Document QA with Visually Rich Elements Using Multimodal Retrieval-Augmented :: Understanding information from a collection of multiple documents, particularly those with visually rich elements, is important for document-grounded question answering. This paper introduces VisDoMBench, the first comprehensive benchmark designed to evaluate QA systems in multi-document settings with rich multimodal content, including tables, charts, and presentation slides. We propose VisDoMRAG, a novel multimodal Retrieval Augmented Generation (RAG) approach that simultaneously utilizes visual and textual RAG, combining robust visual retrieval capabilities with sophisticated linguistic reasoning. VisDoMRAG employs a multi-step reasoning pr
--- [2504.08748] A Survey of Multimodal Retrieval-Augmented Generation :: Multimodal Retrieval-Augmented Generation (MRAG) enhances large language models (LLMs) by integrating multimodal data (text, images, videos) into retrieval and generation processes, overcoming the limitations of text-only Retrieval-Augmented Generation (RAG). While RAG improves response accuracy by incorporating external textual knowledge, MRAG extends this framework to include multimodal retrieval and generation, leveraging contextual information from diverse data types. This approach reduces hallucinations and enhances question-answering systems by grounding responses in factual, multimodal knowledge. Recent studies show MRAG outperforms tr

######## U3-6 | 재무 보고서처럼 수치가 많은 문서에서 LLM이 계산을 틀리지 않게 하는 연구 있어? | direct_answer/B | 34.6s
컨텍스트: 2508.05201
=== 답
<b>서론</b>
재무 보고서와 같은 <b>수치가 많은 금융 문서</b>에서 LLM은 정확한 수치 추출과 계산을 요구하지만, 작은 오차도 의사결정과 규제 준수를 위협할 수 있어 평가가 어렵습니다. 이러한 문제를 해결하기 위해 기존 벤치마크보다 더 엄격한 방법이 필요합니다.

<b>본론</b>
1. <b>FAITH</b>: 재무 데이터에 대한 고유한 맥락 의존성·수치적 특성 및 비공개 데이터를 고려해, 실제 금융 문서에서 마스크된 스팬 예측을 통해 LLM의 내재 환각을 평가하는 자동화된 프레임워크를 개발했습니다[2508.05201v2].

<b>결론</b>
제공된 연구는 재무 보고서와 같은 수치 중심 문서를 대상으로 LLM이 계산 오류 없이 작동하도록 설계된 <b>FAITH</b>라는 평가를 제시하고 있습니다. 이는 기존 벤치마크보다 금융 데이터의 고유 요구사항을 반영한 엄격한 평가 방법입니다.
--- [2508.05201] FAITH: A Framework for Assessing Intrinsic Tabular Hallucinations in Finance :: Hallucination remains a critical challenge for deploying Large Language Models (LLMs) in finance. Accurate extraction and precise calculation from tabular data are essential for reliable financial analysis, since even minor numerical errors can undermine decision-making and regulatory compliance. Financial applications have unique requirements, often relying on context-dependent, numerical, and proprietary tabular data that existing hallucination benchmarks rarely capture. In this study, we develop a rigorous and scalable framework for evaluating intrinsic hallucinations in financial LLMs, conceptualized as a context-aware masked span predict

######## U4-1 | RAG 문서 청킹 전략(고정 길이, 의미 단위 등)을 비교한 연구 있어? | direct_answer/B | 91.1s
컨텍스트: 2601.14123, 2603.25333, 2603.24556, 2402.05131
=== 답
<b>서론</b>
문서 청킹 전략은 <b>Retrieval-Augmented Generation (RAG)</b> 시스템에서 검색 정확도와 비용 효율성을 결정하는 핵심 요소이며, 다양한 문서 유형과 구조에 따라 최적의 방법이 달라지기 때문에 선택이 어렵습니다.

<b>본론</b>
1. <b>Chunking Strategies for Reliable Question Answering</b>: 토큰·문장·semantic·code 등 청킹 방법, 크기, 오버랩 및 컨텍스트 길이를 체계적으로 변형하여 평가하고, SPLADE 검색과 Mistral‑8B 생성기를 사용한 산업적 설정에서 비용 효율적인 배포 교훈을 도출했습니다. [2601.14123v1]
2. <b>Adaptive Chunking</b>: 다섯 가지 고유 문서 기반 메트릭(References Completeness, Intrachunk Cohesion, Document Contextual Coherence, Block Integrity, Size Compliance) 을 이용해 각 문서를 위해 가장 적합한 청킹 전략을 선택하는 프레임워크를 제안하고, LLM‑regex 및 split‑then‑merge recursive splitter와 포스트프로세싱 기술을 도입하여 RAG 성능을 향상시켰습니다. [2603.25333v1]
3. <b>Chunking Strategies for Oil and Gas Enterprise Documents</b>: 고정 크기 슬라이딩 윈도우·recursive·breakpoint 기반 semantic·structure-aware 등 네 가지 청킹 전략을 오일‑가스 기업 문서에 적용해 평가하고, 구조 인식형(chunk)이 top‑K 검색 효과와 낮은 계산 비용을 제공한다는 결과를 제시했습니다. [2603.24556v1]

<b>결론</b>
제공된 문서들은 청킹 전략의 효과를 비교하지만, 데이터와 도메인에 따라 결과가 달라진다는 점을 보여줍니다. [2601.14123v1]은 Natural Questions 데이터셋에서 고정 길이 토큰·문장·의미 단위 청킹을 평가하여 문장 기반이 비용 효율적임을 제시하고, [2603.25333v1]는 법적·기술적·사회과학 도메인을 아우르는 다중 도메인 코퍼스에 대해 적응형 메트릭 기반 청킹이 정답률을 62-64%에서 72%로 향상시킨다고 보고합니다. 또한 [2603.24556v1]은 석유·가스 기업 문서라는 특정 도메인과 비공개 데이터셋을 대상으로 구조 보존이 중요한 역할을 한다고 결론지었습니다. 따라서 청킹 전략의 성능은 평가 대상의 데이터 유형과 도메인 특성에 크게 의존하며, 일반적인 비교는 제한된 조건에서만 가능합니다.
--- [2601.14123] A Systematic Analysis of Chunking Strategies for Reliable Question Answering :: We study how document chunking choices impact the reliability of Retrieval-Augmented Generation (RAG) systems in industry. While practice often relies on heuristics, our end-to-end evaluation on Natural Questions systematically varies chunking method (token, sentence, semantic, code), chunk size, overlap, and context length. We use a standard industrial setup: SPLADE retrieval and a Mistral-8B generator. We derive actionable lessons for cost-efficient deployment: (i) overlap provides no measurable benefit and increases indexing cost; (ii) sentence chunking is the most cost-effective method, matching semantic chunking up to ~5k tokens; (iii) a
--- [2603.25333] Adaptive Chunking: Optimizing Chunking-Method Selection for RAG :: The effectiveness of Retrieval-Augmented Generation (RAG) is highly dependent on how documents are chunked, that is, segmented into smaller units for indexing and retrieval. Yet, commonly used "one-size-fits-all" approaches often fail to capture the nuanced structure and semantics of diverse texts. Despite its central role, chunking lacks a dedicated evaluation framework, making it difficult to assess and compare strategies independently of downstream performance. We challenge this paradigm by introducing Adaptive Chunking, a framework that selects the most suitable chunking strategy for each document based on a set of five novel intrinsic, d
--- [2603.24556] Evaluating Chunking Strategies For Retrieval-Augmented Generation in Oil and Gas Enterpris :: Retrieval-Augmented Generation (RAG) has emerged as a framework to address the constraints of Large Language Models (LLMs). Yet, its effectiveness fundamentally hinges on document chunking - an often-overlooked determinant of its quality. This paper presents an empirical study quantifying performance differences across four chunking strategies: fixed-size sliding window, recursive, breakpoint-based semantic, and structure-aware. We evaluated these methods using a proprietary corpus of oil and gas enterprise documents, including text-heavy manuals, table-heavy specifications, and piping and instrumentation diagrams (P and IDs). Our findings sh

######## U4-2 | BM25랑 dense retrieval 차이가 뭐야? | direct_answer/B | 81.7s
컨텍스트: 2608.00229, 2603.05781, 2404.00684, 2607.26497
=== 답
<b>서론</b>
BM25와 dense retrieval은 각각 <b>lexical(단어 기반)</b>과 <b>dense vector</b>를 이용해 문서 관련성을 평가하는 두 가지 근본적으로 다른 접근법이다. BM25는 역문서빈도(IDF) 와 단어 빈도를 조합한 통계적 모델로, 반면 dense retrieval 은 임베딩 벡터와 내적을 통해 의미 유사도를 계산한다[2607.26497v3].

<b>본론</b>
1. <b>BM25</b>: Okapi BM25 scoring을 적용해 역문서빈도(IDF) 와 단어 빈도에 기반한 점수를 산출하며, 대규모 문서 집에서도 정확한 top‑k 검색이 가능하도록 설계되었다[2608.00229v1][2607.26497v3].
2. <b>Dense Retrieval (Multi-Vector Dense)</b>: 다중 벡터와 정렬 행렬을 이용해 쿼리·문서의 관련성을 곱의 합으로 계산한다; 이는 BM25보다 의미 기반 유사도를 제공한다[2404.00684v1].

<b>결론</b>
BM25는 단어 빈도와 역빈도에 의존하는 통계적 모델로, 대규모 데이터에서도 정확한 lexical 검색이 가능하다. Dense retrieval은 벡터 내적을 통해 의미를 직접 비교하므로 의미가 풍부한 쿼리에 더 적합하다. 두 방법은 각각 다른 관련성 측정 방식을 사용한다[2608.00229v1][2404.00684v1].
--- [2607.26497] BM25 Wins at Scale: A Scaling Study of Retrieval-Augmented Generation Paradigms :: Retrieval-augmented generation (RAG) spans lexical and dense retrieval, graph-based indexing, and agentic search, but these paradigms are usually evaluated on different benchmarks at one corpus size, leaving their accuracy-cost scaling unclear. To bridge this gap, we present a controlled study that varies corpus size along 28 strictly nested tiers spanning roughly 450-fold, while holding questions and a fixed bedrock of relevant and adversarial documents unchanged. Under one reader model and one judging protocol, we measure official accuracy, construction and query tokens, and latency. The results reveal a scale-dependent crossover rather tha
--- [2608.00229] Hierarchical BM25: Lexical Search at Billion-Document Scale :: A flat BM25 index over one billion documents occupies about 400 GB. Holding it in memory requires DRAM proportional to corpus size. Serving it from disk takes 4-12 seconds per query. Exact top-k lexical retrieval at this scale is therefore impractical within an interactive latency budget. Hierarchical BM25 gives up exact ranking in exchange for fixed bounds on memory and latency. A resident coarse index selects which of ~1K topical, size-balanced document groups a query visits, using two signals: the total frequency of each query term within a group, and, for informative terms spread too thinly across groups for frequency totals to reflect, w
--- [2404.00684] Generative Retrieval as Multi-Vector Dense Retrieval :: Generative retrieval generates identifiers of relevant documents in an end-to-end manner using a sequence-to-sequence architecture for a given query. The relation between generative retrieval and other retrieval methods, especially those based on matching within dense retrieval models, is not yet fully comprehended. Prior work has demonstrated that generative retrieval with atomic identifiers is equivalent to single-vector dense retrieval. Accordingly, generative retrieval exhibits behavior analogous to hierarchical search within a tree index in dense retrieval when using hierarchical semantic identifiers. However, prior work focuses solely o

######## U4-3 | 하이브리드 검색에서 희소·밀집 검색 결과를 합치는 방법 연구 찾아줘 | direct_answer/B | 74.9s
컨텍스트: 2210.11934, 2604.13728
=== 답
<b>서론</b>
하이브리드 검색은 <b>희소</b>(lexical)와 <b>밀집</b>(semantic)검색 결과를 결합해 관련성 점수를 산출하는 과정으로, 두 접근법의 상보성을 활용해야 하지만 적절한 융합 함수를 선택하지 않으면 성능이 크게 달라질 수 있어 어려운 문제입니다.

<b>본론</b>
1. <b>Convex Combination (CC)</b>: 희소와 밀집 검색의 점수 간 가중 평균을 통해 결합하며, 기존 연구와는 달리 파라미터 학습에 대한 정규화 방식 의존성이 낮고 도메인 내·외에서 RRF보다 우수한 성능과 높은 샘플 효율성을 보입니다[2210.11934v2].
2. <b>Reciprocal Rank Fusion (RRF)</b>: 희소와 밀집 검색 결과를 순위 리스트로 변환한 뒤, 각 문서의 랭크에 역수 가중치를 부여해 합산하는 방식으로 구현되며, TREC‑COVID 벤치마크에서 nDCG@10 = 0.828을 달성하여 가장 높은 관련성 점수를 기록했습니다[2604.13728v1].

<b>결론</b>
[2210.11934v2]은 RRF가 파라미터에 민감하고, CC가 도메인 내·외 설정에서 RRF를 능가하며 소량의 학습 데이터로도 튜닝이 가능하다고 보고한다[2210.11934v2]. [2604.13728v1]는 COVID-19 문헌 검색에서 RRF가 절대적인 nDCG@10 성능은 유지하지만, B5와 같은 다른 융합 방식이 키워드 중심 재형식화에 상대적으로 큰 이득을 보았으며, MMR 재랭킹은 다양성을 높이지만 nDCG@10이 일부 감소한다고 제시한다[2604.13728v1]. 따라서 두 연구는 모두 하이브리드 검색에서 희소·밀집 결과를 합치는 방법을 평가하지만, [2210.11934v2]은 일반적인 도메인 설정과 학습 효율성에 초점을 맞추고, [2604.13728v1]는 특정 COVID-19 데이터셋과 다양한 쿼리 스타일을 대상으로 성능과 속도를 비교한다는 점에서 대상과 조건이 다르다.
--- [2210.11934] An Analysis of Fusion Functions for Hybrid Retrieval :: We study hybrid search in text retrieval where lexical and semantic search are fused together with the intuition that the two are complementary in how they model relevance. In particular, we examine fusion by a convex combination (CC) of lexical and semantic scores, as well as the Reciprocal Rank Fusion (RRF) method, and identify their advantages and potential pitfalls. Contrary to existing studies, we find RRF to be sensitive to its parameters; that the learning of a CC fusion is generally agnostic to the choice of score normalization; that CC outperforms RRF in in-domain and out-of-domain settings; and finally, that CC is sample efficient, 
--- [2604.13728] Hybrid Retrieval for COVID-19 Literature: Comparing Rank Fusion and Projection Fusion with :: We present a hybrid retrieval system for COVID-19 scientific literature, evaluated on the TREC-COVID benchmark (171,332 papers, 50 expert queries). The system implements six retrieval configurations spanning sparse (SPLADE), dense (BGE), rank-level fusion (RRF), and a projection-based vector fusion (B5) approach. RRF fusion achieves the best relevance (nDCG@10 = 0.828), outperforming dense-only by 6.1% and sparse-only by 14.9%. Our projection fusion variant reaches nDCG@10 = 0.678 on expert queries while being 33% faster (847 ms vs. 1271 ms) and producing 2.2x higher ILD@10 than RRF. Evaluation across 400 queries -- including expert, machine-

######## U4-4 | cross-encoder 재순위랑 ColBERT 차이가 뭐야? | direct_answer/B | 303.6s
컨텍스트: 2603.25248, 2004.12832, 2509.25085
=== 답
<b>서론</b>
Cross‑encoder와 ColBERT은 모두 <b>문서 재순위</b>를 수행하지만, 상호작용 방식과 연산 효율에서 근본적인 차이가 있습니다. Cross‑encoder는 쿼리·문서를 동시에 입력해 전체 쌍에 대해 전파를 통과시키며 높은 정확도를 얻지만 계산 비용이 큽니다[2509.25085v4]. ColBERT은 BERT로 각각 인코딩한 후, 비싼 상호작용 없이도 정교한 유사성을 모델링하는 <b>late‑interaction</b> 구조를 도입하여 속도와 메모리 효율을 크게 향상시킵니다[2004.12832v2][2603.25248v1]．

<b>본론</b>
1. <b>Cross-encoder</b>: 쿼리와 문서를 함께 입력해 전체 쌍에 대해 전파가 통과되도록 설계되어 높은 정확도를 달성하지만, 각 쿼리‑문서 쌍마다 별도의 forward pass를 수행해야 하므로 대규모 검색에서 계산 병목이 발생한다[2509.25085v4].
2. <b>ColBERT</b>: BERT로 각각 인코딩한 후 cheap interaction 단계만 추가하는 late‑interaction 구조를 도입해 정교하면서도 효율적인 재순위를 가능하게 하며, 문서 표현을 오프라인에 사전 계산할 수 있어 쿼리 처리 속도가 기존 모델보다 두 배 이상 빨라진다[2004.12832v2].
3. <b>ColBERT-Att</b>: ColBERT의 late‑interaction 프레임워크에 attention 메커니즘을 명시적으로 통합해 쿼리와 문서 단어 간의 중요도를 반영한 유사성을 학습하도록 개선한다[2603.25248v1]．

<b>결론</b>
ColBERT는 문서와 쿼리를 사전에 독립적으로 인코딩한 후 다중 벡터 매칭을 통해 재순위화하는 방식이며, 이는 기존 BERT 기반 모델과 경쟁할 만큼 효과적이면서도 두 배 이상의 속도 향상과 4배의 FLOPs 감소 효과를 보인다 [2004.12832v2]. ColBERT-Att는 이러한 메커니즘에 주의력을 추가하여 MS-MARCO 및 BEIR, LoTTE 등 다양한 벤치마크에서 리콜 정확도를 개선한 결과를 보였다 [2603.25248v1]. 반면 Cross-encoder 기반 재순위기는 쿼리‑문서 쌍마다 전방 전파를 수행하므로 대규모 검색에서는 계산 병목이 발생하지만, 전통적인 크로스‑엔코더가 여전히 다양한 시나리오에서 높은 성능을 유지한다는 점에서도 차이가 있다 [2509.25085v4]. 따라서 ColBERT 계열은 효율성과 정확성 측면에서 기존 크로스‑엔코더보다 유리한 반면, 크로스‑엔코더는 완전한 상호작용으로 인해 높은 성능을 보이지만 계산 비용이 큰 차이가 있다.
--- [2509.25085] jina-reranker-v3: Last but Not Late Interaction for Listwise Document Reranking :: jina-reranker-v3 is a 0.6B-parameter multilingual listwise reranker that introduces a novel "last but not late" interaction. Unlike late interaction models like ColBERT that encode documents separately before multi-vector matching, our approach applies causal attention between the query and all candidate documents in the same context window, enabling rich interactions before extracting contextual embeddings from each document's final token. The new model achieves state-of-the-art BEIR performance with 61.94 nDCG@10 while being significantly smaller than other models with comparable performance.
--- [2004.12832] ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over B :: Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that indepen
--- [2603.25248] ColBERT-Att: Late-Interaction Meets Attention for Enhanced Retrieval :: Vector embeddings from pre-trained language models form a core component in Neural Information Retrieval systems across a multitude of knowledge extraction tasks. The paradigm of late interaction, introduced in ColBERT, demonstrates high accuracy along with runtime efficiency. However, the current formulation fails to take into account the attention weights of query and document terms, which intuitively capture the "importance" of similarities between them, that might lead to a better understanding of relevance between the queries and documents. This work proposes ColBERT-Att, to explicitly integrate attention mechanism into the late interact

######## U4-5 | 도메인 특화 문서용으로 임베딩 모델을 파인튜닝하는 연구들 정리해줘 | direct_answer/B | 92.3s
컨텍스트: 2506.17277, 2410.18344, 2406.04165, 2412.17364
=== 답
<b>서론</b>
제공된 문서들은 도메인 특화(화학·과학) 환경에서 텍스트 임베딩 모델을 파인튜닝하거나 평가하는 연구들을 다루고 있습니다. 각 접근법은 모델 설계, 데이터 선택 및 손실 함수 최적화에 초점을 맞추어 검색 성능을 향상시키려는 목표를 공유합니다.

<b>본론</b>
1. <b>Chunk Twice, Embed Once</b>: 화학에 특화된 RAG 시스템에서 chunking 전략과 임베딩 모델을 대규모로 체계적으로 평가했으며, Nomic·Intfloat E5와 같은 retrieval‑optimized 모델이 SciBERT보다 현저히 우수한 성능을 보인다고 보고합니다 [2506.17277v1]
2. <b>Aggregated Knowledge Model</b>: Lawrence Berkeley National Laboratory ScienceIT 도메인에 맞춘 폐쇄형 QA 시스템을 강화하기 위해 파인튜닝과 RAG 모델을 결합한 새로운 접근법을 제시하고, 해당 통찰은 특정 분야에 특화된 QA 시스템 개발에도 적용 가능하다고 언급합니다 [2410.18344v1]
3. <b>Repurposing Language Models into Embedding Models</b>: 전체 fine‑tuning 과 low‑rank adaptation을 각각 저·고 컴퓨팅 예산에서 최적의 임베딩 모델로 만들 수 있음을 확인했습니다[2406.04165v2].
4. <b>Efficient Fine-Tuning Methodology (CLP)</b>: 데이터 선택, 손실 함수 및 아키텍처를 포함한 효율적인 파인튜닝 방법론을 제시하여 사전 학습된 텍스트 임베딩 모델의 정보 검색 성능을 향상시켰으며, 관련 코드는 GitHub에 공개되어 있습니다[2412.17364v1].

<b>결론</b>
제공된 문서들은 도메인 특화 문서에 대한 임베딩 모델 파인튜닝 연구 결과를 제시하고 있습니다. 먼저, [2506.17277v1]은 화학 분야 검색 강화 생성(RAG)에서 retrieval-optimized embeddings(예: Nomic, Intfloat E5 변형)이 SciBERT와 같은 도메인 특화 모델보다 크게 우수함을 보여줍니다[2506.17277v1]. 두 번째로, [2406.04165v2]은 전량 파인튜닝과 저랭크 적응 파인튜닝이 각각 낮은 및 높은 컴퓨팅 예산에서 최적 모델을 생성한다는 점을 강조하며, 이는 계산 비용에 따라 다른 접근법이 효과적임을 시사합니다[2406.04165v2]. 마지막으로, [2412.17364v1]는 정보 검색을 위한 텍스트 임베딩 모델의 효율적인 파인튜닝 방법론을 제시하고, 해당 연구의 코드는 GitHub에 공개되어 있습니다[2412.17364v1]. 이러한 결과들은 도메인과 데이터 유형에 따라 최적의 파인튜닝 전략이 달라질 수 있음을 보여줍니다.
--- [2506.17277] Chunk Twice, Embed Once: A Systematic Study of Segmentation and Representation Trade-offs  :: Retrieval-Augmented Generation (RAG) systems are increasingly vital for navigating the ever-expanding body of scientific literature, particularly in high-stakes domains such as chemistry. Despite the promise of RAG, foundational design choices -- such as how documents are segmented and represented -- remain underexplored in domain-specific contexts. This study presents the first large-scale, systematic evaluation of chunking strategies and embedding models tailored to chemistry-focused RAG systems. We investigate 25 chunking configurations across five method families and evaluate 48 embedding models on three chemistry-specific benchmarks, inc
--- [2410.18344] Aggregated Knowledge Model: Enhancing Domain-Specific QA with Fine-Tuned and Retrieval-Aug :: This paper introduces a novel approach to enhancing closed-domain Question Answering (QA) systems, focusing on the specific needs of the Lawrence Berkeley National Laboratory (LBL) Science Information Technology (ScienceIT) domain. Utilizing a rich dataset derived from the ScienceIT documentation, our study embarks on a detailed comparison of two fine-tuned large language models and five retrieval-augmented generation (RAG) models. Through data processing techniques, we transform the documentation into structured context-question-answer triples, leveraging the latest Large Language Models (AWS Bedrock, GCP PaLM2, Meta LLaMA2, OpenAI GPT-4, Go
--- [2406.04165] Repurposing Language Models into Embedding Models: Finding the Compute-Optimal Recipe :: Text embeddings are essential for many tasks, such as document retrieval, clustering, and semantic similarity assessment. In this paper, we study how to contrastively train text embedding models in a compute-optimal fashion, given a suite of pre-trained decoder-only language models. Our innovation is an algorithm that produces optimal configurations of model sizes, data quantities, and fine-tuning methods for text-embedding models at different computational budget levels. The resulting recipe, which we obtain through extensive experiments, can be used by practitioners to make informed design choices for their embedding models. Specifically, o
--- [2412.17364] Efficient fine-tuning methodology of text embedding models for information retrieval: cont :: Text embedding models play a crucial role in natural language processing, particularly in information retrieval, and their importance is further highlighted with the recent utilization of RAG (Retrieval- Augmented Generation). This study presents an efficient fine-tuning methodology encompassing data selection, loss function, and model architecture to enhance the information retrieval performance of pre-trained text embedding models. In particular, this study proposes a novel Contrastive Learning Penalty function that overcomes the limitations of existing Contrastive Learning. The proposed methodology achieves significant performance improvem

######## U4-6 | 여러 문서를 거쳐야 답이 나오는 multi-hop RAG 연구 동향 정리해줘 | direct_answer/B | 131.4s
컨텍스트: 2408.11875, 2401.15391, 2502.01113, 2412.01572
=== 답
<b>서론</b>
Multi-hop 질문을 해결하기 위해 최근 연구들은 복잡한 추론 과정을 지원하도록 설계된 새로운 RAG 프레임워크를 제안하고 있습니다. 이러한 접근법에는 <b>Hierarchical Retrieval-Augmented Generation Model with Rethink</b>, <b>MultiHop-RAG 데이터셋 및 벤치마크</b>, 그리고 그래프 기반 모델인 <b>GFM‑RAG</b>가 포함됩니다.

<b>본론</b>
1. <b>HiRAG</b>: Decomposer, Definer, Retriever, Filter, Summarizer 다섯 개의 모듈로 구성된 새로운 프레임워크를 제안하고, 네 개 데이터셋에서 기존 최첨단 모델을 대부분 능가하는 성능을 보였습니다[2408.11875v1]
2. <b>MultiHop‑RAG</b>: 지식베이스와 다중 홉 쿼리 집합이 포함된 새 데이터셋과 벤치마크 도구를 개발하여, 현재 RAG 방법이 다중 홉 질문에서 Retrieval 및 Answering에 만족스럽지 못함을 입증했습니다[2401.15391v1]
3. <b>GFM‑RAG</b>: 그래프 기반 모델(GFM)을 활용한 새로운 GFM‑RAG를 도입하고, 세 개의 다중 홉 QA 데이터셋과七个 도메인 특화 RAG 데이터셋에서 최첨단 성능을 달성하며 효율성과 신경 스케일링 법칙과의 정렬성을 유지했습니다[2502.01113v3]
4. <b>MBA‑RAG</b>: 쿼리 복잡도에 따라 가장 적합한 Retrieval 전략을 동적으로 선택하는 강화학습 기반 프레임워크를 제안하고, 단일 홉 및 다중 홉 데이터셋에서 새로운 최첨단 결과를 달성하면서 검색 비용을 감소시켰습니다[2412.01572v4]

<b>결론</b>
제공된 문서들은 모두 복잡한 추론이 필요한 Multi-hop 질문 처리에 초점을 맞추고 있으며, 각각의 접근법은 기존 RAG 방법들의 한계를 극복하기 위해 설계되었습니다. HiRAG는 모듈화된 계층 구조를 통해 성능을 향상시키고, GFM‑RAG은 그래프 기반 모델로 효율성과 확장성을 강조하며, MBA‑RAG와 MultiHop‑RAG 데이터셋/벤치마크는 각각 적응형 전략과 평가 도구를 제공함으로써 연구 흐름이 점차 다각화되고 있음을 보여줍니다.
--- [2408.11875] Hierarchical Retrieval-Augmented Generation Model with Rethink for Multi-hop Question Answ :: Multi-hop Question Answering (QA) necessitates complex reasoning by integrating multiple pieces of information to resolve intricate questions. However, existing QA systems encounter challenges such as outdated information, context window length limitations, and an accuracy-quantity trade-off. To address these issues, we propose a novel framework, the Hierarchical Retrieval-Augmented Generation Model with Rethink (HiRAG), comprising Decomposer, Definer, Retriever, Filter, and Summarizer five key modules. We introduce a new hierarchical retrieval strategy that incorporates both sparse retrieval at the document level and dense retrieval at the c
--- [2401.15391] MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries :: Retrieval-augmented generation (RAG) augments large language models (LLM) by retrieving relevant knowledge, showing promising potential in mitigating LLM hallucinations and enhancing response quality, thereby facilitating the great adoption of LLMs in practice. However, we find that existing RAG systems are inadequate in answering multi-hop queries, which require retrieving and reasoning over multiple pieces of supporting evidence. Furthermore, to our knowledge, no existing RAG benchmarking dataset focuses on multi-hop queries. In this paper, we develop a novel dataset, MultiHop-RAG, which consists of a knowledge base, a large collection of m
--- [2502.01113] GFM-RAG: Graph Foundation Model for Retrieval Augmented Generation :: Retrieval-augmented generation (RAG) has proven effective in integrating knowledge into large language models (LLMs). However, conventional RAGs struggle to capture complex relationships between pieces of knowledge, limiting their performance in intricate reasoning that requires integrating knowledge from multiple sources. Recently, graph-enhanced retrieval augmented generation (GraphRAG) builds graph structure to explicitly model these relationships, enabling more effective and efficient retrievers. Nevertheless, its performance is still hindered by the noise and incompleteness within the graph structure. To address this, we introduce GFM-RA
--- [2412.01572] MBA-RAG: a Bandit Approach for Adaptive Retrieval-Augmented Generation through Question Co :: Retrieval Augmented Generation (RAG) has proven to be highly effective in boosting the generative performance of language model in knowledge-intensive tasks. However, existing RAG framework either indiscriminately perform retrieval or rely on rigid single-class classifiers to select retrieval methods, leading to inefficiencies and suboptimal performance across queries of varying complexity. To address these challenges, we propose a reinforcement learning-based framework that dynamically selects the most suitable retrieval strategy based on query complexity. % our solution Our approach leverages a multi-armed bandit algorithm, which treats eac

######## U5-1 | HNSW 인덱스 파라미터가 검색 정확도와 속도에 주는 영향을 분석한 연구 있어? | direct_answer/B | 85.0s
컨텍스트: 2608.00229, 2602.23368, 2411.07396, 2602.07297, 2504.20018
=== 답
<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>HNSW</b>: HNSW는 높은 정확도를 여러 시나리오에서 달성하지만, 그래프 구조를 구축하는 데 시간이 많이 걸리고 복잡도가 높아 시간 효율성을 공정하게 비교하기 어렵다는 한계가 있다[2602.07297v1].
2. <b>MINT (Multi-Vector Search Index Tuning)</b>: MINT 프레임워크는 HNSW와 DiskANN과 같은 벡터 인덱스를 지원하며, 지연 시간을 최소화하면서 저장 및 재현율 제약 조건을 만족하도록 최적화된 인덱스를 제안한다[2504.20018v3].

<b>결론</b>
HNSW는 여러 시나리오에서 높은 정확도를 달성하지만, 그래프 구조 구축에 필요한 시간이 과도하고 복잡하여 시간 효율성을 공정하게 비교하기 어렵다는 결과가 보고되었습니다[2602.07297v1]. 반면, ANNOY와 IVF-PQ는 빠른 성능을 보였으나 KNN에 비해 정확도가 낮았습니다[2602.07297v1]. 이러한 결과는 HNSW가 정확도 측면에서 우수하지만 속도에서는 제한적이며, 다른 인덱스들은 속도는 빠르지만 정확도가 떨어지는 상충 관계를 보여줍니다.
--- [2602.07297] Progressive Searching for Retrieval in RAG :: Retrieval Augmented Generation (RAG) is a promising technique for mitigating two key limitations of large language models (LLMs): outdated information and hallucinations. RAG system stores documents as embedding vectors in a database. Given a query, search is executed to find the most related documents. Then, the topmost matching documents are inserted into LLMs' prompt to generate a response. Efficient and accurate searching is critical for RAG to get relevant information. We propose a cost-effective searching algorithm for retrieval process. Our progressive searching algorithm incrementally refines the candidate set through a hierarchy of s
--- [2504.20018] MINT: Multi-Vector Search Index Tuning :: Vector search plays a crucial role in many real-world applications. In addition to single-vector search, multi-vector search becomes important for multi-modal and multi-feature scenarios today. In a multi-vector database, each row is an item, each column represents a feature of items, and each cell is a high-dimensional vector. In multi-vector databases, the choice of indexes can have a significant impact on performance. Although index tuning for relational databases has been extensively studied, index tuning for multi-vector search remains unclear and challenging. In this paper, we define multi-vector search index tuning and propose a framew

######## U5-2 | 임베딩 벡터를 양자화해서 메모리를 줄이면서 검색 성능을 유지하는 방법 찾아줘 | direct_answer/B | 69.2s
컨텍스트: 2601.10155, 2506.18879
=== 답
<b>서론</b>
임베딩 벡터를 <b>양자화</b>하면 메모리 사용량을 크게 줄일 수 있지만, 양자화된 상태를 이용해 검색이나 어텐션 연산을 수행하려면 디코더가 필요해 추가적인 계산 비용이 발생합니다. 이러한 trade‑off를 해결하면서도 높은 정확도를 유지하는 방법이 필요합니다.

<b>본론</b>
1. <b>LOOKAT</b>: 키 벡터를 서브스페이스로 분할하고 각 서브공간을 독립적으로 양자화한 뒤, lookup 테이블과 비대칭 거리 계산을 통해 어텐션 점수를 계산합니다. 이 방식은 메모리‑바운드에서 컴퓨트‑바운드로 전환되어 64× 압축(95.7 % 정확도) 및 32× 압축(95.0 % 정확도)을 달성하며, 아키텍처 변경이나 재학습 없이 순위 상관관계 ρ&gt;0.95를 유지합니다[2601.10155v1].
2. <b>CommVQ</b>: 가산형 양자화와 경량 인코더·코드북으로 KV 캐시를 압축하고, RoPE와 교환 가능한 코드북을 EM 알고리즘으로 학습시켜 어텐션 메커니즘에 효율적으로 통합합니다. 이 접근은 FP16 KV 캐시 크기를 87.5% 감소시키고(2‑비트 양자화), 최소 정확도 손실로 1‑비트 압축까지 가능하게 합니다[2506.18879v1].

<b>결론</b>
LOOKAT은 GPT‑2에서 64배 압축을 달성하면서 95.7%의 출력 충실도를 유지하고, 32배 압축 시에도 95.0%의 충실도를 확보한다[2601.10155v1]. CommVQ는 FP16 KV 캐시를 2비트 양자화하여 87.5%를 감소시키며 기존 최첨단 KV 캐시 양자화 방법보다 우수한 성능을 보인다[2506.18879v1]. 두 연구 모두 임베딩 벡터(또는 KV 캐시)를 양자화함으로써 메모리 사용량을 크게 줄이면서도 검색·생성 성능을 거의 손실하지 않는다는 공통된 결론을 제시한다.
--- [2601.10155] LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers :: Compressing the KV cache is a required step to deploy large language models on edge devices. Current quantization methods compress storage but fail to reduce bandwidth as attention calculation requires dequantizing keys from INT4/INT8 to FP16 before use. We observe that attention scoring is mathematically equivalent to the inner product similarity search and we can apply some compression techniques from vector databases to compress KV-cache better. We propose LOOKAT, which applies product quantization and asymmetric distance computation, to transformer architecture by decomposing key vectors into subspaces, learning codebooks and computing at
--- [2506.18879] CommVQ: Commutative Vector Quantization for KV Cache Compression :: Large Language Models (LLMs) are increasingly used in applications requiring long context lengths, but the key-value (KV) cache often becomes a memory bottleneck on GPUs as context grows. To address this, we propose Commutative Vector Quantization (CommVQ) to significantly reduce memory usage for long-context LLM inference. We first introduce additive quantization with a lightweight encoder and codebook to compress the KV cache, which can be decoded via simple matrix multiplication. To further reduce computational costs during decoding, we design the codebook to be commutative with Rotary Position Embedding (RoPE) and train it using an Expect

######## U5-3 | 메타데이터 필터링과 근사 최근접 검색을 같이 할 때 성능 문제를 다룬 연구 있어? | direct_answer/B | 79.3s
컨텍스트: 2508.16263, 2402.00943, 2605.17992, 2609.15058
=== 답
<b>서론</b>
메타데이터(또는 라벨) 필터링과 근사 최근접 검색(ANN) 을 동시에 수행하는 작업은 <b>속도</b>와 <b>정확성</b>(recall) 사이의 트레이드오프가 발생하기 때문에 어려운 문제입니다. 특히 다양한 속도와 선택성에 따라 성능이 크게 달라져 일관된 평가 기준을 마련해야 합니다.

<b>본론</b>
1. <b>Filtering ANN</b>: 기존 필터링 기반 근사 최근접 검색 알고리즘들의 핵심 기술과 설계 차이점을 체계적으로 분류하고, 4개 데이터셋에서 최대 10백만 항목까지 확장하여 실험 평가를 수행했습니다[2508.16263v2].
2. <b>Window Filters (c‑approximate window search)</b>: 라벨 범위를 지정해 최근접 이웃을 찾는 문제를 정의했으며, 기존 솔루션 대비 동일한 recall 수준에서도 속도 향상을 달성하는 모듈형 트리 기반 프레임워크를 제안하고 이론적 분석과 실험 결과를 제시했습니다[2402.00943v2].
3. <b>PipeANN‑Filter</b>: SSD 환경에서 속성 검증 후 상위 k개 벡터를 탐색하도록 설계된 필터링 시스템으로, Bloom filter 같은 확률 데이터 구조로 유효 후보 집합을 확장해 I/O 비용을 크게 줄이고 검색 지연과 처리량을 개선했습니다[2605.17992v1].
4. <b>LSSG (Label‑Stratified Similarity Graph)</b>: 라벨 세트가 층화된 유사도 임계값 내에서 연결되는 그래프를 정의하고, 점진적 삽입 알고리즘으로 중복 에지를 제거하며 MinHash 구조로 대규모 라벨에 대한 확장성을 확보했습니다[2609.15058v1].

<b>결론</b>
제공된 문서들은 메타데이터 필터링과 근사 최근접 검색을 결합한 연구가 존재함을 보여준다. [2508.16263v2]은 10개의 알고리즘과 12개의 방법을 대상으로 4개 데이터셋에서 광범위한 실험 평가를 수행했으며, 가지치기, 엔트리 포인트 선택, 엣지 필터링 비용이 전체 성능에 미치는 영향을 분석했다. 또한 [2402.00943v2]는 최근 연구가 벡터-메타데이터 검색을 결합한 트리 기반 엔진과 범위 기반 필터를 제시하고, 역사적 쿼리와 배치 처리를 통해 성능 향상을 달성했다고 보고한다. 이러한 결과들은 데이터 규모와 조건에 따라 성능 개선 효과가 다르게 나타날 수 있음을 시사한다.
--- [2508.16263] Attribute Filtering in Approximate Nearest Neighbor Search: An In-depth Experimental Study :: With the growing integration of structured and unstructured data, new methods have emerged for performing similarity searches on vectors while honoring structured attribute constraints, i.e., a process known as Filtering Approximate Nearest Neighbor (Filtering ANN) search. Since many of these algorithms have only appeared in recent years and are designed to work with a variety of base indexing methods and filtering strategies, there is a pressing need for a unified analysis that identifies their core techniques and enables meaningful comparisons. In this work, we present a unified Filtering ANN search interface that encompasses the latest alg
--- [2402.00943] Approximate Nearest Neighbor Search with Window Filters :: We define and investigate the problem of $\textit{c-approximate window search}$: approximate nearest neighbor search where each point in the dataset has a numeric label, and the goal is to find nearest neighbors to queries within arbitrary label ranges. Many semantic search problems, such as image and document search with timestamp filters, or product search with cost filters, are natural examples of this problem. We propose and theoretically analyze a modular tree-based framework for transforming an index that solves the traditional c-approximate nearest neighbor problem into a data structure that solves window search. On standard nearest ne
--- [2605.17992] PipeANN-Filter: An Efficient Filtered Vector Search System on SSD :: We propose PipeANN-Filter, an efficient filtered vector search system on SSD. Unlike existing systems that explore only valid vectors (i.e., those satisfying the attribute constraints) during search, PipeANN-Filter explores a superset of valid vectors, and performs attribute verification after getting the top-k closest result vectors. This allows PipeANN-Filter to leverage probabilistic data structures (e.g., Bloom filters) to identify the superset, trading off a small number of false-positive vector explorations for a massive reduction in SSD I/O for attribute reading. Evaluations show that PipeANN-Filter improves search latency and throughp
--- [2609.15058] Fast Label-Filtering Approximate Nearest Neighbor Search via Progressive Label Set Stratif :: Approximate nearest neighbor search (ANNS) retrieves the most similar vectors to a query vector in high-dimensional space. Label-filtering ANNS (LFANNS) extends ANNS with a label filter that the labels of base vectors must satisfy a set relation (e.g., equality, containment, or overlap) with the query labels. Existing LFANNS indices suffer from inconsistent performance across different filter types and degraded scalability under varying label scale and distribution. In this paper, we define label-stratified similarity graph (LSSG), where edges connect neighboring vectors whose label sets fall within stratified similarity thresholds. To implem

######## U5-4 | 벡터 검색 인덱스 최적화 연구들 정리해줘 | direct_answer/B | 68.4s
컨텍스트: 2504.20018, 2503.17911, 2511.14748, 2605.17992, 2510.20296, 2601.01937
=== 답
<b>서론</b>
벡터 검색에서 인덱스 최적화는 지연 시간, 저장 공간 및 재현율 요구사항을 동시에 만족하도록 설계된 핵심 과제이다. 최근 연구들은 다양한 하드웨어 환경과 워크로드에 맞춰 효율적인 인덱싱 기법을 제시하고 있다.

<b>본론</b>
1. <b>MINT</b>: 다중 벡터 검색 작업량에 대해 지연 시간을 최소화하면서 저장 및 재현율 제약을 충족하는 알고리즘을 개발하였다[2504.20018v3]
2. <b>VSAG</b>: 그래프 기반 근접 이웃 탐색 성능 향상을 목표로 오픈소스 프레임워크를 제공하며, HNSWlib 대비 최대 4배 속도 향상과 동일한 정확도를 달성한다[2503.17911v3]
3. <b>Cloud-Native Vector Search 분석</b>: 온‑클라우드 환경에서는 디스크 검색보다 다른 인덱싱 및 파라미터화가 필요함을 발견하고, 캐시 최적화와의 상호작용을 연구하였다[2511.14748v2]
4. <b>PipeANN-Filter</b>: SSD 기반 필터링 벡터 검색 시스템으로 Bloom filter 등 확률적 구조를 활용해 위상집합 식별과 함께 탐색 오류는 최소화하면서 지연 시간 및 처리량을 크게 개선한다[2605.17992v1]

<b>결론</b>
벡터 검색 인덱스 최적화 연구들은 각각 다른 접근법과 성능 향상을 보고하고 있다. MINT는 다중 벡터 검색 작업에 대해 지연 시간을 2.1배에서 8.3배까지 단축하며 저장 및 재현율 제약을 만족한다[2504.20018v3]. VSAG는 그래프 기반 근접 이웃 검색에서 HNSWlib 대비 최대 4배 속도 향상을 달성하면서 정확도는 동일하게 유지한다[2503.17911v3]. PipeANN-Filter는 Bloom 필터와 같은 확률적 데이터 구조를 활용해 위상집합을 식별함으로써 지연 시간과 처리량을 기존 최첨단 시스템보다 개선한다[2605.17992v1]. 이러한 결과들은 각 연구가 서로 다른 최적화 기법과 평가 조건에서 유사한 목표인 검색 성능 향상을 달성하고 있음을 보여준다.
--- [2504.20018] MINT: Multi-Vector Search Index Tuning :: Vector search plays a crucial role in many real-world applications. In addition to single-vector search, multi-vector search becomes important for multi-modal and multi-feature scenarios today. In a multi-vector database, each row is an item, each column represents a feature of items, and each cell is a high-dimensional vector. In multi-vector databases, the choice of indexes can have a significant impact on performance. Although index tuning for relational databases has been extensively studied, index tuning for multi-vector search remains unclear and challenging. In this paper, we define multi-vector search index tuning and propose a framew
--- [2503.17911] VSAG: An Optimized Search Framework for Graph-based Approximate Nearest Neighbor Search :: Approximate nearest neighbor search (ANNS) is a fundamental problem in vector databases and AI infrastructures. Recent graph-based ANNS algorithms have achieved high search accuracy with practical efficiency. Despite the advancements, these algorithms still face performance bottlenecks in production, due to the random memory access patterns of graph-based search and the high computational overheads of vector distance. In addition, the performance of a graph-based ANNS algorithm is highly sensitive to parameters, while selecting the optimal parameters is cost-prohibitive, e.g., manual tuning requires repeatedly re-building the index. This pape
--- [2511.14748] Cloud-Native Vector Search: A Comprehensive Performance Analysis :: Vector search has been widely employed in recommender system and retrieval-augmented-generation pipelines, commonly performed with vector indexes to efficiently find similar items in large datasets. Recent growths in both data and task complexity have motivated placing vector indexes onto remote storage -- cloud-native vector search, which cloud providers have recently introduced services for. Yet, despite varying workload characteristics and various available vector index forms, providers default to using cluster-based indexes, which on paper do adapt well to differences between disk and cloud-based environment: their fetch granularities and
--- [2605.17992] PipeANN-Filter: An Efficient Filtered Vector Search System on SSD :: We propose PipeANN-Filter, an efficient filtered vector search system on SSD. Unlike existing systems that explore only valid vectors (i.e., those satisfying the attribute constraints) during search, PipeANN-Filter explores a superset of valid vectors, and performs attribute verification after getting the top-k closest result vectors. This allows PipeANN-Filter to leverage probabilistic data structures (e.g., Bloom filters) to identify the superset, trading off a small number of false-positive vector explorations for a massive reduction in SSD I/O for attribute reading. Evaluations show that PipeANN-Filter improves search latency and throughp

######## U6-1 | RAG 시스템을 검색과 생성 단계로 나눠 평가하는 프레임워크 연구 있어? | direct_answer/B | 76.8s
컨텍스트: 2408.08067, 2412.12322, 2504.07803
=== 답
<b>서론</b>
RAG 시스템은 <b>검색(retrieval)</b>과 <b>생성(generation)</b>이라는 두 개의 독립된 모듈로 구성되어 있어, 각 단계별 성능을 정밀하게 측정하고 비교하는 것이 어렵습니다. 이러한 다단계 구조 때문에 전체적인 평가가 복잡해집니다.

<b>본론</b>
1. <b>RAGChecker</b>: 검색 및 생성 모듈에 대한 진단 메트릭트를 포함하여 세분화된 평가를 제공합니다[2408.08067v2].
2. <b>SCARF (System for Comprehensive Assessment of RAG Frameworks)</b>: 엔드‑투‑엔드 블랙박스 평가 방법과 다중 배포 구성을 지원하며, 응답 일관성 등을 포함한 종합적인 성능 보고서를 생성합니다[2504.07803v1].

<b>결론</b>
제공된 문서들에 따르면, RAG 시스템을 검색과 생성 단계로 나누어 평가하는 프레임워크 연구가 존재합니다. [2408.08067v2]은 RAGChecker를 통해 검색 및 생성 모듈에 대한 진단 메트릭을 통합한 정교한 평가 프레임워크를 제안하고, 메타 평가를 통해 인간 판단과의 상관관계가 다른 메트릭보다 유의미하게 높음을 검증했습니다. 또한 [2504.07803v1]에서는 SCARF라는 모듈형·유연한 평가 프레임워크를 소개하며, REST API 인터페이스를 활용해 다양한 RAG 프레임워크와 구성을 비교할 수 있는 엔드투엔드 블랙박스 평가 방법을 제시했습니다. 두 연구 모두 RAG 시스템의 검색과 생성 단계를 구분하여 평가하는 접근법을 취하고 있으나, 각각 다른 메트릭 설계와 적용 방식(정교한 진단 메트릭 vs 모듈형·유연한 벤치마킹) 을 통해 서로 보완적인 결과를 제공합니다.
--- [2408.08067] RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation :: Despite Retrieval-Augmented Generation (RAG) showing promising capability in leveraging external knowledge, a comprehensive evaluation of RAG systems is still challenging due to the modular nature of RAG, evaluation of long-form responses and reliability of measurements. In this paper, we propose a fine-grained evaluation framework, RAGChecker, that incorporates a suite of diagnostic metrics for both the retrieval and generation modules. Meta evaluation verifies that RAGChecker has significantly better correlations with human judgments than other evaluation metrics. Using RAGChecker, we evaluate 8 RAG systems and conduct an in-depth analysis 
--- [2504.07803] A System for Comprehensive Assessment of RAG Frameworks :: Retrieval Augmented Generation (RAG) has emerged as a standard paradigm for enhancing the factual accuracy and contextual relevance of Large Language Models (LLMs) by integrating retrieval mechanisms. However, existing evaluation frameworks fail to provide a holistic black-box approach to assessing RAG systems, especially in real-world deployment scenarios. To address this gap, we introduce SCARF (System for Comprehensive Assessment of RAG Frameworks), a modular and flexible evaluation framework designed to benchmark deployed RAG applications systematically. SCARF provides an end-to-end, black-box evaluation methodology, enabling a limited-ef

######## U6-2 | LLM-as-a-judge의 편향(위치 편향, 길이 편향)을 분석한 연구 찾아줘 | direct_answer/B | 45.6s
컨텍스트: 2410.02736, 2504.09946, 2506.22316
=== 답
<b>서론</b>
LLM-as-a-Judge는 자동 평가 도구로 널리 쓰이지만, <b>위치 편향</b>과 <b>길이 편향</b> 같은 시스템적 왜곡에 취약해 신뢰성이 떨어집니다. 이러한 편향을 정량화하고 완화하는 연구가 필요합니다.

<b>본론</b>
1. <b>CALM</b>: 12가지 잠재적인 편향을 식별했으며, 그중 위치와 길이 등 기존 분석이 제한적이었던 영역을 포함합니다[2506.22316v4]. LLM-as-a-Judge에서 길이를 포함한 여섯 가지 유형의 편향(길이 편향, 구체성 편향, 빈 참조편향 등) 을 식별했습니다[2506.22316v4].
<b>결론</b>
제공된 문서들은 CALM과 OffsetBias가 각각 위치·길이에 대한 기존 분석의 한계를 보완하고 구체적인 편향을 정의한다는 공통점을 가집니다. 따라서 LLM-as-a-Judge에서 위치와 길이 편향을 연구한 주요 접근법은 이 두 프레임워크에 해당합니다.
--- [2506.22316] Evaluating Scoring Bias in LLM-as-a-Judge :: The "LLM-as-a-Judge" paradigm, using Large Language Models (LLMs) as automated evaluators, is pivotal to LLM development, offering scalable feedback for complex tasks. However, the reliability of these judges is compromised by various biases. Existing research has heavily concentrated on biases in comparative evaluations. In contrast, scoring-based evaluations-which assign an absolute score and are often more practical in industrial applications-remain under-investigated. To address this gap, we undertake the first dedicated examination of scoring bias in LLM judges. We shift the focus from biases tied to the evaluation targets to those origi

######## U6-3 | RAG 평가용 질문-정답 데이터를 LLM으로 합성하는 방법 알려줘 | direct_answer/B | 68.5s
컨텍스트: 2408.01262, 2505.11626
=== 답
<b>서론</b>
RAG 시스템은 외부 지식을 활용해 답변 생성하지만, <b>시나리오별 평가 데이터</b>를 구축하는 비용과 적합한 메트릭 부재 때문에 효과성을 검증하기 어렵습니다. 특히 질문‑정답 쌍을 자동으로 합성해야 하는 과정이 핵심 과제입니다.

<b>본론</b>
1. <b>RAGEval</b>: 시나리오에 특화된 RAG 평가 데이터를 자동 생성하며, 스키마 기반 파이프라인으로 고품질 문서·질의·응답·참조 자료를 만들어냅니다[2408.01262v5].
2. <b>THELMA</b>: 레이블이 없는 참조 없이 질문‑소스‑반응을 입력받아 논리적 분해 후 메트릭 점수를 산출하는 다차원 평가 프레임워크를 제공합니다[2505.11626v2].

<b>결론</b>
RAGEval은 자동으로 시나리오별 RAG 평가 데이터셋을 생성하는 프레임워크를 제안하고, ROUGEL과 BLEU보다 사실 정확성을 더 효과적으로 측정하는 세 가지 새로운 평가 지표를 도입하였다[2408.01262v5]. 반면 THELMA는 레이블이 없는 출처나 참조 응답 없이도 RAG 질문 답변 파이프라인을 종합적으로 평가·모니터링할 수 있는 프레임워크를 제시한다[2505.11626v2]. 따라서 두 연구 모두 RAG 시스템의 성능을 평가하는 방법을 제공하지만, RAGEval은 시나리오별 데이터셋 생성과 기존 지표 대비 향상된 정확성 측정에 초점을 맞추고, THELMA는 레이블 없이 전체 파이프라인을 평가한다는 점에서 접근 방식이 다르다.
--- [2408.01262] RAGEval: Scenario Specific RAG Evaluation Dataset Generation Framework :: Retrieval-Augmented Generation (RAG) is a powerful approach that enables large language models (LLMs) to incorporate external knowledge. However, evaluating the effectiveness of RAG systems in specialized scenarios remains challenging due to the high costs of data construction and the lack of suitable evaluation metrics. This paper introduces RAGEval, a framework designed to assess RAG systems across diverse scenarios by generating high-quality documents, questions, answers, and references through a schema-based pipeline. With a focus on factual accuracy, we propose three novel metrics: Completeness, Hallucination, and Irrelevance to evaluate
--- [2505.11626] THELMA: Task Based Holistic Evaluation of Large Language Model Applications-RAG Question A :: We propose THELMA (Task Based Holistic Evaluation of Large Language Model Applications), a reference free framework for RAG (Retrieval Augmented generation) based question answering (QA) applications. THELMA consist of six interdependent metrics specifically designed for holistic, fine grained evaluation of RAG QA applications. THELMA framework helps developers and application owners evaluate, monitor and improve end to end RAG QA pipelines without requiring labelled sources or reference responses.We also present our findings on the interplay of the proposed THELMA metrics, which can be interpreted to identify the specific RAG component needi

######## U6-4 | 검색 평가 지표 nDCG랑 recall@k 차이가 뭐야? | direct_answer/B | 70.5s
컨텍스트: 2510.21440, 2512.20854
=== 답
<b>서론</b>
검색 평가 지표 <b>nDCG</b>와 <b>Recall@k</b>는 각각 순위별 관련성 점수와 상위 K개 문서 내 포함된 전체 관련 문서 비율이라는 점에서 근본적인 차이가 있습니다. nDCG은 로그 할인 함수를 적용해 높은 순위에 있는 문서를 더 크게 가중치로 부여하고, Recall@k는 특정 K까지의 검색 결과에서 얼마나 많은 관련 항목이 포함되었는지 측정합니다[2510.21440v1][2512.20854v2].

<b>본론</b>
1. <b>Normalized Discounted Cumulative Gain (nDCG)</b>: 순위별 점수화된 관련성을 이용해 로그 할인 함수를 적용해 상위 문서에 더 큰 가중치를 부여하고, 하위 문서는 기여도를 감소시킵니다[2510.21440v1]
2. <b>Recall@k</b>: 검색된 결과 중 K개까지의 항목에서 전체 관련 문서가 차지하는 비율을 계산하며, 실제 데이터셋에서는 총 관련 문서 수가 알려져 있지 않아 정확한 recall 값을 구하기 어려운 경우가 많습니다[2512.20854v2].

<b>결론</b>
제공된 문서들은 nDCG와 recall@k에 대한 직접적인 비교 결과를 제시하지 않습니다. [2510.21440v1]은 nDCG가 등급화된 관련성 판단을 활용한다는 점을 강조하고, [2512.20854v2]는 recall이 제한된 관련 문서 수(2-15개) 환경에서 평가되는 전략을 검토한다고 언급합니다. 따라서 두 지표의 차이와 성능 비교에 대한 결론은 제공된 결과만으로는 도출할 수 없습니다.
--- [2510.21440] Redefining Retrieval Evaluation in the Era of LLMs :: Traditional Information Retrieval (IR) metrics, such as nDCG, MAP, and MRR, assume that human users sequentially examine documents with diminishing attention to lower ranks. This assumption breaks down in Retrieval Augmented Generation (RAG) systems, where search results are consumed by Large Language Models (LLMs), which, unlike humans, process all retrieved documents as a whole rather than sequentially. Additionally, traditional IR metrics do not account for related but irrelevant documents that actively degrade generation quality, rather than merely being ignored. Due to these two major misalignments, namely human vs. machine position disc
--- [2512.20854] How important is Recall for Measuring Retrieval Quality? :: In realistic retrieval settings with large and evolving knowledge bases, the total number of documents relevant to a query is typically unknown, and recall cannot be computed. In this paper, we evaluate several established strategies for handling this limitation by measuring the correlation between retrieval quality metrics and LLM-based judgments of response quality, where responses are generated from the retrieved documents. We conduct experiments across multiple datasets with a relatively low number of relevant documents (2-15). We also introduce a simple retrieval quality measure that performs well without requiring knowledge of the total

######## U6-5 | LLM 애플리케이션 회귀 테스트나 지속 평가 방법 연구들 정리해줘 | direct_answer/B | 90.7s
컨텍스트: 2503.05070, 2601.00497, 2501.00217, 2503.22851, 2601.18827
=== 답
<b>서론</b>
LLM 애플리케이션에 대한 <b>회귀 테스트</b>와 지속 평가를 자동화하는 연구들이 최근 활발히 진행되고 있습니다. 이러한 접근들은 모델이 새로운 프롬프트나 워크플로우 변경 시에도 일관된 성능을 유지하도록 검증합니다.

<b>본론</b>
1. <b>PromptPex</b>: LLM 기반 도구로 주어진 프롬프트에 대한 단위 테스트를 자동으로 생성·평가하며, 8개의 벤치마크 프롬프트와 네 가지 다름 모델에서 무효 출력을 유발하는지 확인하여 품질을 측정한다 [2503.05070v2]
2. <b>STELLAR</b>: 자동 검색‑기반 프레임워크로 LLM 기반 애플리케이션에 부적절한 응답을 유도하는 텍스트 입력을 체계적으로 발견하며, 세 개의 대화형 QA 시스템 평가에서 기존 기법보다 최대 4.3배(평균 2.5배) 더 많은 실패를 노출한다 [2601.00497v2]
3. <b>Agent‑oriented automated testing</b>: LLM이 인간 개입을 줄이고 테스트 효율성을 높이는 에이전트 기반 접근법을 제시하고, Python·Java 등 여러 애플리케이션에서 높은 코드 커버리지와 빠른 운영 성능을 입증했다[2501.00217v1]

<b>결론</b>
PromptPex는 프롬프트‑단위 회귀 검증을 자동화하는 반면, STELLAR은 검색 기반으로 시스템 응답의 부적절성을 지속적으로 탐지합니다. 두 방법은 각각 단위 테스트 생성과 실패 사례 발견에 초점을 맞추어 LLM 애플리케이션의 안정성 확보를 지원합니다.
--- [2503.05070] PromptPex: Automatic Test Generation for Language Model Prompts :: Large language models (LLMs) are being used in many applications and prompts for these models are integrated into software applications as code-like artifacts. These prompts behave much like traditional software in that they take inputs, generate outputs, and perform some specific function. However, prompts differ from traditional code in many ways and require new approaches to ensure that they are robust. For example, unlike traditional software the output of a prompt depends on the AI model that interprets it. Also, while natural language prompts are easy to modify, the impact of updates is harder to predict. New approaches to testing, debu
--- [2601.00497] STELLAR: A Search-Based Testing Framework for Large Language Model Applications :: Large Language Model (LLM)-based applications are increasingly deployed across various domains, including customer service, education, and mobility. However, these systems are prone to inaccurate, fictitious, or harmful responses, and their vast, high-dimensional input space makes systematic testing particularly challenging. To address this, we present STELLAR, an automated search-based testing framework for LLM-based applications that systematically uncovers text inputs leading to inappropriate system responses. Our framework models test generation as an optimization problem and discretizes the input space into stylistic, content-related, an
--- [2501.00217] The Potential of LLMs in Automating Software Testing: From Generation to Reporting :: Having a high quality software is essential in software engineering, which requires robust validation and verification processes during testing activities. Manual testing, while effective, can be time consuming and costly, leading to an increased demand for automated methods. Recent advancements in Large Language Models (LLMs) have significantly influenced software engineering, particularly in areas like requirements analysis, test automation, and debugging. This paper explores an agent-oriented approach to automated software testing, using LLMs to reduce human intervention and enhance testing efficiency. The proposed framework integrates LLM

######## U6-6 | 벤치마크 데이터 오염 때문에 평가가 부풀려지는 문제를 다룬 연구 있어? | direct_answer/B | 108.1s
컨텍스트: 2602.12413, 2311.09783, 2402.15938, 2406.18326
=== 답
<b>서론</b>
벤치마크 데이터가 모델 학습에 포함되면 <b>평가 점수가 실제 능력보다 과대</b>하게 나타나는 문제가 발생합니다. 이는 벤치마크 성능과 일반화 능력을 구분하기 어렵게 만들어 신뢰할 수 있는 평가 결과를 얻는 데 큰 걸림돌이 됩니다[2602.12413v1][2311.09783v2].

<b>본론</b>
1. <b>Soft Contamination</b>: 훈련 데이터에 의미적 중복을 포함시켜도 벤치마크 점수가 향상되고, 해당 데이터를 이용한 미세조정 시 진짜 홀드아웃 포인트에서도 성능 향상이 관찰됩니다. 이는 최근 벤치마크 성취가 실제 능력 개선과 함께 테스트 데이터 누적을 반영한 결과임을 시사합니다[2602.12413v1].
2. <b>Retrieval‑based contamination detection &amp; TS‑Guessing</b>: 검색 기반 시스템으로 평가 세트와 사전학습 코퍼스의 중복을 탐색하고, 다중 선택 문제에서 정답을 가리고 모델이 빈칸을 채우도록 하는 \textbf{TS-Guessing} 프로토콜을 제안하여 벤치마크 오염 가능성을 탐지합니다[2311.09783v2].
3. <b>CDD &amp; TED</b>: 출력 분포의 첨도를 이용해 데이터 오염 여부를 판단하는 CDD와, 이를 기반으로 모델 출력을 교정해 평가 성능 향상을 완화하는 TED를 도입하고, DETCON·COMIEVAL 두 벤치마크로 검증을 수행합니다[2402.15938v3].
4. <b>PaCoST</b>: 각 데이터를 동일한 분포의 대응 항목으로 만들고 통계적 신뢰도 분석을 통해 원래 벤치마크보다 모델이 유의하게 더 확신하도록 하는 Paired Confidence Significance Testing 방법을 제안하여 오염 가능성을 탐지하고, 실제 오픈소스 모델을 대상으로 검증했습니다[2406.18326v2].

<b>결론</b>
제공된 연구들은 모두 <b>벤치마크 데이터가 학습에 포함될 때 평가 점수가 과대평가되는 현상</b>을 다루고 있습니다. Soft Contamination은 이러한 누적을 정량화했으며, Retrieval‑based 탐지·TS-Guessing과 CDD/TED는 오염 여부를 식별하고 그 영향을 완화하는 방법을 제시합니다. PaCoST 역시 통계적 신뢰도 분석으로 벤치마크 오염 가능성을 확인했습니다. 따라서 질문에서 찾는 연구들은 [2602.12413v1]~4에 명시된 네 가지 접근법입니다.
--- [2602.12413] Soft Contamination Means Benchmarks Test Shallow Generalization :: If LLM training data is polluted with benchmark test data, then benchmark performance gives biased estimates of out-of-distribution (OOD) generalization. Typical decontamination filters use n-gram matching which fail to detect semantic duplicates: sentences with equivalent (or near-equivalent) content that are not close in string space. We study this soft contamination of training data by semantic duplicates. Among other experiments, we embed the Olmo3 training corpus and find that: 1) contamination remains widespread, e.g. we find semantic duplicates for 78% of CodeForces and exact duplicates for 50% of ZebraLogic problems; 2) including sema
--- [2311.09783] Investigating Data Contamination in Modern Benchmarks for Large Language Models :: Recent observations have underscored a disparity between the inflated benchmark scores and the actual performance of LLMs, raising concerns about potential contamination of evaluation benchmarks. This issue is especially critical for closed-source models and certain open-source models where training data transparency is lacking. In this paper we study data contamination by proposing two methods tailored for both open-source and proprietary LLMs. We first introduce a retrieval-based system to explore potential overlaps between evaluation benchmarks and pretraining corpora. We further present a novel investigation protocol named \textbf{T}estse
--- [2402.15938] Generalization or Memorization: Data Contamination and Trustworthy Evaluation for Large La :: Recent statements about the impressive capabilities of large language models (LLMs) are usually supported by evaluating on open-access benchmarks. Considering the vast size and wide-ranging sources of LLMs' training data, it could explicitly or implicitly include test data, leading to LLMs being more susceptible to data contamination. However, due to the opacity of training data, the black-box access of models, and the rapid growth of synthetic training data, detecting and mitigating data contamination for LLMs faces significant challenges. In this paper, we propose CDD, which stands for Contamination Detection via output Distribution for LLM
--- [2406.18326] PaCoST: Paired Confidence Significance Testing for Benchmark Contamination Detection in La :: Large language models (LLMs) are known to be trained on vast amounts of data, which may unintentionally or intentionally include data from commonly used benchmarks. This inclusion can lead to cheatingly high scores on model leaderboards, yet result in disappointing performance in real-world applications. To address this benchmark contamination problem, we first propose a set of requirements that practical contamination detection methods should follow. Following these proposed requirements, we introduce PaCoST, a Paired Confidence Significance Testing to effectively detect benchmark contamination in LLMs. Our method constructs a counterpart fo

