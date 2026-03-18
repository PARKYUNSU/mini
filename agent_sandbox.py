"""E2B 샌드박스 코드 실행"""

import os
from pathlib import Path

from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

from agent_config import CODE_TIMEOUT_SEC, ERROR_LOG_MAX_CHARS, PROJECT_ROOT


def run_code_sandbox(code: str) -> str:
    """E2B 클라우드 샌드박스에서 코드 실행. Host 완전 격리."""
    if not os.getenv("E2B_API_KEY"):
        return "실행 오류: E2B_API_KEY가 .env에 설정되지 않았습니다."

    load_dotenv(override=True)
    env_dict = {k: v for k, v in os.environ.items() if isinstance(v, str) and k != "E2B_API_KEY"}
    if "OPENWEATHERMAP_API_KEY" in env_dict and "WEATHER_API_KEY" not in env_dict:
        env_dict["WEATHER_API_KEY"] = env_dict["OPENWEATHERMAP_API_KEY"]

    try:
        with Sandbox.create() as sandbox:
            execution = sandbox.run_code(code, timeout=CODE_TIMEOUT_SEC, envs=env_dict)

            if execution.error:
                err_msg = (
                    f"{execution.error.name}: {execution.error.value}\n"
                    f"{execution.error.traceback or ''}"
                )
                truncated = err_msg[-ERROR_LOG_MAX_CHARS:] if len(err_msg) > ERROR_LOG_MAX_CHARS else err_msg
                return f"실행 오류: {truncated}"

            stdout_parts = execution.logs.stdout if execution.logs else []
            stderr_parts = execution.logs.stderr if execution.logs else []
            stdout = "".join(stdout_parts).strip() if stdout_parts else ""
            stderr = "".join(stderr_parts).strip() if stderr_parts else ""

            result_text = execution.text or ""
            combined = stdout or result_text or stderr
            return combined.strip() or "실행 완료 (출력 없음)"

    except Exception as e:
        err_str = str(e)
        if len(err_str) > ERROR_LOG_MAX_CHARS:
            err_str = f"...{err_str[-ERROR_LOG_MAX_CHARS:]}"
        return f"실행 오류: {type(e).__name__}: {err_str}"
