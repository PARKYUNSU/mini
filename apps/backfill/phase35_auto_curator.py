#!/usr/bin/env python3
"""
Phase 3.5 Step 2 — 윤수르 자율 심사관 & 아이디어 금고 (Auto-Curator).

**무엇을 하는지 (YES와 날짜의 관계)**
- 먼저 arXiv에서 **해당 로컬 날짜에 대응하는 제출일 구간(GMT, submittedDate)** 에 올라온 논문을 **후보**로 가져옵니다.
  기본 실행일이 ``D``이면 대상일은 보통 **``D-1`` (어제)** 입니다 (``--date`` 로 고정 가능).
- 각 후보마다 LLM 심사 → **[판단]: YES** 인 논문만 ``idea_vault.sqlite`` 에 저장하고(중복 적재 로직은 별도),
  PDF는 일일 상한 안에서 Chroma/JSONL 적재를 시도합니다.
- 따라서 “그날짜 YES만 가져온다”가 아니라, **그 제출일 구간의 후보 전부를 심사**하고, 그중 YES만 금고에 남깁니다.

**후보가 비면 (“논문 없음”)**
- 해당 일자·카테고리 조합에 arXiv가 **실제로 0건**이거나, 네트워크/API 오류, XML 파싱 실패(이 경우 빈 리스트만 반환) 등일 수 있습니다.
- 아래 코드는 빈 결과일 때 API가 알려주는 ``totalResults`` 와 검색식 일부를 로그로 출력합니다.
  ``.cron/phase35_curator_stdout.log`` 를 확인하세요.

- 전날(또는 ``--date``) arXiv **제출분** 메타 수집 — 기본 카테고리 ``cs.AI,cs.LG,cs.CL`` (``CURATOR_ARXIV_CATEGORIES``).
  당일 단일 검색 결과가 비면 **최근 N일 폴백** (``CURATOR_FALLBACK_DAY_SPAN``, 기본 7).
- **RAG 선행**: ``rag_engine.get_curator_context_sync`` 로 Chroma 유사 지식 로드 후에만 LLM 심사
- **[판단]: YES** 인 경우만: (A) Chroma 적재 (B) ``idea_vault.sqlite`` 에 한계·메타 저장
- CEO 텔레그램 브리핑 (ALLOWED_CHAT_ID)

크론 예 (Mac mini) — **통합 스케줄러(`apps.scheduler.run_scheduler`)에 동일 작업이 포함되어 있으면 중복 실행되므로 crontab에서는 제거하세요.**

  # (레거시) 수동 crontab 예시 — 미사용 시 생략
  # 30 7 * * * cd "/Volumes/T7 Shield/mini" && PYTHONPATH=. .venv/bin/python -m apps.backfill.morning_scraper >>logs/morning_scraper.log 2>&1
  # 0 8 * * * cd "/Volumes/T7 Shield/mini" && PYTHONPATH=. .venv/bin/python -m apps.backfill.phase35_auto_curator >>logs/phase35_curator.log 2>&1

07:30 ``morning_scraper`` 가 ``morning_cache.json`` 에 날씨·뉴스를 저장하고,
08:00 본 스크립트가 발송 직전 같은 파일을 읽어 임원 브리핑 상단에 합친다.
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import random
import re
import sqlite3
import sys
import tempfile
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
import telebot

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

load_dotenv()
load_dotenv(_ROOT / ".env", override=True)

from apps.telegram_bot import rag_engine  # noqa: E402
from core.config.agent_config import (  # noqa: E402
    ALLOWED_CHAT_ID,
    CHROMA_DB_DIR,
    IDEA_VAULT_DB_PATH,
    RAG_OLLAMA_TIMEOUT_SEC,
    TELEGRAM_TOKEN,
)
from core.config.chroma_lock import chroma_write_lock  # noqa: E402
from pipelines.ingest.arxiv_fetcher import ArxivFetcher, PaperMetadata  # noqa: E402
from pipelines.ingest.data_storage import DataStorage, normalize_paper_id  # noqa: E402
from pipelines.ingest.pdf_parser import PdfParser  # noqa: E402
from pipelines.ingest.rag_processor import RagProcessor  # noqa: E402

RAW_DATA_DIR = Path("./raw_data_queue")
CHROMA_DIR = CHROMA_DB_DIR

# ``morning_scraper`` 와 동일 경로 (mini 루트 ``morning_cache.json``)
MORNING_CACHE_PATH = _ROOT / "morning_cache.json"


def _compose_executive_briefing_with_morning_cache(paper_briefing_body: str) -> str:
    """
    08:00 발송 직전: 오늘 날짜 키의 ``morning_cache.json`` 을 읽어
    [날씨] + [AI 뉴스] + [논문 심사 본문] 순으로 합친다.
    캐시가 없거나 깨지면 상단에 한 줄 경고만 붙이고 논문 본문은 그대로 유지.
    """
    today_s = date.today().isoformat()
    weather_block = ""
    news_block = ""
    cache_ok = False
    try:
        if MORNING_CACHE_PATH.is_file():
            raw = MORNING_CACHE_PATH.read_text(encoding="utf-8")
            data = json.loads(raw)
            if isinstance(data, dict):
                entry = data.get(today_s)
                if isinstance(entry, dict):
                    w = entry.get("weather_markdown")
                    n = entry.get("news_digest_markdown")
                    if isinstance(w, str) and w.strip():
                        weather_block = w.strip()
                    if isinstance(n, str) and n.strip():
                        news_block = n.strip()
                    if weather_block and news_block:
                        cache_ok = True
    except Exception:
        cache_ok = False

    parts: list[str] = []
    if not cache_ok:
        parts.append("⚠️ 날씨/뉴스: 수집 실패")
        parts.append("")
    else:
        parts.append("## ☀️ 오늘의 날씨·기온 요약 (서울)")
        parts.append("")
        parts.append(weather_block)
        parts.append("")
        parts.append("## 📰 AI 뉴스 심층 요약 (한글 브리핑 · 3~5건)")
        parts.append("")
        parts.append(news_block)
        parts.append("")
        parts.append("---")
        parts.append("")

    parts.append("## 📚 윤수르 YES 논문 심사 브리핑 (arXiv AI 계열)")
    parts.append("")
    parts.append(paper_briefing_body.strip())
    return "\n".join(parts).strip()

CURATOR_PROMPT = PromptTemplate.from_template(
    """당신은 호문클루스 신디게이트의 최고 기술 책임자(CTO)입니다. 제공된 [기존 지식]과 비교했을 때, 이 [새로운 논문]이 AI 산업의 패러다임을 바꿀 혁신적인 SOTA 기술이거나, 우리 신디게이트의 미래 생태계(차세대 아키텍처, 멀티모달, 로보틱스, RAG 고도화 등) 확장에 꼭 필요한 기술인지 심사하세요.

