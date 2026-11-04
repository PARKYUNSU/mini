"""거르기 뒤 5편이 안 되면 찾은 문서로 검색어를 다시 써 한 번 더 찾아 빈 칸을 채운다 (docs/experiments/query_reform_1105).

왜: 거르기가 맞다고 한 문서에는 첫 검색어에 없는 분야 용어가 있다. 맞는 문서만 되먹여 검색어가 새는 것을 줄이고,
새 문서도 같은 거르기를 거친다. 앞선 문서는 밀어내지 않고 빈 칸에만 넣는다. 어느 단계든 실패하면 그대로 둔다.
"""

from __future__ import annotations

import re
import time
from typing import Callable

from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.conclusion_rewrite import brief_findings
from core.llm.presence_judge import gate_types
from core.llm.relevance_filter import _title, filter_relevant

__all__ = ["PROMPT", "parse_query", "fill_slots"]

# 예시 용어를 넣지 않는다 — 무관한 질문에 새어 들어간다 (query_extract_1021)
PROMPT = """A user asked a question about research papers. A search found these relevant papers:

{papers}

User question:
{question}

Search query already used:
{query}

Write one new English search query to find other papers that answer the user question.
Start with the main topic of the user question in a few words. Then add two or three technical terms from the papers above that the used query does not have.
Do not use paper names or system names.
Return only the query on one line: 6 to 10 English words. No explanations."""

_ABS = 300
_MAX_WORDS = 12
_NO_RETRY = {"num", "cmp"}  # 수치 질문은 정답 논문 하나를 묻고 이미 찾는다. 비교 질문은 대상별 검색을 따로 한다.


def _blocks(context: str) -> list[str]:
    return [b.strip() for b in (context or "").split(RAG_HIT_SEP) if _title(b)]


def _pid(block: str) -> str:
    m = re.search(r"\[(\d{4}\.\d{4,5})", _title(block))
    return m.group(1) if m else ""


def _paper(i: int, block: str) -> str:
    head = _title(block)
    if "[초록] " in block:
        text = brief_findings(block.split("[초록] ", 1)[1].split("\n\n", 1)[0], _ABS)
    else:
        text = re.sub(r"\s+", " ", block.split(head, 1)[1]).strip()[:_ABS]
    return f"{i}. {re.sub(r'^\[[^\]]+\]\s*', '', head.strip())}\n{text}"


def parse_query(raw: str, previous: str) -> str | None:
    """모델 출력의 첫 영어 줄 → 검색어. 3단어 미만이거나 이전 검색어와 단어가 같으면 None."""
    line = next((l for l in (raw or "").splitlines() if re.search(r"[A-Za-z]", l)), "")
    words = re.sub(r"[^A-Za-z0-9\-\s]", " ", line).lower().split()
    if len(words) < 3 or set(words) == set(re.findall(r"[a-z0-9\-]+", (previous or "").lower())):
        return None
    return " ".join(words[:_MAX_WORDS])


def _rewrite(question: str, query: str, blocks: list[str]) -> str:
    from core.llm.agent_llm import get_rag_query_rewrite_llm

    papers = "\n\n".join(_paper(i, b) for i, b in enumerate(blocks, 1))
    prompt = PROMPT.format(papers=papers, question=question, query=query)
    return str(get_rag_query_rewrite_llm(num_predict=48).invoke(prompt).content or "")


def fill_slots(
    question: str, query: str, pool: str, kept: str, *, search: Callable[[str], str], model: str, n: int = 5
) -> tuple[str, dict]:
    """``(컨텍스트, 기록)``. ``pool``: 거르기 전 첫 검색 결과, ``kept``: 거른 뒤, ``search``: 검색어 → 컨텍스트."""
    blocks = _blocks(kept)
    if not 1 <= len(blocks) < n or _NO_RETRY & set(gate_types(question)):
        return kept, {"on": False}
    info: dict = {"on": True, "query": "", "new": 0, "filter": "", "added": [], "s": {}}
    t = time.perf_counter()

    def lap(name: str) -> None:
        nonlocal t
        info["s"][name] = round(time.perf_counter() - t, 2)
        t = time.perf_counter()

    try:
        raw = _rewrite(question, query, blocks)
    except Exception as exc:  # 다시 못 찾아도 답은 낸다
        print(f"[DEBUG] query_reform 실패: {type(exc).__name__}: {str(exc)[:120]}")
        info["filter"] = "호출 실패"
        return kept, info
    lap("rewrite")
    new_query = parse_query(raw, query)
    if not new_query:
        info["filter"] = "검색어 없음"
        return kept, info
    info["query"] = new_query
    seen = {_pid(b) for b in _blocks(pool)}
    new = [b for b in _blocks(search(new_query)) if _pid(b) not in seen]
    lap("search")
    info["new"] = len(new)
    filtered, status = filter_relevant(question, RAG_HIT_SEP.join(new), model)
    lap("filter")
    info["filter"] = status
    # 거르기가 못 읽거나 '없음'이면 원래 컨텍스트를 그대로 돌려준다 — 그때는 아무것도 더하지 않는다
    added = _blocks(filtered) if re.fullmatch(r"\d+→\d+", status) else []
    info["added"] = [_pid(b) for b in added]
    return RAG_HIT_SEP.join([kept.strip(), *added]) if added else kept, info
