#!/usr/bin/env python3
"""yunsur_v4 학습 데이터 생성 — 슬롯 균형 · 운영 system 정합 · 형식 자동 검증.

  cd mini && PYTHONPATH=. .venv/bin/python scripts/gen_v4_dataset.py --limit 5      # 스모크
  PYTHONPATH=. .venv/bin/python scripts/gen_v4_dataset.py                             # 본 실행
  PYTHONPATH=. .venv/bin/python scripts/gen_v4_dataset.py --slots chat,planner        # 일부 슬롯만
  PYTHONPATH=. .venv/bin/python scripts/gen_v4_dataset.py --assemble                  # 생성 없이 최종 파일만 재조립

입력
  finetune_datasets/v4/seeds/{chat,planner,coding}.txt   — 한 줄에 요청 문장 하나 (# 주석·빈 줄 무시)
  finetune_datasets/train_data_v3_clean.jsonl            — RAG 슬롯은 여기서 무작위 샘플
출력
  finetune_datasets/v4/raw/{slot}.jsonl     — 생성 원본 전부 (통과/거절 모두, 재개 가능)
  finetune_datasets/v4/rejected.jsonl       — 거절 + 사유 (데이터 품질 지표로 02_data_design.md 에 기록)
  finetune_datasets/v4/train_data_v4.jsonl  — 최종 {slot, system, instruction, output, source}
  finetune_datasets/v4/stats.json           — 슬롯별 생성/통과/거절 사유 집계

원칙
  1) system 은 봇이 실제 쓰는 프롬프트 상수 그대로 (core.llm.agent_prompts). 학습 = 운영 정합.
  2) 응답 생성은 베이스 qwen3.5:9b (평가에서 잡담·계획 0% 실패) — 자기 증류.
  3) output 은 평가 스크립트와 같은 판정기(lang_guard / code_extract / _parse_planner_llm_lines)를 통과한 것만.
  4) 평가 30문항(tests/fixtures/local_llm_failure_eval.jsonl)과 유사한 instruction 은 시드·증폭 단계에서 제외.
"""
from __future__ import annotations

import argparse
import ast
import difflib
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ.setdefault("OLLAMA_HOST", "http://127.0.0.1:11434")

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from langchain_core.messages import HumanMessage, SystemMessage

import core.config.agent_config as _cfg
from core.config.agent_config import ollama_kwargs
from core.graph.agent_nodes import _parse_planner_llm_lines
from core.llm.agent_llm import normalize_ai_message_content
from core.llm.agent_prompts import (
    DIRECT_ANSWER_DAILY_CHAT_SYSTEM,
    DIRECT_ANSWER_RAG_SYSTEM_BASE,
    EXECUTOR_SYSTEM_CODE_RUN,
    PLANNER_SYSTEM_BASE,
    direct_answer_daily_user,
    executor_user_prompt_code_run,
    planner_user_prompt,
)
from core.llm.code_extract import extract_python_code
from core.llm.lang_guard import english_ratio, strip_english_meta_sections

V4_DIR = ROOT / "finetune_datasets" / "v4"
SEED_DIR = V4_DIR / "seeds"
RAW_DIR = V4_DIR / "raw"
REJECT_PATH = V4_DIR / "rejected.jsonl"
TRAIN_PATH = V4_DIR / "train_data_v4.jsonl"
STATS_PATH = V4_DIR / "stats.json"
V3_CLEAN = ROOT / "finetune_datasets" / "train_data_v3_clean.jsonl"
EVAL_FIXTURE = ROOT / "tests" / "fixtures" / "local_llm_failure_eval.jsonl"

# 목표 건수 (README §4 설계). --target 로 덮어쓰기 가능
DEFAULT_TARGETS = {"rag": 400, "chat": 350, "planner": 250, "coding": 100}
SYSTEM_BY_SLOT = {
    "chat": DIRECT_ANSWER_DAILY_CHAT_SYSTEM,
    "planner": PLANNER_SYSTEM_BASE,
    "coding": EXECUTOR_SYSTEM_CODE_RUN,
    "rag": DIRECT_ANSWER_RAG_SYSTEM_BASE,
}
# 평가 문항과의 유사도 상한 (SequenceMatcher ratio). 넘으면 학습에서 제외
EVAL_SIM_MAX = 0.72
_THINK_RE = re.compile(r"<(?:/?)(?:redacted_)?think(?:ing)?>|<\|im_(?:start|end)\|>", re.IGNORECASE)


