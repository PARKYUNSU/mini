import pytest

from apps.church_lyrics.setlist import Song, clean_title, parse

pytestmark = pytest.mark.unit


def test_clean_title_strips_only_key_parens():
    assert clean_title("우리 주 하나님 (B -> C)") == "우리 주 하나님"
    assert clean_title("사랑의 계절은 (G)") == "사랑의 계절은"
    assert clean_title("새 노래 (F#m→A)") == "새 노래"
    assert clean_title("주 은혜임을 (Live)") == "주 은혜임을 (Live)"
    assert clean_title("곡명 https://youtu.be/abc") == "곡명"


def test_parse_real_page_shape():
    items = [
        ("other", "<10월4일_드림 주일 예배 찬양 콘티>", []),
        ("numbered", "첫째 곡 (B -> C)\nhttps://youtu.be/aaa?si=1", ["https://youtu.be/aaa?si=1"]),
        ("numbered", "둘째 곡 (G)\nhttps://youtu.be/bbb", []),
        ("bulleted", "인트로 참고\nhttps://youtu.be/ccc", []),
        ("bulleted", "말씀 후 찬양: 셋째 곡", []),
        ("bulleted", "헌금찬양: 넷째 곡\n*파송찬양: 다섯째 곡", []),
    ]
    assert parse(items) == [
        Song("첫째 곡", "https://youtu.be/aaa?si=1"),
        Song("둘째 곡", "https://youtu.be/bbb"),
        Song("셋째 곡", None, "말씀 후 찬양"),
        Song("넷째 곡", None, "헌금찬양"),
        Song("다섯째 곡", None, "파송찬양"),
    ]


def test_parse_typed_numbers_and_duplicates():
    items = [("other", "1. 첫째 곡 (A)\n2) 둘째 곡", []), ("bulleted", "파송찬양: 첫째곡", [])]
    assert [s.title for s in parse(items)] == ["첫째 곡", "둘째 곡"]


def test_empty_setlist():
    assert parse([("other", "여기 아래에 찬양 자료를 그냥 드래그해서 올려 주세요.", [])]) == []
