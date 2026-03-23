#!/usr/bin/env python3
"""Agent 플로우 단계별 테스트 - 오류 원인 파악용"""
import os
os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

from dotenv import load_dotenv
load_dotenv()

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
        print(f"   OK: {r[:80]}")
    except Exception as e:
        print(f"   FAIL: {e}")
        import traceback
        traceback.print_exc()

def test_full_graph():
    print("5. LangGraph 전체 플로우 테스트...")
    try:
        from agent_bot import build_graph
        import sqlite3

        # LangGraph 체크포인트는 워커 스레드에서 접근함 — check_same_thread=False 필수
        conn = sqlite3.connect("./agent_checkpoints.db", check_same_thread=False)
        from langgraph.checkpoint.sqlite import SqliteSaver
        graph = build_graph(checkpointer=SqliteSaver(conn))
        cfg = {"configurable": {"thread_id": "test_flow", "chat_id": "8587793069", "bot": None}}
        for event in graph.stream({"user_request": "print(1+1) 실행해줘", "plan": [], "approval_status": "pending", "generated_code": "", "execution_result": "", "retry_count": 0}, cfg):
            pass
        state = graph.get_state(cfg)
        print(f"   next: {state.next}, values keys: {list(state.values.keys()) if state.values else []}")
        if state.next:
            print("   (interrupt 대기 중 - 정상)")
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
    test_full_graph()
    print("\n테스트 완료")
