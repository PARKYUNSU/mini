"""답 형식 다듬기 (RAG_FORMAT_FIX, docs/experiments/format_fix_1117).

왜: 11-16 업무 질문 10개 사용자 평가에서
- 깨진 글자 5건 — 다시 쓰기가 영어 용어를 소리대로 옮김(포izoning · 판판 · 라울러 · 채킹), 거부된 다시 쓰기 뒤 원래 항목의 한자(六点).
- '없음' 판정 답이 관련 연구를 나열하고도 서론 · 결론에서 "찾는 연구가 없습니다" 라고 해 모순으로 읽힘(1 · 3번).
"""

from __future__ import annotations

import os
import re

__all__ = ["format_fix_active", "term_rule", "strip_hanzi", "partial_wording", "_GLUED"]

_GLUED = re.compile(r"[가-힣][a-z]{2,}")  # 한글 바로 뒤 라틴 소문자 — "포izoning". "LLM을" 같은 대문자 약어 + 조사는 안 걸린다
_HAN = re.compile(r"[一-鿿㐀-䶿]+")
_LEAD_OLD = re.compile(r"제공된 문서에는 질문이 찾는 연구가 없습니다\.?")
_CONCL_OLD = re.compile(r"따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다\.?")
LEAD_NEW = "질문을 직접 다룬 연구는 찾지 못했고, 가장 가까운 연구는 아래와 같습니다."
CONCL_NEW = "따라서 질문을 직접 다룬 연구는 없지만, 위 관련 연구가 가장 가깝습니다."


def format_fix_active() -> bool:
    return os.getenv("RAG_FORMAT_FIX", "0").strip() == "1"


def term_rule() -> str:
    """다시 쓰기 · 결론 프롬프트에 넣는 용어 규칙 한 줄(꺼져 있으면 빈 문자열)."""
    if not format_fix_active():
        return ""
    return "- 영어 전문 용어(예: poisoning · judge · rater · chunking)는 한글로 소리 나는 대로 옮기지 말고 영어 그대로 쓴다.\n"


def strip_hanzi(answer: str) -> tuple[str, int]:
    """남은 한자 덩어리를 지운다 — 앞뒤 공백은 하나로."""
    n = len(_HAN.findall(answer or ""))
    if not n:
        return answer, 0
    return re.sub(r"[ \t]{2,}", " ", _HAN.sub(" ", answer)), n


def partial_wording(answer: str) -> tuple[str, int]:
    """'없음' 판정 답에 (관련 연구) 항목이 있으면 고정 문장을 "직접 다룬 연구는 없고 가장 가까운 연구는" 꼴로."""
    if "관련 연구" not in (answer or ""):
        return answer, 0
    out, a = _LEAD_OLD.subn(LEAD_NEW, answer)
    out, b = _CONCL_OLD.subn(CONCL_NEW, out)
    return out, a + b
