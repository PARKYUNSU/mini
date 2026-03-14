#!/usr/bin/env python3
"""
Multi-Agent 동적 코딩 텔레그램 봇
- LangGraph: [기획 → 인간 승인 → 개발 → 감시] 루프
- Planner(Qwen) → HITL → Executor(Gemini) → Monitor(Gemini) → Self-Correction
"""

import os

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

import json
import re
import sqlite3
import time
from pathlib import Path
import traceback
from collections import deque
from dataclasses import dataclass, field
from typing import Literal, TypedDict

from e2b_code_interpreter import Sandbox

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.types import Command, interrupt
import telebot

load_dotenv()

# ============ 설정 ============
TELEGRAM_TOKEN = os.getenv("AGENT_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_DB_PATH = "./test_chroma_db"
COLLECTION_NAME = "arxiv_papers"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = "qwen2.5:7b"
GEMINI_MODEL = "gemini-2.5-flash"
MEMORY_K = 5  # 최근 K턴 원본 유지
MEMORY_BUFFER = 15  # 요약 전 버퍼 크기 (과거 메시지 축적용)
RAG_TOP_K = 3
AGENT_TOOLS_DIR = Path("./agent_tools")
CODE_TIMEOUT_SEC = 30
ERROR_LOG_MAX_CHARS = 1000
CHECKPOINT_DB_PATH = "./agent_checkpoints.db"
CHAT_MEMORY_DB_PATH = "./chat_memory.db"


# ============ AgentState ============
class AgentState(TypedDict, total=False):
    user_request: str
    plan: list[str]
    approval_status: Literal["pending", "approved", "rejected"]
    generated_code: str
    execution_result: str
    retry_count: int
    error_hint: str  # Monitor → Executor 재시도 시 힌트


# ============ ChromaDB RAG 도구 ============
class ChromaRAGTool:
    def __init__(self, db_path: str = CHROMA_DB_PATH, collection_name: str = COLLECTION_NAME):
        self._embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True
        )
        self._client = chromadb.PersistentClient(
            path=db_path, settings=Settings(anonymized_telemetry=False)
        )
        self._collection = self._client.get_collection(
            name=collection_name, embedding_function=self._embedding_fn
        )

    def search(self, query: str, top_k: int = RAG_TOP_K) -> str:
        try:
            results = self._collection.query(
                query_texts=[query], n_results=top_k, include=["documents"]
            )
            docs = results["documents"][0] if results["documents"] else []
            return "\n\n---\n\n".join(docs) if docs else "관련 문서 없음"
        except Exception as e:
            return f"검색 오류: {e}"


# ============ Tool Maker & Skill Library (자가 진화) ============
class AgentSkillLibrary:
    """agent_tools/ 디렉터리에 저장된 도구 검색 및 저장"""

    def __init__(self, tools_dir: Path = AGENT_TOOLS_DIR):
        self.tools_dir = Path(tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)

    def list_tools(self) -> list[tuple[str, str]]:
        """(파일명, 파일 내용 요약) 리스트 반환"""
        result = []
        for p in self.tools_dir.glob("*.py"):
            try:
                content = p.read_text(encoding="utf-8")
                summary = content[:300].replace("\n", " ") + ("..." if len(content) > 300 else "")
                result.append((p.stem, summary))
            except Exception:
                pass
        return result

    def get_tools_context(self, query: str = "") -> str:
        """Planner용: 기존 도구 목록을 문자열로 반환"""
        tools = self.list_tools()
        if not tools:
            return "저장된 도구 없음."
        lines = [f"- {name}: {desc[:200]}..." for name, desc in tools]
        return "\n".join(lines)

    def save_tool(self, code: str, request_hint: str = "") -> str | None:
        """성공한 코드를 .py 파일로 저장. 파일명 반환."""
        try:
            safe_name = re.sub(r"[^\w가-힣]", "_", request_hint[:30]) or "tool"
            safe_name = safe_name.strip("_") or "tool"
            base = safe_name
            idx = 0
            while (self.tools_dir / f"{base}.py").exists():
                idx += 1
                base = f"{safe_name}_{idx}"
            path = self.tools_dir / f"{base}.py"
            path.write_text(code, encoding="utf-8")
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
            self._llm = ChatOllama(model=OLLAMA_MODEL, temperature=0.3)
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

    def maybe_compress(self) -> None:
        """최근 MEMORY_K턴은 원본 유지, 그 이전은 Qwen으로 요약 후 제거"""
        if len(self.recent_messages) <= MEMORY_K:
            return
        to_remove = len(self.recent_messages) - MEMORY_K
        to_summarize = "\n".join(
            f"{u}\n{a}" for u, a in list(self.recent_messages)[:to_remove]
        )
        if to_summarize:
            self.summary = self._summarize_old(to_summarize)
        for _ in range(to_remove):
            self.recent_messages.popleft()
        self._save_to_store()


