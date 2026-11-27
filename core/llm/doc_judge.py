"""'없음' 판정을 문서별 직접/부분/무관 판정 집계로 (RAG_JUDGE_AGG, docs/experiments/judge_agg_1117).

답에 들어가는 문서마다 큰 판정 모델(기본 27B, 생각 끔)이 직접 · 부분 · 무관을 고르고,
직접 ≥ 1 → (a) · 부분만 → (b) · 전부 무관 → (c). 프롬프트는 doc_judge_1117 dev 에서 고정한 것 그대로.
"""
from __future__ import annotations

import json
import os
import re

PROMPT = """사용자 질문과 검색된 논문 목록이 있다. 논문마다 질문에 대한 관련도를 하나로 판정하라.
- 직접: 논문이 질문의 핵심 물음을 주제와 대상(분야 · 문서 유형 · 언어 · 비교 대상 등 질문의 조건)까지 맞춰 직접 연구 · 제안 · 평가한다.
- 부분: 질문의 일부(하위 물음 하나, 비슷한 과제, 다른 분야나 조건에서의 같은 방법)만 다뤄 답에 참고가 된다. 질문 조건 하나라도 다르면 부분이다.
- 무관: 질문에 답할 근거가 없다. 주제 단어만 겹치고 묻는 것과 다른 문제를 다루면 무관이다.

질문: {q}

논문:
{docs}

JSON 으로만 답하라: {{"판정": [{{"번호": 1, "관련도": "직접|부분|무관"}}, ...]}}"""
SCHEMA = {"type": "object", "properties": {"판정": {"type": "array", "items": {"type": "object",
          "properties": {"번호": {"type": "integer"}, "관련도": {"type": "string", "enum": ["직접", "부분", "무관"]}},
          "required": ["번호", "관련도"]}}}, "required": ["판정"]}
_LAB = {"직접": "D", "부분": "P", "무관": "N"}


def judge_agg_active() -> bool:
    return os.getenv("RAG_JUDGE_AGG", "0").strip() == "1"


def doc_blocks(rag_context: str, limit: int = 900) -> list[tuple[int, str]]:
    """``[문서 N]`` 블록 → [(N, '제목\\n초록 limit 자')]."""
    out = []
    for m in re.finditer(r"\[문서 (\d+)\]\n(.*?)(?=\n\[문서 \d+\]\n|\Z)", rag_context or "", re.S):
        b = m.group(2)
        t = re.search(r"\[\d{4}\.\d{4,5}(?:v\d+)?\]\s*(.*)", b)
        ab = re.sub(r"\s+", " ", b.split("[초록]", 1)[-1] if "[초록]" in b else b).strip()[:limit]
        out.append((int(m.group(1)), (t.group(1).strip() if t else "") + "\n" + ab))
    return out


def aggregate(labels: dict[int, str]) -> tuple[str, int | str]:
    """{문서 번호: D/P/N} → ('a', 첫 직접 문서 번호) · ('b', '없음') · ('c', '없음')."""
    direct = sorted(n for n, x in labels.items() if x == "D")
    if direct:
        return "a", direct[0]
    return ("b" if "P" in labels.values() else "c"), "없음"


def judge_docs(question: str, rag_context: str) -> dict[int, str] | None:
    """문서마다 D/P/N. 실패하면 None — 호출 쪽은 기존 판정으로."""
    import requests

    from core.config.agent_config import ollama_kwargs

    blocks = doc_blocks(rag_context)
    if not blocks:
        return None
    kw = ollama_kwargs()
    docs = "\n\n".join(f"[{i}] {text}" for i, (_, text) in enumerate(blocks, 1))
    try:
        r = requests.post(f"{kw['base_url']}/api/chat", json={
            "model": os.getenv("RAG_DOC_JUDGE_MODEL", "qwen3.6:27b-q4_K_M"), "stream": False, "think": False,
            "format": SCHEMA, "keep_alive": kw["keep_alive"], "options": {"temperature": 0, "num_ctx": 8192},
            "messages": [{"role": "user", "content": PROMPT.format(q=question, docs=docs)}]}, timeout=120)
        got = {x["번호"]: x["관련도"] for x in json.loads(r.json()["message"]["content"])["판정"]}
    except Exception as e:  # noqa: BLE001 — 판정 실패는 기존 판정으로 넘긴다
        print(f"[WARN] doc_judge 실패: {e}")
        return None
    if len(got) < len(blocks):
        return None
    return {n: _LAB.get(got.get(i), "P") for i, (n, _) in enumerate(blocks, 1)}


def agg_slots_active() -> bool:
    return os.getenv("RAG_AGG_SLOTS", "0").strip() == "1"


