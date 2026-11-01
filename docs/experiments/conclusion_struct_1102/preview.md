# R5 미리보기 — 결론을 논문마다 초록 결과 한 줄로 (운영 변경 없음)

답 43개(recheck_1031 3 + weekly_20261101 real40)의 본론 인용 논문 수 = A · B 결론 줄 수: 1편 13답 · 2편 19답 · 3편 4답 · 4편 2답 · 5편 1답 · 6편 1답 · 8편 2답 · 10편 1답.
지금 결론 다시 쓰기처럼 2편 이상만 바꾼다(1편 답은 그대로).
2편 이상 답의 지금 결론 문장: 인용 붙음 88 · 인용 없음 65 — C 는 앞쪽만 바꾼다.

## R_137 — LLM-as-judge self-preference bias를 다룬 논문을 찾아라. 초안 생성 모델과 사실성 판정 모델이 같은 GPT-4 계열일 때, faithfulness나 hallucination rate가 얼마나 낙관적으로 나오는가. 판정자를 다른 모델군으로 두거나, 인간 표본으로 보정하는 절차는 무엇인가.

**지금 결론** (운영 · 9B v2 다시 쓰기 12.8s)

LLM-as-judge가 동일한 GPT-4 계열 모델일 때, 낮은 perplexity를 가진 출력을 인간 평가자보다 훨씬 높은 점수로 부여하는 현상이 관찰되어 자기 선호 편향이 발생한다는 결과가 제시된다[2410.21819v2]. 이러한 편향은 판정자를 다른 모델군으로 교체하거나 인간 표본을 이용해 보정함으로써 완화될 수 있으며, 패널 기반 판정이나 심층 추론과 같은 방법이 일관성을 향상시키는 것으로 나타났다[2512.16041v1]. 또한, 기존 벤치마크가 인간 주석에 의존해 인간 편향을 도입한다는 점에서 인간 평가 자체도 신뢰할 수 없는 금표준이 될 수 있음을 지적한다[2512.16041v1].

**A 논문별 한 줄 · 영어 원문**

- Self-Preference Bias in LLM-as-a-Judge — Our findings reveal that LLMs assign significantly higher evaluations to outputs with lower perplexity than human evaluators, regardless of whether the outputs were self-generated. [2410.21819v2]
- Are We on the Right Way to Assessing LLM-as-a-Judge? — We also find substantial inconsistency in human judgments, which indicates that human annotation may not be a reliable gold standard. [2512.16041v1]

**B 논문별 한 줄 · 9B 번역만 (질문은 안 보여 줌)**

- Self-Preference Bias in LLM-as-a-Judge — 우리의 연구 결과는 LLM이 인간 평가자보다 낮은 불확실성(perplexity)을 가진 출력에 대해 유의미하게 높은 평가를 부여한다는 점을 보여주며, 이러한 출력이 자체 생성되었든 그렇지 않든 관계없이 해당 현상이 관찰됩니다. [2410.21819v2]
- Are We on the Right Way to Assessing LLM-as-a-Judge? — We also find substantial inconsistency in human judgments, which indicates that human annotation may not be a reliable gold standard. [2512.16041v1] (영어로 둠: 부정어 빠짐 — 번역은 「우리는 또한 인간 판단에 상당한 일관성 부재가 존재함을 발견했으며, 이는 인간 주석이 신뢰할 수 있는 금표준이 될 수 있음을 시사한다.」)

**C 혼합 — 인용 붙은 문장만 B 줄로**

- (초록) Self-Preference Bias in LLM-as-a-Judge — 우리의 연구 결과는 LLM이 인간 평가자보다 낮은 불확실성(perplexity)을 가진 출력에 대해 유의미하게 높은 평가를 부여한다는 점을 보여주며, 이러한 출력이 자체 생성되었든 그렇지 않든 관계없이 해당 현상이 관찰됩니다. [2410.21819v2]
- (초록) Are We on the Right Way to Assessing LLM-as-a-Judge? — We also find substantial inconsistency in human judgments, which indicates that human annotation may not be a reliable gold standard. [2512.16041v1]

**D 바꿔 끼우기 — 인용 붙은 문장을 9B 문장과 가장 겹치는 원문 문장으로**

