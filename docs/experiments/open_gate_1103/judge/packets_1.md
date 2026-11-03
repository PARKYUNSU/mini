## O_03

**질문** 문서 청킹 관련 논문 두 편만 골라줘

### 답 A

<b>서론</b>
문서 <b>청킹(chunking)</b> 은 검색‑증강 생성(RAG) 시스템에서 텍스트를 작은 단위로 나누어 인덱싱하고 재검색하는 핵심 전처리 단계이며, 문서의 구조와 의미에 따라 최적화된 청킹 전략을 선택해야 하는 어려움이 존재합니다.

<b>본론</b>
1. <b>Adaptive Chunking</b>: 다섯 가지 고유 메트릭(References Completeness, Intrachunk Cohesion, Document Contextual Coherence, Block Integrity, Size Compliance) 을 이용해 각 문서마다 가장 적합한 청킹 방법을 자동으로 선정하고, LLM‑regex splitter 및 split‑then‑merge recursive splitter와 함께 적용하여 RAG 성능을 크게 향상시킵니다. [2603.25333v1]
2. <b>Element-Based Chunking</b>: 문서를 단순 단락 수준이 아닌 구조적 요소(heading, table 등) 를 기준으로 분할하는 새로운 청킹 방식을 제안하고, 이러한 방식이 정보 검색 정확도와 Q&amp;A 작업에 미치는 영향을 평가합니다. [2402.05131v3]

<b>결론</b>
문서 청킹 관련 두 논문은 각각 다른 도메인과 데이터에 초점을 맞추어 결과를 제시합니다. 첫 번째 연구는 법적, 기술적, 사회과학 분야를 아우르는 다양한 코퍼스에 대해 메트릭 기반 적응형 청킹이 RAG 성능을 크게 향상시킨다고 보고합니다[2603.25333v1]. 반면, 두 번째 연구는 금융 보고서와 같은 특정 도메인에서 요소 유형 기반 청킹이 Q&amp;A 작업의 정확도를 개선한다는 결과를 보여줍니다[2402.05131v3]. 따라서 두 논문은 대상 데이터와 적용 분야가 다르지만, 모두 해당 도메인에 맞는 적절한 청킹 전략을 통해 RAG 성능 향상을 달성했다는 공통점을 가집니다.

_A 컨텍스트 5편_: 2603.25333 Adaptive Chunking: Optimizing Chunking-Method Selection for  · 2402.05131 Financial Report Chunking for Effective Retrieval Augmented  · 2602.16974 Beyond Chunk-Then-Embed: A Comprehensive Taxonomy and Evalua · 2509.11552 HiChunk: Evaluating and Enhancing Retrieval-Augmented Genera · 2601.05265 Cross-Document Topic-Aligned Chunking for Retrieval-Augmente

### 답 B

<b>서론</b>
문서 <b>청킹(chunking)</b> 은 검색‑증강 생성(RAG) 시스템에서 텍스트를 작은 단위로 나누어 인덱싱하고 재검색하는 핵심 전처리 단계이며, 다양한 문서 구조와 의미에 따라 최적의 청킹 전략을 선택해야 하는 어려움이 존재한다.

<b>본론</b>
1. <b>Adaptive Chunking</b>: 다섯 가지 고유 메트릭(References Completeness, Intrachunk Cohesion, Document Contextual Coherence, Block Integrity, Size Compliance) 을 이용해 각 문서마다 가장 적합한 청킹 방법을 자동으로 선정하고, LLM‑regex splitter와 split‑then‑merge recursive splitter를 도입해 RAG 성능을 크게 향상시킨다. [2603.25333v1]
2. <b>Element-Based Chunking</b>: 문서를 구조적 요소(heading, table 등) 로 분할하여 단락 수준보다 더 세분화된 청킹 전략을 제시하고, 이러한 방식이 금융 보고서와 같은 도메인에서 RAG 정확도를 크게 개선한다는 결과를 보여준다. [2402.05131v3]

<b>결론</b>
제공된 문서들은 각각 고유 메트릭 기반의 적응형 선택과 구조적 요소 활용이라는 두 가지 다른 접근법을 통해 청킹 품질을 향상시키고, 이를 적용함으로써 RAG 시스템 전반적인 성능이 유의미하게 증가함을 입증한다.

_B 컨텍스트 5편_: 2603.25333 Adaptive Chunking: Optimizing Chunking-Method Selection for  · 2402.05131 Financial Report Chunking for Effective Retrieval Augmented  · 2602.16974 Beyond Chunk-Then-Embed: A Comprehensive Taxonomy and Evalua · 2509.11552 HiChunk: Evaluating and Enhancing Retrieval-Augmented Genera · 2601.05265 Cross-Document Topic-Aligned Chunking for Retrieval-Augmente

### 인용 블록

- **2603.25333** [인용 AB] Adaptive Chunking: Optimizing Chunking-Method Selection for RAG — [초록] The effectiveness of Retrieval-Augmented Generation (RAG) is highly dependent on how documents are chunked, that is, segmented into smaller units for indexing and retrieval. Yet, commonly used "one-size-fits-all" approaches often fail to capture the nuanced structure and semantics of diverse texts. Despite its central role, chunking lacks a dedicated evaluation framework, making it difficult to assess and compare strategies independently of downstream performance. We challenge this paradigm by introducing Adaptive Chunking, a framework that selects the most suitable chunking strategy for each document based on a set of five novel intrinsic, document-based metrics: References Completeness (RC), Intrachunk Cohesion (ICC), Document Contextual Coherence (DCC), Block Integrity (BI), and Size Compliance (SC), which directly assess chunking quality across key dimensions. To support this fr

- **2402.05131** [인용 AB] Financial Report Chunking for Effective Retrieval Augmented Generation — [초록] Chunking information is a key step in Retrieval Augmented Generation (RAG). Current research primarily centers on paragraph-level chunking. This approach treats all texts as equal and neglects the information contained in the structure of documents. We propose an expanded approach to chunk documents by moving beyond mere paragraph-level chunking to chunk primary by structural element components of documents. Dissecting documents into these constituent elements creates a new way to chunk documents that yields the best chunk size without tuning. We introduce a novel framework that evaluates how chunking based on element types annotated by document understanding models contributes to the overall context and accuracy of the information retrieved. We also demonstrate how this approach impacts RAG assisted Question & Answer task performance. Our research includes a comprehensive analysis 

---

## O_09

**질문** LLM을 평가자로 쓰는 연구 중에 꼭 읽어야 할 논문 두 편만 알려줘

### 답 A

<b>서론</b>
LLM‑based 평가자는 <b>자동화된 점수 부여</b>와 <b>인간 판단과의 정렬</b>, 그리고 <b>perturbation에 대한 견고성</b>이라는 세 가지 핵심 과제를 동시에 만족해야 합니다. 이러한 요구는 모델이 단순한 성능뿐만 아니라 편향과 일관성을 제어할 수 있어야 하기 때문에 어려운 문제입니다.

<b>본론</b>
1. <b>LLM‑based Evaluators under Perturbations</b>: LLM을 평가자로 사용하여 SummEval 및 USR 데이터셋에서 점수와 근거를 생성하고, 입력에 perturbation이 가해졌을 때 견고성이 제한적이며 인간과의 정렬도 낮음을 확인했습니다. [2412.09269v1]
2. <b>LLM‑as-a-Judge Design Study</b>: BIGGENBench와 EvalBiasBench로 평가 설계·decoding 전략·Chain-of-Thought가 신뢰성에 미치는 영향을 분석했으며, 명확한 기준이 있을 때 CoT는 소소한 이득만 제공하고 비결정적 샘플링이 인간 선호도와 정렬을 향상시킨다고 보고했습니다. [2506.13639v1]
3. <b>Cognitive Bias Benchmark for LLM Evaluators</b>: 다양한 크기의 15개 LLM에 대해 Egocentric bias 등 여섯 가지 인지 편향을 측정하는 CoBBLEr 벤치마크를 적용해 평균 비교에서 약 40%의 높은 편향과 인간 선호도와의 RBO 점수 49.6%로 정렬이 부족함을 확인했습니다. [2309.17012v3]
4. <b>Likelihood‑based Mitigation of Evaluation Bias</b>: LLM 평가 시 문장 순열·구조 등 표면적 차이 때문에 발생 가능한 likelihood bias를 조사하고, 편향된 인스턴스를 few-shot 예시로 활용해 in-context 학습으로 이 편향을 완화했으며 데이터‑to-text 및 구문 오류 수정 작업에서 인간 점수와의 상관관계가 크게 향상됨을 보였습니다. [2402.15987v4]

