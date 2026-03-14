#!/usr/bin/env python3
"""
arXiv 논문 자동 수집 및 파싱 파이프라인 (듀얼 파이프라인)
- ArxivFetcher → PdfParser → DataStorage → RagProcessor → QaGenerator
"""

import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

from src.arxiv_fetcher import ArxivFetcher, PaperMetadata
from src.data_storage import DataStorage
from src.pdf_parser import PdfParser
from src.qa_generator import QaGenerator
from src.rag_processor import RagProcessor

# .env에서 환경 변수 로드 (GEMINI_API_KEY 등)
load_dotenv()


def run_pipeline() -> None:
    """전체 파이프라인 실행"""
    fetcher = ArxivFetcher(category="cs.AI", limit=3, min_delay=3.0, max_delay=5.0)
    parser = PdfParser(table_strategy="lines_strict")
    storage = DataStorage(output_path="test_science_data.jsonl")
    rag_processor = RagProcessor(db_path="./test_chroma_db")

    # QaGenerator는 GEMINI_API_KEY가 있을 때만 초기화
    qa_generator: QaGenerator | None = None
    if os.getenv("GEMINI_API_KEY"):
        try:
            qa_generator = QaGenerator(output_path="./test_finetune_data.jsonl")
        except Exception as e:
            print(f"  ⚠️  QaGenerator 초기화 실패 (건너뜀): {e}")
    else:
        print("  ⚠️  GEMINI_API_KEY 미설정 → Q&A 생성 단계 건너뜀 (.env에 추가 시 활성화)")

    # 1. 메타데이터 수집
    print("\n" + "=" * 60)
    print("📚 arXiv 논문 수집 파이프라인 (듀얼) 시작")
    print("=" * 60)

    papers: list[PaperMetadata] = []
    try:
        papers = fetcher.fetch_metadata_list()
    except Exception as e:
        print(f"❌ 수집 단계 예외: {e}")
        return

    if not papers:
        print("⚠️  수집된 논문이 없습니다.")
        return

    print(f"\n✅ {len(papers)}개 논문 메타데이터 수집 완료\n")

    # 2. 각 논문에 대해 PDF 다운로드 → 파싱 → 저장 → RAG → Q&A
    success_count = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        for i, paper in enumerate(papers, start=1):
            print("-" * 50)
            print(f"📄 [{i}/{len(papers)}] {paper.paper_id} - {paper.title[:50]}...")
            print("-" * 50)

            pdf_path = tmpdir_path / f"{paper.paper_id}.pdf"

            # PDF 다운로드
            try:
                print(f"  ⬇️  PDF 다운로드 중...")
                if not fetcher.download_pdf(paper.pdf_url, str(pdf_path)):
                    print(f"  ⏭️  건너뜀 (다운로드 실패)")
                    continue
                print(f"  ✓ 다운로드 완료")
            except Exception as e:
                print(f"  ❌ 다운로드 예외: {e}")
                continue

            # PDF → 마크다운 파싱
            try:
                print(f"  📝 마크다운 파싱 중...")
                markdown_content = parser.to_markdown(pdf_path)
                if not markdown_content:
                    print(f"  ⏭️  건너뜀 (파싱 실패)")
                    continue
                print(f"  ✓ 파싱 완료 ({len(markdown_content):,}자)")
            except Exception as e:
                print(f"  ❌ 파싱 예외: {e}")
                continue

            # JSONL 저장
            try:
                record = storage.build_paper_record(
                    paper_id=paper.paper_id,
                    title=paper.title,
                    authors=paper.authors,
                    abstract=paper.abstract,
                    published=paper.published,
                    pdf_url=paper.pdf_url,
                    markdown_content=markdown_content,
                )
                if storage.save_paper(record):
                    success_count += 1
                    print(f"  💾 저장 완료 → {storage.output_path}")
                else:
                    print(f"  ⏭️  건너뜀 (저장 실패)")
                    continue
            except Exception as e:
                print(f"  ❌ 저장 예외: {e}")
                continue

            # RAG: Chroma DB 적재
            try:
                print(f"  🔗 RAG 청킹 및 Chroma 적재 중...")
                chunk_count = rag_processor.add_paper(
                    markdown_content=markdown_content,
                    title=paper.title,
                    published=paper.published,
                    pdf_url=paper.pdf_url,
                    paper_id=paper.paper_id,
                )
                print(f"  ✓ RAG 완료 ({chunk_count}개 청크) → {rag_processor.db_path}")
            except Exception as e:
                print(f"  ❌ RAG 예외 (건너뜀): {e}")

            # Q&A 생성 (파인튜닝 데이터)
            if qa_generator:
                try:
                    print(f"  🤖 Gemini Q&A 생성 중...")
                    qa_record = qa_generator.generate_qa(markdown_content)
                    if qa_record and qa_generator.save_qa(qa_record):
                        print(f"  ✓ Q&A 저장 완료 → {qa_generator.output_path}")
                    else:
                        print(f"  ⏭️  Q&A 생성 실패 (건너뜀)")
                except Exception as e:
                    print(f"  ❌ Q&A 예외 (건너뜀): {e}")

            # 임시 PDF 삭제
            DataStorage.remove_temp_pdf(pdf_path)

    print("\n" + "=" * 60)
    print(f"🎉 파이프라인 완료: {success_count}/{len(papers)}개 논문 처리 성공")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_pipeline()
