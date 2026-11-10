#!/usr/bin/env python3
"""고전·핵심 AI 논문을 classics.yaml 기반으로 일괄 등록.

기존 백필(run_backfill.py)과 **별개로** 실행하며,
ArxivFetcher·PdfParser·DataStorage·RagProcessor를 그대로 재사용한다.

사용법:
    # 전체 목록 등록
    python -m apps.backfill.ingest_classics

    # 특정 논문만 (arXiv ID 직접 지정)
    python -m apps.backfill.ingest_classics --ids 1706.03762 1810.04805

    # dry-run (실제 다운로드/등록 없이 목록만 확인)
    python -m apps.backfill.ingest_classics --dry-run
"""

from __future__ import annotations

import argparse
import gc
import os
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

import requests
import yaml

# 프로젝트 루트를 PYTHONPATH에 추가
_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

from pipelines.ingest.arxiv_fetcher import PaperMetadata  # noqa: E402
from pipelines.ingest.data_storage import DataStorage, normalize_paper_id  # noqa: E402
from pipelines.ingest.pdf_parser import PdfParser  # noqa: E402
from pipelines.ingest.rag_processor import RagProcessor  # noqa: E402
from core.config.agent_config import CHROMA_DB_DIR  # noqa: E402
from core.config.chroma_lock import chroma_write_lock  # noqa: E402
from core.execution.retry_utils import retry_on_network_error  # noqa: E402

CLASSICS_YAML = Path(__file__).parent / "classics.yaml"
RAW_DATA_DIR = _ROOT / "raw_data_queue"
CHROMA_DIR = CHROMA_DB_DIR

ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_API = "http://export.arxiv.org/api/query"
DELAY_SEC = 5


@retry_on_network_error
def _get(url: str, **kwargs) -> requests.Response:
    """GET. 429 · 5xx · 연결 오류 · 시간 초과는 1 → 3 → 5분 기다려 다시 시도한다(정기 수집과 같은 도우미).
    11-10 canon_1110 에서 arXiv 429 로 38편이 재시도 없이 빠졌다."""
    resp = requests.get(url, **kwargs)
    resp.raise_for_status()  # 429 도 예외로 올려야 재시도된다
    return resp


@dataclass
class ClassicEntry:
    """classics.yaml 에서 읽은 한 항목."""

    arxiv_id: str
    note: str = ""
    title: str = ""
    pdf_url: str = ""
    published: str = ""
    authors: list[str] | None = None


def _load_classics(yaml_path: Path, filter_ids: list[str] | None = None) -> list[ClassicEntry]:
    with yaml_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries: list[ClassicEntry] = []
    for item in data.get("classics", []):
        aid = str(item.get("id", "")).strip()
        if not aid:
            continue
        if filter_ids and aid not in filter_ids:
            continue
        entries.append(
            ClassicEntry(
                arxiv_id=aid,
                note=item.get("note", ""),
                title=item.get("title", ""),
                pdf_url=item.get("pdf_url", ""),
                published=item.get("published", ""),
                authors=item.get("authors"),
            )
        )
    return entries


def _fetch_arxiv_meta(arxiv_id: str) -> PaperMetadata | None:
    """arXiv Atom API로 단일 논문 메타데이터 조회."""
    url = f"{ARXIV_API}?id_list={arxiv_id}&max_results=1"
    try:
        resp = _get(url, timeout=30)
    except requests.RequestException as e:
        print(f"  ❌ arXiv API 실패: {e}")
        return None
    try:
        root = ET.fromstring(resp.content)
        ns = "{" + ATOM_NS + "}"
        entry = root.find(f".//{ns}entry")
        if entry is None:
            print("  ⚠️  arXiv 응답에 entry 없음")
            return None

        id_el = entry.find(f"{ns}id")
        paper_id = id_el.text.split("/abs/")[-1].strip() if id_el is not None and id_el.text else arxiv_id

        title_el = entry.find(f"{ns}title")
        title = title_el.text.strip().replace("\n", " ") if title_el is not None and title_el.text else ""

        authors: list[str] = []
        for a in entry.findall(f"{ns}author"):
            name_el = a.find(f"{ns}name")
            if name_el is not None and name_el.text:
                authors.append(name_el.text.strip())

        summary_el = entry.find(f"{ns}summary")
        abstract = summary_el.text.strip().replace("\n", " ") if summary_el is not None and summary_el.text else ""

        pub_el = entry.find(f"{ns}published")
        published = pub_el.text.strip() if pub_el is not None and pub_el.text else ""

        pdf_url = ""
        for link in entry.findall(f"{ns}link"):
            if link.get("title") == "pdf":
                pdf_url = link.get("href", "")
                break
        if not pdf_url:
            pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

        return PaperMetadata(
            paper_id=paper_id,
            title=title,
            authors=authors,
            abstract=abstract,
            published=published,
            pdf_url=pdf_url,
        )
    except ET.ParseError as e:
        print(f"  ❌ XML 파싱 실패: {e}")
        return None


def _download_pdf(url: str, dest: Path) -> bool:
    try:
        resp = _get(url, timeout=120, stream=True)
        with dest.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  ❌ PDF 다운로드 실패: {e}")
        return False


