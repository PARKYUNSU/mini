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
    monkeypatch.setattr(sources, "bugs_tracks", lambda title: [])
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


def test_youtube_pages_are_never_sources(fake, monkeypatch):
    monkeypatch.setattr(sources, "search", lambda q: [
        {"url": "https://www.youtube.com/watch?v=x", "raw_content": PAGE},
        {"url": "https://m.youtube.com/watch?v=y", "raw_content": PAGE},
        {"url": "https://youtu.be/z", "raw_content": PAGE}])
    assert sources.candidates("첫째 곡") == []
    assert fake["keys"] == []


def test_proofread_spacing_must_keep_letters_and_typos_are_separate(fake):
    lyrics = "구원 하심이 보좌에 앉으신\n우리 하나님과 어린 양께 있도다\n\n함께 모여 친트 열어요"
    fake["answer"] = (
        '{"spacing": [{"line": 0, "text": "구원하심이 보좌에 앉으신"},'
        ' {"line": 1, "text": "우리 하나님과 어린양께 있도다"},'
        ' {"line": 1, "text": "우리 하나님과 어린양께 있나이다"},'   # 글자가 바뀐 띄어쓰기 제안은 버림
        ' {"line": 9, "text": "없는 줄"}, {"line": "x"}],'
        ' "typos": [{"line": 3, "suggest": "함께 모여 잔치 열어요"},'
        ' {"line": 0, "suggest": "구원하심이 보좌에 앉으신"}]}')   # 띄어쓰기뿐인 오탈자 제안은 버림
    spacing, typos = sources.proofread(lyrics, "비전")
    assert spacing == [("구원 하심이 보좌에 앉으신", "구원하심이 보좌에 앉으신"),
                       ("우리 하나님과 어린 양께 있도다", "우리 하나님과 어린양께 있도다")]
    assert typos == [("함께 모여 친트 열어요", "함께 모여 잔치 열어요")]
    assert sources.apply_respace(lyrics, spacing).splitlines()[:2] == [
        "구원하심이 보좌에 앉으신", "우리 하나님과 어린양께 있도다"]


def test_proofread_bad_answer_changes_nothing(fake):
    for answer in ("not json", "[]", '{"spacing": "x", "typos": null}'):
        fake["answer"] = answer
        assert sources.proofread("아무 가사") == ([], [])


def test_naver_blogs_and_daum_cafes_count_per_owner():
    assert sources.site("https://m.blog.naver.com/si2pas/220344062079") == sources.site(
        "https://m.blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=si2pas&logNo=1")
    assert sources.site("https://m.blog.naver.com/97grace/1") != sources.site("https://blog.naver.com/js_cjw/2")
    assert sources.site("https://m.cafe.daum.net/speakjesus/RdMN/47") != sources.site("https://cafe.daum.net/lordfirst/IJYq/1")
    assert sources.site("https://inamen.tistory.com/4521") == "inamen.tistory.com"


SONG = "아침 햇살이 창을 두드리면\n나는 일어나 길을 나서네\n함께 걷는 이 길 위에서\n노래하리 오늘도"
OTHER = "전혀 다른 노래의 첫 줄\n겹치지 않는 둘째 줄\n또 다른 셋째 줄\n마지막 넷째 줄"


def test_bugs_page_parsing(monkeypatch):
    search = """<tr albumId="1" trackId="33" rowType="track"><p class="title" adult_yn="N"><a onclick="x" title="첫째 &amp; 곡">a</a></p>
    <p class="artist"><a href="u" title="어노인팅(Anointing)">b</a></p></tr>"""
    monkeypatch.setattr(sources, "_bugs_get", lambda url: search if "search" in url else f"<xmp>{SONG}\n&lt;후렴&gt;</xmp>")
    assert sources.bugs_tracks("곡") == [("33", "첫째 & 곡", "어노인팅(Anointing)")]
    assert sources.bugs_lyrics("33") == SONG


def _bugs(monkeypatch, tracks, lyrics):
    monkeypatch.setattr(sources, "bugs_tracks", lambda title: tracks)
    monkeypatch.setattr(sources, "bugs_lyrics", lambda track_id: lyrics[track_id])


