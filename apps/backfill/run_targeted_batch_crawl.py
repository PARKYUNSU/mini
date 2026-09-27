#!/usr/bin/env python3
"""
타겟팅 배치 크롤링 (Targeted Batch Crawling)

- **Phase 3.5 (기본)**: 9개 주제·총 560편 상한, 제출일 기본 2022-01-01~2026-12-31,
  키워드 주제는 ``sortBy=relevance`` (arXiv API).
- **``--legacy-topics``**: 예전 주제·기간 기본 2023-01-01~오늘.
- 중복: JSONL + (선택) Chroma ``--chroma-dedup``.
- 수식: ``latex_equation_postprocess`` + ``DataStorage.build_paper_record`` 에서 LaTeX 보정.

실행 예:
  cd /path/to/mini && PYTHONPATH=. .venv/bin/python -m apps.backfill.run_targeted_batch_crawl \\
    >> logs/targeted_batch_crawl.log 2>&1 &
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import tempfile
import time
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.config.agent_config import CHROMA_DB_DIR, COLLECTION_NAME  # noqa: E402
from core.config.chroma_lock import chroma_write_lock  # noqa: E402
from pipelines.ingest.arxiv_fetcher import ArxivFetcher, PaperMetadata  # noqa: E402
from pipelines.ingest.cleanup import cleanup_legacy_files  # noqa: E402
from pipelines.ingest.data_storage import DataStorage, normalize_paper_id  # noqa: E402
from pipelines.ingest.pdf_parser import PdfParser  # noqa: E402
from pipelines.ingest.rag_processor import RagProcessor  # noqa: E402

load_dotenv()

RAW_DATA_DIR = Path("./raw_data_queue")
CHROMA_DIR = CHROMA_DB_DIR
DEBATE_INDEX_PATH = Path("./finetune_datasets/debated_paper_ids.jsonl")

# arXiv API: IP 보호 (요청마다, ArxivFetcher와 동일 스케일)
API_MIN_DELAY = 3.0
API_MAX_DELAY = 5.0

# Phase 3.5 기본 기간: 제출일 2022~2026 (환경변수 PH35_START_DATE / PH35_END_DATE 로 덮어쓰기)
DEFAULT_START_DATE = os.getenv("PH35_START_DATE", "2022-01-01")
_DEFAULT_END = os.getenv("PH35_END_DATE", "2026-12-31")

# 주제별 검색식 (arXiv ``all``) + 목표 신규 저장 건수 — 총 560편 (SOTA 타겟팅)
TARGET_TOPICS: list[tuple[str, str, int]] = [
    ("graph_rag", '(all:"Graph RAG" OR ti:"Graph RAG" OR abs:"Graph RAG")', 100),
    (
        "knowledge_graph",
        '((all:"Knowledge Graph" OR ti:"Knowledge Graph") AND '
        '(all:LLM OR all:"large language model" OR all:RAG OR all:"language model"))',
        100,
    ),
    (
        "vlm",
        '(all:"Vision Language Model" OR all:VLM OR all:"Vision-Language" OR all:"vision language")',
        100,
    ),
    (
        "mamba_ssm",
        '(all:Mamba OR all:"State Space Model" OR all:"state space models" OR all:SSM)',
        50,
    ),
    (
        "slm_edge",
        '(all:"Small Language Model" OR all:SLM OR all:"Edge AI" OR all:"on-device" OR all:"on device")',
        50,
    ),
    (
        "embodied_robotics",
        '(all:"Embodied AI" OR all:Robotics OR all:"robot learning" OR all:"robotic manipulation")',
        50,
    ),
    ("gnn", '(all:"Graph Neural Network" OR all:GNN OR ti:GNN OR abs:GNN)', 50),
    ("rnn", '(all:RNN OR all:"Recurrent Neural Network" OR all:"recurrent neural")', 30),
    (
        "jailbreak_alignment",
        '(all:Jailbreak OR all:"AI alignment" OR all:Alignment OR all:"red teaming" OR all:"LLM safety")',
        30,
    ),
]

# 이전 기본 타겟 (``--legacy-topics`` 시 사용)
LEGACY_TARGET_TOPICS: list[tuple[str, str, int]] = [
    ("agentic_ai", '(all:"Agentic RAG" OR all:"LLM Agent")', 200),
    (
        "graph_rag",
        '(all:"Graph RAG" OR ((all:"Knowledge Graph") AND (all:"LLM")))',
        200,
    ),
    ("long_context", '(all:"Long Context LLM" OR all:"Context Window Extension")', 150),
    ("hallucination", '(all:"LLM Hallucination" OR all:"Factuality in LLM")', 150),
    ("multimodal", '(all:"Multimodal RAG" OR all:"Vision-Language Model")', 200),
    ("retrieval_opt", '(all:"Semantic Chunking" OR all:"Cross-encoder Reranking")', 100),
]


def _configure_utf8_stdio() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace", line_buffering=True, write_through=True)
            except Exception:
                pass


def _load_debated_base_ids() -> set[str]:
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
        print(f"⚠️ 토론 인덱스 로드 실패: {e}")
    return ids


LEGACY_DEFAULT_START = "2023-01-01"


def _published_in_range(paper: PaperMetadata, start_d: date, end_d: date) -> bool:
    """제출/게시 일시가 [start_d, end_d] 안인지 (API submittedDate 보조 검증)."""
    raw = (paper.published or "").strip()
    if not raw:
        return False
    try:
        d = datetime.strptime(raw[:10], "%Y-%m-%d").date()
        return start_d <= d <= end_d
    except (ValueError, TypeError):
        return False


def _load_chroma_paper_ids(db_path: Path, collection_name: str, *, batch: int = 2000) -> set[str]:
    """Chroma 컬렉션에서 paper_id 수집 (배치 페이징)."""
    out: set[str] = set()
    if not db_path.exists():
        return out
    try:
        import chromadb
    except ImportError:
        print("⚠️ chromadb 미설치 — Chroma 중복 스킵 생략")
        return out

    try:
        client = chromadb.PersistentClient(path=str(db_path))
        coll = client.get_collection(collection_name)
    except Exception as e:
        print(f"⚠️ Chroma 로드 실패(중복 스킵 생략): {e}")
        return out

    offset = 0
    while True:
        try:
            r = coll.get(include=["metadatas"], limit=batch, offset=offset)
        except TypeError:
            # 구버전: offset 미지원
            r = coll.get(include=["metadatas"])
            offset = -1
        metas = r.get("metadatas") or []
        if not metas:
            break
        for m in metas:
            if not m:
                continue
            pid = normalize_paper_id(str(m.get("paper_id", "")).strip())
            if pid:
                out.add(pid)
        if offset < 0 or len(metas) < batch:
            break
        offset += batch
    return out


def ensure_data_dirs() -> None:
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(CHROMA_DIR, exist_ok=True)


def run_targeted_batch(
    *,
    start_date: str,
    end_date: str,
    category: str,
    batch_size: int,
    topics: list[tuple[str, str, int]],
    chroma_dedup: bool,
    time_limit_sec: int | None,
    dry_run: bool,
    batch_tag: str = "phase35_2022_2026",
) -> None:
    _configure_utf8_stdio()
    project_root = Path(__file__).resolve().parent
    if cleanup_legacy_files(project_root) > 0:
        print()

    ensure_data_dirs()
    start_d = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_d = datetime.strptime(end_date, "%Y-%m-%d").date()

    parser = PdfParser(table_strategy="lines_strict")
    storage = DataStorage(output_path=RAW_DATA_DIR / "crawled_papers.jsonl")
    rag_processor = RagProcessor(db_path=str(CHROMA_DIR))
    debated = _load_debated_base_ids()

    skip_ids: set[str] = set(storage._known_paper_ids)
    skip_ids |= debated
    if chroma_dedup:
        chroma_ids = _load_chroma_paper_ids(CHROMA_DIR, COLLECTION_NAME)
        print(f"   Chroma 기존 paper_id: {len(chroma_ids):,}건 (스킵 집합에 합침)")
        skip_ids |= chroma_ids
    else:
        print("   Chroma 중복 스킵: 끔 (--chroma-dedup 로 켤 수 있음)")

    print("\n" + "=" * 60)
    print("🎯 arXiv 타겟팅 배치 크롤링")
    print(f"   기간(제출일): {start_date} ~ {end_date}")
    print(f"   카테고리: {category}")
    print(f"   API 딜레이: {API_MIN_DELAY}~{API_MAX_DELAY}초/요청")
    print(f"   JSONL·토론 인덱스 스킵 집합: {len(skip_ids):,} paper_id")
    print(f"   주제 수: {len(topics)}, dry_run={dry_run}")
    print("=" * 60 + "\n")

    total_success = 0
    total_skipped_dup = 0
    total_skipped_date = 0
    pipeline_start = time.time()

    for topic_key, extra_query, cap in topics:
        if time_limit_sec and (time.time() - pipeline_start) >= time_limit_sec:
            print(f"\n⏱️ 시간 제한({time_limit_sec}s) 도달. 종료.")
            break

        topic_success = 0
        topic_seen = 0
        start_offset = 0

        fetcher = ArxivFetcher(
            category=category,
            limit=batch_size,
            min_delay=API_MIN_DELAY,
            max_delay=API_MAX_DELAY,
            extra_query=extra_query,
            sort_by=ArxivFetcher.SORT_RELEVANCE if extra_query else ArxivFetcher.SORT_SUBMITTED,
            sort_order="descending",
        )
        print("\n" + "-" * 60)
        print(f"📌 주제 [{topic_key}] 목표 신규 {cap}편")
        print(f"   검색식: {extra_query}")
        api_total = fetcher.get_search_total_results(start_date, end_date)
        if api_total is not None:
            print(f"   API 총 결과(대략): {api_total:,}건")

        while topic_success < cap:
            if time_limit_sec and (time.time() - pipeline_start) >= time_limit_sec:
                print(f"\n⏱️ 시간 제한 도달 (주제 {topic_key} 중단).")
                break

            try:
                papers = fetcher.fetch_metadata_batch(
                    start=start_offset,
                    limit=batch_size,
                    start_date=start_date,
                    end_date=end_date,
                )
            except Exception as e:
                print(f"❌ 메타데이터 수집 실패 offset={start_offset}: {e}")
                break

            if not papers:
                print(f"⚠️ 주제 [{topic_key}] 더 이상 결과 없음 (offset={start_offset}).")
                break

            print(f"   배치 offset={start_offset} 수신 {len(papers)}건")

            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir_path = Path(tmpdir)
                for paper in papers:
                    if topic_success >= cap:
                        break
                    if time_limit_sec and (time.time() - pipeline_start) >= time_limit_sec:
                        break

                    topic_seen += 1
                    base_id = normalize_paper_id(paper.paper_id)
                    if not base_id:
                        continue

                    if not _published_in_range(paper, start_d, end_d):
                        total_skipped_date += 1
                        continue

                    if base_id and base_id in skip_ids:
                        total_skipped_dup += 1
                        continue

                    if dry_run:
                        print(f"  [dry-run] would ingest {paper.paper_id} — {paper.title[:60]}...")
                        topic_success += 1
                        total_success += 1
                        skip_ids.add(base_id)
                        continue

                    pdf_path = tmpdir_path / f"{paper.paper_id}.pdf"
                    print("-" * 40)
                    print(f"📄 {paper.paper_id} — {paper.title[:55]}...")

                    try:
                        print("  ⬇️ PDF...")
                        if not fetcher.download_pdf(paper.pdf_url, str(pdf_path)):
                            continue
                    except Exception as e:
                        print(f"  ❌ 다운로드: {e}")
                        continue

                    try:
                        print("  📝 파싱...")
                        markdown_content = parser.to_markdown(pdf_path)
                        if not markdown_content:
                            continue
                    except Exception as e:
                        print(f"  ❌ 파싱: {e}")
                        continue

                    record = storage.build_paper_record(
                        paper_id=paper.paper_id,
                        title=paper.title,
                        authors=paper.authors,
                        abstract=paper.abstract,
                        published=paper.published,
                        pdf_url=paper.pdf_url,
                        markdown_content=markdown_content,
                    )
                    record["target_topic"] = topic_key
                    record["target_batch"] = batch_tag

                    if not storage.save_paper(record):
                        continue

                    topic_success += 1
                    total_success += 1
                    skip_ids.add(base_id)

                    try:
                        print("  🔗 RAG...")
                        with chroma_write_lock():
                            rag_processor.add_paper(
                                markdown_content=markdown_content,
                                title=paper.title,
                                published=paper.published,
                                pdf_url=paper.pdf_url,
                                paper_id=paper.paper_id,
                                abstract=paper.abstract,
                            )
                    except Exception as e:
                        print(f"  ⚠️ RAG 실패(파일은 저장됨): {e}")

                    DataStorage.remove_temp_pdf(pdf_path)
                    del markdown_content
                    gc.collect()
                    time.sleep(1.0)

            start_offset += len(papers)
            if len(papers) < batch_size:
                break

        print(
            f"✅ 주제 [{topic_key}] 완료: 신규 {topic_success}편 "
            f"(누적 전체 {total_success}편, 본 메타 {topic_seen}건)"
        )

    print("\n" + "=" * 60)
    print(
        f"🎉 타겟 배치 종료: 신규 저장 {total_success:,}편 | "
        f"중복 스킵 {total_skipped_dup:,} | 날짜 스킵 {total_skipped_date:,}"
    )
    print("=" * 60 + "\n")


def _parse_topic_filter(
    only: str | None, topics: list[tuple[str, str, int]]
) -> list[tuple[str, str, int]] | None:
    if not only or not str(only).strip():
        return None
    allowed = {t[0]: t for t in topics}
    keys = [k.strip() for k in str(only).split(",") if k.strip()]
    out: list[tuple[str, str, int]] = []
    for k in keys:
        if k not in allowed:
            raise ValueError(f"알 수 없는 주제 키: {k}. 가능: {list(allowed.keys())}")
        out.append(allowed[k])
    return out


def main() -> None:
    today = date.today().isoformat()
    parser = argparse.ArgumentParser(
        description="주제별 상한 타겟팅 arXiv 크롤링 (Phase 3.5: 기본 2022~2026, 관련도 정렬)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--legacy-topics",
        action="store_true",
        help="이전 주제 세트(에이전틱·롱컨텍스트 등) + 기간 기본값 2023-01-01~오늘",
    )
    parser.add_argument(
        "-s",
        "--start-date",
        default=None,
        help="제출일 하한 (YYYY-MM-DD). 생략 시 Phase3.5→2022-01-01, --legacy-topics→2023-01-01",
    )
    parser.add_argument(
        "-e",
        "--end-date",
        default=None,
        help="제출일 상한. 생략 시 Phase3.5→2026-12-31, --legacy-topics→오늘",
    )
    parser.add_argument("-c", "--category", default="cs.AI", help="arXiv 카테고리")
    parser.add_argument("-b", "--batch-size", type=int, default=100, help="페이지당 max_results")
    parser.add_argument(
        "--only-topic",
        type=str,
        default=None,
        metavar="KEYS",
        help="쉼표로 구분한 주제만 실행 (예: agentic_ai,graph_rag). 전체는 생략.",
    )
    parser.add_argument(
        "--chroma-dedup",
        action="store_true",
        help="ChromaDB에 이미 있는 paper_id도 스킵 (대량이면 초기 스캔 시간 소요)",
    )
    parser.add_argument("-t", "--time-limit", type=int, default=None, metavar="SEC", help="전체 최대 실행 시간(초)")
    parser.add_argument("--dry-run", action="store_true", help="메타만 확인·카운트 (PDF/저장 안 함)")
    args = parser.parse_args()

    legacy = bool(args.legacy_topics)
    topics = LEGACY_TARGET_TOPICS if legacy else TARGET_TOPICS
    start_date = args.start_date or (LEGACY_DEFAULT_START if legacy else DEFAULT_START_DATE)
    end_date = args.end_date or (today if legacy else _DEFAULT_END)

    if args.only_topic:
        try:
            topics = _parse_topic_filter(args.only_topic, topics)
        except ValueError as e:
            parser.error(str(e))

    run_targeted_batch(
        start_date=start_date,
        end_date=end_date,
        category=args.category,
        batch_size=max(1, min(args.batch_size, 2000)),
        topics=topics,
        chroma_dedup=args.chroma_dedup,
        time_limit_sec=args.time_limit,
        dry_run=args.dry_run,
        batch_tag="sota_2023p" if legacy else "phase35_2022_2026",
    )


if __name__ == "__main__":
    main()
