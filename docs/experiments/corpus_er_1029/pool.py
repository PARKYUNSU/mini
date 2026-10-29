"""corpus_er_1029 §2 판정 풀: ce0 · ce1 대상 12문항 컨텍스트 논문을 질문별로 합쳐 섞는다(조건 표시 없음)."""
import json, random, re
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "corpus_er_1029/"
qs = dict(l.rstrip("\n").split("\t")[:2] for l in open(D + "questions.tsv"))
arms = [{json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}_er.jsonl")} for a in ("ce0", "ce1")]
meta, pairs = {}, []
for a in arms:
    for r in a.values():
        for blk in re.split(r"\n(?=\[문서 \d+\])", r.get("numbered_context") or ""):
            m = re.search(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\] ([^\n]+)", blk)
            if m and m.group(1) not in meta:
                ab = re.search(r"\[초록\] ([^\n]+)", blk)
                meta[m.group(1)] = (m.group(2).strip(), ab.group(1).strip() if ab else "")
for q in arms[0]:
    for p in dict.fromkeys(p for a in arms for p in (a[q].get("doc_ids") or a[q]["context_papers"])):
        pairs.append({"q": q, "question": qs[q], "p": p})
random.Random(10291).shuffle(pairs)
out = [dict(x, k=k, title=meta.get(x["p"], ("(제목 없음)", ""))[0], abstract=meta.get(x["p"], ("", ""))[1][:600]) for k, x in enumerate(pairs)]
json.dump(out, open(D + "pool.json", "w"), ensure_ascii=False)
print("쌍", len(out), "· 제목 없음", sum(o["title"] == "(제목 없음)" for o in out))
