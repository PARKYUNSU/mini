"""결론 다시 쓰기의 대상 고르기 · 숫자 검사 (docs/experiments/conclusion_rewrite_1021)."""

from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.conclusion_rewrite import check_conclusion, cited_blocks, replace_conclusion

CTX = RAG_HIT_SEP.join([
    "[문서 1]\n[2601.14123v1] Chunking\n[초록] sentence chunking is the most cost-effective; overlap gives no benefit.",
    "[문서 2]\n[2603.25333v1] Adaptive\n[초록] correctness to 72% (from 62-64%).",
    "[문서 3]\n[2506.16035v2] Vision\n[초록] curated dataset, qualitative analysis.",
])
IDS = {1: "2601.14123v1", 2: "2603.25333v1", 3: "2506.16035v2"}
ANS = "<b>서론</b>\n…\n<b>본론</b>\n1. <b>A</b>: …[2601.14123v1]\n2. <b>B</b>: …[2603.25333v1]\n<b>결론</b>\n상투어."


def test_cited_blocks_only_body_papers():
    assert set(cited_blocks(ANS, CTX, IDS)) == {1, 2}


def test_check_numbers_must_be_in_cited_block():
    blocks = cited_blocks(ANS, CTX, IDS)
    ok = "문서 유형이 다양하면 적응형 선택이 정확도를 62-64%에서 72%로 올린다[문서 2]. 범용 텍스트면 문장 청킹이 가장 비용 효율적이다[문서 1]."
    assert check_conclusion(ok, blocks) == ""
    assert check_conclusion(ok.replace("62-64%에서 72%로", "약 10%p"), blocks).startswith("문서 밖 숫자")  # 계산한 값
    assert check_conclusion("72% 로 올린다 " * 5 + "[문서 1]", blocks).startswith("문서 밖 숫자")  # 다른 문서의 숫자
    assert check_conclusion("인용 없는 결론입니다. " * 5, blocks) == "인용 없음"
    assert check_conclusion("멀티모달이 낫다고 보고했다. " * 4 + "[문서 3]", blocks) == "본론 밖 문서 인용"


def test_replace_conclusion():
    assert replace_conclusion(ANS, "새 결론[2601.14123v1].").endswith("<b>결론</b>\n새 결론[2601.14123v1].\n")
