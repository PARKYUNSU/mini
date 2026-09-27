#!/usr/bin/env python3
"""
arXiv 논문 자동 수집 및 파싱 파이프라인
- ArxivFetcher → PdfParser → DataStorage → RagProcessor
- 역할: 수집 → ChromaDB 적재 → raw_data_queue/ 원본 저장 (Q&A 생성은 llm_debate_scheduler 전담)
- 스캔 폭: ``ARXIV_INGEST_BATCH_SIZE``(기본 50) · ``ARXIV_INGEST_MAX_SCAN``(기본 200) · 선택 ``ARXIV_INGEST_TARGET_NEW``
- 메타 페이징 시 ``ARXIV_INGEST_PAGE_SLEEP_SEC``(기본 18)·요청 전 지연 ``ARXIV_INGEST_MIN_DELAY_SEC``/``MAX`` 로 arXiv **429** 완화.
  429 발생 시 ``ARXIV_429_BACKOFF_SEC``·``ARXIV_429_MAX_RETRY``(백필과 동일)로 동일 offset 재시도.
"""

import os
import json
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import telebot

from core.config.agent_config import CHROMA_DB_DIR
from core.execution.retry_utils import retry_on_network_error
from pipelines.ingest.arxiv_fetcher import ArxivFetcher, PaperMetadata
from pipelines.ingest.cleanup import cleanup_legacy_files
from pipelines.ingest.data_storage import DataStorage, normalize_paper_id
from pipelines.ingest.pdf_parser import PdfParser
from pipelines.ingest.rag_processor import RagProcessor

# .env에서 환경 변수 로드 (GEMINI_API_KEY 등)
_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_ROOT / ".env", override=True)
load_dotenv()

# 데이터 저장 경로 (폴더 자동 생성)
RAW_DATA_DIR = Path("./raw_data_queue")
CHROMA_DIR = CHROMA_DB_DIR
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


def _arxiv_ingest_batch_size() -> int:
    """API ``max_results`` 한 번에 가져올 상한 (1~300)."""
    try:
        n = int((os.getenv("ARXIV_INGEST_BATCH_SIZE") or "50").strip())
    except ValueError:
        n = 50
    return max(1, min(n, 300))


def _arxiv_ingest_max_scan() -> int:
    """한 실행에서 메타데이터를 최대 몇 편까지 나열할지 (중복이 많을수록 넓게)."""
    try:
        n = int((os.getenv("ARXIV_INGEST_MAX_SCAN") or "200").strip())
    except ValueError:
        n = 200
    b = _arxiv_ingest_batch_size()
    return max(b, min(n, 2000))


def _arxiv_ingest_target_new() -> int:
    """신규 JSONL 저장이 이 수에 도달하면 같은 실행에서 나머지 메타는 건너뜀. 0 = 비활성."""
    try:
        n = int((os.getenv("ARXIV_INGEST_TARGET_NEW") or "0").strip())
    except ValueError:
        n = 0
    return max(0, min(n, 500))


def _arxiv_ingest_page_sleep_sec() -> float:
    """메타 페이징 시 페이지마다 추가 대기.arXiv 429 완화."""
    try:
        v = float((os.getenv("ARXIV_INGEST_PAGE_SLEEP_SEC") or "18").strip())
    except ValueError:
        v = 18.0
    return max(0.0, min(600.0, v))


