"""본론 항목의 숫자를 그 항목이 인용한 블록과 대조한다 (docs/experiments/list_findings_v2_1026).

왜: list_findings_1023 에서 목록 블록에 결과 문장을 넣자 근거 수치 항목이 7 → 41 로 늘었지만, 숫자를 잘못 옮긴
항목도 생겼다(RAGSmith 46,080 → "약 10만", Multi-LCB 24 → 12). 결론 다시 쓰기의 숫자 검사와 같은 방식으로,
블록에 그대로 없는 숫자가 든 문장을 항목에서 뺀다. 문장을 다 빼야 하면 항목은 그대로 둔다.
줄 끝 공백이 만든 빈 조각이나 마침표 뒤에 따로 선 인용은 문장으로 세지 않는다 — 그것만 남기면 번호와 인용뿐인 항목이 된다.
"""

from __future__ import annotations

import re

from core.llm.answer_fix import _CITED, _find
from core.llm.citation_fix import RAG_HIT_SEP

__all__ = ["check_body_numbers"]

_ITEM = re.compile(r"^(\s*(?:<b>)?\d+\.\s)(.*)$", re.M)
_DOC_N = re.compile(r"\[\s*문서\s*(\d{1,2})\s*\]")
_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
_NOT_TEXT = re.compile(r"\[[^\]\n]*\]|\([^()\n]*\)|<b>[^<\n]*</b>|\*\*[^*\n]*\*\*|<[^>]+>")  # 인용 · 괄호 · 굵은 이름 · 태그


def _norm(text: str) -> str:
    return text.replace("{,}", ",").replace("\\%", "%")


def _blocks(numbered_context: str, doc_ids: dict[int, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for blk in numbered_context.split(RAG_HIT_SEP):
        m = _DOC_N.match(blk.strip())
        if m and int(m.group(1)) in doc_ids:
            k = re.sub(r"v\d+$", "", doc_ids[int(m.group(1))])
            out[k] = out.get(k, "") + "\n" + _norm(blk)
    return out


def _bad(sentence: str, src: str) -> bool:
    text = _YEAR.sub(" ", re.sub(r"<[^>]+>", " ", _CITED.sub(" ", sentence)))
    for tok in _NUM.findall(text):
        if len(tok) == 1:  # 한 자리 수(1편 · 3가지 · GPT-4)는 세지 않는다
            continue
        if not re.search(rf"(?<![\d.,]){re.escape(tok)}(?![\d])", src):
            return True
    return False


def _has_text(sentence: str) -> bool:
    return bool(re.search(r"\w", _NOT_TEXT.sub(" ", sentence)))


def check_body_numbers(answer: str, numbered_context: str, doc_ids: dict[int, str]) -> tuple[str, int]:
    """``(답, 뺀 문장 수)``. 본론 번호 항목에서 인용 블록에 없는 숫자가 든 문장을 뺀다."""
    b, c = _find("본론", answer), _find("결론", answer)
    if not b:
        return answer, 0
    end = c.start() if c and c.start() > b.end() else len(answer)
    by = _blocks(numbered_context, doc_ids)
    dropped = 0

    def fix(m: re.Match[str]) -> str:
        nonlocal dropped
        head, text = m.group(1), m.group(2)
        refs = _CITED.findall(text)
        src = "\n".join(by.get(r, "") for r in refs)
        if not refs or not src:
            return m.group(0)
        sents = re.split(r"(?<=[.!?。])\s+", text)
        keep = [s for s in sents if not _bad(s, src)]
        if len(keep) == len(sents) or not any(_has_text(s) for s in keep):
            return m.group(0)
        out = " ".join(keep)
        missing = [t for r, t in dict(zip(refs, (x.group(0) for x in _CITED.finditer(text)))).items() if r not in _CITED.findall(out)]
        dropped += len(sents) - len(keep)
        return head + out + "".join(missing)

    body = _ITEM.sub(fix, answer[b.end():end])
    return answer[:b.end()] + body + answer[end:], dropped
