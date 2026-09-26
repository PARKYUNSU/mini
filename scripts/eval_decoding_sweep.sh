#!/bin/bash
# 디코딩 스윕 — "종료하지 못하는 행동" 을 디코딩 설정으로 억제할 수 있는지 본다. 학습 없음.
#   bash scripts/eval_decoding_sweep.sh [<대상모델>]   (기본 yunsur_v6)
#
# 배경 (docs/experiments/baseline_0926/README.md):
#   v6 는 코딩 실패 42건 중 35건이 "120초 안에 못 끝냄" 이다. 출력 상한을 800 → 4096 으로
#   5.1배 줬더니 syntax 24건이 timeout 35건으로 라벨만 옮겨갔다 — 토큰도 시간도 원인이
#   아니고 모델이 멈추지 않는다. 학습 데이터 필터로는 안 잡히므로(v6 소급 감사 307건 중 1건)
#   디코딩 쪽을 먼저 본다.
#
# 표적 문항: baseline_0926 에서 v6 만 실패한 코딩 9문항. 전체 30문항을 다 도는 대신 이 9개만
#   재서 비용을 1/3.3 로 줄인다. 어느 설정이 이 9개를 움직이면 전체로 확인한다.
#
# 맥미니에서:
#   cd "/Volumes/T7 Shield/mini" && nohup caffeinate -i bash scripts/eval_decoding_sweep.sh > .cron/sweep.log 2>&1 &
#   진행 확인: tail -f .cron/sweep.log
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
TARGET="${1:-yunsur_v6}"
IDS="coding_07,coding_19,coding_21,coding_22,coding_25,coding_26,coding_27,coding_28,coding_30"
OUT=".cron/sweep_$(date +%m%d)"
mkdir -p "$OUT"

# 이름:추가인자 — A 는 대조군(baseline_0926 을 만든 설정)이므로 인자를 주지 않는다
ARMS=(
  "A_control:"
  "B_rp135:--repeat-penalty 1.35"
  "C_narrow:--temperature 0.1 --top-p 0.5 --top-k 20"
  "D_greedy:--temperature 0.0"
)

echo "===== 사전 확인 ====="
echo "커밋: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
echo "대상: $TARGET · 표적 문항 9개 (baseline_0926 의 'v6만 실패')"
for m in "qwen3.5:9b" "$TARGET"; do
  ollama show "$m" >/dev/null 2>&1 || { echo "❌ Ollama 에 $m 없음"; ollama list; exit 1; }
done
if [[ "${RESUME:-0}" != "1" ]] && ls "$OUT"/*.jsonl >/dev/null 2>&1; then
  echo "❌ $OUT 에 기존 결과가 있다 — RESUME=1 또는 rm -r $OUT"; exit 1
fi

START=$(date +%s)
run() {  # $1=태그 $2=모델 $3...=추가인자
  local tag="$1" model="$2"; shift 2
  local t0; t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $tag · $model · 인자[$*] ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --ids "$IDS" \
      --repeats 3 --quality --out "$OUT/${tag}.jsonl" $*
  echo "[$(date '+%m-%d %H:%M')] $tag 완료 ($(( ($(date +%s) - t0) / 60 ))분)"
}

# base 는 이 9문항을 전부 통과하는 것이 정의상 맞다 — 표적 문항이 망가지지 않았다는 확인
run "base_ref" "qwen3.5:9b"
for arm in "${ARMS[@]}"; do
  run "${arm%%:*}" "$TARGET" ${arm#*:}
done

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
"$PY" - "$OUT" <<'PY'
import json, sys
from collections import Counter
from pathlib import Path
d = Path(sys.argv[1])
order = ["base_ref", "A_control", "B_rp135", "C_narrow", "D_greedy"]
print(f"{'arm':11} {'디코딩':22} {'실패':>7} {'timeout':>8} {'시간중앙':>9} {'출력중앙':>9}  실패 문항")
for tag in order:
    p = d / f"{tag}.jsonl"
    if not p.is_file():
        print(f"{tag:11} (결과 없음)"); continue
    rows = [json.loads(l) for l in p.open(encoding="utf-8")]
    bad = [r for r in rows if (not r.get("ok")) or r.get("quality_ok") is False]
    to = sum(1 for r in bad if r.get("fail_kind") == "timeout")
    el = sorted(float(r.get("elapsed_sec") or 0) for r in rows)
    oc = sorted(int(r.get("out_chars") or 0) for r in rows)
    dec = next((r.get("decoding") for r in rows if r.get("decoding")), "-")
    # 문항 단위 과반 실패
    per = Counter()
    tot = Counter()
    for r in rows:
        tot[r["id"]] += 1
        if (not r.get("ok")) or r.get("quality_ok") is False:
            per[r["id"]] += 1
    items = sorted(i for i in tot if per[i] * 2 > tot[i])
    print(f"{tag:11} {str(dec):22} {len(bad):3}/{len(rows):<3} {to:8} "
          f"{el[len(el)//2]:8.1f}s {oc[len(oc)//2]:8}자  {len(items)}개 {items}")
print()
print("A_control 이 baseline_0926 을 만든 설정이다. B~D 중 '실패'·'timeout'·'문항 수' 가")
print("뚜렷이 낮은 팔이 있으면 전체 30문항으로 확인한다. 없으면 디코딩으로는 못 고친다.")
PY
