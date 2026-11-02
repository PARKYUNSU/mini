#!/bin/zsh
# conclusion_struct_1102 §2 — held-out 90 답 만들기(운영 .env 그대로, 플래그 끔) → D 오프라인 적용. Chroma 쓰기 중이면 안 돈다.
cd "/Volumes/T7 Shield/mini" || exit 1
A=${1:-cs0_heldout}; B=${2:-cs1_heldout}  # 답 라벨 · 적용 라벨(D2: cs0_h2 cs2_h2)
export PATH=/opt/homebrew/bin:$PATH
D=docs/experiments/conclusion_struct_1102; L=.cron/conclusion_struct_1102.log
if pgrep -f "pipelines[.]ingest|build_emb_cache[.]py" > /dev/null; then echo "Chroma 쓰기 중 — 안 돈다 $(date)" >> $L; exit 1; fi
.venv/bin/python docs/experiments/ce_rerank_1101/chroma_count.py >> $L 2>&1 || { echo "Chroma 잠금 — 안 돈다 $(date)" >> $L; exit 1; }
echo "held-out 답 시작 $(date)" >> $L
.venv/bin/python -u scripts/eval_e2e_ko.py --answer --save-context \
  --questions docs/experiments/foundation_1031/heldout.tsv --gold docs/experiments/foundation_1031/heldout_gold.jsonl \
  --label $A > .cron/$A.log 2>&1; rc=$?
echo "held-out 답 끝 $(date) (종료 코드 $rc) $(tail -2 .cron/$A.log | tr '\n' ' ')" >> $L
[ $rc -eq 0 ] || exit $rc
.venv/bin/python -u $D/apply.py $B $A > .cron/$B.log 2>&1; rc=$?
grep -v "^\[DEBUG\]" .cron/$B.log >> $L
echo "D 적용 끝 $(date) (종료 코드 $rc)" >> $L
exit $rc
