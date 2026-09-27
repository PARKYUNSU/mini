#!/usr/bin/env python3
"""
스케줄 작업 실행기. run_scheduler에서 due job 발생 시
LangGraph 워크플로우를 실행하고 결과를 텔레그램으로 전송합니다.
"""
import os
import sqlite3
import sys
import time
from pathlib import Path

# 프로젝트 루트 (mini/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")


_SCHEDULE_OUTPUT_KO_SUFFIX = (
    "\n\n[출력 언어·예약 발송] 이 요청은 텔레그램 예약(크론) 알림입니다. "
    "최종 답변은 **한국어 문장만** 사용하고, 웹 검색·스니펫이 영어면 **한글로 번역**해 전달하세요."
)

# 동일 채팅에 스케줄 실패 알림이 여러 작업·재시도로 동시에 쏟아지는 것 방지
_schedule_fail_notify_ts: dict[str, float] = {}


def _schedule_failure_telegram_allowed(chat_id: str) -> bool:
    try:
        cool = float((os.getenv("SCHEDULE_FAILURE_TELEGRAM_COOLDOWN_SEC") or "600").strip())
    except ValueError:
        cool = 600.0
    cool = max(30.0, min(cool, 86400.0))
    now = time.time()
    last = _schedule_fail_notify_ts.get(chat_id, 0.0)
    if now - last < cool:
        print(
            f"[agent_scheduled_runner] 스케줄 실패 텔레그램 쿨다운 ({cool:.0f}s) — chat_id={chat_id} 알림 생략",
            flush=True,
        )
        return False
    _schedule_fail_notify_ts[chat_id] = now
    if len(_schedule_fail_notify_ts) > 500:
        cutoff = now - cool * 2
        for k, t in list(_schedule_fail_notify_ts.items()):
            if t < cutoff:
                del _schedule_fail_notify_ts[k]
    return True


def run_scheduled_job(prompt: str, chat_id: str) -> str:
    """
    prompt를 LangGraph에 주입해 실행하고, 결과를 텔레그램으로 전송.
    Returns: "ok" 또는 에러 메시지
    """
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env", override=True)
    load_dotenv()

    prompt_eff = prompt.strip()
    if prompt_eff:
        prompt_eff = prompt_eff + _SCHEDULE_OUTPUT_KO_SUFFIX

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        return "TELEGRAM_TOKEN이 설정되지 않았습니다."

    try:
        from core.graph.agent_graph import build_graph
        from core.config.agent_config import CHECKPOINT_DB_PATH
        from apps.telegram_bot.agent_telegram import safe_telegram_send
        from langgraph.checkpoint.sqlite import SqliteSaver
    except Exception as e:
        return f"import 오류: {e!r}"

    try:
        try:
            _sq_timeout = float((os.getenv("CHECKPOINT_SQLITE_TIMEOUT_SEC") or "60").strip())
        except ValueError:
            _sq_timeout = 60.0
        _sq_timeout = max(5.0, min(_sq_timeout, 300.0))
        conn = sqlite3.connect(
            CHECKPOINT_DB_PATH,
            check_same_thread=False,
            timeout=_sq_timeout,
        )
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
            "user_request": prompt_eff,
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
        # Telegram 레거시 Markdown은 ** 볼드를 지원하지 않아 400 엔티티 오류가 나기 쉬움 → 평문만 사용
        body = f"⏰ 스케줄 실행\n\n{out[:4000]}"
        if not safe_telegram_send(bot, chat_id, body, parse_mode=None):
            print(f"[agent_scheduled_runner] 텔레그램 전송 실패 chat_id={chat_id}", flush=True)
            return "텔레그램 전송 실패"

        return "ok"
    except Exception as e:
        import traceback
        err = str(e)[:300]
        print(f"[agent_scheduled_runner] 오류: {e}\n{traceback.format_exc()}")
        try:
            if _schedule_failure_telegram_allowed(chat_id):
                from apps.telegram_bot.agent_telegram import safe_telegram_send

                bot = __import__("telebot").TeleBot(token)
                hint = ""
                el = err.lower()
                if "disk i/o" in el or "unable to open database" in el:
                    hint = (
                        "\n(체크포인트 DB가 외장 디스크면 내장 경로로 옮기세요: .env 에 "
                        "CHECKPOINT_DB_PATH=/Users/…/agent_checkpoints.db)"
                    )
                safe_telegram_send(
                    bot,
                    chat_id,
                    f"⚠️ 스케줄 실행 오류: {err[:200]}{hint}",
                    parse_mode=None,
                )
        except Exception:
            pass
        return f"오류: {err}"
