## d0001 (R-)

**질문** 네 지식 베이스(ChromaDB)에서 최근 AI 논문 아무거나 하나 찾아서 요약해 봐

[문서 1]
[발행일: 2024-06-21]
[2406.15187v2] UDA: A Benchmark Suite for Retrieval Augmented Generation in Real-world Document Analysis
[초록] The use of Retrieval-Augmented Generation (RAG) has improved Large Language Models (LLMs) in collaborating with external data, yet significant challenges exist in real-world scenarios. In areas such as academic literature and finance question answering, data are often found in raw text and tables in HTML or PDF formats, which can be lengthy and highly unstructured. In this paper, we introduce a benchmark suite, namely Unstructured Document Analysis (UDA), that involves 2,965 real-world documents and 29,590 expert-annotated Q&A pairs. We revisit popular LLM- and RAG-based solutions for document analysis and evaluate the design choices and answer qualities across multiple document domains and diverse query types. Our evaluation yields interesting findings and highlights the importance of data parsing and retrieval. We hope our benchmark can shed light and

---

## d0013 (R-)

**질문** Transformer 논문 자세히 설명해줘

[문서 1]
[발행일: 2025-01-03]
[2501.02040v2] A Separable Self-attention Inspired by the State Space Model for Computer Vision
[초록] Mamba is an efficient State Space Model (SSM) with linear computational complexity. Although SSMs are not suitable for handling non-causal data, Vision Mamba (ViM) methods still demonstrate good performance in tasks such as image classification and object detection. Recent studies have shown that there is a rich theoretical connection between state space models and attention variants. We propose a novel separable self attention method, for the first time introducing some excellent design concepts of Mamba into separable self-attention. To ensure a fair comparison with ViMs, we introduce VMINet, a simple yet powerful prototype architecture, constructed solely by stacking our novel attention modules with the most basic down-sampling layers. Notably, VMINet differs significantly from the conventional Transformer architecture. Our experiments demonstrate that VMINet

[문서 2]
[발행일: 2025-01-03]
[2501.02040v2] A Separable Self-attention Inspired by the State Space Model for Computer Vision
[초록] Mamba is an efficient State Space Model (SSM) with linear computational complexity. Although SSMs are not suitable for handling non-causal data, Vision Mamba (ViM) methods still demonstrate good performance in tasks such as image classification and object detection. Recent studies have shown that there is a rich theoretical connection between state space models and attention variants. We propose a novel separable self attention method, for the first time introducing some excellent design concepts of Mamba into separable self-attention. To ensure a fair comparison with ViMs, we introduce VMINet, a simple yet powerful prototype architecture, constructed solely by stacking our novel attention modules with the most basic down-sampling layers. Notably, VMINet differs significantly from the conventional Transformer architecture. Our experiments demonstrate that VMINet

---

## d0014 (R-)

**질문** Attention Is All You Need 논문 자세히 설명해줘

[문서 1]
[발행일: 2024-12-23]
[2412.18040v1] Theoretical Constraints on the Expressive Power of $\mathsf{RoPE}$-based Tensor Attention Transformers
[초록] Tensor Attention extends traditional attention mechanisms by capturing high-order correlations across multiple modalities, addressing the limitations of classical matrix-based attention. Meanwhile, Rotary Position Embedding ($\mathsf{RoPE}$) has shown superior performance in encoding positional information in long-context scenarios, significantly enhancing transformer models' expressiveness. Despite these empirical successes, the theoretical limitations of these technologies remain underexplored. In this study, we analyze the circuit complexity of Tensor Attention and $\mathsf{RoPE}$-based Tensor Attention, showing that with polynomial precision, constant-depth layers, and linear or sublinear hidden dimension, they cannot solve fixed membership problems or $(A_{F,r})^*$ closure problems, under the assumption that $\mathsf{TC}^0 \neq \mathsf

[문서 2]
[발행일: 2024-12-23]
[2412.18040v1] Theoretical Constraints on the Expressive Power of $\mathsf{RoPE}$-based Tensor Attention Transformers
[초록] Tensor Attention extends traditional attention mechanisms by capturing high-order correlations across multiple modalities, addressing the limitations of classical matrix-based attention. Meanwhile, Rotary Position Embedding ($\mathsf{RoPE}$) has shown superior performance in encoding positional information in long-context scenarios, significantly enhancing transformer models' expressiveness. Despite these empirical successes, the theoretical limitations of these technologies remain underexplored. In this study, we analyze the circuit complexity of Tensor Attention and $\mathsf{RoPE}$-based Tensor Attention, showing that with polynomial precision, constant-depth layers, and linear or sublinear hidden dimension, they cannot solve fixed membership problems or $(A_{F,r})^*$ closure problems, under the assumption that $\mathsf{TC}^0 \neq \mathsf

---

## d0015 (R-)

**질문** ttention Is All You Need 논문 자세히 설명해줘

[문서 1]
[발행일: 2024-04-15]
[2404.09516v1] State Space Model for New-Generation Network Alternative to Transformers: A Survey
[초록] In the post-deep learning era, the Transformer architecture has demonstrated its powerful performance across pre-trained big models and various downstream tasks. However, the enormous computational demands of this architecture have deterred many researchers. To further reduce the complexity of attention models, numerous efforts have been made to design more efficient methods. Among them, the State Space Model (SSM), as a possible replacement for the self-attention based Transformer model, has drawn more and more attention in recent years. In this paper, we give the first comprehensive review of these works and also provide experimental comparisons and analysis to better demonstrate the features and advantages of SSM. Specifically, we first give a detailed description of principles to help the readers quickly capture the key ideas of SSM. After that, we dive in

[문서 2]
[발행일: 2024-04-15]
[2404.09516v1] State Space Model for New-Generation Network Alternative to Transformers: A Survey
[초록] In the post-deep learning era, the Transformer architecture has demonstrated its powerful performance across pre-trained big models and various downstream tasks. However, the enormous computational demands of this architecture have deterred many researchers. To further reduce the complexity of attention models, numerous efforts have been made to design more efficient methods. Among them, the State Space Model (SSM), as a possible replacement for the self-attention based Transformer model, has drawn more and more attention in recent years. In this paper, we give the first comprehensive review of these works and also provide experimental comparisons and analysis to better demonstrate the features and advantages of SSM. Specifically, we first give a detailed description of principles to help the readers quickly capture the key ideas of SSM. After that, we dive in

---

## d0032 (RL)

**질문** """RAG 검색 정확도 향상(retrieval accuracy), Reranking, Chunking, Hallucination mitigation 관련 최신 논문 찾아줘."""

[문서 1]
[발행일: 2026-03-26]
[2603.25333v1] Adaptive Chunking: Optimizing Chunking-Method Selection for RAG
[초록] The effectiveness of Retrieval-Augmented Generation (RAG) is highly dependent on how documents are chunked, that is, segmented into smaller units for indexing and retrieval. Yet, commonly used "one-size-fits-all" approaches often fail to capture the nuanced structure and semantics of diverse texts. Despite its central role, chunking lacks a dedicated evaluation framework, making it difficult to assess and compare strategies independently of downstream performance. We challenge this paradigm by introducing Adaptive Chunking, a framework that selects the most suitable chunking strategy for each document based on a set of five novel intrinsic, document-based metrics: References Completeness (RC), Intrachunk Cohesion (ICC), Document Contextual Coherence (DCC), Block Integrity (BI), and Size Compliance (SC), which directly assess chunking quality across key dimensions. To support thi

[문서 2]
[발행일: 2025-11-08]
[2601.05265v1] Cross-Document Topic-Aligned Chunking for Retrieval-Augmented Generation
[초록] Chunking quality determines RAG system performance. Current methods partition documents individually, but complex queries need information scattered across multiple sources: the knowledge fragmentation problem. We introduce Cross-Document Topic-Aligned (CDTA) chunking, which reconstructs knowledge at the corpus level. It first identifies topics across documents, maps segments to each topic, and synthesizes them into unified chunks. On HotpotQA multi-hop reasoning, our method reached 0.93 faithfulness versus 0.83 for contextual retrieval and 0.78 for semantic chunking, a 12% improvement over current industry best practice (p < 0.05). On UAE Legal texts, it reached 0.94 faithfulness with 0.93 citation accuracy. At k = 3, it maintains 0.91 faithfulness while semantic methods drop to 0.68, with a single CDTA chunk containing information requiring multiple traditional fragme

