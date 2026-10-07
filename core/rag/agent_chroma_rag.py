"""논문 RAG (ChromaDB + 임베딩). agent_bot과 분리해 테스트·재사용 용이.

동기(sync)만 사용(asyncio 미사용).

macOS(Apple Silicon)에서 ``multiprocessing`` spawn 자식 + Chroma Rust 조합은
반복적으로 Segmentation fault가 나므로 **사용하지 않는다.**

**전략:** 메인 프로세스에서 ``ChromaRAGTool`` 싱글톤 1개만 두고,
``threading.Lock``(``_chroma_singleton_lock`` + ``ChromaRAGTool._db_lock``)으로
``collection.query()`` 호출을 직렬화한다.

- ``CHROMA_VECTOR_DISABLED=1`` : 부팅부터 벡터 query 없이 JSONL 폴백만
- (레거시) ``CHROMA_SUBPROCESS`` 는 더 이상 사용하지 않으며, import 시 ``0``으로 고정한다.
"""

from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.messages import HumanMessage, SystemMessage

from core.config.agent_config import (
    BM25_UNION_CHUNKS_PER_PAPER,
    BM25_UNION_TOP_M,
    CHROMA_CROSS_ENCODER_RERANK,
    CHROMA_DB_DIR,
    CHROMA_FETCH_MIN,
    CHROMA_FETCH_MULTIPLIER,
    COLLECTION_NAME,
    ENABLE_PAPER_LIGHT_RERANK,
    PAPER_LIGHT_RERANK_TOP_K,
    HYBRID_MULTI_QUERY_MAX_CHUNKS,
    HYBRID_MULTI_QUERY_MAX_QUERIES,
    HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS,
    HYBRID_MULTI_QUERY_RETRIEVAL,
    EMBEDDING_MODEL,
    HYBRID_FUSION_MODE,
    HYBRID_CHUNKS_PER_PAPER,
    HYBRID_EVAL_CHUNKS_PER_PAPER,
    HYBRID_PAPER_FIFTH_BEST_EPSILON,
    HYBRID_PAPER_FOURTH_BEST_DELTA,
    HYBRID_PAPER_MULTIEVIDENCE_BETA,
    HYBRID_PAPER_MULTIEVIDENCE_REL,
    HYBRID_PAPER_SCORE_TOP_N,
    HYBRID_PAPER_SECOND_BEST_ALPHA,
    HYBRID_PAPER_THIRD_BEST_GAMMA,
    HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT,
    HYBRID_PAPER_TITLE_SIM_HIGH_MULTIPLIER,
    HYBRID_PAPER_TITLE_SIM_HIGH_THRESHOLD,
    HYBRID_PAPER_TITLE_SIM_MULTIPLIER,
    HYBRID_PAPER_TITLE_SIM_THRESHOLD,
    HYBRID_PAPER_TITLE_SIM_WEIGHT,
    HYBRID_RRF_K,
    HYBRID_TITLE_BOOST_MULTIPLIER,
    PROJECT_ROOT,
    RAG_TOP_K,
)
from core.config.chroma_lock import is_chroma_write_locked
from core.llm.agent_llm import get_rag_query_rewrite_llm
from core.rag.bm25_index import HYBRID_BM25_WEIGHT, HYBRID_VECTOR_WEIGHT, _normalize_pid, get_bm25_searcher
from core.rag.query_expansion import build_multi_query_retrieval_queries, expand_query_for_bm25

# 레거시·문서 혼동 방지: subprocess(spawn) Chroma 경로는 비활성화
os.environ["CHROMA_SUBPROCESS"] = "0"

_log = logging.getLogger(__name__)

_SEARCH_TIMEOUT_SEC = 600.0

# ── Cross-encoder reranker (lazy singleton, 기본 비활성 — CHROMA_CROSS_ENCODER_RERANK=1 일 때만) ──
_CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_cross_encoder: object | None = None
_cross_encoder_lock = threading.Lock()


def _get_cross_encoder():
    """Cross-encoder 모델을 lazy 로드 (첫 호출 시 1회만)."""
    from sentence_transformers import CrossEncoder

    global _cross_encoder
    if _cross_encoder is not None:
        return _cross_encoder
    with _cross_encoder_lock:
        if _cross_encoder is None:
            print(f"[ChromaRAG TRACE] loading cross-encoder: {_CROSS_ENCODER_MODEL}", flush=True)
            _cross_encoder = CrossEncoder(_CROSS_ENCODER_MODEL)
            print("[ChromaRAG TRACE] cross-encoder loaded OK", flush=True)
        return _cross_encoder


def _cross_encoder_rerank(
    query: str,
    docs: list[str],
    metas: list[dict[str, str]],
    dists: list[float | None] | None,
    *,
    top_k: int,
    max_unique_papers: int = 0,
) -> tuple[list[str], list[dict[str, str]], list[float | None] | None]:
    """Cross-encoder로 (query, doc) 쌍을 재정렬.

    1. 모든 후보에 cross-encoder score 부여
    2. paper_id 기반 다양성 보장: 각 논문에서 최고 점수 청크 1개만 우선 선택
    3. top_k개까지 반환

    .. note::
        청크 단위 CE는 대규모 코퍼스에서 비용·역효과가 있어 기본 비활성이다.
        재도입 시에는 **논문 단위**로 ``title + abstract + 대표 청크``를 한 덩어리로 묶어
        (query, paper_text) 한 번만 스코어링하는 방식만 실험할 것.

    Args:
        max_unique_papers: 0이면 top_k 그대로, >0이면 최소 이 수만큼 고유 논문 확보 시도
    """
    if not docs or not query.strip():
        return docs[:top_k], metas[:top_k], dists[:top_k] if dists else None

    try:
        ce = _get_cross_encoder()
        pairs = [(query, doc[:512]) for doc in docs]
        scores = ce.predict(pairs).tolist()
    except Exception as exc:
        print(f"[ChromaRAG TRACE] cross-encoder rerank failed: {exc}", flush=True)
        return docs[:top_k], metas[:top_k], dists[:top_k] if dists else None

    # (score, original_index) 쌍으로 정렬
    indexed = sorted(enumerate(scores), key=lambda x: -x[1])

    # paper_id 기반 다양성 보장: 논문별 최고 점수 청크 우선
    first_per_paper: list[int] = []
    extra: list[int] = []
    seen_pids: set[str] = set()
    for orig_idx, score in indexed:
        pid = (metas[orig_idx].get("paper_id") or "").strip()
        if not pid or pid not in seen_pids:
            if pid:
                seen_pids.add(pid)
            first_per_paper.append(orig_idx)
        else:
            extra.append(orig_idx)

    # 고유 논문 우선 + 나머지 추가 청크
    final_order = first_per_paper + extra
    final_order = final_order[:top_k]

    out_docs = [docs[i] for i in final_order]
    out_metas = [metas[i] for i in final_order]
    out_dists = [dists[i] for i in final_order] if dists and len(dists) == len(docs) else None

    # 로그
    print(f"[ChromaRAG TRACE] cross-encoder rerank: {len(docs)} candidates → {len(out_docs)} results", flush=True)
    for rank, idx in enumerate(final_order[:5]):
        pid = (metas[idx].get("paper_id") or "?")[:20]
        print(f"  #{rank+1} ce_score={scores[idx]:.4f} pid={pid}", flush=True)

    return out_docs, out_metas, out_dists


def _minmax_normalize_01(vals: list[float]) -> list[float]:
    """후보 집합 내 min-max → [0, 1]. 전부 동일하면 0.5 (순위 붕괴 방지).

    BM25 열에는 사용하지 말 것: 전부 0·전부 동일일 때 0.5로 채우면 하이브리드가
    사실상 벡터만 쓰는 것과 구분되지 않는다. BM25는 ``_compute_hybrid_chunk_scores``에서 별도 분기.
    """
    if not vals:
        return []
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-12:
        return [0.5] * len(vals)
    return [(x - lo) / (hi - lo) for x in vals]


def _rrf_two_signals(v_raw: list[float], b_raw: list[float], *, k: float) -> list[float]:
    """두 시그널의 순위로 RRF: 1/(k+rank_v) + 1/(k+rank_b)."""
    n = len(v_raw)
    if n != len(b_raw) or n == 0:
        return []
    order_v = sorted(range(n), key=lambda i: -v_raw[i])
    rank_v = [0] * n
    for pos, ii in enumerate(order_v):
        rank_v[ii] = pos + 1
    order_b = sorted(range(n), key=lambda i: -b_raw[i])
    rank_b = [0] * n
    for pos, ii in enumerate(order_b):
        rank_b[ii] = pos + 1
    return [1.0 / (k + rank_v[i]) + 1.0 / (k + rank_b[i]) for i in range(n)]


def _compute_hybrid_chunk_scores(
    metas_clean: list[dict[str, str]],
    dists_clean: list[float | None] | None,
    bm25_pid_scores: dict[str, float],
    *,
    title_boost_query: str = "",
) -> list[float]:
    """후보 청크마다 dense·BM25 raw를 구한 뒤, 후보 집합에서 각각 min-max 후 가중합 또는 RRF.

    기존처럼 거리·BM25를 한 번에 섞으면 스케일에 따라 한쪽이 지배하기 쉬워,
    **열 단위로 정규화**한 뒤 `HYBRID_VECTOR_WEIGHT` / `HYBRID_BM25_WEIGHT`를 적용한다.
    """
    _vw, _bw = HYBRID_VECTOR_WEIGHT, HYBRID_BM25_WEIGHT
    n = len(metas_clean)
    if n == 0:
        return []

    dists = list(dists_clean) if dists_clean is not None else [None] * n
    while len(dists) < n:
        dists.append(None)
    dists = dists[:n]

    has_any_dist = any(d is not None for d in dists)
    v_raw: list[float] = []
    for i in range(n):
        d = dists[i]
        if d is None:
            v_raw.append(0.0)
            continue
        try:
            dv = float(d)
        except (TypeError, ValueError):
            v_raw.append(0.0)
            continue
        # 거리 작을수록 유사: 단조 변환만 하고 스케일은 후보 내 min-max에서 맞춘다.
        dv = max(0.0, dv)
        v_raw.append(1.0 / (1.0 + dv))

    if not has_any_dist:
        v_raw = [float(n - i) / float(max(n, 1)) for i in range(n)]

    b_raw: list[float] = []
    for i in range(n):
        raw_pid = (metas_clean[i].get("paper_id") or "").strip()
        if not raw_pid:
            b_raw.append(0.0)
            continue
        npid = _normalize_pid(raw_pid)
        try:
            val = bm25_pid_scores.get(npid)
            if val is None:
                val = bm25_pid_scores.get(raw_pid, 0.0)
            b_raw.append(float(val if val is not None else 0.0))
        except (TypeError, ValueError):
            b_raw.append(0.0)

    if HYBRID_FUSION_MODE == "rrf":
        scores = _rrf_two_signals(v_raw, b_raw, k=HYBRID_RRF_K)
    else:
        v_n = _minmax_normalize_01(v_raw)
        b_lo, b_hi = (min(b_raw), max(b_raw)) if b_raw else (0.0, 0.0)
        if not b_raw or (b_hi - b_lo) < 1e-12:
            # 전부 0 또는 전부 동일: BM25 열은 변별력 없음 → 0으로 두어 가중합에서 제거
            b_n = [0.0] * n
        else:
            b_n = [(x - b_lo) / (b_hi - b_lo) for x in b_raw]
        scores = [_vw * v_n[i] + _bw * b_n[i] for i in range(n)]

    q = (title_boost_query or "").strip().lower()
    if len(q) >= 5 and HYBRID_TITLE_BOOST_MULTIPLIER > 1.0 + 1e-12:
        mult = HYBRID_TITLE_BOOST_MULTIPLIER
        for i in range(n):
            t = (metas_clean[i].get("title") or "").strip().lower()
            if t and q in t:
                scores[i] *= mult

    return scores


