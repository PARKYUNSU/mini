#!/usr/bin/env python3
"""
Phase 4 — 3단계: E2B 샌드박스 코딩 공장.

Boardroom 회의록(``archives/boardroom/`` 최신 .md)을 읽고, Claude + ``execute_python_in_sandbox`` 도구로
코드를 짜서 샌드박스에서 검증한 뒤 최종 마크다운을 출력하는 독립 스크립트.
에이전트는 **LangGraph** ``create_react_agent`` (``langgraph.prebuilt.chat_agent_executor``) +
``recursion_limit``(기본 32) (요금/루프 상한) + ``stream`` 으로 도구/모델 출력을 터미널에 중계한다.

실행 (``mini`` 루트):

  python -m apps.engineering.sandbox_coder
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()
load_dotenv(_ROOT / ".env", override=True)

# --- 아래 import는 _ROOT 가 sys.path 에 있을 때만 의미가 있으므로 noqa 로 묶는다. ---

logger = logging.getLogger("sandbox_coder")

# Anthropic 본사 API 공식 모델 ID (2026) — 키/리전에 아직 없으면 404 → ``_MODEL_FALLBACKS`` 로만 재시도
_SANDBOX_CODER_MODEL = "claude-sonnet-4-6-20260217"
# ``SANDBOX_CODER_CLAUDE_MODEL`` 미설정 시, 위 ID 다음 순서로 시도 (404/not_found일 때만)
_MODEL_FALLBACKS: tuple[str, ...] = (
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-20250514",
    "claude-3-5-sonnet-20241022",
)


def _is_anthropic_model_not_found(exc: BaseException) -> bool:
    """모델 ID 미지원(404)일 때만 True — 다른 오류는 재시도로 삼지 않는다."""
    sc = getattr(exc, "status_code", None)
    if sc == 404:
        return True
    resp = getattr(exc, "response", None)
    if resp is not None and getattr(resp, "status_code", None) == 404:
        return True
    try:
        from anthropic import NotFoundError as _NFE  # noqa: E402
    except ImportError:
        pass
    else:
        if isinstance(exc, _NFE):
            return True
    msg = str(exc).lower()
    if "not_found" in msg or "404" in msg and "model" in msg:
        return True
    return False


def _sandbox_model_try_order() -> list[str]:
    """
    시도 순서: ``.env`` 의 ``SANDBOX_CODER_CLAUDE_MODEL``(있으면),
    이후 ``_SANDBOX_CODER_MODEL``, ``_MODEL_FALLBACKS`` (중복 제거).
    """
    out: list[str] = []
    for m in (
        (os.getenv("SANDBOX_CODER_CLAUDE_MODEL") or "").strip(),
        _SANDBOX_CODER_MODEL,
        *_MODEL_FALLBACKS,
    ):
        if m and m not in out:
            out.append(m)
    return out


_SYSTEM_ROLE = (
    "당신은 Homunculus Syndicate의 수석 파이썬 개발자입니다. "
    "제공된 회의록의 [제안된 해결책]을 바탕으로 작동 가능한 완벽한 파이썬 코드를 작성하십시오. "
    "코드를 작성한 후에는 반드시 `execute_python_in_sandbox` 도구를 호출하여 코드를 실행해 보십시오. "
    "만약 에러(stderr)가 발생하면, 에러 로그를 분석하고 스스로 코드를 수정하여 다시 도구를 호출하십시오. "
    "에러 없이 완벽하게 실행되면, 최종 완성된 코드를 마크다운으로 출력하십시오. "
    "⚠️ Anthropic tool_use 필수 형식: 도구 이름 `execute_python_in_sandbox` 의 **input 객체는 키가 `code` 하나뿐**이어야 "
    "합니다. 예: `{{\"code\": \"print(1+1)\\\\n\"}}` 처럼 **문자열 값**으로 전체 파이썬 소스를 넣으십시오. "
    "빈 `{{}}` 나 `code` 없이 호출하면 안 됩니다. "
    "⚠️ 코드만 본문(content) 텍스트로 답하지 말고, 반드시 위 도구를 호출해 샌드박스에서 실행하십시오."
)


def _latest_boardroom_markdown() -> str:
    """``archives/boardroom`` 에서 가장 최근 수정(mtime)된 ``*.md`` 전체를 읽는다."""
    d = _ROOT / "archives" / "boardroom"
    if not d.is_dir():
        msg = f"회의록 폴더가 없습니다: {d}"
        raise FileNotFoundError(msg)
    mds = [p for p in d.iterdir() if p.is_file() and p.suffix.lower() == ".md"]
    if not mds:
        msg = f"회의록 .md 파일이 없습니다: {d}"
        raise FileNotFoundError(msg)
    latest = max(mds, key=lambda p: p.stat().st_mtime)
    text = latest.read_text(encoding="utf-8", errors="replace")
    return f"---\n(파일: {latest.name}, 경로: {latest})\n---\n\n{text}"


def _anthropic_api_key() -> str:
    for name in (
        "ANTHROPIC_API_KEY",
        "CLAUDE_API_KEY",
        "ANTHROPIC_KEY",
    ):
        v = (os.getenv(name) or "").strip()
        if v:
            return v
    return ""


def _print_react_stream_updates(data: object) -> None:
    """``stream_mode=updates`` 청크: 에이전트/도구 노드의 메시지(도구 인자·샌드박스 결과)를 터미널에 출력."""
    from langchain_core.messages import AIMessage, ToolMessage  # noqa: E402

    if not isinstance(data, dict):
        print(f"[updates] {data!r}\n", flush=True)
        return
    for node, payload in data.items():
        print(f"\n─── [노드: {node}] ───", flush=True)
        if not isinstance(payload, dict):
            print(payload, flush=True)
            continue
        raw = payload.get("messages")
        if raw is None:
            continue
        seq = raw if isinstance(raw, list) else [raw]
        for m in seq:
            if isinstance(m, AIMessage):
                tcalls = getattr(m, "tool_calls", None) or []
                if tcalls:
                    for tc in tcalls:
                        if isinstance(tc, dict):
                            name = tc.get("name", "?")
                            args = tc.get("args") or {}
                        else:
                            name = getattr(tc, "name", None) or "?"
                            args = getattr(tc, "args", None) or {}
                        if isinstance(args, str):
                            try:
                                import json as _json

                                args = _json.loads(args) if args.strip().startswith("{") else {}
                            except Exception:  # noqa: BLE001
                                args = {}
                        py = None
                        if isinstance(args, dict):
                            py = args.get("code") or args.get("python_code") or args.get("input")
                        if name == "execute_python_in_sandbox":
                            if py:
                                print("🔧 [execute_python_in_sandbox] code:\n", flush=True)
                                print(str(py)[:16000] + ("…" if len(str(py)) > 16000 else ""), flush=True)
                            else:
                                print(
                                    "⚠️ [execute_python_in_sandbox] tool_use input 누락 (args="
                                    f"{args!r}) — `code` 키가 비어 있습니다.\n",
                                    flush=True,
                                )
                        else:
                            print(f"🔧 [도구] {name} args={args!r}", flush=True)
                c = m.content
                if c and not tcalls:
                    text = c if isinstance(c, str) else str(c)
                    cap = 6000
                    if len(text) > cap:
                        text = text[:cap] + "\n…(텍스트 잘림)…"
                    print(f"💬 [모델 응답]\n{text}\n", flush=True)
            elif isinstance(m, ToolMessage):
                body = m.content
                if not isinstance(body, str):
                    body = str(body)
                cap = 16000
                if len(body) > cap:
                    body = body[:cap] + "\n…(이하 잘림)…"
                print("📤 [도구 결과 — 샌드박스 stdout/stderr/에러]\n" + body + "\n", flush=True)


def _stream_react_agent(
    graph: object,
    user_block: str,
    *,
    recursion_limit: int,
) -> object:
    """``graph.stream`` 으로 실행; 마지막 ``values`` 상태를 돌려 최종 응답 추출에 쓴다."""
    from langchain_core.messages import HumanMessage  # noqa: E402
    from langgraph.errors import GraphRecursionError  # noqa: E402

    last_values: dict | None = None
    inp = {"messages": [HumanMessage(content=user_block)]}
    cfg = {"recursion_limit": recursion_limit}
    print(
        "\n" + "▼" * 28 + " 실시간 스트림 (updates / values) " + "▼" * 10 + "\n",
        flush=True,
    )
    try:
        for event in graph.stream(
            inp,
            config=cfg,
            stream_mode=["updates", "values"],
        ):
            if isinstance(event, tuple) and len(event) == 2:
                mode, payload = event
                if mode == "updates":
                    _print_react_stream_updates(payload)
                elif mode == "values" and isinstance(payload, dict):
                    last_values = payload
            elif isinstance(event, dict):
                _print_react_stream_updates(event)
    except GraphRecursionError as exc:
        logger.warning(
            "recursion_limit=%s 에 도달했습니다(도구/모델 루프). 마지막 state로 종료 시도. (%s)",
            recursion_limit,
            exc,
        )
        if last_values is not None:
            return last_values
        raise
    if last_values is not None:
        return last_values
    return graph.invoke(inp, config=cfg)


def _last_ai_text_from_react_state(result: object) -> str:
    """``create_react_agent`` ``invoke`` 결과 state에서 마지막 ``AIMessage`` 본문을 꺼낸다."""
    from langchain_core.messages import AIMessage  # noqa: E402

    state = result if isinstance(result, dict) else {}
    msgs: list = list(state.get("messages") or [])
    for m in reversed(msgs):
        if isinstance(m, AIMessage):
            raw = m.content
            if isinstance(raw, str):
                return raw.strip()
            if isinstance(raw, list):
                parts: list[str] = []
                for block in raw:
                    if isinstance(block, str):
                        parts.append(block)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        parts.append(str(block.get("text", "")))
                return "\n".join(parts).strip()
            return str(raw).strip()
    return ""


def _run() -> int:
    from langchain_anthropic import ChatAnthropic  # noqa: E402
    # `langgraph.prebuilt` re-export 는 V1에서 Deprecation 경고를 띄울 수 있어 구현부에서 직접 임포트
    from langgraph.prebuilt.chat_agent_executor import create_react_agent  # noqa: E402

    from tools.runtime.agent_tools.agent_tools.e2b_executor import (  # noqa: E402
        execute_python_in_sandbox,
    )

    tools = [execute_python_in_sandbox]
    api_key = _anthropic_api_key()
    if not api_key:
        logger.error("ANTHROPIC_API_KEY(또는 CLAUDE_API_KEY)가 .env에 없습니다.")
        return 1

    meeting_body = _latest_boardroom_markdown()
    logger.info("최신 회의록을 로드했습니다. (길이: %d 글자)", len(meeting_body))

    user_block = (
        "아래는 The Boardroom에서 저장된 **가장 최신** 회의록 전문입니다. "
        "[제안된 해결책] 섹션(및 맥락)을 반드시 반영하십시오.\n\n"
        f"{meeting_body}"
    )
    # 요금·무한 루프 방지: super-step 상한(빈 tool 인자 반복 + 실제 E2B 실행을 함께 감당)
    _RECURSION_CAP = 32

    models = _sandbox_model_try_order()
    last_err: BaseException | None = None
    for idx, model_name in enumerate(models):
        try:
            logger.info(
                "ChatAnthropic 모델(시도 %d/%d): %s",
                idx + 1,
                len(models),
                model_name,
            )
            llm = ChatAnthropic(
                model=model_name,
                api_key=api_key,
                temperature=0.2,
                max_tokens=4096,
            )
            # Anthropic: strict tool use → input 스키마 준수(빈 ``{}`` 완화). parallel_tool_calls 끄면 인자 1개 도구에 유리
            llm = llm.bind_tools(
                tools,
                strict=True,
                parallel_tool_calls=False,
            )
            graph = create_react_agent(
                llm,
                tools,
                prompt=_SYSTEM_ROLE,
            )
            result = _stream_react_agent(
                graph,
                user_block,
                recursion_limit=_RECURSION_CAP,
            )
            out = _last_ai_text_from_react_state(result) or str(result)
            print("\n" + "=" * 72)
            print("### 최종 응답 (LangGraph create_react_agent)")
            print("=" * 72 + "\n")
            print(out)
            return 0
        except Exception as e:  # noqa: BLE001
            last_err = e
            if _is_anthropic_model_not_found(e) and idx + 1 < len(models):
                nxt = models[idx + 1]
                logger.warning(
                    "모델 `%s` 404/미지원 — 다음 ID로 재시도: `%s` (원하면 .env에 "
                    "SANDBOX_CODER_CLAUDE_MODEL=... 로 고정)",
                    model_name,
                    nxt,
                )
                continue
            raise
    if last_err is not None:
        raise last_err
    return 1


def main() -> int:
    """에이전트 1회 실행. 실패 시 로깅 후 비영 반환."""
    return _run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    try:
        code = main()
    except Exception:  # noqa: BLE001 — 단독 스크립트: 모든 예외를 기록
        logger.exception("sandbox_coder: 예기치 못한 오류로 종료합니다.")
        raise SystemExit(1) from None
    raise SystemExit(code)
