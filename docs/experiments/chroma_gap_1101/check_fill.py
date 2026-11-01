"""채우기 전후 확인 — 읽기만 한다. 서버 청크 수 · 논문별 청크 수 · 제목 벡터 검색 순위.

    .venv/bin/python docs/experiments/chroma_gap_1101/check_fill.py [PID ...]   # 인자 없으면 DynamicRAG · Block-Sphere
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
D = Path(__file__).resolve().parent

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction  # noqa: E402

from core.config.agent_config import CHROMA_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL  # noqa: E402
from core.config.chroma_client import make_chroma_client  # noqa: E402
from core.rag.agent_chroma_rag import _paper_id_version_candidates  # noqa: E402
from core.rag.bm25_index import _normalize_pid  # noqa: E402


def main() -> int:
    pids = sys.argv[1:] or ["2505.07233", "2605.19972"]
    titles = {r["paper_id"]: r["title"] for r in map(json.loads, (D / "gap_before.jsonl").open(encoding="utf-8"))}
    ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True)
    col = make_chroma_client(CHROMA_DB_DIR).get_collection(name=COLLECTION_NAME, embedding_function=ef)
    print(f"서버 청크 수 {col.count():,}", flush=True)
    for pid in pids:
        n = len(col.get(where={"paper_id": {"$in": _paper_id_version_candidates(pid)}}, include=[])["ids"])
        res = col.query(query_texts=[titles[pid]], n_results=10, include=["metadatas"])
        papers = list(dict.fromkeys(_normalize_pid(str(m.get("paper_id") or "")) for m in res["metadatas"][0]))
        rank = papers.index(pid) + 1 if pid in papers else None
        print(f"{pid} 청크 {n} · 제목 검색 상위 10청크 안 논문 순위 {rank or '없음'} · {titles[pid][:60]}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
