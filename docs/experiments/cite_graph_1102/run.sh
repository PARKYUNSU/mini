#!/bin/sh
# cite_graph_1102 §2: 인자 0(수집 전) · 1(수집 후) — held-out 90 · 162 · real40 · real2 를 검색만 잰다.
cd "$(dirname "$0")/../../.." || exit 1
E=docs/experiments
for s in heldout 162 real40 real2; do
  case $s in
    heldout) Q=$E/foundation_1031/heldout.tsv; G=$E/foundation_1031/heldout_gold.jsonl ;;
    162) Q=$E/e2e_ko_1008/ko_questions.tsv; G=$E/retrieval_eval_1007/eval_set.jsonl ;;
    real40) Q=$E/real_eval_1013/questions.tsv; G=$E/real_eval_1013/gold.jsonl ;;
    real2) Q=$E/real_eval2_1015/questions.tsv; G=$E/real_eval2_1015/gold.jsonl ;;
  esac
  .venv/bin/python $E/ce_rerank_1101/chroma_count.py 2>/dev/null | grep "^Chroma" || exit 1
  .venv/bin/python scripts/eval_e2e_ko.py --save-context --questions "$Q" --gold "$G" --label "cg$1_$s" || exit 1
done
.venv/bin/python $E/ce_rerank_1101/chroma_count.py 2>/dev/null | grep "^Chroma"