def _merge_bm25_union_chunks(
    collection,
    bm25_hits: list[dict],
    docs_clean: list[str],
    metas_clean: list[dict[str, str]],
    dists_clean: list[float | None] | None,
    *,
    top_m: int,
    chunks_per_paper: int,
    min_doc_chars: int = 80,
    query_text: str = "",
) -> tuple[list[str], list[dict[str, str]], list[float | None] | None, int]:
    """벡터 후보에 없는 BM25 상위 논문의 청크를 Chroma에서 가져와 합집합.

    ``query_text`` 가 있으면 논문별로 **같은 질의의 필터 벡터 검색**을 해서 그 논문에서 질의와
    가장 가까운 청크와 그 실제 거리를 가져온다. 없으면 예전처럼 앞쪽 청크를 거리 없이(None) 가져온다.
    거리가 None 이면 RRF 에서 벡터 순위가 맨 뒤가 되어, BM25 1위 논문도 구조적으로 상위에 못
    오른다 (retrieval_eval_1007/05_conclusion.md §8.1).

    Returns:
        (docs_clean, metas_clean, dists_clean, bm25_only_paper_count)
    """
    # Chroma 는 JSONL 원본 ID(버전 접미사 포함, 예 2005.14165v4)를, BM25 는 정규화 ID 를 쓴다.
    # 둘 다 정규화해 비교하고, 조회는 버전 후보를 $in 으로 묶는다 — 정확 일치로 조회하던 동안
    # 주입이 한 번도 일어나지 않았다 (docs/experiments/retrieval_eval_1007/05_conclusion.md §7).
    existing = {
        _normalize_pid((m.get("paper_id") or "").strip())
        for m in metas_clean
        if (m.get("paper_id") or "").strip()
    }
    new_pids: list[str] = []
    for h in bm25_hits[:top_m]:
        pid = _normalize_pid((h.get("paper_id") or "").strip())
        if pid and pid not in existing:
            existing.add(pid)
            new_pids.append(pid)
    if not new_pids:
        return docs_clean, metas_clean, dists_clean, 0

    picked = None
    if query_text:
        picked = _nearest_chunks_per_paper_batched(collection, new_pids, query_text, chunks_per_paper)
    if picked is None:
        picked = {}
        for pid in new_pids:
            where = {"paper_id": {"$in": _paper_id_version_candidates(pid)}}
            try:
                if query_text:
                    # 배치 경로를 못 쓸 때만: 논문마다 필터 벡터 검색 (질의당 ~97회, 느림 — §9.1)
                    res = collection.query(
                        query_texts=[query_text],
                        where=where,
                        n_results=chunks_per_paper,
                        include=["documents", "metadatas", "distances"],
                    )
                    picked[pid] = list(zip(*_parse_chroma_query_result_row(res)))
                else:
                    got = collection.get(where=where, include=["documents", "metadatas"], limit=chunks_per_paper)
                    b_docs = got.get("documents") or []
                    picked[pid] = list(zip(b_docs, got.get("metadatas") or [], [None] * len(b_docs)))
            except Exception as exc:
                print(f"[ChromaRAG TRACE] BM25 union get failed for {pid}: {exc}", flush=True)

    injected_papers = 0
    for pid in new_pids:
        added = 0
        for bd, bm, bdist in picked.get(pid, []):
            if bd and len(bd) >= min_doc_chars:
                docs_clean.append(bd if isinstance(bd, str) else str(bd))
                metas_clean.append(
                    {str(k): ("" if v is None else str(v)) for k, v in (bm or {}).items()}
                    if isinstance(bm, dict)
                    else {}
                )
                if dists_clean is not None:
                    dists_clean.append(bdist)
                added += 1
        if added > 0:
            injected_papers += 1
    return docs_clean, metas_clean, dists_clean, injected_papers


def _nearest_chunks_per_paper_batched(
    collection,
    pids: list[str],
    query_text: str,
    k: int,
) -> dict[str, list[tuple[str, dict, float]]] | None:
    """주입 논문 전체의 청크를 **한 번에** 임베딩째 가져와 질의 코사인 거리로 논문별 상위 k개.

    논문마다 필터 검색을 하면 질의당 61s 였다 (§9.1). 컬렉션 공간이 cosine 이라 거리는
    Chroma 와 같은 1 - cos 로 계산한다. 임베딩 함수를 못 찾거나 조회가 실패하면 None
    (호출자가 논문별 경로로 떨어진다).
    """
    import numpy as np

    ef = getattr(collection, "_embedding_function", None)
    if ef is None:
        return None
    try:
        cands = [c for pid in pids for c in _paper_id_version_candidates(pid)]
        got = collection.get(
            where={"paper_id": {"$in": cands}},
            include=["documents", "metadatas", "embeddings"],
        )
        embs = got.get("embeddings")
        if embs is None or len(embs) == 0:
            return {}
        q = np.asarray(ef([query_text])[0], dtype=np.float64)
        x = np.asarray(embs, dtype=np.float64)
        dist = 1.0 - (x @ q) / (np.linalg.norm(x, axis=1) * np.linalg.norm(q) + 1e-12)
    except Exception as exc:
        print(f"[ChromaRAG TRACE] BM25 union batched get failed: {exc}", flush=True)
        return None

    by_pid: dict[str, list[tuple[float, int]]] = {}
    for i, m in enumerate(got.get("metadatas") or []):
        pid = _normalize_pid(((m or {}).get("paper_id") or "").strip())
        by_pid.setdefault(pid, []).append((float(dist[i]), i))
    docs = got.get("documents") or []
    metas = got.get("metadatas") or []
    out: dict[str, list[tuple[str, dict, float]]] = {}
    for pid, rows in by_pid.items():
        rows.sort(key=lambda r: r[0])
        out[pid] = [(docs[i], metas[i], d) for d, i in rows[:k]]
    return out


_PAPER_ID_MAX_VERSION = 20


def _paper_id_version_candidates(pid: str) -> list[str]:
    """정규화 ID → Chroma 에 저장됐을 수 있는 ID 들 (무버전 + v1..v20)."""
    base = _normalize_pid(pid)
    return [base] + [f"{base}v{i}" for i in range(1, _PAPER_ID_MAX_VERSION + 1)]


def _parse_chroma_query_result_row(results: object) -> tuple[list[str], list[dict[str, str]], list[float | None]]:
    """Chroma ``collection.query`` 단일 행 → docs / metas / dists."""
    docs = results["documents"][0] if results.get("documents") else []  # type: ignore[index]
    metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)  # type: ignore[index]
    docs_clean = [d if isinstance(d, str) else str(d) for d in docs]
    metas_clean = [
        {str(k): ("" if v is None else str(v)) for k, v in (m or {}).items()}
        if isinstance(m, dict)
        else {}
        for m in metas
    ]
    raw_dist_row = (results.get("distances") or [[]])[0]  # type: ignore[union-attr]
    dists_clean: list[float | None] = []
    for i in range(len(docs_clean)):
        if i < len(raw_dist_row) and raw_dist_row[i] is not None:
            try:
                dists_clean.append(float(raw_dist_row[i]))
            except (TypeError, ValueError):
                dists_clean.append(None)
        else:
            dists_clean.append(None)
    return docs_clean, metas_clean, dists_clean


def _bm25_pid_scores_from_hits_normalized(bm25_hits: list[dict]) -> dict[str, float]:
    """BM25 히트 목록 → paper_id별 [0,1] 정규화 점수 (max)."""
    bm25_pid_scores: dict[str, float] = {}
    if not bm25_hits:
        return bm25_pid_scores
    raw_bm25 = [float(h.get("bm25_score", 0.0)) for h in bm25_hits]
    max_b = max(raw_bm25) if raw_bm25 else 1.0
    min_b = min(raw_bm25) if raw_bm25 else 0.0
    rng_b = max_b - min_b if max_b > min_b else 1.0
    for h in bm25_hits:
        pid = h.get("paper_id")
        if not pid:
            continue
        npid = _normalize_pid(str(pid).strip())
        if not npid:
            continue
        try:
            norm = (float(h["bm25_score"]) - min_b) / rng_b
        except (TypeError, ValueError, KeyError):
            norm = 0.0
        bm25_pid_scores[npid] = max(bm25_pid_scores.get(npid, 0), norm)
    return bm25_pid_scores


def _merge_bm25_pid_scores_max(dicts: list[dict[str, float]]) -> dict[str, float]:
    """쿼리별 BM25 정규화 점수를 paper_id 기준 max로 합침 (재점수용 폴백)."""
    out: dict[str, float] = {}
    for d in dicts:
        for k, v in d.items():
            try:
                fv = float(v)
            except (TypeError, ValueError):
                fv = 0.0
            sk = str(k).strip()
            nk = _normalize_pid(sk) if sk else ""
            if not nk:
                continue
            out[nk] = max(out.get(nk, 0.0), fv)
    return out


def _merge_ranked_chunk_rows_max_score(
    batches: list[list[tuple[str, dict[str, str], float | None, float]]],
    *,
    max_chunks: int,
) -> tuple[list[str], list[dict[str, str]], list[float | None], list[float]]:
    """쿼리별 상위 청크 배치를 (paper_id, doc접두) 기준 최고 하이브리드 점수로 합집합."""
    best: dict[tuple[str, str], tuple[float, str, dict[str, str], float | None]] = {}
    for batch in batches:
        for doc, meta, dist, sc in batch:
            pid = (meta.get("paper_id") or "").strip()
            prefix = doc[:120] if doc else ""
            key = (pid, prefix)
            try:
                score = float(sc)
            except (TypeError, ValueError):
                score = 0.0
            if key not in best or score > best[key][0]:
                best[key] = (score, doc, meta, dist)
    sorted_items = sorted(best.values(), key=lambda x: -x[0])[: max(1, max_chunks)]
    out_docs = [x[1] for x in sorted_items]
    out_metas = [x[2] for x in sorted_items]
    out_dists = [x[3] for x in sorted_items]
    out_scores = [x[0] for x in sorted_items]
    return out_docs, out_metas, out_dists, out_scores


def _retrieve_and_rank_one_query_intent(
    collection,
    q: str,
    lab: str,
    fetch_n: int,
    lock: threading.Lock | None,
    *,
    per_query_top: int,
    keep_first_raw: bool,
) -> tuple[list[tuple[str, dict[str, str], float | None, float]], dict[str, float], object | None]:
    """단일 의도 쿼리: 벡터 → BM25 union → title/demote → 해당 풀에서만 RRF 하이브리드 점수 → 상위 청크."""
    def _run_q() -> object:
        return collection.query(
            query_texts=[q],
            n_results=fetch_n,
            include=["documents", "metadatas", "distances"],
        )

    if lock:
        with lock:
            results = _run_q()
    else:
        results = _run_q()
    first_raw = results if keep_first_raw else None

    docs_clean, metas_clean, dists_clean = _parse_chroma_query_result_row(results)
    bm25_pid: dict[str, float] = {}
    bm25_ref = None
    bq_expanded = q
    try:
        bm25_ref = get_bm25_searcher()
        bq_expanded = expand_query_for_bm25(q)
        if bq_expanded != q:
            print(
                f"[ChromaRAG TRACE] BM25 expansion [{lab}]: {q[:80]!r} → {bq_expanded[:120]!r}",
                flush=True,
            )
        bm25_hits = bm25_ref.search(bq_expanded, top_k=BM25_UNION_TOP_M)
        bm25_pid = _bm25_pid_scores_from_hits_normalized(bm25_hits)
        bm25_for_union = bm25_hits[:BM25_UNION_TOP_M]
        docs_clean, metas_clean, dists_clean, n_bm25_only = _merge_bm25_union_chunks(
            collection,
            bm25_for_union,
            docs_clean,
            metas_clean,
            dists_clean,
            top_m=BM25_UNION_TOP_M,
            chunks_per_paper=BM25_UNION_CHUNKS_PER_PAPER,
            query_text=q,
        )
        print(
            f"[ChromaRAG TRACE] rank-then-merge sub [{lab}]: chunks={len(docs_clean)} "
            f"bm25_only_injected={n_bm25_only}",
            flush=True,
        )
    except Exception as exc:
        print(f"[ChromaRAG TRACE] BM25 sub [{lab}] skipped: {exc}", flush=True)

    docs_clean, metas_clean, dists_clean = _title_match_rerank(
        docs_clean, metas_clean, q, dists_clean
    )
    docs_clean, metas_clean, dists_clean = _demote_reference_chunks(
        docs_clean, metas_clean, dists_clean
    )

    if bm25_ref is not None:
        pool_pids = {
            _normalize_pid((m.get("paper_id") or "").strip())
            for m in metas_clean
            if (m.get("paper_id") or "").strip()
        }
        if pool_pids:
            try:
                bm25_pid = bm25_ref.paper_bm25_scores_bulk(bq_expanded, pool_pids)
            except Exception as exc:
                print(f"[ChromaRAG TRACE] BM25 bulk sub [{lab}] skipped: {exc}", flush=True)

    cs = _compute_hybrid_chunk_scores(
        metas_clean,
        dists_clean,
        bm25_pid,
        title_boost_query=q,
    )
    rows = list(zip(docs_clean, metas_clean, dists_clean, cs))
    rows.sort(key=lambda x: -x[3])
    take = rows[: max(1, per_query_top)]
    return take, bm25_pid, first_raw


