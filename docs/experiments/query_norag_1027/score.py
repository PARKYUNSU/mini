"""query_norag_1027 §3 채점 (판정 끝난 뒤 조건 열기)."""
import json, re
from math import comb
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "query_norag_1027/"
pool = {x["k"]: x for x in json.load(open(D + "pool.json"))}
J = {k: v for k, v in json.load(open(D + "reused.json")).items()}
for l in open(D + "judged.txt"):
    k, v = l.split(); J[f"{pool[int(k)]['q']}|{pool[int(k)]['p']}"] = int(v)
def sign(w, l):
    n = w + l
    return 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n)
load = lambda a, s: {json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}_{s}.jsonl")}
ctx = lambda r: r.get("doc_ids") or r["context_papers"]
print("보호 — 정답 세트 검색 ok")
for s in ("162", "real40", "real2"):
    a, b = load("rn0", s), load("rn1", s)
    print(f"  {s}: {sum(r['ok'] for r in a.values())} → {sum(r['ok'] for r in b.values())} / {len(a)} (처리만 ok {sum(b[q]['ok'] and not a[q]['ok'] for q in a)} · 대조만 {sum(a[q]['ok'] and not b[q]['ok'] for q in a)})")
QA = {"H": E + "corpus_seed_1020/heldout_questions.tsv", "D": E + "corpus_seed_1020/discovery_questions.tsv", "U": E + "user_suite_1027/questions.tsv"}
asks = re.compile(r"rag|retrieval[- ]augmented|검색\s*증강|리트리벌", re.I)
w = l = 0; tot = {"rn0": 0, "rn1": 0}; ko = {"rn0": 0, "rn1": 0}; rq = {"rn0": 0, "rn1": 0}; noq = chg = 0
for s, f in QA.items():
    qs = dict(x.rstrip("\n").split("\t")[:2] for x in open(f) if "\t" in x)
    a = {"rn0": load("rn0", s), "rn1": load("rn1", s)}
    sw = sl = 0
    for q in a["rn0"]:
        n = {k: sum(J[f"{q}|{p}"] == 2 for p in ctx(a[k][q])) for k in a}
        for k in a:
            tot[k] += n[k]; qq = " ".join(a[k][q].get("rag_queries") or [])
            ko[k] += bool(re.search(r"[가-힣]", qq))
            if not asks.search(qs[q]): rq[k] += bool(re.search(r"\brag\b|retrieval[- ]augmented", qq, re.I))
        noq += not asks.search(qs[q]); chg += (a["rn0"][q].get("rag_queries") or [""])[0] != (a["rn1"][q].get("rag_queries") or [""])[0]
        sw += n["rn1"] > n["rn0"]; sl += n["rn1"] < n["rn0"]
    print(f"  [{s}] '2' 늘어남 {sw} : 줄어듦 {sl}")
    w += sw; l += sl
print(f"주: '2' 합 {tot['rn0']} → {tot['rn1']} | 늘어남 {w} : 줄어듦 {l} · p {sign(w, l):.4f}")
print(f"보호: 검색어에 한글 남음 {ko['rn0']} → {ko['rn1']}")
print(f"보고: 질문에 RAG 없음 {noq} 문항 중 검색어에 rag {rq['rn0']} → {rq['rn1']} · 첫 검색어 바뀜 {chg}/98")
G = {"U1-4": ["2503.17229", "2508.14314"], "U2-3": ["2403.12968", "2410.12388", "2508.15813"], "U2-5": ["2411.13154", "2305.14283"], "U5-2": ["2606.25674"]}
u = {k: load(k, "U") for k in ("rn0", "rn1")}
for q, g in G.items():
    print(f"  {q}: 대조 {[p for p in g if p in ctx(u['rn0'][q])]} · 처리 {[p for p in g if p in ctx(u['rn1'][q])]} | 처리 검색어 {u['rn1'][q]['rag_queries'][0]!r}")
