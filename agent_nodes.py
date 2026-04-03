"""LangGraph 노드·조건부 엣지 (Router → Direct / Tool / Planner / Executor / Monitor)."""

from __future__ import annotations

import contextlib
import logging
import os
import re
import traceback
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from pathlib import Path
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt

from agent_chroma_rag import get_chroma_rag_tool
from agent_config import (
    AGENT_TOOLS_DIR,
    CODE_TIMEOUT_SEC,
    DIRECT_ANSWER_TIMEOUT_SEC,
    ERROR_LOG_MAX_CHARS,
    RAG_TOP_K,
    TOOL_RAG_TOP_K,
    resolve_agent_tool_py,
)
from agent_llm import (
    get_coding_groq_llm,
    get_executor_llm,
    get_planner_llm,
    get_planner_plan_llm,
    get_router_llm,
)
from agent_prompts import (
    DIRECT_ANSWER_DAILY_CHAT_SYSTEM,
    DIRECT_ANSWER_PYTHON_EXAMPLE_SYSTEM,
    DIRECT_ANSWER_RAG_DEPTH_SUFFIX,
    DIRECT_ANSWER_RAG_SYSTEM_BASE,
    EXECUTOR_INTENTIONAL_SYNTAX_BLOCK,
    EXECUTOR_SYSTEM_CODE_RUN,
    EXECUTOR_SYSTEM_FULL,
    EXECUTOR_USER_FOOTER_CODE_RUN,
    EXECUTOR_USER_FOOTER_FULL,
    PLANNER_DEBATE_CRITIC_SYSTEM,
    PLANNER_DEBATE_REVISE_SYSTEM,
    PLANNER_LEARNINGS_BLOCK,
    PLANNER_SYSTEM_BASE,
    PLANNER_URL_SUFFIX,
    direct_answer_daily_user,
    direct_answer_python_example_user,
    direct_answer_rag_user,
    executor_error_append,
    executor_rag_append,
    executor_tools_append,
    executor_user_prompt_code_run,
    executor_user_prompt_full,
    monitor_content_irrelevant_retry_human,
    monitor_error_analysis_human,
    monitor_irrelevance_check_human,
    planner_debate_critic_user,
    planner_debate_revise_user,
    planner_user_prompt,
    router_step3_system_prompt,
    router_step3_user_prompt,
    tavily_summarize_human,
    use_existing_tool_prompt_form_fill,
    use_existing_tool_prompt_generic,
)
from agent_router_rules import (
    is_explicit_python_coding_request,
    is_factual_lookup,
    router_step2_build_features as _router_step2_build_features,
    skip_planner_debate_for_fast_path as _skip_planner_debate_for_fast_path,
    user_wants_intentional_exec_error as _user_wants_intentional_exec_error,
)
from agent_sandbox import run_code_sandbox as _run_code_sandbox
from agent_session import (
    AgentSkillLibrary,
    _plan_cache,
    extract_chat_id_from_thread,
    get_paper_mode,
    get_search_intent_local,
    get_session,
    is_rag_allowed,
    load_learnings,
    remember_tool,
    router_step1_hard_rules,
    with_chat_lock,
)
from agent_tool_rag import get_tool_rag_store
from agent_types import AgentState
from agent_telegram import (
    notify_chat_error as _notify_chat_error,
    rag_structured_lines_to_html as _rag_structured_lines_to_html,
    safe_telegram_send as _safe_telegram_send,
    strip_thinking_tags as _strip_thinking_tags,
)
from agent_vision import build_message_content as _build_message_content

_MINI_ROOT = Path(__file__).resolve().parent

_log = logging.getLogger(__name__)

# RAG 직접 답변: user 말미 단일 지시 (7B 모델용 최소 문구)
RAG_DIRECT_ANSWER_USER_SUFFIX = (
    "\n\n[지시사항: 주어진 문서 1개만 사용하여 아래 3가지 항목으로만 깔끔하게 요약할 것. "
    "(1. 핵심 주제, 2. 주요 방법론, 3. 결론 및 의의)]"
)

_RAG_HIT_SEP = "\n\n---\n\n"


def _prefer_single_hit_rag_context(user_request: str, *, wants_depth: bool) -> bool:
    """단일 문서 요약 의도일 때 Chroma 컨텍스트를 Top-1로 제한 (논문 짬뽕 완화)."""
    if wants_depth:
        return False
    u = (user_request or "").strip()
    vague_markers = (
        "아무거나",
        "하나만",
        "한 편만",
        "한편만",
        "랜덤",
        "상관없",
        "아무 논문",
        "아무것이나",
        "뭐든",
        "아무나",
        "아무거나 하나",
        "하나 요약",
        "한 개만",
        "한개만",
        "편 하나",
    )
    if any(k in u for k in vague_markers):
        return True
    if any(x in u for x in ("비교", "차이", "여러", "두 편", "두편", "세 편", "목록")):
        return False
    if len(u) <= 44 and ("요약" in u or "알려줘" in u or "설명해" in u):
        return True
    return False


def _rag_context_first_hit_only(rag_context: str, *, max_chars: int = 5500) -> str:
    """Chroma `_format_chroma_hits` 구분선 기준 가장 상위(관련도 1위) 블록만 잘라 LLM에 전달."""
    s = (rag_context or "").strip()
    if not s or s == "관련 문서 없음":
        return rag_context
    if _RAG_HIT_SEP not in s:
        return s[:max_chars] + ("...(이하 잘림)" if len(s) > max_chars else "")
    first = s.split(_RAG_HIT_SEP, 1)[0].strip()
    if len(first) > max_chars:
        first = first[:max_chars].rstrip() + "\n\n...(이하 잘림)"
    return first


def _da_trace(step: str, detail: str = "") -> None:
    """DirectAnswer 세그폴트 위치 추적: logger.debug + print(bot.log에 항상 남김)."""
    line = f"DirectAnswer TRACE | {step}"
    if detail:
        line = f"{line} | {detail}"
    _log.debug("%s", line)
    print(f"[DEBUG] {line}", flush=True)


def _llm_invoke_trace(step: str, detail: str = "") -> None:
    line = f"invoke_llm_fallback TRACE | {step}"
    if detail:
        line = f"{line} | {detail}"
    _log.debug("%s", line)
    print(f"[DEBUG] {line}", flush=True)


def _llm_model_label(llm) -> str:
    return str(getattr(llm, "model", None) or getattr(llm, "model_name", None) or type(llm).__name__)


def _paper_knowledge_heuristic(user_request: str, req_lower: str) -> bool:
    """논문 모드에서 일상(A)으로 오분류되기 쉬운 지식·설명형 질문."""
    r = user_request or ""
    markers = (
        "요약",
        "설명",
        "정리",
        "비교",
        "차이",
        "정의",
        "무엇",
        "뭐야",
        "란 ",
        "이란",
        "what is",
        "how does",
    )
    if any(m in r for m in markers):
        code_hits = ("파이썬", "python", "코드", "실행", "크롤", "스크립트", "api 호출")
        if not any(c in req_lower for c in code_hits):
            return True
    return False


