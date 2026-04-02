"""논문 RAG (ChromaDB + 임베딩). agent_bot과 분리해 테스트·재사용 용이.

동기(sync)만 사용(asyncio 미사용).

macOS(Apple Silicon) 등에서 부모 프로세스의 torch/LangGraph·Chroma Rust가 한 프로세스에 있으면
`collection.query`에서 Segmentation fault가 날 수 있다. 이 경우 **기본(darwin)** 으로
`multiprocessing` **spawn** 자식 프로세스만 Chroma+임베딩을 로드하고 `query`를 수행한다.

- ``CHROMA_SUBPROCESS=1`` : 강제 spawn 경로
- ``CHROMA_SUBPROCESS=0`` : 기존처럼 owner 스레드 + in-process Chroma (Linux 등)

그 외: **chroma-rag-owner** 스레드 직렬화 + ``ChromaRAGTool._db_lock``.
"""

from __future__ import annotations

import json
import logging
import multiprocessing as mp
import os
import queue
import sys
import threading
import time
from concurrent.futures import Future
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.messages import HumanMessage, SystemMessage

from agent_config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL, PROJECT_ROOT, RAG_TOP_K
from agent_llm import get_rag_query_rewrite_llm

_PROJECT_ROOT = Path(__file__).resolve().parent

_log = logging.getLogger(__name__)

_CHROMA_SHUTDOWN = object()
_SEARCH_TIMEOUT_SEC = 600.0


def _use_subprocess_chroma() -> bool:
    v = (os.environ.get("CHROMA_SUBPROCESS") or "").strip().lower()
    if v in ("0", "false", "no", "off"):
        return False
    if v in ("1", "true", "yes", "on"):
        return True
    return sys.platform == "darwin"


def _abs_chroma_db_path() -> str:
    p = Path(CHROMA_DB_PATH)
    if p.is_absolute():
        return str(p.resolve())
    return str((PROJECT_ROOT / p).resolve())


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


def _format_chroma_hits(docs: list[str], metas: list[dict[str, str]]) -> str:
    if not docs:
        return "관련 문서 없음"
    parts: list[str] = []
    for doc, meta in zip(docs, metas):
        pid = meta.get("paper_id", "")
        title = meta.get("title", "")
        header = f"[{pid}] {title}\n" if (pid or title) else ""
        parts.append(f"{header}{doc[:800]}" if doc else header)
    return "\n\n---\n\n".join(p for p in parts if p.strip())


def _chroma_spawn_worker(
    task_q: Any,
    result_q: Any,
    db_path: str,
    collection_name: str,
    embedding_model: str,
) -> None:
    """spawn 자식 전용: Chroma·임베딩·query만 로드 (부모와 네이티브 스택 분리)."""
    import chromadb as _chromadb
    from chromadb.config import Settings as _Settings
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction as _STEF

    print("[ChromaRAG TRACE] spawn child: loading embedding + PersistentClient...", flush=True)
    ef = _STEF(model_name=embedding_model, device="cpu", normalize_embeddings=True)
    client = _chromadb.PersistentClient(path=db_path, settings=_Settings(anonymized_telemetry=False))
    col = client.get_collection(name=collection_name, embedding_function=ef)
    print("[ChromaRAG TRACE] spawn child: ready for query", flush=True)

    while True:
        msg = task_q.get()
        if msg is None:
            break
        rid: int
        op: str
        payload: Any
        rid, op, payload = msg
        if op == "ping":
            result_q.put((rid, "ok", None))
            continue
        if op == "query":
            sq, top_k = payload
            try:
                res = col.query(
                    query_texts=[sq], n_results=top_k, include=["documents", "metadatas"]
                )
                docs = res["documents"][0] if res["documents"] else []
                metas_raw = res["metadatas"][0] if res.get("metadatas") else []
                docs_out = [d if isinstance(d, str) else str(d) for d in docs]
                safe_metas: list[dict[str, str]] = []
                for m in metas_raw:
                    d = m if isinstance(m, dict) else {}
                    safe_metas.append({str(k): ("" if v is None else str(v)) for k, v in d.items()})
                result_q.put((rid, "ok", {"documents": docs_out, "metadatas": safe_metas}))
            except Exception as e:
                result_q.put((rid, "err", str(e)))


