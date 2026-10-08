"""노션·검색을 가짜로 바꿔 토요일 작업의 흐름을 확인합니다(네트워크 없음)."""
from datetime import date

import pytest

from apps.church_lyrics import jobs, notion, sources

pytestmark = pytest.mark.unit

LYRICS = "아침 햇살이 창을 두드리면\n나는 일어나 길을 나서네"


def rt(s):
    return [{"plain_text": s, "href": None}]


def block(kind, s="", id_=None, **extra):
    return {"id": id_ or kind + s[:6], "type": kind, "has_children": False,
            kind: {"rich_text": rt(s), **extra}}


@pytest.fixture
def world(monkeypatch):
    monkeypatch.setenv("NOTION_SUNDAY_DB_ID", "sunday")
    monkeypatch.setenv("NOTION_LYRICS_DB_ID", "lyrics?v=abc")
    monkeypatch.delenv("CHURCH_LYRICS_SKIP", raising=False)
    w = {
        "pages": [{"id": "p1", "created_time": "2026-10-07T00:00:00.000Z",
                   "properties": {"실제 주일 날짜": {"formula": {"date": {"start": "2026-10-11"}}}}}],
        "db": [],
        "kids": {"p1": [
            block("heading_3", "01 자막 · 방송(PPT 자료)"),
            {"id": "d1", "type": "divider", "has_children": False, "divider": {}},
            block("heading_3", "02 찬양", "h2"),
            block("callout", "여기 아래에 찬양 자료를 그냥 드래그해서 올려 주세요.", "c0"),
            block("numbered_list_item", "첫째 곡 (G)\nhttps://youtu.be/aaa", "n1"),
            block("bulleted_list_item", "파송찬양: 둘째 곡", "b1"),
            block("paragraph", "", "empty"),   # 실제 페이지처럼 콘티 뒤 빈 줄
        ]},
        "appended": [],
        "saved": [],
    }
    monkeypatch.setattr(notion, "children", lambda i: w["kids"].get(i, []))
    monkeypatch.setattr(notion, "query", lambda db, body=None, limit=None:
                        w["pages"] if db == "sunday" else w["db"])
    monkeypatch.setattr(notion, "append", lambda parent, blocks, after=None:
                        w["appended"].append((parent, after, blocks)))

    def call(method, path, body=None):
        w["saved"].append(body)
        return {"id": "new"}
    monkeypatch.setattr(notion, "call", call)
    monkeypatch.setattr(sources, "candidates", lambda title, url=None: [
        sources.Candidate("https://a.example/1", LYRICS),
        sources.Candidate("https://b.example/2", LYRICS)])
    return w


def header(b):
    return b["callout"]["rich_text"][0]["text"]["content"]


def test_target_sunday():
    assert jobs.target_sunday(date(2026, 10, 10)) == "2026-10-11"   # 토요일
    assert jobs.target_sunday(date(2026, 10, 11)) == "2026-10-11"   # 주일 당일
    assert jobs.target_sunday(date(2026, 10, 7)) == "2026-10-11"    # 수요일


def test_publishes_after_the_setlist(world):
    assert jobs.lyrics_job("2026-10-11") == 0
    (parent, after, blocks), = world["appended"]
    assert (parent, after) == ("p1", "b1")
    assert header(blocks[0]).startswith("[자동 가사] 첫째 곡 · 찬양 — 출처 2곳 일치")
    assert blocks[0]["callout"]["icon"]["emoji"] == "✅"
    # 링크 없는 곡은 출처가 일치해도 사람이 한 번 보게 합니다
    assert "링크 없는 곡" in header(blocks[1]) and blocks[1]["callout"]["icon"]["emoji"] == "⚠️"
    kinds = [k["type"] for k in blocks[0]["callout"]["children"]]
    assert kinds == ["paragraph", "code", "to_do"]


def test_rerun_skips_published_and_dry_run_writes_nothing(world):
    world["kids"]["p1"].append(block("callout", "[자동 가사] 첫째 곡 · 찬양 — 출처 2곳 일치", "auto1"))
    assert jobs.lyrics_job("2026-10-11", dry_run=True) == 0
    assert world["appended"] == []
    jobs.lyrics_job("2026-10-11")
    assert [header(b).split(" · ")[0] for b in world["appended"][0][2]] == ["[자동 가사] 둘째 곡"]


def test_checked_lyrics_go_to_db_then_come_from_db(world):
    world["kids"]["p1"].append(block("callout", "[자동 가사] 둘째 곡 · 파송찬양 — 확인 필요", "auto2"))
    world["kids"]["auto2"] = [block("code", "고친 가사"), block("to_do", "확인 완료", checked=True)]
    jobs.lyrics_job("2026-10-11")
    saved = world["saved"][0]
    assert saved["parent"] == {"database_id": "lyrics"}
    assert saved["properties"]["title"]["title"][0]["text"]["content"] == "둘째 곡"
    assert saved["children"][0]["code"]["rich_text"][0]["text"]["content"] == "고친 가사"

    # 다음 주: 같은 곡이 가사 DB에 있으면 검색하지 않고 그대로 씁니다
    world["db"] = [{"id": "song2", "properties": {"곡명": {"type": "title", "title": rt("둘째곡")}}}]
    world["kids"]["song2"] = [block("code", "고친 가사")]
    world["kids"]["p1"] = world["kids"]["p1"][:5] + [block("bulleted_list_item", "헌금찬양: 둘째 곡", "b2"), block("paragraph", "", "empty")]
    world["appended"].clear()
    jobs.lyrics_job("2026-10-11")
    b = world["appended"][0][2][1]
    assert b["callout"]["icon"]["emoji"] == "📗"
    assert [k["type"] for k in b["callout"]["children"]] == ["code"]


def test_no_setlist_and_missing_page(world):
    world["kids"]["p1"] = world["kids"]["p1"][:4]
    assert jobs.lyrics_job("2026-10-11") == 2
    assert jobs.lyrics_job("2026-10-18") == 1
    assert world["appended"] == []


def test_one_failing_song_does_not_stop_the_rest(world, monkeypatch):
    def flaky(title, url=None):
        if title == "첫째 곡":
            raise RuntimeError("검색 실패")
        return [sources.Candidate("https://a.example/1", LYRICS)]
    monkeypatch.setattr(sources, "candidates", flaky)
    jobs.lyrics_job("2026-10-11")
    icons = [b["callout"]["icon"]["emoji"] for b in world["appended"][0][2]]
    assert icons == ["❌", "⚠️"]


def test_skip_list_leaves_fixed_songs_out(world, monkeypatch):
    monkeypatch.setenv("CHURCH_LYRICS_SKIP", "둘째곡, 없는 곡")
    jobs.lyrics_job("2026-10-11")
    assert [header(b).split(" · ")[0] for b in world["appended"][0][2]] == ["[자동 가사] 첫째 곡"]


def test_mostly_different_sources_are_flagged_as_maybe_other_song(world, monkeypatch):
    monkeypatch.setattr(sources, "candidates", lambda title, url=None: [
        sources.Candidate("https://a.example/1", LYRICS),
        sources.Candidate("https://b.example/2", "전혀 다른 노래의\n가사 두 줄")])
    jobs.lyrics_job("2026-10-11")
    assert "다른 곡일 수 있음" in header(world["appended"][0][2][0])
