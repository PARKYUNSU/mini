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


def test_rag_multi_essay_format_not_flagged():
    """다중 문서 템플릿의 **현재** 형식(서론/본론/결론)에서 오탐하지 않는다.

    2026-10-06 에 RAG_OUTPUT_TEMPLATE_MULTI_STRICT 를 이 형식으로 바꿨다
    (docs/experiments/template_collapse_1006/). 영문 시스템 이름이 굵게 들어가므로
    english_ratio 가 뜨기 쉬운 자리다 — 아래는 실측 응답에서 가져온 모양이다.
    """
    t = (
        "### 서론\n"
        "RAG는 외부 지식을 활용하여 LLM의 환각을 억제하지만, 검색된 정보가 답변에 "
        "부정적 영향을 미치는 **retrieval-induced hallucination**이라는 한계가 있습니다.\n\n"
        "### 본론\n"
        "1. **Hyper-RAG**: 이진 관계에 국한된 구조적 제약에서 벗어나 n-ary relationships를 "
        "포착하는 하이퍼그래프 표현으로 지식 간 상관관계를 보존합니다 [1]\n"
        "2. **RAGO (Retriever and Output Grading)**: 검색과 생성을 분리해 독립적으로 평가하여 "
        "부적절한 정보 수용 경향을 제어합니다 [2]\n\n"
        "### 결론\n"
        "결과적으로 하이퍼그래프 기반 구조화와 단계별 독립 평가가 병행되어야 합니다."
    )
    assert english_ratio(t) < 0.2
    assert not needs_korean_retry(t)


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
