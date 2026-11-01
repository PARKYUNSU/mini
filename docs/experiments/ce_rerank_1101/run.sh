#!/bin/sh
# ce_rerank_1101: 세트마다 CE 재순위 끔(pc0) → 켬(pc1)으로 검색만 잰다. dev 관문 미달이면 held-out 을 안 돌린다 (README §2).
cd "$(dirname "$0")/../../.." || exit 1
E=docs/experiments; D=$E/ce_rerank_1101
for s in 162 real40 real2 heldout; do
  case $s in
    162) Q=$E/e2e_ko_1008/ko_questions.tsv; G=$E/retrieval_eval_1007/eval_set.jsonl ;;
    real40) Q=$E/real_eval_1013/questions.tsv; G=$E/real_eval_1013/gold.jsonl ;;
    real2) Q=$E/real_eval2_1015/questions.tsv; G=$E/real_eval2_1015/gold.jsonl ;;
    heldout) Q=$E/foundation_1031/heldout.tsv; G=$E/foundation_1031/heldout_gold.jsonl
      .venv/bin/python $D/score.py gate || exit 1 ;;
  esac
  IDS=$(.venv/bin/python -c "import json; print(','.join(json.load(open('$D/ids.json')).get('$s', [])))")
  for arm in 0 1; do
    .venv/bin/python $D/chroma_count.py 2>/dev/null | grep "^Chroma" || exit 1
    RAG_PAPER_CE_RERANK=$arm .venv/bin/python scripts/eval_e2e_ko.py --save-context \
      --questions "$Q" --gold "$G" ${IDS:+--ids "$IDS"} --label "pc${arm}_$s" || exit 1
  done
done
.venv/bin/python $D/chroma_count.py 2>/dev/null | grep "^Chroma"
