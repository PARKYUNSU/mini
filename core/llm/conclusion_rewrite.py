"""RAG 답의 결론만 "상황 → 권고 + 근거 결과 [인용]" 으로 다시 쓴다 (docs/experiments/conclusion_rewrite_1021).

왜 따로 쓰나: 본론이 논문의 방법만 설명하고 결론이 상투어로 끝났다. 근거(초록의 결과)는 컨텍스트에
있는데 결과를 뽑아 권고로 묶지 않는다. 답변 프롬프트의 형식 지시는 이 모델이 무시해 왔다
(template_collapse_1006) → 답을 낸 뒤 결론만 따로 묻고, 숫자를 문서와 대조해 통과할 때만 바꾼다.
"""

from __future__ import annotations

import os
import re

from core.llm.answer_fix import _CITED, _find
from core.llm.citation_fix import RAG_HIT_SEP, fix_citations
from core.llm.lang_guard import hanzi_count

__all__ = ["cited_blocks", "extract_findings", "ids_to_doc_refs", "check_conclusion", "replace_conclusion", "rewrite_conclusion"]

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

# v2 (§8): 본론을 빼고 논문별 결과 · 대상 문장을 규칙으로 뽑아 준다 — v1 은 본론을 되풀이했다.
PROMPT_V2 = """[질문]
{question}

[논문별 핵심 — 초록에서 뽑은 원문 문장]
{findings}

[할 일]
위 논문들의 **결과**를 비교해 질문에 대한 결론을 2~4문장으로 써라.
- 논문 간 결과가 문서 유형·데이터·조건에 따라 같은지, 갈리는지 짚고, 질문에 대한 판단을 내린다.
- 문장마다 근거 논문을 [문서 N] 으로 인용한다.
- 수치는 원문 숫자를 그대로 옮기고 계산하지 마라(예: "62-64%에서 72%로").
- 대상이 좁으면(특정 도메인·비공개 데이터·소규모·정성 평가) 그 점을 밝힌다.
- 각 논문의 방법을 다시 설명하지 마라.
- 한국어로. 머리말·제목·번호 없이 결론 문장만 출력한다."""

_RESULT_RE = re.compile(
    r"outperform|improv|reduc|increas|achiev|surpass|benefit|cost-effective|limit|degrad|drop|cliff|"
    r"match|better|worse|gain|lower|higher|faster|slower|show|find|found|reveal|demonstrat",
    re.I,
)
_RESULT_NUM = re.compile(r"\d+(?:\.\d+)?\s*(?:%|x|×|times|배|points?)|from \d|\(\d|\d+\s*(?:vs\.?|→)", re.I)
# 대상 문장: 평가 데이터를 말하는 문장을 먼저, 없으면 도메인을 말하는 문장
_DOMAIN_RES = (
    re.compile(r"dataset|corpus|corpora|benchmark|evaluat\w* on|we evaluate|experiments? on", re.I),
    re.compile(r"domain|documents|industr|enterprise|proprietary|real-world", re.I),
)

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


def extract_findings(block: str) -> tuple[list[str], str]:
    """블록에서 ``(결과 문장 ≤3, 대상 문장)``. 머리(번호 · 거리 · 날짜 · ID 제목) 뒤 본문만 본다."""
    lines = block.split("\n")
    k = next((i for i, l in enumerate(lines) if re.match(r"\[\d{4}\.\d{4,5}", l)), -1)
    text = re.sub(r"\[초록\]|#+\s*\**abstract\**", " ", "\n".join(lines[k + 1:]), flags=re.I)
    sents = [x.strip() for x in re.split(r"(?<!vs\.)(?<!al\.)(?<!e\.g\.)(?<=[.!?])\s+", re.sub(r"\s+", " ", text)) if len(x.strip()) > 20]
    # 첫 문장은 배경이라 뺀다. 결과 수치가 있는 문장 > 결과 동사 문장, 같은 점수면 뒤쪽(초록 끝에 결과가 많다)
    score = {i: 2 * bool(_RESULT_NUM.search(x)) + bool(_RESULT_RE.search(x)) for i, x in enumerate(sents) if i}
    top = sorted((i for i in score if score[i]), key=lambda i: (-score[i], -i))[:3]
    res = [sents[i] for i in sorted(top)] or sents[-2:]
    dom = next((x for r in _DOMAIN_RES for x in sents if r.search(x)), "")
    return res, dom


def _findings_text(blocks: dict[int, str]) -> str:
    out = []
    for n, blk in blocks.items():
        title = next((l for l in blk.split("\n") if re.match(r"\[\d{4}\.\d{4,5}", l)), "")
        res, dom = extract_findings(blk)
        out.append(f"[문서 {n}] {title}\n대상: {dom or '(초록에 없음)'}\n결과: " + " / ".join(res))
    return "\n\n".join(out)


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
    if os.getenv("RAG_CONCLUSION_PROMPT", "v1").strip() == "v2":
        prompt = PROMPT_V2.format(question=question, findings=_findings_text(blocks))
    else:
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
