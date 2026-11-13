"""정답 유무 판정 호출 — 답변 생성 전에 "질문이 찾는 그 연구가 몇 번 문서인가 / 없는가"만 묻는다.

왜 따로 묻나 (docs/experiments/presence_judge_1011, abstract_context_1011): 답변 모델에 판단과 생성을
함께 맡기면 정답 없음 고지와 거짓 부정을 맞바꿀 뿐이었다(v14). 초록이 붙은 컨텍스트에서 이 판정 호출은
거짓 '없음' 3.6%·재현 13/21 로 기준을 통과했다. 판정이 '없음'일 때만 답변 프롬프트에 힌트를 넣는다.

``PROMPT`` 는 오프라인 측정(scripts/presence_judge.py)과 같은 글자다 — 바꾸면 다시 잰다.
"""

from __future__ import annotations

import os
import re

__all__ = ["PROMPT", "gate_types", "should_judge", "NO_DOC_HINT", "parse_pick", "judge_presence",
           "SHARED_TAIL", "shared_prefix_active", "shared_judge_messages", "judge_presence_shared",
           "ITEM_TAIL", "parse_item_docs", "item_docs_note", "judge_items",
           "SHARED_TAIL_V2", "parse_pick_v2", "judge_presence_shared_v2"]

PROMPT = """아래 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 **특정한 연구 하나**를 찾고 있다.

질문이 묘사하는 바로 그 연구가 참고 문서 중에 있으면 그 문서 번호를, 없으면 `없음`을 답하라.
- 주제만 비슷하고 질문이 묘사하는 방법·대상·결과와 맞지 않으면 `없음`이다.
- 같은 논문이 여러 번호에 나뉘어 있으면 가장 앞 번호 하나만 적는다.

출력은 정확히 한 줄: `답: 문서 N` 또는 `답: 없음`

[질문]
{question}

[참고 문서]
{context}"""

# 질문 유형 게이트 (docs/experiments/presence_gate_1014): 수치·비교·목록 질문은 "특정 연구 하나" 전제가
# 맞지 않아 판정이 `없음` 을 남발한다(real_eval_1013 §5). `RAG_PRESENCE_GATE=1` 이면 이런 질문은 판정을 건너뛴다.
_GATE_NUM = re.compile(r"몇\s*(%|퍼센트|배|개|점|명|위)|몇\s*%|얼마나|정확도가|성공률|수치|\d+\s*%")
_GATE_CMP = re.compile(r"차이|비교|어떻게 달라|뭐가 달라|다른 거야|vs\.?|\S+(랑|이랑|와|과)\s+\S+.*(차이|비교|달라|다른)")
_GATE_LIST = re.compile(r"논문들|연구들|동향|정리해|트렌드|\d+\s*개\s*(찾|알려)|목록|방향으로 가")
# 열린 요청(추천 · 아무거나 · N편)도 "특정 연구 하나"가 아니라 판정이 거짓 '없음'을 낸다(judge_none_1103 — 5/5).
# 목록 모드는 켜지 않고 판정만 건너뛴다(`RAG_OPEN_GATE`, docs/experiments/open_gate_1103). "추천 시스템" 같은 주제어는 안 잡게 동사꼴만.
_GATE_OPEN = re.compile(r"추천\s*(해|좀|부탁)|아무\s*(거나|논문|연구)|볼\s*만한|읽어야\s*할|읽을\s*만한|재밌는|재미있는"
                        r"|괜찮은\s*(논문|연구)|좋은\s*(논문|연구)|\d+\s*편|몇\s*편|(두|세|네|다섯|여섯|일곱|여덟|아홉|열)\s*편"
                        r"|뽑아\s*(줘|주)|골라\s*(줘|주)|최신\s*(논문|연구)")


def gate_types(question: str) -> list[str]:
    """질문이 걸리는 유형 이름들(num·cmp·list). 비어 있으면 판정 대상."""
    q = question or ""
    got = [n for n, r in (("num", _GATE_NUM), ("cmp", _GATE_CMP), ("list", _GATE_LIST)) if r.search(q)]
    if os.getenv("RAG_QTYPE_CLF", "0").strip() == "1":
        # 분류기 (docs/experiments/qtype_1102) — 수치 · 비교는 분류기만, 목록은 정규식과 합친다(정규식 쪽이 정밀함)
        from core.llm.qtype import predict

        p = predict(q)
        got = [n for n, t in (("num", "N"), ("cmp", "C"), ("list", "L")) if t in p or (n == "list" and n in got)]
    return got