- (원문) Self-Preference Bias in LLM-as-a-Judge — 우리의 실험 결과는 GPT-4가 상당한 정도의 자기 선호 편향을 보인다는 것을 보여줍니다. [2410.21819v2]
- (원문) Are We on the Right Way to Assessing LLM-as-a-Judge? — We also find substantial inconsistency in human judgments, which indicates that human annotation may not be a reliable gold standard. [2512.16041v1] (영어로 둠: 부정어 빠짐 — 번역은 「우리는 또한 인간 판단에 상당한 일관성 부재가 존재함을 발견했으며, 이는 인간 주석이 신뢰할 수 있는 금표준이 될 수 있음을 시사한다.」)

## R_139 — G-Eval처럼 생성 모델과 판정 모델이 같을 때 자기편향을 어떻게 측정하고, 인간 소표본은 몇 건이면 자동 판정을 보정할 수 있는가. 한국어 장문이면 그 수가 달라지는 논문이 있는가.

**지금 결론** (운영 · 9B v2 다시 쓰기 21.6s)

제공된 문서들은 G-Eval과 같은 생성·판정 모델이 동일한 경우 자기편향을 측정하는 방법과 인간 소표본을 이용한 보정 가능성에 대해 직접적인 결론을 제시하지 않습니다. [2404.13076v1]는 LLM 평가자가 자신의 출력보다 다른 출력을 더 높은 점수를 주는 자기 선호(self-preference) 현상을 보고, 이를 정밀 조정(fine-tuning)하여 자기 인식 능력과 자기 선호 편향 사이의 선형 상관관계를 발견했습니다. 또한 [2410.21819v2]은 낮은 불확실성(perplexity)을 보이는 출력을 인간 평가자보다 유의미하게 더 높은 점수로 평가한다는 결과를 제시하며, 이는 모델이 자신의 출력을 인식하는 메커니즘으로 해석됩니다. 한편 [2309.17012v3]는 LLM 평가자가 자체 출력을 선호하는 자기중심 편향(Egocentric bias)이 전체 비교 중 평균 40%에 달한다고 보고, 인간과 기계의 선호 일치도(RBO)가 49.6%로 낮아 불일치를 보인다고 지적합니다. 따라서 현재 연구들은 자기편향을 측정하고 인간 소표본으로 보정하는 구체적인 임계값이나 한국어 장문 데이터에 따른 차이를 제시하지 않으며, 이러한 세부 조건에 대한 추가 연구가 필요합니다.

**A 논문별 한 줄 · 영어 원문**

- LLM Evaluators Recognize and Favor Their Own Generations — By fine-tuning LLMs, we discover a linear correlation between self-recognition capability and the strength of self-preference bias; using controlled experiments, we show that the causal explanation resists straightforward confounders. [2404.13076v1]
- Self-Preference Bias in LLM-as-a-Judge — Our findings reveal that LLMs assign significantly higher evaluations to outputs with lower perplexity than human evaluators, regardless of whether the outputs were self-generated. [2410.21819v2]
- Benchmarking Cognitive Biases in Large Language Models as Evaluators — We find that LLMs are biased text quality evaluators, exhibiting strong indications on our bias benchmark (average of 40% of comparisons across all models) within each of their evaluations that question their robustness as evaluators. [2309.17012v3]

**B 논문별 한 줄 · 9B 번역만 (질문은 안 보여 줌)**

- LLM Evaluators Recognize and Favor Their Own Generations — LLM을 미세 조정함으로써 자기 인식 능력과 자기 선호 편향 강도 사이의 선형 상관관계를 발견했으며, 통제된 실험을 통해 인과적 설명이 단순한 교란 요인에 저항함을 보였다. [2404.13076v1]
- Self-Preference Bias in LLM-as-a-Judge — 우리의 연구 결과는 LLM이 인간 평가자보다 낮은 불확실성(perplexity)을 가진 출력에 대해 유의미하게 높은 평가를 부여한다는 점을 보여주며, 이러한 출력이 자체 생성되었든 그렇지 않든 관계없이 해당 현상이 관찰됩니다. [2410.21819v2]
- Benchmarking Cognitive Biases in Large Language Models as Evaluators — 우리는 LLM이 편향된 텍스트 품질 평가자임을 발견했으며, 각 모델의 모든 평가에서 편향 벤치마크(모든 모델에 걸친 비교 평균 40%)에서 강력한 징후를 보이며 이를 평가자의 견고성에 대한 의문을 제기한다. [2309.17012v3]

