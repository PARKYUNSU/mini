#!/bin/sh
# flag_cleanup_1101: survey_gate_1030 37문항 검색만 — 인자 cb(정리 전) · ca(정리 뒤). README §2.
cd "$(dirname "$0")/../../.." || exit 1
E=docs/experiments; S=$E/survey_gate_1030
for s in new old; do
  .venv/bin/python $E/ce_rerank_1101/chroma_count.py 2>/dev/null | grep "^Chroma" || exit 1
  .venv/bin/python scripts/eval_e2e_ko.py --save-context \
    --questions $S/${s}_questions.tsv --gold $S/${s}_gold.jsonl --label "$1_$s" || exit 1
done
.venv/bin/python $E/ce_rerank_1101/chroma_count.py 2>/dev/null | grep "^Chroma"
