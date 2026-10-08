"""가사 정리와 출처 간 대조. 네트워크를 쓰지 않는 순수 함수입니다."""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

_LABEL = re.compile(
    r"^\s*[\[(（<]?\s*(verse|chorus|bridge|pre-?chorus|intro|outro|interlude|tag|ending|"
    r"후렴|간주|전주|브릿지|브리지|\d+\s*절)\s*\d*\s*[\])）>]?\s*[:：]?\s*$",
    re.I,
)
_REPEAT = re.compile(r"\s*[(\[]?\s*[x×*]\s*\d+\s*[)\]]?\s*$", re.I)
# 자막에 쓰지 않는 것: 마크다운 강조·제목·인용 표시와 줄 앞 글머리, 문장부호·따옴표
_MARKUP = re.compile(r"[*_#`>]+")
_BULLET = re.compile(r"^[-•·]\s+")
_TIMESTAMP = re.compile(r"[\[(]?\b\d{1,2}:\d{2}(:\d{2})?\b[\])]?")  # 유튜브 본문의 [0:31]
_PUNCT = re.compile(r"[,.!?;:…~\"'“”‘’、。，．！？；：]+")


def key(s: str) -> str:
    """비교용 키: 공백·문장부호를 지웁니다. 띄어쓰기 차이는 차이로 보지 않습니다."""
    return re.sub(r"[\W_]+", "", s).lower()


def tidy(text: str) -> str:
    """마크다운 표시(**)·문장부호(, .)·구간 표시([후렴], 1절)·반복 표시(x2)를 지우고 빈 줄을 하나로 줄입니다.

    글자를 지우기만 하고 바꾸거나 더하지는 않습니다.
    """
    out: list[str] = []
    for raw in text.replace("\r", "").split("\n"):
        line = _BULLET.sub("", _MARKUP.sub("", _TIMESTAMP.sub("", raw)).strip())
        line = _REPEAT.sub("", line)
        if _LABEL.match(line):
            line = ""
        line = re.sub(r"\s+", " ", _PUNCT.sub(" ", line)).strip()
        if line or (out and out[-1]):
            out.append(line)
    return "\n".join(out).strip()


OTHER_SONG = 0.3  # 다른 출처와 겹치는 줄이 이 비율보다 적으면 다른 곡(또는 가사 없는 페이지)으로 봅니다


@dataclass
class Result:
    status: str                      # 'agree' | 'differ' | 'single'
    lyrics: str                      # 기준으로 고른 가사
    base: int = 0                    # 기준 출처의 번호(입력 순서)
    issues: list[tuple[str, str | None]] = field(default_factory=list)  # (기준 줄, 다른 출처의 비슷한 줄)
    used: list[int] = field(default_factory=list)      # 대조에 쓴 출처 번호
    excluded: list[int] = field(default_factory=list)  # 다른 곡으로 보여 뺀 출처 번호
    respaced: list[tuple[str, str]] = field(default_factory=list)  # 띄어쓰기를 맞춘 줄 (전, 후)


def _issues(base: str, others: list[str]):
    blobs = [key(o) for o in others]
    other_lines = [ln.strip() for o in others for ln in o.splitlines() if key(ln)]
    other_keys = [key(ln) for ln in other_lines]
    out, seen = [], set()
    for line in base.splitlines():
        k = key(line)
        if not k or k in seen or any(k in blob for blob in blobs):
            continue
        seen.add(k)
        close = difflib.get_close_matches(k, other_keys, n=1, cutoff=0.6)
        out.append((line.strip(), other_lines[other_keys.index(close[0])] if close else None))
    return out


def overlap(a: str, b: str) -> float:
    """a 의 줄 가운데 b 에도 있는 줄의 비율(줄바꿈·띄어쓰기 차이는 무시)."""
    lines = {key(ln) for ln in a.splitlines() if key(ln)}
    blob = key(b)
    return sum(k in blob for k in lines) / len(lines) if lines else 0.0


def unify_spacing(lyrics: str, sources: list[str]) -> tuple[str, list[tuple[str, str]]]:
    """띄어쓰기만 다른 같은 줄을 한 표기로 맞춥니다. 새 표기를 만들지 않고, 출처들에 실제로 있는 표기 가운데
    가장 많이 쓰인 것을 고릅니다(동점이면 붙여 쓴 쪽)."""
    variants: dict[str, dict[str, int]] = {}
    for text in sources:
        for ln in text.splitlines():
            if key(ln):
                counts = variants.setdefault(key(ln), {})
                counts[ln.strip()] = counts.get(ln.strip(), 0) + 1
    out, changed = [], []
    for ln in lyrics.splitlines():
        counts = variants.get(key(ln), {})
        best = max(counts, key=lambda v: (counts[v], -v.count(" ")), default=ln.strip()) if key(ln) else ln
        if key(ln) and best != ln.strip():
            if (ln.strip(), best) not in changed:
                changed.append((ln.strip(), best))
            ln = best
        out.append(ln)
    return "\n".join(out), changed


def compare(sources: list[str], title: str = "") -> Result:
    """기준 가사의 각 줄이 다른 출처에도 있는지 봅니다(줄바꿈 위치가 달라도 일치로 봅니다).

    다른 어느 출처와도 거의 겹치지 않는 출처는 다른 곡으로 보고 대조에서 뺍니다. 전부 서로 다르면
    가사에 곡 제목이 들어 있는 출처 하나(없으면 검색 순위가 높은 것)만 씁니다.
    """
    texts = {i: t for i, t in ((i, tidy(s)) for i, s in enumerate(sources)) if t}
    if not texts:
        raise ValueError("가사가 없습니다")
    ids = list(texts)
    kept = [i for i in ids if len(ids) == 1
            or max(overlap(texts[i], texts[j]) for j in ids if j != i) >= OTHER_SONG]
    if not kept:
        kept = [next((i for i in ids if title and key(title) in key(texts[i])), ids[0])]
    excluded = [i for i in ids if i not in kept]
    if len(kept) == 1:
        best = Result("single", texts[kept[0]], kept[0], used=kept, excluded=excluded)
    else:
        best = None
        for i in kept:
            issues = _issues(texts[i], [texts[j] for j in kept if j != i])
            if best is None or len(issues) < len(best.issues):
                best = Result("differ" if issues else "agree", texts[i], i, issues, kept, excluded)
    best.lyrics, best.respaced = unify_spacing(best.lyrics, [texts[i] for i in kept])
    return best
