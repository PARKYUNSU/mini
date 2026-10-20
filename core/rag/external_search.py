"""DB 에 없을 때 외부(OpenAlex)에서 찾아보기 (docs/experiments/external_search_1020).

판정이 '없음'이거나 목록 모드인 논문 질문에서, 이미 만든 영어 검색어로 OpenAlex 를 부르고
컨텍스트에 없는 논문을 최대 4편 답 끝에 **제목 · 연도 · 링크만** 덧붙인다(읽지 않은 논문을 요약하면 날조).
arXiv API 는 맥미니에서 시간 초과가 잦고 Semantic Scholar 는 키 없이 429 라 OpenAlex 를 쓴다.
사용자 정보(이메일 등)는 보내지 않는다. 실패하면 빈 목록 — 답변은 그대로 나간다.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
from pathlib import Path

import requests

__all__ = ["external_search_active", "search_openalex", "format_section", "record_candidates", "ExternalSearch"]

OPENALEX_URL = "https://api.openalex.org/works"
TIMEOUT_SEC = 6.0
MAX_ITEMS = 4
MIN_YEAR = 2017
_ARXIV = re.compile(r"(?:arxiv\.org/abs/|10\.48550/arxiv\.)(\d{4}\.\d{4,5})", re.I)


def external_search_active() -> bool:
    return os.getenv("RAG_EXTERNAL_SEARCH", "0").strip() == "1"


def _arxiv_id(work: dict) -> str | None:
    hay = [str((work.get("ids") or {}).get("doi") or ""), str(work.get("doi") or "")]
    for loc in work.get("locations") or []:
        hay.append(str((loc or {}).get("landing_page_url") or ""))
        hay.append(str((loc or {}).get("pdf_url") or ""))
    for h in hay:
        m = _ARXIV.search(h)
        if m:
            return m.group(1)
    return None


def _abstract(work: dict) -> str:
    inv = work.get("abstract_inverted_index") or {}
    pos = sorted((p, w) for w, ps in inv.items() for p in ps)
    return " ".join(w for _, w in pos)


def search_openalex(query: str, exclude_ids: set[str] | None = None, *, timeout: float = TIMEOUT_SEC,
                    limit: int = MAX_ITEMS) -> list[dict]:
    """OpenAlex 검색 → 컨텍스트에 없는 최근(2017~) 논문 최대 ``limit`` 편. 실패하면 []."""
    q = (query or "").strip()
    if not q:
        return []
    try:
        r = requests.get(OPENALEX_URL, params={
            "search": q[:300], "per-page": 8,
            "select": "id,title,ids,doi,publication_year,locations,abstract_inverted_index",
        }, timeout=timeout)
        r.raise_for_status()
        works = r.json().get("results") or []
    except Exception as exc:  # 외부 장애는 답변을 막지 않는다
        print(f"[DEBUG] external_search 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return []
    ex = {re.sub(r"v\d+$", "", i) for i in (exclude_ids or set())}
    out: list[dict] = []
    for w in works:
        title = re.sub(r"\s+", " ", (w.get("title") or "")).strip()
        year = w.get("publication_year") or 0
        ax = _arxiv_id(w)
        if not title or year < MIN_YEAR or (ax and ax in ex):
            continue
        url = f"https://arxiv.org/abs/{ax}" if ax else ((w.get("ids") or {}).get("doi") or w.get("id") or "")
        out.append({"title": title, "year": year, "arxiv": ax, "url": url, "abstract": _abstract(w)[:1200]})
        if len(out) >= limit:
            break
    return out


def format_section(items: list[dict]) -> str:
    """답 끝에 붙일 줄들. arXiv 는 `[ID]` 로 적어 전송 직전 링크로 바뀐다(linkify_arxiv_html)."""
    if not items:
        return ""
    lines = ["", "", "📎 **DB 밖에서 찾은 관련 논문** (OpenAlex 검색 · 내용은 요약하지 않음)"]
    for it in items:
        ref = f"[{it['arxiv']}]" if it.get("arxiv") else it.get("url", "")
        lines.append(f"- {it['title']} ({it['year']}) {ref}".rstrip())
    return "\n".join(lines)


def record_candidates(question: str, items: list[dict], path: Path | None = None) -> None:
    """나중 수집 후보로 arXiv ID 를 남긴다 (자동 수집은 하지 않는다)."""
    ids = [it["arxiv"] for it in items if it.get("arxiv")]
    if not ids:
        return
    p = path or Path(os.getenv("EXTERNAL_CANDIDATES_LOG") or Path(__file__).resolve().parents[2] / ".bridge" / "external_candidates.jsonl")
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "question": question[:300], "arxiv": ids}, ensure_ascii=False) + "\n")
    except OSError:
        pass


class ExternalSearch:
    """답변 생성과 동시에 OpenAlex 를 부르고, 답변이 끝나면 남은 시간만 기다린다."""

    def __init__(self, query: str, exclude_ids: set[str], timeout: float = TIMEOUT_SEC):
        self._items: list[dict] = []
        self._deadline = time.time() + timeout
        self._t = threading.Thread(target=self._run, args=(query, exclude_ids, timeout), daemon=True)
        self._t.start()

    def _run(self, query, exclude_ids, timeout):
        self._items = search_openalex(query, exclude_ids, timeout=timeout)

    def result(self) -> tuple[list[dict], float]:
        """(결과, 답변 뒤 더 기다린 초)."""
        t0 = time.time()
        self._t.join(max(0.0, self._deadline - t0))
        return (self._items if not self._t.is_alive() else []), time.time() - t0
