import json

import scripts.weekly_report as W


def test_row_counts_body_citations_only(tmp_path, monkeypatch):
    res = tmp_path / "res"
    res.mkdir()
    gold = tmp_path / "gold.jsonl"
    gold.write_text("\n".join(json.dumps(g) for g in [
        {"id": "a", "relevant_papers": ["2401.00001"]},
        {"id": "b", "relevant_papers": ["2401.00002"]},
        {"id": "c", "relevant_papers": []},
    ]), encoding="utf-8")
    rows = [
        {"id": "a", "ok": True, "answer": "본론 [2401.00001v1] · [2401.09999]", "doc_ids": ["2401.00001"], "elapsed": 50,
         "stages": [["router", 8.0], ["answer", 30.0]], "error": ""},
        # 정답이 외부 목록에만 있으면 답 정답 인용이 아니다
        {"id": "b", "ok": False, "answer": "제공된 문서에는 질문이 찾는 연구가 없습니다.\n📎 외부\n• X [2401.00002]",
         "doc_ids": [], "elapsed": 70, "stages": [["router", 10.0]], "error": ""},
        {"id": "c", "ok": False, "answer": "답", "doc_ids": [], "elapsed": 60, "stages": [], "error": "Timeout"},
    ]
    (res / "weekly_x.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    monkeypatch.setattr(W, "RES", res)
    monkeypatch.setattr(W, "GOLD", gold)
    cells = [c.strip() for c in W.row("weekly_x").strip("|").split("|")]
    # 날짜 · 커밋 · 문항 · 검색 정답 · 답 정답 인용 · '없음' · 컨텍스트 밖 · 시간 · 단계 · 오류
    assert cells[0] == "x" and cells[2] == "3"
    assert cells[3] == "1/2" and cells[4] == "1/2"
    assert cells[5] == "1" and cells[6] == "1"  # 2401.09999 는 컨텍스트 밖
    assert cells[7] == "60.0s" and cells[8].startswith("9.0 · ") and cells[9] == "1"
    assert W.HEADER.splitlines()[0].count("|") == W.row("weekly_x").count("|")
