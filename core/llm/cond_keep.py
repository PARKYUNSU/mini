"""질문 조건 보존 (RAG_COND_KEEP, docs/experiments/cond_keep_1118 — 사용자 3차 피드백 S2).

27B 한 번으로 ① 질문의 조건(언어 · 문서 유형 · 분야 · 비교 대상)을 뽑고 ② 각 조건을 직접 다룬 문서 번호를 고른다.
어느 문서도 다루지 않은 조건은 서론 첫 문장에 "…를 직접 다룬 연구는 찾지 못했다" 로 밝힌다.
"""
from __future__ import annotations

import json
import os
import re

PROMPT = """사용자 질문과 검색된 논문 목록이 있다.
1) 질문이 연구에 거는 조건을 뽑아라. 조건 종류는 "언어"(예: 한국어), "문서 유형"(예: 지속가능경영보고서, 기준 문서, 회의록), "분야"(예: 금융, 의료), "비교 대상"(질문이 둘 이상을 비교하라고 할 때 그 대상들, 예: "BM25 · 밀집 검색") 뿐이다. 질문에 명시된 것만, 질문에 쓰인 말 그대로 적는다. 일반적인 주제(RAG, LLM 평가 등)는 조건이 아니다. 조건이 없으면 빈 목록.
2) 조건마다 그 조건을 직접 다룬 논문 번호를 고른다. 언어 조건이면 그 언어를 실험에 포함한 논문, 비교 대상이면 그 대상들을 직접 비교한 논문, 문서 유형이면 바로 그 유형의 문서를 다룬 논문이다(비슷한 다른 유형은 아니다 — 예: 법령 · 판례 문서는 기업의 기준 문서가 아니고, 뉴스는 공시 문서가 아니다). 초록에 근거가 없으면 고르지 않는다. 없으면 빈 목록.

질문: {q}

논문:
{docs}

JSON 으로만 답하라: {{"조건": [{{"종류": "언어", "값": "한국어", "다룬 논문": [2]}}]}}"""
SCHEMA = {"type": "object", "properties": {"조건": {"type": "array", "items": {"type": "object", "properties": {
    "종류": {"type": "string", "enum": ["언어", "문서 유형", "분야", "비교 대상"]}, "값": {"type": "string"},
    "다룬 논문": {"type": "array", "items": {"type": "integer"}}}, "required": ["종류", "값", "다룬 논문"]}}},
    "required": ["조건"]}


def cond_keep_active() -> bool:
    return os.getenv("RAG_COND_KEEP", "0").strip() == "1"


def judge_conditions(question: str, rag_context: str) -> list[dict] | None:
    """[{종류, 값, 다룬 논문: [문서 번호]}]. 실패하면 None."""
    import requests

    from core.config.agent_config import ollama_kwargs
    from core.llm.doc_judge import doc_blocks

    blocks = doc_blocks(rag_context, limit=2000)  # 언어 · 문서 유형은 초록 뒤쪽에 나오기도 한다(K13 QTT-RAG)
    if not blocks:
        return None
    kw = ollama_kwargs()
    docs = "\n\n".join(f"[{n}] {text}" for n, text in blocks)
    try:
        r = requests.post(f"{kw['base_url']}/api/chat", json={
            "model": os.getenv("RAG_DOC_JUDGE_MODEL", "qwen3.6:27b-q4_K_M"), "stream": False, "think": False,
            "format": SCHEMA, "keep_alive": kw["keep_alive"], "options": {"temperature": 0, "num_ctx": 8192},
            "messages": [{"role": "user", "content": PROMPT.format(q=question, docs=docs)}]}, timeout=120)
        conds = json.loads(r.json()["message"]["content"])["조건"]
    except Exception as e:  # noqa: BLE001 — 실패하면 조건 처리 없이 간다
        print(f"[WARN] cond_keep 실패: {e}")
        return None
    nums = {n for n, _ in blocks}
    # 질문에 그대로 있는 값만 (지어낸 조건 막기)
    return [{**c, "다룬 논문": [k for k in c["다룬 논문"] if k in nums]} for c in conds
            if c.get("값") and all(w in question for w in re.split(r"\s*[·,/]\s*|\s+", c["값"].strip()) if w)]


def missing_conditions(conds: list[dict] | None) -> list[dict]:
    return [c for c in conds or [] if not c["다룬 논문"]]


def missing_sentence(missing: list[dict]) -> str:
    if not missing:
        return ""
    parts = []
    for c in missing:
        v = c["값"].strip()
        parts.append(f"'{v}' 비교를 직접 다룬 연구" if c["종류"] == "비교 대상" else f"'{v}' 조건을 직접 다룬 연구")
    return " · ".join(parts) + "는 제공된 문서에서 찾지 못했고, 아래는 그 조건을 벗어나 관련된 연구입니다."