def _single_query_candidate_pool(
    collection,
    search_query: str,
    *,
    fetch_n: int,
    lock: threading.Lock | None,
) -> tuple[list[str], list[dict[str, str]], list[float | None], dict[str, float], object | None, None]:
    """멀티 쿼리 끔: 단일 벡터 + BM25 후 전역에서 RRF (merge-then-rank)."""
    def _run_q() -> object:
        return collection.query(
            query_texts=[search_query],
            n_results=fetch_n,
            include=["documents", "metadatas", "distances"],
        )

    if lock:
        with lock:
            results = _run_q()
    else:
        results = _run_q()
    first_raw = results
    docs_clean, metas_clean, dists_clean = _parse_chroma_query_result_row(results)
    print(
        f"[ChromaRAG TRACE] single-query vector: n_results={fetch_n} chunks={len(docs_clean)}",
        flush=True,
    )

    docs_clean, metas_clean, dists_clean = _title_match_rerank(
        docs_clean, metas_clean, search_query, dists_clean
    )
    docs_clean, metas_clean, dists_clean = _demote_reference_chunks(
        docs_clean, metas_clean, dists_clean
    )

    bm25_pid_scores: dict[str, float] = {}
    bm25_ref = None
    bq_expanded = search_query
    try:
        bm25_ref = get_bm25_searcher()
        bq_expanded = expand_query_for_bm25(search_query)
        if bq_expanded != search_query:
            print(
                f"[ChromaRAG TRACE] BM25 expansion: {search_query!r} → {bq_expanded[:120]!r}",
                flush=True,
            )
        bm25_hits = bm25_ref.search(bq_expanded, top_k=BM25_UNION_TOP_M)
        bm25_for_union = bm25_hits[:BM25_UNION_TOP_M]
        docs_clean, metas_clean, dists_clean, n_bm25_only = _merge_bm25_union_chunks(
            collection,
            bm25_for_union,
            docs_clean,
            metas_clean,
            dists_clean,
            top_m=BM25_UNION_TOP_M,
            chunks_per_paper=BM25_UNION_CHUNKS_PER_PAPER,
            query_text=search_query,
        )
        print(
            f"[ChromaRAG TRACE] BM25 single-query: {n_bm25_only} BM25-only papers injected",
            flush=True,
        )
        pool_pids = {
            _normalize_pid((m.get("paper_id") or "").strip())
            for m in metas_clean
            if (m.get("paper_id") or "").strip()
        }
        if pool_pids:
            bm25_pid_scores = bm25_ref.paper_bm25_scores_bulk(bq_expanded, pool_pids)
    except Exception as bm25_exc:
        print(f"[ChromaRAG TRACE] BM25 hybrid skipped: {bm25_exc}", flush=True)

    return docs_clean, metas_clean, dists_clean, bm25_pid_scores, first_raw, None


def _hybrid_retrieve_candidate_pool(
    collection,
    search_query: str,
    *,
    fetch_n: int,
    lock: threading.Lock | None,
) -> tuple[list[str], list[dict[str, str]], list[float | None], dict[str, float], object | None, list[float] | None]:
    """후보 풀: 멀티 쿼리 시 rank-then-merge(쿼리별 RRF 후 상위만 union). 마지막은 사전 계산 청크 점수."""
    if not HYBRID_MULTI_QUERY_RETRIEVAL:
        return _single_query_candidate_pool(collection, search_query, fetch_n=fetch_n, lock=lock)

    queries = build_multi_query_retrieval_queries(
        search_query,
        max_queries=HYBRID_MULTI_QUERY_MAX_QUERIES,
    )
    first_raw: object | None = None
    batches: list[list[tuple[str, dict[str, str], float | None, float]]] = []
    bm25_dicts: list[dict[str, float]] = []
    per_top = HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS

    for qi, (lab, q) in enumerate(queries):
        take, bmd, fr = _retrieve_and_rank_one_query_intent(
            collection,
            q,
            lab,
            fetch_n,
            lock,
            per_query_top=per_top,
            keep_first_raw=(qi == 0),
        )
        if fr is not None:
            first_raw = fr
        batches.append(take)
        bm25_dicts.append(bmd)

    merged_bm25 = _merge_bm25_pid_scores_max(bm25_dicts)
    docs_clean, metas_clean, dists_clean, pre_cs = _merge_ranked_chunk_rows_max_score(
        batches,
        max_chunks=HYBRID_MULTI_QUERY_MAX_CHUNKS,
    )
    print(
        f"[ChromaRAG TRACE] rank-then-merge: {len(queries)} queries × top{per_top} "
        f"→ {len(docs_clean)} chunks after union (cap={HYBRID_MULTI_QUERY_MAX_CHUNKS})",
        flush=True,
    )
    try:
        bm25 = get_bm25_searcher()
        bq = expand_query_for_bm25(search_query)
        pool_pids = {
            _normalize_pid((m.get("paper_id") or "").strip())
            for m in metas_clean
            if (m.get("paper_id") or "").strip()
        }
        if pool_pids:
            merged_bm25 = bm25.paper_bm25_scores_bulk(bq, pool_pids)
    except Exception as exc:
        print(f"[ChromaRAG TRACE] BM25 bulk (multi-query union) skipped: {exc}", flush=True)

    return docs_clean, metas_clean, dists_clean, merged_bm25, first_raw, pre_cs


_st_title_model = None
_st_title_lock = threading.Lock()


def _get_sentence_transformer_for_title_sim():
    """query–title 코사인 유사도용 (Chroma 임베딩과 동일 모델)."""
    global _st_title_model
    if _st_title_model is not None:
        return _st_title_model
    with _st_title_lock:
        if _st_title_model is None:
            from sentence_transformers import SentenceTransformer

            _st_title_model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")
    return _st_title_model


def _batch_query_title_cosine_sims(query: str, titles: list[str]) -> list[float]:
    """쿼리와 각 논문 title의 코사인 유사도 [0,1] 근사."""
    n = len(titles)
    if not (query or "").strip() or n == 0:
        return [0.0] * n
    import numpy as np

    nonempty = [(i, t.strip()) for i, t in enumerate(titles) if t and t.strip()]
    out = [0.0] * n
    if not nonempty:
        return out
    m = _get_sentence_transformer_for_title_sim()
    texts = [t for _, t in nonempty]
    emb_q = m.encode([query.strip()], normalize_embeddings=True)
    emb_t = m.encode(texts, normalize_embeddings=True)
    sims = np.dot(emb_t, emb_q[0])
    for j, (idx, _) in enumerate(nonempty):
        out[idx] = max(0.0, float(sims[j]))
    return out


def _light_rerank_paper_pool_by_embedding(
    query: str,
    paper_best: list[tuple[float, int, str]],
    docs: list[str],
    metas: list[dict[str, str]],
    pool_k: int,
    *,
    max_combined_text_chars: int | None = None,
) -> list[tuple[float, int, str]]:
    """상위 pool_k편만 query vs (title+abstract+best_chunk) 임베딩 코사인으로 순서 재정렬.

    ``max_combined_text_chars``가 주어지면 (예: 토론용 2000) title+abstract+chunk 합산을 해당 길이로 자른 뒤 인코딩한다.
    ``None``이면 기존 동작: chunk만 앞 4000자.
    """
    if not paper_best or pool_k < 1:
        return paper_best
    pool_k = min(pool_k, len(paper_best))
    pool = paper_best[:pool_k]
    rest = paper_best[pool_k:]
    texts: list[str] = []
    for _sc, best_i, _pk in pool:
        title = (metas[best_i].get("title") or "").strip()
        abstract = (metas[best_i].get("abstract") or "").strip()
        chunk = (docs[best_i] or "").strip()
        if max_combined_text_chars is None:
            chunk = chunk[:4000]
        combined = f"{title}\n\n{abstract}\n\n{chunk}".strip()
        if max_combined_text_chars is not None and len(combined) > max_combined_text_chars:
            combined = combined[:max_combined_text_chars]
        texts.append(combined)
    import numpy as np

    m = _get_sentence_transformer_for_title_sim()
    q_emb = m.encode([query.strip()], normalize_embeddings=True)[0]
    p_emb = m.encode(texts, normalize_embeddings=True, batch_size=16)
    sims = np.dot(p_emb, q_emb)
    order = np.argsort(-sims)
    reranked = [pool[int(i)] for i in order]
    print(
        f"[ChromaRAG TRACE] paper-level light rerank: pool={pool_k} "
        f"(embedding cosine on title+abstract+best_chunk)",
        flush=True,
    )
    return reranked + rest


def _apply_title_similarity_to_paper_score(base_sc: float, sim: float) -> float:
    """논문 집계 점수에 제목–쿼리 유사도 반영: 가산 + (고유사도 시) 약한 곱 + (옵션) 레거시 threshold 곱."""
    ns = float(base_sc)
    ns += float(HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT) * float(sim)
    if float(sim) > float(HYBRID_PAPER_TITLE_SIM_HIGH_THRESHOLD):
        ns *= float(HYBRID_PAPER_TITLE_SIM_HIGH_MULTIPLIER)
    if float(HYBRID_PAPER_TITLE_SIM_MULTIPLIER) > 1.0 + 1e-12 and float(sim) >= float(HYBRID_PAPER_TITLE_SIM_THRESHOLD):
        ns *= float(HYBRID_PAPER_TITLE_SIM_MULTIPLIER)
    if float(HYBRID_PAPER_TITLE_SIM_WEIGHT) > 0:
        ns += float(HYBRID_PAPER_TITLE_SIM_WEIGHT) * float(sim)
    return ns


def _paper_score_from_sorted_chunk_scores(
    sorted_desc: list[float],
    *,
    score_top_n: int,
    alpha: float,
    gamma: float,
    delta: float = 0.0,
    epsilon: float = 0.0,
) -> float:
    """논문 내 청크 점수(내림차순)로 s1 + α·s2 + γ·s3 + δ·s4 + ε·s5."""
    if not sorted_desc:
        return 0.0
    paper_sc = sorted_desc[0]
    if score_top_n >= 2 and len(sorted_desc) >= 2 and alpha > 0:
        paper_sc += alpha * sorted_desc[1]
    if score_top_n >= 3 and len(sorted_desc) >= 3 and gamma > 0:
        paper_sc += gamma * sorted_desc[2]
    if score_top_n >= 4 and len(sorted_desc) >= 4 and delta > 0:
        paper_sc += delta * sorted_desc[3]
    if score_top_n >= 5 and len(sorted_desc) >= 5 and epsilon > 0:
        paper_sc += epsilon * sorted_desc[4]
    return paper_sc


