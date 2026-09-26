#!/usr/bin/env python3
"""운영 Executor 의 코딩 LLM(Groq)을 평가기와 '같은 프롬프트·같은 판정'으로 재본다.

목적: 교차 증류 교사 후보 판단 (docs/experiments/prior_work.md §6). 로컬과 직접 비교
가능한 숫자를 얻기 위해 평가기의 프롬프트·`_coding_ok`(ast.parse + 임시 디렉터리 8초
실행)·`extract_python_code` 를 그대로 재사용한다.

  python scripts/eval_groq_coding.py --repeats 3 --out /tmp/groq.jsonl
  python scripts/eval_groq_coding.py --limit 2          # 스모크

`GROQ_API_KEY` 필요. 2026-09-27 결과: openai/gpt-oss-120b 가 30문항 × 3회 **0/90 실패**,
시간 중앙값 2.8초 (base 14/90·5.9초, v9 19/90·7.0초).
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.chdir(Path(__file__).resolve().parents[1])

from scripts.eval_local_llm_failure import _coding_ok, extract_python_code  # 무거운 체인
from core.llm.agent_llm import get_coding_groq_llm, GROQ_CODING_MODEL, normalize_ai_message_content
from core.llm.agent_prompts import EXECUTOR_SYSTEM_CODE_RUN, executor_user_prompt_code_run
from langchain_core.messages import HumanMessage, SystemMessage

FIX = "tests/fixtures/local_llm_failure_eval.jsonl"

def items():
    out = []
    for line in open(FIX, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            if r["slot"] == "coding":
                out.append(r)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    its = items()[: a.limit] if a.limit else items()
    llm = get_coding_groq_llm()
    print(f"model={GROQ_CODING_MODEL} 문항={len(its)} 반복={a.repeats}", flush=True)
    rows = []
    for it in its:
        for t in range(1, a.repeats + 1):
            # 평가기의 코딩 슬롯과 같은 프롬프트
            plan = "1단계: 요청한 계산/출력을 하는 짧은 파이썬 코드 작성\n2단계: print로 결과 확인"
            prompt = executor_user_prompt_code_run(plan, it["text"])
            prompt += "\n\n설명 없이 실행 가능한 파이썬 코드만. 가능하면 ```python 블록."
            t0 = time.perf_counter()
            try:
                resp = llm.invoke([SystemMessage(content=EXECUTOR_SYSTEM_CODE_RUN),
                                   HumanMessage(content=prompt)])
                raw = (normalize_ai_message_content(resp) or "").strip()
                st = "ok" if raw else "empty"
            except Exception as e:
                raw, st = "", f"error:{type(e).__name__}"
            el = round(time.perf_counter() - t0, 2)
            code, unwrap = extract_python_code(raw)
            ok, detail = _coding_ok(code) if st == "ok" else (False, st)
            rows.append({"id": it["id"], "trial": t, "ok": ok, "fail_kind": "" if ok else detail.split(":", 1)[0],
                         "detail": detail, "code_unwrap": unwrap, "elapsed_sec": el,
                         "out_chars": len(raw), "preview": raw[:200]})
            print(f"  [{it['id']} t{t}] {'OK' if ok else 'FAIL:'+detail[:40]} {el}s unwrap={unwrap}", flush=True)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"→ {a.out}")
    bad = [r for r in rows if not r["ok"]]
    print(f"\n실패 {len(bad)}/{len(rows)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
