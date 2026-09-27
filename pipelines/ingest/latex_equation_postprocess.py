"""
LaTeX / 수식 마크다운 보존·정규화.

- arXiv 초록·PyMuPDF4LLM 마크다운에 흔한 ``\\( ... \\)``, ``\\[ ... \\]`` 를
  텔레그램·RAG 친화적인 ``$...$`` / ``$$...$$`` 로 통일
- 이미 ``$$`` 로 감싸진 블록은 건드리지 않음
"""

from __future__ import annotations

import re


def enrich_text_for_llm_math(text: str) -> str:
    """
    수식 구분자를 마크다운 관례에 맞게 정리합니다.

    PDF 파서가 ``$$`` 를 이미 잘 주는 경우가 많아, 여기서는 **누락·혼용** 위주로 보정합니다.
    """
    if not text or not isinstance(text, str):
        return text

    s = text.replace("\r\n", "\n")

    # \[ ... \] → $$ ... $$ (비탐욕, 줄바꿈 포함)
    s = re.sub(
        r"\\\[\s*(.+?)\s*\\\]",
        lambda m: "$$\n" + m.group(1).strip() + "\n$$",
        s,
        flags=re.DOTALL,
    )

    # \( ... \) → $...$ (인라인)
    s = re.sub(
        r"\\\(\s*(.+?)\s*\\\)",
        r"$\1$",
        s,
        flags=re.DOTALL,
    )

    # 흔한 LaTeX 명령 앞뒤 공백 정리 (깨진 OCR류 완화)
    s = re.sub(r"\$\s+([^$]+?)\s+\$", r"$\1$", s)

    return s
