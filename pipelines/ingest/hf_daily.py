"""Hugging Face Daily Papers 를 수집원으로 — 주목 논문을 우선 받는다 (docs/experiments/hf_coverage_1012).

왜: 일일 수집은 cs.AI 최신 제출 20편을 기계적으로 받아, HF Daily Papers(커뮤니티가 고른 주목 논문) 중
코퍼스에 있는 비율이 2026-06 기준 2.6% 였다.

  python -m pipelines.ingest.hf_daily --date 2026-06-15 --top 15          # 하루
  python -m pipelines.ingest.hf_daily --from 2026-05-29 --to 2026-10-06 --top 15   # 백필
  python -m pipelines.ingest.hf_daily --ids-only --date 2026-06-15        # 고른 ID 만 출력

PDF → 파싱 → JSONL → Chroma 는 기존 파이프라인(``pipelines.ingest.main``)과 같은 부품을 쓴다. 중복은 건너뛴다.
arXiv 요청 간격은 ``HF_INGEST_MIN_DELAY`` ~ ``HF_INGEST_MAX_DELAY`` (기본 3~5초, arXiv 규칙: 3초 이상·연결 하나).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HF_API = "https://huggingface.co/api/daily_papers?date={day}"
ARXIV_ID_API = "https://export.arxiv.org/api/query?id_list={ids}&max_results={n}"


def hf_daily_ids(day: str, top: int) -> list[str]:
    """그날 HF Daily Papers 의 arXiv ID, 추천 수 내림차순 상위 ``top``."""
    with urllib.request.urlopen(HF_API.format(day=day), timeout=30) as r:
        items = json.load(r)
    ranked = sorted(items, key=lambda p: -(p.get("paper", {}).get("upvotes") or 0))
    out = []
    for p in ranked:
        pid = (p.get("paper") or {}).get("id")
        if pid and pid not in out:
            out.append(pid)
    return out[:top]


def fetch_metadata(fetcher, ids: list[str]):
    """arXiv ``id_list`` 로 메타데이터. 순서는 ``ids`` 를 따른다."""
    from pipelines.ingest.arxiv_fetcher import ATOM_NS

    if not ids:
        return []
    fetcher._random_delay()
    resp = fetcher._get_with_retry(ARXIV_ID_API.format(ids=",".join(ids), n=len(ids)), timeout=60)
    root = ET.fromstring(resp.content)
    metas = [m for m in (fetcher._parse_entry(e) for e in root.findall("{" + ATOM_NS + "}entry")) if m]
    by_base = {m.paper_id.split("v")[0]: m for m in metas}
    return [by_base[i] for i in ids if i in by_base]


def known_paper_ids() -> set[str]:
    """대기열 + ``processed/`` 보관 파일의 논문 ID. DataStorage 는 대기열만 봐서, 토론 뒤 옮겨진 논문을
    다시 받아 Chroma 에 두 번 넣을 수 있다."""
    import glob
    import re

    ids: set[str] = set()
    files = sorted(glob.glob(str(ROOT / "raw_data_queue/processed/crawled_papers*.jsonl")))
    files.append(str(ROOT / "raw_data_queue/crawled_papers.jsonl"))
    for f in files:
        try:
            for line in open(f, encoding="utf-8", errors="replace"):
                try:
                    pid = json.loads(line).get("paper_id") or ""
                except json.JSONDecodeError:
                    continue
                if pid:
                    ids.add(re.sub(r"v\d+$", "", pid))
        except OSError:
            continue
    return ids


def ingest(papers, fetcher, parser, storage, rag_processor, known: set[str] | None = None) -> tuple[int, int]:
    """(신규 저장 수, 중복 건너뜀 수). 각 단계 실패는 그 논문만 건너뛴다."""
    from pipelines.ingest.data_storage import DataStorage, normalize_paper_id

    known = known if known is not None else known_paper_ids()
    saved = dup = 0
    with tempfile.TemporaryDirectory() as tmp:
        for k, paper in enumerate(papers, 1):
            base = normalize_paper_id(paper.paper_id)
            if base and (base in storage._known_paper_ids or base in known):
                dup += 1
                continue
            print(f"📄 [{k}/{len(papers)}] {paper.paper_id} {paper.title[:60]}", flush=True)
            pdf = Path(tmp) / f"{paper.paper_id}.pdf"
            try:
                if not fetcher.download_pdf(paper.pdf_url, str(pdf)):
                    continue
                md = parser.to_markdown(pdf)
                if not md:
                    print("  ⏭️  파싱 실패", flush=True)
                    continue
                rec = storage.build_paper_record(paper_id=paper.paper_id, title=paper.title, authors=paper.authors,
                                                 abstract=paper.abstract, published=paper.published,
                                                 pdf_url=paper.pdf_url, markdown_content=md)
                if not storage.save_paper(rec):
                    continue
                saved += 1
                known.add(base)
                from core.config.chroma_lock import chroma_write_lock

                with chroma_write_lock():  # 백필 스크립트들과 같은 쓰기 잠금
                    n = rag_processor.add_paper(markdown_content=md, title=paper.title, published=paper.published,
                                                pdf_url=paper.pdf_url, paper_id=paper.paper_id,
                                                abstract=paper.abstract)
                print(f"  💾 저장 · Chroma {n}청크", flush=True)
            except Exception as e:  # 한 편 실패가 전체를 멈추지 않게
                print(f"  ❌ {type(e).__name__}: {str(e)[:160]}", flush=True)
            finally:
                DataStorage.remove_temp_pdf(pdf)
    return saved, dup


def _components():
    from core.config.agent_config import CHROMA_DB_DIR
    from pipelines.ingest.arxiv_fetcher import ArxivFetcher
    from pipelines.ingest.data_storage import DataStorage
    from pipelines.ingest.pdf_parser import PdfParser
    from pipelines.ingest.rag_processor import RagProcessor

    lo = max(3.0, float(os.getenv("HF_INGEST_MIN_DELAY", "3")))
    hi = max(lo, float(os.getenv("HF_INGEST_MAX_DELAY", "5")))
    fetcher = ArxivFetcher(category="cs.AI", limit=50, min_delay=lo, max_delay=hi)
    return (fetcher, PdfParser(table_strategy="lines_strict"),
            DataStorage(output_path=ROOT / "raw_data_queue" / "crawled_papers.jsonl"),
            RagProcessor(db_path=str(CHROMA_DB_DIR)))


def run_day(day: str, top: int, comps=None) -> tuple[int, int, int]:
    """(HF 후보 수, 신규 저장, 중복). ``comps`` 를 넘기면 부품을 재사용한다."""
    fetcher, parser, storage, rag = comps or _components()
    ids = hf_daily_ids(day, top)
    papers = fetch_metadata(fetcher, ids)
    saved, dup = ingest(papers, fetcher, parser, storage, rag)
    print(f"=== HF {day}: 후보 {len(ids)} · 메타 {len(papers)} · 신규 {saved} · 중복 {dup}", flush=True)
    return len(ids), saved, dup


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--top", type=int, default=int(os.getenv("ARXIV_HF_DAILY_TOP", "20")))
    ap.add_argument("--ids-only", action="store_true")
    a = ap.parse_args()
    if a.date:
        days = [a.date]
    else:
        d0, d1 = date.fromisoformat(a.start), date.fromisoformat(a.end)
        days = [(d0 + timedelta(n)).isoformat() for n in range((d1 - d0).days + 1)]
    if a.ids_only:
        for d in days:
            print(d, " ".join(hf_daily_ids(d, a.top)))
        return 0
    comps = _components()
    tot = [0, 0, 0]
    for d in days:
        try:
            r = run_day(d, a.top, comps)
            tot = [x + y for x, y in zip(tot, r)]
        except Exception as e:
            print(f"❌ HF {d}: {type(e).__name__}: {str(e)[:200]}", flush=True)
        time.sleep(1)
    print(f"🎉 HF 수집 끝: 일수 {len(days)} · 후보 {tot[0]} · 신규 {tot[1]} · 중복 {tot[2]}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
