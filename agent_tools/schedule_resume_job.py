"""
스케줄 작업 재개. 일시정지된 작업을 다시 활성화합니다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "cron_engine"))
from cron_api import resume_job


def run(user_request: str) -> str:
    """
    job_id로 작업 재개. user_request에서 JOB-XXXX 형식 추출.
    """
    req = (user_request or "").strip()
    m = re.search(r"(JOB-[A-Z0-9]+)", req, re.I)
    if not m:
        return "job_id를 찾을 수 없습니다. 예: JOB-A1B2 다시 시작해줘"
    return resume_job(m.group(1).upper())
