#!/usr/bin/env python3
"""
라우팅 회귀 테스트 - Golden Cases
검색 의도 분류 및 Tavily 오탐 방지 검증
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _load_yaml(path: Path) -> list:
    """간단 YAML 파싱 (PyYAML 의존 없음)"""
    cases = []
    cur = {}
    for line in open(path, encoding="utf-8"):
        line = line.rstrip()
        if line.startswith("- input:"):
            if cur:
                cases.append(cur)
            val = line.split(":", 1)[1].strip().strip('"\'')
            cur = {"input": val}
        elif line.startswith("  expected_search_intent:"):
            cur["expected_search_intent"] = line.split(":", 1)[1].strip()
        elif line.startswith("  expected_tool:"):
            v = line.split(":", 1)[1].strip().split("#")[0].strip()
            cur["expected_tool"] = None if v == "null" else v
    if cur:
        cases.append(cur)
    return cases


def test_search_intent():
    from agent_bot import _get_search_intent

    cases_path = Path(__file__).parent / "golden_routing_cases.yaml"
    cases = _load_yaml(cases_path)
    assert cases, "golden_routing_cases.yaml 비어 있음"

    for i, c in enumerate(cases):
        inp = c.get("input", "")
        expected = c.get("expected_search_intent")
        if expected is None:
            continue
        got = _get_search_intent(inp, inp.lower())
        assert got == expected, f"[{i+1}] {inp!r} → expected {expected}, got {got}"
    print(f"  OK: search_intent {len(cases)} cases")


def test_whitelisted_tool():
    from agent_bot import _match_whitelisted_tool

    cases_path = Path(__file__).parent / "golden_routing_cases.yaml"
    cases = _load_yaml(cases_path)

    for i, c in enumerate(cases):
        inp = c.get("input", "")
        expected = c.get("expected_tool")
        got = _match_whitelisted_tool(inp, inp.lower())
        exp_val = None if expected is None or expected == "null" else expected
        assert got == exp_val, f"[{i+1}] {inp!r} → expected tool {exp_val}, got {got}"
    print(f"  OK: whitelisted_tool {len(cases)} cases")


if __name__ == "__main__":
    print("Golden routing tests...")
    test_search_intent()
    test_whitelisted_tool()
    print("Done.")
