"""format_fix_1117: 용어 규칙 · 섞인 글자 거르기 · 한자 지우기 · '없음' 문장."""
from core.llm import format_fix as F
from core.llm import item_rewrite


def test_term_rule_off_on(monkeypatch):
    monkeypatch.delenv("RAG_FORMAT_FIX", raising=False)
    assert F.term_rule() == ""
    monkeypatch.setenv("RAG_FORMAT_FIX", "1")
    assert "poisoning" in F.term_rule()


def test_glued_latin():
    assert F._GLUED.search("데이터 포izoning 공격")
    assert not F._GLUED.search("LLM을 쓰는 RAG에서 poisoning 공격")


def test_check_item_rejects_glued(monkeypatch):
    monkeypatch.setenv("RAG_FORMAT_FIX", "1")
    src = "RAG poisoning attacks are analyzed."
    text = "이 연구는 RAG 시스템의 데이터 포izoning 공격을 분석하고 입력 검증 같은 완화 조치를 제시합니다. 실험은 여러 시스템에서 진행되었습니다."
    assert item_rewrite.check_item(text, "짧음", src) == "섞인 글자"


def test_strip_hanzi():
    out, n = F.strip_hanzi("세 가지 척도에서六点 벤치마크에 대해")
    assert n == 1 and "六" not in out and "척도에서" in out


def test_partial_wording():
    a = "서론\n제공된 문서에는 질문이 찾는 연구가 없습니다. 배경.\n본론\n1. <b>X</b> (관련 연구): 내용 [2401.00001v1]\n결론\n따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다."
    out, n = F.partial_wording(a)
    assert n == 2 and F.LEAD_NEW in out and F.CONCL_NEW in out
    assert F.partial_wording(a.replace("(관련 연구)", "")) == (a.replace("(관련 연구)", ""), 0)
