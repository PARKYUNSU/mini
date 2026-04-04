#!/usr/bin/env python3
"""
텔레그램 전용 얇은 프로세스: getUpdates 폴링만 수행하고 SQLite 브리지에 작업을 넣고,
완료된 결과를 읽어 사용자에게 전송합니다. (torch/chromadb/langgraph 미사용)
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
import traceback
import unicodedata
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import telebot
from telebot.types import ReplyKeyboardRemove

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
_TBOT_DIR = Path(__file__).resolve().parent

from core.bridge.agent_bridge_queue import (
    bump_chat_thread,
    clear_approval_session,
    effective_graph_thread_id,
    enqueue_job,
    fetch_outbound_for_receiver,
    get_approval_session,
    init_bridge_db,
    mark_approval_sent,
    mark_delivered,
)
from core.config.agent_config import (
    ALLOWED_CHAT_ID,
    BACKFILL_LOG_PATH,
    LLM_DEBATE_TELEGRAM_LOG_PATH,
    PROJECT_ROOT,
    TELEGRAM_TOKEN,
)
from apps.telegram_bot.agent_telegram import (
    CANCEL_RESTART_CMDS,
    main_keyboard,
    safe_telegram_send,
    strip_wake_word,
)
from apps.telegram_bot.paper_list_light import list_stored_papers_text as papers_list_stdlib


def _acquire_receiver_lock():
    if sys.platform == "win32":
        return None
    import fcntl

    path = PROJECT_ROOT / ".telegram_receiver.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    fp = open(path, "a+", encoding="utf-8")
    try:
        fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        fp.close()
        print("❌ telegram_receiver.py 가 이미 실행 중입니다.")
        sys.exit(1)
    fp.seek(0)
    fp.truncate()
    fp.write(str(os.getpid()))
    fp.flush()
    return fp


def _split_telegram_chunks(text: str, limit: int = 3800) -> list[str]:
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
    return chunks


def _telegram_slash_command_token(text: str) -> str:
    t = unicodedata.normalize("NFKC", (text or "").strip()).lstrip("\ufeff\u200e\u200f").strip()
    if not t:
        return ""
    return t.split()[0].lower()


def _should_notify_auto_cancel(new_text: str) -> bool:
    t = (new_text or "").strip()
    if not t:
        return False
    compact = t.replace(" ", "")
    return len(compact) <= 6 and any(k in compact for k in ("?", "왜", "뭐", "어"))


def _clear_session_subprocess(chat_id: str) -> None:
    try:
        subprocess.run(
            [
                sys.executable,
                "-c",
                f"from core.session.agent_session import clear_session; clear_session({chat_id!r})",
            ],
            cwd=str(PROJECT_ROOT),
            timeout=120,
            capture_output=True,
            text=True,
        )
    except Exception as e:
        print(f"[receiver] clear_session subprocess: {e}")


def _outbound_poller(bot: telebot.TeleBot, allowed_ids: list[str]) -> None:
    init_bridge_db()
    while True:
        try:
            rows = fetch_outbound_for_receiver(30)
            for row in rows:
                jid = int(row["id"])
                chat_id = str(row["chat_id"])
                if chat_id not in allowed_ids:
                    mark_delivered(jid)
                    mark_approval_sent(jid)
                    continue
                st = row["status"]
                if st == "approval_pending":
                    plan = row["plan_text"] or ""
                    if plan:
                        safe_telegram_send(bot, chat_id, plan[:4000], parse_mode="Markdown") or safe_telegram_send(
                            bot, chat_id, plan.replace("**", "")[:4000], parse_mode=None
                        )
                    mark_approval_sent(jid)
                    continue
                if st == "failed":
                    err = (row["error_text"] or "오류")[:4000]
                    safe_telegram_send(bot, chat_id, f"⚠️ {err}", parse_mode=None)
                    mark_delivered(jid)
                    continue
                if st == "completed":
                    body = row["result_text"] or ""
                    pm = row["result_parse_mode"]
                    if pm == "Markdown":
                        if not safe_telegram_send(bot, chat_id, body[:4000], parse_mode="Markdown"):
                            safe_telegram_send(bot, chat_id, body[:4000], parse_mode=None)
                    elif pm == "HTML":
                        if not safe_telegram_send(bot, chat_id, body[:4000], parse_mode="HTML"):
                            safe_telegram_send(bot, chat_id, body[:4000], parse_mode=None)
                    else:
                        for part in _split_telegram_chunks(body, 4000):
                            safe_telegram_send(bot, chat_id, part, parse_mode=None)
                    mark_delivered(jid)
        except Exception as e:
            print(f"[outbound_poller] {e}\n{traceback.format_exc()}")
        time.sleep(0.22)


def main() -> None:
    if not TELEGRAM_TOKEN or not ALLOWED_CHAT_ID:
        print("❌ TELEGRAM_TOKEN, ALLOWED_CHAT_ID 필요")
        sys.exit(1)

    _acquire_receiver_lock()
    init_bridge_db()

    allowed_ids = [a.strip() for a in ALLOWED_CHAT_ID.split(",")]
    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    poller = threading.Thread(target=_outbound_poller, args=(bot, allowed_ids), name="outbound-poller", daemon=True)
    poller.start()

    @bot.message_handler(commands=["start"])
    def on_start(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return
        bot.reply_to(
            message,
            "🤖 **AI 에이전트 봇** (분리 모드: 수신기+워커)\n\n질문을 보내 주세요.",
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )

    @bot.message_handler(commands=["reboot", "rebot"])
    def on_reboot(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            return
        bot.reply_to(message, "🔄 재부팅 스크립트를 호출합니다…")
        try:
            subprocess.Popen(["bash", str(PROJECT_ROOT / "restart.sh")], cwd=str(PROJECT_ROOT), start_new_session=True)
        except Exception as e:
            bot.reply_to(message, f"실패: {e}")

    @bot.message_handler(commands=["backfill_start"])
    def on_backfill_start(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            return
        try:
            from apps.backfill.agent_backfill_telegram import start_backfill_process
            ok, msg = start_backfill_process()
            if ok:
                bot.reply_to(message, f"✅ {msg}\n로그: `{BACKFILL_LOG_PATH.name}`", parse_mode="Markdown")
            else:
                bot.reply_to(message, f"⚠️ {msg}")
        except Exception as e:
            bot.reply_to(message, f"❌ 백필 시작 오류: {e}")

    @bot.message_handler(commands=["backfill_stop"])
    def on_backfill_stop(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            return
        try:
            from apps.backfill.agent_backfill_telegram import stop_backfill_process
            ok, msg = stop_backfill_process()
            bot.reply_to(message, f"{'✅' if ok else '⚠️'} {msg}", parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"❌ 백필 중지 오류: {e}")

    @bot.message_handler(commands=["debate_start", "논문토론시작"])
    def on_debate_start(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            return
        try:
            from apps.telegram_bot.agent_debate_telegram import start_llm_debate_telegram_process
            ok, msg = start_llm_debate_telegram_process()
            if ok:
                bot.reply_to(
                    message,
                    f"✅ {msg}\n로그: `{LLM_DEBATE_TELEGRAM_LOG_PATH.name}`",
                    parse_mode="Markdown",
                )
            else:
                bot.reply_to(message, f"⚠️ {msg}")
        except Exception as e:
            bot.reply_to(message, f"❌ 토론 시작 오류: {e}")

    @bot.message_handler(commands=["debate_stop", "논문토론중지"])
    def on_debate_stop(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            return
        try:
            from apps.telegram_bot.agent_debate_telegram import stop_llm_debate_telegram_process
            ok, msg = stop_llm_debate_telegram_process()
            bot.reply_to(message, f"{'🛑' if ok else '⚠️'} {msg}", parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"❌ 토론 중지 오류: {e}")

    @bot.message_handler(commands=["schedule", "스케줄"])
    def on_schedule(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            return
        tid = effective_graph_thread_id(chat_id)
        enqueue_job(
            chat_id=chat_id,
            graph_thread_id=tid,
            user_text="",
            job_kind="schedule_list",
        )
        bot.reply_to(message, "📅 스케줄 목록을 요청했습니다. 잠시만요…")

    @bot.message_handler(commands=["papers", "paperlist", "논문목록"])
    def on_papers(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            return
        body = papers_list_stdlib(PROJECT_ROOT)
        header = "📚 저장된 논문 (raw_data_queue/crawled_papers.jsonl)\n\n"
        full = header + body
        chunks = _split_telegram_chunks(full)
        for i, chunk in enumerate(chunks):
            prefix = f"({i + 1}/{len(chunks)})\n" if len(chunks) > 1 else ""
            if i == 0:
                bot.reply_to(message, prefix + chunk)
            else:
                bot.send_message(chat_id, prefix + chunk)
            if i < len(chunks) - 1:
                time.sleep(0.35)

    @bot.message_handler(content_types=["text", "photo"], func=lambda m: True)
    def handle(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없습니다.")
            return

        if message.photo:
            import base64
            import uuid

            try:
                file_id = message.photo[-1].file_id
                file_info = bot.get_file(file_id)
                raw = bot.download_file(file_info.file_path)
                b64 = base64.b64encode(raw).decode("ascii")
                cap = (message.caption or "").strip()
                user_request = strip_wake_word(cap) if cap else "이 이미지를 자세히 분석하고 무엇인지 설명해 줘."
                init_bridge_db()
                BRIDGE_DIR = PROJECT_ROOT / ".bridge"
                BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
                img_path = BRIDGE_DIR / f"img_{uuid.uuid4().hex}.b64.txt"
                img_path.write_text(b64, encoding="ascii")
                tid = effective_graph_thread_id(chat_id)
                enqueue_job(
                    chat_id=chat_id,
                    graph_thread_id=tid,
                    user_text=user_request,
                    job_kind="vision",
                    image_path=str(img_path),
                )
                bot.reply_to(message, "🖼 이미지 분석 요청을 접수했습니다. 잠시만요…")
            except Exception as e:
                print(traceback.format_exc())
                bot.reply_to(message, f"사진 처리 실패: {e}"[:300])
            return

        text = strip_wake_word((message.text or "").strip())
        if not text:
            bot.reply_to(message, "메시지를 입력해 주세요.")
            return

        cmd = text.strip().split()[0].lower() if text else ""
        if cmd == "/paper" or cmd.startswith("/paper@"):
            subprocess.run(
                [sys.executable, str(_TBOT_DIR / "paper_mode_cli.py"), chat_id, text],
                cwd=str(PROJECT_ROOT),
                timeout=60,
            )
            bot.reply_to(message, "📚 논문 모드 설정을 반영했습니다.")
            return

        cmd0 = _telegram_slash_command_token(text)
        if cmd0 in ("/debate_start", "/논문토론시작") or (cmd0.startswith("/debate_start@") and "@" in cmd0):
            subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    "from apps.telegram_bot.agent_debate_telegram import start_llm_debate_telegram_process; start_llm_debate_telegram_process()",
                ],
                cwd=str(PROJECT_ROOT),
                start_new_session=True,
            )
            bot.reply_to(message, "🧪 토론 배치 기동 요청")
            return
        if cmd0 in ("/debate_stop", "/논문토론중지") or (cmd0.startswith("/debate_stop@") and "@" in cmd0):
            subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from apps.telegram_bot.agent_debate_telegram import stop_llm_debate_telegram_process; stop_llm_debate_telegram_process()",
                ],
                cwd=str(PROJECT_ROOT),
                timeout=120,
            )
            bot.reply_to(message, "🛑 토론 중지")
            return

        if text in CANCEL_RESTART_CMDS:
            bump_chat_thread(chat_id)
            clear_approval_session(chat_id)
            _clear_session_subprocess(chat_id)
            bot.reply_to(message, "✅ 재시작되었습니다.", reply_markup=ReplyKeyboardRemove())
            return

        sess = get_approval_session(chat_id)
        if sess:
            resume_tid, _ = sess
            if "승인" in text or "거절" in text:
                enqueue_job(
                    chat_id=chat_id,
                    graph_thread_id=resume_tid,
                    user_text=text,
                    job_kind="graph",
                    is_resume=True,
                )
                clear_approval_session(chat_id)
                bot.reply_to(message, "⚙️ 승인/거절을 처리 중입니다…")
                return
            bump_chat_thread(chat_id)
            clear_approval_session(chat_id)
            if _should_notify_auto_cancel(text):
                safe_telegram_send(bot, chat_id, "이전 계획을 정리하고 새 요청을 처리합니다.")

        tid = effective_graph_thread_id(chat_id)
        enqueue_job(
            chat_id=chat_id,
            graph_thread_id=tid,
            user_text=text,
            job_kind="graph",
        )
        bot.reply_to(message, "⏳ 요청을 접수했습니다. AI 워커가 처리 중입니다…")

    print("📡 telegram_receiver 시작 (infinity_polling)", flush=True)
    bot.delete_webhook(drop_pending_updates=True)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