def should_judge(question: str) -> bool:
    if os.getenv("RAG_PRESENCE_GATE", "0").strip() != "1":
        return True
    if os.getenv("RAG_OPEN_GATE", "0").strip() == "1" and _GATE_OPEN.search(question or ""):
        return False
    return not gate_types(question)


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


# 답변과 같은 앞부분으로 판정 (docs/experiments/judge_cache_1017). 답변 프롬프트의 `[사용자]` 앞까지를
# 그대로 두고 판정 지시만 뒤에 붙이면 Ollama 가 그 앞부분을 답변 호출에서 다시 쓴다.
SHARED_TAIL = """
[판정 요청 — 답변을 쓰지 말고 판정 한 줄만]
위 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 **특정한 연구 하나**를 찾고 있다.

질문이 묘사하는 바로 그 연구가 참고 문서 중에 있으면 그 문서 번호를, 없으면 `없음`을 답하라.
- 주제만 비슷하고 질문이 묘사하는 방법·대상·결과와 맞지 않으면 `없음`이다.
- 같은 논문이 여러 번호에 나뉘어 있으면 가장 앞 번호 하나만 적는다.

출력은 정확히 한 줄: `답: 문서 N` 또는 `답: 없음`

[질문]
{question}"""

_USER_MARK = "\n[사용자]\n"


def shared_prefix_active() -> bool:
    return os.getenv("RAG_JUDGE_SHARED_PREFIX", "0").strip() == "1"


def shared_judge_messages(system_prompt: str, answer_prompt: str, question: str):
    """답변 메시지와 같은 앞부분 + 판정 지시. 표지가 없으면 None (호출 쪽은 기존 판정)."""
    from langchain_core.messages import HumanMessage, SystemMessage

    cut = answer_prompt.rfind(_USER_MARK)
    if cut < 0:
        return None
    return [SystemMessage(content=system_prompt), HumanMessage(content=answer_prompt[:cut] + "\n" + SHARED_TAIL.format(question=question))]


