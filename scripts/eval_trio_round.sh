#!/bin/bash
# 세 모델 라운드 — 대조군(base) + 대상 2개를 **같은 세션**에서 재고 세 쌍을 모두 짝지어 본다.
#   bash scripts/eval_trio_round.sh <대상A> <대상B> [<태그>]
#   예: bash scripts/eval_trio_round.sh yunsur_v9 yunsur_v10 v9v10
#
# 왜 필요한가: eval_round.sh 는 대상 1개 + base 고정이라, 학습 모델 둘을 직접 비교하려면
# 서로 다른 밤의 측정을 맞대야 한다. protocol.md §2.2 는 그것을 금지한다 — 기준선이 밤 사이
# 움직이기 때문이다 (baseline_0929: base 코딩이 11.1% ↔ 14.4% 로 움직였다).
# 그렇다고 두 대상만 재면 **영향을 받을 수 없는 대조군**이 없어져 그 밤의 노이즈 크기를
# 알 수 없다. 그래서 셋을 같이 잰다.
#
# 판정기·추출기·문항 집합은 eval_round.sh 와 **완전히 같은 것**을 쓴다. 이 스크립트가 바꾸는
# 것은 실행 순서와 출력 배치뿐이므로 판정 기준은 달라지지 않는다.
#
# 맥미니에서:
#   cd "/Volumes/T7 Shield/mini" && nohup caffeinate -i bash scripts/eval_trio_round.sh yunsur_v9 yunsur_v10 v9v10 > .cron/eval_trio.log 2>&1 &
#
# 중단 후 이어하기: RESUME=1 bash scripts/eval_trio_round.sh <대상A> <대상B> [<태그>]
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
FIXTURE="tests/fixtures/local_llm_failure_eval.jsonl"
EXPECT_SHA="ce4a7fa0acfa"
BASE="qwen3.5:9b"

A="${1:-}"
B="${2:-}"
TAG="${3:-$(date +%m%d)}"
if [[ -z "$A" || -z "$B" ]]; then
  echo "사용법: bash scripts/eval_trio_round.sh <대상A> <대상B> [<태그>]"; exit 2
fi
OUT_DIR=".cron/trio_${TAG}"
mkdir -p "$OUT_DIR"

echo "===== 사전 확인 ====="
echo "커밋: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
if ! git diff --quiet -- scripts/eval_local_llm_failure.py core/llm/code_extract.py core/llm/constraint_check.py "$FIXTURE"; then
  echo "⚠️ 판정기·추출기·제약 검사·문항 집합에 커밋 안 된 수정이 있다 — 결과를 커밋에 귀속시킬 수 없다"
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

for m in "$BASE" "$A" "$B"; do
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
# 대상을 먼저, base 를 마지막에 — 중간에 끊겨도 대상 결과는 남는다 (eval_round.sh 와 같은 순서)
run() {
  local model="$1" tag="$2" t0
  t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality \
      --out "$OUT_DIR/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분)"
}
run "$A" "a"
run "$B" "b"
run "$BASE" "base"

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
echo
echo "===== 슬롯별 실패율 + Wilson 95% 구간 ====="
"$PY" - "$OUT_DIR" <<'PY'
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
for tag in ("base", "a", "b"):
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

for pair in "base:a:$BASE:$A" "base:b:$BASE:$B" "a:b:$A:$B"; do
  IFS=: read -r ltag rtag lname rname <<<"$pair"
  echo
  echo "===== 짝지은 판정: $lname vs $rname (protocol.md §2.3) ====="
  "$PY" scripts/eval_pairwise.py "$OUT_DIR/${ltag}.jsonl" "$OUT_DIR/${rtag}.jsonl"
  echo "A=$lname, B=$rname — 'B만 실패' 가 많으면 B 가 A 보다 나쁘다."
done

echo
echo "판정 규칙은 docs/experiments/protocol.md §2.3 — 결과를 본 뒤 바꾸지 않는다."
echo "세 모델을 같은 세션에서 쟀으므로 세 쌍 모두 같은 밤의 비교다."
