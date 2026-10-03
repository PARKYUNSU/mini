#!/usr/bin/env python3
"""
Chroma 논문 RAG 진단 스크립트.

- 키워드별: dense(벡터) Top-K 결과
- where_document(본문 부분문자열) 적용 전/후 비교
- dense vs JSONL 키워드 스캔(제목·초록) 비교 — 데이터는 있는데 벡터가 못 찾는지 구분

  cd /path/to/mini
  .venv/bin/python scripts/inspect_chroma_rag.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from core.config.agent_config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL, PROJECT_ROOT

RAW_JSONL = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"

# 사용자 요청 키워드 (표시용 문자열 → where_document에 쓸 짧은 토큰)
DEFAULT_KEYWORDS: list[tuple[str, str | None]] = [
    ("RAG", "RAG"),
    ("retrieval-augmented generation", "retrieval"),
    ("CRAG", "CRAG"),
    ("RankRAG", "RankRAG"),
    ("Adaptive-RAG", "Adaptive"),
]


def _load_collection():
    path = CHROMA_DB_PATH if Path(CHROMA_DB_PATH).is_absolute() else str((PROJECT_ROOT / CHROMA_DB_PATH).resolve())
    ef = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True
    )
    client = chromadb.PersistentClient(path=path, settings=Settings(anonymized_telemetry=False))
    col = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)
    return col


def _fmt_hit(meta: dict, dist: float | None, idx: int) -> str:
    pid = (meta or {}).get("paper_id", "") or "?"
    title = (meta or {}).get("title", "") or ""
    t = title.replace("\n", " ")[:90]
    d = f"{dist:.4f}" if dist is not None else "n/a"
    return f"  {idx}. paper_id={pid}  distance={d}\n     title: {t}"


def _query_dense(col, q: str, k: int, where_document: dict | None = None, where_meta: dict | None = None):
    kwargs = {
        "query_texts": [q],
        "n_results": k,
        "include": ["metadatas", "distances"],
    }
    if where_document is not None:
        kwargs["where_document"] = where_document
    if where_meta is not None:
        kwargs["where"] = where_meta
    return col.query(**kwargs)


def _jsonl_keyword_hits(keyword: str) -> tuple[int, list[str]]:
    """제목·초록(소문자)에 부분문자열이 포함된 고유 paper_id 수·샘플."""
    if not RAW_JSONL.is_file():
        return 0, []
    needle = keyword.lower()
    seen: set[str] = set()
    samples: list[str] = []
    try:
        with RAW_JSONL.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pid = str(d.get("paper_id", "") or "").strip()
                title = str(d.get("title", "") or "")
                abstract = str(d.get("abstract", "") or "")
                blob = (title + " " + abstract).lower()
                if needle not in blob:
                    continue
                if pid and pid not in seen:
                    seen.add(pid)
                    samples.append(f"{pid}: {title[:80]}")
                if len(samples) >= 5:
                    break
    except OSError:
        return 0, []
    # 전체 개수는 한 번 더 스캔 (정확 카운트)
    total = 0
    seen2: set[str] = set()
    try:
        with RAW_JSONL.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pid = str(d.get("paper_id", "") or "").strip()
                title = str(d.get("title", "") or "")
                abstract = str(d.get("abstract", "") or "")
                blob = (title + " " + abstract).lower()
                if needle not in blob:
                    continue
                if pid:
                    if pid not in seen2:
                        seen2.add(pid)
                        total += 1
    except OSError:
        pass
    return total, samples


def _vector_pids_from_results(res) -> set[str]:
    out: set[str] = set()
    metas = (res.get("metadatas") or [[]])[0]
    for m in metas:
        if isinstance(m, dict):
            pid = (m.get("paper_id") or "").strip()
            if pid:
                out.add(pid)
    return out


def main() -> int:
    print("=" * 72)
    print("Chroma RAG 진단 (arxiv_papers)")
    print(f"  DB: {CHROMA_DB_PATH}  collection: {COLLECTION_NAME}")
    print(f"  임베딩: {EMBEDDING_MODEL}")
    print(f"  JSONL: {RAW_JSONL}")
    print("=" * 72)

    try:
        col = _load_collection()
    except Exception as e:
        print(f"❌ Chroma 로드 실패: {e}")
        return 1

    try:
        n = col.count()
        print(f"\n[컬렉션] 총 청크 수: {n:,}")
    except Exception as e:
        print(f"\n[컬렉션] count 실패: {e}")

    k = 5

    for label, contains_token in DEFAULT_KEYWORDS:
        q = label
        print("\n" + "-" * 72)
        print(f"■ 키워드(쿼리): {q!r}")
        if contains_token:
            print(f"  (where_document 부분문자열 후보: {contains_token!r})")

        # --- JSONL: 데이터 존재 여부 (키워드 문자열 그대로) ---
        jn, jsamples = _jsonl_keyword_hits(q)
        print(f"\n  [JSONL 키워드 스캔] 제목·초록에 문자열 포함 고유 논문 수: {jn:,}")
        for s in jsamples[:5]:
            print(f"    · {s}")

        # --- Dense only ---
        try:
            res_plain = _query_dense(col, q, k)
            dists = (res_plain.get("distances") or [[]])[0]
            metas = (res_plain.get("metadatas") or [[]])[0]
            print(f"\n  [Dense only] 벡터 Top-{k} (필터 없음)")
            for i, (m, d) in enumerate(zip(metas, dists), 1):
                print(_fmt_hit(m if isinstance(m, dict) else {}, d, i))
            pids_plain = _vector_pids_from_results(res_plain)
        except Exception as e:
            print(f"\n  [Dense only] 오류: {e}")
            pids_plain = set()

        # --- where_document (본문 필터) 전/후: '후'는 청크 본문에 토큰이 있는 것만 후보 ---
        if contains_token:
            try:
                wd = {"$contains": contains_token}
                res_wd = _query_dense(col, q, k, where_document=wd)
                dists2 = (res_wd.get("distances") or [[]])[0]
                metas2 = (res_wd.get("metadatas") or [[]])[0]
                print(f'\n  [Dense + where_document] 본문에 "{contains_token}" 포함 청크만 (Top-{k})')
                if not metas2:
                    print("    (결과 없음 — 해당 문자열이 들어간 청크가 없거나 부족)")
                for i, (m, d) in enumerate(zip(metas2, dists2), 1):
                    print(_fmt_hit(m if isinstance(m, dict) else {}, d, i))
            except Exception as e:
                print(f"\n  [Dense + where_document] 오류: {e}")

        # --- metadata where: title에 토큰 (지원 시) ---
        if contains_token and len(contains_token) >= 2:
            try:
                # Chroma 문자열 메타 $contains (버전에 따라 동작)
                wm = {"title": {"$contains": contains_token}}
                res_m = _query_dense(col, q, k, where_meta=wm)
                dists3 = (res_m.get("distances") or [[]])[0]
                metas3 = (res_m.get("metadatas") or [[]])[0]
                print(f'\n  [Dense + where metadata] title에 "{contains_token}" 포함 (Top-{k})')
                if not metas3:
                    print("    (결과 없음)")
                for i, (m, d) in enumerate(zip(metas3, dists3), 1):
                    print(_fmt_hit(m if isinstance(m, dict) else {}, d, i))
            except Exception as e:
                print(f"\n  [Dense + where metadata] 스킵/오류: {e}")

        # --- Hybrid 요약: JSONL에는 있는데 벡터 Top-K paper_id에 없음 ---
        if jn > 0 and pids_plain:
            # JSONL에서 해당 키워드로 잡힌 paper_id 집합 (간단 재스캔 상위만)
            jsonl_pids: set[str] = set()
            needle = q.lower()
            try:
                with RAW_JSONL.open(encoding="utf-8", errors="replace") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            d = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        pid = str(d.get("paper_id", "") or "").strip()
                        title = str(d.get("title", "") or "")
                        abstract = str(d.get("abstract", "") or "")
                        blob = (title + " " + abstract).lower()
                        if needle in blob and pid:
                            jsonl_pids.add(pid)
            except OSError:
                pass
            only_jsonl = jsonl_pids - pids_plain
            only_vec = pids_plain - jsonl_pids
            print(f"\n  [비교 요약] JSONL 키워드 매칭 고유 논문 {len(jsonl_pids)} vs 벡터 Top-{k} 고유 논문 {len(pids_plain)}")
            if only_jsonl:
                print(f"    → JSONL에만 있고 벡터 Top-{k}에 없는 paper_id (최대 8개): {list(only_jsonl)[:8]}")
            if only_vec:
                print(f"    → 벡터에만 있고 JSONL 키워드 매칭 집합에 없는 paper_id (최대 8개): {list(only_vec)[:8]}")

    print("\n" + "=" * 72)
    print("해석 팁:")
    print("  · JSONL 카운트가 0이면 → 해당 키워드 논문이 큐에 없을 가능성이 큼.")
    print("  · JSONL은 있는데 dense Top-5가 엉뚱하면 → 임베딩 검색 한계 또는 청크 분할 이슈.")
    print("  · where_document 결과가 비면 → 본문 청크에 그 문자열이 아예 없음(약어·표기 차이).")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
