"""LLM 출력에서 실행 가능한 파이썬 코드만 추출.

로컬 9B/Groq 모두 형식이 흔들린다 — ```python 펜스, ```py/```Python 변형, 펜스 없는 순수 코드,
``{"code": "..."}`` JSON 래핑, ```json 안에 다시 code 키, <think> 블록 잔여 등.
Executor 노드와 로컬 실패율 평가 스크립트가 같은 함수를 쓴다.
"""

from __future__ import annotations

import ast
import json
import re

_THINK_RE = re.compile(r"<(?:redacted_)?think(?:ing)?>[\s\S]*?</(?:redacted_)?think(?:ing)?>", re.IGNORECASE)
_FENCE_RE = re.compile(r"```[ \t]*([A-Za-z0-9_+-]*)[ \t]*\r?\n([\s\S]*?)```")
_OPEN_FENCE_RE = re.compile(r"```[ \t]*([A-Za-z0-9_+-]*)[ \t]*\r?\n([\s\S]*)$")
_PY_LANGS = {"", "python", "py", "python3", "py3"}
_JSON_CODE_KEYS = ("code", "python", "script", "source")


def _strip_think(text: str) -> str:
    return _THINK_RE.sub("", text)


def _parses(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def _from_json_wrapper(text: str) -> str | None:
    """``{"code": "..."}`` 형태면 코드 문자열만 꺼낸다 (실패 시 None)."""
    s = text.strip()
    if not s.startswith("{"):
        return None
    try:
        obj = json.loads(s)
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    for k in _JSON_CODE_KEYS:
        v = obj.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def extract_python_code(text: str) -> tuple[str, str]:
    """(code, how) 반환. how: plain | fence | fence_multi | fence_open | json | fence_json | empty.

    - 펜스가 여럿이면 ``ast.parse`` 되는 가장 긴 블록을 고른다 (설명용 짧은 블록 회피).
    - 닫는 펜스가 없으면 (출력 잘림) 여는 펜스 이후 전부를 코드로 본다.
    - 펜스 안/밖이 JSON ``{"code": ...}`` 이면 한 번 더 벗긴다.
    """
    if not text or not text.strip():
        return "", "empty"
    body = _strip_think(text).strip()

    blocks = _FENCE_RE.findall(body)
    if blocks:
        cands = [(lang.lower(), c.strip()) for lang, c in blocks if c.strip()]
        py = [c for lang, c in cands if lang in _PY_LANGS]
        js = [c for lang, c in cands if lang == "json"]
        # JSON 펜스 안에 code 키
        for c in js + [c for _, c in cands]:
            inner = _from_json_wrapper(c)
            if inner is not None:
                return inner, "fence_json"
        pool = py or [c for _, c in cands]
        parsable = [c for c in pool if _parses(c)]
        pick = max(parsable or pool, key=len)
        return pick, ("fence_multi" if len(cands) > 1 else "fence")

    m = _OPEN_FENCE_RE.search(body)
    if m and m.group(1).lower() in _PY_LANGS | {"json"}:
        tail = m.group(2).strip()
        inner = _from_json_wrapper(tail)
        if inner is not None:
            return inner, "fence_json"
        return tail, "fence_open"

    inner = _from_json_wrapper(body)
    if inner is not None:
        return inner, "json"

    # 펜스 없이 "python\n..." 처럼 언어명만 앞에 붙는 경우
    first, _, rest = body.partition("\n")
    if first.strip().lower() in ("python", "py", "python3") and rest.strip():
        return rest.strip(), "plain"
    return body, "plain"