<b>결론</b>
제공한 문서들은 LLM 평가자의 <b>견고성</b>, <b>인간 정렬도</b>, 그리고 다양한 형태의 <b>인지·가능성 편향</b>이 존재한다는 점을 각각 강조하고 있습니다. 따라서 이 네 편의 논문을 반드시 읽어야 합니다.

_A 컨텍스트 5편_: 2412.09269 Towards Understanding the Robustness of LLM-based Evaluation · 2506.13639 An Empirical Study of LLM-as-a-Judge: How Design Choices Imp · 2309.17012 Benchmarking Cognitive Biases in Large Language Models as Ev · 2402.15987 Likelihood-based Mitigation of Evaluation Bias in Large Lang · 2405.01724 Large Language Models are Inconsistent and Biased Evaluators

### 답 B

<b>서론</b>
LLM‑based <b>평가자</b>(evaluator)는 자동화된 평가 메트릭으로 활용되지만, 인간 판단과의 정렬 부족과 입력 변형에 대한 취약성 등 신뢰성과 견고성이 확보되지 않아 연구가 활발히 진행되고 있습니다. 이러한 한계를 극복하기 위해 설계 선택이 어떻게 영향을 미치는지 분석하는 작업이 필요합니다.

<b>본론</b>
1. <b>LLM‑as‑a‑Judge</b>: LLM을 평가자로 활용하여 자동 평가를 가능하게 하지만, 인간 판단과의 정렬과 일관성 등 신뢰성이 불확실한 문제를 해결하기 위해 설계 선택(평가 기준, 디코딩 전략, Chain-of-Thought 추론)의 영향을 분석합니다. [2506.13639v1]
2. <b>LLM‑based Evaluators Robustness</b>: LLM을 평가자로 사용할 때 입력에 가해진 교란(perturbation)이 견고성에 미치는 영향과 인간 판단과의 정렬 한계를 조사하며, 현재 상태에서는 신뢰할 수 있는 단독 사용에는 추가 개선이 필요함을 제시합니다. [2412.09269v1]

<b>결론</b>
제공된 문서들은 LLM을 평가자로 사용하는 연구에서 설계 선택에 따른 신뢰성 분석([2506.13639v1])과 교란 입력에 대한 견고성 한계 ([2412.09269v1])를 다루는 핵심 논문을 제시합니다. 따라서 이 두 논문은 해당 분야의 기초적 이해와 향후 개선 방향 파악에 필수적입니다.

_B 컨텍스트 5편_: 2412.09269 Towards Understanding the Robustness of LLM-based Evaluation · 2506.13639 An Empirical Study of LLM-as-a-Judge: How Design Choices Imp · 2309.17012 Benchmarking Cognitive Biases in Large Language Models as Ev · 2402.15987 Likelihood-based Mitigation of Evaluation Bias in Large Lang · 2405.01724 Large Language Models are Inconsistent and Biased Evaluators

### 인용 블록

- **2412.09269** [인용 AB] Towards Understanding the Robustness of LLM-based Evaluations under Perturbations — [초록] Traditional evaluation metrics like BLEU and ROUGE fall short when capturing the nuanced qualities of generated text, particularly when there is no single ground truth. In this paper, we explore the potential of Large Language Models (LLMs), specifically Google Gemini 1, to serve as automatic evaluators for non-standardized metrics in summarization and dialog-based tasks. We conduct experiments across multiple prompting strategies to examine how LLMs fare as quality evaluators when compared with human judgments on the SummEval and USR datasets, asking the model to generate both a score as well as a justification for the score. Furthermore, we explore the robustness of the LLM evaluator by using perturbed inputs. Our findings suggest that while LLMs show promise, their alignment with human evaluators is limited, they are not robust against perturbations and significant improvements a

- **2506.13639** [인용 AB] An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability — [초록] As large language models (LLMs) continue to advance, reliable evaluation methods are essential particularly for open-ended, instruction-following tasks. LLM-as-a-Judge enables automatic evaluation using LLMs as evaluators, but its reliability remains uncertain. In this work, we analyze key factors affecting its trustworthiness, focusing on alignment with human judgments and evaluation consistency. Using BIGGENBench and EvalBiasBench, we study the effects of evaluation design, decoding strategies, and Chain-of-Tought (CoT) reasoning in evaluation. Our results show that evaluation criteria are critical for reliability, non-deterministic sampling improves alignment with human preferences over deterministic evaluation, and CoT reasoning offers minimal gains when clear evaluation criteria are present. ## **1 Introduction** In recent years, large language models (LLMs) have been evolving 

- **2309.17012** [인용 A] Benchmarking Cognitive Biases in Large Language Models as Evaluators — [초록] Large Language Models are cognitively biased judges. Large Language Models (LLMs) have recently been shown to be effective as automatic evaluators with simple prompting and in-context learning. In this work, we assemble 15 LLMs of four different size ranges and evaluate their output responses by preference ranking from the other LLMs as evaluators, such as System Star is better than System Square. We then evaluate the quality of ranking outputs introducing the Cognitive Bias Benchmark for LLMs as Evaluators (CoBBLEr), a benchmark to measure six different cognitive biases in LLM evaluation outputs, such as the Egocentric bias where a model prefers to rank its own outputs highly in evaluation. We find that LLMs are biased text quality evaluators, exhibiting strong indications on our bias benchmark (average of 40% of comparisons across all models) within each of their evaluations that 

- **2402.15987** [인용 A] Likelihood-based Mitigation of Evaluation Bias in Large Language Models — [초록] Large Language Models (LLMs) are widely used to evaluate natural language generation tasks as automated metrics. However, the likelihood, a measure of LLM's plausibility for a sentence, can vary due to superficial differences in sentences, such as word order and sentence structure. It is therefore possible that there might be a likelihood bias if LLMs are used for evaluation: they might overrate sentences with higher likelihoods while underrating those with lower likelihoods. In this paper, we investigate the presence and impact of likelihood bias in LLM-based evaluators. We also propose a method to mitigate the likelihood bias. Our method utilizes highly biased instances as few-shot examples for in-context learning. Our experiments in evaluating the data-to-text and grammatical error correction tasks reveal that several LLMs we test display a likelihood bias. Furthermore, our propo

---

## O_14

**질문** LLM 워터마크 연구 중에 입문용으로 읽을 만한 논문 알려줘

### 답 A

<b>서론</b>
LLM 워터마크는 생성된 텍스트나 지식베이스에 소유권 정보를 은밀히 삽입해 저작권 침해와 무단 복제를 방지하는 기술이다. 그러나 기존 방법은 백박스 접근이나 관계형 데이터베이스에만 적용 가능하거나, 다중 LLM 환경에서 효과성이 제한되는 등 실용화 장벽이 존재한다[2501.05249v1][2506.10030v2].

