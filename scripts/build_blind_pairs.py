#!/usr/bin/env python3
"""두 답변 모델을 같은 문항으로 짝지어, 모델 이름을 가린 판정 입력을 만든다 — answer_quality_1010 README §6.2.

  python3 scripts/build_blind_pairs.py ans_full ans_base

- 대상: 두 쪽 모두 direct_answer/B, context_papers 가 같고, 컨텍스트에 정답이 있는 문항.
- 출력: blind_input.jsonl (문항마다 답변 X·Y, 순서는 문항 ID 로 시드한 동전) + blind_key.json (X/Y → 모델).
  판정자는 key 를 보지 않는다.
"""
from __future__ import annotations

import glob
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"
EXP = ROOT / "docs" / "experiments" / "answer_quality_1010"


def load_corpus() -> dict[str, dict]:
    out: dict[str, dict] = {}
    files = sorted(glob.glob(str(ROOT / "raw_data_queue/processed/crawled_papers*.jsonl")))
    files.append(str(ROOT / "raw_data_queue/crawled_papers.jsonl"))
    for f in files:
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("paper_id"):
                out[re.sub(r"v\d+$", "", d["paper_id"])] = d
    return out


def main() -> int:
    a_label, b_label = sys.argv[1], sys.argv[2]
    a = {json.loads(l)["id"]: json.loads(l) for l in (RES / f"{a_label}.jsonl").read_text().splitlines()}
    b = {json.loads(l)["id"]: json.loads(l) for l in (RES / f"{b_label}.jsonl").read_text().splitlines()}
    qs = dict(l.split("\t", 1) for l in (ROOT / "docs/experiments/e2e_ko_1008/ko_questions.tsv").read_text().splitlines())
    gold = {json.loads(l)["id"]: json.loads(l)["relevant_papers"]
            for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    corpus = load_corpus()

    stats = {"total": len(a), "not_both_rag": 0, "context_differs": 0, "no_gold_in_context": 0, "empty_answer": 0}
    rows, key = [], {}
    for i in sorted(a):
        ra, rb = a[i], b.get(i)
        if not rb or ra["route"] != "direct_answer/B" or rb["route"] != "direct_answer/B":
            stats["not_both_rag"] += 1
            continue
        if ra["context_papers"] != rb["context_papers"]:
            stats["context_differs"] += 1
            continue
        if not ra["ok"]:
            stats["no_gold_in_context"] += 1
            continue
        if not (ra.get("answer") or "").strip() or not (rb.get("answer") or "").strip():
            stats["empty_answer"] += 1
            continue
        # 기준 논문: 두 답변 중 하나라도 인용한 정답 중 첫 번째, 없으면 목록 첫 번째 (judge_answers.py 와 같은 규칙, 양쪽 공통)
        cited = [g for g in gold[i] if g in set(ra.get("answer_papers") or []) | set(rb.get("answer_papers") or [])]
        pid = (cited or gold[i])[0]
        p = corpus.get(pid, {})
        flip = int(hashlib.sha256(i.encode()).hexdigest(), 16) % 2 == 1
        x, y = (rb, ra) if flip else (ra, rb)
        key[i] = {"X": b_label if flip else a_label, "Y": a_label if flip else b_label}
        rows.append({"id": i, "question": qs[i], "pid": pid, "title": p.get("title", ""),
                     "abstract": (p.get("abstract") or "")[:2000], "X": x["answer"], "Y": y["answer"]})

    tag = f"{a_label}_vs_{b_label}"
    (EXP / f"blind_input_{tag}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    (EXP / f"blind_key_{tag}.json").write_text(json.dumps(key, ensure_ascii=False, indent=1))
    stats["eligible"] = len(rows)
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
