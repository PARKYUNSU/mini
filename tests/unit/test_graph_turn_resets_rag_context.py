"""새 그래프 턴이 rag_context 를 비우는지 지킨다.

그래프는 채팅마다 같은 thread_id 의 체크포인트를 이어 쓴다. 라우터 1단계 하드룰은
rag_context 를 덮어쓰지 않고, DirectAnswer 는 state 의 rag_context 가 있으면 검색하지
않고 재사용한다. 2026-10-08 운영 확인에서 서로 다른 두 논문 질문이 이전 턴의 같은
컨텍스트(2603자)로 답변됐다. 초기 상태에서 비워야 한다.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
ENTRY_POINTS = [
    _ROOT / "core" / "graph" / "agent_worker_runner.py",
    _ROOT / "apps" / "scheduler" / "agent_scheduled_runner.py",
]


def _init_state_dicts(path: Path) -> list[dict]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(node.value, ast.Dict):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == "init_state" for t in targets):
                out.append({k.value: v for k, v in zip(node.value.keys, node.value.values) if isinstance(k, ast.Constant)})
    return out


@pytest.mark.parametrize("path", ENTRY_POINTS, ids=lambda p: p.name)
def test_init_state_clears_rag_context(path):
    dicts = _init_state_dicts(path)
    assert dicts, f"{path.name}: init_state 를 찾지 못함"
    for d in dicts:
        assert "rag_context" in d, f"{path.name}: init_state 에 rag_context 가 없다"
        v = d["rag_context"]
        assert isinstance(v, ast.Constant) and v.value == ""
