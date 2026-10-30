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


def test_survey_gate_flag(monkeypatch):
    q = "RAG검색을 했을시에, 두개의 DB에서 서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘"
    monkeypatch.delenv("RAG_SURVEY_GATE", raising=False)
    assert gate_types(q) == []
    monkeypatch.setenv("RAG_SURVEY_GATE", "1")
    assert gate_types(q) == ["list"]
    assert gate_types("하이브리드 검색 결과를 합치는 방법 연구 찾아줘") == ["list"]
    assert gate_types("그래프 기반 RAG 서베이 알려줘") == []  # 서베이 한 편 찾기는 그대로
    assert gate_types("RAG 평가 연구 있어?") == []
