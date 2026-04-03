from __future__ import annotations

import pytest


def test_circuit_breaker_retry_once(monkeypatch, capsys):
    # import 내부: 쿨다운/플래그 동작만 검증(Chroma query는 호출하지 않음)
    import core.rag.agent_chroma_rag as rag

    # 강제 리셋
    rag._clear_vector_search_disabled()

    now0 = 1_000_000.0
    monkeypatch.setattr(rag.time, "time", lambda: now0)

    rag._set_vector_search_disabled_for_process()
    out = capsys.readouterr().out
    assert "vector search disabled for 600s" in out

    # 쿨다운 중: disallow
    assert rag._vector_search_effective_disabled() is True

    # 쿨다운 종료 직후(첫 retry 허용): allow
    monkeypatch.setattr(rag.time, "time", lambda: now0 + 600.0 + 1.0)
    out = capsys.readouterr().out
    assert rag._vector_search_effective_disabled() is False
    out = capsys.readouterr().out
    assert "cooldown ended, allow 1 retry" in out

    # retry 1회 이미 사용됨: 다시 disallow
    assert rag._vector_search_effective_disabled() is True

    # 성공 가정 후 복구
    rag._clear_vector_search_disabled()
    assert rag._vector_search_effective_disabled() is False


def test_jsonl_rerank_prefers_token_overlap_even_if_not_recent():
    import core.rag.agent_chroma_rag as rag

    query = "hallucination honesty alignment"
    # candidates는 "최근 tail 기반" 순서(0이 더 최근)로 들어온다고 가정.
    candidates = [
        {
            "paper_id": "C2",
            "title": "Security Threats and Alignment",
            "abstract": "We study alignment and security threats.",
            "text": "Safe generation improves alignment.",
            "published_date": "2024-01-02",
        },
        {
            "paper_id": "C1",
            "title": "Hallucination Honesty in LLMs",
            "abstract": "Honesty is reduced when hallucination occurs.",
            "text": "Hallucination harms honesty and truthfulness.",
            "published_date": "2024-01-01",
        },
    ]

    selected = rag._rerank_jsonl_candidates(query, candidates, top_n=1)
    assert len(selected) == 1
    # C2가 더 최근이지만, 토큰 겹침이 더 큰 C1이 상위로 와야 함
    assert selected[0]["paper_id"] == "C1"

