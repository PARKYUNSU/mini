# 후보 10

## weekly_20261101|N14|2.0|percent
- 블록 단위: {'None': 2, 'pp': 2}
- 답: 1.  HarnessPro : 라벨‑프리 방식으로 하네스를 진화시켜 작업 성능을 향상시키면서 동시에 실행 비용이 감소하도록 설계되었다; 후보 하네스들은 LLM 기반 테스트를 통해 평가되고, 전용 에이전트가 실행 궤적을 진단하고 다양한 성과·비용 우선순위로 업데이트 계획을 수립한다 . GPT‑5.5와 Codex 조합에서 Heavy 모드의 HarnessPro가 RHO 대비 평균 패스율 증가 2.0%p를 달성함과 동시에 각 작업당 비용을 최대 26.1% 감소시켰다 .
- 원문: …on, where execution feedback guides further updates. Our experiments cover Terminal-Bench 2, SWE-Bench Pro, and ProgramBench, using GPT-5.5 with Codex…
- 원문: …ng GPT-5.5 with Codex, the heavy mode of HarnessPro achieves an average pass-rate gain of 2.0 percentage points and an average per-task cost reduction…
- 원문: …on, where execution feedback guides further updates. Our experiments cover Terminal-Bench 2, SWE-Bench Pro, and ProgramBench, using GPT-5.5 with Codex…

## weekly_20261101|C09|2.35|times
- 블록 단위: {'usd': 1}
- 답: MoE-Mamba는 Mamba와 동일한 성능을 달성하기 위해 2.35배 적은 학습 단계를 필요로 한다 . BlackMamba는 Mamba와 Transformer 기반 모델에 비해 추론 및 학습 FLOPs에서 더 나은 성능을 보이며, SSM과 MoE의 이점을 결합한다 . 두 방법 모두 Mamba에 MoE를 적용한 것이지만, 학습 효율성과 전체적인 FLOPs 측면에서 BlackMamba가 더 큰 이점을 제공한다.
- 원문: …eline Transformer-MoE. In particular, MoE-Mamba reaches the same performance as Mamba in $2.35\times$ fewer training steps while preserving the infere…

## weekly_20261101|T01|1.62|times
- 블록 단위: {'usd': 1}
- 답: 4.  AdaEAGLE : AdaEAGLE는 적응형 드래프트 구조를 명시적으로 모델링한 최초의 SD 프레임워크로, 임계값 기반 전략과 함께 vanilla AR 디코딩 대비 1.62배 속도 향상을 달성하고 고정 길이 최상위 기준을 능가합니다 .
- 원문: …raft structures. Moreover, together with threshold-based strategies, AdaEAGLE achieves a $1.62\times$ speedup over the vanilla AR decoding and outperf…

## weekly_20261101|R01|3.66|times
- 블록 단위: {'usd': 1}
- 답: 제공된 문서들은 LLM 에이전트가 도구에 의한 오류를 인지하는 정도와 관련 연구 결과를 제시하고 있습니다. 먼저,  은 도구 실패에 대한 탐지 가능성을 언급하지만 구체적인 결과나 데이터는 초록에서 제공되지 않습니다. 두 번째로,  는 기존 벤치마크가 이상적인 경로만 평가한다는 점을 지적하며, 실제 도구의 오류가 발생하면 모든 모델의 성능이 저하되고, 특히 명시적 의미 오류에서 가장 큰 하락을 보인다고 보고합니다. 또한, 에이전트 내내 견고성은 모델 규모 확대에 비해 3.66배 느리게 향상된다고 강조합니다. 마지막으로,  은 DeepDebug가 Who and When 벤치마크에서 28.8%의 정확한 에이전트·단계 귀속 정확도를 달성했으며, GAIA에서는 단일 재실행으로 13개의 실패 작업을 복구하여 전체 정확
- 원문: …tile trial-and-error loops. Crucially, agentic fault-tolerance improves with model scale $3.66\times$ slower than basic task execution, highlighting d…

## pl0_dev|P08|1.62|times
- 블록 단위: {'usd': 1}
- 답: 제공된 문서들은 모두 speculative decoding 관련 연구이지만, 품질 저하에 대한 구체적인 수치나 비교는 제시하지 않습니다.  은 속도‑품질 파레토 프론터를 확장한다는 점을 강조하고,  와  은 각각 lossless speedup(2.91x~3.51x)과 output quality 유지하면서 1.62배 속도 향상을 보고합니다. 따라서 제시된 결과만으로는 품질이 얼마나 떨어지는지를 판단할 수 없으며, 각 연구는 속도 향상과 품질 보존 사이의 trade‑off를 다르게 정의하고 있습니다.
- 원문: …raft structures. Moreover, together with threshold-based strategies, AdaEAGLE achieves a $1.62\times$ speedup over the vanilla AR decoding and outperf…