[문서 3]
[발행일: 2026-02-19]
[2602.16974v1] Beyond Chunk-Then-Embed: A Comprehensive Taxonomy and Evaluation of Document Chunking Strategies for Information Retrieval
[초록] Document chunking is a critical preprocessing step in dense retrieval systems, yet the design space of chunking strategies remains poorly understood. Recent research has proposed several concurrent approaches, including LLM-guided methods (e.g., DenseX and LumberChunker) and contextualized strategies(e.g., Late Chunking), which generate embeddings before segmentation to preserve contextual information. However, these methods emerged independently and were evaluated on benchmarks with minimal overlap, making direct comparisons difficult. This paper reproduces prior studies in document chunking and presents a systematic framework that unifies existing strategies along two key dimensions: (1) segmentation methods, including structure-based methods (fixed-size, sentence-based, and paragraph-based) as well as semantically-inf

[문서 4]
[발행일: 2023-11-09]
[2311.05232v2] A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions
[초록] The emergence of large language models (LLMs) has marked a significant breakthrough in natural language processing (NLP), fueling a paradigm shift in information acquisition. Nevertheless, LLMs are prone to hallucination, generating plausible yet nonfactual content. This phenomenon raises significant concerns over the reliability of LLMs in real-world information retrieval (IR) systems and has attracted intensive research to detect and mitigate such hallucinations. Given the open-ended general-purpose attributes inherent to LLMs, LLM hallucinations present distinct challenges that diverge from prior task-specific models. This divergence highlights the urgency for a nuanced understanding and comprehensive overview of recent advances in LLM hallucinations. In this survey, we begin with an innovative taxonomy of hallucination in the era of L

[문서 5]
[발행일: 2024-01-02]
[2401.01313v3] A Comprehensive Survey of Hallucination Mitigation Techniques in Large Language Models
[초록] As Large Language Models (LLMs) continue to advance in their ability to write human-like text, a key challenge remains around their tendency to hallucinate generating content that appears factual but is ungrounded. This issue of hallucination is arguably the biggest hindrance to safely deploying these powerful LLMs into real-world production systems that impact people's lives. The journey toward widespread adoption of LLMs in practical settings heavily relies on addressing and mitigating hallucinations. Unlike traditional AI systems focused on limited tasks, LLMs have been exposed to vast amounts of online text data during training. While this allows them to display impressive language fluency, it also means they are capable of extrapolating information from the biases in training data, misinterpreting ambiguous prompts, or modifying the information to ali

---

## d0038 (RL)

**질문** 논문 재밌는것좀 요약해줘

[문서 1]
[발행일: 2024-06-28]
[2407.12026v1] The Pitfalls of Publishing in the Age of LLMs: Strange and Surprising Adventures with a High-Impact NLP Journal
[초록] We show the fraught side of the academic publishing realm and illustrate it through a recent case study with an NLP journal.

. Overall, the paper’s literature review appears to be thorough, covering a wide range of relevant sources. However, the assessment of whether any “significant” work is ignored can be subjective, as it depends on the specific criteria for significance and the scope of the paper. We may have varying opinions on whether certain works should have been included, but the paper generally provides a solid foundation in terms of referencing relevant literature.

---

[문서 2]
[발행일: 2024-12-18]
[2412.13612v5] Large Language Models for Automated Literature Review: An Evaluation of Reference Generation, Abstract Writing, and Review Composition
[초록] Large language models (LLMs) have emerged as a potential solution to automate the complex processes involved in writing literature reviews, such as literature collection, organization, and summarization. However, it is yet unclear how good LLMs are at automating comprehensive and reliable literature reviews. This study introduces a framework to automatically evaluate the performance of LLMs in three key tasks of literature writing: reference generation, literature summary, and literature review composition. We introduce multidimensional evaluation metrics that assess the hallucination rates in generated references and measure the semantic coverage and factual consistency of the literature summaries and compositions against human-written counterparts. The experimental results reveal that even the most advanced

[문서 3]
[발행일: 2024-07-30]
[2407.20906v5] Automated Review Generation Method Based on Large Language Models
[초록] Literature research, vital for scientific work, faces the challenge of surging information volumes exceeding researchers' processing capabilities. We present an automated review generation method based on large language models (LLMs) to overcome efficiency bottlenecks and reduce cognitive load. Our statistically validated evaluation framework demonstrates that the generated reviews match or exceed manual quality, offering broad applicability across research fields without requiring users' domain knowledge. Applied to propane dehydrogenation (PDH) catalysts, our method swiftly analyzed 343 articles, averaging seconds per article per LLM account, producing comprehensive reviews spanning 35 topics, with extended analysis of 1041 articles providing insights into catalysts' properties. Through multi-layered quality control, we effectively mitigated LLMs' hallucinations, with expert

[문서 4]
[발행일: 2024-06-30]
[2407.00747v1] A Comparative Study of Quality Evaluation Methods for Text Summarization
[초록] Evaluating text summarization has been a challenging task in natural language processing (NLP). Automatic metrics which heavily rely on reference summaries are not suitable in many situations, while human evaluation is time-consuming and labor-intensive. To bridge this gap, this paper proposes a novel method based on large language models (LLMs) for evaluating text summarization. We also conducts a comparative study on eight automatic metrics, human evaluation, and our proposed LLM-based method. Seven different types of state-of-the-art (SOTA) summarization models were evaluated. We perform extensive experiments and analysis on datasets with patent documents. Our results show that LLMs evaluation aligns closely with human evaluation, while widely-used automatic metrics such as ROUGE-2, BERTScore, and SummaC do not and also lack consistency. Based on the empirical compar

[문서 5]
[발행일: 2025-11-07]
[2601.05264v1] Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems
[초록] This article provides a comprehensive systematic literature review of academic studies, industrial applications, and real-world deployments from 2018 to 2025, providing a practical guide and detailed overview of modern Retrieval-Augmented Generation (RAG) architectures. RAG offers a modular approach for integrating external knowledge without increasing the capacity of the model as LLM systems expand. Research and engineering practices have been fragmented as a result of the increasing diversity of RAG methodologies, which encompasses a variety of fusion mechanisms, retrieval strategies, and orchestration approaches. We provide quantitative assessment frameworks, analyze the implications for trust and alignment, and systematically consolidate existing RAG techniques into a unified taxonomy. This document is a p

---

## d0065 (RL)

**질문** 예를들어 RAG검색을 했을시에, 두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘

[문서 1]
[발행일: 2024-05-31]
[2406.04369v1] RAG Does Not Work for Enterprises
[초록] Retrieval-Augmented Generation (RAG) improves the accuracy and relevance of large language model outputs by incorporating knowledge retrieval. However, implementing RAG in enterprises poses challenges around data security, accuracy, scalability, and integration. This paper explores the unique requirements for enterprise RAG, surveys current approaches and limitations, and discusses potential advances in semantic search, hybrid queries, and optimized retrieval. It proposes an evaluation framework to validate enterprise RAG solutions, including quantitative testing, qualitative analysis, ablation studies, and industry case studies. This framework aims to help demonstrate the ability of purpose-built RAG architectures to deliver accuracy and relevance improvements with enterprise-grade security, compliance and integration. The paper concludes with implications for enterprise deployments, limitations, and future

[문서 2]
[발행일: 2026-04-14]
[2604.14220v1] Knowledge Graph RAG: Agentic Crawling and Graph Construction in Enterprise Documents
[초록] This research paper addresses the limitations of semantic search in complex enterprise document ecosystems. Traditional RAG pipelines often fail to capture hierarchical and interconnected information, leading to retrieval inaccuracies. We propose Agentic Knowledge Graphs featuring Recursive Crawling as a robust solution for navigating superseding logic and multi-hop references. Our benchmark evaluation using the Code of Federal Regulations (CFR) demonstrates that this Knowledge Graph-enhanced approach achieves a 70% accuracy improvement over standard vector-based RAG systems, providing exhaustive and precise answers for complex regulatory queries.

## **2.1 Limitations of Standard Vector RAG**  
Traditional RAG systems, which rely solely on vector-based retrieval (such as those using **Cosine Similarity** ), treat documents as an amorphous collection of text

[문서 3]
[발행일: 2026-03-23]
[2603.22633v1] Graph-Aware Late Chunking for Retrieval-Augmented Generation in Biomedical Literature
[초록] Retrieval-Augmented Generation (RAG) systems for biomedical literature are typically evaluated using ranking metrics like Mean Reciprocal Rank (MRR), which measure how well the system identifies the single most relevant chunk. We argue that for full-text scientific documents, this paradigm is incomplete: it rewards retrieval precision while ignoring retrieval breadth -- the ability to surface evidence from across a document's structural sections. We propose GraLC-RAG, a framework that unifies late chunking with graph-aware structural intelligence, introducing structure-aware chunk boundary detection, UMLS knowledge graph infusion, and graph-guided hybrid retrieval. We evaluate six strategies on 2,359 IMRaD-filtered PubMed Central articles using 2,033 cross-section questions and two metric families: standard ranking metrics (MRR, Recall@k) and structural cov

