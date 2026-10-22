"""관련 문서 거르기의 응답 해석 · 안전장치 (docs/experiments/relevance_filter_1022)."""

from core.llm.relevance_filter import _brief, filter_relevant, parse_relevant


def test_parse_relevant():
    assert parse_relevant("관련: 1, 3", 5) == {1, 3}
    assert parse_relevant("답: 관련: 없음", 5) == set()
    assert parse_relevant("관련: 7", 5) is None  # 범위 밖뿐 → 못 읽음
    assert parse_relevant("모르겠다", 5) is None


def test_single_block_not_called():
    assert filter_relevant("q", "[2401.00001v1] A\n초록", "x") == ("[2401.00001v1] A\n초록", "대상 아님")


def test_brief_skips_header():
    b = "[Distance: 0.3]\n[발행일: 2026-01-01]\n[2410.14641v3] LongPiBench\n[초록] Positional bias in long context."
    assert _brief(2, b) == "[2] LongPiBench\n[초록] Positional bias in long context."


def test_protected_names():
    from core.llm.relevance_filter import _names, protected

    q = "World4RL이랑 가변 길이 잠재 월드모델 연구는 어떻게 달라? LLM RAG 기준으로"
    assert _names(q) == {"world4rl"}  # LLM · RAG 같은 일반 약어는 아니다
    blocks = ["[2606.21775v1] Variable-length Latent World Models\n…", "[2509.19080v2] World4RL: Diffusion World Models\n…"]
    assert protected(q, blocks) == {2}
    assert _names("SLMQuant랑 Block-Sphere Vector Quantization 차이") == {"slmquant", "block-sphere"}
