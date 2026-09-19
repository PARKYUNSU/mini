"""Agent 봇 설정·상수·경로"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# 번호형 변수: GEMINI_API_KEY + GEMINI_API_KEY_2 … _N (아래 끝 번호까지, 비어 있으면 스킵)
_GEMINI_API_KEY_NUMBERED_MAX = 20


def get_gemini_api_keys() -> list[str]:
    """
    Gemini 키 목록 (순서대로 사용, 429 시 다음 키로 폴백).

    - ``GEMINI_API_KEYS=key1,key2,...`` 가 비어 있지 않으면 이 목록만 사용 (개수 제한 없음).
    - 그렇지 않으면 ``GEMINI_API_KEY``, ``GEMINI_API_KEY_2`` … ``GEMINI_API_KEY_20`` 중
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


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Tavily Search (웹 검색 유일 엔진)
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID")
_GEMINI_KEYS = get_gemini_api_keys()
GEMINI_API_KEY = _GEMINI_KEYS[0] if _GEMINI_KEYS else os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Chroma 논문 DB: 기본은 프로젝트 상대 경로. 외장 디스크에서 SQLite 1032가 나면
# CHROMA_DB_PATH=/절대/경로 로 내부 디스크 등에 둔 디렉터리를 지정 (예: ~/Library/.../mini-chroma).
_chroma_raw = (os.getenv("CHROMA_DB_PATH") or "").strip()
if _chroma_raw:
    CHROMA_DB_PATH = str(Path(_chroma_raw).expanduser().resolve())
else:
    CHROMA_DB_PATH = "./chroma_db"
_chroma_p = Path(CHROMA_DB_PATH)
CHROMA_DB_DIR: Path = (
    _chroma_p.resolve() if _chroma_p.is_absolute() else (PROJECT_ROOT / _chroma_p).resolve()
)
COLLECTION_NAME = "arxiv_papers"
# agent_tools/ 전용 RAG (논문 DB와 분리)
_tool_raw = (os.getenv("TOOL_CHROMA_DB_PATH") or "").strip()
if _tool_raw:
    TOOL_CHROMA_DB_PATH = str(Path(_tool_raw).expanduser().resolve())
else:
    TOOL_CHROMA_DB_PATH = "./tool_chroma_db"
_tpp = Path(TOOL_CHROMA_DB_PATH)
TOOL_CHROMA_DB_DIR: Path = (
    _tpp.resolve() if _tpp.is_absolute() else (PROJECT_ROOT / _tpp).resolve()
)
TOOL_COLLECTION_NAME = "agent_tools_rag"
TOOL_RAG_TOP_K = 3
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
OLLAMA_MODEL = os.getenv("LOCAL_LLM_MODEL", "qwen3.5:9b")
# RAG 답변(B) 전용 로컬 모델. 비어 있으면 OLLAMA_MODEL. 실험(docs/experiments/yunsur_v4): 잡담·계획·코딩은 base 가,
# RAG 답변은 yunsur_v4 가 나음 (실패율 0% vs 12%) → 슬롯별로 분리. 두 모델을 번갈아 로드하므로 RAG 첫 응답이 수 초 느려질 수 있음.
RAG_ANSWER_MODEL = (os.getenv("RAG_ANSWER_MODEL") or "").strip() or OLLAMA_MODEL
OLLAMA_TIMEOUT = 120
OLLAMA_KEEP_ALIVE = os.getenv("OLLAMA_KEEP_ALIVE", "-1s")  # -1은 invalid, -1s 등 단위 필요
# Google AI Gemini API 모델 ID. `gemini-3-flash` 단독은 v1beta에서 404 — preview 접미사 필요.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
MEMORY_K = 5
MEMORY_BUFFER = 15
RAG_TOP_K = 3
# cwd와 무관하게 항상 패키지 기준 (상대 경로만 쓰면 다른 디렉터리에서 실행 시 도구 미탐지)
AGENT_TOOLS_DIR = PROJECT_ROOT / "tools" / "runtime" / "agent_tools" / "agent_tools"
# 봇이 새로 저장하는 일회성 도구 (gitignore 대상, 코어 도구는 AGENT_TOOLS_DIR 루트)
AGENT_TOOLS_SAVED_DIR = AGENT_TOOLS_DIR / "saved"
AGENT_LEARNINGS_PATH = Path("agent_learnings/ERRORS.md")
CODE_TIMEOUT_SEC = 30
ERROR_LOG_MAX_CHARS = 1000
# LangGraph SqliteSaver — 외장 디스크·슬립 깨우기 시 disk I/O error 가 나면
# CHECKPOINT_DB_PATH=/Users/…/agent_checkpoints.db 처럼 내장 디스크 절대 경로 권장.
_checkpoint_env = (os.getenv("CHECKPOINT_DB_PATH") or "").strip()
if _checkpoint_env:
    _cp_p = Path(_checkpoint_env).expanduser()
    CHECKPOINT_DB_PATH = str(_cp_p.resolve() if _cp_p.is_absolute() else (PROJECT_ROOT / _cp_p).resolve())
