"""학술 주제 게이트 — 질문이 논문 지식베이스로 답할 주제인가 (결정적 어휘 규칙).

RAG 허용은 원래 '논문 모드 ON' 또는 질문에 '논문' 단어가 있을 때뿐이었다. 모드는 기본 OFF
이고 재시작마다 꺼져서, '논문'이라는 말 없이 물은 논문 질문 139개가 RAG 에 0번 도달했다
(docs/experiments/e2e_ko_1008 §6). 모드를 기본 ON 으로 하면 잡담 9개가 RAG 로 샌다(§8).
그래서 단어 대신 **주제**로 연다. 설계·판정: docs/experiments/topic_gate_1009/README.md.

규칙은 dev 분할만 보고 만들었다. 단어 목록을 바꾸면 test 분할 판정을 다시 해야 한다.
"""

from __future__ import annotations

import re

# 이것만 있어도 학술 질문이다 — 문헌 자체를 가리키는 말
_STRONG = (
    "논문", "연구", "서베이", "survey", "paper", "arxiv", "리뷰 논문", "학회",
)

# ML·AI·과학 분야 용어. 일상·작업 요청에는 거의 나오지 않는다.
_DOMAIN = (
    # 모델·학습
    "llm", "언어모델", "언어 모델", "파운데이션 모델", "신경망", "딥러닝", "머신러닝", "강화학습",
    "지도학습", "자기지도", "사전학습", "파인튜닝", "미세조정", "지시 튜닝", "증류", "학습한", "학습하는",
    "트랜스포머", "어텐션", "임베딩", "토큰", "파라미터", "그래디언트", "경사", "손실 함수",
    "moe", "lora", "qlora", "rlhf", "gnn", "lstm", "cnn", "clip", "bert", "gpt", "vla", "vlm",
    # 생성·검색
    "rag", "검색 증강", "환각", "프롬프트", "인컨텍스트", "퓨샷", "확산 모델", "생성 모델",
    "지식 그래프", "벡터", "bm25", "코퍼스", "컨텍스트 길이", "kv 캐시",
    # 과제·평가
    "벤치마크", "데이터셋", "멀티모달", "비전 언어", "객체 탐지", "분할", "점구름", "라이다",
    "음성 인코더", "질의응답", "추론", "에이전트", "이상 탐지", "분류기", "편향", "워터마크",
    "샘플 복잡도", "베이즈", "확률적", "최적화", "정책", "밴딧", "시뮬레이터", "시계열",
    "shap", "온톨로지", "알고리즘", "코드 생성", "캡션",
    # 다른 과학 분야
    "신약", "재료과학", "최적수송", "pde", "물리", "의료", "임상",
)

# 일상·작업 요청에서 '추론·정책·분할' 같은 말이 다른 뜻으로 쓰이는 것을 막는 문맥
_TASK_HINT = re.compile(
    r"(계획을? 세워|절차를|단계(는|를|마다|당)|차례를|스크립트|코드를 짜|함수 [a-z_]+|print|파이썬으로|"
    r"\d+줄|\d+자 (이내|안|한도|제한|까지))"
)


def is_academic_query(text: str) -> bool:
    """논문 지식베이스로 답할 학술·기술 주제 질문이면 True."""
    t = (text or "").lower()
    if not t.strip():
        return False
    if any(k in t for k in _STRONG):
        return True
    hits = sum(1 for k in _DOMAIN if k in t)
    if hits == 0:
        return False
    # 작업 지시 문맥이면 분야 용어 하나로는 열지 않는다
    if _TASK_HINT.search(t):
        return hits >= 2
    return True


# ── 2단계: 어휘 규칙이 아니라고 할 때만 묻는 LLM 판정 ──────────────────────────────
# 어휘 규칙은 분야 용어가 약한 응용 질문("웹캠으로 표정 감정을 인식해서 음악을 트는 시스템")을
# 놓친다 (test 미탐 7/90). 단어 목록은 test 판정 때문에 고정이므로, 대신 결정적 LLM 에 한 번 더
# 묻는다. 판정: docs/experiments/topic_gate_llm_1010.

_LLM_PROMPT = """You decide whether a user's message should be answered from a library of research papers (AI, machine learning, computer science, and other sciences).

Answer YES if the user asks about a research method, model, system, benchmark, technique, or findings — something a research paper would describe, even if the word "paper" is not used.
Answer NO for everyday life, personal advice, writing or messaging tasks, plans or step-by-step procedures for the user's own files or chores, coding tasks the user wants done, weather, news, or prices.

Message:
{q}

Answer with exactly one word: YES or NO."""


def is_academic_query_llm(text: str) -> bool:
    """결정적 LLM(temperature 0) 판정. 실패하면 False (기존 동작 유지)."""
    t = (text or "").strip()
    if not t:
        return False
    try:
        from langchain_core.messages import HumanMessage

        from core.llm.agent_llm import get_rag_query_rewrite_llm

        resp = get_rag_query_rewrite_llm().invoke([HumanMessage(content=_LLM_PROMPT.format(q=t[:600]))])
        out = str(getattr(resp, "content", resp) or "").strip().upper()
    except Exception:
        return False
    return out.startswith("YES")


def is_academic_query_full(text: str) -> bool:
    """어휘 규칙 → (아니면) LLM. 운영 진입점."""
    return is_academic_query(text) or is_academic_query_llm(text)
