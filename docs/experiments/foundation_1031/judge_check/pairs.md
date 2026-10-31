# 판정자 점검 — 20쌍 (조건 · Claude 판정 모름)

질문마다 논문(제목 + 초록 앞부분)이 질문을 얼마나 직접 다루는지 매겨 주세요.

- **2** = 질문 주제를 직접 다룸
- **1** = 관련은 있지만 비껴감
- **0** = 관련 없음

답은 `1:2 2:0 3:1 …` 처럼 번호:점수로 보내 주세요.

---

### 1
**질문**: 학술 논문 추천 시스템에서 LLM을 쓰는 방법 연구 찾아줘

**논문**: Enhanced Recommendation Combining Collaborative Filtering and Large Language Models

> With the advent of the information explosion era, the importance of recommendation systems in various applications is increasingly significant. Traditional collaborative filtering algorithms are widely used due to their effectiveness in capturing user behavior patterns, but they encounter limitations when dealing with cold start problems and data sparsity. Large Language Models (LLMs), with their strong natural language understanding and generati

---

### 2
**질문**: LLM이 긴 대화를 기억하게 하는 메모리 구조에 대한 연구를 조사해줘

**논문**: Enhancing Long-term RAG Chatbots with Psychological Models of Memory Importance and Forgetting

> Drawing on psychological insights, we propose LUFY, a simple yet effective method that focuses on emotionally arousing memories and retains less than 10% of the conversation. The results demonstrate that prioritizing arousing memories while forgetting the majority of the conversation significantly enhances user experience.

---

### 3
**질문**: 검색 쿼리를 여러 개로 나눠 검색하고 결과를 합치는 방법 연구 찾아줘

**논문**: DMQR-RAG: Diverse Multi-Query Rewriting for RAG

> Large language models often encounter challenges with static knowledge and hallucinations, which undermine their reliability. Retrieval-augmented generation (RAG) mitigates these issues by incorporating external information. However, user queries frequently contain noise and intent deviations, necessitating query rewriting to improve the relevance of retrieved documents. In this paper, we introduce DMQR-RAG, a Diverse Multi-Query Rewriting framew

---

### 4
**질문**: 표나 그래프가 들어 있는 PDF 문서를 RAG로 검색하는 방법 조사해줘

**논문**: Developing Retrieval Augmented Generation (RAG) based LLM Systems from PDFs: An Experience Report

> This paper presents an experience report on the development of Retrieval Augmented Generation (RAG) systems using PDF documents as the primary data source. The RAG architecture combines generative capabilities of Large Language Models (LLMs) with the precision of information retrieval. This approach has the potential to redefine how we interact with and augment both structured and unstructured knowledge in generative models to enhance transparenc

---

### 5
**질문**: 검색 증강 생성에서 질문을 다시 써서 검색을 잘 되게 하는 연구 조사해줘

**논문**: Query Rewriting for Retrieval-Augmented Large Language Models

> Large Language Models (LLMs) play powerful, black-box readers in the retrieve-then-read pipeline, making remarkable progress in knowledge-intensive tasks. This work introduces a new framework, Rewrite-Retrieve-Read instead of the previous retrieve-then-read for the retrieval-augmented LLMs from the perspective of the query rewriting. Unlike prior studies focusing on adapting either the retriever or the reader, our approach pays attention to the a

---

### 6
**질문**: 검색 결과를 LLM으로 다시 순위 매기는 방법에 대해 조사해줘

**논문**: RAGSmith: A Framework for Finding the Optimal Composition of Retrieval-Augmented Generation Methods Across Datasets

> Retrieval-Augmented Generation (RAG) quality depends on many interacting choices across retrieval, ranking, augmentation, prompting, and generation, so optimizing modules in isolation is brittle. We introduce RAGSmith, a modular framework that treats RAG design as an end-to-end architecture search over nine technique families and 46{,}080 feasible pipeline configurations. A genetic search optimizes a scalar objective that jointly aggregates retri

---

