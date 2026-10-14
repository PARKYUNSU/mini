"""Chroma 클라이언트 만들기 — 서버 한 개 방식 (2026-10-14 사고 후).

로컬 ``PersistentClient`` 는 프로세스마다 HNSW 를 메모리에 따로 들고 있다가 저장하므로,
봇·스케줄러 수집·백필·평가가 같은 폴더를 열면 인덱스가 어긋난다
(docs/incidents/2026-10-14_chroma_multiwriter.md).

``CHROMA_SERVER_URL`` (예: ``http://127.0.0.1:8001``) 이 있으면 운영 DB(``CHROMA_DB_DIR``)는
그 서버(``chroma run --path <CHROMA_DB_PATH>``, launchd ``com.mini.chroma``)에 ``HttpClient`` 로 붙는다.
그 밖의 경로(도구 DB, 재구축용 새 폴더 등)나 변수가 없을 때는 지금처럼 ``PersistentClient``.
"""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

import chromadb
from chromadb.config import Settings


def chroma_server_url() -> str:
    return (os.getenv("CHROMA_SERVER_URL") or "").strip()


def _is_main_db(path: str | os.PathLike) -> bool:
    from core.config.agent_config import CHROMA_DB_DIR

    try:
        return Path(path).expanduser().resolve() == Path(CHROMA_DB_DIR).expanduser().resolve()
    except OSError:
        return False


def make_chroma_client(path: str | os.PathLike):
    """운영 DB 이고 서버 주소가 있으면 HttpClient, 아니면 PersistentClient."""
    url = chroma_server_url()
    settings = Settings(anonymized_telemetry=False)
    if url and _is_main_db(path):
        u = urlparse(url)
        return chromadb.HttpClient(host=u.hostname or "127.0.0.1", port=u.port or 8000,
                                   ssl=u.scheme == "https", settings=settings)
    return chromadb.PersistentClient(path=str(path), settings=settings)
