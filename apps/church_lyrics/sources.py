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

from .compare import key, tidy

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
        # 줄바꿈 없이 한 줄로 붙은 가사도 대조용으로 받습니다(너무 짧은 조각만 버림)
        if len(key(lyrics)) >= 15 and len(lyrics.splitlines()) <= 150:
            out.append(Candidate(page_url, lyrics))
    return out[:want]


def proofread(lyrics: str, title: str = "") -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """오탈자 검증. (띄어쓰기 교정, 오탈자 의심)을 돌려줍니다.

    - 띄어쓰기 교정 (전, 후): 공백을 뺀 글자가 원래 줄과 완전히 같은 제안만 받습니다. 바로 반영해도 글자는 그대로입니다.
    - 오탈자 의심 (줄, 제안): 글자가 틀려 보이는 줄. 가사에 반영하지 않고 작업자에게 보여 주기만 합니다.
    """
    lines = lyrics.splitlines()
    numbered = "\n".join(f"{i}| {ln}" for i, ln in enumerate(lines) if ln.strip())
    if not numbered:
        return [], []
    prompt = (
        f"아래는 찬양 '{title}'의 가사에 줄 번호를 붙인 것이다. 자막에 쓰기 전에 두 가지를 검사하라.\n"
        "1. spacing: 표준 맞춤법의 띄어쓰기에 어긋난 줄. 글자는 하나도 바꾸지 말고 공백만 고친 줄을 준다.\n"
        "   같은 가사가 반복되면 모두 같게 고친다. 성경·찬양에서 한 단어로 쓰는 말(어린양 등)은 붙여 쓴다.\n"
        "2. typos: 사전에 없는 낱말이나 소리만 비슷하게 잘못 받아 적은 낱말이 있는 줄(예: 잔치→친트, 수치→주치,\n"
        "   새 옷을 입히시고→태옷들이 피시고). 맞을 것 같은 줄을 제안한다.\n"
        "- 가사는 시적 표현이다. 어미·조사·어순·표현을 다듬는 제안은 하지 않는다(살다가 보면, 찬양하며, 변함이 없는 은 그대로 맞다).\n"
        "- 박자에 맞춘 줄임말(잔칠, 날 위해 등)과 영어 가사는 오탈자가 아니다.\n"
        "- 맞는 줄은 답에 넣지 않는다. 확실하지 않으면 넣지 않는다.\n"
        'JSON으로만 답한다: {"spacing": [{"line": 줄 번호, "text": "고친 줄"}], '
        '"typos": [{"line": 줄 번호, "suggest": "맞을 것 같은 줄"}]}\n\n' + numbered
    )
    from core.config.agent_config import GEMINI_MODEL
    from core.llm.agent_gemini import gemini_sdk_generate_json

    try:
        answer = json.loads(gemini_sdk_generate_json(gemini_keys(), GEMINI_MODEL, prompt))
        spacing_raw, typos_raw = answer.get("spacing") or [], answer.get("typos") or []
    except (AttributeError, TypeError, ValueError):
        return [], []

    def pick(items, field):
        for item in items if isinstance(items, list) else []:
            try:
                old, new = lines[int(item["line"])].strip(), " ".join(str(item[field]).split())
            except (KeyError, TypeError, ValueError, IndexError):
                continue
            if old and new and new != old:
                yield old, new

    spacing = list(dict.fromkeys((o, n) for o, n in pick(spacing_raw, "text") if n.replace(" ", "") == o.replace(" ", "")))
    typos = list(dict.fromkeys((o, n) for o, n in pick(typos_raw, "suggest") if n.replace(" ", "") != o.replace(" ", "")))
    return spacing, typos


def apply_respace(lyrics: str, fixes: list[tuple[str, str]]) -> str:
    """같은 줄은 반복돼도 모두 같게 고칩니다."""
    table = dict(fixes)
    return "\n".join(table.get(ln.strip(), ln) for ln in lyrics.splitlines())
