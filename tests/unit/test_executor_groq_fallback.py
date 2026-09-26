"""executor_node 의 Groq → 로컬 base 폴백 계약.

`docs/experiments/prior_work.md` §6 (2026-09-27 측정): 같은 코딩 30문항에서 Groq
`openai/gpt-oss-120b` 는 0/90 실패, 로컬 base `qwen3.5:9b` 는 14/90(15.6%) 실패다.
base 는 Groq 보다 나쁘지만 **아무 답도 못 주는 것보다는 낫다** — Groq 이 429·장애를
내도 답변이 나가야 한다. 파인튜닝(v6·v9)은 base 보다 나쁘므로 폴백에 쓰지 않는다.

`core.graph.agent_nodes` 임포트는 이 저장소(SMB 마운트)에서 분 단위로 느리다. 그래서
모듈을 임포트하지 않고 **필요한 함수의 소스만 ast 로 떼어내** 스텁 네임스페이스에서
실행한다 (`tests/unit/test_eval_num_predict_matches_prod.py` 와 같은 "무거운 임포트
없음" 방식). 검사하는 코드는 운영 소스 그대로다.
"""

from __future__ import annotations

import ast
import logging
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from pathlib import Path

import pytest

from core.llm.code_extract import extract_python_code

pytestmark = pytest.mark.unit

_ROOT = Path(__file__).resolve().parents[2]
SRC = _ROOT / "core" / "graph" / "agent_nodes.py"

# 폴백 경로에 실제로 참여하는 함수들만 떼어낸다.
WANTED = ("_llm_invoke_trace", "_llm_model_label", "_invoke_llm_with_fallback", "executor_node")


class _Msg:
    """SystemMessage/HumanMessage 대역."""

    def __init__(self, content):
        self.content = content


class _Resp:
    """AIMessage 대역."""

    def __init__(self, content):
        self.content = content


class _FakeLLM:
    def __init__(self, model: str, reply: str):
        self.model = model
        self._reply = reply
        self.calls = 0

    def invoke(self, _messages):
        self.calls += 1
        return _Resp(self._reply)


def _fn_nodes():
    tree = ast.parse(SRC.read_text(encoding="utf-8"), filename=str(SRC))
    found = {
        n.name: n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name in WANTED
    }
    missing = [name for name in WANTED if name not in found]
    assert not missing, f"agent_nodes.py 에서 함수를 찾지 못했다: {missing}"
    return found


def _named(fn, name: str):
    """getter 에 운영과 같은 __name__ 을 붙인다 (폴백 로그가 이 이름을 쓴다)."""

    def _getter():
        return fn()

    _getter.__name__ = name
    return _getter


def _load_ns(*, groq_getter, local_getter, sandbox):
    """WANTED 함수들을 스텁 전역에서 실행 가능한 네임스페이스로 반환."""
    found = _fn_nodes()
    module = ast.parse("from __future__ import annotations\n", filename=str(SRC))
    module.body.extend(found[name] for name in WANTED)
    # 폴백 로그는 getter.__name__ 으로 어느 LLM 이 답했는지 적는다 → 운영 이름을 붙여 둔다.
    groq_getter = _named(groq_getter, "get_coding_groq_llm")
    local_getter = _named(local_getter, "get_planner_llm")
    ns = {
        "__name__": "agent_nodes_executor_fallback_stub",
        "logging": logging,
        "time": time,
        "traceback": traceback,
        "ThreadPoolExecutor": ThreadPoolExecutor,
        "FuturesTimeout": FuturesTimeout,
        "_log": logging.getLogger("test_executor_groq_fallback"),
        "SystemMessage": _Msg,
        "HumanMessage": _Msg,
        "normalize_ai_message_content": lambda resp: resp.content or "",
        "extract_python_code": extract_python_code,
        "_run_code_sandbox": sandbox,
        "_build_message_content": lambda prompt, _image=None: prompt,
        "_user_wants_intentional_exec_error": lambda _req: False,
        "TOOL_RAG_TOP_K": 3,
        "EXECUTOR_SYSTEM_CODE_RUN": "SYS_CODE_RUN",
        "EXECUTOR_SYSTEM_FULL": "SYS_FULL",
        "EXECUTOR_USER_FOOTER_CODE_RUN": "",
        "EXECUTOR_USER_FOOTER_FULL": "",
        "EXECUTOR_INTENTIONAL_SYNTAX_BLOCK": "",
        "executor_user_prompt_code_run": lambda plan, req: f"{plan}\n{req}",
        "executor_user_prompt_full": lambda plan, req: f"{plan}\n{req}",
        "executor_tools_append": lambda _k, _c: "",
        "executor_rag_append": lambda _c: "",
        "executor_error_append": lambda _h: "",
        "get_coding_groq_llm": groq_getter,
        "get_planner_llm": local_getter,
    }
    exec(compile(ast.fix_missing_locations(module), str(SRC), "exec"), ns)
    return ns


def _state():
    # code_run 경로: tool RAG·Chroma 를 타지 않아 LLM 경로만 남는다.
    return {
        "approval_status": "approved",
        "route_type": "code_run",
        "plan": ["41 + 1 을 출력한다"],
        "user_request": "41 더하기 1 출력해줘",
    }


