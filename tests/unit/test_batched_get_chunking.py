"""배치 get 을 SQL 변수 한도 아래로 나눠도 한 번에 가져온 것과 결과가 같아야 한다."""

import numpy as np

from core.rag import agent_chroma_rag as m


class _FakeCollection:
    def __init__(self, rows, max_ids=None):
        self.rows = rows  # (paper_id, doc, emb)
        self.max_ids = max_ids
        self.calls = 0
        self._embedding_function = lambda texts: [np.array([1.0, 0.0])]

    def get(self, where, include):
        ids = where["paper_id"]["$in"]
        self.calls += 1
        if self.max_ids is not None and len(ids) > self.max_ids:
            raise RuntimeError("too many SQL variables")
        hit = [r for r in self.rows if r[0] in set(ids)]
        return {
            "documents": [r[1] for r in hit],
            "metadatas": [{"paper_id": r[0]} for r in hit],
            "embeddings": np.array([r[2] for r in hit]) if hit else np.array([]),
        }


def _rows(n):
    rng = np.random.default_rng(0)
    return [(f"2601.{i:05d}", f"doc{i}-{j}", rng.normal(size=2)) for i in range(n) for j in range(3)]


def test_chunked_equals_single(monkeypatch):
    rows = _rows(60)
    pids = [f"2601.{i:05d}" for i in range(60)]
    monkeypatch.setattr(m, "_BATCHED_GET_MAX_IDS", 10_000)
    one = m._nearest_chunks_per_paper_batched(_FakeCollection(rows), pids, "q", 2)
    monkeypatch.setattr(m, "_BATCHED_GET_MAX_IDS", 798)
    fc = _FakeCollection(rows, max_ids=999)
    many = m._nearest_chunks_per_paper_batched(fc, pids, "q", 2)
    assert fc.calls == 3  # 한 번에(1260 > 999 실패) → 798 + 462
    assert one == many and len(many) == 60


def test_empty_part_skipped(monkeypatch):
    monkeypatch.setattr(m, "_BATCHED_GET_MAX_IDS", 21)
    rows = _rows(1)
    out = m._nearest_chunks_per_paper_batched(_FakeCollection(rows), ["2601.00000", "2699.99999"], "q", 2)
    assert list(out) == ["2601.00000"]


def test_single_call_when_it_fits(monkeypatch):
    monkeypatch.setattr(m, "_BATCHED_GET_MAX_IDS", 21)
    fc = _FakeCollection(_rows(5), max_ids=999)
    out = m._nearest_chunks_per_paper_batched(fc, [f"2601.{i:05d}" for i in range(5)], "q", 2)
    assert fc.calls == 1 and len(out) == 5  # 한도 안이면 나누지 않는다
