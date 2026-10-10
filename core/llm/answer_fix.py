"""RAG 답변 서론의 '문서에 없다' 문장이 결론과 모순되면 지운다.

왜 필요한가 (docs/experiments/yunsur_v12/README.md §4.5): yunsur_v12 는 정답 논문을
컨텍스트에서 받고도 31% (43/138) 에서 서론 첫 문장에 "제공된 문서에는 질문에서 찾는
… 없습니다"라고 쓴 뒤, 본론·결론에서는 그 논문을 찾았다고 설명한다. 학습 데이터 중
정답 없는 예시(7.5%)의 서두가 번진 것으로 보인다.

규칙 — 결론을 믿는다:
  - 서론에 '없다' 문장이 있고 결론에는 '없다/포함되어 있지 않다' 류가 **없으면**
    서론의 그 문장을 지운다 (결론이 찾았다고 말하므로 서론이 모순).
  - 결론도 '없다'고 하면 둔다 (일관되게 없다고 하는 답변).

정답 여부를 모르는 운영에서도 답변 안의 모순만으로 판단한다. 순수 함수다.
"""

from __future__ import annotations

import re

__all__ = ["drop_contradicted_no_doc"]

# 서론의 '문서에 없다' 문장 (v12 가 쓰는 변형들). 문장 끝 마침표까지 지운다.
_NO_DOC_SENT = re.compile(
    r"제공된\s*(?:문서|텍스트|정보|자료)(?:들)?에는[^.\n]*?(?:없습니다|찾을 수 없습니다)\.?[ \t]*"
)
# 결론이 '없다'고 말하는 표현.
_CONCL_NEG = re.compile(
    r"포함되어 있지 않|제공되지 않|찾을 수 없|명시되어 있지 않|존재하지 않|확인되지 않|없습니다"
)
# 섹션 머리 — 운영 원문(### 서론)과 HTML 변환본(<b>서론</b>) 둘 다.
_HEAD = r"(?:^###\s*{0}\s*$|<b>{0}</b>)"


def _find(head: str, text: str) -> re.Match[str] | None:
    return re.search(_HEAD.format(head), text, re.M)


def drop_contradicted_no_doc(answer: str) -> tuple[str, bool]:
    """``(고친 답변, 지웠는가)``. 섹션 머리를 못 찾으면 손대지 않는다."""
    m_intro, m_body, m_concl = _find("서론", answer), _find("본론", answer), _find("결론", answer)
    if not (m_intro and m_body and m_concl) or not (m_intro.end() <= m_body.start() <= m_concl.start()):
        return answer, False
    intro = answer[m_intro.end():m_body.start()]
    if not _NO_DOC_SENT.search(intro):
        return answer, False
    if _CONCL_NEG.search(answer[m_concl.end():]):
        return answer, False
    new_intro = _NO_DOC_SENT.sub("", intro, count=1)
    # 서론 첫 줄이 비면 머리 바로 뒤 줄바꿈만 남긴다.
    new_intro = re.sub(r"^(\n?)[ \t]+", r"\1", new_intro)
    return answer[:m_intro.end()] + new_intro + answer[m_body.start():], True
