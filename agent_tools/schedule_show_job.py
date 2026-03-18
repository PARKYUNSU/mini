"""
스케줄 작업 상세 조회. job_id로 해당 작업의 상세 정보를 보여줍니다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "cron_engine"))
from cron_api import show_job


def run(user_request: str) -> str:
    """
    job_id로 작업 상세 조회.
    """
    req = (user_request or "").strip()
    m = re.search(r"(JOB-[A-Z0-9]+)", req, re.I)
    if not m:
        return "job_id를 찾을 수 없습니다. 예: JOB-A1B2 자세히 보여줘"
    return show_job(m.group(1).upper())
