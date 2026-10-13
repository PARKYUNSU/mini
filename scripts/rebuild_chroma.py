#!/usr/bin/env python3
"""망가진 Chroma 벡터 인덱스를 SQLite 원문에서 다시 만든다 (2026-10-13 디스크 가득 참 사고).

  SQLITE_TMPDIR=/Volumes/T7\\ Shield/tmp .venv/bin/python scripts/rebuild_chroma.py \\
      --src "$HOME/Library/Application Support/mini-chroma" --dst "/Volumes/T7 Shield/mini-chroma-rebuild"

- 원본은 **읽기 전용**(``immutable=1``)으로만 연다 — 손대지 않는다.
- 원본 SQLite 의 ``embeddings``(id ↔ embedding_id) + ``embedding_metadata``(문서·메타) 를 id 순으로 흘려 읽고,
  운영과 같은 임베딩(``EMBEDDING_MODEL``, 정규화)으로 다시 계산해 새 PersistentClient 에 넣는다.
- 컬렉션 이름·``hnsw:space=cosine`` 은 원본과 같다. 이어서 하기: 새 DB 에 이미 있는 id 는 건너뛴다.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def stream_rows(src_db: Path, seg_id: str):
    """(embedding_id, document, metadata) 를 id 순으로."""
    con = sqlite3.connect(f"file:{src_db}?immutable=1", uri=True)
    ids = con.execute("SELECT id, embedding_id FROM embeddings WHERE segment_id=? ORDER BY id", (seg_id,))
    meta = con.cursor()
    meta.execute("SELECT id, key, string_value, int_value, float_value, bool_value FROM embedding_metadata ORDER BY id")
    pending = meta.fetchone()
    for rid, eid in ids:
        doc, md = None, {}
        while pending is not None and pending[0] < rid:
            pending = meta.fetchone()
        while pending is not None and pending[0] == rid:
            _, k, s, i, f, b = pending
            v = s if s is not None else i if i is not None else f if f is not None else (bool(b) if b is not None else None)
            if k == "chroma:document":
                doc = v
            elif not k.startswith("chroma:") and v is not None:
                md[k] = v
            pending = meta.fetchone()
        yield eid, doc, md


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--batch", type=int, default=4000)
    ap.add_argument("--device", default="mps")
    a = ap.parse_args()

    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer

    from core.config.agent_config import COLLECTION_NAME, EMBEDDING_MODEL

    src_db = Path(a.src) / "chroma.sqlite3"
    con = sqlite3.connect(f"file:{src_db}?immutable=1", uri=True)
    coll_id, = con.execute("SELECT id FROM collections WHERE name=?", (COLLECTION_NAME,)).fetchone()
    seg_id, = con.execute("SELECT id FROM segments WHERE collection=? AND scope='METADATA'", (coll_id,)).fetchone()
    total, = con.execute("SELECT count(*) FROM embeddings WHERE segment_id=?", (seg_id,)).fetchone()
    con.close()
    print(f"원본 {COLLECTION_NAME}: {total:,}개 · 모델 {EMBEDDING_MODEL} · device {a.device}", flush=True)

    model = SentenceTransformer(EMBEDDING_MODEL, device=a.device)
    client = chromadb.PersistentClient(path=a.dst, settings=Settings(anonymized_telemetry=False))
    col = client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
    have = col.count()
    print(f"새 DB 에 이미 {have:,}개", flush=True)

    t0, done, buf = time.time(), 0, []

    def flush() -> None:
        ids = [r[0] for r in buf]
        if have:  # 이어서 할 때만 중복을 확인한다
            got = set(col.get(ids=ids, include=[])["ids"])
            rows = [r for r in buf if r[0] not in got]
        else:
            rows = list(buf)
        if rows:
            embs = model.encode([r[1] or "" for r in rows], batch_size=256, normalize_embeddings=True,
                                show_progress_bar=False).tolist()
            col.add(ids=[r[0] for r in rows], embeddings=embs, documents=[r[1] or "" for r in rows],
                    metadatas=[r[2] or None for r in rows])
        buf.clear()

    for row in stream_rows(src_db, seg_id):
        buf.append(row)
        done += 1
        if len(buf) >= a.batch:
            flush()
            if done % (a.batch * 10) == 0:
                el = time.time() - t0
                print(f"  {done:,}/{total:,} ({done / total:.1%}) · {el / 60:.1f}분 · 남은 {el / done * (total - done) / 60:.0f}분",
                      flush=True)
    if buf:
        flush()
    print(f"완료: 새 DB {col.count():,}개 / 원본 {total:,} · {(time.time() - t0) / 60:.1f}분", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
