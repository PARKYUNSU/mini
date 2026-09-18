"""로컬 9B 출력의 '영어로 새는' 패턴 탐지·정리.

실패율 평가(v2)에서 잡담·플래너 실패의 대부분이 한 원인이었다:
한국어 요청에 ``### 🧠 Reasoning Process`` / ``### [Self-Reflection]`` / ``[Full Output (for reference)]``
같은 **영어 메타 섹션**을 먼저 쓰거나 답 전체를 영어로 쓰는 것. 프롬프트 규칙만으로는 잘 안 듣기 때문에
(1) 메타 섹션은 잘라내고 (2) 그래도 영어 비율이 높으면 호출 측이 한국어 재생성을 한 번 시도한다.
"""

from __future__ import annotations

import re

_HANGUL_RE = re.compile(r"[가-힣]")
_LATIN_RE = re.compile(r"[A-Za-z]")
# 영어 비율 계산에서 제외: 코드 블록·인라인 코드·URL·볼드 스팬(영문 논문 제목)·📄 제목 줄
_EXCLUDE_RE = re.compile(
    r"```[\s\S]*?```|`[^`\n]+`|https?://\S+|\*\*[^*\n가-힣]+\*\*|^.*📄.*$", re.MULTILINE
)  # 볼드 스팬은 한글이 없는(영문 논문 제목류) 것만 제외 — 한글 볼드는 답변 본문
# 모델이 답 앞뒤에 붙이는 영어 메타 섹션 헤더 (실패 로그에서 수집)
_META_HEADER_RE = re.compile(
    r"^\s*#{1,4}\s*(?:🧠\s*)?\[?\s*(?:reasoning(?: process)?|self[- ]reflection|planner reasoning|"
    r"thought(?: process)?|analysis|short response|full output[^\n\]]*|internal (?:notes?|critic)|"
    r"step 0[^\n]*)\s*\]?\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def english_ratio(text: str) -> float:
    """(한글+라틴 문자) 중 라틴 비율. 코드·URL·영문 제목은 제외. 0.0~1.0."""
    plain = _EXCLUDE_RE.sub(" ", text or "")
    h = len(_HANGUL_RE.findall(plain))
    l = len(_LATIN_RE.findall(plain))
    return (l / (h + l)) if (h + l) else 0.0


_STEP_LINE_RE = re.compile(r"^\s*\d+\s*단계\s*[:：]")


def strip_english_meta_sections(text: str) -> str:
    """``### Reasoning Process`` 류 영어 메타 섹션을 제거.

    - 헤더부터 다음 헤더(또는 끝)까지를 한 섹션으로 본다.
    - 메타 섹션이라도 영어 추론 뒤에 실제 답(한글 줄, 'N단계:')이 이어지면 그 지점부터는 살린다
      (플래너가 영어로 생각한 뒤 계획을 쓰는 흔한 형태).
    - ``[Full Output (for reference)]`` 처럼 참고용 전체 출력은 통째로 버린다.
    """
    if not text or "#" not in text:
        return text
    parts = re.split(r"(?m)^(?=#{1,4}\s)", text)
    kept: list[str] = []
    for part in parts:
        if not part.strip():
            continue
        first_line, _, body = part.partition("\n")
        if not _META_HEADER_RE.match(first_line):
            kept.append(part)
            continue
        if "full output" in first_line.lower():
            continue
        lines = body.split("\n")
        idx = next(
            (i for i, ln in enumerate(lines) if _HANGUL_RE.search(ln) or _STEP_LINE_RE.match(ln)),
            None,
        )
        if idx is not None:
            kept.append("\n".join(lines[idx:]) + "\n")
    out = "".join(kept).strip()
    return out if out else text


def needs_korean_retry(text: str, *, max_ratio: float = 0.6) -> bool:
    """한국어 답변이 기대되는데 영어가 지배적이면 True (재생성 트리거)."""
    return english_ratio(text) > max_ratio


KOREAN_RETRY_NUDGE = (
    "방금 답변이 영어였습니다. 같은 내용을 **처음부터 끝까지 한국어로만** 다시 쓰세요. "
    "'Reasoning', 'Self-Reflection', 'Step 0' 같은 영어 제목·자기점검 섹션은 절대 넣지 말고, "
    "첫 글자부터 답변 본문으로 시작하세요. 고유명사·제품명·코드 식별자만 영어 허용."
)
