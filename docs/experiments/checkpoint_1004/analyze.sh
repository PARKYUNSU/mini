#!/bin/bash
# checkpoint_1004 의 **사전 등록된** 분석 — README.md §5 를 코드로 고정한 것이다.
#   bash docs/experiments/checkpoint_1004/analyze.sh .cron/multi_ckpt
#
# 측정이 끝나기 전에 써서 커밋했다. 결과를 보고 검정을 더하거나 엔드포인트를 바꾸지 않기 위해서다.
# 태그(t1…)는 models.txt 에서 **모델 이름으로** 찾는다 — 라운드마다 순서가 달라지므로
# 하드코딩하면 조용히 엉뚱한 쌍을 비교하게 된다 (v11 라운드의 analyze.sh 는 순서를 고정했다).
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
D="${1:-.cron/multi_ckpt}"
PY=".venv/bin/python"
PRIMARY="planner_33-48"     # 주 지표 — protocol §3 의 재현이 난 자리 (상한 44~50자)

[[ -d "$D" ]] || { echo "❌ 결과 디렉터리 없음: $D"; exit 1; }
MAP="$D/models.txt"
[[ -s "$MAP" ]] || { echo "❌ models.txt 없음: $MAP"; exit 1; }
echo "결과: $D"; cat "$MAP"

# 모델 이름 → jsonl 경로
f_of() {
  local want="$1" tag=""
  while read -r t m; do [[ "$m" == "$want" ]] && tag="$t"; done < "$MAP"
  [[ -n "$tag" ]] || { echo "MISSING:$want"; return; }
  echo "$D/${tag}.jsonl"
}
CK23=$(f_of yunsur_ckpt23);  CK46=$(f_of yunsur_ckpt46); CK138=$(f_of yunsur_ckpt138)
V9=$(f_of yunsur_v9);        V10=$(f_of yunsur_v10);     V11=$(f_of yunsur_v11)
BASE=$(f_of qwen3.5:9b)
for v in CK23 CK46 CK138 V9 V10 V11 BASE; do
  p="${!v}"
  [[ "$p" == MISSING:* ]] && { echo "❌ models.txt 에 ${p#MISSING:} 가 없다"; exit 1; }
  [[ -s "$p" ]] || { echo "❌ 결과 없음: $p ($v) — 라운드가 끝나지 않았다"; exit 1; }
done

pair() {  # pair <제목> <설명> <A파일> <B파일>
  echo; echo "#################### $1 ####################"; echo "$2"
  "$PY" scripts/eval_pairwise.py "$3" "$4" --ids "$PRIMARY"
}

pair "§5.0 문지기 — v9 vs v10 (여섯 번째 재현)" \
     "불일치가 v10 쪽으로 쏠리고 p < 0.05 여야 이 라운드를 해석한다." "$V9" "$V10"

pair "§5.1 T1a — ckpt23 vs v10 (누적량 정합)" \
     "누적량이 같은 두 모델이 다른가. 비유의 + T1b 유의 → H1(누적량)." "$CK23" "$V10"

pair "§5.1 T1b — v9 vs ckpt23" \
     "ckpt23 이 v9 을 이기는가." "$V9" "$CK23"

pair "§5.1 H3 확인 — base vs ckpt23" \
     "base 와 구분되지 않고 T1b 도 비유의면 '23스텝에선 아직 성질이 없다' → 판정 불가." "$BASE" "$CK23"

pair "§5.1b 학습 간 노이즈 — ckpt138 vs v9" \
     "설정이 같은 두 학습이 주 지표에서 같은 행동을 내는가 (전제 점검 문턱 미달로 들어왔다)." "$CK138" "$V9"

pair "§5.2 T2a — ckpt46 vs v11 (두 번째 정합)" "" "$CK46" "$V11"
pair "§5.2 T2b — v9 vs ckpt46" "" "$V9" "$CK46"

echo
echo "#################### 주 지표 통과 수 (기술 통계 — 판정 아님) ####################"
"$PY" - "$D" "$PRIMARY" <<'PY'
import json, sys
from collections import defaultdict
from pathlib import Path
d, spec = Path(sys.argv[1]), sys.argv[2]
head, _, tail = spec.rpartition("_"); lo, _, hi = tail.partition("-")
want = {f"{head}_{n:0{len(lo)}d}" for n in range(int(lo), int(hi) + 1)}
rows = [l.split() for l in (d / "models.txt").read_text().split("\n") if l.strip()]
print(f"  {'모델':<18} 통과 / {len(want)}")
for tag, name in rows:
    p = d / f"{tag}.jsonl"
    if not p.is_file(): continue
    fail, tot = defaultdict(int), defaultdict(int)
    for line in p.read_text().splitlines():
        if not line.strip(): continue
        r = json.loads(line)
        if r["id"] not in want: continue
        tot[r["id"]] += 1
        if (not r.get("ok")) or r.get("quality_ok") is False: fail[r["id"]] += 1
    ok = sum(1 for i in tot if fail[i] * 2 <= tot[i])
    print(f"  {name:<18} {ok:2} / {len(tot)}")
PY

echo
echo "#################### 참고 (§5.3 — 판정 아님) ####################"
echo "--- 슬롯별 실패율은 .cron/eval_ckpt.log 의 요약 구역 참조 ---"
echo "--- 코딩 (맞교환 방향) ---"
for p in "v9:$V9:ckpt23:$CK23" "v10:$V10:ckpt23:$CK23" "v9:$V9:ckpt138:$CK138"; do
  IFS=: read -r ln lf rn rf <<<"$p"
  echo; echo "$ln vs $rn"
  "$PY" scripts/eval_pairwise.py "$lf" "$rf" --slot coding | grep -E "둘 다|불일치"
done

echo
echo "--- RAG 템플릿 이탈 + 고정 슬롯 길이 (length_mechanism_1003.md §6 지표) ---"
"$PY" - "$D" <<'PY'
import json, re, sys, statistics as st
from pathlib import Path
d = Path(sys.argv[1])
SEC = ("선별 논문", "부족 논문", "Research Gap")
SLOTS = [re.compile(p + r"\s*[:：]\s*(.+)") for p in ("무엇을 개선했는지", "어떻게 해결했는지", "기존 대비 차별점")]
for line in (d / "models.txt").read_text().split("\n"):
    if not line.strip(): continue
    tag, name = line.split()
    f = d / f"{tag}.jsonl"
    if not f.is_file(): continue
    rag = [r for r in (json.loads(l) for l in f.read_text().splitlines() if l.strip())
           if r.get("slot") == "rag" and r.get("text")]
    if not rag:
        print(f"  {name:<18} RAG 원문 없음 (--keep-text 가 꺼져 있었다)"); continue
    off = sum(1 for r in rag if not any(s in r["text"] for s in SEC))
    # §6 과 같은 정의: 응답별 평균을 먼저, 템플릿 이탈(슬롯 0개) 시행은 제외
    per = [st.mean(v) for r in rag
           if (v := [len(x.strip()) for rx in SLOTS for x in rx.findall(r["text"])])]
    sl = f"{st.mean(per):5.1f}" if per else "    -"
    print(f"  {name:<18} 템플릿 이탈 {off:2}/{len(rag):2}  ·  고정슬롯당 길이 {sl}")
PY

echo
echo "판정은 README.md §5 의 표를 그대로 적용한다. 결과를 본 뒤 바꾸지 않는다."
