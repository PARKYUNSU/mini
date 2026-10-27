from core.rag.agent_chroma_rag import _fusion_protect_pids, _paper_max_one_chunk_per_paper


def test_protect_pids_needs_both_top_k():
    metas = [{"paper_id": p} for p in ("2501.00001v1", "2501.00002", "2501.00003", "2501.00002")]
    dists = [0.1, 0.3, 0.2, 0.25]
    bm = {"2501.00002": 9.0, "2501.00003": 1.0, "2501.00001": 5.0}
    assert _fusion_protect_pids(metas, dists, bm, 2) == {"2501.00001v1"}
    assert _fusion_protect_pids(metas, None, bm, 2) == set()


def test_protected_paper_takes_last_slot():
    metas = [{"paper_id": f"p{i}", "title": ""} for i in range(4)]
    docs = [f"d{i}" for i in range(4)]
    out = _paper_max_one_chunk_per_paper(docs, metas, None, [4.0, 3.0, 2.0, 1.0], 2, protect_pids={"p3"})[1]
    assert [m["paper_id"] for m in out] == ["p0", "p3"]
    out = _paper_max_one_chunk_per_paper(docs, metas, None, [4.0, 3.0, 2.0, 1.0], 2, protect_pids={"p1"})[1]
    assert [m["paper_id"] for m in out] == ["p0", "p1"]
