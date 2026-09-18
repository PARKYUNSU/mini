"""
LangGraph 한 턴 실행 (텔레그램 봇 객체 선택).

- agent_bot 단일 프로세스: bot 실객체 + bridge_job_id=None
- ai_worker 브리지: bot=None, bridge_job_id 로 결과를 SQLite 브리지에 기록
"""

from __future__ import annotations

import time
import traceback
from pathlib import Path
from typing import Any, Optional

from langgraph.types import Command

from core.bridge.agent_bridge_queue import (
    complete_job,
    fail_job,
    set_approval_pending,
    set_approval_session,
)
from core.graph.agent_hitl_state import pending_approvals
from core.graph.agent_nodes import _is_execution_failure
from core.session.agent_session import (
    AgentSkillLibrary,
    append_learning,
    get_session,
    remember_tool,
)
from core.graph.agent_types import STREAM_FAILURE_TELEGRAM_MSG


def execute_graph_turn(
    graph: Any,
    *,
    chat_id: str,
    user_text: str,
    thread_id: str | None,
    bot: Any,
    status_msg: Any,
    image_base64: Optional[str],
    is_resume: bool,
    config: Optional[dict],
    bridge_job_id: Optional[int] = None,
) -> None:
    from apps.telegram_bot.agent_telegram import (
        cleanup_status_message as _cleanup_status_msg,
        is_transient_network_error as _is_transient_error,
        notify_chat_error as _notify_chat_error,
        safe_telegram_edit as _safe_telegram_edit,
        safe_telegram_send as _safe_telegram_send,
    )
    from core.config.agent_config import LLM_RETRY_DELAY_SEC, LLM_RETRY_MAX

    print(
        f"[DEBUG] execute_graph_turn: bridge_job_id={bridge_job_id} bot={bool(bot)} is_resume={is_resume}",
        flush=True,
    )

    bridge_plan_sink: dict[str, Any] = {}
    tid = thread_id or f"tg_{chat_id}"
    if config is not None:
        cfg = config
        if bridge_job_id is not None:
            cfg = {
                "configurable": {
                    **(config.get("configurable") or {}),
                    "bot": None,
                    "bridge_plan_sink": bridge_plan_sink,
                }
            }
    else:
        cfg = {
            "configurable": {
                "thread_id": tid,
                "chat_id": chat_id,
                "bot": bot,
                **({"bridge_plan_sink": bridge_plan_sink} if bridge_job_id is not None else {}),
            }
        }
        if bridge_job_id is not None:
            cfg["configurable"]["bot"] = None

    stream_user_notified = False
    try:
        for attempt in range(LLM_RETRY_MAX):
            try:
                if is_resume:
                    for event in graph.stream(Command(resume=user_text), cfg, stream_mode="updates"):
                        if status_msg and bot:
                            try:
                                bot.send_chat_action(chat_id, "typing")
                            except Exception:
                                pass
                        for node_name, node_state in event.items():
                            if bot and status_msg:
                                if node_name == "planner_debate":
                                    _safe_telegram_edit(
                                        bot, "🧠 계획을 내부 검토 중입니다...", chat_id, status_msg.message_id
                                    )
                                elif node_name == "executor":
                                    _safe_telegram_edit(
                                        bot, "💻 Groq(Llama)가 코드를 작성 중입니다...", chat_id, status_msg.message_id
                                    )
                                elif node_name == "monitor":
                                    is_retry = "retry_count" in (node_state or {})
                                    txt = (
                                        "🚨 에러 발생! 코드를 스스로 수정하고 재시도합니다..."
                                        if is_retry
                                        else "🔍 샌드박스에서 코드를 테스트 중입니다..."
                                    )
                                    _safe_telegram_edit(bot, txt, chat_id, status_msg.message_id)
                else:
                    init_state: dict[str, Any] = {
                        "user_request": user_text,
                        "route_type": "",
                        "direct_response": "",
                        "plan": [],
                        "approval_status": "pending",
                        "generated_code": "",
                        "execution_result": "",
                        "retry_count": 0,
                        "error_hint": "",
                    }
                    if image_base64:
                        init_state["image_base64"] = image_base64
                    for event in graph.stream(init_state, cfg, stream_mode="updates"):
                        if not status_msg or not bot:
                            continue
                        if "router" in event:
                            rpatch = event.get("router") or {}
                            rt = rpatch.get("route_type") if isinstance(rpatch, dict) else None
                            if rt == "planner":
                                _safe_telegram_edit(
                                    bot,
                                    "📋 실행 계획 수립 중... (논문·도구 RAG + 로컬 LLM, 최대 ~2분)\n"
                                    "승인 전까지 화면이 그대로여도 정상입니다.",
                                    chat_id,
                                    status_msg.message_id,
                                )
                            elif rt == "direct_answer":
                                _safe_telegram_edit(bot, "✍️ 답변을 작성하는 중입니다...", chat_id, status_msg.message_id)
                            elif rt == "code_run":
                                _safe_telegram_edit(
                                    bot,
                                    "💻 코드 작성·실행 중... (승인 생략, RAG·계획 단계 생략)",
                                    chat_id,
                                    status_msg.message_id,
                                )
                            elif rt == "use_existing_tool":
                                _safe_telegram_edit(
                                    bot, "🔧 저장된 도구를 실행하는 중입니다...", chat_id, status_msg.message_id
                                )
                            else:
                                _safe_telegram_edit(bot, "🔍 요청 분류 중...", chat_id, status_msg.message_id)
                        elif "direct_answer" in event:
                            _safe_telegram_edit(bot, "✍️ 답변을 작성하는 중입니다...", chat_id, status_msg.message_id)
                        elif "use_existing_tool" in event:
                            _safe_telegram_edit(bot, "🔧 저장된 도구를 실행하는 중입니다...", chat_id, status_msg.message_id)
                        elif "planner" in event:
                            _safe_telegram_edit(
                                bot,
                                "📋 실행 계획을 세우는 중입니다... (RAG·LLM, 최대 1~2분)",
                                chat_id,
                                status_msg.message_id,
                            )
                        elif "planner_debate" in event:
                            _safe_telegram_edit(bot, "🧠 계획을 내부 검토 중입니다...", chat_id, status_msg.message_id)
                        elif "executor" in event:
                            _safe_telegram_edit(bot, "💻 코드를 작성·실행하는 중입니다...", chat_id, status_msg.message_id)
                        elif "monitor" in event:
                            is_retry = "retry_count" in (event.get("monitor") or {})
                            txt = (
                                "🚨 오류 분석 후 재시도 중입니다..."
                                if is_retry
                                else "🔍 실행 결과를 검증하는 중입니다..."
                            )
                            _safe_telegram_edit(bot, txt, chat_id, status_msg.message_id)

                break
            except Exception as e:
                if _is_transient_error(e) and attempt < LLM_RETRY_MAX - 1:
                    print(f"[DEBUG] 일시적 오류 재시도 ({attempt+1}/{LLM_RETRY_MAX}): {e}")
                    time.sleep(LLM_RETRY_DELAY_SEC)
                else:
                    stream_user_notified = True
                    if bridge_job_id is not None:
                        fail_job(bridge_job_id, f"{type(e).__name__}: {e}")
                        return
                    if status_msg and bot:
                        _safe_telegram_edit(bot, STREAM_FAILURE_TELEGRAM_MSG, chat_id, status_msg.message_id)
                    elif bot:
                        _safe_telegram_send(bot, chat_id, STREAM_FAILURE_TELEGRAM_MSG)
                    raise

        state = graph.get_state(cfg)
        values = state.values if hasattr(state, "values") else {}
        if state.next:
            print("[DEBUG] execute_graph_turn: interrupt(승인대기)", flush=True)
            if bridge_job_id is not None:
                plan = (
                    bridge_plan_sink.get("last_plan_markdown")
                    or "📋 계획이 준비되었습니다. **승인** 또는 **거절** 로 답해 주세요."
                )
                set_approval_pending(bridge_job_id, plan_text=plan)
                set_approval_session(chat_id, str(cfg["configurable"]["thread_id"]), bridge_job_id)
            else:
                pending_approvals[chat_id] = (cfg["configurable"]["thread_id"], cfg)
                if status_msg and bot:
                    _safe_telegram_edit(
                        bot,
                        "⏳ 실행 계획이 준비되었습니다. 승인 또는 거절을 눌러 주세요.",
                        chat_id,
                        status_msg.message_id,
                    )
            return

        if chat_id in pending_approvals and bridge_job_id is None:
            del pending_approvals[chat_id]

        session = get_session(chat_id)
        user_msg_for_memory = values.get("user_request", user_text) if is_resume else user_text
        session.add_turn(user_msg_for_memory, "")

        fatal = (values.get("agent_fatal_error") or "").strip()
        if fatal:
            if bridge_job_id is not None:
                complete_job(bridge_job_id, result_text=f"🚨 처리 중 오류\n\n{fatal[:3500]}", result_parse_mode=None)
            else:
                _cleanup_status_msg(bot, chat_id, status_msg)
                mid = getattr(status_msg, "message_id", None) if status_msg else None
                if not _notify_chat_error(
                    bot, chat_id, headline="🚨 처리 중 오류", detail=fatal[:900], status_message_id=mid
                ):
                    _notify_chat_error(
                        bot, chat_id, headline="🚨 처리 중 오류", detail=fatal[:900], status_message_id=None
                    )
            session.recent_messages[-1] = (session.recent_messages[-1][0], fatal[:500])
            session.save()
            return

        route_type = values.get("route_type", "")
        direct_resp = values.get("direct_response", "")
        if route_type == "direct_answer" and direct_resp:
            if bridge_job_id is not None:
                rchoice = values.get("router_choice", "")
                # B=RAG는 direct_answer 노드가 Telegram HTML로 통일 저장. A=일상 등은 Markdown 시도.
                _pm = "HTML" if rchoice == "B" else "Markdown"
                complete_job(bridge_job_id, result_text=direct_resp, result_parse_mode=_pm)
            else:
                _cleanup_status_msg(bot, chat_id, status_msg)
            session.recent_messages[-1] = (session.recent_messages[-1][0], direct_resp[:500])
            session.maybe_compress()
            session.save()
            return

        if route_type == "use_existing_tool":
            if bridge_job_id is None:
                _cleanup_status_msg(bot, chat_id, status_msg)
            result = values.get("execution_result", "")
            used_tool_name = values.get("used_tool_name", "")
            if used_tool_name:
                remember_tool(chat_id, used_tool_name, user_msg_for_memory)
            if bridge_job_id is not None:
                header = "📰 IT 뉴스 요약" if any(
                    k in (user_msg_for_memory or "") for k in ("뉴스", "news", "최신", "오늘")
                ) else ("🔍 웹 검색 결과" if used_tool_name == "tavily_search_tool" else "🔧 기존 도구 실행 결과")
                complete_job(bridge_job_id, result_text=f"{header}\n\n{result[:4000]}", result_parse_mode=None)
            session.recent_messages[-1] = (session.recent_messages[-1][0], result[:500])
            session.maybe_compress()
            session.save()
            return

        if values.get("approval_status") == "rejected":
            msg = "❌ 거절되었습니다. 계획이 취소되었습니다."
            if bridge_job_id is not None:
                complete_job(bridge_job_id, result_text=msg, result_parse_mode=None)
            else:
                _cleanup_status_msg(bot, chat_id, status_msg)
                _safe_telegram_send(bot, chat_id, msg)
            session.recent_messages[-1] = (session.recent_messages[-1][0], "거절되었습니다.")
            session.save()
            return

        code = values.get("generated_code", "")
        result = values.get("execution_result", "")
        request = values.get("user_request", "")

        saved_tool = None
        retry_count = values.get("retry_count", 0)
        error_hint = values.get("error_hint", "")
        if code and not _is_execution_failure(result) and not values.get("skip_tool_save"):
            saved_tool = AgentSkillLibrary().save_tool(code, request)
            if saved_tool:
                remember_tool(chat_id, Path(saved_tool).stem, request)
                if retry_count > 0 and error_hint:
                    append_learning(request, error_hint, saved_tool)

        if bridge_job_id is None and status_msg and bot:
            try:
                bot.delete_message(chat_id, status_msg.message_id)
            except Exception:
                pass

        failed = _is_execution_failure(result)
        headline = "❌ **실행 실패**" if failed else "✅ **실행 완료**"
        out = f"{headline}\n\n```\n{result[:3500]}\n```"
        if saved_tool:
            out += f"\n\n📦 도구 저장됨: `agent_tools/{saved_tool}`"
        if code:
            out += f"\n\n📝 **생성된 코드**\n```python\n{code[:1500]}\n```"

        if bridge_job_id is not None:
            complete_job(bridge_job_id, result_text=out, result_parse_mode="Markdown")
        else:
            if not _safe_telegram_send(bot, chat_id, out, parse_mode="Markdown"):
                _safe_telegram_send(bot, chat_id, f"{'실행 실패' if failed else '실행 완료'}\n\n{result[:4000]}")

        session.recent_messages[-1] = (session.recent_messages[-1][0], result[:500])
        session.maybe_compress()
        session.save()

    except Exception as e:
        err_detail = str(e).strip()
        tb = traceback.format_exc()
        print(f"❌ 그래프 오류: {e}\n{tb}")
        if bridge_job_id is not None and not stream_user_notified:
            fail_job(bridge_job_id, f"{type(e).__name__}: {err_detail}")
            return
        if not stream_user_notified and bridge_job_id is None:
            from apps.telegram_bot.agent_telegram import notify_chat_error as _notify2

            mid = getattr(status_msg, "message_id", None) if status_msg else None
            headline = "🚨 처리 중 오류가 발생했습니다."
            detail = (err_detail or type(e).__name__)[:900]
            el = err_detail.lower()
            if "11434" in err_detail or "connectionerror" in el or "ollama" in el:
                headline = "⚠️ Ollama 연결 오류"
                detail = "Ollama 서버에 연결할 수 없습니다. `ollama serve` 실행 후 다시 시도해 주세요."
            elif _is_transient_error(e):
                headline = "⚠️ 일시적 연결 오류"
                detail = "네트워크 또는 API 일시 오류입니다. 잠시 후 다시 말씀해 주세요."
            elif "e2b" in el or "sandbox" in el:
                headline = "⚠️ 코드 샌드박스(E2B) 오류"
            elif "409" in err_detail or ("conflict" in el and "getupdates" in el):
                headline = "⚠️ 텔레그램 봇 충돌(409)"
                detail = "동일 봇 토큰으로 프로세스가 둘 이상 떠 있을 때 발생합니다."
            ok = _notify2(bot, chat_id, headline=headline, detail=detail, status_message_id=mid)
            if not ok:
                _notify2(bot, chat_id, headline=headline, detail=detail, status_message_id=None)
            raise

