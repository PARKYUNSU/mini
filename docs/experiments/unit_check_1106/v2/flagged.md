# 후보 1

## ans_hu|HU27|0.38|pp
- 블록 단위: {'percent': 1}
- 답: Statutory AI는 테스트된 모델에서 유해 콘텐츠를 52~59%p 감소시켜 표준 Constitutional AI보다 약 10%p 더 높은 효과를 보였으며, 계산 시간을 50% 이상 단축했다 . 반면, 향상된 헌법 분류기는 레드팀 평가에서 공격 성공률을 낮추면서도 생산 트래픽 거부율을 0.38%p 증가시키고 추론 오버헤드를 23.7%로 유지하는 결과를 보였다 . 두 연구는 각각 법적 규범 정렬과 레드팀 방어에 초점을 맞추어, 데이터와 평가 조건이 다르지만 모두 기존 Constitutional AI보다 성능을 개선하거나 효율성을 높인다는 공통된 결론을 제시한다.
- 원문: …ecific jailbreaks. These classifiers also maintain deployment viability, with an absolute 0.38% increase in production-traffic refusals and a 23.7% in…

# 단위 없음 표본 8

## weekly_20261101|T01|0.34|ms
- 블록 단위: {'None': 1}
- 답: 8.  SpecKV : SpecKV는 드래프트 모델 자체 신호를 이용해 각 speculation 단계마다 γ 값을 선택하는 경량 적응형 컨트롤러이며, 고정‑γ=4 기준보다 토큰당 기대치를 크게 높이고 오버헤드는 0.34ms에 그칩니다 .
- 원문: …r speculation step, achieving a 56.0% improvement over the fixed-$γ$=4 baseline with only 0.34\,ms overhead per decision ($<$0.5% of step time).…

