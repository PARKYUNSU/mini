"""RAG 답변 서론의 모순된 '문서에 없다' 제거 (`core.llm.answer_fix`).

왜 있나 (docs/experiments/yunsur_v12/README.md §4.5): v12 가 정답을 받고도 31% 에서
서론에 "문서에 없다"고 쓴 뒤 결론에서는 찾았다고 한다. 결론도 없다고 하면 건드리지 않는다.
"""

from __future__ import annotations

from core.llm.answer_fix import drop_contradicted_no_doc

MD = (
    "### 서론\n"
    "제공된 문서에는 질문에서 찾는 연구가 없습니다. 깃허브 이슈의 이미지는 중요합니다.\n\n"
    "### 본론\n"
    "1. **CodeV**: 시각 데이터를 활용한다 [2412.17315v1].\n\n"
    "### 결론\n"
    "CodeV 가 질문에서 찾는 연구입니다.\n"
)


def test_drops_contradicted_intro_sentence():
    out, dropped = drop_contradicted_no_doc(MD)
    assert dropped
    assert "없습니다" not in out
    assert "### 서론\n깃허브 이슈의 이미지는 중요합니다." in out
    assert out.endswith("CodeV 가 질문에서 찾는 연구입니다.\n")


def test_keeps_when_conclusion_also_negative():
    md = MD.replace("CodeV 가 질문에서 찾는 연구입니다.", "질문에서 찾는 구체적인 연구는 제공되지 않았습니다.")
    out, dropped = drop_contradicted_no_doc(md)
    assert not dropped and out == md


def test_html_sections():
    html = MD.replace("### 서론", "<b>서론</b>").replace("### 본론", "<b>본론</b>").replace("### 결론", "<b>결론</b>")
    out, dropped = drop_contradicted_no_doc(html)
    assert dropped and "없습니다" not in out.split("<b>본론</b>")[0]


def test_no_denial_untouched():
    md = MD.replace("제공된 문서에는 질문에서 찾는 연구가 없습니다. ", "")
    assert drop_contradicted_no_doc(md) == (md, False)


def test_denial_outside_intro_untouched():
    md = MD.replace("CodeV 가 질문에서 찾는 연구입니다.", "CodeV 입니다.").replace(
        "1. **CodeV**: 시각 데이터를 활용한다", "1. **CodeV**: 제공된 문서에는 수치가 없습니다. 시각 데이터를 활용한다"
    ).replace("제공된 문서에는 질문에서 찾는 연구가 없습니다. ", "")
    assert drop_contradicted_no_doc(md) == (md, False)


def test_missing_sections_untouched():
    text = "제공된 문서에는 질문에서 찾는 연구가 없습니다."
    assert drop_contradicted_no_doc(text) == (text, False)


# 같은 논문 항목 합치기 (docs/experiments/merge_same_paper_1021)
from core.llm.answer_fix import merge_same_paper_items, renumber_body_items

SPLIT = (
    "<b>서론</b>\nDDC 소개.\n\n<b>본론</b>\n"
    "1. <b>DDC</b>: 폭과 깊이를 같이 본다[2605.15100v1].\n"
    "2. <b>Other</b>: 다른 논문[2401.00001v1].\n"
    "3. <b>DDC</b>: 토큰을 10배 줄였다[2605.15100v1].\n"
    "4. <b>Both</b>: 둘 다[2605.15100v1][2401.00001v1].\n\n"
    "<b>결론</b>\n10배."
)


def test_merges_same_single_paper_items():
    out, ch = merge_same_paper_items(SPLIT)
    out, _ = renumber_body_items(out)
    assert ch
    assert "1. <b>DDC</b>: 폭과 깊이를 같이 본다[2605.15100v1]. 토큰을 10배 줄였다[2605.15100v1].\n" in out
    assert "2. <b>Other</b>" in out and "3. <b>Both</b>: 둘 다" in out  # 두 편 인용 항목은 그대로
    assert out.count("<b>DDC</b>") == 1 and out.endswith("<b>결론</b>\n10배.")


def test_no_merge_when_distinct():
    md = SPLIT.replace("3. <b>DDC</b>: 토큰을 10배 줄였다[2605.15100v1].\n", "")
    assert merge_same_paper_items(md) == (md, False)


# 내부 문서 번호 · 중복 인용 정리 (docs/experiments/cite_cleanup_1022)
from core.llm.answer_fix import clean_internal_refs

IDS = {1: "2503.09579v3", 2: "2607.02980v1", 3: "2410.14641v3", 4: "2503.09579v3"}


def test_clean_internal_refs():
    a = ("2. 위치 편향 문제[2503.09579v3][2607.02980v1] (참고: 문서 1·2는 GQA 및 HiLS 연구이며, 질문과 직접 관련이 없습니다).\n"
         "반면 [2503.09579v3]과 [2503.09579v3]는 FLOPs 를 50% 줄인다. 문서 1과 문서 4 모두 같은 결과다. 문서 3은 벤치마크다[문서 3].")
    out, ch = clean_internal_refs(a, IDS)
    assert ch
    assert "(참고" not in out and "위치 편향 문제[2503.09579v3][2607.02980v1]." in out
    assert "반면 [2503.09579v3]는 FLOPs 를 50% 줄인다." in out
    assert "[2503.09579v3] 모두 같은 결과다." in out and "[2410.14641v3]은 벤치마크다[문서 3]." in out  # 대괄호 인용은 그대로


