"""conclusion_misattr_1025 개발 세트 (맥미니): 결론 문장의 이름이 인용한 블록에 없고 다른 블록에만 있는 경우를 센다."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, ".")
from core.llm.answer_fix import _CITED, _find
from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.conclusion_rewrite import cited_blocks

R = Path("docs/experiments/e2e_ko_1008/results")
NAME = re.compile(r"(?<![A-Za-z0-9])[A-Za-z][A-Za-z0-9]*(?:[-‑][A-Za-z0-9]+)*(?![A-Za-z0-9])")
GENERIC = set("LLM LLMs RAG VLM VLMs MLLM LVLM AI NLP KV MoE GPU CPU SQL API QA RL KG KGs CoT SFT DPO PPO RLHF IR OCR ViT GNN SOTA AUROC".split())
norm = lambda t: t.replace("‑", "-").lower()


def is_name(t):
    return t not in GENERIC and len(t) >= 3 and (sum(c.isupper() for c in t) >= 2 or (any(c.isdigit() for c in t) and any(c.isalpha() for c in t)))


_LEAD = re.compile(r"^\s*((?:\[\s*\d{4}\.\d{4,5}(?:v\d+)?\s*\]\s*)+)(?![은는이가의와과에도를을])")
_TITLE = re.compile(r"\[\d{4}\.\d{4,5}v\d+\]\s*(.*?)\s*\[초록\]", re.S)


def sentences(text):
    """문장으로 나누되, 문장 앞에 붙은 인용([id]…)은 앞 문장 것으로 돌린다."""
    out = []
    for x in re.split(r"(?<=[.!?。])\s+|\n+", text):
        m = _LEAD.match(x)
        if m and out:
            out[-1] += " " + m.group(1).strip(); x = x[m.end():]
        if x.strip():
            out.append(x.strip())
    return out


def titles_by_id(ctx, ids):
    out = {}
    for blk in ctx.split(RAG_HIT_SEP):
        m = re.match(r"\s*\[\s*문서\s*(\d+)\s*\]", blk); t = _TITLE.search(blk)
        if m and t and int(m.group(1)) in ids:
            out[re.sub(r"v\d+$", "", ids[int(m.group(1))])] = norm(t.group(1))
    return out


def blocks_by_id(ctx, ids):
    out = {}
    for blk in ctx.split(RAG_HIT_SEP):
        m = re.match(r"\s*\[\s*문서\s*(\d+)\s*\]", blk)
        if m and int(m.group(1)) in ids:
            k = re.sub(r"v\d+$", "", ids[int(m.group(1))])
            out[k] = out.get(k, "") + "\n" + norm(blk)
    return out


def hits(answer, ctx, ids):
    c = _find("결론", answer)
    if not c:
        return []
    by = blocks_by_id(ctx, ids); ti = titles_by_id(ctx, ids); res = []
    for s in sentences(answer[c.end():]):
        refs = set(_CITED.findall(s))
        if not refs or s.lstrip().startswith(("•", "📎")):
            continue
        own = "\n".join(by.get(r, "") for r in refs)
        other = "\n".join(v for k, v in ti.items() if k not in refs)
        for t in set(NAME.findall(_CITED.sub(" ", s))):
            if is_name(t) and norm(t) not in own and norm(t) in other:
                res.append((s.strip(), t))
    return res


if __name__ == "__main__":
    n = 0; out = []
    for lbl in sys.argv[1:]:
        for r in map(json.loads, open(R / f"{lbl}.jsonl")):
            a, ctx = r.get("answer") or "", r.get("numbered_context") or ""
            ids = dict(enumerate(r.get("doc_ids") or [], 1))
            if not a or len(cited_blocks(a, ctx, ids)) < 2:
                continue
            n += 1
            for s, t in hits(a, ctx, ids):
                out.append((lbl, r["id"], t, s[:160]))
    for x in out:
        print(*x, sep=" | ")
    print("대상", n, "걸린 문장", len(out), "걸린 답", len({(a, b) for a, b, *_ in out}))