<b>본론</b>
1. <b>RAG‑WM</b>: 멀티‑LLM 상호작용 프레임워크를 이용해 워터마크 엔티리 관계 튜플을 기반으로 텍스트에 워터마크를 삽입하고, 다양한 도메인·개인정보 보호 작업에서 스틸된 RAG를 효과적으로 탐지한다[2501.05249v1].
2. <b>AQUA</b>: 이미지 지식도 포함하는 멀티모달 RAG 시스템에서 의미적 신호를 축약어 기반 트리거와 공간 관계 단서를 이용해 합성 이미지에 삽입하며, 간접 워터마크 전파에도 견고하고 보이지 않는 저작권 추적 기능을 제공한다[2506.10030v2].
3. <b>WIND</b>: 창의적인 글쓰기 데이터베이스에 대해 AI 모방을 방지하기 위해 LLM으로 핵심 요소 다섯 가지를 추출·압축한 뒤, 분리된 크리에이티브 공간에서 암묵적 인코딩으로 검증 가능한 워터마크를 생성한다[2504.00035v3].

<b>결론</b>
제공된 문서들은 RAG‑WM과 AQUA가 각각 텍스트와 멀티모달 환경에 적용되는 LLM/멀티모dal 워터마크 접근법을 제시하고, WIND는 창의 글쓰기 보호를 위한 암묵적 인코딩 방식을 제안한다. 따라서 입문용으로 이 세 논문을 읽으면 다양한 맥락에서 구현된 최신 LLM 워터마킹 기술의 핵심 아이디어와 한계를 파악할 수 있다[2501.05249v1][2506.10030v2][2504.00035v3].

_A 컨텍스트 5편_: 2501.05249 RAG-WM: An Efficient Black-Box Watermarking Approach for Ret · 2506.10030 Safeguarding Multimodal Knowledge Copyright in the RAG-as-a- · 2606.22875 FedOT: Ownership Verification and Leakage Tracing via Waterm · 2504.00035 Is Your Writing Being Mimicked by AI? Unveiling Imitation wi · 2412.19834 RoboSignature: Robust Signature and Watermarking on Network 

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. LLM 워터마크는 모델에 저작권 정보를 숨겨 넣거나 검증하는 기술로, 최근 RAG(검색 증강 생성) 시스템과 같은 복잡한 파이프라인에서 적용하기 어려운 점이 있습니다.

<b>본론</b>
1. <b>RAG-WM</b>: 다중‑LLM 상호작용 프레임워크를 이용해 블랙박스 방식으로 지식 워터마크를 생성하고 목표 RAG에 주입하며, 다양한 도메인·개인정보 보호 작업에서 스틸된 RAG 탐지 및 변형 공격 견고성을 입증했습니다[2501.05249v1].
2. <b>AQUA</b>: 멀티모달 RAG 환경에서 이미지 지식을 위한 워터마크 프레임워크로, 약어 기반 트리거와 공간 관계 단서를 이용해 합성 이미지에 의미 신호를 삽입하고 간접 전파에도 강인함을 보였습니다[2506.10030v2] (관련 연구: WARD).
3. <b>WIND</b>: 크리에이티브 글쓰기 데이터베이스에 적용되는 제로‑워터마킹, 검증 가능한 암시적 스킴으로 AI 모방으로부터 저작권을 보호하며 F1 점수 &gt;98%와 낮은 위양성률을 달성했습니다[2504.00035v3].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 5편_: 2501.05249 RAG-WM: An Efficient Black-Box Watermarking Approach for Ret · 2506.10030 Safeguarding Multimodal Knowledge Copyright in the RAG-as-a- · 2606.22875 FedOT: Ownership Verification and Leakage Tracing via Waterm · 2504.00035 Is Your Writing Being Mimicked by AI? Unveiling Imitation wi · 2412.19834 RoboSignature: Robust Signature and Watermarking on Network 

### 인용 블록

- **2501.05249** [인용 AB] RAG-WM: An Efficient Black-Box Watermarking Approach for Retrieval-Augmented Generation of Large Language Models — [초록] In recent years, tremendous success has been witnessed in Retrieval-Augmented Generation (RAG), widely used to enhance Large Language Models (LLMs) in domain-specific, knowledge-intensive, and privacy-sensitive tasks. However, attackers may steal those valuable RAGs and deploy or commercialize them, making it essential to detect Intellectual Property (IP) infringement. Most existing ownership protection solutions, such as watermarks, are designed for relational databases and texts. They cannot be directly applied to RAGs because relational database watermarks require white-box access to detect IP infringement, which is unrealistic for the knowledge base in RAGs. Meanwhile, post-processing by the adversary's deployed LLMs typically destructs text watermark information. To address those problems, we propose a novel black-box "knowledge watermark" approach, named RAG-WM, to detect IP i

- **2506.10030** [인용 AB] Safeguarding Multimodal Knowledge Copyright in the RAG-as-a-Service Environment — [초록] As Retrieval-Augmented Generation (RAG) evolves into service-oriented platforms (Rag-as-a-Service) with shared knowledge bases, protecting the copyright of contributed data becomes essential. Existing watermarking methods in RAG focus solely on textual knowledge, leaving image knowledge unprotected. In this work, we propose AQUA, the first watermark framework for image knowledge protection in Multimodal RAG systems. AQUA embeds semantic signals into synthetic images using two complementary methods: acronym-based triggers and spatial relationship cues. These techniques ensure watermark signals survive indirect watermark propagation from image retriever to textual generator, being efficient, effective and imperceptible. Experiments across diverse models and datasets show that AQUA enables robust, stealthy, and reliable copyright tracing, filling a key gap in multimodal RAG protection.

- **2504.00035** [인용 AB] Is Your Writing Being Mimicked by AI? Unveiling Imitation with Invisible Watermarks in Creative Writing — [초록] Efficient knowledge injection methods for Large Language Models (LLMs), such as In-Context Learning, knowledge editing, and efficient parameter fine-tuning, significantly enhance model utility on downstream tasks. However, they also pose substantial risks of unauthorized imitation and compromised data provenance for high-value unstructured data assets like creative works. Current copyright protection methods for creative works predominantly focus on visual arts, leaving a critical and unaddressed data engineering challenge in the safeguarding of creative writing. In this paper, we propose WIND (Watermarking via Implicit and Non-disruptive Disentanglement), a novel zero-watermarking, verifiable and implicit scheme that safeguards creative writing databases by providing verifiable copyright protection. Specifically, we decompose creative essence into five key elements, which are extra

---

## O_16

**질문** KV 캐시 압축 논문 두 편 추천해줘

### 답 A

<b>서론</b>
KV 캐시 압축은 대규모 언어 모델(LLM) 추론 시 메모리 대역폭과 저장 공간을 크게 줄여야 하는 핵심 과제이며, 특히 긴 컨텍스트에서 KV‑캐시에 접근하는 트래픽이 전체 메모리 사용량을 지배하기 때문에 효율적인 방법이 필요합니다.

<b>본론</b>
1. <b>LOOKAT</b>: 키 벡터를 서브스페이스로 분해하고 코드북을 학습한 뒤 룩업 테이블을 이용해 주의를 계산함으로써, 기존 양자화 방식보다 64배까지 압축률을 달성하면서도 출력 충실도 95.7%를 유지합니다[2601.10155v1].
2. <b>DeltaKV</b>: 장기적인 토큰 간 유사성과 KV 표현에서 공유되는 잠재 성분을 활용해 잔차 기반의 압축을 수행하고, Sparse‑vLLM 엔진과 결합해 메모리 사용량을 기존 대비 약 30%로 줄이면서 거의 손실 없는 정확도를 유지합니다[2602.08005v1].

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다. LOOKAT은 서브스페이스 분해와 룩업 테이블을 통한 압축, DeltaKV는 잔차 기반 유사성 활용과 Sparse‑vLLM 엔진 결합으로 각각 KV 캐시 메모리 효율성을 크게 향상시키는 방법을 제시합니다.

_A 컨텍스트 5편_: 2607.09683 Ablation, Statistical Inference, and Validation for KV-Cache · 2601.10155 LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient  · 2503.24000 Rethinking Key-Value Cache Compression Techniques for Large  · 2502.16886 ReFreeKV: Towards Threshold-Free KV Cache Compression · 2602.08005 DeltaKV: Residual-Based KV Cache Compression via Long-Range 

### 답 B

