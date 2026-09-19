# 실험 노트 — yunsur_v5: 계획·코딩 데이터 보강으로 "base 초과" 재도전

- 시작일: 2026-09-19
- 선행 실험: [`../yunsur_v4/`](../yunsur_v4/) — 데이터 재설계로 v3 26% → v4 17%, RAG만 base 초과(0% vs 12%). **부분 통과**.
- 베이스 모델: `Qwen/Qwen3.5-9B` (Ollama `qwen3.5:9b`). **배포는 머지**: 2026-09-19 재설치된 Ollama가 `ADAPTER`를 거부("LoRA adapters are no longer supported") → HF 베이스를 직접 bf16 GGUF로 만들어 머지 후 q4_k_m, TEMPLATE/PARAMETER는 공식 `qwen3.5:9b`에서 복사 ([`scripts/merge_lora_gguf.sh`](../../../scripts/merge_lora_gguf.sh))
- 비교 대상: `yunsur_v5` / `yunsur_v4_merged` / `yunsur_v3_q4` / `qwen3.5:9b` — **4모델을 같은 밤에 재측정** (v4는 v5와 같은 머지·양자화 경로로 재생성한 것. 운영 중인 어댑터 방식 `yunsur_v4`는 참고로 병기)
- 측정 도구: [`scripts/eval_local_llm_failure.py`](../../../scripts/eval_local_llm_failure.py) `--repeats 3 --quality` — 고정 30문항 × 3회 (n=90), 로컬 1차 호출만, API 폴백 없음
- 실패 정의: v4와 동일 (hard = 타임아웃/빈 답/계획 파싱 실패/코드 문법·실행 오류, quality = 영어 혼입 >45%/think 유출/반복/잡담 코드 펜스/코딩 형식 드리프트). 보고 숫자는 **strict(hard+quality)**, hard는 괄호 병기.

## 1. 문제 정의

v4의 실패 15건(`../yunsur_v4/05_conclusion.md`)은 원인이 분명했다.

