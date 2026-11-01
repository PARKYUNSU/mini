# R1 자리 플래그 정리 — 꺼진 검색 내부 코드 지우기 (사전 등록, 2026-11-01)

> 측정 **전에** 쓴다.
>
> [foundation_1031](../foundation_1031/README.md) §7 은 검색 내부 플래그 3개를 남겨 두었다. "R1(재순위 교체)이 바로 그 자리를 고치므로 그때 정리한다"는 이유였다. R1 은 [ce_rerank_1101](../ce_rerank_1101/README.md) 에서 접었다. 그래서 이번에 그 3개와 R1 에서 넣은 플래그 1개를 함께 지운다.
>
> 운영 `.env` 에는 네 플래그가 하나도 없다. 모두 기본값인 끔으로 돌고 있으므로, 지워도 동작은 바뀌지 않아야 한다.

## 1. 지우는 것

| 플래그 | 라운드 · 판정 | 지우는 코드 |
|---|---|---|
| `RAG_HYPE` · `HYPE_COLLECTION` · `HYPE_TOP_PAPERS` | hype_1014 — 효과 0 | `_hype_enabled` · `ChromaRAGTool._hype_paper_hits` · 검색의 HyPE 갈래 · `scripts/gen_hype_questions.py` · `scripts/index_hype_questions.py` |
| `RAG_FUSION_PROTECT` · `RAG_FUSION_PROTECT_K` | fusion_protect_1027 — 기각 | `_fusion_protect_pids` 와 그 테스트 |
| `CHROMA_CROSS_ENCODER_RERANK` | 청크 단위 CE(옛 기능, 기본 끔) | `agent_config` 의 설정 · `_get_cross_encoder` · `_cross_encoder_rerank` · 검색의 CE 갈래(후보 수 늘리기 · 재정렬) |
| `RAG_PAPER_CE_RERANK` | ce_rerank_1101 — 접음 | `_get_paper_ce` · `_paper_ce_rerank` · `tests/unit/test_paper_ce_rerank.py` |

- 남기는 코드: 보호 자리(`_paper_max_one_chunk_per_paper` 의 `protect_pids`). 이름 찾기(`RAG_NAME_LOOKUP`, 운영 켬)가 쓴다. 그 테스트는 `tests/unit/test_protect_pids.py` 로 이름을 바꿔 남긴다.
- 남기는 데이터: 운영 Chroma 의 HyPE 컬렉션 `paper_questions`. 지우는 일도 운영 DB 쓰기라 이번에는 하지 않는다.
- 운영 `.env` 는 바꾸지 않는다.
- 옛 측정 스크립트: `ce_rerank_1101/run.sh` 는 이제 끔과 켬 두 갈래가 같은 코드로 돈다. 지운 기능을 다시 잴 때는 정리 전 커밋에서 잰다.

## 2. 확인 — 동작이 같은가

- 단위 테스트가 전체 통과해야 한다. 지운 기능의 테스트는 빠진다.
- 검색만 대조한다(foundation_1031 §7 과 같은 방식).
  - 문항: survey_gate_1030 37문항(new 13 · old 24).
  - 방법: `--save-context` 로 검색만 잰다.
  - 순서: 정리 전 코드로 `run.sh cb`(`cb_new` · `cb_old`)를 돌린다. 코드를 정리한다. 정리 뒤 코드로 `run.sh ca`(`ca_new` · `ca_old`)를 돌린다.
  - 코퍼스: 네 실행 모두 같은 코퍼스(Chroma 1,401,935청크)에서 잰다. 실행마다 앞에서 쓰기 잠금과 청크 수를 본다.
  - 시간: 01:00 수집 전에 네 실행을 끝낸다. 끝내지 못하면 수집 뒤 처음부터 다시 잰다.
- 판정(`compare.py`): 검색어(`rag_queries`)와 경로(`route`)가 같은 문항에서 컨텍스트 논문(`doc_ids`, 순서 포함)이 모두 같으면 통과다.
  - 검색어나 경로가 다른 문항은 LLM 흔들림으로 보고 따로 센다. foundation_1031 §7 때는 37 / 37 이 같았다.
  - 검색어와 경로가 같은데 논문이 다르면 정리가 틀린 것이다. 그때는 코드를 고친다.
- 봇 재시작: 동작이 같으므로 지금은 하지 않는다. 정리된 코드는 다음 재시작 때 운영에 들어간다.

## 3. 기록

| 날짜 | 내용 |
|---|---|
| 2026-11-01 | 사전 등록 · `run.sh` · `compare.py`(13fc51f — 정리 전 코드). |
| 2026-11-01 21:15 ~ 21:54 | 정리 전 기준선 `cb_new` · `cb_old` 37행, 오류 0. Chroma 청크는 앞 · 중간 · 끝 모두 1,401,935. |
| 2026-11-01 21:5x | 코드 정리(§4). 단위 테스트 701 통과(705 에서 지운 기능의 테스트 4개가 빠짐). |
| 2026-11-01 21:57 ~ 22:38 | 정리 뒤 `ca_new` · `ca_old` 37행. `compare.py` 결과 **같음 37 · 다름 0**, 검색어 · 경로 다름 0, 오류 행 0 → 통과. Chroma 청크 1,401,935 그대로. |

## 4. 결과 — 통과

- 지운 것:
  - `core/rag/agent_chroma_rag.py` 237줄
  - `core/config/agent_config.py` 의 `CHROMA_CROSS_ENCODER_RERANK` 설정
  - `tests/unit/test_paper_ce_rerank.py`
  - `scripts/gen_hype_questions.py` · `scripts/index_hype_questions.py`
- 남긴 것: `tests/unit/test_fusion_protect.py` 는 `tests/unit/test_protect_pids.py` 로 이름을 바꾸고, 이름 찾기가 쓰는 보호 테스트만 남겼다. 보호 로그 이름도 `fusion protect:` 에서 `protect:` 로 바꿨다.
- 코드가 읽는 `RAG_` 플래그가 39개에서 35개로 줄었다(`RAG_HYPE` · `RAG_FUSION_PROTECT` · `RAG_FUSION_PROTECT_K` · `RAG_PAPER_CE_RERANK`).
- 린트(ruff F)는 정리 전과 같은 경고 2개만 남았다. 쓰지 않는 `chromadb` import 이고, 이번 변경 밖이다.
- 동작: 검색어와 경로가 같은 37문항 모두에서 컨텍스트 논문이 순서까지 같았다.
- 봇은 재시작하지 않았다. 정리된 코드는 다음 재시작 때 운영에 들어간다.
- 커밋에 안 들어간 로컬 도우미 `.cron/run_hype_gen.sh` 는 지운 스크립트를 부르므로 이제 돌지 않는다. HyPE 를 다시 잴 때는 13fc51f 에서 잰다.
