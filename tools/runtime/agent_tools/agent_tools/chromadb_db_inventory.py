"""
ChromaDB 인벤토리 조회. DB에 저장된 논문 목록을 확인하는 전용 도구.
사용자가 "DB에 뭐 있어?", "어떤 논문이 저장되어 있어?", "목록 보여줘"라고 질문할 때 사용.
crawled_papers.jsonl 기준으로 논문 수·목록 산출 (ChromaDB는 청크 단위라 limit=500 시 소수만 추출됨).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def run(user_request: str) -> str:
    """
    저장된 논문 목록(인벤토리) 반환. crawled_papers.jsonl 기준.
    """
    try:
        raw_path = Path(__file__).resolve().parents[1] / "raw_data_queue" / "crawled_papers.jsonl"
        if not raw_path.exists():
            return "현재 데이터베이스가 비어 있습니다."

        seen = set()
        titles = []
        for line in raw_path.read_text(encoding="utf-8").strip().split("\n"):
            if not line.strip():
                continue
            try:
                d = json.loads(line)
                pid = d.get("paper_id", "")
                title = (d.get("title") or "").strip()
                if pid and pid not in seen:
                    seen.add(pid)
                    titles.append(title or pid)
            except json.JSONDecodeError:
                continue

        if not titles:
            return "현재 데이터베이스가 비어 있습니다."

        top10 = titles[:10]
        response = f"✅ 현재 DB에 총 {len(titles)}편의 논문이 있습니다.\n\n[주요 논문 목록 Top 10]\n"
        for i, t in enumerate(top10, 1):
            response += f"{i}. {t}\n"
        if len(titles) > 10:
            response += f"\n... (외 {len(titles) - 10}편 더 있음)"

        return response

    except Exception as e:
        return f"DB 목록 조회 중 에러 발생: {str(e)}"
