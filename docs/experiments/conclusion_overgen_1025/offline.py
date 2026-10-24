"""conclusion_overgen_1025 오프라인 (맥미니): 새 답(cov_new)에 drop_bundled 를 적용하고 눈가림 판정 파일을 만든다. LLM 호출 없음."""
import json, random, re, sys
from pathlib import Path
sys.path.insert(0, ".")
from core.llm.answer_fix import _CITED, _find
from core.llm.conclusion_rewrite import _OVERGEN, cited_blocks, drop_bundled

EXP = Path("docs/experiments"); D = EXP / "conclusion_overgen_1025"
g = {}; exec((EXP / "conclusion_rewrite_1021/offline.py").read_text().split("qs = {}")[0], g)  # grounded · concl
qs = {l.split("\t")[0]: l.split("\t")[1].strip() for l in open(D / "questions.tsv")}
split = lambda t: [x.strip() for x in re.split(r"(?<=[.!?。])\s+|\n+", t) if x.strip()]
out = []; n_target = 0
for r in map(json.loads, open(EXP / "e2e_ko_1008/results/cov_new.jsonl")):
    a, ctx = r.get("answer") or "", r.get("numbered_context") or ""
    ids = dict(enumerate(r.get("doc_ids") or [], 1))
    if not a or not _find("결론", a) or len(cited_blocks(a, ctx, ids)) < 2:
        continue
    n_target += 1
    new, n = drop_bundled(a, bundled=False)
    if not n:
        continue
    sents = split(g["concl"](a))
    out.append({"id": r["id"], "question": qs[r["id"]], "n": n, "sents": sents,
                "drop": ["일반화" if _OVERGEN.search(s) else "" for s in sents],
                "grounded_before": g["grounded"](a, ctx, ids), "grounded_after": g["grounded"](new, ctx, ids),
                "after": g["concl"](new).strip(),
                "blocks": {str(k): b[:1000] for k, b in cited_blocks(a, ctx, ids).items()}, "doc_ids": {str(k): v for k, v in ids.items()}})
with open(D / "results.jsonl", "w") as w:
    w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
random.Random(10253).shuffle(out); key = {}
with open(D / "blind.md", "w") as w:
    for i, x in enumerate(out):
        key[f"Q{i:02d}"] = x["id"]
        w.write(f"######## Q{i:02d} | {x['question']}\n")
        for k, b in x["blocks"].items():
            w.write(f"--- [{x['doc_ids'].get(k, '?')}] {re.sub(chr(10), ' ', b)}\n")
        for j, s in enumerate(x["sents"]):
            w.write(f"Q{i:02d}.{j} {s}\n")
        w.write("\n")
json.dump(key, open(D / "blind_key.json", "w"))
print("답", n_target, "규칙 적용", len(out), "지운 문장", sum(x["n"] for x in out))