def _apply_paper_mode_router_bias(chat_id: str, user_request: str, result: dict) -> dict:
    """
    /paper ON: 라우터를 대체하지 않고 RAG(B)·문서(D) 선호 bias.
    명백한 코드/실행 요청은 C(planner) 허용.
    """
    if not get_paper_mode(chat_id):
        return result
    req_lower = (user_request or "").lower().strip()
    if is_explicit_python_coding_request(user_request, req_lower):
        if result.get("route_type") == "direct_answer" and result.get("router_choice") == "A":
            return {"route_type": "planner", "router_choice": "C"}
        return result
    if result.get("route_type") == "direct_answer" and result.get("router_choice") == "A":
        if is_factual_lookup(user_request) or _paper_knowledge_heuristic(user_request, req_lower):
            return {"route_type": "direct_answer", "router_choice": "B"}
    return result


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = (item or "").strip()
        if not key:
            continue
        norm = re.sub(r"\s+", " ", key).lower()
        if norm in seen:
            continue
        seen.add(norm)
        out.append(key)
    return out


def _extract_bullets(text: str) -> list[str]:
    lines = []
    for raw in (text or "").splitlines():
        s = raw.strip()
        if not s:
            continue
        s = re.sub(r"^[-*]\s*", "", s)
        s = re.sub(r"^\d+[.)]\s*", "", s)
        if len(s) >= 6:
            lines.append(s)
    return _dedupe_preserve_order(lines)


def _enforce_rag_structure_markdown(answer: str) -> str:
    """
    RAG 답변의 최소 구조를 강제.
    - 3개 섹션(핵심 주제/주요 방법론/결론 및 의의) 보장
    - 중복 문장 억제
    """
    text = (answer or "").strip()
    if not text:
        return (
            "1. 핵심 주제\n- 문서에서 핵심 주제를 확인할 수 없습니다.\n\n"
            "2. 주요 방법론\n- 문서에서 방법론을 확인할 수 없습니다.\n\n"
            "3. 결론 및 의의\n- 문서에서 결론/의의를 확인할 수 없습니다."
        )

    bullets = _extract_bullets(text)
    if not bullets:
        # bullet이 전혀 없는 장문이면 문장 단위로 분해
        parts = re.split(r"(?<=[.!?다요])\s+", re.sub(r"\s+", " ", text))
        bullets = _dedupe_preserve_order([p.strip() for p in parts if len(p.strip()) >= 8])
    if not bullets:
        bullets = [text[:180]]

    b = _dedupe_preserve_order(bullets)
    topic: list[str] = []
    method: list[str] = []
    concl: list[str] = []
    i = 0
    while i < len(b) and len(topic) < 2:
        topic.append(b[i])
        i += 1
    while i < len(b) and len(method) < 2:
        method.append(b[i])
        i += 1
    while i < len(b) and len(concl) < 2:
        concl.append(b[i])
        i += 1

    topic = topic or ["핵심 내용을 추출하지 못했습니다."]
    method = method or ["문서에서 방법론을 추가로 확인할 수 없습니다."]
    concl = concl or ["문서에서 결론·의의를 추가로 확인할 수 없습니다."]

    return (
        "1. 핵심 주제\n"
        + "\n".join(f"- {x}" for x in topic)
        + "\n\n2. 주요 방법론\n"
        + "\n".join(f"- {x}" for x in method)
        + "\n\n3. 결론 및 의의\n"
        + "\n".join(f"- {x}" for x in concl)
    )


def _markdown_struct_to_plain(md: str) -> str:
    """Markdown/HTML 실패 시 폴백: 줄바꿈·섹션 구분 유지."""
    plain = (md or "").replace("### ", "").replace("**", "")
    plain = re.sub(r"^\s*-\s*", "• ", plain, flags=re.M)
    # 연속 빈 줄 정리(과도한 공백만), 단일 \n은 유지
    plain = re.sub(r"\n{3,}", "\n\n", plain)
    return plain.strip()


def _is_execution_failure(result: str) -> bool:
    """
    실행 결과가 실패인지 판정. 문자열 부분 매칭 대신 명시적 실패 지표만 사용.
    """
    if not result or not isinstance(result, str):
        return False
    r = result.strip()
    if r.startswith("실행 오류") or r.startswith("도구 실행 오류") or r.startswith("도구 '"):
        return True
    if r == "승인되지 않음":
        return True
    if "실행할 기존 도구가 없습니다" in r:
        return True
    if "적합한 도구를 선택하지 못했습니다" in r or "적합한 기존 도구를 찾지 못했습니다" in r:
        return True
    if "검색 요청 오류" in r or "검색 처리 오류" in r:
        return True
    if r.startswith("Error:"):
        return True
    return False

def _router_step3_llm_classify(
    user_request: str,
    session_context: str,
    rag_context: str,
    tools_context: str,
    tools_list_str: str,
    chat_id: str,
) -> dict:
    """3단계: LLM 분류. 하드룰에 걸리지 않은 경우만 호출. Ollama 실패 시 Gemini 폴백."""
    system_prompt = router_step3_system_prompt(tools_list_str, TOOL_RAG_TOP_K)
    paper_hint = ""
    if get_paper_mode(chat_id):
        paper_hint = (
            "논문 모드(/paper)가 켜져 있음. 지식·문서 설명은 D(또는 B 기존 도구), "
            "명백한 파이썬 코드 실행·크롤링 등은 C. 순수 잡담만 A."
        )
    prompt = router_step3_user_prompt(
        user_request,
        session_context,
        tools_context,
        rag_context,
        TOOL_RAG_TOP_K,
        paper_mode_hint=paper_hint,
    )

    raw = "D"
    for llm_getter in (get_router_llm, get_executor_llm):
        try:
            resp = llm_getter().invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
            raw = (resp.content or "D").strip().upper()
            break
        except Exception as e:
            print(f"[DEBUG] Router LLM 실패 ({llm_getter.__name__}), 다음 시도: {e}")
    if raw.startswith("A") or raw == "A":
        route, choice = "direct_answer", "A"
    elif raw.startswith("B") or raw == "B":
        route, choice = "use_existing_tool", "B"
    elif raw.startswith("D") or raw == "D":
        route, choice = "direct_answer", "B"
    else:
        route, choice = "planner", "C"
    return {"route_type": route, "router_choice": choice}


def _maybe_override_rag_route(chat_id: str, user_request: str, result: dict) -> dict:
    """
    RAG 경로(direct_answer B)인데 논문 모드 OFF + 논문 키워드 없음 → 오버라이드.
    사실 조회(X 알아?)면 Tavily, 아니면 일상(A)으로.
    """
    if result.get("route_type") != "direct_answer" or result.get("router_choice") != "B":
        return result
    if is_rag_allowed(chat_id, user_request):
        return result
    # RAG 불가: 사실 조회면 Tavily, 아니면 일상
    if is_factual_lookup(user_request) and (AGENT_TOOLS_DIR / "tavily_search_tool.py").exists():
        print("[DEBUG] Router: RAG 불가 → Tavily로 오버라이드 (사실 조회)")
        return {"route_type": "use_existing_tool", "router_choice": "B", "used_tool_name": "tavily_search_tool"}
    print("[DEBUG] Router: RAG 불가 → 일상(A)으로 오버라이드")
    return {"route_type": "direct_answer", "router_choice": "A"}