[문서 4]
[발행일: 2023-12-18]
[2312.10997v5] Retrieval-Augmented Generation for Large Language Models: A Survey
[초록] Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes. Retrieval-Augmented Generation (RAG) has emerged as a promising solution by incorporating knowledge from external databases. This enhances the accuracy and credibility of the generation, particularly for knowledge-intensive tasks, and allows for continuous knowledge updates and integration of domain-specific information. RAG synergistically merges LLMs' intrinsic knowledge with the vast, dynamic repositories of external databases. This comprehensive review paper offers a detailed examination of the progression of RAG paradigms, encompassing the Naive RAG, the Advanced RAG, and the Modular RAG. It meticulously scrutinizes the tripartite foundation of RAG frameworks, which includes the retrieval, the

[문서 5]
[발행일: 2025-08-01]
[2508.05666v1] HySemRAG: A Hybrid Semantic Retrieval-Augmented Generation Framework for Automated Literature Synthesis and Methodological Gap Analysis
[초록] We present HySemRAG, a framework that combines Extract, Transform, Load (ETL) pipelines with Retrieval-Augmented Generation (RAG) to automate large-scale literature synthesis and identify methodological research gaps. The system addresses limitations in existing RAG architectures through a multi-layered approach: hybrid retrieval combining semantic search, keyword filtering, and knowledge graph traversal; an agentic self-correction framework with iterative quality assurance; and post-hoc citation verification ensuring complete traceability. Our implementation processes scholarly literature through eight integrated stages: multi-source metadata acquisition, asynchronous PDF retrieval, custom document layout analysis using modified Docling architecture, bibliographic management, LLM-based field extraction, top

---

## d0066 (RL)

**질문** RAG검색을 했을시에, 두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘

[문서 1]
[발행일: 2024-06-19]
[2406.13213v2] Multi-Meta-RAG: Improving RAG for Multi-Hop Queries using Database Filtering with LLM-Extracted Metadata
[초록] The retrieval-augmented generation (RAG) enables retrieval of relevant information from an external knowledge source and allows large language models (LLMs) to answer queries over previously unseen document collections. However, it was demonstrated that traditional RAG applications perform poorly in answering multi-hop questions, which require retrieving and reasoning over multiple elements of supporting evidence. We introduce a new method called Multi-Meta-RAG, which uses database filtering with LLM-extracted metadata to improve the RAG selection of the relevant documents from various sources, relevant to the question. While database filtering is specific to a set of questions from a particular domain and format, we found out that Multi-Meta-RAG greatly improves the results on the MultiHop-RAG benchmark. The code is available at https://

[문서 2]
[발행일: 2026-02-07]
[2602.07297v1] Progressive Searching for Retrieval in RAG
[초록] Retrieval Augmented Generation (RAG) is a promising technique for mitigating two key limitations of large language models (LLMs): outdated information and hallucinations. RAG system stores documents as embedding vectors in a database. Given a query, search is executed to find the most related documents. Then, the topmost matching documents are inserted into LLMs' prompt to generate a response. Efficient and accurate searching is critical for RAG to get relevant information. We propose a cost-effective searching algorithm for retrieval process. Our progressive searching algorithm incrementally refines the candidate set through a hierarchy of searches, starting from low-dimensional embeddings and progressing into a higher, target-dimensionality. This multi-stage approach reduces retrieval time while preserving the desired accuracy. Our findings demonstrate that progressive search in RAG systems achiev

[문서 3]
[발행일: 2026-02-25]
[2602.21553v1] Revisiting RAG Retrievers: An Information Theoretic Benchmark
[초록] Retrieval-Augmented Generation (RAG) systems rely critically on the retriever module to surface relevant context for large language models. Although numerous retrievers have recently been proposed, each built on different ranking principles such as lexical matching, dense embeddings, or graph citations, there remains a lack of systematic understanding of how these mechanisms differ and overlap. Existing benchmarks primarily compare entire RAG pipelines or introduce new datasets, providing little guidance on selecting or combining retrievers themselves. Those that do compare retrievers directly use a limited set of evaluation tools which fail to capture complementary and overlapping strengths. This work presents MIGRASCOPE, a Mutual Information based RAG Retriever Analysis Scope. We revisit state-of-the-art retrievers and introduce principled metrics grounded in information and sta

[문서 4]
[발행일: 2026-01-07]
[2601.03748v1] Bridging OLAP and RAG: A Multidimensional Approach to the Design of Corpus Partitioning
[초록] Retrieval-Augmented Generation (RAG) systems are increasingly deployed on large-scale document collections, often comprising millions of documents and tens of millions of text chunks. In industrial-scale retrieval platforms, scalability is typically addressed through horizontal sharding and a combination of Approximate Nearest-Neighbor search, hybrid indexing, and optimized metadata filtering. Although effective from an efficiency perspective, these mechanisms rely on bottom-up, similarity-driven organization and lack a conceptual rationale for corpus partitioning. In this paper, we claim that the design of large-scale RAG systems may benefit from the combination of two orthogonal strategies: semantic clustering, which optimizes locality in embedding space, and multidimensional partitioning, which governs where retrieval should occur based on conceptual d

[문서 5]
[발행일: 2026-07-09]
[2607.08382v1] H3D: Benchmarking Unsupervised Text Hashing for Fine-Grained Document Deduplication
[초록] Document hashing provides compact representations for efficient similarity search and document deduplication, but existing studies rarely compare hashing pipelines under a unified protocol for fine-grained scientific documents. H3D is an unsupervised text hashing benchmark for fine-grained document deduplication. It evaluates representative unsupervised non-learning hashing approaches (MinHash, SimHash, Winnowing, FuzzyHash, FlyHash) together with semantic-sensitive methods built from frozen BGE embeddings and two quantization strategies (BGE-BIHash and BGE-LSHash). The non-learning methods generate hash fingerprints through manually designed mathematical rules without training or labeled similarity pairs, which distinguishes them from neural semantic hashing models. We benchmark all methods on CSFCube and RELISH, two datasets that provide complementary evalu

---

## d0732 (N)

**질문** 합성 데이터로만 계속 학습하면 모델이 붕괴한다던데, 몇 세대 만에 무너지는지 보인 논문 찾아줘

[문서 1]
[발행일: 2024-12-19]
[2412.14689v3] How to Synthesize Text Data without Model Collapse?
[초록] Model collapse in synthetic data indicates that iterative training on self-generated data leads to a gradual decline in performance. With the proliferation of AI models, synthetic data will fundamentally reshape the web data ecosystem. Future GPT-$\{n\}$ models will inevitably be trained on a blend of synthetic and human-produced data. In this paper, we focus on two questions: what is the impact of synthetic data on language model training, and how to synthesize data without model collapse? We first pre-train language models across different proportions of synthetic data, revealing a negative correlation between the proportion of synthetic data and model performance. We further conduct statistical analysis on synthetic data to uncover distributional shift phenomenon and over-concentration of n-gram features. Inspired by the above findings, we propose token editing on human-produced data to 

---

## Q_G02 (N)

**질문** FlashAttention은 기존 어텐션보다 메모리를 얼마만큼 아꼈어?

[문서 1]
[발행일: 2023-10-05]
[2310.03294v2] DISTFLASHATTN: Distributed Memory-efficient Attention for Long-context LLMs Training
[초록] FlashAttention (Dao, 2023) effectively reduces the quadratic peak memory usage to linear in training transformer-based large language models (LLMs) on a single GPU. In this paper, we introduce DISTFLASHATTN, a distributed memory-efficient attention mechanism optimized for long-context LLMs training. We propose three key techniques: token-level workload balancing, overlapping key-value communication, and a rematerialization-aware gradient checkpointing algorithm. We evaluate DISTFLASHATTN on Llama-7B and variants with sequence lengths from 32K to 512K. DISTFLASHATTN achieves 8x longer sequences, 4.45 - 5.64x speedup compared to Ring Self-Attention, 2 - 8x longer sequences, 1.24 - 2.01x speedup compared to Megatron-LM with FlashAttention. It achieves 1.67x and 1.26 - 1.88x speedup compared to recent Ring Attention and DeepSpeed-Ulysses. Code is available at ht

---

## Q_G03 (N)

