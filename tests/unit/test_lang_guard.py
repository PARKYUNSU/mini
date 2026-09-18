"""core.llm.lang_guard — 로컬 실패율 평가 v2에서 나온 실제 '영어로 새는' 출력 기준."""

import pytest

from core.llm.lang_guard import english_ratio, needs_korean_retry, strip_english_meta_sections

pytestmark = pytest.mark.unit


def test_korean_answer_low_ratio():
    assert english_ratio("안녕하세요, 윤수르입니다. 무엇을 도와드릴까요?") == 0.0


def test_english_answer_high_ratio():
    # chat_05 t2 실제 출력 형태
    t = "### 📌 **Slack Message Draft**\n\nHi team, I've attached the latest paper on Agentic Systems."
    assert english_ratio(t) > 0.9
    assert needs_korean_retry(t)


def test_rag_titles_excluded():
    # RAG 답변: 영문 논문 제목은 볼드/📄 줄이라 제외되어야 함 (v2에서 오탐 22/24 났던 케이스)
    t = (
        "### ✅ 선별 논문\n1. 📄 **RAGChecker: A Fine-grained Framework for Diagnosing RAG**\n"
        "• 📅 발행일: 2024\n• 핵심: 검색 증강 생성의 진단 프레임워크를 제안한다.\n"
        "### 요약\n이 논문은 모듈별 지표를 정의하여 환각 원인을 분리한다."
    )
    assert english_ratio(t) < 0.2
    assert not needs_korean_retry(t)


def test_code_and_urls_excluded():
    t = "다음 URL을 씁니다: https://example.com/docs 그리고 `requests.get()` 을 호출합니다.\n```python\nimport os\n```"
    assert english_ratio(t) < 0.2


def test_strip_reasoning_section_before_plan():
    # planner_03 t2 (parse_fail) 형태: 영어 추론 섹션 뒤에 실제 계획
    t = (
        "### 🧠 Reasoning Process\n\n**Step 0: Strategy Selection**\nThe user wants a plan to extract titles.\n\n"
        "1단계: requests로 HTML 가져오기\n2단계: 제목 추출\n실행할까요? (승인/거절)"
    )
    out = strip_english_meta_sections(t)
    assert out.startswith("1단계:")
    assert "Reasoning" not in out


def test_strip_self_reflection_and_keep_short_response():
    # chat_08 t2 형태: [Short Response] 본문은 살리고 [Full Output ...]은 버림
    t = (
        "### [Short Response]\n감사합니다. 도움이 되어 기쁩니다.\n\n---\n"
        "### [Full Output (for reference)]\nThis is the full internal draft with role adherence notes."
    )
    out = strip_english_meta_sections(t)
    assert "감사합니다" in out
    assert "Full Output" not in out and "role adherence" not in out.lower()


def test_strip_keeps_normal_korean_headers():
    t = "### 회의록 요약\n**제목:** 원전 수출\n\n### 결론\n경쟁력 있음."
    assert strip_english_meta_sections(t) == t


def test_strip_returns_original_if_everything_removed():
    t = "### [Self-Reflection]\n1. Role Adherence: ok"
    assert strip_english_meta_sections(t) == t
