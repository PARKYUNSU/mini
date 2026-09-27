"""
RAG 처리 모듈 (RagProcessor)
- 마크다운 본문을 의미 단위로 청킹 후 Chroma DB에 적재
"""

import hashlib
import os
import threading
import uuid
from pathlib import Path
from typing import Any, Union

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from core.config.agent_config import (
    EMBEDDING_MODEL,
    ENABLE_SEMANTIC_MERGE,
    SEMANTIC_MERGE_THRESHOLD,
)

from .chunking_strategy_proposal import (
    CHUNK_MIN_CHARS,
    passes_chunk_quality_filter,
    preprocess_for_chunking,
)


class RagProcessor:
    """마크다운 청킹 및 Chroma DB 적재 클래스"""

    def __init__(
        self,
        db_path: Union[str, Path] = "./chroma_db",
        embedding_model: str = EMBEDDING_MODEL,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        collection_name: str = "arxiv_papers",
    ):
        """
        Args:
            db_path: Chroma DB 저장 경로
            embedding_model: 임베딩 모델명
            chunk_size: 청크 최대 크기(문자)
            chunk_overlap: 청크 간 겹침 크기
            collection_name: Chroma 컬렉션 이름
        """
        self.db_path = Path(db_path)
        os.makedirs(self.db_path, exist_ok=True)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.collection_name = collection_name
        self._embedding_model_name = embedding_model

        self._embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name=embedding_model,
            device="cpu",
            normalize_embeddings=True,
        )
        self._client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

        self._md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ],
            strip_headers=False,
        )
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        self._semantic_st_model = None
        self._semantic_st_lock = threading.Lock()

    def _get_semantic_merge_model(self):
        if self._semantic_st_model is not None:
            return self._semantic_st_model
        with self._semantic_st_lock:
            if self._semantic_st_model is None:
                from sentence_transformers import SentenceTransformer

                self._semantic_st_model = SentenceTransformer(
                    self._embedding_model_name,
                    device="cpu",
                )
        return self._semantic_st_model

    def _semantic_merge_documents(self, docs: list[Document]) -> list[Document]:
        """인접 청크 임베딩 코사인 유사도가 threshold 이상이면 순서대로 병합."""
        if not docs or len(docs) <= 1:
            return docs
        if not ENABLE_SEMANTIC_MERGE:
            return docs
        try:
            import numpy as np

            texts = [d.page_content for d in docs]
            model = self._get_semantic_merge_model()
            emb = model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False,
                batch_size=32,
            )
            thr = float(SEMANTIC_MERGE_THRESHOLD)
            out: list[Document] = []
            i = 0
            n = len(docs)
            while i < n:
                merged_text = texts[i]
                meta = dict(docs[i].metadata)
                cur_emb = np.asarray(emb[i], dtype=np.float64)
                j = i + 1
                while j < n:
                    sim = float(np.dot(cur_emb, emb[j]))
                    if sim >= thr:
                        merged_text = f"{merged_text}\n\n{texts[j]}"
                        cur_emb = cur_emb + np.asarray(emb[j], dtype=np.float64)
                        norm = float(np.linalg.norm(cur_emb)) + 1e-12
                        cur_emb = cur_emb / norm
                        j += 1
                    else:
                        break
                out.append(Document(page_content=merged_text, metadata=meta))
                i = j
            return out
        except Exception as exc:
            print(f"  ⚠️  semantic merge skipped: {exc}")
            return docs

    def _merge_adjacent_documents(self, docs: list[Document]) -> list[Document]:
        """짧은 인접 청크를 붙여 과분할·노이즈 조각을 줄임."""
        if not docs:
            return []
        sep = "\n\n"
        min_chars = 120
        max_merged = max(900, self.chunk_size * 2)
        out: list[Document] = []
        buf_doc = docs[0]
        buf = buf_doc.page_content.strip()
        for nxt in docs[1:]:
            nxt_t = nxt.page_content.strip()
            if len(buf) < min_chars and len(buf) + len(nxt_t) + len(sep) <= max_merged:
                buf = f"{buf}{sep}{nxt_t}"
            else:
                out.append(Document(page_content=buf, metadata=dict(buf_doc.metadata)))
                buf_doc = nxt
                buf = nxt_t
        out.append(Document(page_content=buf, metadata=dict(buf_doc.metadata)))
        return out

    def chunk_markdown(self, markdown_content: str) -> list[Document]:
        """
        마크다운을 헤더 기준 → 재귀 분할로 청킹합니다.

        - References / Bibliography / Appendix 등 이후 본문 제거(청킹 전 절단)
        - 인접 소청크 병합
        - (옵션) 시맨틱 머지: 인접 청크 임베딩 유사도 ≥ ``SEMANTIC_MERGE_THRESHOLD`` 이면 병합

        Args:
            markdown_content: 마크다운 본문

        Returns:
            Document 리스트
        """
        md = preprocess_for_chunking(markdown_content)
        if not md.strip():
            return []
        md_splits = self._md_splitter.split_text(md)
        splits = self._text_splitter.split_documents(md_splits)
        merged = self._merge_adjacent_documents(splits)
        return self._semantic_merge_documents(merged)

    def add_paper(
        self,
        markdown_content: str,
        title: str,
        published: str,
        pdf_url: str,
        paper_id: str = "",
        abstract: str = "",
    ) -> int:
        """
        논문 본문을 청킹하여 Chroma DB에 적재합니다.

        - Step1 품질 필터: 길이·수식 비율·URL 비율 (``passes_chunk_quality_filter``)
        - paper_id + chunk_index 기반 deterministic ID로 중복 적재 방지 (upsert)

        Args:
            markdown_content: 마크다운 본문
            title: 논문 제목
            published: 출판일
            pdf_url: PDF URL
            paper_id: 논문 ID (고유 식별용)
            abstract: 초록 (경량 논문 단위 리랭크용; 없으면 빈 문자열)

        Returns:
            적재된 청크 수
        """
        chunks = self.chunk_markdown(markdown_content)
        if not chunks:
            return 0

        base_meta = {"title": title, "published": published, "pdf_url": pdf_url}
        if paper_id:
            base_meta["paper_id"] = paper_id
        if (abstract or "").strip():
            base_meta["abstract"] = (abstract or "").strip()

        ids = []
        documents = []
        metadatas = []
        skipped_quality = 0

        for i, doc in enumerate(chunks):
            if not passes_chunk_quality_filter(doc.page_content):
                skipped_quality += 1
                continue

            chunk_meta = {**base_meta, **doc.metadata}

            # 작업 2: paper_id + chunk_index 기반 deterministic ID
            # 동일 논문을 다시 적재해도 같은 ID가 생성되어 upsert로 중복 방지
            if paper_id:
                raw_id = f"{paper_id}::chunk::{i}"
                chunk_id = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()[:32]
            else:
                chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{paper_id}-{i}-{doc.page_content[:50]}"))

            ids.append(chunk_id)
            documents.append(doc.page_content)
            metadatas.append(self._sanitize_metadata(chunk_meta))

        if skipped_quality:
            print(
                f"  ℹ️  Step1 품질 필터로 청크 {skipped_quality}개 제외 "
                f"(길이<{CHUNK_MIN_CHARS} 또는 math/url 비율 초과)"
            )

        if not ids:
            return 0

        # upsert: 동일 ID가 이미 있으면 덮어쓰기 (중복 적재 방지)
        self._collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        return len(ids)

    @staticmethod
    def _sanitize_metadata(meta: dict[str, Any]) -> dict[str, Any]:
        """Chroma DB는 str 값만 허용하므로 변환"""
        return {k: str(v) if v is not None else "" for k, v in meta.items()}
