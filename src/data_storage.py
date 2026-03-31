"""
데이터 적재 모듈 (DataStorage)
- 파싱된 마크다운과 메타데이터를 JSONL 형식으로 저장
- 임시 PDF 파일 정리
"""

import json
import os
from pathlib import Path
from typing import Any, Union

import fcntl


def normalize_paper_id(raw_id: str) -> str:
    """
    arXiv ID에서 버전 접미사 제거: 2401.12345v2 -> 2401.12345.
    패턴에 안 맞으면 원본을 그대로 반환.
    """
    s = (raw_id or "").strip()
    if not s:
        return s
    # 간단히 마지막 'v숫자' 접미사만 제거 (2401.12345v2 -> 2401.12345)
    if "v" in s:
        base, suffix = s.rsplit("v", 1)
        if suffix.isdigit() and base.replace(".", "").isdigit():
            return base
    return s


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
        self._known_paper_ids: set[str] = self._load_existing_paper_ids()

    def _load_existing_paper_ids(self) -> set[str]:
        """기존 JSONL에서 paper_id 집합을 1회 로드해 중복 저장을 방지."""
        ids: set[str] = set()
        if not self.output_path.exists():
            return ids
        try:
            with open(self.output_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    paper_id = normalize_paper_id(str(item.get("paper_id", "")).strip())
                    if paper_id:
                        ids.add(paper_id)
        except OSError as e:
            print(f"  ⚠️ 기존 paper_id 인덱스 로드 실패: {e}")
        return ids

    def save_paper(self, data: dict[str, Any]) -> bool:
        """
        단일 논문 데이터를 JSONL 파일에 한 줄씩 append 저장합니다.

        Args:
            data: 논문 메타데이터 + 마크다운 본문을 담은 딕셔너리

        Returns:
            저장 성공 여부
        """
        try:
            paper_id = normalize_paper_id(str(data.get("paper_id", "")).strip())
            if paper_id and paper_id in self._known_paper_ids:
                print(f"  ⏭️  건너뜀 (이미 저장된 논문): {paper_id}")
                return False

            line = json.dumps(data, ensure_ascii=False) + "\n"
            # 멀티 프로세스 동시 실행 대비: 파일 락으로 단일 writer 구간 보호
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.output_path, "a+", encoding="utf-8") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                # 다른 프로세스가 먼저 쓴 내용을 반영하기 위해 인덱스 재로딩
                self._known_paper_ids = self._load_existing_paper_ids()
                if paper_id and paper_id in self._known_paper_ids:
                    print(f"  ⏭️  건너뜀 (이미 저장된 논문, 락 내 재확인): {paper_id}")
                    return False
                f.write(line)
                f.flush()
            if paper_id:
                self._known_paper_ids.add(paper_id)
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
