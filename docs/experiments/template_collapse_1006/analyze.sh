#!/bin/bash
# template_collapse_1006 의 **사전 등록된** 분석 — README.md §5 를 코드로 고정한 것이다.
#   bash docs/experiments/template_collapse_1006/analyze.sh .cron/multi_tmpl
# 측정이 끝나기 전에 써서 커밋했다.
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
D="${1:-.cron/multi_tmpl}"
[[ -s "$D/models.txt" ]] || { echo "❌ models.txt 없음: $D"; exit 1; }
".venv/bin/python" - "$D" <<'PY'
import json, re, sys, statistics as st
from pathlib import Path

d = Path(sys.argv[1])
SEC = ("선별 논문", "부족 논문", "Research Gap")
SLOTS = [re.compile(p + r"\s*[:：]\s*(.+)") for p in
         ("무엇을 개선했는지", "어떻게 해결했는지", "기존 대비 차별점")]
THRESHOLD = 12          # §5.1 붕괴 지점 정의: 이탈 수가 처음 12/24 이상이 되는 스텝
GATE_BASE, GATE_V9 = 8, 16   # §5.0 전제 점검

rows = [l.split() for l in (d / "models.txt").read_text().split("\n") if l.strip()]
res = {}
missing = []
for tag, name in rows:
    p = d / f"{tag}.jsonl"
    if not p.is_file() or not p.stat().st_size:
        missing.append(name); continue
    rag = [r for r in (json.loads(l) for l in p.read_text().splitlines() if l.strip())
           if r.get("slot") == "rag"]
    texts = [r for r in rag if r.get("text")]
    off = sum(1 for r in texts if not any(s in r["text"] for s in SEC))
    ctx = [r["rag_ctx_chars"] for r in rag if r.get("rag_ctx_chars")]
    per = [st.mean(v) for r in texts
           if (v := [len(x.strip()) for rx in SLOTS for x in rx.findall(r["text"])])]
    res[name] = dict(n=len(rag), with_text=len(texts), off=off,
                     ctx_med=st.median(ctx) if ctx else 0,
                     ctx_lo=min(ctx) if ctx else 0, ctx_hi=max(ctx) if ctx else 0,
                     slot_len=st.mean(per) if per else None,
                     out_med=st.median([r.get("out_chars") or len(r["text"]) for r in texts]) if texts else 0)
if missing:
    print(f"❌ 결과 없음: {missing} — 라운드가 끝나지 않았다"); raise SystemExit(1)

def show(name):
    r = res[name]
    sl = f"{r['slot_len']:5.1f}" if r["slot_len"] is not None else "    -"
    print(f"  {name:<14} {r['off']:2}/{r['n']:<3} {r['ctx_med']:7.0f} "
          f"{r['ctx_lo']:6}~{r['ctx_hi']:<6} {sl}  {r['out_med']:6.0f}")

print("#################### §5.2 조건 1 — rag_ctx_chars 분포 ####################")
print("모델 간에 치우쳐 있으면 **판정 자체를 버린다**.")
print(f"  {'모델':<14} {'이탈':<6} {'ctx중앙':>7} {'ctx범위':>13} {'슬롯길이':>6} {'출력중앙':>7}")
order = [n for _, n in rows]
for n in order: show(n)
meds = [res[n]["ctx_med"] for n in order]
spread = (max(meds) - min(meds)) / st.median(meds) * 100
print(f"\n  ctx 중앙값 퍼짐: {min(meds):.0f} ~ {max(meds):.0f} (중앙 대비 {spread:.1f}%)")
print("  → " + ("치우치지 않았다 — 판정 진행" if spread < 25 else
                "❌ 25% 넘게 치우쳤다 — §5.2 조건 1 위반, 판정에 쓰지 않는다"))

print()
print("#################### §5.0 전제 점검 (문지기) ####################")
b, v9 = res.get("qwen3.5:9b"), res.get("yunsur_v9")
ok_b = b and b["off"] <= GATE_BASE
ok_v9 = v9 and v9["off"] >= GATE_V9
print(f"  base 이탈 {b['off']}/{b['n']}  (≤ {GATE_BASE} 필요) → {'OK' if ok_b else '❌'}")
print(f"  v9   이탈 {v9['off']}/{v9['n']}  (≥ {GATE_V9} 필요) → {'OK' if ok_v9 else '❌'}")
if not (ok_b and ok_v9):
    print("\n  ❌ 문지기 실패 → **판정 불가.** 지표가 이 밤에 작동하지 않았다.")
    print("     체크포인트 수치를 읽지 않는다 (§5.0).")
    raise SystemExit(0)
print("  문지기 통과 — 체크포인트를 읽는다.")

print()
print("#################### §5.1 주 판정 — 붕괴 지점 ####################")
steps = sorted((int(n[len("yunsur_s"):]), n) for n in order if n.startswith("yunsur_s"))
print(f"  {'스텝':>5} {'이탈':>8}   {'누적 예시':>8}")
print(f"  {'base':>5} {b['off']:3}/{b['n']:<4}   {0:>8}")
collapse = None
for s, n in steps:
    r = res[n]
    mark = ""
    if collapse is None and r["off"] >= THRESHOLD:
        collapse = s; mark = "  ← 처음 12/24 돌파"
    print(f"  {s:>5} {r['off']:3}/{r['n']:<4}   {s*8:>8}{mark}")
print(f"  {'v9':>5} {v9['off']:3}/{v9['n']:<4}   {1100:>8}  (138스텝, 끝점)")
print(f"  {'v10':>5} {res['yunsur_v10']['off']:3}/{res['yunsur_v10']['n']:<4}   {1100:>8}  (lr 5e-5, 대조)")

print()
first = steps[0][0] if steps else None
if collapse is None:
    print("  판정: **판정 불가** — 24스텝까지 전부 12/24 미만이다.")
    print("        ckpt23(19/24)과 어긋난다. 학습 간 변동을 먼저 의심한다 (§5.1).")
elif collapse == first:
    print(f"  판정: **H3 (즉시)** — step {first} 에서 이미 {res[steps[0][1]]['off']}/24 다.")
    print(f"        예시 {first*8}건으로 템플릿을 버린다. **이 해상도로는 가를 수 없다** —")
    print("        더 촘촘한 저장을 다음 라운드로 넘긴다 (§5.1).")
else:
    prev = [(s, res[n]['off']) for s, n in steps if s < collapse]
    gradual = any(8 <= o < THRESHOLD for _, o in prev)
    kind = "H1 (점진)" if gradual else "H2 (급변)"
    print(f"  판정: **{kind}** — 붕괴 지점 = **step {collapse}** (예시 {collapse*8}건).")
    print(f"        그 앞: {', '.join(f'{s}→{o}' for s, o in prev)}")
    if not gradual:
        print("        앞 단계들이 8/24 미만이므로 계단형이다 (§5.1).")
print()
print("판정은 README.md §5 의 표를 그대로 적용한다. 결과를 본 뒤 바꾸지 않는다.")
PY
