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
        line = _BULLET.sub("", _MARKUP.sub("", raw).strip())
        line = _REPEAT.sub("", line)
        if _LABEL.match(line):
            line = ""
        line = re.sub(r"\s+", " ", _PUNCT.sub(" ", line)).strip()
        if line or (out and out[-1]):
            out.append(line)
    return "\n".join(out).strip()


@dataclass
class Result:
    status: str                      # 'agree' | 'differ' | 'single'
    lyrics: str                      # 기준으로 고른 가사
    base: int = 0                    # 기준 출처의 번호
    issues: list[tuple[str, str | None]] = field(default_factory=list)  # (기준 줄, 다른 출처의 비슷한 줄)


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


def compare(sources: list[str]) -> Result:
    """기준 가사의 각 줄이 다른 출처에도 있는지 봅니다(줄바꿈 위치가 달라도 일치로 봅니다)."""
    sources = [s for s in (tidy(s) for s in sources) if s]
    if not sources:
        raise ValueError("가사가 없습니다")
    if len(sources) == 1:
        return Result("single", sources[0])
    best = None
    for i, base in enumerate(sources):
        issues = _issues(base, sources[:i] + sources[i + 1:])
        if best is None or len(issues) < len(best.issues):
            best = Result("differ" if issues else "agree", base, i, issues)
    return best