def _fetch_papers_paged(fetcher: ArxivFetcher, *, batch: int, cap: int) -> list[PaperMetadata]:
    """submittedDate 최신순으로 offset 페이징해 최대 ``cap``편까지 메타 수집.

    arXiv export는 연속 요청에 민감해 429가 나기 쉽다. 페이지 간 ``ARXIV_INGEST_PAGE_SLEEP_SEC`` 대기와,
    ``run_backfill`` 과 동일한 429 시 동일 offset 재시도를 적용한다.
    """
    papers: list[PaperMetadata] = []
    offset = 0
    retry429_count = 0
    max_429 = int(os.getenv("ARXIV_429_MAX_RETRY", "12"))
    backoff_sec = int(os.getenv("ARXIV_429_BACKOFF_SEC", "180"))
    page_sleep = _arxiv_ingest_page_sleep_sec()

    while len(papers) < cap:
        need = min(batch, cap - len(papers))
        if offset > 0 and page_sleep > 0:
            print(f"⏳ arXiv ingest 페이지 간격: {page_sleep:.1f}s (env ARXIV_INGEST_PAGE_SLEEP_SEC)", flush=True)
            time.sleep(page_sleep)

        try:
            batch_list = fetcher.fetch_metadata_batch(start=offset, limit=need)
            retry429_count = 0
        except Exception as e:
            status_code = getattr(getattr(e, "response", None), "status_code", None)
            if status_code == 429:
                retry429_count += 1
                if retry429_count > max_429:
                    raise
                retry_after = None
                try:
                    retry_after = getattr(getattr(e, "response", None), "headers", {}).get("Retry-After")
                except Exception:
                    retry_after = None
                if retry_after and str(retry_after).strip().isdigit():
                    wait_sec = int(str(retry_after).strip())
                else:
                    wait_sec = int(backoff_sec * min(retry429_count, 5))
                print(
                    f"⚠️ arXiv 429 (ingest) offset={offset}. {wait_sec}s 대기 후 동일 페이지 재시도 "
                    f"({retry429_count}/{max_429})",
                    flush=True,
                )
                time.sleep(wait_sec)
                continue
            raise

        if not batch_list:
            break
        papers.extend(batch_list)
        offset += len(batch_list)
        if len(batch_list) < need:
            break
    return papers


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

    batch = _arxiv_ingest_batch_size()
    max_scan = _arxiv_ingest_max_scan()
    target_new = _arxiv_ingest_target_new()

    try:
        min_d = float((os.getenv("ARXIV_INGEST_MIN_DELAY_SEC") or "6").strip())
        max_d = float((os.getenv("ARXIV_INGEST_MAX_DELAY_SEC") or "14").strip())
    except ValueError:
        min_d, max_d = 6.0, 14.0
    min_d = max(1.0, min_d)
    max_d = max(min_d, max_d)
    fetcher = ArxivFetcher(category="cs.AI", limit=batch, min_delay=min_d, max_delay=max_d)
    parser = PdfParser(table_strategy="lines_strict")
    storage = DataStorage(output_path=RAW_DATA_DIR / "crawled_papers.jsonl")
    rag_processor = RagProcessor(db_path=str(CHROMA_DIR))
    debated_base_ids = _load_debated_base_ids()

    # 1. 메타데이터 수집 (페이징: 상위 N편만 보던 것을 넓혀 중복 구간을 지나 신규를 찾기 쉽게 함)
    print("\n" + "=" * 60)
    print("📚 arXiv 논문 수집 파이프라인 (수집 → RAG → raw_data_queue)")
    print(
        f"   설정: 배치={batch} · 최대 스캔={max_scan}메타"
        + (f" · 신규 목표={target_new}편(도달 시 조기 종료)" if target_new else "")
    )
    print("=" * 60)

    papers: list[PaperMetadata] = []
    try:
        papers = _fetch_papers_paged(fetcher, batch=batch, cap=max_scan)
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
    queue_duplicate_skipped = 0
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

            if base_paper_id and base_paper_id in storage._known_paper_ids:
                queue_duplicate_skipped += 1
                print(f"  ⏭️  건너뜀 (이미 저장된 논문, 중복 방지): {paper.paper_id} -> {base_paper_id}")
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
                    if target_new > 0 and success_count >= target_new:
                        print(
                            f"  🎯 신규 저장 목표 {target_new}편 달성 "
                            "(같은 실행에서 나머지 메타는 처리하지 않음)",
                            flush=True,
                        )
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
                    abstract=paper.abstract,
                )
                print(f"  ✓ RAG 완료 ({chunk_count}개 청크) → {rag_processor.db_path}")
            except Exception as e:
                print(f"  ❌ RAG 예외 (건너뜀): {e}")

            # 임시 PDF 삭제
            DataStorage.remove_temp_pdf(pdf_path)

            if target_new > 0 and success_count >= target_new:
                break

    print("\n" + "=" * 60)
    print(f"🎉 파이프라인 완료: {success_count}/{len(papers)}개 논문 처리 성공")
    if debate_dedupe_skipped:
        print(f"   참고: 토론 완료 인덱스 선필터로 {debate_dedupe_skipped}건 스킵")
    if queue_duplicate_skipped:
        print(f"   참고: 큐(JSONL)에 이미 있는 논문 {queue_duplicate_skipped}건 스킵")
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
        n = len(papers)
        if queue_duplicate_skipped == n:
            skip_msg = (
                f"메타데이터는 {n}편 받았지만, 모두 이미 crawled_papers.jsonl 에 있습니다 "
                "(최근 제출 순 상위 목록이 이전 실행과 동일)."
            )
        elif debate_dedupe_skipped == n:
            skip_msg = f"{n}편 모두 토론 완료 인덱스(선필터)에 포함되어 신규 저장 없음."
        elif queue_duplicate_skipped + debate_dedupe_skipped == n:
            skip_msg = (
                f"{n}편 중 중복 큐 {queue_duplicate_skipped}건, 토론 선필터 {debate_dedupe_skipped}건 — 신규 저장 없음."
            )
        else:
            skip_msg = (
                f"메타는 {n}편 처리했지만 다운로드·파싱·저장 중 모두 건너뛰거나 실패했습니다. "
                f"(중복 큐 {queue_duplicate_skipped}, 토론 선필터 {debate_dedupe_skipped}) 로그 참고."
            )
        _send_telegram_notification(
            "ℹ️ arXiv 자동 수집 · 신규 0건\n"
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"사유: {skip_msg}"
        )


if __name__ == "__main__":
    run_pipeline()
