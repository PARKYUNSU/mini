#!/usr/bin/env python3
"""
통합 스케줄러 - M2 맥 미니 24시간 운영용
- arXiv 파이프라인: 매일 **01:00** (기본) — ``ARXIV_PIPELINE_SCHEDULE_AT`` (Gemini 키 있을 때만 등록).
  성공 시 ``.cron/arxiv_pipeline_ok_YYYY-MM-DD.marker`` 기록. 오후 기동 시 당일 미실행이면 보충 실행.
- LLM 토론 배치: ``LLM_DEBATE_SCHEDULE_ENABLED=1`` 일 때만 월~금 02:00 (기본 **꺼짐**).
  ``LLM_DEBATE_BATCH_DURATION_SEC``: 0=무제한 시 백그라운드 기동.
- Phase35 YES 심사: 매일 **08:00** (기본) — 하루 1회 스폰(``.cron/phase35_spawned_*.marker``). 오후 기동 시 보충.
- morning_scraper: 매일 **07:30** (기본) — ``MORNING_SCRAPER_SCHEDULE_AT`` (Phase35와 같은 마스터 스위치)
- Boardroom(자율 R&D 회의): 기본 **매일(월~일)** 동일 시각 — ``BOARDROOM_SCHEDULE_DAILY=0`` 이면 **월~금만**
  - ``BOARDROOM_SCHEDULE_AT`` / ``BOARDROOM_SCHEDULE_ENABLED`` / ``BOARDROOM_SCHEDULE_SKIP_IF_NO_YES`` (swarm_meeting 자식)
- 주일 찬양 가사(apps.church_lyrics): 수 08:35 ``rename`` · 토 09:00 ``lyrics`` (종료 코드 2=콘티 없음이면 토 11:00 한 번 더).
  ``NOTION_TOKEN`` 있고 ``CHURCH_LYRICS_SCHEDULE_ENABLED``≠0 일 때. 결과는 ``.cron/job_runs.jsonl`` (event=church_lyrics_run).
- cron_engine: 1분마다 due job 체크 → LangGraph 트리거 → 텔레그램 선톡 (agent_bot 단독 실행 시에도 동일 worker 가 뜸, 락으로 중복 방지)
- 메인 루프: ``SCHEDULER_POLL_SEC``(기본 30초) 간격으로 ``run_pending`` — 예약 시각 부근 재김이 더 촘촘함.
- 프로세스 기동 직후: 서울 당일·각 작업 시각+grace 이후면 ``morning_scraper`` / Phase35 / arXiv / Boardroom 보충 시도(LLM 토론 배치 제외).
- 메인 봇(agent_bot.py)은 별도 프로세스로 실행
"""

import os
import subprocess
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import schedule
from dotenv import load_dotenv

from core.execution.retry_utils import with_scheduler_retry

# cron/nohup 환경에서 부모 stdio가 닫혀 있으면 자식(main.py 등)이 exit 1·Bad file descriptor 낼 수 있음
_SUBPROCESS_KWARGS = {"stdin": subprocess.DEVNULL}

# 프로젝트 루트 (mini/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env", override=True)
load_dotenv()

sys.path.insert(0, str(PROJECT_ROOT))


def _subprocess_env() -> dict:
    env = os.environ.copy()
    root = str(PROJECT_ROOT)
    prev = (env.get("PYTHONPATH") or "").strip()
    env["PYTHONPATH"] = f"{root}:{prev}" if prev else root
    return env
from core.config.agent_config import get_gemini_api_keys  # noqa: E402
from apps.scheduler.agent_cron_worker import start_cron_worker_daemon  # noqa: E402
from pipelines.debate.llm_debate_spawn_guard import (  # noqa: E402
    clear_debate_child_pid_if_matches,
    debate_spawn_lock,
    get_running_debate_scheduler_child_pid,
    register_debate_child_pid,
)
# llm_debate_scheduler.DEBATE_SCHEDULE_WEEKDAYS 와 동일하게 유지
_DEBATE_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday")

_CRON_DIR = PROJECT_ROOT / ".cron"
_BOARDROOM_CHILD_PID_PATH = _CRON_DIR / "boardroom_child.pid"

