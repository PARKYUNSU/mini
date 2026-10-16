"""RAG_HELPER_MODEL — 보조 호출 모델 (docs/experiments/helper_model_1016)."""

from core.config.agent_config import OLLAMA_MODEL
from core.llm import agent_llm as L


def test_default_uses_base(monkeypatch):
    monkeypatch.delenv("RAG_HELPER_MODEL", raising=False)
    assert L.get_router_llm().model == OLLAMA_MODEL
    assert L.get_rag_query_rewrite_llm().model == OLLAMA_MODEL


def test_helper_model_override(monkeypatch):
    monkeypatch.setenv("RAG_HELPER_MODEL", "yunsur_v13")
    assert L.get_router_llm().model == "yunsur_v13"
    assert L.get_rag_query_rewrite_llm().model == "yunsur_v13"
    assert L.get_planner_llm().model == OLLAMA_MODEL  # 잡담·계획은 그대로
