#!/bin/bash
# fix_v4_models.sh 이후: 올바른 yunsur_v4(어댑터) / yunsur_v3_q4(진짜 v3) 만 재측정. base·v3_q8 결과는 유효하므로 재사용.
#   cd "/Volumes/T7 Shield/mini" && nohup bash scripts/eval_v4_rerun.sh > .cron/eval_v4_rerun.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"; export PYTHONUNBUFFERED=1
PY=".venv/bin/python"; OUT_DOCS="docs/experiments/yunsur_v4/04_eval_v4"; mkdir -p "$OUT_DOCS/bad_merge_record"
for m in yunsur_v4 yunsur_v3_q4; do ollama show "$m" >/dev/null 2>&1 || { echo "❌ $m 없음 — 먼저 scripts/fix_v4_models.sh"; exit 1; }; done

# 잘못된 머지 결과는 기록으로 보관 (실험 노트에 "왜 실패했는지" 남김)
for t in yunsur_v4 yunsur_v3_q4; do
  for ext in .jsonl _summary.json; do
    [[ -f ".cron/eval_v4_${t}${ext}" ]] && mv ".cron/eval_v4_${t}${ext}" "$OUT_DOCS/bad_merge_record/${t}${ext}"
  done
  rm -f "$OUT_DOCS/${t}.jsonl" "$OUT_DOCS/${t}_summary.json"
done
[[ -d "$OUT_DOCS/bad_merge_record" ]] && mv "$OUT_DOCS/bad_merge_record/yunsur_v3_q4.jsonl" "$OUT_DOCS/bad_merge_record/yunsur_v2_q4.jsonl" 2>/dev/null; mv "$OUT_DOCS/bad_merge_record/yunsur_v3_q4_summary.json" "$OUT_DOCS/bad_merge_record/yunsur_v2_q4_summary.json" 2>/dev/null

START=$(date +%s)
run_one() { local model="$1" tag="$2" t0; t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality --out ".cron/eval_v4_${tag}.jsonl"
  cp ".cron/eval_v4_${tag}_summary.json" "$OUT_DOCS/${tag}_summary.json"; cp ".cron/eval_v4_${tag}.jsonl" "$OUT_DOCS/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분)"; }
run_one "yunsur_v4"    "yunsur_v4"
run_one "yunsur_v3_q4" "yunsur_v3_q4"
echo; echo "===== 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
for t in yunsur_v4 yunsur_v3_q4 base yunsur_v3_q8; do
  [[ -f "$OUT_DOCS/${t}_summary.json" ]] && "$PY" -c "import json;s=json.load(open('$OUT_DOCS/${t}_summary.json'));print(f\"{'$t':12} {s['one_liner']}\")"
done
