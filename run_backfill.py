#!/usr/bin/env python3
"""
과거 데이터 일괄 수집 (Backfill) - 기간 기반
- start_date, end_date로 수집 기간 지정 (정보 오염 방지)
- arXiv API submittedDate 필터 + 페이징
- MIN_DELAY~MAX_DELAY(기본 60~120초) 랜덤 딜레이로 Rate Limit 방지
  (페이지 간, API 호출 전, PDF 다운로드 전 각각 적용)
- raw_data_queue 저장 + ChromaDB 적재
"""

import argparse
import json
import os
import random
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import telebot

from src.arxiv_fetcher import ArxivFetcher, PaperMetadata
from src.cleanup import cleanup_legacy_files
from src.data_storage import DataStorage, normalize_paper_id
from src.pdf_parser import PdfParser
from src.rag_processor import RagProcessor

load_dotenv()

# 데이터 저장 경로
RAW_DATA_DIR = Path("./raw_data_queue")
CHROMA_DIR = Path("./chroma_db")
DEBATE_INDEX_PATH = Path("./finetune_datasets/debated_paper_ids.jsonl")

# 기본값 (최신 1~2년 치 권장)
DEFAULT_START_DATE = "2024-01-01"
DEFAULT_END_DATE = "2024-12-31"
DEFAULT_BATCH_SIZE = 15
MIN_DELAY = 60
MAX_DELAY = 120


