"""Ollama / Gemini / Groq LLM 팩토리 (노드·RAG에서 공통 사용).

- **Executor / Monitor 노드**: ``get_coding_groq_llm()`` (ChatGroq + 429 재시도).
- **라우터 폴백·도구 선택·Tavily 요약**: ``get_executor_llm()`` (Gemini, 기존과 동일).

Qwen 3.x(Ollama) 샘플링은 Alibaba Qwen 3.5 권장에 맞춘다.

- Router / Direct Answer / RAG·비전 보조: ``temperature``·``top_p``·반복 억제,
  ``reasoning=False`` 로 본문에 think 태그가 섞이지 않게 한다 (LangChain → Ollama think 끔).
- Planner(계획)·LLM 토론 스케줄러: ``reasoning=True`` 로 사고를 분리하고, 에이전트 텔레그램은
  ``agent_telegram.strip_thinking_tags`` 등 기존 정제를 유지.

Ollama API에는 OpenAI식 ``presence_penalty`` 가 없어, 문서의 반복 억제 의도는
``repeat_penalty`` 로 맞춘다 (일반 경로 상향, Planner 계획은 1.0).
"""

import os
from typing import Any, Optional

import httpx
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from agent_config import GEMINI_MODEL, get_gemini_api_keys, ollama_kwargs
from agent_gemini import RotatingGeminiChat

# Groq 무료 한도·코딩용 기본 모델 (환경변수로 덮어쓰기 가능)
GROQ_CODING_MODEL = os.getenv(
    "GROQ_CODING_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"
)


def get_router_llm():
    """라우터 3단계 분류: 안정적 샘플링, 사고 모드 끔."""
    return ChatOllama(
        **ollama_kwargs(
            temperature=0.7,
            top_p=0.8,
            repeat_penalty=1.25,
            reasoning=False,
            num_predict=12,
        )
    )


def get_planner_llm():
    """Direct Answer·라우터 Ollama 폴백·세션 요약 등: 비-thinking, 반복 억제."""
    return ChatOllama(
        **ollama_kwargs(
            temperature=0.7,
            top_p=0.8,
            repeat_penalty=1.25,
            reasoning=False,
        )
    )


def get_planner_plan_llm():
    """Planner·PlannerDebate: 코딩/기획, 반복 페널티 완화, thinking 허용."""
    return ChatOllama(
        **ollama_kwargs(
            temperature=0.6,
            top_p=0.95,
            repeat_penalty=1.0,
            reasoning=True,
            num_predict=300,
        )
    )


def get_llm_debate_scheduler_llm():
    """llm_debate_scheduler: Golden Q&A용 reasoning 유지, 출력 상한은 Q&A 1세트에 맞게 보수적으로."""
    return ChatOllama(
        **ollama_kwargs(
            temperature=0.6,
            top_p=0.95,
            repeat_penalty=1.0,
            reasoning=True,
            num_predict=1500,
        )
    )


def get_rag_query_rewrite_llm():
    """Chroma standalone 검색어 재작성: 짧은 출력, 비-thinking."""
    return ChatOllama(
        **ollama_kwargs(
            temperature=0.7,
            top_p=0.8,
            repeat_penalty=1.25,
            reasoning=False,
            num_predict=160,
        )
    )


def get_vision_llm():
    """이미지 분석: 비-thinking, 설명 길이 여유."""
    return ChatOllama(
        **ollama_kwargs(
            temperature=0.7,
            top_p=0.8,
            repeat_penalty=1.25,
            reasoning=False,
            num_predict=1024,
        )
    )


def get_executor_llm():
    """Gemini: 라우터 3단계 폴백, 기존 도구 LLM 선택, Tavily 요약 등 (Executor 노드 제외).
    키가 여러 개면 429·Rate limit 시 자동으로 다음 키로 재시도."""
    return RotatingGeminiChat(get_gemini_api_keys(), GEMINI_MODEL, 0.1)


def _is_groq_rate_limit_error(exc: BaseException) -> bool:
    """Groq/게이트웨이 429 및 Rate limit 계열 오류 판별."""
    sc = getattr(exc, "status_code", None)
    if sc == 429:
        return True
    response = getattr(exc, "response", None)
    if response is not None:
        rsc = getattr(response, "status_code", None)
        if rsc == 429:
            return True
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429:
        return True
    name = type(exc).__name__
    if "RateLimit" in name or "TooManyRequests" in name:
        return True
    msg = str(exc).lower()
    if "429" in msg and ("rate" in msg or "limit" in msg or "too many" in msg):
        return True
    return False


class _CodingChatGroqWithRetry:
    """Executor·Monitor 전용 ChatGroq 래퍼: 429 시 지수 백오프로 최대 3회 재시도(총 4회 시도)."""

    def __init__(self) -> None:
        key = os.getenv("GROQ_API_KEY")
        self._llm = ChatGroq(
            model=GROQ_CODING_MODEL,
            api_key=key,
            temperature=0.2,
        )

    @retry(
        retry=retry_if_exception(_is_groq_rate_limit_error),
        wait=wait_exponential(multiplier=1, min=2, max=45),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def invoke(
        self,
        input: Any,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ):
        return self._llm.invoke(input, config=config, **kwargs)


_coding_groq_singleton: _CodingChatGroqWithRetry | None = None


def get_coding_groq_llm():
    """코드 작성(Executor)·검수(Monitor) 전용 Groq LLM. ``GROQ_API_KEY`` 필수."""
    global _coding_groq_singleton
    if _coding_groq_singleton is None:
        _coding_groq_singleton = _CodingChatGroqWithRetry()
    return _coding_groq_singleton
