"""BM25 전용 경량 쿼리 확장 — 약어·짧은 토큰을 풀어쓴 구문을 덧붙여 키워드 적합도를 올린다.

벡터 쿼리에는 적용하지 않는다 (의미 검색 노이즈 방지).

멀티 쿼리 검색: ``build_multi_query_retrieval_queries`` — survey / benchmark / framework / method
등 의도를 분리한 벡터·BM25 후보 합집합용.
"""

from __future__ import annotations

import os
import re

# BM25 전용: 짧은 꼬리 키워드 (벡터 쿼리에는 붙이지 않음)
_ENABLE_BM25_TAIL_RAW = (os.getenv("ENABLE_BM25_GENERIC_TAIL") or "1").strip().lower()
ENABLE_BM25_GENERIC_TAIL = _ENABLE_BM25_TAIL_RAW in ("1", "true", "yes", "on")

BM25_GENERIC_TAIL_KEYWORDS: tuple[str, ...] = (
    "survey",
    "benchmark",
    "comparison",
    "analysis",
    "evaluation",
    "method",
    "framework",
    "approach",
)

# 멀티 쿼리 검색: (의도 라벨, 벡터·BM25에 그대로 쓸 쿼리 문자열)
# survey / benchmark / framework / method 를 명시적으로 분리해 recall 후보를 넓힌다.
_MULTI_QUERY_INTENT_SUFFIXES: tuple[tuple[str, str], ...] = (
    ("survey", "survey systematic review overview literature"),
    ("benchmark", "benchmark evaluation metrics dataset"),
    ("framework", "framework architecture pipeline design"),
    ("method", "method approach algorithm methodology"),
)


def _intent_redundant_for_multi_query(base_lower: str, intent_label: str) -> bool:
    """이미 쿼리에 해당 의도가 강하게 있으면 중복 변형 생략."""
    if intent_label == "survey":
        return bool(re.search(r"\b(survey|systematic\s+review|overview|literature\s+review)\b", base_lower))
    if intent_label == "benchmark":
        return "benchmark" in base_lower and (
            "evaluation" in base_lower or "metric" in base_lower or "dataset" in base_lower
        )
    if intent_label == "framework":
        return "framework" in base_lower or "pipeline" in base_lower
    if intent_label == "method":
        return bool(re.search(r"\b(method|approach|algorithm|methodology)\b", base_lower))
    return False


def build_multi_query_retrieval_queries(
    base_search_query: str,
    *,
    max_queries: int = 6,
) -> list[tuple[str, str]]:
    """단일 검색어를 의도별 쿼리 목록으로 확장. (intent_label, query_text).

    첫 항목은 항상 ``base``. 이후 survey / benchmark / framework / method 변형을 추가한다.
    짧은 쿼리는 base만 반환한다.
    """
    base = (base_search_query or "").strip()
    if not base:
        return []
    base_l = base.lower()
    if len(base) < 8:
        return [("base", base)]

    out: list[tuple[str, str]] = [("base", base)]
    seen: set[str] = {base.lower()}

    for label, suffix in _MULTI_QUERY_INTENT_SUFFIXES:
        if _intent_redundant_for_multi_query(base_l, label):
            continue
        q = re.sub(r"\s+", " ", f"{base} {suffix}".strip())
        if len(q) < 10:
            continue
        kl = q.lower()
        if kl in seen:
            continue
        seen.add(kl)
        out.append((label, q))
        if len(out) >= max(1, max_queries):
            break

    return out[: max(1, max_queries)]

# (소문자 키, 확장 구문). 긴 키를 먼저 매칭하도록 아래 정렬 유지.
BM25_PHRASE_EXPANSIONS: tuple[tuple[str, str], ...] = (
    ("self-rag", "Self-Reflective Retrieval Augmented Generation"),
    ("self rag", "Self-Reflective Retrieval Augmented Generation"),
    ("crag", "Corrective Retrieval Augmented Generation"),
    ("dpr", "Dense Passage Retrieval"),
    ("colbert", "ColBERT"),
    ("ragas", "RAGAS retrieval evaluation"),
    ("hyde", "Hypothetical Document Embeddings"),
    ("specter", "SPECTER scientific document embedding"),
)


