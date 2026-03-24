"""Ollama / Gemini LLM 팩토리 (노드·RAG에서 공통 사용).

Qwen 3.x(Ollama) 샘플링은 Alibaba Qwen 3.5 권장에 맞춘다.

- Router / Direct Answer / RAG·비전 보조: ``temperature``·``top_p``·반복 억제,
  ``reasoning=False`` 로 본문에 think 태그가 섞이지 않게 한다 (LangChain → Ollama think 끔).
- Planner(계획)·LLM 토론 스케줄러: ``reasoning=True`` 로 사고를 분리하고, 에이전트 텔레그램은
  ``agent_telegram.strip_thinking_tags`` 등 기존 정제를 유지.

Ollama API에는 OpenAI식 ``presence_penalty`` 가 없어, 문서의 반복 억제 의도는
``repeat_penalty`` 로 맞춘다 (일반 경로 상향, Planner 계획은 1.0).
"""

import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from agent_config import GEMINI_API_KEY, GEMINI_MODEL, ollama_kwargs


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
    """llm_debate_scheduler: Planner와 동일 샘플링, 논문 Q&A 장문용 num_predict만 확대."""
    return ChatOllama(
        **ollama_kwargs(
            temperature=0.6,
            top_p=0.95,
            repeat_penalty=1.0,
            reasoning=True,
            num_predict=4096,
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
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL, api_key=GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"), temperature=0.1
    )


def get_monitor_llm():
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL, api_key=GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"), temperature=0.1
    )
