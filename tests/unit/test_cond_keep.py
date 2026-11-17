from core.llm.cond_keep import add_missing_to_intro, keep_terms_note, missing_conditions, missing_sentence


def test_missing_sentence_and_intro():
    conds = [{"종류": "언어", "값": "한국어", "다룬 논문": []}, {"종류": "문서 유형", "값": "장문 보고서", "다룬 논문": [5]},
             {"종류": "비교 대상", "값": "BM25 · 밀집 검색", "다룬 논문": []}]
    s = missing_sentence(missing_conditions(conds))
    assert s.startswith("'한국어' 조건을 직접 다룬 연구 · 'BM25 · 밀집 검색' 비교를 직접 다룬 연구는")
    out, n = add_missing_to_intro("서론\n원래 서론.\n\n본론\n1. x", s)
    assert n == 1 and out.startswith("서론\n'한국어' 조건") and "\n원래 서론." in out
    assert add_missing_to_intro("서론\n a", "") == ("서론\n a", 0)


def test_keep_terms_note():
    assert "'기준 문서'" in keep_terms_note([{"종류": "문서 유형", "값": "기준 문서", "다룬 논문": []}])
    assert keep_terms_note([{"종류": "언어", "값": "한국어", "다룬 논문": []}]) == ""
