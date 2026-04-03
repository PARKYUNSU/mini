"""저장 큐 JSONL 목록만 조회 (stdlib만 사용, chromadb 미사용)."""

from __future__ import annotations

import json
from pathlib import Path


def list_stored_papers_text(mini_root: Path) -> str:
    raw_path = mini_root / "raw_data_queue" / "crawled_papers.jsonl"
    if not raw_path.exists():
        return "저장된 논문이 없습니다."
    seen: set[str] = set()
    lines: list[str] = []
    try:
        with raw_path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                    pid = d.get("paper_id", "")
                    title = d.get("title", "")
                    if pid and pid not in seen:
                        seen.add(pid)
                        lines.append(f"- {pid}: {title}")
                except json.JSONDecodeError:
                    continue
    except OSError:
        return "목록을 읽을 수 없습니다."
    return "\n".join(lines) if lines else "저장된 논문이 없습니다."
