"""
스케줄 작업 목록 조회. 등록된 반복 작업을 보여줍니다.
"""
import sys
from pathlib import Path

_CRON_ENGINE_DIR = Path(__file__).resolve().parents[4] / "tools" / "cron_engine"
sys.path.insert(0, str(_CRON_ENGINE_DIR))
from cron_api import list_jobs


def run(user_request: str) -> str:
    """등록된 스케줄 작업 목록 반환"""
    return list_jobs()
