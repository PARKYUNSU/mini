#!/usr/bin/env python3
"""논문 모드가 잡담·계획 요청을 RAG 로 끌어들이는지 — 라우터만 잰다.

설계·판정은 docs/experiments/e2e_ko_1008/README.md §8 (측정 전에 고정).

  .venv/bin/python scripts/eval_route_contamination.py --label off_a
  .venv/bin/python scripts/eval_route_contamination.py --label on --paper-mode

문항: tests/fixtures/local_llm_failure_eval.jsonl 의 chat 48 · planner 64.
출력: results/route_<label>.jsonl — 문항당 한 줄 (id·slot·route·rag=direct_answer/B 여부).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "local_llm_failure_eval.jsonl"
OUT = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"
SLOTS = ("chat", "planner")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--paper-mode", action="store_true")
    args = ap.parse_args()

    items = [json.loads(l) for l in FIXTURE.read_text(encoding="utf-8").splitlines() if l.strip()]
    items = [it for it in items if it["slot"] in SLOTS]
    print(f"문항 {len(items)} · paper_mode={args.paper_mode}")

    import core.graph.agent_nodes as N
    from core.session.agent_session import clear_session, set_paper_mode

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"route_{args.label}.jsonl"
    with path.open("w", encoding="utf-8") as w:
        for k, it in enumerate(items, 1):
            chat_id = f"route_eval_{args.label}_{it['id']}"
            clear_session(chat_id)
            set_paper_mode(chat_id, args.paper_mode)
            cfg = {"configurable": {"chat_id": chat_id, "thread_id": chat_id, "bot": None}}
            t0 = time.time()
            err = ""
            try:
                r = N.router_node({"user_request": it["text"], "route_type": "", "rag_context": ""}, config=cfg) or {}
            except Exception as exc:
                r, err = {}, f"{type(exc).__name__}: {exc}"[:300]
            finally:
                clear_session(chat_id)
            route = f"{r.get('route_type', '')}/{r.get('router_choice', '')}"
            row = {"id": it["id"], "slot": it["slot"], "model": args.label, "route": route,
                   "rag": route == "direct_answer/B", "elapsed": round(time.time() - t0, 1), "error": err}
            w.write(json.dumps(row, ensure_ascii=False) + "\n")
            w.flush()
            print(f"[{k}/{len(items)}] {it['id']} {route} {row['elapsed']}s", flush=True)

    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]
    print("\n=== 요약 ===")
    for s in SLOTS:
        xs = [r for r in rows if r["slot"] == s]
        print(f"{s:<8} n={len(xs)} RAG(B)={sum(r['rag'] for r in xs)} 경로={dict(Counter(r['route'] for r in xs))}")
    print(f"저장: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
