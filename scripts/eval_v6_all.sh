#!/bin/bash
# yunsur_v6 재측정: v6 와 v5 를 같은 밤에 연속 측정한다.
#   같은 36문항 × 3회 (n=108), --quality, 판정기는 base·v5 기준선과 동일.
#   base(코딩 11.1%)는 2026-09-23 기준선 값을 그대로 쓴다 — 코딩 슬롯은 재현성이 확인됐다
#   (v5 의 쉬움 4/18 이 두 라운드에서 정확히 재현). docs/experiments/yunsur_v6/README.md §3.
#
# 왜 v5 를 다시 재는가: 부분 통과·실패 조항이 모두 v5 기준이고, RAG 가드가 "v5 + 5%p" 인데
#   v5 가 0% 라서 RAG 실패 2건(8.3%)만 나와도 걸린다. base 가 어느 밤엔 3/24 를 냈으므로
#   같은 밤의 v5 값이 있어야 "노이즈인지 v6 의 악화인지" 구분된다.
#   판정은 §3 에 고정된 기준선으로 하고, 같은 밤 비교는 해석에 쓴다.
#
# 맥미니에서:
#   cd "/Volumes/T7 Shield/mini" && nohup caffeinate -i bash scripts/eval_v6_all.sh > .cron/eval_v6_all.log 2>&1 &
#   진행 확인: tail -f .cron/eval_v6_all.log
#
# 중단 후 이어하기: RESUME=1 bash scripts/eval_v6_all.sh
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
FIXTURE="tests/fixtures/local_llm_failure_eval.jsonl"
OUT_DOCS="docs/experiments/yunsur_v6/04_eval_v6"
mkdir -p "$OUT_DOCS" .cron

MODELS=(
  "yunsur_v6:yunsur_v6"        # 이번 라운드 — RAG 이스케이프 수정
  "yunsur_v5_rerun:yunsur_v5"  # 같은 밤의 v5 (§3 고정값과 별도로 저장한다)
)

echo "===== 사전 확인 ====="
echo "판정기 커밋: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
if ! git diff --quiet -- scripts/eval_local_llm_failure.py "$FIXTURE"; then
  echo "⚠️ 판정기 또는 평가 세트에 커밋 안 된 수정이 있다 — 결과를 커밋에 귀속시킬 수 없다"
fi

# 세트가 기준선과 같은 36문항인지. sha256 이 a1cfe0f7f562 여야 §3 기준선과 같은 세트다.
"$PY" - "$FIXTURE" <<'PY' || exit 1
import json, sys, hashlib
from collections import Counter
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
dist = dict(Counter(r["slot"] for r in rows))
want = {"chat": 8, "rag": 8, "planner": 8, "coding": 12}
digest = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()[:12]
print(f"평가 세트: {len(rows)}문항 {dist} sha256={digest}")
if dist != want or len(rows) != 36:
    print(f"❌ v6 세트가 아니다 — 기대 {want} (36문항)")
    raise SystemExit(1)
if digest != "a1cfe0f7f562":
    print(f"⚠️ 기준선을 잰 세트(sha256 a1cfe0f7f562)와 다르다 — §3 고정값과 직접 비교할 수 없다")
print("세트 확인 OK")
PY

missing=0
for entry in "${MODELS[@]}"; do
  model="${entry#*:}"
  ollama show "$model" >/dev/null 2>&1 || { echo "❌ Ollama 에 $model 없음"; missing=1; }
done
if [[ $missing -eq 1 ]]; then
  echo "--- 등록된 모델 ---"; ollama list
  echo "yunsur_v6 가 없으면: OVERWRITE=1 bash scripts/merge_lora_gguf.sh v6"
  exit 1
fi

if [[ "${RESUME:-0}" != "1" ]]; then
  stale=$(ls .cron/eval_v6r_*.jsonl 2>/dev/null | head -5)
  if [[ -n "$stale" ]]; then
    echo "❌ 기존 결과 파일이 있다:"; echo "$stale"
    echo "   이어서 재려면 RESUME=1, 처음부터 재려면 rm .cron/eval_v6r_*.jsonl"
    exit 1
  fi
fi

START=$(date +%s)
for entry in "${MODELS[@]}"; do
  tag="${entry%%:*}"; model="${entry#*:}"; t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality \
      --out ".cron/eval_v6r_${tag}.jsonl"
  if [[ $? -ne 0 ]]; then
    echo "⚠️ $model 측정이 실패로 끝났다 — RESUME=1 로 이어서 채울 것"
    continue
  fi
  cp ".cron/eval_v6r_${tag}_summary.json" "$OUT_DOCS/${tag}_summary.json"
  cp ".cron/eval_v6r_${tag}.jsonl" "$OUT_DOCS/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분)"