# ---------------------------------------------------------------- 유틸
def _read_jsonl(p: Path) -> list[dict]:
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _append(p: Path, row: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _norm(s: str) -> str:
    return re.sub(r"[\s\W_]+", "", (s or "").lower())


def _read_seeds(slot: str) -> list[str]:
    p = SEED_DIR / f"{slot}.txt"
    if not p.is_file():
        return []
    seeds = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            seeds.append(ln)
    return seeds


def _eval_blacklist() -> list[str]:
    return [r["text"] for r in _read_jsonl(EVAL_FIXTURE) if r.get("text")]


def _too_close_to_eval(text: str, blacklist: list[str]) -> tuple[bool, float]:
    a = _norm(text)
    best = 0.0
    for b in blacklist:
        r = difflib.SequenceMatcher(None, a, _norm(b)).ratio()
        if r > best:
            best = r
    return best >= EVAL_SIM_MAX, round(best, 3)


# ---------------------------------------------------------------- LLM
def _llm(model: str, *, temperature: float, num_predict: int, timeout: float):
    from langchain_ollama import ChatOllama

    return ChatOllama(
        **ollama_kwargs(
            model=model,
            temperature=temperature,
            top_p=0.9 if temperature > 0.5 else 0.8,
            repeat_penalty=1.15,
            reasoning=False,
            num_predict=num_predict,
            timeout=timeout + 5.0,
        )
    )


def _invoke(llm, messages, timeout: float) -> tuple[str, str]:
    """(status, text). status: ok | empty | timeout | error"""
    pool = ThreadPoolExecutor(max_workers=1)
    try:
        fut = pool.submit(lambda: llm.invoke(messages))
        resp = fut.result(timeout=timeout)
        text = (normalize_ai_message_content(resp) or "").strip()
        return ("ok", text) if text else ("empty", "")
    except FuturesTimeout:
        return "timeout", ""
    except Exception as e:  # noqa: BLE001
        return "error", f"{type(e).__name__}: {e}"
    finally:
        pool.shutdown(wait=False, cancel_futures=True)


# ---------------------------------------------------------------- 1) 시드 증폭
AMPLIFY_SYSTEM = "너는 한국어 챗봇 테스트 데이터를 만드는 도우미다. JSON 배열만 출력한다."
AMPLIFY_HINT = {
    "chat": "일상 대화·짧은 실용 요청(인사, 감사, 자기소개 질문, 슬랙/이메일 초안, 요약, 번역, 간단 설명, 추천). 코딩·논문 질문은 제외.",
    "planner": "봇에게 어떤 도구를 만들거나 작업을 자동화해 달라는 요청(크롤링, 파일 처리, API 호출, 데이터 정리, 스케줄 등). '~하는 도구 만들어줘', '~해줘' 말투.",
    "coding": "짧은 파이썬 코드로 바로 실행·출력할 수 있는 요청(계산, 문자열/리스트 처리, 간단 알고리즘). 값은 요청 문장 안에 예시로 넣고, '입력받아서/사용자가 입력한' 같은 stdin 요청과 외부 네트워크·파일 접근은 제외.",
}


def amplify_seed(llm, slot: str, seed: str, n: int) -> list[str]:
    prompt = (
        f"아래 '원본 요청'과 같은 종류이지만 주제·표현·길이가 서로 다른 한국어 요청 문장을 {n}개 만들어라.\n"
        f"종류 힌트: {AMPLIFY_HINT[slot]}\n"
        "조건: 실제 사용자가 텔레그램 봇에 칠 법한 자연스러운 반말/존댓말 섞어서, 한 문장 20~80자, 원본을 그대로 베끼지 말 것.\n"
        '출력은 JSON 배열 하나만: ["문장1", "문장2", ...]\n\n'
        f"원본 요청: {seed}"
    )
    status, text = _invoke(llm, [SystemMessage(content=AMPLIFY_SYSTEM), HumanMessage(content=prompt)], 120)
    if status != "ok":
        return []
    m = re.search(r"\[[\s\S]*\]", text)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
    except json.JSONDecodeError:
        return []
    out = []
    for s in arr:
        if isinstance(s, str):
            s = s.strip().strip('"')
            if 8 <= len(s) <= 160:
                out.append(s)
    return out


# ---------------------------------------------------------------- 2) 응답 생성 + 검증
_PARTICLES = "을|를|이|가|은|는|의|에|에서|에게|으로|로|와|과|도|만|까지|부터|처럼|보다|이나|나"
_SP_NUM_UNIT_RE = re.compile(r"(\d)\s+(?=[가-힣])")
_SP_LATIN_PARTICLE_RE = re.compile(rf"([A-Za-z0-9_.\-]+)\s+(?=(?:{_PARTICLES})(?=[\s,.!?)]|$))")


def _fix_spacing(text: str) -> str:
    """베이스 Qwen 특유의 토큰 경계 공백 제거: '10 개'→'10개', '8 시'→'8시', 'URL 을'→'URL을', 'Python 의'→'Python의'.
    학습 output 에 이 습관이 들어가면 v4 가 그대로 배우므로 생성 단계에서 정규화."""
    if not text:
        return text
    text = _SP_NUM_UNIT_RE.sub(r"\1", text)
    text = _SP_LATIN_PARTICLE_RE.sub(r"\1", text)
    return text


_CJK_RE = re.compile(r"[\u4e00-\u9fff]")  # Qwen 한자(중국어) 누출: '犒劳', '定时任务'
_API_KW_RE = re.compile(r"api|키|토큰|token|key|인증|외부 서비스|오픈웨더|tavily|공공데이터", re.IGNORECASE)
_WARN_LINE_RE = re.compile(r"^\s*(?:\d+단계:\s*)?\[주의\]", re.MULTILINE)


def post_filter(slot: str, instruction: str, output: str) -> tuple[str, str]:
    """생성 output 에 대한 최종 정리. (output, reject_reason). 거절이면 output 은 ''.
    raw 재조립(--assemble) 때도 같은 규칙을 다시 적용하므로, 규칙을 추가하면 기존 생성분에도 소급된다."""
    if slot in ("chat", "planner") and _CJK_RE.search(output):
        return "", "cjk_leak"
    if slot == "planner":
        lines = output.split("\n")
        steps = [ln for ln in lines if re.match(r"^\d+단계:", ln)]
        warn = [ln for ln in steps if "[주의]" in ln]
        if warn:
            # '[주의] .env 에 API 키 …' 는 프롬프트 지시문이 만든 보일러플레이트 — 요청에 근거 없으면 버림
            steps = [ln for ln in steps if "[주의]" not in ln]
            if len(steps) < 2:
                return "", "plan_only_warn"
            canon = [f"{i}단계: {re.sub(r'^\d+단계:\s*', '', ln)}" for i, ln in enumerate(steps, 1)]
            if _API_KW_RE.search(instruction):
                canon.append("[주의] .env에 필요한 API 키를 추가한 뒤 승인해 주세요.")
            canon.append("실행할까요? (승인/거절)")
            output = "\n".join(canon)
    return output, ""


def _coding_ok(code: str) -> tuple[bool, str]:
    if not code.strip():
        return False, "no_code"
    try:
        ast.parse(code)
    except SyntaxError as e:
        return False, f"syntax:{e.msg}"
    low = code.lower()
    if re.search(r"\binput\s*\(", code):
        return False, "uses_input"  # 운영(E2B)·검증 샌드박스 모두 stdin 없음 → 타임아웃 대신 즉시 거절
    if any(b in low for b in ("os.system", "subprocess", "shutil.rmtree", "socket", "requests.", "urllib", "open(")):
        return False, "banned_call"
    fd, path = tempfile.mkstemp(suffix="_v4.py")
    os.close(fd)
    try:
        Path(path).write_text(code, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=8,
            cwd=tempfile.gettempdir(),
            stdin=subprocess.DEVNULL,
        )
        if proc.returncode != 0:
            return False, "runtime:" + (proc.stderr or "")[-160:].strip()
        if not (proc.stdout or "").strip():
            return False, "no_output"
        return True, "ran"
    except subprocess.TimeoutExpired:
        return False, "runtime_timeout"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def gen_response(llm, slot: str, instruction: str, english_max: float, english_max_chat: float) -> dict:
    """{status, output, reject_reason, raw}. 통과 시 reject_reason == ''."""
    if slot == "chat":
        msgs = [
            SystemMessage(content=DIRECT_ANSWER_DAILY_CHAT_SYSTEM),
            HumanMessage(content=direct_answer_daily_user("(없음)", instruction)),
        ]
        status, raw = _invoke(llm, msgs, 90)
        if status != "ok":
            return {"status": status, "output": "", "reject_reason": status, "raw": raw}
        if _THINK_RE.search(raw):
            return {"status": "ok", "output": "", "reject_reason": "think_leak", "raw": raw}
        cleaned = strip_english_meta_sections(raw)
        if cleaned != raw:
            return {"status": "ok", "output": "", "reject_reason": "meta_section", "raw": raw}
        if "```" in raw:
            return {"status": "ok", "output": "", "reject_reason": "code_fence_in_chat", "raw": raw}
        if re.search(r"(?m)^\s*#{1,6}\s", raw):
            return {"status": "ok", "output": "", "reject_reason": "markdown_header", "raw": raw}
        if english_ratio(raw) > english_max_chat:
            return {"status": "ok", "output": "", "reject_reason": "english_mix", "raw": raw}
        if not (8 <= len(raw) <= 900):
            return {"status": "ok", "output": "", "reject_reason": "length", "raw": raw}
        return {"status": "ok", "output": _fix_spacing(raw), "reject_reason": "", "raw": raw}

    if slot == "planner":
        msgs = [
            SystemMessage(content=PLANNER_SYSTEM_BASE),
            HumanMessage(content=planner_user_prompt(3, "(도구 후보 없음)", "(참고 지식 없음)", "(없음)", instruction)),
        ]
        status, raw = _invoke(llm, msgs, 120)
        if status != "ok":
            return {"status": status, "output": "", "reject_reason": status, "raw": raw}
        if _THINK_RE.search(raw):
            return {"status": "ok", "output": "", "reject_reason": "think_leak", "raw": raw}
        if strip_english_meta_sections(raw) != raw:
            return {"status": "ok", "output": "", "reject_reason": "meta_section", "raw": raw}
        lines = _parse_planner_llm_lines(raw)
        if not (2 <= len(lines) <= 5):
            return {"status": "ok", "output": "", "reject_reason": f"plan_n:{len(lines)}", "raw": raw}
        joined = "\n".join(lines)
        if english_ratio(joined) > english_max:
            return {"status": "ok", "output": "", "reject_reason": "english_mix", "raw": raw}
        if re.search(r"```|^\s*(import|def|from)\s", joined, re.MULTILINE):
            return {"status": "ok", "output": "", "reject_reason": "code_in_plan", "raw": raw}
        # 학습 output 은 봇 파서가 뱉는 정규형으로 재직렬화 (운영 형식과 1:1)
        canon = []
        for i, ln in enumerate(lines, 1):
            # 파서가 살리는 형태 모두 정규화: "1단계:", "1.", "1)", "• 1단계:", "- ..."
            body = re.sub(r"^\s*(?:[•\-]\s*)?(?:\d+\s*(?:단계)?\s*[:：.)]\s*)?", "", ln).strip()
            if not body:
                continue
            canon.append(f"{i}단계: {_fix_spacing(body)}")
        canon.append("실행할까요? (승인/거절)")
        return {"status": "ok", "output": "\n".join(canon), "reject_reason": "", "raw": raw}

    if slot == "coding":
        plan_str = "1단계: 요청한 계산/출력을 하는 짧은 파이썬 코드 작성\n2단계: print로 결과 확인"
        msgs = [
            SystemMessage(content=EXECUTOR_SYSTEM_CODE_RUN),
            HumanMessage(content=executor_user_prompt_code_run(plan_str, instruction)),
        ]
        status, raw = _invoke(llm, msgs, 120)
        if status != "ok":
            return {"status": status, "output": "", "reject_reason": status, "raw": raw}
        code, how = extract_python_code(raw)
        if how not in ("fence", "plain"):
            return {"status": "ok", "output": "", "reject_reason": f"format_drift:{how}", "raw": raw}
        ok, detail = _coding_ok(code)
        if not ok:
            return {"status": "ok", "output": "", "reject_reason": detail.split(":", 1)[0], "raw": raw}
        return {"status": "ok", "output": f"```python\n{code}\n```", "reject_reason": "", "raw": raw}

    raise ValueError(slot)


# ---------------------------------------------------------------- 3) RAG 샘플링
def sample_rag(n: int, rng: random.Random) -> list[dict]:
    rows = _read_jsonl(V3_CLEAN)
    rows = [r for r in rows if r.get("instruction") and r.get("output")]
    rng.shuffle(rows)
    out = []
    for r in rows[:n]:
        out.append(
            {
                "slot": "rag",
                "system": DIRECT_ANSWER_RAG_SYSTEM_BASE,
                "instruction": r["instruction"].strip(),
                "output": r["output"].strip(),
                "source": "v3_clean" + (f" ({r['debate_theme']})" if r.get("debate_theme") else ""),
            }
        )
    return out


# ---------------------------------------------------------------- 4) 조립
def assemble(targets: dict[str, int], rng: random.Random) -> dict:
    stats: dict = {"targets": targets, "slots": {}}
    final: list[dict] = []
    for slot in ("chat", "planner", "coding"):
        rows = []
        for r in _read_jsonl(RAW_DIR / f"{slot}.jsonl"):
            if not r.get("output"):
                continue
            out, reason = post_filter(slot, r["instruction"], r["output"])
            if reason:
                _append(REJECT_PATH, {"slot": slot, "instruction": r["instruction"], "reason": reason, "raw_preview": r["output"][:300], "stage": "assemble"})
                continue
            rows.append({**r, "output": out})
        # instruction 중복 제거 (정규화 기준)
        seen: set[str] = set()
        uniq = []
        for r in rows:
            k = _norm(r["instruction"])
            if k in seen:
                continue
            seen.add(k)
            uniq.append(r)
        rng.shuffle(uniq)
        take = uniq[: targets.get(slot, 0)]
        final.extend(
            {
                "slot": slot,
                "system": SYSTEM_BY_SLOT[slot],
                "instruction": r["instruction"],
                "output": r["output"],
                "source": f"qwen3.5:9b self-distill (seed={r.get('seed', '')[:40]})",
            }
            for r in take
        )
        stats["slots"][slot] = {"generated_ok": len(rows), "unique": len(uniq), "used": len(take)}
    rag = sample_rag(targets.get("rag", 0), rng)
    final.extend(rag)
    stats["slots"]["rag"] = {"generated_ok": len(rag), "unique": len(rag), "used": len(rag)}
    rng.shuffle(final)
    TRAIN_PATH.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in final), encoding="utf-8")

    rej = _read_jsonl(REJECT_PATH)
    stats["rejected_total"] = len(rej)
    stats["rejected_by_slot_reason"] = {
        slot: dict(Counter(r.get("reason") for r in rej if r.get("slot") == slot))
        for slot in ("chat", "planner", "coding", "amplify")
    }
    stats["final_total"] = len(final)
    stats["final_by_slot"] = dict(Counter(r["slot"] for r in final))
    STATS_PATH.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return stats


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3.5:9b", help="응답·증폭 생성 모델 (기본 qwen3.5:9b)")
    ap.add_argument("--slots", default="chat,planner,coding", help="생성할 슬롯 (rag 는 샘플링만)")
    ap.add_argument("--target", default="", help="예: chat=350,planner=250,coding=100,rag=400")
    ap.add_argument("--variants", type=int, default=8, help="시드 1개당 증폭 문장 수")
    ap.add_argument("--limit", type=int, default=0, help="슬롯당 instruction N개만 (스모크)")
    ap.add_argument("--english-max", type=float, default=0.30, help="계획 슬롯 영어 비율 상한 (평가 0.45 보다 엄격)")
    ap.add_argument("--english-max-chat", type=float, default=0.15, help="잡담 슬롯 영어 비율 상한 ('anytime 입니다' 류 차단)")
    ap.add_argument("--seed", type=int, default=3407)
    ap.add_argument("--assemble", action="store_true", help="생성 없이 raw → train_data_v4 재조립만")
    args = ap.parse_args()

    targets = dict(DEFAULT_TARGETS)
    for kv in filter(None, args.target.split(",")):
        k, v = kv.split("=")
        targets[k.strip()] = int(v)
    rng = random.Random(args.seed)

    if args.assemble:
        stats = assemble(targets, rng)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return 0

    _cfg.OLLAMA_MODEL = args.model
    blacklist = _eval_blacklist()
    gen_llm = _llm(args.model, temperature=0.3, num_predict=1024, timeout=120)
    amp_llm = _llm(args.model, temperature=0.9, num_predict=1024, timeout=120)
    slots = [s.strip() for s in args.slots.split(",") if s.strip() and s.strip() != "rag"]

    for slot in slots:
        seeds = _read_seeds(slot)
        if not seeds:
            print(f"[{slot}] 시드 없음: {SEED_DIR / (slot + '.txt')} — 건너뜀")
            continue
        raw_path = RAW_DIR / f"{slot}.jsonl"
        done = {_norm(r["instruction"]) for r in _read_jsonl(raw_path)}
        ok_count = sum(
            1 for r in _read_jsonl(raw_path)
            if r.get("output") and not post_filter(slot, r["instruction"], r["output"])[1]
        )
        need = targets.get(slot, 0)
        # 거절률을 감안해 목표의 1.6배까지 instruction 확보
        want_instr = int(need * 1.6)
        print(f"\n===== [{slot}] seeds={len(seeds)} target={need} 이미 통과={ok_count} =====", flush=True)

        # 1) 시드 → instruction 풀 (시드 자체 + 증폭)
        instrs: list[tuple[str, str]] = []  # (instruction, seed)
        for sd in seeds:
            close, sim = _too_close_to_eval(sd, blacklist)
            if close:
                _append(REJECT_PATH, {"slot": "amplify", "instruction": sd, "reason": "eval_similar", "sim": sim})
                print(f"  [seed 제외] 평가 문항과 유사({sim}): {sd}")
                continue
            instrs.append((sd, sd))
        # 이미 raw 에 있는 instruction 은 풀에서 제외되므로, 목표까지 남은 만큼만 새로 뽑는다
        want_new = max(0, int((need - ok_count) * 1.6))
        seen_pool: set[str] = set(done)
        fresh: list[tuple[str, str]] = []
        for ins, sd in instrs:
            k = _norm(ins)
            if k not in seen_pool:
                seen_pool.add(k)
                fresh.append((ins, sd))
        for rnd in range(1, 5):
            if len(fresh) >= want_new:
                break
            rng.shuffle(seeds)
            for sd in seeds:
                if len(fresh) >= want_new:
                    break
                t0 = time.perf_counter()
                vs = amplify_seed(amp_llm, slot, sd, args.variants)
                added = 0
                for v in vs:
                    close, sim = _too_close_to_eval(v, blacklist)
                    if close:
                        _append(REJECT_PATH, {"slot": "amplify", "instruction": v, "reason": "eval_similar", "sim": sim})
                        continue
                    k = _norm(v)
                    if k in seen_pool:
                        continue
                    seen_pool.add(k)
                    fresh.append((v, sd))
                    added += 1
                print(f"  [증폭 r{rnd}] {sd[:30]}… → 신규 {added}개 (풀 {len(fresh)}/{want_new}, {time.perf_counter() - t0:.0f}s)", flush=True)
        instrs = fresh
        # 중복 제거
        seen: set[str] = set()
        uniq: list[tuple[str, str]] = []
        for ins, sd in instrs:
            k = _norm(ins)
            if k in seen or k in done:
                continue
            seen.add(k)
            uniq.append((ins, sd))
        if args.limit:
            uniq = uniq[: args.limit]
        print(f"  instruction {len(uniq)}개 생성 대상", flush=True)

        # 2) 응답 생성 + 검증
        for i, (ins, sd) in enumerate(uniq, 1):
            if ok_count >= need and not args.limit:
                print(f"  목표 {need} 도달 — 중단")
                break
            t0 = time.perf_counter()
            res = gen_response(gen_llm, slot, ins, args.english_max, args.english_max_chat)
            if res["output"]:
                res["output"], pf_reason = post_filter(slot, ins, res["output"])
                if pf_reason:
                    res["reject_reason"] = pf_reason
            el = round(time.perf_counter() - t0, 1)
            row = {
                "slot": slot,
                "instruction": ins,
                "seed": sd,
                "output": res["output"],
                "status": res["status"],
                "reject_reason": res["reject_reason"],
                "raw_preview": (res["raw"] or "")[:300],
                "elapsed_sec": el,
                "model": args.model,
            }
            _append(raw_path, row)
            if res["reject_reason"]:
                _append(REJECT_PATH, {"slot": slot, "instruction": ins, "reason": res["reject_reason"], "raw_preview": row["raw_preview"]})
                mark = f"✗ {res['reject_reason']}"
            else:
                ok_count += 1
                mark = "✓"
            print(f"  [{i}/{len(uniq)}] {mark:24} {el:5.1f}s  통과={ok_count}/{need}  {ins[:40]}", flush=True)

    stats = assemble(targets, rng)
    print("\n===== STATS =====")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"train={TRAIN_PATH}\nrejected={REJECT_PATH}\nstats={STATS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
