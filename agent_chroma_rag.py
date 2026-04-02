"""논문 RAG (ChromaDB + 임베딩). agent_bot과 분리해 테스트·재사용 용이.

동기(sync) API만 사용(asyncio 미사용). macOS 등에서 SentenceTransformer/Chroma 네이티브 스택이
**초기화된 스레드와 다른 스레드**에서 query되면 Segmentation fault가 날 수 있어,
PersistentClient·임베딩·collection.query는 **단일 전용 데몬 스레드**에서만 실행한다.
호출 스레드(텔레그램 ThreadPoolExecutor 등)는 큐로 위임 후 결과만 대기한다.
"""

from __future__ import annotations

import json
import logging
import queue
import threading
from concurrent.futures import Future
from pathlib import Path

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.messages import HumanMessage, SystemMessage

from agent_config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL, RAG_TOP_K
from agent_llm import get_rag_query_rewrite_llm

_PROJECT_ROOT = Path(__file__).resolve().parent

_log = logging.getLogger(__name__)

_CHROMA_SHUTDOWN = object()
_SEARCH_TIMEOUT_SEC = 600.0


class _ChromaOwnerLoop:
    """ChromaRAGTool 인스턴스를 이 스레드에서만 생성·쿼리한다."""

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
                # daemon=False: macOS에서 데몬 스레드에서 torch/onnx 임베딩 후 collection.query 시
                # 세그폴트가 재현되는 경우가 있어 일반 스레드로 둔다(프로세스 종료 시 join 권장).
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
    """어떤 스레드에서든 동일 인터페이스; 검색은 소유 스레드로 위임."""

    def search(self, query: str, top_k: int = RAG_TOP_K, session_context: str = "") -> str:
        return _owner.submit("search", query, top_k=top_k, session_context=session_context).result(
            timeout=_SEARCH_TIMEOUT_SEC
        )

    def list_papers(self) -> str:
        return list_stored_papers_text()


_public = ChromaRAGPublic()


def get_chroma_rag_tool() -> ChromaRAGPublic:
    return _public


def warmup_chroma_rag() -> None:
    """메인 등에서 부팅 시 1회 호출: 소유 스레드에서 클라이언트 선생성."""
    _owner.warmup()


def reset_chroma_rag_singleton_for_tests() -> None:
    """pytest 등에서 프로세스 단위 테스트 시 필요 시 확장. 현재는 owner 스레드 유지."""
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
    """실제 Chroma·임베딩 보유. **chroma-rag-owner 스레드에서만** 인스턴스화·search 호출."""

    def __init__(self, db_path: str = CHROMA_DB_PATH, collection_name: str = COLLECTION_NAME):
        _log.debug("ChromaRAGTool.__init__: SentenceTransformerEmbeddingFunction start")
        print("[ChromaRAG TRACE] __init__ embedding_fn BEGIN", flush=True)
        self._embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True
        )
        _log.debug("ChromaRAGTool.__init__: PersistentClient start path=%s", db_path)
        print("[ChromaRAG TRACE] __init__ PersistentClient BEGIN", flush=True)
        self._client = chromadb.PersistentClient(
            path=db_path, settings=Settings(anonymized_telemetry=False)
        )
        print("[ChromaRAG TRACE] __init__ get_collection BEGIN", flush=True)
        self._collection = self._client.get_collection(
            name=collection_name, embedding_function=self._embedding_fn
        )
        _log.debug("ChromaRAGTool.__init__: done collection=%s", collection_name)
        print("[ChromaRAG TRACE] __init__ get_collection END", flush=True)

    def _strip_urls(self, query: str) -> str:
        if "http" not in query.lower():
            return query
        parts = query.split()
        return " ".join(p for p in parts if not p.lower().startswith("http")).strip()

    def _extract_paper_title(self, query: str) -> str:
        for sep in (" 이거", " 이 논문", " 논문 ", " 논문좀", " 논문 자세히", " 요약", " paper"):
            if sep in query:
                before = query.split(sep)[0].strip()
                if before and len(before) > 10 and any(c.isalnum() for c in before):
                    return before
        return query

    def _rewrite_query(self, query: str, session_context: str) -> str:
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

    def search(self, query: str, top_k: int = RAG_TOP_K, session_context: str = "") -> str:
        """소유 스레드 전용: collection.query 동기 호출."""
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
            results = self._collection.query(
                query_texts=[search_query], n_results=top_k, include=["documents", "metadatas"]
            )
            print("[ChromaRAG TRACE] search AFTER query", flush=True)
            docs = results["documents"][0] if results["documents"] else []
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
            _log.debug("ChromaRAGTool.search: parsed docs count=%s", len(docs))
            if not docs:
                return "관련 문서 없음"
            parts = []
            for doc, meta in zip(docs, metas):
                pid = meta.get("paper_id", "")
                title = meta.get("title", "")
                header = f"[{pid}] {title}\n" if (pid or title) else ""
                parts.append(f"{header}{doc[:800]}" if doc else header)
            return "\n\n---\n\n".join(p for p in parts if p.strip())
        except Exception as e:
            _log.debug("ChromaRAGTool.search: exception %s", e)
            return f"검색 오류: {e}"

    def list_papers(self) -> str:
        return list_stored_papers_text()
