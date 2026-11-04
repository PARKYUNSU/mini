"""찾은 문서로 빈 칸 채우기의 발동 조건 · 안전장치 (docs/experiments/query_reform_1105)."""

import core.llm.query_reform as QR
from core.llm.citation_fix import RAG_HIT_SEP


def _ctx(*pids):
    return RAG_HIT_SEP.join(f"[Distance: 0.3]\n[{p}v1] 제목 {p}\n[초록] 내용 {p}." for p in pids)


def _setup(monkeypatch, *, raw="new search terms for papers", status="2→1", keep_first=True):
    calls = {"rewrite": 0, "search": [], "filter": []}

    def rewrite(q, query, blocks):
        calls["rewrite"] += 1
        return raw

    def filt(q, ctx, model):
        calls["filter"].append(ctx)
        blocks = ctx.split(RAG_HIT_SEP)
        return (blocks[0] if keep_first and "→" in status else ctx), status

    monkeypatch.setattr(QR, "_rewrite", rewrite)
    monkeypatch.setattr(QR, "filter_relevant", filt)
    return calls


def test_parse_query():
    assert QR.parse_query("late chunking contextual embedding retrieval", "chunking") == "late chunking contextual embedding retrieval"
    assert QR.parse_query("새 검색어:\nQuery: late-chunking, context", "x") == "query late-chunking context"
    assert QR.parse_query("한국어만 있는 답", "x") is None
    assert QR.parse_query("two words", "x") is None
    assert QR.parse_query("Late, Chunking retrieval", "retrieval, late chunking") is None  # 같은 단어
    assert len(QR.parse_query(" ".join(f"w{i}" for i in range(20)), "x").split()) == 12


def test_no_trigger(monkeypatch):
    calls = _setup(monkeypatch)
    search = lambda q: calls["search"].append(q) or ""
    kw = {"search": search, "model": "m"}
    full = _ctx("2401.00001", "2401.00002", "2401.00003", "2401.00004", "2401.00005")
    assert QR.fill_slots("연구 있어?", "q", full, full, **kw) == (full, {"on": False})  # 5편이면 그대로
    assert QR.fill_slots("연구 있어?", "q", "관련 문서 없음", "관련 문서 없음", **kw)[1] == {"on": False}  # 0편
    one = _ctx("2401.00001")
    assert QR.fill_slots("정확도가 몇 % 올랐어?", "q", one, one, **kw) == (one, {"on": False})  # 수치
    assert QR.fill_slots("A랑 B 차이 비교해줘", "q", one, one, **kw) == (one, {"on": False})  # 비교
    assert calls["rewrite"] == 0 and not calls["search"]


def test_fills_only_new_docs_after_kept(monkeypatch):
    calls = _setup(monkeypatch)
    pool, kept = _ctx("2401.00001", "2401.00002"), _ctx("2401.00001")
    found = _ctx("2401.00002", "2401.00003", "2401.00004")  # 첫 검색에 있던 00002 는 다시 안 본다
    out, info = QR.fill_slots("연구 있어?", "q", pool, kept, search=lambda q: found, model="m")
    assert "2401.00002" not in calls["filter"][0] and "2401.00003" in calls["filter"][0]
    assert out == RAG_HIT_SEP.join([kept, _ctx("2401.00003")])
    assert info["added"] == ["2401.00003"] and info["new"] == 2 and info["query"] == "new search terms for papers"
    assert set(info["s"]) == {"rewrite", "search", "filter"}


def test_filter_outcomes_add_nothing(monkeypatch):
    pool, kept = _ctx("2401.00001", "2401.00002"), _ctx("2401.00001")
    found = _ctx("2401.00003", "2401.00004")
    for status in ("없음", "못 읽음", "호출 실패", "대상 아님"):
        _setup(monkeypatch, status=status)
        out, info = QR.fill_slots("연구 있어?", "q", pool, kept, search=lambda q: found, model="m")
        assert out == kept and info["added"] == [] and info["filter"] == status


def test_rewrite_failures_leave_context(monkeypatch):
    pool, kept = _ctx("2401.00001", "2401.00002"), _ctx("2401.00001")
    calls = _setup(monkeypatch, raw="한국어만")
    search = lambda q: calls["search"].append(q) or ""
    out, info = QR.fill_slots("연구 있어?", "q", pool, kept, search=search, model="m")
    assert out == kept and info["filter"] == "검색어 없음" and not calls["search"]

    def boom(*a):
        raise RuntimeError("x")

    monkeypatch.setattr(QR, "_rewrite", boom)
    out, info = QR.fill_slots("연구 있어?", "q", pool, kept, search=search, model="m")
    assert out == kept and info["filter"] == "호출 실패"


def test_prompt_has_papers_and_no_domain_terms(monkeypatch):
    block = "[Distance: 0.3]\n[2401.00001v1] 제목 하나\n[초록] We propose a method. It improves recall by 10%."
    assert "제목 하나" in QR._paper(1, block) and "[초록]" not in QR._paper(1, block)
    assert "본문" in QR._paper(1, "[2401.00001v1] 제목\n본문 내용")
    assert "RAG" not in QR.PROMPT  # 프롬프트의 용어가 검색어로 새어 든다 (query_extract_1021)
