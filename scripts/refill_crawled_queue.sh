#!/usr/bin/env bash
# crawled_papers.jsonl 큐 보충 (권장 운영)
#
# /papers 및 LLM 토론 큐는 토론 배치·processed 이동으로 줄어들 수 있습니다.
# raw_data_queue/processed/ 통째 복구보다, 새 논문을 백필·크롤로 쌓는 쪽을 기본으로 둡니다.
#
# 사용:
#   bash scripts/refill_crawled_queue.sh
#   REFILL_QUEUE_LOOKBACK_DAYS=180 bash scripts/refill_crawled_queue.sh
#   bash scripts/refill_crawled_queue.sh -- -s 2025-01-01 -e 2025-03-01 -b 15
#     → run_backfill.py 인자만 사용 (아래 기본 기간 무시)

set -euo pipefail
MINI_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$MINI_ROOT"

PY="${MINI_ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "ERROR: $PY 없음. venv 생성 후 실행하세요."
  exit 1
fi

export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}${MINI_ROOT}"

if [[ "${1:-}" == "--" ]]; then
  shift
  exec "$PY" -u -m apps.backfill.run_backfill "$@"
fi

lookback="${REFILL_QUEUE_LOOKBACK_DAYS:-90}"
case "$(uname -s)" in
  Darwin*)
    start_date=$(date -v-"${lookback}"d +%Y-%m-%d)
    ;;
  *)
    start_date=$(date -d "$lookback days ago" +%Y-%m-%d)
    ;;
esac
end_date=$(date +%Y-%m-%d)

echo "백필 구간: $start_date ~ $end_date (cs.AI, lookback=${lookback}일)"
echo "기간을 바꾸려면: REFILL_QUEUE_LOOKBACK_DAYS=180 bash $0"
echo "또는: bash $0 -- -s 2024-01-01 -e 2024-12-31"
exec "$PY" -u -m apps.backfill.run_backfill -s "$start_date" -e "$end_date"
