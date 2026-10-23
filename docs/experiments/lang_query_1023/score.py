"""lang_query_1023 §3 판정 (맥미니)."""
import json, re
from collections import Counter
from math import comb
from pathlib import Path

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"
A = ("ko", "en_plain", "en_term")
load = lambda a, s: {json.loads(l)["id"]: json.loads(l) for l in open(R / f"lq_{a}_{s}.jsonl")}
mc = lambda b, c: 1.0 if b + c == 0 else min(1, 2 * sum(comb(b + c, i) for i in range(min(b, c) + 1)) / 2 ** (b + c))
real = {a: {(s, k): v for s in ("real40", "real2") for k, v in load(a, s).items()} for a in A}
keys = [k for k in real["ko"] if all(k in real[a] for a in A)]
for a in A:
    rt = Counter(real[a][k]["route"] for k in keys)
    print(f"{a}: real 74 검색 ok {sum(real[a][k]['ok'] for k in keys)} · 경로 {dict(rt)}")
for x, y in (("en_plain", "ko"), ("en_term", "en_plain")):
    b = sum(real[x][k]["ok"] and not real[y][k]["ok"] for k in keys); c = sum(real[y][k]["ok"] and not real[x][k]["ok"] for k in keys)
    print(f"   {x} 대 {y}: real 74 얻음 {b} : 잃음 {c}, p={mc(b, c):.4f}")
    top = [k for k in keys if k[1][0] in "TR"]
    b2 = sum(real[x][k]["ok"] and not real[y][k]["ok"] for k in top); c2 = sum(real[y][k]["ok"] and not real[x][k]["ok"] for k in top)
    print(f"   {x} 대 {y}: real 주제형 T·R {len(top)} 얻음 {b2} : 잃음 {c2}, p={mc(b2, c2):.4f}")
ASP = json.load(open(EXP / "aspect_split_1022/aspects.json"))
for a in A:
    m = load(a, "m12")
    cov = sum(bool(set(m[q].get("doc_ids") or []) & set(v)) for q, asp in ASP.items() if q in m for v in asp.values())
    cs = load(a, "cs3"); gold = {json.loads(l)["id"]: set(json.loads(l)["relevant_papers"]) for l in open(EXP / "corpus_seed_1023/gold.jsonl")}
    print(f"{a}: 조건 커버 {cov}/24 · R01–R04 컨텍스트 gold {[len(set(cs[q].get('doc_ids') or []) & gold[q]) for q in ('R01','R02','R03','R04')]} · "
          f"경로(M12) {dict(Counter(v['route'] for v in m.values()))}")
for q in ("M01", "M04", "M10"):
    print(q, {a: (load(a, "m12")[q].get("rag_queries") or [""])[0][:90] for a in A})
