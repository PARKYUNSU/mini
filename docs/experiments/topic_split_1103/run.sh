#!/bin/bash
# topic_split_1103: 검색만(답 생성 없음) 두 조건 연달아 — 대조 RAG_TOPIC_SPLIT=0 → 처리 =1.
# 컨텍스트 뒤 단계(외부 검색 · 결론 다시 쓰기)는 검색 지표와 무관해 두 조건 모두 끈다.
#   nohup bash docs/experiments/topic_split_1103/run.sh <질문 tsv> <gold jsonl> <label 꼬리> [--ids a,b] > .cron/topic_split_<꼬리>.log 2>&1 &
cd "/Volumes/T7 Shield/mini" || exit 1
for arm in 0 1; do
  RAG_TOPIC_SPLIT=$arm RAG_EXTERNAL_SEARCH=0 RAG_CONCLUSION_REWRITE=0 \
    .venv/bin/python scripts/eval_e2e_ko.py --label "ts${arm}_$3" --questions "$1" --gold "$2" --save-context "${@:4}"
done
echo "끝 $(date '+%m-%d %H:%M')"