else:
    CHECKPOINT_DB_PATH = str((PROJECT_ROOT / "agent_checkpoints.db").resolve())
CHAT_MEMORY_DB_PATH = "./chat_memory.db"
CHROMA_WRITE_LOCK_PATH = PROJECT_ROOT / ".chroma_write.lock"

# Chroma RAG: cross-encoder 재정렬. 대규모 청크 코퍼스에서는 지연·역효과 보고가 있어 기본 비활성.
# 켜려면 환경변수 CHROMA_CROSS_ENCODER_RERANK=1
_CHROMA_CE_RERANK_RAW = (os.getenv("CHROMA_CROSS_ENCODER_RERANK") or "0").strip().lower()
CHROMA_CROSS_ENCODER_RERANK = _CHROMA_CE_RERANK_RAW in ("1", "true", "yes", "on")

# Chroma 벡터 검색 후보 수: max(top_k * CHROMA_FETCH_MULTIPLIER, CHROMA_FETCH_MIN) (CE 끔일 때).
# 대규모 코퍼스에서 retrieval_missing 줄이기 위해 기본 fetch 확장 (env로 조정 가능).
try:
    CHROMA_FETCH_MULTIPLIER = float(os.getenv("CHROMA_FETCH_MULTIPLIER", "20"))
except ValueError:
    CHROMA_FETCH_MULTIPLIER = 20.0
if CHROMA_FETCH_MULTIPLIER < 1.0:
    CHROMA_FETCH_MULTIPLIER = 20.0
try:
    CHROMA_FETCH_MIN = int(os.getenv("CHROMA_FETCH_MIN", "100"))
except ValueError:
    CHROMA_FETCH_MIN = 100
if CHROMA_FETCH_MIN < 1:
    CHROMA_FETCH_MIN = 100
# BM25 상위 M편과 벡터 후보 합집합: 벡터에 없는 논문만 청크 주입.
try:
    BM25_UNION_TOP_M = int(os.getenv("BM25_UNION_TOP_M", "120"))
except ValueError:
    BM25_UNION_TOP_M = 120
if BM25_UNION_TOP_M < 1:
    BM25_UNION_TOP_M = 120
try:
    BM25_UNION_CHUNKS_PER_PAPER = int(os.getenv("BM25_UNION_CHUNKS_PER_PAPER", "5"))
except ValueError:
    BM25_UNION_CHUNKS_PER_PAPER = 5
if BM25_UNION_CHUNKS_PER_PAPER < 1:
    BM25_UNION_CHUNKS_PER_PAPER = 5
if BM25_UNION_CHUNKS_PER_PAPER > 8:
    BM25_UNION_CHUNKS_PER_PAPER = 8

# 인제스트: 인접 청크 임베딩 유사도로 병합 (Recall·문맥 연속성)
_ENABLE_SEM_MERGE_RAW = (os.getenv("ENABLE_SEMANTIC_MERGE") or "1").strip().lower()
ENABLE_SEMANTIC_MERGE = _ENABLE_SEM_MERGE_RAW in ("1", "true", "yes", "on")
try:
    SEMANTIC_MERGE_THRESHOLD = float(os.getenv("SEMANTIC_MERGE_THRESHOLD", "0.85"))
except ValueError:
    SEMANTIC_MERGE_THRESHOLD = 0.85
SEMANTIC_MERGE_THRESHOLD = max(0.5, min(0.99, SEMANTIC_MERGE_THRESHOLD))

# 검색: 하이브리드 후 상위 N편 논문만 임베딩 코사인으로 재정렬 (Cross-encoder 없음)
_ENABLE_PLR_RAW = (os.getenv("ENABLE_PAPER_LIGHT_RERANK") or "1").strip().lower()
ENABLE_PAPER_LIGHT_RERANK = _ENABLE_PLR_RAW in ("1", "true", "yes", "on")
try:
    PAPER_LIGHT_RERANK_TOP_K = int(os.getenv("PAPER_LIGHT_RERANK_TOP_K", os.getenv("RERANK_TOP_K", "50")))