## qt0_s2|H_F04|5|doc
- 블록 단위: {'thousand': 2}
- 답: ※ 요청한 5편 중 2편만 찾았습니다.
- 원문: …i) sentence chunking is the most cost-effective method, matching semantic chunking up to ~5k tokens; (iii) a "context cliff" reduces quality beyond ~2…
- 원문: …token_ ≫ _code (for text)._ Sentence and semantic chunking were statistically tied up to ∼5k tokens; token chunking lagged; code chunking was not comp…

## qt0_s2|Q_C07|60|times
- 블록 단위: {'usd': 1}
- 답: PCA-RAG는 3,072 차원 임베딩을 110 차원으로 축소함으로써 검색 속도를 최대 60배 가속화하고 인덱스 크기를 약 28.6배 감소시켰으며, 인간 주석과 유사한 상관관계가 유지되는 결과를 보였습니다 . K-Token Merging은 입력 길이를 최대 75%까지 줄이면서도 성능 저하가 최소화되어 성능 대비 압축 비율에서 파레토 프론트에 위치한다는 실험 결과를 제시했습니다 . 두 연구 모두 고차원 텍스트 임베딩을 압축하여 효율성을 크게 향상시켰지만, PCA-RAG는 차원 축소와 인덱스 크기 감소에 초점을 둔 반면, K-Token Merging은 토큰 수 자체를 줄이는 방식으로 입력 길이 감소와 성능 보존 사이의 균형을 달성했습니다.
- 원문: …sults show that reducing vectors from 3,072 to 110 dimensions provides a sizeable (up to $60\times$) speedup in retrieval operations and a $\sim 28.6\…

## ans_hu|HU27|59|percent
- 블록 단위: {'pp': 1}
- 답: 1.  Statutory AI : 법적 규범에 맞춰 LLM을 정렬하는 접근법으로, 52‑59%p의 유해 콘텐츠 감소와 컴퓨팅 시간 절감 효과를 보였다 .
- 원문: …ce, fraud, and abuse of vulnerable persons. Statutory AI reduced harmful content by 52 to 59 percentage points across tested models, approximately 10 …

## ans_hu|HU27|0.38|pp
- 블록 단위: {'percent': 1}
- 답: Statutory AI는 테스트된 모델에서 유해 콘텐츠를 52~59%p 감소시켜 표준 Constitutional AI보다 약 10%p 더 높은 효과를 보였으며, 계산 시간을 50% 이상 단축했다 . 반면, 향상된 헌법 분류기는 레드팀 평가에서 공격 성공률을 낮추면서도 생산 트래픽 거부율을 0.38%p 증가시키고 추론 오버헤드를 23.7%로 유지하는 결과를 보였다 . 두 연구는 각각 법적 규범 정렬과 레드팀 방어에 초점을 맞추어, 데이터와 평가 조건이 다르지만 모두 기존 Constitutional AI보다 성능을 개선하거나 효율성을 높인다는 공통된 결론을 제시한다.
- 원문: …ecific jailbreaks. These classifiers also maintain deployment viability, with an absolute 0.38% increase in production-traffic refusals and a 23.7% in…

## ans_hu|HU28|21.9|times
- 블록 단위: {'usd': 1}
- 답: 제공된 문서들은 긴 컨텍스트와 위치 편향 문제를 다루지만, 각각의 접근법과 결과가 명확히 구분된다.  는 'found-in-the-middle' 메커니즘을 통해 중간에 위치한 컨텍스트에도 신뢰성 있게 주의를 기울일 수 있으며, 이는 기존 방법보다 최대 15%p 향상된 RAG 성능을 보인다고 보고한다. 반면  은 RoPE 기반 모델이 토큰 구별은 개선하지만 위치 구별 능력을 희생한다는 한계를 지적하고, 다중 헤드·레이어 구조만으로는 이 문제를 해결할 수 없다고 결론낸다. 또한  는 Orthros가 긴 컨텍스트 능력을 유지하면서 21.9배의 프리필링 속도 향상을 달성했다고 제시한다. 따라서 위치 편향 완화와 긴 컨텍스트 활용은 모델 설계와 메커니즘에 따라 성능이 크게 달라지며, 각 연구는 서로 다른 기술적 접근
- 원문: …ng performance that even surpasses the original Transformer. Finally, Orthros achieves a $21.9\times$ prefilling speedup over Transformers with end-to…

