from core.rag.agent_chroma_rag import _paper_max_one_chunk_per_paper


def test_protected_paper_takes_last_slot():
    metas = [{"paper_id": f"p{i}", "title": ""} for i in range(4)]
    docs = [f"d{i}" for i in range(4)]
    out = _paper_max_one_chunk_per_paper(docs, metas, None, [4.0, 3.0, 2.0, 1.0], 2, protect_pids={"p3"})[1]
    assert [m["paper_id"] for m in out] == ["p0", "p3"]
    out = _paper_max_one_chunk_per_paper(docs, metas, None, [4.0, 3.0, 2.0, 1.0], 2, protect_pids={"p1"})[1]
    assert [m["paper_id"] for m in out] == ["p0", "p1"]
