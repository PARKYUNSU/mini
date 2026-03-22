#!/usr/bin/env python3
"""
Agent/봇·테스트 실행 전 필수 패키지 확인.
langchain-ollama 등이 없으면 agent_bot import 단계에서 실패하므로, CI/로컬에서 먼저 돌리면 원인 분리에 유리합니다.

  python scripts/check_agent_env.py
  python scripts/check_agent_env.py --quiet && pytest tests/
"""
from __future__ import annotations

import argparse
import sys


def _need_py(min_major: int, min_minor: int) -> None:
    if sys.version_info < (min_major, min_minor):
        print(
            f"ERROR: Python {min_major}.{min_minor}+ 필요 (현재 {sys.version_info.major}.{sys.version_info.minor})",
            file=sys.stderr,
        )
        sys.exit(1)


def _try_import(name: str, pip_hint: str) -> str | None:
    try:
        __import__(name)
        return None
    except Exception as e:  # noqa: BLE001 — 환경 점검용
        return f"{name}: {e}  →  pip install {pip_hint}"


def main() -> int:
    parser = argparse.ArgumentParser(description="mini 에이전트 의존성 점검")
    parser.add_argument("--quiet", "-q", action="store_true", help="성공 시 출력 없음")
    args = parser.parse_args()

    _need_py(3, 10)

    # (모듈 import명, pip 패키지 힌트)
    checks = [
        ("langchain_ollama", "langchain-ollama"),
        ("langchain_google_genai", "langchain-google-genai"),
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

    if not args.quiet:
        print(f"OK: Python {sys.version_info.major}.{sys.version_info.minor}, 필수 패키지 import 성공")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
