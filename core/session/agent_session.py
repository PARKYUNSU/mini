"""
세션·대화 메모리·도구 라이브러리·라우터 1단계 의존성.
텔레그램 전용(_pending_approvals 등)은 agent_bot에 둔다.
"""

from __future__ import annotations

import contextlib
import json
import re
import sqlite3
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from core.config.agent_config import (
    AGENT_LEARNINGS_PATH,
    AGENT_TOOLS_DIR,
    CHAT_MEMORY_DB_PATH,
    MEMORY_BUFFER,
    MEMORY_K,
    PROJECT_ROOT,
)
from core.llm.agent_llm import get_planner_llm
from core.graph.agent_router_rules import (
    RouterStep1Deps,
    get_search_intent,
    match_whitelisted_tool,
    resolve_recent_tool_from_snapshot,
    router_step1_hard_rules as _router_step1_hard_rules_core,
)
from core.rag.agent_tool_rag import get_tool_rag_store


# ============ 오답 노트 (Learnings) - 자가 진화 ============
def _ensure_learnings_dir() -> Path:
    """agent_learnings/ 디렉터리 생성 및 ERRORS.md 초기화"""
    learnings_dir = (PROJECT_ROOT / AGENT_LEARNINGS_PATH).parent
    learnings_dir.mkdir(parents=True, exist_ok=True)
    path = PROJECT_ROOT / AGENT_LEARNINGS_PATH
    if not path.exists():
        path.write_text(
            "# Agent 오답 노트 (Learnings)\n\n"
            "재시도(Retry) 끝에 성공한 사례의 에러·해결 요약. Planner가 계획 수립 시 참고합니다.\n\n"
            "---\n\n",
            encoding="utf-8",
        )
    return path


def append_learning(user_request: str, error_hint: str, saved_tool_name: str) -> None:
    """재시도 후 성공 시 오답 노트에 에러·해결 요약 누적"""
    try:
        path = _ensure_learnings_dir()
        ts = time.strftime("%Y-%m-%d %H:%M")
        block = (
            f"### {ts}\n"
            f"- **요청**: {user_request[:200]}{'...' if len(user_request) > 200 else ''}\n"
            f"- **에러/해결**: {error_hint[:500]}{'...' if len(error_hint) > 500 else ''}\n"
            f"- **저장된 도구**: `{saved_tool_name}`\n\n"
        )
        with open(path, "a", encoding="utf-8") as f:
            f.write(block)
        print(f"[DEBUG] Learnings: 오답 노트 기록 ({saved_tool_name})")
    except Exception as e:
        print(f"[DEBUG] Learnings 기록 오류: {e}")


def load_learnings() -> str:
    """agent_learnings/ERRORS.md 내용 반환 (없으면 빈 문자열)"""
    path = PROJECT_ROOT / AGENT_LEARNINGS_PATH
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


