"""cite_graph_1102 §4 판정: 수집 전(cg0_*) · 후(cg1_*), 검색만.

    .venv/bin/python docs/experiments/cite_graph_1102/score.py          # 주 지표 · 보호 1 · 보고
    .venv/bin/python docs/experiments/cite_graph_1102/score.py pool     # 보호 2 판정 풀 → pool.json
    .venv/bin/python docs/experiments/cite_graph_1102/score.py judged   # 보호 2 채점 ← judged.txt (qid<TAB>pid<TAB>0|1|2)
"""
import json
import math
import random
import re
import statistics
import sys
from pathlib import Path

R = Path("docs/experiments/e2e_ko_1008/results")
D = Path(__file__).resolve().parent
SETS = ("heldout", "162", "real40", "real2")


def norm(p):
    return re.sub(r"v\d+$", "", (p or "").strip())


def rows(label):
    return {r["id"]: r for r in map(json.loads, (R / f"{label}.jsonl").open(encoding="utf-8"))}


def ctx(r):
    return {norm(p) for p in r.get("doc_ids") or []}


def sign_p(a, b):
    """부호 검정 양측 p (동점 뺀 a : b)."""
    n, k = a + b, min(a, b)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n) if n else 1.0


def new_ids():
    return {p["id"] for p in json.loads((D / "candidates.json").read_text(encoding="utf-8"))["papers"]}


def main():
    orig = {o["id"]: {norm(g) for g in o["orig"]} for o in map(json.loads, (D / "orig.jsonl").open(encoding="utf-8"))}
    b, a = rows("cg0_heldout"), rows("cg1_heldout")
    hb = {q for q in orig if orig[q] & ctx(b[q])}
    ha = {q for q in orig if orig[q] & ctx(a[q])}
    gain, loss = sorted(ha - hb), sorted(hb - ha)
    p = sign_p(len(gain), len(loss))
    ok = len(gain) > len(loss) and p < 0.05
    print(f"주: held-out 원논문 {len(orig)}문항 — 컨텍스트에 원논문 {len(hb)} → {len(ha)} · "
          f"늘어남 {len(gain)} : 줄어듦 {len(loss)} · p {p:.4g} → {'통과' if ok else '미달'}")
    print("  늘어남", gain, "· 줄어듦", loss)
    new = new_ids()
    for s in SETS:
        b, a = rows(f"cg0_{s}"), rows(f"cg1_{s}")
        assert b.keys() == a.keys(), s
        ob, oa = sum(r["ok"] for r in b.values()), sum(r["ok"] for r in a.values())
        route = sum(b[q]["route"] != a[q]["route"] for q in b)
        changed = sum([norm(x) for x in b[q]["doc_ids"] or []] != [norm(x) for x in a[q]["doc_ids"] or []] for q in b)
        slots = sum(len(ctx(r) & new) for r in a.values())
        err = sum(bool(r["error"]) for r in (*b.values(), *a.values()))
        med = lambda rs, f: statistics.median(f(r) for r in rs.values())
        srch = lambda r: sum(sec for name, sec in r.get("stages") or [] if name == "search")
        verdict = "" if s == "heldout" else (" 통과" if ob - oa <= 2 else " 미달")
        print(f"{s}: ok {ob} → {oa} / {len(b)}{verdict} · 경로 다름 {route} · 컨텍스트 바뀜 {changed} · "
              f"수집 논문 자리 {slots} · 오류 행 {err} · 시간 중앙 {med(b, lambda r: r['elapsed']):.1f} → "
              f"{med(a, lambda r: r['elapsed']):.1f}s · 검색 중앙 {med(b, srch):.2f} → {med(a, srch):.2f}s")


def pool():
    """held-out 90 수집 후 컨텍스트에 든 수집 논문 (질문, 논문) 쌍 — 섞어서 판정용으로."""
    qs = dict(l.rstrip("\n").split("\t", 1) for l in Path("docs/experiments/foundation_1031/heldout.tsv").open(encoding="utf-8") if l.strip())
    meta = {p["id"]: p for p in json.loads((D / "candidates.json").read_text(encoding="utf-8"))["papers"]}
    pairs = [{"qid": q, "question": qs[q], "pid": p, "title": meta[p]["title"], "abstract": meta[p]["abstract"]}
             for q, r in rows("cg1_heldout").items() for p in sorted(ctx(r) & set(meta))]
    random.Random(1102).shuffle(pairs)
    (D / "pool.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=1), encoding="utf-8")
    print("쌍", len(pairs))


def judged():
    lab = [l.split("\t") for l in (D / "judged.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    n = len(lab)
    c = {k: sum(x[2].strip() == k for x in lab) for k in "012"}
    print(f"보호 2: 수집 논문 자리 {n} — '0' {c['0']} · '1' {c['1']} · '2' {c['2']} → "
          f"{'통과' if c['0'] * 3 <= n else '미달'} ('0' 1/3 이하)")


if __name__ == "__main__":
    {"pool": pool, "judged": judged}.get(sys.argv[1] if len(sys.argv) > 1 else "", main)()
