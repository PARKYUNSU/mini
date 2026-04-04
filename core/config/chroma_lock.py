"""Chroma DB 동시 접근 방지 — 파일 락 유틸리티.

PersistentClient(SQLite + HNSW)를 여러 프로세스가 동시 접근하면
HNSW 인덱스가 손상되어 segfault가 발생한다.

**쓰기 프로세스** (backfill, ingest_classics):
    with chroma_write_lock():
        rag_processor.add_paper(...)

**읽기 프로세스** (ai_worker → ChromaRAGTool):
    if is_chroma_write_locked():
        # JSONL 폴백 사용
    else:
        collection.query(...)
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path

from core.config.agent_config import CHROMA_WRITE_LOCK_PATH

_LOCK_PATH = Path(CHROMA_WRITE_LOCK_PATH)
_STALE_THRESHOLD_SEC = 600  # 10분 이상 된 락은 비정상 종료로 간주


def is_chroma_write_locked() -> bool:
    """Chroma 쓰기 락이 걸려 있는지 확인. 오래된 락은 자동 제거."""
    if not _LOCK_PATH.exists():
        return False
    try:
        mtime = _LOCK_PATH.stat().st_mtime
        if time.time() - mtime > _STALE_THRESHOLD_SEC:
            _LOCK_PATH.unlink(missing_ok=True)
            return False
        return True
    except OSError:
        return False


def _acquire_lock() -> None:
    _LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    _LOCK_PATH.write_text(f"pid={os.getpid()} ts={time.time():.0f}\n", encoding="utf-8")


def _release_lock() -> None:
    _LOCK_PATH.unlink(missing_ok=True)


@contextmanager
def chroma_write_lock():
    """컨텍스트 매니저: Chroma 쓰기 구간을 보호."""
    _acquire_lock()
    try:
        yield
    finally:
        _release_lock()
