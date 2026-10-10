#!/usr/bin/env python3
"""v13 — 정답 없는 RAG 예시 30건을 새 형식으로 다시 만든다 (yunsur_v13 README §2).

  .venv/bin/python scripts/teacher_v13_nogold.py [--pids PATH] [--spares N]

- 대상: v12 학습에 들어간 정답 없는 30개 src_pid (같은 운영 프롬프트).
- 교사: Groq gpt-oss-120b, v12 교사 규칙 + 정답 없음 전용 형식(규칙 4b).
- 검증: verify_v12.check + 새 형식 3가지 + 문서 근거 LLM 검증(verify_v12_llm.PROMPT). 통과까지 최대 3회.
  3회 모두 실패하면 다른 적격 정답 없는 프롬프트로 대체하고 기록한다.
- 이어서 하기: 이미 통과한 src_pid 는 건너뛴다.
출력: finetune_datasets/v13/nogold.jsonl (통과분), nogold_log.jsonl (시도 전부)
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.teacher_v12 import TEACHER_RULES, wait_hint  # noqa: E402
from scripts.assemble_v12 import ko_ratio  # noqa: E402
from scripts.verify_v12 import check  # noqa: E402
from scripts.verify_v12_llm import PROMPT as VERIFY_PROMPT  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
V12 = ROOT / "finetune_datasets" / "v12"
D = ROOT / "finetune_datasets" / "v13"
MODEL = "openai/gpt-oss-120b"

INTRO = "제공된 문서에는 질문이 찾는 연구가 없습니다."
CONCL = "따라서 질문이 찾는 연구는 제공된 문서에서 찾을 수 없습니다."
NOGOLD_RULES = f"""
7. [정답 없음 형식 — 규칙 4 의 '정답 문서가 없다고 하면'을 이것으로 대신한다]
   - 서론 첫 문장은 정확히 `{INTRO}` 이다. 그 뒤 질문이 찾는 것을 한 문장으로 적는다.
   - 본론에는 주제가 가장 가까운 문서만 최대 2개 적는다. 각 항목 이름 뒤에 `(관련 연구)` 를 붙인다.
     예: `1. **논문 제목** (관련 연구): 문서 내용 [문서 2]`. 내용은 규칙 1~3 대로 그 문서에 있는 것만 쓴다.
     질문이 찾는 연구인 것처럼 쓰지 않는다. 문서가 영어여도 **한국어로** 요약해 쓴다(원문을 옮겨 적지 않는다).
   - 결론 첫 문장은 정확히 `{CONCL}` 이다. 그 뒤 관련 문서가 다루는 범위를 한 문장 이내로 적는다."""
HINT = "\n\n[정답 힌트] 질문이 찾는 논문은 제공된 문서에 없다."


def check_v13(ans: str, n_docs: int) -> list[str]:
    bad = check(ans, [], n_docs)
    intro_lines = [l.strip() for l in ans.split("### 본론", 1)[0].splitlines() if l.strip() and not l.startswith("###")]
    if not intro_lines or not intro_lines[0].startswith(INTRO):
        bad.append("서론첫문장")
    body = ans.split("### 본론", 1)[-1].split("### 결론", 1)[0]
    items = re.findall(r"^\s*\d+\.\s.*$", body, re.M)
    if not (1 <= len(items) <= 2) or any("(관련 연구)" not in it for it in items):
        bad.append("관련연구표시")
    if ko_ratio(ans) < 0.5:  # v12 와 같은 언어 필터 — 영어 원문을 옮겨 적은 답은 버린다
        bad.append("영어")
    concl = ans.split("### 결론", 1)[-1].strip()
    if not concl.startswith(CONCL):
        bad.append("결론첫문장")
    # 결론은 고정 문장 + 범위 한 문장까지 — 새 주장을 넣을 자리를 없앤다 (LLM 검증은 본론만 본다)
    elif len(re.findall(r"[.!?。](?:\s|$)", concl[len(CONCL):].strip() + " ")) > 1:
        bad.append("결론길이")
    return bad


# 정답 없음은 교사 힌트로 보장된 사실이다 — 결론의 고정 문장과 "문서가 질문 대상을 다루지 않는다"는
# 진술을 새 주장으로 떨어뜨리지 않게 한다. 본론 근거 기준은 v12 와 같다.
VERIFY_NOTE = (f"\n\n[참고] 이 질문이 찾는 연구는 참고 문서에 없다(확인된 사실). 결론의 `{CONCL}` 문장과 "
               "'제공된 문서들은 질문이 찾는 대상을 다루지 않는다'는 취지의 진술은 새 사실 주장으로 보지 않는다. "
               "본론 항목 이름에 붙은 `(관련 연구)` 표시도 주장이 아니다.")


def ground(llm, user: str, ans: str) -> tuple[bool, dict]:
    raw = call(llm, [("user", VERIFY_PROMPT.format(user=user, answer=ans) + VERIFY_NOTE)])
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return False, {"raw": raw[:300]}
    try:
        v = json.loads(m.group(0))
    except json.JSONDecodeError:
        return False, {"raw": raw[:300]}
    # 결론은 check_v13 의 형식 규칙으로 묶는다 — 판정기가 고정 문장 "찾을 수 없습니다"를 새 주장으로 계속 떨어뜨렸다
    ok = bool(v.get("items")) and all(i.get("supported") for i in v["items"])
    return ok, v


BASE_URL = ""  # main() 에서 --base-url 로 채운다 — 주면 Groq 대신 vLLM(OpenAI 호환)을 쓴다


def call(llm, msgs) -> str:
    if BASE_URL:
        import requests
        body = {"model": MODEL, "messages": [{"role": r, "content": c} for r, c in msgs],
                "temperature": 0.3, "max_tokens": 6000, "reasoning_effort": "medium"}
        for attempt in range(4):
            try:
                resp = requests.post(BASE_URL.rstrip("/") + "/chat/completions", json=body, timeout=900)
                return (resp.json()["choices"][0]["message"]["content"] or "").strip()
            except Exception as exc:
                print(f"  vLLM 재시도 {attempt + 1}: {str(exc)[:120]}", flush=True)
                time.sleep(15 * (attempt + 1))
        return ""
    from langchain_core.messages import HumanMessage, SystemMessage
    lc = [SystemMessage(content=c) if r == "system" else HumanMessage(content=c) for r, c in msgs]
    while True:
        try:
            return str(llm.invoke(lc).content or "").strip()
        except Exception as exc:  # 한도면 기다린다
            s = str(exc)
            if "rate_limit" in s or "429" in s:
                wt = wait_hint(s) if ("per day" in s or "TPD" in s) else 60.0
                print(f"  한도 대기 {wt / 60:.1f}분", flush=True)
                time.sleep(wt)
                continue
            raise


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pids", default=str(D / "v12_nogold_pids.json"))
    ap.add_argument("--tries", type=int, default=3)
    ap.add_argument("--pace", type=float, default=20.0)
    ap.add_argument("--base-url", default="", help="vLLM /v1 — 주면 Groq 대신 병렬로 돈다")
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()

    if args.base_url:
        global BASE_URL
        BASE_URL = args.base_url
        return run_parallel(args)

    import core.config.agent_config  # noqa: F401  (.env 로드)
    from langchain_groq import ChatGroq

    llm = ChatGroq(model=MODEL, api_key=os.getenv("GROQ_API_KEY"), temperature=0.3, max_retries=0)
    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (V12 / "prompts.jsonl").read_text().splitlines() if l.strip()}
    targets = json.loads(Path(args.pids).read_text())
    spares = sorted(p for p, r in P.items() if r.get("route") == "direct_answer/B" and r.get("user")
                    and not r.get("eval_leak") and not r["gold_in_context"] and p not in targets)
    random.Random(0).shuffle(spares)

    out_p, log_p = D / "nogold.jsonl", D / "nogold_log.jsonl"
    done = {json.loads(l)["src_pid"] for l in out_p.read_text().splitlines()} if out_p.exists() else set()
    need = len(targets)
    queue = [p for p in targets if p not in done]
    with out_p.open("a", encoding="utf-8") as w, log_p.open("a", encoding="utf-8") as lg:
        while queue and len(done) < need:
            pid = queue.pop(0)
            r = P[pid]
            n_docs = len(r["context_pids"])
            passed = None
            for t in range(1, args.tries + 1):
                ans = call(llm, [("system", r["system"] + TEACHER_RULES + NOGOLD_RULES + HINT), ("user", r["user"])])
                bad = check_v13(ans, n_docs)
                g_ok, verdict = (False, {}) if bad else ground(llm, r["user"], ans)
                lg.write(json.dumps({"src_pid": pid, "try": t, "auto": bad, "ground_ok": g_ok, "verdict": verdict,
                                     "answer": ans}, ensure_ascii=False) + "\n")
                lg.flush()
                print(f"{pid} try{t} auto={bad} ground={g_ok}", flush=True)
                time.sleep(args.pace)
                if not bad and g_ok:
                    passed = ans
                    break
            if passed:
                w.write(json.dumps({"src_pid": pid, "answer": passed, "replaced": pid not in targets},
                                   ensure_ascii=False) + "\n")
                w.flush()
                done.add(pid)
            elif spares:
                sp = spares.pop(0)
                print(f"  {pid} 3회 실패 → 대체 {sp}", flush=True)
                queue.append(sp)
    print(f"완료: {len(done)}/{need}", flush=True)
    return 0


def attempt(pid: str, P: dict, tries: int, lg, lock) -> str | None:
    r = P[pid]
    for t in range(1, tries + 1):
        ans = call(None, [("system", r["system"] + TEACHER_RULES + NOGOLD_RULES + HINT), ("user", r["user"])])
        bad = check_v13(ans, len(r["context_pids"]))
        g_ok, verdict = (False, {}) if bad else ground(None, r["user"], ans)
        with lock:
            lg.write(json.dumps({"src_pid": pid, "try": t, "auto": bad, "ground_ok": g_ok, "verdict": verdict,
                                 "answer": ans}, ensure_ascii=False) + "\n")
            lg.flush()
            print(f"{pid} try{t} auto={bad} ground={g_ok}", flush=True)
        if not bad and g_ok:
            return ans
    return None


def run_parallel(args) -> int:
    """vLLM 병렬: 대상 30개를 동시에, 실패한 수만큼 예비 프롬프트를 묶음으로 채운다."""
    import threading
    from concurrent.futures import ThreadPoolExecutor

    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (V12 / "prompts.jsonl").read_text().splitlines() if l.strip()}
    targets = json.loads(Path(args.pids).read_text())
    spares = sorted(p for p, r in P.items() if r.get("route") == "direct_answer/B" and r.get("user")
                    and not r.get("eval_leak") and not r["gold_in_context"] and p not in targets)
    random.Random(0).shuffle(spares)
    out_p, log_p = D / "nogold.jsonl", D / "nogold_log.jsonl"
    done = {json.loads(l)["src_pid"] for l in out_p.read_text().splitlines()} if out_p.exists() else set()
    lock = threading.Lock()
    batch = [p for p in targets if p not in done]
    with out_p.open("a", encoding="utf-8") as w, log_p.open("a", encoding="utf-8") as lg:
        while batch and len(done) < len(targets):
            with ThreadPoolExecutor(args.workers) as ex:
                res = list(ex.map(lambda p: (p, attempt(p, P, args.tries, lg, lock)), batch))
            for pid, ans in res:
                if ans and len(done) < len(targets):
                    w.write(json.dumps({"src_pid": pid, "answer": ans, "replaced": pid not in targets},
                                       ensure_ascii=False) + "\n")
                    done.add(pid)
            w.flush()
            short = len(targets) - len(done)
            batch, spares = spares[:short], spares[short:]
            if batch:
                print(f"  부족 {short} → 예비 {len(batch)}개 시도", flush=True)
    print(f"완료: {len(done)}/{len(targets)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