except ValueError:
    PAPER_LIGHT_RERANK_TOP_K = 50
if PAPER_LIGHT_RERANK_TOP_K < 5:
    PAPER_LIGHT_RERANK_TOP_K = 50
if PAPER_LIGHT_RERANK_TOP_K > 200:
    PAPER_LIGHT_RERANK_TOP_K = 200

# Hybrid RRF·minmax: dense vs BM25 상대 가중 (합≈1 권장). 서베이/키워드 도메인은 BM25 균형 권장.
try:
    HYBRID_VECTOR_WEIGHT = float(os.getenv("HYBRID_VECTOR_WEIGHT", "0.5"))
except ValueError:
    HYBRID_VECTOR_WEIGHT = 0.5
try:
    HYBRID_BM25_WEIGHT = float(os.getenv("HYBRID_BM25_WEIGHT", "0.5"))
except ValueError:
    HYBRID_BM25_WEIGHT = 0.5

# 멀티 쿼리 검색: 실험 시에만. 기본 끔(0). 켜면 단일쿼리 랭킹 튜닝과 신호가 섞임 → eval·튜닝 전에는 반드시 0.
_HYBRID_MQ_RAW = (os.getenv("HYBRID_MULTI_QUERY_RETRIEVAL") or "0").strip().lower()
HYBRID_MULTI_QUERY_RETRIEVAL = _HYBRID_MQ_RAW in ("1", "true", "yes", "on")
try:
    HYBRID_MULTI_QUERY_MAX_CHUNKS = int(os.getenv("HYBRID_MULTI_QUERY_MAX_CHUNKS", "250"))
except ValueError:
    HYBRID_MULTI_QUERY_MAX_CHUNKS = 250
if HYBRID_MULTI_QUERY_MAX_CHUNKS < 50:
    HYBRID_MULTI_QUERY_MAX_CHUNKS = 250
try:
    HYBRID_MULTI_QUERY_MAX_QUERIES = int(os.getenv("HYBRID_MULTI_QUERY_MAX_QUERIES", "6"))
except ValueError:
    HYBRID_MULTI_QUERY_MAX_QUERIES = 6
if HYBRID_MULTI_QUERY_MAX_QUERIES < 1:
    HYBRID_MULTI_QUERY_MAX_QUERIES = 6
# 멀티 쿼리: 쿼리마다 독립 RRF 후 상위 N청크만 합집합(rank-then-merge).
try:
    HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS = int(os.getenv("HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS", "50"))
except ValueError:
    HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS = 50
if HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS < 10:
    HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS = 50
if HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS > 200:
    HYBRID_MULTI_QUERY_PER_QUERY_TOP_CHUNKS = 200

# Hybrid retrieval: 청크 후보 집합에서 dense·BM25 결합 방식.
# minmax = 각 시그널을 후보 내 min-max 후 HYBRID_*_WEIGHT 가중합 (기본).
# rrf = Reciprocal Rank Fusion (스케일 무관, rank만 사용; VECTOR/BM25 가중은 미적용).
_HYBRID_FUSION_RAW = (os.getenv("HYBRID_FUSION_MODE") or "minmax").strip().lower()
HYBRID_FUSION_MODE: str = _HYBRID_FUSION_RAW if _HYBRID_FUSION_RAW in ("minmax", "rrf") else "minmax"
try:
    HYBRID_RRF_K = float(os.getenv("HYBRID_RRF_K", "60"))
    if HYBRID_RRF_K < 1.0:
        HYBRID_RRF_K = 60.0
except ValueError:
    HYBRID_RRF_K = 60.0
# 메타 title에 쿼리 부분문자열이 있으면 해당 청크 하이브리드 점수에 곱함 (집계 전).
try:
    HYBRID_TITLE_BOOST_MULTIPLIER = float(os.getenv("HYBRID_TITLE_BOOST_MULTIPLIER", "1.2"))
except ValueError:
    HYBRID_TITLE_BOOST_MULTIPLIER = 1.2
# 논문 점수: 상위 N개 청크 (N=1이면 max 청크만; 여러 청크는 HYBRID_CHUNKS_PER_PAPER로 컨텍스트 유지).
try:
    HYBRID_PAPER_SCORE_TOP_N = int(os.getenv("HYBRID_PAPER_SCORE_TOP_N", "2"))
except ValueError:
    HYBRID_PAPER_SCORE_TOP_N = 2
if HYBRID_PAPER_SCORE_TOP_N < 1:
    HYBRID_PAPER_SCORE_TOP_N = 1
