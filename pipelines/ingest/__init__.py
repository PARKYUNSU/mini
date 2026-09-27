"""arXiv 논문 수집 및 파싱 파이프라인 패키지.

하위 모듈을 직접 import 하세요. 예:

    from pipelines.ingest.arxiv_fetcher import ArxivFetcher, PaperMetadata
    from pipelines.ingest.pdf_parser import PdfParser

이 패키지의 ``__init__`` 에서 chromadb·pymupdf4llm 등을 선로드하지 않아,
arxiv_fetcher 만 필요한 스크립트가 가벼운 의존성만으로 동작할 수 있습니다.

``from pipelines.ingest import PdfParser`` 형태는 :func:`__getattr__` 로 지원합니다.
"""

from __future__ import annotations

__all__ = [
    "ArxivFetcher",
    "PaperMetadata",
    "PdfParser",
    "DataStorage",
    "RagProcessor",
    "QaGenerator",
]


def __getattr__(name: str):
    if name == "ArxivFetcher":
        from pipelines.ingest.arxiv_fetcher import ArxivFetcher

        return ArxivFetcher
    if name == "PaperMetadata":
        from pipelines.ingest.arxiv_fetcher import PaperMetadata

        return PaperMetadata
    if name == "DataStorage":
        from pipelines.ingest.data_storage import DataStorage

        return DataStorage
    if name == "PdfParser":
        from pipelines.ingest.pdf_parser import PdfParser

        return PdfParser
    if name == "RagProcessor":
        from pipelines.ingest.rag_processor import RagProcessor

        return RagProcessor
    if name == "QaGenerator":
        from pipelines.ingest.qa_generator import QaGenerator

        return QaGenerator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