def router_node(state: AgentState, *, config: RunnableConfig) -> dict:
    """Router: 1단계 하드룰 → 2단계 feature → 3단계 LLM 분류"""
    try:
        print("[DEBUG] Router: 진입")
        conf = config.get("configurable", {})
        chat_id = str(conf.get("chat_id", ""))
        is_scheduled = conf.get("is_scheduled", False)
        user_request = str(state.get("user_request") or "").strip()
        req_lower = user_request.lower().strip()
        print(f"[DEBUG] Router: user_request={user_request[:80]}...")

        # 1단계: 명백한 하드룰
        result = router_step1_hard_rules(user_request, req_lower, chat_id)
        if result:
            rule_name = result.get("route_type", "")
            choice = result.get("router_choice", "")
            print(f"[DEBUG] Router: 1단계 하드룰 → {rule_name} ({choice})")
            if is_scheduled and rule_name in ("planner", "code_run"):
                result = {"route_type": "direct_answer", "router_choice": "B"}
                print("[DEBUG] Router: 스케줄 작업 → planner/code_run 차단, direct_answer로 우회")
            result = _maybe_override_rag_route(chat_id, user_request, result)
            return result

        # 2단계: feature dict (LLM 분류용 컨텍스트)
        features = _router_step2_build_features(user_request, req_lower)

        # 3단계: LLM 분류
        session = get_session(chat_id)
        session_context = session.get_recent_context(max_turns=2)
        rag = get_chroma_rag_tool()
        rag_context = rag.search(user_request)
        _trs = get_tool_rag_store()
        tools_context = _trs.format_topk_block(user_request, k=TOOL_RAG_TOP_K)
        tools_list_str = _trs.format_router_tools_tag(user_request, k=TOOL_RAG_TOP_K)

        result = _router_step3_llm_classify(
            user_request, session_context, rag_context, tools_context, tools_list_str, chat_id
        )
        result = _apply_paper_mode_router_bias(chat_id, user_request, result)
        print(f"[DEBUG] Router: 3단계 LLM 분류 → {result.get('route_type')} (features={features})")
        # 스케줄 작업: planner는 승인 대기로 멈추므로, direct_answer로 강제 우회
        if is_scheduled and result.get("route_type") in ("planner", "code_run"):
            result = {"route_type": "direct_answer", "router_choice": "B"}
            print("[DEBUG] Router: 스케줄 작업 → planner/code_run 차단, direct_answer로 우회")
        result = _maybe_override_rag_route(chat_id, user_request, result)
        return result
    except Exception as e:
        print(f"❌ Router 노드 오류: {e}\n{traceback.format_exc()}")
        return {
            "route_type": "direct_answer",
            "router_choice": "A",
            "agent_fatal_error": f"Router: {type(e).__name__}: {e}",
        }


def _invoke_llm_with_fallback(
    messages,
    fallback_msg: str = "죄송해요, 답변을 생성하지 못했어요. 잠시 후 다시 질문해 주세요.",
    timeout_sec: float | None = None,
) -> str:
    """Ollama 우선, 실패 시 Gemini 폴백. 타임아웃 시 executor는 wait=False로 블로킹 없이 정리."""
    _llm_invoke_trace("entry", f"timeout_sec={timeout_sec!r} n_msg={len(messages) if messages else 0}")
    getters = (get_planner_llm, get_executor_llm)
    n = len(getters)
    for i, llm_getter in enumerate(getters):
        pool = None
        try:
            _llm_invoke_trace(f"loop i={i}", f"getter={llm_getter.__name__}")
            llm = llm_getter()
            label = _llm_model_label(llm)
            _llm_invoke_trace("after llm_getter()", f"label={label!r}")
            t0 = time.perf_counter()
            if timeout_sec and timeout_sec > 0:
                pool = ThreadPoolExecutor(max_workers=1)
                # submit(fn, *args)는 args를 먼저 평가해 llm.invoke 조회가 일어남 → lambda로 지연(타임아웃·테스트 목)
                _llm_invoke_trace("before pool.submit(lambda: llm.invoke)", f"timeout={timeout_sec}")
                fut = pool.submit(lambda: llm.invoke(messages))
                try:
                    _llm_invoke_trace("before fut.result(timeout)", "")
                    resp = fut.result(timeout=timeout_sec)
                    _llm_invoke_trace("after fut.result(timeout)", "ok")
                except FuturesTimeout:
                    elapsed = time.perf_counter() - t0
                    _llm_invoke_trace("FuturesTimeout", f"getter={llm_getter.__name__} elapsed={elapsed:.3f}s")
                    _log.debug(
                        "LLM timeout model=%s getter=%s elapsed=%.3fs next_fallback=%s",
                        label,
                        llm_getter.__name__,
                        elapsed,
                        i + 1 < n,
                    )
                    continue
                except Exception as e:
                    elapsed = time.perf_counter() - t0
                    _llm_invoke_trace("invoke thread Exception", f"{type(e).__name__}: {e}")
                    _log.debug(
                        "LLM invoke failed model=%s getter=%s elapsed=%.3fs err=%s next_fallback=%s",
                        label,
                        llm_getter.__name__,
                        elapsed,
                        e,
                        i + 1 < n,
                    )
                    continue
            else:
                _llm_invoke_trace("before llm.invoke (no thread timeout)", "")
                resp = llm.invoke(messages)
                _llm_invoke_trace("after llm.invoke (no thread timeout)", "ok")
            elapsed = time.perf_counter() - t0
            _log.debug(
                "LLM adopted model=%s getter=%s elapsed=%.3fs",
                label,
                llm_getter.__name__,
                elapsed,
            )
            _llm_invoke_trace("returning content", f"elapsed={elapsed:.3f}s len={len((resp.content or fallback_msg).strip())}")
            return (resp.content or fallback_msg).strip()
        except Exception as e:
            _llm_invoke_trace("outer loop Exception", f"getter={llm_getter.__name__} {type(e).__name__}: {e}")
            _log.debug(
                "LLM getter/invoke failed getter=%s err=%s next_fallback=%s",
                llm_getter.__name__,
                e,
                i + 1 < n,
            )
        finally:
            if pool is not None:
                pool.shutdown(wait=False, cancel_futures=True)
    _llm_invoke_trace("all getters exhausted", "returning fallback_msg")
    _log.debug("LLM all getters exhausted; returning fallback_msg")
    return fallback_msg


