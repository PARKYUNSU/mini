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


def test_brief_findings_flag(monkeypatch):
    background = "Retrieval systems are widely used across many different applications today. " * 9
    abstract = f"{background}We propose LongPiBench for long context. The results show a 40% accuracy drop."
    b = f"[2410.14641v3] LongPiBench\n[초록] {abstract}\n\n청크 본문"
    monkeypatch.delenv("RAG_FILTER_FINDINGS", raising=False)
    assert "We propose" not in _brief(1, b)  # 기본은 앞 600자
    monkeypatch.setenv("RAG_FILTER_FINDINGS", "1")
    out = _brief(1, b)
    assert out.startswith("[1] LongPiBench\n[초록] ") and "We propose LongPiBench" in out and "40%" in out
    assert "청크" not in out and len(out.split("\n", 1)[1]) <= 600
    no_abstract = "[2410.14641v3] LongPiBench\n본문 앞부분"
    assert _brief(1, no_abstract) == "[1] LongPiBench\n본문 앞부분"  # 초록 없는 블록은 그대로


def test_protected_names():
    from core.llm.relevance_filter import _names, protected

    q = "World4RL이랑 가변 길이 잠재 월드모델 연구는 어떻게 달라? LLM RAG 기준으로"
    assert _names(q) == {"world4rl"}  # LLM · RAG 같은 일반 약어는 아니다
    blocks = ["[2606.21775v1] Variable-length Latent World Models\n…", "[2509.19080v2] World4RL: Diffusion World Models\n…"]
    assert protected(q, blocks) == {2}
    assert _names("SLMQuant랑 Block-Sphere Vector Quantization 차이") == {"slmquant", "block-sphere"}


def test_parse_graded():
    from core.llm.relevance_filter import parse_graded

    assert parse_graded("1: 핵심\n2: 무관\n3: 관련", 3) == {1: "핵심", 2: "무관", 3: "관련"}
    assert parse_graded("[1] 핵심\n2. **관련**\n3) 무관", 3) == {1: "핵심", 2: "관련", 3: "무관"}
    assert parse_graded("1: 핵심\n2: 무관", 3) is None  # 하나 빠지면 못 읽음
    assert parse_graded("관련: 1, 3", 3) is None


def test_none_keep_top(monkeypatch):
    # filter_none_1114: '관련: 없음' 이면 다 남기던 것을 RAG_FILTER_NONE_KEEP 편만 (이름 보호 문서는 남김)
    import langchain_ollama

    from core.llm import relevance_filter as RF
    from core.llm.citation_fix import RAG_HIT_SEP

    class _LLM:
        def __init__(self, **kw):
            pass

        def invoke(self, p):
            return type("R", (), {"content": "관련: 없음"})()

    monkeypatch.setattr(langchain_ollama, "ChatOllama", _LLM)
    blocks = [f"[240{i}.0000{i}v1] Paper{i}\n[초록] x" for i in range(1, 5)] + ["[2405.00005v1] World4RL: y\n[초록] z"]
    ctx = RAG_HIT_SEP.join(blocks)
    monkeypatch.delenv("RAG_FILTER_NONE_KEEP", raising=False)
    assert RF.filter_relevant("질문", ctx, "m") == (ctx, "없음")
    monkeypatch.setenv("RAG_FILTER_NONE_KEEP", "1")
    out, st = RF.filter_relevant("World4RL 설명해줘", ctx, "m")
    assert st == "없음→2" and out == RAG_HIT_SEP.join([blocks[0], blocks[4]])
    out, st = RF.filter_relevant("질문", ctx, "m")
    assert st == "없음→1" and out == blocks[0]