**질문** Chinchilla 논문에서 권장한 토큰 대 파라미터 비율이 얼마야?

[문서 1]
[발행일: 2020-01-23]
[2001.08361v1] Scaling Laws for Neural Language Models
[초록] We study empirical scaling laws for language model performance on the cross-entropy loss. The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude. Other architectural details such as network width or depth have minimal effects within a wide range. Simple equations govern the dependence of overfitting on model/dataset size and the dependence of training speed on model size. These relationships allow us to determine the optimal allocation of a fixed compute budget. Larger models are significantly more sample-efficient, such that optimally compute-efficient training involves training very large models on a relatively modest amount of data and stopping significantly before convergence.

Throughout we will observe precise power-law scalings for performance as a function of training time, context 

[문서 2]
[발행일: 2024-06-27]
[2406.18922v2] Time Matters: Scaling Laws for Any Budget
[초록] A primary cost driver for training large models is wall-clock training time. We show that popular time estimates based on FLOPs are poor estimates, and construct a more accurate proxy based on memory copies. This allows us to accurately estimate the training speed of a transformer model from its hyperparameters. Combined with a scaling law curve like Chinchilla, this allows us to accurately predict the final loss of a model from a simple equation. We show that this expression is accurate across a wide range of model hyperparameter values, enabling us to analytically make architectural decisions and train models more efficiently. Crucially, this analysis predicts that in contrast to existing literature, models should be wider rather than deeper, as the benefits of speed outweigh the benefits of depth.

Preprint. Under review.  
predicting their final loss using our refined scaling law. This is the sam

[문서 3]
[발행일: 2022-03-29]
[2203.15556v1] Training Compute-Optimal Large Language Models
[초록] We investigate the optimal model size and number of tokens for training a transformer language model under a given compute budget. We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models whilst keeping the amount of training data constant. By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and the number of training tokens should be scaled equally: for every doubling of model size the number of training tokens should also be doubled. We test this hypothesis by training a predicted compute-optimal model, Chinchilla, that uses the same compute budget as Gopher but with 70B parameters and 4$\times$ more more data. Chinchilla uniformly and significantly outperforms Gopher (280B), GPT-3 (175B), Jur

---

## Q_H01 (C)

**질문** ColBERT랑 SPLADE 중에 뭘 쓰는 게 나아?

[문서 1]
[발행일: 2020-04-27]
[2004.12832v2] ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT
[초록] Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction

[문서 2]
[발행일: 2026-03-26]
[2603.25248v1] ColBERT-Att: Late-Interaction Meets Attention for Enhanced Retrieval
[초록] Vector embeddings from pre-trained language models form a core component in Neural Information Retrieval systems across a multitude of knowledge extraction tasks. The paradigm of late interaction, introduced in ColBERT, demonstrates high accuracy along with runtime efficiency. However, the current formulation fails to take into account the attention weights of query and document terms, which intuitively capture the "importance" of similarities between them, that might lead to a better understanding of relevance between the queries and documents. This work proposes ColBERT-Att, to explicitly integrate attention mechanism into the late interaction framework for enhanced retrieval performance. Empirical evaluation of ColBERT-Att depicts improvements in recall accuracy on MS-MARCO as well as on a wide range of BEIR and LoTTE benchmark datasets.

- Keshav Santhanam, Omar Khattab

[문서 3]
[발행일: 2026-04-15]
[2604.13728v1] Hybrid Retrieval for COVID-19 Literature: Comparing Rank Fusion and Projection Fusion with Diversity Reranking
[초록] We present a hybrid retrieval system for COVID-19 scientific literature, evaluated on the TREC-COVID benchmark (171,332 papers, 50 expert queries). The system implements six retrieval configurations spanning sparse (SPLADE), dense (BGE), rank-level fusion (RRF), and a projection-based vector fusion (B5) approach. RRF fusion achieves the best relevance (nDCG@10 = 0.828), outperforming dense-only by 6.1% and sparse-only by 14.9%. Our projection fusion variant reaches nDCG@10 = 0.678 on expert queries while being 33% faster (847 ms vs. 1271 ms) and producing 2.2x higher ILD@10 than RRF. Evaluation across 400 queries -- including expert, machine-generated, and three paraphrase styles -- shows that B5 delivers the largest relative gain on keyword-heavy reformulations (+8.8%), although RRF remains best in absolute nDCG@10. On expert queri

[문서 4]
[발행일: 2025-09-29]
[2509.25085v4] jina-reranker-v3: Last but Not Late Interaction for Listwise Document Reranking
[초록] jina-reranker-v3 is a 0.6B-parameter multilingual listwise reranker that introduces a novel "last but not late" interaction. Unlike late interaction models like ColBERT that encode documents separately before multi-vector matching, our approach applies causal attention between the query and all candidate documents in the same context window, enabling rich interactions before extracting contextual embeddings from each document's final token. The new model achieves state-of-the-art BEIR performance with 61.94 nDCG@10 while being significantly smaller than other models with comparable performance.

- Omar Khattab and Matei Zaharia. ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. In _Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval_ , pages 39–48, 2020. doi: 

[문서 5]
[발행일: 2021-07-12]
[2107.05720v1] SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking
[초록] In neural Information Retrieval, ongoing research is directed towards improving the first retriever in ranking pipelines. Learning dense embeddings to conduct retrieval using efficient approximate nearest neighbors methods has proven to work well. Meanwhile, there has been a growing interest in learning sparse representations for documents and queries, that could inherit from the desirable properties of bag-of-words models such as the exact matching of terms and the efficiency of inverted indexes. In this work, we present a new first-stage ranker based on explicit sparsity regularization and a log-saturation effect on term weights, leading to highly sparse representations and competitive results with respect to state-of-the-art dense and sparse methods. Our approach is simple, trained end-to-end in a single stage. We also explore the trade-off between effectiveness and effici

---

## Q_H04 (C)

**질문** HyDE랑 쿼리 재작성 방식은 언제 각각 쓰면 좋아?

[문서 1]
[발행일: 2024-11-20]
[2411.13154v1] DMQR-RAG: Diverse Multi-Query Rewriting for RAG
[초록] Large language models often encounter challenges with static knowledge and hallucinations, which undermine their reliability. Retrieval-augmented generation (RAG) mitigates these issues by incorporating external information. However, user queries frequently contain noise and intent deviations, necessitating query rewriting to improve the relevance of retrieved documents. In this paper, we introduce DMQR-RAG, a Diverse Multi-Query Rewriting framework designed to improve the performance of both document retrieval and final responses in RAG. Specifically, we investigate how queries with varying information quantities can retrieve a diverse array of documents, presenting four rewriting strategies that operate at different levels of information to enhance the performance of baseline approaches. Additionally, we propose an adaptive strategy selection method that minimizes the number of rewrites while

[문서 2]
[발행일: 2023-10-15]
[2310.09716v2] Enhancing Conversational Search: Large Language Model-Aided Informative Query Rewriting
[초록] Query rewriting plays a vital role in enhancing conversational search by transforming context-dependent user queries into standalone forms. Existing approaches primarily leverage human-rewritten queries as labels to train query rewriting models. However, human rewrites may lack sufficient information for optimal retrieval performance. To overcome this limitation, we propose utilizing large language models (LLMs) as query rewriters, enabling the generation of informative query rewrites through well-designed instructions. We define four essential properties for well-formed rewrites and incorporate all of them into the instruction. In addition, we introduce the role of rewrite editors for LLMs when initial query rewrites are available, forming a "rewrite-then-edit" process. Furthermore, we propose distilling the rewriting capabilities of LLMs into smaller mo

[문서 3]
[발행일: 2023-05-23]
[2305.14283v3] Query Rewriting for Retrieval-Augmented Large Language Models
[초록] Large Language Models (LLMs) play powerful, black-box readers in the retrieve-then-read pipeline, making remarkable progress in knowledge-intensive tasks. This work introduces a new framework, Rewrite-Retrieve-Read instead of the previous retrieve-then-read for the retrieval-augmented LLMs from the perspective of the query rewriting. Unlike prior studies focusing on adapting either the retriever or the reader, our approach pays attention to the adaptation of the search query itself, for there is inevitably a gap between the input text and the needed knowledge in retrieval. We first prompt an LLM to generate the query, then use a web search engine to retrieve contexts. Furthermore, to better align the query to the frozen modules, we propose a trainable scheme for our pipeline. A small language model is adopted as a trainable rewriter to cater to the black-box LLM reader. The rewrit