# CHAT_ID → SessionMemory
_sessions: dict[str, SessionMemory] = {}
# CHAT_ID → (thread_id, config) for HITL resume
_pending_approvals: dict[str, tuple[str, dict]] = {}


def get_session(chat_id: str) -> SessionMemory:
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


# ============ LLM 인스턴스 ============
def get_planner_llm():
    return ChatOllama(model=OLLAMA_MODEL, temperature=0.2)


def get_executor_llm():
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL, api_key=GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"), temperature=0.1
    )


def get_monitor_llm():
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL, api_key=GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"), temperature=0.1
    )


# ============ 노드 함수 ============
def planner_node(state: AgentState, *, config: RunnableConfig) -> dict:
    """Planner: Qwen으로 계획 수립 → HITL interrupt"""
    conf = config.get("configurable", {})
    rag = ChromaRAGTool()
    skill_lib = AgentSkillLibrary()
    rag_context = rag.search(state["user_request"])
    tools_context = skill_lib.get_tools_context()

    llm = get_planner_llm()
    session = get_session(str(conf.get("chat_id", "")))

    prompt = f"""[기존 도구 라이브러리 - agent_tools/ 폴더]
반드시 먼저 확인: 비슷한 요청이면 새로 코딩하지 말고 아래 기존 도구를 재활용해.
{tools_context}

[참고 지식 - 필요시 활용]
{rag_context[:2000]}

[대화 맥락]
{session.get_context()}

[사용자 요청]
{state["user_request"]}

위 요청을 수행하기 위한 구체적인 파이썬 코딩/실행 계획을 단계별로 나열해.
- 기존 도구로 해결 가능하면 '기존 도구 X 사용' 형태로 계획에 포함.
- 새 코드가 필요하면 단계별로 작성. 3~7단계 정도로."""

    resp = llm.invoke([HumanMessage(content=prompt)])
    plan_text = resp.content.strip() if resp.content else "계획 생성 실패"
    plan_lines = [
        ln.strip() for ln in plan_text.split("\n")
        if ln.strip() and (ln.strip()[0].isdigit() or ln.strip().startswith("-") or ln.strip().startswith("•"))
    ]
    if not plan_lines:
        plan_lines = [plan_text]

    bot = conf.get("bot")
    chat_id = str(conf.get("chat_id", ""))

    plan_display = "\n".join(f"• {p}" for p in plan_lines)
    msg = (
        f"📋 **계획을 세웠습니다.**\n\n{plan_display}\n\n"
        "실행할까요? **승인** 또는 **거절** 로 답장해 주세요."
    )

    if bot and chat_id:
        try:
            bot.send_message(chat_id, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"텔레그램 전송 오류: {e}")

    approval = interrupt({"plan": plan_lines, "status": "pending"})
    approval_str = str(approval).strip().lower() if approval else ""

    if "승인" in approval_str or approval_str == "승인":
        return {"plan": plan_lines, "approval_status": "approved"}
    return {"approval_status": "rejected"}


