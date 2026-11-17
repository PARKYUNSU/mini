"""'없음' 판정을 문서별 직접/부분/무관 판정 집계로 (RAG_JUDGE_AGG, docs/experiments/judge_agg_1117).

답에 들어가는 문서마다 큰 판정 모델(기본 27B, 생각 끔)이 직접 · 부분 · 무관을 고르고,
직접 ≥ 1 → (a) · 부분만 → (b) · 전부 무관 → (c). 프롬프트는 doc_judge_1117 dev 에서 고정한 것 그대로.
"""
from __future__ import annotations

import json
import os
import re

PROMPT = """사용자 질문과 검색된 논문 목록이 있다. 논문마다 질문에 대한 관련도를 하나로 판정하라.
- 직접: 논문이 질문의 핵심 물음을 주제와 대상(분야 · 문서 유형 · 언어 · 비교 대상 등 질문의 조건)까지 맞춰 직접 연구 · 제안 · 평가한다.
- 부분: 질문의 일부(하위 물음 하나, 비슷한 과제, 다른 분야나 조건에서의 같은 방법)만 다뤄 답에 참고가 된다. 질문 조건 하나라도 다르면 부분이다.
- 무관: 질문에 답할 근거가 없다. 주제 단어만 겹치고 묻는 것과 다른 문제를 다루면 무관이다.

질문: {q}

논문:
{docs}

JSON 으로만 답하라: {{"판정": [{{"번호": 1, "관련도": "직접|부분|무관"}}, ...]}}"""
SCHEMA = {"type": "object", "properties": {"판정": {"type": "array", "items": {"type": "object",
          "properties": {"번호": {"type": "integer"}, "관련도": {"type": "string", "enum": ["직접", "부분", "무관"]}},
          "required": ["번호", "관련도"]}}}, "required": ["판정"]}
_LAB = {"직접": "D", "부분": "P", "무관": "N"}


def judge_agg_active() -> bool:
    return os.getenv("RAG_JUDGE_AGG", "0").strip() == "1"


def doc_blocks(rag_context: str) -> list[tuple[int, str]]:
    """``[문서 N]`` 블록 → [(N, '제목\\n초록 900자')]."""
    out = []
    for m in re.finditer(r"\[문서 (\d+)\]\n(.*?)(?=\n\[문서 \d+\]\n|\Z)", rag_context or "", re.S):
        b = m.group(2)
        t = re.search(r"\[\d{4}\.\d{4,5}(?:v\d+)?\]\s*(.*)", b)
        ab = re.sub(r"\s+", " ", b.split("[초록]", 1)[-1] if "[초록]" in b else b).strip()[:900]
        out.append((int(m.group(1)), (t.group(1).strip() if t else "") + "\n" + ab))
    return out


def aggregate(labels: dict[int, str]) -> tuple[str, int | str]:
    """{문서 번호: D/P/N} → ('a', 첫 직접 문서 번호) · ('b', '없음') · ('c', '없음')."""
    direct = sorted(n for n, x in labels.items() if x == "D")
    if direct:
        return "a", direct[0]
    return ("b" if "P" in labels.values() else "c"), "없음"


def judge_docs(question: str, rag_context: str) -> dict[int, str] | None:
    """문서마다 D/P/N. 실패하면 None — 호출 쪽은 기존 판정으로."""
    import requests

    from core.config.agent_config import ollama_kwargs

    blocks = doc_blocks(rag_context)
    if not blocks:
        return None
    kw = ollama_kwargs()
    docs = "\n\n".join(f"[{i}] {text}" for i, (_, text) in enumerate(blocks, 1))
    try:
        r = requests.post(f"{kw['base_url']}/api/chat", json={
            "model": os.getenv("RAG_DOC_JUDGE_MODEL", "qwen3.6:27b-q4_K_M"), "stream": False, "think": False,
            "format": SCHEMA, "keep_alive": kw["keep_alive"], "options": {"temperature": 0, "num_ctx": 8192},
            "messages": [{"role": "user", "content": PROMPT.format(q=question, docs=docs)}]}, timeout=120)
        got = {x["번호"]: x["관련도"] for x in json.loads(r.json()["message"]["content"])["판정"]}
    except Exception as e:  # noqa: BLE001 — 판정 실패는 기존 판정으로 넘긴다
        print(f"[WARN] doc_judge 실패: {e}")
        return None
    if len(got) < len(blocks):
        return None
    return {n: _LAB.get(got.get(i), "P") for i, (n, _) in enumerate(blocks, 1)}


def agg_slots_active() -> bool:
    return os.getenv("RAG_AGG_SLOTS", "0").strip() == "1"


_NO_INTRO = "제공된 문서에는 질문이 찾는 연구가 없습니다."
_NO_CONCL = "따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다."


def agg_slots_template(labels: dict[int, str], agg: str) -> str:
    """판정대로 답 칸 (RAG_AGG_SLOTS, docs/experiments/agg_slots_1117): 직접 · 부분 문서마다 한 칸, 무관 문서는 칸 없음."""
    keep = [n for n in sorted(labels) if labels[n] in ("D", "P")][:5]
    if agg == "c" or not keep:
        intro, body, concl = f"`{_NO_INTRO}` 를 그대로 쓴다.", "질문과 관련된 문서가 없습니다.", f"`{_NO_CONCL}` 를 그대로 쓴다."
    else:
        tag = lambda n: " (관련 연구)" if labels[n] == "P" else ""
        body = "\n".join(f"{i}. **{{핵심 접근·시스템 이름}}**{tag(n)}: 무엇을 했고 결과가 무엇인지 1~2문장 [문서 {n}]"
                         for i, n in enumerate(keep, 1))
        if agg == "b":
            intro, concl = f"첫 문장은 `{_NO_INTRO}` 를 그대로 쓴다.", f"첫 문장은 `{_NO_CONCL}` 를 그대로 쓰고, 위 관련 연구가 질문의 어느 부분과 닿는지 한 문장."
        else:
            intro, concl = "질문이 가리키는 문제와 왜 어려운지 1~2문장. 핵심 용어는 **굵게**.", "위 항목들을 종합해 질문에 답하는 한 단락. 문서에 없는 처방을 지어내지 마세요."
    return f"""[다중 문서 출력 템플릿 지시사항 - 판정된 문서별 칸]
아래 뼈대를 그대로 따라 값만 채우세요.

[출력 템플릿]
### 서론
{intro}

### 본론
{body}

### 결론
{concl}

[규칙]
- 본론의 칸은 모두 채운다. 칸을 빼거나 더하지 않는다. 칸 끝의 `[문서 k]` 는 그대로 둔다.
- 각 칸에는 그 문서에 있는 내용만 쓴다. **arXiv ID 를 옮겨 적지 마세요.**
- `(관련 연구)` 표시는 그대로 둔다.
- 중괄호 안의 안내 문구는 출력 금지.
"""


_C_BODY_ID = re.compile(r"(관련된 문서가 없습니다\.?)[ \t]*(?:\[[^\]\n]*\][ \t]*)+")


def strip_no_doc_ids(answer: str) -> tuple[str, int]:
    """(c) 틀의 "질문과 관련된 문서가 없습니다." 뒤에 v13 이 붙인 인용 꼬리를 지운다 (agg_slots_1117 §6 결함)."""
    return _C_BODY_ID.subn(r"\1", answer or "")
