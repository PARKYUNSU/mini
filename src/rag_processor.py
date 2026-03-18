"""
RAG 처리 모듈 (RagProcessor)
- 마크다운 본문을 의미 단위로 청킹 후 Chroma DB에 적재
"""

import os
import uuid
from pathlib import Path
from typing import Any, Union

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


class RagProcessor:
    """마크다운 청킹 및 Chroma DB 적재 클래스"""

    def __init__(
        self,
        db_path: Union[str, Path] = "./chroma_db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
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

    def chunk_markdown(self, markdown_content: str) -> list[Document]:
        """
        마크다운을 헤더 기준 → 재귀 분할로 청킹합니다.

        Args:
            markdown_content: 마크다운 본문

        Returns:
            Document 리스트
        """
        md_splits = self._md_splitter.split_text(markdown_content)
        splits = self._text_splitter.split_documents(md_splits)
        return splits

    def add_paper(
        self,
        markdown_content: str,
        title: str,
        published: str,
        pdf_url: str,
        paper_id: str = "",
    ) -> int:
        """
        논문 본문을 청킹하여 Chroma DB에 적재합니다.

        Args:
            markdown_content: 마크다운 본문
            title: 논문 제목
            published: 출판일
            pdf_url: PDF URL
            paper_id: 논문 ID (고유 식별용)

        Returns:
            적재된 청크 수
        """
        chunks = self.chunk_markdown(markdown_content)
        if not chunks:
            return 0

        base_meta = {"title": title, "published": published, "pdf_url": pdf_url}
        if paper_id:
            base_meta["paper_id"] = paper_id

        ids = []
        documents = []
        metadatas = []

        for i, doc in enumerate(chunks):
            chunk_meta = {**base_meta, **doc.metadata}
            chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{paper_id}-{i}-{doc.page_content[:50]}"))
            ids.append(chunk_id)
            documents.append(doc.page_content)
            metadatas.append(self._sanitize_metadata(chunk_meta))

        self._collection.add(ids=ids, documents=documents, metadatas=metadatas)
        return len(chunks)

    @staticmethod
    def _sanitize_metadata(meta: dict[str, Any]) -> dict[str, Any]:
        """Chroma DB는 str 값만 허용하므로 변환"""
        return {k: str(v) if v is not None else "" for k, v in meta.items()}
