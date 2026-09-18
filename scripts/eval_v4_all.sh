#!/bin/bash
# yunsur_v4 실험 9단계: 세 모델을 같은 프로토콜로 연속 재측정
#   같은 30문항 × 3회, 같은 프롬프트(2026-09-18 긍정형), --quality
#   순서: yunsur_v4 → yunsur_v3_q4 → base → yunsur_v3(q8, 운영본)  — v4 결과를 가장 먼저
# 맥미니에서 (밤에 걸어두기):
#   cd "/Volumes/T7 Shield/mini" && nohup bash scripts/eval_v4_all.sh > .cron/eval_v4_all.log 2>&1 &
#   진행 확인: tail -f .cron/eval_v4_all.log
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
OUT_DOCS="docs/experiments/yunsur_v4/04_eval_v4"
mkdir -p "$OUT_DOCS" .cron

# v3 는 운영 모델이 q8_0(9.5GB) 이라 v4(q4_k_m) 와 양자화가 다름 → 같은 q4_k_m 으로 하나 더 만들어 공정 비교
V3_F16="/Volumes/T7 Shield/qwen35-merged-f16.gguf"
V3_Q4="/Volumes/T7 Shield/yunsur_v3-q4_k_m.gguf"
QUANTIZE="$HOME/llama.cpp/build/bin/llama-quantize"
if ! ollama show yunsur_v3_q4 >/dev/null 2>&1; then
  echo "== yunsur_v3_q4 생성 (v3 f16 → q4_k_m) =="
  [[ -f "$V3_Q4" ]] || "$QUANTIZE" "$V3_F16" "$V3_Q4" Q4_K_M
  sed "s|^FROM .*|FROM \"$V3_Q4\"|" Modelfile > /tmp/Modelfile.v3q4
  ollama create yunsur_v3_q4 -f /tmp/Modelfile.v3q4
fi

# 이미 등록됐는지 확인
for m in yunsur_v4 yunsur_v3_q4 yunsur_v3:latest qwen3.5:9b; do
  ollama show "$m" >/dev/null 2>&1 || { echo "❌ Ollama 에 $m 없음 (PATH=$PATH)"; ollama list; exit 1; }
done

START=$(date +%s)
run_one() {  # $1=모델 $2=출력 태그
  local model="$1" tag="$2" t0
  t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality \
      --out ".cron/eval_v4_${tag}.jsonl"
  cp ".cron/eval_v4_${tag}_summary.json" "$OUT_DOCS/${tag}_summary.json"
  cp ".cron/eval_v4_${tag}.jsonl" "$OUT_DOCS/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분) → $OUT_DOCS/${tag}_summary.json"
}

run_one "yunsur_v4"        "yunsur_v4"       # q4_k_m, v4 데이터
run_one "yunsur_v3_q4"     "yunsur_v3_q4"    # q4_k_m, v3 데이터 — v4 와 양자화 동일 (주 비교 대상)
run_one "qwen3.5:9b"       "base"            # 무학습
run_one "yunsur_v3:latest" "yunsur_v3_q8"    # 운영 중이던 v3 (q8_0) — 기존 베이스라인과 연결용

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
for t in yunsur_v4 yunsur_v3_q4 base yunsur_v3_q8; do
  "$PY" -c "import json;s=json.load(open('$OUT_DOCS/${t}_summary.json'));print(f\"{'$t':10} {s['one_liner']}\")"
done
