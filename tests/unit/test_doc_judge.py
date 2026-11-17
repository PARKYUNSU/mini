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
