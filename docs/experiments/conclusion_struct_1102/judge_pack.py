"""conclusion_struct_1102 §3 판정 묶음 — 바뀐 답마다 전 · 후 문장을 섞어 무작위 번호로, 인용 블록과 함께 적는다.

    .venv/bin/python docs/experiments/conclusion_struct_1102/judge_pack.py cs1_heldout

judge/packets_K.md(10답씩) · judge/p1.md(질문 + 결론 A/B)를 쓴다. 어느 쪽이 D 인지는 judge/key.json 에만 둔다 —
라벨(judge/labels.tsv · judge/p1_labels.tsv)을 다 쓴 뒤 score.py 가 연다.
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.llm.answer_fix import _CITED, _find  # noqa: E402
from core.llm.citation_fix import RAG_HIT_SEP  # noqa: E402
from core.llm.conclusion_rewrite import _bare  # noqa: E402

D = Path(__file__).resolve().parent
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"
QFILE = ROOT / "docs" / "experiments" / "foundation_1031" / "heldout.tsv"
_TITLE = re.compile(r"^\[(\d{4}\.\d{4,5})(?:v\d+)?\]", re.M)
_END = re.compile(r"\n\s*(?:<b>|📎)")


def conclusion(answer: str) -> str:
    c = _find("결론", answer)
    if not c:
        return ""
    rest = answer[c.end():]
    m = _END.search(rest)
    return (rest[:m.start()] if m else rest).strip()


def main() -> None:
    lab = sys.argv[1]
    J = D / (sys.argv[2] if len(sys.argv) > 2 else "judge")  # dev 시험은 다른 폴더로
    J.mkdir(exist_ok=True)
    if (J / "key.json").exists():
        sys.exit("judge/key.json 이 이미 있다 — 다시 섞지 않는다")
    q = dict(line.rstrip("\n").split("\t", 1) for line in QFILE.open(encoding="utf-8") if "\t" in line)
    rows = [r for r in map(json.loads, (RES / f"{lab}.jsonl").open(encoding="utf-8")) if r["changed"]]
    ctx = {}
    for src in {r["src"] for r in rows}:
        for r in map(json.loads, (RES / f"{src}.jsonl").open(encoding="utf-8")):
            ctx[r["id"]] = r["numbered_context"]
    rng = random.Random(1102)
    key, p1key, packets, p1 = {}, {}, [], ["# 보호 1 — 질문에 답하는 정도 (A · B · 같음)", "",
                                           "문서와 맞는 내용으로 질문에 더 답하는 쪽. 틀린 내용은 답한 것으로 치지 않는다.", ""]
    for r in sorted(rows, key=lambda x: x["id"]):
        sents = [("전", k, p["before"]) for k, p in enumerate(r["pairs"])]
        sents += [("후", k, a) for k, p in enumerate(r["pairs"]) for a in p["after"]]
        rng.shuffle(sents)
        key[r["id"]] = {f"s{n + 1}": [side, k] for n, (side, k, _) in enumerate(sents)}
        ids = {_bare(i) for _, _, s in sents for i in _CITED.findall(s)}
        blocks = list(dict.fromkeys(b.strip() for b in ctx[r["id"]].split(RAG_HIT_SEP)
                                    if (t := _TITLE.search(b)) and t.group(1) in ids))
        packets.append("\n".join([f"## {r['id']} — {q.get(r['id'], '')}", "", "### 인용 블록", "", *blocks, "", "### 문장", "",
                                  *[f"- s{n + 1}: {s}" for n, (_, _, s) in enumerate(sents)], ""]))
        pair = [("전", conclusion(r["before"])), ("후", conclusion(r["after"]))]
        rng.shuffle(pair)
        p1key[r["id"]] = "A" if pair[0][0] == "후" else "B"
        p1 += [f"## {r['id']} — {q.get(r['id'], '')}", "", f"A: {pair[0][1]}", "", f"B: {pair[1][1]}", ""]
    for k in range(0, len(packets), 10):
        head = ["# 주 지표 문장 판정 — 라벨 O · E · X · U · F · ? (README §3)", ""]
        (J / f"packets_{k // 10 + 1}.md").write_text("\n".join(head + packets[k:k + 10]) + "\n", encoding="utf-8")
    (J / "p1.md").write_text("\n".join(p1) + "\n", encoding="utf-8")
    (J / "key.json").write_text(json.dumps({"sentences": key, "p1_d_is": p1key}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"바뀐 답 {len(rows)} · 문장 {sum(len(v) for v in key.values())} · 묶음 {(len(packets) + 9) // 10}")


if __name__ == "__main__":
    main()
