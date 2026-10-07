"""BM25 union 주입이 Chroma 의 버전 접미사 ID 를 찾는지 지킨다.

2026-10-07 retrieval_eval_1007 에서 187문항 전부 `0 BM25-only papers injected` 였다.
Chroma 는 `2005.14165v4` 를, BM25 는 `2005.14165` 를 써서 정확 일치 조회가 늘 0건이었고,
BM25 가 1위로 찾은 논문이 벡터 후보에 없으면 운영 경로에서 영영 빠졌다.
"""

from __future__ import annotations


class _FakeCollection:
    """`where={"paper_id": ...}` 의 정확 일치와 `$in` 만 흉내 낸다."""

    def __init__(self, rows: list[tuple[str, str]]):
        self.rows = rows  # (paper_id 저장값, 문서)

    def get(self, where, include, limit):
        cond = where["paper_id"]
        ok = set(cond["$in"]) if isinstance(cond, dict) else {cond}
        hits = [(pid, doc) for pid, doc in self.rows if pid in ok][:limit]
        return {
            "documents": [d for _, d in hits],
            "metadatas": [{"paper_id": p, "title": "t"} for p, _ in hits],
        }


def _merge(col, hits, metas):
    import core.rag.agent_chroma_rag as rag

    docs = ["x" * 100] * len(metas)
    return rag._merge_bm25_union_chunks(
        col, hits, docs, metas, [0.1] * len(metas), top_m=10, chunks_per_paper=2
    )


def test_injects_versioned_chroma_paper_for_unversioned_bm25_hit():
    col = _FakeCollection([("2005.14165v4", "y" * 200), ("2005.14165v4", "z" * 200)])
    docs, metas, dists, n = _merge(col, [{"paper_id": "2005.14165"}], [])
    assert n == 1
    assert [m["paper_id"] for m in metas] == ["2005.14165v4", "2005.14165v4"]
    assert dists == [None, None]


def test_skips_paper_already_in_vector_pool_across_versions():
    col = _FakeCollection([("2005.14165v4", "y" * 200)])
    _, metas, _, n = _merge(col, [{"paper_id": "2005.14165"}], [{"paper_id": "2005.14165v4"}])
    assert n == 0
    assert len(metas) == 1


class _FakeQueryCollection(_FakeCollection):
    """필터 벡터 검색: 저장된 거리 순으로 돌려준다."""

    def __init__(self, rows: list[tuple[str, str, float]]):
        super().__init__([(p, d) for p, d, _ in rows])
        self.dist = {(p, d): x for p, d, x in rows}

    def query(self, query_texts, where, n_results, include):
        ok = set(where["paper_id"]["$in"])
        hits = sorted(
            [(p, d) for p, d in self.rows if p in ok], key=lambda pd: self.dist[pd]
        )[:n_results]
        return {
            "documents": [[d for _, d in hits]],
            "metadatas": [[{"paper_id": p, "title": "t"} for p, _ in hits]],
            "distances": [[self.dist[h] for h in hits]],
        }


def test_injected_chunks_carry_real_vector_distance_when_query_given():
    """거리가 None 이면 RRF 에서 벡터 순위가 맨 뒤라 BM25 1위 논문도 못 오른다 (§8.1)."""
    import core.rag.agent_chroma_rag as rag

    col = _FakeQueryCollection([
        ("2409.09916v1", "far" * 50, 0.9),
        ("2409.09916v1", "near" * 50, 0.2),
        ("2409.09916v1", "mid" * 50, 0.5),
    ])
    docs, metas, dists, n = rag._merge_bm25_union_chunks(
        col, [{"paper_id": "2409.09916"}], [], [], [],
        top_m=10, chunks_per_paper=2, query_text="faithful small model",
    )
    assert n == 1
    assert dists == [0.2, 0.5]
    assert docs[0].startswith("near")
