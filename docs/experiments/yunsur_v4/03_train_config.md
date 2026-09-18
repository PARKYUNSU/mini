# 03. 학습 설정 · 기록

원칙: **v3와 하이퍼파라미터를 완전히 동일하게** 두고 데이터만 바꾼다. 차이가 나오면 데이터 재설계의 효과로 귀속할 수 있다.

## 고정 설정 (v3 = v4)

| 항목 | 값 |
|---|---|
| 베이스 | `Qwen/Qwen3.5-9B` (transformers ≥ 5.2.0, `qwen3_5`) |
| 방법 | Unsloth + TRL `SFTTrainer`, LoRA |
| LoRA | r=16, α=32, dropout 0, target = q/k/v/o + gate/up/down, gradient checkpointing "unsloth" |
| 템플릿 | ChatML (`<\|im_start\|>system/user/assistant`), `train_on_responses_only` — assistant 토큰만 손실 |
| 옵티마이저 | adamw_8bit, lr 2e-4, linear, warmup 10, weight_decay 0.01 |
| 배치 | per_device 1 × grad_accum 8 (유효 배치 8) |
| epoch | 1 |
| 정밀도 | bf16 (지원 시) / fp16 |
| max_seq_length | 2048, packing off |
| seed | 3407 |
| 양자화 배포 | GGUF q4_k_m → Ollama (`Modelfile.v4`). **주의**: 운영 중이던 v3(`yunsur_v3:latest`)는 q8_0(9.5GB)였음 → 공정 비교를 위해 v3 f16에서 q4_k_m(`yunsur_v3_q4`)을 추가 생성해 재측정 |

## v3와 다른 것 (데이터뿐)

| | v3 | v4 |
|---|---|---|
| 파일 | `train_data_v3_clean.jsonl` | `finetune_datasets/v4/train_data_v4.jsonl` |
| 건수 | 1,073 | 1,099 |
| 슬롯 | RAG 100% | RAG 36% / 잡담 32% / 계획 23% / 코딩 9% |
| system | 노트북 `SYSTEM_PERSONA` 단일 덮어쓰기 | 레코드별 `system` = 운영 프롬프트 4종 |
| 노트북 | `yunsur_v3_unsloth_finetune.ipynb` | `finetune_datasets/v4/yunsur_v4_unsloth_finetune.ipynb` (변경 셀: 0·7·13·14·20·22) |

## 실행 절차 (RunPod)

1. `train_data_v4.jsonl` + `yunsur_v4_unsloth_finetune.ipynb`를 같은 작업 폴더에 업로드
2. 설치 셀 → **커널 재시작** → 검증 셀부터 순서대로
3. 데이터 로드 셀 출력에서 아래 표의 "데이터" 항목을 옮겨 적기 (슬롯 분포 / system 4종 / 토큰 길이 / 잘림 수)
4. 학습 셀이 끝나면 `yunsur_v4_train_log.json`이 생성됨 — 노트북과 함께 다운로드
5. 저장 셀 → GGUF 셀 (실패 시 `yunsur_v4_model/`만 받아 맥에서 llama.cpp 변환)
6. 맥미니: GGUF를 `/Volumes/T7 Shield/yunsur_v4-q4_k_m.gguf`로 두고 `ollama create yunsur_v4 -f Modelfile.v4`

## 실행 기록 (2026-09-18)

| 항목 | 값 |
|---|---|
| 실행일 | 2026-09-18 (RunPod On-Demand) |
| GPU · VRAM | NVIDIA L40S 48GB · 컨테이너 `runpod/pytorch:2.4.0-py3.11-cuda12.4.1` |
| 데이터: 샘플 수 / 슬롯 분포 / system 종류 | 1,099 / chat 350 · planner 249 · coding 100 · rag 400 / 4 |
| 토큰 길이 중앙값 / p95 / max / 잘림 수 | 678 / 1,302 / 1,776 / 0 (max_seq 2048) |
| 총 step | 138 (1,099 ÷ 유효배치 8) |
| loss 시작 → 끝 (logging_steps=10) | 1.748 → 1.201 (step 10 → 130), 평균 1.353 |
| 학습 소요 시간 | 11분 16초 (`train_runtime` 676s, 1.63 samples/s) |
| 비용 | (RunPod 청구액 기입) |
| GGUF 변환 경로 | Pod: 볼륨 20GB 부족으로 `save_pretrained_gguf` 실패 → 어댑터(107MB)만 회수 → 맥미니 `convert_lora_to_gguf.py` (f16, 256 텐서) → **Ollama `FROM qwen3.5:9b` + `ADAPTER`** (머지 없이 런타임 적용). 최초 `llama-export-lora` 머지는 베이스 파일 오인으로 폐기(05 참조) |
| Ollama 등록 확인 | `yunsur_v4:latest` (Modelfile.v4) |

loss 추이 (step: loss): 10: 1.748 · 20: 1.515 · 30: 1.437 · 40: 1.295 · 50: 1.399 · 60: 1.351 · 70: 1.322 · 80: 1.283 · 90: 1.291 · 100: 1.175 · 110: 1.341 · 120: 1.235 · 130: 1.201

원본: [`yunsur_v4_train_log.json`](yunsur_v4_train_log.json)