# 단위 없음 표본 24

## us_1027|U5-2|32|times
- 블록 단위: {'None': 1}
- 답: LOOKAT은 GPT‑2에서 64배 압축을 달성하면서 95.7%의 출력 충실도를 유지하고, 32배 압축 시에도 95.0%의 충실도를 확보한다 . CommVQ는 FP16 KV 캐시를 2비트 양자화하여 87.5%를 감소시키며 기존 최첨단 KV 캐시 양자화 방법보다 우수한 성능을 보인다 . 두 연구 모두 임베딩 벡터(또는 KV 캐시)를 양자화함으로써 메모리 사용량을 크게 줄이면서도 검색·생성 성능을 거의 손실하지 않는다는 공통된 결론을 제시한다.
- 원문: …nd to compute-bound. LOOKAT achieves 64 $\times$ compression at 95.7% output fidelity and 32 $\times$ compression at 95.0% fidelity when tested on GPT…

## us_1027|U3-5|5|doc
- 블록 단위: {'None': 1}
- 답: ※ 요청한 5편 중 3편만 찾았습니다.
- 원문: …rk suite and code can be found at https://github.com/qinchuanhui/UDA-Benchmark.  ---  [문서 5] [Distance: 0.4138] [발행일: 2025-09-25] [2509.20769v1] Prove…

## qt0_s2|Q_D02|56.7|percent
- 블록 단위: {'None': 1}
- 답: 3.  Prompt-SAW : 텍스트 정보를 이용해 그래프를 구축한 뒤 핵심 정보 요소를 추출하여 프롬프트를 압축하며, 가독성 향상과 함께 작업‑무관/작업‑인식 설정에서 각각 최대 10.1·77.1까지 성능을 개선하고 원본 대비 34.9~56.7%의 텍스트 감소율을 달성합니다 .
- 원문: …k-agnostic and task-aware settings while compressing the original prompt text by 34.9 and 56.7.  To further support our claims, we also conducted a qu…

