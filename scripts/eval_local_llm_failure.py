#!/usr/bin/env python3
"""로컬 LLM 1차 실패율 측정 (API 폴백 없음).

고정 문항 × 반복. 로컬이 슬롯 성공 조건을 못 맞추면 실패로 센다.
Gemini/Groq는 호출하지 않는다. 코딩은 ast.parse + 짧은 로컬 exec (E2B 없음).

  cd mini && PYTHONPATH=. python scripts/eval_local_llm_failure.py
  python scripts/eval_local_llm_failure.py --repeats 3
  python scripts/eval_local_llm_failure.py --limit 1   # 스모크
  python scripts/eval_local_llm_failure.py --quality   # 품질 실패(영어 혼입·think 유출·반복)도 집계

실패 정의는 두 층이다.
- hard  : 타임아웃/빈 답/형식 파싱 실패/코드 문법·실행 오류  → ``ok`` / ``fail_kind``
- quality: 영어 혼입 과다·<think> 유출·같은 줄 반복·펜스 없는 잡담 등 → ``quality_ok`` / ``quality_kind``
  (항상 기록하며, ``--quality`` 를 주면 요약의 실패율에도 합산한다)
  판정 예외(yunsur_v5 사전 선언): 잡담의 ``code_fence_in_chat`` 은 요청이 템플릿·표·양식·서식·
  마크다운을 요구했으면 실패로 세지 않는다 (``TEMPLATE_REQUEST_RE``). 4모델에 동일 적용.
코드 추출은 Executor 노드와 같은 ``core.llm.code_extract.extract_python_code`` 를 쓴다
(펜스 변형·JSON {"code": ...} 래핑 대응). 벗겨낸 방식은 ``code_unwrap`` 으로 남긴다.

결과는 JSONL에 누적되며 같은 (id, trial)은 건너뛴다 (재개 가능).
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ.setdefault("OLLAMA_HOST", "http://127.0.0.1:11434")

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from langchain_core.messages import HumanMessage, SystemMessage

from core.config.agent_config import (
    OLLAMA_MODEL,
    ollama_kwargs,
)
from core.graph.agent_nodes import _parse_planner_llm_lines
from core.llm.agent_llm import normalize_ai_message_content
from core.llm.code_extract import extract_python_code
from core.llm.agent_prompts import (
    DIRECT_ANSWER_DAILY_CHAT_SYSTEM,
    DIRECT_ANSWER_RAG_SYSTEM_BASE,
    EXECUTOR_SYSTEM_CODE_RUN,
    PLANNER_SYSTEM_BASE,
    RAG_OUTPUT_TEMPLATE_MULTI_STRICT,
    direct_answer_daily_user,
    direct_answer_rag_user,
    executor_user_prompt_code_run,
    planner_user_prompt,
)

FALLBACK_MSG = "죄송해요, 답변을 생성하지 못했어요"
PLANNER_FALLBACK = [
    "1단계: 사용자의 특별한 요청에 따른 코드 작성",
    "2단계: 샌드박스 실행 및 결과 확인",
]


def _ollama_ok() -> tuple[bool, str]:
    base = (os.getenv("OLLAMA_HOST") or "http://127.0.0.1:11434").rstrip("/")
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        names = [m.get("name") for m in data.get("models") or []]
        return True, f"ok models={names[:8]}"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _load_items(path: Path) -> list[dict]:
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        items.append(json.loads(line))
    return items


def _done_keys(out_path: Path) -> set[tuple[str, int]]:
    done: set[tuple[str, int]] = set()
    if not out_path.is_file():
        return done
    for line in out_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        iid, trial = row.get("id"), row.get("trial")
        if iid and isinstance(trial, int):
            done.add((str(iid), trial))
    return done


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()


def _invoke_local_num_predict(messages, timeout_sec: float, num_predict: int) -> dict:
    from langchain_ollama import ChatOllama
    from core.config.agent_config import ollama_planner_reasoning_enabled

    llm = ChatOllama(
        **ollama_kwargs(
            temperature=0.2,
            top_p=0.8,
            repeat_penalty=1.18,
            reasoning=False,
            num_predict=num_predict,
            timeout=max(float(timeout_sec) + 5.0, 30.0),
        )
    )
    t0 = time.perf_counter()
    pool = ThreadPoolExecutor(max_workers=1)
    try:
        fut = pool.submit(lambda: llm.invoke(messages))
        resp = fut.result(timeout=timeout_sec)
        text = normalize_ai_message_content(resp)
        elapsed = time.perf_counter() - t0
        if not (text or "").strip():
            return {"status": "empty", "text": "", "elapsed_sec": round(elapsed, 3)}
        return {"status": "ok", "text": text.strip(), "elapsed_sec": round(elapsed, 3)}
    except FuturesTimeout:
        elapsed = time.perf_counter() - t0
        return {"status": "timeout", "text": "", "elapsed_sec": round(elapsed, 3)}
    except Exception as e:  # noqa: BLE001
        elapsed = time.perf_counter() - t0
        return {
            "status": "error",
            "text": "",
            "elapsed_sec": round(elapsed, 3),
            "error": f"{type(e).__name__}: {e}",
        }
    finally:
        pool.shutdown(wait=False, cancel_futures=True)


from core.llm.lang_guard import english_ratio as _english_ratio  # 봇 노드와 동일한 지표

_THINK_LEAK_RE = re.compile(r"<(?:/?)(?:redacted_)?think(?:ing)?>|<\|im_(?:start|end)\|>", re.IGNORECASE)

# 잡담 펜스 판정 예외 (yunsur_v5 사전 선언, docs/experiments/yunsur_v5/README.md §3):
# 요청이 템플릿·표·양식·서식·마크다운을 요구했으면 답변의 코드 펜스는 합리적이므로 실패로 세지 않는다.
# scripts/gen_v5_dataset.py 의 TEMPLATE_REQUEST_RE 와 같은 패턴이어야 한다 (생성 필터 = 평가 판정기).
# 두 패턴이 갈라지지 않도록 tests/unit/test_eval_chat_fence_exception.py 가 동일성을 검사한다.
TEMPLATE_REQUEST_RE = re.compile(r"템플릿|양식|서식|표로|표 만들|표를|마크다운|markdown", re.IGNORECASE)


def _wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """실패율의 95% Wilson 점수 구간. (low, high) 또는 n=0 이면 None.

    왜 필요한가 (docs/experiments/protocol.md): n=24 에서 1건은 4.17%p 다. yunsur_v5~v7 에서
    같은 모델·같은 문항의 실패가 밤마다 ±1~2건 움직였고, 그 폭이 판정선 ±5%p 와 같은
    크기였다. 실패율만 적으면 그 사실이 보이지 않으므로 구간을 같이 기록한다.
    정규근사(wald)는 k=0 에서 폭이 0 이 되어 오해를 부르므로 Wilson 을 쓴다.
    """
    if n <= 0:
        return None
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return round(max(0.0, center - half), 4), round(min(1.0, center + half), 4)


def _repeated_line(text: str, min_chars: int = 20, times: int = 3) -> bool:
    """같은 긴 줄이 3번 이상 나오면 반복 붕괴로 본다."""
    cnt = Counter(ln.strip() for ln in (text or "").splitlines() if len(ln.strip()) >= min_chars)
    return any(c >= times for c in cnt.values())


def _quality_check(slot: str, text: str, *, english_max: float, request: str = "") -> tuple[bool, str]:
    """(quality_ok, quality_kind). hard 통과한 답변에만 의미 있음.

    ``request`` 는 그 답변을 만든 요청 문장. 잡담 펜스 예외 판정에만 쓴다.
    """
    body = text or ""
    if _THINK_LEAK_RE.search(body):
        return False, "think_leak"
    if _repeated_line(body):
        return False, "repetition"
    if slot in ("chat", "rag", "planner"):
        r = _english_ratio(body)
        if r > english_max:
            return False, f"english_mix"
    if slot == "chat" and "```" in body and not TEMPLATE_REQUEST_RE.search(request or ""):
        return False, "code_fence_in_chat"
    return True, ""


def _coding_ok(code: str) -> tuple[bool, str]:
    if not code.strip():
        return False, "no_code"
    try:
        ast.parse(code)
    except SyntaxError as e:
        return False, f"syntax:{e.msg}"
    banned = ("os.system", "subprocess", "shutil.rmtree", "socket", "requests.", "pathlib")
    low = code.lower()
    if any(b.lower() in low for b in banned):
        # still syntax-ok; allow pathlib/os for simple scripts but block subprocess/system
        if "os.system" in low or "subprocess" in low:
            return False, "banned_call"
    fd, path = tempfile.mkstemp(suffix="_eval.py")
    os.close(fd)
    try:
        Path(path).write_text(code, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=8,
            cwd=tempfile.gettempdir(),
        )
        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "")[-240:]
            return False, f"runtime:{err.strip()[:200]}"
        return True, "ran"
    except subprocess.TimeoutExpired:
        return False, "runtime_timeout"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _rag_context(user_request: str) -> tuple[str, int]:
    try:
        from core.rag.agent_chroma_rag import get_chroma_rag_tool
        from core.graph.agent_nodes import _extract_english_rag_query
    except Exception as e:  # noqa: BLE001
        return f"(RAG 로드 실패: {e})", 0
    try:
        rag = get_chroma_rag_tool()
        q = _extract_english_rag_query(user_request, session_context="")
        ctx = rag.search(q, session_context="") or ""
        return ctx, len(ctx)
    except Exception as e:  # noqa: BLE001
        return f"(RAG 검색 실패: {e})", 0


def run_one(item: dict, *, english_max: float = 0.45) -> dict:
    slot = item["slot"]
    text = item["text"]
    timeout_sec = float(item.get("timeout_sec") or 55)
    if slot == "chat":
        messages = [
            SystemMessage(content=DIRECT_ANSWER_DAILY_CHAT_SYSTEM),
            HumanMessage(content=direct_answer_daily_user("(없음)", text)),
        ]
        inv = _invoke_local_num_predict(messages, timeout_sec, num_predict=512)
        ok = inv["status"] == "ok" and len(inv.get("text") or "") >= 8
        fail_kind = "" if ok else (inv["status"] if inv["status"] != "ok" else "too_short")
        q_ok, q_kind = _quality_check("chat", inv.get("text") or "", english_max=english_max, request=text) if ok else (False, "")
        return {
            **inv,
            "ok": ok,
            "fail_kind": fail_kind,
            "quality_ok": q_ok,
            "quality_kind": q_kind,
            "english_ratio": round(_english_ratio(inv.get("text") or ""), 3),
            "preview": (inv.get("text") or "")[:240],
        }

    if slot == "rag":
        ctx, ctx_len = _rag_context(text)
        user = direct_answer_rag_user(
            "(없음)",
            ctx,
            "",
            text,
            output_template_strict=RAG_OUTPUT_TEMPLATE_MULTI_STRICT,
        )
        messages = [
            SystemMessage(content=DIRECT_ANSWER_RAG_SYSTEM_BASE),
            HumanMessage(content=user),
        ]
        inv = _invoke_local_num_predict(messages, timeout_sec, num_predict=2048)
        body = inv.get("text") or ""
        ok = inv["status"] == "ok" and len(body) >= 120 and FALLBACK_MSG not in body
        fail_kind = "" if ok else (inv["status"] if inv["status"] != "ok" else "too_short")
        q_ok, q_kind = _quality_check("rag", body, english_max=english_max, request=text) if ok else (False, "")
        return {
            **inv,
            "ok": ok,
            "fail_kind": fail_kind,
            "quality_ok": q_ok,
            "quality_kind": q_kind,
            "english_ratio": round(_english_ratio(body), 3),
            "rag_ctx_chars": ctx_len,
            "preview": body[:240],
        }

    if slot == "planner":
        messages = [
            SystemMessage(content=PLANNER_SYSTEM_BASE),
            HumanMessage(
                content=planner_user_prompt(3, "(도구 후보 없음)", "(참고 지식 없음)", "(없음)", text)
            ),
        ]
        inv = _invoke_local_num_predict(messages, timeout_sec, num_predict=400)
        body = inv.get("text") or ""
        lines = _parse_planner_llm_lines(body)
        parse_ok = len(lines) >= 2 and lines != PLANNER_FALLBACK
        ok = inv["status"] == "ok" and parse_ok
        if inv["status"] != "ok":
            fail_kind = inv["status"]
        elif not parse_ok:
            fail_kind = "parse_fail"
        else:
            fail_kind = ""
        q_ok, q_kind = _quality_check("planner", "\n".join(lines), english_max=english_max, request=text) if ok else (False, "")
        return {
            **inv,
            "ok": ok,
            "fail_kind": fail_kind,
            "quality_ok": q_ok,
            "quality_kind": q_kind,
            "plan_n": len(lines),
            "plan_lines": lines[:6],
            "preview": body[:240],
        }

    if slot == "coding":
        plan_str = "1단계: 요청한 계산/출력을 하는 짧은 파이썬 코드 작성\n2단계: print로 결과 확인"
        prompt = executor_user_prompt_code_run(plan_str, text)
        prompt += "\n\n설명 없이 실행 가능한 파이썬 코드만. 가능하면 ```python 블록."
        messages = [
            SystemMessage(content=EXECUTOR_SYSTEM_CODE_RUN),
            HumanMessage(content=prompt),
        ]
        inv = _invoke_local_num_predict(messages, timeout_sec, num_predict=800)
        body = inv.get("text") or ""
        code, unwrap = extract_python_code(body)
        ran_ok, detail = _coding_ok(code) if inv["status"] == "ok" else (False, inv["status"])
        ok = inv["status"] == "ok" and ran_ok
        if inv["status"] != "ok":
            fail_kind = inv["status"]
        elif not ran_ok:
            fail_kind = detail.split(":", 1)[0]
        else:
            fail_kind = ""
        if ok:
            q_ok, q_kind = _quality_check("coding", body, english_max=1.0, request=text)
            if q_ok and unwrap in ("json", "fence_json", "fence_multi", "fence_open"):
                q_ok, q_kind = False, f"format_drift:{unwrap}"
        else:
            q_ok, q_kind = False, ""
        return {
            **inv,
            "ok": ok,
            "fail_kind": fail_kind,
            "quality_ok": q_ok,
            "quality_kind": q_kind,
            "coding_detail": detail,
            "code_unwrap": unwrap,
            "code_preview": code[:400],
            "preview": body[:240],
        }

    raise ValueError(f"unknown slot {slot}")


def _summarize(out_path: Path, model: str, *, include_quality: bool = False) -> dict:
    rows = []
    if out_path.is_file():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    n = len(rows)
    fails = [r for r in rows if not r.get("ok")]
    # quality_ok 키가 없는 옛 결과는 품질 통과로 간주 (v1 결과와 호환)
    q_fails = [r for r in rows if r.get("ok") and r.get("quality_ok") is False]
    strict_fails = len(fails) + len(q_fails)
    by_slot: dict[str, list] = defaultdict(list)
    for r in rows:
        by_slot[r.get("slot") or "?"].append(r)
    slot_stats = {}
    for slot, rs in sorted(by_slot.items()):
        nf = sum(1 for x in rs if not x.get("ok"))
        kinds = Counter(x.get("fail_kind") or "ok" for x in rs)
        nq = sum(1 for x in rs if x.get("ok") and x.get("quality_ok") is False)
        qkinds = Counter(x.get("quality_kind") for x in rs if x.get("ok") and x.get("quality_ok") is False)
        elapsed = sorted(float(x.get("elapsed_sec") or 0) for x in rs)
        slot_stats[slot] = {
            "n": len(rs),
            "fail": nf,
            "fail_rate": round(nf / len(rs), 4) if rs else None,
            "fail_kinds": dict(kinds),
            "quality_fail": nq,
            "quality_kinds": dict(qkinds),
            "strict_fail_rate": round((nf + nq) / len(rs), 4) if rs else None,
            "strict_fail_ci95": _wilson_ci(nf + nq, len(rs)),
            "fail_ci95": _wilson_ci(nf, len(rs)),
            "elapsed_median_sec": round(elapsed[len(elapsed) // 2], 1) if elapsed else None,
            "elapsed_max_sec": round(elapsed[-1], 1) if elapsed else None,
        }
    summary = {
        "generated": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "model": model,
        "n": n,
        "fail": len(fails),
        "fail_rate": round(len(fails) / n, 4) if n else None,
        "quality_fail": len(q_fails),
        "strict_fail": strict_fails,
        "strict_fail_rate": round(strict_fails / n, 4) if n else None,
        "strict_fail_ci95": _wilson_ci(strict_fails, n),
        "fail_ci95": _wilson_ci(len(fails), n),
        "repeats": max((int(r.get("trial") or 1) for r in rows), default=0),
        "one_liner": (
            f"고정 {len({r.get('id') for r in rows})}문항 반복 포함 n={n}, 로컬 1차만: "
            f"hard 실패 {len(fails)}/{n} = {100 * len(fails) / n:.0f}%"
            + (
                f" · 품질 포함 {strict_fails}/{n} = {100 * strict_fails / n:.0f}%"
                if include_quality
                else ""
            )
            if n
            else "결과 없음"
        ),
        "by_slot": slot_stats,
        "results_path": str(out_path),
    }
    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--file",
        type=Path,
        default=ROOT / "tests" / "fixtures" / "local_llm_failure_eval.jsonl",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / ".cron" / "local_llm_failure_eval.jsonl",
    )
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0, help="앞에서 N문항만 (스모크)")
    ap.add_argument("--slots", default="", help="쉼표 구분 chat,rag,planner,coding")
    ap.add_argument("--model", default="", help="Ollama 모델명 (기본 LOCAL_LLM_MODEL). 예: qwen3.5:9b 로 베이스 A/B")
    ap.add_argument("--quality", action="store_true", help="품질 실패(영어 혼입·think 유출·반복)를 요약 실패율에 합산")
    ap.add_argument(
        "--english-max",
        type=float,
        default=0.45,
        help="chat/rag/planner에서 (한글+라틴) 중 라틴 비율이 이 값을 넘으면 english_mix (기본 0.45)",
    )
    args = ap.parse_args()
    if args.model:
        os.environ["LOCAL_LLM_MODEL"] = args.model
        import core.config.agent_config as _cfg
        _cfg.OLLAMA_MODEL = args.model
        globals()["OLLAMA_MODEL"] = args.model

    ok, why = _ollama_ok()
    if not ok:
        print(f"Ollama 불가: {why}")
        return 2

    items = _load_items(args.file)
    if args.slots:
        allow = {s.strip() for s in args.slots.split(",") if s.strip()}
        items = [i for i in items if i.get("slot") in allow]
    if args.limit and args.limit > 0:
        items = items[: args.limit]

    jobs = [(it, t) for it in items for t in range(1, args.repeats + 1)]
    done = _done_keys(args.out)
    pending = [(it, t) for it, t in jobs if (it["id"], t) not in done]
    print(
        f"model={OLLAMA_MODEL} ollama={why}\n"
        f"total={len(jobs)} done={len(jobs) - len(pending)} pending={len(pending)}\n"
        f"out={args.out}"
    )

    for i, (it, trial) in enumerate(pending, 1):
        print(
            f"\n[{i}/{len(pending)}] {it['id']} trial={trial} slot={it['slot']} "
            f"timeout={it.get('timeout_sec')}s",
            flush=True,
        )
        t0 = time.perf_counter()
        try:
            res = run_one(it, english_max=args.english_max)
        except Exception as e:  # noqa: BLE001
            res = {
                "status": "error",
                "ok": False,
                "fail_kind": "error",
                "text": "",
                "elapsed_sec": round(time.perf_counter() - t0, 3),
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc()[-800:],
            }
        row = {
            "id": it["id"],
            "slot": it["slot"],
            "trial": trial,
            "timeout_sec": it.get("timeout_sec"),
            "model": OLLAMA_MODEL,
            **res,
        }
        # 원문 전체는 파일만 비대하게 만드니 preview/code만 유지
        row.pop("text", None)
        _append_jsonl(args.out, row)
        mark = "OK" if row.get("ok") else f"FAIL:{row.get('fail_kind')}"
        print(
            f"  → {mark} elapsed={row.get('elapsed_sec')}s preview={(row.get('preview') or '')[:80]!r}",
            flush=True,
        )

    summary = _summarize(args.out, OLLAMA_MODEL, include_quality=args.quality)
    sum_path = args.out.with_name(args.out.stem + "_summary.json")
    sum_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n===== SUMMARY =====")
    print(summary["one_liner"])
    print(json.dumps(summary["by_slot"], ensure_ascii=False, indent=2))
    print(f"summary={sum_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
