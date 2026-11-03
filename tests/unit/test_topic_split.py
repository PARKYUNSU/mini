"""core.graph.agent_nodes 여러 주제 질문 나눠 검색 — 후보 고르기 · 블록 번갈아 합치기 (docs/experiments/topic_split_1103)."""
from core.graph.agent_nodes import _RAG_HIT_SEP, _interleave_topic_blocks, topic_split_candidate


def _blk(pid: str, text: str = "x") -> str:
    return f"[paper_id: {pid}v1]\n{text}"


def _pids(ctx: str) -> list[str]:
    return [b.split("]")[0][len("[paper_id: "):-2] for b in ctx.split(_RAG_HIT_SEP)]


def test_candidate_real_shapes():
    # 실사용 job 140 · 76 · 74 · 77 · 75 모양
    assert topic_split_candidate("…찾아주세요.\n\n1. LLM-as-a-Judge의 한계 (1.0% vs 11.4%)\n2. 인간 검증의 필수성\n3. 범위 보고")
    assert topic_split_candidate("아래 4개 축 중 하나로 분류해줘:\n(1) Retrieval 개선\n(2) Reranking\n(3) Chunking")
    assert topic_split_candidate("논문 5개를 찾아줘: 'Improving RAG retrieval accuracy', 'Reranking', 'Chunking optimization'.")
    assert topic_split_candidate("RAG 검색 정확도 향상(retrieval accuracy), Reranking, Chunking, Hallucination mitigation 관련 최신 논문 찾아줘.")
    assert topic_split_candidate("① 검색 개선 ② 재순위")


def test_candidate_skips_single_topic():
    assert not topic_split_candidate("LLM-as-a-Judge 판정 불일치 논문 찾아줘")
    assert not topic_split_candidate("GPT-4o와 Grok의 판정 결과(1.0% vs 11.4%)가 갈리는 이유가 뭐야?")
    assert not topic_split_candidate("버전 1.5와 2.0 중 뭐가 나아?")
    assert not topic_split_candidate("LoRA랑 QLoRA, 뭐가 달라?")
    assert not topic_split_candidate("2. 만 있는 질문")


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
