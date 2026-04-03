"""HITL·스레드 버전 전역 (단일 프로세스 agent_bot 또는 브리지 수신기와 공유 파일 없음)."""

from __future__ import annotations

# agent_bot 단일 프로세스 모드에서만 사용. ai_worker 브리지 모드에서는 브리지 DB를 씀.
pending_approvals: dict[str, tuple[str, dict]] = {}
thread_version: dict[str, int] = {}
