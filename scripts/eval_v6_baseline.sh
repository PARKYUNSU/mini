#!/bin/bash
# yunsur_v6 기준선: 새 36문항 세트로 base 와 v5 를 재측정해 기준 숫자를 고정한다.
#   평가 세트가 30 → 36 (코딩 6→12) 으로 바뀌어 v5 라운드 숫자를 그대로 쓸 수 없다.
#   docs/experiments/yunsur_v6/README.md §3 의 성공 기준이 "같은 세트에서 잰 base·v5" 에 대한
#   상대 규칙이므로, 이 스크립트 결과가 그 기준값이 된다. v6 학습·측정은 이게 끝난 뒤다.
#
# 맥미니에서:
#   cd "/Volumes/T7 Shield/mini" && nohup caffeinate -i bash scripts/eval_v6_baseline.sh > .cron/eval_v6_baseline.log 2>&1 &
#   진행 확인: tail -f .cron/eval_v6_baseline.log
#
# 중단 후 이어하기: RESUME=1 bash scripts/eval_v6_baseline.sh
# (RESUME 없이 기존 결과 파일이 있으면 멈춘다 — 다른 세트·다른 판정기로 잰 행이 섞이는 것을 막는다.)
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
FIXTURE="tests/fixtures/local_llm_failure_eval.jsonl"
OUT_DOCS="docs/experiments/yunsur_v6/04_eval_v6"
mkdir -p "$OUT_DOCS" .cron

MODELS=(
  "base:qwen3.5:9b"      # 무학습 기준선 — 통과 기준의 기준점
  "yunsur_v5:yunsur_v5"  # 직전 라운드 — 부분 통과·실패 기준의 기준점
)

echo "===== 사전 확인 ====="
echo "판정기 커밋: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
if ! git diff --quiet -- scripts/eval_local_llm_failure.py "$FIXTURE"; then
  echo "⚠️ 판정기 또는 평가 세트에 커밋 안 된 수정이 있다 — 결과를 커밋에 귀속시킬 수 없다"
fi

# 세트가 36문항(코딩 12)인지 먼저 본다. 옛 30문항으로 몇 시간을 태우면 그대로 버린다.
"$PY" - "$FIXTURE" <<'PY' || exit 1
import json, sys, hashlib
from collections import Counter
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
dist = Counter(r["slot"] for r in rows)
want = {"chat": 8, "rag": 8, "planner": 8, "coding": 12}
digest = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()[:12]
print(f"평가 세트: {len(rows)}문항 {dict(dist)} sha256={digest}")
if dict(dist) != want or len(rows) != 36:
    print(f"❌ v6 세트가 아니다 — 기대 {want} (36문항). 평가 세트 확장이 반영됐는지 확인할 것")
    raise SystemExit(1)
print("세트 확인 OK")
PY

missing=0
for entry in "${MODELS[@]}"; do
  model="${entry#*:}"
  ollama show "$model" >/dev/null 2>&1 || { echo "❌ Ollama 에 $model 없음"; missing=1; }
done
if [[ $missing -eq 1 ]]; then echo "--- 등록된 모델 ---"; ollama list; exit 1; fi

if [[ "${RESUME:-0}" != "1" ]]; then
  stale=$(ls .cron/eval_v6_*.jsonl 2>/dev/null | head -5)
  if [[ -n "$stale" ]]; then
    echo "❌ 기존 결과 파일이 있다:"; echo "$stale"
    echo "   이어서 재려면 RESUME=1, 처음부터 재려면 rm .cron/eval_v6_*.jsonl"
    exit 1
  fi
fi

START=$(date +%s)
for entry in "${MODELS[@]}"; do
  tag="${entry%%:*}"; model="${entry#*:}"; t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality \
      --out ".cron/eval_v6_${tag}.jsonl"
  if [[ $? -ne 0 ]]; then
    echo "⚠️ $model 측정이 실패로 끝났다 — RESUME=1 로 이어서 채울 것"
    continue
  fi
  cp ".cron/eval_v6_${tag}_summary.json" "$OUT_DOCS/${tag}_summary.json"
  cp ".cron/eval_v6_${tag}.jsonl" "$OUT_DOCS/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분)"
done

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
"$PY" - "$OUT_DOCS" base yunsur_v5 <<'PY'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
# 난이도 구간 — README §5. 판정에는 쓰지 않고 기록만 한다 (문항 수가 적다)
TIER = {**{f"coding_{i:02d}": "쉬움" for i in range(1, 7)},
        **{f"coding_{i:02d}": "보통" for i in range(7, 11)},
        **{f"coding_{i:02d}": "어려움" for i in range(11, 13)}}
for tag in sys.argv[2:]:
    sp = out / f"{tag}_summary.json"
    if not sp.is_file():
        print(f"{tag}: 결과 없음"); continue
    s = json.loads(sp.read_text(encoding="utf-8"))
    print(f"\n=== {tag} ===")
    print(" ", s["one_liner"])
    for slot, st in (s.get("by_slot") or {}).items():
        print(f"  {slot:8} strict={st.get('strict_fail_rate')} hard={st.get('fail_rate')} 중앙값={st.get('elapsed_median_sec')}s")
    rows = [json.loads(l) for l in (out / f"{tag}.jsonl").open(encoding="utf-8")]
    agg = {}
    for r in rows:
        if r.get("slot") != "coding":
            continue
        tier = TIER.get(r["id"], "?")
        n, bad = agg.get(tier, (0, 0))
        is_bad = (not r.get("ok")) or r.get("quality_ok") is False
        agg[tier] = (n + 1, bad + (1 if is_bad else 0))
    print("  코딩 난이도별 (기록용, 판정 아님):")
    for tier in ("쉬움", "보통", "어려움"):
        if tier in agg:
            n, bad = agg[tier]
            print(f"    {tier:4} {bad}/{n} = {100 * bad / n:.1f}%")
PY
echo
echo "이 숫자가 v6 성공 기준의 기준값이다 (README §3). 고정한 뒤 v6 학습으로 넘어간다."