<b>서론</b>
KV 캐시 압축은 대규모 언어 모델(LLM) 추론 시 메모리 대역폭과 저장 공간을 크게 감소시켜 지연시간 및 처리량을 개선하는 핵심 기술이다. 그러나 데이터의 분포 특성에 따라 기존 방법이 성능 저하를 보일 수 있어, 다양한 접근법을 비교·검증해야 한다.

<b>본론</b>
1. <b>Turbo‑Quant</b>: WHT 회전과 Beta Lloyd-Max을 결합한 압축 기법으로, 통계적 검증 방법론을 통해 시스템 코덱 차이와 구현 변동성을 분리한다[2607.09683v1].
2. <b>LOOKAT</b>: 키 벡터를 서브스페이스로 분해하고 코드북 학습·검색 테이블 활용하여 제품 양자화와 비대칭 거리 계산을 적용함으로써 메모리‑바운드 문제를 컴퓨팅‑바운드로 전환시킨다[2601.10155v1].

<b>결론</b>
제공된 두 논문은 각각 통계적 검증 기반의 압축 설계와 서브스페이스 분해 및 검색 메커니즘을 활용한 LOOKAT이라는 서로 다른 접근법을 제시한다. 따라서 KV 캐시 압축 연구에서는 이러한 방법론들을 상황에 맞게 선택·조합하는 것이 효율적인 모델 배포에 도움이 된다.

_B 컨텍스트 5편_: 2607.09683 Ablation, Statistical Inference, and Validation for KV-Cache · 2601.10155 LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient  · 2503.24000 Rethinking Key-Value Cache Compression Techniques for Large  · 2502.16886 ReFreeKV: Towards Threshold-Free KV Cache Compression · 2602.08005 DeltaKV: Residual-Based KV Cache Compression via Long-Range 

### 인용 블록

- **2601.10155** [인용 AB] LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers — [초록] Compressing the KV cache is a required step to deploy large language models on edge devices. Current quantization methods compress storage but fail to reduce bandwidth as attention calculation requires dequantizing keys from INT4/INT8 to FP16 before use. We observe that attention scoring is mathematically equivalent to the inner product similarity search and we can apply some compression techniques from vector databases to compress KV-cache better. We propose LOOKAT, which applies product quantization and asymmetric distance computation, to transformer architecture by decomposing key vectors into subspaces, learning codebooks and computing attention tables via lookup tables. This transforms attention from memory-bound to compute-bound. LOOKAT achieves 64 $\times$ compression at 95.7\% output fidelity and 32 $\times$ compression at 95.0\% fidelity when tested on GPT-2. LOOKAT require

- **2602.08005** [인용 A] DeltaKV: Residual-Based KV Cache Compression via Long-Range Similarity — [초록] The deployment of efficient long-context LLMs in applications like autonomous agents, long-chain reasoning, and creative writing is fundamentally bottlenecked by the linear growth of KV cache memory. Existing compression and eviction methods often struggle to balance accuracy, compression ratio, and hardware efficiency. We propose DeltaKV, a residual-based KV cache compression framework motivated by two empirical findings: long-range inter-token similarity and highly shared latent components in KV representations. Instead of discarding tokens, DeltaKV encodes semantic residuals relative to retrieved historical references, preserving fidelity while substantially reducing storage. To translate compression gains into real system speedups, we further introduce Sparse-vLLM, a high-performance inference engine with decoupled memory management and kernels optimized for sparse and irregular

- **2607.09683** [인용 B] Ablation, Statistical Inference, and Validation for KV-Cache Compression — [초록] This study systematically compares Turbo-Quant and SpectralQuant KV-cache compression, evaluating non-dominated schemes, including WHT rotation with Beta Lloyd-Max and QJL, through a statistical validation methodology that separates systematic codec differences from implementation variance. Key findings reveal that while eigenbasis-based methods fail on heavy-tailed data due to covariance instability, they excel in structured regimes, with the effective semantic dimension ($d_{eff}$) adapting to calibration budgets rather than true data rank. (this is an abstract of the abstract thank you ) ## **1 Introduction** Transformer inference at scale is bounded by memory bandwidth: KV-cache access dominates total memory traffic for long-context generation, and reducing cache size directly translates to latency and throughput improvements. Quantization of keys and values is the standard appr

---

## O_30

**질문** 멀티모달 모델 논문 중 재밌는 거 세 편만 뽑아줘

### 답 A

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 멀티모달 모델은 텍스트·이미지·오디오 등 다양한 데이터를 통합해 복잡한 작업을 수행하지만, 아직 완전한 일반 인공지능이나 세계 모델을 구현하는 데 한계가 있습니다. 이러한 배경에서 최근 주목받는 주요 접근법들을 살펴보겠습니다.

<b>본론</b>
1. <b>Multimodal Chain of Thought (M-COT)</b>: 멀티모달 모델의 핵심 기술로 소개되며, 사고 과정을 단계별로 확장해 복잡한 추론을 가능하게 합니다[2407.00118v1].
2. <b>Multi-Dimensional Insights Benchmark</b>: 이미지와 다양한 연령대에 맞춘 질문으로 LMMs를 평가하는 벤치마크이며, 기존 평가를 보완합니다[2412.12606v1].

<b>결론</b>
따라서 질문에 찾는 연구는 제공된 문서에서 찾을 수 없습니다. 대신 멀티모달 모델 분야에서 최근 주목받는 M-COT 사고 과정과 MDI 벤치마킹 등 두 가지 주요 접근법이 제시되어 있습니다.

_A 컨텍스트 5편_: 2407.00118 From Efficient Multimodal Models to World Models: A Survey · 2412.17759 Survey of Large Multimodal Model Datasets, Application Categ · 2412.18619 Next Token Prediction Towards Multimodal Intelligence: A Com · 2504.08748 A Survey of Multimodal Retrieval-Augmented Generation · 2412.12606 Multi-Dimensional Insights: Benchmarking Real-World Personal

### 답 B

<b>서론</b>
멀티모달 모델은 텍스트·이미지·오디오 등 다양한 데이터 유형을 동시에 처리해야 하므로, 기존 단일 모달 방식보다 설계와 평가가 훨씬 복잡합니다. 이러한 복합성을 다루는 연구들은 최근 급격히 늘어나고 있습니다.

<b>본론</b>
1. <b>Multimodal Chain of Thought (M‑COT)</b>: 멀티모달 모델에 사슬 사고를 도입해 복잡한 추론을 가능하게 합니다[2407.00118v1].
2. <b>MDI Benchmark</b>: 이미지와 다양한 연령대별 질문으로 LMM의 이해·추리 능력을 종합적으로 평가합니다[2412.12606v1].

<b>결론</b>
제공된 문서들은 멀티모달 모델 연구의 서로 다른 측면을 다루며, 결과에 있어서는 공통된 목표와 차이점을 보여줍니다. 첫 번째 논문은 멀티모달 모델을 세계 모델로 발전시키는 잠재력과 3D 생성 및 외부 규칙 시스템 통합을 제안합니다[2407.00118v1]. 두 번째 논문은 기존 벤치마크가 실세계 다양성을 충분히 평가하지 못한다는 한계를 지적하고, MDI-Benchmark를 통해 연령별 질문 분류와 복잡한 추론 능력을 측정함으로써 GPT-4o가 79% 정확도를 달성했으나 여전히 개선 여지가 있음을 밝힙니다[2412.12606v1]. 따라서 두 연구는 모두 멀티모달 모델의 실용적 한계와 발전 방향을 제시하지만, 하나는 이론적·구조적 통합에 초점을 맞추고 다른 하나는 실제 성능 평가와 벤치마크 설계에 중점을 둡니다.

_B 컨텍스트 5편_: 2407.00118 From Efficient Multimodal Models to World Models: A Survey · 2412.17759 Survey of Large Multimodal Model Datasets, Application Categ · 2412.18619 Next Token Prediction Towards Multimodal Intelligence: A Com · 2504.08748 A Survey of Multimodal Retrieval-Augmented Generation · 2412.12606 Multi-Dimensional Insights: Benchmarking Real-World Personal

