#!/bin/zsh
# cite_graph_1102 §1 수집 — 사용자 승인 뒤에만 띄운다. 수집 전 측정 끝 대기 → 수집 → 임베딩 캐시 → 수집 후 측정(run.sh 1).
cd "/Volumes/T7 Shield/mini" || exit 1
export PATH=/opt/homebrew/bin:$PATH
D=docs/experiments/cite_graph_1102; L=.cron/cite_graph_1102.log
while pgrep -f "wait_run0[.]sh|cite_graph_1102/run[.]sh" > /dev/null; do sleep 60; done
for s in heldout 162 real40 real2; do
  [ -s docs/experiments/e2e_ko_1008/results/cg0_$s.jsonl ] || { echo "수집 전 측정 cg0_$s 없음 — 멈춤 $(date)" >> $L; exit 1; }
done
echo "수집 시작 $(date)" >> $L
.venv/bin/python -u -m apps.backfill.ingest_classics --yaml $D/candidates.yaml > .cron/cite_graph_1102_ingest.log 2>&1
echo "수집 끝 $(date) $(tail -3 .cron/cite_graph_1102_ingest.log | tr '\n' ' ')" >> $L
.venv/bin/python -u scripts/build_emb_cache.py > .cron/cite_graph_1102_embcache.log 2>&1
echo "임베딩 캐시 끝 $(date) $(tail -1 .cron/cite_graph_1102_embcache.log)" >> $L
sh $D/run.sh 1 >> $L 2>&1; rc=$?
echo "수집 후 측정 끝 $(date) (종료 코드 $rc)" >> $L
