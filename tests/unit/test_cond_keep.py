from core.llm.cond_keep import add_missing_to_intro, keep_terms_note, missing_conditions, missing_sentence


def test_missing_sentence_and_intro():
    conds = [{"종류": "언어", "값": "한국어", "다룬 논문": []}, {"종류": "문서 유형", "값": "장문 보고서", "다룬 논문": [5]},
             {"종류": "비교 대상", "값": "BM25 · 밀집 검색", "다룬 논문": []}]
    s = missing_sentence(missing_conditions(conds))
    assert s.startswith("'한국어' 조건을 직접 다룬 연구 · 'BM25 · 밀집 검색' 비교를 직접 다룬 연구는")
    out, n = add_missing_to_intro("서론\n원래 서론.\n\n본론\n1. x", s)
    assert n == 1 and out.startswith("서론\n'한국어' 조건") and "\n원래 서론." in out
    one = missing_sentence([{"종류": "언어", "값": "한국어", "다룬 논문": []}])
    out, _ = add_missing_to_intro("서론\n질문을 직접 다룬 연구는 찾지 못했고, 가장 가까운 연구는 아래와 같습니다.\n본론", one)
    assert out == "서론\n'한국어' 조건을 직접 다룬 연구는 찾지 못했고, 가장 가까운 연구는 아래와 같습니다.\n본론"
    out, _ = add_missing_to_intro("서론\n제공된 문서에는 질문이 찾는 연구가 없습니다.\n본론", one)
    assert out == "서론\n'한국어' 조건을 직접 다룬 연구를 포함해 질문이 찾는 연구는 제공된 문서에 없습니다.\n본론"
    assert missing_conditions([{"종류": "문서 유형", "값": "보고서", "다룬 논문": []}]) == []
    assert add_missing_to_intro("서론\n a", "") == ("서론\n a", 0)


def test_keep_terms_note():
    assert "'기준 문서'" in keep_terms_note([{"종류": "문서 유형", "값": "기준 문서", "다룬 논문": []}])
    assert keep_terms_note([{"종류": "언어", "값": "한국어", "다룬 논문": []}]) == ""


def test_judge_docs_and_conditions(monkeypatch):
    import json

    import requests

    from core.llm.cond_keep import judge_docs_and_conditions

    class R:
        def json(self):
            return {"message": {"content": json.dumps({"판정": [{"번호": 1, "관련도": "직접"}, {"번호": 2, "관련도": "무관"}],
                                                       "조건": [{"종류": "언어", "값": "한국어", "다룬 논문": [2]},
                                                              {"종류": "분야", "값": "우주", "다룬 논문": []}]})}}
    monkeypatch.setattr(requests, "post", lambda *a, **k: R())
    ctx = "[문서 3]\n[2401.00001] A\n[초록] a\n\n[문서 7]\n[2401.00002] B\n[초록] b"
    labels, conds = judge_docs_and_conditions("한국어 문서 연구", ctx)
    assert labels == {3: "D", 7: "N"}
    assert conds == [{"종류": "언어", "값": "한국어", "다룬 논문": [7]}]  # '우주' 는 질문에 없어 버림, 번호는 문서 번호로
