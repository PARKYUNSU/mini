"""로컬·클라우드 LLM이 동일 구절을 연속 반복할 때 텔레그램·캐시 오염을 막기 위한 후처리."""

from __future__ import annotations


def collapse_adjacent_repeated_spans(text: str, *, span_lo: int = 18, span_hi: int = 420) -> str:
    """
    문자열 안에서 어떤 부분 문자열이 바로 옆에 똑같이 이어 붙은 경우,
    연속 반복 전체를 **첫 한 번**만 남긴다. (작은 모델의 repetition 붕괴 완화)
    """
    if not text or len(text) < span_lo * 3:
        return text
    out: list[str] = []
    i = 0
    n = len(text)
    hi = min(span_hi, n)
    while i < n:
        matched = False
        upper_bound = min(hi, n - i)
        for length in range(upper_bound, span_lo - 1, -1):
            if i + 2 * length > n:
                continue
            chunk = text[i : i + length]
            if chunk != text[i + length : i + 2 * length]:
                continue
            j = i + length
            while j + length <= n and text[j : j + length] == chunk:
                j += length
            out.append(chunk)
            i = j
            matched = True
            break
        if not matched:
            out.append(text[i])
            i += 1
    return "".join(out)


def collapse_long_consecutive_duplicate_lines(text: str, *, min_line_chars: int = 28) -> str:
    """같은 긴 줄이 여러 번 연속이면 한 줄만 유지."""
    lines = text.split("\n")
    out: list[str] = []
    for ln in lines:
        if (
            out
            and ln == out[-1]
            and len(ln.strip()) >= min_line_chars
        ):
            continue
        out.append(ln)
    return "\n".join(out)


def sanitize_llm_news_like_blob(text: str) -> str:
    """뉴스 브리핑·웹요약 등 마크다운 블롭용 안전 후처리(순서 고정)."""
    if not text or not text.strip():
        return text
    t = text.strip()
    for _ in range(24):
        u = collapse_adjacent_repeated_spans(t)
        u = collapse_long_consecutive_duplicate_lines(u)
        if u == t:
            break
        t = u
    # 줄 병합 후에도 한 줄 안 인접 반복이 드러날 수 있음
    t = collapse_adjacent_repeated_spans(t)
    return t.strip()
