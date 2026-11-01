"""결론 인용 문장 바꿔 끼우기 (docs/experiments/conclusion_struct_1102)."""

from core.llm.answer_fix import _CITED
from core.llm.citation_fix import RAG_HIT_SEP
from core.llm.conclusion_swap import check_translation, first_person, sentences, snap, swap_conclusion

CTX = RAG_HIT_SEP.join([
    "[문서 1]\n[2410.21819v2] Self-Preference Bias\n[초록] Judges are widely used today. GPT-4 exhibits a significant degree of "
    "self-preference bias. LLMs assign higher evaluations to outputs with lower perplexity, regardless of whether the outputs "
    "were self-generated.",
    "[문서 2]\n[2512.16041v1] Right Way\n[초록] Benchmarks rely on human labels. Panels improve consistency by 12% over single "
    "judges. Human annotation may not be a reliable gold standard.",
])
IDS = {1: "2410.21819", 2: "2512.16041"}
HEAD = "<b>서론</b>\n…\n<b>본론</b>\n1. <b>A</b>: …[2410.21819v2]\n2. <b>B</b>: …[2512.16041v1]\n<b>결론</b>\n"
TAIL = "\n\n📎 **DB 밖에서 찾은 관련 논문** (OpenAlex 검색 · 내용은 요약하지 않음)\n- X (2024) [2404.13076]"
ANS = (HEAD + "같은 계열이면 perplexity 가 낮은 출력을 높게 본다[2410.21819v2]. 판정자를 바꾸면 완화되고 panel 이 12% 낫다"
       "[2512.16041v1]. 사람 표본 보정은 문서에 없습니다." + TAIL)


def test_sentences_leading_citation_goes_to_previous():
    assert sentences("A 는 좋다. [2401.00001v1] 따라서 B 다. [2401.00002]는 C 다.") == \
        ["A 는 좋다. [2401.00001v1]", "따라서 B 다.", "[2401.00002]는 C 다."]


def test_snap_numbers_then_words():
    blk = CTX.split(RAG_HIT_SEP)[1]
    assert snap("panel 이 12% 낫다[2512.16041v1].", blk) == "Panels improve consistency by 12% over single judges."
    # 모델 이름 속 숫자는 숫자로 안 센다 — "4 points" 문장이 아니라 GPT-4 문장
    blk2 = "[2401.00001v1] T\n[초록] Intro sentence is long enough. Our method improves results by 4 points. GPT-4 is the judge model here."
    assert snap("GPT-4 판정[2401.00001v1].", blk2) == "GPT-4 is the judge model here."


def test_check_translation():
    assert check_translation("Accuracy rose by 12%.", "정확도가 12% 올랐다.") == ""
    assert check_translation("Accuracy rose by 12%.", "정확도가 13% 올랐다.") == "원문 밖 숫자 13"
    src = "Human annotation may not be a reliable gold standard."
    assert check_translation(src, "인간 주석은 신뢰할 수 있는 금표준이 될 수 있다.") == "부정어 빠짐"
    assert check_translation(src, "인간 주석은 신뢰할 수 있는 금표준이 아닐 수 있다.") == ""
    assert check_translation("Results improve.", "결과가\n좋아진다.") == "꼴"


def test_first_person():
    assert first_person("우리의 실험 결과는 우리가 가정한 대로였고, 우리는 이를 공개한다.") == \
        "이 논문의 실험 결과는 이 논문이 가정한 대로였고, 이 논문은 이를 공개한다."
    assert first_person("우리나라 데이터") == "우리나라 데이터"


def test_swap_replaces_cited_keeps_uncited_and_tail():
    ko = {"Panels improve consistency by 12% over single judges.": "패널이 단일 판정자보다 일관성을 12% 높인다."}
    out, status, info = swap_conclusion(ANS, CTX, IDS, "m", translate=lambda s: ko.get(s, "번역\n실패"))
    assert status == "바꿈 2"
    concl = out[len(HEAD):]
    assert "판정자를 바꾸면" not in concl and "높게 본다" not in concl
    assert "패널이 단일 판정자보다 일관성을 12% 높인다. [2512.16041v1]" in concl
    assert "LLMs assign higher evaluations to outputs with lower perplexity" in concl  # 번역 탈락 → 영어 원문
    assert "사람 표본 보정은 문서에 없습니다." in concl and out.endswith(TAIL)
    assert set(_CITED.findall(out)) == set(_CITED.findall(ANS))
    assert info["fallback"] == ["꼴"] and info["dropped"] == 0


def test_swap_dedupes_same_source_and_skips_single_paper():
    ans = HEAD + "panel 이 12% 낫다[2512.16041v1]. 12% 로 판정이 고르다[2512.16041v1]."
    out, status, info = swap_conclusion(ans, CTX, IDS, "m", translate=lambda s: s)
    assert status == "바꿈 2" and out.count("Panels improve consistency") == 1 and info["pairs"][1]["after"] == []
    one = "<b>본론</b>\n1. <b>A</b>: …[2410.21819v2]\n<b>결론</b>\n높게 본다[2410.21819v2]."
    assert swap_conclusion(one, CTX, IDS, "m", translate=lambda s: s)[1] == "대상 아님"
    assert swap_conclusion(HEAD + "인용 없는 결론입니다.", CTX, IDS, "m", translate=lambda s: s)[1] == "인용 문장 없음"
