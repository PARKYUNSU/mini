"""RAG 답변 서론의 모순된 '문서에 없다' 제거 (`core.llm.answer_fix`).

왜 있나 (docs/experiments/yunsur_v12/README.md §4.5): v12 가 정답을 받고도 31% 에서
서론에 "문서에 없다"고 쓴 뒤 결론에서는 찾았다고 한다. 결론도 없다고 하면 건드리지 않는다.
"""

from __future__ import annotations

from core.llm.answer_fix import drop_contradicted_no_doc

MD = (
    "### 서론\n"
    "제공된 문서에는 질문에서 찾는 연구가 없습니다. 깃허브 이슈의 이미지는 중요합니다.\n\n"
    "### 본론\n"
    "1. **CodeV**: 시각 데이터를 활용한다 [2412.17315v1].\n\n"
    "### 결론\n"
    "CodeV 가 질문에서 찾는 연구입니다.\n"
)


def test_drops_contradicted_intro_sentence():
    out, dropped = drop_contradicted_no_doc(MD)
    assert dropped
    assert "없습니다" not in out
    assert "### 서론\n깃허브 이슈의 이미지는 중요합니다." in out
    assert out.endswith("CodeV 가 질문에서 찾는 연구입니다.\n")


def test_keeps_when_conclusion_also_negative():
    md = MD.replace("CodeV 가 질문에서 찾는 연구입니다.", "질문에서 찾는 구체적인 연구는 제공되지 않았습니다.")
    out, dropped = drop_contradicted_no_doc(md)
    assert not dropped and out == md


def test_html_sections():
    html = MD.replace("### 서론", "<b>서론</b>").replace("### 본론", "<b>본론</b>").replace("### 결론", "<b>결론</b>")
    out, dropped = drop_contradicted_no_doc(html)
    assert dropped and "없습니다" not in out.split("<b>본론</b>")[0]


def test_no_denial_untouched():
    md = MD.replace("제공된 문서에는 질문에서 찾는 연구가 없습니다. ", "")
    assert drop_contradicted_no_doc(md) == (md, False)


def test_denial_outside_intro_untouched():
    md = MD.replace("CodeV 가 질문에서 찾는 연구입니다.", "CodeV 입니다.").replace(
        "1. **CodeV**: 시각 데이터를 활용한다", "1. **CodeV**: 제공된 문서에는 수치가 없습니다. 시각 데이터를 활용한다"
    ).replace("제공된 문서에는 질문에서 찾는 연구가 없습니다. ", "")
    assert drop_contradicted_no_doc(md) == (md, False)


def test_missing_sections_untouched():
    text = "제공된 문서에는 질문에서 찾는 연구가 없습니다."
    assert drop_contradicted_no_doc(text) == (text, False)
