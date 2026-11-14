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

__all__ = ["align_conclusion_numbers", "clean_internal_refs", "drop_contradicted_no_doc", "mark_related_items",
           "merge_same_paper_items", "normalize_fullwidth_punct", "renumber_body_items"]

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


# 본론 번호 다시 매기기 (2026-10-20 실제 사용 피드백): 목록 번호 칸 템플릿(list_slots_1016)에서 모델이
# 관련 없는 칸을 빼고도 남은 칸의 원래 번호(1, 4, 7, 8)를 그대로 썼다. 본론 안의 "N. " 항목만 1부터 다시 매긴다.
_ITEM = re.compile(r"^(\s*)(\d{1,2})\.(\s+)")


def renumber_body_items(answer: str) -> tuple[str, bool]:
    """본론 머리와 결론 머리 사이의 번호 항목을 1, 2, 3… 으로 다시 매긴다. 바뀌었으면 True."""
    b, c = _find("본론", answer), _find("결론", answer)
    if not b:
        return answer, False
    end = c.start() if c and c.start() > b.end() else len(answer)
    body = answer[b.end():end]
    lines, n, changed = body.split("\n"), 0, False
    for k, line in enumerate(lines):
        m = _ITEM.match(line)
        if not m:
            continue
        n += 1
        if int(m.group(2)) != n:
            lines[k] = f"{m.group(1)}{n}.{m.group(3)}" + line[m.end():]
            changed = True
    return (answer[:b.end()] + "\n".join(lines) + answer[end:], changed) if changed else (answer, False)


# 같은 논문 항목 합치기 (docs/experiments/merge_same_paper_1021): 판정이 한 편을 고르면 모델이 그 논문을
# "1. **X**: 방법" / "2. **X**: 결과" 로 나눠 써서(수치 질문 19/26) 항목 수가 논문 수처럼 읽혔다.
_CITED = re.compile(r"\[\s*(\d{4}\.\d{4,5})(?:v\d+)?\s*\]")
_ITEM_HEAD = re.compile(r"^\d{1,2}\.\s+(?:(?:<b>[^<\n]*</b>|\*\*[^*\n]*\*\*)\s*[:：]\s*)?")


def merge_same_paper_items(answer: str) -> tuple[str, bool]:
    """본론에서 논문 한 편만 인용한 항목이 앞 항목과 같은 한 편이면 앞 항목에 붙인다. 번호는 renumber_body_items 가."""
    b, c = _find("본론", answer), _find("결론", answer)
    if not b:
        return answer, False
    end = c.start() if c and c.start() > b.end() else len(answer)
    chunks = re.split(r"(?m)^(?=[ \t]*\d{1,2}\.\s)", answer[b.end():end])
    out, owner, changed = [chunks[0]], {}, False
    for ch in chunks[1:]:
        ids = set(_CITED.findall(ch))
        pid = next(iter(ids)) if len(ids) == 1 else None
        if pid in owner:
            k = owner[pid]
            tail = out[k][len(out[k].rstrip()):]
            out[k] = out[k].rstrip() + " " + _ITEM_HEAD.sub("", ch.strip(), count=1) + tail
            changed = True
            continue
        if pid:
            owner[pid] = len(out)
        out.append(ch)
    return (answer[:b.end()] + "".join(out) + answer[end:], True) if changed else (answer, False)


# 내부 문서 번호 노출 · 같은 인용 중복 정리 (docs/experiments/cite_cleanup_1022): 같은 논문이 두 블록에 나뉘면
# "[A]과 [A]는" 처럼 같은 인용이 겹치고, 모델이 "(참고: 문서 1·2는 …)" · "문서 1은 …" 으로 내부 번호를 드러냈다.
_ID_REF = r"\[\d{4}\.\d{4,5}(?:v\d+)?\]"
_DOC_PAREN = re.compile(r"\s*\((?:참고[:：]?\s*)?[^()\n]*문서\s*\d[^()\n]*\)")
_DOC_BARE = re.compile(r"(?<![\[\w])문서\s*(\d{1,2}(?:\s*·\s*\d{1,2}(?!\d|\.\d))*)(?!\s*\])")  # `문서 1·2` 도 (answer_review_1030)
_DUP_CITE = re.compile(rf"({_ID_REF})(?:\s*(?:과|와|,|및|그리고)?\s*\1)+")