_NO_INTRO = "제공된 문서에는 질문이 찾는 연구가 없습니다."
_NO_CONCL = "따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다."


def rec_active() -> bool:
    return os.getenv("RAG_REC_MODE", "0").strip() == "1"


# 추천형 질문(6차 H16–H19 👎 0/4): 모델 · 도구 · 방법 이름을 골라 달라는 요청. "추천 시스템" 같은 주제어는 안 잡게 동사꼴만.
_REC = re.compile(r"추천\s*(?:해|좀|부탁|받|할\s*만)|뭘?\s*(?:써야|쓰면\s*좋)|어떤\s*(?:걸|것을?|모델|도구|툴|라이브러리|프레임워크)[^?]{0,15}(?:써야|쓰면|좋을까|좋아)")
REC_CONCL_RULE = "- 추천 질문이다. 마지막 문장은 '…이 필요하면 A, …이면 B' 꼴로 상황별로 무엇을 쓸지 권고한다. 권고 근거는 위 논문 결과만 쓴다.\n"


def is_recommend(question: str) -> bool:
    return rec_active() and bool(_REC.search(question or ""))


def agg_slots_template(labels: dict[int, str], agg: str, rec: bool = False) -> str:
    """판정대로 답 칸 (RAG_AGG_SLOTS, docs/experiments/agg_slots_1117): 직접 · 부분 문서마다 한 칸, 무관 문서는 칸 없음.

    rec(추천형, RAG_REC_MODE): 칸을 '후보 이름 / 무엇인지 / 근거 / 한계·조건' 으로, 결론은 상황별 권고로.
    """
    keep = [n for n in sorted(labels) if labels[n] in ("D", "P")][:5]
    if agg == "c" or not keep:
        intro, body, concl = f"`{_NO_INTRO}` 를 그대로 쓴다.", "질문과 관련된 문서가 없습니다.", f"`{_NO_CONCL}` 를 그대로 쓴다."
    else:
        tag = lambda n: " (관련 연구)" if labels[n] == "P" else ""
        slot = ("**{후보 이름(모델 · 도구 · 방법)}**{tag}: 무엇인지 한 문장 · 문서의 근거 결과 한 문장 · 한계나 쓸 조건 한 문장"
                if rec else "**{{핵심 접근·시스템 이름}}**{tag}: 무엇을 했고 결과가 무엇인지 1~2문장")
        body = "\n".join(f"{i}. " + slot.replace("{tag}", tag(n)).replace("{{", "{").replace("}}", "}") + f" [문서 {n}]"
                         for i, n in enumerate(keep, 1))
        if rec:
            concl_a = "상황별로 무엇을 쓰면 좋은지 권고 2~3문장('…이 필요하면 A, …이면 B'). 권고 근거는 위 항목의 결과만 쓴다."
        else:
            concl_a = "위 항목들을 종합해 질문에 답하는 한 단락. 문서에 없는 처방을 지어내지 마세요."
        if agg == "b":
            concl_b = f"첫 문장은 `{_NO_CONCL}` 를 그대로 쓰고, 위 관련 연구가 질문의 어느 부분과 닿는지 한 문장."
            if rec:
                concl_b += " 그다음 위 관련 연구 중 조건이 맞을 때 쓸 만한 것을 '…이면 A' 꼴로 한 문장."
            intro, concl = f"첫 문장은 `{_NO_INTRO}` 를 그대로 쓴다.", concl_b
        else:
            intro, concl = "질문이 가리키는 문제와 왜 어려운지 1~2문장. 핵심 용어는 **굵게**.", concl_a
    return f"""[다중 문서 출력 템플릿 지시사항 - 판정된 문서별 칸]
아래 뼈대를 그대로 따라 값만 채우세요.

[출력 템플릿]
### 서론
{intro}

### 본론
{body}

### 결론
{concl}

[규칙]
- 본론의 칸은 모두 채운다. 칸을 빼거나 더하지 않는다. 칸 끝의 `[문서 k]` 는 그대로 둔다.
- 각 칸에는 그 문서에 있는 내용만 쓴다. **arXiv ID 를 옮겨 적지 마세요.**
- `(관련 연구)` 표시는 그대로 둔다.
- 중괄호 안의 안내 문구는 출력 금지.
"""


_C_BODY_ID = re.compile(r"(관련된 문서가 없습니다\.?)[ \t]*(?:\[[^\]\n]*\][ \t]*)+")