**C 혼합 — 인용 붙은 문장만 B 줄로**

- (그대로) 제공된 문서들은 G-Eval과 같은 생성·판정 모델이 동일한 경우 자기편향을 측정하는 방법과 인간 소표본을 이용한 보정 가능성에 대해 직접적인 결론을 제시하지 않습니다.
- (초록) LLM Evaluators Recognize and Favor Their Own Generations — LLM을 미세 조정함으로써 자기 인식 능력과 자기 선호 편향 강도 사이의 선형 상관관계를 발견했으며, 통제된 실험을 통해 인과적 설명이 단순한 교란 요인에 저항함을 보였다. [2404.13076v1]
- (초록) Self-Preference Bias in LLM-as-a-Judge — 우리의 연구 결과는 LLM이 인간 평가자보다 낮은 불확실성(perplexity)을 가진 출력에 대해 유의미하게 높은 평가를 부여한다는 점을 보여주며, 이러한 출력이 자체 생성되었든 그렇지 않든 관계없이 해당 현상이 관찰됩니다. [2410.21819v2]
- (초록) Benchmarking Cognitive Biases in Large Language Models as Evaluators — 우리는 LLM이 편향된 텍스트 품질 평가자임을 발견했으며, 각 모델의 모든 평가에서 편향 벤치마크(모든 모델에 걸친 비교 평균 40%)에서 강력한 징후를 보이며 이를 평가자의 견고성에 대한 의문을 제기한다. [2309.17012v3]
- (그대로) 따라서 현재 연구들은 자기편향을 측정하고 인간 소표본으로 보정하는 구체적인 임계값이나 한국어 장문 데이터에 따른 차이를 제시하지 않으며, 이러한 세부 조건에 대한 추가 연구가 필요합니다.

**D 바꿔 끼우기 — 인용 붙은 문장을 9B 문장과 가장 겹치는 원문 문장으로**

- (그대로) 제공된 문서들은 G-Eval과 같은 생성·판정 모델이 동일한 경우 자기편향을 측정하는 방법과 인간 소표본을 이용한 보정 가능성에 대해 직접적인 결론을 제시하지 않습니다.
- (원문) LLM Evaluators Recognize and Favor Their Own Generations — 이러한 편향 중 하나는 자기 선호도이며, LLM 평가자가 자신의 출력을 다른 것보다 더 높은 점수로 평가하는 반면 인간 주석가는 이를 동일한 품질로 판단한다. [2404.13076v1]
- (원문) Self-Preference Bias in LLM-as-a-Judge — 원인을 탐색하기 위해 우리는 LLM이 낮은 불확실성(perplexity)을 나타내는 더 익숙한 출력을 선호할 수 있다고 가정한다. [2410.21819v2]
- (원문) Benchmarking Cognitive Biases in Large Language Models as Evaluators — 우리는 LLM이 편향된 텍스트 품질 평가자임을 발견했으며, 각 모델의 모든 평가에서 편향 벤치마크(모든 모델에 걸친 비교 평균 40%)에서 강력한 징후를 보이며 이를 평가자의 견고성에 대한 의문을 제기한다. [2309.17012v3]
- (그대로) 따라서 현재 연구들은 자기편향을 측정하고 인간 소표본으로 보정하는 구체적인 임계값이나 한국어 장문 데이터에 따른 차이를 제시하지 않으며, 이러한 세부 조건에 대한 추가 연구가 필요합니다.

## N04 — 코드가 깔끔하면 코딩 에이전트가 토큰을 덜 쓴다는 연구 있던데 얼마나 줄었어?

**지금 결론** (운영 · 9B v2 다시 쓰기 13.8s)

제공된 문서에는 코드가 깔끔할 때 토큰 사용량이 감소한다는 연구 결과가 없습니다. [2610.08662v1]는 코드 에이전트에서 불필요한 위험 처리가 11.2%~58.7%의 실행에서 발생한다는 점을 보고하고 있으며, 이는 에이전트 구성에 따라 큰 차이가 있음을 보여줍니다. 또한 [2603.08993v1]는 LLM 에이전트 시스템 프롬프트에서 불필요한 요구사항이 작업 수행을 어렵게 하고 비용을 증가시킨다고 결론지었습니다. 따라서 두 논문 모두 불필요한 요소가 존재하면 성능이나 효율성이 저하된다는 공통된 인식을 가지고 있지만, 구체적인 토큰 감소 수치에 대한 언급은 없습니다.

