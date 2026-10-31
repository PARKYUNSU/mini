import json, sys
R = "docs/experiments/e2e_ko_1008/results/"
same = diff = 0
for s in ("new", "old"):
    try:
        b = {json.loads(l)["id"]: json.loads(l) for l in open(R + f"sg0_{s}.jsonl")}
        a = [json.loads(l) for l in open(R + f"fc_{s}.jsonl")]
    except FileNotFoundError:
        continue
    for r in a:
        x, y = b[r["id"]]["doc_ids"], r["doc_ids"]
        if x == y:
            same += 1
        else:
            diff += 1
            print(s, r["id"], "전", x, "후", y, "| 검색어", b[r["id"]]["rag_queries"][-1:] == r["rag_queries"][-1:])
print("같음", same, "다름", diff)
