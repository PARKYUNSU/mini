"""
agent_tools/에 저장된 도구 목록 조회.
사용자가 "저장된 도구 목록", "기존 도구 뭐 있어?", "등록된 도구 알려줘"라고 질문할 때 사용.
"""

from pathlib import Path


def run(user_request: str) -> str:
    """
    agent_tools/ 폴더의 .py 도구 목록을 반환.
    """
    try:
        tools_dir = Path(__file__).resolve().parent
        # 최상위 .py만 (cron_engine 등 하위 폴더 제외)
        py_files = sorted(p for p in tools_dir.glob("*.py") if p.name != "__init__.py")
        if not py_files:
            return "저장된 도구가 없습니다."

        lines = [f"✅ agent_tools/에 총 {len(py_files)}개의 도구가 있습니다.\n"]
        for i, p in enumerate(py_files, 1):
            desc = ""
            try:
                content = p.read_text(encoding="utf-8")
                if '"""' in content:
                    parts = content.split('"""')
                    if len(parts) >= 2:
                        desc = parts[1].strip().split("\n")[0][:80].strip()
            except Exception:
                pass
            lines.append(f"{i}. {p.stem}" + (f": {desc}" if desc else ""))

        return "\n".join(lines)

    except Exception as e:
        return f"도구 목록 조회 중 에러 발생: {str(e)}"
