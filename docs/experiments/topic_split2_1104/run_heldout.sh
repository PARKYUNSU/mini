#!/bin/bash
# topic_split2_1104 held-out 한 번에 (README §3): HU40 두 조건 → 보호 2b 단일 주제 15 → 보호 2 단일 주제 90 → 나뉜 문항만 두 조건 검색.
#   nohup bash docs/experiments/topic_split2_1104/run_heldout.sh > .cron/topic_split2_hu.log 2>&1 &
cd "/Volumes/T7 Shield/mini" || exit 1
D=docs/experiments/topic_split2_1104
F=docs/experiments/foundation_1031
bash docs/experiments/topic_split_1103/run.sh $D/heldout.tsv $D/heldout_gold.jsonl hu
.venv/bin/python $D/extract_diag.py tsv $D/heldout_single.tsv
.venv/bin/python $D/extract_diag.py tsv $F/heldout.tsv
ids=$(.venv/bin/python -c "import json; print(','.join(r['id'] for r in map(json.loads, open('$D/gate_heldout.jsonl')) if r['got']))")
echo "보호 2 나뉜 문항: ${ids:-없음}"
[ -n "$ids" ] && bash docs/experiments/topic_split_1103/run.sh $F/heldout.tsv $F/heldout_gold.jsonl fh2 --ids "$ids"
echo "전부 끝 $(date '+%m-%d %H:%M')"