def direct_answer_node(state: AgentState, *, config: RunnableConfig) -> dict:
    """Direct Answer: A(일상 대화) 또는 B(RAG 검색)로 즉시 답변 (승인 불필요)"""
    conf = config.get("configurable", {})
    chat_id = str(conf.get("chat_id", ""))
    user_request = (state.get("user_request") or "").strip()
    image_base64 = state.get("image_base64")  # 직전 턴 이미지(문맥용)
    session = get_session(chat_id)
    router_choice = state.get("router_choice", "B")
    _da_trace(
        "entry",
        f"chat_id={chat_id!r} router_choice={router_choice!r} ulen={len(user_request)}",
    )

    if (state.get("agent_fatal_error") or "").strip():
        _da_trace("early_return", "agent_fatal_error set")
        return {}

    _da_timeout = DIRECT_ANSWER_TIMEOUT_SEC if DIRECT_ANSWER_TIMEOUT_SEC > 0 else None
    try:
        answer = ""
        if router_choice == "A":
            req_lower = user_request.lower()
            _da_trace("branch", "A daily/python_example")
            if state.get("python_example_direct"):
                session_ctx = session.get_recent_context(max_turns=2)
                sys_pe = DIRECT_ANSWER_PYTHON_EXAMPLE_SYSTEM
                prompt = direct_answer_python_example_user(session_ctx, user_request)
                content = _build_message_content(prompt, image_base64)
                _da_trace("before _invoke_llm_with_fallback", "A python_example")
                answer = _invoke_llm_with_fallback(
                    [SystemMessage(content=sys_pe), HumanMessage(content=content)],
                    timeout_sec=_da_timeout,
                )
                _da_trace("after _invoke_llm_with_fallback", "A python_example")
            elif any(x in req_lower for x in ("안녕", "hello", "hi", "반가", "좋은 아침")):
                answer = "안녕하세요. 윤수르입니다."
            elif any(x in user_request for x in ("누구야", "누구니", "누구세요", "자기소개", "정체", "이름이 뭐야", "윤수르")):
                answer = "윤수르입니다."
            elif any(x in user_request for x in ("기분이 어때", "기분은 어때", "기분이 어떠니", "기분은 어떠니", "기분이 어떠냐고")) or re.search(r"(너|넌|너는).*(어때|어떠니|어떠냐)", user_request):
                answer = "감정을 느끼지는 않지만, 지금처럼 편하게 대화 도와드릴 준비는 되어 있습니다."
            elif any(x in user_request for x in ("할 줄 아는 게 뭐야", "할 수 있어")):
                answer = "대화, 요약, 코드 작성, 도구 실행, 논문 검색과 정리 같은 작업을 도와드릴 수 있습니다."
            elif any(x in user_request for x in ("어디 서버",)):
                answer = "로컬 환경에서 실행 중인 텔레그램 봇입니다."
            elif any(x in user_request for x in ("위로", "힘들어", "피곤", "지쳤어", "격려", "응원")):
                answer = "많이 지치셨겠네요. 잠깐 쉬어 가셔도 괜찮고, 필요하시면 제가 바로 옆에서 하나씩 도와드릴게요."
            elif any(x in user_request for x in ("배고프", "출출")):
                answer = "배고프시겠네요. 간단하게라도 드시고 오시면 훨씬 낫습니다."
            elif any(x in user_request for x in ("졸려", "졸리")):
                answer = "많이 피곤하신가 봐요. 가능하면 잠깐이라도 쉬는 게 좋겠습니다."
            elif any(x in user_request for x in ("심심해", "심심하")):
                answer = "그러시군요. 가볍게 이야기 나누거나 바로 해볼 일 하나를 같이 정해볼까요?"
            else:
                # A: 일상 대화 - Chroma 절대 호출 금지, RAG/문서 관련 표현 0바이트
                system_prompt = DIRECT_ANSWER_DAILY_CHAT_SYSTEM
                session_ctx = session.get_recent_context(max_turns=2)
                prompt = direct_answer_daily_user(session_ctx, user_request)
                content = _build_message_content(prompt, image_base64)
                _da_trace("before _invoke_llm_with_fallback", "A daily_chat")
                answer = _invoke_llm_with_fallback(
                    [SystemMessage(content=system_prompt), HumanMessage(content=content)],
                    timeout_sec=_da_timeout,
                )
                _da_trace("after _invoke_llm_with_fallback", "A daily_chat")
        else:
            # B: RAG — rag.search()는 agent_chroma_rag에서 owner 스레드로 직렬화되며,
            # ChromaRAGTool 내부에서 collection.query는 _db_lock으로 동시 진입을 막는다(async 미사용).
            _da_trace("branch", "B RAG chroma+llm")
            req_lower = user_request.lower()

            depth_keywords = ("자세히", "더", "길게", "상세하게", "구체적으로")
            wants_depth = any(k in user_request for k in depth_keywords)
            top_k = RAG_TOP_K * 2 if wants_depth else RAG_TOP_K

            _da_trace("before get_chroma_rag_tool()", f"top_k={top_k} wants_depth={wants_depth}")
            rag = get_chroma_rag_tool()
            _da_trace("after get_chroma_rag_tool()", "ok")

            if ("chromadb" in req_lower or "논문" in user_request) and any(w in user_request for w in ("목록", "알려줘", "뭐 있어", "조회", "검색")):
                _da_trace("before rag.list_papers()", "sync jsonl, no chroma query")
                rag_context = rag.list_papers()
                _da_trace("after rag.list_papers()", f"len={len(rag_context)}")
            else:
                _da_trace("before rag.search()", f"top_k={top_k} (sync collection.query)")
                rag_context = rag.search(user_request, top_k=top_k)
                _da_trace("after rag.search()", f"len={len(rag_context)}")
                if _prefer_single_hit_rag_context(user_request, wants_depth=wants_depth):
                    rag_context = _rag_context_first_hit_only(rag_context)
                    _da_trace("rag_context top-1 only", f"len={len(rag_context)}")

            _da_trace("before session.get_last_assistant_response()", "")
            last_ai = session.get_last_assistant_response()
            _da_trace("after session.get_last_assistant_response()", f"last_ai_len={len(last_ai)}")

            system_prompt = DIRECT_ANSWER_RAG_SYSTEM_BASE
            if wants_depth:
                system_prompt += DIRECT_ANSWER_RAG_DEPTH_SUFFIX

            prompt = direct_answer_rag_user(
                session.get_context(), rag_context, last_ai, user_request
            )
            content = _build_message_content(prompt, image_base64)
            if isinstance(content, str):
                content = content + RAG_DIRECT_ANSWER_USER_SUFFIX
            elif isinstance(content, list) and content and isinstance(content[0], dict):
                t0 = str(content[0].get("text") or "")
                content[0]["text"] = t0 + RAG_DIRECT_ANSWER_USER_SUFFIX
            _da_trace("before _invoke_llm_with_fallback", "B RAG answer")
            answer = _invoke_llm_with_fallback(
                [SystemMessage(content=system_prompt), HumanMessage(content=content)],
                timeout_sec=_da_timeout,
            )
            _da_trace("after _invoke_llm_with_fallback", "B RAG answer")

        _da_trace("before telegram / structure", f"answer_len={len(answer)}")
        print(f"[DEBUG] DirectAnswer: 답변 생성 완료 ({len(answer)}자), 텔레그램 전송 시도")
        bot = conf.get("bot")
        chat_id = str(conf.get("chat_id", ""))
        if router_choice == "B":
            answer = _strip_thinking_tags(answer)
            answer = _enforce_rag_structure_markdown(answer)
        if router_choice == "B" and get_paper_mode(chat_id):
            answer = f"[논문 모드]\n\n{answer}"
        if bot and chat_id:
            if router_choice == "B":
                # HTML: 제목/불릿 이스케이프로 파싱 실패·벽돌 텍스트 폴백 최소화, \n 유지
                html_body = _rag_structured_lines_to_html(answer)
                if _safe_telegram_send(bot, chat_id, html_body[:4000], parse_mode="HTML"):
                    print("[DEBUG] DirectAnswer: 텔레그램 HTML 전송 성공")
                else:
                    plain_answer = _markdown_struct_to_plain(answer)
                    if _safe_telegram_send(bot, chat_id, plain_answer[:4000], parse_mode=None):
                        print("[DEBUG] DirectAnswer: 텔레그램 평문 전송 성공 (HTML 실패 후, 줄바꿈 유지)")
                    else:
                        print("[DEBUG] DirectAnswer: 텔레그램 전송 실패 (일시 오류)")
                        _notify_chat_error(
                            bot,
                            chat_id,
                            headline="⚠️ 답변 전송 실패",
                            detail="텔레그램으로 답변을 보내지 못했습니다. 네트워크·봇 토큰을 확인 후 다시 시도해 주세요.",
                            status_message_id=None,
                        )
            else:
                if _safe_telegram_send(bot, chat_id, answer[:4000], parse_mode="Markdown"):
                    print("[DEBUG] DirectAnswer: 텔레그램 전송 성공")
                else:
                    if _safe_telegram_send(bot, chat_id, answer[:4000], parse_mode=None):
                        print("[DEBUG] DirectAnswer: 텔레그램 평문 전송 성공 (Markdown 실패 후)")
                    else:
                        print("[DEBUG] DirectAnswer: 텔레그램 전송 실패 (일시 오류)")
                        _notify_chat_error(
                            bot,
                            chat_id,
                            headline="⚠️ 답변 전송 실패",
                            detail="텔레그램으로 답변을 보내지 못했습니다. 네트워크·봇 토큰을 확인 후 다시 시도해 주세요.",
                            status_message_id=None,
                        )

        return {"direct_response": answer}
    except Exception as e:
        print(f"❌ DirectAnswer 노드 오류: {e}\n{traceback.format_exc()}")
        err_text = f"Error: DirectAnswer: {type(e).__name__}: {e}"
        bot = conf.get("bot")
        chat_id = str(conf.get("chat_id", ""))
        if bot and chat_id:
            _safe_telegram_send(bot, chat_id, err_text[:4000])
        return {"direct_response": err_text, "execution_result": err_text}


