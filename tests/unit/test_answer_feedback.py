"""답변 👍/👎 피드백: 버튼 데이터 왕복, JSONL 기록, 꺼짐 스위치."""

import json

from apps.telegram_bot import answer_feedback as fb


def test_markup_roundtrip():
    kb = fb.markup(42)
    datas = [b.callback_data for b in kb.keyboard[0]]
    assert datas == ["fb:42:up", "fb:42:down"]
    assert [fb.parse(d) for d in datas] == [(42, "up"), (42, "down")]
    chosen = [b.text for b in fb.markup(42, chosen="down").keyboard[0]]
    assert chosen == ["👍", "✅ 👎"]


def test_parse_rejects_other_callbacks():
    for d in (None, "", "fb:x:up", "fb:1:meh", "other:1:up", "fb:1"):
        assert fb.parse(d) is None


def test_record_appends_jsonl(monkeypatch, tmp_path):
    p = tmp_path / "fb.jsonl"
    monkeypatch.setenv("BOT_FEEDBACK_LOG", str(p))
    job = {"user_text": "LightKV 랑 CommVQ 비교", "result_text": "[2605.00789v2] 와 2606.09076 은 …",
           "job_kind": "graph", "created_at": 1.0, "updated_at": 2.0}
    fb.record(job, 7, "up", "123")
    fb.record(None, 8, "down", "123")  # 잡이 지워졌어도 평가는 남긴다
    rows = [json.loads(l) for l in p.read_text().splitlines()]
    assert rows[0]["question"] == "LightKV 랑 CommVQ 비교" and rows[0]["rating"] == "up"
    assert rows[0]["answer_papers"] == ["2605.00789", "2606.09076"]
    assert rows[1]["job_id"] == 8 and rows[1]["question"] == ""


def test_enabled_switch(monkeypatch):
    monkeypatch.delenv("BOT_FEEDBACK_BUTTONS", raising=False)
    assert fb.enabled()
    monkeypatch.setenv("BOT_FEEDBACK_BUTTONS", "0")
    assert not fb.enabled()
