"""답 칸 검사기 (RAG_SLOT_FILL, docs/experiments/slot_fill_1124 — 5차 피드백 U2 일부).

왜: 27B 판정대로 칸 틀(RAG_AGG_SLOTS)을 줘도 v13 이 칸을 덜 채우거나(W07 5차: 4칸 중 1칸, K13: 4칸 중 2칸)
같은 논문을 한 항목 안에서 이름부터 다시 쓴다(W07 "**Auto‑ARGUE** …[ID] **Auto‑ARGUE** …[ID]").
- dedupe_repeated_heads: 한 항목 안에서 같은 이름 머리가 다시 나오면 그 머리만 지운다(내용은 둔다 → 항목 다시 쓰기가 한 편으로 정리).
- fill_missing_slots: 칸을 받은 직접 · 부분 논문 중 본론에 인용되지 않은 논문마다 그 논문 블록 하나로 항목을 만들어 결론 앞에 붙인다.
  빠진 칸이 없으면 LLM 을 부르지 않는다.
"""
from __future__ import annotations

import os
import re

from core.llm.answer_fix import _CITED, _find

_ITEM_LINE = re.compile(r"^(\s*(?:<b>)?\d+\.\s)(.*)$")
_HEADNAME = re.compile(r"(\*\*[^*\n]+\*\*|<b>[^<\n]+</b>)(\s*\(관련 연구\))?\s*[:：]?\s*")


def slot_fill_active() -> bool:
    return os.getenv("RAG_SLOT_FILL", "0").strip() == "1"


def _body_span(answer: str) -> tuple[int, int] | None:
    b, c = _find("본론", answer), _find("결론", answer)
    if not b:
        return None
    return b.end(), (c.start() if c and c.start() > b.end() else len(answer))


def dedupe_repeated_heads(answer: str) -> tuple[str, int]:
    """한 항목 안에서 인용 뒤에 항목 머리와 같은 굵은 이름이 다시 나오면 그 이름 머리를 지운다."""
    span = _body_span(answer)
    if not span:
        return answer, 0
    lines, n = answer[span[0]:span[1]].split("\n"), 0
    for k, line in enumerate(lines):
        m = _ITEM_LINE.match(line)
        h = _HEADNAME.match(m.group(2)) if m else None
        if not h:
            continue
        name = h.group(1)
        rest = m.group(2)[h.end():]
        pat = re.compile(r"(\]\s*)" + re.escape(name) + r"(?:\s*\(관련 연구\))?\s*[:：]?\s*")
        new, c = pat.subn(r"\1", rest)
        if c:
            lines[k] = m.group(1) + m.group(2)[:h.end()] + new
            n += c
    if not n:
        return answer, 0
    return answer[:span[0]] + "\n".join(lines) + answer[span[1]:], n


def expected_ids(labels: dict[int, str], doc_ids: dict[int, str]) -> list[tuple[str, str]]:
    """칸을 받은 (논문 ID, 라벨) — agg_slots_template 과 같은 규칙(직접 · 부분, 앞 5편)."""
    keep = [n for n in sorted(labels) if labels[n] in ("D", "P")][:5]
    return [(re.sub(r"v\d+$", "", str(doc_ids[n])), labels[n]) for n in keep if n in doc_ids]


def missing_ids(answer: str, labels: dict[int, str], doc_ids: dict[int, str]) -> list[tuple[str, str]]:
    span = _body_span(answer)
    if not span:
        return []
    cited = set(_CITED.findall(answer[span[0]:span[1]]))
    return [(pid, lab) for pid, lab in expected_ids(labels, doc_ids) if pid not in cited]


def fill_missing_slots(
    answer: str, question: str, rag_context: str, labels: dict[int, str], doc_ids: dict[int, str], model: str
) -> tuple[str, dict[str, int]]:
    """``(답, 상태별 수)``. 빠진 칸마다 항목 하나를 만들어 결론 앞에 붙인다. 못 만든 칸은 비워 둔다."""
    stats: dict[str, int] = {}
    miss = missing_ids(answer, labels, doc_ids)
    span = _body_span(answer)
    if not miss or not span:
        return answer, stats
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs
    from core.llm.body_numbers import _blocks
    from core.llm.format_fix import _REF_TITLE, _short_title, term_rule
    from core.llm.item_rewrite import _BLOCK_MAX, PROMPT, SYSTEM, check_item

    by = _blocks(rag_context, doc_ids)
    titles = dict(_REF_TITLE.findall(rag_context or ""))
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=400))
    bold = "<b>" in answer[span[0]:span[1]] and "**" not in answer[span[0]:span[1]]
    new_items = []
    for pid, lab in miss:
        src = by.get(pid)
        if not src:
            stats["블록 없음"] = stats.get("블록 없음", 0) + 1
            continue
        try:
            msg = PROMPT.format(question=question, block=src.strip()[:_BLOCK_MAX], item="(아직 없음)", term_rule=term_rule())
            text = str(llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=msg)]).content or "").strip()
        except Exception as exc:  # 칸을 못 채워도 답은 낸다
            print(f"[DEBUG] slot_fill 실패: {type(exc).__name__}: {str(exc)[:120]}")
            stats["호출 실패"] = stats.get("호출 실패", 0) + 1
            continue
        text = re.sub(r"\s+", " ", _CITED.sub("", re.sub(r"\[\s*문서\s*\d+\s*\]", "", text))).strip()
        why = check_item(text, "", src)
        if why:
            stats[why] = stats.get(why, 0) + 1
            continue
        name = _short_title(titles.get(pid, pid))
        name = f"<b>{name}</b>" if bold else f"**{name}**"
        tag = " (관련 연구)" if lab == "P" else ""
        new_items.append(f"0. {name}{tag}: {text} [{pid}]")
        stats["채움"] = stats.get("채움", 0) + 1
    if not new_items:
        return answer, stats
    body = answer[span[0]:span[1]].rstrip("\n")
    return answer[:span[0]] + body + "\n" + "\n".join(new_items) + "\n\n" + answer[span[1]:].lstrip("\n"), stats


def drop_n_active() -> bool:
    return os.getenv("RAG_DROP_N_CITES", "0").strip() == "1"


def drop_n_cited(answer: str, labels: dict[int, str], doc_ids: dict[int, str]) -> tuple[str, int]:
    """27B 가 무관(N)으로 판정한 논문만 인용한 본론 항목 · 결론 문장을 지운다 (6차 W03: 칸 틀에 없는 항목을 v13 이 더 씀).

    직접 · 부분 논문도 같이 인용한 항목 · 문장은 둔다. ``(답, 지운 수)``.
    """
    n_ids = {re.sub(r"v\d+$", "", str(doc_ids[k])) for k, v in labels.items() if v == "N" and k in doc_ids}
    span = _body_span(answer)
    if not n_ids or not span:
        return answer, 0
    only_n = lambda s: bool(_CITED.findall(s)) and set(_CITED.findall(s)) <= n_ids
    lines = answer[span[0]:span[1]].split("\n")
    keep = [ln for ln in lines if not (_ITEM_LINE.match(ln) and only_n(ln))]
    n = len(lines) - len(keep)
    tail = answer[span[1]:]
    c = _find("결론", tail)
    if c:
        sents = re.split(r"(?<=[.!?。\]])\s+(?=\S)", tail[c.end():])
        ks = [s for s in sents if not only_n(s)]
        n += len(sents) - len(ks)
        tail = tail[:c.end()] + " ".join(ks)
    return (answer[:span[0]] + "\n".join(keep) + tail, n) if n else (answer, 0)