### 인용 블록

- **2407.00118** [인용 AB] From Efficient Multimodal Models to World Models: A Survey — [초록] Multimodal Large Models (MLMs) are becoming a significant research focus, combining powerful large language models with multimodal learning to perform complex tasks across different data modalities. This review explores the latest developments and challenges in MLMs, emphasizing their potential in achieving artificial general intelligence and as a pathway to world models. We provide an overview of key techniques such as Multimodal Chain of Thought (M-COT), Multimodal Instruction Tuning (M-IT), and Multimodal In-Context Learning (M-ICL). Additionally, we discuss both the fundamental and specific technologies of multimodal models, highlighting their applications, input/output modalities, and design characteristics. Despite significant advancements, the development of a unified multimodal model remains elusive. We discuss the integration of 3D generation and embodied intelligence to en

- **2412.12606** [인용 AB] Multi-Dimensional Insights: Benchmarking Real-World Personalization in Large Multimodal Models — [초록] The rapidly developing field of large multimodal models (LMMs) has led to the emergence of diverse models with remarkable capabilities. However, existing benchmarks fail to comprehensively, objectively and accurately evaluate whether LMMs align with the diverse needs of humans in real-world scenarios. To bridge this gap, we propose the Multi-Dimensional Insights (MDI) benchmark, which includes over 500 images covering six common scenarios of human life. Notably, the MDI-Benchmark offers two significant advantages over existing evaluations: (1) Each image is accompanied by two types of questions: simple questions to assess the model's understanding of the image, and complex questions to evaluate the model's ability to analyze and reason beyond basic content. (2) Recognizing that people of different age groups have varying needs and perspectives when faced with the same scenario, our 

---

## O_38

**질문** 합성 데이터로 학습하는 연구 중 읽어야 할 논문 두 편

### 답 A

<b>서론</b>
합성 데이터를 이용해 모델을 학습시키는 연구는 데이터 부족과 프라이버시 문제를 해결할 수 있지만, 생성된 합성 데이터가 실제 데이터와 얼마나 유사한지 평가하는 것이 어렵습니다. 특히 <b>모델 붕괴</b> 현상이나 분포 차이로 인해 성능이 저하될 위험을 고려해야 합니다.

<b>본론</b>
1. <b>Assessing Generative Models for Structured Data</b>: 이 논문은 합성 표형 데이터를 직접적으로 평가하기 위해 데이터 내 열 간 의존성을 분석하는 엄격한 방법을 제시하고, GPT‑2와 CTGAN 모델에서 이러한 의존성이 원본과 일치하지 않음을 보여줍니다[2503.20903v1].
2. <b>Autodata: An agentic data scientist to create high quality synthetic data</b>: Autodata는 AI 에이전트를 데이터 과학자로 활용하여 고품질 학습·평가 데이터를 생성하는 일반화된 방법을 소개하고, 메타‑최적화를 통해 성능을 크게 향상시킵니다[2606.25996v3].
3. <b>How to Synthesize Text Data without Model Collapse?</b>: 이 연구에서는 합성 데이터 비율이 증가함에 따라 모델 성능에 부정적인 상관관계가 있음을 확인했으며, 토큰 편집으로 반합성 데이터를 만들어 모델 붕괴를 방지하고 이론적 상한을 제시합니다[2412.14689v3].

<b>결론</b>
제공된 문서들에 따르면, 합성 데이터 생성 연구들은 모두 기존 방법의 한계를 지적하거나 개선 효과를 보고하고 있다. 첫 번째 연구는 GPT‑2와 CTGAN이 원본 데이터의 의존성을 재현하지 못한다는 결과를 제시한다[2503.20903v1]. 두 번째 연구는 컴퓨터 과학·법률·수학 추론 과제에서 고전적 합성 데이터 생성법보다 향상된 성능을 얻었으며, 추론 효율성도 개선되었다고 보고한다[2606.25996v3]. 세 번째 연구는 토큰 편집을 통한 반합성 데이터가 모델 붕괴를 방지하고 성능을 향상시킨다고 이론적으로 증명하고 실험으로 검증하였다[2412.14689v3]. 따라서 합성 데이터 생성은 도메인과 조건에 따라 결과가 달라지며, 일부에서는 기존 방법보다 우수한 결과를 보이지만 다른 경우에는 의존성 재현 실패와 같은 한계가 존재한다.

_A 컨텍스트 5편_: 2503.20903 Assessing Generative Models for Structured Data · 2606.25996 Autodata: An agentic data scientist to create high quality s · 2412.14689 How to Synthesize Text Data without Model Collapse? · 2403.19866 Is Synthetic Image Useful for Transfer Learning? An Investig · 2407.12813 Data Generation Using Large Language Models for Text Classif

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 합성 데이터를 이용해 모델을 학습시키는 작업은 데이터 부족과 프라이버시 문제를 해결할 수 있지만, 생성된 데이터의 품질 평가와 모델 붕괴 방지 등 여러 어려움이 존재합니다. 이러한 어려움을 극복하기 위해 다양한 접근법이 제안되고 있습니다.

<b>본론</b>
1. <b>Assessing Generative Models for Structured Data</b>: 합성 표 데이터를 직접적으로 평가하는 엄격한 방법을 제시하고, GPT‑2 및 CTGAN이 원본 데이터의 종속성을 재현하지 못한다는 결과를 보여줍니다. [2503.20903v1]
2. <b>Autodata: An agentic data scientist to create high quality synthetic data</b>: AI 에이전트를 활용해 고품질의 훈련·평가 데이터를 생성하는 메타 최적화 방법을 소개하고, 컴퓨터 과학 연구 및 법적 추론 작업에서 기존 합성 데이터 방법보다 향상된 성능을 달성합니다. [2606.25996v3]
3. <b>How to Synthesize Text Data without Model Collapse?</b>: 토큰 편집 기법을 통해 모델 붕괴를 방지한다는 이론적 증명과 실험 결과를 제시하며, 다양한 사전학습 및 미세조정 설정에서 합성 데이터 비율이 낮을수록 성능에 부정적인 상관관계가 있음을 확인합니다. [2412.14689v3]
4. <b>Data Generation Using Large Language Models for Text Classification: An Empirical Case Study</b>: LLM으로 생성된 합성 데이터를 텍스트 분류 모델의 훈련 자료로 활용하고, 프롬프트 선택과 데이터 다양성이 성능에 미치는 영향을 실증 분석하여 개선 방안을 제시합니다. [2407.12813v2]

<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 5편_: 2503.20903 Assessing Generative Models for Structured Data · 2606.25996 Autodata: An agentic data scientist to create high quality s · 2412.14689 How to Synthesize Text Data without Model Collapse? · 2403.19866 Is Synthetic Image Useful for Transfer Learning? An Investig · 2407.12813 Data Generation Using Large Language Models for Text Classif

### 인용 블록

- **2503.20903** [인용 AB] Assessing Generative Models for Structured Data — [초록] Synthetic tabular data generation has emerged as a promising method to address limited data availability and privacy concerns. With the sharp increase in the performance of large language models in recent years, researchers have been interested in applying these models to the generation of tabular data. However, little is known about the quality of the generated tabular data from large language models. The predominant method for assessing the quality of synthetic tabular data is the train-synthetic-test-real approach, where the artificial examples are compared to the original by how well machine learning models, trained separately on the real and synthetic sets, perform in some downstream tasks. This method does not directly measure how closely the distribution of generated data approximates that of the original. This paper introduces rigorous methods for directly assessing syntheti

- **2606.25996** [인용 AB] Autodata: An agentic data scientist to create high quality synthetic data — [초록] We introduce Autodata, a general method that enables AI agents to act as data scientists who build high quality training and evaluation data. We show how to train (meta-optimize) such a data scientist agent, so that it learns to create even stronger data. We describe the overall formulation, and a specific practical implementation, Agentic Self-Instruct. We conduct experiments on computer science research tasks, legal reasoning tasks and reasoning with mathematical objects, where we obtain improved results compared to classical synthetic dataset creation methods. Further, meta-optimizing the data scientist agent itself delivers an even larger performance uplift. Agentic data creation provides a way to convert increased inference compute into higher quality model training. Overall, we believe this direction has the potential to change the way we build AI data. 19 This highlights an u

