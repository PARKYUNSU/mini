"""BM25 인덱스 모듈 — JSONL 논문 title+abstract 기반 키워드 검색.

Hybrid Retrieval 파이프라인의 BM25 컴포넌트.
벡터 검색이 놓치는 키워드 매칭(CRAG, Self-RAG, DPR 등)을 보완한다.

사용법:
    from core.rag.bm25_index import get_bm25_searcher
    searcher = get_bm25_searcher()
    results = searcher.search("CRAG corrective retrieval", top_k=10)
"""

from __future__ import annotations

import json
import logging
import re
import threading
import time
from pathlib import Path
from typing import Any

from core.config.agent_config import HYBRID_BM25_WEIGHT, HYBRID_VECTOR_WEIGHT, PROJECT_ROOT

_log = logging.getLogger(__name__)

_TOKEN_RE = re.compile(r"[^0-9A-Za-z가-힣]+")

# Hybrid retrieval 가중치: agent_config.HYBRID_*_WEIGHT (기본 0.55 / 0.45)

# 하이픈 복합어 → 개별 토큰 + 결합 토큰 모두 생성
_HYPHEN_RE = re.compile(r"(\w+)-(\w+)")


def _tokenize(text: str) -> list[str]:
    """토크나이저: 소문자 + 비알파벳 분리, 하이픈 복합어 확장, 2자 이상만."""
    s = (text or "").lower().strip()
    # 하이픈 복합어 확장: "re-ranking" → "re ranking reranking"
    expanded = _HYPHEN_RE.sub(r"\1 \2 \1\2", s)
    return [t for t in _TOKEN_RE.split(expanded) if len(t) >= 2]


def _normalize_pid(pid: str) -> str:
    """paper_id에서 버전 접미사 제거: 2312.10997v5 → 2312.10997"""
    s = (pid or "").strip()
    if "v" in s:
        base, suffix = s.rsplit("v", 1)
        if suffix.isdigit() and base.replace(".", "").isdigit():
            return base
    return s