**A 논문별 한 줄 · 영어 원문**

- Arbiter: Detecting Interference in LLM Agent System Prompts — One scourer finding was structural data loss in Gemini CLI's memory system was consistent with an issue filed and patched by Google, which addressed the symptom without addressing the schema-level root cause identified by the scourer. [2603.08993v1]
- ParanoiaEval: Benchmarking Unnecessary Defensive Work in Agentic Coding — Large-scale experiments on 8 representative models and a post-hoc human study reveal that (I) unnecessary risk treatment occurs in 11.2%-58.7% of runs despite explicit evidence, with substantial variation across agent configurations; (II) stronger task capability does not ensure more appropriate risk treatment, while treatment violations substantially harm developers' experience, establishing risk treatment as an independent capability dimension; and (III) agents exhibit systematic patterns consistent with established risk-management findings, suggesting that knowledge from human practice can guide the diagnosis and improvement of this capability. [2610.08662v1]

**B 논문별 한 줄 · 9B 번역만 (질문은 안 보여 줌)**

- Arbiter: Detecting Interference in LLM Agent System Prompts — 스커러가 발견한 구조적 데이터 손실은 구글이 보고하고 패치한 문제와 일치하지만, 스커러가 식별한 스키마 수준의 근본 원인은 해결하지 않고 증상만을 완화한 것으로 나타났다. [2603.08993v1]
- ParanoiaEval: Benchmarking Unnecessary Defensive Work in Agentic Coding — 대규모 실험과 사후 인간 연구는 명시적인 증거에도 불구하고 불필요한 위험 처리가 11.2%~58.7%의 실행에서 발생하며 에이전트 구성에 따라 큰 차이가 있음을 보여주며, (II) 더 강력한 작업 능력은 적절한 위험 처리를 보장하지 않지만 위반은 개발자의 경험을 크게 해치고 위험 처리를 독립적인 능력 차원으로 설정한다; 그리고 (III) 에이전트는 기존 위험 관리 연구와 일치하는 체계적인 패턴을 보여 인간 실무에서 얻은 지식이 이 능력의 진단과 개선을 안내할 수 있음을 시사한다. [2610.08662v1]

**C 혼합 — 인용 붙은 문장만 B 줄로**

- (그대로) 제공된 문서에는 코드가 깔끔할 때 토큰 사용량이 감소한다는 연구 결과가 없습니다.
- (초록) ParanoiaEval: Benchmarking Unnecessary Defensive Work in Agentic Coding — 대규모 실험과 사후 인간 연구는 명시적인 증거에도 불구하고 불필요한 위험 처리가 11.2%~58.7%의 실행에서 발생하며 에이전트 구성에 따라 큰 차이가 있음을 보여주며, (II) 더 강력한 작업 능력은 적절한 위험 처리를 보장하지 않지만 위반은 개발자의 경험을 크게 해치고 위험 처리를 독립적인 능력 차원으로 설정한다; 그리고 (III) 에이전트는 기존 위험 관리 연구와 일치하는 체계적인 패턴을 보여 인간 실무에서 얻은 지식이 이 능력의 진단과 개선을 안내할 수 있음을 시사한다. [2610.08662v1]
- (초록) Arbiter: Detecting Interference in LLM Agent System Prompts — 스커러가 발견한 구조적 데이터 손실은 구글이 보고하고 패치한 문제와 일치하지만, 스커러가 식별한 스키마 수준의 근본 원인은 해결하지 않고 증상만을 완화한 것으로 나타났다. [2603.08993v1]
- (그대로) 따라서 두 논문 모두 불필요한 요소가 존재하면 성능이나 효율성이 저하된다는 공통된 인식을 가지고 있지만, 구체적인 토큰 감소 수치에 대한 언급은 없습니다.

**D 바꿔 끼우기 — 인용 붙은 문장을 9B 문장과 가장 겹치는 원문 문장으로**

