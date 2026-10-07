"""가사 후보를 웹에서 가져옵니다.

원칙: 모델은 가사를 쓰지 않습니다. 검색으로 받은 본문에 줄 번호를 붙여 보내고,
모델에게는 "가사가 몇 번째 줄부터 몇 번째 줄까지인가"만 묻습니다. 가사 글자는
항상 원문에서 코드가 잘라냅니다.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

from .compare import tidy

MAX_LINES = 500
MAX_CHARS = 20000


@dataclass
class Candidate:
    url: str
    lyrics: str


def _post(url, body, headers, retries=4):
    data = json.dumps(body).encode()
    for attempt in range(retries):
        req = urllib.request.Request(
            url, data=data, method="POST", headers={"Content-Type": "application/json", **headers}
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                return json.load(res)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            raise RuntimeError(f"POST {url.split('?')[0]} -> {e.code}") from None


def youtube_title(url: str) -> str | None:
    """콘티의 유튜브 링크에서 영상 제목을 읽습니다(같은 제목의 다른 곡 구분용)."""
    try:
        q = urllib.parse.urlencode({"url": url, "format": "json"})
        with urllib.request.urlopen("https://www.youtube.com/oembed?" + q, timeout=15) as res:
            return json.load(res).get("title")
    except Exception:
        return None


def search(query: str, max_results: int = 6) -> list[dict]:
    res = _post(
        "https://api.tavily.com/search",
        {"query": query, "search_depth": "advanced", "include_raw_content": True,
         "max_results": max_results},
        {"Authorization": "Bearer " + os.environ["TAVILY_API_KEY"]},
    )
    return [r for r in res.get("results", []) if r.get("raw_content")]


def locate(title: str, hint: str | None, lines: list[str]) -> tuple[int, int] | None:
    """본문에서 가사 구간의 (시작 줄, 끝 줄)을 모델에게 묻습니다."""
    numbered = "\n".join(f"{i}| {ln}" for i, ln in enumerate(lines))
    prompt = (
        f"아래는 웹페이지 본문에 줄 번호를 붙인 것이다. 찬양 '{title}'의 가사가 시작하는 줄과 "
        "끝나는 줄의 번호를 찾아라.\n"
        + (f"참고: 이 곡의 유튜브 영상 제목은 '{hint}'이다.\n" if hint else "")
        + "- 가사를 직접 쓰지 말고 줄 번호만 답한다.\n"
        "- 제목, 가수 소개, 광고, 댓글, 다른 곡의 가사는 구간에서 제외한다.\n"
        "- 이 곡의 가사가 없거나 다른 곡이면 found를 false로 한다.\n"
        'JSON으로만 답한다: {"found": true 또는 false, "start": 정수, "end": 정수}\n\n'
        + numbered
    )
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    res = _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        {"contents": [{"parts": [{"text": prompt}]}],
         "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}},
        {"x-goog-api-key": os.environ["GEMINI_API_KEY_2"]},
    )
    try:
        answer = json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
        start, end = int(answer["start"]), int(answer["end"])
    except (KeyError, IndexError, TypeError, ValueError):
        return None
    if not answer.get("found") or not 0 <= start <= end < len(lines):
        return None
    return start, end


def candidates(title: str, url: str | None = None, want: int = 3) -> list[Candidate]:
    """서로 다른 사이트에서 가사 후보를 최대 want개 모읍니다."""
    hint = youtube_title(url) if url else None
    out, domains = [], set()
    for hit in search(f"{title} 가사 찬양 CCM"):
        domain = urllib.parse.urlparse(hit["url"]).netloc
        if domain in domains:
            continue
        lines = [ln.rstrip() for ln in hit["raw_content"][:MAX_CHARS].splitlines()][:MAX_LINES]
        span = locate(title, hint, lines)
        if not span:
            continue
        lyrics = tidy("\n".join(lines[span[0]:span[1] + 1]))
        if 4 <= len([ln for ln in lyrics.splitlines() if ln]) <= 150:
            domains.add(domain)
            out.append(Candidate(hit["url"], lyrics))
        if len(out) >= want:
            break
    return out