def add_missing_to_intro(answer: str, sentence: str) -> tuple[str, int]:
    """서론 머리 바로 다음 줄에 조건 문장을 넣는다. 이미 같은 값이 서론에 '찾지 못' 과 함께 있으면 그대로."""
    if not sentence:
        return answer, 0
    m = re.search(r"^[ \t#*]*서론[ \t*]*$\n?", answer or "", re.M)
    if not m:
        return sentence + "\n" + (answer or ""), 1
    return answer[:m.end()] + sentence + "\n" + answer[m.end():], 1


def keep_terms_note(conds: list[dict] | None) -> str:
    """질문의 문서 유형 · 분야 표현을 답에서 바꾸지 말라는 한 줄 (W04 '기준 문서' → '법령 문서')."""
    vals = [c["값"].strip() for c in conds or [] if c["종류"] in ("문서 유형", "분야")]
    if not vals:
        return ""
    q = ", ".join(f"'{v}'" for v in vals)
    return f"\n- 질문의 표현 {q} 은(는) 답에서도 그대로 쓴다. 문서가 다른 유형(예: 법령 · 판례)을 다뤘으면 그 유형 이름은 그 논문 설명에만 쓰고, 질문의 표현을 그것으로 바꾸지 않는다.\n"


_COMBINED_TAIL = """
이어서, 질문이 연구에 거는 조건도 뽑아라. 조건 종류는 "언어"(예: 한국어), "문서 유형"(예: 지속가능경영보고서, 기준 문서, 회의록), "분야"(예: 금융, 의료), "비교 대상"(질문이 둘 이상을 비교하라고 할 때 그 대상들) 뿐이다. 질문에 명시된 것만, 질문에 쓰인 말 그대로 적는다. 일반적인 주제(RAG, LLM 평가 등)는 조건이 아니다. 조건이 없으면 빈 목록.
조건마다 그 조건을 직접 다룬 논문 번호를 고른다. 언어 조건이면 그 언어를 실험에 포함한 논문, 비교 대상이면 그 대상들을 직접 비교한 논문, 문서 유형이면 바로 그 유형의 문서를 다룬 논문이다(비슷한 다른 유형은 아니다 — 예: 법령 · 판례 문서는 기업의 기준 문서가 아니고, 뉴스는 공시 문서가 아니다). 초록에 근거가 없으면 고르지 않는다.

JSON 으로만 답하라: {{"판정": [{{"번호": 1, "관련도": "직접|부분|무관"}}, ...], "조건": [{{"종류": "언어", "값": "한국어", "다룬 논문": [2]}}]}}"""


def judge_docs_and_conditions(question: str, rag_context: str):
    """문서 판정(doc_judge 와 같은 지시 · 같은 초록 900자)과 조건 판정을 27B 한 번에 (cond_keep_1118 §5).

    반환: (labels {문서 번호: D/P/N} | None, conds | None). 실패하면 (None, None) — 호출 쪽은 따로 부른다.
    """
    import requests

    from core.config.agent_config import ollama_kwargs
    from core.llm.doc_judge import _LAB, PROMPT as DOC_PROMPT, SCHEMA as DOC_SCHEMA, doc_blocks

    blocks = doc_blocks(rag_context)
    if not blocks:
        return None, None
    docs = "\n\n".join(f"[{i}] {text}" for i, (_, text) in enumerate(blocks, 1))
    head = DOC_PROMPT.split("JSON 으로만 답하라")[0].rstrip()
    schema = {"type": "object", "properties": {"판정": DOC_SCHEMA["properties"]["판정"], "조건": SCHEMA["properties"]["조건"]},
              "required": ["판정", "조건"]}
    kw = ollama_kwargs()
    try:
        r = requests.post(f"{kw['base_url']}/api/chat", json={
            "model": os.getenv("RAG_DOC_JUDGE_MODEL", "qwen3.6:27b-q4_K_M"), "stream": False, "think": False,
            "format": schema, "keep_alive": kw["keep_alive"], "options": {"temperature": 0, "num_ctx": 8192},
            "messages": [{"role": "user", "content": head.format(q=question, docs=docs) + "\n" + _COMBINED_TAIL.format()}]},
            timeout=150)
        out = json.loads(r.json()["message"]["content"])
        got = {x["번호"]: x["관련도"] for x in out["판정"]}
        conds = out["조건"]
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] doc+cond 판정 실패: {e}")
        return None, None
    if len(got) < len(blocks):
        return None, None
    labels = {n: _LAB.get(got.get(i), "P") for i, (n, _) in enumerate(blocks, 1)}
    idx2num = {i: n for i, (n, _) in enumerate(blocks, 1)}
    conds = [{**c, "다룬 논문": [idx2num[k] for k in c.get("다룬 논문", []) if k in idx2num]} for c in conds
             if c.get("값") and all(w in question for w in re.split(r"\s*[·,/]\s*|\s+", c["값"].strip()) if w)]
    return labels, conds
