#!/usr/bin/env python3
"""정답 유무 — 검색 점수 임계값(§5)과 초록 발췌 원인 확인(§6). docs/experiments/presence_judge_1011/README.md

  python3 scripts/presence_signal_analysis.py
"""
from __future__ import annotations

import glob
import json
import re
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"
EXP = ROOT / "docs" / "experiments" / "presence_judge_1011"
AQ = ROOT / "docs" / "experiments" / "answer_quality_1010"


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """2x2 [[a,b],[c,d]] Fisher 정확 검정(양측)."""
    n, r1, c1 = a + b + c + d, a + b, a + c

    def p(x: int) -> float:
        return comb(c1, x) * comb(n - c1, r1 - x) / comb(n, r1)

    obs = p(a)
    lo, hi = max(0, r1 + c1 - n), min(r1, c1)
    return min(1.0, sum(p(x) for x in range(lo, hi + 1) if p(x) <= obs * (1 + 1e-9)))


def load_abstracts() -> dict[str, str]:
    out: dict[str, str] = {}
    files = sorted(glob.glob(str(ROOT / "raw_data_queue/processed/crawled_papers*.jsonl")))
    files.append(str(ROOT / "raw_data_queue/crawled_papers.jsonl"))
    for f in files:
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("paper_id"):
                out[re.sub(r"v\d+$", "", d["paper_id"])] = d.get("abstract") or ""
    return out


def blocks(ctx: str) -> dict[int, str]:
    parts = re.split(r"^\[문서 (\d{1,2})\]\s*$", ctx, flags=re.M)
    return {int(parts[k]): parts[k + 1] for k in range(1, len(parts) - 1, 2)}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def main() -> int:
    C = {json.loads(l)["id"]: json.loads(l) for l in (RES / "ctx_1011.jsonl").read_text().splitlines()}
    gold = {json.loads(l)["id"]: {re.sub(r"v\d+$", "", g) for g in json.loads(l)["relevant_papers"]}
            for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    J = {json.loads(l)["id"]: json.loads(l) for l in (EXP / "judge_yunsur_v13.jsonl").read_text().splitlines()}
    ids = sorted(J)
    rows = []
    for i in ids:
        ctx = C[i]["numbered_context"]
        dists = [float(x) for x in re.findall(r"\[Distance: ([\d.]+)\]", ctx)]
        rows.append({"id": i, "gold": J[i]["gold_in_context"], "min_d": min(dists) if dists else 9.0})

    # §5 임계값
    g = [r for r in rows if r["gold"]]
    ng = [r for r in rows if not r["gold"]]
    pos = sorted(r["min_d"] for r in ng)
    neg = sorted(r["min_d"] for r in g)
    auc = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))
    best = None
    for t in sorted({r["min_d"] for r in rows} | {0.0}):
        fn = sum(r["min_d"] > t for r in g)
        rec = sum(r["min_d"] > t for r in ng)
        if fn <= 0.05 * len(g) and (best is None or rec > best[2]):
            best = (t, fn, rec)
    print("== §5 검색 점수 임계값 (최소 Distance > t → 없음) ==")
    print(f"정답 있음 {len(g)} · 없음 {len(ng)} · AUC {auc:.3f}")
    print(f"정답 있음 min_d 중앙 {neg[len(neg) // 2]:.3f} · 정답 없음 min_d 중앙 {pos[len(pos) // 2]:.3f}")
    if best:
        t, fn, rec = best
        print(f"거짓 '없음' ≤ 5% 를 지키는 최적 t={t:.4f}: 거짓 '없음' {fn}/{len(g)} · 재현 {rec}/{len(ng)}")
        print(f"표본 안 최적으로도 기준(재현 ≥ 7): {'통과(상한 — 새 문항 검증 필요)' if rec >= 7 else '미달 → 기각'}")

    # §6 초록 발췌
    ab = load_abstracts()
    q_ok = {}
    for f in ("judged_gptoss_ans_v13.jsonl",):
        p = AQ / f
        if p.exists():
            q_ok = {json.loads(l)["id"]: json.loads(l) for l in p.read_text().splitlines()}
    A = {json.loads(l)["id"]: json.loads(l) for l in (RES / "ans_v13.jsonl").read_text().splitlines()}
    split = {True: [], False: []}
    for i in ids:
        if not J[i]["gold_in_context"]:
            continue
        bl = blocks(C[i]["numbered_context"])
        has = False
        for n in J[i]["gold_nums"]:
            body = bl.get(n, "")
            pid = C[i]["doc_ids"][n - 1]
            head = norm(ab.get(pid, ""))[:120]
            if re.search(r"abstract", body, re.I) or (head and head[:80] in norm(body)):
                has = True
        split[has].append(i)
    print("\n== §6 정답 블록에 초록이 있는가 ==")
    for has in (True, False):
        S = split[has]
        fn = sum(J[i]["pick"] == "없음" for i in S)
        first = sum(bool(A[i].get("answer_first_ok")) for i in S)
        ok = [q_ok[i].get("description") in ("correct", "partial") for i in S if q_ok.get(i, {}).get("judged")]
        print(f"초록 {'있음' if has else '없음'} {len(S)}: 판정 거짓 '없음' {fn} ({fn / max(len(S), 1):.1%}) · "
              f"v13 첫 항목 정답 {first}/{len(S)} · gpt-oss ok {sum(ok)}/{len(ok)}")
    a = sum(J[i]["pick"] == "없음" for i in split[False]); b = len(split[False]) - a
    c = sum(J[i]["pick"] == "없음" for i in split[True]); d = len(split[True]) - c
    print(f"Fisher 정확(거짓 '없음' 초록 없음 vs 있음): p={fisher_two_sided(a, b, c, d):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