def _run_code_sandbox(code: str) -> str:
    """E2B 클라우드 샌드박스에서 코드 실행 (30초 timeout, Host 완전 격리)"""
    if not os.getenv("E2B_API_KEY"):
        return "실행 오류: E2B_API_KEY가 .env에 설정되지 않았습니다."

    try:
        with Sandbox.create() as sandbox:
            execution = sandbox.run_code(code, timeout=CODE_TIMEOUT_SEC)

            if execution.error:
                err_msg = (
                    f"{execution.error.name}: {execution.error.value}\n"
                    f"{execution.error.traceback or ''}"
                )
                truncated = err_msg[-ERROR_LOG_MAX_CHARS:] if len(err_msg) > ERROR_LOG_MAX_CHARS else err_msg
                return f"실행 오류: {truncated}"

            stdout_parts = execution.logs.stdout if execution.logs else []
            stderr_parts = execution.logs.stderr if execution.logs else []
            stdout = "".join(stdout_parts).strip() if stdout_parts else ""
            stderr = "".join(stderr_parts).strip() if stderr_parts else ""

            result_text = execution.text or ""
            combined = stdout or result_text or stderr
            return combined.strip() or "실행 완료 (출력 없음)"

    except Exception as e:
        err_str = str(e)
        if len(err_str) > ERROR_LOG_MAX_CHARS:
            err_str = f"...{err_str[-ERROR_LOG_MAX_CHARS:]}"
        return f"실행 오류: {type(e).__name__}: {err_str}"


def executor_node(state: AgentState) -> dict:
    """Executor: Gemini로 코드 작성 및 exec/eval 실행"""
    if state.get("approval_status") != "approved":
        return {"generated_code": "", "execution_result": "승인되지 않음"}

    rag = ChromaRAGTool()
    skill_lib = AgentSkillLibrary()
    rag_context = rag.search(state["user_request"])
    tools_context = skill_lib.get_tools_context()

    llm = get_executor_llm()
    plan_str = "\n".join(f"{i+1}. {p}" for i, p in enumerate(state.get("plan", [])))
    error_hint = state.get("error_hint", "")

    prompt = f"""[기존 도구 - agent_tools/]
계획에서 기존 도구 사용이 언급되면 import하거나 subprocess로 실행해.
{tools_context}

[참고 지식]
{rag_context[:1500]}

[실행 계획]
{plan_str}

[요청]
{state["user_request"]}
"""
    if error_hint:
        prompt += f"\n[이전 실행 에러 - 반드시 수정할 것]\n{error_hint}\n"

    prompt += """
위 계획에 따라 파이썬 코드를 작성해. try-except로 감싸고, print()로 결과를 출력해.
코드 블록만 반환 (```python ... ``` 없이 순수 코드만)."""

    resp = llm.invoke([HumanMessage(content=prompt)])
    code = resp.content.strip() if resp.content else ""
    for marker in ("```python", "```"):
        if marker in code:
            start = code.find(marker) + len(marker)
            end = code.rfind("```")
            if end > start:
                code = code[start:end].strip()
            break

    # subprocess로 샌드박스 실행 (exec/eval 사용 금지)
    result = _run_code_sandbox(code)

    return {"generated_code": code, "execution_result": result}


def _truncate_error(log: str, max_chars: int = ERROR_LOG_MAX_CHARS) -> str:
    """에러 로그 압축: 마지막 N자만 전달"""
    if len(log) <= max_chars:
        return log
    return f"...(생략)...\n{log[-max_chars:]}"


