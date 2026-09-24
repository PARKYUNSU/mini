#!/bin/bash
# yunsur_v7: 추출기 교정 후 3모델 재측정 → 새 기준선 고정.
#   base / yunsur_v5 / yunsur_v6 을 같은 밤에, 같은 36문항(sha256 a1cfe0f7f562)으로.
#   바뀐 것은 core/llm/code_extract.py 하나뿐이다 (붙은 펜스 복구).
#   _coding_ok 가 extract_python_code 를 쓰므로 이는 판정기 변경이고, v6 라운드 §3 의
#   기준선은 무효다. docs/experiments/yunsur_v7/README.md §2 의 예측 P1~P4 를 여기서 검증한다.
#
# 맥미니에서:
#   cd "/Volumes/T7 Shield/mini" && nohup caffeinate -i bash scripts/eval_v7_rebaseline.sh > .cron/eval_v7.log 2>&1 &
#   진행 확인: tail -f .cron/eval_v7.log
#
# 중단 후 이어하기: RESUME=1 bash scripts/eval_v7_rebaseline.sh
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$(pwd)"
export PYTHONUNBUFFERED=1
PY=".venv/bin/python"
FIXTURE="tests/fixtures/local_llm_failure_eval.jsonl"
OUT_DOCS="docs/experiments/yunsur_v7/04_eval_v7"
mkdir -p "$OUT_DOCS" .cron

MODELS=(
  "yunsur_v6:yunsur_v6"
  "yunsur_v5:yunsur_v5"
  "base:qwen3.5:9b"
)

echo "===== 사전 확인 ====="
echo "판정기 커밋: $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
if ! git diff --quiet -- scripts/eval_local_llm_failure.py core/llm/code_extract.py "$FIXTURE"; then
  echo "⚠️ 판정기·추출기·평가 세트에 커밋 안 된 수정이 있다 — 결과를 커밋에 귀속시킬 수 없다"
fi

# 1) 평가 세트가 v6 라운드와 같아야 한다. 다르면 추출기 효과를 분리할 수 없으므로 중단한다.
"$PY" - "$FIXTURE" <<'PY' || exit 1
import json, sys, hashlib
from collections import Counter
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
dist = dict(Counter(r["slot"] for r in rows))
digest = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()[:12]
print(f"평가 세트: {len(rows)}문항 {dist} sha256={digest}")
if digest != "a1cfe0f7f562":
    print("❌ v6 라운드를 잰 세트(a1cfe0f7f562)와 다르다 — 추출기 효과를 분리할 수 없다")
    raise SystemExit(1)
print("세트 동일 확인 OK")
PY

# 2) 추출기 수정이 실제로 들어 있는지 — 105분을 옛 코드로 태우지 않기 위해 먼저 본다.
"$PY" - <<'PY' || exit 1
import ast, sys
sys.path.insert(0, ".")
from core.llm.code_extract import extract_python_code as ex
code, how = ex("```pythonimport re\nd = {}\nprint(d)\n```")
if "+fused" not in how or not code.startswith("import re"):
    print(f"❌ 추출기에 붙은 펜스 복구가 없다 (how={how!r}) — git pull 했는지 확인할 것")
    raise SystemExit(1)
ast.parse(code)
c2, h2 = ex("```python\nprint('hi')\n```")
if (h2, c2) != ("fence", "print('hi')"):
    print(f"❌ 정상 펜스가 깨졌다 (how={h2!r} code={c2!r})")
    raise SystemExit(1)
print(f"추출기 확인 OK — 붙은 펜스 복구={how!r}, 정상 펜스 유지={h2!r}")
PY

missing=0
for entry in "${MODELS[@]}"; do
  model="${entry#*:}"
  ollama show "$model" >/dev/null 2>&1 || { echo "❌ Ollama 에 $model 없음"; missing=1; }
done
if [[ $missing -eq 1 ]]; then echo "--- 등록된 모델 ---"; ollama list; exit 1; fi

if [[ "${RESUME:-0}" != "1" ]]; then
  stale=$(ls .cron/eval_v7_*.jsonl 2>/dev/null | head -5)
  if [[ -n "$stale" ]]; then
    echo "❌ 기존 결과 파일이 있다:"; echo "$stale"
    echo "   이어서 재려면 RESUME=1, 처음부터 재려면 rm .cron/eval_v7_*.jsonl"
    exit 1
  fi
fi

START=$(date +%s)
for entry in "${MODELS[@]}"; do
  tag="${entry%%:*}"; model="${entry#*:}"; t0=$(date +%s)
  echo; echo "########## [$(date '+%m-%d %H:%M')] $model → $tag ##########"
  "$PY" scripts/eval_local_llm_failure.py --model "$model" --repeats 3 --quality \
      --out ".cron/eval_v7_${tag}.jsonl"
  if [[ $? -ne 0 ]]; then
    echo "⚠️ $model 측정이 실패로 끝났다 — RESUME=1 로 이어서 채울 것"
    continue
  fi
  cp ".cron/eval_v7_${tag}_summary.json" "$OUT_DOCS/${tag}_summary.json"
  cp ".cron/eval_v7_${tag}.jsonl" "$OUT_DOCS/${tag}.jsonl"
  echo "[$(date '+%m-%d %H:%M')] $model 완료 ($(( ($(date +%s) - t0) / 60 ))분)"
done

