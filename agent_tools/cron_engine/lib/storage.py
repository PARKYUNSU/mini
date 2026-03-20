#!/usr/bin/env python3
"""cron_engine 저장소. jobs.json, runs.json, stats.json 관리."""
import json
import os
from datetime import datetime

# 프로젝트 루트 기준 .cron (agent_config.CRON_JOBS_DIR 사용)
def _get_cron_dir():
    try:
        import sys
        from pathlib import Path
        root = Path(__file__).resolve().parents[3]  # cron_engine/lib/ -> mini/
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from agent_config import CRON_JOBS_DIR
        return str(CRON_JOBS_DIR)
    except ImportError:
        return os.path.join(os.path.expanduser("~"), ".cron")

CRON_DIR = _get_cron_dir()
JOBS_FILE = os.path.join(CRON_DIR, "jobs.json")
RUNS_FILE = os.path.join(CRON_DIR, "runs.json")
STATS_FILE = os.path.join(CRON_DIR, "stats.json")
JOB_RUNS_JSONL = os.path.join(CRON_DIR, "job_runs.jsonl")  # 실행 이력 (append-only)

def ensure_dir():
    os.makedirs(CRON_DIR, exist_ok=True)

def _safe_load(path, default):
    ensure_dir()
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default

def _atomic_save(path, data):
    ensure_dir()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def load_jobs():
    now = datetime.now().isoformat()
    return _safe_load(JOBS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "jobs": {}
    })

def save_jobs(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(JOBS_FILE, data)

def load_runs():
    now = datetime.now().isoformat()
    return _safe_load(RUNS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": now,
            "last_updated": now
        },
        "runs": {}
    })

def save_runs(data):
    data.setdefault("metadata", {})
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    _atomic_save(RUNS_FILE, data)

def load_stats():
    return _safe_load(STATS_FILE, {
        "total_jobs_created": 0,
        "total_jobs_paused": 0,
        "total_jobs_resumed": 0,
        "total_runs_completed": 0,
        "last_reviewed_at": None
    })

def save_stats(data):
    _atomic_save(STATS_FILE, data)


def append_job_run(evt: dict) -> None:
    """실행 이력 1줄 append (JSONL). 운영 관측용."""
    ensure_dir()
    import json
    line = json.dumps(evt, ensure_ascii=False) + "\n"
    try:
        with open(JOB_RUNS_JSONL, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        pass
