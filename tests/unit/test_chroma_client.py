"""core.config.chroma_client — 운영 DB 만 서버로, 나머지는 로컬."""
from __future__ import annotations

import chromadb

from core.config import chroma_client as cc
from core.config.agent_config import CHROMA_DB_DIR


def test_no_server_url_uses_persistent(monkeypatch, tmp_path):
    monkeypatch.delenv("CHROMA_SERVER_URL", raising=False)
    calls = {}
    monkeypatch.setattr(chromadb, "PersistentClient", lambda path, settings: calls.setdefault("p", path))
    monkeypatch.setattr(chromadb, "HttpClient", lambda **kw: calls.setdefault("h", kw))
    cc.make_chroma_client(CHROMA_DB_DIR)
    assert "p" in calls and "h" not in calls


def test_server_url_main_db_uses_http(monkeypatch):
    monkeypatch.setenv("CHROMA_SERVER_URL", "http://127.0.0.1:8001")
    calls = {}
    monkeypatch.setattr(chromadb, "PersistentClient", lambda path, settings: calls.setdefault("p", path))
    monkeypatch.setattr(chromadb, "HttpClient", lambda **kw: calls.setdefault("h", kw))
    cc.make_chroma_client(str(CHROMA_DB_DIR))
    assert calls["h"]["host"] == "127.0.0.1" and calls["h"]["port"] == 8001 and "p" not in calls


def test_server_url_other_path_stays_local(monkeypatch, tmp_path):
    monkeypatch.setenv("CHROMA_SERVER_URL", "http://127.0.0.1:8001")
    calls = {}
    monkeypatch.setattr(chromadb, "PersistentClient", lambda path, settings: calls.setdefault("p", path))
    monkeypatch.setattr(chromadb, "HttpClient", lambda **kw: calls.setdefault("h", kw))
    cc.make_chroma_client(tmp_path / "rebuild_new")
    assert "p" in calls and "h" not in calls
