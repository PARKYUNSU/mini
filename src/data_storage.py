"""
데이터 적재 모듈 (DataStorage)
- 파싱된 마크다운과 메타데이터를 JSONL 형식으로 저장
- 임시 PDF 파일 정리
"""

import json
import os
from pathlib import Path
from typing import Any, Union


class DataStorage:
    """파싱 결과를 JSONL 파일에 누적 저장하는 클래스"""

    def __init__(self, output_path: Union[str, Path] = "raw_data_queue/crawled_papers.jsonl"):
        """
        Args:
            output_path: JSONL 저장 경로
        """
        self.output_path = Path(output_path)
        parent = self.output_path.parent
        if parent != Path("."):
            os.makedirs(parent, exist_ok=True)

    def save_paper(self, data: dict[str, Any]) -> bool:
        """
        단일 논문 데이터를 JSONL 파일에 한 줄씩 append 저장합니다.

        Args:
            data: 논문 메타데이터 + 마크다운 본문을 담은 딕셔너리

        Returns:
            저장 성공 여부
        """
        try:
            line = json.dumps(data, ensure_ascii=False) + "\n"
            with open(self.output_path, "a", encoding="utf-8") as f:
                f.write(line)
            return True
        except (OSError, TypeError) as e:
            print(f"  ❌ 저장 실패: {e}")
            return False

    def build_paper_record(
        self,
        paper_id: str,
        title: str,
        authors: list[str],
        abstract: str,
        published: str,
        pdf_url: str,
        markdown_content: str,
    ) -> dict[str, Any]:
        """
        메타데이터와 마크다운 본문을 하나의 JSON 객체로 묶습니다.

        Args:
            paper_id: 논문 ID
            title: 제목
            authors: 저자 목록
            abstract: 요약
            published: 출판일
            pdf_url: PDF URL
            markdown_content: 파싱된 마크다운 본문

        Returns:
            QLoRA/RAG용으로 구조화된 딕셔너리
        """
        return {
            "paper_id": paper_id,
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "published": published,
            "pdf_url": pdf_url,
            "content": markdown_content,
        }

    @staticmethod
    def remove_temp_pdf(pdf_path: Union[str, Path]) -> bool:
        """
        처리 완료된 임시 PDF 파일을 삭제합니다.

        Args:
            pdf_path: 삭제할 PDF 경로

        Returns:
            삭제 성공 여부
        """
        try:
            path = Path(pdf_path)
            if path.exists():
                path.unlink()
                return True
            return False
        except OSError as e:
            print(f"  ⚠️  임시 PDF 삭제 실패: {e}")
            return False
