#!/usr/bin/env python3
"""
동일 ``discussion_digest`` 로 로컬 Ollama 모델만 바꿔 회의록을 두 번 생성해 한 파일에 적습니다.

사전 준비
---------
1. Boardroom 전체를 **한 번** 돌리면 ``mini/.cron/boardroom_last_agenda.txt`` 와
   ``boardroom_last_digest.txt`` 가 자동으로 갱신됩니다 (압축 단계 직후).
2. 또는 ``--agenda`` / ``--digest`` 로 파일 경로를 직접 지정합니다.

실행 (mini 루트에서):

  PYTHONPATH=. python3 scripts/boardroom_minutes_ab.py
  PYTHONPATH=. python3 scripts/boardroom_minutes_ab.py \\
      --models yunsur_v3:latest qwen3.5:9b \\
      --digest mini/.cron/boardroom_last_digest.txt \\
      --agenda mini/.cron/boardroom_last_agenda.txt

출력: ``mini/archives/boardroom/boardroom_ab_<타임스탬프>.md``
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv()
load_dotenv(_ROOT / ".env", override=True)

from apps.boardroom import swarm_meeting as sm  # noqa: E402


def _safe_tag(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name.strip())[:80] or "model"


def main() -> int:
    default_digest = _ROOT / ".cron" / "boardroom_last_digest.txt"
    default_agenda = _ROOT / ".cron" / "boardroom_last_agenda.txt"
    ap = argparse.ArgumentParser(description="동일 digest로 Ollama 모델 A/B 회의록 생성")
    ap.add_argument(
        "--digest",
        type=Path,
        default=default_digest,
        help=f"압축본 텍스트 파일 (기본: {default_digest})",
    )
    ap.add_argument(
        "--agenda",
        type=Path,
        default=default_agenda,
        help=f"안건 전문 텍스트 파일 (기본: {default_agenda})",
    )
    ap.add_argument(
        "--models",
        nargs="+",
        default=["yunsur_v3:latest", "qwen3.5:9b"],
        help="비교할 Ollama 모델 태그 (순서대로 생성)",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="결과 마크다운 경로 (기본: archives/boardroom/boardroom_ab_<시각>.md)",
    )
    args = ap.parse_args()

    if not args.digest.is_file():
        print(
            f"❌ digest 파일이 없습니다: {args.digest}\n"
            "   Boardroom을 한 번 실행해 스냅샷을 만들거나, --digest 로 경로를 지정하세요.\n",
            file=sys.stderr,
        )
        return 2
    if not args.agenda.is_file():
        print(
            f"❌ agenda 파일이 없습니다: {args.agenda}\n"
            "   Boardroom을 한 번 실행하거나, --agenda 로 경로를 지정하세요.\n",
            file=sys.stderr,
        )
        return 2

    digest = args.digest.read_text(encoding="utf-8")
    agenda = args.agenda.read_text(encoding="utf-8")
    if not digest.strip():
        print("❌ digest 내용이 비었습니다.", file=sys.stderr)
        return 2
    if not agenda.strip():
        print("❌ agenda 내용이 비었습니다.", file=sys.stderr)
        return 2

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = args.out
    if out is None:
        tag_join = "_".join(_safe_tag(m) for m in args.models)
        out = _ROOT / "archives" / "boardroom" / f"boardroom_ab_{stamp}_{tag_join}.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    chunks: list[str] = [
        "# Boardroom — 동일 digest Ollama A/B\n",
        f"- 생성 시각: {stamp}\n",
        f"- digest: `{args.digest}` ({len(digest):,}자)\n",
        f"- agenda: `{args.agenda}` ({len(agenda):,}자)\n",
        "- 모델 순서: " + ", ".join(f"`{m}`" for m in args.models) + "\n",
        "\n---\n\n",
    ]

    for model in args.models:
        chunks.append("## 모델: `" + model.strip() + "`\n\n")
        body = sm.generate_boardroom_minutes_from_digest(
            agenda,
            digest,
            model=model.strip(),
            quiet=False,
        )
        chunks.append(body.strip() + "\n\n---\n\n")

    out.write_text("".join(chunks), encoding="utf-8")
    print(f"✅ 저장: {out}\n", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