def _run_tool_on_host(tool_name: str, user_request: str, chat_id: str = "") -> str:
    """
    agent_tools/ 도구를 맥 미니 본체(Host)에서 직접 실행. E2B 샌드박스 절대 사용 안 함.
    - run(user_request) 함수가 있으면 호출
    - 없으면 스크립트로 subprocess 실행 후 stdout 캡처
    - schedule_* 도구는 chat_id를 SCHEDULE_CHAT_ID 환경변수로 전달
    """
    import importlib.util
    import subprocess
    import sys

    if tool_name and tool_name.startswith("schedule_") and chat_id:
        os.environ["SCHEDULE_CHAT_ID"] = chat_id

    tools_dir = AGENT_TOOLS_DIR
    tool_path = resolve_agent_tool_py(tool_name, tools_dir)
    if tool_path is None:
        return f"도구 '{tool_name}'을 찾을 수 없습니다."

    try:
        parent_dir = str(tools_dir.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        spec = importlib.util.spec_from_file_location(f"tool_{tool_name}", tool_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, "run") and callable(getattr(mod, "run")):
            return str(mod.run(user_request))

        # run() 없음 → 스크립트로 실행 (print 출력 캡처)
        result = subprocess.run(
            [sys.executable, str(tool_path)],
            cwd=str(_MINI_ROOT),
            capture_output=True,
            text=True,
            timeout=CODE_TIMEOUT_SEC,
            env={**os.environ, "USER_REQUEST": user_request},
        )
        out = (result.stdout or "").strip()
        err = (result.stderr or "").strip()
        if result.returncode != 0 and err:
            return f"실행 오류: {err[:ERROR_LOG_MAX_CHARS]}"
        return out or "실행 완료 (출력 없음)"
    except subprocess.TimeoutExpired:
        return "실행 오류: 타임아웃"
    except Exception as e:
        return f"도구 실행 오류: {str(e)[:ERROR_LOG_MAX_CHARS]}"


def _tools_prompt_lines_for_llm(user_request: str, tools: list[tuple[str, str]]) -> list[str]:
    """도구 선택용 Gemini 프롬프트: Tool RAG Top-K 우선, 인덱스 비었을 때만 짧은 폴백."""
    hits = get_tool_rag_store().search(user_request, k=TOOL_RAG_TOP_K)
    if hits:
        return [f"- {h['name']}: {(h.get('doc') or '')[:180]}" for h in hits]
    if tools:
        return [f"- {name}" for name, _ in tools[:12]]
    return ["(저장된 도구 없음)"]


def use_existing_tool_node(state: AgentState, *, config: RunnableConfig) -> dict:
    """Use Existing Tool: agent_tools/ 도구를 맥 미니 본체에서 직접 실행 (E2B 샌드박스 절대 사용 안 함)"""
    print("[DEBUG] UseExistingTool: 진입 (Host 실행)")
    conf = config.get("configurable", {})
    chat_id = str(conf.get("chat_id", ""))
    user_request = (state.get("user_request") or "").strip()
    image_base64 = state.get("image_base64")
    used_tool_name = ""
    try:
        skill_lib = AgentSkillLibrary()
        tools = skill_lib.list_tools()
        selected_tool_name = state.get("used_tool_name", "")

        if not tools:
            result = "실행할 기존 도구가 없습니다."
        elif selected_tool_name and selected_tool_name in [n for n, _ in tools]:
            used_tool_name = selected_tool_name
            result = _run_tool_on_host(used_tool_name, user_request, chat_id)
        else:
            tools_list = _tools_prompt_lines_for_llm(user_request, tools)
            llm = get_executor_llm()
            form_write_keywords = ("입력해", "기입해", "입력해 줘", "기입해 줘", "기입해 봐", "입력해 봐", "써 봐", "넣어")
            if "http" in user_request and any(kw in user_request for kw in form_write_keywords):
                if "fill_google_form" in [n for n, _ in tools]:
                    used_tool_name = "fill_google_form"
                    result = _run_tool_on_host(used_tool_name, user_request, chat_id)
                else:
                    prompt = use_existing_tool_prompt_form_fill(
                        TOOL_RAG_TOP_K, chr(10).join(tools_list), user_request
                    )
                    content = _build_message_content(prompt, image_base64)
                    resp = llm.invoke([HumanMessage(content=content)])
                    raw = (resp.content or "").strip().replace(".py", "").strip().lower()
                    tool_names = [n for n, _ in tools]
                    tool_name = "fill_google_form" if "fill_google_form" in tool_names and "fill" in raw else None
                    if not tool_name:
                        tool_name = next((n for n in tool_names if n.lower() in raw or raw in n.lower()), None)
                    used_tool_name = tool_name or ""
                    result = _run_tool_on_host(tool_name, user_request, chat_id) if tool_name else "적합한 도구를 선택하지 못했습니다. fill_google_form을 사용하세요."
            else:
                search_intent = get_search_intent_local(user_request, user_request.lower())
                if search_intent == "web" and "tavily_search_tool" in [n for n, _ in tools]:
                    used_tool_name = "tavily_search_tool"
                    result = _run_tool_on_host(used_tool_name, user_request, chat_id)
                else:
                    prompt = use_existing_tool_prompt_generic(
                        TOOL_RAG_TOP_K, chr(10).join(tools_list), user_request
                    )
                    content = _build_message_content(prompt, image_base64)
                    resp = llm.invoke([HumanMessage(content=content)])
                    raw = (resp.content or "").strip().replace(".py", "").strip().lower()
                    tool_names = [n for n, _ in tools]
                    tool_name = next((n for n in tool_names if n.lower() in raw or raw in n.lower()), None)
                    used_tool_name = tool_name or ""
                    result = _run_tool_on_host(tool_name, user_request, chat_id) if tool_name else "적합한 기존 도구를 찾지 못했습니다. 요청 목적이나 도구명을 더 구체적으로 말씀해 주세요."

            if chat_id and used_tool_name:
                remember_tool(chat_id, used_tool_name, user_request)

        is_summarized = False
        if used_tool_name == "tavily_search_tool" and result and not result.startswith(("실행 오류", "도구 실행 오류", "TAVILY_API_KEY", "검색어를 입력")):
            try:
                print("[DEBUG] Tavily 요약: get_executor_llm(Gemini) 호출")
                resp = get_executor_llm().invoke([
                    HumanMessage(content=tavily_summarize_human(result[:6000])),
                ])
                summary = (resp.content or "").strip()
                if summary and len(summary) > 50:
                    result = summary
                    is_summarized = True
            except Exception as ex:
                print(f"[DEBUG] Tavily 요약 실패, 원문 전달: {ex}")

        bot = conf.get("bot")
        if bot and chat_id:
            if is_summarized:
                header = "📰 IT 뉴스 요약" if any(k in (user_request or "") for k in ("뉴스", "news", "최신", "오늘")) else "🔍 웹 검색 결과"
                _safe_telegram_send(bot, chat_id, f"{header}\n\n{result[:4000]}")
            else:
                header = "🔍 웹 검색 결과" if used_tool_name == "tavily_search_tool" else "🔧 기존 도구 실행 결과"
                if used_tool_name == "tavily_search_tool":
                    _safe_telegram_send(bot, chat_id, f"{header}\n\n{result[:4000]}")
                else:
                    msg = f"{header}\n\n```\n{result[:3500]}\n```"
                    if not _safe_telegram_send(bot, chat_id, msg, parse_mode="Markdown"):
                        _safe_telegram_send(bot, chat_id, f"{header}\n\n{result[:4000]}")

        return {"execution_result": result, "used_tool_name": used_tool_name}
    except Exception as e:
        print(f"❌ UseExistingTool 노드 오류: {e}\n{traceback.format_exc()}")
        err_text = f"Error: UseExistingTool: {type(e).__name__}: {e}"
        bot = conf.get("bot")
        if bot and chat_id:
            _safe_telegram_send(bot, chat_id, err_text[:4000])
        return {"execution_result": err_text, "used_tool_name": used_tool_name}


def route_after_router(state: AgentState) -> Literal["direct_answer", "use_existing_tool", "planner", "executor"]:
    """Router 분기: code_run→executor(승인 생략), A/B→direct_answer, 기본 planner"""
    if (state.get("agent_fatal_error") or "").strip():
        return "direct_answer"
    r = state.get("route_type", "planner")
    if r == "direct_answer":
        return "direct_answer"
    if r == "use_existing_tool":
        return "use_existing_tool"
    if r == "code_run":
        return "executor"
    return "planner"


# Planner: LLM 거부·비규격 응답 시에도 결재 단계까지 진행하기 위한 폴백 계획
PLANNER_FALLBACK_PLAN_STEPS = [
    "1단계: 사용자의 특별한 요청에 따른 코드 작성",
    "2단계: 샌드박스 실행 및 결과 확인",
]


def _parse_planner_llm_lines(plan_text: str) -> list[str]:
    """LLM 계획 텍스트에서 단계 줄만 안전하게 추출 (한 줄씩 예외 방지)."""
    out: list[str] = []
    text = plan_text if isinstance(plan_text, str) else str(plan_text or "")
    for raw in text.split("\n"):
        ln = raw.strip()
        if not ln:
            continue
        try:
            first = ln[0]
            head_digit = first.isdigit()
            if "단계" in ln and (head_digit or ln.startswith("•") or ln.startswith("-")):
                out.append(ln)
            elif head_digit or ln.startswith("•") or ln.startswith("-"):
                out.append(ln)
        except (IndexError, TypeError):
            continue
    return out


def planner_node(state: AgentState, *, config: RunnableConfig) -> dict:
    """Planner: Qwen으로 계획 수립 → HITL interrupt"""
    print("[DEBUG] Planner: 진입")
    conf = config.get("configurable", {})
    bot = conf.get("bot")
    chat_id = str(conf.get("chat_id", ""))
    thread_id = str(conf.get("thread_id", ""))

    # 재개(Resume) 시: 캐시 또는 state에 계획이 있으면 LLM·메시지 생략 (중복 방지)
    plan_cid = extract_chat_id_from_thread(thread_id)
    with with_chat_lock(plan_cid) if plan_cid else contextlib.nullcontext():
        existing_plan = state.get("plan") or (_plan_cache.get(thread_id) if plan_cid else None)
        if existing_plan:
            if thread_id in _plan_cache:
                del _plan_cache[thread_id]
    if existing_plan:
        approval = interrupt({"plan": existing_plan, "status": "pending"})
        approval_str = str(approval).strip().lower() if approval else ""
        if "승인" in approval_str or approval_str == "승인":
            return {"plan": existing_plan, "approval_status": "approved"}
        return {"approval_status": "rejected"}

    try:
        print("[DEBUG] Planner: RAG(논문·도구) 검색 시작...")
        rag = get_chroma_rag_tool()
        rag_context = rag.search(state["user_request"])
        tools_context = get_tool_rag_store().format_topk_block(state["user_request"], k=TOOL_RAG_TOP_K)
        print("[DEBUG] Planner: 로컬 Ollama 계획 생성 호출 (timeout≈120s)...")

        llm = get_planner_plan_llm()
        session = get_session(chat_id)

        system_prompt = PLANNER_SYSTEM_BASE
        learnings = load_learnings()
        if learnings:
            system_prompt += PLANNER_LEARNINGS_BLOCK.format(
                learnings=learnings[:3000],
                trunc_note="...(이하 생략)" if len(learnings) > 3000 else "",
            )
        if "http" in (state.get("user_request") or "").lower():
            system_prompt += PLANNER_URL_SUFFIX

        prompt = planner_user_prompt(
            TOOL_RAG_TOP_K,
            tools_context,
            rag_context,
            session.get_context(),
            state["user_request"],
        )

        image_base64 = state.get("image_base64")
        content = _build_message_content(prompt, image_base64)

        plan_lines: list[str] = []
        plan_text = ""
        try:
            resp = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=content)])
            raw_content = getattr(resp, "content", None) if resp is not None else None
            plan_text = (raw_content if isinstance(raw_content, str) else str(raw_content or "")).strip()
            plan_lines = _parse_planner_llm_lines(plan_text)
            if len(plan_lines) > 5:
                print(f"[WARN] Planner: 단계 {len(plan_lines)}개 → 상한 5개로 절단 (토큰/형식 방어)")
                plan_lines = plan_lines[:5]
        except Exception as parse_ex:
            print(
                f"[WARN] Planner LLM 호출 또는 응답 처리 중 예외 — 폴백 계획 사용: {parse_ex}\n{traceback.format_exc()}"
            )
            plan_lines = list(PLANNER_FALLBACK_PLAN_STEPS)

        if not plan_lines:
            # 규격 없는 장문 응답(거부·설명만 등)으로 단계 줄이 0개인 경우
            if plan_text:
                print("[WARN] Planner: 단계 형식 파싱 결과 없음(거부/비규격 응답 가능) — 폴백 계획 사용")
                plan_lines = list(PLANNER_FALLBACK_PLAN_STEPS)
            else:
                has_url = "http" in (state.get("user_request") or "").lower()
                plan_lines = (
                    ["1단계: URL 접근 파이썬 코드 작성 (requests, BeautifulSoup 등)", "2단계: 결과 확인 및 출력"]
                    if has_url
                    else ["1단계: 요청에 맞는 파이썬 코드 작성", "2단계: 실행 및 결과 확인"]
                )

        plan_display = "\n".join(f"• {p}" for p in plan_lines)
        msg = (
            f"📋 **계획을 세웠습니다.**\n\n{plan_display}\n\n"
            "실행할까요? **승인** 또는 **거절** 로 답장해 주세요."
        )

        sink = conf.get("bridge_plan_sink")
        if isinstance(sink, dict) and not bot:
            sink["last_plan_markdown"] = msg

        print(f"[DEBUG] Planner: 계획 {len(plan_lines)}단계 생성 완료, 텔레그램 전송 시도")
        if bot and chat_id:
            if _safe_telegram_send(bot, chat_id, msg, parse_mode="Markdown"):
                print("[DEBUG] Planner: 텔레그램 전송 성공")
            else:
                # Markdown 파싱 오류 등으로 본문이 아예 안 가는 경우 평문 재시도
                plain = msg.replace("**", "").replace("`", "")
                if _safe_telegram_send(bot, chat_id, plain, parse_mode=None):
                    print("[DEBUG] Planner: 텔레그램 평문 전송 성공 (Markdown 실패 후)")
                else:
                    print("[DEBUG] Planner: 텔레그램 전송 실패 (일시 오류)")

        with with_chat_lock(plan_cid) if plan_cid else contextlib.nullcontext():
            _plan_cache[thread_id] = plan_lines
    except Exception as e:
        print(f"❌ Planner 노드 오류: {e}\n{traceback.format_exc()}")
        err = f"Error: Planner: {type(e).__name__}: {e}"
        return {
            "agent_fatal_error": f"Planner: {type(e).__name__}: {e}",
            "approval_status": "rejected",
            "execution_result": err,
        }

    approval = interrupt({"plan": plan_lines, "status": "pending"})
    approval_str = str(approval).strip().lower() if approval else ""

    if "승인" in approval_str or approval_str == "승인":
        return {"plan": plan_lines, "approval_status": "approved"}
    return {"approval_status": "rejected"}


