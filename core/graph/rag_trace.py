"""요청별 RAG 단계 기록 — 단계마다 걸린 시간과 중간 결과를 JSONL 한 줄로 남긴다 (docs/experiments/foundation_1031 §1).

왜: 실사용 답이 틀려도 어느 단계에서 틀렸는지 못 봤고(answer_review_1030 §2-3 — 다시 쓰기 전 결론이 로그에 없음),
어느 단계가 느린지도 몰랐다. 워커가 ``start`` → 노드가 ``mark`` → 워커가 ``finish`` (chat_id 로 묶음).

- ``RAG_TRACE=0`` 이면 끈다(기본 켬). 기록 위치 ``RAG_TRACE_LOG`` (기본 ``.bridge/rag_trace.jsonl``, git 밖).
- 기록이 실패해도 답변은 낸다 — 모든 함수가 예외를 삼킨다.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

from core.config.agent_config import PROJECT_ROOT

_TRACES: dict[str, dict] = {}
_PID_HEAD = re.compile(r"(?m)^\[(\d{4}\.\d{4,5})(?:v\d+)?\]")


def enabled() -> bool:
    return os.getenv("RAG_TRACE", "1").strip() != "0"


def log_path() -> Path:
    return Path(os.getenv("RAG_TRACE_LOG") or PROJECT_ROOT / ".bridge" / "rag_trace.jsonl")


def paper_ids(ctx: str) -> list[str]:
    """컨텍스트 블록 머리줄의 논문 ID(버전 뺌), 처음 나온 순서."""
    return list(dict.fromkeys(_PID_HEAD.findall(ctx or "")))


def start(key: str, **info) -> None:
    if not enabled():
        return
    now = time.perf_counter()
    _TRACES[str(key)] = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), **info, "stages": [], "_t0": now, "_t": now}


def mark(key: str, stage: str, **data) -> None:
    """직전 mark(또는 start) 뒤 걸린 초와 함께 단계를 붙인다. start 없으면 아무것도 안 한다."""
    try:
        t = _TRACES.get(str(key))
        if t is None:
            return
        now = time.perf_counter()
        t["stages"].append({"stage": stage, "s": round(now - t["_t"], 2), **data})
        t["_t"] = now
    except Exception:
        pass


def finish(key: str, *, write: bool = True) -> dict:
    """기록을 닫고 돌려준다. 단계가 하나도 없으면(RAG 경로 아님) 쓰지 않는다."""
    t = _TRACES.pop(str(key), None)
    if t is None:
        return {}
    t["total_s"] = round(time.perf_counter() - t.pop("_t0"), 2)
    t.pop("_t", None)
    if write and t["stages"]:
        try:
            p = log_path()
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open("a", encoding="utf-8") as f:
                f.write(json.dumps(t, ensure_ascii=False, default=str) + "\n")
        except Exception as exc:
            print(f"[WARN] rag_trace 기록 실패: {type(exc).__name__}: {exc}")
    return t