- (그대로) 제공된 문서에는 코드가 깔끔할 때 토큰 사용량이 감소한다는 연구 결과가 없습니다.
- (원문) ParanoiaEval: Benchmarking Unnecessary Defensive Work in Agentic Coding — 대규모 실험과 사후 인간 연구는 명시적인 증거에도 불구하고 불필요한 위험 처리가 11.2%~58.7%의 실행에서 발생하며 에이전트 구성에 따라 큰 차이가 있음을 보여주며, (II) 더 강력한 작업 능력은 적절한 위험 처리를 보장하지 않지만 위반은 개발자의 경험을 크게 해치고 위험 처리를 독립적인 능력 차원으로 설정한다; 그리고 (III) 에이전트는 기존 위험 관리 연구와 일치하는 체계적인 패턴을 보여 인간 실무에서 얻은 지식이 이 능력의 진단과 개선을 안내할 수 있음을 시사한다. [2610.08662v1]
- (원문) Arbiter: Detecting Interference in LLM Agent System Prompts — 우리는 시스템 프롬프트 내 간섭 패턴을 탐지하기 위해 형식적 평가 규칙과 다중 모델 LLM 스쿠어링을 결합한 Arbiter 프레임워크를 제시한다. [2603.08993v1]
- (그대로) 따라서 두 논문 모두 불필요한 요소가 존재하면 성능이나 효율성이 저하된다는 공통된 인식을 가지고 있지만, 구체적인 토큰 감소 수치에 대한 언급은 없습니다.

## C08 — RAG에 프롬프트 인젝션 공격하는 DeRAG랑, 브라우저 에이전트를 인젝션에서 막는 Cognitive Firewall 비교해줘

**지금 결론** (운영 · 9B v2 다시 쓰기 18.8s)

DeRAG와 Cognitive Firewall은 모두 프롬프트 인젝션과 관련된 연구이지만 목적에 차이가 있습니다: DeRAG는 RAG 시스템의 취약점을 이용해 공격 성공률을 높이는 데 초점을 맞추고, 반면 Cognitive Firewall은 브라우저 에이전트에서 간접 프롬프트 인젝션을 효과적으로 차단하는 방어 메커니즘을 제공합니다. 따라서 두 접근법은 각각 “공격”과 “방어”라는 반대 목표를 달성하기 위해 설계된 시스템입니다.

**A 논문별 한 줄 · 영어 원문**

- DeRAG: Black-box Adversarial Attacks on Multiple Retrieval-Augmented Generation Applications via Prompt Injection — Through evaluations with a BERT-based adversarial suffix detector, we show that DE-generated suffixes evade detection, yielding near-chance detection accuracy. [2507.15042v1]
- The Cognitive Firewall:Securing Browser Based AI Agents Against Indirect Prompt Injection Via Hybrid Edge Cloud Defense — By filtering presentation-layer attacks locally, the system avoids unnecessary cloud inference and achieves an approximately 17,000x latency advantage over cloud-only baselines. [2603.23791v1]

**B 논문별 한 줄 · 9B 번역만 (질문은 안 보여 줌)**

- DeRAG: Black-box Adversarial Attacks on Multiple Retrieval-Augmented Generation Applications via Prompt Injection — BERT 기반 적대적 접미어 탐지기로 평가한 결과, DE가 생성한 접미어는 탐지를 회피하여 거의 우연 수준의 탐지 정확도를 보인다는 것을 보여준다. [2507.15042v1]
- The Cognitive Firewall:Securing Browser Based AI Agents Against Indirect Prompt Injection Via Hybrid Edge Cloud Defense — 프레젠테이션 레이어 공격을 로컬에서 필터링함으로써 불필요한 클라우드 추론을 피하고, 클라우드 전용 베이스라인 대비 약 17,000배의 지연 시간 우위를 달성한다. [2603.23791v1]

**C 혼합 — 인용 붙은 문장만 B 줄로**

- (그대로) DeRAG와 Cognitive Firewall은 모두 프롬프트 인젝션과 관련된 연구이지만 목적에 차이가 있습니다: DeRAG는 RAG 시스템의 취약점을 이용해 공격 성공률을 높이는 데 초점을 맞추고, 반면 Cognitive Firewall은 브라우저 에이전트에서 간접 프롬프트 인젝션을 효과적으로 차단하는 방어 메커니즘을 제공합니다.
- (그대로) 따라서 두 접근법은 각각 “공격”과 “방어”라는 반대 목표를 달성하기 위해 설계된 시스템입니다.

