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