done

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
"$PY" - "$OUT_DOCS" <<'PY'
import json, sys
from pathlib import Path
from collections import Counter

out = Path(sys.argv[1])
TIER = {**{f"coding_{i:02d}": "쉬움" for i in range(1, 7)},
        **{f"coding_{i:02d}": "보통" for i in range(7, 11)},
        **{f"coding_{i:02d}": "어려움" for i in range(11, 13)}}
# §3 에 고정된 기준선 (2026-09-23). 판정은 이 값으로 한다.
PINNED = {"base": {"chat": 0.0, "planner": 0.0, "rag": 0.125, "coding": 0.1111},
          "yunsur_v5": {"chat": 0.0, "planner": 0.0, "rag": 0.0, "coding": 0.25}}
LINES = {"통과": 0.161, "부분통과": 0.125, "실패": 0.30}

def load(tag):
    p = out / f"{tag}_summary.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None

def rows(tag):
    p = out / f"{tag}.jsonl"
    return [json.loads(l) for l in p.open(encoding="utf-8")] if p.is_file() else []

for tag in ("yunsur_v6", "yunsur_v5_rerun"):
    s = load(tag)
    if not s:
        print(f"{tag}: 결과 없음"); continue
    print(f"\n=== {tag} ===")
    print(" ", s["one_liner"])
    for slot, st in (s.get("by_slot") or {}).items():
        print(f"  {slot:8} strict={st.get('strict_fail_rate')} hard={st.get('fail_rate')} 중앙값={st.get('elapsed_median_sec')}s")
    rs = rows(tag)
    agg = {}
    for r in rs:
        if r.get("slot") != "coding":
            continue
        t = TIER.get(r["id"], "?")
        n, bad = agg.get(t, (0, 0))
        agg[t] = (n + 1, bad + (1 if ((not r.get("ok")) or r.get("quality_ok") is False) else 0))
    print("  코딩 난이도별 (기록용):")
    for t in ("쉬움", "보통", "어려움"):
        if t in agg:
            n, bad = agg[t]
            print(f"    {t:4} {bad}/{n} = {100 * bad / n:.1f}%")
    # H1 기록 지표: 응답에 literal \n 이 남아 있는가
    lit = Counter()
    tot = Counter()
    for r in rs:
        tot[r["slot"]] += 1
        if "\\n" in (r.get("preview") or ""):
            lit[r["slot"]] += 1
    print("  literal \\n 유출 (preview 기준, 판정 아님): "
          + " ".join(f"{s}={lit[s]}/{tot[s]}" for s in ("chat", "rag", "planner", "coding")))

v6 = load("yunsur_v6")
if v6:
    cod = (v6["by_slot"].get("coding") or {}).get("strict_fail_rate")
    print(f"\n===== 판정 (§3 고정 기준선) =====")
    print(f"v6 코딩 strict = {cod}")
    if cod is None:
        verdict = "판정 불가"
    elif cod <= LINES["부분통과"]:
        verdict = "부분 통과 후보 (≤12.5%) — 통과선도 만족하므로 다른 슬롯 가드 확인 필요"
    elif cod <= LINES["통과"]:
        verdict = "통과 후보 (≤16.1%) — 다른 슬롯 가드 확인 필요"
    elif cod < LINES["실패"]:
        verdict = "미달 (16.1% 초과 30% 미만)"
    else:
        verdict = "실패 (≥30%)"
    print(f"→ {verdict}")
    print("  다른 슬롯 가드 (각각 v5 고정값 + 5%p): 잡담 ≤5% · 계획 ≤5% · RAG ≤5%")
    for slot in ("chat", "planner", "rag"):
        got = (v6["by_slot"].get(slot) or {}).get("strict_fail_rate")
        cap = PINNED["yunsur_v5"][slot] + 0.05
        mark = "OK" if (got is not None and got <= cap + 1e-9) else "초과"
        print(f"    {slot:8} {got} vs 상한 {round(cap, 4)}  {mark}")
    v5r = load("yunsur_v5_rerun")
    if v5r:
        print("\n  같은 밤 v5 대조 (노이즈 판단용, 판정 아님):")
        for slot in ("chat", "planner", "rag", "coding"):
            a = (v6["by_slot"].get(slot) or {}).get("strict_fail_rate")
            b = (v5r["by_slot"].get(slot) or {}).get("strict_fail_rate")
            c = PINNED["yunsur_v5"][slot]
            print(f"    {slot:8} v6={a}  v5(같은밤)={b}  v5(고정값)={c}")
PY
echo
echo "성공 기준은 docs/experiments/yunsur_v6/README.md §3 — 결과를 본 뒤 바꾸지 않는다."
echo "다음: 05_conclusion.md 작성"
