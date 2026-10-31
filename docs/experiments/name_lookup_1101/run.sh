#!/bin/sh
# name_lookup_1101: 규칙이 걸리는 33문항(affected.json)을 이름 찾기 끔(0) · 켬(1)으로 검색만 잰다.
cd "$(dirname "$0")/../../.." || exit 1
E=docs/experiments
for arm in 0 1; do
  for s in llm heldout real40 real2 162 sv_old; do
    case $s in
      162) Q=$E/e2e_ko_1008/ko_questions.tsv; G=$E/retrieval_eval_1007/eval_set.jsonl ;;
      real40) Q=$E/real_eval_1013/questions.tsv; G=$E/real_eval_1013/gold.jsonl ;;
      real2) Q=$E/real_eval2_1015/questions.tsv; G=$E/real_eval2_1015/gold.jsonl ;;
      llm) Q=$E/corpus_llmeval_1030/questions.tsv; G=$E/corpus_llmeval_1030/gold.jsonl ;;
      sv_old) Q=$E/survey_gate_1030/old_questions.tsv; G=$E/survey_gate_1030/old_gold.jsonl ;;
      heldout) Q=$E/foundation_1031/heldout.tsv; G=$E/foundation_1031/heldout_gold.jsonl ;;
    esac
    IDS=$(.venv/bin/python -c "import json; print(','.join(x['id'] for x in json.load(open('$E/name_lookup_1101/affected.json')) if x['set'] == '$s'))")
    RAG_NAME_LOOKUP=$arm .venv/bin/python scripts/eval_e2e_ko.py --save-context \
      --questions "$Q" --gold "$G" --ids "$IDS" --label "nl${arm}_$s" || exit 1
  done
done
