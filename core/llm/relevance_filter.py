"""답변 전에 질문 주제를 직접 다루지 않는 문서를 뺀다 (docs/experiments/relevance_filter_1022).

왜: 정답 유무 판정은 문서 하나만 고르고, 답변 단계는 판정과 무관하게 받은 문서를 다 쓴다. 그래서
"중간 정보 손실" 질문에 GQA 비용 최적화 · 희소 어텐션 논문을 인용하고 "(질문과 관련 없음)"이라고 적었다.
판정과 따로 "직접 다루는 문서를 모두" 묻고 나머지를 뺀다. 못 읽거나 '없음'이면 그대로 둔다.
"""

from __future__ import annotations

import re

from core.llm.citation_fix import RAG_HIT_SEP

__all__ = ["PROMPT", "parse_relevant", "filter_relevant"]

PROMPT = """아래는 사용자의 질문으로 검색한 논문 목록이다.

[질문]
{question}

[논문 목록]
{docs}

질문이 묻는 주제를 **직접** 다루는 논문의 번호를 모두 적어라.
- 단어 몇 개만 겹치고 다른 문제(예: 효율화 · 다른 과제)를 다루는 논문은 빼라.
- 출력은 정확히 한 줄: `관련: 1, 3` 또는 `관련: 없음`"""

_ABS = 600


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
    return RAG_HIT_SEP.join(b for i, b in enumerate(blocks, 1) if i in keep), f"{len(blocks)}→{len(keep)}"
