"""
스케줄 작업 수정. 구조화된 명령만 (LLM 없이 파싱).
- edit JOB-XXXX time HH:MM
- edit JOB-XXXX prompt (나머지 전체가 새 프롬프트)
"""
import re
import sys
from pathlib import Path

_CRON_ENGINE_DIR = Path(__file__).resolve().parents[4] / "tools" / "cron_engine"
sys.path.insert(0, str(_CRON_ENGINE_DIR))
from cron_api import edit_job_prompt, edit_job_time


def run(user_request: str) -> str:
    req = (user_request or "").strip()

    m = re.match(r"(?i)^\s*edit\s+(JOB-[A-Z0-9]+)\s+time\s+(\d{1,2}:\d{2})\s*$", req)
    if m:
        return edit_job_time(m.group(1).upper(), m.group(2))

    m = re.match(r"(?i)^\s*edit\s+(JOB-[A-Z0-9]+)\s+prompt\s+(.*)$", req, re.DOTALL)
    if m:
        body = (m.group(2) or "").strip()
        if not body:
            return "프롬프트 내용이 비어 있습니다. 예: edit JOB-A1B2 prompt 오늘 IT 뉴스 요약"
        return edit_job_prompt(m.group(1).upper(), body)

    return (
        "형식:\n"
        "• edit JOB-XXXX time 09:00\n"
        "• edit JOB-XXXX prompt 실행할 때 쓸 문장 전체"
    )
