import pytest

from apps.church_lyrics.compare import compare, tidy

pytestmark = pytest.mark.unit

A = "[Verse 1]\n아침 햇살이 창을 두드리면\n나는 일어나 길을 나서네\n\n\n후렴\n함께 걷는 이 길 위에서 (x2)\n노래하리 오늘도"


def test_tidy_removes_labels_and_repeats():
    assert tidy(A) == "아침 햇살이 창을 두드리면\n나는 일어나 길을 나서네\n\n함께 걷는 이 길 위에서\n노래하리 오늘도"


def test_tidy_removes_markdown_and_punctuation():
    raw = "**내게로 부터 눈을 들어**\n\n**주를 보기 시작할 때\n주의 일을 보겠네**\n아버지, 당신 같은 분은 없네.\n- “할렐루야!” 주님…"
    assert tidy(raw) == "내게로 부터 눈을 들어\n\n주를 보기 시작할 때\n주의 일을 보겠네\n아버지 당신 같은 분은 없네\n할렐루야 주님"
    assert tidy("**[후렴]**\n주님을 볼 때 (x2)") == "주님을 볼 때"
    assert tidy("[0:31] 매일의 삶을 살다가\n1:02:15 보면") == "매일의 삶을 살다가\n보면"


def test_agree_despite_line_breaks_and_spacing():
    b = "아침 햇살이 창을 두드리면 나는 일어나 길을 나서네\n함께걷는 이 길 위에서\n노래하리, 오늘도"
    result = compare([A, b])
    assert result.status == "agree" and result.issues == []


def test_differ_reports_the_line_and_its_counterpart():
    b = tidy(A).replace("길을 나서네", "길을 떠나네")
    result = compare([A, b])
    assert result.status == "differ"
    assert len(result.issues) == 1
    line, other = result.issues[0]
    assert {line, other} == {"나는 일어나 길을 나서네", "나는 일어나 길을 떠나네"}


def test_third_source_breaks_the_tie():
    wrong = tidy(A).replace("두드리면", "두드리며")
    result = compare([wrong, A, tidy(A)])
    assert result.status == "agree" and "두드리면" in result.lyrics


def test_single_and_empty():
    assert compare([A]).status == "single"
    with pytest.raises(ValueError):
        compare(["", "  "])


def test_source_sharing_nothing_is_excluded():
    other_song = "완전히 다른 노래\n전혀 겹치지 않는\n세 번째 줄"
    result = compare([A, other_song, tidy(A)])
    assert result.status == "agree" and result.used == [0, 2] and result.excluded == [1]


def test_two_unrelated_sources_keep_the_one_with_the_title():
    song = "자유를 선포해\n난 용납되었네\n정죄함은 없네"
    result = compare(["완전히 다른 노래\n전혀 겹치지 않는", song], title="자유를 선포해")
    assert result.status == "single" and result.base == 1 and result.excluded == [0]
    assert compare(["가 나 다\n라 마 바", "사 아 자\n차 카 타"]).base == 0  # 제목이 둘 다 없으면 검색 순위
