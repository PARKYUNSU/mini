"""doc_slots_1111 §2 보호 세트 고르기 (측정 전 고정, seed 1111).

    .venv/bin/python docs/experiments/doc_slots_1111/build_set.py

- 162 에서 무작위 40문항 → ids_162s.txt
- real40 의 수치(N) · 비교(C) 26문항 → ids_realnc.txt
"""
import json
import random

E = "docs/experiments/"
D = E + "doc_slots_1111/"
ids162 = [l.split("\t")[0] for l in open(E + "e2e_ko_1008/ko_questions.tsv", encoding="utf-8") if l.strip()]
pick = sorted(random.Random(1111).sample(ids162, 40))
open(D + "ids_162s.txt", "w").write(",".join(pick) + "\n")
nc = [json.loads(l)["id"] for l in open(E + "real_eval_1013/spec.jsonl", encoding="utf-8") if json.loads(l)["type"] in ("N", "C")]
open(D + "ids_realnc.txt", "w").write(",".join(nc) + "\n")
print(f"162 표본 {len(pick)} / {len(ids162)} · real40 N·C {len(nc)}")
assert len(pick) == 40 and len(nc) == 26
