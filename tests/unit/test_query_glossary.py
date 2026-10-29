from core.rag.query_glossary import add_field_terms


def test_adds_field_term_for_everyday_wording():
    q = "rag search across multiple databases duplicate content detection"
    out = add_field_terms("두 DB에서 서로 비슷하거나 같은 내용, 중복을 찾는 연구", q)
    assert out == q + ", near-duplicate detection deduplication"


def test_skips_term_already_in_query_and_caps_at_two():
    q = "citation attribution llm"
    out = add_field_terms("출처 인용 · 같은 사람 찾기 · 중복 제거 · 표에서 답 찾기", q)
    assert out == q + ", near-duplicate detection deduplication, entity resolution entity matching"


def test_leaves_korean_fallback_and_unmatched_alone():
    assert add_field_terms("중복 문서", "중복 문서") == "중복 문서"
    assert add_field_terms("에이전트 메모리 구조", "agent memory") == "agent memory"