# ============ Tool Maker & Skill Library (자가 진화) ============
class AgentSkillLibrary:
    """agent_tools/ 디렉터리에 저장된 도구 검색 및 저장"""

    def __init__(self, tools_dir: Path = AGENT_TOOLS_DIR):
        self.tools_dir = Path(tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)

    def list_tools(self) -> list[tuple[str, str]]:
        """(파일명, 파일 내용 요약) 리스트 반환"""
        result = []
        paths = sorted(self.tools_dir.glob("*.py"))
        saved = self.tools_dir / "saved"
        if saved.is_dir():
            paths += sorted(saved.glob("*.py"))
        for p in paths:
            try:
                content = p.read_text(encoding="utf-8")
                summary = content[:300].replace("\n", " ") + ("..." if len(content) > 300 else "")
                result.append((p.stem, summary))
            except Exception:
                pass
        return result

    def get_tools_context(self, query: str = "") -> str:
        """[레거시] 전체 목록 문자열. Router/Planner는 Tool RAG(get_tool_rag_store) 사용 권장."""
        tools = self.list_tools()
        if not tools:
            return "저장된 도구 없음."
        lines = [f"- {name}: {desc[:200]}..." for name, desc in tools]
        return "\n".join(lines)

    def save_tool(self, code: str, request_hint: str = "") -> Optional[str]:
        """성공한 코드를 agent_tools/saved/*.py 로 저장. 파일명 반환."""
        try:
            saved_dir = self.tools_dir / "saved"
            saved_dir.mkdir(parents=True, exist_ok=True)
            safe_name = re.sub(r"[^\w가-힣]", "_", request_hint[:30]) or "tool"
            safe_name = safe_name.strip("_") or "tool"
            base = safe_name
            idx = 0
            while (saved_dir / f"{base}.py").exists():
                idx += 1
                base = f"{safe_name}_{idx}"
            path = saved_dir / f"{base}.py"
            path.write_text(code, encoding="utf-8")
            try:
                get_tool_rag_store().upsert_file(path)
            except Exception as ex:
                print(f"[ToolRAG] 저장 후 인덱스 갱신 실패: {ex}")
            return path.name
        except Exception as e:
            print(f"도구 저장 오류: {e}")
            return None


