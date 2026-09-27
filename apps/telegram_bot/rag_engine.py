"""
Phase 3.0 — 논문 Chroma + 윤수르 V3 RAG 엔진 (리시버·단독 봇 공용).

- Chroma / HuggingFaceEmbeddings / ChatOllama / PromptTemplate 캡슐화
- ``async def process_rag_query`` : Chroma는 ``asyncio.to_thread``, LLM은 ``ainvoke``
- 리시버 통합 시: ``submit_rag_job`` + 데몬 워커 스레드로 폴링 스레드 비차단
"""

from __future__ import annotations

import asyncio
import logging
import os
import queue
import re
import threading
import traceback
from pathlib import Path

import chromadb
import chromadb.errors
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
import telebot

try:
    from telebot.apihelper import ApiTelegramException
except ImportError:

    class ApiTelegramException(Exception):
        """telebot 구버전 스텁"""


from apps.telegram_bot.agent_telegram import (
    escape_telegram_html,
    rag_structured_lines_to_html,
    safe_telegram_send,
    strip_thinking_tags,
)
from core.config.agent_config import CHROMA_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL

logger = logging.getLogger(__name__)

RAG_LOADING_MESSAGE = (
    "⏳ [윤수르 V3]: 지식 창고를 검색하여 마크다운 보고서를 작성 중입니다... (잠시만 기다려주세요)"
)
RAG_ERROR_MESSAGE = "⚠️ 검색된 논문이 없거나 AI 엔진에 문제가 발생했습니다."

_OLLAMA_STOP = ["<|im_end|>", "<|im_start|>", "<|endoftext|>"]

_RAG_PROMPT = PromptTemplate.from_template(
    """당신은 호문클루스 신디게이트의 최고 기술 책임자(CTO)입니다.
아래 제공된 [검색된 논문 내용]만 바탕으로, 사용자의 질문에 대한 완벽한 마크다운 보고서(서론/본론/결론)를 작성하세요.

[검색된 논문 내용]:
{context}

[사용자 질문]:
{question}
"""
)

_retriever = None
_llm: ChatOllama | None = None
_stack_init_lock = threading.Lock()

_rag_job_queue: queue.Queue[tuple[str, str]] = queue.Queue()
_worker_started = False
_worker_lock = threading.Lock()


def chroma_persist_path() -> str:
    return os.environ.get("CHROMA_PATH") or str(CHROMA_DB_DIR)


def normalize_model_newlines(text: str) -> str:
    return (text or "").replace("\\n", "\n")


