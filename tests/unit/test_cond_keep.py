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

    import core.llm.doc_judge as dj
    from core.llm.cond_keep import judge_docs_and_conditions

    sent = []

    class R:
        def json(self):
            return {"message": {"content": json.dumps({"조건": [{"종류": "언어", "값": "한국어", "다룬 논문": [2]},
                                                                {"종류": "분야", "값": "우주", "다룬 논문": []}]})}}
    monkeypatch.setattr(requests, "post", lambda *a, **k: sent.append(k["json"]["messages"][0]["content"]) or R())
    monkeypatch.setattr(dj, "judge_docs", lambda q, ctx: {3: "D", 7: "N"})
    ctx = "[문서 3]\n[2401.00001] A\n[초록] a\n\n[문서 7]\n[2401.00002] B\n[초록] b"
    labels, conds = judge_docs_and_conditions("한국어 문서 연구", ctx)
    assert labels == {3: "D", 7: "N"}  # 문서 판정은 단독 호출 그대로
    assert conds == [{"종류": "언어", "값": "한국어", "다룬 논문": [7]}]
    blocks_docs = "[1] A\na\n\n[2] B\nb"
    assert sent[0].startswith(dj.PROMPT.format(q="한국어 문서 연구", docs=blocks_docs))  # 같은 앞부분 → 캐시


def test_restore_cond_terms():
    from core.llm.cond_keep import restore_cond_terms

    c = [{"종류": "문서 유형", "값": "기준 문서", "다룬 논문": []}, {"종류": "비교 대상", "값": "검색 방법", "다룬 논문": []}]
    a = "서론\n어려운 문제이다. 이러한 긴 법적 텍스트에서는 희석된다.\n본론\n1. X: 이러한 법률 문서를 나눈다.\n결론\n이런 방대한 법률 텍스트를 다룰 때"
    out, n = restore_cond_terms(a, c)
    assert n == 2
    assert "이러한 긴 기준 문서에서는" in out and "이런 방대한 기준 문서를" in out
    assert "1. X: 이러한 법률 문서를 나눈다." in out  # 본론 항목은 그대로
    # 질문 유형과 같은 낱말 · 조건 둘 이상 · 조건 없음은 그대로
    assert restore_cond_terms("이러한 규제 문서는", [{"종류": "문서 유형", "값": "규제 문서", "다룬 논문": []}]) == ("이러한 규제 문서는", 0)
    two = c[:1] + [{"종류": "문서 유형", "값": "회의록", "다룬 논문": []}]
    assert restore_cond_terms(a, two) == (a, 0)
    assert restore_cond_terms(a, None) == (a, 0)
    assert restore_cond_terms("이러한 긴 문서는", c) == ("이러한 긴 문서는", 0)
