#!/usr/bin/env python3
"""
CEO 뇌 복제용 SQLite 초기화 — ``CEO_Profile.sqlite`` + ``rules`` 테이블 + 시드.

기존 봇·크론과 무관하게 단독 실행.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

_MINI_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_T7 = Path("/Volumes/T7 Shield/mini/CEO_Profile.sqlite")

if len(sys.argv) > 1:
    DB_PATH = Path(sys.argv[1]).expanduser().resolve()
elif _MINI_ROOT.resolve() == Path("/Volumes/T7 Shield/mini").resolve():
    DB_PATH = _DEFAULT_T7
else:
    DB_PATH = (_MINI_ROOT / "CEO_Profile.sqlite").resolve()


SEED_ROWS: list[tuple[str, str]] = [
    (
        "coding",
        "오버엔지니어링을 절대 금지한다. 코드는 직관적이고 최대한 심플하게 작성하라.",
    ),
    (
        "security",
        "본진 코드(telegram_receiver.py 등)는 CEO의 명시적 승인 없이 절대 자율적으로 수정하지 마라.",
    ),
    (
        "architecture",
        "모든 코드는 격리된 샌드박스에서 먼저 테스트되어야 한다.",
    ),
]


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL UNIQUE,
                philosophy TEXT NOT NULL
            )
            """
        )
        for category, philosophy in SEED_ROWS:
            conn.execute(
                """
                INSERT INTO rules (category, philosophy)
                VALUES (?, ?)
                ON CONFLICT(category) DO UPDATE SET philosophy = excluded.philosophy
                """,
                (category, philosophy),
            )
        conn.commit()
    finally:
        conn.close()
    print(f"✅ CEO_Profile 준비 완료: {DB_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"❌ 실패: {e}", file=sys.stderr)
        raise SystemExit(1) from e