class _SpawnChromaRunner:
    """부모 쪽: 요청 직렬화 + spawn 자식 1개 유지(죽으면 한 번 재기동 시도)."""

    def __init__(self) -> None:
        self._ctx = mp.get_context("spawn")
        self._task_q: Any = self._ctx.Queue()
        self._result_q: Any = self._ctx.Queue()
        self._proc: mp.Process | None = None
        self._plock = threading.Lock()
        self._seq = 0

    def _start_proc(self) -> None:
        if self._proc is not None and self._proc.is_alive():
            return
        print("[ChromaRAG TRACE] spawning chroma-rag child (spawn)...", flush=True)
        self._proc = self._ctx.Process(
            target=_chroma_spawn_worker,
            args=(self._task_q, self._result_q, _abs_chroma_db_path(), COLLECTION_NAME, EMBEDDING_MODEL),
            name="chroma-rag-spawn",
            daemon=True,
        )
        self._proc.start()
        time.sleep(0.4)
        if not self._proc.is_alive():
            code = self._proc.exitcode
            self._proc = None
            raise RuntimeError(f"Chroma spawn 자식이 즉시 종료됨 (exit={code})")

    def _drain_stale_results(self) -> None:
        while True:
            try:
                self._result_q.get_nowait()
            except queue.Empty:
                break

    def _request(self, op: str, payload: Any, *, timeout: float = _SEARCH_TIMEOUT_SEC) -> Any:
        with self._plock:
            for attempt in range(2):
                self._drain_stale_results()
                self._start_proc()
                assert self._proc is not None
                self._seq += 1
                rid = self._seq
                self._task_q.put((rid, op, payload))
                deadline = time.monotonic() + timeout
                while True:
                    if not self._proc.is_alive():
                        self._proc = None
                        if attempt == 0:
                            break
                        raise RuntimeError(
                            "Chroma spawn 프로세스가 응답 중 종료되었습니다(세그폴트 가능). 봇을 재시작하거나 CHROMA_SUBPROCESS=0으로 시도해 보세요."
                        )
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("Chroma subprocess")
                    try:
                        got = self._result_q.get(timeout=min(remaining, 5.0))
                    except queue.Empty:
                        continue
                    gr, status, data = got
                    if gr != rid:
                        continue
                    if status == "err":
                        raise RuntimeError(data)
                    return data
            raise RuntimeError("Chroma spawn 자식을 시작하지 못했습니다.")

    def ping(self) -> None:
        self._request("ping", None, timeout=_SEARCH_TIMEOUT_SEC)

    def query_raw(self, search_query: str, top_k: int) -> dict[str, Any]:
        return self._request("query", (search_query, top_k), timeout=_SEARCH_TIMEOUT_SEC)


_spawn_runner: _SpawnChromaRunner | None = None
_spawn_runner_lock = threading.Lock()


def _get_spawn_runner() -> _SpawnChromaRunner:
    global _spawn_runner
    with _spawn_runner_lock:
        if _spawn_runner is None:
            _spawn_runner = _SpawnChromaRunner()
        return _spawn_runner


def _search_via_subprocess(query: str, top_k: int, session_context: str) -> str:
    if session_context:
        _log.debug("ChromaRAG subprocess path: _rewrite_rag_query (parent LLM)")
        print("[ChromaRAG TRACE] search rewrite_query branch (parent thread)", flush=True)
        query = _rewrite_rag_query(query, session_context)
    query = _strip_urls_text(query)
    if not query.strip():
        return "관련 문서 없음"
    search_query = _extract_paper_title_text(query)
    print(
        f"[ChromaRAG TRACE] subprocess query (spawn child) top_k={top_k} qlen={len(search_query)}",
        flush=True,
    )
    try:
        raw = _get_spawn_runner().query_raw(search_query, top_k)
        docs = raw.get("documents") or []
        metas = raw.get("metadatas") or []
        return _format_chroma_hits(docs, metas)
    except Exception as e:
        _log.debug("subprocess search failed: %s", e)
        return f"검색 오류: {e}"


