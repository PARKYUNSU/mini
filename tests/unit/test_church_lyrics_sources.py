"""sources: 모델은 줄 번호만 돌려주고 가사 글자는 코드가 원문에서 자릅니다(네트워크 없음)."""
import pytest

from apps.church_lyrics import sources
from core.llm import agent_gemini

pytestmark = pytest.mark.unit

PAGE = "광고\n첫째 곡 가사\n아침 햇살이\n창을 두드리면\n나는 일어나\n길을 나서네\n댓글 3개"


@pytest.fixture
def fake(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY_2", "k2")
    calls = {"answer": '{"found": true, "start": 2, "end": 5}', "keys": None}

    def generate(keys, model, prompt):
        calls["keys"] = keys
        return calls["answer"]
    monkeypatch.setattr(agent_gemini, "gemini_sdk_generate_json", generate)
    monkeypatch.setattr(sources, "search", lambda q: [
        {"url": "https://a.example/1", "raw_content": PAGE},
        {"url": "https://a.example/2", "raw_content": PAGE},   # 같은 사이트는 한 번만
        {"url": "https://b.example/1", "raw_content": PAGE}])
    return calls


def test_lyrics_are_cut_from_source_by_line_numbers(fake):
    found = sources.candidates("첫째 곡")
    assert [c.url for c in found] == ["https://a.example/1", "https://b.example/1"]
    assert found[0].lyrics == "아침 햇살이\n창을 두드리면\n나는 일어나\n길을 나서네"
    assert fake["keys"] == ["k2"]


@pytest.mark.parametrize("answer", [
    '{"found": false}', '{"found": true, "start": 5, "end": 2}',
    '{"found": true, "start": 0, "end": 99}', "[]", "not json"])
def test_bad_answers_are_dropped(fake, answer):
    fake["answer"] = answer
    assert sources.candidates("첫째 곡") == []