# ============ 대화 기록 영구 저장소 (SQLite) ============
class ChatMemoryStore:
    """SessionMemory를 SQLite에 영구 저장/불러오기"""

    def __init__(self, db_path: str = CHAT_MEMORY_DB_PATH):
        self.db_path = db_path
        self._init_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_table(self) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_memory (
                    chat_id TEXT PRIMARY KEY,
                    recent_messages TEXT NOT NULL,
                    summary TEXT NOT NULL DEFAULT '',
                    updated_at REAL
                )
                """
            )
            conn.commit()

    def save(self, chat_id: str, recent_messages: list[tuple[str, str]], summary: str) -> None:
        """recent_messages와 summary를 JSON 직렬화하여 저장"""
        data = json.dumps([[u, a] for u, a in recent_messages], ensure_ascii=False)
        with self._get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO chat_memory (chat_id, recent_messages, summary, updated_at) VALUES (?, ?, ?, ?)",
                (chat_id, data, summary, time.time()),
            )
            conn.commit()

    def load(self, chat_id: str) -> tuple[list[tuple[str, str]], str] | None:
        """chat_id에 해당하는 대화 기록 불러오기. 없으면 None."""
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT recent_messages, summary FROM chat_memory WHERE chat_id = ?",
                (chat_id,),
            ).fetchone()
        if row is None:
            return None
        messages_json, summary = row
        try:
            messages = [tuple(pair) for pair in json.loads(messages_json)]
            return (messages, summary)
        except (json.JSONDecodeError, TypeError):
            return None

    def clear(self, chat_id: str) -> None:
        """chat_id의 대화 기록을 DB에서 완전 삭제 (재시작/취소 시 호출)"""
        with self._get_conn() as conn:
            conn.execute("DELETE FROM chat_memory WHERE chat_id = ?", (chat_id,))
            conn.commit()


_chat_memory_store = ChatMemoryStore()


# ============ 세션 메모리 (CHAT_ID별) ============
@dataclass
class SessionMemory:
    """최근 K턴 원본 + 이전 대화 요약 (디스크 영구 저장)"""

    chat_id: str
    recent_messages: deque = field(default_factory=lambda: deque(maxlen=MEMORY_BUFFER))
    summary: str = ""
    _llm: ChatOllama | None = None

    def save(self) -> None:
        """현재 상태를 chat_memory.db에 즉시 저장 (수동 업데이트 후 호출)"""
        self._save_to_store()

    def _save_to_store(self) -> None:
        try:
            _chat_memory_store.save(
                self.chat_id,
                list(self.recent_messages),
                self.summary,
            )
        except Exception as e:
            print(f"대화 기록 저장 오류: {e}")

    def _get_llm(self) -> ChatOllama:
        if self._llm is None:
            self._llm = get_planner_llm()
        return self._llm

    def add_turn(self, user_msg: str, assistant_msg: str) -> None:
        self.recent_messages.append((f"User: {user_msg}", f"Assistant: {assistant_msg}"))
        self._save_to_store()

    def _summarize_old(self, new_turns: str) -> str:
        try:
            llm = self._get_llm()
            resp = llm.invoke(
                [
                    SystemMessage(content="다음 대화를 2~3문장으로 요약해. 핵심만."),
                    HumanMessage(content=f"기존 요약:\n{self.summary}\n\n새 대화:\n{new_turns}"),
                ]
            )
            return resp.content.strip() if resp.content else self.summary
        except Exception:
            return self.summary

    def get_context(self) -> str:
        recent = "\n".join(
            f"{u}\n{a}" for u, a in self.recent_messages
        )
        if self.summary:
            return f"[이전 대화 요약]\n{self.summary}\n\n[최근 대화]\n{recent}"
        return f"[최근 대화]\n{recent}"

    def get_last_assistant_response(self) -> str:
        """직전 턴의 AI 응답만 반환 (앵무새 방지용)"""
        if not self.recent_messages:
            return ""
        _, last_assistant = self.recent_messages[-1]
        return last_assistant.replace("Assistant: ", "").strip()

    def get_recent_context(self, max_turns: int = 2) -> str:
        """라우터용: 직전 N턴만 반환 (문맥 인지 라우팅)"""
        recent = list(self.recent_messages)[-max_turns:]
        return "\n".join(f"{u}\n{a}" for u, a in recent) if recent else ""

    def maybe_compress(self) -> None:
        """최근 MEMORY_K턴은 원본 유지, 그 이전은 Qwen으로 요약 후 제거. Ollama 미실행 시 요약만 스킵."""
        if len(self.recent_messages) <= MEMORY_K:
            return
        try:
            to_remove = len(self.recent_messages) - MEMORY_K
            to_summarize = "\n".join(
                f"{u}\n{a}" for u, a in list(self.recent_messages)[:to_remove]
            )
            if to_summarize:
                self.summary = self._summarize_old(to_summarize)
            for _ in range(to_remove):
                self.recent_messages.popleft()
            self._save_to_store()
        except Exception as e:
            print(f"[DEBUG] maybe_compress 스킵 (Ollama 미실행 등): {e}")


# CHAT_ID → SessionMemory
_sessions: dict[str, SessionMemory] = {}
# thread_id → plan_lines (Resume 시 중복 계획 전송 방지)
_plan_cache: dict[str, list[str]] = {}
_recent_tools: dict[str, list[dict[str, str]]] = {}
# 사진 후속 텍스트 질문용 (1회 소비)
_pending_image: dict[str, str] = {}
_paper_mode: dict[str, bool] = {}

_chat_locks: dict[str, threading.RLock] = {}
_lock_for_locks = threading.Lock()


def _get_chat_lock(chat_id: str) -> threading.RLock:
    with _lock_for_locks:
        if chat_id not in _chat_locks:
            _chat_locks[chat_id] = threading.RLock()
        return _chat_locks[chat_id]


def extract_chat_id_from_thread(thread_id: str) -> str:
    """thread_id(tg_123 또는 tg_123_456)에서 chat_id 추출."""
    if not thread_id or not thread_id.startswith("tg_"):
        return thread_id or ""
    parts = thread_id.split("_")
    return parts[1] if len(parts) >= 2 else thread_id


def get_paper_mode(chat_id: str) -> bool:
    return _paper_mode.get(chat_id, False)


def set_paper_mode(chat_id: str, on: bool) -> None:
    with with_chat_lock(chat_id):
        _paper_mode[chat_id] = on


def _has_explicit_paper_intent(user_request: str) -> bool:
    r = (user_request or "").lower()
    keywords = ("논문", "chromadb", "chroma", "paper", "저장된 문서", "db에", "db에서")
    return any(k in r for k in keywords)


def is_rag_allowed(chat_id: str, user_request: str) -> bool:
    return get_paper_mode(chat_id) or _has_explicit_paper_intent(user_request)


@contextlib.contextmanager
def with_chat_lock(chat_id: str):
    lock = _get_chat_lock(chat_id)
    lock.acquire()
    try:
        yield
    finally:
        lock.release()


def stash_pending_image(chat_id: str, image_b64: str) -> None:
    with with_chat_lock(chat_id):
        _pending_image[chat_id] = image_b64


def take_pending_image(chat_id: str) -> Optional[str]:
    with with_chat_lock(chat_id):
        return _pending_image.pop(chat_id, None)


def _infer_tool_tag(tool_name: str, request_hint: str = "") -> str:
    text = f"{tool_name} {request_hint}".lower()
    if any(k in text for k in ("성경", "bible", "genesis", "john")):
        return "bible"
    if any(k in text for k in ("환율", "exchange", "usd", "krw", "달러")):
        return "exchange_rate"
    if any(k in text for k in ("주가", "stock", "삼성전자")):
        return "stock_price"
    if any(k in text for k in ("비트코인", "이더리움", "btc", "eth", "coin")):
        return "coin_price"
    if any(k in text for k in ("날씨", "weather", "wttr")):
        return "weather"
    if any(k in text for k in ("form", "폼", "google_form")):
        return "google_form"
    return "general"


def remember_tool(chat_id: str, tool_name: str, request_hint: str = "") -> None:
    with with_chat_lock(chat_id):
        bucket = _recent_tools.setdefault(chat_id, [])
        bucket = [x for x in bucket if x.get("tool_name") != tool_name]
        bucket.insert(0, {
            "tool_name": tool_name,
            "tag": _infer_tool_tag(tool_name, request_hint),
            "request_hint": request_hint[:200],
        })
        _recent_tools[chat_id] = bucket[:5]


def _resolve_recent_tool_reference(chat_id: str, user_request: str) -> Optional[str]:
    with with_chat_lock(chat_id):
        recent = list(_recent_tools.get(chat_id, []))
    return resolve_recent_tool_from_snapshot(recent, user_request)


def get_search_intent_local(user_request: str, req_lower: str) -> Literal["web", "rag", "tool", "none"]:
    return get_search_intent(user_request, req_lower)


def match_whitelisted_tool_local(user_request: str, req_lower: str) -> Optional[str]:
    return match_whitelisted_tool(user_request, req_lower, AGENT_TOOLS_DIR)


def router_step1_hard_rules(user_request: str, req_lower: str, chat_id: str) -> Optional[dict]:
    return _router_step1_hard_rules_core(
        user_request,
        req_lower,
        chat_id,
        RouterStep1Deps(
            agent_tools_dir=AGENT_TOOLS_DIR,
            get_paper_mode=get_paper_mode,
            resolve_recent_tool=_resolve_recent_tool_reference,
        ),
    )


def get_session(chat_id: str) -> SessionMemory:
    with with_chat_lock(chat_id):
        if chat_id not in _sessions:
            loaded = _chat_memory_store.load(chat_id)
            if loaded:
                messages_list, summary = loaded
                recent = deque(messages_list, maxlen=MEMORY_BUFFER)
                _sessions[chat_id] = SessionMemory(
                    chat_id=chat_id,
                    recent_messages=recent,
                    summary=summary or "",
                )
            else:
                _sessions[chat_id] = SessionMemory(chat_id=chat_id)
        return _sessions[chat_id]


def clear_session(chat_id: str) -> None:
    with with_chat_lock(chat_id):
        _chat_memory_store.clear(chat_id)
        if chat_id in _sessions:
            del _sessions[chat_id]
        if chat_id in _recent_tools:
            del _recent_tools[chat_id]
        if chat_id in _pending_image:
            del _pending_image[chat_id]
        if chat_id in _paper_mode:
            del _paper_mode[chat_id]
