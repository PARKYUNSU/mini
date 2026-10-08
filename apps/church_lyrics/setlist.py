"""콘티(02 찬양 아래 목록)에서 곡명을 뽑습니다. 네트워크를 쓰지 않는 순수 함수입니다."""
from __future__ import annotations

import re
from dataclasses import dataclass

_KEY = r"[A-G][#b♭♯]?m?"
# 키 표기만 떼어냅니다: (G), ( G -> A ), (A→B), (F, 후렴만)
_KEY_PAREN = re.compile(rf"\s*[(（]\s*{_KEY}(\s*(->|=>|→|-|~|>)\s*{_KEY})*\s*(?:[,，/]([^)）]*))?[)）]")
# 키 표기 뒤의 인도자 이름: "곡명 (B): 인화"
_LEADER = re.compile(r"([)）])\s*[:：]\s*[^\s:：()（）]{1,10}\s*$")
# 곡이 아닌 것: 연주 구간, 아직 정하지 않은 자리
_NOT_SONG = {"인트로", "전주", "간주", "미정", "tbd", "추후공지"}
_URL = re.compile(r"https?://\S+")
_NUMBERED = re.compile(r"^\s*\d+\s*[.)]\s*(.+)$")
_ROLE = re.compile(
    r"^\s*\*?\s*(말씀\s*후\s*찬양|헌금\s*찬양|봉헌\s*찬양|파송\s*찬양|결단\s*찬양)\s*[:：]\s*(.+)$"
)


@dataclass
class Song:
    title: str
    url: str | None = None
    role: str = "찬양"
    note: str = ""        # 키 표기 안의 메모: (F, 후렴만) → '후렴만'


def clean_title(raw: str) -> str:
    title = _URL.sub("", raw).strip()
    title = _LEADER.sub(r"\1", title)
    title = _KEY_PAREN.sub("", title)
    return title.strip(" \t-·*")


def titles(raw: str) -> list[tuple[str, str]]:
    """한 줄에서 (곡명, 메모)들. '+' 는 이어 부르는 곡:
    '입례(E->F) + 날 향한 계획 (F, 후렴만): 인화' → [('입례', ''), ('날 향한 계획', '후렴만')]."""
    out = []
    for part in raw.split("+"):
        title = clean_title(part)
        if title and norm(title) not in {norm(x) for x in _NOT_SONG}:
            notes = [m.group(3).strip() for m in _KEY_PAREN.finditer(_URL.sub("", part)) if m.group(3)]
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
