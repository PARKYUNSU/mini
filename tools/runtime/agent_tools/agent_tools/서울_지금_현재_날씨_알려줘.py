"""
OpenWeatherMap 현재·미세먼지·24h 예보(한국 전역 도시). .env에 WEATHER_API_KEY 필요.
【도구 선택】사용자가 특정 지역의 날씨·기온·미세먼지·예보를 물으면, 그곳이 대도시든 소도시(파주·분당·제주·수원 등)든 상관없이 **일반 웹 검색(Tavily 등)보다 무조건 이 날씨 도구를 최우선**으로 호출하세요.
【파라미터】도시명은 OpenWeatherMap에 넘기기 전에 **반드시 영문 표기**로 바꿉니다(예: 서울→Seoul, 파주→Paju, 부산→Busan). 한국어 지명은 아래 매핑으로 해석합니다.
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests

KST = ZoneInfo("Asia/Seoul")
SESSION = requests.Session()
TIMEOUT = 20

# 긴 키워드 먼저 (부분 문자열 오매칭 방지)
_KO_TO_EN_CITY: tuple[tuple[str, str], ...] = (
    ("서울특별시", "Seoul"),
    ("제주특별자치도", "Jeju"),
    ("부산광역시", "Busan"),
    ("대구광역시", "Daegu"),
    ("인천광역시", "Incheon"),
    ("광주광역시", "Gwangju"),
    ("대전광역시", "Daejeon"),
    ("울산광역시", "Ulsan"),
    ("파주시", "Paju"),
    ("성남시", "Seongnam"),
    ("제주시", "Jeju"),
    ("수원시", "Suwon"),
    ("고양시", "Goyang"),
    ("용인시", "Yongin"),
    ("청주시", "Cheongju"),
    ("전주시", "Jeonju"),
    ("창원시", "Changwon"),
    ("시흥시", "Siheung"),
    ("김포시", "Gimpo"),
    ("안산시", "Ansan"),
    ("안양시", "Anyang"),
    ("남양주시", "Namyangju"),
    ("하남시", "Hanam"),
    ("의정부시", "Uijeongbu"),
    ("과천시", "Gwacheon"),
    ("구리시", "Guri"),
    ("광명시", "Gwangmyeong"),
    ("군포시", "Gunpo"),
    ("오산시", "Osan"),
    ("서울", "Seoul"),
    ("제주도", "Jeju"),
    ("제주", "Jeju"),
    ("부산", "Busan"),
    ("대구", "Daegu"),
    ("인천", "Incheon"),
    ("광주", "Gwangju"),
    ("대전", "Daejeon"),
    ("울산", "Ulsan"),
    ("파주", "Paju"),
    ("분당", "Bundang"),
    ("성남", "Seongnam"),
    ("수원", "Suwon"),
    ("고양", "Goyang"),
    ("용인", "Yongin"),
    ("청주", "Cheongju"),
    ("전주", "Jeonju"),
    ("창원", "Changwon"),
    ("시흥", "Siheung"),
    ("김포", "Gimpo"),
    ("안산", "Ansan"),
    ("안양", "Anyang"),
    ("남양주", "Namyangju"),
    ("하남", "Hanam"),
    ("의정부", "Uijeongbu"),
    ("과천", "Gwacheon"),
    ("구리", "Guri"),
    ("광명", "Gwangmyeong"),
    ("군포", "Gunpo"),
    ("오산", "Osan"),
)

_EN_CITY_WORD = re.compile(
    r"\b(Seoul|Busan|Daegu|Incheon|Gwangju|Daejeon|Ulsan|Jeju|Paju|Bundang|"
    r"Suwon|Goyang|Yongin|Seongnam|Cheongju|Jeonju|Changwon|Siheung|Gimpo|Ansan|Anyang|"
    r"Namyangju|Hanam|Uijeongbu|Gwacheon|Guri|Gwangmyeong|Gunpo|Osan)\b",
    re.I,
)


def resolve_city_en_from_user_request(user_request: str) -> str:
    """사용자 문장에서 도시명을 찾아 OpenWeatherMap용 영문 도시명으로 반환. 기본은 Seoul."""
    req = (user_request or "").strip()
    if not req:
        return "Seoul"
    for ko, en in _KO_TO_EN_CITY:
        if ko in req:
            return en
    m = _EN_CITY_WORD.search(req)
    if m:
        return m.group(1).title() if m.group(1).lower() != "bundang" else "Bundang"
    return "Seoul"


def _owm_city_query(city_en: str) -> str:
    """한국 좌표 모호성 완화를 위해 ,KR 접미사 사용."""
    c = (city_en or "Seoul").strip()
    return f"{c},KR"


def _pm25_grade_kr(pm25: float) -> str:
    """대기환경정보 통합누리엑 화면과 유사한 구간(µg/m³)."""
    if pm25 <= 15:
        return "좋음"
    if pm25 <= 35:
        return "보통"
    if pm25 <= 75:
        return "나쁨"
    return "매우 나쁨"


def _owm_aqi_label(aqi: int) -> str:
    return {
        1: "좋음",
        2: "보통",
        3: "민감군 유의",
        4: "나쁨",
        5: "매우 나쁨",
    }.get(aqi, f"코드{aqi}")


def _fmt_kst(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(KST).strftime("%m/%d %H:%M")


def _fetch_json(url: str, params: dict) -> dict | None:
    try:
        r = SESSION.get(url, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError):
        return None


def build_city_weather_report(city_en: str = "Seoul") -> str:
    """OpenWeatherMap: 현재 + 미세먼지 + 24시간 예보(강수·기온 구간). city_en은 영문 도시명."""
    api_key = (os.getenv("WEATHER_API_KEY") or "").strip()
    if not api_key:
        return "오류: WEATHER_API_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인해 주세요."

    city_q = _owm_city_query(city_en)
    display_name = city_en.strip() or "Seoul"
    base = "https://api.openweathermap.org/data/2.5"
    common = {"appid": api_key, "units": "metric", "lang": "kr"}

    cur = _fetch_json(f"{base}/weather", {"q": city_q, **common})
    if not cur or not cur.get("main") or not cur.get("weather"):
        return f"오류: {display_name} 현재 날씨 응답을 해석할 수 없습니다. (도시명 영문·철자 확인)"

    m = cur["main"]
    w0 = cur["weather"][0]
    temp = m.get("temp")
    feels = m.get("feels_like")
    desc = w0.get("description", "")
    humidity = m.get("humidity")
    wind = (cur.get("wind") or {}).get("speed", 0)

    lines: list[str] = [
        f"현재 {display_name}({city_q})의 날씨 정보:",
        f"  온도: {temp}°C (체감: {feels}°C)",
        f"  날씨: {desc}",
        f"  습도: {humidity}%",
        f"  바람: {wind} m/s",
    ]

    # 현재 강수/적설
    rain_cur = cur.get("rain") or {}
    snow_cur = cur.get("snow") or {}
    if rain_cur:
        lines.append(f"  현재 강수(1h): {rain_cur.get('1h', rain_cur.get('3h', '?'))} mm")
    if snow_cur:
        lines.append(f"  현재 적설(1h): {snow_cur.get('1h', snow_cur.get('3h', '?'))} mm")

    coord = cur.get("coord") or {}
    lat, lon = coord.get("lat"), coord.get("lon")
    if lat is not None and lon is not None:
        air = _fetch_json(
            f"{base}/air_pollution",
            {"lat": lat, "lon": lon, "appid": api_key},
        )
        if air and air.get("list"):
            comp = air["list"][0].get("components") or {}
            aqi = (air["list"][0].get("main") or {}).get("aqi")
            pm25 = comp.get("pm2_5")
            pm10 = comp.get("pm10")
            if pm25 is not None:
                lines.append(
                    f"  초미세먼지(PM2.5): {pm25:.1f} µg/m³ (등급: {_pm25_grade_kr(float(pm25))})"
                )
            if pm10 is not None:
                lines.append(f"  미세먼지(PM10): {pm10:.1f} µg/m³")
            if aqi is not None:
                lines.append(f"  OWM 대기질 지수: {_owm_aqi_label(int(aqi))} (1~5단계)")
        else:
            lines.append("  미세먼지: 공기질 API 조회 실패(키·쿼터 확인).")

    fc = _fetch_json(f"{base}/forecast", {"q": city_q, **common})
    if fc and fc.get("list"):
        slots = fc["list"][:8]  # 약 24시간(3시간×8)
        temps: list[float] = []
        alerts: list[str] = []
        for it in slots:
            mm = it.get("main") or {}
            t = mm.get("temp")
            if t is not None:
                temps.append(float(t))
            pop = float(it.get("pop") or 0)
            w = (it.get("weather") or [{}])[0]
            wid = int(w.get("id") or 0)
            wdesc = w.get("description") or ""
            ts = int(it.get("dt") or 0)
            # 강수·눈·뇌우 계열 또는 강수확률 35% 이상
            wet = (200 <= wid < 600) or pop >= 0.35
            if wet:
                alerts.append(
                    f"    · {_fmt_kst(ts)} — {wdesc} (강수확률 {int(pop * 100)}%)"
                )
        if temps:
            lines.append(
                f"  향후 24시간 예보 기온 구간(3h 단위): {min(temps):.1f}°C ~ {max(temps):.1f}°C"
            )
        if alerts:
            lines.append("  돌발성 강수·눈·뇌우 가능 구간(요약):")
            lines.extend(alerts[:6])
            if len(alerts) > 6:
                lines.append(f"    · 외 {len(alerts) - 6}건 …")
        else:
            lines.append(
                "  향후 24h: 강수확률 35% 이상 또는 눈·비 예보 슬롯 없음(맑거나 약한 구름 위주)."
            )
    else:
        lines.append("  단기 예보: API 조회 실패.")

    return "\n".join(lines)


def build_seoul_weather_report() -> str:
    """호환용: 서울 고정."""
    return build_city_weather_report("Seoul")


def run(user_request: str = "") -> str:
    """
    OpenWeatherMap으로 지역 날씨 조회. run(user_request) 시그니처 유지.

    【필수 라우팅】사용자가 특정 지역의 날씨를 물어보면, 대도시·소도시(예: 파주, 분당, 제주)를 가리키든 **웹 검색보다 무조건 이 날씨 도구를 최우선**으로 사용하세요.
    【도시명】API에는 한국어 지명을 영문으로 바꿔 전달합니다(예: 서울→Seoul, 파주→Paju, 부산→Busan). 본 구현은 user_request에서 지명을 추출해 매핑합니다.
    """
    city_en = resolve_city_en_from_user_request(user_request)
    return build_city_weather_report(city_en)


if __name__ == "__main__":
    print(build_seoul_weather_report())
