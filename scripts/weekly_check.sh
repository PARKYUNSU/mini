#!/bin/sh
# 주간 점검 (docs/experiments/foundation_1031 §6): real40 고정 40문항을 운영 경로(.env 그대로)로 답까지 재고,
# 사람 판정 없이 셀 수 있는 지표 한 줄을 foundation_1031/weekly.md 에 붙인다.
cd "$(dirname "$0")/.." || exit 1
L="weekly_$(date +%Y%m%d)"
OUT=docs/experiments/foundation_1031/weekly.md
.venv/bin/python scripts/eval_e2e_ko.py --answer --save-context \
  --questions docs/experiments/real_eval_1013/questions.tsv --gold docs/experiments/real_eval_1013/gold.jsonl \
  --label "$L" > ".cron/$L.log" 2>&1 || exit 1
[ -f "$OUT" ] || { printf '# 주간 점검 (real40 고정 40문항, 자동 지표)\n\n' > "$OUT"; .venv/bin/python scripts/weekly_report.py --header >> "$OUT"; }
.venv/bin/python scripts/weekly_report.py "$L" >> "$OUT"
