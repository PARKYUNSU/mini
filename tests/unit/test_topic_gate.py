"""학술 주제 게이트가 사전 등록 판정을 계속 지키는지 (docs/experiments/topic_gate_1009).

test 분할: TPR ≥ 0.90, chat+planner 오탐 ≤ 3/61. 단어 목록을 바꾸면 이 테스트가 그
판정을 다시 잰다 — dev 만 보고 고치고, 여기서 깨지면 목록 변경을 되돌린다.
"""

from __future__ import annotations

import json
from pathlib import Path

from core.rag.topic_gate import is_academic_query

ITEMS = Path(__file__).resolve().parents[2] / "docs" / "experiments" / "topic_gate_1009" / "items.jsonl"


def _rows(split: str) -> list[dict]:
    rows = [json.loads(l) for l in ITEMS.read_text(encoding="utf-8").splitlines() if l.strip()]
    return [r for r in rows if r["split"] == split]


def test_test_split_meets_preregistered_thresholds():
    rows = _rows("test")
    pos = [r for r in rows if r["label"] == 1]
    neg = [r for r in rows if r["source"] in ("fixture_chat", "fixture_planner")]
    tpr = sum(is_academic_query(r["text"]) for r in pos) / len(pos)
    fp = sum(is_academic_query(r["text"]) for r in neg)
    assert tpr >= 0.90, tpr
    assert fp <= 3, fp


def test_rag_allowed_without_paper_word_for_academic_question():
    from core.session.agent_session import is_rag_allowed

    q = "토큰마다 8개 전문가 중 2개로 보내는 희소 MoE 언어모델 설명해줘"
    assert "논문" not in q
    assert is_rag_allowed("gate_unit_test_chat", q)


def test_daily_request_still_not_rag():
    from core.session.agent_session import is_rag_allowed

    assert not is_rag_allowed("gate_unit_test_chat", "장마철에 빨래 말리는 요령을 알려줘. '입니다' 라는 말은 빼고.")


def test_names_in_db_opens_rag(monkeypatch):
    # answer_issues_1113 B22: 분야 용어 없이 DB 논문 이름만 있는 질문이 일반 대화로 갔다
    import core.rag.bm25_index as B
    import core.rag.topic_gate as G

    class _BM:
        def named_paper(self, n):
            return {"DynaFlow": "2610.34467", "OmniNova": "2503.20028"}.get(n)

    monkeypatch.setattr(B, "get_bm25_searcher", lambda: _BM())
    monkeypatch.setattr(G, "is_academic_query_llm", lambda t: False)
    monkeypatch.setenv("RAG_NAME_LOOKUP", "1")
    q = "DynaFlow랑 OmniNova 성능 수치 비교해줘"
    assert G.names_in_db(q) == ["DynaFlow", "OmniNova"] and G.is_academic_query_full(q)
    assert G.names_in_db("iPhone 배터리 오래 쓰는 법") == [] and not G.is_academic_query_full("iPhone 배터리 오래 쓰는 법")
    monkeypatch.setenv("RAG_NAME_LOOKUP", "0")
    assert G.names_in_db(q) == []


def test_router_reverts_planner_for_db_names(monkeypatch):
    # cross_metric_1113: 이름만 있는 비교 질문을 3단계 LLM 이 계획(C)으로 보냈고 되돌림이 어휘만 봐 못 막았다
    import core.rag.bm25_index as B
    from core.graph.agent_nodes import _revert_academic_misroute

    class _BM:
        def named_paper(self, n):
            return {"QJL": "2406.03482", "CommVQ": "2506.18879"}.get(n)

    import core.rag.topic_gate as G

    monkeypatch.setattr(B, "get_bm25_searcher", lambda: _BM())
    monkeypatch.setattr(G, "is_academic_query_llm", lambda t: False)  # 이름 규칙만 본다
    monkeypatch.setenv("RAG_NAME_LOOKUP", "1")
    planner = {"route_type": "planner", "router_choice": "C"}
    q = "QJL이랑 CommVQ 중 어느 쪽이 메모리를 더 많이 줄여?"
    assert _revert_academic_misroute(q, q.lower(), dict(planner)) == {"route_type": "direct_answer", "router_choice": "B"}
    other = "iPhone 배터리 오래 쓰는 법"
    assert _revert_academic_misroute(other, other.lower(), dict(planner)) == planner
    code = "QJL 논문 파이썬 코드로 구현해서 실행해줘"
    assert _revert_academic_misroute(code, code.lower(), dict(planner)) == planner
    monkeypatch.setenv("RAG_NAME_LOOKUP", "0")
    assert _revert_academic_misroute(q, q.lower(), dict(planner)) == planner


