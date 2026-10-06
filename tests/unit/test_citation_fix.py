"""RAG 답변의 arXiv ID 인용 교정 (`core.llm.citation_fix`).

왜 있나 (docs/experiments/protocol.md §5.4): 모델이 ID 를 옮겨 적다가 자릿수를
흘린다 — 인용 ID 중 20~36% 가 코퍼스에 없고 전부 실제 ID 의 변형이다. 사용자가
그 ID 로 논문을 찾으면 없으므로 출처로 쓸 수 없다.

이 테스트가 지키는 것은 **"애매하면 고치지 않는다"** 는 쪽이다. 잘못 고친 인용은
틀린 출처를 그럴듯하게 만들어 더 나쁘다.
"""

from __future__ import annotations

import pytest

from core.llm.citation_fix import extract_context_ids, fix_citations

CTX = (
    "[Distance: 0.4997]\n[발행일: 2024-08-15]\n"
    "[2408.08067v2] RAGChecker: A Fine-grained Framework\n본문...\n\n---\n\n"
    "[Distance: 0.4433]\n[발행일: 2024-07-26]\n"
    "[2407.21059v1] Modular RAG: LEGO-like Frameworks\n본문...\n"
)


def test_extracts_ids_in_order_without_metadata_noise() -> None:
    """`[Distance: …]`·`[발행일: …]` 같은 대괄호는 ID 가 아니다."""
    assert extract_context_ids(CTX) == ["2408.08067v2", "2407.21059v1"]


def test_extracts_paper_id_form() -> None:
    """다른 컨텍스트 빌더는 `paper_id=…` 형태를 쓴다 (agent_chroma_rag.py:1852)."""
    assert extract_context_ids("### [1] paper_id=2406.18975v1\n제목") == ["2406.18975v1"]


def test_exact_citation_is_left_alone() -> None:
    out, st = fix_citations("근거다 [2408.08067v2].", CTX)
    assert out == "근거다 [2408.08067v2]."
    assert (st["kept"], st["fixed"], st["dropped"]) == (1, 0, 0)


@pytest.mark.parametrize(
    "cited",
    [
        "2408.0806v2",    # 자릿수 하나 빠짐 — 실측된 실패 모양
        "2408.08167v2",   # 한 자리 치환
        "2408.080617v2",  # 자릿수 하나 더 들어감
        "2408.08067v1",   # 판만 다름
        "2408.08067",     # 판 없음
    ],
)
def test_single_edit_is_corrected(cited: str) -> None:
    out, st = fix_citations(f"근거다 [{cited}].", CTX)
    assert out == "근거다 [2408.08067v2].", out
    assert st["fixed"] == 1


def test_unmatchable_citation_is_removed_with_cleanup() -> None:
    """후보가 없으면 지운다 — 틀린 출처를 남기는 것보다 없는 편이 낫다."""
    out, st = fix_citations("근거다 [2409.99999v1].", CTX)
    assert out == "근거다."
    assert st["dropped"] == 1 and st["unknown_ids"] == ["2409.99999v1"]


def test_ambiguous_citation_is_removed_not_guessed() -> None:
    """두 후보가 똑같이 한 글자 차이면 **고치지 않고 지운다.**"""
    ctx = "[2408.08067v2] 논문A\n[2408.08167v2] 논문B\n"
    # 2408.0806 7 ↔ 2408.0816 7 : 둘 다 2408.08?67 에서 한 글자 차이
    out, st = fix_citations("근거다 [2408.08?67v2].".replace("?", "9"), ctx)
    assert "[2408.08067v2]" not in out and "[2408.08167v2]" not in out
    assert st["fixed"] == 0 and st["dropped"] == 1


def test_no_context_ids_leaves_answer_untouched() -> None:
    """컨텍스트에 ID 가 없으면 판단 근거가 없다 — 인용을 전부 지워 버리면 안 된다."""
    ans = "근거다 [2408.08067v2] 그리고 [1234.5678v1]."
    for ctx in ("", "관련 문서 없음", "(RAG 검색 실패: timeout)"):
        out, st = fix_citations(ans, ctx)
        assert out == ans, ctx
        assert st.get("skipped_no_context_ids") is True
        assert st["dropped"] == 0


def test_mixed_answer() -> None:
    out, st = fix_citations(
        "첫째 [2408.08067v2] 둘째 [2407.2105v1] 셋째 [2409.00000v9] 이다.", CTX
    )
    assert "[2408.08067v2]" in out and "[2407.21059v1]" in out
    assert "2409.00000" not in out
    assert (st["kept"], st["fixed"], st["dropped"]) == (1, 1, 1)


def test_order_number_citations_are_untouched() -> None:
    """`[1]` 같은 순서 번호는 arXiv ID 가 아니므로 건드리지 않는다."""
    ans = "첫째 [1] 둘째 [2] 이다."
    out, st = fix_citations(ans, CTX)
    assert out == ans
    assert (st["kept"], st["fixed"], st["dropped"]) == (0, 0, 0)


