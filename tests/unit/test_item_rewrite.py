"""item_rewrite_1114: 항목을 논문 블록으로 다시 쓰고, 문서 밖 숫자 · 짧아짐이면 그대로 둔다."""
from core.llm import item_rewrite

CTX = (
    "[문서 1]\n[2605.20049v1] Code Cleanliness\n[초록] Agents on cleaner code use 7 to 8% fewer tokens "
    "and reduce file revisitations by 34% across 660 trials."
)
ANS = (
    "<b>서론</b>\n질문.\n\n<b>본론</b>\n"
    "1. <b>Minimal-Pair</b>: 깨끗한 코드에서 토큰이 줄었습니다. [2605.20049v1]\n"
    "<b>결론</b>\n끝."
)


def _run(monkeypatch, reply):
    class Fake:
        def __init__(self, **kw):
            pass

        def invoke(self, msgs):
            return type("R", (), {"content": reply})()

    import langchain_ollama

    monkeypatch.setattr(langchain_ollama, "ChatOllama", Fake)
    return item_rewrite.rewrite_items(ANS, "q", CTX, {1: "2605.20049v1"}, "m")


def test_rewrites_item_keeps_head_and_citation(monkeypatch):
    new = "이 연구는 구조가 같고 깔끔함만 다른 저장소 쌍을 만들어 비교했습니다. 660회 실험에서 깔끔한 코드는 토큰을 7 to 8% 덜 쓰고 파일 재방문을 34% 줄였습니다."
    out, st = _run(monkeypatch, new)
    assert st == {"바꿈": 1}
    assert f"1. <b>Minimal-Pair</b>: {new} [2605.20049v1]" in out
    assert out.endswith("<b>결론</b>\n끝.")


def test_keeps_item_when_number_not_in_doc(monkeypatch):
    out, st = _run(monkeypatch, "이 연구는 저장소 쌍을 만들어 비교했습니다. 깔끔한 코드는 토큰을 55% 덜 쓰고 재방문을 크게 줄였으며 실험 규모도 충분했고 여러 저장소와 여러 작업에 걸쳐 같은 경향이 나타났습니다.")
    assert st == {"문서 밖 숫자": 1} and out == ANS


def test_keeps_item_when_shorter(monkeypatch):
    out, st = _run(monkeypatch, "짧음")
    assert st == {"길이": 1} and out == ANS
