#!/usr/bin/env python3
"""yunsur_v6 학습 데이터 — v5 에서 RAG 이스케이프 결함만 고친다 (단일 변수).

docs/experiments/yunsur_v6/README.md §4. v5 학습 파일의 RAG 400건 중 175건이 개행을
literal `\\n`(역슬래시+n 두 글자)으로 담고 있다. 출처는 전부 `train_data_v3_clean.jsonl`
이고 v4 에도 164건 있었다 — v3 파이프라인의 이중 이스케이프가 그대로 상속됐다.

학습된 모델은 이 습관을 재현하고 다른 슬롯으로 번뜨린다. 기준선 측정의 대조:
base 는 108건 전부 literal `\\n` 을 쓰지 않는데, v5 는 RAG 24/24 전부, 잡담 3/24,
코딩 3/36 에서 쓴다. 코딩에서는 코드 추출이 깨져 `syntax` 실패가 된다.

**v6 는 그 175건의 이스케이프만 되돌린다.** 나머지 1,225건은 v5 파일을 그대로 쓴다 —
바이트 단위로 같다. 그래서 v6 와 v5 의 차이는 이 수정 하나로 귀속된다.
코딩 샘플의 literal `\\n` 2건은 `sep='\\n'` 등 파이썬 코드 안의 정상 문자열이므로
건드리지 않는다.

  python scripts/gen_v6_dataset.py --build     # train_data_v5 → train_data_v6 (+ 검증)
  python scripts/gen_v6_dataset.py --verify    # 결과 검증만
  python scripts/gen_v6_dataset.py --audit     # 데이터 실태 조사 (이스케이프 현황·필터 소급)

LLM·무거운 임포트가 필요 없다. 맥북에서도 즉시 돌아간다.

왜 코딩 필터가 없는가: 원래 v6 는 코딩 거절 필터(multi_block·self_revision) 교체를
같이 하려 했으나, --audit 으로 v5 생성분에 소급 적용해 보니 307건 중 1건만 걸렸다.
자기 수정 행동은 학습 데이터에 없고 추론 시점에 생긴다 — 필터로는 바꿀 수 없어
범위에서 뺐다. 그 조사 기능은 --audit 에 남겨 두었다 (v7 질문).
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v6"
V5_DIR = ROOT / "finetune_datasets" / "v5"
V6_DIR = ROOT / "finetune_datasets" / VERSION
TRAIN_V5 = V5_DIR / "train_data_v5.jsonl"
TRAIN_V6 = V6_DIR / f"train_data_{VERSION}.jsonl"
STATS_V6 = V6_DIR / "stats.json"

# v5 실패 원문에서 추린 자기 수정 표현. --audit 전용 (v6 는 이 필터를 쓰지 않는다).
SELF_REVISION_RE = re.compile(
    r"재작성"
    r"|다시\s*(?:쓰|작성)"
    r"|로직\s*수정"
    r"|수정\s*(?:필요|하겠|합니다|해야|하면)"
    r"|올바른\s*(?:구현|코드|방식|피보나치)"
    r"|더\s*(?:간결|정확|직관|짧)"
    r"|또는\s*(?:다음|기존|아래|이렇게|단순히)"
    r"|실제로\s*요청하신"
    r"|코드\s*참조"
    r"|앞서(?:의|서)"
    r"|대신\s*이렇게"
)


def literal_newlines(text: str) -> int:
    """진짜 개행이 아니라 역슬래시+n 두 글자의 개수."""
    return (text or "").count("\\n")


def unescape_newlines(text: str) -> str:
    return (text or "").replace("\\n", "\n")


def _read_jsonl(p: Path) -> list[dict]:
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def _write_jsonl(p: Path, rows: list[dict]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


# ---------------------------------------------------------------- --build
def build() -> int:
    rows = _read_jsonl(TRAIN_V5)
    if not rows:
        print(f"❌ {TRAIN_V5} 없음")
        return 1
    print(f"v5 학습 파일: {len(rows)}건 {dict(Counter(r['slot'] for r in rows))}")

    changed_rows = 0
    changed_fields = 0
    changed_chars = 0
    out: list[dict] = []
    for r in rows:
        r = dict(r)
        if r.get("slot") == "rag":
            hit = 0
            for k in ("instruction", "output"):
                n = literal_newlines(r.get(k, ""))
                if n:
                    r[k] = unescape_newlines(r[k])
                    hit += 1
                    changed_chars += n
            if hit:
                changed_rows += 1
                changed_fields += hit
                r["escape_fixed"] = True
        out.append(r)

    _write_jsonl(TRAIN_V6, out)
    print(f"이스케이프 수정: RAG {changed_rows}건 · {changed_fields}필드 · {changed_chars}개 개행")
    print(f"→ {TRAIN_V6} ({len(out)}건)")

    # v5 와 달라진 행이 RAG 수정분뿐인지 확인한다 — 단일 변수의 근거
    diff_slots = Counter()
    for a, b in zip(rows, out):
        if a != b:
            diff_slots[a["slot"]] += 1
    print(f"v5 대비 달라진 행: {dict(diff_slots)}  (rag 외에 있으면 단일 변수가 깨진 것)")

    stats = {
        "version": VERSION,
        "source": str(TRAIN_V5.relative_to(ROOT)),
        "samples": len(out),
        "slot_dist": dict(Counter(r["slot"] for r in out)),
        "change": {
            "kind": "rag_unescape_newlines",
            "rows": changed_rows,
            "fields": changed_fields,
            "newlines": changed_chars,
        },
        "note": "v5 와 RAG 이스케이프 수정분 외에는 동일. 코딩·잡담·계획은 v5 그대로.",
    }
    STATS_V6.parent.mkdir(parents=True, exist_ok=True)
    STATS_V6.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"→ {STATS_V6}")
    return verify()


# ---------------------------------------------------------------- --verify
def verify() -> int:
    rows = _read_jsonl(TRAIN_V6)
    if not rows:
        print(f"❌ {TRAIN_V6} 없음 — 먼저 --build")
        return 1
    print(f"\n===== 검증 =====")
    print(f"{TRAIN_V6.name}: {len(rows)}건 {dict(Counter(r['slot'] for r in rows))}")
    rc = 0

    rag = [r for r in rows if r["slot"] == "rag"]
    rag_bad = [r for r in rag if literal_newlines(r.get("output", "")) or literal_newlines(r.get("instruction", ""))]
    if rag_bad:
        print(f"❌ RAG {len(rag_bad)}건에 literal \\n 이 남았다")
        rc = 1
    else:
        print(f"✅ RAG {len(rag)}건 literal \\n 0건")

    # 코딩의 정상 \n 은 보존돼야 한다
    cod = [r for r in rows if r["slot"] == "coding"]
    cod_lit = [r for r in cod if literal_newlines(r.get("output", ""))]
    if len(cod_lit) == 2:
        print(f"✅ 코딩의 정상 literal \\n 2건 보존 (파이썬 코드 안 문자열)")
    else:
        print(f"⚠️ 코딩의 literal \\n 이 {len(cod_lit)}건 — v5 에서는 2건이었다")
        for r in cod_lit:
            print(f"     {r['output'][:90]!r}")

    # 다른 슬롯은 v5 와 동일해야 한다
    v5 = _read_jsonl(TRAIN_V5)
    if len(v5) == len(rows):
        diff = Counter(a["slot"] for a, b in zip(v5, rows) if a != b)
        extra = {k: v for k, v in diff.items() if k != "rag"}
        if extra:
            print(f"❌ rag 외 슬롯이 바뀌었다 {extra} — 단일 변수가 아니다")
            rc = 1
        else:
            print(f"✅ 바뀐 행은 rag {diff.get('rag', 0)}건뿐 — 단일 변수 유지")
    else:
        print(f"❌ 건수가 v5({len(v5)})와 다르다({len(rows)})")
        rc = 1

    # 개행이 실제로 늘었는지 (되돌리기가 문자열만 지운 게 아님을 확인)
    nl5 = sum(r["output"].count("\n") for r in v5 if r["slot"] == "rag")
    nl6 = sum(r["output"].count("\n") for r in rag)
    print(f"   RAG 진짜 개행 수: v5 {nl5} → v6 {nl6} (+{nl6 - nl5})")
    return rc


# ---------------------------------------------------------------- --audit
def audit() -> int:
    rows = _read_jsonl(TRAIN_V5)
    print("===== RAG 이스케이프 현황 (v5 학습 파일) =====")
    rag = [r for r in rows if r["slot"] == "rag"]
    bad = [r for r in rag if literal_newlines(r.get("output", "")) or literal_newlines(r.get("instruction", ""))]
    tot = sum(literal_newlines(r.get("output", "")) for r in bad)
    print(f"RAG {len(rag)}건 중 {len(bad)}건({100 * len(bad) / max(1, len(rag)):.0f}%) · literal \\n {tot}개")
    other = [r for r in rows if r["slot"] != "rag" and literal_newlines(r.get("output", ""))]
    print(f"다른 슬롯: {len(other)}건 {dict(Counter(r['slot'] for r in other))}")
    for r in other:
        print(f"  [{r['slot']}] {r['output'][:90]!r}  ← 코드 안 정상 문자열, 보존")

    print("\n===== 슬롯별 자기 수정 표현·길이 =====")
    for slot in ("rag", "chat", "planner", "coding"):
        rs = [r for r in rows if r["slot"] == slot]
        if not rs:
            continue
        hit = [r for r in rs if SELF_REVISION_RE.search(r["output"])]
        ls = sorted(len(r["output"]) for r in rs)
        print(f"{slot:8} 자기수정 {len(hit):3}/{len(rs):4} = {100 * len(hit) / len(rs):5.1f}%"
              f"   길이 중앙값 {ls[len(ls) // 2]:5} p95 {ls[int(len(ls) * 0.95)]:5}")

    print("\n===== 코딩 필터 소급 적용 (v6 범위에서 빠진 이유) =====")
    raw = _read_jsonl(V5_DIR / "raw" / "coding.jsonl")
    passed = [r for r in raw if r.get("output") and not r.get("reject_reason")]
    rej = Counter()
    for r in passed:
        n_fence = r["output"].count("```")
        why = "multi_block" if n_fence >= 3 else ("self_revision" if SELF_REVISION_RE.search(r["output"]) else "pass")
        rej[why] += 1
    print(f"v5 코딩 raw 통과분 {len(passed)}건 → {dict(rej)}")
    print("  거절이 거의 없다 = 자기 수정 행동은 학습 데이터에 없고 추론 시점에 생긴다.")
    print("  필터로는 바꿀 수 없어 v6 범위에서 뺐다 (v7 질문: RAG 의 길이·비중이 원인인가).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", action="store_true", help="train_data_v5 → train_data_v6 (RAG 이스케이프 수정 + 검증)")
    g.add_argument("--verify", action="store_true", help="train_data_v6 검증만")
    g.add_argument("--audit", action="store_true", help="데이터 실태 조사 (판정 아님, 기록용)")
    args = ap.parse_args()
    if args.build:
        return build()
    if args.verify:
        return verify()
    return audit()


if __name__ == "__main__":
    raise SystemExit(main())
