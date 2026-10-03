#!/usr/bin/env python3
"""
07:30 크론용 — 날씨·뉴스 수집 후 로컬 LLM으로 요약해 ``morning_cache.json`` 에만 저장.
텔레그램 발송 없음 (08:00 ``phase35_auto_curator`` 가 읽어 합성).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()
load_dotenv(_ROOT / ".env", override=True)

try:
    from langchain_ollama import ChatOllama  # noqa: E402
except Exception:  # pragma: no cover
    ChatOllama = None  # type: ignore[misc, assignment]

try:
    from langchain_core.messages import HumanMessage, SystemMessage  # noqa: E402
except Exception:  # pragma: no cover
    HumanMessage = None  # type: ignore[misc, assignment]
    SystemMessage = None  # type: ignore[misc, assignment]

from core.collapse_llm_repetition import sanitize_llm_news_like_blob  # noqa: E402
from core.config.agent_config import RAG_OLLAMA_TIMEOUT_SEC  # noqa: E402

# 스크래퍼·Phase35가 동일 파일을 보도록 프로젝트 루트 고정 (외장 경로 하드코딩 금지)
MORNING_CACHE_PATH = _ROOT / "morning_cache.json"

HTTP_TIMEOUT_SEC = 25
HTTP_UA = (
    "Mozilla/5.0 (compatible; HomunculusMorningScraper/1.0; "
    "+https://localhost/local-cron)"
)

SEOUL_LAT = 37.5665
SEOUL_LON = 126.9780

# Open-Meteo weather_code(WMO) → 한글
_WMO_DESCRIPTION_KO: dict[int, str] = {
    0: "맑음",
    1: "대체로 맑음",
    2: "부분적으로 흐림",
    3: "흐림",
    45: "안개",
    48: "서리 안개",
    51: "약한 이슬비",
    53: "보통 이슬비",
    55: "강한 이슬비",
    61: "약한 비",
    63: "보통 비",
    65: "강한 비",
    71: "약한 눈",
    73: "보통 눈",
    75: "강한 눈",
    77: "눈알갱이",
    80: "약한 소나기",
    81: "보통 소나기",
    82: "강한 소나기",
    85: "약한 눈 소나기",
    86: "강한 눈 소나기",
    95: "뇌우",
    96: "우박 동반 약한 뇌우",
    97: "뇌우",
    99: "심한 우박 동반 뇌우",
}


def _wmo_label_ko(code: Any) -> str:
    try:
        c = int(code)
    except (TypeError, ValueError):
        return str(code)
    return _WMO_DESCRIPTION_KO.get(c, f"코드 {c}(WMO), 상세는 기상청·Open-Meteo 코드표 참고")


def _http_get(url: str, *, accept: str | None = None) -> str:
    headers = {"User-Agent": HTTP_UA}
    if accept:
        headers["Accept"] = accept
    req = Request(url, headers=headers, method="GET")
    with urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
        raw = resp.read()
    return raw.decode("utf-8", errors="replace")


def _strip_xml_ns(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _parse_rss_titles(xml_text: str, max_items: int = 12) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return out

    def walk(elem: ET.Element) -> None:
        if len(out) >= max_items:
            return
        tag = _strip_xml_ns(elem.tag)
        if tag == "item":
            title = ""
            link = ""
            for child in elem:
                ct = _strip_xml_ns(child.tag)
                if ct == "title" and child.text:
                    title = (child.text or "").strip()
                elif ct == "link" and child.text:
                    link = (child.text or "").strip()
            if title:
                out.append((title, link))
            return
        for child in elem:
            walk(child)

    walk(root)
    return out


def collect_weather_markdown_seoul() -> str:
    """Open-Meteo: 현재·일별 + 대기질(무료)."""
    try:
        q1 = urlencode(
            {
                "latitude": SEOUL_LAT,
                "longitude": SEOUL_LON,
                "current": ",".join(
                    [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "apparent_temperature",
                        "precipitation",
                        "rain",
                        "weather_code",
                        "cloud_cover",
                        "wind_speed_10m",
                        "wind_direction_10m",
                    ]
                ),
                "daily": ",".join(
                    [
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_probability_max",
                        "sunrise",
                        "sunset",
                    ]
                ),
                "timezone": "Asia/Seoul",
                "forecast_days": 1,
            }
        )
        weather_json = json.loads(_http_get(f"https://api.open-meteo.com/v1/forecast?{q1}"))

        q2 = urlencode(
            {
                "latitude": SEOUL_LAT,
                "longitude": SEOUL_LON,
                "current": "pm10,pm2_5,european_aqi",
                "timezone": "Asia/Seoul",
            }
        )
        aq_text = _http_get(f"https://air-quality-api.open-meteo.com/v1/air-quality?{q2}")
        aq_json = json.loads(aq_text)
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as e:
        return f"(날씨 API 오류: {e})"

    try:
        cur = (weather_json.get("current") or {}) if isinstance(weather_json, dict) else {}
        daily = (weather_json.get("daily") or {}) if isinstance(weather_json, dict) else {}
        t_now = cur.get("temperature_2m")
        t_app = cur.get("apparent_temperature")
        rh = cur.get("relative_humidity_2m")
        code = cur.get("weather_code")
        wind = cur.get("wind_speed_10m")
        clouds = cur.get("cloud_cover")
        rain = cur.get("rain")

        tmax = None
        tmin = None
        pop = None
        if isinstance(daily, dict):
            tmax_l = daily.get("temperature_2m_max") or []
            tmin_l = daily.get("temperature_2m_min") or []
            pop_l = daily.get("precipitation_probability_max") or []
            if tmax_l:
                tmax = tmax_l[0]
            if tmin_l:
                tmin = tmin_l[0]
            if pop_l:
                pop = pop_l[0]

        aq_cur = (aq_json.get("current") or {}) if isinstance(aq_json, dict) else {}
        pm25 = aq_cur.get("pm2_5")
        pm10 = aq_cur.get("pm10")
        aqi = aq_cur.get("european_aqi")

        lines = [
            "**지역**: 서울 (Open-Meteo, Asia/Seoul)",
            f"- **현재 기온**: {t_now}°C (체감 {t_app}°C)" if t_now is not None else "- **현재 기온**: (데이터 없음)",
        ]
        if tmax is not None and tmin is not None:
            lines.append(f"- **오늘 최고/최저**: {tmax}°C / {tmin}°C")
        if pop is not None:
            lines.append(f"- **강수 확률(일 최대)**: {pop}%")
        if rh is not None:
            lines.append(f"- **습도**: {rh}%")
        if code is not None:
            lines.append(f"- **하늘 상태**: {_wmo_label_ko(code)}")
        if clouds is not None:
            lines.append(f"- **운량**: {clouds}%")
        if wind is not None:
            lines.append(f"- **풍속(10m)**: {wind} km/h")
        if rain is not None:
            lines.append(f"- **강우량(현재)**: {rain} mm")
        if pm25 is not None or pm10 is not None or aqi is not None:
            extra = []
            if pm25 is not None:
                extra.append(f"PM2.5 {pm25} µg/m³")
            if pm10 is not None:
                extra.append(f"PM10 {pm10} µg/m³")
            if aqi is not None:
                extra.append(f"유럽 AQI {aqi}")
            lines.append(f"- **대기**: {', '.join(extra)}")
        return "\n".join(lines)
    except Exception as e:  # noqa: BLE001
        return f"(날씨 파싱 오류: {e})"


def _google_news_ai_rss() -> str:
    # 한글 검색어 우선 — 피드 헤드라인 한국어 비중↑ (글로벌 이슈는 한글 키워드로도 잡힘)
    q = quote_plus(
        "인공지능 OR 생성형 AI OR 대규모언어모델 OR 챗봇 OR 오픈AI OR 앤트로픽 OR 구글 제미나이"
    )
    url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
    xml_text = _http_get(url, accept="application/rss+xml, text/xml, */*")
    items = _parse_rss_titles(xml_text, max_items=14)
    lines = ["[Google News — AI (한국어 피드)]", ""]
    for title, link in items:
        lines.append(f"- {title}")
        if link:
            lines.append(f"  {link}")
    return "\n".join(lines).strip()


def _techcrunch_ai_rss() -> str:
    url = "https://techcrunch.com/category/artificial-intelligence/feed/"
    xml_text = _http_get(url, accept="application/rss+xml, text/xml, */*")
    items = _parse_rss_titles(xml_text, max_items=12)
    lines = ["[TechCrunch — AI (영문 헤드라인, 요약 시 한글로 번역)]", ""]
    for title, link in items:
        lines.append(f"- {title}")
        if link:
            lines.append(f"  {link}")
    return "\n".join(lines).strip()


def _hackernews_ai_hits() -> str:
    """Algolia HN Search API (키 불필요)."""
    now = int(datetime.now(tz=timezone.utc).timestamp())
    since = now - 86400 * 2
    q = urlencode(
        {
            "tags": "story",
            "query": "AI OR LLM OR OpenAI OR Anthropic OR Gemini",
            "numericFilters": f"created_at_i>{since}",
            "hitsPerPage": "18",
        }
    )
    url = f"https://hn.algolia.com/api/v1/search?{q}"
    data = json.loads(_http_get(url, accept="application/json"))
    hits = data.get("hits") if isinstance(data, dict) else None
    if not isinstance(hits, list):
        return "[Hacker News]\n(검색 결과 없음)"
    lines = ["[Hacker News — Algolia (영문, 요약 시 한글로 번역)]", ""]
    for h in hits[:18]:
        if not isinstance(h, dict):
            continue
        title = (h.get("title") or "").strip()
        url_u = (h.get("url") or "").strip()
        story = h.get("story_text") or ""
        pts = h.get("points")
        created = h.get("created_at")
        if not title:
            continue
        line = f"- {title}"
        if pts is not None:
            line += f" (points: {pts})"
        lines.append(line)
        if created:
            lines.append(f"  시간: {created}")
        if url_u:
            lines.append(f"  {url_u}")
        elif story:
            lines.append(f"  {story[:200]}...")
    return "\n".join(lines).strip()


def collect_news_corpus() -> str:
    parts: list[str] = []
    feed_jobs: list[tuple[str, Any]] = [("google", _google_news_ai_rss)]
    if (os.environ.get("MORNING_NEWS_EN_FEEDS") or "0").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    ):
        feed_jobs.extend(
            [
                ("techcrunch", _techcrunch_ai_rss),
                ("hackernews", _hackernews_ai_hits),
            ]
        )
    for name, fn in feed_jobs:
        try:
            chunk = fn()
            parts.append(chunk)
        except Exception as e:  # noqa: BLE001
            parts.append(f"[{name} 수집 실패: {e}]")
    corpus = "\n\n".join(parts)
    if len(corpus) > 12000:
        corpus = corpus[:12000] + "\n\n…(truncated)"
    return corpus


def _hangul_syllable_count(s: str) -> int:
    return sum(1 for c in s if "\uac00" <= c <= "\ud7a3")


def _news_digest_korean_too_weak(text: str) -> bool:
    """요약이 영어 위주로 나온 경우 재시도 트리거."""
    t = (text or "").strip()
    if len(t) < 160:
        return False
    h = _hangul_syllable_count(t)
    if h >= 120:
        return False
    letters = sum(1 for c in t if c.isalpha() and ord(c) < 128)
    if letters > 220 and h < 80:
        return True
    if h < 50 and len(t) > 200:
        return True
    return False


_MORNING_NEWS_SYSTEM_KO = """당신은 한국어 AI 데일리 브리핑 에디터입니다.
규칙(위반 금지):
- 사용자에게 보여 줄 **모든 문장·목록·제목은 한국어**여야 합니다.
- 입력 코퍼스가 영어·일본어여도 **번역한 뒤 한국어로만** 씁니다.
- 예외: 회사·모델·법안 등 고유명사는 필요 시 괄호에 원문 1~3단어 병기.
- 영어로만 된 단락·영문 헤드라인을 그대로 베끼지 마세요.
- **동일 문장·동일 수치 나열을 복붙하듯 반복하지 마세요.** 한 번만 쓰고 다음 문장으로 넘어갑니다."""


def _polish_news_digest_korean(llm: Any, draft: str) -> str:
    """두 번째 패스: 초안을 통째로 한국어 브리핑으로 정제."""
    if HumanMessage is None or SystemMessage is None:
        return draft
    d = (draft or "").strip()
    if len(d) < 40:
        return draft
    try:
        msg = [
            SystemMessage(content=_MORNING_NEWS_SYSTEM_KO),
            HumanMessage(
                content=(
                    "아래는 AI 뉴스 초안입니다. **새 사실 추가 금지.** 영어 문장·영문 헤드라인·영문 불릿을 "
                    "**자연스러운 한국어로 모두 바꾼 최종 브리핑만** 출력하세요.\n"
                    "- 각 항목은 `### ` + 한글 제목.\n"
                    "- 브랜드·모델명 등 고유명사만 영문 병기 허용.\n\n---\n"
                    f"{d[:7800]}"
                )
            ),
        ]
        out = llm.invoke(msg)
        text = (getattr(out, "content", None) or str(out) or "").strip()
        return text or draft
    except Exception:  # noqa: BLE001
        return draft


def summarize_news_with_ollama(corpus: str) -> str:
    if not corpus.strip():
        return "(뉴스 원문이 비어 있어 요약을 생략합니다.)"
    if ChatOllama is None:
        return (
            "(ChatOllama 로드 실패 — 한글 요약을 할 수 없습니다. "
            "Ollama 기동 후 재실행하세요.)\n\n"
            f"--- 원문 발췌(영문 포함) ---\n{corpus[:2500]}"
        )
    model = os.environ.get("LOCAL_LLM_MODEL", "yunsur_v3:latest")
    base_url = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
    try:
        llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.15,
            timeout=float(RAG_OLLAMA_TIMEOUT_SEC or 120),
        )
        user_body = f"""아래는 여러 매체 RSS·검색에서 모은 인공지능 관련 헤드라인·링크입니다.