def test_is_idempotent() -> None:
    """한 번 고친 답변을 다시 넣어도 더 바뀌지 않는다."""
    once, _ = fix_citations("근거다 [2408.0806v2] 또 [2409.99999v1].", CTX)
    twice, st = fix_citations(once, CTX)
    assert twice == once
    assert st["dropped"] == 0


# ── 번호 인용 (`[문서 N]`) ──────────────────────────────────────────────────
from core.llm.citation_fix import RAG_HIT_SEP, number_context_papers  # noqa: E402

CTX2 = (
    "[Distance: 0.5]\n[2408.08067v2] 논문 A\n본문 A"
    + RAG_HIT_SEP
    + "[Distance: 0.4]\n[2407.21059v1] 논문 B\n본문 B"
)


def test_numbering_labels_each_block_and_maps_ids() -> None:
    nc, mp = number_context_papers(CTX2)
    assert mp == {1: "2408.08067v2", 2: "2407.21059v1"}
    assert nc.startswith("[문서 1]\n")
    assert "[문서 2]\n" in nc
    # 본문은 보존된다
    assert "본문 A" in nc and "본문 B" in nc


def test_numbering_is_contiguous_after_filtering() -> None:
    """핵심 설계 요건 — 블록이 걸러진 뒤 번호를 매기면 구멍이 없다.

    agent_nodes 는 rag.search() 뒤에 _rag_context_top_n_hits 등으로 블록을
    걸러낸다. 조립 시점에 번호를 매겼다면 [1],[3] 처럼 비었을 것이다.
    """
    filtered = RAG_HIT_SEP.join(
        [b for i, b in enumerate(CTX2.split(RAG_HIT_SEP)) if i != 0]
    )
    nc, mp = number_context_papers(filtered)
    assert list(mp) == [1], mp          # 1번부터 연속
    assert mp[1] == "2407.21059v1"      # 남은 블록이 1번이 된다
    assert "[문서 2]" not in nc


def test_numbering_skips_blocks_without_id() -> None:
    """ID 가 없는 블록도 번호는 받지만 매핑에는 없다 — 인용되면 지워진다."""
    ctx = "[Distance: 0.5]\nID 없는 블록" + RAG_HIT_SEP + "[2407.21059v1] 논문 B"
    nc, mp = number_context_papers(ctx)
    assert "[문서 1]" in nc and "[문서 2]" in nc
    assert mp == {2: "2407.21059v1"}
    out, st = fix_citations("근거 [문서 1] 과 [문서 2].", nc, doc_ids=mp)
    assert "[2407.21059v1]" in out
    assert st["expanded"] == 1 and st["bad_refs"] == [1]


def test_numbering_noop_on_empty_context() -> None:
    for ctx in ("", "   ", "관련 문서 없음"):
        nc, mp = number_context_papers(ctx)
        assert nc == ctx and mp == {}


def test_doc_refs_expand_to_ids() -> None:
    nc, mp = number_context_papers(CTX2)
    out, st = fix_citations("첫째 [문서 1] 둘째 [문서 2] 이다.", nc, doc_ids=mp)
    assert out == "첫째 [2408.08067v2] 둘째 [2407.21059v1] 이다."
    assert st["expanded"] == 2


def test_out_of_range_doc_ref_is_dropped() -> None:
    """문서가 2편인데 [문서 7] 이면 가리킬 대상이 없다 — 지운다."""
    nc, mp = number_context_papers(CTX2)
    out, st = fix_citations("근거다 [문서 7].", nc, doc_ids=mp)
    assert "문서 7" not in out and "[" not in out
    assert st["bad_refs"] == [7] and st["expanded"] == 0


def test_raw_ids_still_fixed_when_numbering_used() -> None:
    """번호 인용으로 바꿔도 모델이 ID 를 쓸 수 있다 — 그 경로도 살아 있어야 한다."""
    nc, mp = number_context_papers(CTX2)
    out, st = fix_citations("A [문서 1] B [2407.2105v1] C [9999.99999v9].", nc, doc_ids=mp)
    assert "[2408.08067v2]" in out        # 번호 → ID
    assert "[2407.21059v1]" in out        # 한 글자 오류 → 교정
    assert "9999.99999" not in out        # 후보 없음 → 삭제
    assert (st["expanded"], st["fixed"], st["dropped"]) == (1, 1, 1)


def test_doc_ref_expansion_is_idempotent() -> None:
    nc, mp = number_context_papers(CTX2)
    once, _ = fix_citations("근거 [문서 1].", nc, doc_ids=mp)
    twice, st = fix_citations(once, nc, doc_ids=mp)
    assert twice == once and st["expanded"] == 0
