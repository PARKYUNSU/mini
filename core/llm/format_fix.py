"""답 형식 다듬기 (RAG_FORMAT_FIX, docs/experiments/format_fix_1117).

왜: 11-16 업무 질문 10개 사용자 평가에서
- 깨진 글자 5건 — 다시 쓰기가 영어 용어를 소리대로 옮김(포izoning · 판판 · 라울러 · 채킹), 거부된 다시 쓰기 뒤 원래 항목의 한자(六点).
- '없음' 판정 답이 관련 연구를 나열하고도 서론 · 결론에서 "찾는 연구가 없습니다" 라고 해 모순으로 읽힘(1 · 3번).
"""

from __future__ import annotations

import os
import re

__all__ = ["format_fix_active", "term_rule", "strip_hanzi", "partial_wording", "_GLUED"]

_GLUED = re.compile(r"[가-힣][a-z]{2,}")  # 한글 바로 뒤 라틴 소문자 — "포izoning". "LLM을" 같은 대문자 약어 + 조사는 안 걸린다
_HAN = re.compile(r"[一-鿿㐀-䶿]+")
_LEAD_OLD = re.compile(r"제공된 문서에는 질문이 찾는 연구가 없습니다\.?")
_CONCL_OLD = re.compile(r"따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다\.?")
LEAD_NEW = "질문을 직접 다룬 연구는 찾지 못했고, 가장 가까운 연구는 아래와 같습니다."
CONCL_NEW = "따라서 질문을 직접 다룬 연구는 없지만, 위 관련 연구가 가장 가깝습니다."


def format_fix_active() -> bool:
    return os.getenv("RAG_FORMAT_FIX", "0").strip() == "1"


def term_rule() -> str:
    """다시 쓰기 · 결론 프롬프트에 넣는 용어 규칙 한 줄(꺼져 있으면 빈 문자열)."""
    if not format_fix_active():
        return ""
    return ("- 영어 전문 용어(예: poisoning · judge · chunking)는 한글로 소리 나는 대로 옮기지 말고 영어 그대로 쓴다.\n"
            "- 다음은 정해진 번역을 쓴다: recall = 재현율, rater = 평가자, crowdsourced = 크라우드소싱, meta-classifier = 메타 분류기.\n")


def strip_hanzi(answer: str) -> tuple[str, int]:
    """남은 한자 덩어리를 지운다 — 앞뒤 공백은 하나로."""
    n = len(_HAN.findall(answer or ""))
    if not n:
        return answer, 0
    return re.sub(r"[ \t]{2,}", " ", _HAN.sub(" ", answer)), n


def partial_wording(answer: str) -> tuple[str, int]:
    """'없음' 판정 답에 (관련 연구) 항목이 있으면 고정 문장을 "직접 다룬 연구는 없고 가장 가까운 연구는" 꼴로."""
    if "관련 연구" not in (answer or ""):
        return answer, 0
    out, a = _LEAD_OLD.subn(LEAD_NEW, answer)
    out, b = _CONCL_OLD.subn(CONCL_NEW, out)
    return out, a + b


# --- S7 용어 · 항목 제목 (RAG_TERM_FIX, docs/experiments/term_fix_1118) ---
# 저장 답 2,551개(11-18)에서 실제로 나온 잘못된 음차만. 뒤 조사는 그대로 둔다.
_JONG = {"를": "을", "가": "이", "는": "은", "와": "과", "로": "으로"}  # 받침 없는 말 뒤 조사 → 받침 있는 말 뒤 조사
_TERMS = [
    (re.compile(r"(?:차킹|채킹|청크링)"), "청킹"),  # chunking
    (re.compile(r"허할루시네이션"), "환각"),
    (re.compile(r"판판이"), "판정자가"), (re.compile(r"판판은"), "판정자는"), (re.compile(r"판판을"), "판정자를"),
    (re.compile(r"판판"), "판정자"),  # judges — '판판하다'(평평하다)는 이 도메인 답에 안 나옴. 받침 달라 조사도 바꿈
    (re.compile(  # CoT rationale — 라울러 · 라테이션 · 라우널 … 매번 다르게 깨짐
        r"CoT\s*(?:[-‑]\s*)?(?:라울러|라테이션|라우널|라울린|라울|라벨링된(?=\s+(?:이유|합리화))|(?<=[-‑])(?!라벨)라[가-힣]{1,4}?)"
        r"(?:\s+(?:이유|합리화))?(으로|[을를이가은는의과와로도에])?(?![가-힣])"), lambda m: "CoT 근거 설명" + _JONG.get(m.group(1) or "", m.group(1) or "")),
    # 'rationale' 를 '이유' · '합리화' 로 옮긴 꼬리는 같이 지운다(U5 "CoT 근거 설명 이유를"), 조사는 받침 있는 '설명' 에 맞춘다
    # 6차 피드백 용어 사전 — 바꾼 말과 받침이 같아 뒤 조사는 그대로 둔다. 영어는 소문자 낱말만(논문 제목의 대문자는 둔다)
    (re.compile(r"회고율"), "재현율"),
    (re.compile(r"(?<![가-힣])라이터(?=들|에게|[가는를와의도로]|[^가-힣]|$)"), "평가자"),  # rater — 받침 없음 = 평가자
    (re.compile(r"메타\s?클래(?:서퍼|시파이어|시퍼)"), "메타 분류기"),
    (re.compile(r"(?<![A-Za-z0-9-])meta-classifiers?(?![A-Za-z0-9-])"), "메타 분류기"),
    (re.compile(r"(?<![A-Za-z0-9-])crowdsourc(?:ed|ing)(?![A-Za-z0-9-])"), "크라우드소싱"),
    (re.compile(r"(?<![A-Za-z0-9-])raters?(?![A-Za-z0-9-])"), "평가자"),
    (re.compile(r"(?<![A-Za-z0-9@-])recall(?![A-Za-z0-9@-])"), "재현율"),
]
_ITEM = re.compile(r"^(\s*\d+\.\s+)(.*)$")
_HANGUL = re.compile(r"[가-힣]")
_REF_TITLE = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n\[]+)")


