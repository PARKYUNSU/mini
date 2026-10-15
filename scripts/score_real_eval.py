#!/usr/bin/env python3
"""real_eval_1013 자동 채점 — 수치(N) 정답·주제 목록(T) 개수·검색 적중.

  .venv/bin/python scripts/score_real_eval.py real_v13 [real_v13_detail]
  .venv/bin/python scripts/score_real_eval.py --set real_eval2_1015 now_real2   # 다른 평가셋(spec.jsonl 같은 형식)

- N: 기대 수치 문자열이 모두 답에 등장 **그리고** 정답 논문을 인용(answer_papers).
- C: 두 논문 모두 컨텍스트에 있음 / 한 편만 (검색). 답변 판정은 Claude 가 따로.
- T: 컨텍스트 안 정답(제목 키워드) 논문 수, 답이 인용한 정답 논문 수(≥ 3 이면 자동 통과 후보).
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "docs" / "experiments" / "real_eval_1013"
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"


def norm(p: str) -> str:
    return re.sub(r"v\d+$", "", p)


def wilson(k: int, n: int, z: float = 1.96) -> str:
    if not n:
        return "—"
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return f"{k}/{n} ({p:.0%}, {max(0, c - h):.0%}–{min(1, c + h):.0%})"


def score(label: str, d: Path = D) -> dict:
    spec = {json.loads(l)["id"]: json.loads(l) for l in (d / "spec.jsonl").read_text(encoding="utf-8").splitlines()}
    rows = {json.loads(l)["id"]: json.loads(l) for l in (RES / f"{label}.jsonl").read_text(encoding="utf-8").splitlines()}
    out: dict = {"N": [], "C": [], "T": []}
    for i, s in spec.items():
        r = rows.get(i)
        if r is None:
            continue
        ctx = {norm(p) for p in r.get("context_papers") or []}
        ans = {norm(p) for p in r.get("answer_papers") or []}
        text = (r.get("answer") or "").replace(",", "")
        gold = set(s.get("papers") or [])
        if s["type"] == "N":
            nums = all(re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", text) for n in s["numbers"])
            out["N"].append({"id": i, "retrieved": bool(gold & ctx), "cited": bool(gold & ans), "numbers": nums,
                             "ok": nums and bool(gold & ans)})
        elif s["type"] == "C":
            out["C"].append({"id": i, "both_ctx": gold <= ctx, "one_ctx": len(gold & ctx) == 1, "both_cited": gold <= ans})
        elif s["type"] == "T":
            out["T"].append({"id": i, "gold_in_ctx": len(gold & ctx), "gold_cited": len(gold & ans), "cited": len(ans)})
    return out


def main() -> int:
    args = sys.argv[1:]
    d = D
    if args[:1] == ["--set"]:
        d, args = ROOT / "docs" / "experiments" / args[1], args[2:]
    for label in args:
        s = score(label, d)
        n, c, t = s["N"], s["C"], s["T"]
        print(f"== {label}")
        print("N 수치  검색", wilson(sum(x["retrieved"] for x in n), len(n)),
              "· 인용", wilson(sum(x["cited"] for x in n), len(n)),
              "· 수치 정답", wilson(sum(x["ok"] for x in n), len(n)))
        print("  틀린 N:", [x["id"] for x in n if not x["ok"]])
        print("C 비교  둘 다 검색", wilson(sum(x["both_ctx"] for x in c), len(c)),
              "· 한 편만", sum(x["one_ctx"] for x in c), "· 둘 다 인용", wilson(sum(x["both_cited"] for x in c), len(c)))
        print("T 목록 ", " ".join(f"{x['id']}:ctx{x['gold_in_ctx']}/cite{x['gold_cited']}/전체{x['cited']}" for x in t))
        print("  정답 인용 ≥3", wilson(sum(x["gold_cited"] >= 3 for x in t), len(t)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