### 7
**질문**: 여러 단계 추론이 필요한 질문에서 검색을 반복하는 방법 조사해줘

**논문**: Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG

> However, their reliance on static training data limits their ability to respond to dynamic, real-time queries, resulting in outdated or inaccurate outputs. Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding autonomous AI agents into the RAG pipeline. This paper presents an analytical survey of Agentic RAG systems.

---

### 8
**질문**: LLM 출력이 JSON 같은 정해진 형식을 지키게 하는 구조화 생성 방법 연구 찾아줘

**논문**: CHORUS: Zero-shot Hierarchical Retrieval and Orchestration for Generating Linear Programming Code

> We propose CHORUS, a retrieval-augmented generation (RAG) framework for synthesizing Gurobi-based LP code from natural language problem statements. Experiments on the NL4Opt-Code benchmark show that CHORUS improves the performance of open-source LLMs such as Llama3.1 (8B), Llama3.3 (70B), Phi4 (14B), Deepseek-r1 (32B), and Qwen2.5-coder (32B) by a significant margin compared to baseline and conv…

---

### 9
**질문**: 검색 증강 생성에서 질문을 다시 써서 검색을 잘 되게 하는 연구 조사해줘

**논문**: Retrieval-Augmented Generation Systems for Intellectual Property via Synthetic Multi-Angle Fine-tuning

> Retrieval-Augmented Generation (RAG) systems in the Intellectual Property (IP) field often struggle with diverse user queries, including colloquial expressions, spelling errors, and ambiguous terminology, leading to inaccurate retrieval and suboptimal responses. To address this challenge, we propose Multi-Angle Question Generation and Retrieval Fine-Tuning Method (MQG-RFM), a novel framework that leverages large language models (LLMs) to simulate

---

### 10
**질문**: 검색 쿼리를 여러 개로 나눠 검색하고 결과를 합치는 방법 연구 찾아줘

**논문**: Blended RAG: Improving RAG (Retriever-Augmented Generation) Accuracy with Semantic Search and Hybrid Query-Based Retrievers

> Retrieval-Augmented Generation (RAG) is a prevalent approach to infuse a private knowledge base of documents with Large Language Models (LLM) to build Generative Q\&A (Question-Answering) systems. However, RAG accuracy becomes increasingly challenging as the corpus of documents scales up, with Retrievers playing an outsized role in the overall RAG accuracy by extracting the most relevant document from the corpus to provide context to the LLM. In 

---

### 11
**질문**: RAG에서 검색된 문서의 순서나 개수가 답변 품질에 주는 영향을 분석한 연구 찾아줘

**논문**: OpenDecoder: Open Large Language Model Decoding to Incorporate Document Quality in RAG

> In this paper, we propose OpenDecoder, a new approach that leverages explicit evaluation of the retrieved information as quality indicator features for generation. The experimental results on five benchmark datasets demonstrate the effectiveness and better robustness of OpenDecoder by outperforming various baseline methods.

---

### 12
**질문**: 레이블 데이터가 거의 없을 때 두 데이터셋의 같은 항목을 맞추는 방법 조사해줘

**논문**: Label-template based Few-Shot Text Classification with Contrastive Learning

> As an algorithmic framework for learning to learn, meta-learning provides a promising solution for few-shot text classification. However, most existing research fail to give enough attention to class labels. Traditional basic framework building meta-learner based on prototype networks heavily relies on inter-class variance, and it is easily influenced by noise. To address these limitations, we proposes a simple and effective few-shot text classif

---

### 13
**질문**: 질문마다 검색이 필요한지 모델이 스스로 판단하게 하는 연구 찾아줘

**논문**: Fishing for Answers: Exploring One-shot vs. Iterative Retrieval Strategies for Retrieval Augmented Generation

> Retrieval-Augmented Generation (RAG) based on Large Language Models (LLMs) is a powerful solution to understand and query the industry's closed-source documents. However, basic RAG often struggles with complex QA tasks in legal and regulatory domains, particularly when dealing with numerous government documents. The top-$k$ strategy frequently misses golden chunks, leading to incomplete or inaccurate answers. To address these retrieval bottleneck

