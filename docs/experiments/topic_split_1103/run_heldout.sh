#!/bin/bash
# topic_split_1103 held-out 한 번에 (README §3): HT30 두 조건 → 보호 2 단일 주제 90 나뉨 확인 → 나뉜 문항만 두 조건 검색.
#   nohup bash docs/experiments/topic_split_1103/run_heldout.sh > .cron/topic_split_ht.log 2>&1 &
cd "/Volumes/T7 Shield/mini" || exit 1
D=docs/experiments/topic_split_1103
F=docs/experiments/foundation_1031
bash $D/run.sh $D/heldout_topics.tsv $D/heldout_topics_gold.jsonl ht
.venv/bin/python $D/gate_check.py run $F/heldout.tsv
ids=$(.venv/bin/python -c "import json; print(','.join(r['src'] for r in map(json.loads, open('$D/gate_heldout.jsonl')) if r['topics']))")
echo "보호 2 나뉜 문항: ${ids:-없음}"
[ -n "$ids" ] && bash $D/run.sh $F/heldout.tsv $F/heldout_gold.jsonl fh --ids "$ids"
echo "전부 끝 $(date '+%m-%d %H:%M')"