## ans_hu|HU39|87|percent
- 블록 단위: {'None': 1}
- 답: 3.  T-FREE : 토크나이저 없이 문자 삼중항 기반 희소 활성화 패턴으로 직접 단어를 임베딩하고, 유사한 단어의 압축을 통해 파라미터와 인코더 길이를 각각 87%·56%까지 감소시키는 방법을 제안했습니다
- 원문: … exploitation of similarities allows T-FREE to reduce the size of the embedding layers by 87 _._ 5%[3] and the average encoding length of text by 56%[…

## us_1027|U5-2|64|times
- 블록 단위: {'None': 1}
- 답: LOOKAT은 GPT‑2에서 64배 압축을 달성하면서 95.7%의 출력 충실도를 유지하고, 32배 압축 시에도 95.0%의 충실도를 확보한다 . CommVQ는 FP16 KV 캐시를 2비트 양자화하여 87.5%를 감소시키며 기존 최첨단 KV 캐시 양자화 방법보다 우수한 성능을 보인다 . 두 연구 모두 임베딩 벡터(또는 KV 캐시)를 양자화함으로써 메모리 사용량을 크게 줄이면서도 검색·생성 성능을 거의 손실하지 않는다는 공통된 결론을 제시한다.
- 원문: …kup tables. This transforms attention from memory-bound to compute-bound. LOOKAT achieves 64 $\times$ compression at 95.7% output fidelity and 32 $\ti…

## qt0_s2|Q_A05|10|doc
- 블록 단위: {'None': 1}
- 답: ※ 요청한 10편 중 1편만 찾았습니다.
- 원문: …ts to advance chunk-based retrieval in long-document Information Retrieval (IR).  ## June 10, 2025  ## **ABSTRACT**  Chunking is a crucial preprocessi…

## ans_hu|HU36|9|billion
- 블록 단위: {'None': 1}
- 답: 질문은 로컬 환경에서 9B 모델을 실행할 때  모델 라우팅 ,  로딩·콜드 스타트 지연 감소 와 같은 문제를 해결하기 위해 작은 모델과 보조 모델을 어떻게 나누어야 하는지에 대한 정보를 찾고 있습니다. 이러한 문제는 메모리 제약이 큰 상황에서 응답 속도를 높이기 위한 핵심 과제입니다.
- 원문: … benchmarking data, we offer valuable insights to advance research in this field.  Figure 9: The relationship between the latency and quantization met…

## weekly_20261101|C09|35|times
- 블록 단위: {'None': 1}
- 답: 1.  MoE‑Mamba : 실험 결과에 따라 2 × 35배 적은 학습 단계로 동일한 성능을 달성하며, 추론 시 Mamba 대비 Transformer보다 우수한 효율성을 유지합니다 .
- 원문: …the performance of Mamba. Our main result, see Figure 1, shows that MoE-Mamba needs 2 _._ 35 _× fewer training steps_ to reach the same performance as…

## pl0_dev|P29|1024|token
- 블록 단위: {'None': 1}
- 답: 제공된 문서들에 따르면, 청크 크기가 작아질수록 인용 정확도가 항상 높아지는 것은 아니며, 데이터 유형과 모델에 따라 최적의 크기가 달라진다.  는 짧은 형식의 데이터셋에서는 작은 청크(64-128 토큰)가, 긴 문맥이 필요한 데이터셋에서는 큰 청크(512-1024 토큰)가 더 효과적임을 보여준다. 또한  은 모든 문서 유형에서 512 또는 1024 토큰 크기가 다른 크기보다 일관되게 우수한 성능을 보인다고 보고한다. 따라서 청크 크기를 작게 할수록 인용 정확도가 무조건 오르는 것이 아니라, 데이터 특성과 모델에 맞는 적절한 크기를 선택하는 것이 중요하다.
- 원문: … of chunk size and top-k, we find that across all three document types chunk sizes 512 or 1024 consistently outperform other chunk sizes for both mode…

## weekly_20261101|T02|32|times
- 블록 단위: {'None': 1}
- 답: 3.  LOOKAT : 키 벡터를 서브스페이스로 분해하고 코드북 학습 및 룩업 테이블을 통해 주의를 계산하는 제품 양자화와 비대칭 거리 계산을 적용한 메모리 효율적 트랜스포머입니다; GPT‑2에서 64× 압축 시 95.7% 출력 충실도, 32× 압축 시 95.0% 충실도를 달성합니다.
- 원문: …s via lookup tables. LOOKAT achieves 64 $\times$ compression at 95.7% output fidelity and 32 $\times$ compression at 95.0% fidelity when tested on GPT…

## weekly_20261101|R02|3|doc
- 블록 단위: {'None': 1}
- 답: ※ 요청한 5편 중 3편만 찾았습니다.
- 원문: …untime and consuming up to 50 times less GPU memory than end-to-end evaluation.  ---  [문서 3] [Distance: 0.3677] [발행일: 2023-12-12] [2312.07796v1] Harne…

## ogb0_s2|OB_069|2|man
- 블록 단위: {'None': 1}
- 답: 1.  SciCap : SciBERT를 이용해 논문 제목·추록·인용 등 메타데이터를 인코딩한 후, CLIP+GPT‑2와 GPT‑2만 사용한 두 모델을 비교해 텍스트 기반 캡셔닝 성능을 평가한다 .
- 원문: …ciBERT+GPT2 model that uses only the textual metadata achieved optimal performance.  ## **2 Related Work**   Image captioning has received significant…

## qt0_s2|H_F04|2|doc
- 블록 단위: {'None': 2}
- 답: ※ 요청한 5편 중 2편만 찾았습니다.
- 원문: … and show how granularity affects RAG with Long Context LLMs.[Leng et al. 2024]  ---  [문서 2] [Distance: 0.3347] [발행일: 2025-02-20] [2502.14759v1] On th…
- 원문: … tokens; token chunking lagged; code chunking was not competitive on this text task (Fig. 2). Mechanism: sentence-preserving methods keep topical cohe…

## us_1027|U5-4|8.3|times
- 블록 단위: {'None': 1}
- 답: 벡터 검색 인덱스 최적화 연구들은 각각 다른 접근법과 성능 향상을 보고하고 있다. MINT는 다중 벡터 검색 작업에 대해 지연 시간을 2.1배에서 8.3배까지 단축하며 저장 및 재현율 제약을 만족한다 . VSAG는 그래프 기반 근접 이웃 검색에서 HNSWlib 대비 최대 4배 속도 향상을 달성하면서 정확도는 동일하게 유지한다 . PipeANN-Filter는 Bloom 필터와 같은 확률적 데이터 구조를 활용해 위상집합을 식별함으로써 지연 시간과 처리량을 기존 최첨단 시스템보다 개선한다 . 이러한 결과들은 각 연구가 서로 다른 최적화 기법과 평가 조건에서 유사한 목표인 검색 성능 향상을 달성하고 있음을 보여준다.
- 원문: …et storage and recall constraints. Compared to the baseline, our latency achieves 2.1X to 8.3X speedup.  [문서 2] [Distance: 0.3942] [발행일: 2025-03-23] […

## weekly_20261101|T02|64|times
- 블록 단위: {'None': 1}
- 답: 제공된 문서들은 KV 캐시 압축 연구에서 서로 다른 접근법과 결과를 보여줍니다. LOOKAT는 GPT‑2를 대상으로 64× 압축 시 95.7%의 출력 충실도를 달성했습니다 . KeyDiff는 Llama와 Qwen 모델에서 8K 캐시 예산 하에 기존 방식 대비 약 0.04% 성능 격차만을 보이며 KV 캐시를 약 23% 감소시켰습니다 . 반면, KVSculpt는 압축 난이도가 레이어마다 최대 100배까지 차이가 나며 두 개의 KV 헤드 간에도 큰 차이가 있음을 분석했습니다 . 이러한 결과들은 모델 종류와 평가 조건에 따라 압축 비율과 성능 손실이 크게 달라진다는 점을 시사합니다.
- 원문: …ces, learning codebooks and computing attention tables via lookup tables. LOOKAT achieves 64 $\times$ compression at 95.7% output fidelity and 32 $\ti…

## weekly_20261101|N03|60|person
- 블록 단위: {'None': 1}
- 답: 1.  CCBENCH‑Health : 60명의 이론적 배경을 가진 페르소나와 각 문화를 대표하는 암시된 규준 상태, 총 3 120개의 고유한 상호작용으로 구성된 벤치마크를 통해 LLM의 문화 역량을 평가합니다 .
- 원문: …ltural belongingness. As a case study on health, we create CCBENCH-Health, which includes 60 theoretically grounded personas exhibiting varied norm-ad…

## us_1027|U5-4|2.1|times
- 블록 단위: {'None': 1}
- 답: 벡터 검색 인덱스 최적화 연구들은 각각 다른 접근법과 성능 향상을 보고하고 있다. MINT는 다중 벡터 검색 작업에 대해 지연 시간을 2.1배에서 8.3배까지 단축하며 저장 및 재현율 제약을 만족한다 . VSAG는 그래프 기반 근접 이웃 검색에서 HNSWlib 대비 최대 4배 속도 향상을 달성하면서 정확도는 동일하게 유지한다 . PipeANN-Filter는 Bloom 필터와 같은 확률적 데이터 구조를 활용해 위상집합을 식별함으로써 지연 시간과 처리량을 기존 최첨단 시스템보다 개선한다 . 이러한 결과들은 각 연구가 서로 다른 최적화 기법과 평가 조건에서 유사한 목표인 검색 성능 향상을 달성하고 있음을 보여준다.
- 원문: …y and meet storage and recall constraints. Compared to the baseline, our latency achieves 2.1X to 8.3X speedup.  [문서 2] [Distance: 0.3942] [발행일: 2025-…

## qt0_s2|Q_C07|28.6|times
- 블록 단위: {'None': 1}
- 답: PCA-RAG는 3,072 차원 임베딩을 110 차원으로 축소함으로써 검색 속도를 최대 60배 가속화하고 인덱스 크기를 약 28.6배 감소시켰으며, 인간 주석과 유사한 상관관계가 유지되는 결과를 보였습니다 . K-Token Merging은 입력 길이를 최대 75%까지 줄이면서도 성능 저하가 최소화되어 성능 대비 압축 비율에서 파레토 프론트에 위치한다는 실험 결과를 제시했습니다 . 두 연구 모두 고차원 텍스트 임베딩을 압축하여 효율성을 크게 향상시켰지만, PCA-RAG는 차원 축소와 인덱스 크기 감소에 초점을 둔 반면, K-Token Merging은 토큰 수 자체를 줄이는 방식으로 입력 길이 감소와 성능 보존 사이의 균형을 달성했습니다.
- 원문: …nsions provides a sizeable (up to $60\times$) speedup in retrieval operations and a $\sim 28.6\times$ reduction in index size, with only moderate decl…

## qt0_s2|Q_D02|6|times
- 블록 단위: {'None': 1}
- 답: 제공된 문서들은 프롬프트 압축 방법들을 동일한 조건에서 비교한 벤치마크 결과를 제시하고 있습니다. SCOPE는 질문‑답변 및 요약 과제와 다양한 도메인 데이터를 이용해 평가했으며, 높은 압축 비율에서도 기존 최첨단 방법보다 압축 품질과 안정성이 크게 향상됨을 보였습니다 . Prompt-SAW는 GSM8K‑aug 벤치마크를 사용해 작업‑무관 프롬프트에 대해 가독성뿐만 아니라 성능 측면에서 베이스라인 대비 최대 10.1 및 77.1의 향상을 달성하고, 원본 텍스트를 각각 34.9와 56.7만큼 압축함을 확인했습니다 . LLMLingua‑2는 데이터 증류 방식을 통해 작업‑무관 프롬프트 압축에 초점을 맞추어 기존 방법보다 3배~6배 빠른 속도와 1.6배~2.9배 감소된 전체 지연 시간을 보여주며, 성능과 압축 지
- 원문: …h compression ratios of 2x-5x. Our code is available at https://aka.ms/LLMLingua-2.  ## **6 Conclusion**  This paper targets task-agnostic prompt comp…

## qt0_s2|Q_A05|1|doc
- 블록 단위: {'None': 2}
- 답: ※ 요청한 10편 중 1편만 찾았습니다.
- 원문: …[문서 1] [Distance: 0.4194] [발행일: 2025-09-05] [2509.04820v1] Fishi…
- 원문: …ance for real-world applications in legal and regulatory domains.  As illustrated in Fig. 1(b), such a greedy retrieval RelevantHighly  Chunk Delete<b…

## weekly_20261101|R02|5|doc
- 블록 단위: {'None': 1}
- 답: ※ 요청한 5편 중 3편만 찾았습니다.
- 원문: …ations for enterprise deployments, limitations, and future research directions.  ---  [문서 5] [Distance: 0.3064] [발행일: 2025-08-21] [2508.15437v2] Test-…

## qt0_s2|Q_C07|3,072|dim
- 블록 단위: {'None': 2}
- 답: PCA-RAG는 3,072 차원 임베딩을 110 차원으로 축소함으로써 검색 속도를 최대 60배 가속화하고 인덱스 크기를 약 28.6배 감소시켰으며, 인간 주석과 유사한 상관관계가 유지되는 결과를 보였습니다 . K-Token Merging은 입력 길이를 최대 75%까지 줄이면서도 성능 저하가 최소화되어 성능 대비 압축 비율에서 파레토 프론트에 위치한다는 실험 결과를 제시했습니다 . 두 연구 모두 고차원 텍스트 임베딩을 압축하여 효율성을 크게 향상시켰지만, PCA-RAG는 차원 축소와 인덱스 크기 감소에 초점을 둔 반면, K-Token Merging은 토큰 수 자체를 줄이는 방식으로 입력 길이 감소와 성능 보존 사이의 균형을 달성했습니다.
- 원문: …ll-dimensional and PCA-compressed embeddings. Our results show that reducing vectors from 3,072 to 110 dimensions provides a sizeable (up to $60\times…
- 원문: …e first few dozen principal components accounted for the vast majority of variance in the 3,072-dimension embeddings  [문서 3] [Distance: 0.3282] [발행일: …

## qt0_s2|Q_A04|2|doc
- 블록 단위: {'None': 2}
- 답: ※ 요청한 3편 중 2편만 찾았습니다.
- 원문: …s have been unable to accomplish.  ## **5.2 Performance on One-shot Reasoning**  In Table 2, we present the performance of all methods in the one-shot…
- 원문: …ons chosen by our method better stimulate the LLM’s contextual learning ability  ---  [문서 2] [Distance: 0.4078] [발행일: 2025-02-14] [2502.09933v5] MIR-B…

## us_1027|U3-5|3|doc
- 블록 단위: {'None': 1}
- 답: ※ 요청한 5편 중 3편만 찾았습니다.
- 원문: …and long-context LLM baselines for end-to-end multimodal document QA by 12-20%.  ---  [문서 3] [Distance: 0.2597] [발행일: 2025-03-26] [2504.08748v1] A Sur…

