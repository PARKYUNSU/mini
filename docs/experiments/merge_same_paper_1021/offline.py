"""merge_same_paper_1021 §3 오프라인 평가 (맥미니): 기존 답에 합치기를 적용해 전후 비교."""
import collections, json, re, sys
from pathlib import Path
sys.path.insert(0, ".")
from core.llm.answer_fix import merge_same_paper_items, renumber_body_items, _CITED
from core.graph.agent_nodes import body_item_ids
from scripts.score_real_eval import score
EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"
SETS = {"s18_real40": "real_eval_1013", "s18_real2": "real_eval2_1015", "mt1": None}
_NUM = re.compile(r"\d+(?:\.\d+)?%?")


def nums(a):  # 항목 번호 · 머리 제목(<b>…</b>) 속 숫자는 뺀다
    a = re.sub(r"(?m)^[ \t]*\d{1,2}\.\s", "", re.sub(r"<b>[^<]*</b>|\*\*[^*]*\*\*", "", a))
    return collections.Counter(_NUM.findall(_CITED.sub("", a)))


def dup(a):
    c = collections.Counter(i for i, it in zip(body_item_ids(a), re.split(r"\n\s*\d+\.\s", "\n" + a.split("본론", 1)[-1].split("결론", 1)[0])[1:])
                            if i and len(set(_CITED.findall(it))) == 1)
    return any(v > 1 for v in c.values())


samples = []
for lbl, d in SETS.items():
    rows = [json.loads(l) for l in open(R / f"{lbl}.jsonl")]
    bad_ids = bad_nums = merged = before = after = 0; by = collections.Counter()
    out = []
    for r in rows:
        a = r.get("answer") or ""
        m, ch = merge_same_paper_items(a)
        m, _ = renumber_body_items(m) if ch else (m, False)
        before += dup(a); after += dup(m)
        if ch:
            merged += 1; by[r["id"].split("_")[-1][0]] += 1; samples.append((lbl, r["id"], m))
        bad_ids += set(_CITED.findall(a)) != set(_CITED.findall(m))
        bad_nums += nums(a) != nums(m)
        out.append({**r, "answer": m})
    print(f"{lbl}: 주 중복 답 {before} → {after} · 합친 답 {merged} {dict(by)} · 인용 집합 바뀜 {bad_ids} · 숫자 바뀜 {bad_nums}")
    if d:
        with open(R / f"{lbl}_merged.jsonl", "w") as w:
            w.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
        s0, s1 = score(lbl, EXP / d), score(f"{lbl}_merged", EXP / d)
        f = lambda s: (sum(x["ok"] for x in s["N"]), sum(x["both_cited"] for x in s["C"]), sum(x["gold_cited"] >= 3 for x in s["T"]))
        print(f"   N 정답 · C 두 편 · T≥3: 전 {f(s0)} → 후 {f(s1)}")
with open("docs/experiments/merge_same_paper_1021/samples.md", "w") as w:
    for lbl, i, m in samples[:10]:
        w.write(f"## {lbl} {i}\n\n{m.split('<b>결론</b>')[0].split('본론', 1)[-1].strip()}\n\n")