| 슬롯 | v4 실패 | 원인 진단 | v5 조치 |
|---|---|---|---|
| 플래너 33% (8건 parse_fail) | Tavily·pandas·FastAPI 같은 **개발 도구 요청**에서 `N단계:` 번호를 빼고 산문으로 씀 | 학습 계획 샘플 249건이 크롤링·파일·스케줄 위주, 단계 수 98%가 2~3단계 | 계획 250→**400**, 개발 도구 시드(API 서버·데이터 조인·검색 도구·DB) + **4~5단계 시드** 추가 |
| 코딩 28% (5건) | 코드 안에 긴 한국어 주석 → 토큰 상한(800)에서 잘림 | 코딩 샘플 100건(9%)은 너무 적고, 주석 습관을 못 눌렀음 | 코딩 100→**300**, **주석 비율 >30% 거절** 필터 |
| 잡담 8% (2건) | "회의록 마크다운 템플릿" 요청에 ```markdown 펜스 | 합리적 답변인데 판정기가 실패로 봄 (경계 사례) | 템플릿/표 요청은 생성 필터·평가 판정기 모두 **펜스 허용 예외** |
| RAG 0% | — | 400건이 반복 붕괴를 억제함 (효과 확인) | **400 유지** |

## 2. 가설

- H1: 계획 슬롯의 실패는 **커버리지**(개발 도구 요청 부재) 문제다 → 시드 보강만으로 parse_fail이 base 수준(≤ +5%p)으로 내려간다.
- H2: 코딩 슬롯의 실패는 **주석 습관**을 학습한 것이다 → 주석 비율 필터 + 3배 샘플로 잘림·문법 오류가 사라진다.
- H3: 잡담·RAG는 v4 수준을 유지한다 (데이터 비중이 바뀌어도 나빠지지 않는다).

하이퍼파라미터는 v3 = v4 = v5로 **완전히 고정**한다 (LoRA r16/α32, lr 2e-4, 1 epoch, seq 2048, adamw_8bit, seed 3407). 총 건수는 ≈1,400으로 v4(1,099)보다 27% 많아지므로, 효과가 나오면 "슬롯 비중 + 필터"와 "양 증가"가 섞인 것임을 인정하고 기록한다. 양만의 효과를 분리하는 것은 v5 범위 밖.

## 3. 성공 기준 (사전 선언 — 결과를 본 뒤 바꾸지 않는다)

같은 30문항 × 3회, 같은 프롬프트, 4모델(v5 / v4 / v3_q4 / base)을 같은 밤에 재측정한 결과에서:

- **통과**: yunsur_v5가 **모든 슬롯**에서 base 대비 strict 실패율 **+5%p 이내**이고, **RAG 슬롯**에서는 base보다 **낮다**. (v4와 동일 기준)
- **부분 통과**: 플래너와 코딩이 **모두 v4 대비 절반 이하**로 개선되고(플래너 ≤16%, 코딩 ≤14%), 잡담·RAG가 v4보다 나빠지지 않음 → "H1·H2 유효, base 초과는 미달"로 기록.
- **실패**: 어느 슬롯이든 v4보다 **+5%p 이상 악화** → 원인 분석 후 기록. 운영 모델은 현행(base + RAG만 v4) 유지.

판정 예외(사전 선언): 잡담 `code_fence_in_chat`은 **요청 문장에 "템플릿·표·양식·서식·마크다운" 중 하나가 있으면 실패로 세지 않는다.** 이 예외는 4모델에 동일하게 적용한다 (판정기 수정 → 4모델 모두 재측정이므로 공정).

속도(중앙값)는 판정 기준에 넣지 않되 표에 병기한다.

## 4. 데이터 설계

→ [`02_data_design.md`](02_data_design.md) (생성 완료 후 실제 분포·거절률로 채움)

| 슬롯 | v4 | **v5 목표** | 출처 | 새 규칙 |
|---|---|---|---|---|
| RAG | 400 | **400** | `train_data_v3_clean.jsonl` 무작위 샘플 (v4와 같은 seed → 같은 샘플) | 없음 |
| 잡담 | 350 | **300** | 베이스 자기 증류 | 템플릿/표 요청은 펜스 허용 |
| 계획 | 249 | **400** | 베이스 자기 증류 | 개발 도구·4~5단계 시드, 단계 수 분포 기록 |
| 코딩 | 100 | **300** | 베이스 자기 증류 | 주석 비율 >30% 거절, 코드 300줄 이하 |
| 합계 | 1,099 | **≈1,400** | | |

생성: [`scripts/gen_v5_dataset.py`](../../../scripts/gen_v5_dataset.py), 시드: [`finetune_datasets/v5/seeds/`](../../../finetune_datasets/v5/seeds/). 평가 30문항과 유사도 ≥0.72인 시드·증폭 문장은 자동 제외 (v4와 동일).

## 5. 학습

→ [`03_train_config.md`](03_train_config.md)

노트북 대신 스크립트: [`scripts/train_lora.py`](../../../scripts/train_lora.py) (v4 노트북 셀 순서 그대로, 하이퍼파라미터 상수 고정) → RunPod 시작 명령 [`scripts/runpod_train.sh`](../../../scripts/runpod_train.sh) (clone → 설치 → 학습 → HF Hub private 업로드 → Pod 자동 종료).
Pod 사양: **L40S 48GB, 볼륨 50GB** (v4 때 20GB로 GGUF 실패). GGUF 변환은 Pod에서 하지 않고 맥미니 `scripts/merge_lora_gguf.sh v5` (HF 베이스 다운로드 → bf16 GGUF → `general.name` 검증 → LoRA 머지 → q4_k_m → `Modelfile.v5` 생성 → 등록). v4도 같은 스크립트로 재생성해야 4모델이 같은 베이스·템플릿·양자화가 된다 (`merge_lora_gguf.sh v4`).

## 6. 재측정 · 결론

→ `04_eval_v5/`, `05_conclusion.md` (측정 후 작성)

## 체크리스트

- [ ] 시드 작성 (`finetune_datasets/v5/seeds/`) — 계획 60+ / 코딩 60+ / 잡담 30+, 저장 후 `grep -cvE '^\s*(#|$)'`로 줄 수 확인
- [x] 맥미니: `gen_v5_dataset.py --import-v4-raw --limit 3` 스모크 (v4 raw 흡수 후 1,047건 조립, 소급 거절 22: `comment_heavy` 7·한자 13·기타 2, 코딩 주석 p95 0.42→0.13)
- [x] 본 실행 → 1,400건 (계획 +151 / 코딩 +207 신규). [`02_data_design.md`](02_data_design.md) 기입
- [ ] 평가 판정기 잡담 펜스 예외 (`eval_local_llm_failure.py`) — 4모델 재측정 전에 반영
- [ ] `git push` (v5 데이터 포함 — `.gitignore`에 `!finetune_datasets/v5/` 있음)
- [ ] RunPod Secret `HF_TOKEN`(write) · HF private 모델 레포 생성 · (레포가 private이면) Secret `GH_TOKEN`
- [ ] RunPod MCP로 Pod 생성 (L40S, 볼륨 50GB, 시작 명령 `scripts/runpod_train.sh`)
- [ ] 맥미니: `huggingface-cli download $HF_REPO --local-dir "/Volumes/T7 Shield/yunsur_v5_hub"` → `bash scripts/merge_lora_gguf.sh v5` (베이스 `general.name` 검증 포함)
- [x] 기존 `yunsur_v4`(ADAPTER 방식) Ollama 0.34.2에서 어댑터 적용 확인 (temperature 0·seed 고정 A/B에서 base와 출력 상이) → 운영 유지
- [x] 공정 비교용 `merge_lora_gguf.sh v4` → `yunsur_v4_merged` 등록(2026-09-19, 5.8GB). temp 0·seed 고정 A/B: base와 상이, 어댑터판 v4와 첫 문장 거의 동일 → 머지 적용 확인. 재측정 4모델 = v5 / v4_merged / v3_q4 / base, 참고로 v4(어댑터) 병기
- [ ] 4모델 같은 밤 재측정 (`scripts/eval_v5_all.sh`) → 05_conclusion.md

## 진행 로그

| 날짜 | 내용 |
|---|---|
| 2026-09-19 | 본 생성 완료 1,400건 (17:49→19:50). 개발 도구 커버리지 24%→62%(신규분), 코딩 주석 p95 0.42→0.16. 4~5단계 계획은 실패(38건 중 1건) — 자기 증류 한계로 기록. |
| 2026-09-19 | 스모크 통과. HF 베이스 원본 다운로드 → `llm/Qwen3.5-9B-base.BF16.gguf`(진짜 베이스, 공용) → `yunsur_v4_merged` 등록·A/B 검증. |
| 2026-09-19 | Ollama brew 재설치 후 4모델 존재 확인. 그러나 `ollama create -f Modelfile.v4` → "LoRA adapters are no longer supported" — 배포 방식을 ADAPTER → 머지로 변경, `scripts/merge_lora_gguf.sh` 작성. |
| 2026-09-19 | v4 운영 반영 완료(base + RAG만 v4). v5 실험 노트 개설, 성공 기준 선언. `gen_v5_dataset.py`·시드 초안·`train_lora.py`·`runpod_train.sh` 작성. 시드 chat 43 / planner 72 / coding 73 (평가 유사도 최대 0.59, 제외 0). v5 필터를 v4 raw에 소급 시험: 코딩 100건 중 `comment_heavy` 7건(주석 비율 p95 0.42), v4 계획 단계 수 분포 2:19 / 3:235 / 4:4 / 5:1 — 4~5단계 시드 필요성 확인. |
