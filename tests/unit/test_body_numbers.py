"""본론 항목 숫자 대조 (docs/experiments/list_findings_v2_1026)."""

from core.llm.body_numbers import check_body_numbers
from core.llm.citation_fix import RAG_HIT_SEP

CTX = RAG_HIT_SEP.join([
    "[문서 1]\n[2511.01386v1] RAGSmith\n[초록] search over 46{,}080 configurations, gains of 3.8\\%.",
    "[문서 2]\n[2606.20517v1] Multi-LCB\n[초록] extends LCB to 24 languages.",
])
IDS = {1: "2511.01386v1", 2: "2606.20517v1"}


def test_check_body_numbers():
    ans = ("<b>본론</b>\n1. <b>RAGSmith</b>: 46,080 가지 구성을 탐색한다. 약 10만 개 구성이다[2511.01386v1]\n"
           "2. <b>Multi-LCB</b>: 12개 언어로 넓힌다[2606.20517v1]\n"
           "3. <b>X</b>: 2025년 연구로 3.8% 향상[2511.01386v1]\n<b>결론</b>\n끝.")
    out, n = check_body_numbers(ans, CTX, IDS)
    assert n == 1
    assert "1. <b>RAGSmith</b>: 46,080 가지 구성을 탐색한다.[2511.01386v1]" in out
    assert "12개 언어" in out  # 문장이 하나뿐이면 항목은 그대로
    assert "3.8% 향상" in out and out.endswith("<b>결론</b>\n끝.")
