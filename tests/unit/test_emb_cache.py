"""로컬 임베딩 캐시 경로는 현행 배치 get 경로와 결과가 같아야 한다 (docs/experiments/emb_cache_1015)."""

import json

import numpy as np

from core.rag import agent_chroma_rag as m


class _FakeCollection:
    """rows: (chunk_id, paper_id, doc, emb). get(where=$in) 은 현행 경로, get(ids=) 는 캐시 경로."""

    def __init__(self, rows):
        self.rows = rows
        self.calls = []
        self._embedding_function = lambda texts: [np.array([1.0, 0.3, -0.2])]

    def get(self, where=None, ids=None, include=()):
        if ids is not None:
            self.calls.append(("ids", len(ids)))
            hit = [r for r in self.rows if r[0] in set(ids)]
        else:
            self.calls.append(("where", len(where["paper_id"]["$in"])))
            want = set(where["paper_id"]["$in"])
            hit = [r for r in self.rows if r[1] in want]
        return {
            "ids": [r[0] for r in hit],
            "documents": [r[2] for r in hit],
            "metadatas": [{"paper_id": r[1]} for r in hit],
            "embeddings": np.array([r[3] for r in hit]) if hit else np.array([]),
        }


def _rows(n, per=5, seed=0):
    rng = np.random.default_rng(seed)
    return [
        (f"c{i}_{j}", f"2601.{i:05d}v{1 + i % 2}", f"doc{i}-{j}", rng.normal(size=3).astype(np.float32))
        for i in range(n)
        for j in range(per)
    ]


def _build_cache(tmp_path, rows):
    """scripts/build_emb_cache.py 와 같은 배치: 논문별 연속, 논문 안에서는 원래 순서."""
    pids = [m._normalize_pid(r[1]) for r in rows]
    order = sorted(range(len(rows)), key=lambda i: (pids[i], i))
    index = {}
    for row, i in enumerate(order):
        index.setdefault(pids[i], [row, row])[1] = row + 1
    np.save(tmp_path / "emb.npy", np.array([rows[i][3] for i in order], dtype=np.float64))
    np.save(tmp_path / "ids.npy", np.array([rows[i][0] for i in order], dtype="S"))
    (tmp_path / "paper_index.json").write_text(json.dumps(index))


def _use_cache(monkeypatch, tmp_path):
    monkeypatch.setenv("RAG_EMB_CACHE", "1")
    monkeypatch.setenv("RAG_EMB_CACHE_DIR", str(tmp_path))
    m._emb_cache_state.clear()


def test_cache_equals_batched_get(monkeypatch, tmp_path):
    rows = _rows(40)
    _build_cache(tmp_path, rows)
    pids = [f"2601.{i:05d}" for i in range(40)]
    monkeypatch.setenv("RAG_EMB_CACHE", "0")
    base = m._nearest_chunks_per_paper_batched(_FakeCollection(rows), pids, "q", 3)
    _use_cache(monkeypatch, tmp_path)
    fc = _FakeCollection(rows)
    got = m._nearest_chunks_per_paper_batched(fc, pids, "q", 3)
    assert fc.calls == [("ids", 120)]  # 임베딩 배치 get 없이 고른 청크만
    assert got.keys() == base.keys()
    for p in base:
        assert [(d, mt) for d, mt, _ in got[p]] == [(d, mt) for d, mt, _ in base[p]]
        assert np.allclose([x for *_, x in got[p]], [x for *_, x in base[p]], rtol=0, atol=1e-12)


def test_missing_paper_falls_back(monkeypatch, tmp_path):
    rows = _rows(10)
    _build_cache(tmp_path, rows[:25])  # 논문 0~4 만 캐시에
    _use_cache(monkeypatch, tmp_path)
    fc = _FakeCollection(rows)
    pids = [f"2601.{i:05d}" for i in range(10)]
    got = m._nearest_chunks_per_paper_batched(fc, pids, "q", 2)
    assert fc.calls == [("ids", 10), ("where", 5 * 21)]  # 캐시 5편 + 나머지 5편만 현행 경로
    assert len(got) == 10


def test_changed_ids_fall_back(monkeypatch, tmp_path):
    rows = _rows(3)
    _build_cache(tmp_path, rows)
    rows2 = [(cid + "_new", p, d, e) if p.startswith("2601.00001") else (cid, p, d, e) for cid, p, d, e in rows]
    _use_cache(monkeypatch, tmp_path)
    fc = _FakeCollection(rows2)
    got = m._nearest_chunks_per_paper_batched(fc, ["2601.00000", "2601.00001", "2601.00002"], "q", 2)
    assert fc.calls == [("ids", 6), ("where", 21)]  # ID 가 바뀐 논문 하나만 다시
    assert len(got) == 3 and all(len(v) == 2 for v in got.values())


def test_cache_off_or_missing_dir(monkeypatch, tmp_path):
    rows = _rows(3)
    monkeypatch.setenv("RAG_EMB_CACHE", "1")
    monkeypatch.setenv("RAG_EMB_CACHE_DIR", str(tmp_path / "none"))
    m._emb_cache_state.clear()
    fc = _FakeCollection(rows)
    got = m._nearest_chunks_per_paper_batched(fc, ["2601.00000"], "q", 2)
    assert fc.calls == [("where", 21)] and len(got) == 1


def _with_meta(tmp_path, rows):
    (tmp_path / "meta.json").write_text(json.dumps({"collection_rows": rows}))


def test_complete_cache_skips_absent_paper(monkeypatch, tmp_path):
    rows = _rows(5)
    _build_cache(tmp_path, rows)
    _with_meta(tmp_path, len(rows))
    _use_cache(monkeypatch, tmp_path)
    fc = _FakeCollection(rows)
    fc.count = lambda: len(rows)
    got = m._nearest_chunks_per_paper_batched(fc, ["2601.00000", "2699.99999"], "q", 2)
    assert fc.calls == [("ids", 2)]  # Chroma 에 없는 논문은 0행 조회를 하지 않는다
    assert list(got) == ["2601.00000"]


def test_grown_collection_still_falls_back(monkeypatch, tmp_path):
    rows = _rows(6)
    _build_cache(tmp_path, rows[:25])
    _with_meta(tmp_path, 25)
    _use_cache(monkeypatch, tmp_path)
    fc = _FakeCollection(rows)
    fc.count = lambda: len(rows)  # 캐시 뒤 수집됨
    got = m._nearest_chunks_per_paper_batched(fc, [f"2601.{i:05d}" for i in range(6)], "q", 2)
    assert fc.calls == [("ids", 10), ("where", 21)]  # 새 논문은 현행 경로로
    assert len(got) == 6