class _Sandbox:
    def __init__(self, result: str = "42"):
        self.result = result
        self.codes: list[str] = []

    def __call__(self, code: str) -> str:
        self.codes.append(code)
        return self.result


def test_groq_getter_failure_falls_back_to_local_base(capsys):
    """Groq getter 가 429 를 던지면 로컬 base 가 답하고 실행까지 간다."""
    groq_calls = []

    def groq_getter():
        groq_calls.append(1)
        raise RuntimeError("429 Too Many Requests: rate limit exceeded")

    local = _FakeLLM("qwen3.5:9b", "```python\nprint(41 + 1)\n```")
    sandbox = _Sandbox("42")
    ns = _load_ns(groq_getter=groq_getter, local_getter=lambda: local, sandbox=sandbox)

    out = ns["executor_node"](_state())

    assert groq_calls == [1], "Groq 을 먼저 시도해야 한다"
    assert local.calls == 1, "Groq 실패 시 로컬 base 가 받아야 한다"
    assert out["execution_result"] == "42"
    assert out["generated_code"] == "print(41 + 1)"
    assert sandbox.codes == ["print(41 + 1)"]

    # 어느 LLM 이 답했는지 로그에 남는다 (폴백 발동 추적).
    logged = capsys.readouterr().out
    assert "fallback_used=True" in logged
    assert "get_planner_llm" in logged
    assert "qwen3.5:9b" in logged


def test_healthy_groq_answers_without_touching_local():
    """Groq 이 정상이면 로컬은 호출되지 않는다 (base 는 15.6% 실패 — 2순위여야 한다)."""
    groq = _FakeLLM("openai/gpt-oss-120b", "```python\nprint(41 + 1)\n```")
    local_calls: list[int] = []

    def local_getter():
        # 폴백 헬퍼가 getter 예외를 삼키므로, 호출 사실만 기록해 뒤에서 단정한다.
        local_calls.append(1)
        return _FakeLLM("qwen3.5:9b", "```python\nprint(0)\n```")

    sandbox = _Sandbox("42")
    ns = _load_ns(groq_getter=lambda: groq, local_getter=local_getter, sandbox=sandbox)

    out = ns["executor_node"](_state())

    assert groq.calls == 1
    assert local_calls == [], "Groq 이 정상인데 로컬 폴백이 호출됐다"
    assert out["execution_result"] == "42"


def test_local_invoke_failure_also_falls_back():
    """getter 는 성공하고 invoke 가 죽는 경우(장애)도 폴백한다."""

    class _BoomLLM:
        model = "openai/gpt-oss-120b"

        def invoke(self, _messages):
            raise RuntimeError("503 Service Unavailable")

    local = _FakeLLM("qwen3.5:9b", "```python\nprint(41 + 1)\n```")
    sandbox = _Sandbox("42")
    ns = _load_ns(groq_getter=lambda: _BoomLLM(), local_getter=lambda: local, sandbox=sandbox)

    out = ns["executor_node"](_state())

    assert local.calls == 1
    assert out["execution_result"] == "42"


def test_all_llms_down_returns_error_and_runs_nothing(capsys):
    """둘 다 죽으면 기존과 같은 Error: Executor: ... 를 돌려주고, 사과문을 실행하지 않는다."""

    def boom_groq():
        raise RuntimeError("429 rate limit")

    def boom_local():
        raise RuntimeError("ollama connection refused")

    sandbox = _Sandbox("SHOULD_NOT_RUN")
    ns = _load_ns(groq_getter=boom_groq, local_getter=boom_local, sandbox=sandbox)

    out = ns["executor_node"](_state())

    assert out["generated_code"] == ""
    assert out["execution_result"].startswith("Error: Executor:")
    assert sandbox.codes == [], "LLM 이 전부 실패했으면 코드를 실행하지 않는다"
    assert "all getters exhausted" in capsys.readouterr().out


def test_executor_wires_groq_then_base_and_no_finetune():
    """배선이 되돌아가지 않게 소스를 고정한다 — 폴백은 base(get_planner_llm)여야 한다.

    파인튜닝(yunsur_v6·v9)은 base 보다 나쁘므로 (prior_work.md §6) 폴백에 쓰지 않는다.
    """
    node = _fn_nodes()["executor_node"]
    getters = None
    for call in (n for n in ast.walk(node) if isinstance(n, ast.Call)):
        if getattr(call.func, "id", None) != "_invoke_llm_with_fallback":
            continue
        for kw in call.keywords:
            if kw.arg == "getters":
                getters = [getattr(e, "id", None) for e in kw.value.elts]
    assert getters == ["get_coding_groq_llm", "get_planner_llm"], (
        f"executor_node 의 폴백 체인이 바뀌었다: {getters}"
    )
    src = ast.unparse(node)
    for finetuned in ("yunsur", "RAG_ANSWER_MODEL"):
        assert finetuned not in src, f"폴백에 {finetuned} 를 쓰면 안 된다 (base 보다 나쁘다)"