class _ChromaOwnerLoop:
    """ChromaRAGTool 인스턴스를 이 스레드에서만 생성·쿼리한다 (CHROMA_SUBPROCESS=0 시)."""

    def __init__(self) -> None:
        self._q: queue.Queue = queue.Queue()
        self._thr: threading.Thread | None = None
        self._start_lock = threading.Lock()

    def _loop(self) -> None:
        tool: ChromaRAGTool | None = None
        while True:
            item = self._q.get()
            if item is _CHROMA_SHUTDOWN:
                break
            fut: Future
            op: str
            args: tuple
            kwargs: dict
            fut, op, args, kwargs = item
            try:
                if op == "_init":
                    if tool is None:
                        _log.debug("chroma owner thread: constructing ChromaRAGTool")
                        print("[ChromaRAG TRACE] owner thread: constructing ChromaRAGTool", flush=True)
                        tool = ChromaRAGTool()
                    fut.set_result(None)
                elif op == "search":
                    if tool is None:
                        tool = ChromaRAGTool()
                    fut.set_result(tool.search(*args, **kwargs))
                else:
                    fut.set_exception(RuntimeError(f"unknown chroma op: {op}"))
            except BaseException as e:
                if not fut.done():
                    fut.set_exception(e)
            finally:
                self._q.task_done()

    def _ensure_started(self) -> None:
        with self._start_lock:
            if self._thr is None or not self._thr.is_alive():
                self._thr = threading.Thread(
                    target=self._loop, name="chroma-rag-owner", daemon=False
                )
                self._thr.start()

    def submit(self, op: str, *args, **kwargs) -> Future:
        self._ensure_started()
        fut: Future = Future()
        self._q.put((fut, op, args, kwargs))
        return fut

    def warmup(self) -> None:
        self.submit("_init").result(timeout=_SEARCH_TIMEOUT_SEC)


_owner = _ChromaOwnerLoop()


class ChromaRAGPublic:
    """어떤 스레드에서든 동일 인터페이스. darwin 기본은 spawn 자식에서 Chroma query."""

    def search(self, query: str, top_k: int = RAG_TOP_K, session_context: str = "") -> str:
        if _use_subprocess_chroma():
            return _search_via_subprocess(query, top_k, session_context)
        return _owner.submit("search", query, top_k=top_k, session_context=session_context).result(
            timeout=_SEARCH_TIMEOUT_SEC
        )

    def list_papers(self) -> str:
        return list_stored_papers_text()


_public = ChromaRAGPublic()


def get_chroma_rag_tool() -> ChromaRAGPublic:
    return _public


def warmup_chroma_rag() -> None:
    """부팅 시 1회: spawn 자식에 Chroma 로드 또는 owner 스레드에 in-process 로드."""
    if _use_subprocess_chroma():
        print("[ChromaRAG TRACE] warmup: spawn child ping", flush=True)
        _get_spawn_runner().ping()
        print("[ChromaRAG TRACE] warmup: spawn child OK", flush=True)
        return
    _owner.warmup()


def reset_chroma_rag_singleton_for_tests() -> None:
    """pytest 등에서만 확장."""
    pass


def list_stored_papers_text() -> str:
    """raw_data_queue/crawled_papers.jsonl 기준 고유 paper_id·title (Chroma/임베딩 로드 없음)."""
    try:
        raw_path = _PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"
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
    """in-process Chroma (CHROMA_SUBPROCESS=0 또는 직접 인스턴스화 시). owner 스레드에서만 쓸 것."""

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
        if _use_subprocess_chroma():
            return _search_via_subprocess(query, top_k, session_context)
        if session_context:
            _log.debug("ChromaRAGTool.search: _rewrite_query (sync LLM) may run")
            print("[ChromaRAG TRACE] search rewrite_query branch", flush=True)
            query = self._rewrite_query(query, session_context)
        query = self._strip_urls(query)
        if not query.strip():
            return "관련 문서 없음"
        search_query = self._extract_paper_title(query)
        try:
            _log.debug(
                "ChromaRAGTool.search: before collection.query top_k=%s q_preview=%r",
                top_k,
                search_query[:160],
            )
            print(
                f"[ChromaRAG TRACE] search BEFORE query (sync) top_k={top_k} qlen={len(search_query)}",
                flush=True,
            )
            with self._db_lock:
                results = self._collection.query(
                    query_texts=[search_query], n_results=top_k, include=["documents", "metadatas"]
                )
            print("[ChromaRAG TRACE] search AFTER query", flush=True)
            docs = results["documents"][0] if results["documents"] else []
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
            return _format_chroma_hits(
                [d if isinstance(d, str) else str(d) for d in docs],
                [
                    {str(k): ("" if v is None else str(v)) for k, v in (m or {}).items()}
                    if isinstance(m, dict)
                    else {}
                    for m in metas
                ],
            )
        except Exception as e:
            _log.debug("ChromaRAGTool.search: exception %s", e)
            return f"검색 오류: {e}"

    def list_papers(self) -> str:
        return list_stored_papers_text()