[문서 4]
[발행일: 2024-11-13]
[2411.08438v1] Towards Optimizing a Retrieval Augmented Generation using Large Language Model on Academic Data
[초록] Given the growing trend of many organizations integrating Retrieval Augmented Generation (RAG) into their operations, we assess RAG on domain-specific data and test state-of-the-art models across various optimization techniques. We incorporate four optimizations; Multi-Query, Child-Parent-Retriever, Ensemble Retriever, and In-Context-Learning, to enhance the functionality and performance in the academic domain. We focus on data retrieval, specifically targeting various study programs at a large technical university. We additionally introduce a novel evaluation approach, the RAG Confusion Matrix designed to assess the effectiveness of various configurations within the RAG framework. By exploring the integration of both open-source (e.g., Llama2, Mistral) and closed-source (GPT-3.5 and GPT-4) Large Language Models, we offer valuable insights into th

---

## Q_B06 (L)

**질문** 논문 검색 봇의 답이 길고 장황하다는 피드백을 받았다. 답변 길이와 사용자 만족도의 관계를 다룬 연구, 그리고 RAG 답변을 간결하게 만드는 방법 연구를 몇 편 추천해줘.

[문서 1]
[발행일: 2024-05-13]
[2405.08120v1] From Questions to Insightful Answers: Building an Informed Chatbot for University Resources
[초록] This paper presents BARKPLUG V.2, a Large Language Model (LLM)-based chatbot system built using Retrieval Augmented Generation (RAG) pipelines to enhance the user experience and access to information within academic settings.The objective of BARKPLUG V.2 is to provide information to users about various campus resources, including academic departments, programs, campus facilities, and student resources at a university setting in an interactive fashion. Our system leverages university data as an external data corpus and ingests it into our RAG pipelines for domain-specific question-answering tasks. We evaluate the effectiveness of our system in generating accurate and pertinent responses for Mississippi State University, as a case study, using quantitative measures, employing frameworks such as Retrieval Augmented Generation Assessment(RAGAS). Furthermo

[문서 2]
[발행일: 2025-09-30]
[2509.26205v1] Human-Centered Evaluation of RAG outputs: a framework and questionnaire for human-AI collaboration
[초록] Retrieval-augmented generation (RAG) systems are increasingly deployed in user-facing applications, yet systematic, human-centered evaluation of their outputs remains underexplored. Building on Gienapp's utility-dimension framework, we designed a human-centred questionnaire that assesses RAG outputs across 12 dimensions. We iteratively refined the questionnaire through several rounds of ratings on a set of query-output pairs and semantic discussions. Ultimately, we incorporated feedback from both a human rater and a human-LLM pair. Results indicate that while large language models (LLMs) reliably focus on metric descriptions and scale labels, they exhibit weaknesses in detecting textual format variations. Humans struggled to focus strictly on metric descriptions and labels. LLM ratings and explanations were viewed as a helpful support, but nume

