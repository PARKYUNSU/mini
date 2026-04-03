"""
스케줄 작업 추가 도구. 윤수르가 "매일 아침 8시에 뉴스 줘" 같은 요청을 받으면
add_job을 사용해 jobs.json에 일정을 저장합니다.

사용 예: "매일 8시에 뉴스 요약해줘", "매주 월요일 9시에 주간 리포트 줘"
형식: user_request에서 schedule_type, time_of_day, prompt 추출
"""
import re
import sys
from pathlib import Path

# cron_engine import (repo: tools/cron_engine)
_CRON_ENGINE_DIR = Path(__file__).resolve().parents[4] / "tools" / "cron_engine"
sys.path.insert(0, str(_CRON_ENGINE_DIR))
from cron_api import add_job, VALID_TYPES

# chat_id는 config에서 전달. user_request에 |chat_id=XXX 가 있으면 사용
def _parse_add_job_request(user_request: str, chat_id: str = "") -> dict:
    """user_request에서 스케줄 정보 추출. 예: 매일 8시 뉴스 줘 -> daily, 08:00, 뉴스 요약해줘"""
    req = (user_request or "").strip()
    if not req:
        return {}

    # |chat_id=XXX 형식 추출
    if "|chat_id=" in req:
        parts = req.split("|chat_id=", 1)
        req = parts[0].strip()
        if len(parts) > 1:
            chat_id = parts[1].split("|")[0].strip() or chat_id

    # schedule_type 추출
    schedule_type = "daily"
    days_of_week = []
    day_of_month = None
    interval = None

    if re.search(r"매주|매\s*주|주간", req):
        schedule_type = "weekly"
        weekdays = {"월": "mon", "화": "tue", "수": "wed", "목": "thu", "금": "fri", "토": "sat", "일": "sun",
                    "월요일": "mon", "화요일": "tue", "수요일": "wed", "목요일": "thu", "금요일": "fri", "토요일": "sat", "일요일": "sun"}
        for kr, en in weekdays.items():
            if kr in req:
                days_of_week.append(en)
        if not days_of_week:
            days_of_week = ["mon"]
    elif re.search(r"매월|매\s*월|매달|월간", req):
        schedule_type = "monthly"
        m = re.search(r"(\d{1,2})\s*일", req)
        day_of_month = int(m.group(1)) if m else 1
    elif re.search(r"(\d+)\s*분\s*마다|(\d+)\s*분\s*간격", req):
        m = re.search(r"(\d+)\s*분", req)
        interval = int(m.group(1)) if m else 60
        schedule_type = "interval"

    # time_of_day 추출 (HH:MM)
    time_of_day = None
    if schedule_type != "interval":
        # "8시", "08:00", "아침 8시", "7시반", "오전 9시 30분"
        m = re.search(r"(?:오전|아침|오후|저녁|낮)?\s*(\d{1,2})\s*시(?:\s*반|\s*(\d{1,2})\s*분)?", req)
        if m:
            h = int(m.group(1))
            mn = 30 if re.search(r"\d\s*시\s*반", req) else int(m.group(2) or 0)
            if "오후" in req or "저녁" in req or "낮" in req:
                if h < 12:
                    h += 12
            time_of_day = f"{h:02d}:{mn:02d}"
        else:
            m = re.search(r"(\d{1,2}):(\d{2})", req)
            if m:
                time_of_day = f"{int(m.group(1)):02d}:{int(m.group(2)):02d}"
        if not time_of_day:
            time_of_day = "08:00"

    # prompt: 스케줄 표현 제거 후 남은 부분 (할 일)
    prompt = req
    for pat in [r"매일\s*", r"매주\s*", r"매월\s*", r"매\s*주\s*", r"매\s*월\s*", r"\d+\s*분\s*마다\s*",
                r"아침\s*", r"오전\s*", r"오후\s*", r"저녁\s*", r"\d{1,2}\s*시(?:\s*반|\s*\d{1,2}\s*분)?\s*",
                r"\d{1,2}:\d{2}\s*", r"월요일\s*", r"화요일\s*", r"수요일\s*", r"목요일\s*", r"금요일\s*", r"토요일\s*", r"일요일\s*",
                r"에\s*", r"에\s*줘\s*", r"에\s*해\s*줘\s*", r"마다\s*"]:
        prompt = re.sub(pat, " ", prompt, flags=re.I)
    prompt = re.sub(r"\s+", " ", prompt).strip() or "할 일을 알려주세요"

    title = prompt[:30] if len(prompt) > 30 else prompt

    return {
        "title": title,
        "schedule_type": schedule_type,
        "prompt": prompt,
        "chat_id": chat_id,
        "time_of_day": time_of_day,
        "days_of_week": days_of_week if days_of_week else None,
        "day_of_month": day_of_month,
        "interval": interval,
    }


def run(user_request: str) -> str:
    """
    스케줄 작업 추가. user_request에서 "매일 8시 뉴스 줘" 형식 파싱.
    chat_id는 환경변수 SCHEDULE_CHAT_ID 또는 user_request 내 |chat_id=XXX 로 전달.
    """
    chat_id = __import__("os").environ.get("SCHEDULE_CHAT_ID", "")
    parsed = _parse_add_job_request(user_request, chat_id)

    if not parsed:
        return "요청을 파싱할 수 없습니다. 예: 매일 8시에 뉴스 요약해줘, 매주 월요일 9시에 리포트 줘"

    if not chat_id and not parsed.get("chat_id"):
        return "chat_id가 필요합니다. 스케줄은 텔레그램 대화 중에만 등록할 수 있습니다."

    chat_id = parsed.get("chat_id") or chat_id

    return add_job(
        title=parsed["title"],
        schedule_type=parsed["schedule_type"],
        prompt=parsed["prompt"],
        chat_id=chat_id,
        time_of_day=parsed.get("time_of_day"),
        days_of_week=parsed.get("days_of_week"),
        day_of_month=parsed.get("day_of_month"),
        interval=parsed.get("interval"),
    )
