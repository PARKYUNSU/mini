"""평가기의 슬롯별 출력 상한이 운영과 어긋나지 않게 지킨다.

2026-09-25 측정에서 이것이 결론을 흔들었다 (docs/experiments/baseline_0925/README.md):
평가기가 코딩에 800 을 줬는데 그 상한이 병목이어서 실패 36건 중 16건이 잘림이었고,
잘림을 통과로 바꾸는 낙관적 상한에서 McNemar p 가 0.002 → 0.250 으로 바뀌었다.
평가기가 운영보다 엄격하면 **장황한 모델이 잘림으로 실패하고 그것이 모델 차이로
오인된다.** 그래서 소스를 ast 로 읽어 두 값을 맞춰 둔다 (무거운 임포트 없음).

코딩 슬롯은 예외다 — 운영 Executor 는 로컬이 아니라 Groq(`get_coding_groq_llm`)을
쓰므로 대응하는 운영 값이 없다. 그 슬롯은 "로컬이 Groq 을 대신할 수 있나" 라는 가정
질문이고, 상한이 병목이 되지 않도록 넉넉한 쪽(OLLAMA_DIRECT_NUM_PREDICT)에 맞춘다.
"""

from __future__ import annotations

import ast
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
EVAL = _ROOT / "scripts" / "eval_local_llm_failure.py"
PROD = _ROOT / "core" / "llm" / "agent_llm.py"

# 슬롯 → 운영 getter. 코딩은 운영 대응이 없어 제외한다.
SLOT_TO_GETTER = {
    "chat": "get_planner_llm",
    "rag": "get_rag_answer_llm",
    "planner": "get_planner_plan_llm",
}
GENEROUS = "OLLAMA_DIRECT_NUM_PREDICT"


def _expr(node: ast.AST) -> str:
    """num_predict 값을 비교 가능한 문자열로. 정수 리터럴이면 그 값, 이름이면 이름."""
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return str(node.value)
    if isinstance(node, ast.Name):
        return node.id
    return ast.dump(node)


def _prod_caps() -> dict[str, str]:
    """운영 getter 이름 → num_predict 표현."""
    tree = ast.parse(PROD.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for fn in tree.body:
        if not isinstance(fn, ast.FunctionDef):
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.keyword) and node.arg == "num_predict":
                out[fn.name] = _expr(node.value)
    return out


def _eval_caps() -> dict[str, str]:
    """평가기 SLOT_NUM_PREDICT 의 슬롯 → 표현."""
    tree = ast.parse(EVAL.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "SLOT_NUM_PREDICT" for t in node.targets
        ):
            assert isinstance(node.value, ast.Dict)
            return {
                k.value: _expr(v)
                for k, v in zip(node.value.keys, node.value.values)
                if isinstance(k, ast.Constant)
            }
    raise AssertionError("SLOT_NUM_PREDICT 를 찾지 못했다")


def test_slot_caps_cover_every_slot():
    caps = _eval_caps()
    assert set(caps) == {"chat", "rag", "planner", "coding"}, caps


def test_slots_with_a_production_counterpart_match_it():
    prod, ev = _prod_caps(), _eval_caps()
    mismatched = {}
    for slot, getter in SLOT_TO_GETTER.items():
        assert getter in prod, f"운영에서 {getter} 의 num_predict 를 찾지 못했다"
        if ev[slot] != prod[getter]:
            mismatched[slot] = f"평가기 {ev[slot]} vs 운영 {getter} {prod[getter]}"
    assert not mismatched, (
        "평가기와 운영의 출력 상한이 다르다 — 장황한 모델이 잘림으로 실패해 모델 차이로 "
        f"오인된다:\n{mismatched}"
    )


def test_coding_cap_is_generous_because_production_uses_groq():
    """운영 Executor 는 Groq 이라 대응 값이 없다. 상한이 병목이 되지 않게 넉넉히 준다."""
    ev = _eval_caps()
    assert ev["coding"] == GENEROUS, (
        f"코딩 상한이 {ev['coding']} 다. 병목이 되면 능력이 아니라 장황함을 재게 된다 "
        "(docs/experiments/baseline_0925/README.md)"
    )
    src = PROD.read_text(encoding="utf-8")
    assert "def get_coding_groq_llm" in src, "운영 코딩 LLM 이 바뀌었다면 이 예외를 재검토할 것"