def monitor_node(state: AgentState) -> dict:
    """Monitor: 실행 결과 감시 → 에러 시 error_hint와 함께 Executor로 (로그 압축)"""
    result = state.get("execution_result", "")
    retry = state.get("retry_count", 0)
    max_retry = 2

    is_error = "오류" in result or "Error" in result or "Exception" in result or "Timeout" in result

    if is_error and retry < max_retry:
        truncated = _truncate_error(result)
        llm = get_monitor_llm()
        resp = llm.invoke(
            [
                HumanMessage(
                    content=f"실행 결과(에러):\n{truncated}\n\n"
                    f"기존 코드:\n{state.get('generated_code','')[:1500]}\n\n"
                    "에러 원인을 짧게 분석하고, 수정 방향 1문장으로 알려줘."
                )
            ]
        )
        hint = resp.content.strip() if resp.content else "재시도"
        return {"retry_count": retry + 1, "error_hint": hint}
    return {}


def route_after_monitor(state: AgentState) -> Literal["executor", "__end__"]:
    result = state.get("execution_result", "")
    retry = state.get("retry_count", 0)
    is_error = "오류" in result or "Error" in result or "Exception" in result or "Timeout" in result
    if is_error and retry < 2:
        return "executor"
    return "__end__"


# ============ 그래프 빌드 ============
def build_graph(checkpointer=None):
    """SqliteSaver로 영구 체크포인트 (봇 재시작 후에도 State 복구)"""
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("monitor", monitor_node)

    workflow.set_entry_point("planner")
    workflow.add_conditional_edges("planner", lambda s: "executor" if s.get("approval_status") == "approved" else "__end__", {"executor": "executor", "__end__": END})
    workflow.add_edge("executor", "monitor")
    workflow.add_conditional_edges("monitor", route_after_monitor, {"executor": "executor", "__end__": END})

    if checkpointer is None:
        conn = sqlite3.connect(CHECKPOINT_DB_PATH, check_same_thread=False)
        checkpointer = SqliteSaver(conn)
    return workflow.compile(checkpointer=checkpointer)


