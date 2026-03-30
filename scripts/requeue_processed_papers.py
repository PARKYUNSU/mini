#!/usr/bin/env python3
"""
raw_data_queue/processed/crawled_papers*.jsonl 에만 있는 논문 중
- finetune_datasets/debated_paper_ids.jsonl 에 없는 paper_id
- content/body 가 비어 있지 않음
- 현재 crawled_papers.jsonl 큐에 아직 없음
인 레코드를 raw_data_queue/crawled_papers.jsonl 끝에 append.

실행 (mini 루트):
  .venv/bin/python scripts/requeue_processed_papers.py
  .venv/bin/python scripts/requeue_processed_papers.py --dry-run
(macOS 에서 `python` 이 없으면 위처럼 venv 또는 `python3` 사용)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_QUEUE = PROJECT_ROOT / "raw_data_queue"
PROCESSED_DIR = RAW_QUEUE / "processed"
QUEUE_PATH = RAW_QUEUE / "crawled_papers.jsonl"
DEBATE_INDEX = PROJECT_ROOT / "finetune_datasets" / "debated_paper_ids.jsonl"


def _body_len(rec: dict) -> int:
    return len((rec.get("content") or rec.get("body") or ""))


def _load_jsonl_paper_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    if not path.exists():
        return ids
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            pid = str(d.get("paper_id", "")).strip()
            if pid:
                ids.add(pid)
    return ids


def _load_debated_ids() -> set[str]:
    return _load_jsonl_paper_ids(DEBATE_INDEX)


def main() -> int:
    parser = argparse.ArgumentParser(description="processed 크롤 JSONL → 토론 큐(crawled_papers.jsonl) 재유입")
    parser.add_argument("--dry-run", action="store_true", help="append 없이 건수만 출력")
    args = parser.parse_args()

    debated = _load_debated_ids()
    in_queue = _load_jsonl_paper_ids(QUEUE_PATH)

    # processed 내 동일 paper_id는 본문이 더 긴 레코드 우선
    best: dict[str, dict] = {}
    sources: list[Path] = sorted(PROCESSED_DIR.glob("crawled_papers*.jsonl"))
    if not sources:
        print(f"ℹ️ {PROCESSED_DIR} 에 crawled_papers*.jsonl 없음")
        return 0

    for path in sources:
        try:
            with path.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    pid = str(rec.get("paper_id", "")).strip()
                    if not pid or pid in debated or pid in in_queue:
                        continue
                    if _body_len(rec) == 0:
                        continue
                    old = best.get(pid)
                    if old is None or _body_len(rec) > _body_len(old):
                        best[pid] = rec
        except OSError as e:
            print(f"⚠️ 읽기 스킵 {path.name}: {e}", file=sys.stderr)

    to_add = [best[k] for k in sorted(best.keys())]
    n = len(to_add)

    if n == 0:
        print(
            "ℹ️ 큐에 넣을 논문 없음 "
            "(이미 큐/토론완료이거나 본문 없음, 또는 processed에 후보 없음)"
        )
        return 0

    print(f"📥 processed 소스 파일: {len(sources)}개")
    print(f"📊 토론 완료 인덱스 제외 후 고유 후보: {n}건 (append 예정)")

    if args.dry_run:
        for rec in to_add[:8]:
            print(f"   - {rec.get('paper_id')}: {(rec.get('title') or '')[:60]}")
        if n > 8:
            print(f"   ... 외 {n - 8}건")
        return 0

    RAW_QUEUE.mkdir(parents=True, exist_ok=True)
    with QUEUE_PATH.open("a", encoding="utf-8") as out:
        for rec in to_add:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"✅ {QUEUE_PATH.relative_to(PROJECT_ROOT)} 에 {n}건 append 완료")
    return 0


if __name__ == "__main__":
    sys.exit(main())
