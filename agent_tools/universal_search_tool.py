"""
이 도구는 최신 인터넷 정보, 뉴스, 환율, 수학 계산 등을 검색할 때 사용하는 만능 웹 검색기입니다.
"""

import re
import urllib.parse

import requests
from bs4 import BeautifulSoup

# 구글 봇 차단 회피용 Chrome User-Agent (완전 위장)
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# Google time filter 매핑 (tbs 파라미터)
_TIME_FILTER_MAP = {
    "qdr:h": "1시간",
    "qdr:d": "1일",
    "qdr:w": "1주",
    "qdr:m": "1개월",
    "qdr:y": "1년",
}


def universal_search(
    keyword: str,
    engine: str = "duckduckgo",
    time_filter: str = "",
) -> str:
    """
    이 도구는 최신 인터넷 정보, 뉴스, 환율, 수학 계산 등을 검색할 때 사용하는 만능 웹 검색기입니다.

    Args:
        keyword: 검색어
        engine: "google", "duckduckgo", "wolframalpha" 중 하나 (기본: duckduckgo)
        time_filter: 구글 전용. "qdr:h"(1시간), "qdr:d"(1일), "qdr:w"(1주), "qdr:m"(1개월), "qdr:y"(1년)

    Returns:
        검색 결과 제목과 요약 텍스트
    """
    keyword = (keyword or "").strip()
    if not keyword:
        return "검색어를 입력해 주세요."

    engine = (engine or "duckduckgo").lower().strip()
    if engine not in ("google", "duckduckgo", "wolframalpha"):
        engine = "duckduckgo"

    headers = {"User-Agent": _USER_AGENT}

    try:
        if engine == "google":
            return _search_google(keyword, time_filter, headers)
        if engine == "duckduckgo":
            return _search_duckduckgo(keyword, headers)
        if engine == "wolframalpha":
            return _search_wolframalpha(keyword, headers)
    except requests.exceptions.RequestException as e:
        return f"검색 요청 오류: {e}"
    except Exception as e:
        return f"검색 처리 오류: {e}"

    return "지원하지 않는 검색 엔진입니다."


def _search_google(keyword: str, time_filter: str, headers: dict) -> str:
    encoded = urllib.parse.quote_plus(keyword)
    url = f"https://www.google.com/search?q={encoded}"
    if time_filter and time_filter in _TIME_FILTER_MAP:
        url += f"&tbs={time_filter}"

    resp = requests.get(url, headers=headers, timeout=12)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    for g in soup.select(".g, .fP1Qef"):
        title_el = g.select_one("h3")
        link_el = g.select_one("a[href]")
        desc_el = g.select_one(".BNeawe, .VwiC3b, .yXK7lf")

        title = title_el.get_text(strip=True) if title_el else ""
        link = link_el.get("href", "") if link_el else ""
        desc = desc_el.get_text(strip=True) if desc_el else ""

        if title or desc:
            line = f"• {title}" if title else ""
            if desc:
                line += f"\n  {desc}" if line else f"• {desc}"
            if link and link.startswith("http"):
                line += f"\n  {link}"
            results.append(line)

    if not results:
        return "구글 검색 결과를 찾을 수 없습니다. (HTML 구조 변경 또는 차단 가능)"
    return "\n\n".join(results[:10])


def _search_duckduckgo(keyword: str, headers: dict) -> str:
    encoded = urllib.parse.quote_plus(keyword)
    url = f"https://duckduckgo.com/html/?q={encoded}"

    resp = requests.get(url, headers=headers, timeout=12)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    for result in soup.select(".result, .results_links"):
        title_el = result.select_one(".result__a, .result__title a, h2 a")
        snippet_el = result.select_one(".result__snippet, .result__body")

        title = title_el.get_text(strip=True) if title_el else ""
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""

        if title or snippet:
            line = f"• {title}" if title else ""
            if snippet:
                line += f"\n  {snippet}" if line else f"• {snippet}"
            results.append(line)

    if not results:
        return "DuckDuckGo 검색 결과를 찾을 수 없습니다."
    return "\n\n".join(results[:10])


def _search_wolframalpha(keyword: str, headers: dict) -> str:
    encoded = urllib.parse.quote_plus(keyword)
    url = f"https://www.wolframalpha.com/input?i={encoded}"

    resp = requests.get(url, headers=headers, timeout=12)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # WolframAlpha는 대부분 JS로 동적 로딩되어 정적 HTML에는 제한적
    text_parts = []
    for tag in soup.find_all(["p", "span", "div"], class_=lambda c: c and "output" in str(c).lower()):
        t = tag.get_text(strip=True)
        if t and len(t) > 2:
            text_parts.append(t)

    if not text_parts:
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            text_parts.append(meta["content"])
        else:
            text_parts.append("WolframAlpha는 JavaScript로 결과를 동적 로딩합니다. 정적 크롤링으로는 제한적입니다.")
            text_parts.append(f"직접 확인: {url}")

    return "\n".join(text_parts[:5]) if text_parts else "WolframAlpha 결과를 추출할 수 없습니다."


def _parse_user_request(user_request: str) -> tuple[str, str, str]:
    """user_request에서 keyword, engine, time_filter 추출"""
    req = (user_request or "").strip()
    if not req:
        return "", "duckduckgo", ""

    # 엔진 추출
    engine = "duckduckgo"
    if "구글" in req or "google" in req.lower():
        engine = "google"
    elif "울프람" in req or "wolfram" in req.lower() or "수학" in req or "계산" in req:
        engine = "wolframalpha"

    # 시간 필터 (구글용)
    time_filter = ""
    if "오늘" in req or "오늘자" in req:
        time_filter = "qdr:d"
    elif "이번 주" in req or "최근 일주일" in req or "일주일" in req:
        time_filter = "qdr:w"
    elif "이번 달" in req or "최근 한 달" in req or "한 달" in req:
        time_filter = "qdr:m"
    elif "올해" in req or "최근 일년" in req or "일년" in req:
        time_filter = "qdr:y"
    elif "최근 1시간" in req or "1시간" in req:
        time_filter = "qdr:h"

    # 검색어 추출: 검색/알려 관련 꼬리 제거
    keyword = req
    for suffix in (
        r"\s*검색해\s*줘",
        r"\s*검색해\s*줘요",
        r"\s*검색해",
        r"\s*검색",
        r"\s*알려\s*줘",
        r"\s*알려\s*줘요",
        r"\s*알려줘",
        r"\s*알려줘요",
        r"\s*찾아\s*줘",
        r"\s*찾아줘",
        r"\s*구글로\s*",
        r"\s*듀크듀크고로\s*",
        r"\s*울프람으로\s*",
    ):
        keyword = re.sub(suffix, "", keyword, flags=re.IGNORECASE).strip()

    return keyword or req, engine, time_filter


def run(user_request: str) -> str:
    """
    Host 실행용 표준 인터페이스.
    user_request에서 검색어, 엔진, 시간 필터를 추출해 universal_search를 호출합니다.
    """
    keyword, engine, time_filter = _parse_user_request(user_request)
    return universal_search(keyword=keyword, engine=engine, time_filter=time_filter)
