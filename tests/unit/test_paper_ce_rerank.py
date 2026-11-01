"""논문 단위 cross-encoder 재순위 (docs/experiments/ce_rerank_1101)."""

import numpy as np

import core.rag.agent_chroma_rag as acr


class _FakeCE:
    def __init__(self, scores):
        self.scores, self.pairs = scores, []

    def predict(self, pairs):
        self.pairs = pairs
        return np.array(self.scores[: len(pairs)])


def _pool(n):
    metas = [{"paper_id": f"2401.{i:05d}", "title": f"T{i} ", "abstract": f" a{i}\n b "} for i in range(n)]
    return [(1.0 - i / 100, i, f"p{i}") for i in range(n)], metas


def test_rrf_top30_and_tail(monkeypatch):
    best, metas = _pool(35)
    fake = _FakeCE([0.0] * 29 + [9.0])  # 30위를 CE 1위로
    monkeypatch.setattr(acr, "_get_paper_ce", lambda: fake)
    out = [p for _, _, p in acr._paper_ce_rerank("q", best, metas)]
    assert len(fake.pairs) == 30 and fake.pairs[0] == ("q", "T0. a0 b")
    # p29: 1/90 + 1/61 — p11(1/72 + 1/73) 보다 작고 p12(1/73 + 1/74) 보다 크다. 31위 아래는 그대로
    assert out == [f"p{i}" for i in range(12)] + ["p29"] + [f"p{i}" for i in range(12, 29)] + [f"p{i}" for i in range(30, 35)]


def test_failure_keeps_order(monkeypatch):
    best, metas = _pool(3)

    def boom():
        raise OSError("no model")

    monkeypatch.setattr(acr, "_get_paper_ce", boom)
    assert acr._paper_ce_rerank("q", best, metas) == best


def test_flag_runs_after_light_rerank(monkeypatch):
    calls = []
    monkeypatch.setattr(acr, "ENABLE_PAPER_LIGHT_RERANK", True)
    monkeypatch.setattr(acr, "_light_rerank_paper_pool_by_embedding", lambda q, pb, d, m, k, **kw: pb)
    monkeypatch.setattr(acr, "_paper_ce_rerank", lambda q, pb, m: calls.append(q) or pb[::-1])
    docs, metas = ["x", "y"], [{"paper_id": "2401.00001"}, {"paper_id": "2401.00002"}]
    monkeypatch.delenv("RAG_PAPER_CE_RERANK", raising=False)
    assert acr._paper_max_one_chunk_per_paper(docs, metas, None, [0.9, 0.1], 2, light_rerank_query="q")[0] == ["x", "y"]
    assert calls == []
    monkeypatch.setenv("RAG_PAPER_CE_RERANK", "1")
    assert acr._paper_max_one_chunk_per_paper(docs, metas, None, [0.9, 0.1], 2, light_rerank_query="q")[0] == ["y", "x"]
    assert calls == ["q"]
    assert acr._paper_max_one_chunk_per_paper(docs, metas, None, [0.9, 0.1], 2, light_rerank_query="")[0] == ["x", "y"]
    assert calls == ["q"]  # 가벼운 재순위가 안 돌면 CE 도 안 돈다
