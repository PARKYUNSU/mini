from core.llm.doc_judge import aggregate, doc_blocks

CTX = """[문서 1]
[Distance: 0.3]
[발행일: 2024-01-01]
[2401.00001v1] Paper One
[초록] First   abstract.

[문서 2]
[Distance: 0.4]
[2402.00002] Paper Two
body without abstract tag"""


def test_doc_blocks():
    b = doc_blocks(CTX)
    assert [n for n, _ in b] == [1, 2]
    assert b[0][1] == "Paper One\nFirst abstract."
    assert b[1][1].startswith("Paper Two\n")


def test_aggregate():
    assert aggregate({1: "P", 2: "D", 3: "D"}) == ("a", 2)
    assert aggregate({1: "P", 2: "N"}) == ("b", "없음")
    assert aggregate({1: "N", 2: "N"}) == ("c", "없음")


def test_agg_slots_template():
    from core.llm.doc_judge import agg_slots_template
    t = agg_slots_template({1: "D", 2: "N", 3: "P", 4: "D"}, "a")
    assert "[문서 1]" in t and "[문서 2]" not in t and "[문서 3]" in t and "[문서 4]" in t
    assert t.count("(관련 연구)") == 2  # 칸 하나 + 규칙 한 줄
    b = agg_slots_template({1: "P", 2: "N"}, "b")
    assert "질문이 찾는 연구가 없습니다" in b and "[문서 1]" in b
    c = agg_slots_template({1: "N"}, "c")
    assert "[문서 1]" not in c and "관련된 문서가 없습니다" in c


def test_strip_no_doc_ids():
    from core.llm.doc_judge import strip_no_doc_ids
    a = "본론\n질문과 관련된 문서가 없습니다. [2506.07315v2]\n\n결론\n따라서 ... [<a href=\"x\">2506.07315</a>]"
    out, n = strip_no_doc_ids(a)
    assert n == 1 and "없습니다.\n" in out and "결론\n따라서 ... [<a" in out
    assert strip_no_doc_ids("질문과 관련된 문서가 없습니다.")[1] == 0
