#!/usr/bin/env python3
"""
Agent/봇·테스트 실행 전 필수 패키지 확인.
langchain-ollama 등이 없으면 agent_bot import 단계에서 실패하므로, CI/로컬에서 먼저 돌리면 원인 분리에 유리합니다.

  python scripts/check_agent_env.py
  python scripts/check_agent_env.py --quiet && pytest tests/
  python scripts/check_agent_env.py --keys --services
  python scripts/check_agent_env.py --models
"""
from __future__ import annotations

import argparse
import os
import sys
import urllib.request
import warnings
from pathlib import Path

from dotenv import load_dotenv


def _need_py(min_major: int, min_minor: int) -> None:
    if sys.version_info < (min_major, min_minor):
        print(
            f"ERROR: Python {min_major}.{min_minor}+ 필요 (현재 {sys.version_info.major}.{sys.version_info.minor})",
            file=sys.stderr,
        )
        sys.exit(1)


def _try_import(name: str, pip_hint: str) -> str | None:
    try:
        if name == "google.generativeai":
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", FutureWarning)
                __import__(name)
        else:
            __import__(name)
        return None
    except Exception as e:  # noqa: BLE001 — 환경 점검용
        return f"{name}: {e}  →  pip install {pip_hint}"


def _check_ollama_line() -> str:
    load_dotenv()
    base = (os.getenv("OLLAMA_HOST") or "http://localhost:11434").rstrip("/")
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=3) as resp:
            resp.read(64)
        return f"Ollama ({base}): OK"
    except Exception as e:  # noqa: BLE001
        return f"Ollama ({base}): unreachable — {type(e).__name__}: {e}"


def _check_keys_lines() -> list[str]:
    load_dotenv()
    optional = [
        ("GEMINI_API_KEY", "라우터 폴백·도구·Tavily 요약"),
        ("GROQ_API_KEY", "Executor/Monitor 코딩·검수"),
        ("E2B_API_KEY", "test_agent_flow 4·코드 실행"),
        ("TELEGRAM_TOKEN", "agent_bot.py"),
        ("TAVILY_API_KEY", "웹 검색 도구"),
    ]
    lines = []
    for key, hint in optional:
        v = os.getenv(key)
        if v and str(v).strip() and "your_" not in str(v).lower() and "here" not in str(v).lower():
            lines.append(f"  {key}: 설정됨 ({hint})")
        else:
            lines.append(f"  {key}: 없음 또는 placeholder — {hint} 시 필요")
    return lines


def _check_models_lines() -> list[str]:
    """sentence-transformers 임베딩 캐시(Chroma RAG) — 있으면 첫 실행이 빨라짐."""
    load_dotenv()
    hub_root = Path(os.getenv("HF_HOME", str(Path.home() / ".cache" / "huggingface")))
    hub = hub_root / "hub"
    lines = [f"  HF_HOME/hub: {hub}"]
    if not hub.is_dir():
        lines.append("  → 디렉터리 없음. Chroma 첫 검색 시 모델 다운로드가 발생할 수 있습니다.")
        return lines
    mini_lm = list(hub.glob("**/models--sentence-transformers--all-MiniLM-L6-v2/**"))
    if mini_lm:
        lines.append("  → all-MiniLM-L6-v2 캐시 흔적: 있음")
    else:
        lines.append("  → all-MiniLM-L6-v2 캐시 흔적: 없음 (첫 RAG 시 다운로드)")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="mini 에이전트 의존성·키·서비스 점검")
    parser.add_argument("--quiet", "-q", action="store_true", help="성공 시 패키지 OK 한 줄만 생략(확장 플래그 출력은 유지)")
    parser.add_argument("--keys", action="store_true", help="주요 API 키 존재 여부 요약")
    parser.add_argument("--services", action="store_true", help="Ollama HTTP 연결 확인")
    parser.add_argument("--models", action="store_true", help="HuggingFace 캐시·임베딩 모델 흔적")
    args = parser.parse_args()

    _need_py(3, 10)

    checks = [
        ("langchain_ollama", "langchain-ollama"),
        ("langchain_google_genai", "langchain-google-genai"),
        ("langchain_groq", "langchain-groq"),
        ("langchain_core", "langchain-core"),
        ("langgraph", "langgraph"),
        ("chromadb", "chromadb"),
        ("telebot", "pyTelegramBotAPI"),
        ("e2b_code_interpreter", "e2b-code-interpreter"),
        ("google.generativeai", "google-generativeai"),
        ("dotenv", "python-dotenv"),
    ]
    errors: list[str] = []
    for mod, pip in checks:
        err = _try_import(mod, pip)
        if err:
            errors.append(err)

    if errors:
        print("환경 점검 실패 — 아래 패키지를 설치하세요:\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print(
            "\n권장: 프로젝트 루트에서\n"
            "  python3 -m venv .venv && source .venv/bin/activate\n"
            "  pip install -U pip && pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    ext = args.keys or args.services or args.models
    if not args.quiet or ext:
        if not args.quiet:
            print(f"OK: Python {sys.version_info.major}.{sys.version_info.minor}, 필수 패키지 import 성공")

    if args.services:
        print("[--services]", _check_ollama_line(), sep="\n", end="\n\n")
    if args.keys:
        print("[--keys]")
        for line in _check_keys_lines():
            print(line)
        print()
    if args.models:
        print("[--models]")
        for line in _check_models_lines():
            print(line)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
