"""조건부 승격(RAG_COND_PROMOTE) 규칙 — 27B 안 부르는 부분만."""
from core.llm import doc_judge as J


def test_promote_only_n_with_fs_p_and_specific_condition():
    labels = {1: "N", 2: "N", 3: "D", 4: "N"}
    conds = [{"값": "한국어", "다룬 논문": [1, 3]}, {"값": "보고서", "다룬 논문": [2, 4]}]
    fs = {1: "P", 2: "P", 3: "P", 4: "D"}
    # 1: 한국어 다룸 → P · 2: 일반 명사 '보고서' 만 다룸 → 그대로 · 3: D 안 낮춤 · 4: fs D 는 안 올림
    assert J.promote_labels(labels, conds, fs) == {1: "P", 2: "N", 3: "D", 4: "N"}


def test_skip_without_specific_condition_or_n(monkeypatch):
    called = []
    monkeypatch.setattr(J, "judge_task", lambda *a, **k: called.append(1) or {1: "인접"})
    assert J.promote_by_conditions("q", "ctx", {1: "N"}, [{"값": "보고서", "다룬 논문": [1]}]) == ({1: "N"}, [])
    assert J.promote_by_conditions("q", "ctx", {1: "P"}, [{"값": "한국어", "다룬 논문": [1]}]) == ({1: "P"}, [])
    assert J.promote_by_conditions("q", "ctx", {1: "N"}, None) == ({1: "N"}, [])
    assert not called


def test_promote_calls_fs_prompt(monkeypatch):
    seen = {}
    monkeypatch.setattr(J, "judge_task", lambda q, c, prompt=None: seen.setdefault("p", prompt) and {1: "인접", 2: "아님"})
    got = J.promote_by_conditions("q", "ctx", {1: "N", 2: "N"}, [{"값": "한국어", "다룬 논문": [1, 2]}])
    assert got == ({1: "P", 2: "N"}, [1])
    assert seen["p"] is J.TASK_FS_PROMPT


def test_flag_default_off(monkeypatch):
    monkeypatch.delenv("RAG_COND_PROMOTE", raising=False)
    assert not J.cond_promote_active()