def _configure_utf8_stdio() -> None:
    """cron 환경에서도 한글 로그가 최대한 UTF-8로 남도록 표준 입출력 인코딩 고정."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace", line_buffering=True, write_through=True)
            except Exception:
                pass


def _get_telegram_targets() -> tuple[str, list[str]]:
    token = os.getenv("TELEGRAM_TOKEN") or ""
    chat_ids = [cid.strip() for cid in (os.getenv("ALLOWED_CHAT_ID") or "").split(",") if cid.strip()]
    return token, chat_ids


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
        bot = telebot.TeleBot(token)
        for cid in chat_ids:
            bot.send_message(cid, message)
            print(f"✅ 텔레그램 알림 전송 성공: chat_id={cid}")
        return True
    except Exception as e:
        print(f"⚠️ 텔레그램 알림 전송 실패: {e}")
        return False


def ensure_data_dirs() -> None:
    """데이터 폴더 자동 생성"""
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


def run_backfill(
    start_date: str = DEFAULT_START_DATE,
    end_date: str = DEFAULT_END_DATE,
    batch_size: int = DEFAULT_BATCH_SIZE,
    category: str = "cs.AI",
    time_limit_sec: int | None = None,
) -> None:
    """
    기간 기반 과거 논문 수집 후 raw_data_queue와 ChromaDB에 적재.
    submittedDate 필터로 해당 기간 논문만 가져옵니다.

    Args:
        start_date: 수집 시작일 (YYYY-MM-DD)
        end_date: 수집 종료일 (YYYY-MM-DD)
        batch_size: API 한 번에 가져올 개수 (10~20 권장)
        category: arXiv 카테고리
        time_limit_sec: 최대 실행 시간(초). None이면 제한 없음.
    """
    _configure_utf8_stdio()
    project_root = Path(__file__).resolve().parent
    if cleanup_legacy_files(project_root) > 0:
        print()

    ensure_data_dirs()

    fetcher = ArxivFetcher(
        category=category,
        limit=batch_size,
        min_delay=MIN_DELAY,
        max_delay=MAX_DELAY,
    )
    parser = PdfParser(table_strategy="lines_strict")
    storage = DataStorage(output_path=RAW_DATA_DIR / "crawled_papers.jsonl")
    rag_processor = RagProcessor(db_path=str(CHROMA_DIR))
    debated_base_ids = _load_debated_base_ids()
    print(f"   토론 완료 인덱스(베이스 ID) 선필터: {len(debated_base_ids):,}건")

    print("\n" + "=" * 60)
    print("📚 arXiv 백필 (기간 기반 과거 데이터 수집)")
    print(f"   기간: {start_date} ~ {end_date}")
    print(f"   배치: {batch_size}개, 카테고리: {category}")
    if time_limit_sec:
        print(f"   ⏱️  시간 제한: {time_limit_sec // 3600}시간 {time_limit_sec % 3600 // 60}분")
    print("=" * 60)

    print("📊 arXiv API 총 검색 결과(opensearch:totalResults) 조회 중...")
    api_total = fetcher.get_search_total_results(start_date, end_date)
    if api_total is not None:
        print(f"   → 이 쿼리 기준 총 {api_total:,}건 (페이징 끝까지 가면 메타데이터 수신 합이 이 값과 같아야 함)")
    else:
        print("   → 총건수를 가져오지 못했습니다. 로그의 메타 수신 합만 참고하세요.")
    print()

    total_success = 0
    total_fetched = 0
    debate_dedupe_skipped = 0
    success_papers: list[tuple[str, str]] = []
    start_offset = 0
    pipeline_start = time.time()
    backfill_429_retries = 0

    while True:
        if time_limit_sec and (time.time() - pipeline_start) >= time_limit_sec:
            print(f"\n⏱️  시간 제한({time_limit_sec}초) 도달. 수집 종료.")
            break

        # 페이지 간 MIN_DELAY~MAX_DELAY(60~120초) 랜덤 딜레이 (첫 페이지 제외)
        if start_offset > 0:
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"\n⏳ Rate Limit 방지: {delay:.1f}초 대기 중...")
            time.sleep(delay)

        # 메타데이터 배치 수집 (submittedDate 필터 적용)
        papers: list[PaperMetadata] = []
        try:
            papers = fetcher.fetch_metadata_batch(
                start=start_offset,
                limit=batch_size,
                start_date=start_date,
                end_date=end_date,
            )
        except Exception as e:
            # arXiv export은 burst 요청 시 429로 레이트리밋이 걸릴 수 있음.
            # 이 경우에는 start_offset을 그대로 둔 채 잠시 대기 후 같은 페이지를 재시도한다.
            try:
                status_code = getattr(getattr(e, "response", None), "status_code", None)
                if status_code == 429:
                    backfill_429_retries += 1
                    max_retries = int(os.getenv("ARXIV_429_MAX_RETRY", "8"))
                    if backfill_429_retries > max_retries:
                        print(
                            f"❌ 429 재시도 초과({backfill_429_retries}/{max_retries}). start={start_offset}: {e}"
                        )
                        raise

                    retry_after = None
                    try:
                        retry_after = getattr(getattr(e, "response", None), "headers", {}).get("Retry-After")
                    except Exception:
                        retry_after = None

                    if retry_after and str(retry_after).strip().isdigit():
                        wait_sec = int(str(retry_after).strip())
                    else:
                        wait_sec = int(os.getenv("ARXIV_429_BACKOFF_SEC", "180"))

                    print(
                        f"⚠️ arXiv export 429 레이트리밋(start={start_offset}). {wait_sec}s 대기 후 동일 offset 재시도... "
                        f"(retry {backfill_429_retries}/{max_retries})"
                    )
                    time.sleep(wait_sec)
                    continue
            except Exception:
                # 429 판별이 실패해도 아래의 일반 실패 처리로 흘려보낸다.
                pass

            print(f"❌ 메타데이터 수집 실패 (start={start_offset}): {e}")
            _send_telegram_notification(
                "🚨 arXiv 백필 수집 실패\n"
                f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"수집 기간: {start_date} ~ {end_date}\n"
                f"실패 단계: 메타데이터 수집(start={start_offset})\n"
                f"오류: {str(e)[:500]}"
            )
            break

        if not papers:
            print(f"\n⚠️  start={start_offset}에서 더 이상 논문 없음. 수집 종료.")
            break

        print(f"\n✅ [{start_offset + 1}~{start_offset + len(papers)}] {len(papers)}개 메타데이터 수집")

        # 각 논문 처리 (main.py와 동일한 파이프라인)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            for i, paper in enumerate(papers, start=1):
                global_idx = start_offset + i
                print("-" * 50)
                print(f"📄 [{global_idx}] {paper.paper_id} - {paper.title[:50]}...")
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

                # JSONL 저장 (raw_data_queue)
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
                        total_success += 1
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
                    print(f"  ✓ RAG 완료 ({chunk_count}개 청크)")
                except Exception as e:
                    print(f"  ❌ RAG 예외 (건너뜀): {e}")

                DataStorage.remove_temp_pdf(pdf_path)

        total_fetched += len(papers)
        start_offset += batch_size

        if len(papers) < batch_size:
            print(f"\n⚠️  요청한 {batch_size}개 미만 수신. 수집 종료.")
            break

    print("\n" + "=" * 60)
    print(f"🎉 백필 종료: 저장 성공 {total_success:,}건 / 메타데이터 수신 합 {total_fetched:,}건")
    if api_total is not None:
        print(f"   arXiv API 총건수(totalResults): {api_total:,}건")
        if total_fetched == api_total:
            print("   → 수신 합 = API 총건: 해당 기간·카테고리 목록 페이징을 끝까지 본 상태로 보면 됩니다.")
        elif total_fetched < api_total:
            print("   → 수신 합 < API 총건: 시간 제한·오류·중지 등으로 중간에 끊겼을 수 있습니다.")
    if total_fetched > 0 and total_success < total_fetched:
        print("   참고: 수신 대비 저장 성공이 적음 (다운로드·파싱 실패 또는 이미 저장된 중복 등)")
    print("=" * 60 + "\n")

    stat_bits: list[str] = []
    if api_total is not None:
        stat_bits.append(f"API총건: {api_total:,}")
    stat_bits.append(f"메타수신합: {total_fetched:,}")
    stat_bits.append(f"저장성공: {total_success:,}")
    if debate_dedupe_skipped:
        stat_bits.append(f"토론중복선필터: {debate_dedupe_skipped:,}")
    if api_total is not None:
        if total_fetched == api_total:
            stat_bits.append("페이징완주")
        elif total_fetched < api_total:
            stat_bits.append("페이징미완주가능")
    stats_line = " | ".join(stat_bits)

    # 텔레그램 알림 (TELEGRAM_TOKEN, ALLOWED_CHAT_ID 설정 시)
    if success_papers:
        lines = [f"• {pid}: {title[:60]}{'...' if len(title) > 60 else ''}" for pid, title in success_papers]
        preview_lines = lines[:15]
        msg = (
            "🔔 arXiv 백필 수집 알림\n"
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"처리 결과: {total_success}개 논문 수집 및 RAG 적재 완료\n"
            f"수집 기간: {start_date} ~ {end_date} ({category})\n"
            f"{stats_line}\n\n"
            "[신규 논문]\n"
            + "\n".join(preview_lines)
        )
        if len(success_papers) > 15:
            msg += f"\n\n... 외 {len(success_papers) - 15}개"
        if len(msg) > 4000:
            msg = msg[:3990] + "\n...(생략)"
        _send_telegram_notification(msg)
    else:
        _send_telegram_notification(
            "ℹ️ arXiv 백필 수집 스킵\n"
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"수집 기간: {start_date} ~ {end_date} ({category})\n"
            f"{stats_line}\n"
            "사유: 처리 성공한 논문이 없습니다."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="arXiv 기간 기반 과거 논문 일괄 수집 (Backfill)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-s", "--start-date",
        type=str,
        default=DEFAULT_START_DATE,
        help="수집 시작일 (YYYY-MM-DD)",
    )
    parser.add_argument(
        "-e", "--end-date",
        type=str,
        default=DEFAULT_END_DATE,
        help="수집 종료일 (YYYY-MM-DD)",
    )
    parser.add_argument(
        "-b", "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="API 한 번에 가져올 개수 (10~20 권장)",
    )
    parser.add_argument(
        "-c", "--category",
        type=str,
        default="cs.AI",
        help="arXiv 카테고리",
    )
    parser.add_argument(
        "-t", "--time-limit",
        type=int,
        default=None,
        metavar="SEC",
        help="최대 실행 시간(초). 예: 7200 = 2시간",
    )
    args = parser.parse_args()

    run_backfill(
        start_date=args.start_date,
        end_date=args.end_date,
        batch_size=args.batch_size,
        category=args.category,
        time_limit_sec=args.time_limit,
    )


if __name__ == "__main__":
    main()
