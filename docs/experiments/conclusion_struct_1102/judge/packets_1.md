# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)

## H_A04 — 문서를 계층적으로 요약해서 트리로 만든 뒤 그 트리에서 검색하는 연구 알려줘

### 인용 블록

[문서 1]
[Distance: 0.4340]
[발행일: 2025-12-03]
[2512.03413v1] BookRAG: A Hierarchical Structure-aware Index-based Approach for Retrieval-Augmented Generation on Complex Documents
[초록] As an effective method to boost the performance of Large Language Models (LLMs) on the question answering (QA) task, Retrieval-Augmented Generation (RAG), which queries highly relevant information from external complex documents, has attracted tremendous attention from both industry and academia. Existing RAG approaches often focus on general documents, and they overlook the fact that many real-world documents (such as books, booklets, handbooks, etc.) have a hierarchical structure, which organizes their content from different granularity levels, leading to poor performance for the QA task. To address these limitations, we introduce BookRAG, a novel RAG approach targeted for documents with a hierarchical structure, which exploits logical hierarchies and traces entity relations to query the highly relevant information. Specifically, we build a novel index structure, called BookIndex, by extracting a hierarchical tree from the document, which serves as the role of its table of contents, using a graph to capture the intricate relationships between entities, and mapping entities to tree nodes. Leveraging the BookIndex, we then propose an agent-based query method inspired by the Information Foraging Theory, which dynamically classifies queries and employs a tailored retrieval workflow. Extensive experiments on three widely adopted benchmarks demonstrate that BookRAG achieves state-of-the-art performance, significantly outperforming baselines in both retrieval recall and QA accuracy while maintaining competitive efficiency.

. However, these general workflows often treat the index as a structure derived purely from content, potentially detaching it from the document’s original logical hierarchy. In contrast, our approach seeks to deeply integrate these retrieval structures with the document’s native tree topology.
[문서 3]
[Distance: 0.3762]
[발행일: 2025-09-15]
[2509.11552v3] HiChunk: Evaluating and Enhancing Retrieval-Augmented Generation with Hierarchical Chunking
[초록] Retrieval-Augmented Generation (RAG) enhances the response capabilities of language models by integrating external knowledge sources. However, document chunking as an important part of RAG system often lacks effective evaluation tools. This paper first analyzes why existing RAG evaluation benchmarks are inadequate for assessing document chunking quality, specifically due to evidence sparsity. Based on this conclusion, we propose HiCBench, which includes manually annotated multi-level document chunking points, synthesized evidence-dense quetion answer(QA) pairs, and their corresponding evidence sources. Additionally, we introduce the HiChunk framework, a multi-level document structuring framework based on fine-tuned LLMs, combined with the Auto-Merge retrieval algorithm to improve retrieval quality. Experiments demonstrate that HiCBench effectively evaluates the impact of different chunking methods across the entire RAG pipeline. Moreover, HiChunk achieves better chunking quality within reasonable time consumption, thereby enhancing the overall performance of RAG systems.

1. **Document Hierarchical Annotation and Summarization** : To enable LLMs to gain an overall understanding of the specific document _D_ while constructing QA pairs, we first generated summaries for corresponding sections based on the annotated hierarchical structure, denoted as _S ← LLMs_ ( _D_ ). These summaries will be used in QA pair generation.

### 문장

- s1: 또한, 미세 조정된 대형 언어 모델(LLM)을 기반으로 한 다단계 문서 구조화 프레임워크인 HiChunk와 자동 병합 검색 알고리즘을 결합하여 검색 품질을 향상시키기 위해 이를 소개합니다. [2509.11552v3]
- s2: HiChunk는 문서의 계층적 구조를 기반으로 섹션별 요약을 생성하고 이를 이용해 전체 문서를 이해하도록 LLM을 설계하는 방법을 제시한다[2509.11552v3].
- s3: BookRAG은 계층적 구조를 가진 문서에 대해 실험을 수행하여 검색 재현율과 QA 정확도에서 기존 기법보다 뛰어난 성능을 보였으며, 효율성도 유지했다[2512.03413v1].
- s4: 이러한 한계를 해결하기 위해 계층적 구조를 가진 문서에 적용되는 새로운 RAG 접근법인 BookRAG을 제안한다. BookRAG는 논리적 계층을 활용하고 엔티티 관계를 추적함으로써 매우 관련성 높은 정보를 검색한다. [2512.03413v1]

## H_A05 — 표와 텍스트가 섞인 질문에 답할 때 표 부분을 SQL로 바꿔서 푸는 연구 있어?

### 인용 블록

[문서 1]
[Distance: 0.4308]
[발행일: 2025-06-12]
[2506.10380v2] TableRAG: A Retrieval Augmented Generation Framework for Heterogeneous Document Reasoning
[초록] Retrieval-Augmented Generation (RAG) has demonstrated considerable effectiveness in open-domain question answering. However, when applied to heterogeneous documents, comprising both textual and tabular components, existing RAG approaches exhibit critical limitations. The prevailing practice of flattening tables and chunking strategies disrupts the intrinsic tabular structure, leads to information loss, and undermines the reasoning capabilities of LLMs in multi-hop, global queries. To address these challenges, we propose TableRAG, an SQL-based framework that unifies textual understanding and complex manipulations over tabular data. TableRAG iteratively operates in four steps: context-sensitive query decomposition, text retrieval, SQL programming and execution, and compositional intermediate answer generation. We also develop HeteQA, a novel benchmark designed to evaluate the multi-hop heterogeneous reasoning capabilities. Experimental results demonstrate that TableRAG consistently outperforms existing baselines on both public datasets and our HeteQA, establishing a new state-of-the-art for heterogeneous document question answering. We release TableRAG at https://github.com/yxh-y/TableRAG/tree/main.

