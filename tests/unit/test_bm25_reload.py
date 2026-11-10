"""BM25 색인이 JSONL 이 바뀌면 다시 지어지는지 (ops_audit_1111 — 전에는 봇 재시작 전까지 새 논문이 안 들어왔다)."""
import json
import os
import time

import pytest

from core.rag import bm25_index as b


def _paper(i):
    return json.dumps({"paper_id": f"2601.{i:05d}", "title": f"Paper {i} about retrieval", "abstract": "dense retrieval study"})


@pytest.fixture
def corpus(tmp_path, monkeypatch):
    q = tmp_path / "raw_data_queue"
    q.mkdir()
    f = q / "crawled_papers.jsonl"
    f.write_text(_paper(1) + "\n" + _paper(2) + "\n", encoding="utf-8")
    old = time.time() - 600
    os.utime(f, (old, old))
    monkeypatch.setattr(b, "PROJECT_ROOT", tmp_path)
    b.invalidate_bm25_searcher()
    monkeypatch.setattr(b, "_stale_checked_at", 0.0)
    yield f
    b.invalidate_bm25_searcher()


def _append(f, i, age):
    with f.open("a", encoding="utf-8") as w:
        w.write(_paper(i) + "\n")
    t = time.time() - age
    os.utime(f, (t, t))


def test_rebuilds_after_jsonl_changes(corpus, monkeypatch):
    s1 = b.get_bm25_searcher()
    assert s1.paper_count == 2
    _append(corpus, 3, age=300)  # 5분 전에 끝난 쓰기
    monkeypatch.setattr(b, "_stale_checked_at", 0.0)
    s2 = b.get_bm25_searcher()
    assert s2 is not s1 and s2.paper_count == 3
    assert s2.named_paper("Paper 3") == "2601.00003"


def test_same_object_when_unchanged(corpus, monkeypatch):
    s1 = b.get_bm25_searcher()
    assert s1.paper_count == 2
    monkeypatch.setattr(b, "_stale_checked_at", 0.0)
    assert b.get_bm25_searcher() is s1


def test_waits_while_file_is_being_written(corpus, monkeypatch):
    s1 = b.get_bm25_searcher()
    assert s1.paper_count == 2
    _append(corpus, 3, age=5)  # 방금 쓴 파일 — 수집 중일 수 있다
    monkeypatch.setattr(b, "_stale_checked_at", 0.0)
    assert b.get_bm25_searcher() is s1


def test_check_is_throttled(corpus, monkeypatch):
    s1 = b.get_bm25_searcher()
    assert s1.paper_count == 2
    _append(corpus, 3, age=300)
    monkeypatch.setattr(b, "_stale_checked_at", time.time())  # 방금 점검함
    assert b.get_bm25_searcher() is s1
