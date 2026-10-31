"""survey_gate_1030 §2 판정 풀: sg0 · sg1 답 **본문**(📎 외부 검색 목록 앞)이 인용한 논문을 질문별로 합쳐 섞는다(조건 표시 없음).
외부 목록은 "내용은 요약하지 않음" 부록이고 목록 질문에만 붙어 처리 쪽만 늘리므로 주 지표에서 뺀다(판정 전 결정, README §5)."""
import json, random, re


def body_cites(r):
    body = (r.get("answer") or "").split("📎")[0]
    return [p for p in (r.get("answer_papers") or []) if p in body]

E = "docs/experiments/"; R = E + "e2e_ko_1008/results/"; D = E + "survey_gate_1030/"
qs = {}
for s in ("new", "old"):
    qs.update(l.rstrip("\n").split("\t")[:2] for l in open(D + f"{s}_questions.tsv"))
arms = [{json.loads(l)["id"]: json.loads(l) for s in ("new", "old") for l in open(R + f"{a}_{s}.jsonl")} for a in ("sg0", "sg1")]
meta, pairs = {}, []
for a in arms:
    for r in a.values():
        for blk in re.split(r"\n(?=\[문서 \d+\])", r.get("numbered_context") or ""):
            m = re.search(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\] ([^\n]+)", blk)
            if m and m.group(1) not in meta:
                ab = re.search(r"\[초록\] ([^\n]+)", blk)
                meta[m.group(1)] = (m.group(2).strip(), ab.group(1).strip() if ab else "")
for q in arms[0]:
    for p in dict.fromkeys(p for a in arms for p in body_cites(a[q])):
        pairs.append({"q": q, "question": qs[q], "p": p})
random.Random(10311).shuffle(pairs)
out = [dict(x, k=k, title=meta.get(x["p"], ("(제목 없음)", ""))[0], abstract=meta.get(x["p"], ("", ""))[1][:600]) for k, x in enumerate(pairs)]
json.dump(out, open(D + "pool.json", "w"), ensure_ascii=False)
print("쌍", len(out), "· 제목 없음", sum(o["title"] == "(제목 없음)" for o in out))