def strip_no_doc_ids(answer: str) -> tuple[str, int]:
    """(c) 틀의 "질문과 관련된 문서가 없습니다." 뒤에 v13 이 붙인 인용 꼬리를 지운다 (agg_slots_1117 §6 결함)."""
    return _C_BODY_ID.subn(r"\1", answer or "")


def ext_promote_active() -> bool:
    return os.getenv("RAG_EXT_PROMOTE", "0").strip() == "1"


def ext_promote_a_active() -> bool:
    """판정 (a) 직접 있음이어도 외부 승격 (RAG_EXT_PROMOTE_A, ext_promote_a_1124)."""
    return os.getenv("RAG_EXT_PROMOTE_A", "0").strip() == "1"


def ext_list_judge_active() -> bool:
    """📎 DB 밖 목록도 27B 로 판정해 무관은 뺀다 (RAG_EXT_LIST_JUDGE, ext_promote_a_1124)."""
    return os.getenv("RAG_EXT_LIST_JUDGE", "0").strip() == "1"


def judge_external_list(question: str, items: list[dict]) -> tuple[list[dict], int]:
    """📎 후보 중 초록 있는 것을 27B 로 판정해 무관(N)은 뺀다. 초록 없는 후보 · 판정 실패는 그대로 둔다. (남긴 것, 뺀 수)."""
    judged = [(k, it) for k, it in enumerate(items) if len(it.get("abstract") or "") >= 200]
    if not judged:
        return items, 0
    ctx = "\n\n---\n\n".join(f"[문서 {n}]\n[{it.get('arxiv') or ''}] {it.get('title') or ''}\n[초록] {it['abstract']}"
                             for n, (_, it) in enumerate(judged, 1))
    got = judge_docs(question, ctx)
    if not got:
        return items, 0
    drop = {k for n, (k, _) in enumerate(judged, 1) if got.get(n) == "N"}
    return [it for k, it in enumerate(items) if k not in drop], len(drop)


def promote_external(question: str, query: str, rag_context: str, doc_ids: dict, labels: dict,
                     years=None, max_cands: int = 4, max_keep: int = 2, items: list[dict] | None = None):
    """DB 밖(OpenAlex) 후보를 27B 로 판정해 직접 · 부분이면 컨텍스트에 붙인다 (RAG_EXT_PROMOTE, docs/experiments/ext_promote_1117).

    반환: (rag_context, doc_ids, labels, 올린 [{arxiv, title, label}]). 실패하면 입력 그대로 · 빈 목록.
    shortcut: arXiv ID 있는 후보만 올린다 — 학회판(DOI 만)은 인용 · 링크 형식이 arXiv 기준이라 뺀다.
    """
    from core.rag.external_search import search_openalex

    titles = set(re.findall(r"\[\d{4}\.\d{4,5}(?:v\d+)?\]\s*([^\[\n]+)", rag_context or ""))
    if items is None:  # 미리 찾아 둔 결과가 없으면 지금 찾는다
        items = search_openalex(query, {str(p) for p in doc_ids.values()}, exclude_titles=titles, years=years)
    cands = [it for it in items if it.get("arxiv") and len(it.get("abstract") or "") >= 200][:max_cands]
    if not cands:
        return rag_context, doc_ids, labels, []
    start = max(doc_ids) + 1 if doc_ids else 1
    blocks = {start + i: f"[문서 {start + i}]\n[{c['arxiv']}] {c['title']}\n[초록] {c['abstract']}" for i, c in enumerate(cands)}
    got = judge_docs(question, "\n\n".join(blocks.values()))
    if not got:
        return rag_context, doc_ids, labels, []
    keep = [n for n in sorted(got) if got[n] in ("D", "P")][:max_keep]
    if not keep:
        return rag_context, doc_ids, labels, []
    doc_ids, labels, added = dict(doc_ids), dict(labels), []
    for k, n in enumerate(keep):
        num = (max(doc_ids) + 1) if doc_ids else 1
        c = cands[n - start]
        # 다른 블록과 같은 구분자 — 없으면 _blocks 가 앞 문서에 합쳐 항목 다시 쓰기 · 칸 채우기가 엉뚱한 초록을 본다(slot_fill_1124)
        rag_context = rag_context.rstrip() + "\n\n---\n\n" + blocks[n].replace(f"[문서 {n}]", f"[문서 {num}]", 1)
        doc_ids[num] = c["arxiv"]
        labels[num] = got[n]
        added.append({"arxiv": c["arxiv"], "title": c["title"], "label": got[n]})
    return rag_context, doc_ids, labels, added


