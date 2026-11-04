"""core.graph.agent_nodes 여러 주제 질문 나눠 검색 — 후보 고르기 · 블록 번갈아 합치기 (docs/experiments/topic_split_1103)."""
from core.llm.presence_judge import item_docs_note, parse_item_docs
from core.graph.agent_nodes import _RAG_HIT_SEP, _explicit_subtopics, _interleave_topic_blocks, _parse_subtopics, topic_answer_items, topic_split_candidate


def _blk(pid: str, text: str = "x") -> str:
    return f"[paper_id: {pid}v1]\n{text}"


def _pids(ctx: str) -> list[str]:
    return [b.split("]")[0][len("[paper_id: "):-2] for b in ctx.split(_RAG_HIT_SEP)]


def test_candidate_real_shapes():
    # 실사용 job 140 · 76 · 74 · 77 · 75 모양
    assert topic_split_candidate("…찾아주세요.\n\n1. LLM-as-a-Judge의 한계 (1.0% vs 11.4%)\n2. 인간 검증의 필수성\n3. 범위 보고")
    assert topic_split_candidate("아래 4개 축 중 하나로 분류해줘:\n(1) Retrieval 개선\n(2) Reranking\n(3) Chunking")
    assert topic_split_candidate("논문 5개를 찾아줘: 'Improving RAG retrieval accuracy', 'Reranking', 'Chunking optimization'.")
    assert topic_split_candidate("Hallucination detection, Uncertainty estimation, Selective prediction\n\n[요청]\n논문 찾아줘")
    assert topic_split_candidate("이런 deep research 에이전트의 평가 벤치마크, 출처 검증 방법, 긴 보고서의 사실성 평가를 다룬 최신 연구를 찾아주세요.")
    assert topic_split_candidate("RAG 검색 정확도 향상(retrieval accuracy), Reranking, Chunking, Hallucination mitigation 관련 최신 논문 찾아줘.")
    assert topic_split_candidate("① 검색 개선 ② 재순위")


def test_candidate_skips_single_topic():
    assert not topic_split_candidate("LLM-as-a-Judge 판정 불일치 논문 찾아줘")
    assert not topic_split_candidate("GPT-4o와 Grok의 판정 결과(1.0% vs 11.4%)가 갈리는 이유가 뭐야?")
    assert not topic_split_candidate("버전 1.5와 2.0 중 뭐가 나아?")
    assert not topic_split_candidate("LoRA랑 QLoRA, 뭐가 달라?")
    assert not topic_split_candidate("2. 만 있는 질문")
    # 쉼표가 있어도 뒤가 내용이면 한 주제
    assert not topic_split_candidate("벡터 저장소, 지식 그래프, 텐서 분해를 합친 도메인 특화 RAG 연구 요약해줘")
    assert not topic_split_candidate("RAG의 신뢰성, 프라이버시, 보안 문제를 정리한 서베이 알려줘")
    assert not topic_split_candidate("5W3H 구조화 의도 프롬프트가 Claude, GPT-4o, Gemini에서도 잘 통하는지 비교한 연구 알려줘")


def test_interleave_alternates_topics_then_primary():
    primary = _RAG_HIT_SEP.join([_blk("2401.00001"), _blk("2401.00002")])
    t1 = _RAG_HIT_SEP.join([_blk("2402.00001"), _blk("2402.00002"), _blk("2402.00003"), _blk("2402.00004")])
    t2 = _RAG_HIT_SEP.join([_blk("2403.00001"), _blk("2402.00001")])
    t3 = _RAG_HIT_SEP.join([_blk("2404.00001")])
    out = _pids(_interleave_topic_blocks(primary, [t1, t2, t3]))
    # 주제별 상위 3까지, 겹친 논문(2402.00001)은 한 번만, 원래 검색은 뒤에
    assert out == ["2402.00001", "2403.00001", "2404.00001", "2402.00002", "2402.00003", "2401.00001", "2401.00002"]


def test_interleave_skips_empty():
    primary = _RAG_HIT_SEP.join(_blk(f"2401.{i:05d}") for i in range(3))
    t1 = _RAG_HIT_SEP.join(_blk(f"2402.{i:05d}") for i in range(5))
    assert len(_pids(_interleave_topic_blocks(primary, [t1, "관련 문서 없음"]))) == 6
    assert _interleave_topic_blocks(primary, ["관련 문서 없음", "", "검색 오류: x"]) == primary
    assert _pids(_interleave_topic_blocks("관련 문서 없음", [t1])) == [f"2402.{i:05d}" for i in range(3)]


def test_candidate_ignores_commas_in_parens():
    assert not topic_split_candidate("디코딩 전략(greedy, beam, sampling)에 따라 환각이 어떻게 달라지는지 본 연구 있어?")
    assert topic_split_candidate("하이브리드 검색(BM25+dense), 쿼리 확장, 문서 청크 크기 최적화 관련 논문 찾아줘")


def test_parse_reads_lines_with_or_without_numbers():
    q = "양자화, 가지치기, 저랭크 분해 논문 찾아줘"
    # 번호 없이 쓴 줄 · 번호 줄 · 덧붙인 설명
    assert _parse_subtopics("model quantization weights\nmodel pruning methods\nlow rank decomposition", q) == [
        "model quantization weights", "model pruning methods", "low rank decomposition"]
    assert _parse_subtopics("1: model quantization\n2) model pruning\n\n(Note: two topics here.)", q) == ["model quantization", "model pruning"]
    assert _parse_subtopics("only one topic line here", q) == []


