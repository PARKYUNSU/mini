#!/usr/bin/env python3
"""
Multi-Agent 동적 코딩 텔레그램 봇
- Router(Qwen) → Direct Answer | Use Existing Tool | Planner(HITL) → Executor → Monitor
- 일상/RAG: 즉시 답변. 기존 도구: 즉시 실행. 새 코드: 승인 후 실행.
"""

import multiprocessing
import os
import sys

# macOS: fork + Objective-C 런타임 충돌 방지 (Chroma/토치 등 네이티브 스택에서 세그폴트 완화)
if sys.platform == "darwin":
    if multiprocessing.get_start_method(allow_none=True) != "spawn":
        multiprocessing.set_start_method("spawn", force=True)

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

import sqlite3
import subprocess
import time
import unicodedata
from pathlib import Path
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from langgraph.checkpoint.sqlite import SqliteSaver
import telebot
from telebot.types import ReplyKeyboardRemove

from apps.backfill.agent_backfill_telegram import start_backfill_process, stop_backfill_process
from apps.telegram_bot.agent_debate_telegram import (
    start_llm_debate_telegram_process,
    stop_llm_debate_telegram_process,
)
from core.rag.agent_chroma_rag import list_stored_papers_text, warmup_chroma_rag
from core.config.agent_config import (
    BACKFILL_LOG_PATH,
    CHECKPOINT_DB_PATH,
    GROQ_API_KEY,
    LLM_DEBATE_TELEGRAM_LOG_PATH,
    get_gemini_api_keys,
    LLM_RETRY_DELAY_SEC,
    LLM_RETRY_MAX,
    PROJECT_ROOT,
    TELEGRAM_TOKEN,
    ALLOWED_CHAT_ID,
)
from apps.scheduler.agent_cron_worker import start_cron_worker_daemon
from core.graph.agent_graph import build_graph
from core.graph.agent_hitl_state import pending_approvals as _pending_approvals, thread_version as _thread_version
from core.graph.agent_nodes import _run_tool_on_host
from core.graph.agent_worker_runner import execute_graph_turn
from core.session.agent_session import (
    clear_session,
    get_paper_mode as _get_paper_mode,
    get_session,
    remember_tool as _remember_tool,
    set_paper_mode as _set_paper_mode,
    stash_pending_image,
    take_pending_image,
    with_chat_lock as _with_chat_lock,
)
from core.rag.agent_tool_rag import sync_tool_chroma_from_disk
from apps.telegram_bot.agent_telegram import (
    CANCEL_RESTART_CMDS as _CANCEL_RESTART_CMDS,
    cleanup_status_message as _cleanup_status_msg,
    is_transient_network_error as _is_transient_error,
    main_keyboard as _main_keyboard,
    notify_chat_error as _notify_chat_error,
    safe_telegram_edit as _safe_telegram_edit,
    safe_telegram_send as _safe_telegram_send,
    safe_telegram_send_and_get as _safe_telegram_send_and_get,
    strip_wake_word as _strip_wake_word,
)
from core.llm.agent_vision import download_photo_to_base64 as _download_photo_to_base64, run_vision_analysis as _run_vision_analysis


# HITL 전역은 agent_hitl_state (단일 프로세스 모드)
_AGENT_BOT_LOCK_FD_HOLDER: list = []

_TELEGRAM_MSG_SOFT_LIMIT = 3800


def _should_notify_auto_cancel(new_text: str) -> bool:
    """
    승인 대기 중 새 입력이 들어와 자동 취소될 때의 사용자 알림 여부.
    기본은 조용히 재라우팅하고, 아주 짧은 혼란 표현일 때만 안내를 보낸다.
    """
    t = (new_text or "").strip()
    if not t:
        return False
    compact = t.replace(" ", "")
    if len(compact) <= 6 and any(k in compact for k in ("?", "왜", "뭐", "어")):
        return True
    return False


def _telegram_slash_command_token(text: str) -> str:
    """BOM·양방향 문자·전각 슬래시 정규화 후 첫 토큰 소문자 (/debate_start 등)."""
    t = unicodedata.normalize("NFKC", (text or "").strip()).lstrip("\ufeff\u200e\u200f").strip()
    if not t:
        return ""
    return t.split()[0].lower()


