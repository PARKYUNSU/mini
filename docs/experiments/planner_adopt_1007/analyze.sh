#!/bin/bash
# planner_adopt_1007 의 **사전 등록된** 분석 — README.md §4 를 코드로 고정한 것이다.
#   bash docs/experiments/planner_adopt_1007/analyze.sh .cron/multi_adopt
# 측정이 끝나기 전에 써서 커밋했다. 태그는 models.txt 에서 **이름으로** 찾는다.
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
D="${1:-.cron/multi_adopt}"
PY=".venv/bin/python"
PRIMARY="planner_33-48"

[[ -s "$D/models.txt" ]] || { echo "❌ models.txt 없음: $D"; exit 1; }
echo "결과: $D"; cat "$D/models.txt"
f_of() {
  local want="$1" tag=""
  while read -r t m; do [[ "$m" == "$want" ]] && tag="$t"; done < "$D/models.txt"
  [[ -n "$tag" ]] || { echo "MISSING:$want"; return; }
  echo "$D/${tag}.jsonl"
}
V10=$(f_of yunsur_v10); V9=$(f_of yunsur_v9); BASE=$(f_of qwen3.5:9b)
for v in V10 V9 BASE; do
  p="${!v}"
  [[ "$p" == MISSING:* ]] && { echo "❌ models.txt 에 ${p#MISSING:} 가 없다"; exit 1; }
  [[ -s "$p" ]] || { echo "❌ 결과 없음: $p ($v) — 라운드가 끝나지 않았다"; exit 1; }
done

pair() { echo; echo "#################### $1 ####################"; echo "$2"
  "$PY" scripts/eval_pairwise.py "$3" "$4" --ids "$PRIMARY" | grep -vE "^A = |^B = |^공통|^--ids|^===== planner"; }

pair "§4.0 문지기 — v9 vs v10 (일곱 번째 재현)" \
     "v10 쪽으로 쏠리고 p<0.05 여야 해석한다." "$V9" "$V10"
pair "§4.1 주 판정 — base vs v10" \
     "p<0.05 → 이번 세션 유의. 불일치 6쌍 미만 → 판정 불가." "$BASE" "$V10"
pair "§4.3 참고 — base vs v9 (§3 은 null 을 예측한다)" \
     "v9 쪽으로 유의하면 §3 의 lr 축 귀속이 흔들린다." "$BASE" "$V9"

echo
echo "#################### 주 지표 통과 수 (기술 통계) ####################"
"$PY" - "$D" "$PRIMARY" <<'PY'
import json, sys
from collections import defaultdict
from pathlib import Path
d, spec = Path(sys.argv[1]), sys.argv[2]
head, _, tail = spec.rpartition("_"); lo, _, hi = tail.partition("-")
want = {f"{head}_{n:0{len(lo)}d}" for n in range(int(lo), int(hi) + 1)}
for line in (d / "models.txt").read_text().split("\n"):
    if not line.strip(): continue
    tag, name = line.split()
    p = d / f"{tag}.jsonl"
    if not p.is_file(): continue
    fail, tot = defaultdict(int), defaultdict(int)
    for l in p.read_text().splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        if r["id"] not in want: continue
        tot[r["id"]] += 1
        if (not r.get("ok")) or r.get("quality_ok") is False: fail[r["id"]] += 1
    ok = sum(1 for i in tot if fail[i] * 2 <= tot[i])
    print(f"  {name:<14} {ok:2} / {len(tot)}")
PY

echo
echo "#################### 참고 — 주 지표 밖 (판정 아님) ####################"
for ids in planner_09-48 planner_49-64; do
  for p in "base:$BASE:v10:$V10" "v9:$V9:v10:$V10"; do
    IFS=: read -r ln lf rn rf <<<"$p"
    echo; echo "[$ids] $ln vs $rn"
    "$PY" scripts/eval_pairwise.py "$lf" "$rf" --ids "$ids" | grep -E "둘 다|불일치"
  done
done

echo
echo "#################### 최장 단계줄 길이 (§3 기전 지표) ####################"
"$PY" - "$D" <<'PY'
import json, re, statistics as st
from pathlib import Path
d = Path(sys.argv[1]) if False else Path(__import__("sys").argv[1])
for line in (d / "models.txt").read_text().split("\n"):
    if not line.strip(): continue
    tag, name = line.split()
    p = d / f"{tag}.jsonl"
    if not p.is_file(): continue
    longest = []
    for l in p.read_text().splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        if r.get("slot") != "planner" or not r.get("text"): continue
        # base 는 `1 단계:` 처럼 숫자와 단계 사이에 공백을 넣고 v9/v10 은 붙여 쓴다 —
        # 공백을 허용하지 않으면 base 표본이 192 → 26 으로 줄어 비교가 성립하지 않는다.
        steps = [s for s in re.findall(r"^\s*\d+\s*단계\s*:\s*(.+)$", r["text"], re.M)]
        if steps: longest.append(max(len(s.strip()) for s in steps))
    if longest:
        print(f"  {name:<14} 최장 단계줄 중앙 {st.median(longest):5.1f}자  (n={len(longest)})")
PY
echo
echo "판정은 README.md §4 를 그대로 적용한다. **채택은 독립 두 세션을 요구한다** (§4.2)."
