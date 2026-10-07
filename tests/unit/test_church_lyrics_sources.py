"""sources: 모델은 줄 번호만 돌려주고 가사 글자는 코드가 원문에서 자릅니다(네트워크 없음)."""
import pytest

from apps.church_lyrics import sources
from core.config import agent_config  # noqa: F401 — 실제 .env 로딩을 가짜 키 설정보다 먼저 끝냄
from core.llm import agent_gemini

pytestmark = pytest.mark.unit

PAGE = "광고\n첫째 곡 가사\n아침 햇살이\n창을 두드리면\n나는 일어나\n길을 나서네\n댓글 3개"
BOTH = '{"spans": [{"doc": 0, "found": true, "start": 2, "end": 5}, {"doc": 1, "found": true, "start": 2, "end": 5}]}'


@pytest.fixture
def fake(monkeypatch):
    for i in range(1, 21):
        monkeypatch.delenv(f"GEMINI_API_KEY_{i}", raising=False)
    monkeypatch.setenv("GEMINI_API_KEY", "k1")
    monkeypatch.setenv("GEMINI_API_KEY_2", "k2")
    monkeypatch.setenv("GEMINI_API_KEY_5", "k5")
    monkeypatch.setenv("GEMINI_API_KEY_7", "k2")   # 중복 값은 한 번만
    calls = {"answer": BOTH, "keys": [], "prompts": []}

    def generate(keys, model, prompt):
        calls["keys"].append(keys)
        calls["prompts"].append(prompt)
        return calls["answer"]
    monkeypatch.setattr(agent_gemini, "gemini_sdk_generate_json", generate)
    monkeypatch.setattr(sources, "search", lambda q: [
        {"url": "https://a.example/1", "raw_content": PAGE},
        {"url": "https://a.example/2", "raw_content": PAGE},          # 같은 사이트는 한 번만
        {"url": "https://c.example/1", "raw_content": "다른 곡 이야기"},  # 곡명 없는 페이지는 보내지 않음
        {"url": "https://b.example/1", "raw_content": PAGE}])
    return calls


def test_one_call_per_song_and_lyrics_cut_from_source(fake):
    found = sources.candidates("첫째 곡")
    assert [c.url for c in found] == ["https://a.example/1", "https://b.example/1"]
    assert found[0].lyrics == "아침 햇살이\n창을 두드리면\n나는 일어나\n길을 나서네"
    assert fake["keys"] == [["k2", "k5"]]  # 1번 키는 쓰지 않고 2~20번을 순서대로
    assert "=== 문서 1 ===" in fake["prompts"][0] and "=== 문서 2 ===" not in fake["prompts"][0]


@pytest.mark.parametrize("answer", [
    '{"spans": [{"doc": 0, "found": false}]}',
    '{"spans": [{"doc": 0, "found": true, "start": 5, "end": 2}]}',
    '{"spans": [{"doc": 0, "found": true, "start": 0, "end": 99}]}',
    '{"spans": [{"doc": 7, "found": true, "start": 2, "end": 5}]}',
    '{"spans": "x"}', "[]", "not json"])
def test_bad_answers_are_dropped(fake, answer):
    fake["answer"] = answer
    assert sources.candidates("첫째 곡") == []


def test_no_model_call_when_no_page_has_the_title(fake, monkeypatch):
    monkeypatch.setattr(sources, "search", lambda q: [{"url": "https://c.example/1", "raw_content": "다른 곡"}])
    assert sources.candidates("첫째 곡") == []
    assert fake["keys"] == []