def _split_telegram_chunks(text: str, limit: int = _TELEGRAM_MSG_SOFT_LIMIT) -> list[str]:
    """텔레그램 한 메시지 상한(4096) 여유를 두고 줄 단위로 분할."""
    text = (text or "").strip()
    if not text:
        return ["(내용 없음)"]
    if len(text) <= limit:
        return [text]
    lines = text.split("\n")
    chunks: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for line in lines:
        add_len = len(line) + (1 if cur else 0)
        if cur and cur_len + add_len > limit:
            chunks.append("\n".join(cur))
            cur = [line]
            cur_len = len(line)
        else:
            if cur:
                cur_len += 1
            cur.append(line)
            cur_len += len(line)
    if cur:
        chunks.append("\n".join(cur))
    # 한 줄이 limit 초과인 경우(극단적 긴 제목 등)
    out: list[str] = []
    for c in chunks:
        if len(c) <= limit:
            out.append(c)
            continue
        start = 0
        while start < len(c):
            out.append(c[start : start + limit])
            start += limit
    return out


# ============ 단일 인스턴스 (Telegram 409 getUpdates 충돌 방지) ============
def _acquire_agent_bot_singleton_lock():
    """
    동일 머신에서 agent_bot.py 가 두 개 뜨면 Telegram API 409가 난다.
    non-Windows: flock으로 프로세스당 1개만 허용.
    """
    if sys.platform == "win32":
        return None
    import fcntl

    path = PROJECT_ROOT / ".agent_bot_singleton.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    fp = open(path, "a+", encoding="utf-8")
    try:
        fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        fp.close()
        print(
            "❌ agent_bot.py 가 이미 실행 중입니다. (중복 실행 시 Telegram 409: getUpdates 충돌)\n"
            "   분리 모드는 telegram_receiver / ai_worker 만 단일 실행하면 됩니다.\n"
            "   종료: pkill -f telegram_receiver  또는  pkill -f ai_worker"
        )
        sys.exit(1)
    fp.seek(0)
    fp.truncate()
    fp.write(str(os.getpid()))
    fp.flush()
    return fp


