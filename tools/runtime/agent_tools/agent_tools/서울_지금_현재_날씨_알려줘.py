"""
서울 날씨: OpenWeatherMap 현재 + 미세먼지 + 24시간 예보(강수·기온 구간).
.env 에 WEATHER_API_KEY 필요. (에어/예보는 동일 키로 무료 티어에서 일반적으로 사용 가능)
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests

KST = ZoneInfo("Asia/Seoul")
SESSION = requests.Session()
TIMEOUT = 20


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


def build_seoul_weather_report() -> str:
    api_key = (os.getenv("WEATHER_API_KEY") or "").strip()
    if not api_key:
        return "오류: WEATHER_API_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인해 주세요."

    city = "Seoul"
    base = "https://api.openweathermap.org/data/2.5"
    common = {"appid": api_key, "units": "metric", "lang": "kr"}

    cur = _fetch_json(f"{base}/weather", {"q": city, **common})
    if not cur or not cur.get("main") or not cur.get("weather"):
        return "오류: 서울 현재 날씨 응답을 해석할 수 없습니다."

    m = cur["main"]
    w0 = cur["weather"][0]
    temp = m.get("temp")
    feels = m.get("feels_like")
    desc = w0.get("description", "")
    humidity = m.get("humidity")
    wind = (cur.get("wind") or {}).get("speed", 0)

    lines: list[str] = [
        f"현재 {city}의 날씨 정보:",
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

    fc = _fetch_json(f"{base}/forecast", {"q": city, **common})
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


def run(user_request: str = "") -> str:
    """호스트 도구 로더(importlib)가 우선 호출."""
    return build_seoul_weather_report()


if __name__ == "__main__":
    print(build_seoul_weather_report())
