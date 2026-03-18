"""
스크래핑 기반 웹 검색 도구. DuckDuckGo(기본)·Google·WolframAlpha 지원.
최신 정보·뉴스·환율 등 검색 시 사용. HTML 구조 변경·차단에 취약하므로 DuckDuckGo 우선 권장.
네트워크 요청에 tenacity 재시도 (1분→3분→5분, 최대 3회).
"""

import re
import sys
import urllib.parse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# retry_utils (프로젝트 루트)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from retry_utils import retry_on_network_error

# 구글 봇 차단 회피용 Chrome User-Agent (완전 위장)
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

@retry_on_network_error
def _get_with_retry(url: str, headers: dict, timeout: int = 12) -> requests.Response:
    """네트워크 재시도 적용 GET 요청"""
    return requests.get(url, headers=headers, timeout=timeout)


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
    스크래핑 기반 웹 검색. DuckDuckGo(기본)·Google·WolframAlpha 지원.
    Google 실패 시 DuckDuckGo로 자동 재시도.

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
            result = _search_google(keyword, time_filter, headers)
            # Google 실패(차단/구조변경) 시 DuckDuckGo로 fallback
            if "찾을 수 없습니다" in result or "차단" in result:
                return f"[Google 실패 → DuckDuckGo로 재시도]\n\n{_search_duckduckgo(keyword, headers)}"
            return result
        if engine == "duckduckgo":
            return _search_duckduckgo(keyword, headers)
        if engine == "wolframalpha":
            return _search_wolframalpha(keyword, headers)
    except requests.exceptions.RequestException as e:
        if engine == "google":
            try:
                return f"[Google 요청 실패] DuckDuckGo로 재시도:\n\n{_search_duckduckgo(keyword, headers)}"
            except Exception:
                return f"검색 요청 오류: {e}"
        return f"검색 요청 오류: {e}"
    except Exception as e:
        if engine == "google":
            try:
                return f"[Google 처리 실패] DuckDuckGo로 재시도:\n\n{_search_duckduckgo(keyword, headers)}"
            except Exception:
                return f"검색 처리 오류: {e}"
        return f"검색 처리 오류: {e}"

    return "지원하지 않는 검색 엔진입니다."


def _search_google(keyword: str, time_filter: str, headers: dict) -> str:
    encoded = urllib.parse.quote_plus(keyword)
    url = f"https://www.google.com/search?q={encoded}"
    if time_filter and time_filter in _TIME_FILTER_MAP:
        url += f"&tbs={time_filter}"

    resp = _get_with_retry(url, headers, timeout=12)
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

    resp = _get_with_retry(url, headers, timeout=12)
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

    resp = _get_with_retry(url, headers, timeout=12)
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
            text_parts.append(
                "[WolframAlpha 제한] 이 도구는 정적 HTML만 파싱합니다. "
                "WolframAlpha는 JavaScript로 결과를 동적 로딩해, 수학·계산 결과가 추출되지 않을 수 있습니다. "
                "정확한 결과가 필요하면 wolframalpha.com에서 직접 검색하거나, 공식 API를 사용하세요."
            )
            text_parts.append(f"직접 확인: {url}")

    return "\n".join(text_parts[:5]) if text_parts else (
        "[WolframAlpha 제한] 정적 크롤링으로 결과를 추출할 수 없습니다. "
        "수학·과학 계산은 wolframalpha.com에서 직접 검색하세요."
    )


# 엔진 탐지: 문장 어디든 독립 토큰+조사 패턴만 인정. 우선순위: wolfram > google > duckduckgo
_ENGINE_PATTERNS = [
    (r"(?:^|\s)(울프람|wolfram|wolframalpha)(?:로|으로)?(?:\s|$)", "wolframalpha"),
    (r"(?:^|\s)(구글|google)(?:로|으로)?(?:\s|$)", "google"),
    (r"(?:^|\s)(듀크듀크고|duckduckgo)(?:로|으로)?(?:\s|$)", "duckduckgo"),
]

# keyword에서 제거할 엔진 토큰 (독립 토큰+조사만, 부분 문자열 제거 방지)
_ENGINE_REMOVE_PATTERNS = [
    r"(?:^|\s)(울프람|wolfram|wolframalpha)(?:로|으로)?(?=\s|$)",
    r"(?:^|\s)(구글|google)(?:로|으로)?(?=\s|$)",
    r"(?:^|\s)(듀크듀크고|duckduckgo)(?:로|으로)?(?=\s|$)",
]

# 문장 끝 suffix 제거 (검색어 손실 방지)
_SUFFIX_PATTERNS = (
    r"검색해\s*줘요?$",
    r"검색해\s*줘$",
    r"검색해\s*봐$",
    r"검색해\s*봐요?$",
    r"검색해$",
    r"검색\s*해\s*줘요?$",
    r"조회해\s*줘요?$",
    r"조회해줘$",
    r"알려\s*줘요?$",
    r"알려줘요?$",
    r"찾아\s*줘요?$",
    r"찾아줘$",
    r"보여\s*줘요?$",
    r"보여줘$",
    r"알아봐\s*줘요?$",
    r"알아봐줘$",
    r"계산해\s*줘요?$",
)


def _parse_user_request(user_request: str) -> tuple[str, str, str]:
    """
    user_request에서 keyword, engine, time_filter 추출.
    3단계: (1) 정규화 (2) 엔진·시간 탐지 (3) 엔진 토큰·suffix 제거.
    """
    req = re.sub(r"\s+", " ", (user_request or "").strip())
    if not req:
        return "", "duckduckgo", ""

    # 1단계: 시간 필터 추출 (google에서만 사용)
    time_filter = ""
    if "오늘" in req or "오늘자" in req:
        time_filter = "qdr:d"
    elif "이번 주" in req or "최근 일주일" in req or "일주일" in req:
        time_filter = "qdr:w"
    elif "이번 달" in req or "최근 한 달" in req or "한 달" in req:
        time_filter = "qdr:m"
    elif "올해" in req or "최근 일년" in req or "일년" in req:
        time_filter = "qdr:y"
    elif "최근 1시간" in req:
        time_filter = "qdr:h"

    # 2단계: 엔진 탐지 (문장 어디든, 우선순위: wolfram > google > duckduckgo)
    engine = "duckduckgo"
    for pattern, eng in _ENGINE_PATTERNS:
        if re.search(pattern, req, re.I):
            engine = eng
            break
    if engine == "duckduckgo" and ("수학" in req or "계산" in req):
        engine = "wolframalpha"  # 명시 없을 때만 의미 기반 추론

    # 3단계: keyword 정리 — 엔진 토큰 제거 후 suffix 제거
    keyword = req
    for pat in _ENGINE_REMOVE_PATTERNS:
        keyword = re.sub(pat, " ", keyword, flags=re.I)
    keyword = re.sub(r"\s+", " ", keyword).strip()

    for suffix in _SUFFIX_PATTERNS:
        keyword = re.sub(suffix, "", keyword, flags=re.IGNORECASE).strip()

    return keyword or req, engine, time_filter


def run(user_request: str) -> str:
    """
    Host 실행용 표준 인터페이스.
    user_request에서 검색어, 엔진, 시간 필터를 추출해 universal_search를 호출합니다.
    """
    keyword, engine, time_filter = _parse_user_request(user_request)
    return universal_search(keyword=keyword, engine=engine, time_filter=time_filter)