- **2412.14689** [인용 AB] How to Synthesize Text Data without Model Collapse? — [초록] Model collapse in synthetic data indicates that iterative training on self-generated data leads to a gradual decline in performance. With the proliferation of AI models, synthetic data will fundamentally reshape the web data ecosystem. Future GPT-$\{n\}$ models will inevitably be trained on a blend of synthetic and human-produced data. In this paper, we focus on two questions: what is the impact of synthetic data on language model training, and how to synthesize data without model collapse? We first pre-train language models across different proportions of synthetic data, revealing a negative correlation between the proportion of synthetic data and model performance. We further conduct statistical analysis on synthetic data to uncover distributional shift phenomenon and over-concentration of n-gram features. Inspired by the above findings, we propose token editing on human-produced 

- **2407.12813** [인용 B] Data Generation Using Large Language Models for Text Classification: An Empirical Case Study — [초록] Using Large Language Models (LLMs) to generate synthetic data for model training has become increasingly popular in recent years. While LLMs are capable of producing realistic training data, the effectiveness of data generation is influenced by various factors, including the choice of prompt, task complexity, and the quality, quantity, and diversity of the generated data. In this work, we focus exclusively on using synthetic data for text classification tasks. Specifically, we use natural language understanding (NLU) models trained on synthetic data to assess the quality of synthetic data from different generation approaches. This work provides an empirical analysis of the impact of these factors and offers recommendations for better data generation practices. To evaluate the success of synthetic data generation, we train a NLU model on the synthetic data and assess its performance 

---

## H_C07

**질문** 작은 언어 모델로 추론 능력을 끌어올린 연구 추천해줘

### 답 A

<b>서론</b>
작은 언어 모델(LLM) 은 파라미터 수가 제한되어 복잡한 추론 작업을 수행하기 어렵습니다. 이러한 한계를 극복하려면 외부 지식과 도구 사용을 결합한 <b>추증 기반 생성(RAG)</b> 및 <b>시스템 1·2</b> 방식의 접근이 필요합니다.

<b>본론</b>
1. <b>Reasoning Agentic RAG</b>: 고정된 모듈 파이프라인을 통해 추증을 강화하거나, 모델 스스로 도구를 조율하는 에이전트 방식을 도입해 복잡한 상황에서도 유연한 추론과 도구 사용을 가능하게 합니다 [2506.10408v1].
2. <b>SBI‑RAG (Schema-Based Instruction Retrieval-Augmented Generation)</b>: 스키마 기반 지시를 이용해 수학 단어 문제의 구조를 분류하고, LLM을 활용해 단계별 해결 과정을 안내함으로써 학생들의 추론 명확성을 높입니다 [2410.13293v2].

<b>결론</b>
제공된 문서에 따르면, 작은 언어 모델의 추론 능력을 향상시키기 위해 <b>Reasoning Agentic RAG</b>와 <b>SBI‑RAG</b>가 각각 고정 파이프라인·에이전트 방식과 스키마 기반 지시 방식을 통해 외부 지식 및 도구 활용을 결합한 접근법을 제시하고 있습니다.

_A 컨텍스트 3편_: 2506.10408 Reasoning RAG via System 1 or System 2: A Survey on Reasonin · 2410.13293 SBI-RAG: Enhancing Math Word Problem Solving for Students th · 2604.03174 Beyond the Parameters: A Technical Survey of Contextual Enri

### 답 B

<b>서론</b>
작은 언어 모델(LLM) 은 파라미터 수가 제한되어 복잡한 추론 작업을 수행하기 어렵습니다. 이러한 한계를 극복하려면 외부 지식을 활용하거나 구조화된 맥락을 제공하는 <b>추리 강화</b> 기법이 필요합니다.

<b>본론</b>
1. <b>Reasoning Agentic RAG</b>: 고정된 모듈 파이프라인을 따르는 사전 정의된 추리와, 모델이 인ферен스 중에 도구 상호작용을 자율적으로 조정하는 에이전트형 추리로 두 가지 패러다임을 제시합니다[2506.10408v1].
2. <b>SBI-RAG (Schema-Based Instruction Retrieval-Augmented Generation)</b>: 스키마 기반 지시를 활용해 수학 단어 문제의 핵심 정보를 식별하고 단계별로 해결하도록 유도하며, GPT‑4·GPT‑3.5 Turbo와 비교해 추론 명확성을 향상시킵니다[2410.13293v2].
3. <b>CausalRAG</b>: 인과 관계를 모델링한 검색 기반 증강 방식을 통해 LLM의 정적 지식 한계를 보완하고 구조화된 맥락을 제공함으로써 신뢰성 있는 NLP 작업을 지원합니다[2604.03174v1].

<b>결론</b>
제공된 문서들은 모두 추론 능력 향상을 목표로 하지만, 적용 대상과 방법의 차이가 명확히 구분된다. [2506.10408v1]은 초기 정적 파이프라인 기반 RAG가 복잡한 추론이 필요한 실제 시나리오에서 한계를 보인다고 보고한다. 반면 [2410.13293v2]는 스키마 기반 지시와 RAG를 결합한 SBI-RAG 프레임워크가 수학 단어 문제 해결 정확도를 향상시킨다고 제시한다. 따라서 작은 언어 모델의 추론 능력을 끌어올리는 연구는 도메인(일반적 복잡 추론 vs 교육용 수학 문제)과 접근 방식에 따라 효과가 달라진다.

_B 컨텍스트 3편_: 2506.10408 Reasoning RAG via System 1 or System 2: A Survey on Reasonin · 2410.13293 SBI-RAG: Enhancing Math Word Problem Solving for Students th · 2604.03174 Beyond the Parameters: A Technical Survey of Contextual Enri

### 인용 블록

- **2506.10408** [인용 AB] Reasoning RAG via System 1 or System 2: A Survey on Reasoning Agentic Retrieval-Augmented Generation for Industry Challenges — [초록] Retrieval-Augmented Generation (RAG) has emerged as a powerful framework to overcome the knowledge limitations of Large Language Models (LLMs) by integrating external retrieval with language generation. While early RAG systems based on static pipelines have shown effectiveness in well-structured tasks, they struggle in real-world scenarios requiring complex reasoning, dynamic retrieval, and multi-modal integration. To address these challenges, the field has shifted toward Reasoning Agentic RAG, a paradigm that embeds decision-making and adaptive tool use directly into the retrieval process. In this paper, we present a comprehensive review of Reasoning Agentic RAG methods, categorizing them into two primary systems: predefined reasoning, which follows fixed modular pipelines to boost reasoning, and agentic reasoning, where the model autonomously orchestrates tool interaction during i

- **2410.13293** [인용 AB] SBI-RAG: Enhancing Math Word Problem Solving for Students through Schema-Based Instruction and Retrieval-Augmented Generation — [초록] Many students struggle with math word problems (MWPs), often finding it difficult to identify key information and select the appropriate mathematical operations. Schema-based instruction (SBI) is an evidence-based strategy that helps students categorize problems based on their structure, improving problem-solving accuracy. Building on this, we propose a Schema-Based Instruction Retrieval-Augmented Generation (SBI-RAG) framework that incorporates a large language model (LLM). Our approach emphasizes step-by-step reasoning by leveraging schemas to guide solution generation. We evaluate its performance on the GSM8K dataset, comparing it with GPT-4 and GPT-3.5 Turbo, and introduce a "reasoning score" metric to assess solution quality. Our findings suggest that SBI-RAG enhances reasoning clarity and facilitates a more structured problem-solving process potentially providing educational b