중복·유사 이슈를 합치고 **가장 중요한 AI 뉴스 3~5개**만 골라 마크다운으로 정리하세요.

형식(필수):
- 각 항목은 `### ` + **한글 제목 한 줄**만.
- 그 다음 줄부터 핵심 **2~4문장**, 모두 한국어.
- 출처 추정 시 한 줄 `(출처: …)` 도 한국어.
- 3개 이상 5개 이하만 출력. 서론·결론·「Here is」 같은 영어 메타 문구 금지.
- 같은 문장이나 같은 숫자·단위 조합(예: 압축 비율·초 단위 시간)을 연속·반복해 채우지 마세요.

최종 검증: 제출 전에 출력 전체에 **영어로만 된 설명 문장**이 남아 있으면 모두 한국어로 고친 뒤 출력합니다.

[원문 코퍼스]
{corpus}
"""
        if HumanMessage is not None and SystemMessage is not None:
            messages = [
                SystemMessage(content=_MORNING_NEWS_SYSTEM_KO),
                HumanMessage(content=user_body),
            ]
            resp = llm.invoke(messages)
        else:
            resp = llm.invoke(_MORNING_NEWS_SYSTEM_KO + "\n\n" + user_body)
        text = (getattr(resp, "content", None) or str(resp) or "").strip()
        text = text or "(LLM이 빈 응답을 반환했습니다.)"

        if _news_digest_korean_too_weak(text) and HumanMessage is not None:
            fix_msg = [
                SystemMessage(content=_MORNING_NEWS_SYSTEM_KO),
                HumanMessage(
                    content=(
                        "이전 답변은 한국어 비중이 너무 납니다. 아래 텍스트의 **사실 내용은 유지**하되, "
                        "표현을 전부 한국어 문장으로 다시 쓰세요. `###` 제목도 한글만.\n\n---\n"
                        f"{text[:7000]}"
                    )
                ),
            ]
            try:
                resp2 = llm.invoke(fix_msg)
                text2 = (getattr(resp2, "content", None) or str(resp2) or "").strip()
                if text2 and _hangul_syllable_count(text2) >= _hangul_syllable_count(text):
                    text = text2
            except Exception:  # noqa: BLE001
                pass

        _truthy = ("1", "true", "yes", "on")
        if (
            (os.getenv("MORNING_NEWS_ALWAYS_POLISH") or "1").strip().lower() in _truthy
            and HumanMessage is not None
        ):
            refined = _polish_news_digest_korean(llm, text)
            if refined and _hangul_syllable_count(refined) >= max(
                30,
                _hangul_syllable_count(text) - 15,
            ):
                text = refined
        return sanitize_llm_news_like_blob(text)
    except Exception as e:  # noqa: BLE001
        return (
            f"(뉴스 LLM 요약 실패: {e})\n\n"
            "--- 원문 발췌(영문 포함; Ollama 복구 후 morning_scraper 재실행 권장) ---\n"
            f"{corpus[:3500]}"
        )


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        prefix="morning_cache_",
        suffix=".json",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def run_morning_scrape(*, day_key: str | None = None) -> dict[str, Any]:
    """단일 일자 키에 대한 캐시 엔트리를 생성해 반환 (파일에도 병합 저장)."""
    key = day_key or datetime.now().strftime("%Y-%m-%d")
    entry: dict[str, Any] = {
        "weather_markdown": "",
        "news_digest_markdown": "",
        "errors": [],
    }
    try:
        entry["weather_markdown"] = collect_weather_markdown_seoul()
    except Exception as e:  # noqa: BLE001
        entry["weather_markdown"] = f"(날씨 수집 예외: {e})"
        entry["errors"].append(f"weather:{e}")

    corpus = ""
    try:
        corpus = collect_news_corpus()
    except Exception as e:  # noqa: BLE001
        entry["errors"].append(f"news_corpus:{e}")
        corpus = f"(뉴스 코퍼스 수집 실패: {e})"

    try:
        entry["news_digest_markdown"] = summarize_news_with_ollama(corpus)
    except Exception as e:  # noqa: BLE001
        entry["news_digest_markdown"] = f"(요약 단계 예외: {e})"
        entry["errors"].append(f"summary:{e}")

    entry["collected_at"] = datetime.now(tz=timezone.utc).isoformat()

    all_data: dict[str, Any] = {}
    try:
        if MORNING_CACHE_PATH.is_file():
            all_data = json.loads(MORNING_CACHE_PATH.read_text(encoding="utf-8"))
            if not isinstance(all_data, dict):
                all_data = {}
    except Exception:
        all_data = {}

    all_data[key] = entry
    try:
        _atomic_write_json(MORNING_CACHE_PATH, all_data)
    except Exception as e:  # noqa: BLE001
        entry["errors"].append(f"write:{e}")
        print(f"⚠️ morning_cache.json 저장 실패: {e}", flush=True)

    return entry


def main() -> None:
    try:
        out = run_morning_scrape()
        print(f"✅ morning_cache 저장 완료: {MORNING_CACHE_PATH}", flush=True)
        wlen = len((out.get("weather_markdown") or ""))
        nlen = len((out.get("news_digest_markdown") or ""))
        print(f"   weather chars={wlen}, news_digest chars={nlen}", flush=True)
    except Exception as e:  # noqa: BLE001
        # 최후 방어: 파일에 오늘 키로 오류만 남김 (크론은 0으로 종료해 재시도 스팸 방지)
        key = datetime.now().strftime("%Y-%m-%d")
        fallback = {
            key: {
                "weather_markdown": f"(치명적 오류: {e})",
                "news_digest_markdown": "",
                "errors": [str(e)],
                "collected_at": datetime.now(tz=timezone.utc).isoformat(),
            }
        }
        try:
            prev: dict[str, Any] = {}
            if MORNING_CACHE_PATH.is_file():
                prev = json.loads(MORNING_CACHE_PATH.read_text(encoding="utf-8"))
                if isinstance(prev, dict):
                    prev.update(fallback)
                    _atomic_write_json(MORNING_CACHE_PATH, prev)
                else:
                    _atomic_write_json(MORNING_CACHE_PATH, fallback)
            else:
                _atomic_write_json(MORNING_CACHE_PATH, fallback)
        except Exception as e2:  # noqa: BLE001
            print(f"❌ 치명 오류 후에도 저장 실패: {e2}", flush=True)
        print(f"⚠️ morning_scraper 비정상 종료(캐시에 기록 시도함): {e}", flush=True)
        raise SystemExit(0) from e


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="07:30 날씨·뉴스 캐시 수집")
    ap.add_argument(
        "--date",
        type=str,
        default=None,
        help="캐시 키 YYYY-MM-DD (기본: 오늘 로컬 날짜)",
    )
    args = ap.parse_args()
    if args.date:
        try:
            run_morning_scrape(day_key=args.date.strip())
            print(f"✅ morning_cache 갱신 키={args.date.strip()}: {MORNING_CACHE_PATH}", flush=True)
        except Exception as ex:  # noqa: BLE001
            print(f"⚠️ --date 실행 실패: {ex}", flush=True)
            raise SystemExit(0) from ex
    else:
        main()
