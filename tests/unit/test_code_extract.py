"""core.llm.code_extract — LLM 출력 → 파이썬 코드 추출 (로컬 실패율 평가에서 나온 실제 케이스 포함)."""

import ast

import pytest

from core.llm.code_extract import extract_python_code

pytestmark = pytest.mark.unit


def _parses(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def test_plain_code_passthrough():
    code, how = extract_python_code("x = 1\nprint(x)")
    assert how == "plain" and code == "x = 1\nprint(x)"


@pytest.mark.parametrize("lang", ["python", "py", "Python", "python3", ""])
def test_fence_variants(lang):
    code, how = extract_python_code(f"설명입니다.\n```{lang}\nprint('hi')\n```\n끝.")
    assert how == "fence" and code == "print('hi')"


def test_json_code_wrapper_inside_json_fence():
    # eval coding_05 trial 1 실제 출력 형태
    raw = '```json\n{\n    "code": "d = {\'a\': 1, \'b\': 2}\\nprint(sum(d.values()))"\n}\n```'
    code, how = extract_python_code(raw)
    assert how == "fence_json"
    assert code == "d = {'a': 1, 'b': 2}\nprint(sum(d.values()))"
    assert _parses(code)


def test_json_code_wrapper_bare():
    code, how = extract_python_code('{"code": "print(1)"}')
    assert how == "json" and code == "print(1)"


def test_multiple_fences_prefers_longest_parsable():
    raw = "예:\n```python\nx =\n```\n실제:\n```python\nfor i in range(3):\n    print(i)\n```"
    code, how = extract_python_code(raw)
    assert how == "fence_multi" and code.startswith("for i in range(3)") and _parses(code)


def test_open_fence_truncated_output():
    raw = "```python\nprint('a')\nprint('b')"
    code, how = extract_python_code(raw)
    assert how == "fence_open" and code == "print('a')\nprint('b')"


def test_think_block_stripped():
    raw = "<think>계획을 세운다</think>\n```python\nprint(2)\n```"
    code, how = extract_python_code(raw)
    assert code == "print(2)" and how == "fence"


def test_language_name_line_without_fence():
    code, how = extract_python_code("python\nprint(3)")
    assert how == "plain" and code == "print(3)"


def test_empty():
    assert extract_python_code("   ") == ("", "empty")


def test_fused_fence_is_repaired():
    """```python 과 첫 코드 줄이 붙어 나오는 출력을 복구한다.

    파인튜닝 모델이 코드가 import 로 시작할 때 내는 결함 (base 는 내지 않는다).
    docs/experiments/yunsur_v6/05_conclusion.md — 고치기 전에는 펜스 정규식이 언어 태그를
    "pythonimport" 로 읽어 매치에 실패하고 전체가 plain 으로 떨어져 ast.parse 가 깨졌다.
    """
    code, how = extract_python_code("```pythonimport re\nd = {}\nprint(d)\n```")
    assert how == "fence+fused"
    assert code == "import re\nd = {}\nprint(d)"
    assert _parses(code)


def test_fused_fence_open_and_variants():
    code, how = extract_python_code("```pythonimport ast, json\ns = 'x'\nprint(s)")
    assert how == "fence_open+fused" and _parses(code)

    code, how = extract_python_code("```py3print(1)\n```")
    assert how == "fence+fused" and code == "print(1)"

    code, how = extract_python_code("```python3import os\nprint(1)\n```")
    assert how == "fence+fused" and code == "import os\nprint(1)"


def test_normal_language_tags_are_not_split():
    """python 이 py + thon 으로 쪼개지면 안 된다 (정확 일치 가드).

    언어 후보를 정규식 교대로 쓰면 python 이 조건에 걸려 실패한 뒤 백트래킹으로 py 가
    매치돼 thon 을 코드로 잘라낸다 — 실제로 한 번 그렇게 깨뜨렸다.
    """
    for lang in ("python", "py", "Python", "python3", "py3"):
        code, how = extract_python_code(f"```{lang}\nprint('hi')\n```")
        assert how == "fence", f"{lang}: how={how}"
        assert code == "print('hi')", f"{lang}: code={code!r}"
