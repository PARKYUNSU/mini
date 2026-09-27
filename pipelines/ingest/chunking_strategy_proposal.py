"""청킹 보조 유틸 — 참고문헌 컷·노이즈 휴리스틱·인접 소청크 병합.

``RagProcessor.chunk_markdown`` / ``add_paper``에서 import 해 사용한다.
(시맨틱 병합 ``semantic_merge_placeholder``만 아직 미연동.)
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

# --- 참고문헌 / 부록 컷오프 (휴리스틱) ------------------------------------------

# 줄 시작 헤딩 형태: References, Bibliography, Appendix, Acknowledgements, Works Cited 등
_REF_HEADING_RE = re.compile(
    r"(?im)^\s*(#+\s*)?"
    r"(references|bibliography|"
    r"acknowledg(?:e)?ments?|"
    r"appendix(?:\s+[a-z0-9.\-:]+)?|"
    r"works\s+cited|literature\s+cited|"
    r"end\s*notes?)"
    r"\b.*$"
)


def truncate_at_references_section(markdown: str) -> str:
    """본문 뒤 References / Bibliography / Appendix 등 이후는 청킹·BM25 노이즈이므로 삭제.

    - 첫 번째 매칭 섹션 헤딩(``# References`` 또는 단독 줄) **이전**만 유지.
    - 매칭이 없으면 원문 유지.
    """
    if not (markdown or "").strip():
        return markdown or ""
    m = _REF_HEADING_RE.search(markdown)
    if not m:
        return markdown.rstrip()
    return markdown[: m.start()].rstrip()


# --- 수식·URL·짧은 줄 비율 (노이즈 힌트) ----------------------------------------

_DISPLAY_MATH_FRAG = re.compile(r"\$\$[\s\S]{0,800}?\$\$")
_INLINE_MATH_DENSE = re.compile(r"(?<!\\)\$(?!\$)[^$\n]{1,120}\$(?!\$)")
# LaTeX 스타일 블록 (PDF→MD에서 흔함)
_DISPLAY_BRACKET = re.compile(r"\\\[[\s\S]{0,2000}?\\\]")
_INLINE_PAREN = re.compile(r"\\\([\s\S]{0,800}?\\\)")
_URL_LINE = re.compile(r"https?://\S+", re.I)


def math_token_ratio(text: str) -> float:
    """0~1 근사: 수식·LaTeX 블록 문자 비율. 높을수록 서술형 검색 청크로 부적합."""
    if not text.strip():
        return 1.0
    sample = text if len(text) <= 12000 else text[:12000]
    math_chars = 0
    for seg in _DISPLAY_MATH_FRAG.findall(sample):
        math_chars += len(seg)
    for seg in _INLINE_MATH_DENSE.findall(sample):
        math_chars += len(seg)
    for seg in _DISPLAY_BRACKET.findall(sample):
        math_chars += len(seg)
    for seg in _INLINE_PAREN.findall(sample):
        math_chars += len(seg)
    return min(1.0, math_chars / max(len(sample), 1))


def url_token_ratio(text: str) -> float:
    if not text.strip():
        return 0.0
    sample = text if len(text) <= 12000 else text[:12000]
    hit = sum(len(m.group(0)) for m in _URL_LINE.finditer(sample))
    return min(1.0, hit / max(len(sample), 1))


# --- Step 1: 청크 품질 게이트 (Scale-up 전 데이터 정제) -------------------------

CHUNK_MIN_CHARS = 80
CHUNK_MAX_MATH_RATIO = 0.3
CHUNK_MAX_URL_RATIO = 0.2


def passes_chunk_quality_filter(text: str) -> bool:
    """Chroma·BM25 적재 전 청크 품질 검사. False면 DB에 넣지 않음.

    - 너무 짧음 (노이즈 조각)
    - 수식/특수기호 비율 과다 (math_ratio > CHUNK_MAX_MATH_RATIO)
    - URL 비율 과다 (url_ratio > CHUNK_MAX_URL_RATIO)
    """
    t = (text or "").strip()
    if len(t) < CHUNK_MIN_CHARS:
        return False
    if math_token_ratio(t) > CHUNK_MAX_MATH_RATIO:
        return False
    if url_token_ratio(t) > CHUNK_MAX_URL_RATIO:
        return False
    return True


def is_probably_noise_paragraph(text: str, *, max_len: int = 400) -> bool:
    """레거시 호환: ``passes_chunk_quality_filter`` 와 동일 기준으로 노이즈 여부."""
    return not passes_chunk_quality_filter(text)


# --- 인접 소청크 병합 (문자 기반, 임베딩 없음) ------------------------------------

def merge_small_neighbors(
    chunks: list[str],
    *,
    min_chars: int = 120,
    max_merged: int = 900,
    separator: str = "\n\n",
) -> list[str]:
    """연속된 짧은 청크를 앞 청크에 붙여 과분할을 줄임 (문맥 단절 완화).

    - ``min_chars`` 미만이면 다음과 합침(합친 길이가 ``max_merged`` 넘기 전까지).
    - LangChain Document 리스트에는 ``page_content``에 적용하면 됨.
    """
    if not chunks:
        return []
    out: list[str] = []
    buf = chunks[0].strip()
    for nxt in chunks[1:]:
        nxt = nxt.strip()
        if len(buf) < min_chars and len(buf) + len(nxt) + len(separator) <= max_merged:
            buf = f"{buf}{separator}{nxt}"
        else:
            if buf:
                out.append(buf)
            buf = nxt
    if buf:
        out.append(buf)
    return out


def preprocess_for_chunking(markdown: str) -> str:
    """청킹 전 단일 파이프라인: References/Bibliography/Appendix 등 이후 절단 + 공백 정리."""
    md = (markdown or "").strip()
    if not md:
        return md
    md = truncate_at_references_section(md)
    return md


# --- (선택) 시맨틱 병합 훅 — 구현은 비워 두고 시그니처만 제안 --------------------

def semantic_merge_placeholder(
    chunks: list[str],
    _embed_fn: Callable[..., Any] | None = None,
    _similarity_threshold: float = 0.92,
) -> list[str]:
    """레거시 이름 유지. 실제 시맨틱 병합은 ``RagProcessor._semantic_merge_documents``에서 수행."""
    return chunks


def proposed_pipeline_order() -> list[str]:
    """RagProcessor 실제 순서 (문서화용)."""
    return [
        "preprocess_for_chunking (truncate references)",
        "MarkdownHeaderTextSplitter + RecursiveCharacterTextSplitter",
        "RagProcessor._merge_adjacent_documents",
        "RagProcessor._semantic_merge_documents (ENABLE_SEMANTIC_MERGE)",
        "add_paper: passes_chunk_quality_filter (len≥80, math≤0.3, url≤0.2)",
        "upsert to Chroma",
    ]
