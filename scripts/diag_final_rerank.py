#!/usr/bin/env python3
"""hype_1014 §6 진단 — 정답이 후보 풀에 있는데 최종 3편에서 빠지는 단계 찾기.

  CHROMA_SERVER_URL=http://127.0.0.1:8001 .venv/bin/python scripts/diag_final_rerank.py A023 A042 C1_06 A012 A039

저장된 운영 검색어(`hype0_162.jsonl` 의 rag_queries)로 ChromaRAGTool.search 를 다시 돌리며,
논문 단위 light rerank 직전·직후 순위와 최종 선택에서 정답 논문 위치를 찍는다(LLM 호출 없음).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def norm(p: str) -> str:
    return re.sub(r"v\d+$", "", p or "")


def main() -> int:
    import core.rag.agent_chroma_rag as m

    rows = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "docs/experiments/e2e_ko_1008/results/hype0_162.jsonl").read_text(encoding="utf-8").splitlines()}
    gold = {json.loads(l)["id"]: {norm(p) for p in json.loads(l)["relevant_papers"]} for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    cap: dict = {}
    orig = m._light_rerank_paper_pool_by_embedding

    def wrapped(q, paper_best, docs, metas, pk, **kw):
        cap["before"] = [(round(sc, 4), norm(pid)) for sc, _, pid in paper_best[:60]]
        out = orig(q, paper_best, docs, metas, pk, **kw)
        cap["after"] = [(round(sc, 4), norm(pid)) for sc, _, pid in out[:60]]
        return out

    m._light_rerank_paper_pool_by_embedding = wrapped
    tool = m.get_chroma_rag_tool() if hasattr(m, "get_chroma_rag_tool") else m.ChromaRAGTool()
    for qid in sys.argv[1:]:
        r = rows[qid]
        q = (r.get("rag_queries") or [""])[0] if isinstance(r.get("rag_queries"), list) else (r.get("rag_queries") or "")
        cap.clear()
        tool.search(q, top_k=3)
        g = gold[qid]

        def pos(lst):
            for k, (sc, pid) in enumerate(lst, 1):
                if pid in g:
                    return k, sc
            return None, None

        bp, bs = pos(cap.get("before", []))
        ap, as_ = pos(cap.get("after", []))
        top_after = cap.get("after", [])[:4]
        print(f"== {qid} q={q!r}")
        print(f"   light rerank 전 정답 순위 {bp} (점수 {bs}) → 후 {ap} (점수 {as_}) · 전 1위 {cap.get('before', [None])[:1]} · 후 상위 {top_after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
