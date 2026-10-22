"""논문 단위 컨텍스트 (docs/experiments/paper_blocks_1022)."""

from core.rag.agent_chroma_rag import _format_chroma_hits

DOCS = ["A 첫 청크", "B 첫 청크", "A 둘째 청크", "C 청크"]
METAS = [{"paper_id": "2510.21440v1", "title": "A"}, {"paper_id": "2411.19463v2", "title": "B"},
         {"paper_id": "2510.21440v1", "title": "A"}, {"paper_id": "2307.03172v3", "title": "C"}]


def test_default_keeps_extra_chunks_after():
    out = _format_chroma_hits(DOCS, METAS, [0.1, 0.2, 0.3, 0.4])
    assert out.count("[2510.21440v1]") == 2  # 지금 동작: 같은 논문 추가 청크가 뒤에 붙는다


def test_one_per_paper():
    out = _format_chroma_hits(DOCS, METAS, [0.1, 0.2, 0.3, 0.4], one_per_paper=True)
    blocks = out.split("\n\n---\n\n")
    assert [b.split("] ")[0].split("[")[-1] for b in blocks if "[2" in b] == ["2510.21440v1", "2411.19463v2", "2307.03172v3"]
    assert "A 둘째 청크" not in out
