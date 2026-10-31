import os
import subprocess


def test_weekly_check_reads_fresh_dotenv(tmp_path, monkeypatch):
    saved = dict(os.environ)
    import apps.scheduler.run_scheduler as S  # 모듈이 .env 를 override 로 읽는다 — 다른 테스트에 안 새게 되돌림

    os.environ.clear()
    os.environ.update(saved)
    monkeypatch.setenv("RAG_LIST_MODE", "1")  # 스케줄러가 기동 때 읽어 둔 .env 값 흉내
    seen = {}

    class FakePopen:
        pid = 1

        def __init__(self, cmd, **kw):
            seen.update(cmd=cmd, **kw)

    monkeypatch.setattr(subprocess, "Popen", FakePopen)
    monkeypatch.setattr(S, "_CRON_DIR", tmp_path)
    S.run_weekly_check()
    assert seen["cmd"] == ["/bin/sh", "scripts/weekly_check.sh"] and seen["start_new_session"]
    assert seen["cwd"] == S.PROJECT_ROOT
    # 지금의 .env 를 자식이 읽게 — 기동 때 값은 넘기지 않는다
    assert "RAG_LIST_MODE" not in seen["env"] and seen["env"]["PYTHONPATH"] == str(S.PROJECT_ROOT)
