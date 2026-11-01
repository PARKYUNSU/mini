"""빠진 논문(gap_before.jsonl)의 원인 나누기 — 읽기만 한다.

- 옛 Chroma 두 벌(10-13 사고 전 원본 백업 · 10-13 재구축본)을 읽기 전용(``immutable=1``)으로 열어 논문별 청크 수를 센다.
  → 재구축 때 잃었는지, 처음부터 없었는지.
- 수집 로그(logs/ · .cron/ · 스케줄러 로그)에서 그 논문 ID 가 나온 줄을 모은다.
- 본문을 운영과 같은 청킹(``RagProcessor.chunk_markdown`` + 품질 필터)에 넣어 청크가 몇 개 나오는지 센다(임베딩 없음).

    .venv/bin/python docs/experiments/chroma_gap_1101/classify.py
"""
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
D = Path(__file__).resolve().parent

from core.config.agent_config import COLLECTION_NAME  # noqa: E402
from core.rag.agent_chroma_rag import _paper_id_version_candidates  # noqa: E402

OLD_DBS = {
    "old_1013": "/Volumes/T7 Shield/backup/mini-chroma-old-20261013/chroma.sqlite3",
    "rebuild1": "/Volumes/T7 Shield/mini-chroma-rebuild/chroma.sqlite3",
}
LOGS = sorted(ROOT.glob("logs/*.log")) + sorted(ROOT.glob(".cron/*.log")) + [
    Path.home() / "Library/Logs/mini-runscheduler.log"]


def chunk_counts(db: str, pids: list[str]) -> dict[str, int]:
    con = sqlite3.connect(f"file:{db}?immutable=1", uri=True)
    seg, = con.execute(
        "SELECT s.id FROM segments s JOIN collections c ON s.collection = c.id WHERE c.name = ? AND s.scope = 'METADATA'",
        (COLLECTION_NAME,),
    ).fetchone()
    out = {}
    for pid in pids:
        cands = _paper_id_version_candidates(pid)
        n, = con.execute(
            f"SELECT count(*) FROM embedding_metadata m JOIN embeddings e ON e.id = m.id "
            f"WHERE m.key = 'paper_id' AND m.string_value IN ({','.join('?' * len(cands))}) AND e.segment_id = ?",
            (*cands, seg),
        ).fetchone()
        out[pid] = n
    con.close()
    return out


def log_hits(pids: list[str]) -> dict[str, list[str]]:
    pat = D / "_pids.txt"
    pat.write_text("\n".join(pids) + "\n")
    r = subprocess.run(["grep", "-n", "-F", "-f", str(pat), *map(str, LOGS)], capture_output=True, text=True)
    pat.unlink()
    out: dict[str, list[str]] = {p: [] for p in pids}
    for line in r.stdout.splitlines():
        for p in pids:
            if re.search(rf"(?<![\d.]){re.escape(p)}(v\d+)?(?!\d)", line):
                out[p].append(line.replace(str(ROOT) + "/", "")[:240])
    return out


def chunkable(rows: list[dict]) -> dict[str, int]:
    """운영 청킹 + 품질 필터를 통과하는 청크 수 (임베딩 없이)."""
    import tempfile

    from pipelines.ingest.chunking_strategy_proposal import passes_chunk_quality_filter
    from pipelines.ingest.rag_processor import RagProcessor

    rp = RagProcessor(db_path=tempfile.mkdtemp())  # 빈 임시 폴더 — 운영 DB 아님, 청킹만 쓴다
    want = {r["paper_id"] for r in rows}
    out = {}
    for f in [*sorted((ROOT / "raw_data_queue/processed").glob("crawled_papers*.jsonl")),
              ROOT / "raw_data_queue/crawled_papers.jsonl"]:
        for line in f.open(encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            pid = re.sub(r"v\d+$", "", (d.get("paper_id") or "").strip())
            if pid in want and pid not in out:
                docs = rp.chunk_markdown(d.get("content") or d.get("text") or "")
                out[pid] = sum(passes_chunk_quality_filter(x.page_content) for x in docs)
    return out


def main() -> int:
    rows = [json.loads(x) for x in (D / "gap_before.jsonl").open(encoding="utf-8")]
    pids = [r["paper_id"] for r in rows]
    old = {k: chunk_counts(v, pids) for k, v in OLD_DBS.items() if Path(v).exists()}
    hits = log_hits(pids)
    chunks = chunkable(rows)
    with (D / "gap_causes.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            p = r["paper_id"]
            r2 = {**r, **{f"chunks_{k}": v[p] for k, v in old.items()}, "chunkable": chunks.get(p), "log": hits[p]}
            f.write(json.dumps(r2, ensure_ascii=False) + "\n")
    for k, v in old.items():
        print(f"{k}: 청크 있는 논문 {sum(1 for n in v.values() if n)} / {len(pids)}")
    print(f"청킹 0 인 논문 {sum(1 for n in chunks.values() if not n)} · 로그에 나온 논문 {sum(1 for h in hits.values() if h)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
