"""canon_1110 후보 80편 중 코퍼스 JSONL 에 들어간 수를 찍는다(retry.sh 가 쓴다)."""
import glob
import json
import re

c = {p["id"] for p in json.load(open("docs/experiments/canon_1110/candidates.json", encoding="utf-8"))["papers"]}
got = set()
for f in sorted(glob.glob("raw_data_queue/processed/crawled_papers*.jsonl")) + ["raw_data_queue/crawled_papers.jsonl"]:
    for l in open(f, encoding="utf-8", errors="replace"):
        m = re.search(r'"paper_id":\s*"(\d{4}\.\d{4,5})', l)
        if m and m.group(1) in c:
            got.add(m.group(1))
print(len(got))
