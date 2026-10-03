# -*- coding: utf-8 -*-
"""E2B 격리 샌드박스에서 Python 실행 (에이전트 Tool)."""

import logging
import os
import sys
from typing import Any

logger = logging.getLogger(__name__)

# 프로젝트 루트( mini/ )를 path에 올리기: 도구 러너가 sys.path[0]을 설정하지 않은 경우
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv(override=True)

from core.config.agent_config import CODE_TIMEOUT_SEC, ERROR_LOG_MAX_CHARS
from core.execution.agent_sandbox import _e2b_sandbox_envs


def _format_execution(execution: Any) -> str:
    """E2B run_code 실행 결과의 stdout, stderr, text, error를 구획 라벨로 합침."""
    parts: list[str] = []
    logs = execution.logs
    if logs:
        stdout = "".join(logs.stdout or [])
        if stdout.strip():
            parts.append(f"[stdout]\n{stdout.rstrip()}")
        stderr = "".join(logs.stderr or [])
        if stderr.strip():
            parts.append(f"[stderr]\n{stderr.rstrip()}")
    if getattr(execution, "text", None) and str(execution.text).strip():
        parts.append(f"[result]\n{str(execution.text).rstrip()}")
    err = execution.error
    if err is not None:
        tb = getattr(err, "traceback", None) or ""
        parts.append(
            f"[error]\n{getattr(err, 'name', 'Error')}: {getattr(err, 'value', err)}\n{tb.rstrip()}"
        )
    if parts:
        return "\n\n".join(parts)
    return "실행 완료 (출력 없음)"


def _execute_python_in_sandbox_core(code: str) -> str:
    """E2B 샌드박스에서 코드 실행(순수 구현; 도구 래퍼는 별도)."""
    try:
        from e2b_code_interpreter import Sandbox

        api_key = (os.getenv("E2B_API_KEY") or "").strip()
        if not api_key:
            return "실행 오류: E2B_API_KEY가 .env(또는 환경 변수)에 설정되지 않았습니다."

        env_dict = _e2b_sandbox_envs()
        with Sandbox.create() as sandbox:
            execution = sandbox.run_code(code, timeout=CODE_TIMEOUT_SEC, envs=env_dict)

        out = _format_execution(execution)
        if len(out) > ERROR_LOG_MAX_CHARS * 4:
            return f"{out[: ERROR_LOG_MAX_CHARS * 2]}\n\n…(이하 잘림)…\n\n{out[-ERROR_LOG_MAX_CHARS * 2 :]}"
        return out
    except Exception as e:  # noqa: BLE001 — 도구는 모든 실패를 문자열로 돌려 에이전트에 전달
        err = str(e)
        if len(err) > ERROR_LOG_MAX_CHARS:
            err = f"...{err[-ERROR_LOG_MAX_CHARS:]}"
        return f"실행 오류: {type(e).__name__}: {err}"


@tool
def execute_python_in_sandbox(code: str = "") -> str:
    """
    격리된 E2B 샌드박스 가상 환경에서 파이썬 코드를 실행합니다.

    Args:
        code (str): 실행할 파이썬 소스 **전체**를 담은 하나의 문자열 (tool input JSON의 ``code`` 필드).

    Note:
        인자는 **반드시 한 개** ``code`` 만 사용합니다 (Anthropic tool_use 입력 키와 동일).
        빈 ``{}`` 방지용 기본값 ``""`` — 비어 있으면 아래에서 안내 후 반환합니다.
    """
    src = (code or "").strip()
    if not src:
        return (
            "[도구 입력 누락] execute_python_in_sandbox 의 tool input 에 "
            '`{"code": "<여기에 전체 파이썬 코드>"}` '
            "처럼 **code 키에 소스 전체**를 넣으십시오. 빈 입력 객체는 동작하지 않습니다."
        )
    return _execute_python_in_sandbox_core(src)
