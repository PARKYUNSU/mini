# 2026-10-14 Chroma 벡터 인덱스 손상 (여러 프로세스 동시 쓰기 추정)

## 증상

- 01:49 `real_eval_1013` 측정(`eval_e2e_ko.py`)이 10문항 뒤 **세그폴트**로 종료. 바로 이어 시작한 두 번째 실행도 시작 직후 종료. 파이썬 Traceback 없음.
- 크래시 리포트(`~/Library/Logs/DiagnosticReports/Python-2026-10-14-01494*.ips`): `EXC_BAD_ACCESS / SIGSEGV`, 실패 스레드가 전부 `chromadb_rust_bindings.abi3.so`.
- 새 프로세스에서 `collection.count()` 만 해도 세그폴트(`chromadb/api/rust.py:_count`).

## 상태 (01:5x 확인)

- **SQLite 원본은 정상**: `embeddings` 1,236,213행, `embeddings_queue` 536행.
- `max_seq_id`: 메타데이터 세그먼트 1,236,213 · **벡터(HNSW) 세그먼트 1,235,678** → 큐에 남은 535건을 HNSW 에 반영하는 단계에서 충돌로 보인다(10-13 사고의 "Failed to apply logs" 와 같은 단계).
- HNSW 파일 크기는 정상(`link_lists.bin` 10 MB, `data_level0.bin` 2.0 GB) — 10-13 처럼 부풀지는 않았다.

## 추정 원인

**여러 프로세스가 같은 PersistentClient 폴더에 쓴 것.** 이 시각에 DB 를 연 프로세스:

1. HF 공백 백필 `hf_daily`(pid 34449) — 10-13 12:37 부터 떠 있으며, 측정 중에는 `kill -STOP` 했다가 측정 사이(01:38–01:39)와 그 전 공백에 `CONT` 되어 계속 쓰기.
2. 스케줄러 일일 수집(01:00, 마커 01:11) + 그 뒤 HF Daily 수집 — **별도 프로세스에서 쓰기**.
3. 봇 `ai_worker`(pid 34855) — 시작 시 Chroma 싱글턴을 열어 계속 보유(읽기지만 로그 반영 과정에서 인덱스를 저장할 수 있음).
4. 평가 프로세스(읽기).

각 프로세스가 HNSW 를 메모리에 따로 들고 있다가 저장하면, 다른 프로세스가 쓴 내용과 어긋난다. `chroma_write_lock` 은 쓰기 순서만 맞출 뿐 **각 프로세스 메모리의 낡은 인덱스**는 막지 못한다. Chroma 로컬 PersistentClient 는 단일 프로세스용이다.

## 조치

- 01:5x HF 백필 일시정지(`kill -STOP 34449`).
- 01:5x `scripts/rebuild_chroma.py --src mini-chroma-rebuild --dst mini-chroma-rebuild2 --device cpu`(원본 읽기 전용) 시작 — 10-13 과 같은 절차, 약 3.5시간.
- 완료 후: 컬렉션 embedding function 설정을 원본과 같게(`{}`) → 검색 평가 가드(162문항 적중 138 기준) → **사용자 승인 후** `.env` `CHROMA_DB_PATH` 교체 · 봇/스케줄러 재시작.

## 재발 방지 (제안, 미적용)

- **재구축 체크리스트에 추가:** `rebuild_chroma.py` 뒤에 embedding function 보정을 넣는다(두 번 연속 같은 문제).

- **Chroma 를 서버 한 개로**: `chroma run --path <DB>` 를 launchd 로 띄우고 봇·스케줄러·백필·평가가 모두 `HttpClient` 로 접속 → 인덱스를 들고 있는 프로세스가 하나뿐.
- 그 전까지는 **쓰는 프로세스를 한 번에 하나만**: 백필은 스케줄러 수집 시간(01:00–02:00)과 겹치지 않게, 장시간 백필 프로세스 금지(하루치마다 새 프로세스).

## 기록

| 시각 | 내용 |
|---|---|
| 10-14 01:39 | real_eval 시작 |
| 10-14 01:49 | 세그폴트 2회, 측정 종료 |
| 10-14 01:5x | 손상 확인, 백필 정지, 재구축 시작 |
| 10-14 06:0x | 재구축 완료 1,236,213 / 1,236,213 (250분) |
| 10-14 06:1x | 검색 평가 0/162 — 새 컬렉션 schema 의 embedding function 이 `default` 라 운영 코드(`sentence_transformer`)와 충돌(ValueError). 10-13 과 같은 보정(`collection.modify(configuration={"embedding_function": ef})`, 로컬 객체 갱신 단계 ValueError 는 무시 — schema 에는 반영됨) |
| 10-14 08:3x | 검색 평가 162문항 적중 138 = 138 (짝 0:0) · HF 40문항 29 = 29 → 통과 |
| 10-14 08:45 | 사용자 승인대로 `.env` `CHROMA_DB_PATH` → `mini-chroma-rebuild2` (이전 줄 주석 보존, 백업 `.cron/env.bak.20261014`), 스케줄러·봇 재시작, worker 가 rebuild2 를 연 것 확인(lsof). 정지해 둔 HF 백필(pid 34449)은 옛 경로를 들고 있어 종료 — 공백 백필은 재발 방지책 결정 후 재개 |
