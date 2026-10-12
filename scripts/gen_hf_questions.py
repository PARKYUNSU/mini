#!/usr/bin/env python3
"""hf_june40 질문 세트 — docs/experiments/hf_coverage_1012 §3.

  .venv/bin/python scripts/gen_hf_questions.py

2026-06 HF Daily Papers 일별 상위 10편 중 **현재 코퍼스에 없는** 논문에서 시드 0 으로 40편을 골라,
arXiv 제목·초록으로 한국어 질문 1개씩 만든다(v12 질문 생성 프롬프트, qwen3.5:9b).
출력: docs/experiments/hf_coverage_1012/questions.tsv, gold.jsonl (eval_e2e_ko.py --questions/--gold 형식)
"""
from __future__ import annotations

import json
import random
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
EXP = ROOT / "docs" / "experiments" / "hf_coverage_1012"


def main() -> int:
    from langchain_core.messages import HumanMessage
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs
    from pipelines.ingest.hf_daily import _components, fetch_metadata, hf_daily_ids, known_paper_ids
    from scripts.gen_v12_questions import PAPER_PROMPT

    have = known_paper_ids()
    pool: list[str] = []
    for d in range(1, 31):
        for pid in hf_daily_ids(f"2026-06-{d:02d}", 10):
            if pid not in have and pid not in pool:
                pool.append(pid)
        time.sleep(1)
    pool.sort()
    pick = random.Random(0).sample(pool, 40)
    print(f"후보 {len(pool)} → 40편", flush=True)

    fetcher = _components()[0]
    metas = fetch_metadata(fetcher, pick)
    llm = ChatOllama(**ollama_kwargs(temperature=0.7, top_p=0.9, reasoning=False, num_predict=160, model="qwen3.5:9b"))
    EXP.mkdir(parents=True, exist_ok=True)
    qs, golds = [], []
    for k, m in enumerate(metas, 1):
        base = m.paper_id.split("v")[0]
        q = ""
        for _ in range(3):
            raw = str(llm.invoke([HumanMessage(content=PAPER_PROMPT.format(title=m.title, abstract=m.abstract[:1500]))]).content)
            q = raw.strip().splitlines()[-1].strip().strip('"“”\'') if raw.strip() else ""
            if len(q) >= 10 and re.search(r"[가-힣]", q) and not re.search(r"\d{4}\.\d{4,5}", q):
                break
            q = ""
        if not q:
            print(f"  생성 실패 {base}", flush=True)
            continue
        qid = f"H{k:03d}"
        qs.append(f"{qid}\t{q}")
        golds.append({"id": qid, "stratum": "H", "relevant_papers": [base], "title": m.title})
        print(f"[{k}/{len(metas)}] {qid} {base} {q[:70]}", flush=True)
    (EXP / "questions.tsv").write_text("\n".join(qs) + "\n", encoding="utf-8")
    (EXP / "gold.jsonl").write_text("".join(json.dumps(g, ensure_ascii=False) + "\n" for g in golds), encoding="utf-8")
    print(f"저장: 질문 {len(qs)}개", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
