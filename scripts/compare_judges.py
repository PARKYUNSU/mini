#!/usr/bin/env python3
"""두 판정기의 일치도 — docs/experiments/answer_quality_1010/README.md §6.1.

  python3 scripts/compare_judges.py judged_ans_full.jsonl judged_claude_ans_full.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent / "docs" / "experiments" / "answer_quality_1010"
DESC = ["correct", "partial", "wrong", "absent"]


def load(name: str) -> dict[str, dict]:
    rows = [json.loads(l) for l in (EXP / name).read_text(encoding="utf-8").splitlines() if l.strip()]
    return {r["id"]: r for r in rows if r.get("judged")}


def kappa(pairs: list[tuple]) -> float:
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def report(label: str, pairs: list[tuple]) -> None:
    agree = sum(a == b for a, b in pairs) / len(pairs)
    print(f"{label:<12} 일치 {agree:.3f}  κ {kappa(pairs):.3f}  (n={len(pairs)})")


def main() -> int:
    a, b = load(sys.argv[1]), load(sys.argv[2])
    ids = sorted(set(a) & set(b))
    ok = [(a[i]["description"] in ("correct", "partial"), b[i]["description"] in ("correct", "partial")) for i in ids]
    report("ok", ok)
    report("description", [(a[i]["description"], b[i]["description"]) for i in ids])
    report("fabrication", [(bool(a[i]["fabrication"]), bool(b[i]["fabrication"])) for i in ids])
    report("identifies", [(bool(a[i]["identifies_paper"]), bool(b[i]["identifies_paper"])) for i in ids])
    print(f"\n혼동표 (행 {sys.argv[1]} · 열 {sys.argv[2]})")
    print(" " * 9 + "".join(f"{d:>9}" for d in DESC))
    for da in DESC:
        print(f"{da:<9}" + "".join(f"{sum(a[i]['description'] == da and b[i]['description'] == db for i in ids):>9}" for db in DESC))
    print("\nok 불일치:", [(i, a[i]["description"], b[i]["description"]) for i, (x, y) in zip(ids, ok) if x != y])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
