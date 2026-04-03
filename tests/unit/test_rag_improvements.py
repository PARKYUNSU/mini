"""RAG 개선 PR 테스트: dedupe, reverse_readline, wants_depth, rag_context state 전달."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))


# ─── M1: _dedupe_hits_by_paper ───


def test_dedupe_hits_by_paper_reorders_same_pid():
    from core.rag.agent_chroma_rag import _dedupe_hits_by_paper

    docs = ["chunk A1", "chunk A2", "chunk B1", "chunk A3"]
    metas = [
        {"paper_id": "A"},
        {"paper_id": "A"},
        {"paper_id": "B"},
        {"paper_id": "A"},
    ]
    result = _dedupe_hits_by_paper(docs, metas)
    pids = [m["paper_id"] for _, m in result]
    assert pids == ["A", "B", "A", "A"], f"Expected A,B then extras but got {pids}"
    assert result[0][0] == "chunk A1"
    assert result[1][0] == "chunk B1"


def test_dedupe_hits_by_paper_no_pid():
    from core.rag.agent_chroma_rag import _dedupe_hits_by_paper

    docs = ["c1", "c2", "c3"]
    metas = [{"paper_id": ""}, {}, {"paper_id": ""}]
    result = _dedupe_hits_by_paper(docs, metas)
    assert len(result) == 3
    assert [d for d, _ in result] == ["c1", "c2", "c3"]


def test_dedupe_hits_by_paper_all_unique():
    from core.rag.agent_chroma_rag import _dedupe_hits_by_paper

    docs = ["c1", "c2", "c3"]
    metas = [{"paper_id": "A"}, {"paper_id": "B"}, {"paper_id": "C"}]
    result = _dedupe_hits_by_paper(docs, metas)
    pids = [m["paper_id"] for _, m in result]
    assert pids == ["A", "B", "C"]


def test_format_chroma_hits_uses_dedupe():
    from core.rag.agent_chroma_rag import _format_chroma_hits

    docs = ["body1", "body2", "body3"]
    metas = [
        {"paper_id": "X", "title": "X Paper"},
        {"paper_id": "X", "title": "X Paper"},
        {"paper_id": "Y", "title": "Y Paper"},
    ]
    text = _format_chroma_hits(docs, metas)
    blocks = text.split("\n\n---\n\n")
    assert "[X]" in blocks[0]
    assert "[Y]" in blocks[1]


# ─── S4: _reverse_readline ───


def test_reverse_readline_order():
    from core.rag.agent_chroma_rag import _reverse_readline

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        for i in range(50):
            f.write(json.dumps({"idx": i}) + "\n")
        fpath = Path(f.name)

    try:
        lines = list(_reverse_readline(fpath))
        parsed = [json.loads(ln) for ln in lines if ln.strip()]
        assert len(parsed) == 50
        assert parsed[0]["idx"] == 49, "Should read from end first"
        assert parsed[-1]["idx"] == 0
    finally:
        fpath.unlink(missing_ok=True)


def test_reverse_readline_empty_file():
    from core.rag.agent_chroma_rag import _reverse_readline

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        fpath = Path(f.name)
    try:
        lines = [ln for ln in _reverse_readline(fpath) if ln.strip()]
        assert lines == []
    finally:
        fpath.unlink(missing_ok=True)


def test_reverse_readline_single_line():
    from core.rag.agent_chroma_rag import _reverse_readline

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        f.write('{"only": true}\n')
        fpath = Path(f.name)
    try:
        lines = [ln for ln in _reverse_readline(fpath) if ln.strip()]
        assert len(lines) == 1
        assert json.loads(lines[0])["only"] is True
    finally:
        fpath.unlink(missing_ok=True)


# ─── S2: _prefer_single_hit_rag_context (wants_depth 반영) ───


def test_prefer_single_depth_true():
    from core.graph.agent_nodes import _prefer_single_hit_rag_context

    assert _prefer_single_hit_rag_context("transformer 논문 자세히 알려줘", wants_depth=True) is True


def test_prefer_single_depth_false_multi_keywords():
    from core.graph.agent_nodes import _prefer_single_hit_rag_context

    assert _prefer_single_hit_rag_context("여러 논문 비교해줘", wants_depth=True) is False
    assert _prefer_single_hit_rag_context("서베이 해줘", wants_depth=True) is False


def test_prefer_single_no_depth_short():
    from core.graph.agent_nodes import _prefer_single_hit_rag_context

    assert _prefer_single_hit_rag_context("GPT 요약", wants_depth=False) is True


def test_prefer_single_no_depth_long_no_keyword():
    from core.graph.agent_nodes import _prefer_single_hit_rag_context

    long_q = "이 논문에서 사용한 모델 아키텍처가 기존 방법론 대비 어떤 장점이 있는지 상세하게 분석해줘"
    assert _prefer_single_hit_rag_context(long_q, wants_depth=False) is False


# ─── M3: rag_context in AgentState ───


def test_agent_state_has_rag_context_field():
    from core.graph.agent_types import AgentState

    hints = AgentState.__annotations__
    assert "rag_context" in hints, "AgentState should have rag_context field"