def try_parse_rag_command(text: str) -> str | None:
    """
    명시적 ``/rag`` 라우팅만 인정 (``/ragonly`` 등 오매칭 방지).

    Returns:
        ``None`` — RAG 명령이 아님.
        ``""`` — ``/rag`` 만 있고 본문 없음 → 호출측에서 사용법 안내.
        그 외 — 질문 본문.
    """
    raw = (text or "").strip()
    if not raw:
        return None
    m = re.match(r"^/rag(?:@\S+)?(?:\s+(.*))?$", raw, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    inner = m.group(1)
    if inner is None:
        return ""
    return inner.strip()


def _init_rag_stack_sync() -> None:
    global _retriever, _llm
    with _stack_init_lock:
        if _retriever is not None and _llm is not None:
            return
        chroma_path = chroma_persist_path()
        if not Path(chroma_path).is_dir():
            raise FileNotFoundError(f"Chroma 경로 없음: {chroma_path}")

        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        # RagProcessor 등과 동일한 Chroma 설정이어야 SharedSystemClient가 같은 경로를 재사용한다.
        chroma_client = chromadb.PersistentClient(
            path=chroma_path,
            settings=Settings(anonymized_telemetry=False),
        )
        vectorstore = Chroma(
            client=chroma_client,
            persist_directory=chroma_path,
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME,
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        try:
            retriever.invoke("__rag_engine_embedding_dim_probe__")
        except chromadb.errors.InvalidArgumentError as exc:
            if "dimension" in str(exc).lower():
                raise RuntimeError(
                    f"임베딩 차원 불일치: DB와 EMBEDDING_MODEL={EMBEDDING_MODEL!r} 을 맞추세요."
                ) from exc
            raise

        _llm_local = ChatOllama(
            model=os.environ.get("LOCAL_LLM_MODEL", "yunsur_v3:latest"),
            base_url=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"),
            temperature=0.1,
            stop=_OLLAMA_STOP,
        )
        _retriever = retriever
        _llm = _llm_local


def _retrieve_context_sync(user_question: str) -> str:
    assert _retriever is not None
    docs = _retriever.invoke(user_question)
    return "\n\n".join(d.page_content for d in docs if d.page_content)


def get_curator_context_sync(rag_query: str, top_k: int = 6) -> str:
    """
    심사관용: 기존 Chroma에서 유사 청크만 동기 검색 (크론 스크립트 등).
    ``top_k`` 는 리시버 RAG(3)와 별도로 넉넉히 가져옵니다.
    """
    _init_rag_stack_sync()
    assert _retriever is not None
    vs = _retriever.vectorstore
    docs = vs.similarity_search(rag_query, k=max(1, top_k))
    return "\n\n".join(d.page_content for d in docs if getattr(d, "page_content", None))


async def process_rag_query(user_question: str) -> str:
    """
    RAG 전체 파이프라인 (단일 이벤트 루프에서 ``asyncio.run`` 으로 호출할 것).

    - 초기화·Chroma 검색: ``asyncio.to_thread`` (블로킹 분리)
    - LLM: ``ainvoke``
    """
    await asyncio.to_thread(_init_rag_stack_sync)
    context = await asyncio.to_thread(_retrieve_context_sync, user_question)
    if not context.strip():
        raise ValueError("empty_chroma_context")

    final_prompt = _RAG_PROMPT.format(context=context, question=user_question)
    assert _llm is not None
    msg = await _llm.ainvoke(final_prompt)
    raw = (getattr(msg, "content", None) or "").strip()
    if not raw:
        raise ValueError("empty_llm_response")
    return strip_thinking_tags(normalize_model_newlines(raw))


def split_html_chunks(text: str, limit: int = 3800) -> list[str]:
    t = (text or "").strip()
    if not t:
        return ["(내용 없음)"]
    if len(t) <= limit:
        return [t]
    return [t[i : i + limit] for i in range(0, len(t), limit)]


def send_rag_answer_telebot(bot: telebot.TeleBot, chat_id: str, markdown_answer: str) -> None:
    """마크다운류 응답을 HTML로 바꿔 전송. 파싱 실패 시 평문 폴백."""
    body = normalize_model_newlines(strip_thinking_tags(markdown_answer))
    html_text = rag_structured_lines_to_html(body)
    for part in split_html_chunks(html_text, 3800):
        try:
            bot.send_message(
                chat_id,
                part,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
        except ApiTelegramException as e:
            desc = (getattr(e, "description", "") or "").lower()
            if "parse" in desc or "can't find end" in desc or "entity" in desc:
                safe_telegram_send(
                    bot,
                    chat_id,
                    escape_telegram_html(body)[:4096],
                    parse_mode=None,
                )
            else:
                raise


def _rag_worker_loop(telegram_token: str) -> None:
    """데몬 스레드: 큐에서 작업을 꺼내 ``asyncio.run(process_rag_query)`` 후 전송."""
    tb = telebot.TeleBot(telegram_token, threaded=False)
    while True:
        chat_id, query = _rag_job_queue.get()
        try:
            answer = asyncio.run(process_rag_query(query))
            send_rag_answer_telebot(tb, chat_id, answer)
        except Exception:
            logger.exception("rag_engine worker 실패 chat_id=%s", chat_id)
            traceback.print_exc()
            try:
                safe_telegram_send(tb, chat_id, RAG_ERROR_MESSAGE, parse_mode=None)
            except Exception as send_exc:
                logger.exception("rag_engine 오류 회신 실패: %s", send_exc)
        finally:
            try:
                _rag_job_queue.task_done()
            except Exception:
                pass


def ensure_rag_worker_started(telegram_token: str) -> None:
    """``telegram_receiver`` ``main()`` 에서 1회 호출."""
    global _worker_started
    with _worker_lock:
        if _worker_started:
            return
        t = threading.Thread(
            target=_rag_worker_loop,
            args=(telegram_token,),
            daemon=True,
            name="rag-outbound-worker",
        )
        t.start()
        _worker_started = True


def submit_rag_job(chat_id: str, query: str) -> None:
    """폴링 스레드에서 논블로킹으로 RAG 작업만 큐잉 (토큰은 ``ensure_rag_worker_started`` 시 고정)."""
    _rag_job_queue.put((chat_id, query))


async def send_rag_answer_async(async_bot, chat_id: str, markdown_answer: str) -> None:
    """AsyncTeleBot 용: HTML 변환·청크 전송·파싱 실패 시 평문 폴백."""
    try:
        from telebot.asyncio_helper import ApiTelegramException as AsyncApiTelegramException
    except ImportError:
        AsyncApiTelegramException = ApiTelegramException  # type: ignore[misc, assignment]

    body = normalize_model_newlines(strip_thinking_tags(markdown_answer))
    html_text = rag_structured_lines_to_html(body)
    for part in split_html_chunks(html_text, 3800):
        try:
            await async_bot.send_message(
                chat_id,
                part,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
        except (ApiTelegramException, AsyncApiTelegramException) as e:
            desc = (getattr(e, "description", "") or "").lower()
            if "parse" in desc or "can't find end" in desc or "entity" in desc:
                await async_bot.send_message(
                    chat_id,
                    escape_telegram_html(body)[:4096],
                    parse_mode=None,
                    disable_web_page_preview=True,
                )
            else:
                raise
