"""판정용 파일: 문항마다 경로 · 시간 · 컨텍스트 논문 · 답 · 본론 인용 논문 초록."""
import glob, json, re
from pathlib import Path
D = Path("docs/experiments/user_suite_1027")
AB = {}
for f in ["raw_data_queue/crawled_papers.jsonl"] + glob.glob("raw_data_queue/processed/*.jsonl"):
    for l in open(f):
        try: d = json.loads(l)
        except ValueError: continue
        AB.setdefault(re.sub(r"v\d+$", "", d.get("paper_id", "")), (d.get("title", ""), re.sub(r"\s+", " ", d.get("abstract") or "")))
qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(D / "questions.tsv")}
with open(D / "judge.md", "w") as w:
    for r in map(json.loads, open("docs/experiments/e2e_ko_1008/results/us_1027.jsonl")):
        a = r.get("answer") or "(없음)"
        w.write(f"######## {r['id']} | {qs[r['id']]} | {r.get('route')} | {r.get('elapsed')}s\n")
        w.write("컨텍스트: " + ", ".join(re.sub(r"v\d+$", "", x) for x in (r.get("doc_ids") or [])) + "\n")
        w.write("=== 답\n" + a.split("📎")[0].strip() + "\n")
        for p in dict.fromkeys(re.findall(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]", a.split("📎")[0])):
            t, ab = AB.get(p, ("?", ""))
            w.write(f"--- [{p}] {t[:90]} :: {ab[:650]}\n")
        w.write("\n")
