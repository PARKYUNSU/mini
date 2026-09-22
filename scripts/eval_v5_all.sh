#!/bin/bash
# yunsur_v5 재측정: 4모델을 같은 밤·같은 프로토콜로 연속 측정 (+ 참고로 v4 어댑터판 병기)
#   같은 30문항 × 3회, 같은 프롬프트, --quality (strict = hard + quality)
#   순서: yunsur_v5 → yunsur_v4_merged → yunsur_v3_q4 → base → (참고) yunsur_v4
#
# ⚠️ 판정기가 바뀌었다 (잡담 펜스 예외, docs/experiments/yunsur_v5/README.md §3).
#    그래서 v4 라운드의 측정값을 재사용하면 안 되고 4모델을 전부 다시 잰다. 이 스크립트가 그 전제다.
#
# 맥미니에서 (밤에 걸어두기):
#   cd "/Volumes/T7 Shield/mini" && nohup bash scripts/eval_v5_all.sh > .cron/eval_v5_all.log 2>&1 &
#   진행 확인: tail -f .cron/eval_v5_all.log
#
# 중단 후 이어하기: 평가기가 (id, trial) 단위로 건너뛰므로 RESUME=1 로 다시 돌리면 남은 것만 잰다.
#   RESUME=1 bash scripts/eval_v5_all.sh
# (RESUME 없이 기존 결과 파일이 있으면 멈춘다 — 판정기가 다른 시점의 행과 섞이는 것을 막기 위해서다.)
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
OUT_DOCS="docs/experiments/yunsur_v5/04_eval_v5"
mkdir -p "$OUT_DOCS" .cron

# 측정 대상: "태그:Ollama모델명" — 태그가 결과 파일 이름이 된다
MODELS=(
  "yunsur_v5:yunsur_v5"                # v5 머지·q4_k_m (이번 라운드 주인공)
  "yunsur_v4_merged:yunsur_v4_merged"  # v4 를 v5 와 같은 머지·양자화 경로로 재생성한 것 (주 비교 대상)
  "yunsur_v3_q4:yunsur_v3_q4"          # v3, 같은 q4_k_m
  "base:qwen3.5:9b"                    # 무학습 기준선
  "yunsur_v4_adapter:yunsur_v4"        # 참고: 운영 중인 ADAPTER 방식 v4 (판정 기준에는 안 넣고 병기만)
)

echo "===== 사전 확인 ====="
echo "판정기 커밋: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
if ! git diff --quiet -- scripts/eval_local_llm_failure.py; then
  echo "⚠️ scripts/eval_local_llm_failure.py 에 커밋 안 된 수정이 있다 — 결과를 커밋에 귀속시킬 수 없다"
fi

# Ollama 에 다 올라와 있는지 먼저 본다 (3시간짜리 측정을 중간에 못 찾아서 죽이지 않기 위해)
missing=0
for entry in "${MODELS[@]}"; do
  model="${entry#*:}"
  ollama show "$model" >/dev/null 2>&1 || { echo "❌ Ollama 에 $model 없음"; missing=1; }
done
if [[ $missing -eq 1 ]]; then
  echo "--- 등록된 모델 ---"; ollama list
  echo "yunsur_v5 가 없으면: bash scripts/merge_lora_gguf.sh v5"
  exit 1
fi

# 판정기가 바뀐 뒤의 측정이어야 하므로, 예전 결과 파일이 남아 있으면 멈춘다
if [[ "${RESUME:-0}" != "1" ]]; then
  stale=$(ls .cron/eval_v5_*.jsonl 2>/dev/null | head -5)
  if [[ -n "$stale" ]]; then
    echo "❌ 기존 결과 파일이 있다 — 판정기가 다른 시점의 행과 섞일 수 있다:"
    echo "$stale"
    echo "   이어서 재려면 RESUME=1, 처음부터 재려면 rm .cron/eval_v5_*.jsonl"
    exit 1
  fi
fi

START=$(date +%s)
run_one() {  # $1=태그 $2=모델
  local tag="$1" model="$2" t0 rc
  t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality \
      --out ".cron/eval_v5_${tag}.jsonl"
  rc=$?
  if [[ $rc -ne 0 ]]; then
    echo "⚠️ $model 측정이 rc=$rc 로 끝났다 — 다음 모델로 넘어간다 (RESUME=1 로 이어서 채울 것)"
    return 0
  fi
  cp ".cron/eval_v5_${tag}_summary.json" "$OUT_DOCS/${tag}_summary.json"
  cp ".cron/eval_v5_${tag}.jsonl" "$OUT_DOCS/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분) → $OUT_DOCS/${tag}_summary.json"
}

for entry in "${MODELS[@]}"; do
  run_one "${entry%%:*}" "${entry#*:}"
done

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
for entry in "${MODELS[@]}"; do
  tag="${entry%%:*}"
  [[ -f "$OUT_DOCS/${tag}_summary.json" ]] || { echo "$tag: 결과 없음"; continue; }
  "$PY" - "$OUT_DOCS/${tag}_summary.json" "$tag" <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
tag = sys.argv[2]
print(f"{tag:18} {s['one_liner']}")
for slot, st in (s.get("by_slot") or {}).items():
    print(f"  {slot:8} strict={st.get('strict_fail_rate')} hard={st.get('fail_rate')} 중앙값={st.get('elapsed_median_sec')}s")
PY
done
echo
echo "성공 기준은 docs/experiments/yunsur_v5/README.md §3 — 결과를 본 뒤 바꾸지 않는다."
echo "다음: 05_conclusion.md 작성"
