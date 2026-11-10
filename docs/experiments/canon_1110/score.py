"""canon_1110 §3 판정: 수집 전(cn0_*) · 후(cn1_*), 검색만.

    .venv/bin/python docs/experiments/canon_1110/score.py pool   # 판정 풀 → pool.json (대상 40 중 컨텍스트가 바뀐 문항 + held-out 수집 논문 자리)
    .venv/bin/python docs/experiments/canon_1110/score.py        # judged.txt(k<TAB>0|1|2)를 다 단 뒤 조건을 열고 채점
"""
import collections
import glob
import json
import math
import random
import re
import statistics
import subprocess
import sys
from pathlib import Path

E = Path("docs/experiments")
R = E / "e2e_ko_1008/results"
D = E / "canon_1110"
SETS = ("canon", "162", "real40", "real2", "ev30")
KNOWN16 = ["2005.11401", "2004.04906", "2002.08909", "2112.04426", "2208.03299", "2212.10496", "2305.06983", "2310.11511",
           "2401.15884", "2307.03172", "2302.00093", "2310.01558", "2309.01431", "2401.14887", "2401.00396", "2305.14627"]  # audit_1110 §2.1


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


assert abs(sign_p(20, 8) - 0.0357) < 5e-4 and abs(sign_p(9, 0) - 0.0039) < 5e-4


def tsv(path):
    return dict(l.rstrip("\n").split("\t", 1) for l in Path(path).open(encoding="utf-8") if l.strip())


