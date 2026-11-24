"""답 칸 검사기 (core/llm/slot_fill.py, slot_fill_1124)."""
from unittest import mock

from core.llm import slot_fill as sf

CTX = """[문서 1]
[2509.26184v4] Auto-ARGUE: LLM-Based Report Generation Evaluation
[초록] We implement ARGUE with LLMs. It shows high correlation with human judgments on TREC 2024 NeuCLIR.

---

[문서 2]
[2305.14251v2] FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation
[초록] We introduce FActScore, which breaks a generation into atomic facts. ChatGPT reaches only 58%.

---

[문서 3]
[2401.00001v1] Unrelated Paper
[초록] Nothing."""
IDS = {1: "2509.26184v4", 2: "2305.14251v2", 3: "2401.00001v1"}
LABELS = {1: "P", 2: "P", 3: "N"}

W07 = """### 서론
'한국어' 조건을 직접 다룬 연구는 찾지 못했고, 가장 가까운 연구는 아래와 같습니다.

### 본론
1. **Auto‑ARGUE** (관련 연구): ARGUE 를 LLM 으로 구현했다. [2509.26184v4] **Auto‑ARGUE** (관련 연구): 웹 앱으로 결과를 본다. [2509.26184v4]

### 결론
위 관련 연구가 가장 가깝습니다."""


def test_dedupe_removes_repeated_head_keeps_text():
    out, n = sf.dedupe_repeated_heads(W07)
    assert n == 1
    line = [l for l in out.split("\n") if l.startswith("1.")][0]
    assert line.count("**Auto‑ARGUE**") == 1 and "웹 앱으로 결과를 본다." in line


def test_dedupe_noop_without_repeat():
    ans = W07.replace(" **Auto‑ARGUE** (관련 연구): 웹 앱으로 결과를 본다. [2509.26184v4]", "")
    assert sf.dedupe_repeated_heads(ans) == (ans, 0)


def test_missing_ids_skips_unrelated():
    assert sf.missing_ids(W07, LABELS, IDS) == [("2305.14251", "P")]


def test_fill_appends_item_before_conclusion():
    text = "원자 사실 단위로 생성물을 나눠 지식 출처가 지지하는 비율을 계산하는 FActScore 를 제안했다. ChatGPT 는 58% 에 그쳤으며, 사람 평가 대신 쓸 자동 추정 방법도 함께 제시해 장문 생성의 사실 정밀도를 값싸게 잴 수 있게 했다."
    fake = mock.MagicMock()
    fake.invoke.return_value.content = text
    with mock.patch("langchain_ollama.ChatOllama", return_value=fake):
        out, st = sf.fill_missing_slots(W07, "q", CTX, LABELS, IDS, "m")
    assert st == {"채움": 1}
    body = out.split("### 본론")[1].split("### 결론")[0]
    assert "**FActScore** (관련 연구): " + text + " [2305.14251]" in body
    assert out.rstrip().endswith("위 관련 연구가 가장 가깝습니다.")


def test_fill_rejects_foreign_number_and_no_call_when_complete():
    fake = mock.MagicMock()
    fake.invoke.return_value.content = "FActScore 를 제안했고 정확도는 91% 였다. 원자 사실 단위로 생성물을 나눠 지식 출처가 지지하는 비율을 계산하며, 여러 상용 모델의 장문 생성 결과를 사람 평가로 비교했다."
    with mock.patch("langchain_ollama.ChatOllama", return_value=fake):
        out, st = sf.fill_missing_slots(W07, "q", CTX, LABELS, IDS, "m")
    assert out == W07 and st == {"문서 밖 숫자": 1}
    full = W07.replace("[2509.26184v4]\n", "[2509.26184v4]\n2. **FActScore**: x [2305.14251v2]\n")
    with mock.patch("langchain_ollama.ChatOllama") as co:
        assert sf.fill_missing_slots(full, "q", CTX, LABELS, IDS, "m") == (full, {})
        co.assert_not_called()
