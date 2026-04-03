#!/usr/bin/env python3
"""
연도 백필을 분기(Q1~Q4)로 자동 분할 실행.

예시:
  python scripts/run_backfill_quarterly.py --year 2024 --category cs.AI --batch-size 15
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUN_BACKFILL = PROJECT_ROOT / "apps" / "backfill" / "run_backfill.py"


def _quarter_ranges(year: int) -> list[tuple[str, str, str]]:
    return [
        (f"{year}-01-01", f"{year}-03-31", "Q1"),
        (f"{year}-04-01", f"{year}-06-30", "Q2"),
        (f"{year}-07-01", f"{year}-09-30", "Q3"),
        (f"{year}-10-01", f"{year}-12-31", "Q4"),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="연도 백필을 분기 단위로 실행")
    parser.add_argument("--year", type=int, required=True, help="대상 연도 (예: 2024)")
    parser.add_argument("--category", type=str, default="cs.AI", help="arXiv 카테고리")
    parser.add_argument("--batch-size", type=int, default=15, help="API 요청 배치 크기")
    parser.add_argument(
        "--time-limit",
        type=int,
        default=None,
        metavar="SEC",
        help="분기별 최대 실행 시간(초). 지정 시 각 분기에 개별 적용",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="한 분기 실패해도 다음 분기 계속 실행",
    )
    args = parser.parse_args()

    if not RUN_BACKFILL.is_file():
        print(f"❌ run_backfill.py 없음: {RUN_BACKFILL}")
        return 2

    failed: list[str] = []
    for start_date, end_date, label in _quarter_ranges(args.year):
        print("\n" + "=" * 72)
        print(f"🚀 분기 백필 시작: {args.year} {label} ({start_date} ~ {end_date})")
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
        print(f"\n⚠️ 실패 분기: {', '.join(failed)}")
        return 1

    print("\n🎉 모든 분기 백필 완료")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

