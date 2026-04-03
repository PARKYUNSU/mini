#!/usr/bin/env python3
"""
연도 백필을 월 단위로 순차 실행 (분기보다 짧은 프로세스로 세그폴트·메모리 부담 완화).

예:
  python apps/backfill/run_backfill_monthly.py --year 2026 --category cs.AI --batch-size 15
  python apps/backfill/run_backfill_monthly.py --year 2026 --months 1-6 --continue-on-error
"""

from __future__ import annotations

import argparse
import calendar
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUN_BACKFILL = PROJECT_ROOT / "apps" / "backfill" / "run_backfill.py"


def _parse_month_list(spec: str) -> list[int]:
    """'1,2,3' 또는 '1-6' 또는 '1,3-5,12' 형태 → [1,2,3,...] (1~12, 중복 제거·정렬)."""
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a_str, b_str = part.split("-", 1)
            a, b = int(a_str.strip()), int(b_str.strip())
            for m in range(a, b + 1):
                out.append(m)
        else:
            out.append(int(part))
    seen = sorted({m for m in out if 1 <= m <= 12})
    bad = [m for m in out if m < 1 or m > 12]
    if bad:
        raise ValueError(f"월은 1~12만 허용입니다: {bad}")
    return seen


def _month_ranges(year: int, months: list[int]) -> list[tuple[str, str, str]]:
    ranges: list[tuple[str, str, str]] = []
    for m in months:
        last = calendar.monthrange(year, m)[1]
        start = f"{year}-{m:02d}-01"
        end = f"{year}-{m:02d}-{last:02d}"
        label = f"{year}-{m:02d}"
        ranges.append((start, end, label))
    return ranges


def main() -> int:
    parser = argparse.ArgumentParser(description="연도 백필을 월 단위로 실행")
    parser.add_argument("--year", type=int, required=True, help="대상 연도 (예: 2026)")
    parser.add_argument(
        "--months",
        type=str,
        default="",
        help="실행할 월만 지정 (예: 1,2,3 또는 1-6). 비우면 1~12월 전체",
    )
    parser.add_argument("--category", type=str, default="cs.AI", help="arXiv 카테고리")
    parser.add_argument("--batch-size", type=int, default=15, help="API 요청 배치 크기")
    parser.add_argument(
        "--time-limit",
        type=int,
        default=None,
        metavar="SEC",
        help="월별 최대 실행 시간(초). 지정 시 각 월에 개별 적용",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="한 달 실패해도 다음 달 계속 실행",
    )
    args = parser.parse_args()

    if not RUN_BACKFILL.is_file():
        print(f"❌ run_backfill.py 없음: {RUN_BACKFILL}")
        return 2

    raw_m = (args.months or "").strip()
    try:
        months = _parse_month_list(raw_m) if raw_m else list(range(1, 13))
    except ValueError as e:
        print(f"❌ --months 파싱 실패: {e}")
        return 2

    if not months:
        print("❌ 실행할 월이 없습니다.")
        return 2

    print(f"📌 월 필터: {', '.join(str(m) for m in months)} ({args.year}년)")

    failed: list[str] = []
    for start_date, end_date, label in _month_ranges(args.year, months):
        print("\n" + "=" * 72)
        print(f"🚀 월간 백필 시작: {label} ({start_date} ~ {end_date})")
        print("=" * 72)
        cmd = [
            sys.executable,
            str(RUN_BACKFILL),
            "--start-date",
            start_date,
            "--end-date",
            end_date,
            "--batch-size",
            str(args.batch_size),
            "--category",
            args.category,
        ]
        if args.time_limit is not None:
            cmd += ["--time-limit", str(args.time_limit)]

        rc = subprocess.call(cmd, cwd=str(PROJECT_ROOT))
        if rc != 0:
            failed.append(label)
            print(f"❌ {label} 실행 실패 (exit={rc})")
            if not args.continue_on_error:
                break
        else:
            print(f"✅ {label} 실행 완료")

    if failed:
        print(f"\n⚠️ 실패한 월: {', '.join(failed)}")
        return 1

    print("\n🎉 지정한 모든 월 백필 완료")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