_SEOUL_TZ = ZoneInfo("Asia/Seoul")
# schedule 라이브러리는 당일 지난 시각 작업을 보통 내일로 미룸 → 오후에 스케줄러가 뜬 경우 보충 실행용
_CATCHUP_GRACE = timedelta(minutes=75)


def _scheduler_poll_sec() -> int:
    try:
        sec = int((os.getenv("SCHEDULER_POLL_SEC") or "30").strip())
    except ValueError:
        sec = 30
    return max(10, min(120, sec))


def _parse_hhmm(hhmm: str) -> tuple[int, int]:
    parts = (hhmm or "00:00").strip().split(":")
    h = int(parts[0]) if parts else 0
    m = int(parts[1]) if len(parts) > 1 else 0
    return h % 24, m % 60


def _wall_datetime_on(d: date, hhmm: str, tz: ZoneInfo = _SEOUL_TZ) -> datetime:
    h, m = _parse_hhmm(hhmm)
    return datetime(d.year, d.month, d.day, h, m, 0, tzinfo=tz)


def _seoul_now() -> datetime:
    return datetime.now(_SEOUL_TZ)


def _morning_cache_mtime_date() -> date | None:
    p = PROJECT_ROOT / "morning_cache.json"
    if not p.is_file():
        return None
    ts = p.stat().st_mtime
    return datetime.fromtimestamp(ts, tz=_SEOUL_TZ).date()


def _arxiv_ok_marker_path(d: date) -> Path:
    return _CRON_DIR / f"arxiv_pipeline_ok_{d.isoformat()}.marker"


def _touch_arxiv_ok_marker() -> None:
    try:
        _CRON_DIR.mkdir(parents=True, exist_ok=True)
        p = _arxiv_ok_marker_path(_seoul_now().date())
        p.write_text(_seoul_now().isoformat(timespec="seconds") + "\n", encoding="utf-8")
    except OSError:
        pass


def _phase35_spawn_marker_path(d: date) -> Path:
    return _CRON_DIR / f"phase35_spawned_{d.isoformat()}.marker"


def _touch_phase35_spawn_marker() -> None:
    try:
        _CRON_DIR.mkdir(parents=True, exist_ok=True)
        _phase35_spawn_marker_path(_seoul_now().date()).write_text(
            _seoul_now().isoformat(timespec="seconds") + "\n", encoding="utf-8"
        )
    except OSError:
        pass


def _boardroom_archive_exists_for_date(d: date) -> bool:
    root = PROJECT_ROOT / "archives" / "boardroom"
    if not root.is_dir():
        return False
    prefix = d.strftime("%Y%m%d") + "_"
    for p in root.iterdir():
        if p.name.startswith(prefix) and p.suffix == ".md" and "_meeting" in p.name:
            return True
    return False


