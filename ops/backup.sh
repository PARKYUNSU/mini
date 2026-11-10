#!/bin/bash
# 내장 디스크 백업 (ops_audit_1111). T7 한 장에 코드 · 코퍼스 · 대화 기록 · .env 가 다 있어, T7 이 죽거나
# 없어지면 모두 잃는다. 올리지 않은 커밋도 여기서만 산다.
#
#   bash ops/backup.sh      →  ~/backups/mini/YYYY-MM-DD/  (폴더 700 · 파일 600)
#
# - Chroma(16GB)는 뺀다. raw_data_queue 의 JSONL 로 다시 만들 수 있다.
# - 옛 백업은 지우지 않는다(손으로 정리). env.backup 에는 비밀 값이 있다 — 기기를 넘기기 전에 ~/backups 를 옮기고 지운다.
# - 01:00 정기 수집 중에는 돌리지 않는다(JSONL 을 쓰는 중이라 마지막 줄이 잘릴 수 있다).
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${HOME}/backups/mini/$(date +%F)"
umask 077
mkdir -p "$OUT"

git bundle create -q "$OUT/mini.bundle" --all
git bundle verify -q "$OUT/mini.bundle"
git diff HEAD > "$OUT/tracked_changes.patch"
git ls-files --others --exclude-standard -z | tar --null -czf "$OUT/untracked.tgz" -T -
tar -czf "$OUT/raw_data_queue.tgz" raw_data_queue
sqlite3 .bridge/agent_bridge.sqlite ".backup '$OUT/agent_bridge.sqlite'"
tar -czf "$OUT/bridge_files.tgz" --exclude='*.sqlite*' .bridge
if [ -f idea_vault.sqlite ]; then sqlite3 idea_vault.sqlite ".backup '$OUT/idea_vault.sqlite'"; fi
cp .env "$OUT/env.backup"
(cd "$OUT" && shasum -a 256 -- * > SHA256SUMS.tmp && mv SHA256SUMS.tmp SHA256SUMS)

echo "백업 끝: $OUT ($(du -sh "$OUT" | cut -f1)) · HEAD $(git rev-parse --short HEAD) · 번들 커밋 $(git rev-list --all --count)"
