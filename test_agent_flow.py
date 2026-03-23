#!/usr/bin/env python3
"""Agent 플로우 단계별 테스트 - 오류 원인 파악용

- 5a: `print(1+1) 실행해줘` 는 라우터 산수 패턴(`\\d+\\+\\d+`)에 걸려 **direct_answer** 로 가는 것이
  현재 규칙상 정상입니다 (스모크: 그래프·SqliteSaver·체크포인트).
- 5b: `+` 없는 실행 문장으로 **code_run → executor** 경로를 추가 검증합니다.
"""
import os
os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

from dotenv import load_dotenv
load_dotenv()


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

def test_ollama():
    print("1. Ollama (Planner) 테스트...")
    try:
        from langchain_core.messages import HumanMessage
        from langchain_ollama import ChatOllama

        llm = ChatOllama(
            model=os.getenv("LOCAL_LLM_MODEL", "qwen3.5:9b"),
            base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            temperature=0.2,
        )
        r = llm.invoke([HumanMessage(content="1+1은? 한 단어로")])
        print(f"   OK: {r.content[:50]}...")
    except Exception as e:
        print(f"   FAIL: {e}")
        import traceback
        traceback.print_exc()

def test_gemini():
    print("2. Gemini (Executor/Monitor) 테스트...")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"), temperature=0.1)
        r = llm.invoke([HumanMessage(content="1+1은? 숫자만")])
        print(f"   OK: {r.content[:50]}...")
    except Exception as e:
        print(f"   FAIL: {e}")
        import traceback
        traceback.print_exc()

def test_chromadb():
    print("3. ChromaDB (RAG) 테스트...")
    try:
        from agent_bot import ChromaRAGTool
        rag = ChromaRAGTool()
        r = rag.search("test")
        print(f"   OK: {r[:80]}...")
    except Exception as e:
        print(f"   FAIL: {e}")
        import traceback
        traceback.print_exc()

def test_e2b():
    print("4. E2B Sandbox 테스트...")
    try:
        from agent_bot import _run_code_sandbox

        r = _run_code_sandbox("print(1+1)")
        snippet = (r or "")[:200]
        if (r or "").strip().startswith("실행 오류"):
            print(f"   FAIL: 샌드박스가 오류 문자열을 반환했습니다.\n      → {snippet}")
            if "unicodeescape" in (r or "").lower():
                print(
                    "      힌트: .env 등 환경 변수 값에 `\\` 가 있으면 E2B에 넘길 때 "
                    "파이썬 소스 해석 오류로 이어질 수 있습니다. 경로는 / 또는 raw 문자열을 검토하세요."
                )
            return
        if "2" not in (r or "").replace(" ", ""):
            print(f"   WARN: 성공으로 보이나 출력에 '2'가 없습니다. 원문: {snippet!r}")
        else:
            print(f"   OK: {snippet[:80]}{'...' if len(snippet) > 80 else ''}")
    except Exception as e:
        print(f"   FAIL: {e}")
        import traceback
        traceback.print_exc()


def test_full_graph_smoke():
    """direct_answer 경로 스모크 (`1+1` 산수 패턴 → 일상 하드룰)."""
    print("5a. LangGraph 스모크 (direct_answer·체크포인트)...")
    try:
        from agent_bot import build_graph
        import sqlite3
        from langgraph.checkpoint.sqlite import SqliteSaver

        conn = sqlite3.connect("./agent_checkpoints.db", check_same_thread=False)
        graph = build_graph(checkpointer=SqliteSaver(conn))
        cfg = {"configurable": {"thread_id": "test_flow_smoke", "chat_id": "8587793069", "bot": None}}
        _run_graph_stream(graph, _base_graph_state("print(1+1) 실행해줘"), cfg)
        state = graph.get_state(cfg)
        vals = state.values or {}
        print(f"   route_type={vals.get('route_type')!r}, next={state.next!r}")
        print(f"   keys: {list(vals.keys())}")
        if state.next:
            print("   (interrupt 대기 중)")
        if vals.get("route_type") != "direct_answer":
            print(f"   WARN: 스모크는 보통 direct_answer 예상 (산수 패턴). 실제={vals.get('route_type')!r}")
        print("   OK")
    except Exception as e:
        print(f"   FAIL: {e}")
        import traceback
        traceback.print_exc()


def test_full_graph_code_run():
    """`\\d+ \\+ \\d+` 형태가 없어 산수 하드룰을 피하고 code_run으로 가는지 확인."""
    print("5b. LangGraph code_run → executor 경로...")
    try:
        from agent_bot import build_graph
        import sqlite3
        from langgraph.checkpoint.sqlite import SqliteSaver

        # '+' 산수 패턴 없음 → is_smalltalk 산수 룰 미적용, '실행해' → tier run → code_run
        msg = "파이썬으로 len('hello')를 print하는 한 줄만 실행해 줘"
        conn = sqlite3.connect("./agent_checkpoints.db", check_same_thread=False)
        graph = build_graph(checkpointer=SqliteSaver(conn))
        cfg = {"configurable": {"thread_id": "test_flow_coderun", "chat_id": "8587793069", "bot": None}}
        _run_graph_stream(graph, _base_graph_state(msg), cfg)
        state = graph.get_state(cfg)
        vals = state.values or {}
        rt = vals.get("route_type")
        er = (vals.get("execution_result") or "")[:120]
        print(f"   route_type={rt!r}, next={state.next!r}")
        print(f"   execution_result(앞 120자): {er!r}...")
        if rt != "code_run":
            print(f"   FAIL: code_run 기대, 실제={rt!r}")
            return
        if state.next:
            print("   WARN: code_run은 보통 끝까지 진행. interrupt(next)가 비어 있지 않음.")
        res = vals.get("execution_result") or ""
        if res.strip().startswith("실행 오류"):
            print(f"   WARN: executor는 돌았으나 E2B/실행 오류. (4번 E2B와 동일 원인 가능)\n      → {res[:150]}...")
        else:
            print("   OK")
    except Exception as e:
        print(f"   FAIL: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    from langchain_core.messages import HumanMessage
    test_ollama()
    test_gemini()
    test_chromadb()
    test_e2b()
    test_full_graph_smoke()
    test_full_graph_code_run()
    print("\n테스트 완료")
