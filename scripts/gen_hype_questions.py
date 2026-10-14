#!/usr/bin/env python3
"""hype_1014 — 논문마다 가상 질문 4개 (한국어 원문 · 영어 질문 · 영어 키워드) 생성.

  .venv/bin/python scripts/gen_hype_questions.py --base-url https://<pod>-8000.proxy.runpod.net/v1 --workers 16

- 논문 목록: Chroma SQLite(읽기 전용 ``immutable=1``)의 paper_id · title · abstract (논문당 1행).
- 출력: docs/experiments/hype_1014/questions.jsonl (이어 하기: 이미 있는 paper_id 는 건너뜀).
- 키워드 줄은 운영 ``agent_nodes._extract_english_rag_query`` 출력과 같은 형식(쉼표 구분 소문자 3~5개).
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "experiments" / "hype_1014" / "questions.jsonl"

PROMPT = """You index research papers for a Korean researcher's paper-search chatbot.

Paper title: {title}
Abstract: {abstract}

Write 4 different questions this researcher might type when this paper is the answer.
Vary them: (1) asks for the paper by its problem without naming the method, (2) asks how a technique works,
(3) asks about a specific result or comparison stated in the abstract, (4) a short casual request.
Do not copy the title verbatim. Use only facts in the abstract.

For each question give:
- "ko": the question in natural casual Korean (e.g. "~ 알려줘", "~ 있어?")
- "en": the same question in English
- "keywords": 3-5 core English search keywords for academic retrieval, one comma-separated lowercase line

Return ONLY JSON: {{"items": [{{"ko": "...", "en": "...", "keywords": "..."}}, ...4 items]}}"""


def load_papers(db: Path) -> list[dict]:
    con = sqlite3.connect(f"file:{db}?immutable=1", uri=True)
    rows = con.execute(
        """SELECT m.string_value AS pid,
                  MAX(CASE WHEN t.key='title' THEN t.string_value END),
                  MAX(CASE WHEN t.key='abstract' THEN t.string_value END)
           FROM embedding_metadata m JOIN embedding_metadata t ON t.id = m.id
           WHERE m.key='paper_id' AND t.key IN ('title','abstract')
           GROUP BY m.string_value"""
    ).fetchall()
    con.close()
    return [{"paper_id": p, "title": t or "", "abstract": a or ""} for p, t, a in rows if p]


def parse(raw: str) -> list[dict] | None:
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return None
    try:
        items = json.loads(m.group(0)).get("items") or []
    except json.JSONDecodeError:
        return None
    out = []
    for it in items[:4]:
        en, kw, ko = (it.get("en") or "").strip(), (it.get("keywords") or "").strip().lower(), (it.get("ko") or "").strip()
        kw = ", ".join(k.strip() for k in re.split(r"[,\n]+", re.sub(r"[^a-z0-9,\-\s]", " ", kw)) if k.strip())
        if en and kw:
            out.append({"ko": ko, "en": en, "keywords": kw})
    return out if len(out) >= 3 else None


def ask(base: str, paper: dict) -> list[dict] | None:
    body = {"model": "openai/gpt-oss-120b", "temperature": 0.7, "max_tokens": 2000, "reasoning_effort": "low",
            "messages": [{"role": "user", "content": PROMPT.format(title=paper["title"], abstract=paper["abstract"][:2500])}]}
    for _ in range(2):
        try:
            r = requests.post(base.rstrip("/") + "/chat/completions", json=body, timeout=300)
            got = parse(r.json()["choices"][0]["message"]["content"] or "")
            if got:
                return got
        except Exception as exc:  # noqa: BLE001
            print(f"  재시도 {paper['paper_id']}: {str(exc)[:80]}", flush=True)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--db", default="/Volumes/T7 Shield/mini-chroma-rebuild2/chroma.sqlite3")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    papers = load_papers(Path(a.db))
    done = set()
    if OUT.exists():
        done = {json.loads(l)["paper_id"] for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()}
    todo = [p for p in papers if p["paper_id"] not in done and p["abstract"]]
    if a.limit:
        todo = todo[: a.limit]
    print(f"논문 {len(papers)} · 완료 {len(done)} · 할 일 {len(todo)} (초록 없음 {sum(not p['abstract'] for p in papers)})", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lock, ok, fail = threading.Lock(), 0, []
    with OUT.open("a", encoding="utf-8") as w, ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(ask, a.base_url, p): p for p in todo}
        for n, f in enumerate(as_completed(futs), 1):
            p, items = futs[f], f.result()
            with lock:
                if items:
                    w.write(json.dumps({"paper_id": p["paper_id"], "items": items}, ensure_ascii=False) + "\n")
                    w.flush()
                    ok += 1
                else:
                    fail.append(p["paper_id"])
            if n % 200 == 0:
                print(f"  {n}/{len(todo)} · 성공 {ok} · 실패 {len(fail)}", flush=True)
    print(f"완료: 성공 {ok} · 실패 {len(fail)} {fail[:20]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
