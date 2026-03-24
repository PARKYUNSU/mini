"""
agent_tools/ 전용 Tool RAG: 파일명 + 모듈 docstring만 임베딩하여 논문 Chroma와 분리 저장.
Router/Planner/Executor 컨텍스트 팽창 방지용 Top-K 검색.
"""

from __future__ import annotations

import ast
import threading
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from agent_config import (
    AGENT_TOOLS_DIR,
    EMBEDDING_MODEL,
    PROJECT_ROOT,
    TOOL_CHROMA_DB_PATH,
    TOOL_COLLECTION_NAME,
    TOOL_RAG_TOP_K,
)


def extract_module_docstring(source: str) -> str:
    """파이썬 소스에서 모듈 최상위 docstring만 추출."""
    try:
        tree = ast.parse(source)
        doc = ast.get_docstring(tree)
        return (doc or "").strip()
    except SyntaxError:
        return ""


class ToolRAGStore:
    """도구 전용 Chroma 컬렉션: 스캔·동기화·유사도 검색."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True
        )
        abs_db = Path(TOOL_CHROMA_DB_PATH)
        if not abs_db.is_absolute():
            abs_db = PROJECT_ROOT / abs_db
        abs_db.mkdir(parents=True, exist_ok=True)
        self._db_path = str(abs_db)
        self._client = chromadb.PersistentClient(
            path=self._db_path, settings=Settings(anonymized_telemetry=False)
        )
        self._collection = self._client.get_or_create_collection(
            name=TOOL_COLLECTION_NAME,
            embedding_function=self._embedding_fn,
            metadata={"description": "agent_tools docstring index"},
        )

    def full_sync(self, tools_dir: Path | None = None) -> int:
        """
        agent_tools/*.py 전체 스캔 후 컬렉션과 디스크 동기화.
        디스크에 없는 id는 Chroma에서 삭제. 반환: 인덱싱된 파일 수.
        """
        root = Path(tools_dir or AGENT_TOOLS_DIR)
        root = root.resolve()
        root.mkdir(parents=True, exist_ok=True)

        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict[str, Any]] = []

        py_paths = sorted(root.glob("*.py"))
        saved_dir = root / "saved"
        if saved_dir.is_dir():
            py_paths += sorted(saved_dir.glob("*.py"))
        for p in py_paths:
            try:
                content = p.read_text(encoding="utf-8")
                doc = extract_module_docstring(content) or "(docstring 없음)"
                stem = p.stem
                ids.append(stem)
                documents.append(f"{stem}\n{doc}")
                metadatas.append({"tool_name": stem, "source_file": p.name})
            except OSError as e:
                print(f"[ToolRAG] 파일 읽기 스킵 {p}: {e}")

        with self._lock:
            try:
                existing = self._collection.get(include=[])
                old_ids = set(existing.get("ids") or [])
            except Exception:
                old_ids = set()
            new_ids = set(ids)
            to_delete = list(old_ids - new_ids)
            if to_delete:
                try:
                    self._collection.delete(ids=to_delete)
                except Exception as e:
                    print(f"[ToolRAG] 삭제(id 정리) 경고: {e}")
            if ids:
                try:
                    self._collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
                except Exception as e:
                    print(f"[ToolRAG] upsert 오류: {e}")
                    raise
        print(f"[ToolRAG] 동기화 완료: {len(ids)}개 도구 (DB={self._db_path})")
        return len(ids)

    def upsert_file(self, path: Path) -> None:
        """단일 .py 추가/갱신 (도구 저장 직후 호출)."""
        path = path.resolve()
        if path.suffix != ".py" or not path.exists():
            return
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"[ToolRAG] upsert_file 읽기 실패: {e}")
            return
        doc = extract_module_docstring(content) or "(docstring 없음)"
        stem = path.stem
        with self._lock:
            self._collection.upsert(
                ids=[stem],
                documents=[f"{stem}\n{doc}"],
                metadatas=[{"tool_name": stem, "source_file": path.name}],
            )
        print(f"[ToolRAG] upsert: {stem}")

    def remove_tool_id(self, stem: str) -> None:
        """도구 파일 삭제 시 인덱스에서 제거."""
        with self._lock:
            try:
                self._collection.delete(ids=[stem])
                print(f"[ToolRAG] delete id={stem}")
            except Exception as e:
                print(f"[ToolRAG] delete 경고 {stem}: {e}")

    def search(self, query: str, k: int | None = None) -> list[dict[str, Any]]:
        """유사도 Top-K: [{name, doc, distance?}, ...]"""
        k = k if k is not None else TOOL_RAG_TOP_K
        q = (query or "").strip()
        if not q:
            return []
        with self._lock:
            try:
                n = self._collection.count()
            except Exception:
                n = 0
            if n == 0:
                return []
            n_results = min(max(k, 1), n)
            try:
                results = self._collection.query(
                    query_texts=[q],
                    n_results=n_results,
                    include=["documents", "metadatas", "distances"],
                )
            except Exception as e:
                print(f"[ToolRAG] query 오류: {e}")
                return []

        docs = (results.get("documents") or [[]])[0]
        metas = (results.get("metadatas") or [[]])[0]
        dists = (results.get("distances") or [[]])[0] if results.get("distances") else [None] * len(docs)

        out: list[dict[str, Any]] = []
        for i, doc in enumerate(docs):
            meta = metas[i] if i < len(metas) else {}
            name = (meta or {}).get("tool_name") or ""
            if not name and doc:
                name = (doc.split("\n", 1)[0] or "").strip()
            body = ""
            if doc and "\n" in doc:
                body = doc.split("\n", 1)[1].strip()
            elif doc:
                body = doc.strip()
            dist = dists[i] if i < len(dists) else None
            out.append({"name": name, "doc": body, "distance": dist})
        return out

    def format_topk_block(self, query: str, k: int | None = None) -> str:
        """프롬프트용 압축 블록."""
        k = k if k is not None else TOOL_RAG_TOP_K
        hits = self.search(query, k=k)
        if not hits:
            return (
                "관련 도구 후보 없음. 저장된 도구가 없거나 질문과 유사한 도구가 인덱스에 없습니다. "
                "맞는 도구가 없으면 Plan&Code(C 경로)로 새 도구를 만드는 것이 적절합니다."
            )
        lines = []
        for h in hits:
            name = h.get("name") or "unknown"
            doc = (h.get("doc") or "")[:500]
            lines.append(f"- **{name}**: {doc}")
        return (
            "이 질문을 해결하는 데 유용할 수 있는 관련 도구 후보:\n"
            + "\n".join(lines)
        )

    def format_router_tools_tag(self, query: str, k: int | None = None) -> str:
        """라우터 system_prompt <tools>용 짧은 나열."""
        k = k if k is not None else TOOL_RAG_TOP_K
        hits = self.search(query, k=k)
        if not hits:
            return "(유사 도구 후보 없음 — B는 요청과 100% 일치할 때만; 아니면 C 또는 D)"
        parts = []
        for h in hits:
            name = h.get("name") or "?"
            doc = (h.get("doc") or "").replace("\n", " ")[:100]
            parts.append(f"{name}: {doc}")
        return "; ".join(parts)


_tool_rag_singleton: ToolRAGStore | None = None
_tool_rag_lock = threading.Lock()


def get_tool_rag_store() -> ToolRAGStore:
    global _tool_rag_singleton
    with _tool_rag_lock:
        if _tool_rag_singleton is None:
            _tool_rag_singleton = ToolRAGStore()
        return _tool_rag_singleton


def sync_tool_chroma_from_disk() -> int:
    """봇 기동 시 등: 디스크 기준 전체 동기화."""
    return get_tool_rag_store().full_sync(AGENT_TOOLS_DIR)
