#!/usr/bin/env python3
"""두 모델의 평가 결과를 문항별로 짝지어 비교한다 (McNemar 정확검정).

왜 짝지어 비교하는가 (docs/experiments/protocol.md):
두 모델이 **같은 문항**에 답하므로 문항 난이도는 두 모델에 공유된다. 실패율을 독립
비율로 비교하면 그 분산을 그대로 뒤집어쓰지만, 문항별로 짝지으면 상쇄된다.
yunsur_v7 에서 확인했듯 실패는 소수 문항에 뭉치고(36문항 중 2~4개), 문항별 실패율의
관측 분산이 시행 독립 가정의 1.4~2.5배다 — 즉 유효 표본은 시행 수가 아니라 문항 수에
가깝다. 그래서 반복을 늘리는 것보다 문항을 늘리는 것이 해상도를 올린다.

  python scripts/eval_pairwise.py <A.jsonl> <B.jsonl>
  python scripts/eval_pairwise.py A.jsonl B.jsonl --slot coding --rule any

무거운 임포트가 없다. 맥북에서도 즉시 돌아간다.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from math import comb
from pathlib import Path

RULES = ("majority", "any")


def _load(path: Path) -> tuple[dict[str, bool], dict[str, str], str]:
    """(문항→실패여부, 문항→슬롯, 모델명). 실패 판정은 --rule 로 정한다."""
    fails: dict[str, int] = defaultdict(int)
    total: dict[str, int] = defaultdict(int)
    slot: dict[str, str] = {}
    model = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        total[r["id"]] += 1
        slot[r["id"]] = r.get("slot", "?")
        model = r.get("model") or model
        if (not r.get("ok")) or r.get("quality_ok") is False:
            fails[r["id"]] += 1
    return dict(fails), slot, model, dict(total)


def _verdict(fails: dict, total: dict, rule: str) -> dict[str, bool]:
    if rule == "any":
        return {i: fails.get(i, 0) > 0 for i in total}
    return {i: fails.get(i, 0) * 2 > total[i] for i in total}  # majority


def parse_ids(spec: str) -> list[str]:
    """``planner_33-48,chat_02`` 같은 지정을 문항 id 목록으로 펼친다.

    범위는 ``<접두사>_<시작>-<끝>`` 이고 끝 번호는 **포함**이다. 자리수는 시작 번호의
    표기를 따른다 (``planner_09-12`` → planner_09 … planner_12).
    순서는 적은 순서를 지키고 중복은 없앤다.
    """
    out: list[str] = []
    for part in (p.strip() for p in spec.split(",")):
        if not part:
            continue
        head, sep, tail = part.rpartition("_")
        if sep and "-" in tail:
            lo_s, _, hi_s = tail.partition("-")
            if lo_s.isdigit() and hi_s.isdigit():
                lo, hi = int(lo_s), int(hi_s)
                if lo > hi:
                    raise SystemExit(f"--ids 범위가 거꾸로다: {part}")
                width = len(lo_s)
                out += [f"{head}_{n:0{width}d}" for n in range(lo, hi + 1)]
                continue
        out.append(part)
    seen: dict[str, None] = {}
    for i in out:
        seen.setdefault(i, None)
    return list(seen)


def _mcnemar_exact(b: int, c: int) -> float:
    """양측 이항검정. b, c 는 불일치 쌍의 두 방향 개수."""
    n = b + c
    if n == 0:
        return 1.0
    k = max(b, c)
    tail = sum(comb(n, j) for j in range(k, n + 1))
    return min(1.0, 2 * tail / 2**n)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("a", type=Path, help="A 모델 결과 jsonl")
    ap.add_argument("b", type=Path, help="B 모델 결과 jsonl")
    ap.add_argument("--slot", default="", help="한 슬롯만 (chat/rag/planner/coding). 기본: 전체 + 슬롯별")
    ap.add_argument("--ids", default="",
                    help="문항 id 만 골라 비교한다. 쉼표 구분이고 범위를 쓸 수 있다 "
                         "(예: planner_33-48 → planner_33 … planner_48). "
                         "사전 등록한 주 지표만 재는 데 쓴다")
    ap.add_argument("--rule", default="majority", choices=RULES,
                    help="문항 실패 판정: majority(과반 시행 실패) | any(한 번이라도 실패)")
    args = ap.parse_args()

    fa, sa, ma, ta = _load(args.a)
    fb, sb, mb, tb = _load(args.b)
    va = _verdict(fa, ta, args.rule)
    vb = _verdict(fb, tb, args.rule)

    common = sorted(set(va) & set(vb))
    if args.ids:
        want = parse_ids(args.ids)
        missing = [i for i in want if i not in set(va) & set(vb)]
        if missing:
            raise SystemExit(f"❌ --ids 에 두 결과에 없는 문항이 있다: {missing}")
        common = [i for i in sorted(common) if i in set(want)]
        print(f"--ids 로 {len(common)}문항만 비교한다: {args.ids}")
    only_a = sorted(set(va) - set(vb))
    only_b = sorted(set(vb) - set(va))
    print(f"A = {ma}  ({args.a.name}, 문항 {len(va)})")
    print(f"B = {mb}  ({args.b.name}, 문항 {len(vb)})")
    print(f"공통 문항 {len(common)}개 · 문항 실패 판정 규칙: {args.rule}")
    if only_a or only_b:
        print(f"⚠️ 한쪽에만 있는 문항 — A만 {only_a} B만 {only_b} (비교에서 제외)")

    slots = [args.slot] if args.slot else ["coding", "chat", "planner", "rag"]
    groups = [("전체", common)] if args.slot else [("전체", common)] + [
        (s, [i for i in common if sa.get(i) == s]) for s in slots
    ]
    if args.slot:
        groups = [(args.slot, [i for i in common if sa.get(i) == args.slot])]

    for name, ids in groups:
        if not ids:
            continue
        both = [i for i in ids if va[i] and vb[i]]
        a_only = [i for i in ids if va[i] and not vb[i]]
        b_only = [i for i in ids if vb[i] and not va[i]]
        neither = len(ids) - len(both) - len(a_only) - len(b_only)
        p = _mcnemar_exact(len(a_only), len(b_only))
        print(f"\n===== {name} (문항 {len(ids)}) =====")
        print(f"  둘 다 실패 {len(both)}  ·  A만 실패 {len(a_only)}  ·  B만 실패 {len(b_only)}  ·  둘 다 통과 {neither}")
        if a_only:
            print(f"  A만 실패: {a_only}")
        if b_only:
            print(f"  B만 실패: {b_only}")
        disc = len(a_only) + len(b_only)
        print(f"  불일치 쌍 {disc}개 → McNemar 양측 p = {p:.3f}"
              + ("  (유의)" if p < 0.05 else "  (유의하지 않음)"))
        if disc and p >= 0.05:
            need = 0
            for n in range(disc, 41):
                if _mcnemar_exact(n, 0) < 0.05:
                    need = n
                    break
            print(f"  → 한쪽으로 완전히 쏠려도 p<0.05 가 되려면 불일치 쌍 {need}개 이상 필요하다")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