def run(
    yaml_path: Path = CLASSICS_YAML,
    filter_ids: list[str] | None = None,
    dry_run: bool = False,
) -> int:
    """실패한 편수를 돌려준다(main 은 1 이상이면 종료 코드 1)."""
    entries = _load_classics(yaml_path, filter_ids)
    if not entries:
        print("⚠️  등록할 논문이 없습니다.")
        return 0

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(CHROMA_DIR, exist_ok=True)

    storage = DataStorage(output_path=RAW_DATA_DIR / "crawled_papers.jsonl")
    parser = PdfParser(table_strategy="lines_strict")
    rag = RagProcessor(db_path=str(CHROMA_DIR))

    print("=" * 60)
    print(f"📚 고전 논문 등록 (총 {len(entries)}편)")
    if dry_run:
        print("   🧪 DRY-RUN 모드 (실제 등록 없음)")
    print("=" * 60)

    success = 0
    skipped = 0
    failed: list[str] = []

    for idx, entry in enumerate(entries, 1):
        print(f"\n{'─' * 50}")
        print(f"[{idx}/{len(entries)}] {entry.arxiv_id}  {entry.note}")
        print(f"{'─' * 50}")

        base_id = normalize_paper_id(entry.arxiv_id)
        if base_id and base_id in storage._known_paper_ids:
            print("  ⏭️  건너뜀 (이미 등록됨)")
            skipped += 1
            continue

        if dry_run:
            print("  🧪 dry-run: 등록 대상 확인 완료")
            continue

        if entry.pdf_url:
            meta = PaperMetadata(
                paper_id=entry.arxiv_id,
                title=entry.title,
                authors=entry.authors or [],
                abstract="",
                published=entry.published,
                pdf_url=entry.pdf_url,
            )
        else:
            print("  📡 arXiv 메타데이터 조회 중...")
            time.sleep(DELAY_SEC)
            meta = _fetch_arxiv_meta(entry.arxiv_id)
            if not meta:
                print("  ⏭️  건너뜀 (메타데이터 조회 실패)")
                failed.append(entry.arxiv_id)
                continue
            print(f"  ✓ {meta.title[:60]}")

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = Path(tmpdir) / f"{meta.paper_id.replace('/', '_')}.pdf"

            print("  ⬇️  PDF 다운로드 중...")
            time.sleep(DELAY_SEC)
            if not _download_pdf(meta.pdf_url, pdf_path):
                print("  ⏭️  건너뜀 (다운로드 실패)")
                failed.append(entry.arxiv_id)
                continue
            print(f"  ✓ 다운로드 완료 ({pdf_path.stat().st_size / 1024:.0f} KB)")

            print("  📝 마크다운 파싱 중...")
            try:
                markdown = parser.to_markdown(pdf_path)
                if not markdown:
                    print("  ⏭️  건너뜀 (파싱 결과 없음)")
                    failed.append(entry.arxiv_id)
                    continue
                print(f"  ✓ 파싱 완료 ({len(markdown):,}자)")
            except Exception as e:
                print(f"  ❌ 파싱 실패: {e}")
                failed.append(entry.arxiv_id)
                continue

            record = storage.build_paper_record(
                paper_id=meta.paper_id,
                title=meta.title,
                authors=meta.authors,
                abstract=meta.abstract,
                published=meta.published,
                pdf_url=meta.pdf_url,
                markdown_content=markdown,
            )
            if not storage.save_paper(record):
                print("  ⏭️  건너뜀 (JSONL 저장 실패/중복)")
                failed.append(entry.arxiv_id)
                continue
            print("  💾 JSONL 저장 완료")

            try:
                print("  🔗 RAG 청킹 + Chroma 적재 중...")
                with chroma_write_lock():
                    chunk_count = rag.add_paper(
                        markdown_content=markdown,
                        title=meta.title,
                        published=meta.published,
                        pdf_url=meta.pdf_url,
                        paper_id=meta.paper_id,
                        abstract=getattr(meta, "abstract", "") or "",
                    )
                print(f"  ✓ Chroma 적재 완료 ({chunk_count}개 청크)")
                success += 1
            except Exception as e:
                # JSONL 에는 이미 저장돼 다시 돌려도 '이미 등록됨' 으로 건너뛴다 — Chroma 는 따로 채워야 한다.
                print(f"  ❌ RAG 적재 실패(JSONL 에는 저장됨): {e}")
                failed.append(entry.arxiv_id)

        gc.collect()

    print(f"\n{'=' * 60}")
    print(f"🎉 완료: 성공 {success} / 스킵 {skipped} / 실패 {len(failed)} / 전체 {len(entries)}")
    if failed:
        print(f"❌ 실패 ID: {' '.join(failed)}")
    print("=" * 60)
    return len(failed)


def main() -> None:
    ap = argparse.ArgumentParser(description="고전·핵심 AI 논문 일괄 등록")
    ap.add_argument(
        "--ids",
        nargs="*",
        default=None,
        help="특정 arXiv ID만 처리 (예: 1706.03762 1810.04805)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="실제 등록 없이 목록만 확인",
    )
    ap.add_argument(
        "--yaml",
        type=Path,
        default=CLASSICS_YAML,
        help="큐레이션 YAML 파일 경로",
    )
    args = ap.parse_args()
    sys.exit(1 if run(yaml_path=args.yaml, filter_ids=args.ids, dry_run=args.dry_run) else 0)


if __name__ == "__main__":
    main()