def clean_internal_refs(answer: str, doc_ids: dict[int, str]) -> tuple[str, bool]:
    """``(고친 답, 바뀌었나)``. doc_ids 는 ``{문서 번호: 논문 ID}``."""
    out = _DOC_PAREN.sub("", answer)
    def _bare(m: re.Match[str]) -> str:
        ns = [int(n) for n in re.findall(r"\d{1,2}", m.group(1))]
        return "".join(f"[{doc_ids[n]}]" for n in ns) if all(n in doc_ids for n in ns) else m.group(0)
    out = _DOC_BARE.sub(_bare, out)
    out = _DUP_CITE.sub(r"\1", out)
    return out, out != answer


# 9B 가 한국어 문장 끝에 중국어 전각 문장부호를 섞는다(cross_metric_1113 텔레그램 "…결과이다 [2509.25085v4]。").
_FULLWIDTH = {"。": ". ", "，": ", ", "：": ": ", "；": "; ", "！": "! ", "？": "? "}


def normalize_fullwidth_punct(answer: str) -> tuple[str, bool]:
    """``(고친 답, 바꿨는가)``. 전각 문장부호를 반각 + 공백으로 바꾸고 겹친 공백을 하나로."""
    if not any(ch in answer for ch in _FULLWIDTH):
        return answer, False
    out = answer
    for k, v in _FULLWIDTH.items():
        out = out.replace(k, v)
    return re.sub(r"[ \t]+(\n)", r"\1", re.sub(r"(?<=\S) {2,}", " ", out)), True


_CITE = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]")
_DEC = re.compile(r"(?<![\d.])(\d+\.\d+)(?![\d.])")
_ARXIV_ID = re.compile(r"^\d{4}\.\d{4,5}$")  # 인용 ID(2412.13050) 는 소수가 아니다


def align_conclusion_numbers(answer: str) -> tuple[str, int]:
    """``(고친 답, 바꾼 수)``. 결론의 소수가 같은 논문의 본론 항목 소수와 정수부가 같고 1% 안으로만 다르면
    본론 값으로 맞춘다 — 한 논문이 초록 61.94 · 본문 61.85 로 다르게 적어, 답의 본론과 결론이 어긋났다
    (cross_metric_1113 텔레그램 jina-reranker-v3). 크게 다른 수는 다른 지표일 수 있어 건드리지 않는다."""
    m_b, m_c = _find("본론", answer), _find("결론", answer)
    if not (m_b and m_c) or m_c.start() < m_b.end():
        return answer, 0
    body = answer[m_b.end():m_c.start()]
    per: dict[str, list[str]] = {}
    for item in re.split(r"\n(?=\s*(?:<b>)?\d+\.\s)", body):
        for pid in set(_CITE.findall(item)):
            per.setdefault(pid, []).extend(v for v in _DEC.findall(item) if not _ARXIV_ID.match(v))
    tail = answer[m_c.end():]
    cut = tail.find("\n\n📎")
    concl, rest = (tail[:cut], tail[cut:]) if cut >= 0 else (tail, "")
    n = 0

    def fix_sent(sent: str) -> str:
        nonlocal n
        pids = set(_CITE.findall(sent))
        cands = [v for p in pids for v in per.get(p, [])]
        if not cands:
            return sent

        def rep(m: re.Match[str]) -> str:
            nonlocal n
            x = m.group(1)
            if _ARXIV_ID.match(x) or x in cands:
                return x
            # 본론 값이 이미 같은 문장에 있으면 x 는 다른 조건의 수(LOOKAT 64배 95.7% · 32배 95.0%),
            # 본론 값이 자릿수가 적으면 반올림한 것(2.9 ↔ 2.92) — 둘 다 건드리지 않는다 (회귀 확인 5,677 답)
            near = [v for v in cands if v.split(".")[0] == x.split(".")[0]
                    and abs(float(v) - float(x)) <= 0.01 * max(float(x), 1e-9)
                    and v not in sent and len(v.split(".")[1]) >= len(x.split(".")[1])]
            if len(set(near)) == 1:
                n += 1
                return near[0]
            return x
        return _DEC.sub(rep, sent)

    # 문장 단위(인용이 문장 끝에 붙는 꼴) — 마침표 뒤 공백 · 줄바꿈으로 자른다
    parts = re.split(r"(?<=[.!?。])(\s+)", concl)
    concl2 = "".join(fix_sent(p) if i % 2 == 0 else p for i, p in enumerate(parts))
    return (answer[:m_c.end()] + concl2 + rest, n) if n else (answer, 0)


