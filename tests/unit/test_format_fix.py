"""format_fix_1117: 용어 규칙 · 섞인 글자 거르기 · 한자 지우기 · '없음' 문장."""
from core.llm import format_fix as F
from core.llm import item_rewrite


def test_term_rule_off_on(monkeypatch):
    monkeypatch.delenv("RAG_FORMAT_FIX", raising=False)
    assert F.term_rule() == ""
    monkeypatch.setenv("RAG_FORMAT_FIX", "1")
    assert "poisoning" in F.term_rule()


def test_glued_latin():
    assert F._GLUED.search("데이터 포izoning 공격")
    assert not F._GLUED.search("LLM을 쓰는 RAG에서 poisoning 공격")


def test_check_item_rejects_glued(monkeypatch):
    monkeypatch.setenv("RAG_FORMAT_FIX", "1")
    src = "RAG poisoning attacks are analyzed."
    text = "이 연구는 RAG 시스템의 데이터 포izoning 공격을 분석하고 입력 검증 같은 완화 조치를 제시합니다. 실험은 여러 시스템에서 진행되었습니다."
    assert item_rewrite.check_item(text, "짧음", src) == "섞인 글자"


def test_strip_hanzi():
    out, n = F.strip_hanzi("세 가지 척도에서六点 벤치마크에 대해")
    assert n == 1 and "六" not in out and "척도에서" in out


def test_partial_wording():
    a = "서론\n제공된 문서에는 질문이 찾는 연구가 없습니다. 배경.\n본론\n1. <b>X</b> (관련 연구): 내용 [2401.00001v1]\n결론\n따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다."
    out, n = F.partial_wording(a)
    assert n == 2 and F.LEAD_NEW in out and F.CONCL_NEW in out
    assert F.partial_wording(a.replace("(관련 연구)", "")) == (a.replace("(관련 연구)", ""), 0)


def test_fix_terms():
    from core.llm.format_fix import fix_terms
    out, n = fix_terms("동적 차킹과 채킹이 청크링을, 인간 판판이 허할루시네이션을 CoT‑라울러로")
    assert out == "동적 청킹과 청킹이 청킹을, 인간 판정자가 환각을 CoT 근거 설명으로" and n == 6


def test_fix_item_titles():
    from core.llm.format_fix import fix_item_titles
    ctx = "[문서 2]\n[2406.12624v6] Judging the Judges: Evaluating Alignment\n[초록] x"
    a = ("서론\n질문.\n\n본론\n1. TabRAG TabRAG은 표를 파싱한다. [2511.06582]\n"
         "2. 가장 큰 모델들만 정렬이 높다. [2406.12624v6]\n3. LADFA (관련 연구) 이 연구는. [2601.10413]\n"
         "4. Metric Match: 이미 꼴. [2606.15029]\n\n결론\n결론 문장 1. 2. 그대로")
    out, n = fix_item_titles(a, ctx)
    assert n == 3
    assert "1. TabRAG: TabRAG은" in out and "2. Judging the Judges: 가장 큰" in out
    assert "3. LADFA (관련 연구): 이 연구는" in out and "4. Metric Match: 이미 꼴" in out
    assert out.endswith("결론\n결론 문장 1. 2. 그대로")


def test_fix_item_titles_shapes():
    from core.llm.format_fix import fix_item_titles
    ctx = "[2407.12023v1] CMMaTH: A Chinese benchmark\n[2604.01221v1] HippoCamp Bench"
    a = ("본론\n1. **MonkeyOCR v1.5** MonkeyOCR v1.5은 파싱. [2511.10390]\n2. [2407.12023v1] 데이터셋 도구. [2407.12023v1]\n"
         "3. (관련 연구) 또한 평가. [2604.01221v1]\n결론\n끝")
    out, n = fix_item_titles(a, ctx)
    assert n == 3
    assert "1. **MonkeyOCR v1.5**: MonkeyOCR v1.5은" in out
    assert "2. CMMaTH: 데이터셋 도구." in out and "3. HippoCamp Bench (관련 연구): 또한 평가." in out


def test_fix_item_titles_sentence_start():
    from core.llm.format_fix import fix_item_titles
    ctx = "[2406.19102v1] Statements: Universal Information Extraction\n[2511.06582v1] TabRAG: Improving Tabular QA"
    a = "본론\n1. T5 기반 모델은 82%다. [2406.19102v1]\n2. TabRAG TabRAG은 파싱. [2511.06582v1]\n결론\n끝"
    out, n = fix_item_titles(a, ctx)
    assert "1. Statements: T5 기반 모델은 82%다." in out and "2. TabRAG: TabRAG은 파싱." in out and n == 2


def test_fix_terms_rationale_variants():
    from core.llm.format_fix import fix_terms
    for w in ("CoT-라우널을", "CoT‑라테이션과", "CoT 라울러로"):
        out, n = fix_terms(w)
        assert out.startswith("CoT 근거 설명") and n == 1, out
    assert fix_terms("CoT 라벨을")[0] == "CoT 라벨을"  # 붙임표 없는 'CoT 라…' 는 알려진 음차만


def test_fix_terms_rationale_tail_and_particle():  # U5 — 저장 답에서 실제로 나온 꼴
    from core.llm.format_fix import fix_terms
    cases = {
        "CoT‑라벨링된 이유를 이용해": "CoT 근거 설명을 이용해",
        "CoT‑라벨링된 합리화를 이용한": "CoT 근거 설명을 이용한",
        "CoT‑라울린을 활용한": "CoT 근거 설명을 활용한",
        "CoT-라울에 기반한": "CoT 근거 설명에 기반한",
        "CoT‑라울러를 이용한": "CoT 근거 설명을 이용한",
        "CoT‑라울러 기반": "CoT 근거 설명 기반",
        "CoT‑라우널이 있다": "CoT 근거 설명이 있다",
    }
    for src, want in cases.items():
        out, n = fix_terms(src)
        assert out == want and n == 1, (src, out)
    assert fix_terms("CoT‑라벨링된 데이터")[0] == "CoT‑라벨링된 데이터"  # 진짜 '라벨링된' 은 둔다
