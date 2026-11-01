"""conclusion_struct_1102 §3 채점 — 라벨을 다 쓴 뒤에만 돌린다(열쇠를 연다).

    .venv/bin/python docs/experiments/conclusion_struct_1102/score.py cs1_heldout

judge/labels.tsv(qid \t sN \t O|E|X|U|F|?) · judge/p1_labels.tsv(qid \t A|B|같음) · judge/key.json · results/{LABEL}.jsonl.
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
RES = D.parent / "e2e_ko_1008" / "results"
ERR = {"E", "X", "U"}


def sign_p(w: int, l: int) -> float:
    """양쪽 정확 부호 검정."""
    n = w + l
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n) if n else 1.0


def main() -> None:
    assert abs(sign_p(6, 0) - 0.03125) < 1e-9 and abs(sign_p(5, 0) - 0.0625) < 1e-9 and sign_p(0, 0) == 1.0
    lab = sys.argv[1]
    J = D / (sys.argv[2] if len(sys.argv) > 2 else "judge")  # dev 시험은 다른 폴더로
    rows = {r["id"]: r for r in map(json.loads, (RES / f"{lab}.jsonl").open(encoding="utf-8")) if r["changed"]}
    key = json.loads((J / "key.json").read_text(encoding="utf-8"))
    labels = {}
    for line in (J / "labels.tsv").open(encoding="utf-8"):
        if line.strip():
            qid, s, v = line.rstrip("\n").split("\t")
            labels[(qid, s)] = v.strip()
    missing = [(q, s) for q, m in key["sentences"].items() for s in m if (q, s) not in labels]
    assert not missing, f"라벨 빠짐 {missing[:5]}"
    win = lose = tie = 0
    cnt = {"전": Counter(), "후": Counter()}
    by_slot = Counter()
    for qid, m in key["sentences"].items():
        err = {"전": 0, "후": 0}
        for s, (side, _) in m.items():
            v = labels[(qid, s)]
            cnt[side][v] += 1
            err[side] += v in ERR
        if err["후"] < err["전"]:
            win += 1
            by_slot[rows[qid]["slot"], "이김"] += 1
        elif err["후"] > err["전"]:
            lose += 1
            by_slot[rows[qid]["slot"], "짐"] += 1
        else:
            tie += 1
    n = len(key["sentences"])
    print(f"주 지표: 바뀐 답 {n} · 이김 {win} · 짐 {lose} · 동점 {tie} · 부호 검정 p {sign_p(win, lose):.4g}"
          f" · {'통과' if sign_p(win, lose) < 0.05 else '미달'}")
    print(f"그만두기 조건: 바뀐 답 {n} (< 20 이면 멈춤) · 동점 뺀 답 {win + lose} (< 6 이면 멈춤)")
    for side in ("전", "후"):
        print(f"  {side} 문장 라벨 {dict(cnt[side])}")
    print("  갈래별", dict(sorted(by_slot.items())))
    p1 = dict(line.rstrip("\n").split("\t") for line in (J / "p1_labels.tsv").open(encoding="utf-8") if line.strip())
    assert set(p1) == set(key["p1_d_is"]), "보호 1 라벨 빠짐"
    worse = sum(1 for q, v in p1.items() if v in "AB" and v != key["p1_d_is"][q])
    better = sum(1 for q, v in p1.items() if v in "AB" and v == key["p1_d_is"][q])
    cap = max(2, math.floor(0.1 * n))
    print(f"보호 1: D 쪽이 나쁨 {worse} · 나음 {better} · 같음 {n - worse - better} · 한도 {cap} · {'통과' if worse <= cap else '미달'}")
    diff = sum(not r["cited_same"] for r in rows.values())
    print(f"보호 2: 인용 집합 다른 답 {diff} · 본론 밖 뺌 {sum(r['dropped'] for r in rows.values())} · {'통과' if diff == 0 else '미달'}")
    med = statistics.median(r["tsec"] for r in rows.values())
    print(f"보호 3: 번역 초 중앙 {med:.1f} · {'통과' if med <= 15 else '미달'}")
    fb = Counter(w.split()[0] for r in rows.values() for w in r["fallback"])
    put = sum(len(p["after"]) for r in rows.values() for p in r["pairs"])
    print(f"보고: 넣은 문장 {put} · 영어로 둠 {sum(fb.values())} {dict(fb)} · F 전 {cnt['전']['F']} 후 {cnt['후']['F']}")


if __name__ == "__main__":
    main()
