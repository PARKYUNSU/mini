"""텔레그램 수신기에서 subprocess로만 호출 (논문 모드 토글)."""

from __future__ import annotations

import sys

from agent_session import get_paper_mode, set_paper_mode


def main() -> None:
    if len(sys.argv) < 3:
        print("usage: paper_mode_cli.py <chat_id> <full /paper text>", file=sys.stderr)
        sys.exit(1)
    chat_id = sys.argv[1]
    text = sys.argv[2]
    parts = text.strip().split()
    if len(parts) >= 2:
        sub = parts[1].lower()
        if sub in ("on", "1", "켜", "켜줘"):
            set_paper_mode(chat_id, True)
        elif sub in ("off", "0", "꺼", "꺼줘"):
            set_paper_mode(chat_id, False)
        else:
            cur = get_paper_mode(chat_id)
            print(f"현재: {'ON' if cur else 'OFF'}")
        return
    cur = get_paper_mode(chat_id)
    set_paper_mode(chat_id, not cur)


if __name__ == "__main__":
    main()
