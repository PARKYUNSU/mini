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
# 여는 펜스의 언어 태그와 첫 코드 줄이 개행 없이 붙어 나오는 출력(```pythonimport re)을 복구한다.
# 파인튜닝 모델이 코드가 import 로 시작할 때 내는 결함으로, base 는 내지 않는다
# (docs/experiments/yunsur_v6/05_conclusion.md). 고치지 않으면 펜스 정규식이 언어 태그를
# "pythonimport" 로 읽어 매치에 실패하고 전체가 plain 으로 떨어져 ast.parse 가 깨진다.
_FENCE_TOKEN_RE = re.compile(r"(```[ \t]*)([A-Za-z0-9_+-]+)")
_FUSED_LANGS = ("python3", "python", "py3", "py")  # 긴 것부터 — python3 이 python 보다 먼저
_JSON_CODE_KEYS = ("code", "python", "script", "source")


def _strip_think(text: str) -> str:
    return _THINK_RE.sub("", text)


def _repair_fused_fence(text: str) -> tuple[str, int]:
    """(복구된 텍스트, 복구 횟수). 언어 태그와 첫 코드 줄 사이에 개행을 끼워 넣는다.

    언어 후보를 정규식 교대로 쓰면 ``\u0060\u0060\u0060python\n`` 에서 ``python`` 이 조건에 걸려 실패한 뒤
    백트래킹으로 ``py`` 가 매치돼 ``thon`` 을 코드로 잘라낸다. 그래서 토큰을 통째로 잡고
    접두어를 직접 검사한다.
    """
    count = 0

    def _rep(m: re.Match[str]) -> str:
        nonlocal count
        prefix, token = m.group(1), m.group(2)
        low = token.lower()
        if low in _FUSED_LANGS:
            return m.group(0)  # 정상 태그 — 없으면 python 이 py + thon 으로 다시 쪼개진다
        for lang in _FUSED_LANGS:
            if low.startswith(lang) and len(token) > len(lang):
                rest = token[len(lang) :]
                if rest[0].isalpha() or rest[0] == "_":
                    count += 1
                    return f"{prefix}{token[: len(lang)]}\n{rest}"
        return m.group(0)

    return _FENCE_TOKEN_RE.sub(_rep, text), count


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

    여는 펜스가 첫 코드 줄과 붙어 있으면 개행을 복구하고 how 에 ``+fused`` 를 붙인다
    (예: ``fence+fused``). 모델 결함을 가리지 않고 세기 위한 표시다.

    - 펜스가 여럿이면 ``ast.parse`` 되는 가장 긴 블록을 고른다 (설명용 짧은 블록 회피).
    - 닫는 펜스가 없으면 (출력 잘림) 여는 펜스 이후 전부를 코드로 본다.
    - 펜스 안/밖이 JSON ``{"code": ...}`` 이면 한 번 더 벗긴다.
    """
    if not text or not text.strip():
        return "", "empty"
    body = _strip_think(text).strip()
    body, fused = _repair_fused_fence(body)
    tag = "+fused" if fused else ""

    blocks = _FENCE_RE.findall(body)
    if blocks:
        cands = [(lang.lower(), c.strip()) for lang, c in blocks if c.strip()]
        py = [c for lang, c in cands if lang in _PY_LANGS]
        js = [c for lang, c in cands if lang == "json"]
        # JSON 펜스 안에 code 키
        for c in js + [c for _, c in cands]:
            inner = _from_json_wrapper(c)
            if inner is not None:
                return inner, "fence_json" + tag
        pool = py or [c for _, c in cands]
        parsable = [c for c in pool if _parses(c)]
        pick = max(parsable or pool, key=len)
        return pick, ("fence_multi" if len(cands) > 1 else "fence") + tag

    m = _OPEN_FENCE_RE.search(body)
    if m and m.group(1).lower() in _PY_LANGS | {"json"}:
        tail = m.group(2).strip()
        inner = _from_json_wrapper(tail)
        if inner is not None:
            return inner, "fence_json" + tag
        return tail, "fence_open" + tag

    inner = _from_json_wrapper(body)
    if inner is not None:
        return inner, "json"

    # 펜스 없이 "python\n..." 처럼 언어명만 앞에 붙는 경우
    first, _, rest = body.partition("\n")
    if first.strip().lower() in ("python", "py", "python3") and rest.strip():
        return rest.strip(), "plain"
    return body, "plain"
