#!/bin/bash
# v11 라운드의 **사전 등록된** 분석을 그대로 돌린다 — README.md §4 의 판정을 코드로 고정한 것이다.
#   bash docs/experiments/yunsur_v11/analyze.sh .cron/multi_lr3
#
# 측정 전에 써서 커밋했다. 결과를 보고 검정을 더하거나 엔드포인트를 바꾸지 않기 위해서다.
# 참고 지표(§4.3)는 아래 "참고" 구역에만 있고, 주 판정은 §4.0·§4.1 구역 세 줄뿐이다.
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
D="${1:-.cron/multi_lr3}"
PY=".venv/bin/python"
PRIMARY="planner_33-48"     # 주 지표 — §3 의 네 세션 재현이 난 자리 (상한 44~50자)

[[ -d "$D" ]] || { echo "❌ 결과 디렉터리 없음: $D"; exit 1; }
echo "결과: $D"; cat "$D/models.txt" 2>/dev/null
# 태그 매핑: t1=v9 t2=v11 t3=v10 base=qwen3.5:9b (eval_multi_round.sh lr3 yunsur_v9 yunsur_v11 yunsur_v10)
V9="$D/t1.jsonl"; V11="$D/t2.jsonl"; V10="$D/t3.jsonl"; BASE="$D/base.jsonl"
for f in "$V9" "$V11" "$V10" "$BASE"; do
  [[ -s "$f" ]] || { echo "❌ 없음: $f — 라운드가 끝나지 않았다"; exit 1; }
done

echo
echo "#################### §4.0 문지기 — v9 vs v10 (다섯 번째 재현) ####################"
echo "통과 조건: 불일치가 v10 쪽으로 쏠리고 p < 0.05. 깨지면 용량-반응은 판정 불가."
"$PY" scripts/eval_pairwise.py "$V9" "$V10" --ids "$PRIMARY"

echo
echo "#################### §4.1 T1 — v9 vs v11 ####################"
echo "1e-4 가 2e-4 보다 좋은가 (α=0.05)"
"$PY" scripts/eval_pairwise.py "$V9" "$V11" --ids "$PRIMARY"

echo
echo "#################### §4.1 T2 — v11 vs v10 ####################"
echo "5e-5 가 1e-4 보다 더 좋은가 (α=0.05)"
"$PY" scripts/eval_pairwise.py "$V11" "$V10" --ids "$PRIMARY"

echo
echo "#################### §4.2 열화 — 세 운영 슬롯에서 v11 만 실패 ####################"
echo "base 대비 v11 만 실패한 문항이 잡담·계획·RAG 합쳐 2개 이상이면 H4 가 깨진 것으로 본다."
for s in chat planner rag; do
  "$PY" scripts/eval_pairwise.py "$BASE" "$V11" --slot "$s" | sed -n '/^=====/,$p'
done

echo
echo "#################### 참고 (§4.3 — 판정 아님) ####################"
echo "--- 주 지표 밖의 계획 문항: 40개 전체 · 바닥 구간 · must_exclude ---"
for ids in planner_09-48 planner_09-32 planner_49-64; do
  for pair in "v9:$V9:v11:$V11" "v11:$V11:v10:$V10" "base:$BASE:v11:$V11"; do
    IFS=: read -r ln lf rn rf <<<"$pair"
    echo; echo "[$ids] $ln vs $rn"
    "$PY" scripts/eval_pairwise.py "$lf" "$rf" --ids "$ids" | grep -E "둘 다|불일치"
  done
done

echo
echo "--- 코딩 (맞교환 방향 확인) ---"
for pair in "v9:$V9:v11:$V11" "v11:$V11:v10:$V10" "base:$BASE:v11:$V11"; do
  IFS=: read -r ln lf rn rf <<<"$pair"
  echo; echo "$ln vs $rn"
  "$PY" scripts/eval_pairwise.py "$lf" "$rf" --slot coding | grep -E "둘 다|불일치"
done

echo
echo "--- RAG 템플릿 이탈 + 고정 슬롯 길이 (length_mechanism_1003.md §6 지표) ---"
echo "원문이 필요하다 — eval_multi_round.sh 가 --keep-text 로 남긴다."
"$PY" - "$D" <<'PY'
import json, re, sys, statistics as st
from pathlib import Path
d = Path(sys.argv[1])
tags = dict(l.split() for l in (d / "models.txt").read_text().split("\n") if l.strip())
SEC = ("선별 논문", "부족 논문", "Research Gap")
SLOTS = [re.compile(p + r"\s*[:：]\s*(.+)") for p in ("무엇을 개선했는지", "어떻게 해결했는지", "기존 대비 차별점")]
for tag, name in tags.items():
    f = d / f"{tag}.jsonl"
    if not f.is_file():
        continue
    rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    rag = [r for r in rows if r.get("slot") == "rag" and r.get("text")]
    if not rag:
        print(f"  {name:<14} RAG 원문 없음 (--keep-text 가 꺼져 있었다)"); continue
    off = sum(1 for r in rag if not any(s in r["text"] for s in SEC))
    # §6 과 같은 방식: 응답별 평균을 먼저 내고 그 평균을 낸다 (풀링하면 긴 응답이 과대 반영된다)
    per = [st.mean(v) for r in rag
           if (v := [len(x.strip()) for rx in SLOTS for x in rx.findall(r["text"])])]
    sl = f"{st.mean(per):5.1f}" if per else "    -"
    print(f"  {name:<14} 템플릿 이탈 {off:2}/{len(rag):2}  ·  고정슬롯당 길이 {sl}")
PY

echo
echo "판정은 README.md §4 의 표를 그대로 적용한다. 결과를 본 뒤 바꾸지 않는다."
