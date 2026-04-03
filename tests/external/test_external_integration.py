"""
실서비스 연동 스모크 (Ollama / Gemini / E2B).

- 마커: external → CI 기본은 `pytest -m "not external"` 로 제외.
- 로컬: 키·서비스가 있으면 실행, 없으면 pytest.skip.
"""

from __future__ import annotations

import os
import sys
import urllib.request
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

pytestmark = [pytest.mark.external, pytest.mark.timeout(120)]


def _ollama_ok() -> bool:
    base = (os.getenv("OLLAMA_HOST") or "http://localhost:11434").rstrip("/")
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=3) as resp:
            resp.read(32)
        return True
    except OSError:
        return False


def test_external_ollama_chat_smoke():
    if not _ollama_ok():
        pytest.skip("SKIP: Ollama not reachable (OLLAMA_HOST)")
    from langchain_core.messages import HumanMessage
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model=os.getenv("LOCAL_LLM_MODEL", "qwen3.5:9b"),
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        temperature=0.2,
    )
    r = llm.invoke([HumanMessage(content="Reply with exactly: OK")])
    assert r.content


def test_external_gemini_smoke():
    key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not key:
        pytest.skip("SKIP: GEMINI_API_KEY missing")
    from langchain_core.messages import HumanMessage
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=key, temperature=0.1)
    r = llm.invoke([HumanMessage(content="1+1=? answer digit only")])
    assert r.content and "2" in r.content.replace(" ", "")


def test_external_e2b_print():
    if not (os.getenv("E2B_API_KEY") or "").strip():
        pytest.skip("SKIP: E2B_API_KEY missing")
    from core.execution.agent_sandbox import run_code_sandbox

    r = run_code_sandbox("print(1+1)")
    if (r or "").strip().startswith("실행 오류"):
        pytest.fail(f"E2B returned error string: {r[:300]}")
    assert "2" in (r or "").replace(" ", "")
