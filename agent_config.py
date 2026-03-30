"""Agent 봇 설정·상수·경로"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# 번호형 변수: GEMINI_API_KEY + GEMINI_API_KEY_2 … _N (아래 끝 번호까지, 비어 있으면 스킵)
_GEMINI_API_KEY_NUMBERED_MAX = 8


def get_gemini_api_keys() -> list[str]:
    """
    Gemini 키 목록 (순서대로 사용, 429 시 다음 키로 폴백).

    - ``GEMINI_API_KEYS=key1,key2,...`` 가 비어 있지 않으면 이 목록만 사용 (개수 제한 없음).
    - 그렇지 않으면 ``GEMINI_API_KEY``, ``GEMINI_API_KEY_2`` … ``GEMINI_API_KEY_8`` 중
      값이 있는 것만 순서대로 사용.
    """
    raw = (os.getenv("GEMINI_API_KEYS") or "").strip()
    keys: list[str] = []
    if raw:
        keys = [p.strip() for p in raw.split(",") if p.strip()]
    if not keys:
        primary = (os.getenv("GEMINI_API_KEY") or "").strip()
        if primary:
            keys.append(primary)
        for i in range(2, _GEMINI_API_KEY_NUMBERED_MAX + 1):
            v = (os.getenv(f"GEMINI_API_KEY_{i}") or "").strip()
            if v:
                keys.append(v)
    seen: set[str] = set()
    out: list[str] = []
    for k in keys:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out


PROJECT_ROOT = Path(__file__).resolve().parent
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Tavily Search (웹 검색 유일 엔진)
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID")
_GEMINI_KEYS = get_gemini_api_keys()
GEMINI_API_KEY = _GEMINI_KEYS[0] if _GEMINI_KEYS else os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "arxiv_papers"
# agent_tools/ 전용 RAG (논문 DB와 분리)
TOOL_CHROMA_DB_PATH = "./tool_chroma_db"
TOOL_COLLECTION_NAME = "agent_tools_rag"
TOOL_RAG_TOP_K = 3
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = os.getenv("LOCAL_LLM_MODEL", "qwen3.5:9b")
OLLAMA_TIMEOUT = 120
OLLAMA_KEEP_ALIVE = os.getenv("OLLAMA_KEEP_ALIVE", "-1s")  # -1은 invalid, -1s 등 단위 필요
GEMINI_MODEL = "gemini-2.5-flash"
MEMORY_K = 5
MEMORY_BUFFER = 15
RAG_TOP_K = 3
# cwd와 무관하게 항상 패키지 기준 (상대 경로만 쓰면 다른 디렉터리에서 실행 시 도구 미탐지)
AGENT_TOOLS_DIR = PROJECT_ROOT / "agent_tools"
# 봇이 새로 저장하는 일회성 도구 (gitignore 대상, 코어 도구는 AGENT_TOOLS_DIR 루트)
AGENT_TOOLS_SAVED_DIR = AGENT_TOOLS_DIR / "saved"
AGENT_LEARNINGS_PATH = Path("agent_learnings/ERRORS.md")
CODE_TIMEOUT_SEC = 30
ERROR_LOG_MAX_CHARS = 1000
CHECKPOINT_DB_PATH = "./agent_checkpoints.db"
CHAT_MEMORY_DB_PATH = "./chat_memory.db"
BACKFILL_SCRIPT_PATH = PROJECT_ROOT / "run_backfill.py"
BACKFILL_LOG_PATH = PROJECT_ROOT / "backfill_2023_2026.log"
BACKFILL_PID_PATH = PROJECT_ROOT / ".backfill.pid"
LLM_DEBATE_SCHEDULER_PATH = PROJECT_ROOT / "llm_debate_scheduler.py"
LLM_DEBATE_TELEGRAM_LOG_PATH = PROJECT_ROOT / "llm_debate_telegram.log"
LLM_DEBATE_TELEGRAM_PID_PATH = PROJECT_ROOT / ".llm_debate.telegram.pid"
try:
    # 0 이하 = 시간 제한 없음 (큐 소진 또는 /debate_stop까지)
    LLM_DEBATE_TELEGRAM_DURATION_SEC = int(os.getenv("LLM_DEBATE_TELEGRAM_DURATION_SEC", "0"))
except ValueError:
    LLM_DEBATE_TELEGRAM_DURATION_SEC = 0
# cron_engine: 스케줄 작업 저장 경로 (add_job, list_jobs 등)
CRON_JOBS_DIR = PROJECT_ROOT / ".cron"
LLM_RETRY_MAX = 3
LLM_RETRY_DELAY_SEC = 1.5


def resolve_agent_tool_py(stem: str, tools_dir: Path | None = None) -> Path | None:
    """`agent_tools/<stem>.py` 또는 `agent_tools/saved/<stem>.py`. 없으면 None."""
    root = tools_dir if tools_dir is not None else AGENT_TOOLS_DIR
    direct = root / f"{stem}.py"
    if direct.is_file():
        return direct
    saved = root / "saved" / f"{stem}.py"
    if saved.is_file():
        return saved
    return None


def ollama_kwargs(**extra) -> dict:
    """Ollama 공통 옵션: base_url·timeout·keep_alive (langchain_ollama.ChatOllama 호환)."""
    return {
        "model": OLLAMA_MODEL,
        "base_url": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        "timeout": OLLAMA_TIMEOUT,
        "keep_alive": OLLAMA_KEEP_ALIVE,
        **extra,
    }
