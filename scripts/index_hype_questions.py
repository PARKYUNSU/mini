#!/usr/bin/env python3
"""hype_1014 — questions.jsonl 을 Chroma 컬렉션 ``paper_questions`` 에 넣는다.

  CHROMA_SERVER_URL=http://127.0.0.1:8001 .venv/bin/python scripts/index_hype_questions.py

- 운영 DB 와 같은 Chroma(서버 모드면 서버로) · 같은 임베더(정규화) · cosine.
- 질문마다 두 줄: 영어 질문(kind=question), 영어 키워드(kind=keywords). id = ``<paper_id>::<qi>::<kind>``.
- 이어 하기: 이미 있는 id 는 건너뛴다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SRC = ROOT / "docs" / "experiments" / "hype_1014" / "questions.jsonl"


def main() -> int:
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    from core.config.agent_config import CHROMA_DB_DIR, EMBEDDING_MODEL
    from core.config.chroma_client import chroma_server_url, make_chroma_client
    from core.rag.agent_chroma_rag import HYPE_COLLECTION

    ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True)
    client = make_chroma_client(CHROMA_DB_DIR)
    print(f"Chroma: {'서버 ' + chroma_server_url() if chroma_server_url() else '로컬 ' + str(CHROMA_DB_DIR)}", flush=True)
    col = client.get_or_create_collection(name=HYPE_COLLECTION, embedding_function=ef, metadata={"hnsw:space": "cosine"})

    ids, docs, metas = [], [], []
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        for qi, it in enumerate(r["items"]):
            for kind in ("question", "keywords"):
                text = it["en"] if kind == "question" else it["keywords"]
                ids.append(f"{r['paper_id']}::{qi}::{kind}")
                docs.append(text)
                metas.append({"paper_id": r["paper_id"], "kind": kind, "qi": qi})
    have = set()
    for i in range(0, len(ids), 5000):
        have |= set(col.get(ids=ids[i:i + 5000], include=[])["ids"])
    todo = [k for k, x in enumerate(ids) if x not in have]
    print(f"줄 {len(ids)} · 이미 {len(have)} · 넣을 것 {len(todo)}", flush=True)
    B = 1000
    for s in range(0, len(todo), B):
        part = todo[s:s + B]
        col.add(ids=[ids[k] for k in part], documents=[docs[k] for k in part], metadatas=[metas[k] for k in part])
        if (s // B) % 10 == 0:
            print(f"  {s + len(part)}/{len(todo)}", flush=True)
    print(f"완료: {HYPE_COLLECTION} {col.count()}줄", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
