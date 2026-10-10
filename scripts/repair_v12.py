#!/usr/bin/env python3
"""LLM 근거 검증에서 탈락한 v12 교사 답을 '삭제·축약만' 으로 고치고 다시 검증한다 — yunsur_v12 README §2.4.

  .venv/bin/python scripts/repair_v12.py --base-url <vLLM /v1>

새 내용은 추가하지 않는다. 고친 답은 자동 검증 + LLM 근거 검증을 다시 통과해야 쓴다.
출력: finetune_datasets/v12/repaired.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_v12 import check  # noqa: E402
from verify_v12_llm import PROMPT as VERIFY_PROMPT  # noqa: E402

D = Path(__file__).resolve().parent.parent / "finetune_datasets" / "v12"
MODEL = "openai/gpt-oss-120b"

REPAIR = """아래 [답변]은 [참고 문서]에 근거하지 않은 문장이 있어 검증에서 탈락했다. [지적]을 보고 답변을 고쳐라.

규칙:
- 지적된 주장은 **삭제**하거나, 인용한 [문서 N] 블록에 실제로 있는 표현으로 **줄인다**. 새 내용·새 비교·새 평가를 **추가하지 않는다**.
- "기존 대비 차별점"이 문서에 없으면 쓰지 않는다 (템플릿이 요구해도 생략).
- 결론은 고친 본론에 남은 내용만 한두 문장으로 종합한다.
- 출력 템플릿(### 서론 / ### 본론 / ### 결론), `[문서 N]` 인용 형식, 서론 첫 문장(있다면 "제공된 문서에는 질문이 찾는 연구가 없습니다.")은 유지한다.
- 고친 답변 전체만 출력한다.

[참고 문서와 질문]
{user}

[답변]
{answer}

[지적]
{issues}"""


def chat(url: str, content: str, max_tokens: int, temperature: float) -> str:
    body = {"model": MODEL, "temperature": temperature, "max_tokens": max_tokens, "reasoning_effort": "medium",
            "messages": [{"role": "user", "content": content}]}
    r = requests.post(url, json=body, timeout=600)
    r.raise_for_status()
    return (r.json()["choices"][0]["message"].get("content") or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--answers", default="teacher.jsonl", help="고칠 답이 든 파일(answer 필드)")
    ap.add_argument("--verdicts", default="verified_llm.jsonl", help="판정 파일(ok·verdict·auto_bad)")
    ap.add_argument("--out", default="repaired.jsonl")
    args = ap.parse_args()
    url = args.base_url.rstrip("/") + "/chat/completions"

    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (D / "prompts.jsonl").read_text().splitlines() if l.strip()}
    G = {json.loads(l)["src_pid"]: json.loads(l).get("gold_nums") or [] for l in (D / "teacher.jsonl").read_text().splitlines() if l.strip()}
    T = {json.loads(l)["src_pid"]: {**json.loads(l), "gold_nums": G.get(json.loads(l)["src_pid"], [])}
         for l in (D / args.answers).read_text().splitlines() if l.strip()}
    V = [json.loads(l) for l in (D / args.verdicts).read_text().splitlines() if l.strip()]
    out_path = D / args.out
    done = set()
    if out_path.exists():
        done = {json.loads(l)["src_pid"] for l in out_path.read_text().splitlines() if l.strip()}
    todo = [v for v in V if not v["ok"] and v["src_pid"] not in done]
    lock = threading.Lock()
    print(f"수리 대상 {len(todo)}", flush=True)

    def one(v: dict) -> None:
        pid = v["src_pid"]
        p, t = P[pid], T[pid]
        vd = v.get("verdict") or {}
        issues = "\n".join(f"- 본론 {i['n']}: {i.get('issue', '')}" for i in vd.get("items", []) if not i.get("supported"))
        if vd and not vd.get("conclusion_ok", True):
            issues += "\n- 결론: 본론에 없는 주장이 있다"
        if v.get("auto_bad"):
            issues += "\n- 형식 문제: " + ", ".join(v["auto_bad"])
        for attempt in range(3):
            try:
                new = chat(url, REPAIR.format(user=p["user"], answer=t["answer"], issues=issues), 6000, 0.2)
                auto_bad = check(new, t.get("gold_nums") or [], len(p["context_pids"]))
                ok, verdict = False, None
                if not auto_bad:
                    txt = chat(url, VERIFY_PROMPT.format(user=p["user"], answer=new), 4000, 0.0)
                    verdict = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
                    ok = bool(verdict.get("items")) and all(i.get("supported") for i in verdict["items"]) and bool(verdict.get("conclusion_ok"))
                with lock, out_path.open("a", encoding="utf-8") as w:
                    w.write(json.dumps({"src_pid": pid, "ok": ok, "auto_bad": auto_bad, "answer": new, "verdict": verdict},
                                       ensure_ascii=False) + "\n")
                print(f"  {pid} ok={ok} auto={auto_bad}", flush=True)
                return
            except Exception as exc:
                print(f"  재시도 {pid} ({attempt + 1}): {str(exc)[:120]}", flush=True)
                time.sleep(5 * (attempt + 1))

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(one, todo))
    rows = [json.loads(l) for l in out_path.read_text().splitlines() if l.strip()]
    print(f"완료: 수리 {len(rows)} 중 통과 {sum(r['ok'] for r in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