def _startup_recover_missed_daily_jobs(*, has_gemini: bool) -> None:
    """
    T7 늦게 마운트되거나 스케줄러가 지정 시각 이후에야 기동된 경우, 당일 분량을 한 번 보충.
    LLM 논문 토론 배치는 포함하지 않음.
    """
    now = _seoul_now()
    today = now.date()
    _CRON_DIR.mkdir(parents=True, exist_ok=True)

    if _phase35_daily_schedule_enabled():
        ms_at = _morning_scraper_schedule_at()
        ph_at = _phase35_curator_schedule_at()
        ms_dt = _wall_datetime_on(today, ms_at)
        ph_dt = _wall_datetime_on(today, ph_at)
        cache_day = _morning_cache_mtime_date()

        if cache_day != today and now >= ms_dt + _CATCHUP_GRACE:
            print(
                f"[startup-catchup] morning_cache 서울일자={cache_day} ≠ 오늘={today} "
                f"→ morning_scraper 보충 실행",
                flush=True,
            )
            try:
                run_morning_scraper()
            except Exception as e:
                print(f"[startup-catchup] morning_scraper 실패: {e}", flush=True)

        cache_day2 = _morning_cache_mtime_date()
        sp = _phase35_spawn_marker_path(today)
        if now >= ph_dt + _CATCHUP_GRACE and not sp.is_file():
            if cache_day2 == today:
                print("[startup-catchup] Phase35 당일 미스폰 → curator 보충 기동", flush=True)
                try:
                    run_phase35_curator()
                except Exception as e:
                    print(f"[startup-catchup] Phase35 실패: {e}", flush=True)
            else:
                print(
                    "[startup-catchup] Phase35 스킵: morning_cache가 오늘 날짜가 아님",
                    flush=True,
                )

    if has_gemini:
        ax_at = _arxiv_pipeline_schedule_at()
        ax_dt = _wall_datetime_on(today, ax_at)
        ok_m = _arxiv_ok_marker_path(today)
        if now >= ax_dt + _CATCHUP_GRACE and not ok_m.is_file():
            print("[startup-catchup] arXiv 파이프라인 성공 마커 없음 → ingest 보충 실행", flush=True)
            try:
                run_arxiv_pipeline()
            except Exception as e:
                print(f"[startup-catchup] arXiv 파이프라인 실패: {e}", flush=True)

    if _boardroom_schedule_enabled():
        weekday_ok = True
        if not _boardroom_schedule_daily():
            weekday_ok = now.weekday() < 5
        bt_at = _boardroom_schedule_time()
        bt_dt = _wall_datetime_on(today, bt_at)
        if (
            weekday_ok
            and now >= bt_dt + _CATCHUP_GRACE
            and not _boardroom_archive_exists_for_date(today)
            and _boardroom_child_already_running() is None
        ):
            print("[startup-catchup] Boardroom 오늘 회의 산출 없음 → swarm 보충 기동", flush=True)
            try:
                run_boardroom()
            except Exception as e:
                print(f"[startup-catchup] Boardroom 실패: {e}", flush=True)


def _phase35_daily_schedule_enabled() -> bool:
    """YES 심사관 + 오전 캐시(morning_scraper). 기본 켜짐."""
    v = (os.getenv("PHASE35_SCHEDULE_ENABLED") or "1").strip().lower()
    return v not in ("0", "false", "no", "off", "")


def _morning_scraper_schedule_at() -> str:
    t = (os.getenv("MORNING_SCRAPER_SCHEDULE_AT") or "07:30").strip()
    return t or "07:30"


def _phase35_curator_schedule_at() -> str:
    t = (os.getenv("PHASE35_CURATOR_SCHEDULE_AT") or "08:00").strip()
    return t or "08:00"


def _arxiv_pipeline_schedule_at() -> str:
    t = (os.getenv("ARXIV_PIPELINE_SCHEDULE_AT") or "01:00").strip()
    return t or "01:00"


def _boardroom_schedule_enabled() -> bool:
    v = (os.getenv("BOARDROOM_SCHEDULE_ENABLED") or "1").strip().lower()
    return v not in ("0", "false", "no", "off", "")


def _boardroom_schedule_time() -> str:
    t = (os.getenv("BOARDROOM_SCHEDULE_AT") or "10:00").strip()
    return t or "10:00"


def _boardroom_schedule_daily() -> bool:
    """기본 주말 포함 매일. ``BOARDROOM_SCHEDULE_DAILY=0`` 이면 월~금만 run_boardroom."""
    v = (os.getenv("BOARDROOM_SCHEDULE_DAILY") or "1").strip().lower()
    return v not in ("0", "false", "no", "off")


def _pid_is_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except (OSError, ValueError, TypeError):
        return False
    return True


def _boardroom_child_already_running() -> int | None:
    if not _BOARDROOM_CHILD_PID_PATH.is_file():
        return None
    try:
        raw = _BOARDROOM_CHILD_PID_PATH.read_text(encoding="utf-8").strip().split()
        if not raw:
            return None
        pid = int(raw[0])
    except (OSError, ValueError):
        return None
    if _pid_is_running(pid):
        return pid
    try:
        _BOARDROOM_CHILD_PID_PATH.unlink()
    except OSError:
        pass
    return None