def judge_presence_shared(system_prompt: str, answer_prompt: str, question: str, model: str) -> int | str | None:
    """`judge_presence` 와 같은 설정(temperature 0, seed 0, 64토큰)으로 답변과 같은 앞부분을 보낸다."""
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    msgs = shared_judge_messages(system_prompt, answer_prompt, question)
    if msgs is None:
        return None
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=64))
    try:
        raw = str(llm.invoke(msgs).content or "")
    except Exception as exc:
        print(f"[DEBUG] presence_judge(shared) 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return None
    return parse_pick(raw)


# 여러 주제 질문: "특정한 연구 하나"를 묻는 판정은 '없음'으로 기운다(answer_gap_1104 — 21/36). 항목마다 문서가 있는지 묻는다
# (docs/experiments/topic_answer_1104). 항목 → 문서로 물으면 문서 있는 주제의 27~39% 를 없다고 해서 문서 → 항목으로 묻는다.
ITEM_TAIL = """
[판정 요청 — 답변을 쓰지 말고 판정만]
위 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 아래 [항목]마다 논문을 찾고 있다.

문서마다 그 문서가 다루는 항목 번호를 적어라. 어느 항목도 다루지 않으면 `없음`이라고 적어라.
- 단어만 겹치고 다른 문제를 다루는 문서는 `없음`이다.

출력은 문서마다 한 줄, 다른 말 없이:
문서 1: 항목 2
문서 2: 없음

[항목]
{items}"""


def parse_item_docs(raw: str, n_items: int) -> dict[int, list[int]] | None:
    """``'문서 1: 항목 2'`` 줄들 → ``{항목: [문서 번호]}``. 그런 줄이 없으면 None (호출 쪽은 기존 판정)."""
    rows = re.findall(r"문서\s*(\d{1,2})\s*[:：]\s*(.*)", raw or "")
    if not rows:
        return None
    got: dict[int, list[int]] = {k: [] for k in range(1, n_items + 1)}
    for doc, val in rows:
        if "없음" in val:
            continue
        for k in re.findall(r"\d{1,2}", val):
            if int(k) in got and int(doc) not in got[int(k)]:
                got[int(k)].append(int(doc))
    return got


def item_docs_note(items: list[str], item_docs: dict[int, list[int]]) -> str:
    """답변 프롬프트에 넣는 항목별 문서 표."""
    rows = [
        f"{k}. {x}: " + (", ".join(f"[문서 {d}]" for d in item_docs[k]) if item_docs[k] else "없음")
        for k, x in enumerate(items, 1)
    ]
    return (
        "\n[항목별 문서 — 사전 판정]\n" + "\n".join(rows)
        + "\n본론은 문서가 있는 항목을 항목 순서대로 쓰고, 그 항목에 적힌 문서의 내용만 쓴다. "
        "`없음` 항목은 본론 · 결론에서 다루지 마라(따로 안내한다). 문서에 없는 내용을 지어내지 마라.\n"
    )


def judge_items(system_prompt: str, answer_prompt: str, items: list[str], model: str) -> dict[int, list[int]] | None:
    """답변과 같은 앞부분으로 항목별 판정. 실패 · 형식 밖이면 None — 호출 쪽은 기존 판정으로 간다."""
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    cut = answer_prompt.rfind(_USER_MARK)
    if cut < 0:
        return None
    tail = ITEM_TAIL.format(items="\n".join(f"{k}. {x}" for k, x in enumerate(items, 1)))
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=120))
    try:
        raw = str(llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=answer_prompt[:cut] + "\n" + tail)]).content or "")
    except Exception as exc:
        print(f"[DEBUG] presence_judge(items) 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return None
    return parse_item_docs(raw, len(items))


# 3단계 판정 (docs/experiments/graded_1113). 운영 꼬리는 "특정한 연구 하나" 로 못박아 추천형 질문에서 큰 모델이 '없음' 으로
# 쏠렸다(judge_filter_diag_1113 §2). 질문 꼴을 먼저 가리고 '부분' 을 둔다. 운영 연결 전(기본 꺼짐).
SHARED_TAIL_V2 = """
[판정 요청 — 답변을 쓰지 말고 판정 한 줄만]
위 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다.

먼저 질문이 (가) 특정한 연구 하나를 묘사하는지(방법 · 대상 · 결과 · 이름을 구체적으로 말함), (나) 주제를 주고 논문을 추천 · 정리받으려는지 가린다.
- (가)이면: 질문이 묘사하는 바로 그 연구가 있으면 `있음`, 주제는 같지만 묘사한 방법 · 대상 · 결과와 다른 연구만 있으면 `부분`, 주제부터 다르면 `없음`.
- (나)이면: 질문 주제를 주된 내용으로 다루는 문서가 있으면 `있음`, 가까운 주제만 있으면 `부분`, 낱말이나 분야만 겹치면 `없음`. 주제가 없는 요청(아무 논문 · 재밌는 논문)은 `있음` 에 첫 문서.
`있음` · `부분` 이면 가장 맞는 문서 번호 하나를 함께 적는다.

출력은 정확히 한 줄: `답: 있음 문서 N` 또는 `답: 부분 문서 N` 또는 `답: 없음`

[질문]
{question}"""

_ANS_V2 = re.compile(r"답\s*[:：]\s*(?:(있음|부분)\s*,?\s*\[?\s*문서\s*(\d{1,2})|(없음))")


def parse_pick_v2(raw: str) -> tuple[str, int] | str | None:
    """``'답: 있음 문서 3'`` → ('있음', 3), ``'답: 부분 문서 2'`` → ('부분', 2), ``'답: 없음'`` → '없음', 형식 밖 → None."""
    m = _ANS_V2.search(raw or "")
    if not m:
        return None
    return "없음" if m.group(3) else (m.group(1), int(m.group(2)))


def judge_presence_shared_v2(system_prompt: str, answer_prompt: str, question: str, model: str) -> tuple[str, int] | str | None:
    """`judge_presence_shared` 와 같은 앞부분 · 설정에 v2 꼬리."""
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    cut = answer_prompt.rfind(_USER_MARK)
    if cut < 0:
        return None
    msgs = [SystemMessage(content=system_prompt), HumanMessage(content=answer_prompt[:cut] + "\n" + SHARED_TAIL_V2.format(question=question))]
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=64))
    try:
        raw = str(llm.invoke(msgs).content or "")
    except Exception as exc:
        print(f"[DEBUG] presence_judge(v2) 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return None
    return parse_pick_v2(raw)
