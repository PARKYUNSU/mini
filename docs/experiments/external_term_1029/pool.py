"""external_term_1029 §2 판정 풀: 두 조건 외부 논문을 질문별로 합쳐 섞는다(조건 표시 없음)."""
import json, random
D = "docs/experiments/external_term_1029/"
qs = dict(l.rstrip("\n").split("\t")[:2] for l in open("docs/experiments/nodoc_conclusion_1029/questions.tsv"))
pairs = []
for l in open(D + "results.jsonl"):
    r = json.loads(l); seen = {}
    for it in r["et0"] + r["et1"]:
        seen.setdefault(it["title"], it)
    for t, it in seen.items():
        pairs.append({"q": r["id"], "question": qs[r["id"]], "title": t, "abstract": (it.get("abstract") or "")[:600]})
random.Random(10291).shuffle(pairs)
for k, p in enumerate(pairs):
    p["k"] = k
json.dump(pairs, open(D + "pool.json", "w"), ensure_ascii=False)
for p in pairs:
    print(f"## {p['k']} Q: {p['question']}\n  T: {p['title']}\n  A: {p['abstract'][:350]}\n")
