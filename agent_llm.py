"""Ollama / Gemini LLM 팩토리 (노드·RAG에서 공통 사용)."""

import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from agent_config import GEMINI_API_KEY, GEMINI_MODEL, ollama_kwargs


def get_planner_llm():
    """일반 Ollama (라우터 폴백·DirectAnswer 폴백 등). 장문 응답 허용."""
    return ChatOllama(**ollama_kwargs(temperature=0.2))


def get_planner_plan_llm():
    """Planner·PlannerDebate 전용: num_predict로 계획 장문·다단계 토큰 폭주 방지."""
    return ChatOllama(**ollama_kwargs(temperature=0.2, num_predict=300))


def get_router_llm():
    """라우터 전용: 1토큰만 출력, temperature=0으로 극한 최적화"""
    return ChatOllama(**ollama_kwargs(temperature=0, num_predict=1))


def get_executor_llm():
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL, api_key=GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"), temperature=0.1
    )


def get_monitor_llm():
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL, api_key=GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"), temperature=0.1
    )