def corpus():
    """코퍼스 JSONL 의 제목 · 초록. 판정 풀은 초록을 자르지 않는다(eval30_1110 §6.1)."""
    meta = {}
    for f in sorted(glob.glob("raw_data_queue/processed/crawled_papers*.jsonl")) + ["raw_data_queue/crawled_papers.jsonl"]:
        for l in open(f, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(l)
            except ValueError:
                continue
            m = re.match(r"(\d{4}\.\d{4,5})", str(d.get("paper_id") or ""))
            if m and m.group(1) not in meta:
                meta[m.group(1)] = (d.get("title") or "", d.get("abstract") or "")
    return meta


def cand():
    return json.loads((D / "candidates.json").read_text(encoding="utf-8"))


def pool():
    qs, hq = tsv(D / "questions.tsv"), tsv(E / "foundation_1031/heldout.tsv")
    b, a = rows("cn0_canon"), rows("cn1_canon")
    new = {p["id"] for p in cand()["papers"]}
    pairs = [("canon", q, qs[q], p) for q in qs if ctx(b[q]) != ctx(a[q]) for p in sorted(ctx(b[q]) | ctx(a[q]))]
    pairs += [("heldout", q, hq[q], p) for q, r in rows("cn1_heldout").items() for p in sorted(ctx(r) & new)]
    random.Random(1110).shuffle(pairs)
    meta = corpus()
    out = [{"k": k, "set": s, "q": q, "question": t, "p": p, "title": meta.get(p, ("", ""))[0], "abstract": meta.get(p, ("", ""))[1]}
           for k, (s, q, t, p) in enumerate(pairs)]
    (D / "pool.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("쌍", len(out), "· 대상", sum(x["set"] == "canon" for x in out), "· held-out", sum(x["set"] == "heldout" for x in out),
          "· 제목 없음", sum(not x["title"] for x in out))


def main():
    P = {x["k"]: x for x in json.loads((D / "pool.json").read_text(encoding="utf-8"))}
    J = {}
    for l in (D / "judged.txt").read_text(encoding="utf-8").splitlines():
        if l.strip():
            k, v = l.split()
            x = P[int(k)]
            J[(x["set"], x["q"], x["p"])] = int(v)
    assert len(J) == len(P), f"판정 {len(J)} / 풀 {len(P)}"
    C = cand()
    new = {p["id"] for p in C["papers"]}
    fixed_only = {p["id"] for p in C["papers"] if p["source"] == ["fixed"]}
    # 주 · 보호 3 · 보고 — 대상 40 (컨텍스트 집합이 같은 문항은 동점)
    b, a = rows("cn0_canon"), rows("cn1_canon")
    win = lose = win_nf = lose_nf = judged_q = slots = slots2 = 0
    zero, one, any2 = [0, 0], [0, 0], [0, 0]
    topic = collections.defaultdict(lambda: [0, 0])
    for q in b:
        if ctx(b[q]) == ctx(a[q]):
            continue
        judged_q += 1
        jb = [J[("canon", q, p)] for p in ctx(b[q])]
        ja = [J[("canon", q, p)] for p in ctx(a[q])]
        nb, na = jb.count(2), ja.count(2)
        na_nf = sum(J[("canon", q, p)] == 2 for p in ctx(a[q]) - fixed_only)
        win += na > nb
        lose += na < nb
        win_nf += na_nf > nb
        lose_nf += na_nf < nb
        t = f"T{(int(q[2:]) - 1) // 4 + 1:02d}"
        topic[t][0] += na > nb
        topic[t][1] += na < nb
        for i, js in enumerate((jb, ja)):
            zero[i] += js.count(0)
            one[i] += js.count(1)
            any2[i] += 2 in js
        slots += len(ctx(a[q]) & new)
        slots2 += sum(J[("canon", q, p)] == 2 for p in ctx(a[q]) & new)
    p = sign_p(win, lose)
    print(f"주: 대상 {len(b)}문항 중 컨텍스트 바뀜 {judged_q} — '2' 늘어남 {win} : 줄어듦 {lose} · p {p:.4g} → {'통과' if win > lose and p < 0.05 else '미달'}")
    print(f"  고정 목록에서만 온 논문 자리 빼고: {win_nf} : {lose_nf} · p {sign_p(win_nf, lose_nf):.4g}")
    print(f"보호 3: 판정한 문항 '0' 합 {zero[0]} → {zero[1]} → {'통과' if zero[1] <= zero[0] * 1.5 else '미달'}")
    print(f"보고: 판정한 문항 '2' 있음 {any2[0]} → {any2[1]} · '1' 합 {one[0]} → {one[1]} · 수집 논문 자리 {slots}(그중 '2' {slots2})")
    print("  주제별 늘어남 : 줄어듦", {k: f"{v[0]}:{v[1]}" for k, v in sorted(topic.items())})
    h = [v for (s, _, _), v in J.items() if s == "heldout"]
    print(f"보호 2: held-out 수집 논문 자리 {len(h)} — '0' {h.count(0)} · '1' {h.count(1)} · '2' {h.count(2)} → {'통과' if h.count(0) * 3 <= len(h) else '미달'}")
    med = lambda rs, f: statistics.median(f(r) for r in rs.values())
    srch = lambda r: sum(sec for name, sec in r.get("stages") or [] if name == "search")
    for s in SETS:
        b, a = rows(f"cn0_{s}"), rows(f"cn1_{s}")
        assert b.keys() == a.keys(), s
        ob, oa = sum(r["ok"] for r in b.values()), sum(r["ok"] for r in a.values())
        verdict = (" 통과" if ob - oa <= 2 else " 미달") if s in ("162", "real40", "real2") else ""
        print(f"{s}: ok {ob} → {oa} / {len(b)}{verdict} · 경로 다름 {sum(b[q]['route'] != a[q]['route'] for q in b)} · "
              f"검색어 다름 {sum(b[q].get('rag_queries') != a[q].get('rag_queries') for q in b)} · "
              f"컨텍스트 바뀜 {sum(ctx(b[q]) != ctx(a[q]) for q in b)} · 수집 논문 자리 {sum(len(ctx(r) & new) for r in a.values())} · "
              f"오류 {sum(bool(r.get('error')) for r in (*b.values(), *a.values()))} · "
              f"시간 중앙 {med(b, lambda r: r['elapsed']):.1f} → {med(a, lambda r: r['elapsed']):.1f}s · 검색 중앙 {med(b, srch):.2f} → {med(a, srch):.2f}s")
    a = rows("cn1_heldout")
    print(f"heldout(수집 후만): 수집 논문 자리 {sum(len(ctx(r) & new) for r in a.values())} · 오류 {sum(bool(r.get('error')) for r in a.values())}")
    for lab in ("cn0_ev30", "cn1_ev30"):
        out = subprocess.run([sys.executable, str(E / "eval30_1110/score.py"), lab], capture_output=True, text=True)
        print(f"--- eval30_1110/score.py {lab} (종료 코드 {out.returncode})\n{out.stdout.strip()}")
    g = {x["id"]: x for x in map(json.loads, (E / "eval30_1110/gold.jsonl").open(encoding="utf-8"))}
    b, a = rows("cn0_ev30"), rows("cn1_ev30")
    ms = {i: re.search(r"\d{4}\.\d{4,5}", str(x["absent_paper"])).group(0) for i, x in g.items() if x.get("absent_paper")}
    print("eval30 MS 원논문이 컨텍스트에 (전, 후):", {i: (pid in ctx(b[i]), pid in ctx(a[i])) for i, pid in ms.items()})
    for i in ("MU1", "MU1E"):
        gp = set(map(norm, g[i]["relevant_papers"]))
        print(f"eval30 {i}: 정답 {len(gp)}편 중 5편 안 {len(gp & ctx(b[i]))} → {len(gp & ctx(a[i]))}")
    db = set(corpus())
    top5 = [x for t in C["topics"] for x in t["top"][:5]]
    print(f"점검 지표: 잘 알려진 16편 보유 7 → {sum(k in db for k in KNOWN16)} · "
          f"주제별 인용 상위 5편(arXiv ID 있는 것) {sum(x['in_db'] for x in top5)} → {sum(x['id'] in db for x in top5)} / {len(top5)}")


if __name__ == "__main__":
    {"pool": pool}.get(sys.argv[1] if len(sys.argv) > 1 else "", main)()
