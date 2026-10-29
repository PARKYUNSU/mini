"""query_glossary_1029 §2 판정 풀: 검색어가 바뀐 문항(g · sub · er)의 두 조건 컨텍스트 논문을 섞는다(조건 표시 없음)."""
import json, random, re
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "query_glossary_1029/"
QF = {"g": D + "g_questions.tsv", "sub": D + "sub_questions.tsv", "er": E + "corpus_er_1029/questions.tsv"}
meta, pairs, changed = {}, [], {}
for S, f in QF.items():
    qs = dict(l.rstrip("\n").split("\t")[:2] for l in open(f) if "\t" in l)
    arms = [{json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}_{S}.jsonl")} for a in ("qg0", "qg1")]
    for a in arms:
        for r in a.values():
            for blk in re.split(r"\n(?=\[문서 \d+\])", r.get("numbered_context") or ""):
                m = re.search(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\] ([^\n]+)", blk)
                if m and m.group(1) not in meta:
                    ab = re.search(r"\[초록\] ([^\n]+)", blk)
                    meta[m.group(1)] = (m.group(2).strip(), ab.group(1).strip() if ab else "")
    changed[S] = [q for q in arms[0] if arms[0][q]["rag_queries"][:1] != arms[1][q]["rag_queries"][:1]]
    for q in changed[S]:
        for p in dict.fromkeys(p for a in arms for p in (a[q].get("doc_ids") or a[q]["context_papers"])):
            pairs.append({"q": f"{S}|{q}", "question": qs[q], "p": p})
random.Random(10292).shuffle(pairs)
out = [dict(x, k=k, title=meta.get(x["p"], ("(제목 없음)", ""))[0], abstract=meta.get(x["p"], ("", ""))[1][:600]) for k, x in enumerate(pairs)]
json.dump(out, open(D + "pool.json", "w"), ensure_ascii=False)
json.dump(changed, open(D + "changed.json", "w"))
print("쌍", len(out), "· 바뀐 문항", {k: len(v) for k, v in changed.items()}, "· 제목 없음", sum(o["title"] == "(제목 없음)" for o in out))
