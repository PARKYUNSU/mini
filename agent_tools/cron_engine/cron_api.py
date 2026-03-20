#!/usr/bin/env python3
"""
cron_engine Python API. agent_tools에서 직접 호출.
- add_job, list_jobs, pause_job, resume_job, show_job, get_due_jobs
- prompt, chat_id 필드 지원 (스케줄 실행 시 윤수르가 텔레그램 선톡)
"""
from __future__ import annotations

import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# cron_engine/lib import를 위해 경로 추가
_CRON_ROOT = Path(__file__).resolve().parent
if str(_CRON_ROOT) not in sys.path:
    sys.path.insert(0, str(_CRON_ROOT))

from lib.storage import load_jobs, save_jobs, load_stats, save_stats
from lib.schedule import compute_next_run

VALID_TYPES = ["daily", "weekly", "monthly", "interval"]


def _parse_csv(value):
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def add_job(
    title: str,
    schedule_type: str,
    prompt: str,
    chat_id: str,
    time_of_day: str = None,
    days_of_week: list = None,
    day_of_month: int = None,
    interval: int = None,
    timezone: str = "Asia/Seoul",
    notes: str = "",
) -> str:
    """
    스케줄 작업 추가. prompt는 실행 시 윤수르에게 전달되는 지시문.
    Returns: "✓ Job added: JOB-XXXX" 또는 에러 메시지
    """
    if schedule_type not in VALID_TYPES:
        return f"schedule_type은 {VALID_TYPES} 중 하나여야 합니다."
    if schedule_type in ["daily", "weekly", "monthly"] and not time_of_day:
        return "daily/weekly/monthly는 time_of_day(HH:MM)가 필요합니다."
    if schedule_type == "weekly" and not days_of_week:
        return "weekly는 days_of_week(예: mon,tue,fri)가 필요합니다."
    if schedule_type == "monthly" and not day_of_month:
        return "monthly는 day_of_month(1-31)가 필요합니다."
    if schedule_type == "interval" and not interval:
        return "interval은 interval(분)이 필요합니다."

    job_id = f"JOB-{str(uuid.uuid4())[:4].upper()}"
    now = datetime.now().isoformat()

    try:
        next_run = compute_next_run(
            schedule_type=schedule_type,
            time_of_day=time_of_day,
            days_of_week=days_of_week or [],
            day_of_month=day_of_month,
            interval=interval,
            timezone=timezone,
        )
    except Exception as e:
        return f"스케줄 계산 오류: {e}"

    job = {
        "id": job_id,
        "title": title,
        "prompt": prompt or title,
        "chat_id": chat_id,
        "status": "active",
        "schedule_type": schedule_type,
        "interval": interval,
        "time_of_day": time_of_day,
        "days_of_week": days_of_week or [],
        "day_of_month": day_of_month,
        "timezone": timezone,
        "last_run_at": None,
        "next_run_at": next_run.isoformat() if next_run else None,
        "missed_runs": 0,
        "notes": notes,
        "tags": [],
        "created_at": now,
        "updated_at": now,
    }

    data = load_jobs()
    data["jobs"][job_id] = job
    save_jobs(data)

    stats = load_stats()
    stats["total_jobs_created"] = stats.get("total_jobs_created", 0) + 1
    save_stats(stats)

    return f"✓ Job added: {job_id}\n  Title: {title}\n  Next run: {job['next_run_at']}\n  Prompt: {prompt[:50]}..."


def list_jobs() -> str:
    """등록된 스케줄 작업 목록 반환"""
    data = load_jobs()
    jobs = data.get("jobs", {})

    if not jobs:
        return "등록된 스케줄 작업이 없습니다."

    lines = []
    for job_id, job in jobs.items():
        tz = job.get("timezone") or "Asia/Seoul"
        lines.append(
            f"{job_id} | {job.get('title', '')} | {job.get('status', '')} | next={job.get('next_run_at')} ({tz})"
        )
    return "\n".join(lines)


