"""ProPresenter 찬양 라이브러리 사본으로 맞추기(네트워크 없음)."""
import json

import pytest

from apps.church_lyrics import propresenter

pytestmark = pytest.mark.unit

SONGS = [
    {"name": "아침 햇살이 창을 두드리면", "uuid": "1",
     "lines": ["아침 햇살이 창을 두드리면", "나는 일어나 길을 나서네", "함께 걷는 이 길 위에서", "노래하리 오늘도"]},
    {"name": "비전", "uuid": "2", "lines": ["다른 노래 첫 줄입니다", "비전 비전 우리의 비전"]},
]


def test_clean_name():
    assert propresenter.clean_name("01-바다같은 주의 사랑") == "바다같은 주의 사랑"
    assert propresenter.clean_name("WELOVE- 다시 드리는 고백") == "다시 드리는 고백"
    assert propresenter.clean_name("나는 아무것도 아닙니다 - [ 청년2부 ]") == "나는 아무것도 아닙니다"


def test_by_title_uses_name_or_first_line_only():
    assert propresenter.by_title("비전", SONGS)["uuid"] == "2"                 # 이름이 같음
    assert propresenter.by_title("아침 햇살이", SONGS)["uuid"] == "1"           # 첫 줄 앞부분(4자 이상)
    assert propresenter.by_title("아침", SONGS) is None                        # 너무 짧은 앞부분은 안 씀
    assert propresenter.by_title("길을 나서네", SONGS) is None                  # 가사 안쪽 줄로는 맞추지 않음


def test_by_lyrics_needs_enough_overlap():
    web = "아침 햇살이 창을 두드리면 나는 일어나 길을 나서네\n함께걷는 이 길 위에서\n노래하리, 오늘도"
    assert propresenter.by_lyrics(web, SONGS)["uuid"] == "1"
    assert propresenter.by_lyrics("전혀 다른 가사 한 줄\n또 다른 줄", SONGS) is None


def test_load_missing_or_broken_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(propresenter, "CACHE", tmp_path / "x.json")
    assert propresenter.load() == []
    (tmp_path / "x.json").write_text("{broken", encoding="utf-8")
    assert propresenter.load() == []
    (tmp_path / "x.json").write_text(json.dumps({"songs": SONGS}), encoding="utf-8")
    assert propresenter.load() == SONGS
