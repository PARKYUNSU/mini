"""core.llm.presence_judge 질문 유형 게이트."""
from core.llm.presence_judge import gate_types, should_judge


def test_gate_types():
    assert "num" in gate_types("MXNorm이 RMSNorm보다 커널 속도가 최대 몇 배 빨라?")
    assert "cmp" in gate_types("LightKV랑 CommVQ 차이가 뭐야?")
    assert "list" in gate_types("KV 캐시 압축 관련 논문 5개 찾아서 설명해줘")
    assert gate_types("RoPE 주파수를 잘라서 컨텍스트 길이를 늘리는 방법 알려줘") == []


def test_should_judge_env(monkeypatch):
    monkeypatch.delenv("RAG_PRESENCE_GATE", raising=False)
    assert should_judge("LightKV랑 CommVQ 차이가 뭐야?")
    monkeypatch.setenv("RAG_PRESENCE_GATE", "1")
    assert not should_judge("LightKV랑 CommVQ 차이가 뭐야?")
    assert should_judge("RoPE 주파수를 잘라서 컨텍스트 길이를 늘리는 방법 알려줘")


def test_open_gate(monkeypatch):
    # docs/experiments/open_gate_1103 — 열린 요청은 판정만 건너뛴다(목록 게이트 · 목록 모드는 그대로)
    monkeypatch.setenv("RAG_PRESENCE_GATE", "1")
    monkeypatch.delenv("RAG_OPEN_GATE", raising=False)
    assert should_judge("요즘 볼만한 RAG 논문 추천해줘")
    monkeypatch.setenv("RAG_OPEN_GATE", "1")
    for q in ("요즘 볼만한 RAG 논문 추천해줘", "LLM 안전성 논문 세 편만 알려줘", "논문 6편 알려줘",
              "최근 AI 논문 아무거나 하나 찾아서 요약해 봐", "다국어 임베딩 연구만 골라줘",
              "입문할 때 읽을 만한 RAG 논문 있어?"):
        assert not should_judge(q), q
        assert "list" not in gate_types(q), q
    for q in ("Transformer 논문 자세히 설명해줘", "추천 시스템에 LLM 쓰는 연구 있어?",
              "한편 RAG 는 검색 품질에 민감하다. 이걸 다룬 연구 있어?", "논문 데이터베이스 두 개를 합칠 때 중복 찾는 방법 있어?"):
        assert should_judge(q), q
