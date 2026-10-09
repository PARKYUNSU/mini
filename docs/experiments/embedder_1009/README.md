# 임베더 교체 — all-MiniLM-L6-v2 → bge-small-en-v1.5 (사전 등록)

- 시작일: 2026-10-09
- 선행: [`../retrieval_eval_1007/05_conclusion.md`](../retrieval_eval_1007/05_conclusion.md) — 벡터 단독 Recall@5 0.815 로 세 갈래 중 가장 약하다(BM25 대비 5:22). 하이퍼볼릭 계획([`hyperbolic` 메모](../retrieval_eval_1007/README.md) §1)의 2단계.

## 1. 후보 하나만

`BAAI/bge-small-en-v1.5` — MiniLM 과 같은 384차원·비슷한 크기, MTEB 검색 51.68 (MiniLM ≈ 42). 코퍼스와 검색어(추출 후)가 모두 영어라 영어 모델로 충분하다. 쿼리 지시문(prefix)은 붙이지 않는다 — v1.5 는 지시문 없이도 쓰도록 만들어졌고, 붙이면 운영 코드의 질의 경로 여러 곳을 바꿔야 한다.

여러 후보를 이 평가셋에서 고르면 그 자체가 튜닝이 되므로 **하나만** 잰다.

## 2. 구성

- 새 DB: `/Volumes/T7 Shield/mini-chroma-exp/bge_small` — 운영 DB 의 청크 텍스트·ID·메타데이터를 그대로 읽어 임베딩만 바꿨다 ([`scripts/build_embed_collection.py`](../../../scripts/build_embed_collection.py)). BM25 는 JSONL 기반이라 그대로다.
- 측정 시 `CHROMA_DB_PATH` 와 `EMBEDDING_MODEL` 을 함께 바꾼다 — 운영 경로의 제목 유사도·light rerank 도 같은 임베더를 쓰므로.

## 3. 측정

1. 검색 평가셋: `eval_retrieval.py --label bge_small` (영어 검색어 직접, 187/162문항). 기준선 `fix3_lr` (현행 운영과 같은 코드).
2. 한국어 끝단: `eval_e2e_ko.py --label bge_e2e` (162). 기준선 — 검색어 추출이 결정적이 된 뒤의 `det_r1` (query_determinism_1009).

## 4. 판정 (결과 전 고정)

- **주**: 검색 평가셋 **vector 갈래** Recall@5 (162) — `bge_small` vs `fix3_lr` 짝지은 McNemar, bge 쪽 p<0.05 우세. 임베더 자체의 품질 질문이다.
- **반영 조건**: 주 통과 **그리고** 운영 경로(production 갈래, 162)와 끝단(162)이 둘 다 유의하게 나쁘지 않다(옛 쪽 우세 p<0.05 가 아님).
  - production 은 0.951 로 천장 근처라 유의한 개선은 기대하지 않는다.
- 반영하면 운영 DB 를 새 임베더로 다시 만들고 인제스트 경로의 `EMBEDDING_MODEL` 도 바꾼다 (별도 작업).

## 5. 예상

- vector: 0.815 → **0.87 이상**, 유의.
- production: 0.951 ± 0.02 (BM25 주입이 이미 벡터 약점을 상당히 메운다).
- 끝단: det_r1 ± 노이즈.
