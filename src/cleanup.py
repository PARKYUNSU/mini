"""
프로젝트 루트 찌꺼기 클린업
- 기존 테스트용 파일/폴더 삭제 (정보 오염 방지)
"""

import os
import shutil
from pathlib import Path
from typing import Optional


# 프로젝트 루트에 널부러진 구 테스트 파일/폴더
LEGACY_PATHS = [
    "test_science_data.jsonl",
    "test_finetune_data.jsonl",
    "test_chroma_db",
]


def cleanup_legacy_files(project_root: Optional[Path] = None) -> int:
    """
    기존 테스트용 파일·폴더를 삭제합니다.

    Args:
        project_root: 프로젝트 루트 경로 (None이면 현재 작업 디렉터리)

    Returns:
        삭제된 항목 수
    """
    root = Path(project_root or os.getcwd())
    removed = 0

    for name in LEGACY_PATHS:
        path = root / name
        if not path.exists():
            continue
        try:
            if path.is_file():
                path.unlink()
                print(f"  🧹 삭제: {name}")
                removed += 1
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"  🧹 삭제: {name}/")
                removed += 1
        except OSError as e:
            print(f"  ⚠️  삭제 실패 ({name}): {e}")

    return removed
