#!/bin/bash
# N개 모델 라운드 — 대조군(base) + 대상 N개를 **같은 세션**에서 재고 모든 쌍을 짝지어 본다.
#   bash scripts/eval_multi_round.sh <태그> <대상1> [<대상2> ...]
#   예: bash scripts/eval_multi_round.sh lr3 yunsur_v9 yunsur_v11 yunsur_v10
#
# 왜 필요한가: eval_trio_round.sh 는 대상 2개로 고정이다. lr 용량-반응처럼 **세 수준 이상**을
# 한 밤에 세워야 하는 라운드가 생겼다 (yunsur_v11: lr 2e-4 ↔ 1e-4 ↔ 5e-5).
# protocol.md §2.2 는 밤을 건너뛴 비교를 금지하므로 수준 전부를 같은 세션에 넣어야 한다.
#
# 판정기·추출기·문항 집합은 eval_round.sh / eval_trio_round.sh 와 **완전히 같은 것**을 쓴다.
# 이 스크립트가 바꾸는 것은 대상 개수와 출력 배치뿐이므로 판정 기준은 달라지지 않는다.
#
# 맥미니에서 (4모델 150문항 ≈ 350분):
#   cd "/Volumes/T7 Shield/mini" && nohup caffeinate -i bash scripts/eval_multi_round.sh lr3 yunsur_v9 yunsur_v11 yunsur_v10 > .cron/eval_multi.log 2>&1 &
#
# 중단 후 이어하기: RESUME=1 bash scripts/eval_multi_round.sh <태그> <대상...>
#   (이미 끝난 대상의 jsonl 은 건너뛴다)
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
FIXTURE="tests/fixtures/local_llm_failure_eval.jsonl"
EXPECT_SHA="967eeb460559"
BASE="qwen3.5:9b"

TAG="${1:-}"
shift || true
TARGETS=("$@")
if [[ -z "$TAG" || ${#TARGETS[@]} -eq 0 ]]; then
  echo "사용법: bash scripts/eval_multi_round.sh <태그> <대상1> [<대상2> ...]"; exit 2
fi
OUT_DIR=".cron/multi_${TAG}"

echo "===== 사전 확인 ====="
echo "커밋: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
echo "대상: ${TARGETS[*]}  (대조군 $BASE)"
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

# 모델 중복은 결과를 덮어써 조용히 망가진다 — 먼저 막는다
if [[ $(printf '%s\n' "${TARGETS[@]}" | sort -u | wc -l) -ne ${#TARGETS[@]} ]]; then
  echo "❌ 대상에 중복이 있다: ${TARGETS[*]}"; exit 2
fi
for m in "$BASE" "${TARGETS[@]}"; do
  ollama show "$m" >/dev/null 2>&1 || { echo "❌ Ollama 에 $m 없음"; ollama list; exit 1; }
done

# 태그 배정: 대상은 t1,t2,… · 대조군은 base (끊겨도 어느 파일이 누구인지 남게 매핑을 적어 둔다)
declare -a TAGS=() NAMES=()
for i in "${!TARGETS[@]}"; do TAGS+=("t$((i+1))"); NAMES+=("${TARGETS[$i]}"); done
TAGS+=("base"); NAMES+=("$BASE")
mkdir -p "$OUT_DIR"
: > "$OUT_DIR/models.txt"
for i in "${!TAGS[@]}"; do echo "${TAGS[$i]} ${NAMES[$i]}" >> "$OUT_DIR/models.txt"; done
echo "태그 매핑 → $OUT_DIR/models.txt"; cat "$OUT_DIR/models.txt"

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
for i in "${!TAGS[@]}"; do
  tag="${TAGS[$i]}"; model="${NAMES[$i]}"
  if [[ "${RESUME:-0}" == "1" && -s "$OUT_DIR/${tag}.jsonl" ]]; then
    echo "[건너뜀] $model → $tag (이미 있음)"; continue
  fi
  t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ($((i+1))/${#TAGS[@]}) ##########"
  # --keep-text: 응답 원문을 남긴다. 판정에는 영향이 없고(기록 전용 필드) 사후 기전
  # 분석이 재측정을 요구하지 않게 한다 — length_mechanism_1003.md §6 에서 240자
  # preview 로 섹션을 세다 잘림을 세는 실수를 했고, RAG 전문을 다시 받아야 했다.
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality --keep-text \
      --out "$OUT_DIR/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분)"
done

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
echo
echo "===== 슬롯별 실패율 + Wilson 95% 구간 ====="
"$PY" - "$OUT_DIR" <<'PY'
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
order = [l.split()[0] for l in (d / "models.txt").read_text().split("\n") if l.strip()]
for tag in ["base"] + [t for t in order if t != "base"]:
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

# 모든 쌍 (base 를 왼쪽에 두고, 대상끼리도 전부)
echo
# macOS 기본 bash 는 3.2 로 mapfile 이 없다 — while-read 로 읽는다
MAP=()
while IFS= read -r line; do
  [[ -n "$line" ]] && MAP+=("$line")
done < "$OUT_DIR/models.txt"
n=${#MAP[@]}
for ((i=0; i<n; i++)); do
  for ((j=i+1; j<n; j++)); do
    read -r ltag lname <<<"${MAP[$i]}"
    read -r rtag rname <<<"${MAP[$j]}"
    [[ -s "$OUT_DIR/${ltag}.jsonl" && -s "$OUT_DIR/${rtag}.jsonl" ]] || continue
    echo
    echo "===== 짝지은 판정: $lname vs $rname (protocol.md §2.3) ====="
    "$PY" scripts/eval_pairwise.py "$OUT_DIR/${ltag}.jsonl" "$OUT_DIR/${rtag}.jsonl"
    echo "A=$lname, B=$rname — 'B만 실패' 가 많으면 B 가 A 보다 나쁘다."
  done
done

echo
echo "판정 규칙은 docs/experiments/protocol.md §2.3 — 결과를 본 뒤 바꾸지 않는다."
echo "${#TAGS[@]}개 모델을 같은 세션에서 쟀으므로 모든 쌍이 같은 밤의 비교다."
echo "쌍이 여러 개다 — 다중 비교를 어떻게 다룰지는 라운드 노트의 사전 선언을 따른다."
