"""launchd 용 봇 기동기 (2026-10-13). launchd 의 bash 는 T7 파일을 못 읽어서(TCC) venv Python 이 직접 띄운다.

restart.sh 의 분리 모드와 같다: telegram_receiver · ai_worker 를 각각 백그라운드로, 로그는 T7 의 bot_*.log 에 덧붙인다.
이미 떠 있으면 아무것도 하지 않는다.
"""
import os
import subprocess
import sys
import time

ROOT = "/Volumes/T7 Shield/mini"
PY = os.path.join(ROOT, ".venv/bin/python")
MODS = [("apps.telegram_bot.telegram_receiver", "bot_receiver.log", ".telegram_receiver.pid"),
        ("apps.telegram_bot.ai_worker", "bot_ai_worker.log", ".ai_worker.pid")]


def running(mod: str) -> bool:
    return subprocess.run(["pgrep", "-f", mod], capture_output=True).returncode == 0


def main() -> int:
    os.chdir(ROOT)
    env = dict(os.environ, PYTHONPATH=ROOT, PYTHONUNBUFFERED="1", PYTHONFAULTHANDLER="1",
               TMPDIR=os.path.join(ROOT, "tmp"))
    os.makedirs(env["TMPDIR"], exist_ok=True)
    for mod, log, pidf in MODS:
        if running(mod):
            print(f"이미 실행 중: {mod}", flush=True)
            continue
        with open(log, "ab") as f:
            f.write(f"\n[{time.strftime("%Y-%m-%d %H:%M:%S")}] launchd 기동 (start_telegram_bot.py)\n".encode())
            p = subprocess.Popen([PY, "-m", mod], cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL, start_new_session=True)
        with open(pidf, "w") as f:
            f.write(str(p.pid))
        print(f"기동: {mod} pid={p.pid}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
