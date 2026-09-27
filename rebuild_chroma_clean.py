#!/usr/bin/env python3
"""ChromaDB ``arxiv_papers`` 재인덱싱: JSONL → RagProcessor → 임베딩 재생성.

읽는 JSONL: ``raw_data_queue/processed/crawled_papers*.jsonl`` 전부 + ``raw_data_queue/crawled_papers.jsonl``(있으면 마지막·동일 ID 우선).

청크 품질(References 이후 제거, 노이즈 문단 필터, 인접 소청크 병합 등)은
``pipelines/ingest/rag_processor.py``에 반영되어 있으며, **기존 DB에는 자동 적용되지 않는다.**
이 스크립트로 컬렉션(또는 DB 폴더 전체)을 비운 뒤 전부 다시 적재해야 검색 품질이 반영된다.

권장 (프로덕션급 클린 빌드)::

    cd mini
    .venv/bin/python rebuild_chroma_clean.py --wipe-db

소량 테스트::

    .venv/bin/python rebuild_chroma_clean.py --max-papers 20

재인덱싱 후 평가 (이전 수치와 비교)::

    .venv/bin/python scripts/eval_rag_quality.py
    .venv/bin/python scripts/eval_rag_hybrid.py

BM25는 JSONL 기반이므로 Chroma만 갈아도 내용은 동일하다. JSONL을 바꿨다면
봇/워커 프로세스를 재시작하거나 ``invalidate_bm25_searcher()`` 후 첫 검색에서 재구축된다.

``Database error: no such table: collections`` 등이 나오면 SQLite가 깨진 것이다.
``attempt to write a readonly database``(코드 1032)는 **볼륨/권한이 읽기 전용**이거나
동시 접근으로 SQLite가 쓰기에 실패한 경우가 많다. 스크립트는 이 오류를 감지하면 즉시 중단한다.
``--wipe-db`` 직전에 Chroma 클라이언트로 이전 청크 수를 읽은 뒤 **연결을 닫지 않고** 폴더를 지우면
(macOS에서 흔함) 같은 경로에 다시 열 때 SQLite 1032가 날 수 있어, 삭제 전에 클라이언트를 해제한다.
재인덱싱 중 **다른 프로세스가 같은 chroma_db를 열지 않도록** 봇/워커를 중지하고,
외장 디스크면 절전 방지(예: ``caffeinate -dims``) 후 ``rm -rf chroma_db`` 하고 ``--wipe-db`` 로 다시 실행한다.
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import shutil
import sys
import time
from pathlib import Path

import chromadb
from chromadb.config import Settings

# 프로젝트 루트
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.config.agent_config import CHROMA_DB_DIR, COLLECTION_NAME, PROJECT_ROOT
from core.config.chroma_lock import chroma_write_lock
from core.rag.bm25_index import invalidate_bm25_searcher
from pipelines.ingest.rag_processor import RagProcessor

PROCESSED_DIR = PROJECT_ROOT / "raw_data_queue" / "processed"
ACTIVE_QUEUE = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"


def collect_all_jsonl_files() -> list[Path]:
    """과거 분할본(processed/) 후, 활성 큐(루트 JSONL)를 마지막에 넣어 동일 paper_id는 최신 큐가 우선."""
    out: list[Path] = []
    if PROCESSED_DIR.is_dir():
        out.extend(sorted(PROCESSED_DIR.glob("crawled_papers*.jsonl")))
    if ACTIVE_QUEUE.is_file():
        out.append(ACTIVE_QUEUE)
    if not out:
        print(f"❌ JSONL 없음: {PROCESSED_DIR} 또는 {ACTIVE_QUEUE}")
        return []
    return out


def load_unique_papers(jsonl_files: list[Path], max_papers: int | None) -> dict[str, dict]:
    papers: dict[str, dict] = {}
    total_lines = 0
    for fpath in jsonl_files:
        try:
            with fpath.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    total_lines += 1
                    try:
                        d = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    pid = (d.get("paper_id") or "").strip()
                    if not pid:
                        continue
                    papers[pid] = d
                    if max_papers is not None and len(papers) >= max_papers:
                        break
        except OSError as e:
            print(f"  ⚠️ 파일 읽기 실패: {fpath} — {e}")
        if max_papers is not None and len(papers) >= max_papers:
            break
    print(f"  JSONL 총 라인(읽음): {total_lines}, 고유 논문: {len(papers)}")
    return papers


def _is_sqlite_readonly_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "readonly" in msg or "read-only" in msg or "1032" in msg


def assert_chroma_path_writable(chroma_path: Path) -> None:
    """Chroma 폴더에 실제로 쓸 수 있는지 확인. 실패 시 즉시 예외."""
    chroma_path.mkdir(parents=True, exist_ok=True)
    if not os.access(chroma_path, os.W_OK):
        raise OSError(f"Chroma 경로에 쓰기 권한 없음: {chroma_path}")
    probe = chroma_path / ".chroma_write_probe"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as e:
        raise OSError(
            f"Chroma 경로에 파일을 쓸 수 없습니다 (볼륨 읽기 전용·권한·동기화 도구 등): {chroma_path}"
        ) from e


def remove_empty_chroma_sqlite(chroma_path: Path) -> None:
    """0바이트 chroma.sqlite3은 스키마 없이 깨진 상태이므로 제거해 재생성되게 함."""
    sq = chroma_path / "chroma.sqlite3"
    if sq.is_file() and sq.stat().st_size == 0:
        try:
            sq.unlink()
            print(f"  ⚠️ 0바이트 {sq.name} 제거 (손상·미완성 DB)")
        except OSError as e:
            print(f"  ⚠️ 0바이트 DB 삭제 실패: {e}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--wipe-db",
        action="store_true",
        help="chroma_db 디렉터리 전체 삭제 후 새로 생성 (HNSW/SQLite 잔여 권장)",
    )
    ap.add_argument(
        "--max-papers",
        type=int,
        default=None,
        metavar="N",
        help="테스트용: 고유 논문 N편만 적재",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="JSONL 로드·개수만 출력하고 적재하지 않음",
    )
    args = ap.parse_args()

    chroma_path = CHROMA_DB_DIR

    print("=" * 60)
    print("🔄 ChromaDB 재인덱싱 (RagProcessor + 임베딩 재생성)")
    print("=" * 60)
    print(f"  PROJECT_ROOT:   {PROJECT_ROOT}")
    print(f"  Chroma path:    {chroma_path}")
    print(f"  Collection:     {COLLECTION_NAME}")
    print(f"  wipe-db:        {args.wipe_db}")
    print(f"  max-papers:     {args.max_papers}")
    print("=" * 60)

    jsonl_files = collect_all_jsonl_files()
    if not jsonl_files:
        print("❌ JSONL 파일이 없습니다.")
        return 1
    print(f"\n[로드] JSONL 파일 수: {len(jsonl_files)}")
    papers = load_unique_papers(jsonl_files, args.max_papers)
    if not papers:
        print("❌ 로드된 논문이 없습니다.")
        return 1

    if args.dry_run:
        print("\n[dry-run] 적재 생략. 종료.")
        return 0

    old_count = 0
    if args.wipe_db:
        if chroma_path.exists():
            # wipe 직전에 PersistentClient를 열었다가 rmtree 하면(특히 macOS) Rust/SQLite 핸들이
            # 같은 경로에 재생성될 때까지 남아 1032(readonly)가 날 수 있어, 참고용 청크 수는 생략한다.
            print("\n[1] wipe-db: 기존 폴더 삭제 (이전 청크 수는 생략 — 클라이언트 미오픈)")
            shutil.rmtree(chroma_path)
            print("  ✅ 삭제 완료")
        else:
            print("\n[1] wipe-db: 기존 chroma_db 없음 → 빈 상태에서 신규 생성")
    else:
        print("\n[1] 기존 컬렉션만 삭제 (--wipe-db 없음)")
        client = chromadb.PersistentClient(
            path=str(chroma_path), settings=Settings(anonymized_telemetry=False)
        )
        try:
            old_count = client.get_collection(COLLECTION_NAME).count()
            print(f"  기존 청크 수: {old_count:,}")
        except Exception:
            print("  기존 컬렉션 없음")
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"  ✅ '{COLLECTION_NAME}' 컬렉션 삭제 완료")
        except Exception as e:
            print(f"  ⚠️ 컬렉션 삭제 스킵: {e}")
        del client
        gc.collect()

    # 동시에 봇/워커가 Chroma를 읽으면 SQLite 손상 위험 → 쓰기 락 + 가능하면 워커 중지
    with chroma_write_lock():
        print("\n[2] RagProcessor로 재적재 (references 컷 · 노이즈 필터 · 인접 병합 · 재임베딩)")
        print("     (chroma_write_lock: 읽기 워커는 폴백 경로로 가야 함. 봇 프로세스는 중지 권장.)")
        try:
            assert_chroma_path_writable(chroma_path)
        except OSError as e:
            print(f"\n❌ {e}")
            print(
                "   외장 디스크면 케이블·절전·다른 앱의 동일 폴더 사용을 확인하고,\n"
                "   터미널·Python에 ‘전체 디스크 접근’이 필요할 수 있습니다."
            )
            return 1
        remove_empty_chroma_sqlite(chroma_path)

        try:
            rp = RagProcessor(db_path=str(chroma_path), collection_name=COLLECTION_NAME)
        except Exception as e:
            if _is_sqlite_readonly_error(e):
                print(
                    f"\n❌ Chroma 초기화 실패(읽기 전용 DB): {e}\n"
                    f"   {chroma_path} 를 통째로 지운 뒤 재실행하세요: "
                    "`rm -rf chroma_db` → `python3 rebuild_chroma_clean.py --wipe-db`\n"
                    "   잠긴 0바이트 chroma.sqlite3 이 남아 있으면 이 오류가 날 수 있습니다."
                )
            raise

        success = 0
        failed = 0
        total_chunks = 0
        t0 = time.time()

        for idx, (pid, paper) in enumerate(papers.items(), 1):
            title = (paper.get("title") or "").strip()
            published = (paper.get("published") or paper.get("published_date") or "").strip()
            pdf_url = (paper.get("pdf_url") or "").strip()
            content = (paper.get("content") or paper.get("text") or "").strip()
            if not content:
                content = (paper.get("abstract") or paper.get("summary") or "").strip()
            if not content:
                failed += 1
                continue
            try:
                n_chunks = rp.add_paper(
                    markdown_content=content,
                    title=title,
                    published=published,
                    pdf_url=pdf_url,
                    paper_id=pid,
                    abstract=str(paper.get("abstract", "") or ""),
                )
                total_chunks += n_chunks
                success += 1
                if idx % 50 == 0 or idx == len(papers):
                    elapsed = time.time() - t0
                    print(
                        f"  [{idx}/{len(papers)}] 성공={success} 실패={failed} 청크={total_chunks:,} "
                        f"경과={elapsed:.0f}s"
                    )
            except Exception as e:
                failed += 1
                if idx <= 5 or idx % 100 == 0:
                    print(f"  ❌ [{idx}] {pid}: {e}")
                if _is_sqlite_readonly_error(e):
                    print(
                        "\n❌ 치명: SQLite가 읽기 전용으로 열렸습니다 (코드 1032). "
                        "수천 편을 돌리기 전에 중단합니다."
                    )
                    print(
                        "   → 볼륨이 읽기 전용으로 마운트됐는지(`mount`), "
                        f"{chroma_path} 권한·소유자, 다른 프로세스의 chroma 점유를 확인하세요.\n"
                        "   → 깨진 chroma_db는 `rm -rf chroma_db` 후 `--wipe-db`로 다시 실행하세요."
                    )
                    return 1

    elapsed = time.time() - t0
    final_count = -1
    try:
        final_count = rp._collection.count()
    except Exception as e:
        print(f"\n❌ 최종 청크 수 확인 실패 (DB 손상 가능): {e}")
        print("   → chroma_db 삭제 후 --wipe-db 로 재실행. 재인덱싱 중 다른 프로세스가 DB를 열지 않았는지 확인.")

    try:
        invalidate_bm25_searcher()
        print("\n  ℹ️  BM25 싱글톤 무효화(이 스크립트를 호출한 프로세스 내). 장시간 봇은 재시작 권장.")
    except Exception:
        pass

    print("\n" + "=" * 60)
    if final_count >= 0:
        print("🎉 재인덱싱 완료")
    else:
        print("⚠️ 재인덱싱 비정상 종료 (DB 무효 가능)")
    print("=" * 60)
    print(f"  이전 청크 수(참고): {old_count:,}")
    print(f"  고유 논문 수:      {len(papers):,}")
    print(f"  적재 성공:         {success}")
    print(f"  적재 실패:         {failed}")
    if final_count >= 0:
        print(f"  최종 청크 수:      {final_count:,}")
    else:
        print("  최종 청크 수:      (확인 실패 — DB 무효 가능)")
    print(f"  소요 시간:         {elapsed:.1f}s")
    if old_count > 0 and final_count > 0:
        print(f"  청크 수 변화:      {final_count - old_count:+,} ({100.0 * final_count / old_count - 100:.1f}%)")
    print("=" * 60)
    print("\n다음: 동일 스크립트로 Recall / P@1 / MRR 측정 후 이전 로그와 비교")
    print("  .venv/bin/python scripts/eval_rag_quality.py")
    print("  .venv/bin/python scripts/eval_rag_hybrid.py")
    return 1 if final_count < 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
