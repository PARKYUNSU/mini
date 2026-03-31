#!/usr/bin/env python3
"""
arXiv 논문 자동 수집 및 파싱 파이프라인
- ArxivFetcher → PdfParser → DataStorage → RagProcessor
- 역할: 수집 → ChromaDB 적재 → raw_data_queue/ 원본 저장 (Q&A 생성은 llm_debate_scheduler 전담)
"""

import os
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import telebot

from retry_utils import retry_on_network_error
from src.arxiv_fetcher import ArxivFetcher, PaperMetadata
from src.cleanup import cleanup_legacy_files
from src.data_storage import DataStorage, normalize_paper_id
from src.pdf_parser import PdfParser
from src.rag_processor import RagProcessor

# .env에서 환경 변수 로드 (GEMINI_API_KEY 등)
load_dotenv()

# 데이터 저장 경로 (폴더 자동 생성)
RAW_DATA_DIR = Path("./raw_data_queue")
CHROMA_DIR = Path("./chroma_db")
DEBATE_INDEX_PATH = Path("./finetune_datasets/debated_paper_ids.jsonl")


def _configure_utf8_stdio() -> None:
    """cron 환경에서도 한글 로그가 최대한 UTF-8로 남도록 표준 입출력 인코딩 고정."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _get_telegram_targets() -> tuple[str, list[str]]:
    token = os.getenv("TELEGRAM_TOKEN") or ""
    chat_ids = [cid.strip() for cid in (os.getenv("ALLOWED_CHAT_ID") or "").split(",") if cid.strip()]
    return token, chat_ids


@retry_on_network_error
def _do_send_telegram(token: str, chat_ids: list[str], message: str) -> None:
    """네트워크 재시도 적용 텔레그램 전송"""
    bot = telebot.TeleBot(token)
    for cid in chat_ids:
        bot.send_message(cid, message)
    print(f"✅ 텔레그램 알림 전송 성공: {len(chat_ids)}명")


def _send_telegram_notification(message: str) -> bool:
    token, chat_ids = _get_telegram_targets()
    if not token or not chat_ids:
        print(
            "ℹ️ 텔레그램 알림 스킵: "
            f"token={'Y' if bool(token) else 'N'}, "
            f"chat_ids={len(chat_ids)}"
        )
        return False

    try:
        _do_send_telegram(token, chat_ids, message)
        return True
    except Exception as e:
        print(f"⚠️ 텔레그램 알림 전송 실패: {e}")
        return False


def _ensure_data_dirs() -> None:
    """데이터 폴더가 없으면 자동 생성"""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(CHROMA_DIR, exist_ok=True)


def _load_debated_base_ids() -> set[str]:
    """이미 토론 완료된 논문 ID(베이스 ID 기준) 집합 로드."""
    ids: set[str] = set()
    if not DEBATE_INDEX_PATH.exists():
        return ids
    try:
        with open(DEBATE_INDEX_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pid = normalize_paper_id(str(item.get("paper_id", "")).strip())
                if pid:
                    ids.add(pid)
    except Exception as e:
        print(f"⚠️ 토론 인덱스 로드 실패(선필터 비활성): {e}")
    return ids


def run_pipeline() -> None:
    """전체 파이프라인 실행"""
    _configure_utf8_stdio()
    project_root = Path(__file__).resolve().parent
    if cleanup_legacy_files(project_root) > 0:
        print()
    _ensure_data_dirs()

    fetcher = ArxivFetcher(category="cs.AI", limit=15, min_delay=3.0, max_delay=5.0)
    parser = PdfParser(table_strategy="lines_strict")
    storage = DataStorage(output_path=RAW_DATA_DIR / "crawled_papers.jsonl")
    rag_processor = RagProcessor(db_path=str(CHROMA_DIR))
    debated_base_ids = _load_debated_base_ids()

    # 1. 메타데이터 수집
    print("\n" + "=" * 60)
    print("📚 arXiv 논문 수집 파이프라인 (수집 → RAG → raw_data_queue)")
    print("=" * 60)

    papers: list[PaperMetadata] = []
    try:
        papers = fetcher.fetch_metadata_list()
    except Exception as e:
        print(f"❌ 수집 단계 예외: {e}")
        _send_telegram_notification(
            "🚨 arXiv 자동 수집 실패\n"
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"실패 단계: 메타데이터 수집\n"
            f"오류: {str(e)[:500]}"
        )
        return

    if not papers:
        print("⚠️  수집된 논문이 없습니다.")
        _send_telegram_notification(
            "ℹ️ arXiv 자동 수집 스킵\n"
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "사유: 수집된 논문이 없습니다."
        )
        return

    print(f"\n✅ {len(papers)}개 논문 메타데이터 수집 완료\n")

    # 2. 각 논문에 대해 PDF 다운로드 → 파싱 → raw_data_queue 저장 → RAG 적재
    success_count = 0
    debate_dedupe_skipped = 0
    success_papers: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        for i, paper in enumerate(papers, start=1):
            print("-" * 50)
            print(f"📄 [{i}/{len(papers)}] {paper.paper_id} - {paper.title[:50]}...")
            print("-" * 50)

            base_paper_id = normalize_paper_id(paper.paper_id)
            if base_paper_id and base_paper_id in debated_base_ids:
                debate_dedupe_skipped += 1
                print(f"  ⏭️  건너뜀 (이미 토론한 논문, 선필터): {paper.paper_id} -> {base_paper_id}")
                continue

            pdf_path = tmpdir_path / f"{paper.paper_id}.pdf"

            # PDF 다운로드
            try:
                print("  ⬇️  PDF 다운로드 중...")
                if not fetcher.download_pdf(paper.pdf_url, str(pdf_path)):
                    print("  ⏭️  건너뜀 (다운로드 실패)")
                    continue
                print("  ✓ 다운로드 완료")
            except Exception as e:
                print(f"  ❌ 다운로드 예외: {e}")
                continue

            # PDF → 마크다운 파싱
            try:
                print("  📝 마크다운 파싱 중...")
                markdown_content = parser.to_markdown(pdf_path)
                if not markdown_content:
                    print("  ⏭️  건너뜀 (파싱 실패)")
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
                    success_papers.append((paper.paper_id, paper.title))
                    print(f"  💾 저장 완료 → {storage.output_path}")
                else:
                    print("  ⏭️  건너뜀 (저장 실패)")
                    continue
            except Exception as e:
                print(f"  ❌ 저장 예외: {e}")
                continue

            # RAG: Chroma DB 적재
            try:
                print("  🔗 RAG 청킹 및 Chroma 적재 중...")
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

            # 임시 PDF 삭제
            DataStorage.remove_temp_pdf(pdf_path)

    print("\n" + "=" * 60)
    print(f"🎉 파이프라인 완료: {success_count}/{len(papers)}개 논문 처리 성공")
    if debate_dedupe_skipped:
        print(f"   참고: 토론 완료 인덱스 선필터로 {debate_dedupe_skipped}건 스킵")
    print("=" * 60 + "\n")

    # 텔레그램 알림 (TELEGRAM_TOKEN, ALLOWED_CHAT_ID 설정 시)
    if success_papers:
        lines = [f"• {pid}: {title[:60]}{'...' if len(title) > 60 else ''}" for pid, title in success_papers]
        preview_lines = lines[:10]
        msg = (
            "🔔 arXiv 자동 수집 알림\n"
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"처리 결과: {success_count}개 논문 수집 및 RAG 적재 완료\n"
            + (
                f"토론 중복 선필터 스킵: {debate_dedupe_skipped}건\n\n"
                if debate_dedupe_skipped
                else "\n"
            )
            + "\n"
            "[신규 논문]\n"
            + "\n".join(preview_lines)
        )
        if len(success_papers) > 10:
            msg += f"\n\n... 외 {len(success_papers) - 10}개"
        _send_telegram_notification(msg)
    else:
        _send_telegram_notification(
            "ℹ️ arXiv 자동 수집 스킵\n"
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "사유: 처리 성공한 논문이 없습니다."
        )


if __name__ == "__main__":
    run_pipeline()
