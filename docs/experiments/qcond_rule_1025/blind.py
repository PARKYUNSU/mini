"""qcond_rule_1025 눈가림 판정 파일: 질문마다 cr0 · cr1 답을 A · B 로 섞고, 각 답이 본 블록의 제목 · 발행일을 붙인다."""
import json, random, re
from pathlib import Path

D = Path(__file__).parent; R = D.parent / "e2e_ko_1008/results"
qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(D / "questions.tsv")}
arms = {a: {r["id"]: r for r in map(json.loads, open(R / f"{a}.jsonl"))} for a in ("cr0", "cr1")}
rnd = random.Random(1025); key = {}


def blocks(r):
    out = []
    for b in (r.get("numbered_context") or "").split("\n\n---\n\n"):
        d = re.search(r"\[발행일:\s*([\d-]+)", b); t = re.search(r"\[(\d{4}\.\d{4,5}v\d+)\]\s*([^\[\n]{0,90})", b)
        if t:
            out.append(f"  [{d.group(1) if d else '?'}] {t.group(1)} {t.group(2).strip()}")
    return out


with open(D / "blind.md", "w") as w:
    for q in qs:
        order = ["cr0", "cr1"]; rnd.shuffle(order); key[q] = order
        w.write(f"######## {q} | {qs[q]}\n")
        for tag, a in zip("AB", order):
            r = arms[a].get(q, {})
            w.write(f"=== {q}{tag} route {r.get('route')}\n" + "\n".join(blocks(r)) + "\n--- 답\n")
            w.write(re.sub(r"\n📎.*", "", (r.get("answer") or "(없음)"), flags=re.S).strip() + "\n\n")
json.dump(key, open(D / "blind_key.json", "w"))
print("ok")