# ============ 텔레그램 봇 ============
def main():
    if not all([TELEGRAM_TOKEN, ALLOWED_CHAT_ID, GEMINI_API_KEY]):
        print("❌ .env에 AGENT_BOT_TOKEN(또는 TELEGRAM_TOKEN), ALLOWED_CHAT_ID, GEMINI_API_KEY를 설정하세요.")
        return
    if not os.getenv("E2B_API_KEY"):
        print("⚠️ E2B_API_KEY가 .env에 없습니다. Executor의 코드 실행이 실패합니다.")

    allowed_ids = [a.strip() for a in ALLOWED_CHAT_ID.split(",")]
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    conn = sqlite3.connect(CHECKPOINT_DB_PATH, check_same_thread=False)
    graph = build_graph(checkpointer=SqliteSaver(conn))

    # 재시작 후: 체크포인트에서 승인 대기 중인 세션 복구
    for cid in allowed_ids:
        cfg = {"configurable": {"thread_id": f"tg_{cid}", "chat_id": cid, "bot": bot}}
        try:
            state = graph.get_state(cfg)
            if state and state.next:
                _pending_approvals[cid] = (cfg["configurable"]["thread_id"], cfg)
        except Exception:
            pass

    def run_or_resume(chat_id: str, user_text: str, thread_id: str | None = None, config: dict | None = None, is_resume: bool = False):
        cfg = config if config else {"configurable": {"thread_id": thread_id or f"tg_{chat_id}", "chat_id": chat_id, "bot": bot}}
        try:
            if is_resume:
                for event in graph.stream(Command(resume=user_text), cfg):
                    pass
            else:
                for event in graph.stream({"user_request": user_text, "plan": [], "approval_status": "pending", "generated_code": "", "execution_result": "", "retry_count": 0}, cfg):
                    pass

            state = graph.get_state(cfg)
            values = state.values if hasattr(state, "values") else {}
            if state.next:
                _pending_approvals[chat_id] = (cfg["configurable"]["thread_id"], cfg)
                return

            if chat_id in _pending_approvals:
                del _pending_approvals[chat_id]

            session = get_session(chat_id)
            # Resume 시 원본 요청(user_request) 사용, 신규 요청 시 user_text 사용
            user_msg_for_memory = values.get("user_request", user_text) if is_resume else user_text
            session.add_turn(user_msg_for_memory, "")

            if values.get("approval_status") == "rejected":
                bot.send_message(chat_id, "❌ 거절되었습니다. 계획이 취소되었습니다.")
                session.recent_messages[-1] = (session.recent_messages[-1][0], "거절되었습니다.")
                session.save()
                return

            code = values.get("generated_code", "")
            result = values.get("execution_result", "")
            request = values.get("user_request", "")

            # Tool Maker: 최종 성공 시 agent_tools/에 저장
            saved_tool = None
            if code and not ("오류" in result or "Error" in result or "Exception" in result or "Timeout" in result):
                saved_tool = AgentSkillLibrary().save_tool(code, request)

            out = f"✅ **실행 완료**\n\n```\n{result[:3500]}\n```"
            if saved_tool:
                out += f"\n\n📦 도구 저장됨: `agent_tools/{saved_tool}`"
            if code:
                out += f"\n\n📝 **생성된 코드**\n```python\n{code[:1500]}\n```"
            try:
                bot.send_message(chat_id, out, parse_mode="Markdown")
            except Exception:
                bot.send_message(chat_id, f"실행 완료\n\n{result[:4000]}")

            session.recent_messages[-1] = (session.recent_messages[-1][0], result[:500])
            session.maybe_compress()
            session.save()

        except Exception as e:
            err_detail = str(e)[:300]
            print(f"❌ 그래프 오류: {e}\n{traceback.format_exc()}")
            if "11434" in err_detail or "ConnectionError" in err_detail or "Ollama" in err_detail:
                bot.send_message(chat_id, "⚠️ Ollama 서버에 연결할 수 없습니다. `ollama serve`를 실행한 뒤 다시 시도해 주세요.")
            else:
                bot.send_message(chat_id, f"서버 오류가 발생했습니다.\n({err_detail[:100]})")

    @bot.message_handler(func=lambda m: True)
    def handle(message):
        chat_id = str(message.chat.id)
        if chat_id not in allowed_ids:
            bot.reply_to(message, "접근 권한이 없는 사용자입니다.")
            return

        text = (message.text or "").strip()
        if not text:
            bot.reply_to(message, "메시지를 입력해 주세요.")
            return

        thread_id = f"tg_{chat_id}"

        if chat_id in _pending_approvals:
            tid, cfg = _pending_approvals[chat_id]
            if "승인" in text or "거절" in text:
                run_or_resume(chat_id, text, config=cfg, is_resume=True)
                return
            else:
                bot.reply_to(message, "승인 또는 거절로 답장해 주세요.")
                return

        status_msg = bot.send_message(chat_id, "🔍 계획을 세우는 중...")
        try:
            run_or_resume(chat_id, text, thread_id, is_resume=False)
            try:
                bot.delete_message(chat_id, status_msg.message_id)
            except Exception:
                pass
        except Exception as e:
            err_detail = str(e)[:300]
            print(f"❌ 오류: {e}")
            err_msg = "⚠️ Ollama 서버에 연결할 수 없습니다. `ollama serve`를 실행한 뒤 다시 시도해 주세요." if ("11434" in err_detail or "ConnectionError" in err_detail or "Ollama" in err_detail) else f"서버 오류가 발생했습니다.\n({err_detail[:80]})"
            try:
                bot.edit_message_text(err_msg, chat_id, status_msg.message_id)
            except Exception:
                bot.send_message(chat_id, err_msg)

    print("🤖 Agent 봇 시작 (Ctrl+C로 종료)")
    bot.remove_webhook()
    bot.infinity_polling()


if __name__ == "__main__":
    main()