**언어**: 초록·제목이 영어여도, `[핵심 기여]`, `[우리 시스템 적용점]`, `[한계 및 우려사항]` 내용은 **반드시 한국어 문장**으로만 작성하세요. 불필요한 영어 설명은 쓰지 마세요. (고유명사·저자 제안 약어 등은 괄호로 짧게 병기 가능.)

[기존 지식] (Chroma 유사 청크 요약·발췌):
{existing_knowledge}

[새로운 논문]
제목: {title}
초록:
{abstract}

반드시 아래 형식으로만 답하세요 (각 항목 한 줄, 대괄호 라벨 유지).
[판단]: YES 또는 NO
[핵심 기여]: (기존 지식과 비교하여 어떤 한계를 극복했는지 2문장 요약)
[우리 시스템 적용점]: (이 기술을 우리 시스템의 현재 또는 미래 비전에 도입할 때의 이점을 1문장 제안)
[한계 및 우려사항]: (이 논문의 현실적인 한계나 오버엔지니어링 우려를 1문장 비판)
"""
)


def _init_idea_vault(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS idea_vault_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            paper_id TEXT NOT NULL,
            title TEXT,
            pdf_url TEXT,
            critique TEXT,
            judge_full TEXT,
            verdict_yes INTEGER NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_vault_paper ON idea_vault_entries(paper_id)"
    )
    conn.commit()


def _parse_verdict_yes(text: str) -> bool:
    t = text or ""
    m = re.search(r"\[\s*판단\s*\]\s*:\s*(YES|NO)", t, re.IGNORECASE)
    if not m:
        return False
    return m.group(1).upper() == "YES"


def _extract_section(text: str, label: str) -> str:
    pat = rf"\[\s*{re.escape(label)}\s*\]\s*:\s*(.+?)(?=\n\s*\[|$)"
    m = re.search(pat, text or "", re.DOTALL | re.IGNORECASE)
    return (m.group(1).strip() if m else "")[:4000]


def _build_rag_query(paper: PaperMetadata) -> str:
    title = (paper.title or "")[:240]
    abstract = (paper.abstract or "")[:900]
    return f"{title}\n{abstract}"


def _ingest_paper_to_chroma_and_jsonl(paper: PaperMetadata, fetcher: ArxivFetcher) -> bool:
    """YES 트랙 A: PDF→JSONL→Chroma (기존 파이프라인과 동일)."""
    storage = DataStorage(output_path=RAW_DATA_DIR / "crawled_papers.jsonl")
    base_id = normalize_paper_id(paper.paper_id)
    if base_id and base_id in storage._known_paper_ids:
        return False
    parser = PdfParser(table_strategy="lines_strict")
    rag_processor = RagProcessor(db_path=str(CHROMA_DIR))
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / f"{paper.paper_id}.pdf"
        if not fetcher.download_pdf(paper.pdf_url, str(pdf_path)):
            return False
        md = parser.to_markdown(pdf_path)
        if not md or not md.strip():
            return False
        record = storage.build_paper_record(
            paper_id=paper.paper_id,
            title=paper.title,
            authors=paper.authors,
            abstract=paper.abstract,
            published=paper.published,
            pdf_url=paper.pdf_url,
            markdown_content=md,
        )
        record["target_topic"] = "phase35_curator_yes"
        record["target_batch"] = "auto_curator"
        if not storage.save_paper(record):
            return False
        try:
            with chroma_write_lock():
                rag_processor.add_paper(
                    markdown_content=md,
                    title=paper.title,
                    published=paper.published,
                    pdf_url=paper.pdf_url,
                    paper_id=paper.paper_id,
                    abstract=paper.abstract,
                )
        except Exception:
            DataStorage.remove_temp_pdf(pdf_path)
            return False
        DataStorage.remove_temp_pdf(pdf_path)
        del md
        gc.collect()
    return True


def _send_telegram_chunks(text: str) -> None:
    if not TELEGRAM_TOKEN or not ALLOWED_CHAT_ID:
        print("ℹ️ 텔레그램 스킵: TELEGRAM_TOKEN / ALLOWED_CHAT_ID 없음")
        return
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    for cid in [x.strip() for x in ALLOWED_CHAT_ID.split(",") if x.strip()]:
        for i in range(0, len(text), 3800):
            part = text[i : i + 3800]
            try:
                bot.send_message(cid, part, parse_mode=None, disable_web_page_preview=True)
            except Exception as e:
                print(f"⚠️ 텔레그램 전송 실패 {cid}: {e}")
        time.sleep(0.3)


def _pull_papers_date_range(
    fetcher: ArxivFetcher,
    *,
    start_d: date,
    end_d: date,
    max_fetch: int,
) -> list[PaperMetadata]:
    papers: list[PaperMetadata] = []
    offset = 0
    start_s = start_d.isoformat()
    end_s = end_d.isoformat()
    seen: set[str] = set()
    while len(papers) < max_fetch:
        batch = fetcher.fetch_metadata_batch(
            start=offset,
            limit=fetcher.limit,
            start_date=start_s,
            end_date=end_s,
        )
        if not batch:
            break
        for p in batch:
            if len(papers) >= max_fetch:
                break
            k = normalize_paper_id(p.paper_id)
            if k in seen:
                continue
            seen.add(k)
            papers.append(p)
        offset += len(batch)
        if len(batch) < fetcher.limit:
            break
        time.sleep(random.uniform(3.0, 6.0))
    return papers


def _arxiv_log_total_results(
    fetcher: ArxivFetcher,
    *,
    label: str,
    start_d: date,
    end_d: date,
) -> None:
    """후보가 비었을 때 원인 분리용 (API는 살아 있는데 파싱/페이징 문제인지 등)."""
    try:
        tot = fetcher.get_search_total_results(
            start_d.isoformat(),
            end_d.isoformat(),
        )
        q = fetcher._build_search_query(
            start_d.isoformat(),
            end_d.isoformat(),
        )
        q_short = q if len(q) <= 320 else q[:317] + "..."
        print(
            f"📊 [{label}] arXiv totalResults={tot} search_query={q_short}",
            flush=True,
        )
        if tot is not None and tot > 0:
            print(
                "⚠️  totalResults>0 인데 후보 리스트가 비었습니다. "
                "XML 파싱·응답 크기·네트워크 로그(위 arXiv API 출력)를 확인하세요.",
                flush=True,
            )
    except Exception as e:  # noqa: BLE001
        print(f"📊 [{label}] totalResults 조회 실패: {e}", flush=True)


def _resolve_curator_paper_candidates(
    target_day: date,
    max_fetch: int,
) -> tuple[list[PaperMetadata], str]:
    """
    Returns:
        papers, human-readable 수집 조건 설명 (브리핑 첫머리용).
    """
    cats = (os.getenv("CURATOR_ARXIV_CATEGORIES") or "cs.AI,cs.LG,cs.CL").strip()
    if not cats:
        cats = "cs.AI,cs.LG,cs.CL"
    fetcher = ArxivFetcher(
        category=cats,
        limit=min(100, max_fetch),
        min_delay=3.0,
        max_delay=6.0,
        extra_query=None,
        sort_by=ArxivFetcher.SORT_SUBMITTED,
        sort_order="descending",
    )

    papers = _pull_papers_date_range(
        fetcher, start_d=target_day, end_d=target_day, max_fetch=max_fetch
    )
    if papers:
        note = f"제출일 구간 {target_day.isoformat()} (GMT·arXiv 규칙) · {cats}"
        return papers, note

    _arxiv_log_total_results(
        fetcher, label="당일 단독 구간", start_d=target_day, end_d=target_day
    )

    try:
        fb_days = int(os.getenv("CURATOR_FALLBACK_DAY_SPAN") or "7")
    except ValueError:
        fb_days = 7
    fb_days = max(1, min(21, fb_days))
    start_w = target_day - timedelta(days=fb_days - 1)
    papers = _pull_papers_date_range(
        fetcher, start_d=start_w, end_d=target_day, max_fetch=max_fetch
    )
    if papers:
        note = (
            f"당일({target_day.isoformat()}) 단독 0건 → "
            f"폴백 {fb_days}일치({start_w.isoformat()}~{target_day.isoformat()}) · {cats}"
        )
        return papers, note

    _arxiv_log_total_results(
        fetcher,
        label=f"폴백 {fb_days}일 구간",
        start_d=start_w,
        end_d=target_day,
    )

    return [], f"(수집 실패 또는 0건) 대상일={target_day.isoformat()} · {cats}"


def run_curator_for_day(
    target_day: date,
    *,
    max_fetch: int,
    max_yes_ingest: int,
    rag_top_k: int,
) -> None:
    day_s = target_day.isoformat()
    print(f"🧠 Phase35 Auto-Curator: 제출일 기준 {day_s} (로컬 날짜 키)", flush=True)

    try:
        papers, fetch_note = _resolve_curator_paper_candidates(target_day, max_fetch)
    except requests.RequestException as e:
        err_body = (
            f"⚠️ Phase35: arXiv API 네트워크 오류로 논문 메타를 가져오지 못했습니다.\n"
            f"({type(e).__name__}: {e})\n\n"
            "내장 재시도 후에도 실패한 경우입니다. 네트워크·VPN·방화벽을 확인하거나, "
            "나중에 수동으로 다음을 실행해 보세요:\n"
            f"`PYTHONPATH=. python -m apps.backfill.phase35_auto_curator --date {day_s}`\n\n"
            "(환경변수 ARXIV_API_TIMEOUT_SEC 로 타임아웃 초를 늘릴 수 있습니다.)"
        )
        print(err_body, flush=True)
        final_body = _compose_executive_briefing_with_morning_cache(err_body)
        _send_telegram_chunks(final_body)
        return

    if not papers:
        msg = (
            f"📭 Phase35 심사관: arXiv에서 후보 논문 메타를 가져오지 못했습니다 "
            f"(심사 전 단계).\n"
            f"{fetch_note}\n"
            "기본 대상일은 **실행일 기준 어제** 로컬 날짜입니다. 오늘 제출분을 보시려면 "
            "`python -m apps.backfill.phase35_auto_curator --date YYYY-MM-DD` 로 날짜를 지정하세요.\n"
            "원인 확인: `.cron/phase35_curator_stdout.log` 에 `📊` 로그(arXiv totalResults·검색식)를 확인하세요."
        )
        print(msg, flush=True)
        final_body = _compose_executive_briefing_with_morning_cache(msg)
        _send_telegram_chunks(final_body)
        return

    cats_pdf = (os.getenv("CURATOR_ARXIV_CATEGORIES") or "cs.AI,cs.LG,cs.CL").strip()
    fetcher_for_pdf = ArxivFetcher(
        category=cats_pdf or "cs.AI,cs.LG,cs.CL",
        limit=min(100, max_fetch),
        min_delay=3.0,
        max_delay=6.0,
        extra_query=None,
        sort_by=ArxivFetcher.SORT_SUBMITTED,
        sort_order="descending",
    )

    llm = ChatOllama(
        model=os.environ.get("LOCAL_LLM_MODEL", "yunsur_v3:latest"),
        base_url=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"),
        temperature=0.15,
        timeout=RAG_OLLAMA_TIMEOUT_SEC,
    )

    conn = sqlite3.connect(str(IDEA_VAULT_DB_PATH))
    _init_idea_vault(conn)

    briefing: list[str] = [
        f"☀️ Phase35 CEO 브리핑 ({day_s}) — 후보 {len(papers)}편",
        f"📡 수집: {fetch_note}",
    ]
    yes_ingested = 0

    for idx, paper in enumerate(papers, 1):
        print(f"  [{idx}/{len(papers)}] {paper.paper_id}", flush=True)
        rq = _build_rag_query(paper)
        try:
            existing = rag_engine.get_curator_context_sync(rq, top_k=rag_top_k)
        except Exception as e:
            existing = f"(Chroma 조회 실패: {e})"

        prompt = CURATOR_PROMPT.format(
            existing_knowledge=existing[:12000],
            title=paper.title,
            abstract=(paper.abstract or "")[:6000],
        )
        try:
            resp = llm.invoke(prompt)
            judge_text = (getattr(resp, "content", None) or str(resp)).strip()
        except Exception as e:
            judge_text = f"[판단]: NO\n[핵심 기여]: (LLM 오류: {e})"

        yes = _parse_verdict_yes(judge_text)
        critique = _extract_section(judge_text, "한계 및 우려사항")

        briefing.append(
            f"\n---\n📄 {paper.paper_id} {paper.title[:80]}\n"
            f"{judge_text[:3500]}"
        )

        if yes:
            if yes_ingested < max_yes_ingest:
                if _ingest_paper_to_chroma_and_jsonl(paper, fetcher_for_pdf):
                    yes_ingested += 1
                    print(f"    ✅ YES → Chroma 적재 ({yes_ingested}/{max_yes_ingest})", flush=True)
                else:
                    briefing.append("  (YES — Chroma/JSONL 적재 실패 또는 중복 스킵)")
            else:
                briefing.append(f"  (YES — 일일 Chroma 적재 상한 {max_yes_ingest} 도달, PDF 스킵)")
            conn.execute(
                """
                INSERT INTO idea_vault_entries
                (created_at, paper_id, title, pdf_url, critique, judge_full, verdict_yes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.utcnow().isoformat() + "Z",
                    normalize_paper_id(paper.paper_id),
                    paper.title,
                    paper.pdf_url,
                    critique,
                    judge_text,
                    1,
                ),
            )
            conn.commit()

        time.sleep(float(os.getenv("CURATOR_INTER_PAPER_SLEEP", "2.0")))

    conn.close()
    body = "\n".join(briefing)
    final_body = _compose_executive_briefing_with_morning_cache(body)
    _send_telegram_chunks(final_body)
    print("✅ 브리핑 전송·종료", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase35 일일 심사관")
    ap.add_argument(
        "--date",
        type=str,
        default=None,
        help="검사할 제출일 YYYY-MM-DD (기본: 어제 로컬 달력 기준)",
    )
    ap.add_argument("--max-fetch", type=int, default=int(os.getenv("CURATOR_MAX_FETCH", "40")))
    ap.add_argument("--max-yes-ingest", type=int, default=int(os.getenv("CURATOR_MAX_YES_INGEST", "6")))
    ap.add_argument("--rag-top-k", type=int, default=int(os.getenv("CURATOR_RAG_TOP_K", "6")))
    args = ap.parse_args()

    if args.date:
        target = datetime.strptime(args.date.strip(), "%Y-%m-%d").date()
    else:
        target = date.today() - timedelta(days=1)

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    run_curator_for_day(
        target,
        max_fetch=max(1, args.max_fetch),
        max_yes_ingest=max(0, args.max_yes_ingest),
        rag_top_k=max(1, args.rag_top_k),
    )


if __name__ == "__main__":
    main()