- **2604.03174** [인용 B] Beyond the Parameters: A Technical Survey of Contextual Enrichment in Large Language Models: From In-Context Prompting to Causal Retrieval-Augmented Generation — [초록] Large language models (LLMs) encode vast world knowledge in their parameters, yet they remain fundamentally limited by static knowledge, finite context windows, and weakly structured causal reasoning. This survey provides a unified account of augmentation strategies along a single axis: the degree of structured context supplied at inference time. We cover in-context learning and prompt engineering, Retrieval-Augmented Generation (RAG), GraphRAG, and CausalRAG. Beyond conceptual comparison, we provide a transparent literature-screening protocol, a claim-audit framework, and a structured cross-paper evidence synthesis that distinguishes higher-confidence findings from emerging results. The paper concludes with a deployment-oriented decision framework and concrete research priorities for trustworthy retrieval-augmented NLP. 6 prompting elicits reasoning in large language models. In _Ad

---

## H_C16

**질문** 요즘 재밌는 RAG 논문 추천해줘

### 답 A

<b>서론</b>
최근 <b>Retrieval Augmented Generation (RAG)</b>은 외부 지식과 생성 모델을 결합해 정확성을 높이는 기술로 주목받고 있지만, 다양한 최적화 기법 적용 방법과 평가 지표가 아직 명확히 정리되지 않아 연구와 실용화에 어려움이 있다.

<b>본론</b>
1. <b>Multi-Query</b>: 검색 단계에 Multi‑Query를 도입함으로써 성능이 크게 향상되었다[2411.08438v1]. RAG 프레임워크 내 다양한 구성의 효과를 평가하기 위해 새로운 평가를 제안하였다[2411.08438v1].
2. <b>Auepora (Unified Evaluation Process)</b>: 검색·생성 성분의 관련도, 정확도, 충실도를 포함한 정량적 지표를 비교하고 현재 벤치마크 한계를 분석했다[2405.07437v2].

<b>결론</b>
제공된 문서들은 RAG 시스템의 성능 향상을 위한 구체적인 최적화 기법과 평가 프로세스에 초점을 맞추고 있습니다. [2411.08438v1]은 학술 데이터 도메인에서 멀티-쿼리 방식을 적용했을 때 검색 단계에서 유의미한 성능 향상이 발생한다는 결과를 보고합니다. 반면, [2405.07437v2]는 RAG 시스템 전반에 대한 통합 평가 프로세스와 벤치마크의 한계를 논의하며, 현재 연구가 다양한 데이터셋과 메트릭을 분석하고 향후 방향성을 제시하는 데 주력하고 있음을 강조합니다. 따라서 두 논문은 각각 특정 도메인에서의 성능 개선 효과와 전체적인 평가 체계 구축이라는 서로 다른 목표를 가지고 있어 결과의 초점이 다릅니다.

