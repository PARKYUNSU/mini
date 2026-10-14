"""core.graph.agent_nodes 비교 질문 분리 검색 — 블록 합치기."""
from core.graph.agent_nodes import _RAG_HIT_SEP, _merge_rag_blocks


def _blk(pid: str, text: str = "x") -> str:
    return f"[paper_id: {pid}v1]\n{text}"


def test_merge_puts_targets_first_and_dedupes():
    primary = _RAG_HIT_SEP.join([_blk("2401.00001"), _blk("2401.00002"), _blk("2401.00003")])
    a = _RAG_HIT_SEP.join([_blk("2402.00001"), _blk("2401.00001"), _blk("2402.00009")])
    b = _RAG_HIT_SEP.join([_blk("2403.00001")])
    out = _merge_rag_blocks(primary, [a, b]).split(_RAG_HIT_SEP)
    pids = [o.split("]")[0][len("[paper_id: "):] for o in out]
    assert pids == ["2402.00001v1", "2401.00001v1", "2403.00001v1", "2401.00002v1", "2401.00003v1"]


def test_merge_skips_empty_and_errors():
    primary = _blk("2401.00001")
    assert _merge_rag_blocks(primary, ["관련 문서 없음", "", "검색 오류: x"]) == primary
