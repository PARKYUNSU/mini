"""일상어 → 분야 용어 사전 (docs/experiments/query_glossary_1029).

9B 검색어 LLM 은 일상어를 직역해("duplicate content detection") 분야 용어를 못 만든다.
질문(한국어)에 사전 키가 있고 검색어에 그 용어가 없으면 검색어 뒤에 붙인다 — 검색어는 바꾸지 않는다
(검색어를 통째로 바꾼 query_extract_1021 은 162 ok 135→119 로 기각).
"""
import re

# (질문 정규식, 붙일 영어 용어) — 측정 전 고정
GLOSSARY = [
    (r"중복|거의\s*(?:똑같|같은)\s*문서", "near-duplicate detection deduplication"),
    (r"같은\s*(?:사람|대상|상품|개체|레코드|항목|인물)|동일\s*(?:인물|개체|대상)", "entity resolution entity matching"),
    (r"(?:열|컬럼|칼럼|스키마).{0,15}(?:맞추|매칭|같은\s*뜻)", "schema matching"),
    (r"(?:비슷한|유사한)\s*(?:쌍|것끼리)", "similarity join"),
    (r"모른다고|답이\s*없을\s*때|답을\s*(?:거부|안\s*하)", "abstention unanswerable questions"),
    (r"근거(?:하지\s*않|가\s*없|\s*없)|문서에\s*없는\s*내용", "faithfulness grounding"),
    (r"출처|인용", "citation attribution"),
    (r"지어내|없는\s*사실|거짓\s*(?:답|정보)", "hallucination"),
    (r"긴\s*(?:문서|컨텍스트|문맥)|중간에\s*있는\s*정보", "long-context lost in the middle"),
    (r"(?:문서를?|글을?)\s*(?:자르|쪼개|나누)|청크", "chunking"),
    (r"순위를?\s*다시|다시\s*정렬|재정렬", "reranking"),
    (r"질문을?\s*(?:바꿔|다시\s*써|고쳐\s*써)|질문\s*재작성", "query rewriting"),
    (r"여러\s*(?:단계|번)\s*(?:검색|찾)|단계별로\s*찾", "multi-hop iterative retrieval"),
    (r"검색(?:이|을)?\s*(?:필요한지|할지)", "adaptive retrieval"),
    (r"(?:표|테이블)(?:에서|를|을|로)?\s*(?:질문|답|찾)", "table question answering"),
    (r"(?:컨텍스트|프롬프트|문맥)(?:를|을)?\s*(?:줄이|압축)", "context compression"),
    (r"작은\s*모델(?:에|로)\s*(?:가르|옮기|전달)", "knowledge distillation"),
    (r"확신|자신감|얼마나\s*확실", "confidence calibration uncertainty"),
    (r"관련\s*없는\s*문서|노이즈\s*문서|방해\s*문서", "irrelevant context robustness"),
    (r"이전\s*대화|대화\s*기록|장기\s*기억", "long-term memory"),
    (r"도구를?\s*(?:쓰|호출|사용)|API\s*호출", "tool use function calling"),
]
_COMPILED = [(re.compile(p), t) for p, t in GLOSSARY]
MAX_ADD = 2


def add_field_terms(question: str, query: str) -> str:
    """질문에 맞는 용어를 검색어 뒤에 최대 2개 붙인다. 이미 검색어에 있는 용어 · 한국어 폴백 검색어는 건드리지 않는다."""
    if not query or re.search(r"[가-힣]", query):
        return query
    low = query.lower()
    add = []
    for rx, term in _COMPILED:
        if len(add) >= MAX_ADD:
            break
        if rx.search(question or "") and term.split()[0] not in low and term not in add:
            add.append(term)
    return ", ".join([query] + add)
