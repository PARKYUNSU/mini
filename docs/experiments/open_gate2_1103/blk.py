"""눈가림 유지: 두 조건 컨텍스트에서 한 논문 블록 중 가장 긴 것만 출력(어느 쪽인지 안 보임)."""
import json, re, sys

R = "docs/experiments/e2e_ko_1008/results/"
qid, pids = sys.argv[1], sys.argv[2:]
rows = []
for lb in ("ogb0_s2", "ogb1_s2"):
    try:
        rows += [j for j in map(json.loads, open(R + lb + ".jsonl", encoding="utf-8")) if j["id"] == qid]
    except FileNotFoundError:
        pass
for pid in pids:
    best = ""
    for j in rows:
        for b in re.split(r"\n(?=\[문서 \d+\]\n)", j.get("numbered_context") or ""):
            if pid in b[:400] and len(b) > len(best):
                best = b
    print(f"===== {pid}\n{best[:5000]}\n")
