"""RAG 답의 결론만 "상황 → 권고 + 근거 결과 [인용]" 으로 다시 쓴다 (docs/experiments/conclusion_rewrite_1021).

왜 따로 쓰나: 본론이 논문의 방법만 설명하고 결론이 상투어로 끝났다. 근거(초록의 결과)는 컨텍스트에
있는데 결과를 뽑아 권고로 묶지 않는다. 답변 프롬프트의 형식 지시는 이 모델이 무시해 왔다
(template_collapse_1006) → 답을 낸 뒤 결론만 따로 묻고, 숫자를 문서와 대조해 통과할 때만 바꾼다.
"""

from __future__ import annotations

import re

from core.llm.answer_fix import _CITED, _find
from core.llm.citation_fix import RAG_HIT_SEP, fix_citations
from core.llm.lang_guard import hanzi_count

__all__ = ["cited_blocks", "ids_to_doc_refs", "check_conclusion", "replace_conclusion", "rewrite_conclusion"]

SYSTEM = "너는 논문 검색 답변의 결론을 고쳐 쓰는 편집자다. 참고 문서에 적힌 내용만 쓴다."

PROMPT = """[질문]
{question}

[참고 문서]
{blocks}

[지금 답의 본론]
{body}

[할 일]
위 본론과 참고 문서를 바탕으로 **결론만** 2~4문장으로 새로 써라.
- 문장마다: 어떤 상황·조건이면 → 무엇이 낫다/어떻다 + 그 근거가 된 결과 + 인용 [문서 N].
- 결과는 참고 문서에 적힌 것만 쓴다. 수치는 문서에 적힌 숫자를 그대로 옮기고 계산하지 마라(예: "62-64%에서 72%로").
- 근거가 약하면(평가 규모가 작거나 정성 평가뿐이면) 그렇다고 쓴다.
- 본론을 되풀이하지 말고, 질문한 사람이 무엇을 고르면 되는지 알 수 있게 쓴다.
- 한국어로. 머리말·제목·번호 없이 결론 문장만 출력한다."""

_DOC_N = re.compile(r"\[\s*문서\s*(\d{1,2})\s*\]")
_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_BLOCK_MAX = 2500


def _bare(pid: str) -> str:
    return re.sub(r"v\d+$", "", pid)


def cited_blocks(answer: str, numbered_context: str, doc_ids: dict[int, str]) -> dict[int, str]:
    """본론이 인용한 논문의 ``{문서 번호: 블록}``. 블록은 ``[문서 N]`` 라벨을 단 그대로."""
    b, c = _find("본론", answer), _find("결론", answer)
    body = answer[b.end():c.start()] if b and c and c.start() > b.end() else ""
    ids = set(_CITED.findall(body))
    blocks = {}
    for blk in numbered_context.split(RAG_HIT_SEP):
        m = _DOC_N.match(blk.strip())
        if m and _bare(doc_ids.get(int(m.group(1)), "")) in ids:
            blocks[int(m.group(1))] = blk.strip()[:_BLOCK_MAX]
    return blocks


def ids_to_doc_refs(text: str, blocks: dict[int, str]) -> str:
    """본론 인용 형식을 따라 쓴 ``[2605.15100v1]`` 을 ``[문서 N]`` 으로 — 1차에서 탈락의 대부분이었다 (§5)."""
    first = {}
    for n, blk in sorted(blocks.items()):
        for pid in _CITED.findall(blk[:300]):
            first.setdefault(pid, n)
    return _CITED.sub(lambda m: f"[문서 {first[m.group(1)]}]" if m.group(1) in first else m.group(0), text)


def check_conclusion(text: str, blocks: dict[int, str]) -> str:
    """통과면 "", 아니면 탈락 사유. 숫자는 그 결론이 인용한 블록에 그대로 있어야 한다(계산한 값 금지)."""
    refs = {int(n) for n in _DOC_N.findall(text)}
    if not refs:
        return "인용 없음"
    if not 40 <= len(text) <= 700:
        return "길이"
    if hanzi_count(text):
        return "한자"
    if refs - blocks.keys():
        return "본론 밖 문서 인용"
    src = "\n".join(blocks[n] for n in refs)
    for tok in _NUM.findall(_DOC_N.sub("", text)):
        if not re.search(rf"(?<![\d.,]){re.escape(tok)}(?![\d])", src):
            return f"문서 밖 숫자 {tok}"
    return ""


def replace_conclusion(answer: str, text: str) -> str:
    c = _find("결론", answer)
    return answer[:c.end()] + "\n" + text.strip() + "\n" if c else answer


def rewrite_conclusion(
    answer: str, question: str, numbered_context: str, doc_ids: dict[int, str], model: str
) -> tuple[str, str]:
    """``(답, 상태)``. 상태: "바꿈" · "대상 아님" · 탈락 사유 · "호출 실패". 바꾸지 않으면 답 그대로."""
    blocks = cited_blocks(answer, numbered_context, doc_ids)
    if len(blocks) < 2 or not _find("결론", answer):
        return answer, "대상 아님"
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    b, c = _find("본론", answer), _find("결론", answer)
    prompt = PROMPT.format(
        question=question, blocks=RAG_HIT_SEP.join(blocks.values()), body=answer[b.end():c.start()].strip()
    )
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=400))
    try:
        text = str(llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)]).content or "").strip()
    except Exception as exc:  # 결론을 못 바꿔도 답은 낸다
        print(f"[DEBUG] conclusion_rewrite 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return answer, "호출 실패"
    text = ids_to_doc_refs(text, blocks)
    why = check_conclusion(text, blocks)
    if why:
        return answer, why
    text, _ = fix_citations(text, numbered_context, doc_ids=doc_ids)
    return replace_conclusion(answer, text), "바꿈"
