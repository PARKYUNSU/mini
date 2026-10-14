#!/usr/bin/env python3
"""presence_judge_v2_1014 — 판정 프롬프트 v1 vs v2 오프라인 비교 (저장된 컨텍스트 재사용).

  .venv/bin/python scripts/presence_judge_v2_eval.py

- 162 찾기형: ans_v13_db2.jsonl (정답 있음 → 정답 문서 번호를 골라야 정답, 정답 없음 → `없음` 이 정답)
- 실제 사용형: real_v13.jsonl 의 N·C·T 중 정답이 컨텍스트에 있는 문항 (`없음` 이면 거짓 없음)
- 판정: 운영과 같은 yunsur_v13, temperature 0, seed 0, reasoning off.
"""
from __future__ import annotations

import json
import re
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"
OUT = ROOT / "docs" / "experiments" / "presence_judge_v2_1014"


def norm(p: str) -> str:
    return re.sub(r"v\d+$", "", p or "")


def mc(b: int, c: int) -> float:
    n = b + c
    return 1.0 if n == 0 else min(1.0, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n)


def items() -> list[dict]:
    gold162 = {json.loads(l)["id"]: json.loads(l)["relevant_papers"] for l in
               (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    q162 = dict(l.split("\t", 1) for l in (ROOT / "docs/experiments/e2e_ko_1008/ko_questions.tsv").read_text(encoding="utf-8").splitlines() if l.strip())
    spec = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "docs/experiments/real_eval_1013/spec.jsonl").read_text().splitlines()}
    qr = dict(l.split("\t", 1) for l in (ROOT / "docs/experiments/real_eval_1013/questions.tsv").read_text(encoding="utf-8").splitlines() if l.strip())
    out = []
    for set_name, path, gold_of, q_of in [
        ("162", RES / "ans_v13_db2.jsonl", lambda i: gold162.get(i, []), q162),
        ("real", RES / "real_v13.jsonl", lambda i: spec[i].get("papers") or [] if spec[i]["type"] != "R" else None, qr),
    ]:
        for l in path.read_text(encoding="utf-8").splitlines():
            r = json.loads(l)
            g = gold_of(r["id"])
            if g is None or not r.get("numbered_context") or not r.get("doc_ids"):
                continue
            gold = {norm(p) for p in g}
            ok_nums = [k + 1 for k, d in enumerate(r["doc_ids"]) if norm(d) in gold]
            if set_name == "real" and not ok_nums:
                continue  # 실제 사용형은 정답이 컨텍스트에 있는 문항만
            out.append({"set": set_name, "id": r["id"], "q": q_of[r["id"]].strip(), "ctx": r["numbered_context"],
                        "ok_nums": ok_nums})
    return out


def main() -> int:
    from core.llm import presence_judge as pj
    from core.llm.presence_judge import PROMPT, PROMPT_V2, parse_pick
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    llm = ChatOllama(**ollama_kwargs(model="yunsur_v13", temperature=0.0, seed=0, reasoning=False, num_predict=64))
    its = items()
    OUT.mkdir(parents=True, exist_ok=True)
    res = []
    for n, it in enumerate(its, 1):
        row = dict(it)
        row.pop("ctx")
        for tag, pr in (("v1", PROMPT), ("v2", PROMPT_V2)):
            raw = str(llm.invoke(pr.format(question=it["q"], context=it["ctx"])).content or "")
            row[tag] = parse_pick(raw)
        res.append(row)
        if n % 25 == 0:
            print(f"  {n}/{len(its)}", flush=True)
    (OUT / "judged.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res), encoding="utf-8")

    def correct(r, tag):
        v = r[tag]
        return v == "없음" if not r["ok_nums"] else (v in r["ok_nums"])

    def false_none(r, tag):
        return bool(r["ok_nums"]) and r[tag] == "없음"

    for name, sel in [("162 정답 있음", lambda r: r["set"] == "162" and r["ok_nums"]),
                      ("162 정답 없음", lambda r: r["set"] == "162" and not r["ok_nums"]),
                      ("real 정답 있음", lambda r: r["set"] == "real")]:
        rs = [r for r in res if sel(r)]
        if "없음" in name and "정답 없음" in name:
            a = [r["v1"] == "없음" for r in rs]; b = [r["v2"] == "없음" for r in rs]
            lab = "'없음' 재현"
        else:
            a = [false_none(r, "v1") for r in rs]; b = [false_none(r, "v2") for r in rs]
            lab = "거짓 '없음'"
        x = sum(p and not q for p, q in zip(a, b)); y = sum(q and not p for p, q in zip(a, b))
        print(f"{name} n={len(rs)} · {lab} v1 {sum(a)} · v2 {sum(b)} · 짝 v1만 {x} v2만 {y} p={mc(x, y):.4f}"
              f" · 정답 번호 v1 {sum(correct(r, 'v1') for r in rs)} v2 {sum(correct(r, 'v2') for r in rs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
