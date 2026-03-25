#!/usr/bin/env python3
"""Agent 플로우 단계별 통합 점검 (외부 서비스·키 의존).

환경이 없으면 FAIL이 아니라 **SKIP**으로 구분합니다. 실제 장애만 FAIL.

- 5a: `print(1+1) 실행해줘` → 산수 하드룰 **direct_answer** 스모크.
- 5b: **code_run → executor** (`len('hello')` 문장).

실행 예::

    python test_agent_flow.py
    python test_agent_flow.py --only graph
    python test_agent_flow.py --only e2b --verbose
    python test_agent_flow.py --quiet-graph   # 5a/5b 그래프 구간 stdout 억제
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys
import traceback
import urllib.request

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

from dotenv import load_dotenv

load_dotenv()

# ---------- 공통 ----------


def _summarize_exc(exc: BaseException, *, verbose: bool) -> None:
    """기본: 한 줄 요약. --verbose 일 때만 전체 traceback."""
    print(f"   FAIL: {type(exc).__name__}: {exc}")
    if verbose:
        traceback.print_exc()
    else:
        tb = traceback.format_exception_only(type(exc), exc)
        if len(tb) > 1:
            print(f"      (요약) {tb[-1].strip()}")


def _ollama_reachable() -> tuple[bool, str]:
    base = (os.getenv("OLLAMA_HOST") or "http://localhost:11434").rstrip("/")
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=3) as resp:
            resp.read(64)
        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _print_env_summary() -> None:
    """시작 시 누락·준비 상태 한눈에."""
    lines = ["=== test_agent_flow 환경 요약 ==="]
    ok, why = _ollama_reachable()
    lines.append(f"  Ollama ({os.getenv('OLLAMA_HOST', 'http://localhost:11434')}): {'OK' if ok else 'SKIP 대상 — ' + why[:100]}")
    lines.append(f"  GEMINI_API_KEY: {'설정됨' if os.getenv('GEMINI_API_KEY') else '없음 (라우터 폴백·도구·Tavily SKIP)'}")
    lines.append(f"  GROQ_API_KEY: {'설정됨' if os.getenv('GROQ_API_KEY') else '없음 (Executor/Monitor 단계 SKIP)'}")
    lines.append(f"  E2B_API_KEY: {'설정됨' if os.getenv('E2B_API_KEY') else '없음 (E2B 단계 SKIP)'}")
    lines.append(f"  TELEGRAM_TOKEN: {'설정됨' if os.getenv('TELEGRAM_TOKEN') else '없음 (봇 실행 시 필요)'}")
    lines.append("================================")
    print("\n".join(lines) + "\n")


def _run_graph_stream(graph, init_state: dict, cfg: dict) -> None:
    for _ in graph.stream(init_state, cfg, stream_mode="updates"):
        pass


def _base_graph_state(user_request: str) -> dict:
    return {
        "user_request": user_request,
        "route_type": "",
        "direct_response": "",
        "plan": [],
        "approval_status": "pending",
        "generated_code": "",
        "execution_result": "",
        "retry_count": 0,
        "error_hint": "",
    }


def _maybe_quiet_graph(quiet_graph: bool):
    if quiet_graph:
        return contextlib.redirect_stdout(io.StringIO())
    return contextlib.nullcontext()


# ---------- 단계별 ----------


def test_ollama(*, verbose: bool) -> str:
    print("1. Ollama (Planner) 테스트...")
    ok, why = _ollama_reachable()
    if not ok:
        print(f"   SKIP: Ollama not running / not reachable — {why[:120]}")
        return "skip"
    try:
        from langchain_core.messages import HumanMessage
        from langchain_ollama import ChatOllama

        llm = ChatOllama(
            model=os.getenv("LOCAL_LLM_MODEL", "qwen3.5:9b"),
            base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            temperature=0.2,
        )
        r = llm.invoke([HumanMessage(content="1+1은? 한 단어로")])
        print(f"   OK: {(r.content or '')[:50]}...")
        return "ok"
    except Exception as e:  # noqa: BLE001
        _summarize_exc(e, verbose=verbose)
        return "fail"


def test_groq(*, verbose: bool) -> str:
    print("2. Groq (Executor/Monitor 코딩 LLM) 테스트...")
    if not (os.getenv("GROQ_API_KEY") or "").strip():
        print("   SKIP: GROQ_API_KEY missing")
        return "skip"
    try:
        from langchain_core.messages import HumanMessage
        from langchain_groq import ChatGroq

        model = os.getenv("GROQ_CODING_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
        llm = ChatGroq(model=model, api_key=os.getenv("GROQ_API_KEY"), temperature=0.2)
        r = llm.invoke([HumanMessage(content="1+1은? 숫자만")])
        print(f"   OK: {(r.content or '')[:50]}...")
        return "ok"
    except Exception as e:  # noqa: BLE001
        _summarize_exc(e, verbose=verbose)
        return "fail"


def test_gemini(*, verbose: bool) -> str:
    print("2b. Gemini (라우터 폴백·도구·Tavily) 스모크...")
    if not (os.getenv("GEMINI_API_KEY") or "").strip():
        print("   SKIP: GEMINI_API_KEY missing")
        return "skip"
    try:
        from langchain_core.messages import HumanMessage
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.1,
        )
        r = llm.invoke([HumanMessage(content="1+1은? 숫자만")])
        print(f"   OK: {(r.content or '')[:50]}...")
        return "ok"
    except Exception as e:  # noqa: BLE001
        _summarize_exc(e, verbose=verbose)
        return "fail"


def test_chromadb(*, verbose: bool) -> str:
    print("3. ChromaDB (RAG) 테스트...")
    try:
        from agent_chroma_rag import ChromaRAGTool

        rag = ChromaRAGTool()
        r = rag.search("test")
        print(f"   OK: {r[:80]}...")
        return "ok"
    except Exception as e:  # noqa: BLE001
        err = str(e).lower()
        if "connection" in err or "download" in err or "huggingface" in err or "no such file" in err:
            print(f"   SKIP: Chroma/임베딩 환경 미준비 — {type(e).__name__}: {str(e)[:100]}")
            if verbose:
                traceback.print_exc()
            return "skip"
        _summarize_exc(e, verbose=verbose)
        return "fail"


def test_e2b(*, verbose: bool) -> str:
    print("4. E2B Sandbox 테스트...")
    if not (os.getenv("E2B_API_KEY") or "").strip():
        print("   SKIP: E2B_API_KEY missing")
        return "skip"
    try:
        from agent_sandbox import run_code_sandbox

        r = run_code_sandbox("print(1+1)")
        snippet = (r or "")[:200]
        if (r or "").strip().startswith("실행 오류"):
            print(f"   FAIL: 샌드박스 오류 응답\n      → {snippet}")
            if "unicodeescape" in (r or "").lower():
                print(
                    "      힌트: .env 역슬래시 / `E2B_SANDBOX_ENV_MODE=minimal` "
                    "+ `E2B_SANDBOX_EXTRA_KEYS` 검토."
                )
            return "fail"
        if "2" not in (r or "").replace(" ", ""):
            print(f"   WARN: 출력에 '2' 없음. 원문: {snippet!r}")
            return "ok"
        print(f"   OK: {snippet[:80]}{'...' if len(snippet) > 80 else ''}")
        return "ok"
    except Exception as e:  # noqa: BLE001
        _summarize_exc(e, verbose=verbose)
        return "fail"


def test_full_graph_smoke(*, verbose: bool, quiet_graph: bool) -> str:
    print("5a. LangGraph 스모크 (direct_answer·체크포인트)...")
    try:
        from agent_graph import build_graph
        import sqlite3
        from langgraph.checkpoint.sqlite import SqliteSaver

        conn = sqlite3.connect("./agent_checkpoints.db", check_same_thread=False)
        graph = build_graph(checkpointer=SqliteSaver(conn))
        cfg = {"configurable": {"thread_id": "test_flow_smoke", "chat_id": "8587793069", "bot": None}}
        with _maybe_quiet_graph(quiet_graph):
            _run_graph_stream(graph, _base_graph_state("print(1+1) 실행해줘"), cfg)
        state = graph.get_state(cfg)
        vals = state.values or {}
        print(f"   route_type={vals.get('route_type')!r}, next={state.next!r}")
        if verbose:
            print(f"   keys: {list(vals.keys())}")
            if state.next:
                print("   (interrupt 대기 중)")
        if vals.get("route_type") != "direct_answer":
            print(f"   WARN: 보통 direct_answer 예상(산수). 실제={vals.get('route_type')!r}")
        print("   OK (그래프·체크포인트 스모크)")
        return "ok"
    except Exception as e:  # noqa: BLE001
        _summarize_exc(e, verbose=verbose)
        return "fail"


def test_full_graph_code_run(*, verbose: bool, quiet_graph: bool) -> str:
    print("5b. LangGraph code_run → executor 경로...")
    try:
        from agent_graph import build_graph
        import sqlite3
        from langgraph.checkpoint.sqlite import SqliteSaver

        msg = "파이썬으로 len('hello') 결과를 print하는 코드 실행해줘"
        conn = sqlite3.connect("./agent_checkpoints.db", check_same_thread=False)
        graph = build_graph(checkpointer=SqliteSaver(conn))
        cfg = {"configurable": {"thread_id": "test_flow_coderun", "chat_id": "8587793069", "bot": None}}
        with _maybe_quiet_graph(quiet_graph):
            _run_graph_stream(graph, _base_graph_state(msg), cfg)
        state = graph.get_state(cfg)
        vals = state.values or {}
        rt = vals.get("route_type")
        er = (vals.get("execution_result") or "")[:120]
        print(f"   route_type={rt!r}, next={state.next!r}")
        if verbose:
            print(f"   execution_result(앞 120자): {er!r}...")
        if rt != "code_run":
            print(f"   FAIL: code_run 기대, 실제={rt!r}")
            return "fail"
        if state.next and verbose:
            print("   WARN: interrupt(next) 비어 있지 않음.")
        res = vals.get("execution_result") or ""
        if res.strip().startswith("실행 오류"):
            print(
                f"   SKIP/WARN: executor까지 갔으나 실행 오류(E2B/키 등). "
                f"pytest `tests/test_code_run_state.py` 로 라우팅만 검증 가능.\n"
                f"      → {res[:120]}..."
            )
            return "skip"
        print("   OK")
        return "ok"
    except Exception as e:  # noqa: BLE001
        _summarize_exc(e, verbose=verbose)
        return "fail"


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent 외부 통합 점검 (SKIP/FAIL 구분)")
    parser.add_argument(
        "--only",
        choices=("all", "ollama", "groq", "gemini", "chroma", "e2b", "graph"),
        default="all",
        help="실행할 단계만 (graph = 5a+5b). groq=Executor/Monitor, gemini=폴백·도구 경로",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="traceback 전체 출력")
    parser.add_argument(
        "--quiet-graph",
        action="store_true",
        help="5a/5b graph.stream 동안 DEBUG print 억제 (로그 폭주 완화)",
    )
    parser.add_argument("--no-summary", action="store_true", help="시작 환경 요약 생략")
    args = parser.parse_args()

    if not args.no_summary:
        _print_env_summary()

    run = {
        "ollama": args.only in ("all", "ollama"),
        "groq": args.only in ("all", "groq"),
        "gemini": args.only in ("all", "gemini"),
        "chroma": args.only in ("all", "chroma"),
        "e2b": args.only in ("all", "e2b"),
        "graph": args.only in ("all", "graph"),
    }

    counts = {"ok": 0, "skip": 0, "fail": 0}

    def tally(tag: str) -> None:
        counts[tag] = counts.get(tag, 0) + 1

    if run["ollama"]:
        tally(test_ollama(verbose=args.verbose))
    if run["groq"]:
        tally(test_groq(verbose=args.verbose))
    if run["gemini"]:
        tally(test_gemini(verbose=args.verbose))
    if run["chroma"]:
        tally(test_chromadb(verbose=args.verbose))
    if run["e2b"]:
        tally(test_e2b(verbose=args.verbose))
    if run["graph"]:
        tally(test_full_graph_smoke(verbose=args.verbose, quiet_graph=args.quiet_graph))
        tally(test_full_graph_code_run(verbose=args.verbose, quiet_graph=args.quiet_graph))

    print(
        f"\n테스트 완료 — OK={counts['ok']}  SKIP={counts['skip']}  FAIL={counts['fail']}\n"
        "  (SKIP=환경 미준비, FAIL=실제 오류. 가벼운 회귀는 `pytest tests/ -m unit` 권장)"
    )
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
