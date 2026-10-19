# OpenResearch(`orx`) 사용 정책 (2026-10-14)

alphaXiv OpenResearch CLI 를 **문헌 조사 도구**로만 쓴다. 근거와 첫 사용 기록: [`docs/experiments/lit_review_1014/`](../docs/experiments/lit_review_1014/).

## 설치 상태

- 맥미니 `~/orx/bin/orx` (v0.2.18, `OPENRESEARCH_CLI_NO_MODIFY_PATH=1` 로 설치 — 셸 PATH·프로필 무변경). 설치 스크립트 원본 `~/orx_install/install.sh`.
- 사용 통계 끔(`orx telemetry off`). **로그인 안 함**(`orx login` 금지 — 문헌 검색에는 필요 없다).
- 작업 폴더 `~/orx_lit` (운영 저장소·DB 와 분리). 남길 결과는 `docs/experiments/<라운드>/raw/` 로 복사해 커밋.

## 허용

| 명령 | 용도 |
|---|---|
| `orx discover embedding "<질문>"` · `keyword` · `openalex` | 개선 라운드 **사전 등록 전** 근거 논문 찾기, 실패 유형별 기법 조사 |
| `orx paper <arXiv id>` | 고른 논문의 본문·세부(프롬프트, 하이퍼파라미터) 확인 |
| `orx skill <모듈>` | 사용법 읽기 |

## 금지

- 운영 Chroma(서버 `com.mini.chroma`)·`.env`·봇 코드에 `orx` 를 붙이지 않는다 — 2026-10-14 다중 프로세스 손상 사고 이후 운영 DB 에 붙는 프로세스를 늘리지 않는다.
- `orx exp` · `orx up` 실험 트리, `orx compute` · `orx instance` 원격 실행, `orx agent spawn` — 자동 실험·자동 채택 금지. 채택은 지금처럼 **사전 등록 → 짝 검정 → 사용자 승인**.
- `orx login` 및 계정·관리형 컴퓨트.

## 승인된 추가 용도 (2026-10-20 사용자 승인)

- **코퍼스 수집 후보 찾기**: `orx discover` 로 질문별 후보 논문(arXiv ID)을 찾아 목록을 만든다(docs/experiments/corpus_seed_1020). `orx` 는 목록만 만들고, 실제 수집은 우리 파이프라인(`apps/backfill/ingest_classics.py --ids`)이 한다 — 운영 DB 에 `orx` 를 붙이지 않는 원칙은 그대로.

## 나중에 검토 (승인 필요)

- 실험 트리 기능을 우리 저장소에 붙일지(Git 저장소 단위로 동작).
- `orx discover` 를 **수집 후보 제안**(어떤 논문을 코퍼스에 넣을지)이나 봇의 **외부 검색 갈래**로 쓰는 안 — 운영 경로에 외부 네트워크 의존이 생기므로 따로 사전 등록·측정.

## 다시 설치·끄기

```sh
cd ~/orx_install && OPENRESEARCH_CLI_NO_MODIFY_PATH=1 OPENRESEARCH_CLI_INSTALL_DIR="$HOME/orx" sh install.sh
~/orx/bin/orx telemetry off
rm -rf ~/orx ~/.config/openresearch   # 제거
```
