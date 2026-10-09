#!/usr/bin/env python3
"""라우터가 문항을 어디로 왜 보내는지 — 1단계 하드룰 결과와 도구 이름까지 찍는다.

  .venv/bin/python scripts/diag_route_reasons.py e2e:A010,C2_02 fixture:chat_07
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    texts: dict[str, str] = {}
    for line in (ROOT / "docs/experiments/e2e_ko_1008/ko_questions.tsv").read_text(encoding="utf-8").splitlines():
        i, q = line.split("\t", 1)
        texts[i] = q
    for line in (ROOT / "tests/fixtures/local_llm_failure_eval.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        texts[r["id"]] = r["text"]

    import core.graph.agent_nodes as N
    from core.graph import agent_router_rules as RR
    from core.session.agent_session import clear_session

    ids = [x for arg in sys.argv[1:] for x in arg.split(":", 1)[-1].split(",") if x]
    for qid in ids:
        q = texts[qid]
        chat_id = f"route_diag_{qid}"
        clear_session(chat_id)
        req_lower = q.lower()
        facts = {
            "factual_lookup": RR.is_factual_lookup(q),
            "search_intent": RR.get_search_intent(q, req_lower),
            "whitelisted": RR.match_whitelisted_tool(q, req_lower, N.AGENT_TOOLS_DIR, is_scheduled=False)
            if hasattr(N, "AGENT_TOOLS_DIR") else "?",
        }
        r = N.router_node({"user_request": q, "route_type": "", "rag_context": ""},
                          config={"configurable": {"chat_id": chat_id, "thread_id": chat_id, "bot": None}}) or {}
        clear_session(chat_id)
        print(json.dumps({"id": qid, "route": f"{r.get('route_type')}/{r.get('router_choice')}",
                          "tool": r.get("used_tool_name", ""), **facts, "q": q[:50]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
