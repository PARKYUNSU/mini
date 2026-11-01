#!/bin/zsh
# cite_graph_1102 §2: 오늘 01:00 수집 · 임베딩 캐시 재생성이 끝나면 수집 전 측정(run.sh 0).
# 끝남 = 01:10 뒤 · 수집/캐시 프로세스 없음 · 캐시 meta.json 이 오늘 01:00 뒤(06:00 까지 안 바뀌면 수집이 없던 날로 본다)
# — 5분 간격 두 번 연속. 수집(pipelines.ingest.main)과 캐시 재생성 사이에 HF 수집(pipelines.ingest.hf_daily)이 돈다.
cd "/Volumes/T7 Shield/mini" || exit 1
export PATH=/opt/homebrew/bin:$PATH
L=.cron/cite_graph_1102.log
M="/Volumes/T7 Shield/mini-chroma-rebuild2_emb_cache/meta.json"
echo "대기 시작 $(date)" >> $L
n=0
while [ $n -lt 2 ]; do
  sleep 300
  t=$(date +%H%M)
  if [ $t -ge 0110 ] && ! pgrep -f "pipelines[.]ingest|build_emb_cache[.]py" > /dev/null \
     && { [ -n "$(find "$M" -newermt "$(date +%Y-%m-%d) 01:00")" ] || [ $t -ge 0600 ]; }; then
    n=$((n + 1))
  else
    n=0
  fi
done
echo "수집 전 측정 시작 $(date)" >> $L
sh docs/experiments/cite_graph_1102/run.sh 0 >> $L 2>&1; rc=$?
echo "수집 전 측정 끝 $(date) (종료 코드 $rc)" >> $L
