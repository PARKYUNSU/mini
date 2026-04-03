"""
텔레그램 수신 프로세스 ↔ AI 워커 프로세스 사이 SQLite 브리지.

stdlib + sqlite3 만 사용 (torch/chromadb/langgraph/telebot import 금지).
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

from agent_config import PROJECT_ROOT

BRIDGE_DIR = Path(os.environ.get("AGENT_BRIDGE_DIR", str(PROJECT_ROOT / ".bridge")))
BRIDGE_DB_PATH = BRIDGE_DIR / "agent_bridge.sqlite"

_local = threading.local()


def _conn() -> sqlite3.Connection:
    c = getattr(_local, "conn", None)
    if c is None:
        BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
        c = sqlite3.connect(str(BRIDGE_DB_PATH), timeout=60.0, isolation_level=None)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL;")
        c.execute("PRAGMA synchronous=NORMAL;")
        _local.conn = c
    return c


def init_bridge_db() -> None:
    con = _conn()
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS bridge_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            graph_thread_id TEXT NOT NULL,
            user_text TEXT NOT NULL,
            job_kind TEXT NOT NULL DEFAULT 'graph',
            extra_json TEXT,
            is_resume INTEGER NOT NULL DEFAULT 0,
            image_path TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            result_text TEXT,
            result_parse_mode TEXT,
            error_text TEXT,
            plan_text TEXT,
            approval_sent INTEGER NOT NULL DEFAULT 0,
            delivered INTEGER NOT NULL DEFAULT 0,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_bridge_jobs_pending ON bridge_jobs(status, id)
        WHERE status = 'pending';

        CREATE TABLE IF NOT EXISTS approval_sessions (
            chat_id TEXT PRIMARY KEY,
            graph_thread_id TEXT NOT NULL,
            source_job_id INTEGER NOT NULL,
            updated_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chat_thread_bump (
            chat_id TEXT PRIMARY KEY,
            bump INTEGER NOT NULL DEFAULT 0,
            updated_at REAL NOT NULL
        );
        """
    )


def effective_graph_thread_id(chat_id: str) -> str:
    init_bridge_db()
    con = _conn()
    row = con.execute(
        "SELECT bump FROM chat_thread_bump WHERE chat_id = ?", (chat_id,)
    ).fetchone()
    b = int(row["bump"]) if row else 0
    return f"tg_{chat_id}" if b == 0 else f"tg_{chat_id}_{b}"


def bump_chat_thread(chat_id: str) -> str:
    """취소/재시작 후 새 LangGraph 스레드 접미사."""
    init_bridge_db()
    con = _conn()
    now = time.time()
    row = con.execute(
        "SELECT bump FROM chat_thread_bump WHERE chat_id = ?", (chat_id,)
    ).fetchone()
    n = int(row["bump"]) + 1 if row else 1
    con.execute(
        """INSERT INTO chat_thread_bump(chat_id, bump, updated_at) VALUES(?,?,?)
           ON CONFLICT(chat_id) DO UPDATE SET bump=excluded.bump, updated_at=excluded.updated_at""",
        (chat_id, n, now),
    )
    return f"tg_{chat_id}_{n}"


def enqueue_job(
    *,
    chat_id: str,
    graph_thread_id: str,
    user_text: str,
    job_kind: str = "graph",
    is_resume: bool = False,
    image_path: str | None = None,
    extra: dict[str, Any] | None = None,
) -> int:
    init_bridge_db()
    con = _conn()
    now = time.time()
    ej = json.dumps(extra, ensure_ascii=False) if extra else None
    cur = con.execute(
        """INSERT INTO bridge_jobs(
            chat_id, graph_thread_id, user_text, job_kind, extra_json,
            is_resume, image_path, status, created_at, updated_at
        ) VALUES (?,?,?,?,?,?,?,'pending',?,?)""",
        (
            chat_id,
            graph_thread_id,
            user_text,
            job_kind,
            ej,
            1 if is_resume else 0,
            image_path,
            now,
            now,
        ),
    )
    return int(cur.lastrowid)


