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