## qt0_s2|Q_C07|3,072|dim
- 블록 단위: {'None': 2}
- 답: PCA-RAG는 3,072 차원 임베딩을 110 차원으로 축소함으로써 검색 속도를 최대 60배 가속화하고 인덱스 크기를 약 28.6배 감소시켰으며, 인간 주석과 유사한 상관관계가 유지되는 결과를 보였습니다 . K-Token Merging은 입력 길이를 최대 75%까지 줄이면서도 성능 저하가 최소화되어 성능 대비 압축 비율에서 파레토 프론트에 위치한다는 실험 결과를 제시했습니다 . 두 연구 모두 고차원 텍스트 임베딩을 압축하여 효율성을 크게 향상시켰지만, PCA-RAG는 차원 축소와 인덱스 크기 감소에 초점을 둔 반면, K-Token Merging은 토큰 수 자체를 줄이는 방식으로 입력 길이 감소와 성능 보존 사이의 균형을 달성했습니다.
- 원문: …ll-dimensional and PCA-compressed embeddings. Our results show that reducing vectors from 3,072 to 110 dimensions provides a sizeable (up to $60\times…
- 원문: …e first few dozen principal components accounted for the vast majority of variance in the 3,072-dimension embeddings  [문서 3] [Distance: 0.3282] [발행일: …

## pl0_dev|P29|1024|token
- 블록 단위: {'None': 1}
- 답: 제공된 문서들에 따르면, 청크 크기가 작아질수록 인용 정확도가 항상 높아지는 것은 아니며, 데이터 유형과 모델에 따라 최적의 크기가 달라진다.  는 짧은 형식의 데이터셋에서는 작은 청크(64-128 토큰)가, 긴 문맥이 필요한 데이터셋에서는 큰 청크(512-1024 토큰)가 더 효과적임을 보여준다. 또한  은 모든 문서 유형에서 512 또는 1024 토큰 크기가 다른 크기보다 일관되게 우수한 성능을 보인다고 보고한다. 따라서 청크 크기를 작게 할수록 인용 정확도가 무조건 오르는 것이 아니라, 데이터 특성과 모델에 맞는 적절한 크기를 선택하는 것이 중요하다.
- 원문: … of chunk size and top-k, we find that across all three document types chunk sizes 512 or 1024 consistently outperform other chunk sizes for both mode…

## ans_hu|HU36|9|billion
- 블록 단위: {'None': 1}
- 답: 질문은 로컬 환경에서 9B 모델을 실행할 때  모델 라우팅 ,  로딩·콜드 스타트 지연 감소 와 같은 문제를 해결하기 위해 작은 모델과 보조 모델을 어떻게 나누어야 하는지에 대한 정보를 찾고 있습니다. 이러한 문제는 메모리 제약이 큰 상황에서 응답 속도를 높이기 위한 핵심 과제입니다.
- 원문: … benchmarking data, we offer valuable insights to advance research in this field.  Figure 9: The relationship between the latency and quantization met…

## weekly_20261101|N03|60|person
- 블록 단위: {'None': 1}
- 답: 1.  CCBENCH‑Health : 60명의 이론적 배경을 가진 페르소나와 각 문화를 대표하는 암시된 규준 상태, 총 3 120개의 고유한 상호작용으로 구성된 벤치마크를 통해 LLM의 문화 역량을 평가합니다 .
- 원문: …ltural belongingness. As a case study on health, we create CCBENCH-Health, which includes 60 theoretically grounded personas exhibiting varied norm-ad…

## qt0_s2|Q_D02|56.7|percent
- 블록 단위: {'None': 1}
- 답: 3.  Prompt-SAW : 텍스트 정보를 이용해 그래프를 구축한 뒤 핵심 정보 요소를 추출하여 프롬프트를 압축하며, 가독성 향상과 함께 작업‑무관/작업‑인식 설정에서 각각 최대 10.1·77.1까지 성능을 개선하고 원본 대비 34.9~56.7%의 텍스트 감소율을 달성합니다 .
- 원문: …k-agnostic and task-aware settings while compressing the original prompt text by 34.9 and 56.7.  To further support our claims, we also conducted a qu…

## qt0_s2|Q_D02|6|times
- 블록 단위: {'None': 1}
- 답: 제공된 문서들은 프롬프트 압축 방법들을 동일한 조건에서 비교한 벤치마크 결과를 제시하고 있습니다. SCOPE는 질문‑답변 및 요약 과제와 다양한 도메인 데이터를 이용해 평가했으며, 높은 압축 비율에서도 기존 최첨단 방법보다 압축 품질과 안정성이 크게 향상됨을 보였습니다 . Prompt-SAW는 GSM8K‑aug 벤치마크를 사용해 작업‑무관 프롬프트에 대해 가독성뿐만 아니라 성능 측면에서 베이스라인 대비 최대 10.1 및 77.1의 향상을 달성하고, 원본 텍스트를 각각 34.9와 56.7만큼 압축함을 확인했습니다 . LLMLingua‑2는 데이터 증류 방식을 통해 작업‑무관 프롬프트 압축에 초점을 맞추어 기존 방법보다 3배~6배 빠른 속도와 1.6배~2.9배 감소된 전체 지연 시간을 보여주며, 성능과 압축 지
- 원문: …h compression ratios of 2x-5x. Our code is available at https://aka.ms/LLMLingua-2.  ## **6 Conclusion**  This paper targets task-agnostic prompt comp…

## ans_hu|HU39|87|percent
- 블록 단위: {'None': 1}
- 답: 3.  T-FREE : 토크나이저 없이 문자 삼중항 기반 희소 활성화 패턴으로 직접 단어를 임베딩하고, 유사한 단어의 압축을 통해 파라미터와 인코더 길이를 각각 87%·56%까지 감소시키는 방법을 제안했습니다
- 원문: … exploitation of similarities allows T-FREE to reduce the size of the embedding layers by 87 _._ 5%[3] and the average encoding length of text by 56%[…

