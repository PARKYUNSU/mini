"""콘티(02 찬양 아래 목록)에서 곡명을 뽑습니다. 네트워크를 쓰지 않는 순수 함수입니다."""
from __future__ import annotations

import re
from dataclasses import dataclass

_KEY = r"[A-G][#b♭♯]?m?"
# 키 표기만 떼어냅니다: (G), ( G -> A ), (A→B), (F, 후렴만)
_KEY_PAREN = re.compile(rf"\s*[(（]\s*{_KEY}(\s*(->|=>|→|-|~|>)\s*{_KEY})*\s*(?:[,，/]([^)）]*))?[)）]")
# 키 표기 뒤의 인도자 이름: "곡명 (B): 인화"
# 괄호 없이 끝에 붙인 키: '곡명 Bb', '곡명 D->E', '곡명(메모)Bb'
_BARE_KEY = re.compile(rf"(?:\s+|(?<=[)）]))({_KEY}(?:\s*(?:->|=>|→|-|~|>)\s*{_KEY})*)\s*$")
# 끝의 괄호 연주 메모: (후렴,카피x)
_TAIL_MEMO = re.compile(r"\s*[(（]([^)）]*(?:후렴|브릿지|카피|인트로|간주|엔딩|아웃트로|원곡|만|x|X)[^)）]*)[)）]\s*$")
# 괄호 메모: (*뉴송?)
_MEMO = re.compile(r"\s*[(（]\s*\*([^)）]*)[)）]")
# 괄호 밖의 + 만 곡 구분입니다: (E, 브릿지+후렴만) 은 한 곡의 메모
_MEDLEY = re.compile(r"\+(?![^()（）]*[)）])")
_LEADER = re.compile(r"([)）])\s*[:：]\s*[^\s:：()（）]{1,10}\s*$")
# 곡이 아닌 것: 연주 구간, 아직 정하지 않은 자리
_NOT_SONG = {"인트로", "전주", "간주", "미정", "tbd", "추후공지"}
_URL = re.compile(r"https?://\S+")
_NUMBERED = re.compile(r"^\s*\d+\s*[.)]\s*(.+)$")
_ROLE = re.compile(
    r"^\s*\*?\s*((?:말씀|설교)\s*후\s*찬양|헌금\s*찬양|봉헌\s*찬양|파송\s*찬양|결단\s*찬양)\s*[:：\-–—]\s*(.+)$"
)
# 콘티 머리 줄의 날짜: '2026. 11. 22 드림공동체 주일 찬양' 은 번호 목록이 아님
_DATE_LINE = re.compile(r"^\s*\d{2,4}\s*[./-]\s*\d{1,2}\s*[./-]\s*\d{1,2}\b")


@dataclass
class Song:
    title: str
    url: str | None = None
    role: str = "찬양"
    note: str = ""        # 키 표기 안의 메모: (F, 후렴만) → '후렴만'


def clean_title(raw: str) -> str:
    title = _URL.sub("", raw).strip()
    title = _LEADER.sub(r"\1", title)
    title, _ = _strip_tail(_MEMO.sub("", _KEY_PAREN.sub("", title)))
    return title.strip(" \t-·*")


def _strip_tail(text: str) -> tuple[str, list[str]]:
    """끝의 키와 연주 메모를 번갈아 뗍니다: '곡 Bb -> Cb (원곡C)', '곡(후렴,카피x)Bb'. 뗀 메모도 돌려줍니다."""
    notes, text = [], text.strip()
    while True:
        memo = _TAIL_MEMO.search(text)
        new = _BARE_KEY.sub("", _TAIL_MEMO.sub("", text)).strip()
        if memo:
            notes.insert(0, memo.group(1).strip())
        if new == text:
            return text, notes
        text = new


def titles(raw: str) -> list[tuple[str, str]]:
    """한 줄에서 (곡명, 메모)들. '+' 는 이어 부르는 곡:
    '입례(E->F) + 날 향한 계획 (F, 후렴만): 인화' → [('입례', ''), ('날 향한 계획', '후렴만')]."""
    out = []
    for part in _MEDLEY.split(raw):
        title = clean_title(part)
        if title and norm(title) not in {norm(x) for x in _NOT_SONG}:
            text = _URL.sub("", part)
            notes = [m.group(3).strip() for m in _KEY_PAREN.finditer(text) if m.group(3)]
            notes += [m.group(1).strip() for m in _MEMO.finditer(text)]
            notes += _strip_tail(_KEY_PAREN.sub("", _LEADER.sub(r"\1", text)))[1]
            out.append((title, ", ".join(n for n in notes if n)))
    return out


def norm(title: str) -> str:
    """곡명 비교용 키: 공백·기호를 지우고 소문자로."""
    return re.sub(r"[\W_]+", "", title).lower()


def parse(items) -> list[Song]:
    """items: (kind, text, urls) 목록. kind는 'numbered' | 'bulleted' | 'other'."""
    songs: list[Song] = []

    def add(raw, url, role="찬양"):
        for name, note in titles(raw):  # 이어 부르는 곡들은 같은 영상 링크를 참고로 함께 씁니다
            songs.append(Song(name, url, role, note))

    for kind, text, urls in items:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        found = _URL.findall(text) + list(urls or [])
        if kind == "numbered":
            add(next((ln for ln in lines if not _URL.fullmatch(ln)), ""), found[0] if found else None)
            continue
        for i, ln in enumerate(lines):
            role = _ROLE.match(ln)
            if role:
                add(role.group(2), None, re.sub(r"\s+", " ", role.group(1)))
                continue
            if _DATE_LINE.match(ln):
                continue
            numbered = _NUMBERED.match(ln)  # 번호 목록 대신 "1. 곡명 (G)"로 적은 경우
            if numbered:
                add(numbered.group(1), found[0] if found else None)
            elif i == 0 and kind == "bulleted" and _KEY_PAREN.search(ln):
                add(ln, found[0] if found else None)  # 글머리 목록에 "곡명 (F): 인화"로 적은 곡
    unique, seen = [], set()
    for song in songs:
        if norm(song.title) not in seen:
            seen.add(norm(song.title))
            unique.append(song)
    return unique
