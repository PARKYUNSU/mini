#!/usr/bin/env python3
"""
스케줄 작업 실행기. run_scheduler에서 due job 발생 시
LangGraph 워크플로우를 실행하고 결과를 텔레그램으로 전송합니다.
"""
import os
import sqlite3
import sys
from pathlib import Path

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")


def run_scheduled_job(prompt: str, chat_id: str) -> str:
    """
    prompt를 LangGraph에 주입해 실행하고, 결과를 텔레그램으로 전송.
    Returns: "ok" 또는 에러 메시지
    """
    from dotenv import load_dotenv
    load_dotenv()

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        return "TELEGRAM_TOKEN이 설정되지 않았습니다."

    from agent_bot import build_graph
    from agent_config import CHECKPOINT_DB_PATH
    from agent_telegram import safe_telegram_send
    from langgraph.checkpoint.sqlite import SqliteSaver

    try:
        conn = sqlite3.connect(CHECKPOINT_DB_PATH, check_same_thread=False)
        graph = build_graph(checkpointer=SqliteSaver(conn))

        cfg = {
            "configurable": {
                "thread_id": f"tg_sched_{chat_id}_{os.urandom(4).hex()}",
                "chat_id": chat_id,
                "bot": None,
                "is_scheduled": True,  # planner 경로 차단 → direct_answer/use_existing_tool만 사용
            }
        }

        init_state = {
            "user_request": prompt,
            "route_type": "",
            "direct_response": "",
            "plan": [],
            "approval_status": "pending",
            "generated_code": "",
            "execution_result": "",
            "retry_count": 0,
            "error_hint": "",
        }

        final_state = graph.invoke(init_state, cfg)
        values = final_state if isinstance(final_state, dict) else getattr(final_state, "values", final_state) or {}

        direct_resp = values.get("direct_response", "")
        exec_result = values.get("execution_result", "")
        out = (direct_resp or exec_result or "실행 완료 (출력 없음)").strip()

        bot = __import__("telebot").TeleBot(token)
        if not safe_telegram_send(bot, chat_id, f"⏰ **스케줄 실행**\n\n{out[:3500]}", parse_mode="Markdown"):
            safe_telegram_send(bot, chat_id, f"⏰ 스케줄 실행\n\n{out[:4000]}")

        return "ok"
    except Exception as e:
        import traceback
        err = str(e)[:300]
        print(f"[agent_scheduled_runner] 오류: {e}\n{traceback.format_exc()}")
        try:
            from agent_telegram import safe_telegram_send
            bot = __import__("telebot").TeleBot(token)
            safe_telegram_send(bot, chat_id, f"⚠️ 스케줄 실행 오류: {err[:200]}")
        except Exception:
            pass
        return f"오류: {err}"
