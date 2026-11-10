#!/bin/zsh
# canon_1110 §1 수집 재시도 — 1차 수집(ingest.sh)이 arXiv API 429 · 시간 초과로 42/80 만 넣었다.
# 같은 목록을 다시 돌린다(이미 들어간 논문은 ingest_classics 가 건너뜀). 76편 이상이면 임베딩 캐시 → 수집 후 측정.
cd "/Volumes/T7 Shield/mini" || exit 1
export PATH=/opt/homebrew/bin:$PATH
D=docs/experiments/canon_1110; L=.cron/canon_1110.log
for i in 1 2 3; do
  n=$(.venv/bin/python $D/have.py); [ "$n" = 80 ] && break
  echo "재시도 $i: 수집됨 $n/80 $(date)" >> $L
  [ $i -gt 1 ] && sleep 300
  .venv/bin/python -u -m apps.backfill.ingest_classics --yaml $D/candidates.yaml >> .cron/canon_1110_ingest_retry.log 2>&1
done
n=$(.venv/bin/python $D/have.py); echo "재시도 끝: 수집됨 $n/80 $(date)" >> $L
[ "$n" -ge 76 ] || { echo "76편 미만 — 멈춤 $(date)" >> $L; exit 1; }
.venv/bin/python -u scripts/build_emb_cache.py > .cron/canon_1110_embcache.log 2>&1 \
  || { echo "임베딩 캐시 실패 — 멈춤 $(date)" >> $L; exit 1; }
echo "임베딩 캐시 끝 $(date) $(tail -1 .cron/canon_1110_embcache.log)" >> $L
# 수집 후 측정은 396문항 · 수집 전 측정 기준 약 4.5시간. 01:00 정기 수집 전에 끝나야 비교가 성립한다.
t=$(date +%H%M); [ $t -ge 1200 ] && [ $t -le 2025 ] || { echo "수집 후 측정 시작이 20:25 를 넘음 — 멈춤 $(date)" >> $L; exit 1; }
sh $D/run.sh 1 >> $L 2>&1; rc=$?
echo "수집 후 측정 끝 $(date) (종료 코드 $rc)" >> $L
