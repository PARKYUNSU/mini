"""flag_cleanup_1101 §2 판정: 정리 전(cb_*) · 뒤(ca_*) 컨텍스트 논문(doc_ids, 순서 포함) 대조."""
import json

R = "docs/experiments/e2e_ko_1008/results/"
same = diff = llm = err = 0
for s in ("new", "old"):
    b, a = ({r["id"]: r for r in map(json.loads, open(R + f"{p}_{s}.jsonl"))} for p in ("cb", "ca"))
    assert a.keys() == b.keys(), s
    err += sum(bool(r["error"]) for r in [*a.values(), *b.values()])
    for q in b:
        if b[q]["rag_queries"] != a[q]["rag_queries"] or b[q]["route"] != a[q]["route"]:
            llm += 1
            print(s, q, "검색어·경로 다름(LLM 흔들림)", b[q]["route"], "→", a[q]["route"])
        elif b[q]["doc_ids"] == a[q]["doc_ids"]:
            same += 1
        else:
            diff += 1
            print(s, q, "전", b[q]["doc_ids"], "후", a[q]["doc_ids"])
print(f"같음 {same} · 다름 {diff} · 검색어·경로 다름 {llm} · 오류 행 {err} → {'통과' if diff == 0 else '미달 — 정리 고침'}")
