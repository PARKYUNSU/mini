"""질문에 없는 rag 지우기 (docs/experiments/query_norag_1027)."""

from core.graph.agent_nodes import drop_unasked_rag


def test_drop_unasked_rag():
    q = "프롬프트를 압축해서 컨텍스트 길이를 줄이면서 성능을 유지하는 방법 알려줘"
    assert drop_unasked_rag(q, "prompt compression, context length reduction, performance preservation in rag retrieval") == \
        "prompt compression, context length reduction, performance preservation"
    assert drop_unasked_rag(q, "rag, prompt compression") == "prompt compression"
    # 질문이 RAG 를 물으면 그대로
    assert drop_unasked_rag("RAG 리랭커 연구 정리해줘", "rag reranker") == "rag reranker"
    assert drop_unasked_rag("검색 증강 생성 평가", "rag evaluation") == "rag evaluation"
    # 지우고 남는 게 없으면 원래대로
    assert drop_unasked_rag("하이브리드 검색", "rag") == "rag"
