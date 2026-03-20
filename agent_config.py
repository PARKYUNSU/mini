"""Agent 봇 설정·상수·경로"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Tavily Search (웹 검색 유일 엔진)
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
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
AGENT_LEARNINGS_PATH = Path("agent_learnings/ERRORS.md")
CODE_TIMEOUT_SEC = 30
ERROR_LOG_MAX_CHARS = 1000
CHECKPOINT_DB_PATH = "./agent_checkpoints.db"
CHAT_MEMORY_DB_PATH = "./chat_memory.db"
BACKFILL_SCRIPT_PATH = PROJECT_ROOT / "run_backfill.py"
BACKFILL_LOG_PATH = PROJECT_ROOT / "backfill_2023_2026.log"
BACKFILL_PID_PATH = PROJECT_ROOT / ".backfill.pid"
# cron_engine: 스케줄 작업 저장 경로 (add_job, list_jobs 등)
CRON_JOBS_DIR = PROJECT_ROOT / ".cron"
LLM_RETRY_MAX = 3
LLM_RETRY_DELAY_SEC = 1.5


def ollama_kwargs(**extra) -> dict:
    """Ollama 공통 옵션: timeout·keep_alive로 Broken pipe 방지"""
    return {"model": OLLAMA_MODEL, "timeout": OLLAMA_TIMEOUT, "keep_alive": OLLAMA_KEEP_ALIVE, **extra}
