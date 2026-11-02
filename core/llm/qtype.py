"""질문 유형 분류기 — 목록 · 비교 · 수치 (docs/experiments/qtype_1102, ``RAG_QTYPE_CLF``).

정규식 게이트(``presence_judge._GATE_*``)는 말투가 바뀔 때마다 구멍이 났다: 전제 속 "0%" · "얼마나" 를 수치로,
"모델과 … 달라" · "…비교한 연구 있어?" 를 비교로 잡아 판정을 건너뛰고 엉뚱한 두 대상을 따로 검색했다
(answer_review_1030 §2, 실사용 job 137–140). 라벨 단 질문(``qtype_train.tsv``)으로 글자 · 낱말 n-gram
로지스틱 회귀를 처음 부를 때 학습한다(1초 안팎). LLM 호출 · 내려받기 없음.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

__all__ = ["predict"]

_TRAIN = Path(__file__).with_name("qtype_train.tsv")


@lru_cache(maxsize=1)
def _models():
    from scipy.sparse import hstack
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    rows = [line.rstrip("\n").split("\t", 1) for line in _TRAIN.open(encoding="utf-8") if line.strip()]
    texts = [q for _, q in rows]
    vecs = [TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 4), sublinear_tf=True),
            TfidfVectorizer(analyzer="word", token_pattern=r"\S+", ngram_range=(1, 2), sublinear_tf=True)]
    x = hstack([v.fit_transform(texts) for v in vecs]).tocsr()
    models = {t: LogisticRegression(C=10, class_weight="balanced", max_iter=3000).fit(x, [t in lab for lab, _ in rows])
              for t in "LCN"}
    return vecs, models, hstack


@lru_cache(maxsize=512)
def predict(question: str) -> frozenset[str]:
    """질문이 해당하는 유형 글자들: ``L`` 목록 · 조사, ``C`` 두 대상 비교, ``N`` 수치. 비어 있으면 특정 연구 · 개념."""
    vecs, models, hstack = _models()
    x = hstack([v.transform([question or ""]) for v in vecs]).tocsr()
    return frozenset(t for t, m in models.items() if m.predict(x)[0])
