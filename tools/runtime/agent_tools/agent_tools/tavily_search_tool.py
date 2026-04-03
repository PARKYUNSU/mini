"""
Tavily Search - AI 에이전트 유일 검색 엔진.
이 도구는 최신 인터넷 뉴스, 실시간 정보, 웹 검색이 필요할 때 무조건 사용해야 하는 유일한 검색 엔진입니다.
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv

# mini/.env 명시적 로드 (cwd 무관, 봇 재시작 후에도 최신 값 반영)
_env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_env_path, override=True)

# TAVILY_API_KEY. vly- → tvly- 자동 보정 (Tavily 공식 형식)
_raw_key = os.getenv("TAVILY_API_KEY")
_TAVILY_API_KEY = ("t" + _raw_key) if _raw_key and _raw_key.startswith("vly-") and not _raw_key.startswith("tvly-") else _raw_key

# keyword 추출용 suffix 제거 패턴
_SUFFIX_PATTERNS = (
    r"검색해\s*줘요?$",
    r"검색해\s*줘$",
    r"검색해\s*서\s*요약해\s*줘$",
    r"검색해서\s*요약해\s*줘$",
    r"검색해\s*봐$",
    r"검색해\s*봐요?$",
    r"검색해$",
    r"검색\s*해\s*줘요?$",
    r"요약해\s*줘요?$",
    r"요약해\s*줘$",
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
)


def _extract_query(user_request: str) -> str:
    """사용자 요청에서 검색 쿼리 추출. 핵심 명사 2~3개 유지."""
    req = re.sub(r"\s+", " ", (user_request or "").strip())
    if not req:
        return ""
    query = req
    for suffix in _SUFFIX_PATTERNS:
        query = re.sub(suffix, "", query, flags=re.IGNORECASE).strip()
    # 시간 부사·날짜 표현 제거 (검색 품질 향상)
    for time_word in ("오늘", "오늘자", "이번 주", "최근 일주일", "일주일", "이번 달", "최근 한 달", "한 달", "올해", "최근 일년", "일년", "최근 1시간", "9시 기준", "기준"):
        query = re.sub(re.escape(time_word), " ", query, flags=re.I).strip()
    # YYYY-MM-DD 형식 날짜 제거
    query = re.sub(r"\d{4}-\d{2}-\d{2}", " ", query).strip()
    query = re.sub(r"\s+", " ", query).strip()
    # "IT 뉴스" → "latest technology news Korea" (한국어 사용자 → 한국 IT 뉴스)
    if "IT" in query and "뉴스" in query:
        query = re.sub(r"IT\s*뉴스|IT뉴스", "technology news", query, flags=re.I).strip()
        if re.search(r"[가-힣]", req):
            query = f"latest {query} Korea"
    return query or req


def run(user_request: str) -> str:
    """
    Tavily Search로 웹 검색. .env의 TAVILY_API_KEY 사용.
    이 도구는 최신 인터넷 뉴스, 실시간 정보, 웹 검색이 필요할 때 무조건 사용해야 하는 유일한 검색 엔진입니다.

    Args:
        user_request: 사용자 검색 요청 (예: "오늘 최신 IT 뉴스 검색해 줘")

    Returns:
        검색 결과 제목·요약·링크 텍스트
    """
    if not _TAVILY_API_KEY:
        return "TAVILY_API_KEY가 .env에 설정되지 않았습니다. https://tavily.com 에서 API 키를 발급받아 .env에 추가하세요."

    query = _extract_query(user_request)
    if not query:
        return "검색어를 입력해 주세요."

    # 뉴스 검색: topic=news, time_range=day로 신뢰할 수 있는 뉴스 소스만
    is_news = any(kw in user_request for kw in ("뉴스", "news", "최신", "오늘"))
    topic = "news" if is_news else "general"
    time_range = "day" if is_news else None

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=_TAVILY_API_KEY)
        response = client.search(
            query=query,
            topic=topic,
            time_range=time_range,
            max_results=5,
        )
        result = response.get("results") or []
    except ImportError as e:
        return f"Tavily 도구 로드 실패: {e}. pip install tavily-python 실행 후 재시도하세요."
    except Exception as e:
        return f"검색 중 오류 발생: {e}"

    if not result:
        return "검색 결과가 없습니다."

    lines = []
    if isinstance(result, list):
        for item in result:
            if isinstance(item, dict):
                title = (item.get("title") or item.get("name") or "").strip()
                content = (item.get("content") or item.get("snippet") or "").strip()
                url = (item.get("url") or item.get("link") or "").strip()
                line = f"• {title}" if title else ""
                if content:
                    line += f"\n  {content}" if line else f"• {content}"
                if url and url.startswith("http"):
                    line += f"\n  {url}"
                if line:
                    lines.append(line)

    if not lines:
        return str(result) if result else "검색 결과가 없습니다."
    return "\n\n".join(lines[:10])
