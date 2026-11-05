# jeff_1105: 로컬 결정 모델 `jeff` 오프라인 측정 (dev)

> 측정 **전에** 쓴다. dev 전용이고 운영을 바꾸지 않는다. 사용자 결정(11-05): `Jev` 컨셉을 개발용으로 따로 빼서 지금 시험한다. 진짜 `Jev` 는 키가 없어 같은 API 를 구현한 로컬 서버 `jeff` 로 먼저 잰다.

## 1. 왜

- 지금 손실이 큰 곳은 거르기와 판정이다. 9B 거르기는 상위 5편에서 정밀도 49.3% · 재현율 82.6% 이고, 판정 '없음' 22건 중 11건이 거짓이었다.
- 문서마다 따로 판정하는 안은 호출이 1번에서 15번으로 늘어 9B 로는 미뤘다(`filter_input_1104`). 결정 모델은 문서마다 예/아니오 확률만 내므로 이 자리에 맞다.
- `Jev` 는 가중치가 비공개라 로컬로 못 돌린다. `jeff`(`logan-markewich/jeff`, MIT)는 같은 `POST /v1/systemone` 을 `GLiFormer`(`knowledgator/gliformer-large-v1`, 400M 파라미터)로 구현한다.
- **사전 정보:** `jeff` 저장소가 옮긴 JevBench v1.2.2 공식 실행에서 judge 61.6%(Jev 94.5%) · hard 37.7%(Jev 74.1%)다. 모델 카드는 영어 과제만 평가했다고 밝히는데 우리 질문은 한국어다. 미달할 가능성이 크다. **`jeff` 미달은 `Jev` 미달의 근거가 아니다.**

## 2. 분리

- 코드 · venv · 가중치는 맥미니 내장 `~/dev/jeff_1105/` 에 둔다. 저장소에 넣지 않는다. 코드 커밋 `34b32f99`, 가중치 리비전은 `models/gliformer-large-v1.revision`, 패키지는 `logs/pip_freeze.txt` 에 남긴다.
- 서버는 `127.0.0.1:8090` 에서만 받고, `.env` 없는 깨끗한 환경으로 띄우며, `HF_HUB_OFFLINE=1` 이다. launchd 에 등록하지 않고 측정이 끝나면 끈다.
- 운영 `.venv` 는 평가 스크립트 실행에만 쓰고 패키지를 더하지 않는다. `.env` · 봇 코드는 바꾸지 않고 **Chroma 호출은 0** 이다. 입력은 저장된 파일뿐이다.
- `pytorch_model.bin` 은 pickle 이라 불러오기 전에 `check_weights.py` 로 import 목록을 본다. 허용 목록 밖이 하나라도 있으면 중단한다. `gliformer` 로더 코드도 실행 전에 읽는다.
- 메모리 보호: 스크립트가 25건마다 여유 메모리와 스왑을 본다. 여유가 12% 미만이면 기다리고, 스왑이 6GB 를 넘으면 멈춘다(이어 하기 가능).
- 실사용 질문은 `SYS1_URL` 이 로컬일 때만 쓰고, 결과에는 해시만 남긴다.

## 3. 입력과 질문 (측정 전 고정)

`noul` 질문 하나를 세 자리 중 거르기 · 판정에 함께 쓴다. 문구는 [`run.py`](run.py) 의 `INSTR` · `CRIT` 이고, 판정 `OPEN_TAIL` 의 뜻을 옮겼다.

```
Does this paper mainly address the topic of the request below? Request: {요청}
true: the paper's main subject is this topic, even if its methods or wording differ
false: it only shares some words or the broad field, and its main subject is a different problem
```

**문턱은 `noul ≥ 0.5` 로 고정한다.** `jeff` 의 온도 보정은 0.5 를 넘는지 여부를 바꾸지 않는다.

| 자리 | 입력 | 결정 |
|---|---|---|
| 거르기 | `topic_filter_1104/pool_hu.jsonl` 116줄의 상위 5편 = 580건. 요청은 주제 줄 `line`(모두 영어), 문서는 9B 와 같은 `_brief`(제목 + 본문 600자) | 0.5 이상 남김. 9B 와 같은 후처리: 하나도 안 남으면 5편 유지, 질문 속 고유 이름이 제목에 든 문서 보호 |
| 판정 K (주 지표) | `open_judge_1103/oj_dev.jsonl` 167문항의 저장 컨텍스트 문서 전부. 요청은 한국어 질문 원문, 문서는 9B 가 본 블록 그대로 | 0.5 이상이 하나도 없으면 '없음' |
| 판정 E (보고) | 같은 문항. 요청만 저장된 영어 검색어 `rag_queries` | K 와 같음. K 가 결정당 중앙 1.5초를 넘으면 라벨 달린 33문항만 |
| 분기 (보고) | 합성 25(`router_open_1103/proto.py` 의 지킬 17 · RAG 8), real40 중 RAG 경로 34, 실사용 고유 71 | `choice` 4갈래(`paper_research` · `chat` · `tool` · `coding`) |

새 라벨은 달지 않는다. 라벨은 기존 `labels_hu.tsv` · `labels_pool.tsv` · `open_judge_1103/labels*.tsv` 를 그대로 쓴다. held-out 은 쓰지 않는다.

## 4. 기준 (측정 전 고정)

| 지표 | 기준 | 9B |
|---|---|---|
| 거르기 정밀도 | ≥ 60% (`newmac_1105` §6.2) | 49.3% |
| 거르기 재현율 | ≥ 78% | 82.6% |
| 판정 G1 F 회복 | ≥ 70% (`open_judge_1103`) | `oj_dev.jsonl` 에서 다시 계산 |
| 판정 G2 T · ? 중 '없음' 아님 | ≤ 20% | 같음 |
| 판정 G3 저장 문서 중 새 '없음' | ≤ 3 | 같음 |

보고만 한다: 거르기 AUC, 문턱별 정밀도 · 재현율, 결정당 시간, 서버 메모리, 스왑 변화, 분기 일치율, 판정 E.

## 5. 결정 규칙

- **거르기 · 판정 K 둘 다 통과:** `jeff` 를 꺼 둔 플래그로 거르기 자리에 붙여 `eval_e2e_ko.py` dev 라운드를 따로 사전 등록한다.
- **하나라도 미달:** `jeff` 는 운영 후보에서 뺀다. `run.py` 는 진짜 `Jev` · 새 맥미니 비교에 그대로 쓴다.
- 문턱이나 문구를 바꾸면 통과하더라도 같은 데이터로 통과 처리하지 않고 힌트로만 적는다.
- E 만 통과하면 언어 문제로 적고, 결정은 K 기준으로 한다.
- 운영 변화는 어느 경우에도 없다.

## 6. 한계

이미 여러 라운드에서 본 dev 라벨이고, 라벨은 Claude 한 명이 달았다. 거르기 입력은 영어 주제 줄이라 운영의 한국어 질문과 다르다. 판정 라벨은 저장 '없음' 33문항뿐이라 G1 · G2 표본이 작다(F 23 · T 3 · ? 7).

## 7. 결과

(측정 뒤에 쓴다)
