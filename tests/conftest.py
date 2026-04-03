from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _is_pytest_timeout_plugin_loaded(config) -> bool:
    # pytest-timeout 플러그인은 "timeout" 관련 플러그인을 등록합니다.
    # 실행 환경에 따라 네임/클래스명이 다를 수 있어, 로드된 플러그인 목록을 문자열로 확인합니다.
    loaded = []
    try:
        loaded = [p.__class__.__name__ for p in config.pluginmanager.get_plugins()]  # type: ignore[attr-defined]
    except Exception:
        return False
    return any("Timeout" in name for name in loaded) or any("timeout" in name.lower() for name in loaded)


def pytest_configure(config) -> None:
    timeout_available = _is_pytest_timeout_plugin_loaded(config)

    # 플러그인이 없으면 UnknownMarkWarning/설정 혼동이 생기므로,
    # 마커를 "등록"해 경고를 없애고, timeout 마커를 단 테스트는 skip로 처리합니다.
    config.addinivalue_line(
        "markers",
        "timeout(timeout): pytest-timeout 미설치 환경에서는 이 마커가 실제로 강제되지 않습니다.",
    )

    config._pytest_timeout_available = timeout_available  # type: ignore[attr-defined]


def pytest_runtest_setup(item) -> None:
    timeout_available = bool(getattr(item.config, "_pytest_timeout_available", False))
    if timeout_available:
        return
    if item.get_closest_marker("timeout") is not None:
        pytest.skip("SKIP: pytest-timeout 플러그인 미설치 → timeout 마커가 실제로 동작하지 않습니다.")

