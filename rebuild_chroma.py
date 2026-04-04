#!/usr/bin/env python3
"""
Chroma DB 재구축 스크립트
- crawled_papers.jsonl에서 모든 논문을 읽어 재인제스트
- 손상된 HNSW 인덱스 복구용
"""
import gc
import json
import os
import shutil
import sys
import time

os.environ["TOKENIZERS_PARALLELISM"] = "false"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipelines.ingest.rag_processor import RagProcessor

JSONL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw_data_queue", "crawled_papers.jsonl")
CHROMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")

def load_papers():
    papers = []
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                papers.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return papers


def main():
    papers = load_papers()
    total = len(papers)
    print(f"📚 총 {total}편의 논문을 재인제스트합니다.")
    print(f"   JSONL: {JSONL_PATH}")
    print(f"   Chroma: {CHROMA_PATH}")
    print()

    # 기존 HNSW 세그먼트 정리 (SQLite는 유지 — get_or_create가 기존 메타/문서 위에 upsert)
    # 전체 삭제 후 깨끗하게 재구축
    if os.path.exists(CHROMA_PATH):
        print("🗑  기존 chroma_db 삭제 중...")
        shutil.rmtree(CHROMA_PATH)
        print("   삭제 완료")

    print("🔧 RagProcessor 초기화 중...")
    rag = RagProcessor(db_path=CHROMA_PATH)
    print("   초기화 완료")
    print()

    success = 0
    skip = 0
    fail = 0
    total_chunks = 0
    t0 = time.time()

    for idx, paper in enumerate(papers):
        pid = paper.get("paper_id", "unknown")
        title = paper.get("title", "")[:60]
        content = paper.get("content", "") or paper.get("text", "") or ""
        published = paper.get("published_date", "") or paper.get("published", "") or paper.get("date", "") or ""
        pdf_url = paper.get("pdf_url", "") or paper.get("url", "") or ""

        if not content or len(content) < 100:
            skip += 1
            print(f"  [{idx+1}/{total}] SKIP (no content): {pid} {title}")
            continue

        try:
            n = rag.add_paper(
                markdown_content=content,
                title=paper.get("title", ""),
                published=published,
                pdf_url=pdf_url,
                paper_id=pid,
            )
            success += 1
            total_chunks += n
            elapsed = time.time() - t0
            rate = (idx + 1) / elapsed if elapsed > 0 else 0
            eta = (total - idx - 1) / rate if rate > 0 else 0
            print(
                f"  [{idx+1}/{total}] ✓ {pid} ({n} chunks) | "
                f"누적 {total_chunks} chunks | "
                f"{elapsed:.0f}s elapsed | ETA {eta:.0f}s | {title}"
            )
        except Exception as e:
            fail += 1
            print(f"  [{idx+1}/{total}] ✗ {pid}: {e}")

        if (idx + 1) % 50 == 0:
            gc.collect()

    elapsed = time.time() - t0
    print()
    print("=" * 60)
    print(f"🎉 재구축 완료!")
    print(f"   성공: {success} | 스킵: {skip} | 실패: {fail}")
    print(f"   총 청크: {total_chunks}")
    print(f"   소요시간: {elapsed:.1f}초 ({elapsed/60:.1f}분)")
    print("=" * 60)


if __name__ == "__main__":
    main()
