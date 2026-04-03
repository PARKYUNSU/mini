"""
스케줄 작업 삭제. 구조화된 명령만 (LLM 없이 파싱).
예: delete JOB-A1B2 / 삭제 JOB-A1B2
"""
import re
import sys
from pathlib import Path

_CRON_ENGINE_DIR = Path(__file__).resolve().parents[4] / "tools" / "cron_engine"
sys.path.insert(0, str(_CRON_ENGINE_DIR))
from cron_api import delete_job


def run(user_request: str) -> str:
    req = (user_request or "").strip()
    m = re.match(r"(?i)^\s*(?:delete|삭제)\s+(JOB-[A-Z0-9]+)\s*$", req)
    if not m:
        return "형식: delete JOB-XXXX 또는 삭제 JOB-XXXX (한 줄)"
    return delete_job(m.group(1).upper())