def test_bugs_picks_track_that_matches_other_sources(monkeypatch):
    _bugs(monkeypatch, [("1", "곡", "갑"), ("2", "곡", "을"), ("3", "다른 곡", "병")], {"1": OTHER, "2": SONG})
    got = sources.bugs_candidate("곡", None, [sources.Candidate("https://a.example", SONG)])
    assert got.url.endswith("/track/2") and got.verify_only
    assert sources.bugs_candidate("곡", None, [sources.Candidate("https://a.example", "관계없는 가사 한 줄\n또 한 줄")]) is None


def test_bugs_alone_needs_artist_or_a_single_track(monkeypatch):
    two = [("1", "곡", "갑"), ("2", "곡", "어노인팅(Anointing)")]
    _bugs(monkeypatch, two, {"1": OTHER, "2": SONG})
    assert sources.bugs_candidate("곡", "곡 - 어노인팅 공식", []).url.endswith("/track/2")
    assert sources.bugs_candidate("곡", None, []) is None          # 같은 제목 둘, 가수 모름: 쓰지 않음
    assert sources.bugs_candidate("곡", "곡 - 다른 팀", []) is None
    _bugs(monkeypatch, [("1", "곡", "갑")], {"1": SONG})
    assert sources.bugs_candidate("곡", None, []).url.endswith("/track/1")


def test_bugs_is_off_by_default(fake, monkeypatch):
    monkeypatch.delenv("CHURCH_LYRICS_BUGS", raising=False)
    asked = []
    monkeypatch.setattr(sources, "bugs_tracks", lambda title: asked.append(title) or [])
    sources.candidates("첫째 곡")
    assert asked == []


def test_bugs_failure_keeps_web_results(fake, monkeypatch):
    monkeypatch.setenv("CHURCH_LYRICS_BUGS", "1")
    def boom(title):
        raise OSError("페이지 바뀜")
    monkeypatch.setattr(sources, "bugs_tracks", boom)
    assert len(sources.candidates("첫째 곡")) == 2


def test_bugs_alone_uses_majority_of_same_title_tracks(monkeypatch):
    three = [("1", "곡", "갑"), ("2", "곡", "을"), ("3", "곡", "병")]
    _bugs(monkeypatch, three, {"1": OTHER, "2": SONG, "3": SONG})
    assert sources.bugs_candidate("곡", "곡 - 다른 팀", []).url.endswith("/track/2")
    # 과반이 아니면(1:1) 쓰지 않음, 가수가 맞으면 과반보다 먼저
    _bugs(monkeypatch, three[:2], {"1": OTHER, "2": SONG})
    assert sources.bugs_candidate("곡", None, []) is None
    _bugs(monkeypatch, three + [("4", "곡", "어노인팅")], {"1": SONG, "2": SONG, "3": SONG, "4": OTHER})
    assert sources.bugs_candidate("곡", "곡 어노인팅", []).url.endswith("/track/4")
    # 가사 있는 트랙이 하나뿐이면 그 트랙(⚠️ 출처 1곳뿐으로 게시됨)
    _bugs(monkeypatch, three[:2], {"1": "", "2": SONG})
    assert sources.bugs_candidate("곡", None, []).url.endswith("/track/2")


@pytest.mark.parametrize("hint,title,want", [
    ("F.I.A LIVE WORSHIP - 주 예수 내 맘에 들어와 (찬송가 289장/피아버전) / WHAT A WONDERFUL CHANGE IN MY LIFE (FIA.ver)",
     "주 예수 내 맘에 들어와 계시니", "주 예수 내 맘에 들어와"),
    ("주의 사랑을 주의 선하심을   I   레브워십", "주의 사랑을 주의 선하심을", None),   # 같으면 다시 찾지 않음
    ("[AGAPAO Worship] 베드로의 고백 / Peter's Confession", "베드로의 고백", None),
    ("전혀 다른 영상 - 다른 노래", "베드로의 고백", None),
    (None, "베드로의 고백", None),
])
def test_youtube_song_title(hint, title, want):
    assert sources.youtube_song_title(hint, title) == want


def test_second_search_uses_title_from_video(fake, monkeypatch):
    asked = []
    monkeypatch.setattr(sources, "youtube_title", lambda url: "팀 - 첫째 곡 노래 / Song")
    monkeypatch.setattr(sources, "search", lambda q: asked.append(q) or [])
    assert sources.candidates("첫째 곡 노래 가사말", "https://youtu.be/x") == []
    assert asked == ["첫째 곡 노래 가사말 가사 찬양 CCM", "첫째 곡 노래 가사 찬양 CCM"]
