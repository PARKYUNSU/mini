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


_GENERIC = {"보고서", "문서", "논문", "데이터", "텍스트", "자료", "글", "연구"}  # 혼자서는 한정 조건이 아님(W01 '보고서')


def missing_conditions(conds: list[dict] | None) -> list[dict]:
    return [c for c in conds or [] if not c["다룬 논문"] and c["값"].strip() not in _GENERIC]


def missing_sentence(missing: list[dict]) -> str:
    if not missing:
        return ""
    parts = []
    for c in missing:
        v = c["값"].strip()
        parts.append(f"'{v}' 비교를 직접 다룬 연구" if c["종류"] == "비교 대상" else f"'{v}' 조건을 직접 다룬 연구")
    return " · ".join(parts) + "는 제공된 문서에서 찾지 못했고, 아래는 그 조건을 벗어나 관련된 연구입니다."


_LEAD_PARTIAL = "질문을 직접 다룬 연구는 찾지 못했고, 가장 가까운 연구는 아래와 같습니다."
_LEAD_NONE = "제공된 문서에는 질문이 찾는 연구가 없습니다."


def add_missing_to_intro(answer: str, sentence: str) -> tuple[str, int]:
    """서론 머리에 조건 문장을 넣는다. 판정 안내 문장이 이미 있으면 한 문장으로 합친다(4차 피드백 T3)."""
    if not sentence:
        return answer, 0
    cond = sentence.split("는 제공된 문서에서 찾지 못했고")[0]  # "'한국어' 조건을 직접 다룬 연구 · …"
    if _LEAD_PARTIAL in (answer or ""):
        return answer.replace(_LEAD_PARTIAL, f"{cond}는 찾지 못했고, 가장 가까운 연구는 아래와 같습니다.", 1), 1
    if _LEAD_NONE in (answer or ""):
        return answer.replace(_LEAD_NONE, f"{cond}를 포함해 질문이 찾는 연구는 제공된 문서에 없습니다.", 1), 1
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


_OTHER_TYPE = re.compile(
    r"(이러한|이런|그러한|이와 같은)((?:\s+[가-힣]*[한운은는긴])*)\s+"
    r"(법적|법률|법령|판례|규제|공시|계약|의료|금융|뉴스|학술|기술)\s*(텍스트|문서|자료)")


def restore_cond_terms(answer: str, conds: list[dict] | None) -> tuple[str, int]:
    """서론 · 결론이 지시어로 질문의 문서 유형을 받으면서 다른 유형 이름을 붙이면 질문 표현으로 되돌린다 (5차 피드백 U3).

    W04: 질문 '기준 문서' → 서론 "이러한 긴 법적 텍스트". 본론 항목(번호 줄)은 논문 설명이라 건드리지 않는다.
    문서 유형 조건이 하나일 때만 (둘 이상이면 어느 쪽인지 모름).
    shortcut: 지시어 + 아는 유형 낱말만 잡는다 — 다른 꼴의 바꿔 부르기가 실사용에서 보이면 넓힌다.
    """
    vals = [c["값"].strip() for c in conds or [] if c.get("종류") == "문서 유형" and c.get("값")]
    if len(vals) != 1 or not answer:
        return answer, 0
    v, flat = vals[0], vals[0].replace(" ", "")
    n = 0

    def sub(m):
        nonlocal n
        if m.group(3) in flat:
            return m.group(0)
        n += 1
        return f"{m.group(1)}{m.group(2)} {v}"

    lines = [ln if re.match(r"\s*\d+\.", ln) else _OTHER_TYPE.sub(sub, ln) for ln in answer.split("\n")]
    return "\n".join(lines), n


_COND_TAIL = """

위 판정은 이미 받았다. 이번에는 판정 대신, 질문이 연구에 거는 조건을 뽑아라. 조건 종류는 "언어"(예: 한국어), "문서 유형"(예: 지속가능경영보고서, 기준 문서, 회의록), "분야"(예: 금융, 의료), "비교 대상"(질문이 둘 이상을 비교하라고 할 때 그 대상들) 뿐이다. 질문에 명시된 것만, 질문에 쓰인 말 그대로 적는다. 일반적인 주제(RAG, LLM 평가 등)는 조건이 아니다. 조건이 없으면 빈 목록.
조건마다 그 조건을 직접 다룬 논문 번호를 고른다. 언어 조건이면 그 언어를 실험에 포함한 논문, 비교 대상이면 그 대상들을 직접 비교한 논문, 문서 유형이면 바로 그 유형의 문서를 다룬 논문이다(비슷한 다른 유형은 아니다 — 예: 법령 · 판례 문서는 기업의 기준 문서가 아니고, 뉴스는 공시 문서가 아니다). 초록에 근거가 없으면 고르지 않는다.

JSON 으로만 답하라: {"조건": [{"종류": "언어", "값": "한국어", "다룬 논문": [2]}]}"""


def judge_docs_and_conditions(question: str, rag_context: str):
    """문서 판정과 조건 판정을 27B 두 번에 나눠 부른다 (cond_keep_1118 §8, 5차 피드백).

    한 호출로 합쳤더니(§5) 같은 문서의 판정 라벨이 바뀌었다(W02 · W05 · W08). 이제 ① 문서 판정은 `judge_docs`
    그대로(라벨이 단독 판정과 같음), ② 조건 판정은 ①의 프롬프트를 글자 그대로 앞에 두고 조건 지시만 덧붙여
    Ollama 프롬프트 캐시가 문서 부분을 다시 읽지 않게 한다.
    반환: (labels | None, conds | None).
    """
    import requests

    from core.config.agent_config import ollama_kwargs
    from core.llm.doc_judge import PROMPT as DOC_PROMPT, doc_blocks, judge_docs

    labels = judge_docs(question, rag_context)
    if labels is None:
        return None, None
    blocks = doc_blocks(rag_context)
    docs = "\n\n".join(f"[{i}] {text}" for i, (_, text) in enumerate(blocks, 1))
    kw = ollama_kwargs()
    try:
        r = requests.post(f"{kw['base_url']}/api/chat", json={
            "model": os.getenv("RAG_DOC_JUDGE_MODEL", "qwen3.6:27b-q4_K_M"), "stream": False, "think": False,
            "format": SCHEMA, "keep_alive": kw["keep_alive"], "options": {"temperature": 0, "num_ctx": 8192},
            "messages": [{"role": "user", "content": DOC_PROMPT.format(q=question, docs=docs) + _COND_TAIL}]},
            timeout=150)
        conds = json.loads(r.json()["message"]["content"])["조건"]
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] cond 판정 실패: {e}")
        return labels, None
    idx2num = {i: n for i, (n, _) in enumerate(blocks, 1)}
    conds = [{**c, "다룬 논문": [idx2num[k] for k in c.get("다룬 논문", []) if k in idx2num]} for c in conds
             if c.get("값") and all(w in question for w in re.split(r"\s*[·,/]\s*|\s+", c["값"].strip()) if w)]
    return labels, conds
