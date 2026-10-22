"""cite_cleanup_1022 §3 오프라인 평가 (맥미니): 저장된 답에 clean_internal_refs 를 적용해 전후 비교."""
import collections, json, re, sys
from pathlib import Path
sys.path.insert(0, ".")
from core.llm.answer_fix import _DOC_BARE, _DOC_PAREN, _DUP_CITE, clean_internal_refs
from scripts.score_real_eval import score

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "cite_cleanup_1022"
SETS = {"at1_real40": "real_eval_1013", "at1_real2": "real_eval2_1015", "s18_real40": "real_eval_1013", "s18_real2": "real_eval2_1015", "fr1": None}
_ID = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]")


def nums(a):
    return collections.Counter(re.findall(r"\d+(?:\.\d+)?%?", _DOC_PAREN.sub("", re.sub(r"\[[^\]]*\]|문서\s*\d+", "", a))))


samples = []
for lbl, d in SETS.items():
    rows = [json.loads(l) for l in open(R / f"{lbl}.jsonl")]
    st = collections.Counter(); out = []
    for r in rows:
        a = r.get("answer") or ""; ids = dict(enumerate(r.get("doc_ids") or [], 1))
        b, ch = clean_internal_refs(a, ids)
        for k, rx in (("중복", _DUP_CITE), ("괄호", _DOC_PAREN)):
            st[k + "_전"] += bool(rx.search(a)); st[k + "_후"] += bool(rx.search(b))
        st["맨번호_전"] += bool(_DOC_BARE.search(_DOC_PAREN.sub("", a))); st["맨번호_후"] += bool(_DOC_BARE.search(b))
        st["바뀜"] += ch
        st["ID집합_바뀜"] += set(_ID.findall(a)) != set(_ID.findall(b))
        st["숫자_바뀜"] += nums(a) != nums(b)
        if ch: samples.append((lbl, r["id"], a, b))
        out.append({**r, "answer": b})
    print(lbl, dict(st))
    if d:
        with open(R / f"{lbl}_cc.jsonl", "w") as w:
            w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
        f = lambda s: (sum(x["ok"] for x in s["N"]), sum(x["both_cited"] for x in s["C"]), sum(x["gold_cited"] >= 3 for x in s["T"]))
        print(f"   N · C · T≥3: {f(score(lbl, EXP / d))} → {f(score(f'{lbl}_cc', EXP / d))}")
import difflib
with open(D / "samples.md", "w") as w:
    for lbl, i, a, b in samples[:12]:
        diff = [l for l in difflib.ndiff(a.split("\n"), b.split("\n")) if l[:1] in "-+"]
        w.write(f"## {lbl} {i}\n\n" + "\n".join(diff) + "\n\n")
print("바뀐 답", len(samples))