. Similarly, Chain-of-Table (Wang et al., 2024) extends the CoT methodology to the tabular setting, enabling a multi-step reasoning process for more complex table-based queries. The second category involves utilizing programs to process tabular data. Tabsqlify (Nahid and Rafiei, 2024) employs a textto-SQL approach to decompose tables into smaller, contextually relevant sub-tables
[문서 2]
[Distance: 0.4128]
[발행일: 2024-06-29]
[2407.05952v3] H-STAR: LLM-driven Hybrid SQL-Text Adaptive Reasoning on Tables
[초록] Tabular reasoning involves interpreting natural language queries about tabular data, which presents a unique challenge of combining language understanding with structured data analysis. Existing methods employ either textual reasoning, which excels in semantic interpretation but struggles with mathematical operations, or symbolic reasoning, which handles computations well but lacks semantic understanding. This paper introduces a novel algorithm H-STAR that integrates both symbolic and semantic (textual) approaches in a two-stage process to address these limitations. H-STAR employs: (1) step-wise table extraction using `multi-view' column retrieval followed by row extraction, and (2) adaptive reasoning that adapts reasoning strategies based on question types, utilizing semantic reasoning for direct lookup and complex lexical queries while augmenting textual reasoning with symbolic reasoning support for quantitative and logical tasks. Our extensive experiments demonstrate that H-STAR significantly outperforms state-of-the-art methods across three tabular question-answering (QA) and fact-verification datasets, underscoring its effectiveness and efficiency.

. Moreover, it also highlights the constraints of relying solely on either text or SQL approaches, which are effectively addressed by our H-STAR approach. Together, these findings emphasize the substantial advantages of our hybrid and multi-view approach in addressing complex table reasoning tasks.

### 문장

- s1: 본 논문은 이러한 한계를 해결하기 위해 두 단계 프로세스를 통해 기호와 의미(텍스트) 접근법을 모두 통합한 새로운 알고리즘 H-STAR 를 제안한다. [2407.05952v3]
- s2: 실험 결과는 TableRAG가 공개 데이터셋과 이 논문의 HeteQA에서 모두 기존 베이스라인을 일관되게 능가하여 이질적 문서 질문 답변 분야에서 새로운 최첨단 성능을 달성함을 보여준다. [2506.10380v2]
- s3: H-STAR는 LLM 기반 하이브리드 SQL-텍스트 적응형 추론 방식을 통해 세 개의 표 QA 및 사실 검증 데이터셋에서 기존 방법보다 크게 성능이 향상됨을 입증했습니다[2407.05952v3].
- s4: 또한 TableRAG는 텍스트와 표를 모두 포함한 이질적 문서에 대해 기존 RAG 접근법의 한계를 극복하고, 공개 데이터셋과 자체 HeteQA 벤치마크에서 일관되게 최상위 성능을 달성했습니다[2506.10380v2].

## H_A06 — 긴 문서를 넣을 때 프롬프트를 압축해서 토큰을 줄이는 연구 핵심 내용 설명해줘

### 인용 블록

[문서 1]
[Distance: 0.3441]
[발행일: 2025-08-16]
[2508.15813v1] SCOPE: A Generative Approach for LLM Prompt Compression
[초록] Prompt compression methods enhance the efficiency of Large Language Models (LLMs) and minimize the cost by reducing the length of input context. The goal of prompt compression is to shorten the LLM prompt while maintaining a high generation quality. However, existing solutions, mainly based on token removal, face challenges such as information loss and structural incoherence, like missing grammar elements in a sentence, or incomplete word phrases after token removal. Such challenges limit the final generation quality of LLM. To overcome these limitations, we present a novel generative prompt compression method. Unlike the existing token removal methods, our method centers at a chunking-and-summarization mechanism. Specifically, our method splits prompt into semantically coherent chunks and rewrites the chunks to be more concise. The chunks are reconstructed into meaningful prompt finally. We design several optimization techniques for the mechanism, including optimized semantic chunking, outlier chunk handling, dynamic compression ratio, compression prioritization, and keyword maintaining. These techniques effectively improve the identifying and preserving of critical information and coherence among texts, as well as providing finer grind control of the compression ratio. We conduct extensive evaluation on question-answering and summarization tasks, with datasets covering multiple different domain. The evaluation shows our method achieves a significantly better compression quality, and higher stability than the state-of-the-art methods, especially under high compression ratio, which proves the effectiveness and practicality of our method.

prompt compression method. Unlike the existing token removal
methods, our method centers at a chunking-and-summarization
mechanism. Specifically, our method splits prompt into semantically coherent chunks and rewrites the chunks to be more concise.
The chunks are reconstructed into meaningful prompt finally. We
design several optimization techniques for the mechanism, including optimized semantic chunking, outlier chunk handling, dynamic
[문서 3]
[Distance: 0.3645]
[발행일: 2025-06-05]
[2506.05167v2] ECoRAG: Evidentiality-guided Compression for Long Context RAG
[초록] Large Language Models (LLMs) have shown remarkable performance in Open-Domain Question Answering (ODQA) by leveraging external documents through Retrieval-Augmented Generation (RAG). To reduce RAG overhead, from longer context, context compression is necessary. However, prior compression methods do not focus on filtering out non-evidential information, which limit the performance in LLM-based RAG. We thus propose Evidentiality-guided RAG, or ECoRAG framework. ECoRAG improves LLM performance by compressing retrieved documents based on evidentiality, ensuring whether answer generation is supported by the correct evidence. As an additional step, ECoRAG reflects whether the compressed content provides sufficient evidence, and if not, retrieves more until sufficient. Experiments show that ECoRAG improves LLM performance on ODQA tasks, outperforming existing compression methods. Furthermore, ECoRAG is highly cost-efficient, as it not only reduces latency but also minimizes token usage by retaining only the necessary information to generate the correct answer. Code is available at https://github.com/ldilab/ECoRAG.

## **2.2 Prompt Compression**

Numerous studies (Mu et al., 2024; Li et al., 2023; Kim et al., 2024) have focused on prompt compression to address both cost and performance challenges, as shown in prior research (Shi et al., 2023; Liu et al., 2024; Hsieh et al., 2024). RECOMP (Xu et al., 2024) provides both extractive and generative summaries of documents, considering whether the summaries helped answer the given question

### 문장

- s1: SCOPE는 다양한 도메인을 포함한 질문‑응답 및 요약 데이터셋에서 높은 압축 비율에서도 기존 방법보다 압축 품질과 안정성이 크게 향상됨을 보여준다[2508.15813v1].
- s2: ECoRAG는 오픈‑도메인 질문‑응답(OQDA) 작업에서 기존 압축 방법을 능가하며, 필요한 정보만 유지함으로써 지연 시간과 토큰 사용량을 동시에 감소시킨다[2506.05167v2].
- s3: 따라서 이 논문은 증거성(Evidentiality)을 활용한 RAG 프레임워크인 ECoRAG를 제안합니다. [2506.05167v2]
- s4: 평가 결과, 본 방법은 최신 기술 대비 압축 품질과 안정성이 크게 향상되었으며, 특히 높은 압축 비율에서도 이러한 성능을 유지함으로써 본 방법의 효과성과 실용성을 입증한다. [2508.15813v1]

## H_A07 — LLM이 스스로 검증용 질문을 만들어 답을 확인하면서 환각을 줄이는 방법 다룬 논문 있어?

### 인용 블록

[문서 1]
[Distance: 0.3165]
[발행일: 2023-09-20]
[2309.11495v2] Chain-of-Verification Reduces Hallucination in Large Language Models
[초록] Generation of plausible yet incorrect factual information, termed hallucination, is an unsolved issue in large language models. We study the ability of language models to deliberate on the responses they give in order to correct their mistakes. We develop the Chain-of-Verification (CoVe) method whereby the model first (i) drafts an initial response; then (ii) plans verification questions to fact-check its draft; (iii) answers those questions independently so the answers are not biased by other responses; and (iv) generates its final verified response. In experiments, we show CoVe decreases hallucinations across a variety of tasks, from list-based questions from Wikidata, closed book MultiSpanQA and longform text generation.

8

**Shortform verification questions are more accurately answered than longform queries** In a longform response, LLMs are prone to generate a number of hallucinations. However, it can often be the case that the LLM itself would know these hallucinations are wrong if queried specifically for that individual fact, independent of the rest of the longform generation, see Figure 1, Figure 3, and section 9
[문서 2]
[Distance: 0.3159]
[발행일: 2025-05-13]
[2505.09031v1] Improving the Reliability of LLMs: Combining CoT, RAG, Self-Consistency, and Self-Verification
[초록] Hallucination, where large language models (LLMs) generate confident but incorrect or irrelevant information, remains a key limitation in their application to complex, open-ended tasks. Chain-of-thought (CoT) prompting has emerged as a promising method for improving multistep reasoning by guiding models through intermediate steps. However, CoT alone does not fully address the hallucination problem. In this work, we investigate how combining CoT with retrieval-augmented generation (RAG), as well as applying self-consistency and self-verification strategies, can reduce hallucinations and improve factual accuracy. By incorporating external knowledge sources during reasoning and enabling models to verify or revise their own outputs, we aim to generate more accurate and coherent responses. We present a comparative evaluation of baseline LLMs against CoT, CoT+RAG, self-consistency, and self-verification techniques. Our results highlight the effectiveness of each method and identify the most robust approach for minimizing hallucinations while preserving fluency and reasoning depth.

In addition to CoT, recent advancements have introduced Self Consistency and Self Verification techniques as key components to reduce hallucinations and improve the factual accuracy of LLMs. Self Consistency, as explored by (Wang et al., 2023), emphasizes generating multiple answers and selecting the most consistent one to enhance model reliability and accuracy in ambiguous tasks

### 문장

- s1: 본 연구는 기준 대형 언어 모델(LLMs)을 Chain-of-Thought(CoT), CoT+RAG, 자기일관성(self-consistency), 그리고 자기검증(self-verification) 기법과 비교 평가한다. [2505.09031v1]
- s2: 실험에서 이 논문은 CoVe가 위키데이터 기반 목록 질문, 폐쇄형 MultiSpanQA 및 장문 텍스트 생성 등 다양한 작업 전반에 걸쳐 환각을 감소시킨다는 것을 보여줍니다. [2309.11495v2]
- s3: 따라서 질문처럼 "LLM이 스스로 검증용 질문을 만들어 답을 확인하면서 환각을 줄이는 방법"에 대한 논리는 [2309.11495v2]의 CoVe와 [2505.09031v1]의 자기검증 전략 모두에서 지지됩니다.
- s4: 그러나 LLM이 긴 형식 생성 전체와 무관하게 해당 개별 사실에 대해 구체적으로 질문하면 이러한 환각이 틀렸음을 알 수 있는 경우가 종종 있다. 이는 그림 1, 그림 3 및 제 9 절에서 확인할 수 있다. [2309.11495v2]
- s5: [2309.11495v2]은 CoVe가 다양한 과제(위키데이터 기반 목록 질문, Closed-book MultiSpanQA, 장문 텍스트 생성 등) 에서 환각을 감소시킨다고 보고합니다[2309.11495v2].
- s6: 두 논문 모두 LLM의 환각 감소에 긍정적인 효과를 보였으나, [2309.11495v2]은 구체적인 과제를 명시한 반면 [2505.09031v1]는 CoT·RAG·자기일관성·자기검증 등 여러 기법을 포괄적으로 조사했다는 점에서 연구 범위가 다릅니다.
- s7: 본 연구에서는 Chain-of-Thought(CoT)를 검색 증강 생성(RAG)과 결합하고, 자기 일관성 및 자기 검증 전략을 적용함으로써 환각 현상을 감소시키고 사실 정확도를 향상시키는 방법을 조사한다. [2505.09031v1]
- s8: [2505.09031v1]는 CoT와 RAG를 결합하고 자기일관성·자기검증 전략을 적용했을 때 환각이 줄어들고 사실 정확도가 향상된다고 제시하며, 이를 기존 LLM과 비교 평가했습니다[2505.09031v1].
- s9: We develop the Chain-of-Verification (CoVe) method whereby the model first (i) drafts an initial response; then (ii) plans verification questions to fact-check its draft; (iii) answers those questions independently so the answers are not biased by other responses; and (iv) generates its final verified response. [2309.11495v2]

## H_A08 — 여러 번 샘플링한 답들이 서로 얼마나 일치하는지로 환각을 잡아내는 연구 알려줘

### 인용 블록

[문서 1]
[Distance: 0.3179]
[발행일: 2026-01-07]
[2601.19918v2] Lowest Span Confidence: Zero-Shot Hallucination Detection from a Single LLM Response
[초록] Hallucinations in Large Language Models (LLMs), i.e., plausible but non-factual generations, pose a significant challenge to reliable deployment in high-stakes environments. However, many existing hallucination detectors require expensive repeated sampling for consistency checks or access to model-internal states unavailable in common API-based scenarios. To this end, we propose an efficient zero-shot metric called Lowest Span Confidence (LSC) for hallucination detection under minimal resource assumptions. Concretely, LSC evaluates the local confidence of adjacent complete-word spans. By selecting the lowest aggregated confidence across neighboring words whose token widths can vary, LSC captures localized uncertainty associated with factual inconsistency. This boundary-aligned smoothing reduces the global dilution of perplexity and the sensitivity of minimum token probability to isolated noise. Our main evaluation spans four model families {Llama-2, Qwen2.5, Gemma-2, Mistral} and seven benchmarks {NQ, TriviaQA, SQuAD, CoQA, HotpotQA, RAGTruth, FELM}. Additional analyses examine word reconstruction, span width, and the role of adjacency in preserving local confidence. Across these settings, LSC is competitive with methods that use multiple responses or model-internal information while requiring only one response and its output token probabilities, without training a separate detector or using an auxiliary model.

Table 1: Hallucination Detector Access Requirements. Methods are grouped by required responses and model information. LSC needs one response and selectedtoken probabilities. _†_ means an auxiliary semantic model. Citations for PPL, G-NLL, and Min-P identify studies using these basic scores. Appendix B gives method details.
[문서 2]
[Distance: 0.3219]
[발행일: 2025-08-19]
[2508.14314v2] Zero-knowledge LLM hallucination detection and mitigation through fine-grained cross-model consistency
[초록] Large language models (LLMs) have demonstrated impressive capabilities across diverse tasks, but they remain susceptible to hallucinations--generating content that appears plausible but contains factual inaccuracies. We present Finch-Zk, a black-box framework that leverages fine-grained cross-model consistency to detect and mitigate hallucinations in LLM outputs without requiring external knowledge sources. Finch-Zk introduces two key innovations: 1) a cross-model consistency checking strategy that reveals fine-grained inaccuracies by comparing responses generated by diverse models from semantically-equivalent prompts, and 2) a targeted mitigation technique that applies precise corrections to problematic segments while preserving accurate content. Experiments on the FELM dataset show Finch-Zk improves hallucination detection F1 scores by 6-39\% compared to existing approaches. For mitigation, Finch-Zk achieves up to 9 absolute percentage points improvement in answer accuracy on the GPQA-diamond dataset when applied to state-of-the-art models like Llama 4 Maverick and Claude 4 Sonnet. Extensive evaluation on multiple datasets demonstrates that Finch-Zk provides a practical, deployment-ready safeguard for enhancing factual reliability in production LLM systems.

objectives.
We chose FELM (Zhao et al., 2023) for hallucination detection evaluation for several key reasons:  
- **Fine-grained annotations:** FELM provides
segment-level (sentence-level) human-annotated
factuality labels rather than coarse response-level
labels, enabling evaluation of our fine-grained
detection capabilities. The dataset contains 4,425
annotated segments across 847 samples with high
inter-annotator agreement (91.3%).  
- **Diverse domains:** Unlike benchmarks fo

### 문장

- s1: 반면 Lowest Span Confidence는 Llama-2, Qwen2.5, Gemma-2, Mistral 등 네 모델 계열과 NQ, TriviaQA, SQuAD, CoQA, HotpotQA, RAGTruth, FELM 등 일곱 벤치마크를 대상으로 평가했습니다[2601.19918v2].
- s2: FELM 데이터셋에 대한 실험 결과, Finch-Zk는 기존 접근법 대비 환각 탐지 F1 점수를 6~39% 향상시킨다. [2508.14314v2]
- s3: 본 평가는 Llama-2, Qwen2.5, Gemma-2, Mistral 네 모델 계열과 NQ, TriviaQA, SQuAD, CoQA, HotpotQA, RAGTruth, FELM 일곱 벤치마크를 대상으로 수행되었습니다. [2601.19918v2]
- s4: Finch-Zk는 FELM 데이터셋에서 기존 접근법 대비 환각 탐지 F1 점수를 6~39% 향상시켰으며, GPQA-diamond 데이터셋에서는 정답 정확도를 최대 9%p 개선하는 결과를 보였습니다[2508.14314v2].

## H_A09 — 에이전트가 실패한 시도를 말로 돌아보고 다음 시도에 반영하는 방법 다룬 논문 있어?

### 인용 블록

[문서 1]
[Distance: 0.3768]
[발행일: 2026-10-13]
[2610.17953v1] Agent-Reflex: Teaching Language Agents to Act Reflectively
[초록] Large language models have evolved from single-turn chatbots into interactive agents capable of long-horizon reasoning. In real deployments, MCP tool services can return noisy feedback and users may intervene to correct the agent, but existing methods provide limited supervision for reflection learning and failure recovery. To bridge this gap, we propose Agent-Reflex, a general training framework for incentivizing proactive reflection in agents. Specifically, Agent-Reflex comprises three stages. First, Environment Reflection Skill Discovery (RSD) injects grounded tool-feedback perturbations into environment scaling, samples a capability-diverse LLM pool, mines matched success-failure pairs, and summarizes reusable reflection meta-skills. Building on this skill library, we then apply Reflective Supervised Fine-Tuning (ReSFT) that converts each skill into supervision for self-reflection, skill recovery, and user-centric correction, strengthening complementary reflective behaviors. Finally, we propose On-Policy Reflective Policy Optimization (ORPO) to combine agentic reinforcement learning under noisy interactions with reflection-guided on-policy distillation to further elicit proactive reflection. Built on Qwen3-8B, Agent-Reflex reaches 58.6 overall on five long-horizon tool-use benchmarks and 29.1 on AgentNoiseBench, surpassing strong environment-scaling and reflection baselines. Experiments on six challenging agent benchmark suites demonstrate the effectiveness of Agent-Reflex. Further analyses show that Agent-Reflex improves agents' robustness to noise while maintaining stable training dynamics, supporting scalable agent training. Our code is available at https://github.com/RUC-NLPIR/Agent-Reflex.

## **3 Methodology: Agent-Reflex**  
**Overview.** Figure 2 summarizes the pipeline. To convert environment failures into a reflection capability, AgentReflex comprises three stages:  
**(1) Environment Reflection Skill Discovery (RSD) (§ 3.1)** . Build failure-aware executable environments and mine verifier-matched pairs into an offline skill library.
[문서 2]
[Distance: 0.4254]
[발행일: 2024-12-18]
[2412.13781v1] Meta-Reflection: A Feedback-Free Reflection Learning Framework
[초록] Despite the remarkable capabilities of large language models (LLMs) in natural language understanding and reasoning, they often display undesirable behaviors, such as generating hallucinations and unfaithful reasoning. A prevalent strategy to mitigate these issues is the use of reflection, which refines responses through an iterative process. However, while promising, reflection heavily relies on high-quality external feedback and requires iterative multi-agent inference processes, thus hindering its practical application. In this paper, we propose Meta-Reflection, a novel feedback-free reflection mechanism that necessitates only a single inference pass without external feedback. Motivated by the human ability to remember and retrieve reflections from past experiences when encountering similar problems, Meta-Reflection integrates reflective insights into a codebook, allowing the historical insights to be stored, retrieved, and used to guide LLMs in problem-solving. To thoroughly investigate and evaluate the practicality of Meta-Reflection in real-world scenarios, we introduce an industrial e-commerce benchmark named E-commerce Customer Intent Detection (ECID). Extensive experiments conducted on both public datasets and the ECID benchmark highlight the effectiveness and efficiency of our proposed approach.

- Matthew Renze and Erhan Guven. 2024. Self-reflection in llm agents: Effects on problem-solving performance. _arXiv preprint arXiv:2405.06682_ .  
- Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, et al. 2023. Code llama: Open foundation models for code. _arXiv preprint arXiv:2308.12950_ .

### 문장

- s1: Qwen3-8B 기반인 Agent-Reflex는 다섯 개의 장기 도구 사용 벤치마크에서 전체 점수 58.6을 달성하고 AgentNoiseBench에서는 29.1의 성능을 보이며, 강력한 환경 확장 및 반성 기반 모델을 능가한다. [2610.17953v1]
- s2: 실제 시나리오에서 메타반성(Meta-Reflection)의 실용성을 철저히 조사하고 평가하기 위해 이 논문은 전자상거래 고객 의도 탐지(ECID)라는 산업용 벤치마크를 도입한다. [2412.13781v1]
- s3: Agent-Reflex는 환경 실패를 반성 능력으로 전환하여 58.6의 전반적 점수와 29.1의 AgentNoiseBench 점수를 달성했으며, 이는 강력한 환경 확장 및 반성 기반선을 능가합니다[2610.17953v1].
- s4: Meta-Reflection은 산업용 전자상거래 벤치마크인 ECID를 통해 실제 시나리오에서의 실용성을 조사하고 평가했습니다[2412.13781v1].

## H_A11 — 작은 모델이 초안을 만들고 큰 모델이 한 번에 검증하는 방식으로 생성 속도를 높인 연구 알려줘

### 인용 블록

[문서 1]
[Distance: 0.3673]
[발행일: 2026-07-05]
[2607.04461v1] Flash-BoN: Instant Drafts for Inference-Time Scaling in Diffusion Models
[초록] Inference-time scaling for text-to-image generation has progressed from simple Best-of-$N$ (BoN) sampling to guided search methods that verify and steer candidate trajectories at intermediate denoising steps. These approaches focus on when and how often to verify during denoising but largely treat the cost of generation itself as fixed. Moreover, the standard practice of comparing methods by number of function evaluations (NFEs) counts only denoising forward passes and ignores verifier overhead, which can distort efficiency rankings. We show that under wall-clock evaluation, simple BoN already matches or outperforms several guided search techniques, suggesting that compute is better spent on broader exploration than on repeated intermediate verification. This motivates Flash-BoN, which generates a large pool of inexpensive draft candidates by combining three complementary acceleration knobs: timestep truncation, layer skipping, and activation proxies into a single configuration optimized once per model. An efficient multi-stage verification procedure then identifies the most promising draft, which is refined at full quality. Across three benchmarks and three model scales, Flash-BoN consistently outperforms all baselines under fixed wall-clock budgets, with gains that grow at larger model scales (+8% AUC). We further show that our strategy combines well and improves existing orthogonal techniques such as reflection-based prompt optimization (+16% AUC). The gains correlate with increased candidate diversity, which also enables draft-guided selection to accelerate RL post-training convergence.

## **6 Discussion**

We introduced `Flash-BoN` , an inference-time scaling method that generates a large pool of inexpensive draft candidates, identifies the most promising one via an efficient multi-stage verification procedure, and refines only that candidate at full quality. Across multiple benchmarks and models, `Flash-BoN` consistently outperforms baselines under fixed wall-clock budgets, with gains that grow at larger model scales
[문서 2]
[Distance: 0.4160]
[발행일: 2024-06-27]
[2407.12021v2] Adaptive Draft-Verification for Efficient Large Language Model Decoding
[초록] Large language model (LLM) decoding involves generating a sequence of tokens based on a given context, where each token is predicted one at a time using the model's learned probabilities. The typical autoregressive decoding method requires a separate forward pass through the model for each token generated, which is computationally inefficient and poses challenges for deploying LLMs in latency-sensitive scenarios. The main limitations of current decoding methods stem from their inefficiencies and resource demands. Existing approaches either necessitate fine-tuning smaller models, which is resource-intensive, or rely on fixed retrieval schemes to construct drafts for the next tokens, which lack adaptability and fail to generalize across different models and contexts. To address these issues, we introduce a novel methodology called ADED, which accelerates LLM decoding without requiring fine-tuning. Our approach involves an adaptive draft-verification process that evolves over time to improve efficiency. We utilize a tri-gram matrix-based LLM representation to dynamically approximate the output distribution of the LLM, allowing the model to adjust to changing token probabilities during the decoding process. Additionally, we implement a draft construction mechanism that effectively balances exploration and exploitation, ensuring that the drafts generated are both diverse and close to the true output distribution of the LLM. The importance of this design lies in its ability to optimize the draft distribution adaptively, leading to faster and more accurate decoding. Through extensive experiments on various benchmark datasets and LLM architectures, we demonstrate that ADED significantly accelerates the decoding process while maintaining high accuracy, making it suitable for deployment in a wide range of practical applications.

# **Adaptive Draft-Verification for Efficient Large Language Model Decoding**  
**Xukun Liu**[1] **, Bowen Lei**[2] **, Ruqi Zhang**[3] **Dongkuan Xu**[4]  
1Northwestern University  
2Texas A&M University  
3Purdue University  
4North Carolina State University  
xukunliu2025@u.northwestern.edu, bowenlei@stat.tamu.edu, ruqiz@purdue.edu, dxu27@ncsu.edu
[문서 3]
[Distance: 0.4005]
[발행일: 2024-07-11]
[2407.08223v2] Speculative RAG: Enhancing Retrieval Augmented Generation through Drafting
[초록] Retrieval augmented generation (RAG) combines the generative abilities of large language models (LLMs) with external knowledge sources to provide more accurate and up-to-date responses. Recent RAG advancements focus on improving retrieval outcomes through iterative LLM refinement or self-critique capabilities acquired through additional instruction tuning of LLMs. In this work, we introduce Speculative RAG - a framework that leverages a larger generalist LM to efficiently verify multiple RAG drafts produced in parallel by a smaller, distilled specialist LM. Each draft is generated from a distinct subset of retrieved documents, offering diverse perspectives on the evidence while reducing input token counts per draft. This approach enhances comprehension of each subset and mitigates potential position bias over long context. Our method accelerates RAG by delegating drafting to the smaller specialist LM, with the larger generalist LM performing a single verification pass over the drafts. Extensive experiments demonstrate that Speculative RAG achieves state-of-the-art performance with reduced latency on TriviaQA, MuSiQue, PopQA, PubHealth, and ARC-Challenge benchmarks. It notably enhances accuracy by up to 12.97% while reducing latency by 50.83% compared to conventional RAG systems on PubHealth.

. The draft model is typically either an independent model from the same series (Leviathan et al., 2023; Chen et al., 2023a) or the target model itself (Zhang et al., 2023a; Cai et al., 2024). Our approach extends this concept from token-level drafting to answer-level drafting

### 문장

- s1: ADED는 다양한 벤치마크 데이터셋과 LLM 아키텍처에 대해 광범위한 실험을 통해 디코딩 과정을 크게 가속화하면서도 높은 정확도를 유지함을 보여줍니다[2407.12021v2].
- s2: PubHealth에서 기존 RAG 시스템에 비해 정확도를 최대 12.97% 향상시키고 지연 시간을 50.83% 감소시킨다. [2407.08223v2]
- s3: 이는 Flash-BoN을 동기화시켰으며, 이 방법은 모델마다 한 번만 최적화된 단일 구성으로 시간 단계 절단, 레이어 스킵핑, 활성화 프록시라는 세 가지 상호 보완적인 가속화 요소를 결합하여 저렴한 초안 후보들을 대규모로 생성합니다. [2607.04461v1]
- s4: Speculative RAG는 TriviaQA, MuSiQue, PopQA, PubHealth, ARC-Challenge 등 여러 벤치마크에서 지연 시간을 감소시키고 성능을 향상시켰으며, 특히 PubHealth에서는 지연 시간을 50.83% 줄이고 정확도를 최대 12.97% 향상시켰습니다[2407.08223v2].
- s5: 이러한 문제들을 해결하기 위해 이 논문은 미세 조정 없이도 LLM 디코딩 속도를 향상시키는 새로운 방법론인 ADED를 제안한다. [2407.12021v2]
- s6: Flash-BoN은 고정된 벽시계 예산 하에서 모든 베이스라인을 일관되게 능가하며, 모델 규모가 커질수록 성능 향상이 더 크게 나타납니다[2607.04461v1].

## H_A12 — 질문 난이도에 따라 검색을 안 하거나 한 번 하거나 여러 번 하도록 고르는 RAG 연구 있어?

### 인용 블록

[문서 1]
[Distance: 0.2986]
[발행일: 2024-12-02]
[2412.01572v4] MBA-RAG: a Bandit Approach for Adaptive Retrieval-Augmented Generation through Question Complexity
[초록] Retrieval Augmented Generation (RAG) has proven to be highly effective in boosting the generative performance of language model in knowledge-intensive tasks. However, existing RAG framework either indiscriminately perform retrieval or rely on rigid single-class classifiers to select retrieval methods, leading to inefficiencies and suboptimal performance across queries of varying complexity. To address these challenges, we propose a reinforcement learning-based framework that dynamically selects the most suitable retrieval strategy based on query complexity. % our solution Our approach leverages a multi-armed bandit algorithm, which treats each retrieval method as a distinct ``arm'' and adapts the selection process by balancing exploration and exploitation. Additionally, we introduce a dynamic reward function that balances accuracy and efficiency, penalizing methods that require more retrieval steps, even if they lead to a correct result. Our method achieves new state of the art results on multiple single-hop and multi-hop datasets while reducing retrieval costs. Our code are available at https://github.com/FUTUREEEEEE/MBA .

# **MBA-RAG: a Bandit Approach for Adaptive Retrieval-Augmented Generation through Question Complexity**  
**Xiaqiang Tang**[*] **[1,2] , Qiang Gao[*2,3] , Jian Li[*2] , Nan Du[2] , Qi Li[4]** , **Sihong Xie**[†] **[1]** ,  
1The Hong Kong University of Science and Technology (Guangzhou),  
2Tencent Hunyuan, 3Wuhan University, 4Iowa State University,  
**Correspondence:** sihongxie@hkust-gz.edu.cn
[문서 2]
[Distance: 0.4213]
[발행일: 2025-09-05]
[2509.04820v1] Fishing for Answers: Exploring One-shot vs. Iterative Retrieval Strategies for Retrieval Augmented Generation
[초록] Retrieval-Augmented Generation (RAG) based on Large Language Models (LLMs) is a powerful solution to understand and query the industry's closed-source documents. However, basic RAG often struggles with complex QA tasks in legal and regulatory domains, particularly when dealing with numerous government documents. The top-$k$ strategy frequently misses golden chunks, leading to incomplete or inaccurate answers. To address these retrieval bottlenecks, we explore two strategies to improve evidence coverage and answer quality. The first is a One-SHOT retrieval method that adaptively selects chunks based on a token budget, allowing as much relevant content as possible to be included within the model's context window. Additionally, we design modules to further filter and refine the chunks. The second is an iterative retrieval strategy built on a Reasoning Agentic RAG framework, where a reasoning LLM dynamically issues search queries, evaluates retrieved results, and progressively refines the context over multiple turns. We identify query drift and retrieval laziness issues and further design two modules to tackle them. Through extensive experiments on a dataset of government documents, we aim to offer practical insights and guidance for real-world applications in legal and regulatory domains.

## **1 Introduction**

Retrieval-Augmented Generation (RAG) (Chen et al., 2024; Lewis et al., 2020; Gao et al., 2023) based on Large Language Models (LLMs) has been intensively deployed to conduct questionanswering (QA) towards closed-source or internal documents

### 문장

- s1: Fishing for Answers는 정부 문서 데이터셋을 대상으로 한 실험을 통해 일회성 검색과 반복적 검색 전략을 비교하고, 증거 커버리지와 답변 품질 향상을 목표로 한다 [2509.04820v1].
- s2: MBA-RAG: 질문 복잡도를 활용한 적응형 검색 증강 생성을 위한 밴디트 접근법 (Xiaqiang Tang[*][1,2], Qiang Gao[*2,3], Jian Li[*2], Nan Du[2], Qi Li[4], Sihong Xie[†][1]; 1 홍콩과학기술대학교 (광저우), 2 텐센트 훈위안, 3 후난 대학, 4 아이오와 주립대학교; 대응: sihongxie@hkust-gz.edu.cn) [2412.01572v4]
- s3: top-k 전략은 종종 정답 조각을 놓쳐서 불완전하거나 부정확한 답변을 초래한다. [2509.04820v1]
- s4: MBA-RAG은 단일 홉과 멀티 홉 데이터셋에서 새로운 상태-of-the-art 결과를 달성하면서 검색 비용을 감소시켰다 [2412.01572v4].

## H_A13 — 검색된 문서를 요약하거나 압축해서 LLM에 넣는 방식으로 RAG 비용을 줄인 연구 알려줘

### 인용 블록

[문서 1]
[Distance: 0.4255]
[발행일: 2026-01-10]
[2601.06551v1] L-RAG: Balancing Context and Retrieval with Entropy-Based Lazy Loading
[초록] Retrieval-Augmented Generation (RAG) has emerged as the predominant paradigm for grounding Large Language Model outputs in factual knowledge, effectively mitigating hallucinations. However, conventional RAG systems operate under a "retrieve-always" assumption, querying vector databases for every input regardless of query complexity. This static approach incurs substantial computational overhead and inference latency, particularly problematic for high-throughput production deployments. We introduce L-RAG (Lazy Retrieval-Augmented Generation), an adaptive framework that implements hierarchical context management through entropy-based gating. L-RAG employs a two-tier architecture: queries are first processed with a compact document summary, and expensive chunk retrieval is triggered only when the model's predictive entropy exceeds a calibrated threshold, signaling genuine uncertainty. Through experiments on SQuAD 2.0 (N=500) using the Phi-2 model, we demonstrate that L-RAG provides a tunable accuracy-efficiency trade-off: at a conservative threshold (tau=0.5), L-RAG achieves 78.2% accuracy, matching Standard RAG (77.8%), with 8% retrieval reduction; at a balanced threshold (tau=1.0), retrieval reduction increases to 26% with modest accuracy trade-off (76.0%). Latency analysis shows that L-RAG saves 80-210ms per query when retrieval latency exceeds 500ms. Analysis of entropy distributions reveals statistically significant separation (p < 0.001) between correct predictions (H=1.72) and errors (H=2.20), validating entropy as a reliable uncertainty signal. L-RAG offers a practical, training-free approach toward more efficient RAG deployment, providing system architects with a configurable knob to balance accuracy and throughput requirements.

The success of RAG, however, comes at a substantial computational cost. In conventional implementations, every incoming query triggers a retrieval pipeline: the query must be encoded into a dense vector representation, a nearest neighbor search must be executed against a vector index containing potentially millions of document embeddings, and the retrieved passages must be incorporated into an extended context that the language model processes
[문서 2]
[Distance: 0.4779]
[발행일: 2025-04-11]
[2504.08386v1] PCA-RAG: Principal Component Analysis for Efficient Retrieval-Augmented Generation
[초록] Retrieval-Augmented Generation (RAG) has emerged as a powerful paradigm for grounding large language models in external knowledge sources, improving the precision of agents responses. However, high-dimensional language model embeddings, often in the range of hundreds to thousands of dimensions, can present scalability challenges in terms of storage and latency, especially when processing massive financial text corpora. This paper investigates the use of Principal Component Analysis (PCA) to reduce embedding dimensionality, thereby mitigating computational bottlenecks without incurring large accuracy losses. We experiment with a real-world dataset and compare different similarity and distance metrics under both full-dimensional and PCA-compressed embeddings. Our results show that reducing vectors from 3,072 to 110 dimensions provides a sizeable (up to $60\times$) speedup in retrieval operations and a $\sim 28.6\times$ reduction in index size, with only moderate declines in correlation metrics relative to human-annotated similarity scores. These findings demonstrate that PCA-based compression offers a viable balance between retrieval fidelity and resource efficiency, essential for real-time systems such as Zanista AI's \textit{Newswitch} platform. Ultimately, our study underscores the practicality of leveraging classical dimensionality reduction techniques to scale RAG architectures for knowledge-intensive applications in finance and trading, where speed, memory efficiency, and accuracy must jointly be optimized.

. On the generation side, researchers have addressed the inference bottleneck that arises from conditioning on many retrieved documents. A standard RAG model prepends _k_ retrieved passages to the query, causing input length (and thus Transformer cost) to grow linearly with _k_ [15]. Techniques like Fusion-in-Decoder (FiD) integrate multiple documents by encoding them separately and fusing their representations in the decoder, which improved answer quality for multi-document QA [15]

### 문장

- s1: PCA-RAG는 차원 축소 기법을 적용해 벡터 크기를 3,072에서 110으로 줄였을 때 검색 속도가 최대 60배 빨라지고 인덱스 크기가 약 28.6배 감소하는 효과를 얻었습니다[2504.08386v1].
- s2: 본 연구 결과는 벡터 차원을 3,072에서 110으로 축소할 경우 검색 연산 속도가 크게 향상되고(최대 $60\times$), 인덱스 크기가 약 $28.6\times$ 감소하며, 인간이 주석 처리한 유사도 점수에 대한 상관관계 지표는 중간 정도의 하락만 보인다는 것을 보여줍니다. [2504.08386v1]
- s3: SQuAD 2.0(N=500) 데이터셋에서 Phi-2 모델을 이용해 수행한 실험을 통해 L-RAG가 조정 가능한 정확도‑효율성 트레이드오프를 제공함을 보여준다: 보수적 임계값(τ=0.5)에서는 정확도가 78.2%로 표준 RAG(77.8%)와 동등하며 검색 감소율이 8%이고, 균형 잡힌 임계값(τ=1.0)에서는 검색 감소율이 26%로 증가하면서 정확도는 76.0%로 약간 하락한다. [2601.06551v1]
- s4: L-RAG은 엔트로피 기반의 지연 로딩을 통해 검색량을 최대 26%까지 감소시키면서도 정확도를 표준 RAG와 유사 수준으로 유지하는 결과를 보였습니다[2601.06551v1].

## H_A15 — 평가 문제가 학습 데이터에 섞였는지(데이터 오염) 확인하는 방법 다룬 논문 알려줘

### 인용 블록

[문서 1]
[Distance: 0.3071]
[발행일: 2024-02-24]
[2402.15938v3] Generalization or Memorization: Data Contamination and Trustworthy Evaluation for Large Language Models
[초록] Recent statements about the impressive capabilities of large language models (LLMs) are usually supported by evaluating on open-access benchmarks. Considering the vast size and wide-ranging sources of LLMs' training data, it could explicitly or implicitly include test data, leading to LLMs being more susceptible to data contamination. However, due to the opacity of training data, the black-box access of models, and the rapid growth of synthetic training data, detecting and mitigating data contamination for LLMs faces significant challenges. In this paper, we propose CDD, which stands for Contamination Detection via output Distribution for LLMs. CDD necessitates only the sampled texts to detect data contamination, by identifying the peakedness of LLM's output distribution. To mitigate the impact of data contamination in evaluation, we also present TED: Trustworthy Evaluation via output Distribution, based on the correction of LLM's output distribution. To facilitate this study, we introduce two benchmarks, i.e., DetCon and ComiEval, for data contamination detection and contamination mitigation evaluation tasks. Extensive experimental results show that CDD achieves the average relative improvements of 21.8\%-30.2\% over other contamination detection approaches in terms of Accuracy, F1 Score, and AUC metrics, and can effectively detect implicit contamination. TED substantially mitigates performance improvements up to 66.9\% attributed to data contamination across various contamination setups. In real-world applications, we reveal that ChatGPT exhibits a high potential to suffer from data contamination on HumanEval benchmark.

Data contamination, also known as data leakage, refers to the scenario where the test data has been included in the model’s training data (Magar et al., 2022; Dickson, 2023), leading to the model performing exceptionally well on these leaked test data. Owing to the vast size and wide-ranging sources of the pre-trained datasets for LLMs, they are more susceptible to data contamination, which can be primarily categorized into two situations:  
1
[문서 2]
[Distance: 0.3028]
[발행일: 2023-11-16]
[2311.09783v2] Investigating Data Contamination in Modern Benchmarks for Large Language Models
[초록] Recent observations have underscored a disparity between the inflated benchmark scores and the actual performance of LLMs, raising concerns about potential contamination of evaluation benchmarks. This issue is especially critical for closed-source models and certain open-source models where training data transparency is lacking. In this paper we study data contamination by proposing two methods tailored for both open-source and proprietary LLMs. We first introduce a retrieval-based system to explore potential overlaps between evaluation benchmarks and pretraining corpora. We further present a novel investigation protocol named \textbf{T}estset \textbf{S}lot Guessing (\textit{TS-Guessing}), applicable to both open and proprietary models. This approach entails masking a wrong answer in a multiple-choice question and prompting the model to fill in the gap. Additionally, it involves obscuring an unlikely word in an evaluation example and asking the model to produce it. We find that certain commercial LLMs could surprisingly guess the missing option in various test sets. Specifically, in the TruthfulQA benchmark, we find that LLMs exhibit notable performance improvement when provided with additional metadata in the benchmark. Further, in the MMLU benchmark, ChatGPT and GPT-4 demonstrated an exact match rate of 52\% and 57\%, respectively, in guessing the missing options in benchmark test data. We hope these results underscore the need for more robust evaluation methodologies and benchmarks in the field.

## **6 Conclusion and Future Work**

We introduce two approaches for investigating data contamination in several widely-used contemporary evaluation benchmarks. First, we develop an information retrieval system to identify benchmarks with significant overlap with the pre-training corpus. Second, we propose a novel investigation protocol, TS-Guessing, to assess potential data leakage in benchmark datasets when evaluated with LLMs
[문서 5]
[Distance: 0.2996]
[발행일: 2024-06-26]
[2406.18326v2] PaCoST: Paired Confidence Significance Testing for Benchmark Contamination Detection in Large Language Models
[초록] Large language models (LLMs) are known to be trained on vast amounts of data, which may unintentionally or intentionally include data from commonly used benchmarks. This inclusion can lead to cheatingly high scores on model leaderboards, yet result in disappointing performance in real-world applications. To address this benchmark contamination problem, we first propose a set of requirements that practical contamination detection methods should follow. Following these proposed requirements, we introduce PaCoST, a Paired Confidence Significance Testing to effectively detect benchmark contamination in LLMs. Our method constructs a counterpart for each piece of data with the same distribution, and performs statistical analysis of the corresponding confidence to test whether the model is significantly more confident under the original benchmark. We validate the effectiveness of PaCoST and apply it on popular open-source models and benchmarks. We find that almost all models and benchmarks we tested are suspected contaminated more or less. We finally call for new LLM evaluation methods.

We examine the most popular data contamination detection methods and compare them in Table 1. As evident, all methods, except our proposed one, fail to satisfy all properties. This observation underscores the advantages of our method.

### 문장

- s1: 특히 TruthfulQA 벤치마크에서 이 논문은 추가 메타데이터가 제공될 때 LLM이 현저한 성능 향상을 보인다는 것을 발견했습니다. [2311.09783v2]
- s2: 광범위한 실험 결과는 정확도, F1 점수, AUC 지표에서 CDD가 다른 오염 탐지 접근법보다 평균 상대적 향상이 21.8%~30.2%임을 보여주며, 암시적인 오염을 효과적으로 탐지할 수 있음을 보여줍니다. [2402.15938v3]
- s3: [2402.15938v3]은 CDD와 TED 방법이 각각 정확도, F1 점수, AUC에서 평균 상대적 향상을 21.8%~30.2% 달성하고, HumanEval 벤치마크에서 ChatGPT가 높은 오염 잠재력을 보인다고 보고한다.
- s4: [2311.09783v2]는 TruthfulQA와 MMLU 벤치마크에서 LLM이 누락된 옵션을 추측하거나 메타데이터 제공 시 성능이 크게 향상되는 현상을 관찰하여 오염 가능성을 확인한다.
- s5: 이 논문이 테스트한 거의 모든 모델과 벤치마크가 어느 정도 오염되어 있다고 의심된다는 것을 발견했습니다. [2406.18326v2]
- s6: [2406.18326v2]는 거의 모든 테스트된 모델과 벤치마크가 어느 정도 오염되어 있다고 의심된다고 결론지으며, 이는 대상이 좁은 경우에도 해당 결과가 적용될 수 있음을 시사한다.