# '없음' 힌트 답의 본론 표시 (answer_issues_1113 ①): 힌트는 본론 항목 이름 뒤에 `(관련 연구)` 를 붙이라고 하지만
# v13 은 0/37 붙였다 — 가까운 문서를 정답처럼 나열한 뒤 결론만 '없음' 이라 모순으로 읽혔다(27/37).
# 모델이 결론에서 스스로 '없음' 이라고 쓴 답만 고친다. 힌트를 무시하고 찾았다고 답한 경우(판정이 틀릴 때가 있다)는 둔다.
_NONE = re.compile(r"찾는 연구(는|가)?[^.\n]{0,30}(없|찾을 수 없)|찾을 수 없습니다|다루(지 않|는 연구는 없)|포함되어 있지 않|포함되지 않")
_RELATED = "(관련 연구)"
_LEAD = "제공된 문서에는 질문이 찾는 연구가 없습니다."
_ITEM_NAME = re.compile(r"^(\s*\d{1,2}\.\s+)(\*\*[^*\n]+\*\*|<b>[^<\n]+</b>)?")
_CONCL_END = re.compile(r"\n[ \t]*(?:📎|<b>📎|---)")


def mark_related_items(answer: str) -> tuple[str, int]:
    """``(고친 답, 표시를 붙인 항목 수)``. 결론이 '없음' 이 아니거나 섹션 머리를 못 찾으면 손대지 않는다."""
    m_intro, m_body, m_concl = _find("서론", answer), _find("본론", answer), _find("결론", answer)
    if not (m_body and m_concl) or m_body.end() > m_concl.start():
        return answer, 0
    rest = answer[m_concl.end():]
    e = _CONCL_END.search(rest)
    if not _NONE.search(rest[:e.start()] if e else rest):
        return answer, 0
    lines, n = answer[m_body.end():m_concl.start()].split("\n"), 0
    for k, line in enumerate(lines):
        m = _ITEM_NAME.match(line)
        if not m or "관련 연구" in line:
            continue
        if m.group(2):  # "1. **X**" → "1. **X** (관련 연구)"
            lines[k] = line[:m.end()] + " " + _RELATED + line[m.end():]
        else:  # 이름 강조가 없으면 번호 뒤에
            lines[k] = m.group(1) + _RELATED + " " + line[m.end(1):]
        n += 1
    if not n:
        return answer, 0
    out = answer[:m_body.end()] + "\n".join(lines) + answer[m_concl.start():]
    if m_intro and m_intro.end() <= m_body.start():
        intro = out[m_intro.end():m_body.start()]
        if not _NONE.search(intro):
            out = out[:m_intro.end()] + "\n" + _LEAD + " " + intro.lstrip("\n") + out[m_body.start():]
    return out, n
