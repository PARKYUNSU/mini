#!/bin/bash
# pdf_decimal_1107: 대조 → 처리 (README §2). 맥미니에서 돌린다. 01:00 수집 · 일요일 04:00 주간 점검과 겹치지 않게 시작한다.
cd "/Volumes/T7 Shield/mini" || exit 1
D=docs/experiments/pdf_decimal_1107
for arm in 0 1; do
  echo "== pd$arm 시작 $(date '+%m-%d %H:%M:%S')"
  RAG_FIX_PDF_DECIMAL=$arm .venv/bin/python scripts/eval_e2e_ko.py --answer --save-context \
    --questions $D/questions.tsv --gold $D/gold.jsonl --label pd$arm || exit $((arm + 2))
done
echo "== 끝 $(date '+%m-%d %H:%M:%S')"
