"""ce_rerank_1101 §3.2 판정 풀: held-out 두 실행 중 한쪽 컨텍스트에만 든 논문을 문항별로 모아 섞는다(조건 표시 없음)."""
import glob, json, random, re
from pathlib import Path

D = Path(__file__).parent; E = D.parent; R = E / "e2e_ko_1008/results"
bare = lambda p: re.sub(r"v\d+$", "", p or "")
qs = dict(line.rstrip("\n").split("\t")[:2] for line in open(E / "foundation_1031/heldout.tsv"))
arms = [{r["id"]: r for r in map(json.loads, open(R / f"pc{a}_heldout.jsonl"))} for a in (0, 1)]
meta = {}  # JSONL 제목 · 초록 먼저, 없으면 컨텍스트 블록에서
for f in ["raw_data_queue/crawled_papers.jsonl"] + glob.glob("raw_data_queue/processed/*.jsonl"):
    for line in open(f):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        meta.setdefault(bare(d.get("paper_id", "")), ((d.get("title") or "").strip(), re.sub(r"\s+", " ", d.get("abstract") or "").strip()))
for a in arms:
    for r in a.values():
        for blk in re.split(r"\n(?=\[문서 \d+\])", r.get("numbered_context") or ""):
            m = re.search(r"^\[([^\]\s]+?)(?:v\d+)?\] ([^\n]+)", blk, re.M)  # [ID] 제목 줄 — [문서 N] · [Distance: …] 는 빈칸이 있어 안 걸린다
            if m and m.group(1) not in meta:
                ab = re.search(r"\[초록\] ([^\n]+)", blk)
                meta[m.group(1)] = (m.group(2).strip(), ab.group(1).strip() if ab else "")
pairs = [{"q": q, "question": qs[q], "p": p} for q in arms[0]
         for p in sorted(set(arms[0][q]["context_papers"]) ^ set(arms[1][q]["context_papers"]))]
random.Random(11011).shuffle(pairs)
out = [dict(x, k=k, title=meta.get(x["p"], ("(제목 없음)", ""))[0], abstract=meta.get(x["p"], ("", ""))[1][:600])
       for k, x in enumerate(pairs)]
json.dump(out, open(D / "pool.json", "w"), ensure_ascii=False)
with open(D / "pool.txt", "w") as f:
    for o in out:
        f.write(f"[{o['k']}] Q: {o['question']}\n  T: {o['title']}\n  A: {o['abstract']}\n")
print("쌍", len(out), "· 문항", len({o["q"] for o in out}), "· 제목 없음", sum(o["title"] == "(제목 없음)" for o in out))