def _paper_max_one_chunk_per_paper(
    docs: list[str],
    metas: list[dict[str, str]],
    dists: list[float | None] | None,
    chunk_scores: list[float],
    top_k_papers: int,
    *,
    second_best_alpha: float | None = None,
    title_query: str = "",
    score_top_n: int | None = None,
    third_best_gamma: float | None = None,
    chunks_per_paper_out: int | None = None,
    light_rerank_query: str = "",
    light_rerank_max_input_chars: int | None = None,
) -> tuple[list[str], list[dict[str, str]], list[float | None] | None]:
    """paper_id별 논문 집계 점수로 순위를 정하고, 논문당 상위 청크 K개까지 유지.

    논문 점수: 상위 score_top_n개 청크 점수로 s1 + α·s2 + γ·s3 + δ·s4 + ε·s5 + (옵션) multi-evidence 보너스.
    multi-evidence: max에 가까운 점수의 청크가 여러 개면 일관 매칭으로 가산.
    """
    from collections import defaultdict

    n = len(docs)
    if n == 0:
        return docs, metas, dists
    if len(metas) != n or len(chunk_scores) != n:
        return docs, metas, dists

    alpha = (
        float(second_best_alpha)
        if second_best_alpha is not None
        else float(HYBRID_PAPER_SECOND_BEST_ALPHA)
    )
    if alpha < 0:
        alpha = 0.0
    gamma = float(third_best_gamma) if third_best_gamma is not None else float(HYBRID_PAPER_THIRD_BEST_GAMMA)
    if gamma < 0:
        gamma = 0.0
    delta = float(HYBRID_PAPER_FOURTH_BEST_DELTA)
    if delta < 0:
        delta = 0.0
    epsilon = float(HYBRID_PAPER_FIFTH_BEST_EPSILON)
    if epsilon < 0:
        epsilon = 0.0
    stn = int(score_top_n) if score_top_n is not None else int(HYBRID_PAPER_SCORE_TOP_N)
    if stn < 1:
        stn = 1
    if stn > 5:
        stn = 5
    k_out = int(chunks_per_paper_out) if chunks_per_paper_out is not None else int(HYBRID_CHUNKS_PER_PAPER)
    if k_out < 1:
        k_out = 1
    if k_out > 5:
        k_out = 5

    rel_thr = float(HYBRID_PAPER_MULTIEVIDENCE_REL)
    if rel_thr <= 0 or rel_thr > 1.0:
        rel_thr = 0.85
    beta_me = float(HYBRID_PAPER_MULTIEVIDENCE_BETA)
    if beta_me < 0:
        beta_me = 0.0
    title_w = float(HYBRID_PAPER_TITLE_SIM_WEIGHT)
    if title_w < 0:
        title_w = 0.0
    title_thr = float(HYBRID_PAPER_TITLE_SIM_THRESHOLD)
    title_mult = float(HYBRID_PAPER_TITLE_SIM_MULTIPLIER)

    by_pid: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for i in range(n):
        pid = (metas[i].get("paper_id") or "").strip()
        key = pid if pid else f"__anon_chunk_{i}"
        by_pid[key].append((chunk_scores[i], i))

    paper_best: list[tuple[float, int, str]] = []
    for pid_key, pairs in by_pid.items():
        sorted_pairs = sorted(pairs, key=lambda x: -x[0])
        best_sc, best_i = sorted_pairs[0]
        desc_scores = [sc for sc, _ in sorted_pairs]
        paper_sc = _paper_score_from_sorted_chunk_scores(
            desc_scores,
            score_top_n=stn,
            alpha=alpha,
            gamma=gamma,
            delta=delta,
            epsilon=epsilon,
        )
        if beta_me > 0 and best_sc > 0:
            thr = best_sc * rel_thr
            n_strong = sum(1 for sc, _ in sorted_pairs if sc >= thr)
            if n_strong >= 2:
                paper_sc += beta_me * min(n_strong - 1, 5)
        paper_best.append((paper_sc, best_i, pid_key))

    if (title_query or "").strip() and (
        float(HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT) > 0
        or float(HYBRID_PAPER_TITLE_SIM_HIGH_MULTIPLIER) > 1.0 + 1e-12
        or float(HYBRID_PAPER_TITLE_SIM_MULTIPLIER) > 1.0 + 1e-12
        or float(HYBRID_PAPER_TITLE_SIM_WEIGHT) > 0
    ):
        tq = title_query.strip()
        titles_for_rows = [(metas[bi].get("title") or "").strip() for _, bi, _ in paper_best]
        sims = _batch_query_title_cosine_sims(tq, titles_for_rows)
        adj: list[tuple[float, int, str]] = []
        for (sc, bi, pk), sim in zip(paper_best, sims):
            ns = _apply_title_similarity_to_paper_score(sc, sim)
            adj.append((ns, bi, pk))
        paper_best = adj

    paper_best.sort(key=lambda x: -x[0])
    if ENABLE_PAPER_LIGHT_RERANK and (light_rerank_query or "").strip():
        pk = min(PAPER_LIGHT_RERANK_TOP_K, len(paper_best))
        if pk >= 1:
            paper_best = _light_rerank_paper_pool_by_embedding(
                light_rerank_query.strip(),
                paper_best,
                docs,
                metas,
                pk,
                max_combined_text_chars=light_rerank_max_input_chars,
            )
    cap = max(top_k_papers, 1)
    paper_best = paper_best[:cap]

    out_docs: list[str] = []
    out_metas: list[dict[str, str]] = []
    out_dists: list[float | None] = []
    for _, _best_i, pid_key in paper_best:
        pairs = by_pid.get(pid_key, [])
        sorted_pairs = sorted(pairs, key=lambda x: -x[0])
        take = min(k_out, len(sorted_pairs))
        for j in range(take):
            bi = sorted_pairs[j][1]
            out_docs.append(docs[bi])
            out_metas.append(metas[bi])
            if dists is not None:
                out_dists.append(dists[bi] if bi < len(dists) else None)

    out_d: list[float | None] | None = None if dists is None else out_dists
    print(
        f"[ChromaRAG TRACE] paper-level s1+α·s2+γ·s3+δ·s4+ε·s5+multi-evid+title (α={alpha}, γ={gamma}, "
        f"δ={delta}, ε={epsilon}, score_top_n={stn}, chunks/paper={k_out}, rel={rel_thr}, "
        f"β={beta_me}, title_add={HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT}, "
        f"title_hi>{HYBRID_PAPER_TITLE_SIM_HIGH_THRESHOLD}×{HYBRID_PAPER_TITLE_SIM_HIGH_MULTIPLIER}, "
        f"legacy_thr={title_thr}×{title_mult}, title_w={title_w}): "
        f"{n} chunks → {len(out_docs)} rows ({cap} papers, top_k_papers={cap})",
        flush=True,
    )
    return out_docs, out_metas, out_d


def _compute_paper_ranking_rows(
    docs: list[str],
    metas: list[dict[str, str]],
    dists: list[float | None] | None,
    chunk_scores: list[float],
    *,
    title_query: str,
    second_best_alpha: float | None = None,
    score_top_n: int | None = None,
    third_best_gamma: float | None = None,
) -> list[dict[str, Any]]:
    """후보 풀 전체 논문에 대해 Production과 동일한 집계·제목 보정 후 점수 내림차순 행 (순위 분석용, top_k cap 없음)."""
    from collections import defaultdict

    n = len(docs)
    if n == 0 or len(metas) != n or len(chunk_scores) != n:
        return []

    alpha = (
        float(second_best_alpha)
        if second_best_alpha is not None
        else float(HYBRID_PAPER_SECOND_BEST_ALPHA)
    )
    if alpha < 0:
        alpha = 0.0
    gamma = float(third_best_gamma) if third_best_gamma is not None else float(HYBRID_PAPER_THIRD_BEST_GAMMA)
    if gamma < 0:
        gamma = 0.0
    delta = float(HYBRID_PAPER_FOURTH_BEST_DELTA)
    if delta < 0:
        delta = 0.0
    epsilon = float(HYBRID_PAPER_FIFTH_BEST_EPSILON)
    if epsilon < 0:
        epsilon = 0.0
    stn = int(score_top_n) if score_top_n is not None else int(HYBRID_PAPER_SCORE_TOP_N)
    if stn < 1:
        stn = 1
    if stn > 5:
        stn = 5

    rel_thr = float(HYBRID_PAPER_MULTIEVIDENCE_REL)
    if rel_thr <= 0 or rel_thr > 1.0:
        rel_thr = 0.85
    beta_me = float(HYBRID_PAPER_MULTIEVIDENCE_BETA)
    if beta_me < 0:
        beta_me = 0.0

    by_pid: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for i in range(n):
        pid = (metas[i].get("paper_id") or "").strip()
        key = pid if pid else f"__anon_chunk_{i}"
        by_pid[key].append((chunk_scores[i], i))

    rows_pre: list[dict[str, Any]] = []
    for pid_key, pairs in by_pid.items():
        sorted_pairs = sorted(pairs, key=lambda x: -x[0])
        best_sc, best_i = sorted_pairs[0]
        desc_scores = [sc for sc, _ in sorted_pairs]
        paper_sc_chunk = _paper_score_from_sorted_chunk_scores(
            desc_scores,
            score_top_n=stn,
            alpha=alpha,
            gamma=gamma,
            delta=delta,
            epsilon=epsilon,
        )
        n_strong = 0
        me_bonus = 0.0
        if beta_me > 0 and best_sc > 0:
            thr = best_sc * rel_thr
            n_strong = sum(1 for sc, _ in sorted_pairs if sc >= thr)
            if n_strong >= 2:
                me_bonus = beta_me * min(n_strong - 1, 5)
        paper_sc = paper_sc_chunk + me_bonus
        raw_pid = (metas[best_i].get("paper_id") or "").strip()
        norm_pid = _normalize_pid(raw_pid) if raw_pid else ""
        top5 = desc_scores[:5]
        rows_pre.append(
            {
                "paper_id": norm_pid,
                "pid_key": pid_key,
                "chunk_scores_top5": top5,
                "paper_score_chunk_only": float(paper_sc_chunk),
                "multievidence_bonus": float(me_bonus),
                "n_chunks_in_paper": len(sorted_pairs),
                "n_strong_chunks": int(n_strong),
                "paper_score_before_title": float(paper_sc),
                "title": (metas[best_i].get("title") or "").strip(),
            }
        )

    use_title = (title_query or "").strip() and (
        float(HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT) > 0
        or float(HYBRID_PAPER_TITLE_SIM_HIGH_MULTIPLIER) > 1.0 + 1e-12
        or float(HYBRID_PAPER_TITLE_SIM_MULTIPLIER) > 1.0 + 1e-12
        or float(HYBRID_PAPER_TITLE_SIM_WEIGHT) > 0
    )
    if use_title:
        tq = title_query.strip()
        titles_for_rows = [r["title"] for r in rows_pre]
        sims = _batch_query_title_cosine_sims(tq, titles_for_rows)
        for r, sim in zip(rows_pre, sims):
            r["title_sim"] = float(sim)
            r["paper_score_final"] = _apply_title_similarity_to_paper_score(
                r["paper_score_before_title"], float(sim)
            )
    else:
        for r in rows_pre:
            r["title_sim"] = 0.0
            r["paper_score_final"] = float(r["paper_score_before_title"])

    rows_pre.sort(key=lambda x: -float(x["paper_score_final"]))
    for rank, r in enumerate(rows_pre, start=1):
        r["rank"] = rank
    return rows_pre


