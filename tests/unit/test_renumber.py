"""본론 번호 다시 매기기 (core/llm/answer_fix.py)."""

from core.llm.answer_fix import renumber_body_items

A = "### 서론\n1. 서론 문장\n\n### 본론\n1. **A**: x [문서 1]\n4. **B**: y [문서 4]\n7. **C**: z\n8. **D**: w\n\n### 결론\n1. 결론은 그대로"


def test_renumbers_body_only():
    out, ch = renumber_body_items(A)
    assert ch
    body = out.split("### 본론")[1].split("### 결론")[0]
    assert [l.split(".")[0] for l in body.strip().splitlines()] == ["1", "2", "3", "4"]
    assert "[문서 4]" in out  # 인용 번호는 건드리지 않는다
    assert out.startswith("### 서론\n1. 서론 문장") and out.endswith("1. 결론은 그대로")


def test_unchanged_when_sequential():
    s = "### 본론\n1. a\n2. b\n\n### 결론\nok"
    assert renumber_body_items(s) == (s, False)


def test_html_heads_and_no_body():
    out, ch = renumber_body_items("<b>본론</b>\n2. a\n5. b\n<b>결론</b>\nz")
    assert ch and "\n1. a\n2. b\n" in out
    assert renumber_body_items("본론 없음") == ("본론 없음", False)