# 일반·광범위 주제 쿼리에만 BM25 키워드 다양화 (벡터에는 비적용).
BM25_GENERIC_INTENT_TAIL = (
    "survey systematic review overview benchmark evaluation metrics "
    "methodology experimental results accuracy improvement "
    "state of the art comparison analysis "
    "method framework approach architecture design"
)


def _expand_generic_bm25_intent(query: str) -> str:
    """RAG/검색 일반어처럼 수백 편이 걸리는 쿼리에 조사·벤치·방법론 힌트를 붙인다."""
    q_orig = (query or "").strip()
    if not q_orig or len(q_orig) < 12:
        return q_orig

    norm = q_orig.lower()
    norm_spaced = re.sub(r"[-_]+", " ", norm)
    # 이미 구체적이면 확장 안 함
    if re.search(r"\b\d{4}\.\d{4,5}\b", norm):
        return q_orig

    generic = False
    if "retrieval augmented generation" in norm or "retrieval-augmented" in norm:
        generic = True
    elif "retrieval" in norm and "generation" in norm:
        generic = True
    elif re.search(r"(?<![a-z0-9가-힣])rag(?![a-z0-9가-힣])", norm_spaced):
        generic = True
    elif "retrieval" in norm and (
        "accuracy" in norm or "improve" in norm or "improving" in norm or "quality" in norm
    ):
        generic = True
    elif "question answering" in norm and "retrieval" in norm:
        generic = True

    if not generic:
        return q_orig

    tail_l = BM25_GENERIC_INTENT_TAIL.lower()
    if all(part in norm for part in ("survey", "benchmark")):  # 이미 매우 긴 힌트
        return q_orig
    # tail 단어가 대부분 이미 있으면 생략
    tail_tokens = set(tail_l.split())
    q_tokens = set(norm_spaced.split())
    if len(tail_tokens & q_tokens) >= 5:
        return q_orig

    return f"{q_orig} {BM25_GENERIC_INTENT_TAIL}"


def _append_bm25_short_tail(query: str) -> str:
    """BM25 전용: 짧은 일반 키워드 꼬리 (ENABLE_BM25_GENERIC_TAIL)."""
    if not ENABLE_BM25_GENERIC_TAIL:
        return query
    q = (query or "").strip()
    if len(q) < 8:
        return q
    low = q.lower()
    to_add = [w for w in BM25_GENERIC_TAIL_KEYWORDS if w not in low]
    if not to_add:
        return q
    return f"{q} {' '.join(to_add)}"


def expand_query_for_bm25(query: str) -> str:
    """약어 확장 + (해당 시) 일반 주제 BM25 의도 확장. 벡터 쿼리에는 쓰지 않는다."""
    q_orig = (query or "").strip()
    if not q_orig:
        return q_orig

    norm = q_orig.lower()
    norm_spaced = re.sub(r"[-_]+", " ", norm)
    additions: list[str] = []
    seen_expansion_lower: set[str] = set()

    for phrase, expansion in BM25_PHRASE_EXPANSIONS:
        ph = phrase.lower()
        ph_alt = ph.replace("-", " ")
        pat = (
            rf"(?<![a-z0-9가-힣])(?:{re.escape(ph)}|{re.escape(ph_alt)})(?![a-z0-9가-힣])"
        )
        if not re.search(pat, norm_spaced):
            continue
        ex_l = expansion.lower()
        if ex_l in norm or ex_l in seen_expansion_lower:
            continue
        additions.append(expansion)
        seen_expansion_lower.add(ex_l)

    if additions:
        q_orig = f"{q_orig} {' '.join(additions)}"

    q_orig = _expand_generic_bm25_intent(q_orig)
    return _append_bm25_short_tail(q_orig)