def production_retrieval_debug_for_eval(
    collection,
    query: str,
    *,
    fetch_n: int,
    chunks_per_paper: int | None = None,
) -> dict[str, Any]:
    """Production Hybrid와 동일 후보 풀·청크 점수·논문 집계·제목 보정 후 전체 논문 순위표 (gap 분석용)."""
    original_query = (query or "").strip()
    search_query = _extract_paper_title_text(original_query)
    search_query = re.sub(r"[()（）]", " ", search_query).strip()
    search_query = re.sub(r"\s{2,}", " ", search_query)
    if not search_query:
        return {"error": "empty_query_after_extract", "original_query": original_query}

    docs_clean, metas_clean, dists_clean, bm25_pid_scores, _first_raw, pre_cs = _hybrid_retrieve_candidate_pool(
        collection,
        search_query,
        fetch_n=fetch_n,
        lock=None,
    )
    _tbq = original_query.strip() or search_query.strip()
    if pre_cs is not None:
        _cs = pre_cs
    else:
        _cs = _compute_hybrid_chunk_scores(
            metas_clean,
            dists_clean,
            bm25_pid_scores,
            title_boost_query=_tbq,
        )
    cop = int(chunks_per_paper) if chunks_per_paper is not None else int(HYBRID_EVAL_CHUNKS_PER_PAPER)
    rows = _compute_paper_ranking_rows(
        docs_clean,
        metas_clean,
        dists_clean,
        _cs,
        title_query=_tbq,
    )
    return {
        "original_query": original_query,
        "search_query": search_query,
        "title_boost_query": _tbq,
        "fetch_n": fetch_n,
        "chunks_per_paper_eval": cop,
        "n_chunks_in_pool": len(docs_clean),
        "ranked_papers": rows,
        "production_top5": rows[:5],
    }


# 한 번 Chroma query가 프로세스 단위로 반복 실패하면, 봇 재시작 전까지 벡터 검색 생략
_VECTOR_CIRCUIT_COOLDOWN_SEC: float = 600.0
_vector_search_disabled_until: float = 0.0
_vector_search_retry_used: bool = False
_vector_search_disabled_lock = threading.Lock()

_chroma_singleton: ChromaRAGTool | None = None
_chroma_singleton_lock = threading.Lock()


def _log_rag_debug_chroma_raw(
    *,
    user_query: str,
    vector_query: str,
    top_k: int,
    results: dict,
) -> None:
    """
    Chroma ``collection.query`` 직후 진단용 로그만 출력. 검색·재랭킹 로직은 건드리지 않음.

    Chroma는 ``query`` 응답에 **similarity score 필드가 없고** ``distances``(거리)만 준다.
    컬렉션은 cosine 공간이면 보통 **distance가 작을수록 더 유사** (별도 similarity 엔드포인트 없음).
    """
    try:
        docs = (results.get("documents") or [[]])[0]
        metas = (results.get("metadatas") or [[]])[0]
        raw_dists = results.get("distances")
        dists = (raw_dists or [[]])[0] if raw_dists is not None else []
        uq = (user_query or "").replace("\n", " ").strip()
        vq = (vector_query or "").replace("\n", " ").strip()
        if len(uq) > 220:
            uq = uq[:220] + "…"
        if len(vq) > 220:
            vq = vq[:220] + "…"
        # 임베딩에 넣은 문자열(실제 검색 쿼리) — 사용자 예시와 동일하게 한 줄로
        print(f"[RAG DEBUG] Query: {vq}", flush=True)
        if vq != uq:
            print(f"[RAG DEBUG] Query (user, before extract): {uq}", flush=True)
        print(
            f"[RAG DEBUG] Chroma raw retrieval: top_k={top_k} rows={len(docs)} "
            f"(metric=distance only; no similarity score in API response)",
            flush=True,
        )
        if raw_dists is None:
            print(
                "[RAG DEBUG] distances: MISSING — results dict had no 'distances' key "
                "(expected if include= omits distances; this build uses include with distances).",
                flush=True,
            )
        elif docs and not dists:
            print(
                "[RAG DEBUG] distances: empty list — row count mismatch or Chroma version quirk; "
                "per-hit distance=n/a",
                flush=True,
            )
        if not docs:
            print("[RAG DEBUG] (no hits)", flush=True)
            return
        for i, meta in enumerate(metas):
            m = meta if isinstance(meta, dict) else {}
            pid = (m.get("paper_id") or "").strip() or "?"
            title = (m.get("title") or "").strip().replace("\n", " ")
            if len(title) > 180:
                title = title[:177] + "…"
            if not title:
                title = "?"
            dist = dists[i] if i < len(dists) else None
            if isinstance(dist, (int, float)):
                dist_s = f"{float(dist):.4f}"
            elif dist is None:
                dist_s = "n/a"
            else:
                dist_s = str(dist)
            print(f"#{i + 1} | distance={dist_s} | paper_id={pid} | title={title}", flush=True)
    except Exception as exc:
        print(f"[RAG DEBUG] log skipped: {type(exc).__name__}: {exc}", flush=True)


def _strip_urls_text(query: str) -> str:
    if "http" not in query.lower():
        return query
    parts = query.split()
    return " ".join(x for x in parts if not x.lower().startswith("http")).strip()


def _extract_paper_title_text(query: str) -> str:
    for sep in (" 이거", " 이 논문", " 논문 ", " 논문좀", " 논문 자세히", " 요약", " paper"):
        if sep in query:
            before = query.split(sep)[0].strip()
            if before and len(before) > 10 and any(c.isalnum() for c in before):
                return before
    return query


def _rewrite_rag_query(query: str, session_context: str) -> str:
    if not session_context or len(query) > 50:
        return query
    vague = ("그거", "그게", "그것", "그건", "이거", "저거", "이게", "저게",
             "더 자세히", "자세히 설명", "더 자세하게", "자세하게")
    if not any(v in query for v in vague):
        return query
    try:
        llm = get_rag_query_rewrite_llm()
        resp = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "사용자가 '그거', '더 자세히' 등으로 참조하는 대상의 **논문 제목 또는 핵심 키워드**를 "
                        "10단어 이내로 출력하세요. 설명·사고과정·문장 금지. 키워드만."
                    )
                ),
                HumanMessage(content=f"[대화]\n{session_context[:600]}\n\n[질문]\n{query}\n\n키워드:"),
            ]
        )
        raw = (resp.content or "").strip()
        # <think>...</think> 태그 제거
        cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        # 첫 줄만 사용 (설명 문장 방지)
        first_line = cleaned.split("\n")[0].strip()
        rewritten = first_line[:80] if first_line else query
        print(f"[ChromaRAG TRACE] rewrite: '{query}' → '{rewritten}'", flush=True)
        return rewritten if rewritten else query
    except Exception:
        return query


def _env_chroma_vector_force_disabled() -> bool:
    return os.environ.get("CHROMA_VECTOR_DISABLED", "").strip().lower() in ("1", "true", "yes", "on")


def _vector_search_effective_disabled() -> bool:
    """
    벡터 검색 쿨다운 서킷 브레이커:
    - now < disabled_until: disallow (JSONL 폴백)
    - now >= disabled_until:
        - retry 1회 미사용이면 allow 1회(retry_used=True)
        - retry 1회 사용 이후엔 다시 disallow (다음 disable_until 갱신 전까지 vector search 미시도)
    """
    if _env_chroma_vector_force_disabled():
        return True
    global _vector_search_retry_used
    now = time.time()
    with _vector_search_disabled_lock:
        if _vector_search_disabled_until <= 0:
            return False
        if now < _vector_search_disabled_until:
            return True
        # 쿨다운 종료. retry 1회 allow.
        if not _vector_search_retry_used:
            _vector_search_retry_used = True
            print(
                f"[ChromaRAG TRACE] circuit breaker: cooldown ended, allow 1 retry "
                f"(disabled_until={_vector_search_disabled_until:.0f})",
                flush=True,
            )
            return False
        # retry 이미 사용됨 → disallow
        return True


def _clear_vector_search_disabled() -> None:
    global _vector_search_disabled_until, _vector_search_retry_used
    with _vector_search_disabled_lock:
        _vector_search_disabled_until = 0.0
        _vector_search_retry_used = False
        print("[ChromaRAG TRACE] circuit breaker: vector search restored (no cooldown)", flush=True)


def _set_vector_search_disabled_for_process() -> None:
    global _vector_search_disabled_until, _vector_search_retry_used
    with _vector_search_disabled_lock:
        _vector_search_disabled_until = time.time() + _VECTOR_CIRCUIT_COOLDOWN_SEC
        _vector_search_retry_used = False
    print(
        "[ChromaRAG TRACE] circuit breaker: vector search disabled for 600s. "
        "쿨다운 종료 후 자동 재시도 1회 진행합니다.",
        flush=True,
    )


def _published_line_from_record(meta_or_doc: dict) -> str:
    """
    Chroma 메타데이터 또는 JSONL 레코드에서 발행일을 찾아 [발행일: YYYY-MM-DD] 한 줄로 반환.
    없거나 파싱 불가면 빈 문자열.
    """
    for key in ("published_date", "published", "date"):
        v = meta_or_doc.get(key)
        if v is None:
            continue
        s = str(v).strip()
        if not s:
            continue
        s = s.replace("Z", "").replace("z", "")
        if len(s) >= 10 and s[4] == "-" and s[7] == "-":
            return f"[발행일: {s[:10]}]"
        if "T" in s and len(s) >= 10 and s[4] == "-" and s[7] == "-":
            return f"[발행일: {s[:10]}]"
        # 짧은 비표준 값도 컨텍스트에 남김
        return f"[발행일: {s[:32]}]"
    return ""


_TOKEN_SPLIT_RE = re.compile(r"[^0-9A-Za-z가-힣]+")


def _tokenize_for_overlap(text: str) -> set[str]:
    """
    query 토큰 vs candidate 텍스트 토큰 겹침을 위한 간단 토크나이저.
    """
    s = (text or "").lower().strip()
    if not s:
        return set()
    parts = [p for p in _TOKEN_SPLIT_RE.split(s) if p]
    return {p for p in parts if len(p) >= 2}


def _overlap_score(query_tokens: set[str], title_tokens: set[str], abstract_tokens: set[str], body_tokens: set[str]) -> float:
    if not query_tokens:
        return 0.0
    # title/abstract/body 순으로 더 중요하다고 가정해 가중치 부여
    t = len(query_tokens & title_tokens) * 3.0
    a = len(query_tokens & abstract_tokens) * 2.0
    b = len(query_tokens & body_tokens) * 1.0
    return t + a + b


def _render_jsonl_block_for_record(d: dict) -> str:
    """JSONL 레코드 1개를 LLM 컨텍스트용 블록 문자열로 렌더링."""
    pid = str(d.get("paper_id", "") or "")
    title = str(d.get("title", "") or "")
    abstract = str(d.get("abstract", "") or d.get("summary", "") or "")
    body = str(d.get("text", "") or d.get("content", "") or "")
    chunk = body if len(body) > len(abstract) else abstract
    if not chunk and not title:
        return ""
    head = f"[{pid}] {title}\n".strip() if (pid or title) else ""
    pub = _published_line_from_record(d)
    prefix = f"{pub}\n" if pub else ""
    body_snip = (chunk[:2800] if chunk else "") if chunk else ""
    return f"{prefix}{head}{body_snip}".strip() if body_snip else f"{prefix}{head}".strip()


def _rerank_jsonl_candidates(query: str, candidates: list[dict], *, top_n: int) -> list[dict]:
    """
    JSONL 후보 레코드를 토큰 겹침 + 메타 보너스로 재정렬 후 top_n만 반환.
    candidates는 이미 "최근 tail 기반 풀"로 잘라온 상태를 가정.
    """
    query_tokens = _tokenize_for_overlap(query)
    scored: list[tuple[float, int, dict]] = []
    for rec_idx, d in enumerate(candidates):
        title = str(d.get("title", "") or "")
        abstract = str(d.get("abstract", "") or d.get("summary", "") or "")
        body = str(d.get("text", "") or d.get("content", "") or "")
        body_snip = body[:2000] if body else ""

        title_tokens = _tokenize_for_overlap(title)
        abstract_tokens = _tokenize_for_overlap(abstract)
        body_tokens = _tokenize_for_overlap(body_snip)

        base = _overlap_score(query_tokens, title_tokens, abstract_tokens, body_tokens)

        # 발행일/제목 메타 보너스
        bonus = 0.0
        if title.strip():
            bonus += 2.0
        if d.get("published_date") or d.get("published") or d.get("date"):
            bonus += 1.0

        score = base + bonus
        # rec_idx가 작을수록 더 최근이므로 동점이면 더 최근 우선
        scored.append((score, rec_idx, d))

    scored.sort(key=lambda x: (-x[0], x[1]))
    top = scored[: max(1, top_n)]
    return [d for _, _, d in top]


