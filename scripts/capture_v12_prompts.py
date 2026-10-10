#!/usr/bin/env python3
"""v12 질문을 운영 그래프에 넣고, RAG 답변 LLM 호출 직전의 메시지를 그대로 저장한다 — yunsur_v12 README §2.

  .venv/bin/python scripts/capture_v12_prompts.py

답변 LLM 은 호출하지 않는다(스텁). 이어서 하기: 이미 저장한 src_pid 는 건너뛴다.
출력: finetune_datasets/v12/prompts.jsonl
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = Path(__file__).resolve().parent.parent
QIN = ROOT / "finetune_datasets" / "v12" / "questions.jsonl"
OUT = ROOT / "finetune_datasets" / "v12" / "prompts.jsonl"


def main() -> int:
    import core.graph.agent_nodes as N
    from core.session.agent_session import clear_session

    evalset = [json.loads(l) for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines() if l.strip()]
    eval_gold = {re.sub(r"v\d+$", "", g) for e in evalset for g in e["relevant_papers"]}
    qs = [json.loads(l) for l in QIN.read_text().splitlines() if l.strip()]
    qs = [q for q in qs if q["keep"]]
    done = set()
    if OUT.exists():
        done = {json.loads(l)["src_pid"] for l in OUT.read_text().splitlines() if l.strip()}

    real_invoke, real_number = N._invoke_llm_with_fallback, N.number_context_papers
    with OUT.open("a", encoding="utf-8") as w:
        for k, q in enumerate(qs, 1):
            if q["src_pid"] in done:
                continue
            cid = f"v12_cap_{q['src_pid']}"
            clear_session(cid)
            cap: list = []
            ids: list[str] = []

            def _number(ctx, *a, **kw):
                out, m = real_number(ctx, *a, **kw)
                ids[:] = [m[i] for i in sorted(m)]
                return out, m

            N._invoke_llm_with_fallback = lambda messages, *a, **kw: (cap.append(messages), "stub")[1]
            N.number_context_papers = _number
            cfg = {"configurable": {"chat_id": cid, "thread_id": cid, "bot": None}}
            st = {"user_request": q["question"], "route_type": "", "rag_context": ""}
            err = ""
            try:
                st.update(N.router_node(st, config=cfg) or {})
                route = f"{st.get('route_type', '')}/{st.get('router_choice', '')}"
                if route == "direct_answer/B":
                    N.direct_answer_node(st, config=cfg)
            except Exception as exc:  # 계속 진행
                err = f"{type(exc).__name__}: {exc}"[:300]
                route = f"{st.get('route_type', '')}/{st.get('router_choice', '')}"
            finally:
                N._invoke_llm_with_fallback, N.number_context_papers = real_invoke, real_number
                clear_session(cid)
            ctx = [re.sub(r"v\d+$", "", p or "") for p in ids]
            row = {**q, "route": route, "context_pids": ctx, "error": err,
                   "gold_in_context": q["src_pid"] in ctx,
                   "eval_leak": bool(set(ctx) & eval_gold)}
            if cap:
                m = cap[-1]
                row["system"] = str(getattr(m[0], "content", ""))
                row["user"] = str(getattr(m[-1], "content", ""))
                row["n_messages"] = len(m)
            w.write(json.dumps(row, ensure_ascii=False) + "\n")
            w.flush()
            print(f"[{k}/{len(qs)}] {route} gold={row['gold_in_context']} leak={row['eval_leak']} {q['question'][:50]}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
