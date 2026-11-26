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


def reactions_enabled() -> bool:
    """답 메시지에 남긴 👍/👎 이모지 반응도 기록 (``BOT_FEEDBACK_REACTIONS=1``, 6차 피드백)."""
    return (os.getenv("BOT_FEEDBACK_REACTIONS") or "0").strip() == "1"


_REACTION = {"👍": "up", "👎": "down"}


def rating_from_reaction(new_reaction) -> str | None:
    """새 반응 목록에서 👍/👎 (둘 다 없으면 None — 반응을 지운 것도 None)."""
    for r in new_reaction or []:
        got = _REACTION.get(getattr(r, "emoji", None) or "")
        if got:
            return got
    return None


def _msg_path() -> Path:
    return log_path().with_name("answer_messages.jsonl")


def remember(chat_id: str, message_id: int, job_id: int) -> None:
    """답 메시지 → 잡 (이모지 반응은 메시지 id 만 준다). 실패는 삼킨다."""
    try:
        with _msg_path().open("a", encoding="utf-8") as f:
            f.write(json.dumps({"chat_id": str(chat_id), "message_id": int(message_id), "job_id": int(job_id)}) + "\n")
    except Exception:
        pass


def job_for_message(chat_id: str, message_id: int) -> int | None:
    # shortcut: 파일 전체를 읽는다 — 하루 수십 줄이라 충분, 수만 줄이 되면 sqlite 로
    try:
        for line in reversed(_msg_path().read_text(encoding="utf-8").splitlines()):
            r = json.loads(line)
            if r["chat_id"] == str(chat_id) and r["message_id"] == int(message_id):
                return int(r["job_id"])
    except Exception:
        pass
    return None


def record(job: dict[str, Any] | None, job_id: int, rating: str, chat_id: str, source: str = "button") -> dict[str, Any]:
    """평가 한 줄을 JSONL 에 덧붙이고 그 내용을 돌려준다. 잡이 지워졌어도 평가는 남긴다."""
    job = job or {}
    answer = job.get("result_text") or ""
    row = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "job_id": job_id,
        "chat_id": chat_id,
        "rating": rating,
        "source": source,
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


# ── 주간 다이제스트 항목별 👍/👎 (다이제스트 피드백 11-26 — 4주 뒤 주제별 정밀도) ──
DIGEST_PREFIX = "dg"


def digest_markup(day: str, topic: int, n_items: int, chosen: dict[int, str] | None = None) -> InlineKeyboardMarkup:
    """항목마다 한 줄: ``n 👍 · n 👎``. ``day`` 는 YYYYMMDD, 고른 쪽엔 ✅."""
    chosen = chosen or {}
    kb = InlineKeyboardMarkup()
    for i in range(1, n_items + 1):
        kb.row(*[
            InlineKeyboardButton(f"{'✅ ' if chosen.get(i) == r else ''}{i} {emo}",
                                 callback_data=f"{DIGEST_PREFIX}:{day}:{topic}:{i}:{r}")
            for r, emo in RATINGS.items()
        ])
    return kb


def parse_digest(data: str | None) -> tuple[str, int, int, str] | None:
    """``dg:<YYYYMMDD>:<주제>:<항목>:<up|down>`` → (day, topic, item, rating). 다른 데이터면 None."""
    parts = (data or "").split(":")
    if len(parts) != 5 or parts[0] != DIGEST_PREFIX or parts[4] not in RATINGS or not re.fullmatch(r"\d{8}", parts[1]):
        return None
    try:
        return parts[1], int(parts[2]), int(parts[3]), parts[4]
    except ValueError:
        return None


def chosen_from_markup(kb) -> dict[int, str]:
    """지금 키보드에서 ✅ 붙은 항목 → 평가 (다시 그릴 때 다른 항목 선택을 지키려고)."""
    out = {}
    for row in getattr(kb, "keyboard", None) or []:
        for b in row:
            p = parse_digest(getattr(b, "callback_data", None))
            if p and str(getattr(b, "text", "")).startswith("✅"):
                out[p[2]] = p[3]
    return out


def record_digest(day: str, topic: int, item: int, rating: str, chat_id: str) -> dict[str, Any]:
    """다이제스트 평가 한 줄 — 주제 · 논문은 ``.cron/digest/<YYYY-MM-DD>.json`` 에서 찾는다(못 찾아도 남긴다)."""
    iso = f"{day[:4]}-{day[4:6]}-{day[6:]}"
    paper: dict[str, Any] = {}
    topic_name = ""
    try:
        log = json.loads((PROJECT_ROOT / ".cron" / "digest" / f"{iso}.json").read_text(encoding="utf-8"))
        topic_name = log[topic]["topic"]
        paper = log[topic]["kept"][item - 1]
    except Exception:
        pass
    row = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "digest": iso, "topic_idx": topic, "topic": topic_name,
           "item": item, "paper": paper.get("id", ""), "title": paper.get("title", ""), "rating": rating,
           "chat_id": chat_id}
    p = log_path().with_name("digest_feedback.jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row
