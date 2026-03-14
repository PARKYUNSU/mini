"""
PDF 파싱 모듈 (PdfParser)
- PyMuPDF4LLM을 사용해 PDF를 마크다운 텍스트로 변환
- 수식과 표 보존에 최적화
"""

import tempfile
from pathlib import Path
from typing import Optional

import pymupdf4llm


class PdfParser:
    """PDF를 마크다운으로 변환하는 클래스 (수식·표 보존)"""

    def __init__(
        self,
        table_strategy: str = "lines_strict",
        header: bool = True,
        footer: bool = True,
    ):
        """
        Args:
            table_strategy: 표 감지 전략 (lines_strict: 표 구조 보존에 유리)
            header: 헤더 포함 여부
            footer: 푸터 포함 여부
        """
        self.table_strategy = table_strategy
        self.header = header
        self.footer = footer

    def to_markdown(self, pdf_path: str | Path) -> Optional[str]:
        """
        PDF 파일을 마크다운 텍스트로 변환합니다.

        Args:
            pdf_path: PDF 파일 경로

        Returns:
            변환된 마크다운 문자열, 실패 시 None
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                print(f"  ❌ PDF 파일 없음: {pdf_path}")
                return None

            md_text = pymupdf4llm.to_markdown(
                str(pdf_path),
                table_strategy=self.table_strategy,
                header=self.header,
                footer=self.footer,
            )
            return md_text if md_text else None
        except Exception as e:
            print(f"  ❌ PDF 파싱 실패: {e}")
            return None