def planner_debate_node(state: AgentState) -> dict:
    """Planner Debate: 승인된 계획을 내부적으로 한 번 더 검토/보정.
    사용자에게는 토론 내용을 노출하지 않고, 개선된 plan만 다음 단계로 전달."""
    t0 = time.perf_counter()
    print("[DEBUG] PlannerDebate: 진입")
    if state.get("approval_status") != "approved":
        return {}

    original_plan = state.get("plan") or []
    user_request = (state.get("user_request") or "").strip()
    if not original_plan or not user_request:
        return {}

    try:
        llm = get_planner_plan_llm()
        plan_text = "\n".join(original_plan)

        critique_resp = llm.invoke(
            [
                SystemMessage(content=PLANNER_DEBATE_CRITIC_SYSTEM),
                HumanMessage(content=planner_debate_critic_user(user_request, plan_text)),
            ]
        )
        critique = (critique_resp.content or "").strip()

        revised_resp = llm.invoke(
            [
                SystemMessage(content=PLANNER_DEBATE_REVISE_SYSTEM),
                HumanMessage(
                    content=planner_debate_revise_user(user_request, plan_text, critique)
                ),
            ]
        )
        revised_text = (revised_resp.content or "").strip()

        revised_lines = []
        if revised_text:
            for ln in revised_text.split("\n"):
                ln = ln.strip()
                if not ln:
                    continue
                if "단계" in ln and (ln[0].isdigit() or ln.startswith("•") or ln.startswith("-")):
                    revised_lines.append(ln)
                elif ln[0].isdigit() or ln.startswith("•") or ln.startswith("-"):
                    revised_lines.append(ln)

        if not revised_lines:
            elapsed = time.perf_counter() - t0
            print(f"[DEBUG] PlannerDebate: 보정 없음 (소요 {elapsed:.2f}s)")
            return {"plan": original_plan}

        elapsed = time.perf_counter() - t0
        print(f"[DEBUG] PlannerDebate: 계획 보정 완료 ({len(revised_lines)}단계, 소요 {elapsed:.2f}s)")
        return {"plan": revised_lines}
    except Exception as e:
        print(f"❌ PlannerDebate 노드 오류: {e}\n{traceback.format_exc()}")
        err = f"Error: PlannerDebate: {type(e).__name__}: {e}"
        return {
            "plan": original_plan,
            "agent_fatal_error": f"PlannerDebate: {type(e).__name__}: {e}",
            "execution_result": err,
        }


