"""가사 후보를 웹에서 가져옵니다.

원칙: 모델은 가사를 쓰지 않습니다. 검색으로 받은 본문에 줄 번호를 붙여 보내고,
모델에게는 "가사가 몇 번째 줄부터 몇 번째 줄까지인가"만 묻습니다. 가사 글자는
항상 원문에서 코드가 잘라냅니다.
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from dataclasses import dataclass

from .compare import tidy

# 유튜브 페이지 본문은 자동 생성 자막(음성 인식)이라 '잔치→친트' 같은 오타가 섞입니다. 출처로 쓰지 않습니다.
EXCLUDED_DOMAINS = ("youtube.com", "youtu.be")
MAX_LINES = 500
MAX_CHARS = 20000


@dataclass
class Candidate:
    url: str
    lyrics: str


def _tavily_key() -> str:
    """저장소의 다른 Tavily 사용처와 같은 키·보정(vly- → tvly-)."""
    raw = (os.getenv("TAVILY_API_KEY") or "").strip()
    if raw.startswith("vly-"):
        return "t" + raw
    return raw


def gemini_keys() -> list[str]:
    """이 작업용 키: GEMINI_API_KEY_2 ~ _20 중 값이 있는 것(1번 키는 다른 작업용으로 남김)."""
    keys = [(os.getenv(f"GEMINI_API_KEY_{i}") or "").strip() for i in range(2, 21)]
    return list(dict.fromkeys(k for k in keys if k))


def youtube_title(url: str) -> str | None:
    """콘티의 유튜브 링크에서 영상 제목을 읽습니다(같은 제목의 다른 곡 구분용)."""
    try:
        q = urllib.parse.urlencode({"url": url, "format": "json"})
        with urllib.request.urlopen("https://www.youtube.com/oembed?" + q, timeout=15) as res:
            return json.load(res).get("title")
    except Exception:
        return None


def search(query: str, max_results: int = 6) -> list[dict]:
    from tavily import TavilyClient

    res = TavilyClient(api_key=_tavily_key()).search(
        query=query,
        search_depth="advanced",
        include_raw_content=True,
        max_results=max_results,
    )
    return [r for r in res.get("results", []) if r.get("raw_content")]


def locate(title: str, hint: str | None, docs: list[list[str]]) -> list[tuple[int, int] | None]:
    """문서마다 가사 구간의 (시작 줄, 끝 줄)을 모델에게 묻습니다. 무료 키 하루 호출 수가 적어서 곡당 한 번만 부릅니다."""
    body = "\n\n".join(
        f"=== 문서 {d} ===\n" + "\n".join(f"{i}| {ln}" for i, ln in enumerate(lines))
        for d, lines in enumerate(docs)
    )
    prompt = (
        f"아래는 웹페이지 {len(docs)}개의 본문에 줄 번호를 붙인 것이다. 문서마다 찬양 '{title}'의 가사가 "
        "시작하는 줄과 끝나는 줄의 번호를 찾아라.\n"
        + (f"참고: 이 곡의 유튜브 영상 제목은 '{hint}'이다.\n" if hint else "")
        + "- 가사를 직접 쓰지 말고 줄 번호만 답한다.\n"
        "- 제목, 가수 소개, 광고, 댓글, 다른 곡의 가사는 구간에서 제외한다.\n"
        "- 그 문서에 이 곡의 가사가 없거나 다른 곡이면 found를 false로 한다.\n"
        'JSON으로만 답한다: {"spans": [{"doc": 문서 번호, "found": true 또는 false, "start": 정수, "end": 정수}, ...]}\n\n'
        + body
    )
    # 저장소 공용 호출: 429 면 다음 키로 넘기고, 모든 키가 막히면 쿨다운 후 재시도.
    from core.config.agent_config import GEMINI_MODEL
    from core.llm.agent_gemini import gemini_sdk_generate_json

    raw = gemini_sdk_generate_json(gemini_keys(), GEMINI_MODEL, prompt)
    out: list[tuple[int, int] | None] = [None] * len(docs)
    try:
        spans = json.loads(raw)["spans"]
    except (KeyError, TypeError, ValueError):
        return out
    for span in spans if isinstance(spans, list) else []:
        try:
            d, start, end = int(span["doc"]), int(span["start"]), int(span["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if span.get("found") and 0 <= d < len(docs) and 0 <= start <= end < len(docs[d]):
            out[d] = (start, end)
    return out


def candidates(title: str, url: str | None = None, want: int = 3, max_docs: int = 4) -> list[Candidate]:
    """서로 다른 사이트에서 가사 후보를 최대 want개 모읍니다."""
    from .setlist import norm

    hint = youtube_title(url) if url else None
    hits, domains = [], set()
    for hit in search(f"{title} 가사 찬양 CCM"):
        domain = urllib.parse.urlparse(hit["url"]).netloc
        text = hit["raw_content"][:MAX_CHARS]
        if domain.endswith(EXCLUDED_DOMAINS):
            continue
        if domain in domains or norm(title) not in norm(text):  # 곡명이 없는 페이지는 모델에 보내지 않음
            continue
        domains.add(domain)
        hits.append((hit["url"], [ln.rstrip() for ln in text.splitlines()][:MAX_LINES]))
        if len(hits) >= max_docs:
            break
    if not hits:
        return []
    out = []
    for (page_url, lines), span in zip(hits, locate(title, hint, [lines for _, lines in hits])):
        if not span:
            continue
        lyrics = tidy("\n".join(lines[span[0]:span[1] + 1]))
        if 4 <= len([ln for ln in lyrics.splitlines() if ln]) <= 150:
            out.append(Candidate(page_url, lyrics))
    return out[:want]