def _reverse_readline(fpath: Path, buf_size: int = 8192):
    """파일 끝에서 역방향으로 한 줄씩 yield (전체 메모리 로드 없음)."""
    with fpath.open("rb") as f:
        f.seek(0, 2)
        remaining = f.tell()
        leftover = b""
        while remaining > 0:
            read_size = min(buf_size, remaining)
            remaining -= read_size
            f.seek(remaining)
            chunk = f.read(read_size) + leftover
            lines = chunk.split(b"\n")
            leftover = lines[0]
            for line in reversed(lines[1:]):
                yield line.decode("utf-8", errors="replace")
        if leftover:
            yield leftover.decode("utf-8", errors="replace")


def _fallback_rag_from_jsonl_tail(*, query: str, max_papers: int = 2, max_chars: int = 6500) -> str:
    """Chroma 실패 시 JSONL 후보를 역순 tail로 수집, 토큰 겹침 재정렬 후 상위 문서만 사용."""
    raw_path = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"
    if not raw_path.exists():
        return ""
    candidate_pool_size = max(20, max_papers * 4)
    candidates: list[dict] = []
    try:
        for line in _reverse_readline(raw_path):
            if len(candidates) >= candidate_pool_size:
                break
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            block = _render_jsonl_block_for_record(d)
            if not block:
                continue
            candidates.append(d)
    except OSError:
        return ""
    if not candidates:
        return ""

    selected = _rerank_jsonl_candidates(query, candidates, top_n=max_papers)
    selected_blocks: list[str] = []
    for d in selected:
        block = _render_jsonl_block_for_record(d)
        if block:
            selected_blocks.append(block)
    text = "\n\n---\n\n".join(selected_blocks)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n...(이하 잘림)"
    return (
        "[시스템: Chroma 벡터 검색에 실패해 raw_data_queue/crawled_papers.jsonl의 최근 후보를 "
        "질문 토큰 겹침 기준으로 재정렬 후 상위 문서 텍스트만 불러왔습니다. 아래만 근거로 요약하세요.]\n\n"
        + text
    )


def _keyword_supplement_from_jsonl(
    query: str, existing_pids: set[str], *, max_extra: int = 5
) -> list[tuple[str, dict[str, str]]]:
    """Chroma 벡터 검색으로 놓친 논문을 JSONL에서 키워드 매칭으로 보충.

    title/abstract에 쿼리 핵심 키워드가 포함된 논문 중
    이미 Chroma 결과에 있는 paper_id를 제외한 것만 반환한다.
    """
    raw_path = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"
    if not raw_path.exists():
        return []
    q_lower = (query or "").lower()
    keywords: list[str] = []
    for token in _TOKEN_SPLIT_RE.split(q_lower):
        token = token.strip()
        if len(token) >= 3:
            keywords.append(token)
    if not keywords:
        return []
    matches: list[tuple[str, dict[str, str]]] = []
    try:
        with raw_path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pid = str(d.get("paper_id", "") or "")
                if pid in existing_pids:
                    continue
                title = str(d.get("title", "") or "").lower()
                abstract = str(
                    d.get("abstract", "") or d.get("summary", "") or ""
                ).lower()[:500]
                combined = title + " " + abstract
                if any(kw in combined for kw in keywords):
                    pub = _published_line_from_record(d)
                    title_str = d.get("title", "") or ""
                    body = str(
                        d.get("abstract", "")
                        or d.get("summary", "")
                        or d.get("text", "")
                        or ""
                    )
                    header = (
                        f"[{pid}] {title_str}\n" if (pid or title_str) else ""
                    )
                    prefix = f"{pub}\n" if pub else ""
                    block = f"{prefix}{header}{body[:1200]}".strip()
                    meta: dict[str, str] = {
                        "paper_id": pid,
                        "title": title_str,
                    }
                    for key in ("published_date", "published", "date"):
                        v = d.get(key)
                        if v:
                            meta[key] = str(v)
                            break
                    if block:
                        matches.append((block, meta))
                        existing_pids.add(pid)
                    if len(matches) >= max_extra:
                        break
    except OSError:
        pass
    if matches:
        print(
            f"[ChromaRAG TRACE] keyword_supplement: "
            f"{len(matches)} papers added from JSONL",
            flush=True,
        )
    return matches


_ALIAS_MAP: dict[str, str] = {
    "transformer": "Attention Is All You Need",
    "bert": "BERT Pre-training of Deep Bidirectional Transformers",
    "gpt-3": "Language Models are Few-Shot Learners",
    "gpt-4": "GPT-4 Technical Report",
    "gpt-4o": "GPT-4o System Card",
    "resnet": "Deep Residual Learning for Image Recognition",
    "gan": "Generative Adversarial Networks",
    "vit": "An Image is Worth 16x16 Words",
    "clip": "Learning Transferable Visual Models From Natural Language Supervision",
    "diffusion": "Denoising Diffusion Probabilistic Models",
    "rlhf": "Training language models to follow instructions with human feedback",
    "alphago": "Mastering the game of Go with deep neural networks and tree search",
    "word2vec": "Efficient Estimation of Word Representations in Vector Space",
    "adam": "Adam: A Method for Stochastic Optimization",
    "dropout": "Dropout: A Simple Way to Prevent Neural Networks from Overfitting",
    "batch normalization": "Batch Normalization: Accelerating Deep Network Training",
    "batchnorm": "Batch Normalization: Accelerating Deep Network Training",
    "llama": "LLaMA: Open and Efficient Foundation Language Models",
}

_title_index: list[tuple[str, str]] | None = None
_title_index_lock = threading.Lock()


def _load_title_index() -> list[tuple[str, str]]:
    """JSONL에서 (paper_id, title) 인덱스를 한 번만 로드."""
    global _title_index
    if _title_index is not None:
        return _title_index
    with _title_index_lock:
        if _title_index is not None:
            return _title_index
        idx: list[tuple[str, str]] = []
        raw_path = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"
        if raw_path.exists():
            try:
                with raw_path.open(encoding="utf-8", errors="replace") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            d = json.loads(line)
                            pid = d.get("paper_id", "")
                            title = d.get("title", "")
                            if pid and title:
                                idx.append((pid, title))
                        except json.JSONDecodeError:
                            continue
            except Exception:
                pass
        _title_index = idx
    return _title_index


def _find_paper_by_title(search_query: str, threshold: float = 0.6) -> str | None:
    """쿼리와 제목 토큰 겹침이 threshold 이상인 paper_id 반환.

    별명(alias)도 지원: 'Transformer' → 'Attention Is All You Need' 등.
    """
    effective_query = search_query
    q_lower = search_query.lower().strip()
    for alias, canonical in _ALIAS_MAP.items():
        if alias in q_lower:
            effective_query = canonical
            print(
                f"[ChromaRAG TRACE] alias resolved: '{alias}' -> '{canonical}'",
                flush=True,
            )
            break

    q_tokens = _tokenize_for_overlap(effective_query)
    if len(q_tokens) < 2:
        return None
    idx = _load_title_index()
    best_pid: str | None = None
    best_score = 0.0
    for pid, title in idx:
        t_tokens = _tokenize_for_overlap(title)
        if not t_tokens:
            continue
        overlap = q_tokens & t_tokens
        fwd = len(overlap) / len(q_tokens)
        rev = len(overlap) / len(t_tokens)
        score = max(fwd, rev)
        if score > best_score:
            best_score = score
            best_pid = pid
    if best_score >= threshold:
        print(
            f"[ChromaRAG TRACE] title_index match: pid={best_pid} score={best_score:.2f}",
            flush=True,
        )
        return best_pid
    return None


def _title_match_rerank(
    docs: list[str],
    metas: list[dict[str, str]],
    search_query: str,
    dists: list[float | None] | None = None,
) -> tuple[list[str], list[dict[str, str]], list[float | None] | None]:
    """
    Chroma 벡터 검색 결과를 제목 일치도로 재정렬.
    쿼리 토큰의 60%+ 가 논문 title에 존재하면 해당 논문을 최상위로 올린다.
    벡터 검색은 의미적 유사도만 보므로 정확한 제목 검색에서 오분류가 발생한다.
    """
    if dists is not None and len(dists) != len(docs):
        dists = None
    if not docs or not search_query or len(docs) <= 1:
        return docs, metas, dists
    q_tokens = _tokenize_for_overlap(search_query)
    if len(q_tokens) < 2:
        return docs, metas, dists

    best_idx = -1
    best_score = 0.0
    for i, meta in enumerate(metas):
        title = (meta.get("title") or "").strip()
        if not title:
            continue
        t_tokens = _tokenize_for_overlap(title)
        if not t_tokens:
            continue
        overlap = q_tokens & t_tokens
        score = len(overlap) / len(q_tokens)
        if score > best_score:
            best_score = score
            best_idx = i

    if best_idx > 0 and best_score >= 0.6:
        print(
            f"[ChromaRAG TRACE] title_match_rerank: promoting #{best_idx} "
            f"(score={best_score:.2f}) to #0",
            flush=True,
        )
        docs = [docs[best_idx]] + docs[:best_idx] + docs[best_idx + 1 :]
        metas = [metas[best_idx]] + metas[:best_idx] + metas[best_idx + 1 :]
        if dists is not None:
            dists = [dists[best_idx]] + dists[:best_idx] + dists[best_idx + 1 :]
    return docs, metas, dists


_ITALIC_JOURNAL_RE = re.compile(r"_[A-Z][A-Za-z].*?_")


def _is_reference_chunk(text: str) -> bool:
    """청크가 논문 참고문헌(bibliography) 항목인지 판별.

    벡터 검색에서 키워드가 참고문헌 인용에 나타나면 의미 없는 청크가 상위로 올라온다.
    DOI/ISSN/이탤릭 저널명/[번호] 패턴의 조합으로 참고문헌 여부를 추정한다.
    """
    s = (text or "").strip()
    if len(s) < 30:
        return False
    sample = s[:600]
    lower = sample.lower()
    indicators = 0
    if "doi:" in lower or "doi.org/" in lower:
        indicators += 2
    if "issn" in lower or "isbn" in lower:
        indicators += 2
    if _ITALIC_JOURNAL_RE.search(sample):
        indicators += 1
    if "https://doi.org/" in sample:
        indicators += 1
    bracket_refs = len(re.findall(r"\[\d{1,4}\]", sample))
    indicators += bracket_refs
    if re.match(r"\s*[-–•*]?\s*\[?\d*\]?\s*[A-Z][a-z]+\s+[A-Z]", s):
        indicators += 1
    return indicators >= 3


def _demote_reference_chunks(
    docs: list[str],
    metas: list[dict[str, str]],
    dists: list[float | None] | None = None,
) -> tuple[list[str], list[dict[str, str]], list[float | None] | None]:
    """참고문헌 청크를 결과 뒤쪽으로 밀어내어 본문 청크가 우선 노출되도록 재정렬."""
    if dists is not None and len(dists) != len(docs):
        dists = None
    content_docs: list[str] = []
    content_metas: list[dict[str, str]] = []
    content_dists: list[float | None] = []
    ref_docs: list[str] = []
    ref_metas: list[dict[str, str]] = []
    ref_dists: list[float | None] = []
    demoted = 0
    for i, (doc, meta) in enumerate(zip(docs, metas)):
        dval = dists[i] if dists is not None and i < len(dists) else None
        if _is_reference_chunk(doc):
            ref_docs.append(doc)
            ref_metas.append(meta)
            if dists is not None:
                ref_dists.append(dval)
            demoted += 1
        else:
            content_docs.append(doc)
            content_metas.append(meta)
            if dists is not None:
                content_dists.append(dval)
    if demoted:
        print(
            f"[ChromaRAG TRACE] demote_reference_chunks: {demoted}/{len(docs)} demoted",
            flush=True,
        )
    if dists is None:
        return content_docs + ref_docs, content_metas + ref_metas, None
    return content_docs + ref_docs, content_metas + ref_metas, content_dists + ref_dists