def _spawn_boardroom_background() -> None:
    """``swarm_meeting`` 장시간 돌릴 수 있어 Popen만 하고, YES 없으면 자식이 즉시 종료."""
    existing = _boardroom_child_already_running()
    if existing is not None:
        print(
            f"   ⏭️ Boardroom이 이미 실행 중(pid={existing}) — 중복 기동 생략",
            flush=True,
        )
        return

    _CRON_DIR.mkdir(parents=True, exist_ok=True)
    log_path = _CRON_DIR / "boardroom_stdout.log"
    env = _subprocess_env()
    env["BOARDROOM_SCHEDULE_SKIP_IF_NO_YES"] = "1"
    cmd = [sys.executable, "-u", "-m", "apps.boardroom.swarm_meeting"]
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(f"\n{'=' * 60}\n[{stamp}] run_scheduler → Popen: {' '.join(cmd[2:])}\n")
        logf.flush()
        proc = subprocess.Popen(
            cmd,
            cwd=PROJECT_ROOT,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=logf,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        logf.write(f"boardroom_child_pid={proc.pid}\n")
        logf.flush()
    _BOARDROOM_CHILD_PID_PATH.write_text(f"{proc.pid}\n", encoding="utf-8")
    rel = log_path.relative_to(PROJECT_ROOT)
    print(
        f"   백그라운드 Boardroom PID={proc.pid} (로그: {rel}, pid: .cron/boardroom_child.pid)\n",
        flush=True,
    )


@with_scheduler_retry("Boardroom (swarm_meeting)")
def run_boardroom() -> None:
    print("\n" + "=" * 60)
    print("🏛️  [스케줄] Boardroom (LangGraph 회의) 실행 (백그라운드)")
    print("=" * 60)
    _spawn_boardroom_background()


@with_scheduler_retry("morning_scraper")
def run_morning_scraper() -> None:
    print("\n" + "=" * 60)
    print("☀️  [스케줄] morning_scraper → morning_cache.json")
    print("=" * 60)
    subprocess.run(
        [sys.executable, "-u", "-m", "apps.backfill.morning_scraper"],
        cwd=PROJECT_ROOT,
        env=_subprocess_env(),
        check=True,
        **_SUBPROCESS_KWARGS,
    )


def _spawn_phase35_curator_background() -> None:
    """심사 루프가 길 수 있어 메인 스케줄 루프를 막지 않음."""
    today = _seoul_now().date()
    m = _phase35_spawn_marker_path(today)
    if m.is_file():
        print(
            f"   ⏭️ Phase35 curator 오늘({today.isoformat()}) 이미 스폰됨 — 중복 생략",
            flush=True,
        )
        return
    _touch_phase35_spawn_marker()
    _CRON_DIR.mkdir(parents=True, exist_ok=True)
    log_path = _CRON_DIR / "phase35_curator_stdout.log"
    cmd = [sys.executable, "-u", "-m", "apps.backfill.phase35_auto_curator"]
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(f"\n{'=' * 60}\n[{stamp}] run_scheduler → Popen: {' '.join(cmd[2:])}\n")
        logf.flush()
        proc = subprocess.Popen(
            cmd,
            cwd=PROJECT_ROOT,
            env=_subprocess_env(),
            stdin=subprocess.DEVNULL,
            stdout=logf,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        logf.write(f"phase35_curator_child_pid={proc.pid}\n")
        logf.flush()
    rel = log_path.relative_to(PROJECT_ROOT)
    print(
        f"   백그라운드 Phase35 심사 PID={proc.pid} (로그: {rel})\n",
        flush=True,
    )


def run_phase35_curator() -> None:
    print("\n" + "=" * 60)
    print("📋 [스케줄] Phase35 YES 심사관 (백그라운드)")
    print("=" * 60)
    _spawn_phase35_curator_background()


def _llm_debate_schedule_enabled() -> bool:
    """파인튜닝용 ``llm_debate_scheduler`` 월~금 02:00 배치. 기본 꺼짐."""
    v = (os.getenv("LLM_DEBATE_SCHEDULE_ENABLED") or "0").strip().lower()
    return v in ("1", "true", "yes", "on", "y")


def _llm_debate_batch_duration_sec() -> int:
    """0 이하 = 시간 제한 없음. 미설정 시 0."""
    raw = (os.getenv("LLM_DEBATE_BATCH_DURATION_SEC") or "0").strip()
    try:
        return int(raw)
    except ValueError:
        return 0


@with_scheduler_retry("arXiv 파이프라인")
def run_arxiv_pipeline() -> None:
    """main.py 실행 (arXiv 수집 → RAG → raw_data_queue). 네트워크 에러 시 재시도 후 텔레그램 알림."""
    print("\n" + "=" * 60)
    print("📚 [스케줄] arXiv 파이프라인 실행")
    print("=" * 60)
    subprocess.run(
        [sys.executable, "-m", "pipelines.ingest.main"],
        cwd=PROJECT_ROOT,
        env=_subprocess_env(),
        check=True,
        **_SUBPROCESS_KWARGS,
    )
    _touch_arxiv_ok_marker()


def _spawn_llm_debate_batch_background(duration_sec: int) -> None:
    """
    무제한(또는 장시간) 배치는 subprocess.run으로 기다리지 않고 기동만 함.
    schedule.run_pending()·cron 1분 루프가 막히지 않도록 함.
    """
    with debate_spawn_lock():
        running = get_running_debate_scheduler_child_pid()
        if running is not None:
            print(
                f"   ⏭️ 논문 토론 배치가 이미 실행 중(pid={running}, 스케줄·텔레그램 공통) — 중복 기동 생략",
                flush=True,
            )
            return

        cmd = [
            sys.executable,
            "-u",
            "-m",
            "pipelines.debate.llm_debate_scheduler",
            "--test",
            "--duration-sec",
            str(duration_sec),
        ]
        log_path = PROJECT_ROOT / ".cron" / "llm_debate_batch_stdout.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as logf:
            logf.write(f"\n{'=' * 60}\n[{stamp}] run_scheduler → Popen: {' '.join(cmd[2:])}\n")
            logf.flush()
            proc = subprocess.Popen(
                cmd,
                cwd=PROJECT_ROOT,
                env=_subprocess_env(),
                stdin=subprocess.DEVNULL,
                stdout=logf,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            logf.write(f"child_pid={proc.pid}\n")
            logf.flush()

        register_debate_child_pid(proc.pid)
        rel = log_path.relative_to(PROJECT_ROOT)
        print(
            f"   백그라운드 PID={proc.pid} (로그: {rel}, pid: .cron/llm_debate_child.pid)",
            flush=True,
        )


@with_scheduler_retry("LLM 토론 배치")
def run_llm_debate() -> None:
    """llm_debate_scheduler.py --test. duration>0 만 동기 대기(재시도 적용). duration<=0 은 백그라운드."""
    d = _llm_debate_batch_duration_sec()
    print("\n" + "=" * 60)
    print("🚀 [스케줄] LLM 토론 배치 실행")
    if d <= 0:
        print("   (시간 제한 없음 → 백그라운드 기동, LLM_DEBATE_BATCH_DURATION_SEC=0 또는 미설정)")
    else:
        print(f"   (동기 실행, 최대 {d}초 ≈ {d / 3600:.2f}시간)")
    print("=" * 60)
    if d <= 0:
        _spawn_llm_debate_batch_background(0)
        return
    cmd = [
        sys.executable,
        "-u",
        "-m",
        "pipelines.debate.llm_debate_scheduler",
        "--test",
        "--duration-sec",
        str(d),
    ]
    pid: int
    with debate_spawn_lock():
        running = get_running_debate_scheduler_child_pid()
        if running is not None:
            print(
                f"   ⏭️ 논문 토론 배치가 이미 실행 중(pid={running}) — 동기 배치 생략",
                flush=True,
            )
            return

        proc = subprocess.Popen(cmd, cwd=PROJECT_ROOT, env=_subprocess_env(), **_SUBPROCESS_KWARGS)
        pid = proc.pid
        register_debate_child_pid(pid)
    try:
        rc = proc.wait()
    finally:
        clear_debate_child_pid_if_matches(pid)
    if rc != 0:
        raise subprocess.CalledProcessError(rc, cmd)


def _church_lyrics_schedule_enabled() -> bool:
    """주일 찬양 가사 자동화. NOTION_TOKEN 이 있고 ``CHURCH_LYRICS_SCHEDULE_ENABLED``≠0 일 때 등록."""
    v = (os.getenv("CHURCH_LYRICS_SCHEDULE_ENABLED") or "1").strip().lower()
    return bool((os.getenv("NOTION_TOKEN") or "").strip()) and v not in ("0", "false", "no", "off", "")


def _church_lyrics_pending_marker(d: date) -> Path:
    return _CRON_DIR / f"church_lyrics_pending_{d.isoformat()}.marker"


def _run_church_lyrics_sync(cmd: str) -> None:
    """``python -m apps.church_lyrics <cmd>`` 실행 → 결과를 job_runs.jsonl 에 남김. 종료 코드 2(콘티 없음)면 재시도 마커."""
    from tools.cron_engine.lib.storage import append_job_run

    _CRON_DIR.mkdir(parents=True, exist_ok=True)
    log_path = _CRON_DIR / "church_lyrics_stdout.log"
    argv = [sys.executable, "-u", "-m", "apps.church_lyrics", cmd]
    started = time.time()
    rc: int | None = None
    error: str | None = None
    try:
        with open(log_path, "a", encoding="utf-8") as logf:
            logf.write(f"\n{'=' * 60}\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] run_scheduler → {' '.join(argv[2:])}\n")
            logf.flush()
            rc = subprocess.run(
                argv, cwd=PROJECT_ROOT, env=_subprocess_env(), stdout=logf, stderr=subprocess.STDOUT,
                timeout=3 * 3600, **_SUBPROCESS_KWARGS,
            ).returncode
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
    status = {0: "succeeded", 2: "waiting_setlist"}.get(rc, "failed")
    evt = {
        "event": "church_lyrics_run",
        "job_id": f"church_lyrics_{cmd}",
        "status": status,
        "exit_code": rc,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(started)),
        "duration_ms": int((time.time() - started) * 1000),
    }
    if error:
        evt["error"] = error[:200]
    append_job_run(evt)
    print(f"   church_lyrics {cmd}: {status} (exit={rc}, 로그: .cron/church_lyrics_stdout.log)", flush=True)
    if cmd == "lyrics" and rc == 2:
        _church_lyrics_pending_marker(_seoul_now().date()).write_text(
            _seoul_now().isoformat(timespec="seconds") + "\n", encoding="utf-8"
        )


def _spawn_church_lyrics(cmd: str) -> None:
    """검색·모델 대기(429 쿨다운)가 길 수 있어 메인 루프를 막지 않도록 스레드로 실행."""
    import threading

    threading.Thread(target=_run_church_lyrics_sync, args=(cmd,), daemon=True, name=f"church_lyrics_{cmd}").start()


def run_church_rename() -> None:
    print("\n⛪ [스케줄] 주일 페이지 제목 정리 (church_lyrics rename)", flush=True)
    _spawn_church_lyrics("rename")


def run_church_lyrics() -> None:
    print("\n⛪ [스케줄] 주일 찬양 가사 게시 (church_lyrics lyrics)", flush=True)
    _spawn_church_lyrics("lyrics")


def run_church_lyrics_retry() -> None:
    """같은 날 09:00 실행이 콘티 없음(종료 코드 2)이었을 때만 한 번 더."""
    m = _church_lyrics_pending_marker(_seoul_now().date())
    if not m.is_file():
        return
    m.unlink(missing_ok=True)
    print("\n⛪ [스케줄] 콘티가 비어 있었음 → church_lyrics lyrics 재시도", flush=True)
    _spawn_church_lyrics("lyrics")


def main() -> None:
    # Gemini 없어도 cron_engine(봇 스케줄)은 돌아야 함. 예전에는 여기서 return 해 Ollama 전용일 때 job이 영원히 안 돌았음.
    has_gemini = bool(get_gemini_api_keys())
    if has_gemini:
        _ax_at = _arxiv_pipeline_schedule_at()
        schedule.every().day.at(_ax_at).do(run_arxiv_pipeline)
        if _llm_debate_schedule_enabled():
            for _day in _DEBATE_WEEKDAYS:
                getattr(schedule.every(), _day).at("02:00").do(run_llm_debate)
    else:
        print(
            "⚠️ Gemini API 키 없음 — arXiv 파이프라인을 등록하지 않습니다.\n"
            "   LLM 논문 토론 배치도 등록하지 않습니다.\n"
            "   cron_engine(등록한 매일/주간 작업)은 계속 동작합니다."
        )

    if _boardroom_schedule_enabled():
        _bt = _boardroom_schedule_time()
        if _boardroom_schedule_daily():
            schedule.every().day.at(_bt).do(run_boardroom)
        else:
            for _day in _DEBATE_WEEKDAYS:
                getattr(schedule.every(), _day).at(_bt).do(run_boardroom)
    else:
        print("   Boardroom 스케줄: BOARDROOM_SCHEDULE_ENABLED=0 — 등록 생략\n", flush=True)

    if _phase35_daily_schedule_enabled():
        _ms_at = _morning_scraper_schedule_at()
        _ph_at = _phase35_curator_schedule_at()
        schedule.every().day.at(_ms_at).do(run_morning_scraper)
        schedule.every().day.at(_ph_at).do(run_phase35_curator)
    else:
        print("   Phase35 일일 심사·morning_scraper: PHASE35_SCHEDULE_ENABLED=0 — 등록 생략\n", flush=True)

    if _church_lyrics_schedule_enabled():
        schedule.every().wednesday.at("08:35").do(run_church_rename)
        schedule.every().saturday.at("09:00").do(run_church_lyrics)
        schedule.every().saturday.at("11:00").do(run_church_lyrics_retry)

    # cron_engine: 1분마다 due job 체크 (agent_bot 과 중복 시 파일 락으로 1곳만 실행)
    start_cron_worker_daemon(respect_agent_disable_env=False)

    print("📅 통합 스케줄러 시작")
    if has_gemini:
        print(f"   - arXiv 파이프라인: 매일 {_arxiv_pipeline_schedule_at()} · ARXIV_PIPELINE_SCHEDULE_AT")
        if _llm_debate_schedule_enabled():
            _bd = _llm_debate_batch_duration_sec()
            _bmsg = (
                "시간 제한 없음(백그라운드·.cron/llm_debate_batch_stdout.log)"
                if _bd <= 0
                else f"동기 최대 {_bd}s"
            )
            print(
                f"   - LLM 논문 토론 배치: 월~금 02:00 (주 5회, {_bmsg} · LLM_DEBATE_BATCH_DURATION_SEC)"
            )
        else:
            print(
                "   - LLM 논문 토론 배치: LLM_DEBATE_SCHEDULE_ENABLED≠1 — 등록 생략 "
                "(켜려면 .env에 LLM_DEBATE_SCHEDULE_ENABLED=1)"
            )
    if _boardroom_schedule_enabled():
        if _boardroom_schedule_daily():
            _bmode = f"매일(월~일) {_boardroom_schedule_time()}"
        else:
            _bmode = f"월~금 {_boardroom_schedule_time()}"
        print(
            f"   - Boardroom: {_bmode} (백그라운드, YES 1건만/없으면 스킵, 로그: .cron/boardroom_stdout.log)"
        )
    if _phase35_daily_schedule_enabled():
        print(
            f"   - morning_scraper: 매일 {_morning_scraper_schedule_at()} → morning_cache.json (동기)"
        )
        print(
            f"   - Phase35 YES 심사: 매일 {_phase35_curator_schedule_at()} (백그라운드, 로그: .cron/phase35_curator_stdout.log)"
        )
    else:
        print("   - Phase35/morning_scraper: PHASE35_SCHEDULE_ENABLED=0 — 등록 생략")
    if _church_lyrics_schedule_enabled():
        print(
            "   - 주일 찬양: 수 08:35 제목 정리 · 토 09:00 가사 게시 (콘티 없으면 11:00 재시도, "
            "로그: .cron/church_lyrics_stdout.log)"
        )
    else:
        print("   - 주일 찬양: NOTION_TOKEN 없음 또는 CHURCH_LYRICS_SCHEDULE_ENABLED=0 — 등록 생략")
    print("   - cron_engine: 1분마다 due job 체크 → 텔레그램 선톡")
    poll_sec = _scheduler_poll_sec()
    print(f"   - 메인 루프 폴링: {poll_sec}s · SCHEDULER_POLL_SEC")
    print("   - 메인 봇: 별도 터미널에서 PYTHONPATH=. python3 -m apps.telegram_bot.main")
    print("   Ctrl+C로 종료\n")

    _startup_recover_missed_daily_jobs(has_gemini=has_gemini)

    while True:
        schedule.run_pending()
        time.sleep(poll_sec)


if __name__ == "__main__":
    main()
