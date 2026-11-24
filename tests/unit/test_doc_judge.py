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


def test_promote_external(monkeypatch):
    import core.llm.doc_judge as dj
    import core.rag.external_search as es
    ab = "x" * 250
    monkeypatch.setattr(es, "search_openalex", lambda *a, **k: [
        {"arxiv": "2311.11123", "title": "Regression Testing", "abstract": ab},
        {"arxiv": None, "title": "ACL only", "abstract": ab},
        {"arxiv": "2401.00002", "title": "Unrelated", "abstract": ab}])
    monkeypatch.setattr(dj, "judge_docs", lambda q, ctx: {3: "P", 4: "N"})
    ctx, ids, labs, added = dj.promote_external("q", "q", "[문서 1]\n[2401.00001] A\n[초록] a\n\n---\n\n[문서 2]\n[2401.00003] B\n[초록] b",
                                                {1: "2401.00001", 2: "2401.00003"}, {1: "N", 2: "N"})
    assert [a["arxiv"] for a in added] == ["2311.11123"] and ids[3] == "2311.11123" and labs[3] == "P"
    assert "[문서 3]\n[2311.11123] Regression Testing" in ctx and "2401.00002" not in ctx
    from core.llm.body_numbers import _blocks
    assert "Regression Testing" in _blocks(ctx, ids)["2311.11123"] and "Regression" not in _blocks(ctx, ids)["2401.00003"]


def test_promote_external_uses_prefetched_items(monkeypatch):
    import core.llm.doc_judge as dj
    import core.rag.external_search as es
    monkeypatch.setattr(es, "search_openalex", lambda *a, **k: (_ for _ in ()).throw(AssertionError("검색 다시 함")))
    monkeypatch.setattr(dj, "judge_docs", lambda q, ctx: {2: "D"})
    items = [{"arxiv": "2403.18802", "title": "Long-form factuality", "abstract": "y" * 250}]
    ctx, ids, labs, added = dj.promote_external("q", "q", "[문서 1]\n[2401.00001] A\n[초록] a", {1: "2401.00001"}, {1: "D"}, items=items)
    assert added[0]["arxiv"] == "2403.18802" and labs[2] == "D"


def test_judge_external_list_drops_unrelated_keeps_unjudgeable(monkeypatch):
    import core.llm.doc_judge as dj
    monkeypatch.setattr(dj, "judge_docs", lambda q, ctx: {1: "N", 2: "P"})
    items = [{"arxiv": "2302.06527", "title": "Unit tests", "abstract": "u" * 250},
             {"arxiv": None, "title": "DOI only", "abstract": ""},
             {"arxiv": "2105.09680", "title": "KLUE", "abstract": "k" * 250}]
    kept, n = dj.judge_external_list("q", items)
    assert n == 1 and [it["title"] for it in kept] == ["DOI only", "KLUE"]
    monkeypatch.setattr(dj, "judge_docs", lambda q, ctx: None)
    assert dj.judge_external_list("q", items) == (items, 0)