def test_explicit_items():
    assert _explicit_subtopics("Prompt compression, KV cache eviction, Sparse attention\n\n지시:\n1. 찾아라.\n2. 빼라.") == [
        "Prompt compression", "KV cache eviction", "Sparse attention"]
    assert _explicit_subtopics("키워드 'a b', 'c d', 'e f' 로 찾아줘") == ["a b", "c d", "e f"]
    assert _explicit_subtopics("정렬 공부 중. (1) RLHF 보상 모델 (2) DPO 방법 (3) 보상 해킹 문제 — 이 세 가지 논문을 알려줘.") == [
        "RLHF 보상 모델", "DPO 방법", "보상 해킹 문제"]
    assert _explicit_subtopics("아래 축으로:\n(1) Retrieval 개선\n(2) Reranking\n그리고 균형 있게 골라줘.") == ["Retrieval 개선", "Reranking"]
    # 소수점 · 지시문 항목은 믿지 않는다
    assert _explicit_subtopics("논문 찾아줘. 1. 논문 5개 찾아 주세요. 2. 표로 정리해줘.") == []
    assert _explicit_subtopics("1) 배경 2) 방법 3) 결과 순으로 정리해줘") == []
    assert _explicit_subtopics("RAG 평가 논문 찾아줘. (1) 서베이 제외 (2) 2024년 이후 (3) 다섯 편") == []
    # 일반 문장의 쉼표는 항목 아님
    assert _explicit_subtopics("Which is better, GPT-4, Claude, or Gemini?") == []


def test_parse_rag_context_and_repeats():
    # 조사 붙은 RAG 도 질문의 맥락이다 · 없던 RAG 는 뺀다
    assert _parse_subtopics("query rewriting\ncross encoder rerank", "사내 RAG를 고치려는데 x, y, z 관련 논문") == [
        "query rewriting RAG", "cross encoder rerank RAG"]
    assert _parse_subtopics("pruning methods RAG\nquantization, rag, model size", "모델 경량화 논문") == [
        "pruning methods", "quantization, model size"]
    assert _parse_subtopics("storage systems\nmemory hierarchy", "storage 와 average 논문") == ["storage systems", "memory hierarchy"]
    # 같은 목록을 번호 붙여 한 번 더 쓰면 첫 덩어리만 · 머리말 줄은 뺀다
    assert _parse_subtopics("Agent planning\nSelf reflection\n\n1: Agent planning studies\n2: Reflection studies\n3: Error recovery", "q") == [
        "Agent planning", "Self reflection"]
    assert _parse_subtopics("Topics are as follows:\n1: model pruning\n2: model quantization", "q") == ["model pruning", "model quantization"]


def test_answer_items():
    assert topic_answer_items("찾아 주세요.\n1. 질의 재작성\n2. reranking\n3. faithfulness 평가") == ["질의 재작성", "reranking", "faithfulness 평가"]
    # 마지막 항목의 요청 꼬리는 잘라낸다
    assert topic_answer_items("(1) 자기 지도 학습 (2) 대조 학습 (3) 메타 학습에 대한 논문을 알려줘.") == ["자기 지도 학습", "대조 학습", "메타 학습"]
    assert topic_answer_items("1) 문장 임베딩 평가 2) 다국어 임베딩 3) 임베딩 압축 쪽으로 찾아줘") == ["문장 임베딩 평가", "다국어 임베딩", "임베딩 압축"]
    # 쉼표 목록 · 괄호 안 쉼표는 나누지 않는다
    assert topic_answer_items("어텐션 희소화(예: a, b), 저정밀도 부동소수점, 모델 샤딩을 다룬 최신 논문 알려줘") == ["어텐션 희소화(예: a, b)", "저정밀도 부동소수점", "모델 샤딩"]
    assert topic_answer_items("연합 학습, 차등 프라이버시, 기계 언러닝 논문 추천해줘") == ["연합 학습", "차등 프라이버시", "기계 언러닝"]
    assert topic_answer_items("'late chunking', 'contextual retrieval', 'proposition indexing' 로 논문 찾아줘") == ["late chunking", "contextual retrieval", "proposition indexing"]
    # 항목이 아니면 빈 목록
    assert topic_answer_items("RAG의 정확도, 속도, 비용을 함께 최적화한 논문 알려줘") == []
    assert topic_answer_items("Llama 1, 2, 3을 비교한 논문 알려줘") == []
    assert topic_answer_items("LLM-as-a-Judge 판정 불일치 논문 찾아줘") == []
    assert topic_answer_items("논문 3편 찾아서 1. 제목 2. 저자 3. 핵심 결과 순으로 정리해줘. 주제는 LLM 양자화야.") == []


def test_parse_item_docs():
    raw = "문서 1: 항목 2\n문서 2: 없음\n문서 3: 항목 1, 항목 2\n문서 4: 항목 9"
    assert parse_item_docs(raw, 3) == {1: [3], 2: [1, 3], 3: []}
    assert parse_item_docs("답: 없음", 3) is None
    assert parse_item_docs("", 2) is None


def test_item_docs_note():
    note = item_docs_note(["A", "B"], {1: [2, 3], 2: []})
    assert "1. A: [문서 2], [문서 3]" in note
    assert "2. B: 없음" in note