def test_revert_practical_academic_planner(monkeypatch):
    # 6차 H13 · H17: 어휘 규칙에 안 걸리는 실무형 학술 질문이 계획(C)으로 샜다 → LLM 판정까지 보고 되돌림
    import core.rag.topic_gate as G
    from core.graph.agent_nodes import _revert_academic_misroute

    yes = {"문서에서 추출한 KPI 숫자가 맞는지 어떻게 검증해?", "PDF에서 표를 뽑아내는 도구나 모델 추천해줘"}
    monkeypatch.setattr(G, "is_academic_query_llm", lambda t: t in yes)
    planner = {"route_type": "planner", "router_choice": "C"}
    for q in yes:
        assert _revert_academic_misroute(q, q.lower(), dict(planner)) == {"route_type": "direct_answer", "router_choice": "B"}
    chore = "내 다운로드 폴더 PDF들 정리하는 계획 세워줘"
    assert _revert_academic_misroute(chore, chore.lower(), dict(planner)) == planner
    code = "PDF에서 표를 뽑아내는 파이썬 코드 짜서 실행해줘"
    assert _revert_academic_misroute(code, code.lower(), dict(planner)) == planner


def test_revert_academic_tool_misroute(monkeypatch):
    # W06(11-24~): 3단계가 학술 질문에 도구 이름 없는 B 를 골랐다 → RAG 로 되돌림. 하드룰 도구(이름 있음)는 그대로.
    import core.rag.topic_gate as G
    from core.graph.agent_nodes import _revert_academic_misroute

    monkeypatch.setattr(G, "is_academic_query_llm", lambda t: False)

    tool = {"route_type": "use_existing_tool", "router_choice": "B"}
    q = "서비스 LLM을 다른 모델로 바꿀 때 품질 회귀를 확인하는 방법 연구 있어?"
    assert _revert_academic_misroute(q, q.lower(), dict(tool)) == {"route_type": "direct_answer", "router_choice": "B"}
    named = {**tool, "used_tool_name": "tavily_search_tool"}
    assert _revert_academic_misroute(q, q.lower(), dict(named)) == named
    other = "서울 지금 날씨 알려줘"
    assert _revert_academic_misroute(other, other.lower(), dict(tool)) == tool
    run = "아까 만든 arXiv 도구 실행해줘"  # 실사용 질문: 학술 어휘지만 도구 호출
    assert _revert_academic_misroute(run, run.lower(), dict(tool)) == tool


def test_comparison_targets_local_only(monkeypatch):
    # cmp_targets_1114: 로컬이 "A: … B: …" 를 한 줄에 써도 읽고, 실패해도 Gemini 로 안 넘어간다
    from core.graph import agent_nodes as N

    seen = {}

    class _LLM:
        def __init__(self, out):
            self.out = out

        def invoke(self, msgs):
            return type("R", (), {"content": self.out})()

    def _getter(out):
        def g(**kw):
            seen.update(kw)
            return _LLM(out)
        return g

    monkeypatch.setattr(N, "get_executor_llm", lambda: (_ for _ in ()).throw(AssertionError("Gemini 호출")))
    monkeypatch.setattr(N, "get_rag_query_rewrite_llm", _getter("A: DPO offline preference learning B: PPO online RL"))
    assert N._extract_comparison_targets("DPO랑 PPO 비교해줘") == ["DPO offline preference learning", "PPO online RL"]
    assert seen.get("repeat_penalty") == 1.0
    monkeypatch.setattr(N, "get_rag_query_rewrite_llm", _getter("A: 로짓 증류\nB: 특징 증류"))
    assert N._extract_comparison_targets("로짓 증류랑 특징 증류 비교") == []
