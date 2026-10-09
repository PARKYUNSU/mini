"""라우팅 수정 두 가지의 양쪽 방향 회귀 (docs/experiments/route_fix_1009).

(a) '논문 + 알려줘' 가 주제 질문이면 저장 논문 목록 도구로 가지 않는다 — 목록 요청은 그대로.
(b) 출력 형식 제약·조언형 일상 요청은 웹검색 사실 조회가 아니다 — 뉴스·정의 질문은 그대로.
"""

from __future__ import annotations

import pytest

from core.graph.agent_router_rules import _names_paper_topic, is_factual_lookup


@pytest.mark.parametrize("q", [
    "LLM이 생성한 코드에서 생기는 환각을 분류하고 벤치마크로 만든 논문 알려줘",
    "양방향 마스크 언어모델로 사전학습해서 언어 이해 성능을 올린 논문 알려줘",
    "점진적으로 노이즈를 넣는 과정을 거꾸로 학습해서 이미지를 생성하는 논문 알려줘",
])
def test_topic_paper_question_is_not_inventory(q):
    assert _names_paper_topic(q)


@pytest.mark.parametrize("q", [
    "최신 논문 목록 보여줘",
    "chromadb에 저장된 논문 뭐 있어?",
    "저장된 논문 알려줘",
    "최근 논문 알려줘",
])
def test_inventory_request_stays_inventory(q):
    assert not _names_paper_topic(q)


@pytest.mark.parametrize("q", [
    "할 일 우선순위를 매기는 방법을 4줄로만 설명해줘.",
    "장마철에 빨래 말리는 요령을 알려줘. '입니다' 라는 말은 빼고.",
    "손님 오기 전 치울 곳 3줄만 알려줘.",
    "왜 쉬어야 하는지 설명해줘. '세요' 로 끝나는 말은 금지야.",
    "사진 용량이 커서 크기를 줄이려는데, 단계당 48자 제한을 지켜서 알려줘.",
    "녹음한 회의를 글로 옮기려 한다. '실행하' 는 쓰지 말고 절차를 알려줘.",
])
def test_daily_or_constrained_request_is_not_web_lookup(q):
    assert not is_factual_lookup(q)


@pytest.mark.parametrize("q", [
    "오늘 IT 뉴스 알려줘",
    "비트코인이 뭐야?",
    "엔비디아 블랙웰 알아?",
    "양자컴퓨터 설명해줘",
])
def test_fact_lookup_still_web(q):
    assert is_factual_lookup(q)
