"""
스케줄 작업 일시정지. job_id로 작업을 멈춥니다.
"""
import re
import sys
from pathlib import Path

_CRON_ENGINE_DIR = Path(__file__).resolve().parents[4] / "tools" / "cron_engine"
sys.path.insert(0, str(_CRON_ENGINE_DIR))
from cron_api import pause_job


def run(user_request: str) -> str:
    """
    job_id로 작업 일시정지. user_request에서 JOB-XXXX 형식 추출.
    예: "JOB-A1B2 일시정지해줘", "JOB-A1B2 멈춰"
    """
    req = (user_request or "").strip()
    m = re.search(r"(JOB-[A-Z0-9]+)", req, re.I)
    if not m:
        return "job_id를 찾을 수 없습니다. 예: JOB-A1B2 일시정지해줘"
    return pause_job(m.group(1).upper())
