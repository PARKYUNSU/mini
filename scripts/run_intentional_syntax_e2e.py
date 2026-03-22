#!/usr/bin/env python3
"""
동일 사용자 문장으로 LangGraph를 텔레그램 없이 돌림.

  기본: interrupt → '승인' → executor/monitor 까지 + 단계별 소요 시간(초)
  --reject: interrupt → '거절' 까지만 (Gemini/E2B 불필요)

로컬: Ollama(플래너), 승인 플로우 시 GEMINI_API_KEY + E2B_API_KEY.
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from agent_telegram import strip_wake_word
from agent_bot import build_graph

USER_RAW = (
    "윤수르, 파이썬으로 1부터 10까지 더하는 코드를 짜는데, "
    "일부러 오타(SyntaxError)를 하나 넣어서 실행해 봐"
)


def _run_timed_stream(graph, payload, cfg, label: str) -> dict[str, float]:
    """스트림 한 번 돌리며 노드별 구간 시간(초) 기록."""
    print(f"\n── {label} ──")
    t_prev = time.perf_counter()
    segment: dict[str, float] = {}
    for event in graph.stream(payload, cfg, stream_mode="updates"):
        now = time.perf_counter()
        for node, patch in event.items():
            dt = now - t_prev
            segment[node] = segment.get(node, 0.0) + dt
            keys = list(patch.keys()) if isinstance(patch, dict) else type(patch)
            print(f"   [{node}] +{dt:.2f}s (누적 {segment[node]:.2f}s) keys={keys}")
            t_prev = now
    return segment


def run_reject_flow() -> int:
    text = strip_wake_word(USER_RAW)
    print("=== 거절 플로우만 (승인 단계에서 '거절') ===")
    print("요청:", text[:90], "…" if len(text) > 90 else "")

    fd, db_path = tempfile.mkstemp(suffix="_e2e_reject.db")
    os.close(fd)
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        tid = f"e2e_reject_{int(time.time())}"
        cfg = {"configurable": {"thread_id": tid, "chat_id": "e2e_test", "bot": None}}
        graph = build_graph(checkpointer=SqliteSaver(conn))

        init_state = {
            "user_request": text,
            "route_type": "",
            "direct_response": "",
            "plan": [],
            "approval_status": "pending",
            "generated_code": "",
            "execution_result": "",
            "retry_count": 0,
            "error_hint": "",
        }

        t0 = time.perf_counter()
        _run_timed_stream(graph, init_state, cfg, "초기 실행 → 플래너 interrupt 전")
        st = graph.get_state(cfg)
        if not st.next:
            print("FAIL: interrupt 대기 상태가 아님")
            return 3

        _run_timed_stream(graph, Command(resume="거절"), cfg, "resume=거절")
        st = graph.get_state(cfg)
        vals = st.values or {}
        elapsed = time.perf_counter() - t0

        print(f"\n=== 거절 플로우 완료 (총 {elapsed:.1f}s) ===")
        print("approval_status:", vals.get("approval_status"))
        if vals.get("approval_status") == "rejected":
            print("✅ 거절 처리 정상 (executor 미실행)")
            return 0
        print("❌ 기대: approval_status=rejected")
        return 4
    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass


def run_approve_flow() -> int:
    text = strip_wake_word(USER_RAW)
    print("=== 승인 플로우 (승인 → 실행 → SyntaxError 유지) ===")
    print("요청:", text[:90], "…" if len(text) > 90 else "")

    if not os.getenv("GEMINI_API_KEY"):
        print("SKIP/FAIL: GEMINI_API_KEY 없음 (.env)")
        return 2
    if not os.getenv("E2B_API_KEY"):
        print("SKIP/FAIL: E2B_API_KEY 없음")
        return 2

    fd, db_path = tempfile.mkstemp(suffix="_e2e_agent.db")
    os.close(fd)
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        tid = f"e2e_syntax_{int(time.time())}"
        cfg = {"configurable": {"thread_id": tid, "chat_id": "e2e_test", "bot": None}}
        graph = build_graph(checkpointer=SqliteSaver(conn))

        init_state = {
            "user_request": text,
            "route_type": "",
            "direct_response": "",
            "plan": [],
            "approval_status": "pending",
            "generated_code": "",
            "execution_result": "",
            "retry_count": 0,
            "error_hint": "",
        }

        t0 = time.perf_counter()
        seg1 = _run_timed_stream(graph, init_state, cfg, "① 라우터~플래너 (승인 전, interrupt)")
        st = graph.get_state(cfg)
        print(f"   → next: {st.next}")

        if not st.next:
            print("FAIL: interrupt 없음")
            return 3

        t_approve = time.perf_counter()
        seg2 = _run_timed_stream(graph, Command(resume="승인"), cfg, "② resume=승인 이후 (플래너 마무리~monitor)")
        t_after_approve = time.perf_counter()
        approve_to_end = t_after_approve - t_approve

        st = graph.get_state(cfg)
        if st.next:
            print(f"FAIL: 아직 next={st.next}")
            return 3

        vals = st.values or {}
        total = time.perf_counter() - t0

        print("\n" + "=" * 60)
        print("타임 요약")
        print("=" * 60)
        print(f"  ① 승인 전(메시지 수신 ~ 계획·interrupt): {sum(seg1.values()):.1f}s")
        print("      (참고: LangGraph는 interrupt 직전까지 노드 완료 이벤트가 거의 없어")
        print("       대기 시간이 __interrupt__ 한 줄에 몰려 보일 수 있음 ≈ RAG+Ollama 플래너)")
        if seg1:
            for k, v in sorted(seg1.items(), key=lambda x: -x[1]):
                print(f"      - {k}: {v:.1f}s")
        print(f"  ② 승인 직후 ~ 최종 응답 완료:           {approve_to_end:.1f}s")
        if seg2:
            for k, v in sorted(seg2.items(), key=lambda x: -x[1]):
                print(f"      - {k}: {v:.1f}s")
        print(f"  합계(세션 전체):                        {total:.1f}s")
        print("=" * 60)

        print("\napproval_status:", vals.get("approval_status"))
        er = vals.get("execution_result") or ""
        print("execution_result (앞 800자):\n", er[:800])

        if "planner_debate" in seg2:
            print("\n⚠️ planner_debate 가 실행됨 — 의도적 오류 요청이면 생략되어야 함")
        else:
            print("\n✅ planner_debate 생략됨 (의도적 SyntaxError 경로)")

        if "SyntaxError" in er or "syntax" in er.lower():
            print("✅ SyntaxError 포함 (의도적 오류 시나리오)")
        elif er.startswith("실행 오류"):
            print("⚠️ 실행 오류이나 SyntaxError 문자열 없음")
        return 0
    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--reject", action="store_true", help="거절만 검증 (Gemini/E2B 없이 가능)")
    p.add_argument("--approve-only", action="store_true", help="승인 플로우만 (기본과 동일)")
    args = p.parse_args()
    if args.reject:
        return run_reject_flow()
    return run_approve_flow()


if __name__ == "__main__":
    raise SystemExit(main())
