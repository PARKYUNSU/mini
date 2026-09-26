#!/usr/bin/env python3
"""yunsur_v9 학습 데이터 — v6 에서 코딩 슬롯을 뺀다 (순수 감산, 단일 변수).

왜 빼는가 (docs/experiments/yunsur_v9/README.md §1):
  - 코딩에서 파인튜닝이 base 보다 **유의하게** 나쁘다 (baseline_0926, McNemar p=0.004,
    base 만 실패한 코딩 문항 0개). 네 라운드 일관이다.
  - 디코딩으로는 고칠 수 없다 (yunsur_v8). 그리디가 장황함을 거의 없앴는데도 9문항 중
    2개만 살았다 — 모델이 그 문항들의 코드를 못 쓰는 것이고 장황함은 동반 증상이었다.
  - **운영 Executor 는 로컬을 쓰지 않는다** (`get_coding_groq_llm`, Groq). 즉 네 라운드
    동안 가장 많은 시간을 쓴 슬롯이 운영에 없는 슬롯이다.

v6 1,400건 → v9 1,100건 (RAG 400 / 잡담 300 / 계획 400). **코딩 300건만 빠지고 나머지
1,100건은 v6 와 바이트 단위로 같다** → v9 와 v6 의 차이는 이 감산 하나로 귀속된다.

  python scripts/gen_v9_dataset.py --build     # train_data_v6 → train_data_v9 (+ 검증)
  python scripts/gen_v9_dataset.py --verify    # 결과 검증만

LLM·무거운 임포트가 필요 없다.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v9"
SRC = ROOT / "finetune_datasets" / "v6" / "train_data_v6.jsonl"
DST_DIR = ROOT / "finetune_datasets" / VERSION
DST = DST_DIR / f"train_data_{VERSION}.jsonl"
STATS = DST_DIR / "stats.json"
DROP_SLOT = "coding"
EXPECT = {"rag": 400, "chat": 300, "planner": 400}


def _read(p: Path) -> list[dict]:
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def build() -> int:
    rows = _read(SRC)
    if not rows:
        print(f"❌ {SRC} 없음")
        return 1
    print(f"v6: {len(rows)}건 {dict(Counter(r['slot'] for r in rows))}")
    kept = [r for r in rows if r.get("slot") != DROP_SLOT]
    dropped = len(rows) - len(kept)
    DST_DIR.mkdir(parents=True, exist_ok=True)
    DST.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kept), encoding="utf-8")
    print(f"{DROP_SLOT} {dropped}건 제거 → {DST} ({len(kept)}건)")

    STATS.write_text(
        json.dumps(
            {
                "version": VERSION,
                "source": str(SRC.relative_to(ROOT)),
                "samples": len(kept),
                "slot_dist": dict(Counter(r["slot"] for r in kept)),
                "change": {"kind": "drop_slot", "slot": DROP_SLOT, "rows": dropped},
                "note": (
                    "v6 에서 코딩만 뺐다. 남은 1,100건은 v6 와 동일. 운영 Executor 는 Groq 이라 "
                    "로컬 코딩 능력이 필요 없고, 코딩 학습은 base 보다 나쁜 결과만 냈다 "
                    "(baseline_0926 McNemar p=0.004)."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"→ {STATS}")
    return verify()


def verify() -> int:
    kept = _read(DST)
    if not kept:
        print(f"❌ {DST} 없음 — 먼저 --build")
        return 1
    src = _read(SRC)
    print(f"\n===== 검증 =====")
    dist = dict(Counter(r["slot"] for r in kept))
    print(f"{DST.name}: {len(kept)}건 {dist}")
    rc = 0

    if dist != EXPECT or len(kept) != sum(EXPECT.values()):
        print(f"❌ 슬롯 분포가 기대와 다르다 — 기대 {EXPECT}")
        rc = 1
    else:
        print(f"✅ 슬롯 분포 {EXPECT}")

    if any(r.get("slot") == DROP_SLOT for r in kept):
        print(f"❌ {DROP_SLOT} 이 남아 있다")
        rc = 1
    else:
        print(f"✅ {DROP_SLOT} 0건")

    # 남은 행이 v6 와 정확히 같은가 — 단일 변수의 근거
    src_kept = [r for r in src if r.get("slot") != DROP_SLOT]
    if src_kept == kept:
        print(f"✅ 남은 {len(kept)}건이 v6 와 완전히 동일 (순서·내용) — 단일 변수 유지")
    else:
        diff = sum(1 for a, b in zip(src_kept, kept) if a != b)
        print(f"❌ v6 와 다른 행 {diff}개 (길이 {len(src_kept)} vs {len(kept)}) — 감산 외 변경이 있다")
        rc = 1

    # RAG 이스케이프 수정(v6의 성과)이 보존됐는지
    lit = sum(1 for r in kept if r["slot"] == "rag" and "\\n" in (r.get("output") or ""))
    print(f"{'✅' if lit == 0 else '❌'} RAG literal \\n {lit}건 (v6 의 이스케이프 수정 보존)")
    if lit:
        rc = 1
    return rc


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", action="store_true", help="train_data_v6 → train_data_v9 (코딩 제거 + 검증)")
    g.add_argument("--verify", action="store_true", help="train_data_v9 검증만")
    args = ap.parse_args()
    return build() if args.build else verify()


if __name__ == "__main__":
    raise SystemExit(main())