def test_clean_internal_refs_noop():
    a = "참고 문서에는 없다. 결과[2410.14641v3]. 문서 9는 모른다."
    assert clean_internal_refs(a, IDS) == (a, False)


def test_clean_internal_refs_bare_list():
    out, ch = clean_internal_refs("문서 1·2는 같은 결과다. 문서 3·9는 모른다.", IDS)
    assert out == "[2503.09579v3][2607.02980v1]는 같은 결과다. 문서 3·9는 모른다."


def test_normalize_fullwidth_punct():
    from core.llm.answer_fix import normalize_fullwidth_punct as f
    out, ch = f("향상된 결과이다 [2509.25085v4]。RankZephyr은 강인하다[2312.02724v1]。\n다음")
    assert ch and out == "향상된 결과이다 [2509.25085v4]. RankZephyr은 강인하다[2312.02724v1].\n다음"
    assert f("보통 문장. 끝") == ("보통 문장. 끝", False)


def test_align_conclusion_numbers():
    # 논문이 초록 61.94 · 본문 61.85 로 달라 본론 · 결론이 어긋났다 (cross_metric_1113)
    from core.llm.answer_fix import align_conclusion_numbers as f
    ans = ("<b>서론</b>\n…\n<b>본론</b>\n1. <b>jina</b>: BEIR 61.85 nDCG@10, 4.79% 향상. [2509.25085v4]\n"
           "2. <b>RZ</b>: 정확도 0.72. [2312.02724v1]\n\n<b>결론</b>\njina 는 61.94 nDCG@10 · 4.79% 향상이다 [2509.25085v4]. "
           "RZ 는 0.88 이다[2312.02724v1].\n\n📎 <b>DB 밖</b>\n• X 61.94")
    out, n = f(ans)
    concl = out.split("<b>결론</b>")[1]
    assert n == 1 and "61.85 nDCG@10" in concl and "61.94 nDCG" not in concl.split("📎")[0]
    assert "0.88" in concl  # 크게 다르면(다른 지표일 수 있음) 그대로
    assert "• X 61.94" in out  # DB 밖 목록은 손대지 않는다
    assert f("머리 없는 답 61.94") == ("머리 없는 답 61.94", 0)
    # 인용 ID 의 숫자는 소수로 보지 않는다(회귀 확인에서 [2412.13050v1] 을 바꾼 버그)
    a2 = ("<b>본론</b>\n1. <b>A</b>: x [2412.17188v1][2412.13050v1]\n<b>결론</b>\nA 다[2412.13050v1][2412.17188v1].")
    assert f(a2) == (a2, 0)
    # 같은 문장에 본론 값이 있으면 다른 조건의 수 · 본론이 반올림 값이면 그대로 (회귀 확인 O_16 · T05)
    a3 = ("<b>본론</b>\n1. <b>L</b>: 64배 압축 95.7% [2601.10155v1]\n2. <b>R</b>: 평균 2.9% [2606.15441v1]\n"
          "<b>결론</b>\nL 은 64배 95.7%, 32배 95.0% 다[2601.10155v1]. R 은 2.92% 다[2606.15441v1].")
    assert f(a3) == (a3, 0)


def test_mark_related_items():
    from core.llm.answer_fix import mark_related_items

    a = ("### 서론\nKV 캐시는 중요하다.\n\n### 본론\n1. **HiCBench**: 벤치마크. [문서 1]\n2. 그냥 설명 [문서 3]\n\n"
         "### 결론\n따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.")
    out, n = mark_related_items(a)
    assert n == 2
    assert "1. **HiCBench** (관련 연구): 벤치마크." in out and "2. (관련 연구) 그냥 설명" in out
    assert "### 서론\n제공된 문서에는 질문이 찾는 연구가 없습니다. KV 캐시는 중요하다." in out
    assert mark_related_items(out) == (out, 0)  # 두 번 적용해도 같다
    found = a.replace("따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다.", "HiCBench 가 답이다.")
    assert mark_related_items(found) == (found, 0)  # 결론이 찾았다고 하면 두다
    html = "<b>서론</b>\n제공된 문서에는 질문이 찾는 연구가 없습니다.\n<b>본론</b>\n1. <b>UDA</b>: 설명\n<b>결론</b>\n찾을 수 없습니다."
    out, n = mark_related_items(html)
    assert n == 1 and "1. <b>UDA</b> (관련 연구): 설명" in out and out.count("찾는 연구가 없습니다") == 1


def test_depth_template_keeps_item_shape():
    # depth_1114: 항목 꼴(번호 · 굵은 이름 · 끝 [문서 N])을 바꾸면 후처리(인용 고침 · 항목 합치기 · 관련 연구 표시)가 깨진다
    from core.llm.agent_prompts import RAG_OUTPUT_TEMPLATE_DEPTH as T

    assert "### 서론" in T and "### 본론" in T and "### 결론" in T
    assert "1. **{핵심 접근·시스템 이름}**:" in T and "[문서 1]\n2." in T
