"""정답 유무 판정 호출 — 답변 생성 전에 "질문이 찾는 그 연구가 몇 번 문서인가 / 없는가"만 묻는다.

왜 따로 묻나 (docs/experiments/presence_judge_1011, abstract_context_1011): 답변 모델에 판단과 생성을
함께 맡기면 정답 없음 고지와 거짓 부정을 맞바꿀 뿐이었다(v14). 초록이 붙은 컨텍스트에서 이 판정 호출은
거짓 '없음' 3.6%·재현 13/21 로 기준을 통과했다. 판정이 '없음'일 때만 답변 프롬프트에 힌트를 넣는다.

``PROMPT`` 는 오프라인 측정(scripts/presence_judge.py)과 같은 글자다 — 바꾸면 다시 잰다.
"""

from __future__ import annotations

import re

__all__ = ["PROMPT", "NO_DOC_HINT", "parse_pick", "judge_presence"]

PROMPT = """아래 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 **특정한 연구 하나**를 찾고 있다.

질문이 묘사하는 바로 그 연구가 참고 문서 중에 있으면 그 문서 번호를, 없으면 `없음`을 답하라.
- 주제만 비슷하고 질문이 묘사하는 방법·대상·결과와 맞지 않으면 `없음`이다.
- 같은 논문이 여러 번호에 나뉘어 있으면 가장 앞 번호 하나만 적는다.

출력은 정확히 한 줄: `답: 문서 N` 또는 `답: 없음`

[질문]
{question}

[참고 문서]
{context}"""

# v13 이 학습한 정답 없음 형식(yunsur_v13 README §2)을 그대로 지시한다.
NO_DOC_HINT = """

[사전 판정] 참고 문서에는 질문이 찾는 연구가 없다. 다음 형식을 따른다:
- 서론 첫 문장: `제공된 문서에는 질문이 찾는 연구가 없습니다.`
- 본론: 주제가 가장 가까운 문서만 최대 2개, 항목 이름 뒤에 `(관련 연구)` 를 붙이고 그 문서에 있는 내용만 쓴다.
- 결론 첫 문장: `따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.`"""

_ANS = re.compile(r"답\s*[:：]\s*(?:\[?\s*문서\s*(\d{1,2})\s*\]?|(없음))")


def parse_pick(raw: str) -> int | str | None:
    """``'답: 문서 3'`` → 3, ``'답: 없음'`` → ``'없음'``, 형식 밖 → None."""
    m = _ANS.search(raw or "")
    if not m:
        return None
    return "없음" if m.group(2) else int(m.group(1))


def judge_presence(question: str, numbered_context: str, model: str) -> int | str | None:
    """Ollama 로 판정한다(temperature 0, seed 0, 비-thinking). 실패하면 None — 호출 쪽은 힌트 없이 진행."""
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=64))
    try:
        raw = str(llm.invoke(PROMPT.format(question=question, context=numbered_context)).content or "")
    except Exception as exc:  # 판정이 실패해도 답변은 낸다
        print(f"[DEBUG] presence_judge 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return None
    return parse_pick(raw)
