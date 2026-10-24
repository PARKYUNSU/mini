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


def test_ids_to_doc_refs():
    from core.llm.conclusion_rewrite import ids_to_doc_refs

    blocks = cited_blocks(ANS, CTX, IDS)
    assert ids_to_doc_refs("적응형이 72%로 올린다[2603.25333v1]. 기타[2506.16035v2].", blocks) == \
        "적응형이 72%로 올린다[문서 2]. 기타[2506.16035v2]."  # 본론 밖 논문은 그대로 → 검사가 거른다


def test_extract_findings_v2():
    from core.llm.conclusion_rewrite import extract_findings

    blk = ("[문서 1]\n[Distance: 0.4]\n[발행일: 2026-01-20]\n[2601.14123v1] Chunking\n[초록] We study chunking in industry. "
           "Our end-to-end evaluation on Natural Questions varies chunking method. "
           "Overlap provides no measurable benefit and increases indexing cost. Sentence chunking is the most cost-effective method.")
    res, dom = extract_findings(blk)
    assert res[0].startswith("Overlap provides no measurable benefit") and "cost-effective" in res[1]
    assert dom.startswith("Our end-to-end evaluation on Natural Questions")
    assert "Distance" not in " ".join(res)


def test_brief_findings_picks_result_over_background():
    from core.llm.conclusion_rewrite import brief_findings

    ab = ("Retrieval-augmented generation is routinely extended with methods meant to improve retrieval. "
          "The benefits reported for these methods come almost exclusively from homogeneous corpora. "
          "To study this directly, we build HetDocQA, a heterogeneous benchmark with span-overlap labels. "
          "A strong cross-encoder reranker accounts for most of the pipeline's quality. "
          "Beyond it, only two methods yield reliable gains: query expansion and SSCC.")
    out = brief_findings(ab, 300)
    assert len(out) <= 300
    assert "we build HetDocQA" in out and "accounts for most" in out
    assert not out.startswith("Retrieval-augmented generation is routinely")  # 앞 배경 문장은 밀린다
    assert brief_findings("짧은 초록.", 300) == "짧은 초록."  # 고를 문장이 없으면 앞부분


def test_brief_findings_long_result_truncated_not_dropped():
    from core.llm.conclusion_rewrite import brief_findings

    ab = ("LLM agents rely on long-term memory to support extended interactions. "
          "In this paper, we propose TrustMem, a framework designed to improve the trustworthiness of memory consolidation. "
          "Extensive experiments demonstrate that TrustMem improves memory utility: " + "x " * 150 + "and reduces omission by 40.1\\%.")
    out = brief_findings(ab, 300)
    assert len(out) <= 300 and "we propose TrustMem" in out and out.endswith("…")


def test_v3_violation():
    from core.llm.conclusion_rewrite import _v3_violation

    assert _v3_violation("A 는 72% 를 얻었다[문서 1]. B 는 PDF 에서 낫다[문서 2]. 두 논문은 대상이 다르다.") == ""
    assert _v3_violation("A 와 B 는 정확도를 높였다[문서 1][문서 2].") == "여러 논문 묶음"
    assert _v3_violation("A 는 72%[문서 1]. 모든 연구가 같은 방향을 보인다.") == "과잉 일반화"
    assert _v3_violation("두 연구는 공통된 결론을 제시한다[문서 1].") == "과잉 일반화"