# ============ 텔레그램 봇 ============
def main():
    if not all([TELEGRAM_TOKEN, ALLOWED_CHAT_ID, GROQ_API_KEY]) or not get_gemini_api_keys():
        print(
            "❌ .env에 TELEGRAM_TOKEN, ALLOWED_CHAT_ID, GROQ_API_KEY, "
            "그리고 Gemini 키(GEMINI_API_KEY·GEMINI_API_KEY_2…_8 또는 GEMINI_API_KEYS)를 설정하세요."
            "\n   (Executor/Monitor는 Groq, 라우터·도구·Tavily 폴백은 Gemini를 사용합니다.)"
        )
        return
    if not os.getenv("E2B_API_KEY"):
        print("⚠️ E2B_API_KEY가 .env에 없습니다. Executor의 코드 실행이 실패합니다.")

    _lock_fp = _acquire_agent_bot_singleton_lock()
    if _lock_fp is not None:
        _AGENT_BOT_LOCK_FD_HOLDER.append(_lock_fp)
    allowed_ids = [a.strip() for a in ALLOWED_CHAT_ID.split(",")]
    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    # LangGraph SqliteSaver(checkpoint)가 먼저 열리면 일부 환경에서 Chroma Rust/sqlite와 충돌해
    # collection.query 직전 Segmentation fault가 난다. 논문 Chroma 워밍업을 그보다 먼저 둔다.
    try:
        sync_tool_chroma_from_disk()
    except Exception as e:
        print(f"⚠️ Tool RAG(tool_chroma_db) 초기 동기화 실패 — 빈 인덱스로 동작할 수 있습니다: {e}")

    try:
        warmup_chroma_rag()
        print("✅ Chroma RAG 워밍업 완료 (in-process 싱글톤 + threading.Lock 직렬화)")
    except Exception as e:
        print(f"⚠️ Chroma RAG 워밍업 실패 — 첫 RAG 질문 시 재시도: {e}")

    conn = sqlite3.connect(CHECKPOINT_DB_PATH, check_same_thread=False)
    graph = build_graph(checkpointer=SqliteSaver(conn))
    _executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="agent")

    # cron_engine: run_scheduler 없이 agent_bot 만 켜도 등록 스케줄이 돌아가게 함 (중복은 .cron/cron_worker.lock)
    start_cron_worker_daemon(respect_agent_disable_env=True)

    # 재시작 후: 체크포인트에서 승인 대기 중인 세션 복구
    for cid in allowed_ids:
        cfg = {"configurable": {"thread_id": f"tg_{cid}", "chat_id": cid, "bot": bot}}
        try:
            state = graph.get_state(cfg)
            if state and state.next:
                with _with_chat_lock(cid):
                    _pending_approvals[cid] = (cfg["configurable"]["thread_id"], cfg)
        except Exception:
            pass

    def run_or_resume(chat_id: str, user_text: str, thread_id: Optional[str] = None, config: Optional[dict] = None, is_resume: bool = False, status_msg=None, image_base64: Optional[str] = None):
        """image_base64: 직전 턴 이미지(문맥용). Vision 라우팅은 message.photo 있을 때만.
        chat_id 단위로 직렬화되어 동시에 2개 이상 실행되지 않음."""
        with _with_chat_lock(chat_id):
            _run_or_resume_body(chat_id, user_text, thread_id, config, is_resume, status_msg, image_base64, graph, bot)

    def _run_or_resume_body(chat_id: str, user_text: str, thread_id: Optional[str], config: Optional[dict], is_resume: bool, status_msg, image_base64: Optional[str], graph, bot):
        """run_or_resume 실제 로직. 호출 시 이미 _with_chat_lock(chat_id) 내부여야 함."""
        print(f"[DEBUG] run_or_resume: 진입 is_resume={is_resume}, image_ctx={bool(image_base64)}")
        if status_msg and bot:
            try:
                bot.send_chat_action(chat_id, "typing")
            except Exception:
                pass
        tid = thread_id or f"tg_{chat_id}"
        if not is_resume and _thread_version.get(chat_id, 0) > 0:
            tid = f"tg_{chat_id}_{_thread_version[chat_id]}"
        cfg = config if config else {"configurable": {"thread_id": tid, "chat_id": chat_id, "bot": bot}}
        execute_graph_turn(
            graph,
            chat_id=chat_id,
            user_text=user_text,
            thread_id=str(cfg["configurable"].get("thread_id") or tid),
            bot=bot,
            status_msg=status_msg,
            image_base64=image_base64,
            is_resume=is_resume,
            config=cfg,
            bridge_job_id=None,
        )

    @bot.message_handler(commands=["start"])
    def on_start(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return
        bot.reply_to(
            message,
            "🤖 **AI 에이전트 봇**\n\n질문을 보내 주세요. 아래 버튼으로 언제든 재시작·취소할 수 있어요.",
            parse_mode="Markdown",
            reply_markup=_main_keyboard(),
        )

    @bot.message_handler(commands=["reboot", "rebot"])
    def on_reboot(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return

        bot.reply_to(
            message,
            "🔄 마스터, 봇 프로세스를 재부팅합니다. 코드가 새로 적용되며 약 20초 후 다시 말을 걸어주세요."
        )
        try:
            mini_dir = Path(__file__).resolve().parent
            restart_script = mini_dir / "restart_bot.sh"
            restart_log = mini_dir / "restart.log"
            restart_log.parent.mkdir(parents=True, exist_ok=True)
            with open(restart_log, "a", encoding="utf-8") as log_file:
                subprocess.Popen(
                    ["bash", str(restart_script)],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    cwd=str(mini_dir),
                    start_new_session=True,
                )
        except Exception as e:
            print(f"🚨 /reboot 실행 실패: {e}\n{traceback.format_exc()}")

    @bot.message_handler(commands=["backfill_start"])
    def on_backfill_start(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return

        ok, detail = start_backfill_process()
        prefix = "🚀 마스터, " if ok else "⚠️ "
        bot.reply_to(
            message,
            f"{prefix}{detail}\n로그 파일: `{BACKFILL_LOG_PATH.name}`",
            parse_mode="Markdown",
        )

    @bot.message_handler(commands=["backfill_stop"])
    def on_backfill_stop(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return

        ok, detail = stop_backfill_process()
        prefix = "🛑 " if ok else "ℹ️ "
        bot.reply_to(message, f"{prefix}{detail}", parse_mode="Markdown")

    @bot.message_handler(commands=["debate_start", "논문토론시작"])
    def on_debate_start(message):
        """LLM 논문 토론 배치(llm_debate_scheduler --test) 백그라운드 시작."""
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return

        ok, detail = start_llm_debate_telegram_process()
        prefix = "🧪 " if ok else "⚠️ "
        bot.reply_to(
            message,
            f"{prefix}{detail}\n"
            f"로그: `{LLM_DEBATE_TELEGRAM_LOG_PATH.name}`\n"
            f"중지: `/debate_stop`",
            parse_mode="Markdown",
        )

    @bot.message_handler(commands=["debate_stop", "논문토론중지"])
    def on_debate_stop(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return

        ok, detail = stop_llm_debate_telegram_process()
        prefix = "🛑 " if ok else "ℹ️ "
        bot.reply_to(message, f"{prefix}{detail}", parse_mode="Markdown")

    @bot.message_handler(commands=["schedule", "스케줄"])
    def on_schedule(message):
        """등록된 스케줄 목록 조회"""
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return

        result = _run_tool_on_host("schedule_list_jobs", "등록된 스케줄 보여줘", chat_id)
        bot.reply_to(message, f"📅 등록된 스케줄\n\n{result[:4000]}")

    @bot.message_handler(commands=["papers", "paperlist", "논문목록"])
    def on_papers(message):
        """저장 큐(crawled_papers.jsonl) 기준 논문 ID·제목 목록"""
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return
        try:
            print(f"[papers] 요청 chat_id={chat_id} 처리 시작", flush=True)
            body = list_stored_papers_text()
            header = "📚 저장된 논문 (raw_data_queue/crawled_papers.jsonl)\n\n"
            full = header + body
            chunks = _split_telegram_chunks(full)
            total = len(chunks)
            for i, chunk in enumerate(chunks):
                prefix = f"({i + 1}/{total})\n" if total > 1 else ""
                payload = prefix + chunk
                if i == 0:
                    bot.reply_to(message, payload)
                else:
                    bot.send_message(chat_id, payload)
                if i < total - 1:
                    time.sleep(0.35)
            print(f"[papers] 완료 chat_id={chat_id} chunks={total}", flush=True)
        except Exception as e:
            print(f"[papers] 오류: {e}\n{traceback.format_exc()}", flush=True)
            try:
                bot.reply_to(message, f"⚠️ 목록 전송 실패: {str(e)[:500]}")
            except Exception:
                pass

    @bot.message_handler(content_types=["text", "photo"], func=lambda m: True)
    def handle(message):
        chat_id = str(message.chat.id)
        try:
            if chat_id not in allowed_ids:
                bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
                return

            # --------- 사진 메시지: Vision 전용 경로 (RAG/코딩 우회) ---------
            if message.photo:
                result = _download_photo_to_base64(bot, message)
                if not result:
                    bot.reply_to(message, "사진을 처리할 수 없습니다. 다시 시도해 주세요.")
                    return
                base64_image, user_request = result
                user_request = _strip_wake_word(user_request)

                status_msg = _safe_telegram_send_and_get(bot, chat_id, "👀 윤수르가 이미지를 분석 중입니다...")
                print(f"[DEBUG] Handler: 사진 수신, Vision 경로 진입 (caption={user_request[:50]}...)", flush=True)

                def _do_vision():
                    t_start = time.perf_counter()
                    try:
                        ans = _run_vision_analysis(bot, chat_id, user_request, base64_image, status_msg)
                        if status_msg:
                            if ans:
                                _safe_telegram_edit(bot, ans, chat_id, status_msg.message_id)
                            else:
                                _safe_telegram_edit(bot, "⚠️ 이미지 분석에 실패했습니다. 다시 시도해 주세요.", chat_id, status_msg.message_id)
                        if ans:
                            with _with_chat_lock(chat_id):
                                stash_pending_image(chat_id, base64_image)
                                session = get_session(chat_id)
                                session.add_turn(f"[이미지] {user_request}", ans)
                                session.maybe_compress()
                                session.save()
                        print(f"[DEBUG] Vision: 전체 소요 {time.perf_counter() - t_start:.2f}s", flush=True)
                    except Exception as e:
                        err_detail = str(e)[:300]
                        print(f"[DEBUG] Vision 스레드 예외: {e}\n{traceback.format_exc()}")
                        err_msg = "⚠️ Ollama 서버에 연결할 수 없습니다." if ("11434" in err_detail or "ConnectionError" in err_detail) else f"🚨 이미지 분석 오류: {str(e)[:200]}"
                        if status_msg:
                            _safe_telegram_edit(bot, err_msg, chat_id, status_msg.message_id)
                        else:
                            _safe_telegram_send(bot, chat_id, err_msg)

                _executor.submit(_do_vision)
                return

            # --------- 텍스트 메시지: 일반 Router 경로 (A/B/C). 과거 이미지는 문맥으로만 전달 ---------
            text = (message.text or "").strip()
            text = _strip_wake_word(text)
            print(f"[DEBUG] Handler: 메시지 수신, text={text[:60]}...")

            if not text:
                bot.reply_to(message, "메시지를 입력해 주세요.")
                return

            # /paper: 논문 모드 토글 (저장된 논문만 검색 vs 일반/웹 검색)
            cmd = text.strip().split()[0].lower() if text else ""
            if cmd == "/paper" or cmd.startswith("/paper@"):
                with _with_chat_lock(chat_id):
                    parts = text.strip().split()
                    if len(parts) >= 2:
                        sub = parts[1].lower()
                        if sub in ("on", "1", "켜", "켜줘"):
                            _set_paper_mode(chat_id, True)
                            bot.reply_to(message, "📚 논문 모드 ON. 논문 관련 질문을 저장된 논문(ChromaDB)에서 검색합니다. (인사·날씨·스케줄 등은 기존대로)")
                        elif sub in ("off", "0", "꺼", "꺼줘"):
                            _set_paper_mode(chat_id, False)
                            bot.reply_to(message, "🌐 논문 모드 OFF. 일반 답변 및 웹 검색을 사용합니다.")
                        else:
                            cur = _get_paper_mode(chat_id)
                            bot.reply_to(message, f"현재 논문 모드: {'ON' if cur else 'OFF'}\n사용법: /paper on | /paper off")
                    else:
                        cur = _get_paper_mode(chat_id)
                        _set_paper_mode(chat_id, not cur)
                        status = "ON" if not cur else "OFF"
                        bot.reply_to(message, f"📚 논문 모드 {status}. {'논문 관련 질문을 저장된 논문에서 검색합니다.' if not cur else '일반/웹 검색을 사용합니다.'}")
                return

            # /debate_* : 그룹 등에서 command 엔티티가 아닌 일반 텍스트로 올 때 commands= 핸들러가
            # 건너뛰어 Router로 가는 경우가 있어, /paper 와 같이 여기서도 처리한다.
            cmd0 = _telegram_slash_command_token(text)
            if cmd0 in ("/debate_start", "/논문토론시작") or (
                cmd0.startswith("/debate_start@") and "@" in cmd0
            ):
                ok, detail = start_llm_debate_telegram_process()
                prefix = "🧪 " if ok else "⚠️ "
                bot.reply_to(
                    message,
                    f"{prefix}{detail}\n"
                    f"로그: `{LLM_DEBATE_TELEGRAM_LOG_PATH.name}`\n"
                    f"중지: `/debate_stop`",
                    parse_mode="Markdown",
                )
                return
            if cmd0 in ("/debate_stop", "/논문토론중지") or (
                cmd0.startswith("/debate_stop@") and "@" in cmd0
            ):
                ok, detail = stop_llm_debate_telegram_process()
                prefix = "🛑 " if ok else "ℹ️ "
                bot.reply_to(message, f"{prefix}{detail}", parse_mode="Markdown")
                return

            # 1차 방어: Rule-based 취소/재시작 문지기 (최상단)
            if text in _CANCEL_RESTART_CMDS:
                with _with_chat_lock(chat_id):
                    if chat_id in _pending_approvals:
                        del _pending_approvals[chat_id]
                    _thread_version[chat_id] = int(time.time() * 1000)
                clear_session(chat_id)  # 대화 메모리 RAM·DB 완전 초기화
                bot.reply_to(message, "✅ 재시작되었습니다. 새로운 질문을 해 주세요.", reply_markup=ReplyKeyboardRemove())
                return

            thread_id = f"tg_{chat_id}"

            with _with_chat_lock(chat_id):
                pending = chat_id in _pending_approvals
                if pending:
                    tid, cfg = _pending_approvals[chat_id]
            if pending:
                if "승인" in text or "거절" in text:
                    print("[DEBUG] Handler: 승인/거절 → 스레드로 run_or_resume(is_resume=True)")
                    status_msg = _safe_telegram_send_and_get(bot, chat_id, "⚙️ 작업을 시작합니다...") if "승인" in text else None
                    def _do_resume():
                        try:
                            run_or_resume(chat_id, text, config=cfg, is_resume=True, status_msg=status_msg)
                        except Exception as e:
                            print(f"[DEBUG] 스레드 예외: {e}\n{traceback.format_exc()}")
                            mid = getattr(status_msg, "message_id", None) if status_msg else None
                            detail = str(e)[:800] or type(e).__name__
                            if not _notify_chat_error(
                                bot,
                                chat_id,
                                headline="🚨 승인 후 작업 실패",
                                detail=detail,
                                status_message_id=mid,
                            ):
                                _notify_chat_error(
                                    bot,
                                    chat_id,
                                    headline="🚨 승인 후 작업 실패",
                                    detail=detail,
                                    status_message_id=None,
                                )
                    _executor.submit(_do_resume)
                    return
                # Auto-Cancel & Reroute: 승인/거절/취소가 아닌 엉뚱한 입력 → 계획만 취소, 메모리는 유지
                with _with_chat_lock(chat_id):
                    del _pending_approvals[chat_id]
                    _thread_version[chat_id] = int(time.time() * 1000)
                if _should_notify_auto_cancel(text):
                    _safe_telegram_send(bot, chat_id, "이전 계획을 정리하고 새 요청을 처리합니다.")
                # fall through: 아래에서 방금 입력한 text를 새 질문으로 Router부터 재실행

            status_msg = _safe_telegram_send_and_get(bot, chat_id, "⏳ 처리 중… (잠시만요)")
            print("[DEBUG] Handler: 스레드로 run_or_resume 제출 (메인 스레드 즉시 반환)")

            def _do_run():
                try:
                    try:
                        bot.send_chat_action(chat_id, "typing")
                    except Exception:
                        pass
                    ctx_image = take_pending_image(chat_id)
                    run_or_resume(chat_id, text, thread_id, is_resume=False, status_msg=status_msg, image_base64=ctx_image)
                except Exception as e:
                    err_detail = str(e)[:300]
                    print(f"[DEBUG] 스레드 예외: {e}\n{traceback.format_exc()}")
                    headline = "🚨 요청 처리 실패"
                    if "11434" in err_detail or "ConnectionError" in err_detail or "Ollama" in err_detail:
                        headline = "⚠️ Ollama 연결 오류"
                        detail = "Ollama 서버에 연결할 수 없습니다. `ollama serve`를 실행한 뒤 다시 시도해 주세요."
                    else:
                        detail = str(e)[:800] or type(e).__name__
                    mid = getattr(status_msg, "message_id", None) if status_msg else None
                    if not _notify_chat_error(bot, chat_id, headline=headline, detail=detail, status_message_id=mid):
                        _notify_chat_error(bot, chat_id, headline=headline, detail=detail, status_message_id=None)

            _executor.submit(_do_run)
        except Exception as e:
            print(f"🚨 핸들러 예외: {e}\n{traceback.format_exc()}")
            try:
                cid = str(message.chat.id)
            except Exception:
                cid = ""
            if cid:
                _notify_chat_error(
                    bot,
                    cid,
                    headline="🚨 메시지 처리 실패",
                    detail=str(e)[:800] or type(e).__name__,
                    status_message_id=None,
                )

    print("🤖 Agent 봇 시작 (Ctrl+C로 종료)")
    bot.delete_webhook(drop_pending_updates=True)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