if HYBRID_PAPER_SCORE_TOP_N > 5:
    HYBRID_PAPER_SCORE_TOP_N = 5
try:
    HYBRID_PAPER_THIRD_BEST_GAMMA = float(os.getenv("HYBRID_PAPER_THIRD_BEST_GAMMA", "0.1"))
except ValueError:
    HYBRID_PAPER_THIRD_BEST_GAMMA = 0.1
try:
    HYBRID_PAPER_FOURTH_BEST_DELTA = float(os.getenv("HYBRID_PAPER_FOURTH_BEST_DELTA", "0.08"))
except ValueError:
    HYBRID_PAPER_FOURTH_BEST_DELTA = 0.08
try:
    HYBRID_PAPER_FIFTH_BEST_EPSILON = float(os.getenv("HYBRID_PAPER_FIFTH_BEST_EPSILON", "0.06"))
except ValueError:
    HYBRID_PAPER_FIFTH_BEST_EPSILON = 0.06
# 논문 점수에 반영할 2번째 청크 가중 (기존 명칭 유지).
try:
    HYBRID_PAPER_SECOND_BEST_ALPHA = float(os.getenv("HYBRID_PAPER_SECOND_BEST_ALPHA", "0.15"))
except ValueError:
    HYBRID_PAPER_SECOND_BEST_ALPHA = 0.15
# 논문 내 max(chunk) 대비 이 비율 이상인 청크 개수로 multi-evidence 보너스 (일관 매칭 신호).
try:
    HYBRID_PAPER_MULTIEVIDENCE_REL = float(os.getenv("HYBRID_PAPER_MULTIEVIDENCE_REL", "0.85"))
except ValueError:
    HYBRID_PAPER_MULTIEVIDENCE_REL = 0.85
try:
    HYBRID_PAPER_MULTIEVIDENCE_BETA = float(os.getenv("HYBRID_PAPER_MULTIEVIDENCE_BETA", "0"))
except ValueError:
    HYBRID_PAPER_MULTIEVIDENCE_BETA = 0.0
# 제목–쿼리 유사도 (논문 집계 후): 가산 + 고유사도 시 약한 곱 (기본). 레거시: threshold 넘으면 곱.
try:
    HYBRID_PAPER_TITLE_SIM_THRESHOLD = float(os.getenv("HYBRID_PAPER_TITLE_SIM_THRESHOLD", "0.65"))
except ValueError:
    HYBRID_PAPER_TITLE_SIM_THRESHOLD = 0.65
try:
    HYBRID_PAPER_TITLE_SIM_MULTIPLIER = float(os.getenv("HYBRID_PAPER_TITLE_SIM_MULTIPLIER", "1.0"))
except ValueError:
    HYBRID_PAPER_TITLE_SIM_MULTIPLIER = 1.0
try:
    HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT = float(os.getenv("HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT", "0.08"))
except ValueError:
    HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT = 0.08
try:
    HYBRID_PAPER_TITLE_SIM_HIGH_THRESHOLD = float(os.getenv("HYBRID_PAPER_TITLE_SIM_HIGH_THRESHOLD", "0.7"))
except ValueError:
    HYBRID_PAPER_TITLE_SIM_HIGH_THRESHOLD = 0.7
try:
    HYBRID_PAPER_TITLE_SIM_HIGH_MULTIPLIER = float(os.getenv("HYBRID_PAPER_TITLE_SIM_HIGH_MULTIPLIER", "1.05"))
except ValueError:
    HYBRID_PAPER_TITLE_SIM_HIGH_MULTIPLIER = 1.05
# (선택) 추가 가산. 0이면 비활성.
try:
    HYBRID_PAPER_TITLE_SIM_WEIGHT = float(os.getenv("HYBRID_PAPER_TITLE_SIM_WEIGHT", "0.0"))
except ValueError:
    HYBRID_PAPER_TITLE_SIM_WEIGHT = 0.0
# 논문 집계 후 논문당 유지할 청크 수 (2면 상위 2청크가 컨텍스트에 남음; 집계 점수는 TOP_N과 별개).
try:
    HYBRID_CHUNKS_PER_PAPER = int(os.getenv("HYBRID_CHUNKS_PER_PAPER", "2"))
except ValueError:
    HYBRID_CHUNKS_PER_PAPER = 2
if HYBRID_CHUNKS_PER_PAPER < 1:
    HYBRID_CHUNKS_PER_PAPER = 1
if HYBRID_CHUNKS_PER_PAPER > 5:
    HYBRID_CHUNKS_PER_PAPER = 5