# 추천 · 방법 질문은 9B 선별(15→5)에서 평가 프레임워크 같은 핵심 논문이 빠졌다(7차 회신 §4, H18 RAGChecker · RAGAS).
# RAG_REC_POOL=N 이면 거르기를 통과한 상위 N 편을 27B 로 먼저 판정해 직접 > 부분 > 무관 순으로 5편을 고른다(기본 0 = 끔).
_METHOD = re.compile(r"방법|어떻게|어떤\s*(?:지표|방식|기법|척도)")


def rec_pool_n() -> int:
    try:
        return max(0, int(os.getenv("RAG_REC_POOL", "0").strip() or 0))
    except ValueError:
        return 0


def is_rec_or_method(question: str) -> bool:
    return bool(_REC.search(question or "") or _METHOD.search(question or ""))


def judge_pool_order(question: str, blocks: list[str], numbered: str) -> list[str] | None:
    """번호 붙인 후보 컨텍스트를 27B 로 판정 → 블록을 D, P, N 순(같은 라벨은 검색 순위)으로. 실패하면 None."""
    labels = judge_docs(question, numbered)
    if not labels:
        return None
    rank = {"D": 0, "P": 1, "N": 2}
    order = sorted(range(len(blocks)), key=lambda i: (rank.get(labels.get(i + 1, "P"), 1), i))
    return [blocks[i] for i in order]


# 구조 판정 (7차 회신 §2, .cron/work_1127/judge_struct.py): 27B 는 핵심 과제 일치만 보고, 조건은 조건 판정 결과로,
# D/P/N 은 규칙으로 — 맞음 + 조건 모두 충족 → D · 맞음 + 조건 미충족 → P · 인접 → P · 아님 → N.
# 확정 라벨 104쌍: 일치 73.1→76.0% · P→D 8→7 · P→N 15→5 · N→P/D 2→9 (RAG_JUDGE_STRUCT, 기본 0).
TASK_PROMPT = """사용자 질문과 검색된 논문 목록이 있다. 논문마다 질문의 **핵심 과제**와 맞는지 하나로 판정하라.
- 맞음: 논문이 질문의 핵심 과제 자체를 연구 · 제안 · 평가한다.
- 인접: 핵심 과제 자체는 아니지만, 비슷한 과제나 일부 하위 과제를 다뤄 답에 쓸 만한 근거를 준다.
- 아님: 주제 단어만 겹치고 질문에 쓸 만한 근거가 없다.
언어 · 문서 유형 · 분야 · 비교 대상 같은 조건은 따로 확인하니 여기서는 보지 말고 과제만 보라.

질문: {q}

논문:
{docs}

JSON 으로만 답하라: {{"판정": [{{"번호": 1, "과제": "맞음|인접|아님"}}, ...]}}"""
TASK_SCHEMA = {"type": "object", "properties": {"판정": {"type": "array", "items": {"type": "object",
               "properties": {"번호": {"type": "integer"}, "과제": {"type": "string", "enum": ["맞음", "인접", "아님"]}},
               "required": ["번호", "과제"]}}}, "required": ["판정"]}


def struct_active() -> bool:
    return os.getenv("RAG_JUDGE_STRUCT", "0").strip() == "1"


def judge_task(question: str, rag_context: str, prompt: str | None = None) -> dict[int, str] | None:
    """문서마다 맞음/인접/아님 (문서 번호 기준). 실패하면 None. prompt 없으면 TASK_PROMPT."""
    import requests

    from core.config.agent_config import ollama_kwargs

    blocks = doc_blocks(rag_context)
    if not blocks:
        return None
    kw = ollama_kwargs()
    docs = "\n\n".join(f"[{i}] {text}" for i, (_, text) in enumerate(blocks, 1))
    try:
        r = requests.post(f"{kw['base_url']}/api/chat", json={
            "model": os.getenv("RAG_DOC_JUDGE_MODEL", "qwen3.6:27b-q4_K_M"), "stream": False, "think": False,
            "format": TASK_SCHEMA, "keep_alive": kw["keep_alive"], "options": {"temperature": 0, "num_ctx": 8192},
            "messages": [{"role": "user", "content": (prompt or TASK_PROMPT).format(q=question, docs=docs)}]}, timeout=150)
        got = {x["번호"]: x["과제"] for x in json.loads(r.json()["message"]["content"])["판정"]}
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] 과제 판정 실패: {e}")
        return None
    return {n: got.get(i, "인접") for i, (n, _) in enumerate(blocks, 1)}


