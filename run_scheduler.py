#!/usr/bin/env python3
"""
통합 스케줄러 - M2 맥 미니 24시간 운영용
- arXiv 파이프라인: 매일 06:00
- LLM 토론 배치: 매주 토요일 02:00 (2시간)
- cron_engine: 1분마다 due job 체크 → LangGraph 트리거 → 텔레그램 선톡
- 메인 봇(agent_bot.py)은 별도 프로세스로 실행
"""

import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import schedule
from dotenv import load_dotenv

from retry_utils import with_scheduler_retry

load_dotenv()

# 프로젝트 루트 기준
PROJECT_ROOT = Path(__file__).resolve().parent


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
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ .env에 GEMINI_API_KEY를 설정하세요.")
        return

    # 매일 06:00 - arXiv 파이프라인
    schedule.every().day.at("06:00").do(run_arxiv_pipeline)

    # 매주 토요일 02:00 - LLM 토론 (2시간 배치)
    schedule.every().saturday.at("02:00").do(run_llm_debate)

    # cron_engine: 1분마다 due job 체크 → 윤수르 LangGraph 트리거 → 텔레그램 선톡
    cron_thread = threading.Thread(target=_cron_worker_loop, daemon=True)
    cron_thread.start()

    print("📅 통합 스케줄러 시작")
    print("   - arXiv 파이프라인: 매일 06:00")
    print("   - LLM 토론: 매주 토요일 02:00")
    print("   - cron_engine: 1분마다 due job 체크 → 텔레그램 선톡")
    print("   - 메인 봇: 별도 터미널에서 python agent_bot.py")
    print("   Ctrl+C로 종료\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