def pause_job(job_id: str) -> str:
    """작업 일시정지"""
    data = load_jobs()
    jobs = data.get("jobs", {})

    if job_id not in jobs:
        return f"Job not found: {job_id}"

    jobs[job_id]["status"] = "paused"
    jobs[job_id]["updated_at"] = datetime.now().isoformat()
    save_jobs(data)

    stats = load_stats()
    stats["total_jobs_paused"] = stats.get("total_jobs_paused", 0) + 1
    save_stats(stats)

    return f"✓ Paused {job_id}\n  {jobs[job_id]['title']}"


def resume_job(job_id: str) -> str:
    """작업 재개"""
    data = load_jobs()
    jobs = data.get("jobs", {})

    if job_id not in jobs:
        return f"Job not found: {job_id}"

    job = jobs[job_id]
    job["status"] = "active"
    job["next_run_at"] = compute_next_run(
        schedule_type=job["schedule_type"],
        time_of_day=job.get("time_of_day"),
        days_of_week=job.get("days_of_week"),
        day_of_month=job.get("day_of_month"),
        interval=job.get("interval"),
        timezone=job.get("timezone") or "Asia/Seoul",
    ).isoformat()
    job["updated_at"] = datetime.now().isoformat()
    save_jobs(data)

    stats = load_stats()
    stats["total_jobs_resumed"] = stats.get("total_jobs_resumed", 0) + 1
    save_stats(stats)

    return f"✓ Resumed {job_id}\n  Next run: {job['next_run_at']}"


def show_job(job_id: str) -> str:
    """작업 상세 조회"""
    import json
    jobs = load_jobs().get("jobs", {})
    if job_id not in jobs:
        return f"Job not found: {job_id}"
    return json.dumps(jobs[job_id], indent=2, ensure_ascii=False)


def _zone_for_job(tz_name: str | None) -> ZoneInfo:
    name = (tz_name or "Asia/Seoul").strip() or "Asia/Seoul"
    try:
        return ZoneInfo(name)
    except Exception:
        return ZoneInfo("Asia/Seoul")


def _parse_next_run_at(iso_str: str, tz_name: str) -> datetime | None:
    """next_run_at 문자열을 해당 타임존 기준 aware datetime으로 해석 (저장값은 해당 TZ 벽시계)."""
    try:
        raw = (iso_str or "").strip()
        if not raw:
            return None
        next_at = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        tz = _zone_for_job(tz_name)
        if next_at.tzinfo is None:
            return next_at.replace(tzinfo=tz)
        return next_at.astimezone(tz)
    except (ValueError, TypeError, OSError):
        return None


def get_due_jobs(now=None):
    """
    실행 시각이 된 active 작업 목록 반환.
    각 job의 timezone(기본 Asia/Seoul) 기준으로 next_run_at과 비교. (서버 OS 타임존과 무관)
    """
    jobs = list(load_jobs().get("jobs", {}).values())
    due = []
    for j in jobs:
        if j.get("status") != "active" or not j.get("next_run_at"):
            continue
        tz_name = j.get("timezone") or "Asia/Seoul"
        tz = _zone_for_job(tz_name)
        if now is None:
            cur = datetime.now(tz)
        elif now.tzinfo is None:
            cur = now.replace(tzinfo=tz)
        else:
            cur = now.astimezone(tz)
        next_at = _parse_next_run_at(j["next_run_at"], tz_name)
        if next_at is None:
            continue
        if next_at <= cur:
            due.append(j)
    return sorted(due, key=lambda x: x.get("next_run_at", ""))


def mark_job_run(job_id: str, next_run_at: str = None) -> None:
    """작업 실행 후 next_run_at 갱신"""
    data = load_jobs()
    if job_id not in data.get("jobs", {}):
        return
    job = data["jobs"][job_id]
    job["last_run_at"] = datetime.now().isoformat()
    job["next_run_at"] = next_run_at
    job["updated_at"] = datetime.now().isoformat()
    if next_run_at is None:
        from lib.schedule import compute_next_run
        nr = compute_next_run(
            schedule_type=job["schedule_type"],
            time_of_day=job.get("time_of_day"),
            days_of_week=job.get("days_of_week"),
            day_of_month=job.get("day_of_month"),
            interval=job.get("interval"),
            timezone=job.get("timezone") or "Asia/Seoul",
        )
        job["next_run_at"] = nr.isoformat() if nr else None
    save_jobs(data)
