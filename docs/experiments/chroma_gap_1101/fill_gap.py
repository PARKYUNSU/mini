"""빠진 논문(gap_before.jsonl)을 운영 Chroma 에 채운다 — 사용자 승인 뒤에만 실행.

적재는 기존 경로 그대로: ``RagProcessor.add_paper`` 를 ``chroma_write_lock()`` 안에서 부른다
(hf_daily · ingest_classics 와 같은 호출 — 청킹 · 품질 필터 · 임베딩 · 결정적 청크 ID · upsert).
본문은 JSONL 레코드(bm25_index 처럼 첫 줄)의 ``content`` — 예전 JSONL 재적재 스크립트
(scripts/legacy/rebuild_chroma_from_jsonl.py)와 같은 필드. 이미 Chroma 에 있는 논문은 건너뛴다.

    .venv/bin/python docs/experiments/chroma_gap_1101/fill_gap.py [PID ...]   # 인자 없으면 66편 전부
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
D = Path(__file__).resolve().parent

from core.config.agent_config import CHROMA_DB_DIR  # noqa: E402
from core.config.chroma_lock import chroma_write_lock  # noqa: E402
from core.rag.agent_chroma_rag import _paper_id_version_candidates  # noqa: E402
from pipelines.ingest.rag_processor import RagProcessor  # noqa: E402


def record_at(where: str) -> dict:
    path, ln = where.rsplit(":", 1)
    with (ROOT / path).open(encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if i == int(ln):
                return json.loads(line)
    raise ValueError(where)


def main() -> int:
    rows = [json.loads(x) for x in (D / "gap_before.jsonl").open(encoding="utf-8")]
    if sys.argv[1:]:
        rows = [r for r in rows if r["paper_id"] in set(sys.argv[1:])]
    rag = RagProcessor(db_path=str(CHROMA_DB_DIR))
    col = rag._collection
    total = 0
    with (D / "fill_result.jsonl").open("a", encoding="utf-8") as out:
        for k, r in enumerate(rows, 1):
            pid = r["paper_id"]
            if col.get(where={"paper_id": {"$in": _paper_id_version_candidates(pid)}}, limit=1, include=[])["ids"]:
                print(f"[{k}/{len(rows)}] {pid} 이미 있음 — 건너뜀", flush=True)
                continue
            rec = record_at(r["where"][0])
            t = time.time()
            try:
                with chroma_write_lock():
                    n = rag.add_paper(markdown_content=rec.get("content") or "", title=rec.get("title") or "",
                                      published=rec.get("published") or "", pdf_url=rec.get("pdf_url") or "",
                                      paper_id=rec["paper_id"], abstract=rec.get("abstract") or "")
                err = None
            except Exception as e:  # 한 편 실패가 나머지를 막지 않게 — 기록하고 다음
                n, err = 0, f"{type(e).__name__}: {str(e)[:200]}"
            total += n
            print(f"[{k}/{len(rows)}] {rec['paper_id']} {n}청크 {time.time() - t:.1f}s" + (f" ❌ {err}" if err else ""),
                  flush=True)
            out.write(json.dumps({"paper_id": pid, "raw_id": rec["paper_id"], "chunks": n, "error": err,
                                  "at": time.strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False) + "\n")
    print(f"끝: {len(rows)}편 · 청크 {total:,}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
