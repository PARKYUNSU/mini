#!/bin/bash
# collect_1113: 매일 수집(01:00)·캐시 재생성 끝난 뒤 → 스냅샷 → cl0 측정 → 수집 → 캐시 → cl1 측정
cd "/Volumes/T7 Shield/mini" || exit 1
export PATH=/opt/homebrew/bin:$PATH
L=.cron/collect_1113/run.log; E=docs/experiments; D=$E/collect_1113; P=.cron/collect_1113
log(){ echo "$(date "+%m-%d %H:%M:%S") $*" >> $L; }
busy(){ pgrep -f "pipelines.ingest.main|build_emb_cache|ingest_classics|eval_e2e_ko" >/dev/null; }
log "시작 · 01:00 매일 수집 기다림"
while [ "$(date +%H%M)" -lt 0105 ] || [ "$(date +%H%M)" -gt 1200 ]; do sleep 60; done
q=0; while [ $q -lt 10 ]; do if busy; then q=0; else q=$((q+1)); fi; sleep 60; done
log "매일 수집·캐시 끝(10분 조용)"
( while true; do echo "$(date +%T) $(curl -s localhost:11434/api/ps | python3 -c "import json,sys;print(\" \".join(m[\"name\"] for m in json.load(sys.stdin)[\"models\"]))")"; sleep 60; done ) > $P/ollama_ps.log 2>&1 &
PS=$!
CH="$(grep -E "^CHROMA_DB_PATH=" .env | cut -d= -f2 | tr -d \")"
mkdir -p ~/backups/mini/chroma_1113 && rsync -a "$CH/" ~/backups/mini/chroma_1113/ || { log "스냅샷 실패 — 멈춤"; kill $PS; exit 1; }
log "스냅샷 끝 $(du -sh ~/backups/mini/chroma_1113 | cut -f1)"
measure(){ for s in target 162 real40 real2 heldout bc; do
  case $s in
    target) Q=$P/target_questions.tsv; G=$P/target_gold.jsonl ;;
    162) Q=$E/e2e_ko_1008/ko_questions.tsv; G=$E/retrieval_eval_1007/eval_set.jsonl ;;
    real40) Q=$E/real_eval_1013/questions.tsv; G=$E/real_eval_1013/gold.jsonl ;;
    real2) Q=$E/real_eval2_1015/questions.tsv; G=$E/real_eval2_1015/gold.jsonl ;;
    heldout) Q=$E/judge_v2_1113/heldout120.tsv; G=$E/judge_v2_1113/heldout120_gold.jsonl ;;
    bc) Q=$E/blind_check_1113/questions.tsv; G=$E/blind_check_1113/gold.jsonl ;;
  esac
  .venv/bin/python scripts/eval_e2e_ko.py --save-context --questions "$Q" --gold "$G" --label "cl$1_$s" > $P/cl$1_$s.log 2>&1 || { log "측정 cl$1_$s 실패"; return 1; }
  log "측정 cl$1_$s 끝"
done; }
.venv/bin/python $E/ce_rerank_1101/chroma_count.py 2>/dev/null | grep "^Chroma" >> $L
measure 0 || { kill $PS; exit 1; }
log "수집 시작"
.venv/bin/python -u -m apps.backfill.ingest_classics --yaml $D/candidates.yaml > $P/ingest.log 2>&1 || { log "수집 실패 — 멈춤"; kill $PS; exit 1; }
log "수집 끝: $(tail -3 $P/ingest.log | tr "\n" " ")"
.venv/bin/python -u scripts/build_emb_cache.py > $P/embcache.log 2>&1 || { log "임베딩 캐시 실패 — 멈춤"; kill $PS; exit 1; }
log "임베딩 캐시 끝"
.venv/bin/python $E/ce_rerank_1101/chroma_count.py 2>/dev/null | grep "^Chroma" >> $L
measure 1
log "수집 후 측정 끝 (rc $?)"
kill $PS
