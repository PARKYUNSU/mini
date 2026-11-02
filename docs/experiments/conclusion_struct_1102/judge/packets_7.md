# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)

## H_H04 — 트랜스포머 대체할만한 구조 연구 있나

### 인용 블록

[문서 1]
[Distance: 0.3115]
[발행일: 2024-04-15]
[2404.09516v1] State Space Model for New-Generation Network Alternative to Transformers: A Survey
[초록] In the post-deep learning era, the Transformer architecture has demonstrated its powerful performance across pre-trained big models and various downstream tasks. However, the enormous computational demands of this architecture have deterred many researchers. To further reduce the complexity of attention models, numerous efforts have been made to design more efficient methods. Among them, the State Space Model (SSM), as a possible replacement for the self-attention based Transformer model, has drawn more and more attention in recent years. In this paper, we give the first comprehensive review of these works and also provide experimental comparisons and analysis to better demonstrate the features and advantages of SSM. Specifically, we first give a detailed description of principles to help the readers quickly capture the key ideas of SSM. After that, we dive into the reviews of existing SSMs and their various applications, including natural language processing, computer vision, graph, multi-modal and multi-media, point cloud/event stream, time series data, and other domains. In addition, we give statistical comparisons and analysis of these models and hope it helps the readers to understand the effectiveness of different structures on various tasks. Then, we propose possible research points in this direction to better promote the development of the theoretical model and application of SSM. More related works will be continuously updated on the following GitHub: https://github.com/Event-AHU/Mamba_State_Space_Model_Paper_List.

. The Transformer architecture first swept the NLP community with the help of _pre-training and fine-tuning_ paradigm [14], such as BERT [15], ERNIE [16], BART [17], GPT [18]. Then, other communities are also boosted with such networks, for example, the ViT [19] and Swin-Transformer [20] released in computer vision. Many researchers also exploit the hybrid network architectures by combining Transformer and other networks, or adapting the Transformer for multi-modal research problems [21], [22]
[문서 2]
[Distance: 0.3325]
[발행일: 2024-12-19]
[2412.14847v2] A Survey of RWKV
[초록] The Receptance Weighted Key Value (RWKV) model offers a novel alternative to the Transformer architecture, merging the benefits of recurrent and attention-based systems. Unlike conventional Transformers, which depend heavily on self-attention, RWKV adeptly captures long-range dependencies with minimal computational demands. By utilizing a recurrent framework, RWKV addresses some computational inefficiencies found in Transformers, particularly in tasks with long sequences. RWKV has recently drawn considerable attention for its robust performance across multiple domains. Despite its growing popularity, no systematic review of the RWKV model exists. This paper seeks to fill this gap as the first comprehensive review of the RWKV architecture, its core principles, and its varied applications, such as natural language generation, natural language understanding, and computer vision. We assess how RWKV compares to traditional Transformer models, highlighting its capability to manage long sequences efficiently and lower computational costs. Furthermore, we explore the challenges RWKV encounters and propose potential directions for future research and advancement. We consistently maintain the related open-source materials at: https://github.com/MLGroupJLU/RWKV-Survey.

Proposed by Vaswani et al. in 2017, the Transformer model [20] has since become a dominant architecture in natural language processing (NLP) [21], [22], [23] and various other fields [24], [25], [26]. Transformer-based models such as BERT [27] and GPT [28] have demonstrated exceptional performance in tasks such as text classification [29], language generation [30], and question answering [31]
[문서 3]
[Distance: 0.3287]
[발행일: 2025-01-28]
[2501.17088v1] Mamba-Shedder: Post-Transformer Compression for Efficient Selective Structured State Space Models
[초록] Large pre-trained models have achieved outstanding results in sequence modeling. The Transformer block and its attention mechanism have been the main drivers of the success of these models. Recently, alternative architectures, such as Selective Structured State Space Models (SSMs), have been proposed to address the inefficiencies of Transformers. This paper explores the compression of SSM-based models, particularly Mamba and its hybrids. We study the sensitivity of these models to the removal of selected components at different granularities to reduce the model size and computational overhead, thus improving their efficiency while maintaining accuracy. The proposed solutions, collectively referred to as Mamba-Shedder, achieve a speedup of up to 1.4x during inference, demonstrating that model efficiency can be improved by eliminating several redundancies with minimal impact on the overall model performance. The code is available at https://github.com/IntelLabs/Hardware-Aware-Automated-Machine-Learning.

We have seen an outstanding increase in the number of Transformer-based models (Vaswani et al., 2017) developed to tackle tasks from Natural Language Processing (NLP) and other domains (Parmar et al., 2018; Dosovitskiy et al., 2021; Arnab et al., 2021; Gong et al., 2021) due to their effectiveness at modeling sequences. However, these models also present critical efficiency challenges. For example, the cost of training these models scales quadratically in the sequence length

### 문장

- s1: 세 번째로, Mamba-Shedder는 선택적 구조 상태 공간 모델을 압축하여 추론 속도를 최대 1.4배까지 향상시키며, 모델 크기 감소와 성능 유지 사이의 균형을 달성한다[2501.17088v1].
- s2: 제안된 솔루션들은 집합적으로 Mamba-Shedder라 불리며, 추론 단계에서 최대 1.4배의 속도 향상을 달성함으로써 모델 효율성을 유지하면서 전체 성능에 미치는 영향이 최소인 상태에서 여러 중복을 제거함으로써 모델 효율성을 향상시킬 수 있음을 보여줍니다. [2501.17088v1]
- s3: 먼저, 상태 공간 모델(SSM)에 대한 종합 리뷰와 실험 비교를 통해 복잡성 감소와 다양한 도메인 적용 가능성을 제시한다[2404.09516v1].
- s4: 그 중에서도 자기주의 기반 트랜스포머 모델을 대체할 가능한 후보인 상태공간 모델(SSM)은 최근 몇 년 동안 점점 더 많은 관심을 받고 있다. [2404.09516v1]
- s5: 두 번째로, RWKV는 재귀 프레임워크를 활용해 트랜스포머의 계산 비효율성을 해결하고, 특히 긴 시퀀스 처리에서 효율성과 비용 절감 효과를 입증한다[2412.14847v2].
- s6: Receptance Weighted Key Value(RWKV) 모델은 재귀형 시스템과 주의 기반 시스템의 장점을 결합한 새로운 대안으로 트랜스포머 아키텍처를 대체합니다. [2412.14847v2]

