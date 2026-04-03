#!/usr/bin/env python3
"""
AI 워커: 브리지 큐에서 작업을 꺼내 LangGraph·RAG·LLM만 실행 (텔레그램 폴링 없음).
"""

from __future__ import annotations

import multiprocessing as mp
import os
import sys
import time
import traceback
from pathlib import Path

if sys.platform == "darwin":
    if mp.get_start_method(allow_none=True) != "spawn":
        mp.set_start_method("spawn", force=True)

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

import sqlite3

from dotenv import load_dotenv

load_dotenv()

from langgraph.checkpoint.sqlite import SqliteSaver

from core.bridge.agent_bridge_queue import claim_next_pending_job, init_bridge_db, reset_processing_stale
from core.rag.agent_chroma_rag import warmup_chroma_rag
from core.config.agent_config import CHECKPOINT_DB_PATH, GROQ_API_KEY, PROJECT_ROOT, get_gemini_api_keys
from apps.scheduler.agent_cron_worker import start_cron_worker_daemon
from core.graph.agent_graph import build_graph
from core.graph.agent_nodes import _run_tool_on_host
from core.session.agent_session import get_session, stash_pending_image, with_chat_lock
from core.rag.agent_tool_rag import sync_tool_chroma_from_disk
from core.llm.agent_vision import run_vision_analysis
from core.graph.agent_worker_runner import execute_graph_turn


def _acquire_worker_lock():
    if sys.platform == "win32":
        return None
    import fcntl

    path = PROJECT_ROOT / ".ai_worker.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    fp = open(path, "a+", encoding="utf-8")
    try:
        fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        fp.close()
        print("❌ ai_worker.py 가 이미 실행 중입니다.")
        sys.exit(1)
    fp.seek(0)
    fp.truncate()
    fp.write(str(os.getpid()))
    fp.flush()
    return fp


def _split_chunks(text: str, limit: int = 3800) -> list[str]:
    t = (text or "").strip()
    if not t:
        return ["(내용 없음)"]
    if len(t) <= limit:
        return [t]
    return [t[i : i + limit] for i in range(0, len(t), limit)]


def process_one_job(graph, job: dict) -> None:
    from core.bridge.agent_bridge_queue import complete_job, fail_job

    jid = int(job["id"])
    chat_id = str(job["chat_id"])
    graph_thread_id = str(job["graph_thread_id"])
    user_text = job["user_text"] or ""
    kind = (job["job_kind"] or "graph").strip()
    is_resume = bool(job["is_resume"])
    image_path = job["image_path"]

    try:
        if kind == "vision":
            if not image_path or not Path(image_path).is_file():
                fail_job(jid, "이미지 파일 없음")
                return
            b64 = Path(image_path).read_text(encoding="utf-8", errors="replace")
            try:
                Path(image_path).unlink(missing_ok=True)
            except OSError:
                pass
            ans = run_vision_analysis(None, chat_id, user_text, b64, None)
            if ans:
                with with_chat_lock(chat_id):
                    stash_pending_image(chat_id, b64)
                    session = get_session(chat_id)
                    session.add_turn(f"[이미지] {user_text}", ans)
                    session.maybe_compress()
                    session.save()
                complete_job(jid, result_text=ans, result_parse_mode=None)
            else:
                fail_job(jid, "이미지 분석 실패")
            return

        if kind == "schedule_list":
            out = _run_tool_on_host("schedule_list_jobs", "등록된 스케줄 보여줘", chat_id)
            complete_job(jid, result_text=f"📅 등록된 스케줄\n\n{out[:4000]}", result_parse_mode=None)
            return

        if kind != "graph":
            fail_job(jid, f"unknown job_kind: {kind}")
            return

        img_b64 = None
        if image_path and Path(image_path).is_file():
            img_b64 = Path(image_path).read_text(encoding="utf-8", errors="replace")
            try:
                Path(image_path).unlink(missing_ok=True)
            except OSError:
                pass

        cfg = {
            "configurable": {
                "thread_id": graph_thread_id,
                "chat_id": chat_id,
                "bot": None,
            }
        }
        with with_chat_lock(chat_id):
            execute_graph_turn(
                graph,
                chat_id=chat_id,
                user_text=user_text,
                thread_id=graph_thread_id,
                bot=None,
                status_msg=None,
                image_base64=img_b64,
                is_resume=is_resume,
                config=cfg,
                bridge_job_id=jid,
            )
    except Exception as e:
        print(f"❌ job {jid} 오류: {e}\n{traceback.format_exc()}")
        fail_job(jid, f"{type(e).__name__}: {e}")


def main() -> None:
    if not all([GROQ_API_KEY]) or not get_gemini_api_keys():
        print("❌ .env에 GROQ_API_KEY 및 Gemini 키를 설정하세요.")
        sys.exit(1)

    _acquire_worker_lock()
    init_bridge_db()
    reset_processing_stale()

    try:
        sync_tool_chroma_from_disk()
    except Exception as e:
        print(f"⚠️ Tool RAG 동기화 실패: {e}")

    try:
        warmup_chroma_rag()
        print("✅ Chroma RAG 워밍업 완료 (ai_worker)", flush=True)
    except Exception as e:
        print(f"⚠️ Chroma 워밍업 실패: {e}")

    conn = sqlite3.connect(CHECKPOINT_DB_PATH, check_same_thread=False)
    graph = build_graph(checkpointer=SqliteSaver(conn))
    start_cron_worker_daemon(respect_agent_disable_env=True)

    print("🧪 ai_worker 루프 시작 (브리지 큐 폴링)", flush=True)
    while True:
        job = claim_next_pending_job()
        if not job:
            time.sleep(0.08)
            continue
        print(f"[ai_worker] job id={job['id']} kind={job['job_kind']} chat={job['chat_id']}", flush=True)
        process_one_job(graph, job)


if __name__ == "__main__":
    main()
