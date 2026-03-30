#!/usr/bin/env python3
"""
통합 스케줄러 - M2 맥 미니 24시간 운영용
- arXiv 파이프라인: 매일 06:00
- LLM 토론 배치: 월~금 02:00 각 1회 (LLM_DEBATE_BATCH_DURATION_SEC: 0=무제한 시 **백그라운드 기동**으로 메인 스케줄 루프 비블로킹)
- cron_engine: 1분마다 due job 체크 → LangGraph 트리거 → 텔레그램 선톡 (agent_bot 단독 실행 시에도 동일 worker 가 뜸, 락으로 중복 방지)
- 메인 봇(agent_bot.py)은 별도 프로세스로 실행
"""

import os
import subprocess
import sys

# cron/nohup 환경에서 부모 stdio가 닫혀 있으면 자식(main.py 등)이 exit 1·Bad file descriptor 낼 수 있음
_SUBPROCESS_KWARGS = {"stdin": subprocess.DEVNULL}
import time
from pathlib import Path

import schedule
from dotenv import load_dotenv

from retry_utils import with_scheduler_retry

load_dotenv()

# 프로젝트 루트 기준
PROJECT_ROOT = Path(__file__).resolve().parent

sys.path.insert(0, str(PROJECT_ROOT))
from agent_config import get_gemini_api_keys  # noqa: E402
from agent_cron_worker import start_cron_worker_daemon  # noqa: E402
from llm_debate_spawn_guard import (  # noqa: E402
    clear_debate_child_pid_if_matches,
    get_running_debate_scheduler_child_pid,
    register_debate_child_pid,
)
# llm_debate_scheduler.DEBATE_SCHEDULE_WEEKDAYS 와 동일하게 유지
_DEBATE_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday")


def _llm_debate_batch_duration_sec() -> int:
    """0 이하 = 시간 제한 없음. 미설정 시 0."""
    raw = (os.getenv("LLM_DEBATE_BATCH_DURATION_SEC") or "0").strip()
    try:
        return int(raw)
    except ValueError:
        return 0


@with_scheduler_retry("arXiv 파이프라인")
def run_arxiv_pipeline() -> None:
    """main.py 실행 (arXiv 수집 → RAG → raw_data_queue). 네트워크 에러 시 재시도 후 텔레그램 알림."""
    print("\n" + "=" * 60)
    print("📚 [스케줄] arXiv 파이프라인 실행")
    print("=" * 60)
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "main.py")],
        cwd=PROJECT_ROOT,
        check=True,
        **_SUBPROCESS_KWARGS,
    )


def _spawn_llm_debate_batch_background(duration_sec: int) -> None:
    """
    무제한(또는 장시간) 배치는 subprocess.run으로 기다리지 않고 기동만 함.
    schedule.run_pending()·cron 1분 루프가 막히지 않도록 함.
    """
    running = get_running_debate_scheduler_child_pid()
    if running is not None:
        print(
            f"   ⏭️ 논문 토론 배치가 이미 실행 중(pid={running}, 스케줄·텔레그램 공통) — 중복 기동 생략",
            flush=True,
        )
        return

    cmd = [
        sys.executable,
        "-u",
        str(PROJECT_ROOT / "llm_debate_scheduler.py"),
        "--test",
        "--duration-sec",
        str(duration_sec),
    ]
    log_path = PROJECT_ROOT / ".cron" / "llm_debate_batch_stdout.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(f"\n{'=' * 60}\n[{stamp}] run_scheduler → Popen: {' '.join(cmd[2:])}\n")
        logf.flush()
        proc = subprocess.Popen(
            cmd,
            cwd=PROJECT_ROOT,
            stdin=subprocess.DEVNULL,
            stdout=logf,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        logf.write(f"child_pid={proc.pid}\n")
        logf.flush()
    register_debate_child_pid(proc.pid)
    rel = log_path.relative_to(PROJECT_ROOT)
    print(f"   백그라운드 PID={proc.pid} (로그: {rel}, pid: .cron/llm_debate_child.pid)", flush=True)


@with_scheduler_retry("LLM 토론 배치")
def run_llm_debate() -> None:
    """llm_debate_scheduler.py --test. duration>0 만 동기 대기(재시도 적용). duration<=0 은 백그라운드."""
    d = _llm_debate_batch_duration_sec()
    print("\n" + "=" * 60)
    print("🚀 [스케줄] LLM 토론 배치 실행")
    if d <= 0:
        print("   (시간 제한 없음 → 백그라운드 기동, LLM_DEBATE_BATCH_DURATION_SEC=0 또는 미설정)")
    else:
        print(f"   (동기 실행, 최대 {d}초 ≈ {d / 3600:.2f}시간)")
    print("=" * 60)
    if d <= 0:
        _spawn_llm_debate_batch_background(0)
        return
    running = get_running_debate_scheduler_child_pid()
    if running is not None:
        print(
            f"   ⏭️ 논문 토론 배치가 이미 실행 중(pid={running}) — 동기 배치 생략",
            flush=True,
        )
        return
    cmd = [
        sys.executable,
        "-u",
        str(PROJECT_ROOT / "llm_debate_scheduler.py"),
        "--test",
        "--duration-sec",
        str(d),
    ]
    proc = subprocess.Popen(cmd, cwd=PROJECT_ROOT, **_SUBPROCESS_KWARGS)
    register_debate_child_pid(proc.pid)
    try:
        rc = proc.wait()
    finally:
        clear_debate_child_pid_if_matches(proc.pid)
    if rc != 0:
        raise subprocess.CalledProcessError(rc, cmd)


def main() -> None:
    # Gemini 없어도 cron_engine(봇 스케줄)은 돌아야 함. 예전에는 여기서 return 해 Ollama 전용일 때 job이 영원히 안 돌았음.
    if get_gemini_api_keys():
        schedule.every().day.at("06:00").do(run_arxiv_pipeline)
        for _day in _DEBATE_WEEKDAYS:
            getattr(schedule.every(), _day).at("02:00").do(run_llm_debate)
    else:
        print(
            "⚠️ Gemini API 키 없음 — arXiv(06:00)·LLM토론(월~금 02:00)만 건너뜁니다.\n"
            "   cron_engine(등록한 매일/주간 작업)은 계속 동작합니다."
        )

    # cron_engine: 1분마다 due job 체크 (agent_bot 과 중복 시 파일 락으로 1곳만 실행)
    start_cron_worker_daemon(respect_agent_disable_env=False)

    print("📅 통합 스케줄러 시작")
    if get_gemini_api_keys():
        print("   - arXiv 파이프라인: 매일 06:00")
        _bd = _llm_debate_batch_duration_sec()
        _bmsg = (
            "시간 제한 없음(백그라운드·.cron/llm_debate_batch_stdout.log)"
            if _bd <= 0
            else f"동기 최대 {_bd}s"
        )
        print(f"   - LLM 토론: 월~금 02:00 (주 5회, {_bmsg} · LLM_DEBATE_BATCH_DURATION_SEC)")
    print("   - cron_engine: 1분마다 due job 체크 → 텔레그램 선톡")
    print("   - 메인 봇: 별도 터미널에서 python agent_bot.py")
    print("   Ctrl+C로 종료\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
