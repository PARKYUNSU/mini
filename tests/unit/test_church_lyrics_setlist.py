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


def test_parse_leader_names_medley_and_bulleted_songs():
    """10-11 페이지 모양: 키 뒤 인도자 이름, '입례 + 곡' 메들리, 미정 자리, 글머리 목록의 곡."""
    items = [
        ("other", "<10월 11일_ 드림 주일 예배_ 셀브 앗싸!>", []),
        ("numbered", "입례(E->F) + 날 향한 계획 (F, 후렴만): 인화\nhttps://youtu.be/a", []),
        ("numbered", "자유를 선포해 (B): 인화\nhttps://youtu.be/b", []),
        ("numbered", "주님을 바라보는 자 ( G ): 찬영\nhttps://youtu.be/c", []),
        ("numbered", "비전 ( G -> A ): 찬영\nhttps://youtu.be/d", []),
        ("bulleted", "헌금찬양: 내 영혼은 안전합니다\n*말씀 후 찬양: 미정\n*파송찬양", []),
        ("bulleted", "내 아버지 집에는 기쁨이 넘쳐나네 (F): 인화\n*인터2: 건반 솔로 X, 일렉솔로8마디만\nhttps://youtu.be/e", []),
        ("bulleted", "인트로 참고\nhttps://youtu.be/f", []),
    ]
    assert parse(items) == [
        Song("날 향한 계획", "https://youtu.be/a"),
        Song("자유를 선포해", "https://youtu.be/b"),
        Song("주님을 바라보는 자", "https://youtu.be/c"),
        Song("비전", "https://youtu.be/d"),
        Song("내 영혼은 안전합니다", None, "헌금찬양"),
        Song("내 아버지 집에는 기쁨이 넘쳐나네", "https://youtu.be/e"),
    ]
