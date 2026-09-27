"""LEARNING_RATE 오버라이드 계약 — lr 이 조용히 바뀌지 않는지.

`scripts/train_lora.py` 는 하이퍼파라미터를 HPARAMS 로 고정하고 CLI 로 열지 않는다
("데이터만 바꾼 효과"를 분리하기 위해). 유일한 예외가 lr 이며, lr 자체가 실험
변수인 라운드를 위한 것이다 ([docs/experiments/yunsur_v10/](../../docs/experiments/yunsur_v10/README.md)).

예외인 만큼 조건이 붙는다: 기본값은 그대로 2e-4 여야 하고(이전 라운드 재현이
깨지지 않게), 값이 바뀔 때는 반드시 기록이 남아야 한다(train_stats.json 의
`hparam_overrides`). 그 둘을 여기서 고정한다.

모듈 최상위 임포트는 argparse·json·os·sys·time·collections·pathlib 뿐이고
torch·unsloth 는 main() 안에서 임포트하므로, 이 테스트는 가볍다.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "scripts"))

from train_lora import HPARAMS, resolve_learning_rate  # noqa: E402

pytestmark = pytest.mark.unit

DEFAULT = HPARAMS["learning_rate"]


def test_default_stays_2e_4():
    """기본값이 바뀌면 v3~v9 재현이 깨진다."""
    assert DEFAULT == 2e-4


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_unset_uses_default_without_record(raw):
    lr, overrides = resolve_learning_rate(raw, DEFAULT)
    assert lr == DEFAULT
    assert overrides == {}


def test_override_is_applied_and_recorded():
    """v10 이 쓰는 값. 기록이 없으면 train_stats.json 에 남지 않는다."""
    lr, overrides = resolve_learning_rate("5e-5", DEFAULT)
    assert lr == 5e-5
    assert overrides == {"learning_rate": {"default": 2e-4, "used": 5e-5}}


def test_same_as_default_is_not_an_override():
    lr, overrides = resolve_learning_rate("2e-4", DEFAULT)
    assert lr == DEFAULT
    assert overrides == {}, "기본값과 같으면 오버라이드로 기록하지 않는다"


@pytest.mark.parametrize("raw", ["abc", "5e-5x", "1,5e-5"])
def test_unparsable_stops_the_run(raw):
    """학습을 8분 돌린 뒤가 아니라 시작 전에 죽어야 한다."""
    with pytest.raises(SystemExit):
        resolve_learning_rate(raw, DEFAULT)


@pytest.mark.parametrize("raw", ["0", "-5e-5", "1", "200"])
def test_out_of_range_stops_the_run(raw):
    """0.2 를 5e-5 로 착각해 넣는 식의 오타를 막는다."""
    with pytest.raises(SystemExit):
        resolve_learning_rate(raw, DEFAULT)
