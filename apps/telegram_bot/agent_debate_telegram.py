"""텔레그램 /debate_start·/debate_stop — llm_debate_scheduler.py --test 백그라운드 실행."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from typing import Optional

from dotenv import load_dotenv

from core.config.agent_config import (
    LLM_DEBATE_SCHEDULER_PATH,
    LLM_DEBATE_TELEGRAM_LOG_PATH,
    PROJECT_ROOT,
)
from pipelines.debate.llm_debate_spawn_guard import (
    clear_all_debate_child_pid_files,
    debate_spawn_lock,
    get_running_debate_scheduler_child_pid,
    register_debate_child_pid,
)


def _telegram_debate_duration_sec() -> int:
    """`/debate_start` 호출마다 .env를 다시 읽음. 미설정·0 이하 = 시간 제한 없음."""
    env_path = PROJECT_ROOT / ".env"
    if env_path.is_file():
        load_dotenv(env_path, override=True)
    else:
        load_dotenv(override=True)
    raw = (os.getenv("LLM_DEBATE_TELEGRAM_DURATION_SEC") or "0").strip()
    try:
        return int(raw)
    except ValueError:
        return 0


def get_running_llm_debate_telegram_pid() -> Optional[int]:
    """스케줄·텔레그램 공통 추적 PID (하위 호환 이름)."""
    return get_running_debate_scheduler_child_pid()


def start_llm_debate_telegram_process() -> tuple[bool, str]:
    with debate_spawn_lock():
        running = get_running_debate_scheduler_child_pid()
        if running is not None:
            return (
                False,
                f"이미 논문 토론 배치가 실행 중입니다. (pid={running}, 스케줄·텔레그램 공통)",
            )

        if not LLM_DEBATE_SCHEDULER_PATH.is_file():
            return False, f"스크립트 없음: {LLM_DEBATE_SCHEDULER_PATH}"

        duration = _telegram_debate_duration_sec()
        try:
            LLM_DEBATE_TELEGRAM_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(LLM_DEBATE_TELEGRAM_LOG_PATH, "a", encoding="utf-8") as log_file:
                log_file.write("\n" + "=" * 60 + "\n")
                log_file.write(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [telegram] "
                    f"llm_debate_scheduler.py --test --duration-sec {duration} "
                    f"({'시간제한없음' if duration <= 0 else f'{duration}s'})\n"
                )
                log_file.write("=" * 60 + "\n")
                log_file.flush()
                cmd = [
                    sys.executable,
                    "-u",
                    str(LLM_DEBATE_SCHEDULER_PATH),
                    "--test",
                    "--duration-sec",
                    str(duration),
                ]
                if duration <= 0:
                    # 무제한 모드라도 큐를 모두 소진하면 자동 종료하도록 한다.
                    cmd.append("--stop-on-empty")
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(PROJECT_ROOT),
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                    env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"},
                )
            register_debate_child_pid(proc.pid)
            if duration <= 0:
                detail = (
                    f"논문 토론 배치를 백그라운드에서 시작했습니다. "
                    f"(pid={proc.pid}, 시간 제한 없음 · 큐 소진 시 자동 종료 또는 `/debate_stop`)"
                )
            else:
                h = duration / 3600
                detail = f"논문 토론 배치를 백그라운드에서 시작했습니다. (pid={proc.pid}, 최대 약 {h:.1f}시간)"
            return (True, detail)
        except Exception as e:
            return False, f"시작 실패: {str(e)[:200]}"


def stop_llm_debate_telegram_process() -> tuple[bool, str]:
    with debate_spawn_lock():
        pid = get_running_debate_scheduler_child_pid()
        if not pid:
            return (
                False,
                "실행 중인 논문 토론 배치가 없습니다. (스케줄·텔레그램 공통 PID 없음, 수동 nohup 이면 터미널에서 종료)",
            )

        try:
            os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        except Exception:
            try:
                os.kill(pid, signal.SIGTERM)
            except Exception as e:
                return False, f"중지 실패: {str(e)[:200]}"

        clear_all_debate_child_pid_files()
        return True, f"논문 토론 배치를 중지했습니다. (pid={pid})"