echo; echo "===== 전체 완료: $(( ($(date +%s) - START) / 60 ))분 ====="
"$PY" - "$OUT_DOCS" <<'PY'
import json, re, sys
from collections import Counter
from pathlib import Path

out = Path(sys.argv[1])
TIER = {**{f"coding_{i:02d}": "쉬움" for i in range(1, 7)},
        **{f"coding_{i:02d}": "보통" for i in range(7, 11)},
        **{f"coding_{i:02d}": "어려움" for i in range(11, 13)}}
# v6 라운드(옛 추출기) 실측값 — 예측 P1~P4 의 비교 대상
BEFORE = {
    "base":      {"chat": 0.0, "planner": 0.0, "rag": 0.125, "coding": 0.1111, "fused": 0},
    "yunsur_v5": {"chat": 0.0, "planner": 0.0, "rag": 0.0,   "coding": 0.1944, "fused": 3},  # 09-24 같은 밤 값
    "yunsur_v6": {"chat": 0.0, "planner": 0.0, "rag": 0.0,   "coding": 0.2222, "fused": 3},
}
FUSED_RE = re.compile(r"```python(?=\S)")

def load(tag):
    p = out / f"{tag}_summary.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None

def rows(tag):
    p = out / f"{tag}.jsonl"
    return [json.loads(l) for l in p.open(encoding="utf-8")] if p.is_file() else []

got = {}
for tag in ("yunsur_v6", "yunsur_v5", "base"):
    s = load(tag)
    if not s:
        print(f"{tag}: 결과 없음"); continue
    rs = rows(tag)
    print(f"\n=== {tag} ===")
    print(" ", s["one_liner"])
    for slot, st in (s.get("by_slot") or {}).items():
        print(f"  {slot:8} strict={st.get('strict_fail_rate')} hard={st.get('fail_rate')} 중앙값={st.get('elapsed_median_sec')}s")
    agg = {}
    for r in rs:
        if r.get("slot") != "coding":
            continue
        t = TIER.get(r["id"], "?")
        n, bad = agg.get(t, (0, 0))
        agg[t] = (n + 1, bad + (1 if ((not r.get("ok")) or r.get("quality_ok") is False) else 0))
    print("  코딩 난이도별:", "  ".join(f"{t} {b}/{n}" for t, (n, b) in
          sorted(agg.items(), key=lambda kv: ("쉬움보통어려움".find(kv[0])))))
    # P4: 붙은 펜스 — 복구 표시(code_unwrap 의 +fused)와 원문 패턴 두 방식으로 센다
    marked = sum(1 for r in rs if "+fused" in (r.get("code_unwrap") or ""))
    raw_hit = sum(1 for r in rs if r.get("slot") == "coding" and FUSED_RE.search(r.get("preview") or ""))
    ids = sorted({r["id"] for r in rs if "+fused" in (r.get("code_unwrap") or "")})
    print(f"  붙은 펜스: 복구표시 {marked}건 · 원문패턴 {raw_hit}건  문항 {ids}")
    cod10 = [r for r in rs if r["id"] == "coding_10"]
    bad10 = [r for r in cod10 if (not r.get("ok")) or r.get("quality_ok") is False]
    print(f"  coding_10: {len(bad10)}/{len(cod10)} 실패")
    got[tag] = {
        **{sl: (s["by_slot"].get(sl) or {}).get("strict_fail_rate") for sl in ("chat", "planner", "rag", "coding")},
        "fused": marked, "bad10": len(bad10), "n10": len(cod10),
    }

print("\n===== 예측 판정 (§2, 결과를 본 뒤 바꾸지 않는다) =====")
def line(name, ok, detail):
    print(f"  {name}: {'✅ 맞음' if ok else '❌ 빗나감'} — {detail}")

if "base" in got:
    b = got["base"]; before = BEFORE["base"]["coding"]
    line("P1 base 코딩 불변", abs((b['coding'] or 0) - before) < 1e-9,
         f"{before} → {b['coding']}")
for tag in ("yunsur_v5", "yunsur_v6"):
    if tag in got:
        g = got[tag]
        line(f"P2 {tag} coding_10 통과", g["bad10"] == 0, f"{g['bad10']}/{g['n10']} 실패")
if "yunsur_v6" in got:
    line("P2 v6 코딩 22.2% → 13.9%", abs((got['yunsur_v6']['coding'] or 0) - 0.1389) < 0.005,
         f"{BEFORE['yunsur_v6']['coding']} → {got['yunsur_v6']['coding']}")
print("  P3 다른 슬롯 — 추출기는 코딩 슬롯에서만 쓰이므로 변화는 정의상 노이즈다. 그 폭을 기록한다:")
for tag in ("base", "yunsur_v5", "yunsur_v6"):
    if tag in got:
        for sl in ("chat", "planner", "rag"):
            a, b2 = BEFORE[tag][sl], got[tag][sl]
            if a != b2:
                print(f"    {tag} {sl}: {a} → {b2}  (노이즈)")
print("  P4 붙은 펜스 발생률 불변 (가리지 않았다는 증거):")
for tag in ("base", "yunsur_v5", "yunsur_v6"):
    if tag in got:
        a, b2 = BEFORE[tag]["fused"], got[tag]["fused"]
        print(f"    {tag:10} {a} → {b2}  {'OK' if a == b2 else '차이'}")
PY
echo
echo "예측은 docs/experiments/yunsur_v7/README.md §2 — 결과를 본 뒤 바꾸지 않는다."
echo "다음: 05_conclusion.md 작성, v8 표적 확정"
