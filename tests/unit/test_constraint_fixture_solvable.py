"""제약 문항이 실제로 풀리는지 지킨다 — 참조답안이 제약을 통과해야 한다.

`tests/unit/test_coding_fixture_solvable.py` 와 같은 역할이다. 풀 수 없는 문항이
섞이면 모든 모델이 거기서 실패해 실패율이 **모델이 아니라 문항 결함**을 반영한다
(docs/experiments/yunsur_v6/README.md 의 coding_10 사례).

채점에는 참조답안을 쓰지 않는다. 문항의 풀림 가능성만 확인한다.

계획 슬롯의 참조답안은 판정기가 `_parse_planner_llm_lines` 로 뽑아 이어붙인
'단계 줄' 형태 그대로다 — 참조답안이 단계 줄만 담고 있으므로 파싱은 항등이고,
그래서 이 테스트는 무거운 `core.graph.agent_nodes` 임포트 없이 돈다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

from core.llm.constraint_check import KNOWN_KEYS, check_constraints  # noqa: E402

pytestmark = pytest.mark.unit

FIXTURE = _ROOT / "tests" / "fixtures" / "local_llm_failure_eval.jsonl"
ANSWERS = _ROOT / "tests" / "fixtures" / "constraint_reference_answers.json"


def _constrained_items() -> dict[str, dict]:
    out = {}
    for line in FIXTURE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("constraints"):
            out[row["id"]] = row
    return out


def _answers() -> dict[str, str]:
    return json.loads(ANSWERS.read_text(encoding="utf-8"))["items"]


def test_every_constrained_item_has_a_reference_answer():
    items, answers = _constrained_items(), _answers()
    assert items, "제약 문항이 하나도 없다 — 문항 집합이 바뀌었나?"
    missing = sorted(set(items) - set(answers))
    orphan = sorted(set(answers) - set(items))
    assert not missing, f"참조답안 없는 제약 문항: {missing}"
    assert not orphan, f"문항에 없는 참조답안: {orphan}"


@pytest.mark.parametrize("item_id", sorted(_constrained_items()))
def test_reference_answer_satisfies_constraints(item_id):
    """이게 깨지면 문항이 풀 수 없거나 제약이 잘못 적혔다는 뜻이다."""
    item = _constrained_items()[item_id]
    ok, kind = check_constraints(_answers()[item_id], item["constraints"])
    assert ok, f"{item_id}: 참조답안이 제 제약을 못 지킨다 ({kind})"


@pytest.mark.parametrize("item_id", sorted(_constrained_items()))
def test_constraint_keys_are_known(item_id):
    for key in _constrained_items()[item_id]["constraints"]:
        assert key in KNOWN_KEYS, f"{item_id}: 모르는 제약 키 {key!r}"


@pytest.mark.parametrize("item_id", sorted(_constrained_items()))
def test_item_text_states_its_constraint(item_id):
    """숨은 제약은 함정이다 — 문항이 제약을 말해야 한다.

    숫자 제약은 그 숫자가 문항 문장에 나와야 하고, json_only 는 JSON 을 요구해야 한다.
    """
    item = _constrained_items()[item_id]
    text, cons = item["text"], item["constraints"]
    for key in ("exact_lines", "max_lines", "max_chars_per_line", "max_chars"):
        if key in cons:
            assert str(cons[key]) in text, f"{item_id}: {key}={cons[key]} 가 문항 문장에 없다"
    if cons.get("json_only"):
        assert "JSON" in text.upper(), f"{item_id}: json_only 인데 문항이 JSON 을 요구하지 않는다"
    for needle in cons.get("must_exclude", []):
        assert needle in text, f"{item_id}: 금지어 {needle!r} 가 문항 문장에 안내되지 않았다"
