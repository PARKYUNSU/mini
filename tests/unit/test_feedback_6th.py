"""6차 피드백 버그 수정 (P4): W10 '또한' 조각 · W03 무관 판정 논문 인용 · 용어 사전."""

from core.llm.body_numbers import check_body_numbers
from core.llm.format_fix import fix_terms
from core.llm.slot_fill import drop_n_cited


def test_number_drop_keeps_name_and_strips_connective():
    ctx = "[문서 1]\n[2406.12624] Judging the Judges\n[초록] Scott pi distinguishes judges better than percent agreement."
    ans = ("### 본론\n2. **Judging the Judges**: 13개 모델을 비교했습니다. 또한 단순 퍼센트 일치율보다 Scott’s π가 판정자를 "
           "더 잘 구분한다는 점을 제시했습니다. [2406.12624]\n### 결론\n끝.")
    out, n = check_body_numbers(ans, ctx, {1: "2406.12624"})
    assert n == 1 and "2. **Judging the Judges**: 단순 퍼센트" in out and "또한" not in out


def test_drop_items_and_sentences_citing_only_n():
    a = ("### 서론\nx\n### 본론\n1. **A** (관련 연구): a [2501.00001]\n2. **B** (관련 연구): b [2506.00281v1]\n"
         "3. **C**: c [2501.00001][2506.00281]\n\n### 결론\n가는 맞다[2501.00001]. 나는 틀렸다[2506.00281v1]. 끝.")
    out, n = drop_n_cited(a, {1: "P", 2: "N"}, {1: "2501.00001", 2: "2506.00281v1"})
    assert n == 2 and "**B**" not in out and "나는 틀렸다" not in out and "**C**" in out and "가는 맞다" in out
    assert drop_n_cited(a, {1: "P", 2: "D"}, {1: "2501.00001", 2: "2506.00281v1"}) == (a, 0)


def test_term_dictionary():
    assert fix_terms("인간 라이터 간의 회고율")[0] == "인간 평가자 간의 재현율"
    assert fix_terms("메타클래서퍼가 집계")[0] == "메타 분류기가 집계"
    assert fix_terms("crowdsourced 데이터와 rater를 recall이")[0] == "크라우드소싱 데이터와 평가자를 재현율이"
    assert fix_terms("Crowdsourced Labels · Recall@k · 프라이터")[1] == 0


def test_reaction_maps_to_job(monkeypatch, tmp_path):
    from types import SimpleNamespace as NS

    from apps.telegram_bot import answer_feedback as A

    monkeypatch.setenv("BOT_FEEDBACK_LOG", str(tmp_path / "fb.jsonl"))
    A.remember("7", 101, 55)
    A.remember("7", 102, 56)
    assert A.job_for_message("7", 102) == 56 and A.job_for_message("8", 102) is None
    assert A.rating_from_reaction([NS(emoji="🔥"), NS(emoji="👎")]) == "down"
    assert A.rating_from_reaction([]) is None
    row = A.record({"user_text": "q", "result_text": "a [2501.00001]"}, 56, "up", "7", source="reaction")
    assert row["source"] == "reaction" and row["answer_papers"] == ["2501.00001"]


def test_progress_file(monkeypatch, tmp_path):
    from core.bridge import progress as P

    monkeypatch.setattr(P, "_path", lambda j: tmp_path / f"{j}.txt")
    monkeypatch.setenv("BOT_PROGRESS", "0")
    P.write(3, "query")
    assert P.read(3) is None
    monkeypatch.setenv("BOT_PROGRESS", "1")
    P.write(3, "query")
    P.write(3, "select")  # 문구 없는 단계는 그대로 둔다
    assert P.read(3) == "🔎 논문 검색 중…"
    P.clear(3)
    assert P.read(3) is None


def test_recommend_mode(monkeypatch):
    from core.llm.doc_judge import agg_slots_template, is_recommend
    from core.rag.external_search import rec_query

    q = "ESG 도메인에 특화된 언어모델 추천해줘"
    monkeypatch.setenv("RAG_REC_MODE", "0")
    assert not is_recommend(q)
    monkeypatch.setenv("RAG_REC_MODE", "1")
    assert is_recommend(q) and not is_recommend("추천 시스템 콜드 스타트 연구 있어?")
    assert "후보 이름" in agg_slots_template({1: "D"}, "a", rec=True) and "후보 이름" not in agg_slots_template({1: "D"}, "a")
    assert rec_query("esg domain language model recommendation selection criteria on") == "esg domain language model"


def test_digest_buttons_roundtrip(tmp_path, monkeypatch):
    from apps.telegram_bot import answer_feedback as af

    kb = af.digest_markup("20261130", 1, 3, {2: "down"})
    assert len(kb.keyboard) == 3
    data = kb.keyboard[0][0].callback_data
    assert af.parse_digest(data) == ("20261130", 1, 1, "up")
    assert af.parse(data) is None  # 답 버튼 처리기와 안 겹친다
    assert af.parse_digest("fb:3:up") is None and af.parse_digest("dg:2026113:1:1:up") is None
    assert af.chosen_from_markup(kb) == {2: "down"}
    monkeypatch.setenv("BOT_FEEDBACK_LOG", str(tmp_path / "fb.jsonl"))
    row = af.record_digest("19990101", 0, 1, "up", "1")  # 기록 파일이 없어도 남긴다
    assert row["rating"] == "up" and (tmp_path / "digest_feedback.jsonl").exists()


def test_rec_pool_order(monkeypatch):
    from core.llm import doc_judge as J

    monkeypatch.setattr(J, "judge_docs", lambda q, ctx: {1: "N", 2: "P", 3: "D", 4: "D"})
    assert J.judge_pool_order("q", ["a", "b", "c", "d", "e"], "x") == ["c", "d", "b", "e", "a"]  # 판정 없는 5번은 P
    monkeypatch.setattr(J, "judge_docs", lambda q, ctx: None)
    assert J.judge_pool_order("q", ["a"], "x") is None
    assert J.is_rec_or_method("RAG 시스템 평가 프레임워크 추천해줘") and J.is_rec_or_method("어떤 지표로 평가해?")
    assert not J.is_rec_or_method("BM25 와 dense 중 뭐가 나아?")


def test_combine_struct():
    from core.llm.doc_judge import combine_struct

    task = {1: "맞음", 2: "맞음", 3: "인접", 4: "아님"}
    assert combine_struct(task, [{"값": "한국어", "다룬 논문": [1]}]) == {1: "D", 2: "P", 3: "P", 4: "N"}
    assert combine_struct(task, []) == {1: "D", 2: "D", 3: "P", 4: "N"}  # 조건 없으면 맞음 = 직접


def test_digest_terms_7th():
    from core.llm.format_fix import fix_terms

    s = "30,000개의 인스턴트로 구성. 원샷 프롬팅과 차킹. 일부 규격에서는 허풍(~puffery)과 허풍."
    out = fix_terms(s)[0]
    assert out == "30,000개의 인스턴스로 구성. 원샷 프롬프팅과 청킹. 일부 모형 설정에서는 과장 표현(puffery)과 과장 표현."
    assert fix_terms("국제 규격을 따른다")[0] == "국제 규격을 따른다"
    assert fix_terms("두 동료 평가자(rater)가 판정")[0] == "두 동료 평가자가 판정"