def claim_next_pending_job() -> dict[str, Any] | None:
    init_bridge_db()
    con = _conn()
    con.execute("BEGIN IMMEDIATE")
    try:
        row = con.execute(
            "SELECT id FROM bridge_jobs WHERE status = 'pending' ORDER BY id LIMIT 1"
        ).fetchone()
        if not row:
            con.execute("COMMIT")
            return None
        jid = int(row["id"])
        now = time.time()
        con.execute(
            "UPDATE bridge_jobs SET status = 'processing', updated_at = ? WHERE id = ?",
            (now, jid),
        )
        con.execute("COMMIT")
        r2 = con.execute("SELECT * FROM bridge_jobs WHERE id = ?", (jid,)).fetchone()
        return dict(r2) if r2 else None
    except Exception:
        con.execute("ROLLBACK")
        raise


def complete_job(
    job_id: int,
    *,
    result_text: str,
    result_parse_mode: str | None = None,
) -> None:
    init_bridge_db()
    con = _conn()
    now = time.time()
    con.execute(
        """UPDATE bridge_jobs SET status = 'completed', result_text = ?, result_parse_mode = ?,
           error_text = NULL, updated_at = ?, delivered = 0 WHERE id = ?""",
        (result_text, result_parse_mode, now, job_id),
    )


def fail_job(job_id: int, err: str) -> None:
    init_bridge_db()
    con = _conn()
    now = time.time()
    con.execute(
        """UPDATE bridge_jobs SET status = 'failed', error_text = ?, updated_at = ?, delivered = 0 WHERE id = ?""",
        (err[:8000], now, job_id),
    )


def set_approval_pending(job_id: int, *, plan_text: str) -> None:
    init_bridge_db()
    con = _conn()
    now = time.time()
    con.execute(
        """UPDATE bridge_jobs SET status = 'approval_pending', plan_text = ?, approval_sent = 0,
           updated_at = ? WHERE id = ?""",
        (plan_text, now, job_id),
    )


def fetch_outbound_for_receiver(limit: int = 20) -> list[dict[str, Any]]:
    init_bridge_db()
    con = _conn()
    rows = con.execute(
        """
        SELECT * FROM bridge_jobs
        WHERE (status IN ('completed', 'failed') AND delivered = 0)
           OR (status = 'approval_pending' AND approval_sent = 0)
        ORDER BY id ASC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def mark_delivered(job_id: int) -> None:
    init_bridge_db()
    con = _conn()
    now = time.time()
    con.execute(
        "UPDATE bridge_jobs SET delivered = 1, updated_at = ? WHERE id = ?",
        (now, job_id),
    )


def mark_approval_sent(job_id: int) -> None:
    init_bridge_db()
    con = _conn()
    now = time.time()
    con.execute(
        "UPDATE bridge_jobs SET approval_sent = 1, updated_at = ? WHERE id = ?",
        (now, job_id),
    )


def set_approval_session(chat_id: str, graph_thread_id: str, source_job_id: int) -> None:
    init_bridge_db()
    con = _conn()
    now = time.time()
    con.execute(
        """INSERT INTO approval_sessions(chat_id, graph_thread_id, source_job_id, updated_at)
           VALUES(?,?,?,?)
           ON CONFLICT(chat_id) DO UPDATE SET
             graph_thread_id=excluded.graph_thread_id,
             source_job_id=excluded.source_job_id,
             updated_at=excluded.updated_at""",
        (chat_id, graph_thread_id, source_job_id, now),
    )


def get_approval_session(chat_id: str) -> tuple[str, int] | None:
    init_bridge_db()
    con = _conn()
    row = con.execute(
        "SELECT graph_thread_id, source_job_id FROM approval_sessions WHERE chat_id = ?",
        (chat_id,),
    ).fetchone()
    if not row:
        return None
    return str(row["graph_thread_id"]), int(row["source_job_id"])


def clear_approval_session(chat_id: str) -> None:
    init_bridge_db()
    con = _conn()
    con.execute("DELETE FROM approval_sessions WHERE chat_id = ?", (chat_id,))


def reset_processing_stale(max_age_sec: float = 7200.0) -> None:
    """워커 비정상 종료 시 오래된 processing 을 pending 으로 되돌림."""
    init_bridge_db()
    con = _conn()
    cutoff = time.time() - max_age_sec
    con.execute(
        """UPDATE bridge_jobs SET status = 'pending', updated_at = ?
           WHERE status = 'processing' AND updated_at < ?""",
        (time.time(), cutoff),
    )
