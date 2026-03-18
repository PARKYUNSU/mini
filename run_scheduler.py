#!/usr/bin/env python3
"""
통합 스케줄러 - M2 맥 미니 24시간 운영용
- arXiv 파이프라인: 매일 06:00
- LLM 토론 배치: 매주 토요일 02:00 (2시간)
- 메인 봇(agent_bot.py)은 별도 프로세스로 실행
"""

import os
import subprocess

from dotenv import load_dotenv

load_dotenv()
import sys
import time
from pathlib import Path

import schedule

# 프로젝트 루트 기준
PROJECT_ROOT = Path(__file__).resolve().parent


def run_arxiv_pipeline() -> None:
    """main.py 실행 (arXiv 수집 → RAG → raw_data_queue)"""
    print("\n" + "=" * 60)
    print("📚 [스케줄] arXiv 파이프라인 실행")
    print("=" * 60)
    try:
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "main.py")],
            cwd=PROJECT_ROOT,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ arXiv 파이프라인 실패: {e}")
    except Exception as e:
        print(f"❌ 예외: {e}")


def run_llm_debate() -> None:
    """llm_debate_scheduler.py --test 실행 (2시간 배치)"""
    print("\n" + "=" * 60)
    print("🚀 [스케줄] LLM 토론 배치 실행")
    print("=" * 60)
    try:
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "llm_debate_scheduler.py"), "--test"],
            cwd=PROJECT_ROOT,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ LLM 토론 실패: {e}")
    except Exception as e:
        print(f"❌ 예외: {e}")


def main() -> None:
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ .env에 GEMINI_API_KEY를 설정하세요.")
        return

    # 매일 06:00 - arXiv 파이프라인
    schedule.every().day.at("06:00").do(run_arxiv_pipeline)

    # 매주 토요일 02:00 - LLM 토론 (2시간 배치)
    schedule.every().saturday.at("02:00").do(run_llm_debate)

    print("📅 통합 스케줄러 시작")
    print("   - arXiv 파이프라인: 매일 06:00")
    print("   - LLM 토론: 매주 토요일 02:00")
    print("   - 메인 봇: 별도 터미널에서 python agent_bot.py")
    print("   Ctrl+C로 종료\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
