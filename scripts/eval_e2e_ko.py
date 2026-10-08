#!/usr/bin/env python3
"""한국어 끝단 평가 — 질문 → 라우터 → 검색어 추출 → 검색 → LLM 에 넘어가는 컨텍스트.

설계·판정은 docs/experiments/e2e_ko_1008/README.md (측정 전에 고정).

  .venv/bin/python scripts/eval_e2e_ko.py --label prod

운영 노드(router_node · direct_answer_node)를 그대로 실행하고, 답변 생성 LLM 호출만
가로채 그 직전의 메시지에서 논문 ID 를 읽는다. 답변 품질은 재지 않는다 — 정답 논문이
LLM 에 건네진 컨텍스트 안에 있었는지만 본다.

출력: results/<label>.jsonl — 문항당 한 줄, scripts/eval_pairwise.py 형식 (ok = 컨텍스트에 정답).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "docs" / "experiments" / "e2e_ko_1008"
QUESTIONS = EXP / "ko_questions.tsv"
GOLD = ROOT / "docs" / "experiments" / "retrieval_eval_1007" / "eval_set.jsonl"
# 문항을 의도적으로 바꿨다면 README §2 와 이 값을 같이 갱신할 것
EXPECT_SHA = "7fc27b9d5bc9"
EXCLUDED = {"A026", "A057"}  # retrieval_eval_1007 §3.1 — 정답이 Chroma 에 없음

HANGUL_RE = re.compile(r"[가-힣]")


def load_items() -> list[dict]:
    raw = QUESTIONS.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()[:12]
    print(f"질문 집합 sha256={digest}")
    if digest != EXPECT_SHA:
        print(f"❌ sha256 불일치 (기대 {EXPECT_SHA}) — 측정 중단")
        sys.exit(1)
    gold = {json.loads(l)["id"]: json.loads(l) for l in GOLD.read_text(encoding="utf-8").splitlines() if l.strip()}
    items = []
    for line in raw.decode("utf-8").splitlines():
        if not line.strip():
            continue
        qid, q = line.split("\t", 1)
        if qid in EXCLUDED:
            continue
        items.append({"id": qid, "stratum": gold[qid]["stratum"], "question": q, "gold": gold[qid]["relevant_papers"]})
    return items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--ids", default="", help="쉼표 구분 — 일부 문항만 (파일럿용)")
    args = ap.parse_args()

    items = load_items()
    if args.ids:
        want = set(args.ids.split(","))
        items = [it for it in items if it["id"] in want]
    print(f"측정 {len(items)}문항")

    import core.graph.agent_nodes as N
    from core.session.agent_session import clear_session

    real_extract = N._extract_english_rag_query
    real_invoke = N._invoke_llm_with_fallback
    real_number = N.number_context_papers

    out_path = EXP / "results" / f"{args.label}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as w:
        for k, it in enumerate(items, 1):
            chat_id = f"e2e_eval_{args.label}_{it['id']}"
            clear_session(chat_id)
            queries: list[str] = []
            captured: list[str] = []
            doc_ids: list[str] = []

            def _number(ctx, *a, **kw):
                out_ctx, ids = real_number(ctx, *a, **kw)
                doc_ids[:] = [ids[k] for k in sorted(ids)]
                return out_ctx, ids

            def _extract(*a, **kw):
                q = real_extract(*a, **kw)
                queries.append(q)
                return q

            def _invoke(messages, *a, **kw):
                captured.append("\n".join(str(getattr(m, "content", m)) for m in messages))
                return "평가용 스텁 답변"

            N._extract_english_rag_query = _extract
            N.number_context_papers = _number
            cfg = {"configurable": {"chat_id": chat_id, "thread_id": chat_id, "bot": None}}
            state = {"user_request": it["question"], "route_type": "", "rag_context": ""}
            t0 = time.time()
            err = ""
            try:
                r = N.router_node(state, config=cfg)
                state.update(r or {})
                route = state.get("route_type", "")
                choice = state.get("router_choice", "")
                if route == "direct_answer" and choice == "B":
                    N._invoke_llm_with_fallback = _invoke
                    N.direct_answer_node(state, config=cfg)
            except Exception as exc:  # 평가는 계속한다
                err = f"{type(exc).__name__}: {exc}"[:300]
                route = state.get("route_type", "")
                choice = state.get("router_choice", "")
            finally:
                N._extract_english_rag_query = real_extract
                N._invoke_llm_with_fallback = real_invoke
                N.number_context_papers = real_number
                clear_session(chat_id)
            elapsed = time.time() - t0

            # LLM 에 건네진 [문서 N] 번호표의 논문 ID (청크 본문에 인용된 ID 는 세지 않는다)
            seen: list[str] = []
            for pid in doc_ids:
                npid = re.sub(r"v\d+$", "", (pid or "").strip())
                if npid and npid not in seen:
                    seen.append(npid)
            gold = {re.sub(r"v\d+$", "", g) for g in it["gold"]}
            hit = any(p in gold for p in seen)
            q_used = queries[-1] if queries else ""
            if route != "direct_answer" or choice != "B":
                fail = "route"
            elif not captured:
                fail = "no_context"
            elif q_used and HANGUL_RE.search(q_used):
                fail = "" if hit else "query_korean"
            else:
                fail = "" if hit else "retrieval"
            row = {
                "id": it["id"],
                "slot": it["stratum"],
                "model": args.label,
                "ok": hit,
                "fail": fail,
                "route": f"{route}/{choice}",
                "rag_queries": queries,
                "context_papers": seen,
                "elapsed": round(elapsed, 1),
                "error": err,
            }
            w.write(json.dumps(row, ensure_ascii=False) + "\n")
            w.flush()
            print(f"[{k}/{len(items)}] {it['id']} ok={hit} fail={fail or '-'} route={route}/{choice} {elapsed:.0f}s", flush=True)

    rows = [json.loads(l) for l in out_path.read_text(encoding="utf-8").splitlines()]
    from collections import Counter

    print("\n=== 요약 ===")
    for s in ["all", "A", "C1", "C2"]:
        xs = [r for r in rows if s == "all" or r["slot"] == s]
        if xs:
            print(f"{s:<4} n={len(xs):>3} 컨텍스트에 정답 {sum(r['ok'] for r in xs) / len(xs):.3f}")
    print("실패 원인:", dict(Counter(r["fail"] for r in rows if r["fail"])))
    print("경로:", dict(Counter(r["route"] for r in rows)))
    print(f"저장: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
