"""본론 항목을 논문마다 따로 다시 쓴다 (docs/experiments/item_rewrite_1114).

왜: 답 틀로 "방법 → 결과 → 조건" 을 시켜도 v13 은 한 번의 답에서 여러 논문을 1–2 문장으로 쓴다(depth_1114).
컨텍스트에는 초록 전체가 이미 있으므로, 답을 낸 뒤 항목마다 그 논문 블록 하나만 주고 다시 쓰게 한다.
숫자가 블록에 그대로 없거나 짧아지면 원래 항목을 둔다.
"""

from __future__ import annotations

import os
import re

from core.llm.answer_fix import _CITED, _find
from core.llm.body_numbers import _ITEM, _bad, _blocks
from core.llm.lang_guard import hanzi_count

__all__ = ["rewrite_items", "check_item"]

SYSTEM = "너는 논문 검색 답변의 본론 항목을 고쳐 쓰는 편집자다. 참고 문서에 적힌 내용만 쓴다."

PROMPT = """[질문]
{question}

[참고 논문]
{block}

[지금 항목]
{item}

[할 일]
이 논문 하나를 질문에 맞춰 3~4문장으로 다시 써라.
1) 무엇을 제안하거나 조사했는지
2) 핵심 결과 — 문서에 적힌 숫자·비교를 그대로 옮긴다(계산하지 마라)
3) 평가 대상·조건·한계 — 문서에 있을 때만
4) 질문과 어떻게 이어지는지
- 문서에 없는 내용은 쓰지 마라.
- 한국어로. 논문 이름·번호·인용·머리말 없이 문장만 출력한다."""

_NAME = re.compile(r"^((?:<b>[^<\n]+</b>|\*\*[^*\n]+\*\*)\s*[:：]?\s*)")
_BLOCK_MAX = 2500


def check_item(text: str, old: str, src: str) -> str:
    """통과면 "", 아니면 탈락 사유."""
    if not 80 <= len(text) <= 700:
        return "길이"
    if hanzi_count(text):
        return "한자"
    if len(text) <= len(_CITED.sub("", old).strip()):
        return "짧아짐"
    for s in re.split(r"(?<=[.!?。])\s+", text):
        if _bad(s, src):
            return "문서 밖 숫자"
    return ""


def rewrite_items(
    answer: str, question: str, numbered_context: str, doc_ids: dict[int, str], model: str
) -> tuple[str, dict[str, int]]:
    """``(답, 상태별 항목 수)``. 바꾸지 못한 항목은 그대로 둔다."""
    stats: dict[str, int] = {}
    b, c = _find("본론", answer), _find("결론", answer)
    if not b:
        return answer, stats
    end = c.start() if c and c.start() > b.end() else len(answer)
    by = _blocks(numbered_context, doc_ids)
    cap = int(os.getenv("RAG_ITEM_REWRITE_MAX", "4") or 4)
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=400))
    done = 0

    def fix(m: re.Match[str]) -> str:
        nonlocal done
        head, text = m.group(1), m.group(2)
        refs = set(_CITED.findall(text))
        nxt = m.string[m.end():].lstrip("\n").split("\n", 1)[0] if m.string[m.end():m.end() + 1] == "\n" and not m.string[m.end():].startswith("\n\n") else ""
        multiline = bool(nxt.strip()) and not _ITEM.match(nxt) and not nxt.lstrip().startswith("<b>")
        if len(refs) != 1 or not by.get(next(iter(refs))) or multiline:
            stats["대상 아님"] = stats.get("대상 아님", 0) + 1
            return m.group(0)
        if done >= cap:
            stats["상한"] = stats.get("상한", 0) + 1
            return m.group(0)
        done += 1
        src = by[next(iter(refs))]
        name = (_NAME.match(text) or [""])[0]
        old = text[len(name):]
        try:
            msg = PROMPT.format(question=question, block=src.strip()[:_BLOCK_MAX], item=_CITED.sub("", old).strip())
            new = str(llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=msg)]).content or "").strip()
        except Exception as exc:  # 항목을 못 바꿔도 답은 낸다
            print(f"[DEBUG] item_rewrite 실패: {type(exc).__name__}: {str(exc)[:120]}")
            stats["호출 실패"] = stats.get("호출 실패", 0) + 1
            return m.group(0)
        new = re.sub(r"\s+", " ", _CITED.sub("", re.sub(r"\[\s*문서\s*\d+\s*\]", "", new))).strip()
        why = check_item(new, old, src)
        if why:
            stats[why] = stats.get(why, 0) + 1
            return m.group(0)
        stats["바꿈"] = stats.get("바꿈", 0) + 1
        return f"{head}{name}{new} {_CITED.search(text).group(0)}"

    body = _ITEM.sub(fix, answer[b.end():end])
    return answer[:b.end()] + body + answer[end:], stats