# 조건부 승격 (11-28 회신, .cron/work_1127e/report_fs.md): 운영 판정은 그대로 두고, 운영 N 이면서
# few-shot 과제 판정 + 조건 → P 이고 그 문서가 일반 명사 아닌 명시 조건 하나 이상을 다루면 P 로만 올린다(D 는 안 낮춤).
# 확정 라벨 103쌍(기존 결과 계산): 일치 72.8→77.7% · P→N 15→10 · N→P/D 2 그대로 (RAG_COND_PROMOTE, 기본 0).
TASK_FS_PROMPT = """사용자 질문과 검색된 논문 목록이 있다. 논문마다 질문의 **핵심 과제**와 맞는지 하나로 판정하라.
- 맞음: 논문이 질문의 핵심 과제 자체를 연구 · 제안 · 평가한다.
- 인접: 핵심 과제 자체는 아니지만, 비슷한 과제나 일부 하위 과제를 다뤄 답에 쓸 만한 근거를 준다.
  질문이 말한 언어 · 문서 유형 · 분야의 데이터셋, 벤치마크, 분류 · 추출 연구는 핵심 물음(예: 옮길 때 성능 저하, 두 방법 비교)을 직접 재지 않아도 **인접**이다.
- 아님: 주제 단어만 겹치고 질문에 쓸 만한 근거가 없다. 다른 분야 · 다른 과제에서 같은 단어만 나오면 아님이다.
언어 · 문서 유형 · 분야 · 비교 대상 같은 조건이 맞는지는 따로 확인하니, 여기서는 과제가 얼마나 가까운지만 보라.

예시 (논문 내용은 요약):
질문: 영어 판례로 학습한 요약 모델을 일본어 판결문에 쓰면 품질이 얼마나 떨어져?
- "일본어 판결문 요약 데이터셋 구축과 기준 모델" → 인접 (질문의 언어 · 문서 유형과 같은 데이터셋 · 과제 연구, 성능 저하는 직접 안 잼)
- "다국어 법률 문서 분류에서 언어 간 전이 성능 비교" → 인접 (언어 간 전이를 재지만 요약이 아니라 분류)
- "영어 판례 요약 모델을 일본어 · 한국어 판결문에 옮겼을 때 ROUGE 하락 분석" → 맞음
- "일본어 뉴스 기사 감성 분석" → 아님 (언어만 같고 문서 유형 · 과제가 다름)
질문: 의료 상담 챗봇 답변의 환각을 자동으로 잡는 방법 있어?
- "의료 질의응답 데이터셋에서 LLM 답변 사실성 평가 벤치마크" → 인접 (같은 분야의 답변 사실성 평가)
- "일반 도메인 LLM 환각 탐지기 제안" → 인접 (분야는 다르지만 같은 과제)
- "의료 영상 분할 모델의 오류 분석" → 아님 (분야 단어만 같음)

질문: {q}

논문:
{docs}

JSON 으로만 답하라: {{"판정": [{{"번호": 1, "과제": "맞음|인접|아님"}}, ...]}}"""


def cond_promote_active() -> bool:
    return os.getenv("RAG_COND_PROMOTE", "0").strip() == "1"


def promote_labels(labels: dict[int, str], conds: list[dict], fs: dict[int, str]) -> dict[int, str]:
    """운영 N · fs P · 일반 명사 아닌 조건 하나 이상 다룸 → P. 나머지는 운영 라벨 그대로."""
    from core.llm.cond_keep import _GENERIC

    cov = {n for c in conds or [] if c.get("값", "").strip() not in _GENERIC for n in c.get("다룬 논문") or []}
    return {n: "P" if lab == "N" and fs.get(n) == "P" and n in cov else lab for n, lab in labels.items()}


def promote_by_conditions(question: str, rag_context: str, labels: dict[int, str], conds: list[dict] | None):
    """조건부 승격. 일반 명사 아닌 명시 조건이 있고 운영 N 이 있을 때만 few-shot 과제 판정(27B 1회)을 더 부른다.
    반환: (라벨, 올린 문서 번호 목록)."""
    from core.llm.cond_keep import _GENERIC

    if not labels or "N" not in labels.values() or not any(c.get("값", "").strip() not in _GENERIC for c in conds or []):
        return labels, []
    task = judge_task(question, rag_context, TASK_FS_PROMPT)
    if not task:
        return labels, []
    new = promote_labels(labels, conds, combine_struct(task, conds))
    return new, [n for n in new if new[n] != labels[n]]


def combine_struct(task: dict[int, str], conds: list[dict]) -> dict[int, str]:
    """과제 판정 + 조건 판정([{값, 다룬 논문}]) → D/P/N."""
    out = {}
    for n, t in task.items():
        if t == "아님":
            out[n] = "N"
        elif t == "인접":
            out[n] = "P"
        else:
            out[n] = "D" if all(n in (c.get("다룬 논문") or []) for c in conds) else "P"
    return out
