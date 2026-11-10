#!/bin/sh
# doc_slots_1111 §2: 세트마다 대조(RAG_DOC_SLOTS=0) → 처리(=1) 순서로 답까지 돌린다. 주 세트(canon)가 먼저 끝난다.
cd "$(dirname "$0")/../../.." || exit 1
E=docs/experiments; D=$E/doc_slots_1111
for s in canon 162s realnc; do
  case $s in
    canon) Q=$E/canon_1110/questions.tsv; G=$E/canon_1110/gold.jsonl; I="" ;;
    162s) Q=$E/e2e_ko_1008/ko_questions.tsv; G=$E/retrieval_eval_1007/eval_set.jsonl; I="--ids $(cat $D/ids_162s.txt)" ;;
    realnc) Q=$E/real_eval_1013/questions.tsv; G=$E/real_eval_1013/gold.jsonl; I="--ids $(cat $D/ids_realnc.txt)" ;;
  esac
  for a in 0 1; do
    .venv/bin/python $E/ce_rerank_1101/chroma_count.py 2>/dev/null | grep "^Chroma" || exit 1
    echo "----- $(date '+%F %T') ds${a}_$s"
    RAG_DOC_SLOTS=$a .venv/bin/python scripts/eval_e2e_ko.py --answer --save-context --questions "$Q" --gold "$G" $I --label "ds${a}_$s" || exit 1
  done
done
.venv/bin/python $E/ce_rerank_1101/chroma_count.py 2>/dev/null | grep "^Chroma"
echo "----- $(date '+%F %T') 끝"
