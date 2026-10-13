# 2026-10-13 맥미니 내장 디스크 가득 참 → Chroma 벡터 인덱스 손상

## 무슨 일이 있었나

- 01:30 무렵 맥미니가 꺼졌다 켜짐. 재부팅 뒤 텔레그램 봇은 자동으로 안 떴고(launchd 미등록), 스케줄러·chatbot_dev 는 떴다.
- 04:4x 확인: 내장 디스크 **100% (여유 116MB)**. Chroma(`~/Library/Application Support/mini-chroma`) 가 114GB, 그중 HNSW `link_lists.bin` 이 실제 ~100GB(겉보기 796GB, 희소 파일). 정상이라면 118만 청크에 수 GB 수준이다.
- 벡터 검색이 `Failed to apply logs to the hnsw segment writer` 로 실패. 디스크가 차서 인덱스 갱신을 못 쓴 것. HF 공백 백필이 Chroma 에 쓰던 중이었다.
- 디스크가 가득 찬 동안 다른 SQLite(세션 DB)도 못 열었고, MPS 임베딩 프로세스는 macOS 에 의해 강제 종료됐다.

## 복구

1. 봇·스케줄러·백필 중지.
2. 원본 SQLite(원문 청크 1,185,105 + 메타데이터, 온전)를 **읽기 전용**으로 읽어 같은 임베딩(`all-MiniLM-L6-v2`, 정규화, CPU)으로 다시 계산 → T7 `mini-chroma-rebuild` 에 새 컬렉션 — [`scripts/rebuild_chroma.py`](../../scripts/rebuild_chroma.py), 약 3시간 40분, **13GB**.
   - 컬렉션을 기본 임베딩 설정으로 만들어 운영 코드와 충돌 → 설정을 원본과 같은 `{}` 로 맞춤.
3. 검증: 검색 평가 162문항 적중 138 = 고장 전 138, HF 40문항 29 = 29.
4. `.env` `CHROMA_DB_PATH` → `/Volumes/T7 Shield/mini-chroma-rebuild`, 봇·스케줄러 재기동.
5. 옛 SQLite 를 `/Volumes/T7 Shield/backup/mini-chroma-old-20261013/` 에 백업(크기·행 수 확인) 후 옛 폴더 삭제 → 내장 디스크 44%.

## 재발 방지

- 수집 누락 감시(`apps/telegram_bot/ingest_watchdog.py`)에 **디스크 여유 10% 미만 경고**(내장·T7) 추가.
- 새 DB 크기를 지켜본다 — `link_lists.bin` 이 다시 비정상적으로 커지면 Chroma HNSW 문제로 보고 따로 조사.
- 텔레그램 봇 launchd 등록 완료(2026-10-13, `ops/launchd/`) — 재부팅 후 T7·Ollama 준비를 기다려 자동 기동.
