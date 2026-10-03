#!/usr/bin/env python3
"""
cron_engine ``.cron/jobs.json`` 에서 동일 (chat_id + 정규화 프롬프트 + 스케줄) 작업을 1건만 남기고 나머지 삭제.

무심코 같은 스케줄을 여러 번 등록하면 due 가 수천 건이 되어 매분 텔레그램이 폭주합니다.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

MINI_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MINI_ROOT / "tools" / "cron_engine"))

from lib.storage import JOBS_FILE, load_jobs, save_jobs  # noqa: E402


def normalize_prompt(p: str) -> str:
    p = (p or "").strip()
    if "[출력 언어·예약 발송]" in p:
        p = p.split("[출력 언어·예약 발송]", 1)[0].strip()
    return re.sub(r"\s+", " ", p)


def job_key(j: dict) -> tuple:
    return (
        str(j.get("chat_id") or ""),
        normalize_prompt(j.get("prompt") or j.get("title") or ""),
        j.get("schedule_type"),
        j.get("time_of_day"),
        tuple(sorted(j.get("days_of_week") or [])),
        j.get("day_of_month"),
        j.get("interval"),
        (j.get("timezone") or "Asia/Seoul").strip(),
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="cron_engine jobs.json 중복 제거")
    ap.add_argument("--dry-run", action="store_true", help="삭제 없이 통계만")
    args = ap.parse_args()

    data = load_jobs()
    jobs: dict = dict(data.get("jobs") or {})
    groups: dict[tuple, list[tuple[str, dict]]] = {}
    for jid, j in jobs.items():
        if j.get("status") != "active":
            continue
        groups.setdefault(job_key(j), []).append((jid, j))

    to_remove: list[str] = []
    for _k, lst in groups.items():
        if len(lst) <= 1:
            continue
        lst.sort(key=lambda x: (x[1].get("created_at") or "", x[0]))
        for jid, _ in lst[1:]:
            to_remove.append(jid)

    print(f"active 작업 그룹 수: {len(groups)}")
    print(f"중복으로 삭제할 레코드: {len(to_remove)} (남김 {len(jobs) - len(to_remove)})")

    if args.dry_run:
        print("(dry-run) 샘플 삭제 ID:", to_remove[:15])
        return

    path = Path(JOBS_FILE)
    if path.is_file():
        backup = path.with_suffix(path.suffix + f".bak-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        shutil.copy2(path, backup)
        print("백업:", backup)

    for jid in to_remove:
        jobs.pop(jid, None)
    data["jobs"] = jobs
    save_jobs(data)
    print(f"완료: 삭제 {len(to_remove)}건, 현재 총 {len(jobs)}건")


if __name__ == "__main__":
    main()