---

### 14
**질문**: 검색 인덱스를 GPU로 빠르게 만드는 근사 최근접 검색 라이브러리 연구 찾아줘

**논문**: Vector and Line Quantization for Billion-scale Similarity Search on GPUs

> Billion-scale high-dimensional approximate nearest neighbour (ANN) search has become an important problem for searching similar objects among the vast amount of images and videos available online. The existing ANN methods are usually characterized by their specific indexing structures, including the inverted index and the inverted multi-index structure. The inverted index structure is amenable to GPU-based implementations, and the state-of-the-ar

---

### 15
**질문**: LLM이 긴 대화를 기억하게 하는 메모리 구조에 대한 연구를 조사해줘

**논문**: Learning What Not to Forget: Long-Horizon Agent Memory from a Few Kilobytes of Learning

> Long-running language-model systems accumulate interaction history that outgrows the context window, so they must continually evict. When an eviction policy drops a task-critical detail, for example an access token issued at login or a path the next call needs, the action fails. We present LRE (Learned Relevance Eviction), a kilobyte-scale, CPU-only, language-model-free scorer that learns which units of history are task-critical and keeps them by

---

### 16
**질문**: 임베딩 모델을 특정 분야 문서에 맞게 조정하는 연구 조사해줘

**논문**: Efficient fine-tuning methodology of text embedding models for information retrieval: contrastive learning penalty (clp)

> Text embedding models play a crucial role in natural language processing, particularly in information retrieval, and their importance is further highlighted with the recent utilization of RAG (Retrieval- Augmented Generation). This study presents an efficient fine-tuning methodology encompassing data selection, loss function, and model architecture to enhance the information retrieval performance of pre-trained text embedding models. In particula

---

### 17
**질문**: 질문과 문서의 언어가 다를 때(교차 언어) 검색하는 방법 연구 찾아줘

**논문**: IRSC: A Zero-shot Evaluation Benchmark for Information Retrieval through Semantic Comprehension in Retrieval-Augmented Generation Scenarios

> This paper introduces the IRSC benchmark for evaluating the performance of embedding models in multilingual RAG tasks. Our contributions include: 1) the IRSC benchmark, 2) the SSCI and RCCI metrics, and 3) insights into the cross-lingual limitations of embedding models.

---

### 18
**질문**: 코드 저장소를 검색해서 코드 생성에 쓰는 retrieval-augmented code generation 연구 찾아줘

**논문**: ReCode: Improving LLM-based Code Repair with Fine-Grained Retrieval-Augmented Generation

> Recent advances in large language models (LLMs) have demonstrated impressive capabilities in code-related tasks, such as code generation and automated program repair. Despite their promising performance, most existing approaches for code repair suffer from high training costs or computationally expensive inference. Retrieval-augmented generation (RAG), with its efficient in-context learning paradigm, offers a more scalable alternative. However, c

---

### 19
**질문**: RAG에서 노이즈 문서나 방해 문서에 대한 강건성을 다룬 연구 찾아줘

**논문**: The Power of Noise: Redefining Retrieval for RAG Systems

> One counter-intuitive finding of this work is that the retriever's highest-scoring documents that are not directly relevant to the query (e.g., do not contain the answer) negatively impact the effectiveness of the LLM. Even more surprising, we discovered that adding random documents in the prompt improves the LLM accuracy by up to 35%.

---

### 20
**질문**: RAG검색을 했을시에, 두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘

**논문**: Progressive Searching for Retrieval in RAG

> Retrieval Augmented Generation (RAG) is a promising technique for mitigating two key limitations of large language models (LLMs): outdated information and hallucinations. RAG system stores documents as embedding vectors in a database. Given a query, search is executed to find the most related documents. Then, the topmost matching documents are inserted into LLMs' prompt to generate a response. Efficient and accurate searching is critical for RAG 