**D 바꿔 끼우기 — 인용 붙은 문장을 9B 문장과 가장 겹치는 원문 문장으로**

- (그대로) DeRAG와 Cognitive Firewall은 모두 프롬프트 인젝션과 관련된 연구이지만 목적에 차이가 있습니다: DeRAG는 RAG 시스템의 취약점을 이용해 공격 성공률을 높이는 데 초점을 맞추고, 반면 Cognitive Firewall은 브라우저 에이전트에서 간접 프롬프트 인젝션을 효과적으로 차단하는 방어 메커니즘을 제공합니다.
- (그대로) 따라서 두 접근법은 각각 “공격”과 “방어”라는 반대 목표를 달성하기 위해 설계된 시스템입니다.

## N11 — AI가 사람 스킬 수요를 늘리는지 채용공고로 분석한 연구에서, 회복탄력성 같은 스킬 있는 데이터 과학자는 연봉을 몇 % 더 받는대?

**지금 결론** (운영 · 9B v2 다시 쓰기 10.6s)

제공된 문서에 따르면, 회복탄력성(resilience)을 갖춘 데이터 과학자는 연봉이 5~10% 더 높은 것으로 보고된다[2412.19754v3]. 이는 AI 수요가 증가함에 따라 보완적 스킬을 가진 인재에게 임금 프리미엄이 발생한다는 연구 결과와 일치한다. 따라서 AI는 회복탄력성 같은 인간 스킬의 수요를 늘리고, 해당 스킬을 보유한 데이터 과학자에게 상당한 연봉 상승 효과를 제공한다.

**A 논문별 한 줄 · 영어 원문**

- Complement or substitute? How AI increases the demand for human skills — We observe positive spillover effects: a doubling of AI-specific demand across industries correlates with a 5% increase in demand for complementary skills, even outside AI-related roles. [2412.19754v3]
- Complement or substitute? How AI increases the demand for human skills — We observe positive spillover effects: a doubling of AI-specific demand across industries correlates with a 5% increase in demand for complementary skills, even outside AI-related roles. [2412.19754v3]

**B 논문별 한 줄 · 9B 번역만 (질문은 안 보여 줌)**

- Complement or substitute? How AI increases the demand for human skills — 우리는 산업 전반에 걸친 AI 특화 수요가 두 배로 증가하면 보완적 기술에 대한 수요가 5% 상승하는 긍정적인 파급 효과를 관찰한다: 이는 AI 관련 직무 밖에서도 이러한 현상이 나타난다. [2412.19754v3]
- Complement or substitute? How AI increases the demand for human skills — 우리는 산업 전반에 걸친 AI 특화 수요가 두 배로 증가하면 보완적 기술에 대한 수요가 5% 상승하는 긍정적인 파급 효과를 관찰한다: 이는 AI 관련 직무 밖에서도 이러한 현상이 나타난다. [2412.19754v3]

**C 혼합 — 인용 붙은 문장만 B 줄로**

- (초록) Complement or substitute? How AI increases the demand for human skills — 우리는 산업 전반에 걸친 AI 특화 수요가 두 배로 증가하면 보완적 기술에 대한 수요가 5% 상승하는 긍정적인 파급 효과를 관찰한다: 이는 AI 관련 직무 밖에서도 이러한 현상이 나타난다. [2412.19754v3]
- (그대로) 이는 AI 수요가 증가함에 따라 보완적 스킬을 가진 인재에게 임금 프리미엄이 발생한다는 연구 결과와 일치한다.
- (그대로) 따라서 AI는 회복탄력성 같은 인간 스킬의 수요를 늘리고, 해당 스킬을 보유한 데이터 과학자에게 상당한 연봉 상승 효과를 제공한다.

**D 바꿔 끼우기 — 인용 붙은 문장을 9B 문장과 가장 겹치는 원문 문장으로**

- (원문) Complement or substitute? How AI increases the demand for human skills — 또한 이러한 기술들은 상당한 임금 프리미엄을 제공하며, 예를 들어 회복력이나 윤리 능력을 추가로 갖춘 데이터 과학자들은 5~10% 더 높은 연봉을 받는다. [2412.19754v3]
- (그대로) 이는 AI 수요가 증가함에 따라 보완적 스킬을 가진 인재에게 임금 프리미엄이 발생한다는 연구 결과와 일치한다.
- (그대로) 따라서 AI는 회복탄력성 같은 인간 스킬의 수요를 늘리고, 해당 스킬을 보유한 데이터 과학자에게 상당한 연봉 상승 효과를 제공한다.

