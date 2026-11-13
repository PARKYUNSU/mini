"""답변 전에 질문 주제를 직접 다루지 않는 문서를 뺀다 (docs/experiments/relevance_filter_1022).

왜: 정답 유무 판정은 문서 하나만 고르고, 답변 단계는 판정과 무관하게 받은 문서를 다 쓴다. 그래서
"중간 정보 손실" 질문에 GQA 비용 최적화 · 희소 어텐션 논문을 인용하고 "(질문과 관련 없음)"이라고 적었다.
판정과 따로 "직접 다루는 문서를 모두" 묻고 나머지를 뺀다. 못 읽거나 '없음'이면 그대로 둔다.
"""

from __future__ import annotations

import os
import re

from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.conclusion_rewrite import brief_findings

__all__ = ["PROMPT", "parse_relevant", "protected", "filter_relevant", "PROMPT_V2", "parse_graded", "filter_graded"]

PROMPT = """아래는 사용자의 질문으로 검색한 논문 목록이다.

[질문]
{question}

[논문 목록]
{docs}

질문이 묻는 주제를 **직접** 다루는 논문의 번호를 모두 적어라.
- 단어 몇 개만 겹치고 다른 문제(예: 효율화 · 다른 과제)를 다루는 논문은 빼라.
- 출력은 정확히 한 줄: `관련: 1, 3` 또는 `관련: 없음`"""

_ABS = 600
# 질문에 나온 고유 이름(소문자와 함께 대문자가 둘째 자리 뒤에 있거나 숫자가 섞인 말 — World4RL · SLMQuant · DeepFusion).
# LLM · RAG 같은 일반 약어(소문자 없음)는 아니다. 이 이름이 제목에 든 문서는 늘 남긴다 — 2단계에서 비교 질문의
# World4RL 을 뺐다 (relevance_filter_1022 §6).
_NAME = re.compile(r"(?<![A-Za-z0-9])[A-Za-z][A-Za-z0-9\-]*(?![A-Za-z0-9])")  # "World4RL이랑" — 한글 조사가 붙어도


def names(question: str) -> list[str]:
    """질문 속 고유 이름 — 원래 대소문자 · 나온 순서 그대로 (검색의 이름 찾기 RAG_NAME_LOOKUP 도 쓴다)."""
    return list(dict.fromkeys(t for t in _NAME.findall(question)
                              if len(t) >= 4 and re.search(r"[a-z]", t) and re.search(r"[A-Z0-9]", t[1:])))


def _names(question: str) -> set[str]:
    return {t.lower() for t in names(question)}


def _title(block: str) -> str:
    return next((l for l in block.split("\n") if re.match(r"\[\d{4}\.\d{4,5}", l.strip())), "")


def protected(question: str, blocks: list[str]) -> set[int]:
    """제목에 질문 속 고유 이름이 든 문서 번호(1부터)."""
    names = _names(question)
    return {i for i, b in enumerate(blocks, 1) if names and any(n in _title(b).lower() for n in names)}


def parse_relevant(raw: str, n: int) -> set[int] | None:
    """``{번호}`` · 빈 집합(없음) · None(못 읽음)."""
    m = re.search(r"관련\s*[:：]\s*(.+)", raw or "")
    if not m:
        return None
    if "없음" in m.group(1):
        return set()
    nums = {int(x) for x in re.findall(r"\d{1,2}", m.group(1)) if 1 <= int(x) <= n}
    return nums or None


def _brief(i: int, block: str) -> str:
    lines = block.strip().split("\n")
    k = next((j for j, l in enumerate(lines) if re.match(r"\[\d{4}\.\d{4,5}", l)), 0)
    body = re.sub(r"\s+", " ", " ".join(lines[k + 1:])).strip()
    # 앞 600자는 배경 문장이 많다 — 제안 · 결과 · 대상 문장을 고른다 (RAG_FILTER_FINDINGS, docs/experiments/filter_input_1104)
    if os.getenv("RAG_FILTER_FINDINGS", "0").strip() == "1" and "[초록] " in block:
        body = "[초록] " + brief_findings(block.split("[초록] ", 1)[1].split("\n\n", 1)[0], _ABS - 5)
    return f"[{i}] {re.sub(r'^\[[^\]]+\]\s*', '', lines[k])}\n{body[:_ABS]}"