# eval 스크립트·hybrid_retrieve_paper_ids_for_eval 기본: recall에 유리하도록 2.
try:
    HYBRID_EVAL_CHUNKS_PER_PAPER = int(os.getenv("HYBRID_EVAL_CHUNKS_PER_PAPER", "2"))
except ValueError:
    HYBRID_EVAL_CHUNKS_PER_PAPER = 2
if HYBRID_EVAL_CHUNKS_PER_PAPER < 1:
    HYBRID_EVAL_CHUNKS_PER_PAPER = 2
if HYBRID_EVAL_CHUNKS_PER_PAPER > 5:
    HYBRID_EVAL_CHUNKS_PER_PAPER = 5

BACKFILL_SCRIPT_PATH = PROJECT_ROOT / "apps" / "backfill" / "run_backfill.py"
BACKFILL_QUARTERLY_SCRIPT_PATH = PROJECT_ROOT / "apps" / "backfill" / "run_backfill_quarterly.py"
BACKFILL_LOG_PATH = PROJECT_ROOT / "backfill_2023_2026.log"
BACKFILL_PID_PATH = PROJECT_ROOT / ".backfill.pid"
# Phase 3.5: 윤수르 심사관 NO 트랙·아이디어 금고 (SQLite)
IDEA_VAULT_DB_PATH = PROJECT_ROOT / "idea_vault.sqlite"
LLM_DEBATE_SCHEDULER_PATH = PROJECT_ROOT / "pipelines" / "debate" / "llm_debate_scheduler.py"
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
# Direct answer (A 일상 + B RAG) 공통 LLM 호출 상한(초). 0 이하 = 무제한.
try:
    DIRECT_ANSWER_TIMEOUT_SEC = float(os.getenv("DIRECT_ANSWER_TIMEOUT_SEC", "55"))
except ValueError:
    DIRECT_ANSWER_TIMEOUT_SEC = 55.0


# RAG(B) 경로: 로컬 Ollama가 Top-5 등 긴 컨텍스트로 추론할 때 90초 부족 → 하한을 넉넉히 둠.
# `DIRECT_ANSWER_TIMEOUT_SEC`보다 큰 값과 max(초)로 적용. 짧은 일상(A)은 직전 `DIRECT_ANSWER_TIMEOUT_SEC`만 사용.
try:
    _rag_to = float(os.getenv("RAG_OLLAMA_TIMEOUT_SEC", "300"))
    RAG_OLLAMA_TIMEOUT_SEC = _rag_to if _rag_to > 0 else 300.0
except ValueError:
    RAG_OLLAMA_TIMEOUT_SEC = 300.0

# Direct Answer 1차(Ollama): 생성 토큰 상한. 너무 짧으면 긴 RAG 답변이 중간에 끊겨 재시도·이어쓰기 시 프롬프트 노출 위험이 있다.
try:
    OLLAMA_DIRECT_NUM_PREDICT = int(os.getenv("OLLAMA_DIRECT_NUM_PREDICT", "4096"))
except ValueError:
    OLLAMA_DIRECT_NUM_PREDICT = 4096


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


def ollama_planner_reasoning_enabled() -> bool:
    """Planner·PlannerDebate·llm_debate_scheduler용 Ollama ``reasoning``(thinking) 사용 여부.

    일부 로컬 모델(예: ``yunsur-v2``)은 thinking 미지원으로 ``reasoning=True`` 시 400 오류가 난다.

    - ``OLLAMA_PLANNER_REASONING`` 이 설정되면 이것만 따른다 (0/false/no/off → 끔).
    - 미설정이면 ``LOCAL_LLM_MODEL`` 이름에 ``yunsur`` 가 포함되면 자동으로 끔.
    - 그 외는 켜 둔다 (Qwen 계열 등 기존 동작).
    """
    raw = (os.getenv("OLLAMA_PLANNER_REASONING") or "").strip()
    if raw:
        return raw.lower() not in ("0", "false", "no", "off")
    model = (os.getenv("LOCAL_LLM_MODEL") or "").strip().lower()
    if "yunsur" in model:
        return False
    return True


def ollama_kwargs(**extra) -> dict:
    """Ollama 공통 옵션: base_url·timeout·keep_alive (langchain_ollama.ChatOllama 호환)."""
    return {
        "model": OLLAMA_MODEL,
        "base_url": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        "timeout": OLLAMA_TIMEOUT,
        "keep_alive": OLLAMA_KEEP_ALIVE,
        **extra,
    }
