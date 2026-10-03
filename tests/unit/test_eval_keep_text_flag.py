"""평가기의 응답 원문 보존(`--keep-text`)이 옵트인으로 남아 있게 지킨다.

왜 있나: 라운드 원본은 응답을 240자 `preview` 로만 저장했다. 그 상태로 RAG 응답의
템플릿 섹션을 세다가 **잘림을 세는** 실수를 했다 (docs/experiments/length_mechanism_1003.md
§6 — 다시 측정해야 했다). 그래서 원문을 남기는 선택지를 뒀다.

두 방향을 같이 지킨다:
  (1) 플래그가 있어야 한다 — 없으면 기전 분석이 또 재측정을 요구한다.
  (2) **기본값은 꺼짐이어야 한다** — 켜지면 과거 라운드와 파일 크기·형식이 달라지고,
      무엇보다 판정에 쓰이지 않는 필드가 조용히 늘어난다.

소스를 ast 로 읽는다 (이 스크립트는 무거운 임포트를 끌고 온다).
"""

from __future__ import annotations

import ast
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
EVAL = _ROOT / "scripts" / "eval_local_llm_failure.py"

_TREE = ast.parse(EVAL.read_text(encoding="utf-8"))


def _add_argument_calls() -> dict[str, ast.Call]:
    """`ap.add_argument("--x", ...)` 들을 플래그명 → Call 로 모은다."""
    out: dict[str, ast.Call] = {}
    for node in ast.walk(_TREE):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "add_argument"):
            continue
        if node.args and isinstance(node.args[0], ast.Constant):
            name = node.args[0].value
            if isinstance(name, str) and name.startswith("--"):
                out[name] = node
    return out


def test_keep_text_flag_exists_and_is_a_store_true_optin() -> None:
    call = _add_argument_calls().get("--keep-text")
    assert call is not None, "--keep-text 플래그가 사라졌다 — 원문 보존 수단이 없으면 기전 분석이 재측정을 요구한다"
    action = next((kw.value for kw in call.keywords if kw.arg == "action"), None)
    assert isinstance(action, ast.Constant) and action.value == "store_true", (
        "--keep-text 는 store_true 여야 한다 (기본 꺼짐)"
    )
    # store_true 는 기본이 False 다. default 를 따로 줘서 켜 두는 일이 없어야 한다.
    default = next((kw.value for kw in call.keywords if kw.arg == "default"), None)
    assert default is None or (isinstance(default, ast.Constant) and default.value is False), (
        "--keep-text 의 기본값이 켜져 있다 — 과거 라운드와 원본 형식이 달라진다"
    )


def test_text_is_dropped_unless_keep_text() -> None:
    """`row.pop("text", None)` 이 `args.keep_text` 분기 **안에** 있어야 한다."""
    pops: list[ast.Call] = []
    for node in ast.walk(_TREE):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "pop"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "row"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value == "text"
        ):
            pops.append(node)
    assert pops, 'row.pop("text", ...) 가 없다 — 기본 동작이 원문을 남기도록 바뀌었다'

    # pop 을 감싸는 if 가 keep_text 를 본다
    guarded = False
    for node in ast.walk(_TREE):
        if not isinstance(node, ast.If):
            continue
        names = {
            n.attr for n in ast.walk(node.test) if isinstance(n, ast.Attribute)
        } | {n.id for n in ast.walk(node.test) if isinstance(n, ast.Name)}
        if "keep_text" not in names:
            continue
        if any(p in ast.walk(node) for p in pops):
            guarded = True
    assert guarded, 'row.pop("text") 가 args.keep_text 분기 안에 없다'