## C09 — MoE-Mamba랑 BlackMamba는 둘 다 Mamba에 MoE 붙인 건데 뭐가 달라?

**지금 결론** (운영 · 9B v2 다시 쓰기 10.9s)

MoE-Mamba는 Mamba와 동일한 성능을 달성하기 위해 2.35배 적은 학습 단계를 필요로 한다[2401.04081v2]. BlackMamba는 Mamba와 Transformer 기반 모델에 비해 추론 및 학습 FLOPs에서 더 나은 성능을 보이며, SSM과 MoE의 이점을 결합한다[2402.01771v1]. 두 방법 모두 Mamba에 MoE를 적용한 것이지만, 학습 효율성과 전체적인 FLOPs 측면에서 BlackMamba가 더 큰 이점을 제공한다.

**A 논문별 한 줄 · 영어 원문**

- MoE-Mamba: Efficient Selective State Space Models with Mixture of Experts — In particular, MoE-Mamba reaches the same performance as Mamba in $2.35\times$ fewer training steps while preserving the inference performance gains of Mamba against Transformer. [2401.04081v2]
- BlackMamba: Mixture of Experts for State-Space Models — We show that BlackMamba inherits and combines both of the benefits of SSM and MoE architectures, combining linear-complexity generation from SSM with cheap and fast inference from MoE. [2402.01771v1]

**B 논문별 한 줄 · 9B 번역만 (질문은 안 보여 줌)**

- MoE-Mamba: Efficient Selective State Space Models with Mixture of Experts — 특히 MoE-Mamba는 Mamba의 추론 성능 향상을 유지하면서, Transformer 대비 Mamba의 성능을 동일한 수준으로 달성하기 위해 필요한 학습 단계를 2.35배 줄였습니다. [2401.04081v2]
- BlackMamba: Mixture of Experts for State-Space Models — BlackMamba 가 SSM 과 MoE 구조의 장점을 모두 계승·결합하여, SSM 의 선형 복잡도 생성과 MoE 의 저렴하고 빠른 추론을 결합한다는 것을 보여줍니다. [2402.01771v1]

**C 혼합 — 인용 붙은 문장만 B 줄로**

- (초록) MoE-Mamba: Efficient Selective State Space Models with Mixture of Experts — 특히 MoE-Mamba는 Mamba의 추론 성능 향상을 유지하면서, Transformer 대비 Mamba의 성능을 동일한 수준으로 달성하기 위해 필요한 학습 단계를 2.35배 줄였습니다. [2401.04081v2]
- (초록) BlackMamba: Mixture of Experts for State-Space Models — BlackMamba 가 SSM 과 MoE 구조의 장점을 모두 계승·결합하여, SSM 의 선형 복잡도 생성과 MoE 의 저렴하고 빠른 추론을 결합한다는 것을 보여줍니다. [2402.01771v1]
- (그대로) 두 방법 모두 Mamba에 MoE를 적용한 것이지만, 학습 효율성과 전체적인 FLOPs 측면에서 BlackMamba가 더 큰 이점을 제공한다.

**D 바꿔 끼우기 — 인용 붙은 문장을 9B 문장과 가장 겹치는 원문 문장으로**

- (원문) MoE-Mamba: Efficient Selective State Space Models with Mixture of Experts — 특히 MoE-Mamba는 Mamba의 추론 성능 향상을 유지하면서, Transformer 대비 Mamba의 성능을 동일한 수준으로 달성하기 위해 필요한 학습 단계를 2.35배 줄였습니다. [2401.04081v2]
- (원문) BlackMamba: Mixture of Experts for State-Space Models — 본 논문에서는 Mamba 상태공간 모델(SSM)과 MoE를 결합한 새로운 구조인 BlackMamba를 제시하여 두 접근법의 장점을 모두 확보한다. [2402.01771v1]
- (그대로) 두 방법 모두 Mamba에 MoE를 적용한 것이지만, 학습 효율성과 전체적인 FLOPs 측면에서 BlackMamba가 더 큰 이점을 제공한다.

번역 호출 17번 총 65.7s (모델 yunsur_v13)
