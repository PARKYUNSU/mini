"""텔레그램 진행 메시지 (BOT_PROGRESS, 6차 피드백 P4 — p90 81초 대기 체감 줄이기).

워커가 RAG 단계(rag_trace.mark)마다 짧은 진행 문구를 ``.bridge/progress/<job_id>.txt`` 에 쓰고,
수신기가 '⏳ 접수' 메시지를 그 문구로 고쳐 쓴다. 실패는 모두 삼킨다 — 진행 표시는 답에 영향을 주지 않는다.
"""
from __future__ import annotations

import os
from pathlib import Path

from core.config.agent_config import PROJECT_ROOT

# 단계가 끝난 뒤 불리므로 '다음에 할 일' 을 쓴다 (query 뒤 검색 → filter 뒤 판정 → judge 뒤 답 → answer 뒤 다듬기)
STAGE_TEXT = {
    "query": "🔎 논문 검색 중…",
    "filter": "⚖️ 근거 판정 중…",
    "judge": "✍️ 답 작성 중…",
    "answer": "✍️ 답 다듬는 중…",
}


def active() -> bool:
    return os.getenv("BOT_PROGRESS", "0").strip() == "1"


def _path(job_id) -> Path:
    return PROJECT_ROOT / ".bridge" / "progress" / f"{int(job_id)}.txt"


def write(job_id, stage: str) -> None:
    text = STAGE_TEXT.get(stage)
    if not text or job_id is None or not active():
        return
    try:
        p = _path(job_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(p)
    except Exception:
        pass


def read(job_id) -> str | None:
    try:
        return _path(job_id).read_text(encoding="utf-8")
    except Exception:
        return None


def clear(job_id) -> None:
    try:
        _path(job_id).unlink(missing_ok=True)
    except Exception:
        pass
