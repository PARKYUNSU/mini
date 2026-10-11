#!/usr/bin/env python3
"""거짓 부정·정답 없음 고지·자기모순을 두 답변 실행 사이에서 짝 비교한다 — yunsur_v13/v14 README §3.

  python3 scripts/nogold_metrics.py ans_v14 ans_v13

- 대상: 두 쪽 모두 direct_answer/B 이고 context_papers 가 같은 문항. 후처리 전 원문(eval 출력)으로 센다.
- 거짓 부정: 정답이 컨텍스트에 있는데 서론이 "문서에 없다".
- 정답 없음 일관 고지: 정답이 컨텍스트에 없을 때 서론·결론 모두 "없다".
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_blind_pairs import mcnemar_exact  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"
DENY = re.compile(r"제공된\s*(?:문서|텍스트|정보|자료)(?:들)?에는[^.]*?(?:없습니다|찾을 수 없습니다)")
NEG = re.compile(r"포함되어 있지 않|제공되지 않|찾을 수 없|명시되어 있지 않|존재하지 않|확인되지 않|없습니다")


def intro(a: str) -> str:
    return a.split("<b>본론</b>", 1)[0]


def concl(a: str) -> str:
    return a.split("<b>결론</b>", 1)[-1]


def main() -> int:
    a, b = sys.argv[1], sys.argv[2]
    gold = {json.loads(l)["id"]: set(json.loads(l)["relevant_papers"])
            for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    A = {m: {json.loads(l)["id"]: json.loads(l) for l in (RES / f"{m}.jsonl").read_text().splitlines()} for m in (a, b)}
    ids = [i for i in A[a] if i in A[b] and A[a][i]["route"] == A[b][i]["route"] == "direct_answer/B"
           and A[a][i]["context_papers"] == A[b][i]["context_papers"] and A[a][i].get("answer") and A[b][i].get("answer")]
    g = [i for i in ids if gold[i] & set(A[a][i]["context_papers"])]
    ng = [i for i in ids if i not in g]
    deny = {m: {i: bool(DENY.search(intro(A[m][i]["answer"]))) for i in ids} for m in (a, b)}
    cons = {m: {i: deny[m][i] and bool(NEG.search(concl(A[m][i]["answer"]))) for i in ids} for m in (a, b)}
    print(f"같은 컨텍스트 RAG {len(ids)}문항 · 정답 있음 {len(g)} · 정답 없음 {len(ng)}\n")
    print(f"{'':<22}{a:>10}{b:>10}")
    rows = [("거짓 부정(정답 있음)", lambda m: sum(deny[m][i] for i in g)),
            ("자기모순(전체)", lambda m: sum(deny[m][i] and not cons[m][i] for i in ids)),
            ("일관 고지(정답 없음)", lambda m: sum(cons[m][i] for i in ng)),
            ("어디든 '없다'(정답 없음)", lambda m: sum(bool(NEG.search(A[m][i]["answer"])) for i in ng)),
            ("첫 항목 정답(정답 있음)", lambda m: sum(bool(A[m][i].get("answer_first_ok")) for i in g))]
    for name, f in rows:
        print(f"{name:<22}{f(a):>10}{f(b):>10}")
    for name, d, S in [("거짓 부정", deny, g), ("일관 고지", cons, ng)]:
        x = sum(d[a][i] and not d[b][i] for i in S)
        y = sum(d[b][i] and not d[a][i] for i in S)
        print(f"\n{name} 짝: {a}만 {x} · {b}만 {y} · McNemar 정확 p={mcnemar_exact(x, y):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