def filter_relevant(question: str, context: str, model: str) -> tuple[str, str]:
    """``(걸러진 컨텍스트, 상태)``. 상태: "n→m" · "대상 아님" · "못 읽음" · "없음" · "호출 실패"."""
    blocks = [b for b in (context or "").split(RAG_HIT_SEP) if b.strip()]
    if len(blocks) < 2:
        return context, "대상 아님"
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    prompt = PROMPT.format(question=question, docs="\n\n".join(_brief(i, b) for i, b in enumerate(blocks, 1)))
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=32))
    try:
        raw = str(llm.invoke(prompt).content or "")
    except Exception as exc:  # 거르지 못해도 답은 낸다
        print(f"[DEBUG] relevance_filter 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return context, "호출 실패"
    keep = parse_relevant(raw, len(blocks))
    if keep is None:
        return context, "못 읽음"
    if not keep:
        return context, "없음"
    keep |= protected(question, blocks)
    return RAG_HIT_SEP.join(b for i, b in enumerate(blocks, 1) if i in keep), f"{len(blocks)}→{len(keep)}"


# 3단계 거르기 (docs/experiments/graded_1113) — 남김/뺌 대신 문서마다 핵심 · 관련 · 무관. 운영 연결 전(기본 꺼짐).
PROMPT_V2 = """아래는 사용자의 질문으로 검색한 논문 목록이다.

[질문]
{question}

[논문 목록]
{docs}

논문마다 질문과의 관계를 하나로 판정하라.
- 핵심: 질문이 묻는 주제(질문에 여러 항목이 있으면 그중 하나)가 이 논문의 주된 내용이다.
- 관련: 질문 주제를 일부 다루거나 가까운 문제를 다룬다(같은 문제의 다른 측면, 그 기법을 한 단계로 쓰는 연구).
- 무관: 낱말이나 넓은 분야만 겹치고 주된 내용이 다른 문제다. 질문 주제가 중심이 아닌 넓은 개관 · 서베이도 무관이다.

출력은 논문마다 한 줄, 다른 말 없이:
1: 핵심
2: 무관"""

_GRADE = re.compile(r"^\s*\[?(\d{1,2})\]?\s*[:：.)]?\s*\**\s*(핵심|관련|무관)", re.M)


def parse_graded(raw: str, n: int) -> dict[int, str] | None:
    """``{번호: 핵심|관련|무관}``. 번호 하나라도 못 읽으면 None — 호출 쪽은 거르지 않는다."""
    got = {int(i): g for i, g in _GRADE.findall(raw or "") if 1 <= int(i) <= n}
    return got if len(got) == n else None


def filter_graded(question: str, context: str, model: str, keep: tuple[str, ...] = ("핵심", "관련")) -> tuple[str, str, dict[int, str] | None]:
    """``(걸러진 컨텍스트, 상태, 등급)``. 상태는 ``filter_relevant`` 와 같다. 남는 게 없으면 그대로 둔다."""
    blocks = [b for b in (context or "").split(RAG_HIT_SEP) if b.strip()]
    if len(blocks) < 2:
        return context, "대상 아님", None
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    prompt = PROMPT_V2.format(question=question, docs="\n\n".join(_brief(i, b) for i, b in enumerate(blocks, 1)))
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=16 * len(blocks) + 16))
    try:
        raw = str(llm.invoke(prompt).content or "")
    except Exception as exc:  # 거르지 못해도 답은 낸다
        print(f"[DEBUG] relevance_filter(v2) 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return context, "호출 실패", None
    grades = parse_graded(raw, len(blocks))
    if grades is None:
        return context, "못 읽음", None
    kept = {i for i, g in grades.items() if g in keep} | protected(question, blocks)
    if not kept:
        return context, "없음", grades
    return RAG_HIT_SEP.join(b for i, b in enumerate(blocks, 1) if i in kept), f"{len(blocks)}→{len(kept)}", grades