def _dedupe_hits_by_paper(
    docs: list[str],
    metas: list[dict[str, str]],
    dists: list[float | None] | None = None,
) -> list[tuple[str, dict[str, str], float | None]]:
    """
    동일 paper_id 청크가 상위에 몰리는 편향 완화.
    논문별로 첫 번째(최고 관련도) 청크만 우선 배치하고,
    같은 논문의 추가 청크는 뒤에 붙인다.
    paper_id가 없는 청크는 고유한 것으로 취급.
    """
    if dists is not None and len(dists) != len(docs):
        dists = None
    first_per_paper: list[tuple[str, dict[str, str], float | None]] = []
    extra: list[tuple[str, dict[str, str], float | None]] = []
    seen_pids: set[str] = set()
    for i, (doc, meta) in enumerate(zip(docs, metas)):
        dval = dists[i] if dists is not None and i < len(dists) else None
        pid = (meta.get("paper_id") or "").strip()
        if not pid:
            first_per_paper.append((doc, meta, dval))
            continue
        if pid not in seen_pids:
            seen_pids.add(pid)
            first_per_paper.append((doc, meta, dval))
        else:
            extra.append((doc, meta, dval))
    return first_per_paper + extra


def _distance_block_line(dval: float | None) -> str:
    """LLM 컨텍스트용: Chroma cosine distance (작을수록 유사). 없으면 미상."""
    if dval is None:
        return "[Distance: 미상]\n"
    try:
        return f"[Distance: {float(dval):.4f}]\n"
    except (TypeError, ValueError):
        return "[Distance: 미상]\n"


def _unique_ordered_paper_ids_from_metas(
    metas: list[dict[str, str]],
    *,
    max_papers: int,
) -> list[str]:
    """메타 행 순서를 유지한 고유 paper_id (eval recall@K용)."""
    seen: set[str] = set()
    out: list[str] = []
    for m in metas:
        raw = (m.get("paper_id") or "").strip()
        pid = _normalize_pid(raw) if raw else ""
        if not pid or pid in seen:
            continue
        seen.add(pid)
        out.append(pid)
        if len(out) >= max_papers:
            break
    return out


def hybrid_retrieve_paper_ids_for_eval(
    collection,
    query: str,
    *,
    fetch_n: int,
    top_k: int,
    chunks_per_paper: int | None = None,
) -> list[str]:
    """평가 스크립트용: CE·JSONL 보강·depth 제외, 나머지는 ``search``와 동일한 랭킹.

    논문 순위: 청크 점수(hybrid+RRF) 후 논문 집계(s1+α·s2+…) 및 제목 보정과 동일.
    ``chunks_per_paper``가 None이면 ``HYBRID_EVAL_CHUNKS_PER_PAPER`` 사용.
    """
    import re as _re

    original_query = (query or "").strip()
    search_query = _extract_paper_title_text(original_query)
    search_query = _re.sub(r"[()（）]", " ", search_query).strip()
    search_query = _re.sub(r"\s{2,}", " ", search_query)
    if not search_query:
        return []

    docs_clean, metas_clean, dists_clean, bm25_pid_scores, _first_raw, pre_cs = (
        _hybrid_retrieve_candidate_pool(
            collection,
            search_query,
            fetch_n=fetch_n,
            lock=None,
        )
    )

    _tbq = original_query.strip() or search_query.strip()
    if pre_cs is not None:
        _cs = pre_cs
    else:
        _cs = _compute_hybrid_chunk_scores(
            metas_clean,
            dists_clean,
            bm25_pid_scores,
            title_boost_query=_tbq,
        )
    cop = int(chunks_per_paper) if chunks_per_paper is not None else HYBRID_EVAL_CHUNKS_PER_PAPER
    _, metas_out, _ = _paper_max_one_chunk_per_paper(
        docs_clean,
        metas_clean,
        dists_clean,
        _cs,
        top_k_papers=max(top_k, 1),
        title_query=_tbq,
        chunks_per_paper_out=cop,
        light_rerank_query=_tbq,
    )
    return _unique_ordered_paper_ids_from_metas(metas_out, max_papers=max(top_k, 1))


def _format_debate_context_blocks(
    docs: list[str],
    metas: list[dict[str, str]],
    *,
    max_chars_per_chunk: int = 6000,
    max_abstract_chars: int = 2000,
) -> str:
    """하이브리드로 뽑은 (다중 청크) 히트를 토론 프롬프트용 블록 문자열로 묶는다."""
    from collections import defaultdict

    if not docs or not metas:
        return "관련 문서 없음"
    by_pid: dict[str, list[tuple[str, dict[str, str]]]] = defaultdict(list)
    for d, m in zip(docs, metas):
        pid = (m.get("paper_id") or "").strip() or "__anon__"
        by_pid[pid].append((d, m))
    parts: list[str] = []
    for idx, (pid, items) in enumerate(by_pid.items(), 1):
        m0 = items[0][1]
        title = (m0.get("title") or "").strip()
        abst = (m0.get("abstract") or "").strip()
        if len(abst) > max_abstract_chars:
            abst = abst[:max_abstract_chars] + "…"
        chunk_parts: list[str] = []
        for d, _ in items:
            t = (d or "").strip()
            if len(t) > max_chars_per_chunk:
                t = t[:max_chars_per_chunk] + "\n(중략)"
            chunk_parts.append(t)
        body = "\n\n--- chunk ---\n\n".join(chunk_parts)
        parts.append(f"### [{idx}] paper_id={pid}\n**제목:** {title}\n**초록 일부:** {abst}\n\n**본문 발췌:**\n{body}")
    return "\n\n\n".join(parts)


def hybrid_retrieve_context_for_debate(
    query: str,
    *,
    top_k_papers: int = 5,
    light_rerank_input_max_chars: int = 2000,
) -> str:
    """LLM 토론용: Production 하이브리드 + 논문 단위 Light Rerank로 상위 논문 텍스트를 반환.

    - 평가 스크립트와 동일한 후보 풀·집계 경로.
    - Light Rerank 입력은 ``light_rerank_input_max_chars``(기본 2000)로 잘라 BGE/임베딩 토큰 부담을 줄인다.
    """
    if _vector_search_effective_disabled():
        return _fallback_rag_from_jsonl_tail(query=query, max_papers=max(1, top_k_papers))
    if is_chroma_write_locked():
        print("[ChromaRAG TRACE] debate retrieve: chroma_write_lock → JSONL fallback", flush=True)
        return _fallback_rag_from_jsonl_tail(query=query, max_papers=max(1, top_k_papers))

    original_query = (query or "").strip()
    search_query = _extract_paper_title_text(original_query)
    search_query = re.sub(r"[()（）]", " ", search_query).strip()
    search_query = re.sub(r"\s{2,}", " ", search_query)
    if not search_query:
        return "관련 문서 없음"

    tool = _get_chroma_singleton()
    collection = tool._collection
    lock = tool._db_lock

    max_k = max(int(top_k_papers), 1)
    fetch_n = int(max(float(max_k) * float(CHROMA_FETCH_MULTIPLIER), float(CHROMA_FETCH_MIN)))

    docs_clean, metas_clean, dists_clean, bm25_pid_scores, _first_raw, pre_cs = (
        _hybrid_retrieve_candidate_pool(
            collection,
            search_query,
            fetch_n=fetch_n,
            lock=lock,
        )
    )
    _tbq = original_query.strip() or search_query.strip()
    if pre_cs is not None:
        _cs = pre_cs
    else:
        _cs = _compute_hybrid_chunk_scores(
            metas_clean,
            dists_clean,
            bm25_pid_scores,
            title_boost_query=_tbq,
        )
    cop = int(HYBRID_EVAL_CHUNKS_PER_PAPER)
    docs_out, metas_out, _dout = _paper_max_one_chunk_per_paper(
        docs_clean,
        metas_clean,
        dists_clean,
        _cs,
        top_k_papers=max_k,
        title_query=_tbq,
        chunks_per_paper_out=cop,
        light_rerank_query=_tbq,
        light_rerank_max_input_chars=light_rerank_input_max_chars,
    )
    return _format_debate_context_blocks(docs_out, metas_out)


def _format_chroma_hits(
    docs: list[str],
    metas: list[dict[str, str]],
    dists: list[float | None] | None = None,
) -> str:
    if not docs:
        return "관련 문서 없음"
    deduped = _dedupe_hits_by_paper(docs, metas, dists)
    parts: list[str] = []
    for doc, meta, dval in deduped:
        dist_line = _distance_block_line(dval)
        pub = _published_line_from_record(meta)
        pid = meta.get("paper_id", "")
        title = meta.get("title", "")
        header = f"[{pid}] {title}\n" if (pid or title) else ""
        body = doc[:1200] if doc else ""
        prefix = f"{pub}\n" if pub else ""
        block = f"{dist_line}{prefix}{header}{body}".strip() if body else f"{dist_line}{prefix}{header}".strip()
        if block:
            parts.append(block)
    return "\n\n---\n\n".join(p for p in parts if p.strip())


def _get_chroma_singleton() -> ChromaRAGTool:
    global _chroma_singleton
    with _chroma_singleton_lock:
        if _chroma_singleton is None:
            print("[ChromaRAG TRACE] lazy init ChromaRAGTool (in-process singleton)", flush=True)
            _chroma_singleton = ChromaRAGTool()
        return _chroma_singleton


class ChromaRAGPublic:
    """어떤 스레드에서든 동일 인터페이스. Chroma는 싱글톤 + Lock으로 직렬화."""

    def search(self, query: str, top_k: int = RAG_TOP_K, session_context: str = "", wants_depth: bool = False) -> str:
        if _vector_search_effective_disabled():
            print("[ChromaRAG TRACE] vector search skipped (disabled), jsonl only", flush=True)
            fb = _fallback_rag_from_jsonl_tail(query=query, max_papers=max(1, top_k))
            return fb if fb.strip() else "관련 문서 없음 (JSONL 큐 비어 있음)"
        return _get_chroma_singleton().search(query, top_k=top_k, session_context=session_context, wants_depth=wants_depth)

    def list_papers(self) -> str:
        return list_stored_papers_text()


_public = ChromaRAGPublic()


def get_chroma_rag_tool() -> ChromaRAGPublic:
    return _public


def warmup_chroma_rag() -> None:
    """부팅 시 1회: in-process 싱글톤 로드(임베딩·PersistentClient)."""
    if _env_chroma_vector_force_disabled():
        print("[ChromaRAG TRACE] warmup: CHROMA_VECTOR_DISABLED → Chroma 로드 생략", flush=True)
        return
    print("[ChromaRAG TRACE] warmup: in-process Chroma singleton", flush=True)
    _get_chroma_singleton()
    print("[ChromaRAG TRACE] warmup: Chroma singleton OK", flush=True)


def reset_chroma_rag_singleton_for_tests() -> None:
    """pytest 등에서만 확장."""
    global _chroma_singleton
    with _chroma_singleton_lock:
        _chroma_singleton = None


def list_stored_papers_text() -> str:
    """raw_data_queue/crawled_papers.jsonl 기준 고유 paper_id·title (Chroma/임베딩 로드 없음)."""
    try:
        raw_path = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"
        if not raw_path.exists():
            return "저장된 논문이 없습니다."
        seen: set[str] = set()
        lines: list[str] = []
        with raw_path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                    pid = d.get("paper_id", "")
                    title = d.get("title", "")
                    if pid and pid not in seen:
                        seen.add(pid)
                        lines.append(f"- {pid}: {title}")
                except json.JSONDecodeError:
                    continue
        return "\n".join(lines) if lines else "저장된 논문이 없습니다."
    except Exception as e:
        return f"목록 조회 오류: {e}"


