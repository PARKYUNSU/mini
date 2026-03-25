#!/usr/bin/env python3
"""
통합 스케줄러 - M2 맥 미니 24시간 운영용
- arXiv 파이프라인: 매일 06:00
- LLM 토론 배치: 월~금 02:00 각 1회 (각 최대 2시간)
- cron_engine: 1분마다 due job 체크 → LangGraph 트리거 → 텔레그램 선톡
- 메인 봇(agent_bot.py)은 별도 프로세스로 실행
"""

import os
import subprocess
import sys

# cron/nohup 환경에서 부모 stdio가 닫혀 있으면 자식(main.py 등)이 exit 1·Bad file descriptor 낼 수 있음
_SUBPROCESS_KWARGS = {"stdin": subprocess.DEVNULL}
import threading
import time
from pathlib import Path

import schedule
from dotenv import load_dotenv

from retry_utils import with_scheduler_retry

load_dotenv()

# 프로젝트 루트 기준
PROJECT_ROOT = Path(__file__).resolve().parent
# llm_debate_scheduler.DEBATE_SCHEDULE_WEEKDAYS 와 동일하게 유지
_DEBATE_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday")


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


@with_scheduler_retry("LLM 토론 배치")
def run_llm_debate() -> None:
    """llm_debate_scheduler.py --test 실행 (2시간 배치). 네트워크 에러 시 재시도 후 텔레그램 알림."""
    print("\n" + "=" * 60)
    print("🚀 [스케줄] LLM 토론 배치 실행")
    print("=" * 60)
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "llm_debate_scheduler.py"), "--test"],
        cwd=PROJECT_ROOT,
        check=True,
        **_SUBPROCESS_KWARGS,
    )


def _cron_worker_loop() -> None:
    """1분마다 cron_engine의 due job 체크 → LangGraph 트리거 → 텔레그램 선톡"""
    sys.path.insert(0, str(PROJECT_ROOT))
    from agent_tools.cron_engine.cron_api import get_due_jobs, mark_job_run
    from agent_tools.cron_engine.lib.storage import append_job_run
    from agent_scheduled_runner import run_scheduled_job

    while True:
        try:
            due = get_due_jobs()
            for job in due:
                job_id = job.get("id")
                prompt = job.get("prompt") or job.get("title", "")
                chat_id = job.get("chat_id", "")
                started_at = time.time()

                def _log_run(status: str, error: str = None, message_preview: str = None):
                    evt = {
                        "event": "cron_job_run",
                        "job_id": job_id,
                        "chat_id": chat_id,
                        "status": status,
                        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(started_at)),
                        "duration_ms": int((time.time() - started_at) * 1000),
                    }
                    if message_preview:
                        evt["prompt_preview"] = message_preview[:80]
                    if error:
                        evt["error"] = error[:200]
                    append_job_run(evt)

                if not prompt or not chat_id:
                    mark_job_run(job_id)
                    _log_run("skipped", message_preview="prompt/chat_id 없음")
                    continue
                print(f"[cron] 실행: {job_id} → {prompt[:40]}... (chat={chat_id})")
                result = run_scheduled_job(prompt, chat_id)
                if result == "ok":
                    mark_job_run(job_id)
                    _log_run("succeeded", message_preview=prompt[:80])
                else:
                    _log_run("failed", error=str(result)[:200], message_preview=prompt[:80])
                    print(f"[cron] 실행 실패 (next_run 유지): {result}")
        except Exception as e:
            print(f"[cron] worker 예외: {e}")
        time.sleep(60)


def main() -> None:
    # Gemini 없어도 cron_engine(봇 스케줄)은 돌아야 함. 예전에는 여기서 return 해 Ollama 전용일 때 job이 영원히 안 돌았음.
    if os.getenv("GEMINI_API_KEY"):
        schedule.every().day.at("06:00").do(run_arxiv_pipeline)
        for _day in _DEBATE_WEEKDAYS:
            getattr(schedule.every(), _day).at("02:00").do(run_llm_debate)
    else:
        print(
            "⚠️ GEMINI_API_KEY 없음 — arXiv(06:00)·LLM토론(월~금 02:00)만 건너뜁니다.\n"
            "   cron_engine(등록한 매일/주간 작업)은 계속 동작합니다."
        )

    # cron_engine: 1분마다 due job 체크 → 윤수르 LangGraph 트리거 → 텔레그램 선톡
    cron_thread = threading.Thread(target=_cron_worker_loop, daemon=True)
    cron_thread.start()

    print("📅 통합 스케줄러 시작")
    if os.getenv("GEMINI_API_KEY"):
        print("   - arXiv 파이프라인: 매일 06:00")
        print("   - LLM 토론: 월~금 02:00 (주 5회)")
    print("   - cron_engine: 1분마다 due job 체크 → 텔레그램 선톡")
    print("   - 메인 봇: 별도 터미널에서 python agent_bot.py")
    print("   Ctrl+C로 종료\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