def executor_node(state: AgentState) -> dict:
    """Executor: Groq(ChatGroq)로 코드 작성 및 exec/eval 실행"""
    if state.get("approval_status") != "approved":
        return {"generated_code": "", "execution_result": "승인되지 않음"}
    fe = (state.get("agent_fatal_error") or "").strip()
    if fe:
        return {"generated_code": "", "execution_result": f"Error: {fe}"}

    try:
        is_code_run = state.get("route_type") == "code_run"
        if is_code_run:
            tools_context = ""
            rag_context = ""
        else:
            tools_context = get_tool_rag_store().format_topk_block(
                state.get("user_request") or "", k=TOOL_RAG_TOP_K
            )
            rag = get_chroma_rag_tool()
            rag_context = rag.search(state["user_request"])[:500] if state.get("user_request") else ""

        llm = get_coding_groq_llm()
        plan_str = "\n".join(f"{i+1}. {p}" for i, p in enumerate(state.get("plan", [])))
        error_hint = state.get("error_hint", "")
        user_request = state.get("user_request", "")
        image_base64 = state.get("image_base64")

        if is_code_run:
            prompt = executor_user_prompt_code_run(plan_str, user_request)
        else:
            prompt = executor_user_prompt_full(plan_str, user_request)

        if tools_context:
            prompt += executor_tools_append(TOOL_RAG_TOP_K, tools_context)
        if rag_context:
            prompt += executor_rag_append(rag_context)
        if error_hint:
            prompt += executor_error_append(error_hint)
        if _user_wants_intentional_exec_error(user_request):
            prompt += EXECUTOR_INTENTIONAL_SYNTAX_BLOCK
        prompt += EXECUTOR_USER_FOOTER_CODE_RUN if is_code_run else EXECUTOR_USER_FOOTER_FULL

        content = _build_message_content(prompt, image_base64)
        executor_system_prompt = EXECUTOR_SYSTEM_CODE_RUN if is_code_run else EXECUTOR_SYSTEM_FULL

        resp = llm.invoke([SystemMessage(content=executor_system_prompt), HumanMessage(content=content)])
        code = resp.content.strip() if resp.content else ""
        for marker in ("```python", "```"):
            if marker in code:
                start = code.find(marker) + len(marker)
                end = code.rfind("```")
                if end > start:
                    code = code[start:end].strip()
                break

        result = _run_code_sandbox(code)

        return {"generated_code": code, "execution_result": result}
    except Exception as e:
        print(f"❌ Executor 노드 오류: {e}\n{traceback.format_exc()}")
        err = f"Error: Executor: {type(e).__name__}: {e}"
        return {"generated_code": "", "execution_result": err}


