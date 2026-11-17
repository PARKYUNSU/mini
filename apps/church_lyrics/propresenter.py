"""교회 ProPresenter 찬양 라이브러리 사본. 실제 예배에 띄운 가사라 웹 가사보다 먼저 씁니다.

- 사본: ``.cron/propresenter_songs.json`` (주 1회 GET 으로 새로 받음, 교회 맥이 꺼져 있어도 사본으로 동작)
- 라이브러리 곡 이름은 대개 첫 가사라 콘티 곡명과 다릅니다. 그래서 이름·첫 줄이 같을 때만 이름으로 맞추고,
  나머지는 웹에서 찾은 가사와 줄이 충분히 겹치는 곡을 찾아 맞춥니다(곡명이 가사 어딘가에 있는지는 보지 않음 —
  '비전'·'날마다' 처럼 짧은 곡명은 다른 곡 가사에도 흔함).
- 읽기 전용: GET 만 보냅니다.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
import urllib.request
from pathlib import Path

from .compare import agreement
from .setlist import norm

CACHE = Path(__file__).resolve().parents[2] / ".cron" / "propresenter_songs.json"
SAME_SONG = 0.5     # 웹 가사와 이만큼 겹치면 같은 곡
MIN_PREFIX = 4      # 첫 줄 앞부분으로 맞출 때 곡명 최소 글자 수(공백 빼고)


def _get(path: str):
    base = os.environ["PROPRESENTER_URL"].rstrip("/")
    with urllib.request.urlopen(urllib.request.Request(base + path, headers={"Accept": "application/json"}), timeout=15) as r:
        return json.load(r)


def _nfc(s) -> str:
    return unicodedata.normalize("NFC", s or "")


def clean_name(name: str) -> str:
    """'01-곡', 'WELOVE- 곡', '곡 - [ 청년2부 ]' → '곡'."""
    name = re.sub(r"\s*-\s*\[[^\]]*\]\s*$", "", _nfc(name))
    return re.sub(r"^\d+\s*-\s*|^[A-Za-z]+\s*-\s*", "", name).strip()


def sync() -> int:
    """라이브러리(PROPRESENTER_LIBRARY, 기본 '찬양')의 곡 가사를 받아 사본을 새로 씁니다. 받은 곡 수를 돌려줍니다."""
    want = os.getenv("PROPRESENTER_LIBRARY", "찬양")
    lib = next(x for x in _get("/v1/libraries") if _nfc(x.get("name")) == want)
    songs = []
    for item in _get(f"/v1/library/{lib['uuid']}").get("items", []):
        pres = _get(f"/v1/presentation/{item['uuid']}").get("presentation", {})
        lines = [_nfc(ln).strip() for g in pres.get("groups", []) for s in g.get("slides", [])
                 for ln in (s.get("text") or "").splitlines() if ln.strip()]
        if lines:
            songs.append({"name": clean_name(item.get("name")), "uuid": item["uuid"], "lines": lines})
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"library": want, "songs": songs}, ensure_ascii=False), encoding="utf-8")
    tmp.replace(CACHE)
    return len(songs)


def load() -> list[dict]:
    """사본의 곡 목록. 사본이 없거나 깨졌으면 빈 목록(웹 검색만으로 계속)."""
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))["songs"]
    except (OSError, ValueError, KeyError):
        return []


def by_title(title: str, songs: list[dict]) -> dict | None:
    """곡 이름이 같거나, 첫 줄이 콘티 곡명으로 시작하는 곡."""
    k = norm(title)
    for song in songs:
        if norm(song["name"]) == k:
            return song
    if len(k) >= MIN_PREFIX:
        for song in songs:
            if norm(song["lines"][0]).startswith(k):
                return song
    return None


def by_lyrics(lyrics: str, songs: list[dict]) -> dict | None:
    """웹에서 찾은 가사와 줄이 가장 많이 겹치는 곡(SAME_SONG 이상일 때만)."""
    best, found = SAME_SONG, None
    for song in songs:
        score = agreement(lyrics, "\n".join(song["lines"]))
        if score >= best:
            best, found = score, song
    return found