_A 컨텍스트 5편_: 2411.08438 Towards Optimizing a Retrieval Augmented Generation using La · 2410.12837 A Comprehensive Survey of Retrieval-Augmented Generation (RA · 2508.06401 A Systematic Literature Review of Retrieval-Augmented Genera · 2312.07796 Harnessing Retrieval-Augmented Generation (RAG) for Uncoveri · 2405.07437 Evaluation of Retrieval-Augmented Generation: A Survey

### 답 B

<b>서론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다.

<b>본론</b>
1. <b>Multi‑Query</b>: Retrieval 단계에 Multi‑Query를 도입하여 성능 향상을 달성했습니다[2411.08438v1]. RAG 프레임워크 내 다양한 구성의 효과를 평가하기 위해 새로운 평가 방법인 RAG Confusion Matix을 제안합니다[2411.08438v1].
<b>결론</b>
따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 5편_: 2411.08438 Towards Optimizing a Retrieval Augmented Generation using La · 2410.12837 A Comprehensive Survey of Retrieval-Augmented Generation (RA · 2508.06401 A Systematic Literature Review of Retrieval-Augmented Genera · 2312.07796 Harnessing Retrieval-Augmented Generation (RAG) for Uncoveri · 2405.07437 Evaluation of Retrieval-Augmented Generation: A Survey

### 인용 블록

- **2411.08438** [인용 AB] Towards Optimizing a Retrieval Augmented Generation using Large Language Model on Academic Data — [초록] Given the growing trend of many organizations integrating Retrieval Augmented Generation (RAG) into their operations, we assess RAG on domain-specific data and test state-of-the-art models across various optimization techniques. We incorporate four optimizations; Multi-Query, Child-Parent-Retriever, Ensemble Retriever, and In-Context-Learning, to enhance the functionality and performance in the academic domain. We focus on data retrieval, specifically targeting various study programs at a large technical university. We additionally introduce a novel evaluation approach, the RAG Confusion Matrix designed to assess the effectiveness of various configurations within the RAG framework. By exploring the integration of both open-source (e.g., Llama2, Mistral) and closed-source (GPT-3.5 and GPT-4) Large Language Models, we offer valuable insights into the application and optimization of RA

- **2405.07437** [인용 A] Evaluation of Retrieval-Augmented Generation: A Survey — [초록] Retrieval-Augmented Generation (RAG) has recently gained traction in natural language processing. Numerous studies and real-world applications are leveraging its ability to enhance generative models through external information retrieval. Evaluating these RAG systems, however, poses unique challenges due to their hybrid structure and reliance on dynamic knowledge sources. To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehensive overview of the evaluation and benchmarks of RAG systems. Specifically, we examine and compare several quantifiable metrics of the Retrieval and Generation components, such as relevance, accuracy, and faithfulness, within the current RAG benchmarks, encompassing the possible output and ground truth pairs. We then analyze the various datasets and metrics, discuss the limitations of curre

---

## H_I04b

**질문** 다른 논문도 추천해줘

### 답 A

<b>서론</b>
RAG 시스템에서 답변에 제시된 <b>증거 기반 근거성</b>은 신뢰성을 판단하는 핵심 요소이지만, 외부 검색 결과와 모델 내부 지식 사이의 충돌이나 오류를 자동으로 식별하기 어려운 문제가 존재합니다. 이러한 문제를 해결하려면 정교한 평가 메트릭과 진단 프레임워크가 필요합니다.

<b>본론</b>
1. <b>RAGChecker</b>: Retrieval 및 Generation 모듈을 각각 세부적으로 측정하는 일련의 진단 지표를 도입하여, 기존 지표보다 인간 판단과의 상관관계에서 유의미하게 높은 성능을 보입니다[2408.08067v2].
2. <b>ChainPoll</b>: LLM 홀루시네이션 감지를 위해 Adherence와 Correctness라는 두 가지 새로운 메트릭과 RealHall 벤치마크를 제시하며, 모든 테스트 항목에서 기존 방법보다 우수한 AUROC(0.781) 를 달성합니다[2310.18344v1].
3. <b>Probabilistic distances-based hallucination detection</b>: 프롬프트 토큰 임베딩과 모델 응답 토크임베딩 사이의 거리 분포를 추정하여 사실성을 신호로 추출하는 방법을 제안하고, NLI 작업에서 학습된 지식을 홀루시네이션 감지에 전이시켜 완전히 비지도 방식으로 높은 성능을 달성합니다[2506.09886v2].
4. <b>Evidence Graph Consistency (EGC)</b>: 각 응답에 대해 로컬 증거 그래프를 구축하고 다섯 가지 구조적 일관성 측정치를 계산하여 모델‑종속적인 홀루시네이션 감지 신호로 활용하며, Llama-2와 GPT 계열에서 서로 다른 진단 방향을 관찰합니다[2606.06748v2].

<b>결론</b>
제공된 문서들은 RAG 시스템의 근거성을 평가하거나 홀루시네이션을 자동으로 탐지하는 다양한 접근법을 제시하고 있습니다. 각 방법은 모듈별 진단 지표(예: RAGChecker), 새로운 메트릭과 벤치마크 (ChainPoll, Probabilistic distances-based detection) 및 구조적 일관성 분석(Evidence Graph Consistency) 등을 통해 기존 방법의 한계를 극복하거나 보완합니다. 따라서 질문에서 요구한 “다른 논문”으로는 위 네 가지 연구가 적합하며, 각각 고유한 평가·탐지 메커니즘을 제공합니다.

_A 컨텍스트 5편_: 2408.08067 RAGChecker: A Fine-grained Framework for Diagnosing Retrieva · 2310.18344 Chainpoll: A high efficacy method for LLM hallucination dete · 2506.09886 Probabilistic distances-based hallucination detection in LLM · 2606.06748 Evidence Graph Consistency in Retrieval-Augmented Generation · 2502.17125 LettuceDetect: A Hallucination Detection Framework for RAG A

### 답 B

<b>서론</b>
RAG 시스템에서 답변에 제시된 <b>증거 기반성</b>은 신뢰성을 판단하는 핵심 요소이지만, 검색 결과와 모델 생성 과정 사이에 오류가 발생할 수 있어 자동 평가가 어렵습니다. 특히 의료 등 전문 분야에서 정밀한 근거 검증이 요구됩니다.

<b>본론</b>
1. <b>Evaluating RAG Reliability under Clean, Misleading, and Mixed Retrieval</b>: 이 연구는 청정·오인성 혼합 검색 환경에서 파라메트릭 지식과 증거 간 충돌을 테스트하는 평가 프로토콜을 제안하고, 신뢰성을 측정하기 위해 분석적 프레임워크를 구축합니다. [2606.07783v1]
2. <b>RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation</b>: RAG의 검색·생성 모듈에 대한 세부 진단 메트릭트를 포함하는 평가 프레임을 제시하며, 인간 판단과의 상관관계가 다른 지표보다 높음을 검증합니다. [2408.08067v2]
3. <b>RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems</b>: 오픈소스 프레임워크로 세 가지 검색 접근법과 다양한 프롬프트 전략을 비교하고, 새로운 메트릭으로 성능 개선을 정량화합니다. [2412.12322v1]
4. <b>CARE-RAG - Clinical Assessment and Reasoning in RAG</b>: 의료 분야에서 retrieval와 reasoning 사이의 격차를 평가하는 프레임워크를 제안하며, 정확성·일관성·신뢰성을 측정하고 오류 원인을 구분합니다. [2511.15994v1]

<b>결론</b>
제공된 문서에는 질문이 찾는 연구가 없습니다. 따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.

_B 컨텍스트 5편_: 2606.07783 Evaluating RAG Reliability under Clean, Misleading, and Mixe · 2408.08067 RAGChecker: A Fine-grained Framework for Diagnosing Retrieva · 2412.12322 RAG Playground: A Framework for Systematic Evaluation of Ret · 2511.15994 CARE-RAG - Clinical Assessment and Reasoning in RAG · 2603.03541 RAG-X: Systematic Diagnosis of Retrieval-Augmented Generatio

### 인용 블록

- **2408.08067** [인용 AB] RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation — [초록] Despite Retrieval-Augmented Generation (RAG) showing promising capability in leveraging external knowledge, a comprehensive evaluation of RAG systems is still challenging due to the modular nature of RAG, evaluation of long-form responses and reliability of measurements. In this paper, we propose a fine-grained evaluation framework, RAGChecker, that incorporates a suite of diagnostic metrics for both the retrieval and generation modules. Meta evaluation verifies that RAGChecker has significantly better correlations with human judgments than other evaluation metrics. Using RAGChecker, we evaluate 8 RAG systems and conduct an in-depth analysis of their performance, revealing insightful patterns and trade-offs in the design choices of RAG architectures. The metrics of RAGChecker can guide researchers and practitioners in developing more effective RAG systems. This work has been open so

- **2310.18344** [인용 A] Chainpoll: A high efficacy method for LLM hallucination detection — [초록] Large language models (LLMs) have experienced notable advancements in generating coherent and contextually relevant responses. However, hallucinations - incorrect or unfounded claims - are still prevalent, prompting the creation of automated metrics to detect these in LLM outputs. Our contributions include: introducing ChainPoll, an innovative hallucination detection method that excels compared to its counterparts, and unveiling RealHall, a refined collection of benchmark datasets to assess hallucination detection metrics from recent studies. While creating RealHall, we assessed tasks and datasets from previous hallucination detection studies and observed that many are not suitable for the potent LLMs currently in use. Overcoming this, we opted for four datasets challenging for modern LLMs and pertinent to real-world scenarios. Using RealHall, we conducted a comprehensive comparison

- **2506.09886** [인용 A] Probabilistic distances-based hallucination detection in LLMs with RAG — [초록] Detecting hallucinations in large language models (LLMs) is critical for their safety in many applications. Without proper detection, these systems often provide harmful, unreliable answers. In recent years, LLMs have been actively used in retrieval-augmented generation (RAG) settings. However, hallucinations remain even in this setting, and while numerous hallucination detection methods have been proposed, most approaches are not specifically designed for RAG systems. To overcome this limitation, we introduce a hallucination detection method based on estimating the distances between the distributions of prompt token embeddings and language model response token embeddings. The method examines the geometric structure of token hidden states to reliably extract a signal of factuality in text, while remaining friendly to long sequences. Extensive experiments demonstrate that our method 

- **2606.06748** [인용 A] Evidence Graph Consistency in Retrieval-Augmented Generation: A Model-Dependent Analysis of Hallucination Detection — [초록] Retrieval-Augmented Generation (RAG) reduces but does not eliminate hallucination in large language models. Existing detection methods rely on flat similarity between generated answers and retrieved passages, ignoring structural relationships among evidence pieces and answer claims. We propose Evidence Graph Consistency (EGC), a framework that constructs a local evidence graph per response and computes five structural consistency measures as hallucination indicators. Evaluated on the full question answering split of RAGTruth across six LLMs (5,767 responses), EGC reveals a consistent model-family split: graph consistency features show the expected diagnostic direction for hallucinations in Llama-2 models but exhibit systematic reversal in GPT-4, GPT-3.5, and Mistral-7B. This reversal suggests qualitatively different hallucination patterns across model families and indicates that emb

- **2606.07783** [인용 B] Evaluating RAG Reliability under Clean, Misleading, and Mixed Retrieval — [초록] Retrieval-Augmented Generation (RAG) is widely used to improve the factual reliability of large language models (LLMs) by grounding answers in retrieved evidence. In misinformation-rich environments, however, retrieved content may include plausible but incorrect information, raising concerns about the reliability of RAG-based information access systems. In this work, we propose an evaluation protocol to systematically test how the RAG system handles conflicts between parametric knowledge and evidence retrieved from context with varying amounts of misleading information. We target correct answers to factoid questions that the model responds to correctly, even when there is no retrieval, and use this to test the system with clean, poisoned, and mixed evidence. The proposed analytical framework combines parametric override and confidence metrics to assess when and how misleading inform

- **2412.12322** [인용 B] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems — [초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical results comparing different language models (Llama 3.1 and Qwen 2.5) across various retrieval configurations. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. The results also highlight the importance of prompt engineering in RAG systems, with our custom-prompted agents showing consistent improvements in retrieval ac

- **2511.15994** [인용 B] CARE-RAG - Clinical Assessment and Reasoning in RAG — [초록] Access to the right evidence does not guarantee that large language models (LLMs) will reason with it correctly. This gap between retrieval and reasoning is especially concerning in clinical settings, where outputs must align with structured protocols. We study this gap using Written Exposure Therapy (WET) guidelines as a testbed. In evaluating model responses to curated clinician-vetted questions, we find that errors persist even when authoritative passages are provided. To address this, we propose an evaluation framework that measures accuracy, consistency, and fidelity of reasoning. Our results highlight both the potential and the risks: retrieval-augmented generation (RAG) can constrain outputs, but safe deployment requires assessing reasoning as rigorously as retrieval. ## **2.2 Assessing RAG system performance across reasoning levels** Research on retrieval-augmented generatio
