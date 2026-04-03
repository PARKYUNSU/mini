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

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.messages import HumanMessage, SystemMessage

from core.config.agent_config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL, PROJECT_ROOT, RAG_TOP_K
from core.llm.agent_llm import get_rag_query_rewrite_llm

# 레거시·문서 혼동 방지: subprocess(spawn) Chroma 경로는 비활성화
os.environ["CHROMA_SUBPROCESS"] = "0"

_log = logging.getLogger(__name__)

_SEARCH_TIMEOUT_SEC = 600.0

# 한 번 Chroma query가 프로세스 단위로 반복 실패하면, 봇 재시작 전까지 벡터 검색 생략
_VECTOR_CIRCUIT_COOLDOWN_SEC: float = 600.0
_vector_search_disabled_until: float = 0.0
_vector_search_retry_used: bool = False
_vector_search_disabled_lock = threading.Lock()

_chroma_singleton: ChromaRAGTool | None = None
_chroma_singleton_lock = threading.Lock()


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
    vague = ("그거", "그게", "그것", "그건", "이거", "저거", "이게", "저게", "더 자세히", "자세히 설명")
    if not any(v in query for v in vague):
        return query
    try:
        llm = get_rag_query_rewrite_llm()
        resp = llm.invoke(
            [
                SystemMessage(
                    content="대화 맥락을 보고 사용자가 '그거', '더 자세히' 등으로 물어본 대상의 구체적 검색어를 1문장으로만 출력. 검색어만. 사고 과정 출력 금지."
                ),
                HumanMessage(content=f"[대화]\n{session_context[:800]}\n\n[현재 질문]\n{query}\n\n검색어:"),
            ]
        )
        rewritten = (resp.content or query).strip()
        return rewritten[:200] if rewritten else query
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


def _fallback_rag_from_jsonl_tail(*, query: str, max_papers: int = 2, max_chars: int = 6500) -> str:
    """Chroma 실패 시 JSONL 후보를 토큰 겹침 기반으로 재정렬 후 상위 문서 텍스트만 사용."""
    raw_path = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"
    if not raw_path.exists():
        return ""
    try:
        with raw_path.open(encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return ""
    candidate_pool_size = max(20, max_papers * 4)
    candidates: list[dict] = []
    for line in reversed(lines):
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


def _format_chroma_hits(docs: list[str], metas: list[dict[str, str]]) -> str:
    if not docs:
        return "관련 문서 없음"
    parts: list[str] = []
    for doc, meta in zip(docs, metas):
        pub = _published_line_from_record(meta)
        pid = meta.get("paper_id", "")
        title = meta.get("title", "")
        header = f"[{pid}] {title}\n" if (pid or title) else ""
        body = doc[:1200] if doc else ""
        prefix = f"{pub}\n" if pub else ""
        block = f"{prefix}{header}{body}".strip() if body else f"{prefix}{header}".strip()
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

    def search(self, query: str, top_k: int = RAG_TOP_K, session_context: str = "") -> str:
        if _vector_search_effective_disabled():
            print("[ChromaRAG TRACE] vector search skipped (disabled), jsonl only", flush=True)
            fb = _fallback_rag_from_jsonl_tail(query=query, max_papers=max(1, top_k))
            return fb if fb.strip() else "관련 문서 없음 (JSONL 큐 비어 있음)"
        return _get_chroma_singleton().search(query, top_k=top_k, session_context=session_context)

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

    def __init__(self, db_path: str = CHROMA_DB_PATH, collection_name: str = COLLECTION_NAME):
        path = db_path if Path(db_path).is_absolute() else str((PROJECT_ROOT / Path(db_path)).resolve())
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

    def search(self, query: str, top_k: int = RAG_TOP_K, session_context: str = "") -> str:
        if _vector_search_effective_disabled():
            fb = _fallback_rag_from_jsonl_tail(query=query, max_papers=max(1, top_k))
            return fb if fb.strip() else "관련 문서 없음 (JSONL 큐 비어 있음)"
        if session_context:
            _log.debug("ChromaRAGTool.search: _rewrite_query (sync LLM) may run")
            print("[ChromaRAG TRACE] search rewrite_query branch", flush=True)
            query = self._rewrite_query(query, session_context)
        query = self._strip_urls(query)
        if not query.strip():
            return "관련 문서 없음"
        query_for_rerank = query
        search_query = self._extract_paper_title(query)
        try:
            _log.debug(
                "ChromaRAGTool.search: before collection.query top_k=%s q_preview=%r",
                top_k,
                search_query[:160],
            )
            print(
                f"[ChromaRAG TRACE] search BEFORE query (sync, _db_lock) top_k={top_k} qlen={len(search_query)}",
                flush=True,
            )
            with self._db_lock:
                results = self._collection.query(
                    query_texts=[search_query], n_results=top_k, include=["documents", "metadatas"]
                )
            print("[ChromaRAG TRACE] search AFTER query", flush=True)
            docs = results["documents"][0] if results["documents"] else []
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
            hits = _format_chroma_hits(
                [d if isinstance(d, str) else str(d) for d in docs],
                [
                    {str(k): ("" if v is None else str(v)) for k, v in (m or {}).items()}
                    if isinstance(m, dict)
                    else {}
                    for m in metas
                ],
            )
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
