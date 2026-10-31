"""이름 붙은 논문 찾기 (docs/experiments/name_lookup_1101)."""

from core.llm.relevance_filter import _names, names
from core.rag.agent_chroma_rag import _front_named
from core.rag.bm25_index import BM25Searcher


def test_names_keep_case_and_order():
    assert names("FActScore 계열이다. LLM-as-judge 랑 G-Eval 처럼") == ["FActScore", "LLM-as-judge", "G-Eval"]
    assert names("RAG 랑 LLM 차이") == []
    assert _names("FActScore 계열") == {"factscore"}  # 관련 문서 거르기 보호는 그대로


def _searcher(titles):
    s = BM25Searcher()
    s._papers = [{"paper_id": f"2401.{i:05d}", "title": t, "abstract": ""} for i, t in enumerate(titles)]
    s._loaded = True
    return s


def test_named_paper():
    s = _searcher([
        "FActScore: Fine-grained Atomic Evaluation", "Beyond FActScore: long text", "How LLMs react to edits",
        "ReAct: Synergizing Reasoning and Acting", "GraphRAG-Bench: a benchmark", "A GraphRAG survey", "MoE-Mamba: y",
    ])
    assert s.named_paper("FActScore") == "2401.00000"  # '이름:' 으로 시작하는 제목이 하나
    assert s.named_paper("ReAct") == "2401.00003"  # 대소문자 그대로 — 'react' 는 아니다
    assert s.named_paper("GraphRAG") is None  # 여럿이고 'GraphRAG:' 로 시작하는 제목이 없다
    assert s.named_paper("MoE-Mamba") == "2401.00006"
    assert s.named_paper("JetSpec") is None


def test_front_named():
    metas = [{"paper_id": "2401.00001v1"}, {"paper_id": "2401.00002v2"}, {"paper_id": "2401.00003v1"}]
    d, m, x = _front_named(["a", "b", "c"], metas, [0.1, 0.2, 0.3], ["2401.00003"])
    assert d == ["c", "a", "b"] and x == [0.3, 0.1, 0.2] and m[0]["paper_id"] == "2401.00003v1"
    assert _front_named(["a"], metas[:1], None, ["2409.99999"]) == (["a"], metas[:1], None)