class ChromaRAGTool:
    """in-process Chroma. ``_db_lock``으로 ``collection.query`` 직렬화."""

    def __init__(self, db_path: str | None = None, collection_name: str = COLLECTION_NAME):
        raw = db_path if db_path is not None else str(CHROMA_DB_DIR)
        path = raw if Path(raw).is_absolute() else str((PROJECT_ROOT / Path(raw)).resolve())
        _log.debug("ChromaRAGTool.__init__: SentenceTransformerEmbeddingFunction start")
        print("[ChromaRAG TRACE] __init__ embedding_fn BEGIN", flush=True)
        self._embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True
        )
        _log.debug("ChromaRAGTool.__init__: PersistentClient start path=%s", path)
        print("[ChromaRAG TRACE] __init__ PersistentClient BEGIN", flush=True)
        self._client = chromadb.PersistentClient(path=path, settings=Settings(anonymized_telemetry=False))
        print("[ChromaRAG TRACE] __init__ get_collection BEGIN", flush=True)
        self._collection = self._client.get_collection(
            name=collection_name, embedding_function=self._embedding_fn
        )
        _log.debug("ChromaRAGTool.__init__: done collection=%s", collection_name)
        print("[ChromaRAG TRACE] __init__ get_collection END", flush=True)
        self._db_lock = threading.Lock()

    def _strip_urls(self, query: str) -> str:
        return _strip_urls_text(query)

    def _extract_paper_title(self, query: str) -> str:
        return _extract_paper_title_text(query)

    def _rewrite_query(self, query: str, session_context: str) -> str:
        return _rewrite_rag_query(query, session_context)

    def _fetch_depth_chunks(
        self, paper_id: str, *, max_chunks: int = 15, max_chars: int = 6000
    ) -> tuple[list[str], list[dict[str, str]]]:
        """paper_id로 Chroma에서 핵심 청크를 추가 조회 (wants_depth용)."""
        try:
            with self._db_lock:
                extra = self._collection.get(
                    where={"paper_id": paper_id},
                    include=["documents", "metadatas"],
                )
            e_docs = extra.get("documents") or []
            e_metas = extra.get("metadatas") or []
            kept_docs: list[str] = []
            kept_metas: list[dict[str, str]] = []
            total = 0
            skip_patterns = ("Table ", "---|", "picture", "intentionally omitted")
            for doc, meta in zip(e_docs, e_metas):
                d = doc if isinstance(doc, str) else str(doc)
                if len(d) < 30 or any(p in d[:60] for p in skip_patterns):
                    continue
                if total + len(d) > max_chars:
                    break
                kept_docs.append(d)
                kept_metas.append(
                    {str(k): ("" if v is None else str(v)) for k, v in (meta or {}).items()}
                    if isinstance(meta, dict)
                    else {}
                )
                total += len(d)
                if len(kept_docs) >= max_chunks:
                    break
            print(
                f"[ChromaRAG TRACE] depth chunks: pid={paper_id} fetched={len(e_docs)} kept={len(kept_docs)} chars={total}",
                flush=True,
            )
            return kept_docs, kept_metas
        except Exception as exc:
            print(f"[ChromaRAG TRACE] depth chunks fetch failed: {exc}", flush=True)
            return [], []

    def search(self, query: str, top_k: int = RAG_TOP_K, session_context: str = "", wants_depth: bool = False) -> str:
        if _vector_search_effective_disabled():
            fb = _fallback_rag_from_jsonl_tail(query=query, max_papers=max(1, top_k))
            return fb if fb.strip() else "관련 문서 없음 (JSONL 큐 비어 있음)"
        if is_chroma_write_locked():
            print("[ChromaRAG TRACE] chroma_write_lock active → JSONL fallback", flush=True)
            fb = _fallback_rag_from_jsonl_tail(query=query, max_papers=max(1, top_k))
            return fb if fb.strip() else "관련 문서 없음 (백필 진행 중, 잠시 후 재시도)"
        original_query = query
        if session_context:
            _log.debug("ChromaRAGTool.search: _rewrite_query (sync LLM) may run")
            print("[ChromaRAG TRACE] search rewrite_query branch", flush=True)
            rewritten = self._rewrite_query(query, session_context)
            if rewritten and len(rewritten) >= 4 and not rewritten.strip().startswith("<"):
                query = rewritten
            else:
                print(
                    f"[ChromaRAG TRACE] rewrite rejected (garbage): {rewritten!r:.40}, keeping original",
                    flush=True,
                )
        query = self._strip_urls(query)
        if not query.strip():
            return "관련 문서 없음"
        query_for_rerank = query
        search_query = self._extract_paper_title(query)
        search_query = re.sub(r"[()（）]", " ", search_query).strip()
        search_query = re.sub(r"\s{2,}", " ", search_query)
        try:
            _log.debug(
                "ChromaRAGTool.search: before collection.query top_k=%s q_preview=%r",
                top_k,
                search_query[:160],
            )
            # CE 켜짐: 넓게 가져와 재정렬. CE 끔: 논문 집계 전 청크 후보 풀 (CHROMA_FETCH_MULTIPLIER / MIN).
            _fetch_n = int(max(float(top_k) * CHROMA_FETCH_MULTIPLIER, float(CHROMA_FETCH_MIN)))
            if CHROMA_CROSS_ENCODER_RERANK:
                _fetch_n = max(_fetch_n, int(max(float(top_k) * 6.0, 30.0)))
            print(
                f"[ChromaRAG TRACE] search BEFORE multi-query pool top_k={top_k} fetch_n={_fetch_n} "
                f"ce_rerank={'on' if CHROMA_CROSS_ENCODER_RERANK else 'off'} qlen={len(search_query)}",
                flush=True,
            )
            docs_clean, metas_clean, dists_clean, bm25_pid_scores, first_chroma_raw, pre_cs = (
                _hybrid_retrieve_candidate_pool(
                    self._collection,
                    search_query,
                    fetch_n=_fetch_n,
                    lock=self._db_lock,
                )
            )
            _retrieval_pool_len = len(docs_clean)
            if first_chroma_raw is not None:
                _log_rag_debug_chroma_raw(
                    user_query=original_query,
                    vector_query=search_query,
                    top_k=top_k,
                    results=first_chroma_raw,
                )
            print("[ChromaRAG TRACE] search AFTER multi-query pool", flush=True)

            # ── Cross-encoder rerank (기본 끔): 대형 코퍼스에서는 하이브리드만 최종 순서로 사용 ──
            _post_hybrid_cap = max(top_k * 2, 10)
            if CHROMA_CROSS_ENCODER_RERANK:
                docs_clean, metas_clean, dists_clean = _cross_encoder_rerank(
                    search_query,
                    docs_clean,
                    metas_clean,
                    dists_clean,
                    top_k=_post_hybrid_cap,
                )
            else:
                # CE 끔: 청크 단위 조기 cap 하지 않음 → 논문별 MAX 집계에 벡터 후보 전부 반영
                print(
                    "[ChromaRAG TRACE] cross-encoder rerank skipped; "
                    "paper-level MAX aggregation will apply",
                    flush=True,
                )

            # Title-first inject: 원본 쿼리와 search_query 모두로 제목 매칭 시도
            title_pid = _find_paper_by_title(original_query) or _find_paper_by_title(search_query)
            if title_pid:
                existing_pids = {(m.get("paper_id") or "").strip() for m in metas_clean}
                if title_pid not in existing_pids:
                    print(
                        f"[ChromaRAG TRACE] title-first inject: {title_pid} not in vector results, fetching by metadata",
                        flush=True,
                    )
                    inject_docs, inject_metas = self._fetch_depth_chunks(title_pid)
                    if inject_docs:
                        inject_dists = [None] * len(inject_docs)
                        old_n = len(docs_clean)
                        docs_clean = inject_docs + docs_clean
                        metas_clean = inject_metas + metas_clean
                        if dists_clean is None:
                            dists_clean = inject_dists + [None] * old_n
                        else:
                            dists_clean = inject_dists + dists_clean
                elif (metas_clean[0].get("paper_id") or "").strip() != title_pid:
                    # 결과에 있지만 #0이 아니면 승격
                    for idx_t, m_t in enumerate(metas_clean):
                        if (m_t.get("paper_id") or "").strip() == title_pid:
                            print(
                                f"[ChromaRAG TRACE] title-first promote: #{idx_t} -> #0",
                                flush=True,
                            )
                            if dists_clean is not None and len(dists_clean) != len(docs_clean):
                                dists_clean = None
                            docs_clean = [docs_clean[idx_t]] + docs_clean[:idx_t] + docs_clean[idx_t + 1:]
                            metas_clean = [metas_clean[idx_t]] + metas_clean[:idx_t] + metas_clean[idx_t + 1:]
                            if dists_clean is not None:
                                dists_clean = (
                                    [dists_clean[idx_t]]
                                    + dists_clean[:idx_t]
                                    + dists_clean[idx_t + 1 :]
                                )
                            break

            if wants_depth and docs_clean and metas_clean:
                top_pid = (metas_clean[0].get("paper_id") or "").strip()
                if top_pid:
                    depth_docs, depth_metas = self._fetch_depth_chunks(top_pid)
                    if depth_docs:
                        existing_texts = set(d[:80] for d in docs_clean)
                        for dd, dm in zip(depth_docs, depth_metas):
                            if dd[:80] not in existing_texts:
                                docs_clean.append(dd)
                                metas_clean.append(dm)
                                if dists_clean is not None:
                                    dists_clean.append(None)

            if not wants_depth:
                chroma_pids = {
                    (m.get("paper_id") or "").strip()
                    for m in metas_clean
                    if (m.get("paper_id") or "").strip()
                }
                supplements = _keyword_supplement_from_jsonl(
                    query_for_rerank, chroma_pids, max_extra=5
                )
                for sdoc, smeta in supplements:
                    docs_clean.append(sdoc)
                    metas_clean.append(smeta)
                    if dists_clean is not None:
                        dists_clean.append(None)

            if not CHROMA_CROSS_ENCODER_RERANK and docs_clean:
                _tbq = (original_query.strip() or search_query.strip())
                if pre_cs is not None and len(docs_clean) == _retrieval_pool_len:
                    _cs = pre_cs
                else:
                    if len(docs_clean) != _retrieval_pool_len:
                        try:
                            bm25 = get_bm25_searcher()
                            bq = expand_query_for_bm25(search_query)
                            pool_pids = {
                                _normalize_pid((m.get("paper_id") or "").strip())
                                for m in metas_clean
                                if (m.get("paper_id") or "").strip()
                            }
                            if pool_pids:
                                bm25_pid_scores = bm25.paper_bm25_scores_bulk(bq, pool_pids)
                        except Exception as exc:
                            print(f"[ChromaRAG TRACE] BM25 bulk (post-inject) skipped: {exc}", flush=True)
                    _cs = _compute_hybrid_chunk_scores(
                        metas_clean,
                        dists_clean,
                        bm25_pid_scores,
                        title_boost_query=_tbq,
                    )
                docs_clean, metas_clean, dists_clean = _paper_max_one_chunk_per_paper(
                    docs_clean,
                    metas_clean,
                    dists_clean,
                    _cs,
                    top_k_papers=max(top_k, 1),
                    title_query=_tbq,
                    chunks_per_paper_out=HYBRID_CHUNKS_PER_PAPER,
                    light_rerank_query=_tbq,
                )

            hits = _format_chroma_hits(docs_clean, metas_clean, dists_clean)
            _clear_vector_search_disabled()
            return hits
        except Exception as e:
            _log.warning("ChromaRAGTool.search failed: %s", e)
            print(f"[ChromaRAG TRACE] search exception, jsonl fallback: {e}", flush=True)
            _set_vector_search_disabled_for_process()
            fb = _fallback_rag_from_jsonl_tail(query=query_for_rerank, max_papers=max(1, top_k))
            if fb.strip():
                return fb
            return f"검색 오류: {e}"

    def list_papers(self) -> str:
        return list_stored_papers_text()
