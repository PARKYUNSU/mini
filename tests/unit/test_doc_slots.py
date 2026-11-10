"""문서마다 한 칸 템플릿 (RAG_DOC_SLOTS, docs/experiments/doc_slots_1111)."""
from core.llm.agent_prompts import (
    RAG_OUTPUT_TEMPLATE_MULTI_STRICT,
    direct_answer_rag_user,
    doc_slots_template,
)


def test_one_slot_per_document_up_to_five():
    t = doc_slots_template(4)
    assert all(f"[문서 {k}]" in t for k in range(1, 5)) and "[문서 5]" not in t
    assert doc_slots_template(9).count("**{핵심 접근·시스템 이름}**") == 5
    assert "문서별 칸]" in t


def test_cap_sentence_follows_template():
    slots = direct_answer_rag_user("", "[문서 1] a\n[문서 2] b\n[문서 3] c", "", "질문", output_template_strict=doc_slots_template(3), doc_count=3)
    assert "관련 문서마다 한 칸" in slots and "넘기지 않는다" not in slots
    # 일반 템플릿은 그대로다
    base = direct_answer_rag_user("", "[문서 1] a\n[문서 2] b\n[문서 3] c", "", "질문", output_template_strict=RAG_OUTPUT_TEMPLATE_MULTI_STRICT, doc_count=3)
    assert "3개를 넘기지 않는다" in base and "관련 문서마다 한 칸" not in base
