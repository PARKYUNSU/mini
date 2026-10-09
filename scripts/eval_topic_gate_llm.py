#!/usr/bin/env python3
"""학술 주제 게이트 2단계(LLM) 평가 — topic_gate_1009/items.jsonl 의 dev 또는 test.

  .venv/bin/python scripts/eval_topic_gate_llm.py dev
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITEMS = Path(__file__).resolve().parent.parent / "docs/experiments/topic_gate_1009/items.jsonl"


def main() -> int:
    split = sys.argv[1]
    from core.rag.topic_gate import is_academic_query, is_academic_query_llm

    rows = [json.loads(l) for l in ITEMS.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = [r for r in rows if r["split"] == split]
    out = []
    for r in rows:
        lex = is_academic_query(r["text"])
        llm = is_academic_query_llm(r["text"]) if not lex else None
        out.append({**r, "lex": lex, "llm": llm, "full": lex or bool(llm)})
    pos = [r for r in out if r["label"] == 1]
    cp = [r for r in out if r["source"] in ("fixture_chat", "fixture_planner")]
    cod = [r for r in out if r["source"] == "fixture_coding"]
    for name, key in (("어휘만", "lex"), ("어휘+LLM", "full")):
        tpr = sum(bool(r[key]) for r in pos) / len(pos)
        print(f"{split} {name}: TPR {tpr:.3f} ({sum(bool(r[key]) for r in pos)}/{len(pos)}) · "
              f"오탐 chat+planner {sum(bool(r[key]) for r in cp)}/{len(cp)} · coding {sum(bool(r[key]) for r in cod)}/{len(cod)}")
    for r in out:
        if r["label"] == 1 and not r["full"]:
            print("  미탐", r["id"], r["text"][:60])
        if r["label"] == 0 and r["full"]:
            print("  오탐", r["id"], r["text"][:60])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