def _truncate_error(log: str, max_chars: int = ERROR_LOG_MAX_CHARS) -> str:
    """에러 로그 압축: 마지막 N자만 전달"""
    if len(log) <= max_chars:
        return log
    return f"...(생략)...\n{log[-max_chars:]}"


def _is_result_irrelevant(user_request: str, execution_result: str) -> bool:
    """실행 결과가 사용자 요청과 무관한지 LLM으로 판단. (예: 구글 폼 요청했는데 매출 데이터 나옴)"""
    if not user_request.strip() or not execution_result.strip():
        return False
    try:
        llm = get_coding_groq_llm()
        resp = llm.invoke(
            [HumanMessage(content=monitor_irrelevance_check_human(user_request, execution_result))]
        )
        ans = (resp.content or "").strip().upper()
        return "FAIL" in ans
    except Exception:
        return False


def monitor_node(state: AgentState) -> dict:
    """Monitor(Groq): 실행 결과 감시 → 에러 시 error_hint와 함께 Executor로 (로그 압축).
    문법 에러 없어도, 실행 결과가 user_request와 무관하면 반려(Retry)."""
    result = state.get("execution_result", "")
    retry = state.get("retry_count", 0)
    max_retry = 1 if state.get("light_monitor") else 2
    user_request = state.get("user_request", "")

    is_error = _is_execution_failure(result)

    # 의도적 SyntaxError/오타 실행 요청: 에러 출력이 곧 성공이므로 재시도하지 않음
    if is_error and _user_wants_intentional_exec_error(user_request):
        print("[DEBUG] Monitor: 의도적 오류 실행 요청 → 재시도 생략")
        return {"content_irrelevant": False}

    # 1) 문법/런타임 에러 → 기존 로직: 에러 분석 후 재시도
    if is_error and retry < max_retry:
        truncated = _truncate_error(result)
        try:
            llm = get_coding_groq_llm()
            resp = llm.invoke(
                [
                    HumanMessage(
                        content=monitor_error_analysis_human(
                            truncated, state.get("generated_code", "") or ""
                        )
                    )
                ]
            )
            hint = resp.content.strip() if resp.content else "재시도"
        except Exception as ex:
            print(f"❌ Monitor(LLM 분석) 오류: {ex}\n{traceback.format_exc()}")
            hint = f"Monitor LLM 오류: {ex}. 코드를 점검해 재시도하세요."
        return {"retry_count": retry + 1, "error_hint": hint}

    # 2) 에러 없음 → 실행 결과가 user_request와 관련 있는지 검수 (code_run 경로는 생략)
    if (
        not is_error
        and retry < max_retry
        and not state.get("light_monitor")
        and _is_result_irrelevant(user_request, result)
    ):
        try:
            llm = get_coding_groq_llm()
            resp = llm.invoke(
                [HumanMessage(content=monitor_content_irrelevant_retry_human(user_request, result))]
            )
            hint = (resp.content or "요청과 무관한 결과. 올바른 주제로 다시 코딩하라.").strip()
        except Exception as ex:
            print(f"❌ Monitor(관련성 검수) 오류: {ex}\n{traceback.format_exc()}")
            hint = f"Monitor 검수 LLM 오류: {ex}"
        return {"retry_count": retry + 1, "error_hint": hint, "content_irrelevant": True}

    return {"content_irrelevant": False}  # 성공 시 플래그 초기화


def route_after_monitor(state: AgentState) -> Literal["executor", "__end__"]:
    user_request = state.get("user_request", "")
    result = state.get("execution_result", "")
    retry = state.get("retry_count", 0)
    is_error = _is_execution_failure(result)
    content_irrelevant = state.get("content_irrelevant", False)
    # 의도적 SyntaxError 시나리오: Monitor가 재시도를 막아도 retry 카운트는 0이라
    # 아래 분기만 보면 다시 executor로 가버림 → 한 번 더 돌며 '고쳐진' 성공 출력이 나올 수 있음.
    if is_error and _user_wants_intentional_exec_error(user_request):
        return "__end__"
    if (is_error or content_irrelevant) and retry < 2:
        return "executor"
    return "__end__"


def route_after_planner(state: AgentState) -> Literal["planner_debate", "executor", "__end__"]:
    """승인 후: 의도적 오류·트리비얼 코딩은 planner_debate(Ollama 2회) 생략 → 바로 executor."""
    if state.get("approval_status") != "approved":
        return "__end__"
    user_request = state.get("user_request", "")
    if _user_wants_intentional_exec_error(user_request):
        print("[DEBUG] route_after_planner: 의도적 오류 실행 요청 → planner_debate 생략, executor로")
        return "executor"
    if _skip_planner_debate_for_fast_path(user_request):
        print("[DEBUG] route_after_planner: 트리비얼 코딩 요청 → planner_debate 생략, executor로")
        return "executor"
    return "planner_debate"
