import json

from core.graph import rag_trace


def test_trace_writes_one_line(tmp_path, monkeypatch):
    log = tmp_path / "t.jsonl"
    monkeypatch.setenv("RAG_TRACE_LOG", str(log))
    rag_trace.start("c1", job_id=7, question="q")
    rag_trace.mark("c1", "query", query="rag eval")
    rag_trace.mark("c1", "answer", raw="답")
    t = rag_trace.finish("c1")
    rows = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1 and rows[0]["job_id"] == 7 and rows[0]["question"] == "q"
    assert [x["stage"] for x in rows[0]["stages"]] == ["query", "answer"]
    assert t["total_s"] >= 0 and "_t0" not in rows[0]


def test_trace_noop_without_start_or_stages(tmp_path, monkeypatch):
    log = tmp_path / "t.jsonl"
    monkeypatch.setenv("RAG_TRACE_LOG", str(log))
    rag_trace.mark("nobody", "query")  # start 없으면 무시
    assert rag_trace.finish("nobody") == {}
    rag_trace.start("c2")
    rag_trace.finish("c2")  # 단계 없으면(RAG 경로 아님) 쓰지 않음
    monkeypatch.setenv("RAG_TRACE", "0")
    rag_trace.start("c3")
    rag_trace.mark("c3", "query")
    assert rag_trace.finish("c3") == {}
    assert not log.exists()


def test_paper_ids_block_heads_only():
    ctx = "[문서 1]\n[Distance: 0.2]\n[2601.07422v1] Two Pathways\n본문 [2401.00001] 인용\n\n[2411.09689v4] SHINE\n[2601.07422v2] 같은 논문"
    assert rag_trace.paper_ids(ctx) == ["2601.07422", "2411.09689"]
