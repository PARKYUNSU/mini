"""답변 👍/👎 피드백 — 실제 사용 질문으로 평가셋을 쌓는다.

AI 워커 답변(브리지 ``graph`` 잡)의 마지막 메시지에 인라인 버튼을 달고, 누르면 질문·답·평가를
JSONL 한 줄로 남긴다. 다시 누르면 새 줄이 붙는다 — 분석은 잡별 **마지막** 줄을 쓴다.

- ``BOT_FEEDBACK_BUTTONS=0`` 이면 버튼을 달지 않는다 (기본 켬).
- 기록 위치 ``BOT_FEEDBACK_LOG`` (기본 ``.bridge/answer_feedback.jsonl`` — git 에 안 올라간다).
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.config.agent_config import PROJECT_ROOT

PREFIX = "fb"
RATINGS = {"up": "👍", "down": "👎"}
_ARXIV_ID_RE = re.compile(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b")


def enabled() -> bool:
    return (os.getenv("BOT_FEEDBACK_BUTTONS") or "1").strip() != "0"


def log_path() -> Path:
    return Path(os.getenv("BOT_FEEDBACK_LOG") or PROJECT_ROOT / ".bridge" / "answer_feedback.jsonl")


def markup(job_id: int, chosen: str | None = None) -> InlineKeyboardMarkup:
    """👍 / 👎 버튼. 고른 쪽에는 ✅ 를 붙인다 (다시 눌러 바꿀 수 있다)."""
    kb = InlineKeyboardMarkup()
    kb.row(*[
        InlineKeyboardButton(("✅ " if chosen == r else "") + emo, callback_data=f"{PREFIX}:{job_id}:{r}")
        for r, emo in RATINGS.items()
    ])
    return kb


def parse(data: str | None) -> tuple[int, str] | None:
    """``fb:<job_id>:<up|down>`` → (job_id, rating). 다른 데이터면 None."""
    parts = (data or "").split(":")
    if len(parts) != 3 or parts[0] != PREFIX or parts[2] not in RATINGS:
        return None
    try:
        return int(parts[1]), parts[2]
    except ValueError:
        return None


def record(job: dict[str, Any] | None, job_id: int, rating: str, chat_id: str) -> dict[str, Any]:
    """평가 한 줄을 JSONL 에 덧붙이고 그 내용을 돌려준다. 잡이 지워졌어도 평가는 남긴다."""
    job = job or {}
    answer = job.get("result_text") or ""
    row = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "job_id": job_id,
        "chat_id": chat_id,
        "rating": rating,
        "question": job.get("user_text") or "",
        "answer": answer,
        "answer_papers": sorted(set(_ARXIV_ID_RE.findall(answer))),
        "job_kind": job.get("job_kind") or "",
        "asked_at": job.get("created_at"),
        "job_updated_at": job.get("updated_at"),  # 전달 표시 때도 바뀐다 — 답변 시각의 근사
    }
    p = log_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row
