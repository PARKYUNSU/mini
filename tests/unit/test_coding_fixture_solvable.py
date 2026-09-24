"""평가 문항이 실제로 풀리는지 지킨다 — 참조답안이 판정기 조건을 통과해야 한다.

`_coding_ok` 는 추출한 코드를 임시 디렉터리에서 8초 제한으로 **실제 실행**한다.
그래서 문항은 자기완결이어야 한다 (파일·네트워크·input() 금지). 풀 수 없는 문항이
섞이면 모든 모델이 그 문항에서 실패해 실패율이 문항 결함을 반영하게 된다 —
docs/experiments/yunsur_v6/README.md 에서 coding_10 을 두고 실제로 의심했던 문제다.

채점에는 참조답안을 쓰지 않는다. 문항의 풀림 가능성만 확인한다.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
FIXTURE = _ROOT / "tests" / "fixtures" / "local_llm_failure_eval.jsonl"
SOLUTIONS = _ROOT / "tests" / "fixtures" / "coding_reference_solutions.json"
TIERS = ("쉬움", "보통", "어려움")


def _fixture_coding_ids() -> list[str]:
    ids = []
    for line in FIXTURE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            if r["slot"] == "coding":
                ids.append(r["id"])
    return ids


def _solutions() -> dict[str, dict]:
    return json.loads(SOLUTIONS.read_text(encoding="utf-8"))["items"]


def test_every_coding_question_has_a_reference_solution():
    missing = sorted(set(_fixture_coding_ids()) - set(_solutions()))
    assert not missing, f"참조답안 없는 문항: {missing}"


def test_reference_solutions_all_run():
    """ast.parse + 8초 실행. 판정기(_coding_ok)와 같은 조건이다."""
    failures = []
    for cid, item in sorted(_solutions().items()):
        code = item["solution"]
        try:
            ast.parse(code)
        except SyntaxError as e:
            failures.append(f"{cid} syntax: {e.msg}")
            continue
        fd, path = tempfile.mkstemp(suffix="_eval.py")
        os.close(fd)
        try:
            Path(path).write_text(code, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, path], capture_output=True, text=True,
                timeout=8, cwd=tempfile.gettempdir(),
            )
            if proc.returncode != 0:
                failures.append(f"{cid} runtime: {(proc.stderr or '').strip()[-120:]}")
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass
    assert not failures, "풀리지 않는 문항:\n" + "\n".join(failures)


def test_tiers_are_declared_and_balanced():
    """난이도가 선언돼 있고, 변별력 있는 구간(보통·어려움)이 충분해야 한다.

    base 는 쉬움 구간을 전부 통과하므로 쉬움 문항은 모델 간 불일치를 만들지 못한다
    (docs/experiments/protocol.md).
    """
    items = _solutions()
    for cid in _fixture_coding_ids():
        assert items[cid]["tier"] in TIERS, f"{cid}: tier={items[cid].get('tier')!r}"
    counts = {t: sum(1 for cid in _fixture_coding_ids() if items[cid]["tier"] == t) for t in TIERS}
    assert counts["보통"] + counts["어려움"] >= 20, counts
