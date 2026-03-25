"""논문 RAG (ChromaDB + 임베딩). agent_bot과 분리해 테스트·재사용 용이."""

from __future__ import annotations

import json
from pathlib import Path

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.messages import HumanMessage, SystemMessage

from agent_config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL, RAG_TOP_K
from agent_llm import get_rag_query_rewrite_llm

_PROJECT_ROOT = Path(__file__).resolve().parent


def list_stored_papers_text() -> str:
    """raw_data_queue/crawled_papers.jsonl 기준 고유 paper_id·title (Chroma/임베딩 로드 없음)."""
    try:
        raw_path = _PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"
        if not raw_path.exists():
            return "저장된 논문이 없습니다."
        seen: set[str] = set()
        lines: list[str] = []
        # 전체 read_text()는 수백 MB JSONL에서 메모리·지연 폭주 → 줄 단위 스트림
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
    def __init__(self, db_path: str = CHROMA_DB_PATH, collection_name: str = COLLECTION_NAME):
        self._embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True
        )
        self._client = chromadb.PersistentClient(
            path=db_path, settings=Settings(anonymized_telemetry=False)
        )
        self._collection = self._client.get_collection(
            name=collection_name, embedding_function=self._embedding_fn
        )

    def _strip_urls(self, query: str) -> str:
        """URL 텍스트 제거 → RAG 검색어 정제 (심플 방식: http 포함 시 제거)"""
        if "http" not in query.lower():
            return query
        parts = query.split()
        return " ".join(p for p in parts if not p.lower().startswith("http")).strip()

    def _extract_paper_title(self, query: str) -> str:
        """'X 이거 논문 요약해줘' 형태에서 논문 제목 X 추출 → 검색 정확도 향상"""
        for sep in (" 이거", " 이 논문", " 논문 ", " 논문좀", " 논문 자세히", " 요약", " paper"):
            if sep in query:
                before = query.split(sep)[0].strip()
                if before and len(before) > 10 and any(c.isalnum() for c in before):
                    return before
        return query

    def _rewrite_query(self, query: str, session_context: str) -> str:
        """후속 질문('그거', '더 자세히' 등)일 때 대화 맥락으로 검색어 재구성 (Standalone Query)"""
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
        if session_context:
            query = self._rewrite_query(query, session_context)
        query = self._strip_urls(query)
        if not query.strip():
            return "관련 문서 없음"
        search_query = self._extract_paper_title(query)
        try:
            results = self._collection.query(
                query_texts=[search_query], n_results=top_k, include=["documents", "metadatas"]
            )
            docs = results["documents"][0] if results["documents"] else []
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
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
            return f"검색 오류: {e}"

    def list_papers(self) -> str:
        """저장 큐 JSONL 기준 논문 목록(고유 paper_id, title). Chroma와 동일 출처."""
        return list_stored_papers_text()
