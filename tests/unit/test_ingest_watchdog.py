"""논문 수집 누락 감시 (apps.telegram_bot.ingest_watchdog.check_ingest)."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from apps.telegram_bot.ingest_watchdog import check_ingest

TZ = ZoneInfo("Asia/Seoul")
NOW = datetime(2026, 10, 13, 3, 35, tzinfo=TZ)


def test_before_check_time_silent(tmp_path):
    assert check_ingest(datetime(2026, 10, 13, 2, 0, tzinfo=TZ), tmp_path, False) is None


def test_missing_marker_alerts(tmp_path):
    msg = check_ingest(NOW, tmp_path, True)
    assert msg and "2026-10-13" in msg and "스케줄러" not in msg


def test_ok_marker_and_alive_silent(tmp_path):
    (tmp_path / "arxiv_pipeline_ok_2026-10-13.marker").write_text("x")
    assert check_ingest(NOW, tmp_path, True) is None


def test_dead_scheduler_alerts_even_with_marker(tmp_path):
    (tmp_path / "arxiv_pipeline_ok_2026-10-13.marker").write_text("x")
    msg = check_ingest(NOW, tmp_path, False)
    assert msg and "스케줄러 데몬" in msg


def test_once_per_day(tmp_path):
    (tmp_path / "ingest_watchdog_alert_2026-10-13.marker").write_text("x")
    assert check_ingest(NOW, tmp_path, False) is None
