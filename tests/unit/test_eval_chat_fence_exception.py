"""잡담 펜스 판정 예외 (yunsur_v5 사전 선언, docs/experiments/yunsur_v5/README.md §3).

요청이 템플릿·표·양식·서식·마크다운을 요구했으면 답변의 코드 펜스는 합리적이므로
``code_fence_in_chat`` 으로 세지 않는다. 생성 필터(gen_v5_dataset)와 평가 판정기가
같은 패턴을 써야 하므로 동일성까지 검사한다 — 갈라지면 4모델 비교가 공정하지 않다.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

from scripts.eval_local_llm_failure import TEMPLATE_REQUEST_RE, _quality_check  # noqa: E402

_FENCED = "회의록은 이렇게 쓰시면 됩니다.\n\n```markdown\n# 회의록\n- 참석자:\n```"


def _load_generator():
    spec = importlib.util.spec_from_file_location("_gen_v5", _ROOT / "scripts" / "gen_v5_dataset.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_fence_is_failure_without_template_request():
    ok, kind = _quality_check("chat", _FENCED, english_max=0.45, request="오늘 기분 어때?")
    assert (ok, kind) == (False, "code_fence_in_chat")


def test_fence_allowed_when_request_asks_for_template():
    for request in (
        "회의록 마크다운 템플릿 만들어줘",
        "주간 보고 양식 좀 잡아줘",
        "이걸 표로 정리해줘",
        "지출 내역을 표 만들어줘",
        "이력서 서식 추천해줘",
        "Markdown 으로 정리해줘",
    ):
        ok, kind = _quality_check("chat", _FENCED, english_max=0.45, request=request)
        assert (ok, kind) == (True, ""), request


def test_exception_is_chat_only():
    """rag·planner·coding 은 펜스 검사 자체가 없다 — 예외가 다른 슬롯을 건드리지 않는다."""
    for slot in ("rag", "planner", "coding"):
        ok, _ = _quality_check(slot, _FENCED, english_max=1.0, request="오늘 기분 어때?")
        assert ok is True, slot


def test_other_quality_failures_survive_the_exception():
    """템플릿 요청이어도 think 유출·반복은 그대로 실패여야 한다."""
    ok, kind = _quality_check("chat", "<think>음</think>\n```markdown\n#표\n```", english_max=0.45, request="표로 정리해줘")
    assert (ok, kind) == (False, "think_leak")

    repeated = "\n".join(["같은 줄이 계속 반복되고 있습니다 표 양식입니다"] * 3)
    ok, kind = _quality_check("chat", repeated, english_max=0.45, request="표로 정리해줘")
    assert (ok, kind) == (False, "repetition")


def test_pattern_matches_generator():
    """생성 필터와 평가 판정기가 같은 예외를 써야 공정하다."""
    gen = _load_generator()
    assert TEMPLATE_REQUEST_RE.pattern == gen.TEMPLATE_REQUEST_RE.pattern
    assert TEMPLATE_REQUEST_RE.flags == gen.TEMPLATE_REQUEST_RE.flags