class BM25Searcher:
    """JSONL 기반 BM25 검색기. title + abstract를 인덱싱."""

    def __init__(self):
        self._papers: list[dict] = []  # [{paper_id, title, abstract, ...}]
        self._corpus_tokens: list[list[str]] = []
        self._bm25: Any = None  # rank_bm25.BM25Okapi (lazy import in _load)
        self._pid_to_idx: dict[str, int] = {}  # paper_id → index
        self._loaded = False
        self._lock = threading.Lock()

    def _load(self) -> None:
        """JSONL에서 논문 메타데이터 로드 및 BM25 인덱스 구축."""
        if self._loaded:
            return

        t0 = time.time()
        processed_dir = PROJECT_ROOT / "raw_data_queue" / "processed"
        main_jsonl = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"

        papers_by_pid: dict[str, dict] = {}

        # processed/ 디렉토리의 모든 JSONL 파일 로드
        jsonl_files: list[Path] = []
        if processed_dir.exists():
            jsonl_files = sorted(processed_dir.glob("crawled_papers*.jsonl"))
        if main_jsonl.exists():
            jsonl_files.append(main_jsonl)

        for fpath in jsonl_files:
            try:
                with fpath.open(encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            d = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        pid = _normalize_pid((d.get("paper_id") or "").strip())
                        if not pid:
                            continue
                        if pid not in papers_by_pid:
                            papers_by_pid[pid] = d
            except OSError:
                continue

        # 인덱스 구축
        self._papers = []
        self._corpus_tokens = []
        self._pid_to_idx = {}

        for pid, d in papers_by_pid.items():
            title = (d.get("title") or "").strip()
            abstract = (
                d.get("abstract") or d.get("summary") or ""
            ).strip()
            # content를 더 넓게 포함 (키워드 커버리지 확대)
            content_head = (d.get("content") or d.get("text") or "").strip()[:3000]

            # title 3x 가중 + abstract 전체 + content 앞부분
            combined = f"{title} {title} {title} {abstract} {content_head}"
            tokens = _tokenize(combined)
            if not tokens:
                continue

            idx = len(self._papers)
            self._papers.append({
                "paper_id": pid,
                "title": title,
                "abstract": abstract[:500],
            })
            self._corpus_tokens.append(tokens)
            self._pid_to_idx[pid] = idx

        if self._corpus_tokens:
            from rank_bm25 import BM25Okapi

            self._bm25 = BM25Okapi(self._corpus_tokens)

        elapsed = time.time() - t0
        self._loaded = True
        print(
            f"[BM25] 인덱스 구축 완료: {len(self._papers):,}편 논문, {elapsed:.1f}초",
            flush=True,
        )

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        """BM25 검색. Returns list of {paper_id, title, score, rank}.

        Args:
            query: 검색 쿼리
            top_k: 반환할 최대 논문 수

        Returns:
            [{paper_id, title, bm25_score}, ...]
        """
        with self._lock:
            if not self._loaded:
                self._load()

        if not self._bm25 or not self._papers:
            return []

        tokens = _tokenize(query)
        if not tokens:
            return []

        scores = self._bm25.get_scores(tokens)

        # top_k 인덱스 추출
        top_indices = sorted(range(len(scores)), key=lambda i: -scores[i])[:top_k]

        results = []
        for idx in top_indices:
            if scores[idx] <= 0:
                continue
            paper = self._papers[idx]
            results.append({
                "paper_id": paper["paper_id"],
                "title": paper["title"],
                "bm25_score": float(scores[idx]),
            })

        return results

    def get_paper_score(self, query: str, paper_id: str) -> float:
        """특정 paper_id의 BM25 점수 반환."""
        with self._lock:
            if not self._loaded:
                self._load()

        if not self._bm25:
            return 0.0

        pid = _normalize_pid(paper_id)
        idx = self._pid_to_idx.get(pid)
        if idx is None:
            return 0.0

        tokens = _tokenize(query)
        if not tokens:
            return 0.0

        scores = self._bm25.get_scores(tokens)
        return float(scores[idx]) if idx < len(scores) else 0.0

    def paper_bm25_scores_bulk(self, query: str, paper_ids: set[str]) -> dict[str, float]:
        """후보 풀에 등장하는 논문들에 대한 BM25 원시 점수(Okapi).

        ``get_scores``를 **한 번만** 호출해 인덱스 전체 점수 벡터를 얻고,
        ``paper_ids``에 해당하는 행만 꺼낸다. (상위 M개 히트에만 키가 있을 때
        벡터-only 풀의 나머지 논문이 전부 0으로 남는 문제를 막는다.)
        """
        with self._lock:
            if not self._loaded:
                self._load()

        out: dict[str, float] = {}
        if not self._bm25 or not paper_ids:
            return out

        tokens = _tokenize(query)
        if not tokens:
            return out

        scores = self._bm25.get_scores(tokens)
        for raw in paper_ids:
            s = (raw or "").strip()
            if not s:
                continue
            npid = _normalize_pid(s)
            if not npid:
                continue
            idx = self._pid_to_idx.get(npid)
            if idx is None or idx >= len(scores):
                out[npid] = 0.0
            else:
                out[npid] = max(0.0, float(scores[idx]))
        return out

    @property
    def paper_count(self) -> int:
        with self._lock:
            if not self._loaded:
                self._load()
        return len(self._papers)


# ── Singleton ──
_bm25_searcher: BM25Searcher | None = None
_bm25_lock = threading.Lock()


def get_bm25_searcher() -> BM25Searcher:
    """BM25Searcher 싱글톤 반환."""
    global _bm25_searcher
    if _bm25_searcher is not None:
        return _bm25_searcher
    with _bm25_lock:
        if _bm25_searcher is None:
            _bm25_searcher = BM25Searcher()
        return _bm25_searcher


def invalidate_bm25_searcher() -> None:
    """JSONL 갱신·재인덱싱 후 장시간 실행 프로세스에서 BM25 캐시를 비울 때 호출."""
    global _bm25_searcher
    with _bm25_lock:
        _bm25_searcher = None


def hybrid_merge(
    vector_results: list[dict],
    bm25_results: list[dict],
    *,
    vector_weight: float = HYBRID_VECTOR_WEIGHT,
    bm25_weight: float = HYBRID_BM25_WEIGHT,
    top_k: int = 30,
) -> list[dict]:
    """벡터 검색 결과와 BM25 결과를 score 기반 가중합으로 병합.

    Args:
        vector_results: [{paper_id, doc, meta, distance}, ...]
            distance는 cosine distance (작을수록 유사)
        bm25_results: [{paper_id, title, bm25_score}, ...]
        vector_weight: 벡터 검색 가중치 (기본 0.5)
        bm25_weight: BM25 가중치 (기본 0.5)
        top_k: 최종 반환 수

    Returns:
        [{paper_id, doc, meta, distance, hybrid_score}, ...] 정렬된 리스트
    """
    # 1. 벡터 결과의 distance를 similarity로 변환 (cosine: sim = 1 - dist)
    # 그리고 min-max 정규화
    v_scores: dict[str, float] = {}  # chunk_key → normalized score
    v_items: dict[str, dict] = {}  # chunk_key → full item

    if vector_results:
        raw_sims = []
        for item in vector_results:
            dist = item.get("distance", 0.5)
            if dist is None:
                dist = 0.5
            sim = 1.0 - float(dist)
            raw_sims.append(sim)

        min_sim = min(raw_sims) if raw_sims else 0
        max_sim = max(raw_sims) if raw_sims else 1
        rng = max_sim - min_sim if max_sim > min_sim else 1.0

        for i, item in enumerate(vector_results):
            key = f"v_{i}"
            norm_score = (raw_sims[i] - min_sim) / rng
            v_scores[key] = norm_score
            v_items[key] = item

    # 2. BM25 결과 정규화
    b_scores: dict[str, float] = {}  # paper_id → normalized score
    if bm25_results:
        raw_bm25 = [r["bm25_score"] for r in bm25_results]
        min_b = min(raw_bm25) if raw_bm25 else 0
        max_b = max(raw_bm25) if raw_bm25 else 1
        rng_b = max_b - min_b if max_b > min_b else 1.0
        for r in bm25_results:
            pid = _normalize_pid(r["paper_id"])
            norm = (r["bm25_score"] - min_b) / rng_b
            b_scores[pid] = max(b_scores.get(pid, 0), norm)

    # 3. 벡터 결과에 BM25 보너스 추가
    merged: list[tuple[float, dict]] = []
    for key, item in v_items.items():
        v_norm = v_scores[key]
        pid = _normalize_pid((item.get("meta", {}).get("paper_id") or "").strip())
        b_norm = b_scores.get(pid, 0.0)
        hybrid = vector_weight * v_norm + bm25_weight * b_norm
        item_copy = {**item, "hybrid_score": hybrid}
        merged.append((hybrid, item_copy))

    # 4. BM25에만 있는 논문 추가 (벡터 결과에 없는 것)
    existing_pids = set()
    for _, item in merged:
        pid = _normalize_pid((item.get("meta", {}).get("paper_id") or "").strip())
        if pid:
            existing_pids.add(pid)

    for r in bm25_results:
        pid = _normalize_pid(r["paper_id"])
        if pid not in existing_pids:
            # BM25 only — 벡터 점수 0으로 처리
            hybrid = bm25_weight * b_scores.get(pid, 0.0)
            merged.append((hybrid, {
                "paper_id": pid,
                "title": r.get("title", ""),
                "meta": {"paper_id": pid, "title": r.get("title", "")},
                "doc": "",  # 벡터 결과 없으므로 빈 문서
                "distance": None,
                "hybrid_score": hybrid,
                "bm25_only": True,
            }))
            existing_pids.add(pid)

    # 5. hybrid_score 내림차순 정렬
    merged.sort(key=lambda x: -x[0])

    return [item for _, item in merged[:top_k]]
