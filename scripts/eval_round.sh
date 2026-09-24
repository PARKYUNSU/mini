#!/bin/bash
# 라운드 측정 하네스 — 대조군(base)과 대상 모델을 같은 세션에서 재고 짝지어 비교한다.
#   bash scripts/eval_round.sh <대상모델> [<태그>]
#   예: bash scripts/eval_round.sh yunsur_v6
#       bash scripts/eval_round.sh yunsur_v8 v8round
#
# docs/experiments/protocol.md 의 규칙을 구현한다:
#   - 고정 54문항(sha256 a94d4708f9b6), 반복 3회, 문항 실패는 과반 시행
#   - 영향을 받을 수 없는 대조군(base)을 같은 세션에서 같이 잰다
#   - 판정은 독립 비율 ±%p 가 아니라 짝지은 문항 단위 McNemar
#   - 실패율에 Wilson 95% 구간을 병기한다
#
# 맥미니에서:
#   cd "/Volumes/T7 Shield/mini" && nohup caffeinate -i bash scripts/eval_round.sh yunsur_v6 > .cron/eval_round.log 2>&1 &
#   진행 확인: tail -f .cron/eval_round.log
#
# 중단 후 이어하기: RESUME=1 bash scripts/eval_round.sh <대상모델> [<태그>]
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
FIXTURE="tests/fixtures/local_llm_failure_eval.jsonl"
EXPECT_SHA="a94d4708f9b6"

TARGET="${1:-}"
TAG="${2:-$(date +%m%d)}"
if [[ -z "$TARGET" ]]; then
  echo "사용법: bash scripts/eval_round.sh <대상모델> [<태그>]"; exit 2
fi
OUT_DIR=".cron/round_${TAG}"
mkdir -p "$OUT_DIR"

echo "===== 사전 확인 ====="
echo "커밋: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
if ! git diff --quiet -- scripts/eval_local_llm_failure.py core/llm/code_extract.py "$FIXTURE"; then
  echo "⚠️ 판정기·추출기·문항 집합에 커밋 안 된 수정이 있다 — 결과를 커밋에 귀속시킬 수 없다"
fi

"$PY" - "$FIXTURE" "$EXPECT_SHA" <<'PY' || exit 1
import json, sys, hashlib
from collections import Counter
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
dist = dict(Counter(r["slot"] for r in rows))
digest = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()[:12]
print(f"문항 집합: {len(rows)}문항 {dist} sha256={digest}")
if digest != sys.argv[2]:
    print(f"❌ protocol.md 가 정한 집합({sys.argv[2]})과 다르다 — 이전 라운드와 비교할 수 없다")
    print("   문항을 의도적으로 바꿨다면 protocol.md §2.1 과 이 스크립트의 EXPECT_SHA 를 같이 갱신할 것")
    raise SystemExit(1)
print("문항 집합 확인 OK")
PY

for m in "qwen3.5:9b" "$TARGET"; do
  ollama show "$m" >/dev/null 2>&1 || { echo "❌ Ollama 에 $m 없음"; ollama list; exit 1; }
done

if [[ "${RESUME:-0}" != "1" ]]; then
  stale=$(ls "$OUT_DIR"/*.jsonl 2>/dev/null | head -5)
  if [[ -n "$stale" ]]; then
    echo "❌ $OUT_DIR 에 기존 결과가 있다:"; echo "$stale"
    echo "   이어서 재려면 RESUME=1, 처음부터 재려면 rm -r $OUT_DIR"
    exit 1
  fi
fi

START=$(date +%s)
# 대상 모델을 먼저 — 중간에 끊겨도 대상 결과는 남는다
run() {
  local model="$1" tag="$2" t0
  t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality \
      --out "$OUT_DIR/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분)"
}
run "$TARGET" "target"
run "qwen3.5:9b" "base"

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
echo
echo "===== 슬롯별 실패율 + Wilson 95% 구간 ====="
"$PY" - "$OUT_DIR" <<'PY'
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
for tag in ("base", "target"):
    p = d / f"{tag}_summary.json"
    if not p.is_file():
        print(f"{tag}: 결과 없음"); continue
    s = json.loads(p.read_text(encoding="utf-8"))
    ci = s.get("strict_fail_ci95")
    ci_s = f"[{ci[0]*100:.1f}, {ci[1]*100:.1f}]" if ci else "-"
    print(f"\n=== {tag}: {s['model']} ===")
    print(f"  전체 strict {s['strict_fail']}/{s['n']} = {(s['strict_fail_rate'] or 0)*100:.1f}%  95%CI {ci_s}")
    for slot, st in (s.get("by_slot") or {}).items():
        c = st.get("strict_fail_ci95")
        cs = f"[{c[0]*100:5.1f}, {c[1]*100:5.1f}]" if c else "-"
        print(f"  {slot:8} {st['fail'] + st['quality_fail']:3}/{st['n']:3} = {(st['strict_fail_rate'] or 0)*100:5.1f}%  95%CI {cs}  중앙값 {st.get('elapsed_median_sec')}s")
PY
echo
echo "===== 짝지은 판정 (protocol.md §2.3) ====="
"$PY" scripts/eval_pairwise.py "$OUT_DIR/base.jsonl" "$OUT_DIR/target.jsonl"
echo
echo "A=base, B=$TARGET — 'B만 실패' 가 많으면 대상 모델이 base 보다 나쁘다."
echo "판정 규칙은 docs/experiments/protocol.md §2.3 — 결과를 본 뒤 바꾸지 않는다."
