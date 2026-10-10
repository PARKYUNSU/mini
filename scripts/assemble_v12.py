#!/usr/bin/env python3
"""v12 검증 통과분을 모은다 — 각 src_pid 의 '처음 통과한 판본'(원본 → 수리 1·2·3차, 자동탈락 수리 → 그 2차).

  python3 scripts/assemble_v12.py
출력: finetune_datasets/v12/final_pass.jsonl
"""
import collections
import json
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "finetune_datasets" / "v12"
STAGES = ["verified_llm", "repaired", "repaired2", "repaired3", "repaired_auto", "repaired_auto2"]


def L(f):
    p = D / f
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def ko_ratio(s: str) -> float:
    body = s.split("### 본론", 1)[-1]
    letters = re.findall(r"[가-힣A-Za-z]", body)
    return sum(1 for c in letters if "가" <= c <= "힣") / max(1, len(letters))


def main() -> int:
    T = {r["src_pid"]: r for r in L("teacher.jsonl")}
    final = {}
    for st in STAGES:
        for r in L(st + ".jsonl"):
            if r["ok"] and r["src_pid"] not in final:
                ans = r.get("answer") or T[r["src_pid"]]["answer"]
                final[r["src_pid"]] = {"src_pid": r["src_pid"], "answer": ans, "stage": st,
                                       "gold": bool(T[r["src_pid"]].get("gold_nums")), "ko": round(ko_ratio(ans), 3)}
    (D / "final_pass.jsonl").write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in final.values()))
    print(len(final), dict(collections.Counter(v["stage"] for v in final.values())),
          "gold", sum(v["gold"] for v in final.values()), "영어(ko<0.5)", sum(v["ko"] < 0.5 for v in final.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
