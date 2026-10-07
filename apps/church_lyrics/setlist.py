"""콘티(02 찬양 아래 목록)에서 곡명을 뽑습니다. 네트워크를 쓰지 않는 순수 함수입니다."""
from __future__ import annotations

import re
from dataclasses import dataclass

_KEY = r"[A-G][#b♭♯]?m?"
# 곡명 뒤의 키 표기만 떼어냅니다: (G), (B -> C), (A→B)
_KEY_PAREN = re.compile(rf"\s*[(（]\s*{_KEY}(\s*(->|=>|→|-|~|>)\s*{_KEY})*\s*[)）]\s*$")
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


def clean_title(raw: str) -> str:
    title = _URL.sub("", raw).strip()
    title = _KEY_PAREN.sub("", title)
    return title.strip(" \t-·*")


def norm(title: str) -> str:
    """곡명 비교용 키: 공백·기호를 지우고 소문자로."""
    return re.sub(r"[\W_]+", "", title).lower()


def parse(items) -> list[Song]:
    """items: (kind, text, urls) 목록. kind는 'numbered' | 'bulleted' | 'other'."""
    songs: list[Song] = []
    for kind, text, urls in items:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        found = _URL.findall(text) + list(urls or [])
        if kind == "numbered":
            name = next((ln for ln in lines if not _URL.fullmatch(ln)), "")
            if clean_title(name):
                songs.append(Song(clean_title(name), found[0] if found else None))
            continue
        for ln in lines:
            role = _ROLE.match(ln)
            if role:
                name = clean_title(role.group(2))
                if name:
                    songs.append(Song(name, None, re.sub(r"\s+", " ", role.group(1))))
                continue
            numbered = _NUMBERED.match(ln)  # 번호 목록 대신 "1. 곡명 (G)"로 적은 경우
            if numbered and clean_title(numbered.group(1)):
                songs.append(Song(clean_title(numbered.group(1)), found[0] if found else None))
    unique, seen = [], set()
    for song in songs:
        if norm(song.title) not in seen:
            seen.add(norm(song.title))
            unique.append(song)
    return unique