def term_fix_active() -> bool:
    return os.getenv("RAG_TERM_FIX", "0").strip() == "1"


def fix_terms(answer: str) -> tuple[str, int]:
    n = 0
    for pat, rep in _TERMS:
        answer, k = pat.subn(rep, answer or "")
        n += k
    return answer, n


def _title_key(s: str) -> str:
    return re.sub(r"[^0-9a-z]", "", (s or "").lower())


def _short_title(title: str) -> str:
    t = title.strip().split(":")[0].strip()
    return t if len(t) <= 60 else t[:60].rsplit(" ", 1)[0]


def fix_item_titles(answer: str, rag_context: str) -> tuple[str, int]:
    """본론 항목을 '제목: 요약' 꼴로. 이름 뒤 콜론이 빠졌으면 넣고, 이름이 아예 없으면 인용 논문 제목을 붙인다."""
    mb = re.search(r"^[ \t#*]*본론[ \t*]*$", answer or "", re.M)
    if not mb:
        return answer, 0
    _full = dict(_REF_TITLE.findall(rag_context or ""))
    titles = {pid: _short_title(t) for pid, t in _full.items()}
    head, rest = answer[:mb.end()], answer[mb.end():]
    mc = re.search(r"^[ \t#*]*결론[ \t*]*$", rest, re.M)
    body, tail = (rest[:mc.start()], rest[mc.start():]) if mc else (rest, "")
    out, n = [], 0
    for line in body.split("\n"):
        m = _ITEM.match(line)
        if not m or ":" in m.group(2)[:120]:
            out.append(line)
            continue
        num, text = m.groups()
        cid = re.search(r"\[(\d{4}\.\d{4,5})", text)
        t = titles.get(cid.group(1)) if cid else None
        lead_id = re.match(r"\[\d{4}\.\d{4,5}(?:v\d+)?\]\s*", text)
        bold = re.match(r"(\*\*[^*\n]+\*\*)\s*(\(관련 연구\))?\s*", text)
        if lead_id:  # '[ID] 설명' — 이름 자리에 ID: 제목으로 바꾼다
            if t:
                line = f"{num}{t}: {text[lead_id.end():]}"
                n += 1
        elif text.startswith("(관련 연구)"):  # 이름 없이 표시만
            if t:
                line = f"{num}{t} (관련 연구): {text[len('(관련 연구)'):].lstrip(' :')}"
                n += 1
        elif bold:  # '**이름** (관련 연구) 설명' → '**이름** (관련 연구): 설명'
            line = num + bold.group(1) + (" " + bold.group(2) if bold.group(2) else "") + ": " + text[bold.end():]
            n += 1
        elif "(관련 연구)" in text[:120]:  # 'X (관련 연구) 설명' → 'X (관련 연구): 설명'
            line = num + text.replace("(관련 연구)", "(관련 연구):", 1)
            n += 1
        elif not _HANGUL.match(text) and _HANGUL.search(text):  # 'Name 설명' → 'Name: 설명'
            k = _HANGUL.search(text).start()
            k = text.rfind(" ", 0, k) + 1  # 'TabRAG은' 처럼 조사가 붙은 단어는 그 단어 앞에서 끊는다
            name = text[:k].strip()
            # 앞 영어가 논문 제목의 일부일 때만 이름으로 본다 — 'T5 기반 모델은' 같은 문장 첫 단어는 이름이 아니다
            if k > 0 and (not t or _title_key(name)[:12] in _title_key(_full.get(cid.group(1), t))):
                line = num + name + ": " + text[k:]
                n += 1
            elif t:
                line = f"{num}{t}: {text}"
                n += 1
        elif t:  # 한글로 시작 — 이름 없음: 인용 논문 제목을 붙인다
            line = f"{num}{t}: {text}"
            n += 1
        out.append(line)
    return head + "\n".join(out) + tail, n
