#!/usr/bin/env python3
"""Chroma 컬렉션에서 paper_id 누락 비율을 샘플로 측정한다.

임베딩 모델을 한 번 로드해 컬렉션을 연다(Chroma 제약). 샘플은 앞쪽 limit건.
paper_id 없음 비율이 --threshold-pct(기본 1%%)를 넘으면 종료 코드 1.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from core.config.agent_config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL, PROJECT_ROOT


def _resolve_db_path() -> str:
    p = Path(CHROMA_DB_PATH)
    return str(p.resolve()) if p.is_absolute() else str((PROJECT_ROOT / p).resolve())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=5000, help="검사할 최대 청크 수(앞에서부터)")
    ap.add_argument(
        "--threshold-pct",
        type=float,
        default=1.0,
        help="paper_id 없음 비율(%%)이 이 값을 넘으면 경고 후 exit 1",
    )
    args = ap.parse_args()

    path = _resolve_db_path()
    if not Path(path).is_dir():
        print(f"Chroma 경로 없음: {path}", file=sys.stderr)
        return 2

    print(f"DB: {path}\ncollection: {COLLECTION_NAME}\nsample_limit: {args.limit}")

    ef = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True
    )
    client = chromadb.PersistentClient(path=path, settings=Settings(anonymized_telemetry=False))
    coll = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)
    total = coll.count()
    if total == 0:
        print("문서 0건.")
        return 0

    n = min(args.limit, total)
    batch = coll.get(include=["metadatas"], limit=n)
    metas = batch.get("metadatas") or []

    missing = 0
    for m in metas:
        if not isinstance(m, dict):
            missing += 1
            continue
        pid = (m.get("paper_id") or "").strip()
        if not pid:
            missing += 1

    rate_pct = 100.0 * missing / len(metas) if metas else 0.0
    print(f"샘플: {len(metas)}건 (컬렉션 count={total})")
    print(f"paper_id 없음: {missing}건 → {rate_pct:.2f}%")

    if rate_pct > args.threshold_pct:
        print(
            f"⚠️  {args.threshold_pct}% 초과 — __anon_chunk_ 집계 증가·성능 저하 가능. "
            "인제스트 메타 paper_id를 점검하세요.",
            file=sys.stderr,
        )
        return 1
    print("임계값 이내.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
