"""목록·동향 질문 모드 RAG_LIST_MODE (docs/experiments/list_mode_1016)."""

from core.graph import agent_nodes as N
from core.llm.agent_prompts import direct_answer_rag_user

SEP = "\n\n---\n\n"
BLOCK = "거리 0.3\n발행 2026-01-01\n[2601.00001v1] Title A\n[초록] " + "a" * 900 + "\n\n" + "body " * 300


def test_gate(monkeypatch):
    monkeypatch.setenv("RAG_LIST_MODE", "1")
    assert N.list_mode_active("LLM 탈옥 공격 논문들 정리해줘")
    assert not N.list_mode_active("RAG-Instruct 설명해줘")
    assert not N.list_mode_active("LLM 탈옥 공격 논문들 정리해줘", prefer_single_hit=True)
    monkeypatch.setenv("RAG_LIST_MODE", "0")
    assert not N.list_mode_active("LLM 탈옥 공격 논문들 정리해줘")


def test_compact_blocks_keep_head_and_short_abstract():
    out = N._compact_list_blocks(SEP.join([BLOCK, BLOCK.replace("2601.00001", "2601.00002")]))
    blocks = out.split(SEP)
    assert len(blocks) == 2
    assert blocks[0].startswith("거리 0.3\n발행 2026-01-01\n[2601.00001v1] Title A\n[초록] ")
    assert blocks[0].endswith("a" * 10) and "body" not in blocks[0]
    assert len(blocks[0].split("[초록] ")[1]) == N.LIST_MODE_ABS_CHARS


def test_compact_without_abstract_keeps_body_head():
    b = "[2601.00003] Title C\n" + "x" * 900
    out = N._compact_list_blocks(b)
    assert out.startswith("[2601.00003] Title C\n") and len(out) == len("[2601.00003] Title C\n") + 500


def test_prompt_cap():
    p = direct_answer_rag_user("", "ctx", "", "q", doc_count=10, list_mode=True)
    assert "최대 8개" in p and "4개를 넘기지" not in p
    p0 = direct_answer_rag_user("", "ctx", "", "q", doc_count=10)
    assert "4개를 넘기지" in p0
