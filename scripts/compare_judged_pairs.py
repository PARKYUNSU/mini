#!/usr/bin/env python3
"""gpt-oss 단일 답변 판정 두 개를 같은 문항 짝으로 비교한다 — yunsur_v13 README §3.

  python3 scripts/compare_judged_pairs.py ans_v13 ans_v12

- 대상: 두 쪽 모두 direct_answer/B, context_papers 가 같고, 컨텍스트에 정답이 있는 문항
  (build_blind_pairs.py 와 같은 기준).
- 판정은 답변 하나씩 모델 이름 없이 하므로 눈가림이다 (scripts/judge_answers.py --base-url).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_blind_pairs import mcnemar_exact  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"
EXP = ROOT / "docs" / "experiments" / "answer_quality_1010"


def main() -> int:
    a, b = sys.argv[1], sys.argv[2]
    rows = {m: {json.loads(l)["id"]: json.loads(l) for l in (RES / f"{m}.jsonl").read_text().splitlines()} for m in (a, b)}
    J = {m: {json.loads(l)["id"]: json.loads(l) for l in (EXP / f"judged_gptoss_{m}.jsonl").read_text().splitlines()} for m in (a, b)}
    gold = {json.loads(l)["id"]: set(json.loads(l)["relevant_papers"])
            for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    ids = sorted(i for i in rows[a] if i in rows[b]
                 and rows[a][i]["route"] == rows[b][i]["route"] == "direct_answer/B"
                 and rows[a][i]["context_papers"] == rows[b][i]["context_papers"]
                 and gold[i] & set(rows[a][i]["context_papers"])
                 and J[a].get(i, {}).get("judged") and J[b].get(i, {}).get("judged"))
    ok = {m: {i: J[m][i].get("description") in ("correct", "partial") for i in ids} for m in (a, b)}
    fab = {m: {i: bool(J[m][i].get("fabrication")) for i in ids} for m in (a, b)}
    print(f"짝 {len(ids)}문항 (컨텍스트 동일·정답 있음·양쪽 판정됨)\n")
    print(f"{'':<10}{a:>10}{b:>10}")
    for name, f in [("ok", lambda m, i: ok[m][i]),
                    ("correct", lambda m, i: J[m][i].get("description") == "correct"),
                    ("wrong", lambda m, i: J[m][i].get("description") == "wrong"),
                    ("absent", lambda m, i: J[m][i].get("description") == "absent"),
                    ("날조", lambda m, i: fab[m][i])]:
        print(f"{name:<10}{sum(f(a, i) for i in ids):>10}{sum(f(b, i) for i in ids):>10}")
    oa = sum(ok[a][i] and not ok[b][i] for i in ids)
    ob = sum(ok[b][i] and not ok[a][i] for i in ids)
    fa = sum(fab[a][i] and not fab[b][i] for i in ids)
    fb = sum(fab[b][i] and not fab[a][i] for i in ids)
    print(f"\nok 짝: {a}만 {oa} · {b}만 {ob} · McNemar 정확 p={mcnemar_exact(oa, ob):.4f}")
    print(f"날조 짝: {a}만 {fa} · {b}만 {fb} · p={mcnemar_exact(fa, fb):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