[문서 3]
[발행일: 2024-12-16]
[2412.12322v1] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems
[초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical results comparing different language models (Llama 3.1 and Qwen 2.5) across various retrieval configurations. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. The results also highlight the importance of prompt engineering in RAG systems, with our custom-prompte

[문서 4]
[발행일: 2024-05-13]
[2405.07437v2] Evaluation of Retrieval-Augmented Generation: A Survey
[초록] Retrieval-Augmented Generation (RAG) has recently gained traction in natural language processing. Numerous studies and real-world applications are leveraging its ability to enhance generative models through external information retrieval. Evaluating these RAG systems, however, poses unique challenges due to their hybrid structure and reliance on dynamic knowledge sources. To better understand these challenges, we conduct A Unified Evaluation Process of RAG (Auepora) and aim to provide a comprehensive overview of the evaluation and benchmarks of RAG systems. Specifically, we examine and compare several quantifiable metrics of the Retrieval and Generation components, such as relevance, accuracy, and faithfulness, within the current RAG benchmarks, encompassing the possible output and ground truth pairs. We then analyze the various datasets and metrics, discuss the limitations of current be

[문서 5]
[발행일: 2026-03-09]
[2603.08819v2] Beyond Relevance: On the Relationship Between Retrieval and RAG Information Coverage
[초록] Retrieval-augmented generation (RAG) systems combine document retrieval with a generative model to address complex information seeking tasks like report generation. While the relationship between retrieval quality and generation effectiveness seems intuitive, it has not been systematically studied. We investigate whether upstream retrieval metrics can serve as reliable early indicators of the final generated response's information coverage. Through experiments across two text RAG benchmarks (TREC NeuCLIR 2024 and TREC RAG 2024) and one multimodal benchmark (WikiVideo), we analyze 15 text retrieval stacks and 10 multimodal retrieval stacks across four RAG pipelines and multiple evaluation frameworks (Auto-ARGUE and MiRAGE). Our findings demonstrate strong correlations between coverage-based retrieval metrics and nugget coverage in generated responses at both 

---

## Q_F03 (L)

**질문** LLM 안전성 쪽에서 꼭 읽어야 할 논문 세 편만 뽑아줘

[문서 1]
[발행일: 2024-12-31]
[2501.00517v1] A Method for Enhancing the Safety of Large Model Generation Based on Multi-dimensional Attack and Defense
[초록] Currently, large models are prone to generating harmful content when faced with complex attack instructions, significantly reducing their defensive capabilities. To address this issue, this paper proposes a method based on constructing data aligned with multi-dimensional attack defense to enhance the generative security of large models. The core of our method lies in improving the effectiveness of safe alignment learning for large models by innova-tively increasing the diversity of attack instruction dimensions and the accuracy of generat-ing safe responses. To validate the effectiveness of our method, beyond existing security evaluation benchmarks, we additionally designed new security evaluation benchmarks and conducted comparative experiments using Llama3.2 as the baseline model. The final ex-perimental results demonstrate that our me

[문서 2]
[발행일: 2024-12-18]
[2412.13705v1] Mitigating Adversarial Attacks in LLMs through Defensive Suffix Generation
[초록] Large language models (LLMs) have exhibited outstanding performance in natural language processing tasks. However, these models remain susceptible to adversarial attacks in which slight input perturbations can lead to harmful or misleading outputs. A gradient-based defensive suffix generation algorithm is designed to bolster the robustness of LLMs. By appending carefully optimized defensive suffixes to input prompts, the algorithm mitigates adversarial influences while preserving the models' utility. To enhance adversarial understanding, a novel total loss function ($L_{\text{total}}$) combining defensive loss ($L_{\text{def}}$) and adversarial loss ($L_{\text{adv}}$) generates defensive suffixes more effectively. Experimental evaluations conducted on open-source LLMs such as Gemma-7B, mistral-7B, Llama2-7B, and Llama2-13B show that the proposed method reduces attack 

[문서 3]
[발행일: 2024-12-23]
[2412.17614v1] Emerging Security Challenges of Large Language Models
[초록] Large language models (LLMs) have achieved record adoption in a short period of time across many different sectors including high importance areas such as education [4] and healthcare [23]. LLMs are open-ended models trained on diverse data without being tailored for specific downstream tasks, enabling broad applicability across various domains. They are commonly used for text generation, but also widely used to assist with code generation [3], and even analysis of security information, as Microsoft Security Copilot demonstrates [18]. Traditional Machine Learning (ML) models are vulnerable to adversarial attacks [9]. So the concerns on the potential security implications of such wide scale adoption of LLMs have led to the creation of this working group on the security of LLMs. During the Dagstuhl seminar on "Network Attack Detection and Defense - AI-Powered Threats and Responses", the wor

[문서 4]
[발행일: 2024-12-29]
[2501.00066v2] On Adversarial Robustness of Language Models in Transfer Learning
[초록] We investigate the adversarial robustness of LLMs in transfer learning scenarios. Through comprehensive experiments on multiple datasets (MBIB Hate Speech, MBIB Political Bias, MBIB Gender Bias) and various model architectures (BERT, RoBERTa, GPT-2, Gemma, Phi), we reveal that transfer learning, while improving standard performance metrics, often leads to increased vulnerability to adversarial attacks. Our findings demonstrate that larger models exhibit greater resilience to this phenomenon, suggesting a complex interplay between model size, architecture, and adaptation methods. Our work highlights the crucial need for considering adversarial robustness in transfer learning scenarios and provides insights into maintaining model security without compromising performance. These findings have significant implications for the development and deployment of LLMs in real-world applic

[문서 5]
[발행일: 2024-12-13]
[2412.10535v1] On Adversarial Robustness and Out-of-Distribution Robustness of Large Language Models
[초록] The increasing reliance on large language models (LLMs) for diverse applications necessitates a thorough understanding of their robustness to adversarial perturbations and out-of-distribution (OOD) inputs. In this study, we investigate the correlation between adversarial robustness and OOD robustness in LLMs, addressing a critical gap in robustness evaluation. By applying methods originally designed to improve one robustness type across both contexts, we analyze their performance on adversarial and out-of-distribution benchmark datasets. The input of the model consists of text samples, with the output prediction evaluated in terms of accuracy, precision, recall, and F1 scores in various natural language inference tasks. Our findings highlight nuanced interactions between adversarial robustness and OOD robustness, with results indicating limited transferabil

---

## Q_F04 (L)

**질문** 요즘 많이 인용되는 검색 증강 생성 논문 추천해줘

[문서 1]
[발행일: 2024-10-03]
[2410.12837v1] A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions
[초록] This paper presents a comprehensive study of Retrieval-Augmented Generation (RAG), tracing its evolution from foundational concepts to the current state of the art. RAG combines retrieval mechanisms with generative language models to enhance the accuracy of outputs, addressing key limitations of LLMs. The study explores the basic architecture of RAG, focusing on how retrieval and generation are integrated to handle knowledge-intensive tasks. A detailed review of the significant technological advancements in RAG is provided, including key innovations in retrieval-augmented language models and applications across various domains such as question-answering, summarization, and knowledge-based tasks. Recent research breakthroughs are discussed, highlighting novel methods for improving retrieval efficiency. Furthermore, the paper exam

[문서 2]
[발행일: 2024-06-11]
[2406.07257v1] Scholarly Question Answering using Large Language Models in the NFDI4DataScience Gateway
[초록] This paper introduces a scholarly Question Answering (QA) system on top of the NFDI4DataScience Gateway, employing a Retrieval Augmented Generation-based (RAG) approach. The NFDI4DS Gateway, as a foundational framework, offers a unified and intuitive interface for querying various scientific databases using federated search. The RAG-based scholarly QA, powered by a Large Language Model (LLM), facilitates dynamic interaction with search results, enhancing filtering capabilities and fostering a conversational engagement with the Gateway search. The effectiveness of both the Gateway and the scholarly QA system is demonstrated through experimental analysis.

12. L´ala, J., O’Donoghue, O., Shtedritski, A., Cox, S., Rodriques, S.G., White, A.D.: Paperqa: Retrieval-augmented generative agent for scientific research. CoRR **abs/2312.07559** (2023). https://doi.o

[문서 3]
[발행일: 2024-12-16]
[2412.12322v1] RAG Playground: A Framework for Systematic Evaluation of Retrieval Strategies and Prompt Engineering in RAG Systems
[초록] We present RAG Playground, an open-source framework for systematic evaluation of Retrieval-Augmented Generation (RAG) systems. The framework implements and compares three retrieval approaches: naive vector search, reranking, and hybrid vector-keyword search, combined with ReAct agents using different prompting strategies. We introduce a comprehensive evaluation framework with novel metrics and provide empirical results comparing different language models (Llama 3.1 and Qwen 2.5) across various retrieval configurations. Our experiments demonstrate significant performance improvements through hybrid search methods and structured self-evaluation prompting, achieving up to 72.7% pass rate on our multi-metric evaluation framework. The results also highlight the importance of prompt engineering in RAG systems, with our custom-prompte

[문서 4]
[발행일: 2023-12-12]
[2312.07796v1] Harnessing Retrieval-Augmented Generation (RAG) for Uncovering Knowledge Gaps
[초록] The paper presents a methodology for uncovering knowledge gaps on the internet using the Retrieval Augmented Generation (RAG) model. By simulating user search behaviour, the RAG system identifies and addresses gaps in information retrieval systems. The study demonstrates the effectiveness of the RAG system in generating relevant suggestions with a consistent accuracy of 93%. The methodology can be applied in various fields such as scientific discovery, educational enhancement, research development, market analysis, search engine optimisation, and content development. The results highlight the value of identifying and understanding knowledge gaps to guide future endeavours.

In this paper, we employ the Retrieval Augmented Generation (RAG) model to simulate user search behaviour, aiming to identify and address knowledge gaps on the Internet. We posit that uncovering

[문서 5]
[발행일: 2025-05-06]
[2505.03452v3] An Analysis of Hyper-Parameter Optimization Methods for Retrieval Augmented Generation
[초록] Optimizing Retrieval-Augmented Generation (RAG) configurations for specific tasks is a complex and resource-intensive challenge. Motivated by this challenge, frameworks for RAG hyper-parameter optimization (HPO) have recently emerged, yet their effectiveness has not been rigorously benchmarked. To fill this gap, we present a comprehensive study involving five HPO algorithms over five datasets from diverse domains, including a newly curated real-world product documentation dataset. Our study explores the largest RAG HPO search space to date that includes full grid-search evaluations, and uses three evaluation metrics as optimization targets. Analysis of the results shows that RAG HPO can be done efficiently, either greedily or with random search, and that it significantly boosts RAG performance for all datasets. For greedy HPO approaches, we show that optim

---

## d0802 (L)

**질문** LLM 추론 강화학습 논문 6편 알려줘

[문서 1]
[발행일: 2024-03-30]
[2404.00282v3] Survey on Large Language Model-Enhanced Reinforcement Learning: Concept, Taxonomy, and Methods
[초록] With extensive pre-trained knowledge and high-level general capabilities, large language models (LLMs) emerge as a promising avenue to augment reinforcement learning (RL) in aspects such as multi-task learning, sample efficiency, and high-level task planning. In this survey, we provide a comprehensive review of the existing literature in LLM-enhanced RL and summarize its characteristics compared to conventional RL methods, aiming to clarify the research scope and directions for future studies. Utilizing the classical agent-environment interaction paradigm, we propose a structured taxonomy to systematically categorize LLMs' functionalities in RL, including four roles: information processor, reward designer, decision-maker, and generator. For each role, we summarize the methodologies, analyze the specific RL challenges that are mitigated, and provide

[문서 2]
[발행일: 2026-04-30]
[2604.27859v1] Rethinking Agentic Reinforcement Learning In Large Language Models
[초록] Reinforcement Learning (RL) has traditionally focused on training specialized agents to optimize predefined reward functions within narrowly defined environments. However, the advent of powerful Large Language Models (LLMs) and increasingly complex, open-ended tasks has catalyzed a paradigm shift towards agentic paradigms within RL. This emerging framework extends beyond traditional RL by emphasizing the development of autonomous agents capable of goal-setting, long-term planning, dynamic strategy adaptation, and interactive reasoning in uncertain, real-world environments. Unlike conventional approaches that rely heavily on static objectives and episodic interactions, LLM-based Agentic RL incorporates cognitive-like capabilities such as meta-reasoning, self-reflection, and multi-step decision-making directly into the learning loop. In this paper, we provide a deep insight for

[문서 3]
[발행일: 2026-03-31]
[2604.00076v2] Learning to Play Blackjack: A Curriculum Learning Perspective
[초록] Reinforcement Learning (RL) agents often struggle with efficiency and performance in complex environments. We propose a novel framework that uses a Large Language Model (LLM) to dynamically generate a curriculum over available actions, enabling the agent to incorporate each action individually. We apply this framework to the game of Blackjack, where the LLM creates a multi-stage training path that progressively introduces complex actions to a Tabular Q-Learning and a Deep Q-Network (DQN) agent. Our evaluation in a realistic 8-deck simulation over 10 independent runs demonstrates significant performance gains over standard training methods. The curriculum-based approach increases the DQN agent's average win rate from 43.97% to 47.41%, reduces the average bust rate from 32.9% to 28.0%, and accelerates the overall workflow by over 74%, with the agent's full training completing faster

[문서 4]
[발행일: 2024-12-22]
[2412.16878v1] Online Preference-based Reinforcement Learning with Self-augmented Feedback from Large Language Model
[초록] Preference-based reinforcement learning (PbRL) provides a powerful paradigm to avoid meticulous reward engineering by learning rewards based on human preferences. However, real-time human feedback is hard to obtain in online tasks. Most work suppose there is a "scripted teacher" that utilizes privileged predefined reward to provide preference feedback. In this paper, we propose a RL Self-augmented Large Language Model Feedback (RL-SaLLM-F) technique that does not rely on privileged information for online PbRL. RL-SaLLM-F leverages the reflective and discriminative capabilities of LLM to generate self-augmented trajectories and provide preference labels for reward learning. First, we identify an failure issue in LLM-based preference discrimination, specifically "query ambiguity", in online PbRL. Then LLM is employed to provide preference labe

[문서 5]
[발행일: 2025-03-27]
[2503.21683v1] LLM-Gomoku: A Large Language Model-Based System for Strategic Gomoku with Self-Play and Reinforcement Learning
[초록] In recent years, large language models (LLMs) have shown significant advancements in natural language processing (NLP), with strong capa-bilities in generation, comprehension, and rea-soning. These models have found applications in education, intelligent decision-making, and gaming. However, effectively utilizing LLMs for strategic planning and decision-making in the game of Gomoku remains a challenge. This study aims to develop a Gomoku AI system based on LLMs, simulating the human learning process of playing chess. The system is de-signed to understand and apply Gomoku strat-egies and logic to make rational decisions. The research methods include enabling the model to "read the board," "understand the rules," "select strategies," and "evaluate positions," while en-hancing its abilities through self-play and rein-forcement learning

---

## d0463 (-)

**질문** 재무제표 같은 표에서 LLM이 숫자를 정확히 계산하게 하는 프로그램 생성 방법 있어?

[문서 1]
[발행일: 2025-03-16]
[2503.12345v3] General Table Question Answering via Answer-Formula Joint Generation
[초록] Advanced table question answering (TableQA) methods prompt large language models (LLMs) to generate answer text, SQL query, Python code, or custom operation, which impressively improve the complex reasoning problems in the TableQA task. However, these methods lack the versatility to cope with specific question types or table structures. In contrast, the Spreadsheet Formula, the widely used and well-defined operation language for tabular data, has not been thoroughly explored to solve TableQA. In this paper, we first attempt to use the Formula as the executable representation for solving complex reasoning on tables with different structures. Specifically, we construct \texttt{FromulaQA}, a large Formula-annotated TableQA dataset from existing datasets. In addition, we propose \texttt{TabAF}, a general table answering framework to solve multiple types of tasks over multiple t

[문서 2]
[발행일: 2024-02-04]
[2402.05121v3] Large Language Model for Table Processing: A Survey
[초록] Tables, typically two-dimensional and structured to store large amounts of data, are essential in daily activities like database queries, spreadsheet manipulations, web table question answering, and image table information extraction. Automating these table-centric tasks with Large Language Models (LLMs) or Visual Language Models (VLMs) offers significant public benefits, garnering interest from academia and industry. This survey provides a comprehensive overview of table-related tasks, examining both user scenarios and technical aspects. It covers traditional tasks like table question answering as well as emerging fields such as spreadsheet manipulation and table data analysis. We summarize the training techniques for LLMs and VLMs tailored for table processing. Additionally, we discuss prompt engineering, particularly the use of LLM-powered agents, for various table-related tasks. Finally

[문서 3]
[발행일: 2026-05-21]
[2605.22664v1] WorkstreamBench: Evaluating LLM Agents on End-to-End Spreadsheet Tasks in Finance
[초록] LLM agents are increasingly expected to carry out end-to-end workflows, producing complete artifacts from high-level user instructions. To meet enterprise needs, frontier AI labs have developed agents that can construct entire spreadsheets from scratch. This is especially relevant in finance, where core workflows such as financial modeling, forecasting, and scenario analysis are commonly conducted through spreadsheets. Yet, existing spreadsheet benchmarks do not measure this advanced capability, focusing instead on question-answering or single-formula edits. To address this gap, we provide one of the first evaluations of agents on end-to-end spreadsheet tasks, focusing on economically critical financial workflows such as modeling and scenario analysis. Since deliverables therein are routinely reviewed and revised by multiple stakeholders, judging their quality 

---

## d0478 (-)

**질문** RAG 파이프라인 구성 요소를 자동으로 고르는 AutoML 같은 방법 있어?

[문서 1]
[발행일: 2024-03-29]
[2404.00137v1] Budget-aware Query Tuning: An AutoML Perspective
[초록] Modern database systems rely on cost-based query optimizers to come up with good execution plans for input queries. Such query optimizers rely on cost models to estimate the costs of candidate query execution plans. A cost model represents a function from a set of cost units to query execution cost, where each cost unit specifies the unit cost of executing a certain type of query processing operation (such as table scan or join). These cost units are traditionally viewed as constants, whose values only depend on the platform configuration where the database system runs on top of but are invariant for queries processed by the database system. In this paper, we challenge this classic view by thinking of these cost units as variables instead. We show that, by varying the cost-unit values one can obtain query plans that significantly outperform the default query plans returned by the query optimiz

[문서 2]
[발행일: 2025-05-06]
[2505.03452v3] An Analysis of Hyper-Parameter Optimization Methods for Retrieval Augmented Generation
[초록] Optimizing Retrieval-Augmented Generation (RAG) configurations for specific tasks is a complex and resource-intensive challenge. Motivated by this challenge, frameworks for RAG hyper-parameter optimization (HPO) have recently emerged, yet their effectiveness has not been rigorously benchmarked. To fill this gap, we present a comprehensive study involving five HPO algorithms over five datasets from diverse domains, including a newly curated real-world product documentation dataset. Our study explores the largest RAG HPO search space to date that includes full grid-search evaluations, and uses three evaluation metrics as optimization targets. Analysis of the results shows that RAG HPO can be done efficiently, either greedily or with random search, and that it significantly boosts RAG performance for all datasets. For greedy HPO approaches, we show that optim

[문서 3]
[발행일: 2026-02-24]
[2602.20735v1] RMIT-ADM+S at the MMU-RAG NeurIPS 2025 Competition
[초록] This paper presents the award-winning RMIT-ADM+S system for the Text-to-Text track of the NeurIPS~2025 MMU-RAG Competition. We introduce Routing-to-RAG (R2RAG), a research-focused retrieval-augmented generation (RAG) architecture composed of lightweight components that dynamically adapt the retrieval strategy based on inferred query complexity and evidence sufficiency. The system uses smaller LLMs, enabling operation on a single consumer-grade GPU while supporting complex research tasks. It builds on the G-RAG system, winner of the ACM~SIGIR~2025 LiveRAG Challenge, and extends it with modules informed by qualitative review of outputs. R2RAG won the Best Dynamic Evaluation award in the Open Source category, demonstrating high effectiveness with careful design and efficient use of resources.

Our results show that small reasoning-oriented models can effectively support dynamic RAG pipelines un

[문서 4]
[발행일: 2024-12-30]
[2501.00138v1] NiaAutoARM: Automated generation and evaluation of Association Rule Mining pipelines
[초록] The Numerical Association Rule Mining paradigm that includes concurrent dealing with numerical and categorical attributes is beneficial for discovering associations from datasets consisting of both features. The process is not considered as easy since it incorporates several processing steps running sequentially that form an entire pipeline, e.g., preprocessing, algorithm selection, hyper-parameter optimization, and the definition of metrics evaluating the quality of the association rule. In this paper, we proposed a novel Automated Machine Learning method, NiaAutoARM, for constructing the full association rule mining pipelines based on stochastic population-based meta-heuristics automatically. Along with the theoretical representation of the proposed method, we also present a comprehensive experimental evaluation of the proposed method.

To the best knowled

[문서 5]
[발행일: 2025-05-01]
[2505.07833v1] Patchwork: A Unified Framework for RAG Serving
[초록] Retrieval Augmented Generation (RAG) has emerged as a new paradigm for enhancing Large Language Model reliability through integration with external knowledge sources. However, efficient deployment of these systems presents significant technical challenges due to their inherently heterogeneous computational pipelines comprising LLMs, databases, and specialized processing components. We introduce Patchwork, a comprehensive end-to-end RAG serving framework designed to address these efficiency bottlenecks. Patchwork's architecture offers three key innovations: First, it provides a flexible specification interface enabling users to implement custom RAG pipelines. Secondly, it deploys these pipelines as distributed inference systems while optimizing for the unique scalability characteristics of individual RAG components. Third, Patchwork incorporates an online scheduling mechanism that continuously mo

---

## d0491 (-)

**질문** 임베딩 검색 결과를 키워드 일치로 다시 걸러내는 하이브리드 재순위 방법 있어?

[문서 1]
[발행일: 2022-10-21]
[2210.11934v2] An Analysis of Fusion Functions for Hybrid Retrieval
[초록] We study hybrid search in text retrieval where lexical and semantic search are fused together with the intuition that the two are complementary in how they model relevance. In particular, we examine fusion by a convex combination (CC) of lexical and semantic scores, as well as the Reciprocal Rank Fusion (RRF) method, and identify their advantages and potential pitfalls. Contrary to existing studies, we find RRF to be sensitive to its parameters; that the learning of a CC fusion is generally agnostic to the choice of score normalization; that CC outperforms RRF in in-domain and out-of-domain settings; and finally, that CC is sample efficient, requiring only a small set of training examples to tune its only parameter to a target domain.

- [19] Ji Ma, Ivan Korotkov, Keith Hall, and Ryan T. McDonald. 2020. Hybrid First-stage Retrieval Models for Biomedical Literature. In _CLEF_ .  
- [20] Xue

[문서 2]
[발행일: 2026-04-15]
[2604.13728v1] Hybrid Retrieval for COVID-19 Literature: Comparing Rank Fusion and Projection Fusion with Diversity Reranking
[초록] We present a hybrid retrieval system for COVID-19 scientific literature, evaluated on the TREC-COVID benchmark (171,332 papers, 50 expert queries). The system implements six retrieval configurations spanning sparse (SPLADE), dense (BGE), rank-level fusion (RRF), and a projection-based vector fusion (B5) approach. RRF fusion achieves the best relevance (nDCG@10 = 0.828), outperforming dense-only by 6.1% and sparse-only by 14.9%. Our projection fusion variant reaches nDCG@10 = 0.678 on expert queries while being 33% faster (847 ms vs. 1271 ms) and producing 2.2x higher ILD@10 than RRF. Evaluation across 400 queries -- including expert, machine-generated, and three paraphrase styles -- shows that B5 delivers the largest relative gain on keyword-heavy reformulations (+8.8%), although RRF remains best in absolute nDCG@10. On expert queri

---

## d0495 (-)

**질문** LLM 출력이 JSON 같은 정해진 형식을 지키게 하는 구조화 생성 방법 연구 찾아줘

[문서 1]
[발행일: 2024-12-31]
[2501.00539v2] MCP-Solver: Integrating Language Models with Constraint Programming Systems
[초록] The MCP Solver bridges Large Language Models (LLMs) with symbolic solvers through the Model Context Protocol (MCP), an open-source standard for AI system integration. Providing LLMs access to formal solving and reasoning capabilities addresses their key deficiency while leveraging their strengths. Our implementation offers interfaces for constraint programming (Minizinc), propositional satisfiability (PySAT), and SAT modulo Theories (Python Z3). The system employs an editing approach with iterated validation to ensure model consistency during modifications and enable structured refinement.

2  
ation of streamlining constraints to accelerate constraint solving. Finally, LLMS4CP [10] shows how pre-trained LLMs can transform textual problem descriptions into executable Constraint Programming specifications through retrieval-augmented in-context learning.

---

[문서 2]
[발행일: 2026-03-20]
[2603.19957v1] HiPath: Hierarchical Vision-Language Alignment for Structured Pathology Report Prediction
[초록] Pathology reports are structured, multi-granular documents encoding diagnostic conclusions, histological grades, and ancillary test results across one or more anatomical sites; yet existing pathology vision-language models (VLMs) reduce this output to a flat label or free-form text. We present HiPath, a lightweight VLM framework built on frozen UNI2 and Qwen3 backbones that treats structured report prediction as its primary training objective. Three trainable modules totalling 15M parameters address complementary aspects of the problem: a Hierarchical Patch Aggregator (HiPA) for multi-image visual encoding, Hierarchical Contrastive Learning (HiCL) for cross-modal alignment via optimal transport, and Slot-based Masked Diagnosis Prediction (Slot-MDP) for structured diagnosis generation. Trained on 749K real-world Chinese pathology cases from three hospita

[문서 3]
[발행일: 2024-05-03]
[2405.02105v1] Evaluating Large Language Models for Structured Science Summarization in the Open Research Knowledge Graph
[초록] Structured science summaries or research contributions using properties or dimensions beyond traditional keywords enhances science findability. Current methods, such as those used by the Open Research Knowledge Graph (ORKG), involve manually curating properties to describe research papers' contributions in a structured manner, but this is labor-intensive and inconsistent between the domain expert human curators. We propose using Large Language Models (LLMs) to automatically suggest these properties. However, it's essential to assess the readiness of LLMs like GPT-3.5, Llama 2, and Mistral for this task before application. Our study performs a comprehensive comparative analysis between ORKG's manually curated properties and those generated by the aforementioned state-of-the-art LLMs. We evaluate LLM performance through four unique perspe

---

## Q_A12 (-)

**질문** 같은 질문인데 문서 순서만 바꿔도 답이 달라진다. 검색 문서 순서에 대한 민감도를 측정하고 줄이는 방법을 다룬 연구가 있어?

[문서 1]
[발행일: 2026-08-24]
[2608.23419v2] Robustness of IR Models to Collection Growth
[초록] Information Retrieval (IR) systems seek to identify relevant documents within a collection. In practical applications, collections are dynamic, with documents frequently added. We argue that ideally, a retriever's effectiveness should not decrease when non-relevant documents are added to a collection. This study formalises this concept and empirically evaluates it by merging two collections with negligible topic overlap. We hypothesise that the way an IR model conditions its ranking on other documents in a collection (e.g., the IDF component in BM25 or contextual documents in listwise rerankers) plays an important role in its robustness to the addition of non-relevant documents. We broadly classify models as those that do not depend on other documents (Multi-Document-Agnostic, MDA) and those that do (Multi-Document-Dependent, MDD). Our results show that neither MDD nor MDA models are fully robust 

[문서 2]
[발행일: 2024-04-21]
[2404.13781v1] Evaluating Retrieval Quality in Retrieval-Augmented Generation
[초록] Evaluating retrieval-augmented generation (RAG) presents challenges, particularly for retrieval models within these systems. Traditional end-to-end evaluation methods are computationally expensive. Furthermore, evaluation of the retrieval model's performance based on query-document relevance labels shows a small correlation with the RAG system's downstream performance. We propose a novel evaluation approach, eRAG, where each document in the retrieval list is individually utilized by the large language model within the RAG system. The output generated for each document is then evaluated based on the downstream task ground truth labels. In this manner, the downstream performance for each document serves as its relevance label. We employ various downstream task metrics to obtain document-level annotations and aggregate them using set-based or ranking metrics. Extensive experiments o

[문서 3]
[발행일: 2026-07-22]
[2607.19747v2] Beyond Relevance-Centric Retrieval: Rubric-Oriented Document Set Selection and Ranking
[초록] As large language models and AI agents become the primary consumers of search results, document set quality determines the upper bound of downstream generation. Yet existing evaluation systems remain confined to scoring documents independently and aggregating via nDCG, ignoring inter-document interactions (redundancy, conflict, complementarity) and unable to answer what makes one document set better than another. To address these issues, we propose a complete evaluate-diagnose-optimize framework. We design SetwiseEvalKit, a three-level, nine-dimension document set evaluation benchmark covering both short-form and long-form scenarios, comprising approximately 28K high-quality evaluation rubrics. We systematically evaluate 12 rerankers: even the best method achieves no more than 45% coverage, cross-document coordination dimensions are universally weak, and n

[문서 4]
[발행일: 2026-07-31]
[2608.00229v1] Hierarchical BM25: Lexical Search at Billion-Document Scale
[초록] A flat BM25 index over one billion documents occupies about 400 GB. Holding it in memory requires DRAM proportional to corpus size. Serving it from disk takes 4-12 seconds per query. Exact top-k lexical retrieval at this scale is therefore impractical within an interactive latency budget. Hierarchical BM25 gives up exact ranking in exchange for fixed bounds on memory and latency. A resident coarse index selects which of ~1K topical, size-balanced document groups a query visits, using two signals: the total frequency of each query term within a group, and, for informative terms spread too thinly across groups for frequency totals to reflect, whether several of them appear together in one document. Selected groups are then searched exhaustively and scored against ~100 KB of global statistics. Every returned score therefore equals the flat index's score, and the approximation is confin

[문서 5]
[발행일: 2025-05-06]
[2505.03452v3] An Analysis of Hyper-Parameter Optimization Methods for Retrieval Augmented Generation
[초록] Optimizing Retrieval-Augmented Generation (RAG) configurations for specific tasks is a complex and resource-intensive challenge. Motivated by this challenge, frameworks for RAG hyper-parameter optimization (HPO) have recently emerged, yet their effectiveness has not been rigorously benchmarked. To fill this gap, we present a comprehensive study involving five HPO algorithms over five datasets from diverse domains, including a newly curated real-world product documentation dataset. Our study explores the largest RAG HPO search space to date that includes full grid-search evaluations, and uses three evaluation metrics as optimization targets. Analysis of the results shows that RAG HPO can be done efficiently, either greedily or with random search, and that it significantly boosts RAG performance for all datasets. For greedy HPO approaches, we show that optim
