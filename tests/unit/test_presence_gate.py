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
