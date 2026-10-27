"""fusion_protect_1027 §2 판정 풀: rn0 · rn1 컨텍스트 논문(H · D · U)을 질문별로 합쳐, 이미 판정한 쌍은 재사용하고 새 쌍만 섞는다(조건 표시 없음)."""
import json, random, re
E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "fusion_protect_1027/"; QN = E + "query_norag_1027/"
QF = {"H": E + "corpus_seed_1020/heldout_questions.tsv", "D": E + "corpus_seed_1020/discovery_questions.tsv", "U": E + "user_suite_1027/questions.tsv"}
old = {}  # (질문 글, 논문) -> 판정
for s in ("H", "D", "qc"):
    pool = {x["k"]: x for x in json.load(open(f".cron/cs/pool_{s}.json"))}
    for l in open(f".cron/cs/judged_{s}.txt"):
        k, v = l.split(); old[(pool[int(k)]["question"].strip(), pool[int(k)]["p"])] = int(v)
qp = {x["k"]: x for x in json.load(open(QN + "pool.json"))}  # query_norag_1027 판정도 재사용
for l in open(QN + "judged.txt"):
    k, v = l.split(); old[(qp[int(k)]["question"].strip(), qp[int(k)]["p"])] = int(v)
meta, pairs, reuse = {}, [], {}
for S, f in QF.items():
    qs = dict(l.rstrip("\n").split("\t")[:2] for l in open(f) if "\t" in l)
    arms = [{json.loads(l)["id"]: json.loads(l) for l in open(R + f"{a}_{S}.jsonl")} for a in ("fp0", "fp1")]
    for a in arms:
        for r in a.values():
            for blk in re.split(r"\n(?=\[문서 \d+\])", r.get("numbered_context") or ""):
                m = re.search(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\] ([^\n]+)", blk)
                if m and m.group(1) not in meta:
                    ab = re.search(r"\[초록\] ([^\n]+)", blk)
                    meta[m.group(1)] = (m.group(2).strip(), ab.group(1).strip() if ab else "")
    for q in arms[0]:
        ps = list(dict.fromkeys(p for a in arms for p in (a[q].get("doc_ids") or a[q]["context_papers"])))
        for p in ps:
            key = (qs[q].strip(), p)
            if key in old: reuse[f"{q}|{p}"] = old[key]
            else: pairs.append({"q": q, "question": qs[q], "p": p})
random.Random(10271).shuffle(pairs)
out = [dict(x, k=k, title=meta.get(x["p"], ("(제목 없음)", ""))[0], abstract=meta.get(x["p"], ("", ""))[1][:600]) for k, x in enumerate(pairs)]
json.dump(out, open(D + "pool.json", "w"), ensure_ascii=False)
json.dump(reuse, open(D + "reused.json", "w"), ensure_ascii=False)
print("새 쌍", len(out), "· 재사용", len(reuse), "· 제목 없음", sum(o["title"] == "(제목 없음)" for o in out))
