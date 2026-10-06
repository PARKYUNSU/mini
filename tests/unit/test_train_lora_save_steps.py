"""``SAVE_STEPS`` 중간 체크포인트 배선이 **학습을 바꾸지 않게** 지킨다.

왜 있나: 기전 라운드(docs/experiments/checkpoint_1004/)는 "행동이 몇 스텝에서
꺾이나" 를 보려고 중간 어댑터를 남긴다. 그런데 이 스위치가 하이퍼파라미터를 건드리면
v3~v11 과 비교할 수 없게 된다. 그래서 두 가지를 못 박는다:

  (1) 기본값은 꺼짐 — 안 주면 산출물이 이전 라운드와 같다.
  (2) 검증을 통과하지 못한 값은 **조용히 무시하지 않고 중단**한다. 파드는 돈을 쓰며
      돌고 자동 종료되므로, 잘못된 값으로 8분을 태우고 체크포인트가 없는 것을
      나중에 발견하면 다시 학습해야 한다.

소스를 ast 로 읽어 함수만 떼어 돌린다 (이 스크립트는 unsloth·torch 를 끌고 온다).
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_SRC = (Path(__file__).resolve().parents[2] / "scripts" / "train_lora.py").read_text(encoding="utf-8")
_TREE = ast.parse(_SRC)


def _load(name: str):
    fn = next(
        (n for n in _TREE.body if isinstance(n, ast.FunctionDef) and n.name == name), None
    )
    assert fn is not None, f"{name} 이 사라졌다"
    ns: dict = {}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), "<train_lora>", "exec"), ns)
    return ns[name]


resolve_save_steps = _load("resolve_save_steps")


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_default_is_off(raw) -> None:
    """안 주면 None — 중간 저장 없이 이전 라운드와 같은 산출물."""
    assert resolve_save_steps(raw) is None


@pytest.mark.parametrize("raw,want", [("23", 23), (" 46 ", 46), ("1", 1), ("138", 138)])
def test_accepts_valid_intervals(raw, want) -> None:
    assert resolve_save_steps(raw) == want


@pytest.mark.parametrize("raw", ["abc", "23.5", "", None])
def test_rejects_unparsable_without_crashing_on_empty(raw) -> None:
    """빈 값은 '꺼짐', 파싱 불가는 중단 — 둘을 섞지 않는다."""
    if raw in ("", None):
        assert resolve_save_steps(raw) is None
    else:
        with pytest.raises(SystemExit):
            resolve_save_steps(raw)


@pytest.mark.parametrize("raw", ["0", "-1", "-23"])
def test_rejects_non_positive(raw) -> None:
    with pytest.raises(SystemExit):
        resolve_save_steps(raw)


def test_rejects_interval_larger_than_total() -> None:
    """전체 스텝보다 크면 중간 저장이 하나도 안 생긴다 — 조용히 넘기지 않는다."""
    with pytest.raises(SystemExit):
        resolve_save_steps("200")
    # 경계: 전체와 같으면 허용 (마지막 스텝에 한 번 저장)
    assert resolve_save_steps("138", total_hint=138) == 138


def test_save_steps_is_recorded_in_train_stats() -> None:
    """산출물만 보고 '이 어댑터가 어떤 간격으로 저장됐나' 를 알 수 있어야 한다."""
    assert '"save_steps": save_steps,' in _SRC, "train_stats.json 에 save_steps 기록이 사라졌다"


def test_save_steps_does_not_touch_hparams() -> None:
    """HPARAMS 에 save_steps 가 들어가면 안 된다 — 학습 설정이 아니다."""
    hp = next(
        n for n in _TREE.body
        if isinstance(n, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "HPARAMS" for t in n.targets
        )
    )
    keys = {k.value for k in hp.value.keys if isinstance(k, ast.Constant)}
    assert "save_steps" not in keys and "save_strategy" not in keys


resolve_save_steps_max = _load("resolve_save_steps_max")


@pytest.mark.parametrize("raw", [None, "", "  "])
def test_save_steps_max_default_is_off(raw) -> None:
    """안 주면 None — 체크포인트를 전부 올린다."""
    assert resolve_save_steps_max(raw) is None


@pytest.mark.parametrize("raw,want", [("24", 24), (" 3 ", 3), ("138", 138), ("500", 500)])
def test_save_steps_max_accepts_positive(raw, want) -> None:
    """전체 스텝보다 커도 받는다 — '전부 올려라' 와 같은 뜻이고 해로울 게 없다."""
    assert resolve_save_steps_max(raw) == want


@pytest.mark.parametrize("raw", ["0", "-1", "abc", "24.5"])
def test_save_steps_max_rejects_bad(raw) -> None:
    with pytest.raises(SystemExit):
        resolve_save_steps_max(raw)


def test_cap_filters_upload_not_training() -> None:
    """상한은 **업로드**만 건다 — 학습·디스크 저장은 건드리지 않는다.

    sft_kwargs(= 학습 설정)에 save_steps_max 가 들어가면 안 된다.
    """
    assert "save_steps_max" in _SRC
    # 학습 설정 블록에서 쓰이지 않는지 본다
    i = _SRC.index('sft_kwargs["save_steps"] = save_steps')
    j = _SRC.index("trainer = SFTTrainer")
    assert "save_steps_max" not in _SRC[i:j], "save_steps_max 가 학습 설정에 새어들었다"
    # 업로드 선별 자리에서는 쓰인다
    assert "step > save_steps_max" in _SRC
