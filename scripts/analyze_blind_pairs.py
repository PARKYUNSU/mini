#!/usr/bin/env python3
"""눈가림 짝 판정을 풀어 두 답변 모델을 비교한다 — answer_quality_1010 README §6.2.

  python3 scripts/analyze_blind_pairs.py ans_full ans_base
"""
from __future__ import annotations

import json
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "docs" / "experiments" / "answer_quality_1010"
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def main() -> int:
    a, b = sys.argv[1], sys.argv[2]
    tag = f"{a}_vs_{b}"
    key = json.loads((EXP / f"blind_key_{tag}.json").read_text())
    judged = [json.loads(l) for l in (EXP / f"judged_claude_blind_{tag}.jsonl").read_text().splitlines()]
    rows = {m: {json.loads(l)["id"]: json.loads(l) for l in (RES / f"{m}.jsonl").read_text().splitlines()} for m in (a, b)}
    gold = {json.loads(l)["id"]: set(json.loads(l)["relevant_papers"])
            for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}

    per: dict[str, dict[str, dict]] = {a: {}, b: {}}
    for j in judged:
        for slot in ("X", "Y"):
            per[key[j["id"]][slot]][j["id"]] = j[slot]
    ids = sorted(per[a])
    ok = {m: {i: per[m][i]["description"] in ("correct", "partial") for i in ids} for m in (a, b)}

    print(f"짝 {len(ids)}문항 (컨텍스트 동일, 정답이 컨텍스트에 있음)\n")
    print(f"{'':<10}{a:>10}{b:>10}")
    for name, f in [("ok", lambda m, i: ok[m][i]),
                    ("correct", lambda m, i: per[m][i]["description"] == "correct"),
                    ("wrong", lambda m, i: per[m][i]["description"] == "wrong"),
                    ("absent", lambda m, i: per[m][i]["description"] == "absent"),
                    ("날조", lambda m, i: per[m][i]["fabrication"]),
                    ("ID맞고틀림", lambda m, i: per[m][i]["description"] == "wrong"
                     and bool(gold[i] & set(rows[m][i].get("answer_papers") or [])))]:
        print(f"{name:<10}{sum(f(a, i) for i in ids):>10}{sum(f(b, i) for i in ids):>10}")
    only_a = sum(ok[a][i] and not ok[b][i] for i in ids)
    only_b = sum(ok[b][i] and not ok[a][i] for i in ids)
    print(f"\nok 짝: {a}만 {only_a} · {b}만 {only_b} · McNemar 정확 p={mcnemar_exact(only_a, only_b):.4f}")
    fa = sum(per[a][i]["fabrication"] and not per[b][i]["fabrication"] for i in ids)
    fb = sum(per[b][i]["fabrication"] and not per[a][i]["fabrication"] for i in ids)
    print(f"날조 짝: {a}만 {fa} · {b}만 {fb} · p={mcnemar_exact(fa, fb):.4f}")

    # 재판정 일관성: 1단계(눈가림 아님) Claude 판정 vs 이번 판정, 같은 v9 답변
    first = {json.loads(l)["id"]: json.loads(l) for l in (EXP / f"judged_claude_{a}.jsonl").read_text().splitlines()}
    both = [i for i in ids if i in first]
    agree = sum((first[i]["description"] in ("correct", "partial")) == ok[a][i] for i in both)
    agree4 = sum(first[i]["description"] == per[a][i]["description"] for i in both)
    print(f"\n재판정 일관성 ({a}, n={len(both)}): ok 일치 {agree / len(both):.3f} · 4분류 일치 {agree4 / len(both):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
